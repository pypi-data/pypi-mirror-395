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
    jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCaseMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "steps": "steps",
        "tags": "tags",
    },
)
class CfnTestCaseMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        steps: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTestCasePropsMixin.StepProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnTestCasePropsMixin.

        :param description: The description of the test case.
        :param name: The name of the test case.
        :param steps: The steps in the test case.
        :param tags: The specified tags of the test case.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apptest-testcase.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
            
            cfn_test_case_mixin_props = apptest_mixins.CfnTestCaseMixinProps(
                description="description",
                name="name",
                steps=[apptest_mixins.CfnTestCasePropsMixin.StepProperty(
                    action=apptest_mixins.CfnTestCasePropsMixin.StepActionProperty(
                        compare_action=apptest_mixins.CfnTestCasePropsMixin.CompareActionProperty(
                            input=apptest_mixins.CfnTestCasePropsMixin.InputProperty(
                                file=apptest_mixins.CfnTestCasePropsMixin.InputFileProperty(
                                    file_metadata=apptest_mixins.CfnTestCasePropsMixin.FileMetadataProperty(
                                        database_cdc=apptest_mixins.CfnTestCasePropsMixin.DatabaseCDCProperty(
                                            source_metadata=apptest_mixins.CfnTestCasePropsMixin.SourceDatabaseMetadataProperty(
                                                capture_tool="captureTool",
                                                type="type"
                                            ),
                                            target_metadata=apptest_mixins.CfnTestCasePropsMixin.TargetDatabaseMetadataProperty(
                                                capture_tool="captureTool",
                                                type="type"
                                            )
                                        ),
                                        data_sets=[apptest_mixins.CfnTestCasePropsMixin.DataSetProperty(
                                            ccsid="ccsid",
                                            format="format",
                                            length=123,
                                            name="name",
                                            type="type"
                                        )]
                                    ),
                                    source_location="sourceLocation",
                                    target_location="targetLocation"
                                )
                            ),
                            output=apptest_mixins.CfnTestCasePropsMixin.OutputProperty(
                                file=apptest_mixins.CfnTestCasePropsMixin.OutputFileProperty(
                                    file_location="fileLocation"
                                )
                            )
                        ),
                        mainframe_action=apptest_mixins.CfnTestCasePropsMixin.MainframeActionProperty(
                            action_type=apptest_mixins.CfnTestCasePropsMixin.MainframeActionTypeProperty(
                                batch=apptest_mixins.CfnTestCasePropsMixin.BatchProperty(
                                    batch_job_name="batchJobName",
                                    batch_job_parameters={
                                        "batch_job_parameters_key": "batchJobParameters"
                                    },
                                    export_data_set_names=["exportDataSetNames"]
                                ),
                                tn3270=apptest_mixins.CfnTestCasePropsMixin.TN3270Property(
                                    export_data_set_names=["exportDataSetNames"],
                                    script=apptest_mixins.CfnTestCasePropsMixin.ScriptProperty(
                                        script_location="scriptLocation",
                                        type="type"
                                    )
                                )
                            ),
                            properties=apptest_mixins.CfnTestCasePropsMixin.MainframeActionPropertiesProperty(
                                dms_task_arn="dmsTaskArn"
                            ),
                            resource="resource"
                        ),
                        resource_action=apptest_mixins.CfnTestCasePropsMixin.ResourceActionProperty(
                            cloud_formation_action=apptest_mixins.CfnTestCasePropsMixin.CloudFormationActionProperty(
                                action_type="actionType",
                                resource="resource"
                            ),
                            m2_managed_application_action=apptest_mixins.CfnTestCasePropsMixin.M2ManagedApplicationActionProperty(
                                action_type="actionType",
                                properties=apptest_mixins.CfnTestCasePropsMixin.M2ManagedActionPropertiesProperty(
                                    force_stop=False,
                                    import_data_set_location="importDataSetLocation"
                                ),
                                resource="resource"
                            ),
                            m2_non_managed_application_action=apptest_mixins.CfnTestCasePropsMixin.M2NonManagedApplicationActionProperty(
                                action_type="actionType",
                                resource="resource"
                            )
                        )
                    ),
                    description="description",
                    name="name"
                )],
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ded8d520283d97bd0a24f1fbf7b3ee13ded205256ce23df2aa9251d070bfc33)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument steps", value=steps, expected_type=type_hints["steps"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if steps is not None:
            self._values["steps"] = steps
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the test case.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apptest-testcase.html#cfn-apptest-testcase-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the test case.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apptest-testcase.html#cfn-apptest-testcase-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def steps(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.StepProperty"]]]]:
        '''The steps in the test case.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apptest-testcase.html#cfn-apptest-testcase-steps
        '''
        result = self._values.get("steps")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.StepProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The specified tags of the test case.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apptest-testcase.html#cfn-apptest-testcase-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTestCaseMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTestCasePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin",
):
    '''Creates a test case for an application.

    For more information about test cases, see `Test cases <https://docs.aws.amazon.com/m2/latest/userguide/testing-test-cases.html>`_ and `Application Testing concepts <https://docs.aws.amazon.com/m2/latest/userguide/concepts-apptest.html>`_ in the *AWS Mainframe Modernization User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apptest-testcase.html
    :cloudformationResource: AWS::AppTest::TestCase
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
        
        cfn_test_case_props_mixin = apptest_mixins.CfnTestCasePropsMixin(apptest_mixins.CfnTestCaseMixinProps(
            description="description",
            name="name",
            steps=[apptest_mixins.CfnTestCasePropsMixin.StepProperty(
                action=apptest_mixins.CfnTestCasePropsMixin.StepActionProperty(
                    compare_action=apptest_mixins.CfnTestCasePropsMixin.CompareActionProperty(
                        input=apptest_mixins.CfnTestCasePropsMixin.InputProperty(
                            file=apptest_mixins.CfnTestCasePropsMixin.InputFileProperty(
                                file_metadata=apptest_mixins.CfnTestCasePropsMixin.FileMetadataProperty(
                                    database_cdc=apptest_mixins.CfnTestCasePropsMixin.DatabaseCDCProperty(
                                        source_metadata=apptest_mixins.CfnTestCasePropsMixin.SourceDatabaseMetadataProperty(
                                            capture_tool="captureTool",
                                            type="type"
                                        ),
                                        target_metadata=apptest_mixins.CfnTestCasePropsMixin.TargetDatabaseMetadataProperty(
                                            capture_tool="captureTool",
                                            type="type"
                                        )
                                    ),
                                    data_sets=[apptest_mixins.CfnTestCasePropsMixin.DataSetProperty(
                                        ccsid="ccsid",
                                        format="format",
                                        length=123,
                                        name="name",
                                        type="type"
                                    )]
                                ),
                                source_location="sourceLocation",
                                target_location="targetLocation"
                            )
                        ),
                        output=apptest_mixins.CfnTestCasePropsMixin.OutputProperty(
                            file=apptest_mixins.CfnTestCasePropsMixin.OutputFileProperty(
                                file_location="fileLocation"
                            )
                        )
                    ),
                    mainframe_action=apptest_mixins.CfnTestCasePropsMixin.MainframeActionProperty(
                        action_type=apptest_mixins.CfnTestCasePropsMixin.MainframeActionTypeProperty(
                            batch=apptest_mixins.CfnTestCasePropsMixin.BatchProperty(
                                batch_job_name="batchJobName",
                                batch_job_parameters={
                                    "batch_job_parameters_key": "batchJobParameters"
                                },
                                export_data_set_names=["exportDataSetNames"]
                            ),
                            tn3270=apptest_mixins.CfnTestCasePropsMixin.TN3270Property(
                                export_data_set_names=["exportDataSetNames"],
                                script=apptest_mixins.CfnTestCasePropsMixin.ScriptProperty(
                                    script_location="scriptLocation",
                                    type="type"
                                )
                            )
                        ),
                        properties=apptest_mixins.CfnTestCasePropsMixin.MainframeActionPropertiesProperty(
                            dms_task_arn="dmsTaskArn"
                        ),
                        resource="resource"
                    ),
                    resource_action=apptest_mixins.CfnTestCasePropsMixin.ResourceActionProperty(
                        cloud_formation_action=apptest_mixins.CfnTestCasePropsMixin.CloudFormationActionProperty(
                            action_type="actionType",
                            resource="resource"
                        ),
                        m2_managed_application_action=apptest_mixins.CfnTestCasePropsMixin.M2ManagedApplicationActionProperty(
                            action_type="actionType",
                            properties=apptest_mixins.CfnTestCasePropsMixin.M2ManagedActionPropertiesProperty(
                                force_stop=False,
                                import_data_set_location="importDataSetLocation"
                            ),
                            resource="resource"
                        ),
                        m2_non_managed_application_action=apptest_mixins.CfnTestCasePropsMixin.M2NonManagedApplicationActionProperty(
                            action_type="actionType",
                            resource="resource"
                        )
                    )
                ),
                description="description",
                name="name"
            )],
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTestCaseMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppTest::TestCase``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea107efdd2b85ba1845f882331d30a1394ecf4af7f0caa080d3760e2ed23bcf0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2355fbfb1c1a03626247c36393e4e6ec71570453c2b3f9e4e7716ee0b3535fb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60202a81d1adbb46ae9657fa260dfab58d5a2a9b4d456efb23512c0403004782)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTestCaseMixinProps:
        return typing.cast(CfnTestCaseMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin.BatchProperty",
        jsii_struct_bases=[],
        name_mapping={
            "batch_job_name": "batchJobName",
            "batch_job_parameters": "batchJobParameters",
            "export_data_set_names": "exportDataSetNames",
        },
    )
    class BatchProperty:
        def __init__(
            self,
            *,
            batch_job_name: typing.Optional[builtins.str] = None,
            batch_job_parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            export_data_set_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Defines a batch.

            :param batch_job_name: The job name of the batch.
            :param batch_job_parameters: The batch job parameters of the batch.
            :param export_data_set_names: The export data set names of the batch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-batch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
                
                batch_property = apptest_mixins.CfnTestCasePropsMixin.BatchProperty(
                    batch_job_name="batchJobName",
                    batch_job_parameters={
                        "batch_job_parameters_key": "batchJobParameters"
                    },
                    export_data_set_names=["exportDataSetNames"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__481ecda2ba4c8bcc7a614f36e31e0507506cf71504b623ba07e941df5ee132f6)
                check_type(argname="argument batch_job_name", value=batch_job_name, expected_type=type_hints["batch_job_name"])
                check_type(argname="argument batch_job_parameters", value=batch_job_parameters, expected_type=type_hints["batch_job_parameters"])
                check_type(argname="argument export_data_set_names", value=export_data_set_names, expected_type=type_hints["export_data_set_names"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if batch_job_name is not None:
                self._values["batch_job_name"] = batch_job_name
            if batch_job_parameters is not None:
                self._values["batch_job_parameters"] = batch_job_parameters
            if export_data_set_names is not None:
                self._values["export_data_set_names"] = export_data_set_names

        @builtins.property
        def batch_job_name(self) -> typing.Optional[builtins.str]:
            '''The job name of the batch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-batch.html#cfn-apptest-testcase-batch-batchjobname
            '''
            result = self._values.get("batch_job_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def batch_job_parameters(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The batch job parameters of the batch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-batch.html#cfn-apptest-testcase-batch-batchjobparameters
            '''
            result = self._values.get("batch_job_parameters")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def export_data_set_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The export data set names of the batch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-batch.html#cfn-apptest-testcase-batch-exportdatasetnames
            '''
            result = self._values.get("export_data_set_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin.CloudFormationActionProperty",
        jsii_struct_bases=[],
        name_mapping={"action_type": "actionType", "resource": "resource"},
    )
    class CloudFormationActionProperty:
        def __init__(
            self,
            *,
            action_type: typing.Optional[builtins.str] = None,
            resource: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the CloudFormation action.

            :param action_type: The action type of the CloudFormation action.
            :param resource: The resource of the CloudFormation action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-cloudformationaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
                
                cloud_formation_action_property = apptest_mixins.CfnTestCasePropsMixin.CloudFormationActionProperty(
                    action_type="actionType",
                    resource="resource"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__507908a4c65372443e0c8e4246fbec98f80d054bae5b300dd5881ac01ac40990)
                check_type(argname="argument action_type", value=action_type, expected_type=type_hints["action_type"])
                check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action_type is not None:
                self._values["action_type"] = action_type
            if resource is not None:
                self._values["resource"] = resource

        @builtins.property
        def action_type(self) -> typing.Optional[builtins.str]:
            '''The action type of the CloudFormation action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-cloudformationaction.html#cfn-apptest-testcase-cloudformationaction-actiontype
            '''
            result = self._values.get("action_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource(self) -> typing.Optional[builtins.str]:
            '''The resource of the CloudFormation action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-cloudformationaction.html#cfn-apptest-testcase-cloudformationaction-resource
            '''
            result = self._values.get("resource")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudFormationActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin.CompareActionProperty",
        jsii_struct_bases=[],
        name_mapping={"input": "input", "output": "output"},
    )
    class CompareActionProperty:
        def __init__(
            self,
            *,
            input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTestCasePropsMixin.InputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            output: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTestCasePropsMixin.OutputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Compares the action.

            :param input: The input of the compare action.
            :param output: The output of the compare action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-compareaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
                
                compare_action_property = apptest_mixins.CfnTestCasePropsMixin.CompareActionProperty(
                    input=apptest_mixins.CfnTestCasePropsMixin.InputProperty(
                        file=apptest_mixins.CfnTestCasePropsMixin.InputFileProperty(
                            file_metadata=apptest_mixins.CfnTestCasePropsMixin.FileMetadataProperty(
                                database_cdc=apptest_mixins.CfnTestCasePropsMixin.DatabaseCDCProperty(
                                    source_metadata=apptest_mixins.CfnTestCasePropsMixin.SourceDatabaseMetadataProperty(
                                        capture_tool="captureTool",
                                        type="type"
                                    ),
                                    target_metadata=apptest_mixins.CfnTestCasePropsMixin.TargetDatabaseMetadataProperty(
                                        capture_tool="captureTool",
                                        type="type"
                                    )
                                ),
                                data_sets=[apptest_mixins.CfnTestCasePropsMixin.DataSetProperty(
                                    ccsid="ccsid",
                                    format="format",
                                    length=123,
                                    name="name",
                                    type="type"
                                )]
                            ),
                            source_location="sourceLocation",
                            target_location="targetLocation"
                        )
                    ),
                    output=apptest_mixins.CfnTestCasePropsMixin.OutputProperty(
                        file=apptest_mixins.CfnTestCasePropsMixin.OutputFileProperty(
                            file_location="fileLocation"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__41991261f52553328563584b5c07a061be1e472c0f1b6ed63d2264ccd14730d1)
                check_type(argname="argument input", value=input, expected_type=type_hints["input"])
                check_type(argname="argument output", value=output, expected_type=type_hints["output"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if input is not None:
                self._values["input"] = input
            if output is not None:
                self._values["output"] = output

        @builtins.property
        def input(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.InputProperty"]]:
            '''The input of the compare action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-compareaction.html#cfn-apptest-testcase-compareaction-input
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.InputProperty"]], result)

        @builtins.property
        def output(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.OutputProperty"]]:
            '''The output of the compare action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-compareaction.html#cfn-apptest-testcase-compareaction-output
            '''
            result = self._values.get("output")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.OutputProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CompareActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin.DataSetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ccsid": "ccsid",
            "format": "format",
            "length": "length",
            "name": "name",
            "type": "type",
        },
    )
    class DataSetProperty:
        def __init__(
            self,
            *,
            ccsid: typing.Optional[builtins.str] = None,
            format: typing.Optional[builtins.str] = None,
            length: typing.Optional[jsii.Number] = None,
            name: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines a data set.

            :param ccsid: The CCSID of the data set.
            :param format: The format of the data set.
            :param length: The length of the data set.
            :param name: The name of the data set.
            :param type: The type of the data set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-dataset.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
                
                data_set_property = apptest_mixins.CfnTestCasePropsMixin.DataSetProperty(
                    ccsid="ccsid",
                    format="format",
                    length=123,
                    name="name",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a7bd476b45d6f3681dc405f70f3a7daf6de456e6fbc729f068e684b608b88807)
                check_type(argname="argument ccsid", value=ccsid, expected_type=type_hints["ccsid"])
                check_type(argname="argument format", value=format, expected_type=type_hints["format"])
                check_type(argname="argument length", value=length, expected_type=type_hints["length"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ccsid is not None:
                self._values["ccsid"] = ccsid
            if format is not None:
                self._values["format"] = format
            if length is not None:
                self._values["length"] = length
            if name is not None:
                self._values["name"] = name
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def ccsid(self) -> typing.Optional[builtins.str]:
            '''The CCSID of the data set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-dataset.html#cfn-apptest-testcase-dataset-ccsid
            '''
            result = self._values.get("ccsid")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def format(self) -> typing.Optional[builtins.str]:
            '''The format of the data set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-dataset.html#cfn-apptest-testcase-dataset-format
            '''
            result = self._values.get("format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def length(self) -> typing.Optional[jsii.Number]:
            '''The length of the data set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-dataset.html#cfn-apptest-testcase-dataset-length
            '''
            result = self._values.get("length")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the data set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-dataset.html#cfn-apptest-testcase-dataset-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of the data set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-dataset.html#cfn-apptest-testcase-dataset-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataSetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin.DatabaseCDCProperty",
        jsii_struct_bases=[],
        name_mapping={
            "source_metadata": "sourceMetadata",
            "target_metadata": "targetMetadata",
        },
    )
    class DatabaseCDCProperty:
        def __init__(
            self,
            *,
            source_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTestCasePropsMixin.SourceDatabaseMetadataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            target_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTestCasePropsMixin.TargetDatabaseMetadataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Defines the Change Data Capture (CDC) of the database.

            :param source_metadata: The source metadata of the database CDC.
            :param target_metadata: The target metadata of the database CDC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-databasecdc.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
                
                database_cDCProperty = apptest_mixins.CfnTestCasePropsMixin.DatabaseCDCProperty(
                    source_metadata=apptest_mixins.CfnTestCasePropsMixin.SourceDatabaseMetadataProperty(
                        capture_tool="captureTool",
                        type="type"
                    ),
                    target_metadata=apptest_mixins.CfnTestCasePropsMixin.TargetDatabaseMetadataProperty(
                        capture_tool="captureTool",
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fc061f3f8f82ee3909d53e0b6a02ac46c7e7657b20df03104e2d1482d7bab72d)
                check_type(argname="argument source_metadata", value=source_metadata, expected_type=type_hints["source_metadata"])
                check_type(argname="argument target_metadata", value=target_metadata, expected_type=type_hints["target_metadata"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source_metadata is not None:
                self._values["source_metadata"] = source_metadata
            if target_metadata is not None:
                self._values["target_metadata"] = target_metadata

        @builtins.property
        def source_metadata(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.SourceDatabaseMetadataProperty"]]:
            '''The source metadata of the database CDC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-databasecdc.html#cfn-apptest-testcase-databasecdc-sourcemetadata
            '''
            result = self._values.get("source_metadata")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.SourceDatabaseMetadataProperty"]], result)

        @builtins.property
        def target_metadata(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.TargetDatabaseMetadataProperty"]]:
            '''The target metadata of the database CDC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-databasecdc.html#cfn-apptest-testcase-databasecdc-targetmetadata
            '''
            result = self._values.get("target_metadata")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.TargetDatabaseMetadataProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatabaseCDCProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin.FileMetadataProperty",
        jsii_struct_bases=[],
        name_mapping={"database_cdc": "databaseCdc", "data_sets": "dataSets"},
    )
    class FileMetadataProperty:
        def __init__(
            self,
            *,
            database_cdc: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTestCasePropsMixin.DatabaseCDCProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            data_sets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTestCasePropsMixin.DataSetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies a file metadata.

            :param database_cdc: The database CDC of the file metadata.
            :param data_sets: The data sets of the file metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-filemetadata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
                
                file_metadata_property = apptest_mixins.CfnTestCasePropsMixin.FileMetadataProperty(
                    database_cdc=apptest_mixins.CfnTestCasePropsMixin.DatabaseCDCProperty(
                        source_metadata=apptest_mixins.CfnTestCasePropsMixin.SourceDatabaseMetadataProperty(
                            capture_tool="captureTool",
                            type="type"
                        ),
                        target_metadata=apptest_mixins.CfnTestCasePropsMixin.TargetDatabaseMetadataProperty(
                            capture_tool="captureTool",
                            type="type"
                        )
                    ),
                    data_sets=[apptest_mixins.CfnTestCasePropsMixin.DataSetProperty(
                        ccsid="ccsid",
                        format="format",
                        length=123,
                        name="name",
                        type="type"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__02dbca42e7f25c3b6c450944aa6c63ecd0002fbb3a5f4003c5051146f4b3d047)
                check_type(argname="argument database_cdc", value=database_cdc, expected_type=type_hints["database_cdc"])
                check_type(argname="argument data_sets", value=data_sets, expected_type=type_hints["data_sets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if database_cdc is not None:
                self._values["database_cdc"] = database_cdc
            if data_sets is not None:
                self._values["data_sets"] = data_sets

        @builtins.property
        def database_cdc(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.DatabaseCDCProperty"]]:
            '''The database CDC of the file metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-filemetadata.html#cfn-apptest-testcase-filemetadata-databasecdc
            '''
            result = self._values.get("database_cdc")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.DatabaseCDCProperty"]], result)

        @builtins.property
        def data_sets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.DataSetProperty"]]]]:
            '''The data sets of the file metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-filemetadata.html#cfn-apptest-testcase-filemetadata-datasets
            '''
            result = self._values.get("data_sets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.DataSetProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FileMetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin.InputFileProperty",
        jsii_struct_bases=[],
        name_mapping={
            "file_metadata": "fileMetadata",
            "source_location": "sourceLocation",
            "target_location": "targetLocation",
        },
    )
    class InputFileProperty:
        def __init__(
            self,
            *,
            file_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTestCasePropsMixin.FileMetadataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            source_location: typing.Optional[builtins.str] = None,
            target_location: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the input file.

            :param file_metadata: The file metadata of the input file.
            :param source_location: The source location of the input file.
            :param target_location: The target location of the input file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-inputfile.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
                
                input_file_property = apptest_mixins.CfnTestCasePropsMixin.InputFileProperty(
                    file_metadata=apptest_mixins.CfnTestCasePropsMixin.FileMetadataProperty(
                        database_cdc=apptest_mixins.CfnTestCasePropsMixin.DatabaseCDCProperty(
                            source_metadata=apptest_mixins.CfnTestCasePropsMixin.SourceDatabaseMetadataProperty(
                                capture_tool="captureTool",
                                type="type"
                            ),
                            target_metadata=apptest_mixins.CfnTestCasePropsMixin.TargetDatabaseMetadataProperty(
                                capture_tool="captureTool",
                                type="type"
                            )
                        ),
                        data_sets=[apptest_mixins.CfnTestCasePropsMixin.DataSetProperty(
                            ccsid="ccsid",
                            format="format",
                            length=123,
                            name="name",
                            type="type"
                        )]
                    ),
                    source_location="sourceLocation",
                    target_location="targetLocation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a6cf3eca24c2e90878e4235206c622f1d8ca0afb16b20f300fc2a495caf72992)
                check_type(argname="argument file_metadata", value=file_metadata, expected_type=type_hints["file_metadata"])
                check_type(argname="argument source_location", value=source_location, expected_type=type_hints["source_location"])
                check_type(argname="argument target_location", value=target_location, expected_type=type_hints["target_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if file_metadata is not None:
                self._values["file_metadata"] = file_metadata
            if source_location is not None:
                self._values["source_location"] = source_location
            if target_location is not None:
                self._values["target_location"] = target_location

        @builtins.property
        def file_metadata(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.FileMetadataProperty"]]:
            '''The file metadata of the input file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-inputfile.html#cfn-apptest-testcase-inputfile-filemetadata
            '''
            result = self._values.get("file_metadata")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.FileMetadataProperty"]], result)

        @builtins.property
        def source_location(self) -> typing.Optional[builtins.str]:
            '''The source location of the input file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-inputfile.html#cfn-apptest-testcase-inputfile-sourcelocation
            '''
            result = self._values.get("source_location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_location(self) -> typing.Optional[builtins.str]:
            '''The target location of the input file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-inputfile.html#cfn-apptest-testcase-inputfile-targetlocation
            '''
            result = self._values.get("target_location")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputFileProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin.InputProperty",
        jsii_struct_bases=[],
        name_mapping={"file": "file"},
    )
    class InputProperty:
        def __init__(
            self,
            *,
            file: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTestCasePropsMixin.InputFileProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the input.

            :param file: The file in the input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-input.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
                
                input_property = apptest_mixins.CfnTestCasePropsMixin.InputProperty(
                    file=apptest_mixins.CfnTestCasePropsMixin.InputFileProperty(
                        file_metadata=apptest_mixins.CfnTestCasePropsMixin.FileMetadataProperty(
                            database_cdc=apptest_mixins.CfnTestCasePropsMixin.DatabaseCDCProperty(
                                source_metadata=apptest_mixins.CfnTestCasePropsMixin.SourceDatabaseMetadataProperty(
                                    capture_tool="captureTool",
                                    type="type"
                                ),
                                target_metadata=apptest_mixins.CfnTestCasePropsMixin.TargetDatabaseMetadataProperty(
                                    capture_tool="captureTool",
                                    type="type"
                                )
                            ),
                            data_sets=[apptest_mixins.CfnTestCasePropsMixin.DataSetProperty(
                                ccsid="ccsid",
                                format="format",
                                length=123,
                                name="name",
                                type="type"
                            )]
                        ),
                        source_location="sourceLocation",
                        target_location="targetLocation"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__445b776b20d6bba582861061125bb9ce60ab4fe629747862dbe4a23f3869278a)
                check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if file is not None:
                self._values["file"] = file

        @builtins.property
        def file(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.InputFileProperty"]]:
            '''The file in the input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-input.html#cfn-apptest-testcase-input-file
            '''
            result = self._values.get("file")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.InputFileProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin.M2ManagedActionPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "force_stop": "forceStop",
            "import_data_set_location": "importDataSetLocation",
        },
    )
    class M2ManagedActionPropertiesProperty:
        def __init__(
            self,
            *,
            force_stop: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            import_data_set_location: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the Mainframe Modernization managed action properties.

            :param force_stop: Force stops the Mainframe Modernization managed action properties.
            :param import_data_set_location: The import data set location of the Mainframe Modernization managed action properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-m2managedactionproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
                
                m2_managed_action_properties_property = apptest_mixins.CfnTestCasePropsMixin.M2ManagedActionPropertiesProperty(
                    force_stop=False,
                    import_data_set_location="importDataSetLocation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__20d17eef27087a50d016bffef379b134b971fdbd8ad2462c57188e223f64c78d)
                check_type(argname="argument force_stop", value=force_stop, expected_type=type_hints["force_stop"])
                check_type(argname="argument import_data_set_location", value=import_data_set_location, expected_type=type_hints["import_data_set_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if force_stop is not None:
                self._values["force_stop"] = force_stop
            if import_data_set_location is not None:
                self._values["import_data_set_location"] = import_data_set_location

        @builtins.property
        def force_stop(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Force stops the Mainframe Modernization managed action properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-m2managedactionproperties.html#cfn-apptest-testcase-m2managedactionproperties-forcestop
            '''
            result = self._values.get("force_stop")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def import_data_set_location(self) -> typing.Optional[builtins.str]:
            '''The import data set location of the Mainframe Modernization managed action properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-m2managedactionproperties.html#cfn-apptest-testcase-m2managedactionproperties-importdatasetlocation
            '''
            result = self._values.get("import_data_set_location")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "M2ManagedActionPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin.M2ManagedApplicationActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_type": "actionType",
            "properties": "properties",
            "resource": "resource",
        },
    )
    class M2ManagedApplicationActionProperty:
        def __init__(
            self,
            *,
            action_type: typing.Optional[builtins.str] = None,
            properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTestCasePropsMixin.M2ManagedActionPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resource: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the Mainframe Modernization managed application action.

            :param action_type: The action type of the Mainframe Modernization managed application action.
            :param properties: The properties of the Mainframe Modernization managed application action.
            :param resource: The resource of the Mainframe Modernization managed application action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-m2managedapplicationaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
                
                m2_managed_application_action_property = apptest_mixins.CfnTestCasePropsMixin.M2ManagedApplicationActionProperty(
                    action_type="actionType",
                    properties=apptest_mixins.CfnTestCasePropsMixin.M2ManagedActionPropertiesProperty(
                        force_stop=False,
                        import_data_set_location="importDataSetLocation"
                    ),
                    resource="resource"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__22b4257fe855fcb5b600d998d69859c81fad99ffab6efd0c0b368f4fccbe4091)
                check_type(argname="argument action_type", value=action_type, expected_type=type_hints["action_type"])
                check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
                check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action_type is not None:
                self._values["action_type"] = action_type
            if properties is not None:
                self._values["properties"] = properties
            if resource is not None:
                self._values["resource"] = resource

        @builtins.property
        def action_type(self) -> typing.Optional[builtins.str]:
            '''The action type of the Mainframe Modernization managed application action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-m2managedapplicationaction.html#cfn-apptest-testcase-m2managedapplicationaction-actiontype
            '''
            result = self._values.get("action_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.M2ManagedActionPropertiesProperty"]]:
            '''The properties of the Mainframe Modernization managed application action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-m2managedapplicationaction.html#cfn-apptest-testcase-m2managedapplicationaction-properties
            '''
            result = self._values.get("properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.M2ManagedActionPropertiesProperty"]], result)

        @builtins.property
        def resource(self) -> typing.Optional[builtins.str]:
            '''The resource of the Mainframe Modernization managed application action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-m2managedapplicationaction.html#cfn-apptest-testcase-m2managedapplicationaction-resource
            '''
            result = self._values.get("resource")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "M2ManagedApplicationActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin.M2NonManagedApplicationActionProperty",
        jsii_struct_bases=[],
        name_mapping={"action_type": "actionType", "resource": "resource"},
    )
    class M2NonManagedApplicationActionProperty:
        def __init__(
            self,
            *,
            action_type: typing.Optional[builtins.str] = None,
            resource: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the Mainframe Modernization non-managed application action.

            :param action_type: The action type of the Mainframe Modernization non-managed application action.
            :param resource: The resource of the Mainframe Modernization non-managed application action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-m2nonmanagedapplicationaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
                
                m2_non_managed_application_action_property = apptest_mixins.CfnTestCasePropsMixin.M2NonManagedApplicationActionProperty(
                    action_type="actionType",
                    resource="resource"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__961bec98e59ff4405adde66de375138fda8a0390464d790bc71745ead022a121)
                check_type(argname="argument action_type", value=action_type, expected_type=type_hints["action_type"])
                check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action_type is not None:
                self._values["action_type"] = action_type
            if resource is not None:
                self._values["resource"] = resource

        @builtins.property
        def action_type(self) -> typing.Optional[builtins.str]:
            '''The action type of the Mainframe Modernization non-managed application action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-m2nonmanagedapplicationaction.html#cfn-apptest-testcase-m2nonmanagedapplicationaction-actiontype
            '''
            result = self._values.get("action_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource(self) -> typing.Optional[builtins.str]:
            '''The resource of the Mainframe Modernization non-managed application action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-m2nonmanagedapplicationaction.html#cfn-apptest-testcase-m2nonmanagedapplicationaction-resource
            '''
            result = self._values.get("resource")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "M2NonManagedApplicationActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin.MainframeActionPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"dms_task_arn": "dmsTaskArn"},
    )
    class MainframeActionPropertiesProperty:
        def __init__(
            self,
            *,
            dms_task_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the mainframe action properties.

            :param dms_task_arn: The DMS task ARN of the mainframe action properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-mainframeactionproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
                
                mainframe_action_properties_property = apptest_mixins.CfnTestCasePropsMixin.MainframeActionPropertiesProperty(
                    dms_task_arn="dmsTaskArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__92cfd92adeef1398833ad57becb97a89f6c58caf9c36b766b592067fe22007a3)
                check_type(argname="argument dms_task_arn", value=dms_task_arn, expected_type=type_hints["dms_task_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dms_task_arn is not None:
                self._values["dms_task_arn"] = dms_task_arn

        @builtins.property
        def dms_task_arn(self) -> typing.Optional[builtins.str]:
            '''The DMS task ARN of the mainframe action properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-mainframeactionproperties.html#cfn-apptest-testcase-mainframeactionproperties-dmstaskarn
            '''
            result = self._values.get("dms_task_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MainframeActionPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin.MainframeActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_type": "actionType",
            "properties": "properties",
            "resource": "resource",
        },
    )
    class MainframeActionProperty:
        def __init__(
            self,
            *,
            action_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTestCasePropsMixin.MainframeActionTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTestCasePropsMixin.MainframeActionPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resource: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the mainframe action.

            :param action_type: The action type of the mainframe action.
            :param properties: The properties of the mainframe action.
            :param resource: The resource of the mainframe action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-mainframeaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
                
                mainframe_action_property = apptest_mixins.CfnTestCasePropsMixin.MainframeActionProperty(
                    action_type=apptest_mixins.CfnTestCasePropsMixin.MainframeActionTypeProperty(
                        batch=apptest_mixins.CfnTestCasePropsMixin.BatchProperty(
                            batch_job_name="batchJobName",
                            batch_job_parameters={
                                "batch_job_parameters_key": "batchJobParameters"
                            },
                            export_data_set_names=["exportDataSetNames"]
                        ),
                        tn3270=apptest_mixins.CfnTestCasePropsMixin.TN3270Property(
                            export_data_set_names=["exportDataSetNames"],
                            script=apptest_mixins.CfnTestCasePropsMixin.ScriptProperty(
                                script_location="scriptLocation",
                                type="type"
                            )
                        )
                    ),
                    properties=apptest_mixins.CfnTestCasePropsMixin.MainframeActionPropertiesProperty(
                        dms_task_arn="dmsTaskArn"
                    ),
                    resource="resource"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__db1027de5a730fa61c60a560d91cd94e75faa574eb546f4440140a8e2baddd3d)
                check_type(argname="argument action_type", value=action_type, expected_type=type_hints["action_type"])
                check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
                check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action_type is not None:
                self._values["action_type"] = action_type
            if properties is not None:
                self._values["properties"] = properties
            if resource is not None:
                self._values["resource"] = resource

        @builtins.property
        def action_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.MainframeActionTypeProperty"]]:
            '''The action type of the mainframe action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-mainframeaction.html#cfn-apptest-testcase-mainframeaction-actiontype
            '''
            result = self._values.get("action_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.MainframeActionTypeProperty"]], result)

        @builtins.property
        def properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.MainframeActionPropertiesProperty"]]:
            '''The properties of the mainframe action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-mainframeaction.html#cfn-apptest-testcase-mainframeaction-properties
            '''
            result = self._values.get("properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.MainframeActionPropertiesProperty"]], result)

        @builtins.property
        def resource(self) -> typing.Optional[builtins.str]:
            '''The resource of the mainframe action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-mainframeaction.html#cfn-apptest-testcase-mainframeaction-resource
            '''
            result = self._values.get("resource")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MainframeActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin.MainframeActionTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"batch": "batch", "tn3270": "tn3270"},
    )
    class MainframeActionTypeProperty:
        def __init__(
            self,
            *,
            batch: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTestCasePropsMixin.BatchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            tn3270: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTestCasePropsMixin.TN3270Property", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the mainframe action type.

            :param batch: The batch of the mainframe action type.
            :param tn3270: The tn3270 port of the mainframe action type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-mainframeactiontype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
                
                mainframe_action_type_property = apptest_mixins.CfnTestCasePropsMixin.MainframeActionTypeProperty(
                    batch=apptest_mixins.CfnTestCasePropsMixin.BatchProperty(
                        batch_job_name="batchJobName",
                        batch_job_parameters={
                            "batch_job_parameters_key": "batchJobParameters"
                        },
                        export_data_set_names=["exportDataSetNames"]
                    ),
                    tn3270=apptest_mixins.CfnTestCasePropsMixin.TN3270Property(
                        export_data_set_names=["exportDataSetNames"],
                        script=apptest_mixins.CfnTestCasePropsMixin.ScriptProperty(
                            script_location="scriptLocation",
                            type="type"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__80572a381d7b0623b3aac68aae352a719226ce65ec890b4042d3064199c8a538)
                check_type(argname="argument batch", value=batch, expected_type=type_hints["batch"])
                check_type(argname="argument tn3270", value=tn3270, expected_type=type_hints["tn3270"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if batch is not None:
                self._values["batch"] = batch
            if tn3270 is not None:
                self._values["tn3270"] = tn3270

        @builtins.property
        def batch(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.BatchProperty"]]:
            '''The batch of the mainframe action type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-mainframeactiontype.html#cfn-apptest-testcase-mainframeactiontype-batch
            '''
            result = self._values.get("batch")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.BatchProperty"]], result)

        @builtins.property
        def tn3270(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.TN3270Property"]]:
            '''The tn3270 port of the mainframe action type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-mainframeactiontype.html#cfn-apptest-testcase-mainframeactiontype-tn3270
            '''
            result = self._values.get("tn3270")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.TN3270Property"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MainframeActionTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin.OutputFileProperty",
        jsii_struct_bases=[],
        name_mapping={"file_location": "fileLocation"},
    )
    class OutputFileProperty:
        def __init__(
            self,
            *,
            file_location: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an output file.

            :param file_location: The file location of the output file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-outputfile.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
                
                output_file_property = apptest_mixins.CfnTestCasePropsMixin.OutputFileProperty(
                    file_location="fileLocation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b34949df24bf28c34ed85aa7d19e004762b77fdfd24fe24b86f645e451e305f4)
                check_type(argname="argument file_location", value=file_location, expected_type=type_hints["file_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if file_location is not None:
                self._values["file_location"] = file_location

        @builtins.property
        def file_location(self) -> typing.Optional[builtins.str]:
            '''The file location of the output file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-outputfile.html#cfn-apptest-testcase-outputfile-filelocation
            '''
            result = self._values.get("file_location")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputFileProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin.OutputProperty",
        jsii_struct_bases=[],
        name_mapping={"file": "file"},
    )
    class OutputProperty:
        def __init__(
            self,
            *,
            file: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTestCasePropsMixin.OutputFileProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies an output.

            :param file: The file of the output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-output.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
                
                output_property = apptest_mixins.CfnTestCasePropsMixin.OutputProperty(
                    file=apptest_mixins.CfnTestCasePropsMixin.OutputFileProperty(
                        file_location="fileLocation"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__798c86cf68a04a1ee78acbe398fcc96d4badbcd05884a855ccb0fd58b66b5fd1)
                check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if file is not None:
                self._values["file"] = file

        @builtins.property
        def file(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.OutputFileProperty"]]:
            '''The file of the output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-output.html#cfn-apptest-testcase-output-file
            '''
            result = self._values.get("file")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.OutputFileProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin.ResourceActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_formation_action": "cloudFormationAction",
            "m2_managed_application_action": "m2ManagedApplicationAction",
            "m2_non_managed_application_action": "m2NonManagedApplicationAction",
        },
    )
    class ResourceActionProperty:
        def __init__(
            self,
            *,
            cloud_formation_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTestCasePropsMixin.CloudFormationActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            m2_managed_application_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTestCasePropsMixin.M2ManagedApplicationActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            m2_non_managed_application_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTestCasePropsMixin.M2NonManagedApplicationActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies a resource action.

            :param cloud_formation_action: The CloudFormation action of the resource action.
            :param m2_managed_application_action: The Mainframe Modernization managed application action of the resource action.
            :param m2_non_managed_application_action: The Mainframe Modernization non-managed application action of the resource action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-resourceaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
                
                resource_action_property = apptest_mixins.CfnTestCasePropsMixin.ResourceActionProperty(
                    cloud_formation_action=apptest_mixins.CfnTestCasePropsMixin.CloudFormationActionProperty(
                        action_type="actionType",
                        resource="resource"
                    ),
                    m2_managed_application_action=apptest_mixins.CfnTestCasePropsMixin.M2ManagedApplicationActionProperty(
                        action_type="actionType",
                        properties=apptest_mixins.CfnTestCasePropsMixin.M2ManagedActionPropertiesProperty(
                            force_stop=False,
                            import_data_set_location="importDataSetLocation"
                        ),
                        resource="resource"
                    ),
                    m2_non_managed_application_action=apptest_mixins.CfnTestCasePropsMixin.M2NonManagedApplicationActionProperty(
                        action_type="actionType",
                        resource="resource"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__df1aba57c9e80e09d1611d96db8c61824b1b8dfe91f96092019e45fbbba5e034)
                check_type(argname="argument cloud_formation_action", value=cloud_formation_action, expected_type=type_hints["cloud_formation_action"])
                check_type(argname="argument m2_managed_application_action", value=m2_managed_application_action, expected_type=type_hints["m2_managed_application_action"])
                check_type(argname="argument m2_non_managed_application_action", value=m2_non_managed_application_action, expected_type=type_hints["m2_non_managed_application_action"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_formation_action is not None:
                self._values["cloud_formation_action"] = cloud_formation_action
            if m2_managed_application_action is not None:
                self._values["m2_managed_application_action"] = m2_managed_application_action
            if m2_non_managed_application_action is not None:
                self._values["m2_non_managed_application_action"] = m2_non_managed_application_action

        @builtins.property
        def cloud_formation_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.CloudFormationActionProperty"]]:
            '''The CloudFormation action of the resource action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-resourceaction.html#cfn-apptest-testcase-resourceaction-cloudformationaction
            '''
            result = self._values.get("cloud_formation_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.CloudFormationActionProperty"]], result)

        @builtins.property
        def m2_managed_application_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.M2ManagedApplicationActionProperty"]]:
            '''The Mainframe Modernization managed application action of the resource action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-resourceaction.html#cfn-apptest-testcase-resourceaction-m2managedapplicationaction
            '''
            result = self._values.get("m2_managed_application_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.M2ManagedApplicationActionProperty"]], result)

        @builtins.property
        def m2_non_managed_application_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.M2NonManagedApplicationActionProperty"]]:
            '''The Mainframe Modernization non-managed application action of the resource action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-resourceaction.html#cfn-apptest-testcase-resourceaction-m2nonmanagedapplicationaction
            '''
            result = self._values.get("m2_non_managed_application_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.M2NonManagedApplicationActionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin.ScriptProperty",
        jsii_struct_bases=[],
        name_mapping={"script_location": "scriptLocation", "type": "type"},
    )
    class ScriptProperty:
        def __init__(
            self,
            *,
            script_location: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the script.

            :param script_location: The script location of the scripts.
            :param type: The type of the scripts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-script.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
                
                script_property = apptest_mixins.CfnTestCasePropsMixin.ScriptProperty(
                    script_location="scriptLocation",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4805a976e80b858c552ae5fc986ade07c1dac47d744ca1ac94f722bda95bec59)
                check_type(argname="argument script_location", value=script_location, expected_type=type_hints["script_location"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if script_location is not None:
                self._values["script_location"] = script_location
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def script_location(self) -> typing.Optional[builtins.str]:
            '''The script location of the scripts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-script.html#cfn-apptest-testcase-script-scriptlocation
            '''
            result = self._values.get("script_location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of the scripts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-script.html#cfn-apptest-testcase-script-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScriptProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin.SourceDatabaseMetadataProperty",
        jsii_struct_bases=[],
        name_mapping={"capture_tool": "captureTool", "type": "type"},
    )
    class SourceDatabaseMetadataProperty:
        def __init__(
            self,
            *,
            capture_tool: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the source database metadata.

            :param capture_tool: The capture tool of the source database metadata.
            :param type: The type of the source database metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-sourcedatabasemetadata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
                
                source_database_metadata_property = apptest_mixins.CfnTestCasePropsMixin.SourceDatabaseMetadataProperty(
                    capture_tool="captureTool",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0454dd540598f7afcaa1ac4d8e4d858a17aa41a3a6fcbc70401c4a3e351351d7)
                check_type(argname="argument capture_tool", value=capture_tool, expected_type=type_hints["capture_tool"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if capture_tool is not None:
                self._values["capture_tool"] = capture_tool
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def capture_tool(self) -> typing.Optional[builtins.str]:
            '''The capture tool of the source database metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-sourcedatabasemetadata.html#cfn-apptest-testcase-sourcedatabasemetadata-capturetool
            '''
            result = self._values.get("capture_tool")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of the source database metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-sourcedatabasemetadata.html#cfn-apptest-testcase-sourcedatabasemetadata-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceDatabaseMetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin.StepActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "compare_action": "compareAction",
            "mainframe_action": "mainframeAction",
            "resource_action": "resourceAction",
        },
    )
    class StepActionProperty:
        def __init__(
            self,
            *,
            compare_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTestCasePropsMixin.CompareActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            mainframe_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTestCasePropsMixin.MainframeActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resource_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTestCasePropsMixin.ResourceActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies a step action.

            :param compare_action: The compare action of the step action.
            :param mainframe_action: The mainframe action of the step action.
            :param resource_action: The resource action of the step action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-stepaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
                
                step_action_property = apptest_mixins.CfnTestCasePropsMixin.StepActionProperty(
                    compare_action=apptest_mixins.CfnTestCasePropsMixin.CompareActionProperty(
                        input=apptest_mixins.CfnTestCasePropsMixin.InputProperty(
                            file=apptest_mixins.CfnTestCasePropsMixin.InputFileProperty(
                                file_metadata=apptest_mixins.CfnTestCasePropsMixin.FileMetadataProperty(
                                    database_cdc=apptest_mixins.CfnTestCasePropsMixin.DatabaseCDCProperty(
                                        source_metadata=apptest_mixins.CfnTestCasePropsMixin.SourceDatabaseMetadataProperty(
                                            capture_tool="captureTool",
                                            type="type"
                                        ),
                                        target_metadata=apptest_mixins.CfnTestCasePropsMixin.TargetDatabaseMetadataProperty(
                                            capture_tool="captureTool",
                                            type="type"
                                        )
                                    ),
                                    data_sets=[apptest_mixins.CfnTestCasePropsMixin.DataSetProperty(
                                        ccsid="ccsid",
                                        format="format",
                                        length=123,
                                        name="name",
                                        type="type"
                                    )]
                                ),
                                source_location="sourceLocation",
                                target_location="targetLocation"
                            )
                        ),
                        output=apptest_mixins.CfnTestCasePropsMixin.OutputProperty(
                            file=apptest_mixins.CfnTestCasePropsMixin.OutputFileProperty(
                                file_location="fileLocation"
                            )
                        )
                    ),
                    mainframe_action=apptest_mixins.CfnTestCasePropsMixin.MainframeActionProperty(
                        action_type=apptest_mixins.CfnTestCasePropsMixin.MainframeActionTypeProperty(
                            batch=apptest_mixins.CfnTestCasePropsMixin.BatchProperty(
                                batch_job_name="batchJobName",
                                batch_job_parameters={
                                    "batch_job_parameters_key": "batchJobParameters"
                                },
                                export_data_set_names=["exportDataSetNames"]
                            ),
                            tn3270=apptest_mixins.CfnTestCasePropsMixin.TN3270Property(
                                export_data_set_names=["exportDataSetNames"],
                                script=apptest_mixins.CfnTestCasePropsMixin.ScriptProperty(
                                    script_location="scriptLocation",
                                    type="type"
                                )
                            )
                        ),
                        properties=apptest_mixins.CfnTestCasePropsMixin.MainframeActionPropertiesProperty(
                            dms_task_arn="dmsTaskArn"
                        ),
                        resource="resource"
                    ),
                    resource_action=apptest_mixins.CfnTestCasePropsMixin.ResourceActionProperty(
                        cloud_formation_action=apptest_mixins.CfnTestCasePropsMixin.CloudFormationActionProperty(
                            action_type="actionType",
                            resource="resource"
                        ),
                        m2_managed_application_action=apptest_mixins.CfnTestCasePropsMixin.M2ManagedApplicationActionProperty(
                            action_type="actionType",
                            properties=apptest_mixins.CfnTestCasePropsMixin.M2ManagedActionPropertiesProperty(
                                force_stop=False,
                                import_data_set_location="importDataSetLocation"
                            ),
                            resource="resource"
                        ),
                        m2_non_managed_application_action=apptest_mixins.CfnTestCasePropsMixin.M2NonManagedApplicationActionProperty(
                            action_type="actionType",
                            resource="resource"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7a0766788ddb686b0ffa08da7d98f21287379c7c4a582735ffc0fd29b9bcc161)
                check_type(argname="argument compare_action", value=compare_action, expected_type=type_hints["compare_action"])
                check_type(argname="argument mainframe_action", value=mainframe_action, expected_type=type_hints["mainframe_action"])
                check_type(argname="argument resource_action", value=resource_action, expected_type=type_hints["resource_action"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if compare_action is not None:
                self._values["compare_action"] = compare_action
            if mainframe_action is not None:
                self._values["mainframe_action"] = mainframe_action
            if resource_action is not None:
                self._values["resource_action"] = resource_action

        @builtins.property
        def compare_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.CompareActionProperty"]]:
            '''The compare action of the step action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-stepaction.html#cfn-apptest-testcase-stepaction-compareaction
            '''
            result = self._values.get("compare_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.CompareActionProperty"]], result)

        @builtins.property
        def mainframe_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.MainframeActionProperty"]]:
            '''The mainframe action of the step action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-stepaction.html#cfn-apptest-testcase-stepaction-mainframeaction
            '''
            result = self._values.get("mainframe_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.MainframeActionProperty"]], result)

        @builtins.property
        def resource_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.ResourceActionProperty"]]:
            '''The resource action of the step action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-stepaction.html#cfn-apptest-testcase-stepaction-resourceaction
            '''
            result = self._values.get("resource_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.ResourceActionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StepActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin.StepProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "description": "description",
            "name": "name",
        },
    )
    class StepProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTestCasePropsMixin.StepActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            description: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines a step.

            :param action: The action of the step.
            :param description: The description of the step.
            :param name: The name of the step.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-step.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
                
                step_property = apptest_mixins.CfnTestCasePropsMixin.StepProperty(
                    action=apptest_mixins.CfnTestCasePropsMixin.StepActionProperty(
                        compare_action=apptest_mixins.CfnTestCasePropsMixin.CompareActionProperty(
                            input=apptest_mixins.CfnTestCasePropsMixin.InputProperty(
                                file=apptest_mixins.CfnTestCasePropsMixin.InputFileProperty(
                                    file_metadata=apptest_mixins.CfnTestCasePropsMixin.FileMetadataProperty(
                                        database_cdc=apptest_mixins.CfnTestCasePropsMixin.DatabaseCDCProperty(
                                            source_metadata=apptest_mixins.CfnTestCasePropsMixin.SourceDatabaseMetadataProperty(
                                                capture_tool="captureTool",
                                                type="type"
                                            ),
                                            target_metadata=apptest_mixins.CfnTestCasePropsMixin.TargetDatabaseMetadataProperty(
                                                capture_tool="captureTool",
                                                type="type"
                                            )
                                        ),
                                        data_sets=[apptest_mixins.CfnTestCasePropsMixin.DataSetProperty(
                                            ccsid="ccsid",
                                            format="format",
                                            length=123,
                                            name="name",
                                            type="type"
                                        )]
                                    ),
                                    source_location="sourceLocation",
                                    target_location="targetLocation"
                                )
                            ),
                            output=apptest_mixins.CfnTestCasePropsMixin.OutputProperty(
                                file=apptest_mixins.CfnTestCasePropsMixin.OutputFileProperty(
                                    file_location="fileLocation"
                                )
                            )
                        ),
                        mainframe_action=apptest_mixins.CfnTestCasePropsMixin.MainframeActionProperty(
                            action_type=apptest_mixins.CfnTestCasePropsMixin.MainframeActionTypeProperty(
                                batch=apptest_mixins.CfnTestCasePropsMixin.BatchProperty(
                                    batch_job_name="batchJobName",
                                    batch_job_parameters={
                                        "batch_job_parameters_key": "batchJobParameters"
                                    },
                                    export_data_set_names=["exportDataSetNames"]
                                ),
                                tn3270=apptest_mixins.CfnTestCasePropsMixin.TN3270Property(
                                    export_data_set_names=["exportDataSetNames"],
                                    script=apptest_mixins.CfnTestCasePropsMixin.ScriptProperty(
                                        script_location="scriptLocation",
                                        type="type"
                                    )
                                )
                            ),
                            properties=apptest_mixins.CfnTestCasePropsMixin.MainframeActionPropertiesProperty(
                                dms_task_arn="dmsTaskArn"
                            ),
                            resource="resource"
                        ),
                        resource_action=apptest_mixins.CfnTestCasePropsMixin.ResourceActionProperty(
                            cloud_formation_action=apptest_mixins.CfnTestCasePropsMixin.CloudFormationActionProperty(
                                action_type="actionType",
                                resource="resource"
                            ),
                            m2_managed_application_action=apptest_mixins.CfnTestCasePropsMixin.M2ManagedApplicationActionProperty(
                                action_type="actionType",
                                properties=apptest_mixins.CfnTestCasePropsMixin.M2ManagedActionPropertiesProperty(
                                    force_stop=False,
                                    import_data_set_location="importDataSetLocation"
                                ),
                                resource="resource"
                            ),
                            m2_non_managed_application_action=apptest_mixins.CfnTestCasePropsMixin.M2NonManagedApplicationActionProperty(
                                action_type="actionType",
                                resource="resource"
                            )
                        )
                    ),
                    description="description",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b31ff635556700d4e9fcce53386e402e5d1bc2c293c38fe2a334b9495fce87ae)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if description is not None:
                self._values["description"] = description
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.StepActionProperty"]]:
            '''The action of the step.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-step.html#cfn-apptest-testcase-step-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.StepActionProperty"]], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the step.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-step.html#cfn-apptest-testcase-step-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the step.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-step.html#cfn-apptest-testcase-step-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StepProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin.TN3270Property",
        jsii_struct_bases=[],
        name_mapping={
            "export_data_set_names": "exportDataSetNames",
            "script": "script",
        },
    )
    class TN3270Property:
        def __init__(
            self,
            *,
            export_data_set_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            script: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTestCasePropsMixin.ScriptProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the TN3270 protocol.

            :param export_data_set_names: The data set names of the TN3270 protocol.
            :param script: The script of the TN3270 protocol.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-tn3270.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
                
                t_n3270_property = apptest_mixins.CfnTestCasePropsMixin.TN3270Property(
                    export_data_set_names=["exportDataSetNames"],
                    script=apptest_mixins.CfnTestCasePropsMixin.ScriptProperty(
                        script_location="scriptLocation",
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9babb608ab3460a267396836a247f1074fc737dd884141529847ee8ffab815a4)
                check_type(argname="argument export_data_set_names", value=export_data_set_names, expected_type=type_hints["export_data_set_names"])
                check_type(argname="argument script", value=script, expected_type=type_hints["script"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if export_data_set_names is not None:
                self._values["export_data_set_names"] = export_data_set_names
            if script is not None:
                self._values["script"] = script

        @builtins.property
        def export_data_set_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The data set names of the TN3270 protocol.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-tn3270.html#cfn-apptest-testcase-tn3270-exportdatasetnames
            '''
            result = self._values.get("export_data_set_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def script(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.ScriptProperty"]]:
            '''The script of the TN3270 protocol.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-tn3270.html#cfn-apptest-testcase-tn3270-script
            '''
            result = self._values.get("script")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTestCasePropsMixin.ScriptProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TN3270Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin.TargetDatabaseMetadataProperty",
        jsii_struct_bases=[],
        name_mapping={"capture_tool": "captureTool", "type": "type"},
    )
    class TargetDatabaseMetadataProperty:
        def __init__(
            self,
            *,
            capture_tool: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies a target database metadata.

            :param capture_tool: The capture tool of the target database metadata.
            :param type: The type of the target database metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-targetdatabasemetadata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
                
                target_database_metadata_property = apptest_mixins.CfnTestCasePropsMixin.TargetDatabaseMetadataProperty(
                    capture_tool="captureTool",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fc2f418828afe5528227427b544feaca7be99d748296769ad1eaf377c7807f12)
                check_type(argname="argument capture_tool", value=capture_tool, expected_type=type_hints["capture_tool"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if capture_tool is not None:
                self._values["capture_tool"] = capture_tool
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def capture_tool(self) -> typing.Optional[builtins.str]:
            '''The capture tool of the target database metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-targetdatabasemetadata.html#cfn-apptest-testcase-targetdatabasemetadata-capturetool
            '''
            result = self._values.get("capture_tool")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of the target database metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-targetdatabasemetadata.html#cfn-apptest-testcase-targetdatabasemetadata-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetDatabaseMetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apptest.mixins.CfnTestCasePropsMixin.TestCaseLatestVersionProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status", "version": "version"},
    )
    class TestCaseLatestVersionProperty:
        def __init__(
            self,
            *,
            status: typing.Optional[builtins.str] = None,
            version: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the latest version of a test case.

            :param status: The status of the test case latest version.
            :param version: The version of the test case latest version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-testcaselatestversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apptest import mixins as apptest_mixins
                
                test_case_latest_version_property = apptest_mixins.CfnTestCasePropsMixin.TestCaseLatestVersionProperty(
                    status="status",
                    version=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ba08ac267f5eea6c5a88ecf78a060a1263f241025aaf1d424212b39b7899fb4e)
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if status is not None:
                self._values["status"] = status
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of the test case latest version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-testcaselatestversion.html#cfn-apptest-testcase-testcaselatestversion-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[jsii.Number]:
            '''The version of the test case latest version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apptest-testcase-testcaselatestversion.html#cfn-apptest-testcase-testcaselatestversion-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TestCaseLatestVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnTestCaseMixinProps",
    "CfnTestCasePropsMixin",
]

publication.publish()

def _typecheckingstub__7ded8d520283d97bd0a24f1fbf7b3ee13ded205256ce23df2aa9251d070bfc33(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    steps: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTestCasePropsMixin.StepProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea107efdd2b85ba1845f882331d30a1394ecf4af7f0caa080d3760e2ed23bcf0(
    props: typing.Union[CfnTestCaseMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2355fbfb1c1a03626247c36393e4e6ec71570453c2b3f9e4e7716ee0b3535fb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60202a81d1adbb46ae9657fa260dfab58d5a2a9b4d456efb23512c0403004782(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__481ecda2ba4c8bcc7a614f36e31e0507506cf71504b623ba07e941df5ee132f6(
    *,
    batch_job_name: typing.Optional[builtins.str] = None,
    batch_job_parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    export_data_set_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__507908a4c65372443e0c8e4246fbec98f80d054bae5b300dd5881ac01ac40990(
    *,
    action_type: typing.Optional[builtins.str] = None,
    resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41991261f52553328563584b5c07a061be1e472c0f1b6ed63d2264ccd14730d1(
    *,
    input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTestCasePropsMixin.InputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    output: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTestCasePropsMixin.OutputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7bd476b45d6f3681dc405f70f3a7daf6de456e6fbc729f068e684b608b88807(
    *,
    ccsid: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
    length: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc061f3f8f82ee3909d53e0b6a02ac46c7e7657b20df03104e2d1482d7bab72d(
    *,
    source_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTestCasePropsMixin.SourceDatabaseMetadataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTestCasePropsMixin.TargetDatabaseMetadataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02dbca42e7f25c3b6c450944aa6c63ecd0002fbb3a5f4003c5051146f4b3d047(
    *,
    database_cdc: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTestCasePropsMixin.DatabaseCDCProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    data_sets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTestCasePropsMixin.DataSetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6cf3eca24c2e90878e4235206c622f1d8ca0afb16b20f300fc2a495caf72992(
    *,
    file_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTestCasePropsMixin.FileMetadataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_location: typing.Optional[builtins.str] = None,
    target_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__445b776b20d6bba582861061125bb9ce60ab4fe629747862dbe4a23f3869278a(
    *,
    file: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTestCasePropsMixin.InputFileProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20d17eef27087a50d016bffef379b134b971fdbd8ad2462c57188e223f64c78d(
    *,
    force_stop: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    import_data_set_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22b4257fe855fcb5b600d998d69859c81fad99ffab6efd0c0b368f4fccbe4091(
    *,
    action_type: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTestCasePropsMixin.M2ManagedActionPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__961bec98e59ff4405adde66de375138fda8a0390464d790bc71745ead022a121(
    *,
    action_type: typing.Optional[builtins.str] = None,
    resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92cfd92adeef1398833ad57becb97a89f6c58caf9c36b766b592067fe22007a3(
    *,
    dms_task_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1027de5a730fa61c60a560d91cd94e75faa574eb546f4440140a8e2baddd3d(
    *,
    action_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTestCasePropsMixin.MainframeActionTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTestCasePropsMixin.MainframeActionPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80572a381d7b0623b3aac68aae352a719226ce65ec890b4042d3064199c8a538(
    *,
    batch: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTestCasePropsMixin.BatchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tn3270: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTestCasePropsMixin.TN3270Property, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b34949df24bf28c34ed85aa7d19e004762b77fdfd24fe24b86f645e451e305f4(
    *,
    file_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__798c86cf68a04a1ee78acbe398fcc96d4badbcd05884a855ccb0fd58b66b5fd1(
    *,
    file: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTestCasePropsMixin.OutputFileProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df1aba57c9e80e09d1611d96db8c61824b1b8dfe91f96092019e45fbbba5e034(
    *,
    cloud_formation_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTestCasePropsMixin.CloudFormationActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    m2_managed_application_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTestCasePropsMixin.M2ManagedApplicationActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    m2_non_managed_application_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTestCasePropsMixin.M2NonManagedApplicationActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4805a976e80b858c552ae5fc986ade07c1dac47d744ca1ac94f722bda95bec59(
    *,
    script_location: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0454dd540598f7afcaa1ac4d8e4d858a17aa41a3a6fcbc70401c4a3e351351d7(
    *,
    capture_tool: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a0766788ddb686b0ffa08da7d98f21287379c7c4a582735ffc0fd29b9bcc161(
    *,
    compare_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTestCasePropsMixin.CompareActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mainframe_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTestCasePropsMixin.MainframeActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTestCasePropsMixin.ResourceActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31ff635556700d4e9fcce53386e402e5d1bc2c293c38fe2a334b9495fce87ae(
    *,
    action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTestCasePropsMixin.StepActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9babb608ab3460a267396836a247f1074fc737dd884141529847ee8ffab815a4(
    *,
    export_data_set_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    script: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTestCasePropsMixin.ScriptProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc2f418828afe5528227427b544feaca7be99d748296769ad1eaf377c7807f12(
    *,
    capture_tool: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba08ac267f5eea6c5a88ecf78a060a1263f241025aaf1d424212b39b7899fb4e(
    *,
    status: typing.Optional[builtins.str] = None,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
