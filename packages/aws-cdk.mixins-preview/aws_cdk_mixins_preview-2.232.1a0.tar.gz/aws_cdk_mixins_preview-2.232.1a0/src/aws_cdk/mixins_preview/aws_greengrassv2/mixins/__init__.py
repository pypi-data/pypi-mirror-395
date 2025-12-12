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
    jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnComponentVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "inline_recipe": "inlineRecipe",
        "lambda_function": "lambdaFunction",
        "tags": "tags",
    },
)
class CfnComponentVersionMixinProps:
    def __init__(
        self,
        *,
        inline_recipe: typing.Optional[builtins.str] = None,
        lambda_function: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentVersionPropsMixin.LambdaFunctionRecipeSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnComponentVersionPropsMixin.

        :param inline_recipe: The recipe to use to create the component. The recipe defines the component's metadata, parameters, dependencies, lifecycle, artifacts, and platform compatibility. You must specify either ``InlineRecipe`` or ``LambdaFunction`` .
        :param lambda_function: The parameters to create a component from a Lambda function. You must specify either ``InlineRecipe`` or ``LambdaFunction`` .
        :param tags: Application-specific metadata to attach to the component version. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tag your AWS IoT Greengrass Version 2 resources <https://docs.aws.amazon.com/greengrass/v2/developerguide/tag-resources.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-componentversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
            
            cfn_component_version_mixin_props = greengrassv2_mixins.CfnComponentVersionMixinProps(
                inline_recipe="inlineRecipe",
                lambda_function=greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaFunctionRecipeSourceProperty(
                    component_dependencies={
                        "component_dependencies_key": greengrassv2_mixins.CfnComponentVersionPropsMixin.ComponentDependencyRequirementProperty(
                            dependency_type="dependencyType",
                            version_requirement="versionRequirement"
                        )
                    },
                    component_lambda_parameters=greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaExecutionParametersProperty(
                        environment_variables={
                            "environment_variables_key": "environmentVariables"
                        },
                        event_sources=[greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaEventSourceProperty(
                            topic="topic",
                            type="type"
                        )],
                        exec_args=["execArgs"],
                        input_payload_encoding_type="inputPayloadEncodingType",
                        linux_process_params=greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaLinuxProcessParamsProperty(
                            container_params=greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaContainerParamsProperty(
                                devices=[greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaDeviceMountProperty(
                                    add_group_owner=False,
                                    path="path",
                                    permission="permission"
                                )],
                                memory_size_in_kb=123,
                                mount_ro_sysfs=False,
                                volumes=[greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaVolumeMountProperty(
                                    add_group_owner=False,
                                    destination_path="destinationPath",
                                    permission="permission",
                                    source_path="sourcePath"
                                )]
                            ),
                            isolation_mode="isolationMode"
                        ),
                        max_idle_time_in_seconds=123,
                        max_instances_count=123,
                        max_queue_size=123,
                        pinned=False,
                        status_timeout_in_seconds=123,
                        timeout_in_seconds=123
                    ),
                    component_name="componentName",
                    component_platforms=[greengrassv2_mixins.CfnComponentVersionPropsMixin.ComponentPlatformProperty(
                        attributes={
                            "attributes_key": "attributes"
                        },
                        name="name"
                    )],
                    component_version="componentVersion",
                    lambda_arn="lambdaArn"
                ),
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49df39751f98d5c603e15c210ce1dd5b8c6026e0bce42fdf6b665d9e71f956c0)
            check_type(argname="argument inline_recipe", value=inline_recipe, expected_type=type_hints["inline_recipe"])
            check_type(argname="argument lambda_function", value=lambda_function, expected_type=type_hints["lambda_function"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if inline_recipe is not None:
            self._values["inline_recipe"] = inline_recipe
        if lambda_function is not None:
            self._values["lambda_function"] = lambda_function
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def inline_recipe(self) -> typing.Optional[builtins.str]:
        '''The recipe to use to create the component.

        The recipe defines the component's metadata, parameters, dependencies, lifecycle, artifacts, and platform compatibility.

        You must specify either ``InlineRecipe`` or ``LambdaFunction`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-componentversion.html#cfn-greengrassv2-componentversion-inlinerecipe
        '''
        result = self._values.get("inline_recipe")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lambda_function(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentVersionPropsMixin.LambdaFunctionRecipeSourceProperty"]]:
        '''The parameters to create a component from a Lambda function.

        You must specify either ``InlineRecipe`` or ``LambdaFunction`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-componentversion.html#cfn-greengrassv2-componentversion-lambdafunction
        '''
        result = self._values.get("lambda_function")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentVersionPropsMixin.LambdaFunctionRecipeSourceProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Application-specific metadata to attach to the component version.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tag your AWS IoT Greengrass Version 2 resources <https://docs.aws.amazon.com/greengrass/v2/developerguide/tag-resources.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-componentversion.html#cfn-greengrassv2-componentversion-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnComponentVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnComponentVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnComponentVersionPropsMixin",
):
    '''Creates a component.

    Components are software that run on AWS IoT Greengrass core devices. After you develop and test a component on your core device, you can use this operation to upload your component to AWS IoT Greengrass . Then, you can deploy the component to other core devices.

    You can use this operation to do the following:

    - *Create components from recipes*

    Create a component from a recipe, which is a file that defines the component's metadata, parameters, dependencies, lifecycle, artifacts, and platform capability. For more information, see `AWS IoT Greengrass component recipe reference <https://docs.aws.amazon.com/greengrass/v2/developerguide/component-recipe-reference.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

    To create a component from a recipe, specify ``inlineRecipe`` when you call this operation.

    - *Create components from Lambda functions*

    Create a component from an AWS Lambda function that runs on AWS IoT Greengrass . This creates a recipe and artifacts from the Lambda function's deployment package. You can use this operation to migrate Lambda functions from AWS IoT Greengrass V1 to AWS IoT Greengrass V2 .

    This function accepts Lambda functions in all supported versions of Python, Node.js, and Java runtimes. AWS IoT Greengrass doesn't apply any additional restrictions on deprecated Lambda runtime versions.

    To create a component from a Lambda function, specify ``lambdaFunction`` when you call this operation.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-componentversion.html
    :cloudformationResource: AWS::GreengrassV2::ComponentVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
        
        cfn_component_version_props_mixin = greengrassv2_mixins.CfnComponentVersionPropsMixin(greengrassv2_mixins.CfnComponentVersionMixinProps(
            inline_recipe="inlineRecipe",
            lambda_function=greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaFunctionRecipeSourceProperty(
                component_dependencies={
                    "component_dependencies_key": greengrassv2_mixins.CfnComponentVersionPropsMixin.ComponentDependencyRequirementProperty(
                        dependency_type="dependencyType",
                        version_requirement="versionRequirement"
                    )
                },
                component_lambda_parameters=greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaExecutionParametersProperty(
                    environment_variables={
                        "environment_variables_key": "environmentVariables"
                    },
                    event_sources=[greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaEventSourceProperty(
                        topic="topic",
                        type="type"
                    )],
                    exec_args=["execArgs"],
                    input_payload_encoding_type="inputPayloadEncodingType",
                    linux_process_params=greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaLinuxProcessParamsProperty(
                        container_params=greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaContainerParamsProperty(
                            devices=[greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaDeviceMountProperty(
                                add_group_owner=False,
                                path="path",
                                permission="permission"
                            )],
                            memory_size_in_kb=123,
                            mount_ro_sysfs=False,
                            volumes=[greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaVolumeMountProperty(
                                add_group_owner=False,
                                destination_path="destinationPath",
                                permission="permission",
                                source_path="sourcePath"
                            )]
                        ),
                        isolation_mode="isolationMode"
                    ),
                    max_idle_time_in_seconds=123,
                    max_instances_count=123,
                    max_queue_size=123,
                    pinned=False,
                    status_timeout_in_seconds=123,
                    timeout_in_seconds=123
                ),
                component_name="componentName",
                component_platforms=[greengrassv2_mixins.CfnComponentVersionPropsMixin.ComponentPlatformProperty(
                    attributes={
                        "attributes_key": "attributes"
                    },
                    name="name"
                )],
                component_version="componentVersion",
                lambda_arn="lambdaArn"
            ),
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnComponentVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GreengrassV2::ComponentVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__663a0ee564d5de028a1bff39802202e8e949ef2c642cff06185e11507f065c8c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4812465db085497d2d562fa36714ca253e015af839126bd5e6098783e8274f93)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b23180d0eff8eaeee65db14cf8db4a03a4014b77b7d2d8c50ff58a4cec862b7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnComponentVersionMixinProps:
        return typing.cast(CfnComponentVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnComponentVersionPropsMixin.ComponentDependencyRequirementProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dependency_type": "dependencyType",
            "version_requirement": "versionRequirement",
        },
    )
    class ComponentDependencyRequirementProperty:
        def __init__(
            self,
            *,
            dependency_type: typing.Optional[builtins.str] = None,
            version_requirement: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about a component dependency for a Lambda function component.

            :param dependency_type: The type of this dependency. Choose from the following options:. - ``SOFT`` – The component doesn't restart if the dependency changes state. - ``HARD`` – The component restarts if the dependency changes state. Default: ``HARD``
            :param version_requirement: The component version requirement for the component dependency. AWS IoT Greengrass uses semantic version constraints. For more information, see `Semantic Versioning <https://docs.aws.amazon.com/https://semver.org/>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-componentdependencyrequirement.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
                
                component_dependency_requirement_property = greengrassv2_mixins.CfnComponentVersionPropsMixin.ComponentDependencyRequirementProperty(
                    dependency_type="dependencyType",
                    version_requirement="versionRequirement"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9f762a8a78c9621232d4d77bc0d80337cde334b1095f4751b539c5fdc07d0353)
                check_type(argname="argument dependency_type", value=dependency_type, expected_type=type_hints["dependency_type"])
                check_type(argname="argument version_requirement", value=version_requirement, expected_type=type_hints["version_requirement"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dependency_type is not None:
                self._values["dependency_type"] = dependency_type
            if version_requirement is not None:
                self._values["version_requirement"] = version_requirement

        @builtins.property
        def dependency_type(self) -> typing.Optional[builtins.str]:
            '''The type of this dependency. Choose from the following options:.

            - ``SOFT`` – The component doesn't restart if the dependency changes state.
            - ``HARD`` – The component restarts if the dependency changes state.

            Default: ``HARD``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-componentdependencyrequirement.html#cfn-greengrassv2-componentversion-componentdependencyrequirement-dependencytype
            '''
            result = self._values.get("dependency_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version_requirement(self) -> typing.Optional[builtins.str]:
            '''The component version requirement for the component dependency.

            AWS IoT Greengrass uses semantic version constraints. For more information, see `Semantic Versioning <https://docs.aws.amazon.com/https://semver.org/>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-componentdependencyrequirement.html#cfn-greengrassv2-componentversion-componentdependencyrequirement-versionrequirement
            '''
            result = self._values.get("version_requirement")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentDependencyRequirementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnComponentVersionPropsMixin.ComponentPlatformProperty",
        jsii_struct_bases=[],
        name_mapping={"attributes": "attributes", "name": "name"},
    )
    class ComponentPlatformProperty:
        def __init__(
            self,
            *,
            attributes: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about a platform that a component supports.

            :param attributes: A dictionary of attributes for the platform. The AWS IoT Greengrass Core software defines the ``os`` and ``platform`` by default. You can specify additional platform attributes for a core device when you deploy the AWS IoT Greengrass nucleus component. For more information, see the `AWS IoT Greengrass nucleus component <https://docs.aws.amazon.com/greengrass/v2/developerguide/greengrass-nucleus-component.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* .
            :param name: The friendly name of the platform. This name helps you identify the platform. If you omit this parameter, AWS IoT Greengrass creates a friendly name from the ``os`` and ``architecture`` of the platform.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-componentplatform.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
                
                component_platform_property = greengrassv2_mixins.CfnComponentVersionPropsMixin.ComponentPlatformProperty(
                    attributes={
                        "attributes_key": "attributes"
                    },
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6287916204d51d4cc486ea874e0c3b6dd237d15211c6794f2192d98cdf3c6c83)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def attributes(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''A dictionary of attributes for the platform.

            The AWS IoT Greengrass Core software defines the ``os`` and ``platform`` by default. You can specify additional platform attributes for a core device when you deploy the AWS IoT Greengrass nucleus component. For more information, see the `AWS IoT Greengrass nucleus component <https://docs.aws.amazon.com/greengrass/v2/developerguide/greengrass-nucleus-component.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-componentplatform.html#cfn-greengrassv2-componentversion-componentplatform-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The friendly name of the platform. This name helps you identify the platform.

            If you omit this parameter, AWS IoT Greengrass creates a friendly name from the ``os`` and ``architecture`` of the platform.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-componentplatform.html#cfn-greengrassv2-componentversion-componentplatform-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentPlatformProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnComponentVersionPropsMixin.LambdaContainerParamsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "devices": "devices",
            "memory_size_in_kb": "memorySizeInKb",
            "mount_ro_sysfs": "mountRoSysfs",
            "volumes": "volumes",
        },
    )
    class LambdaContainerParamsProperty:
        def __init__(
            self,
            *,
            devices: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentVersionPropsMixin.LambdaDeviceMountProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            memory_size_in_kb: typing.Optional[jsii.Number] = None,
            mount_ro_sysfs: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            volumes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentVersionPropsMixin.LambdaVolumeMountProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Contains information about a container in which AWS Lambda functions run on AWS IoT Greengrass core devices.

            :param devices: The list of system devices that the container can access.
            :param memory_size_in_kb: The memory size of the container, expressed in kilobytes. Default: ``16384`` (16 MB)
            :param mount_ro_sysfs: Whether or not the container can read information from the device's ``/sys`` folder. Default: ``false``
            :param volumes: The list of volumes that the container can access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdacontainerparams.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
                
                lambda_container_params_property = greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaContainerParamsProperty(
                    devices=[greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaDeviceMountProperty(
                        add_group_owner=False,
                        path="path",
                        permission="permission"
                    )],
                    memory_size_in_kb=123,
                    mount_ro_sysfs=False,
                    volumes=[greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaVolumeMountProperty(
                        add_group_owner=False,
                        destination_path="destinationPath",
                        permission="permission",
                        source_path="sourcePath"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__34c477251c4f1700daf571f2b8a89deeb520a40cb3584e52b2b2177b14e58feb)
                check_type(argname="argument devices", value=devices, expected_type=type_hints["devices"])
                check_type(argname="argument memory_size_in_kb", value=memory_size_in_kb, expected_type=type_hints["memory_size_in_kb"])
                check_type(argname="argument mount_ro_sysfs", value=mount_ro_sysfs, expected_type=type_hints["mount_ro_sysfs"])
                check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if devices is not None:
                self._values["devices"] = devices
            if memory_size_in_kb is not None:
                self._values["memory_size_in_kb"] = memory_size_in_kb
            if mount_ro_sysfs is not None:
                self._values["mount_ro_sysfs"] = mount_ro_sysfs
            if volumes is not None:
                self._values["volumes"] = volumes

        @builtins.property
        def devices(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentVersionPropsMixin.LambdaDeviceMountProperty"]]]]:
            '''The list of system devices that the container can access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdacontainerparams.html#cfn-greengrassv2-componentversion-lambdacontainerparams-devices
            '''
            result = self._values.get("devices")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentVersionPropsMixin.LambdaDeviceMountProperty"]]]], result)

        @builtins.property
        def memory_size_in_kb(self) -> typing.Optional[jsii.Number]:
            '''The memory size of the container, expressed in kilobytes.

            Default: ``16384`` (16 MB)

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdacontainerparams.html#cfn-greengrassv2-componentversion-lambdacontainerparams-memorysizeinkb
            '''
            result = self._values.get("memory_size_in_kb")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def mount_ro_sysfs(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether or not the container can read information from the device's ``/sys`` folder.

            Default: ``false``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdacontainerparams.html#cfn-greengrassv2-componentversion-lambdacontainerparams-mountrosysfs
            '''
            result = self._values.get("mount_ro_sysfs")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def volumes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentVersionPropsMixin.LambdaVolumeMountProperty"]]]]:
            '''The list of volumes that the container can access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdacontainerparams.html#cfn-greengrassv2-componentversion-lambdacontainerparams-volumes
            '''
            result = self._values.get("volumes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentVersionPropsMixin.LambdaVolumeMountProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaContainerParamsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnComponentVersionPropsMixin.LambdaDeviceMountProperty",
        jsii_struct_bases=[],
        name_mapping={
            "add_group_owner": "addGroupOwner",
            "path": "path",
            "permission": "permission",
        },
    )
    class LambdaDeviceMountProperty:
        def __init__(
            self,
            *,
            add_group_owner: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            path: typing.Optional[builtins.str] = None,
            permission: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about a device that Linux processes in a container can access.

            :param add_group_owner: Whether or not to add the component's system user as an owner of the device. Default: ``false``
            :param path: The mount path for the device in the file system.
            :param permission: The permission to access the device: read/only ( ``ro`` ) or read/write ( ``rw`` ). Default: ``ro``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdadevicemount.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
                
                lambda_device_mount_property = greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaDeviceMountProperty(
                    add_group_owner=False,
                    path="path",
                    permission="permission"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8b4805a6303580a0913041f4fba903b7a6839a4de559ff37013fcd846bb265d3)
                check_type(argname="argument add_group_owner", value=add_group_owner, expected_type=type_hints["add_group_owner"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if add_group_owner is not None:
                self._values["add_group_owner"] = add_group_owner
            if path is not None:
                self._values["path"] = path
            if permission is not None:
                self._values["permission"] = permission

        @builtins.property
        def add_group_owner(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether or not to add the component's system user as an owner of the device.

            Default: ``false``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdadevicemount.html#cfn-greengrassv2-componentversion-lambdadevicemount-addgroupowner
            '''
            result = self._values.get("add_group_owner")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The mount path for the device in the file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdadevicemount.html#cfn-greengrassv2-componentversion-lambdadevicemount-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def permission(self) -> typing.Optional[builtins.str]:
            '''The permission to access the device: read/only ( ``ro`` ) or read/write ( ``rw`` ).

            Default: ``ro``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdadevicemount.html#cfn-greengrassv2-componentversion-lambdadevicemount-permission
            '''
            result = self._values.get("permission")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaDeviceMountProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnComponentVersionPropsMixin.LambdaEventSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"topic": "topic", "type": "type"},
    )
    class LambdaEventSourceProperty:
        def __init__(
            self,
            *,
            topic: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about an event source for an AWS Lambda function.

            The event source defines the topics on which this Lambda function subscribes to receive messages that run the function.

            :param topic: The topic to which to subscribe to receive event messages.
            :param type: The type of event source. Choose from the following options:. - ``PUB_SUB`` – Subscribe to local publish/subscribe messages. This event source type doesn't support MQTT wildcards ( ``+`` and ``#`` ) in the event source topic. - ``IOT_CORE`` – Subscribe to AWS IoT Core MQTT messages. This event source type supports MQTT wildcards ( ``+`` and ``#`` ) in the event source topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaeventsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
                
                lambda_event_source_property = greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaEventSourceProperty(
                    topic="topic",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1aef5532273311adf689e9ded57540a9266fea5b493f96a22cd0dbeace8c1c8a)
                check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if topic is not None:
                self._values["topic"] = topic
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def topic(self) -> typing.Optional[builtins.str]:
            '''The topic to which to subscribe to receive event messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaeventsource.html#cfn-greengrassv2-componentversion-lambdaeventsource-topic
            '''
            result = self._values.get("topic")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of event source. Choose from the following options:.

            - ``PUB_SUB`` – Subscribe to local publish/subscribe messages. This event source type doesn't support MQTT wildcards ( ``+`` and ``#`` ) in the event source topic.
            - ``IOT_CORE`` – Subscribe to AWS IoT Core MQTT messages. This event source type supports MQTT wildcards ( ``+`` and ``#`` ) in the event source topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaeventsource.html#cfn-greengrassv2-componentversion-lambdaeventsource-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaEventSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnComponentVersionPropsMixin.LambdaExecutionParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "environment_variables": "environmentVariables",
            "event_sources": "eventSources",
            "exec_args": "execArgs",
            "input_payload_encoding_type": "inputPayloadEncodingType",
            "linux_process_params": "linuxProcessParams",
            "max_idle_time_in_seconds": "maxIdleTimeInSeconds",
            "max_instances_count": "maxInstancesCount",
            "max_queue_size": "maxQueueSize",
            "pinned": "pinned",
            "status_timeout_in_seconds": "statusTimeoutInSeconds",
            "timeout_in_seconds": "timeoutInSeconds",
        },
    )
    class LambdaExecutionParametersProperty:
        def __init__(
            self,
            *,
            environment_variables: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            event_sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentVersionPropsMixin.LambdaEventSourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            exec_args: typing.Optional[typing.Sequence[builtins.str]] = None,
            input_payload_encoding_type: typing.Optional[builtins.str] = None,
            linux_process_params: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentVersionPropsMixin.LambdaLinuxProcessParamsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            max_idle_time_in_seconds: typing.Optional[jsii.Number] = None,
            max_instances_count: typing.Optional[jsii.Number] = None,
            max_queue_size: typing.Optional[jsii.Number] = None,
            pinned: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            status_timeout_in_seconds: typing.Optional[jsii.Number] = None,
            timeout_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains parameters for a Lambda function that runs on AWS IoT Greengrass .

            :param environment_variables: The map of environment variables that are available to the Lambda function when it runs.
            :param event_sources: The list of event sources to which to subscribe to receive work messages. The Lambda function runs when it receives a message from an event source. You can subscribe this function to local publish/subscribe messages and AWS IoT Core MQTT messages.
            :param exec_args: The list of arguments to pass to the Lambda function when it runs.
            :param input_payload_encoding_type: The encoding type that the Lambda function supports. Default: ``json``
            :param linux_process_params: The parameters for the Linux process that contains the Lambda function.
            :param max_idle_time_in_seconds: The maximum amount of time in seconds that a non-pinned Lambda function can idle before the AWS IoT Greengrass Core software stops its process.
            :param max_instances_count: The maximum number of instances that a non-pinned Lambda function can run at the same time.
            :param max_queue_size: The maximum size of the message queue for the Lambda function component. The AWS IoT Greengrass core device stores messages in a FIFO (first-in-first-out) queue until it can run the Lambda function to consume each message.
            :param pinned: Whether or not the Lambda function is pinned, or long-lived. - A pinned Lambda function starts when the AWS IoT Greengrass Core starts and keeps running in its own container. - A non-pinned Lambda function starts only when it receives a work item and exists after it idles for ``maxIdleTimeInSeconds`` . If the function has multiple work items, the AWS IoT Greengrass Core software creates multiple instances of the function. Default: ``true``
            :param status_timeout_in_seconds: The interval in seconds at which a pinned (also known as long-lived) Lambda function component sends status updates to the Lambda manager component.
            :param timeout_in_seconds: The maximum amount of time in seconds that the Lambda function can process a work item.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaexecutionparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
                
                lambda_execution_parameters_property = greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaExecutionParametersProperty(
                    environment_variables={
                        "environment_variables_key": "environmentVariables"
                    },
                    event_sources=[greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaEventSourceProperty(
                        topic="topic",
                        type="type"
                    )],
                    exec_args=["execArgs"],
                    input_payload_encoding_type="inputPayloadEncodingType",
                    linux_process_params=greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaLinuxProcessParamsProperty(
                        container_params=greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaContainerParamsProperty(
                            devices=[greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaDeviceMountProperty(
                                add_group_owner=False,
                                path="path",
                                permission="permission"
                            )],
                            memory_size_in_kb=123,
                            mount_ro_sysfs=False,
                            volumes=[greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaVolumeMountProperty(
                                add_group_owner=False,
                                destination_path="destinationPath",
                                permission="permission",
                                source_path="sourcePath"
                            )]
                        ),
                        isolation_mode="isolationMode"
                    ),
                    max_idle_time_in_seconds=123,
                    max_instances_count=123,
                    max_queue_size=123,
                    pinned=False,
                    status_timeout_in_seconds=123,
                    timeout_in_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__893141011743decfde4df8d391b40c6dfb06e2138a976aff0d648188f6775f8b)
                check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
                check_type(argname="argument event_sources", value=event_sources, expected_type=type_hints["event_sources"])
                check_type(argname="argument exec_args", value=exec_args, expected_type=type_hints["exec_args"])
                check_type(argname="argument input_payload_encoding_type", value=input_payload_encoding_type, expected_type=type_hints["input_payload_encoding_type"])
                check_type(argname="argument linux_process_params", value=linux_process_params, expected_type=type_hints["linux_process_params"])
                check_type(argname="argument max_idle_time_in_seconds", value=max_idle_time_in_seconds, expected_type=type_hints["max_idle_time_in_seconds"])
                check_type(argname="argument max_instances_count", value=max_instances_count, expected_type=type_hints["max_instances_count"])
                check_type(argname="argument max_queue_size", value=max_queue_size, expected_type=type_hints["max_queue_size"])
                check_type(argname="argument pinned", value=pinned, expected_type=type_hints["pinned"])
                check_type(argname="argument status_timeout_in_seconds", value=status_timeout_in_seconds, expected_type=type_hints["status_timeout_in_seconds"])
                check_type(argname="argument timeout_in_seconds", value=timeout_in_seconds, expected_type=type_hints["timeout_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if environment_variables is not None:
                self._values["environment_variables"] = environment_variables
            if event_sources is not None:
                self._values["event_sources"] = event_sources
            if exec_args is not None:
                self._values["exec_args"] = exec_args
            if input_payload_encoding_type is not None:
                self._values["input_payload_encoding_type"] = input_payload_encoding_type
            if linux_process_params is not None:
                self._values["linux_process_params"] = linux_process_params
            if max_idle_time_in_seconds is not None:
                self._values["max_idle_time_in_seconds"] = max_idle_time_in_seconds
            if max_instances_count is not None:
                self._values["max_instances_count"] = max_instances_count
            if max_queue_size is not None:
                self._values["max_queue_size"] = max_queue_size
            if pinned is not None:
                self._values["pinned"] = pinned
            if status_timeout_in_seconds is not None:
                self._values["status_timeout_in_seconds"] = status_timeout_in_seconds
            if timeout_in_seconds is not None:
                self._values["timeout_in_seconds"] = timeout_in_seconds

        @builtins.property
        def environment_variables(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The map of environment variables that are available to the Lambda function when it runs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaexecutionparameters.html#cfn-greengrassv2-componentversion-lambdaexecutionparameters-environmentvariables
            '''
            result = self._values.get("environment_variables")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def event_sources(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentVersionPropsMixin.LambdaEventSourceProperty"]]]]:
            '''The list of event sources to which to subscribe to receive work messages.

            The Lambda function runs when it receives a message from an event source. You can subscribe this function to local publish/subscribe messages and AWS IoT Core MQTT messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaexecutionparameters.html#cfn-greengrassv2-componentversion-lambdaexecutionparameters-eventsources
            '''
            result = self._values.get("event_sources")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentVersionPropsMixin.LambdaEventSourceProperty"]]]], result)

        @builtins.property
        def exec_args(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of arguments to pass to the Lambda function when it runs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaexecutionparameters.html#cfn-greengrassv2-componentversion-lambdaexecutionparameters-execargs
            '''
            result = self._values.get("exec_args")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def input_payload_encoding_type(self) -> typing.Optional[builtins.str]:
            '''The encoding type that the Lambda function supports.

            Default: ``json``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaexecutionparameters.html#cfn-greengrassv2-componentversion-lambdaexecutionparameters-inputpayloadencodingtype
            '''
            result = self._values.get("input_payload_encoding_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def linux_process_params(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentVersionPropsMixin.LambdaLinuxProcessParamsProperty"]]:
            '''The parameters for the Linux process that contains the Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaexecutionparameters.html#cfn-greengrassv2-componentversion-lambdaexecutionparameters-linuxprocessparams
            '''
            result = self._values.get("linux_process_params")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentVersionPropsMixin.LambdaLinuxProcessParamsProperty"]], result)

        @builtins.property
        def max_idle_time_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of time in seconds that a non-pinned Lambda function can idle before the AWS IoT Greengrass Core software stops its process.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaexecutionparameters.html#cfn-greengrassv2-componentversion-lambdaexecutionparameters-maxidletimeinseconds
            '''
            result = self._values.get("max_idle_time_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_instances_count(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of instances that a non-pinned Lambda function can run at the same time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaexecutionparameters.html#cfn-greengrassv2-componentversion-lambdaexecutionparameters-maxinstancescount
            '''
            result = self._values.get("max_instances_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_queue_size(self) -> typing.Optional[jsii.Number]:
            '''The maximum size of the message queue for the Lambda function component.

            The AWS IoT Greengrass core device stores messages in a FIFO (first-in-first-out) queue until it can run the Lambda function to consume each message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaexecutionparameters.html#cfn-greengrassv2-componentversion-lambdaexecutionparameters-maxqueuesize
            '''
            result = self._values.get("max_queue_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def pinned(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether or not the Lambda function is pinned, or long-lived.

            - A pinned Lambda function starts when the AWS IoT Greengrass Core starts and keeps running in its own container.
            - A non-pinned Lambda function starts only when it receives a work item and exists after it idles for ``maxIdleTimeInSeconds`` . If the function has multiple work items, the AWS IoT Greengrass Core software creates multiple instances of the function.

            Default: ``true``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaexecutionparameters.html#cfn-greengrassv2-componentversion-lambdaexecutionparameters-pinned
            '''
            result = self._values.get("pinned")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def status_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The interval in seconds at which a pinned (also known as long-lived) Lambda function component sends status updates to the Lambda manager component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaexecutionparameters.html#cfn-greengrassv2-componentversion-lambdaexecutionparameters-statustimeoutinseconds
            '''
            result = self._values.get("status_timeout_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of time in seconds that the Lambda function can process a work item.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaexecutionparameters.html#cfn-greengrassv2-componentversion-lambdaexecutionparameters-timeoutinseconds
            '''
            result = self._values.get("timeout_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaExecutionParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnComponentVersionPropsMixin.LambdaFunctionRecipeSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component_dependencies": "componentDependencies",
            "component_lambda_parameters": "componentLambdaParameters",
            "component_name": "componentName",
            "component_platforms": "componentPlatforms",
            "component_version": "componentVersion",
            "lambda_arn": "lambdaArn",
        },
    )
    class LambdaFunctionRecipeSourceProperty:
        def __init__(
            self,
            *,
            component_dependencies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentVersionPropsMixin.ComponentDependencyRequirementProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            component_lambda_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentVersionPropsMixin.LambdaExecutionParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            component_name: typing.Optional[builtins.str] = None,
            component_platforms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentVersionPropsMixin.ComponentPlatformProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            component_version: typing.Optional[builtins.str] = None,
            lambda_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about an AWS Lambda function to import to create a component.

            :param component_dependencies: The component versions on which this Lambda function component depends.
            :param component_lambda_parameters: The system and runtime parameters for the Lambda function as it runs on the AWS IoT Greengrass core device.
            :param component_name: The name of the component. Defaults to the name of the Lambda function.
            :param component_platforms: The platforms that the component version supports.
            :param component_version: The version of the component. Defaults to the version of the Lambda function as a semantic version. For example, if your function version is ``3`` , the component version becomes ``3.0.0`` .
            :param lambda_arn: The ARN of the Lambda function. The ARN must include the version of the function to import. You can't use version aliases like ``$LATEST`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdafunctionrecipesource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
                
                lambda_function_recipe_source_property = greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaFunctionRecipeSourceProperty(
                    component_dependencies={
                        "component_dependencies_key": greengrassv2_mixins.CfnComponentVersionPropsMixin.ComponentDependencyRequirementProperty(
                            dependency_type="dependencyType",
                            version_requirement="versionRequirement"
                        )
                    },
                    component_lambda_parameters=greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaExecutionParametersProperty(
                        environment_variables={
                            "environment_variables_key": "environmentVariables"
                        },
                        event_sources=[greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaEventSourceProperty(
                            topic="topic",
                            type="type"
                        )],
                        exec_args=["execArgs"],
                        input_payload_encoding_type="inputPayloadEncodingType",
                        linux_process_params=greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaLinuxProcessParamsProperty(
                            container_params=greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaContainerParamsProperty(
                                devices=[greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaDeviceMountProperty(
                                    add_group_owner=False,
                                    path="path",
                                    permission="permission"
                                )],
                                memory_size_in_kb=123,
                                mount_ro_sysfs=False,
                                volumes=[greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaVolumeMountProperty(
                                    add_group_owner=False,
                                    destination_path="destinationPath",
                                    permission="permission",
                                    source_path="sourcePath"
                                )]
                            ),
                            isolation_mode="isolationMode"
                        ),
                        max_idle_time_in_seconds=123,
                        max_instances_count=123,
                        max_queue_size=123,
                        pinned=False,
                        status_timeout_in_seconds=123,
                        timeout_in_seconds=123
                    ),
                    component_name="componentName",
                    component_platforms=[greengrassv2_mixins.CfnComponentVersionPropsMixin.ComponentPlatformProperty(
                        attributes={
                            "attributes_key": "attributes"
                        },
                        name="name"
                    )],
                    component_version="componentVersion",
                    lambda_arn="lambdaArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b962c84eeba16492d06c3d29e51e15782eaeb8d55a4e60a9b87128b81ab0d12f)
                check_type(argname="argument component_dependencies", value=component_dependencies, expected_type=type_hints["component_dependencies"])
                check_type(argname="argument component_lambda_parameters", value=component_lambda_parameters, expected_type=type_hints["component_lambda_parameters"])
                check_type(argname="argument component_name", value=component_name, expected_type=type_hints["component_name"])
                check_type(argname="argument component_platforms", value=component_platforms, expected_type=type_hints["component_platforms"])
                check_type(argname="argument component_version", value=component_version, expected_type=type_hints["component_version"])
                check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if component_dependencies is not None:
                self._values["component_dependencies"] = component_dependencies
            if component_lambda_parameters is not None:
                self._values["component_lambda_parameters"] = component_lambda_parameters
            if component_name is not None:
                self._values["component_name"] = component_name
            if component_platforms is not None:
                self._values["component_platforms"] = component_platforms
            if component_version is not None:
                self._values["component_version"] = component_version
            if lambda_arn is not None:
                self._values["lambda_arn"] = lambda_arn

        @builtins.property
        def component_dependencies(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentVersionPropsMixin.ComponentDependencyRequirementProperty"]]]]:
            '''The component versions on which this Lambda function component depends.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdafunctionrecipesource.html#cfn-greengrassv2-componentversion-lambdafunctionrecipesource-componentdependencies
            '''
            result = self._values.get("component_dependencies")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentVersionPropsMixin.ComponentDependencyRequirementProperty"]]]], result)

        @builtins.property
        def component_lambda_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentVersionPropsMixin.LambdaExecutionParametersProperty"]]:
            '''The system and runtime parameters for the Lambda function as it runs on the AWS IoT Greengrass core device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdafunctionrecipesource.html#cfn-greengrassv2-componentversion-lambdafunctionrecipesource-componentlambdaparameters
            '''
            result = self._values.get("component_lambda_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentVersionPropsMixin.LambdaExecutionParametersProperty"]], result)

        @builtins.property
        def component_name(self) -> typing.Optional[builtins.str]:
            '''The name of the component.

            Defaults to the name of the Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdafunctionrecipesource.html#cfn-greengrassv2-componentversion-lambdafunctionrecipesource-componentname
            '''
            result = self._values.get("component_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def component_platforms(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentVersionPropsMixin.ComponentPlatformProperty"]]]]:
            '''The platforms that the component version supports.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdafunctionrecipesource.html#cfn-greengrassv2-componentversion-lambdafunctionrecipesource-componentplatforms
            '''
            result = self._values.get("component_platforms")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentVersionPropsMixin.ComponentPlatformProperty"]]]], result)

        @builtins.property
        def component_version(self) -> typing.Optional[builtins.str]:
            '''The version of the component.

            Defaults to the version of the Lambda function as a semantic version. For example, if your function version is ``3`` , the component version becomes ``3.0.0`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdafunctionrecipesource.html#cfn-greengrassv2-componentversion-lambdafunctionrecipesource-componentversion
            '''
            result = self._values.get("component_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def lambda_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Lambda function.

            The ARN must include the version of the function to import. You can't use version aliases like ``$LATEST`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdafunctionrecipesource.html#cfn-greengrassv2-componentversion-lambdafunctionrecipesource-lambdaarn
            '''
            result = self._values.get("lambda_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaFunctionRecipeSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnComponentVersionPropsMixin.LambdaLinuxProcessParamsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "container_params": "containerParams",
            "isolation_mode": "isolationMode",
        },
    )
    class LambdaLinuxProcessParamsProperty:
        def __init__(
            self,
            *,
            container_params: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentVersionPropsMixin.LambdaContainerParamsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            isolation_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains parameters for a Linux process that contains an AWS Lambda function.

            :param container_params: The parameters for the container in which the Lambda function runs.
            :param isolation_mode: The isolation mode for the process that contains the Lambda function. The process can run in an isolated runtime environment inside the AWS IoT Greengrass container, or as a regular process outside any container. Default: ``GreengrassContainer``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdalinuxprocessparams.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
                
                lambda_linux_process_params_property = greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaLinuxProcessParamsProperty(
                    container_params=greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaContainerParamsProperty(
                        devices=[greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaDeviceMountProperty(
                            add_group_owner=False,
                            path="path",
                            permission="permission"
                        )],
                        memory_size_in_kb=123,
                        mount_ro_sysfs=False,
                        volumes=[greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaVolumeMountProperty(
                            add_group_owner=False,
                            destination_path="destinationPath",
                            permission="permission",
                            source_path="sourcePath"
                        )]
                    ),
                    isolation_mode="isolationMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__36b39a09abb3d306b59503e4d756a25ad7a2771ad4a9ed6558090fb866a4bf5c)
                check_type(argname="argument container_params", value=container_params, expected_type=type_hints["container_params"])
                check_type(argname="argument isolation_mode", value=isolation_mode, expected_type=type_hints["isolation_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if container_params is not None:
                self._values["container_params"] = container_params
            if isolation_mode is not None:
                self._values["isolation_mode"] = isolation_mode

        @builtins.property
        def container_params(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentVersionPropsMixin.LambdaContainerParamsProperty"]]:
            '''The parameters for the container in which the Lambda function runs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdalinuxprocessparams.html#cfn-greengrassv2-componentversion-lambdalinuxprocessparams-containerparams
            '''
            result = self._values.get("container_params")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentVersionPropsMixin.LambdaContainerParamsProperty"]], result)

        @builtins.property
        def isolation_mode(self) -> typing.Optional[builtins.str]:
            '''The isolation mode for the process that contains the Lambda function.

            The process can run in an isolated runtime environment inside the AWS IoT Greengrass container, or as a regular process outside any container.

            Default: ``GreengrassContainer``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdalinuxprocessparams.html#cfn-greengrassv2-componentversion-lambdalinuxprocessparams-isolationmode
            '''
            result = self._values.get("isolation_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaLinuxProcessParamsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnComponentVersionPropsMixin.LambdaVolumeMountProperty",
        jsii_struct_bases=[],
        name_mapping={
            "add_group_owner": "addGroupOwner",
            "destination_path": "destinationPath",
            "permission": "permission",
            "source_path": "sourcePath",
        },
    )
    class LambdaVolumeMountProperty:
        def __init__(
            self,
            *,
            add_group_owner: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            destination_path: typing.Optional[builtins.str] = None,
            permission: typing.Optional[builtins.str] = None,
            source_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about a volume that Linux processes in a container can access.

            When you define a volume, the AWS IoT Greengrass Core software mounts the source files to the destination inside the container.

            :param add_group_owner: Whether or not to add the AWS IoT Greengrass user group as an owner of the volume. Default: ``false``
            :param destination_path: The path to the logical volume in the file system.
            :param permission: The permission to access the volume: read/only ( ``ro`` ) or read/write ( ``rw`` ). Default: ``ro``
            :param source_path: The path to the physical volume in the file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdavolumemount.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
                
                lambda_volume_mount_property = greengrassv2_mixins.CfnComponentVersionPropsMixin.LambdaVolumeMountProperty(
                    add_group_owner=False,
                    destination_path="destinationPath",
                    permission="permission",
                    source_path="sourcePath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2face038fb7858b8dce075d5cee462f3e70d28105ec12176b8ec7e8b9cefcfbd)
                check_type(argname="argument add_group_owner", value=add_group_owner, expected_type=type_hints["add_group_owner"])
                check_type(argname="argument destination_path", value=destination_path, expected_type=type_hints["destination_path"])
                check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
                check_type(argname="argument source_path", value=source_path, expected_type=type_hints["source_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if add_group_owner is not None:
                self._values["add_group_owner"] = add_group_owner
            if destination_path is not None:
                self._values["destination_path"] = destination_path
            if permission is not None:
                self._values["permission"] = permission
            if source_path is not None:
                self._values["source_path"] = source_path

        @builtins.property
        def add_group_owner(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether or not to add the AWS IoT Greengrass user group as an owner of the volume.

            Default: ``false``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdavolumemount.html#cfn-greengrassv2-componentversion-lambdavolumemount-addgroupowner
            '''
            result = self._values.get("add_group_owner")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def destination_path(self) -> typing.Optional[builtins.str]:
            '''The path to the logical volume in the file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdavolumemount.html#cfn-greengrassv2-componentversion-lambdavolumemount-destinationpath
            '''
            result = self._values.get("destination_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def permission(self) -> typing.Optional[builtins.str]:
            '''The permission to access the volume: read/only ( ``ro`` ) or read/write ( ``rw`` ).

            Default: ``ro``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdavolumemount.html#cfn-greengrassv2-componentversion-lambdavolumemount-permission
            '''
            result = self._values.get("permission")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_path(self) -> typing.Optional[builtins.str]:
            '''The path to the physical volume in the file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdavolumemount.html#cfn-greengrassv2-componentversion-lambdavolumemount-sourcepath
            '''
            result = self._values.get("source_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaVolumeMountProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnDeploymentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "components": "components",
        "deployment_name": "deploymentName",
        "deployment_policies": "deploymentPolicies",
        "iot_job_configuration": "iotJobConfiguration",
        "parent_target_arn": "parentTargetArn",
        "tags": "tags",
        "target_arn": "targetArn",
    },
)
class CfnDeploymentMixinProps:
    def __init__(
        self,
        *,
        components: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentPropsMixin.ComponentDeploymentSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        deployment_name: typing.Optional[builtins.str] = None,
        deployment_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentPropsMixin.DeploymentPoliciesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        iot_job_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentPropsMixin.DeploymentIoTJobConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        parent_target_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        target_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDeploymentPropsMixin.

        :param components: The components to deploy. This is a dictionary, where each key is the name of a component, and each key's value is the version and configuration to deploy for that component.
        :param deployment_name: The name of the deployment.
        :param deployment_policies: The deployment policies for the deployment. These policies define how the deployment updates components and handles failure.
        :param iot_job_configuration: The job configuration for the deployment configuration. The job configuration specifies the rollout, timeout, and stop configurations for the deployment configuration.
        :param parent_target_arn: The parent deployment's `ARN <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ for a subdeployment.
        :param tags: Application-specific metadata to attach to the deployment. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tag your AWS IoT Greengrass Version 2 resources <https://docs.aws.amazon.com/greengrass/v2/developerguide/tag-resources.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }
        :param target_arn: The ARN of the target AWS IoT thing or thing group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-deployment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
            
            # rate_increase_criteria: Any
            
            cfn_deployment_mixin_props = greengrassv2_mixins.CfnDeploymentMixinProps(
                components={
                    "components_key": greengrassv2_mixins.CfnDeploymentPropsMixin.ComponentDeploymentSpecificationProperty(
                        component_version="componentVersion",
                        configuration_update=greengrassv2_mixins.CfnDeploymentPropsMixin.ComponentConfigurationUpdateProperty(
                            merge="merge",
                            reset=["reset"]
                        ),
                        run_with=greengrassv2_mixins.CfnDeploymentPropsMixin.ComponentRunWithProperty(
                            posix_user="posixUser",
                            system_resource_limits=greengrassv2_mixins.CfnDeploymentPropsMixin.SystemResourceLimitsProperty(
                                cpus=123,
                                memory=123
                            ),
                            windows_user="windowsUser"
                        )
                    )
                },
                deployment_name="deploymentName",
                deployment_policies=greengrassv2_mixins.CfnDeploymentPropsMixin.DeploymentPoliciesProperty(
                    component_update_policy=greengrassv2_mixins.CfnDeploymentPropsMixin.DeploymentComponentUpdatePolicyProperty(
                        action="action",
                        timeout_in_seconds=123
                    ),
                    configuration_validation_policy=greengrassv2_mixins.CfnDeploymentPropsMixin.DeploymentConfigurationValidationPolicyProperty(
                        timeout_in_seconds=123
                    ),
                    failure_handling_policy="failureHandlingPolicy"
                ),
                iot_job_configuration=greengrassv2_mixins.CfnDeploymentPropsMixin.DeploymentIoTJobConfigurationProperty(
                    abort_config=greengrassv2_mixins.CfnDeploymentPropsMixin.IoTJobAbortConfigProperty(
                        criteria_list=[greengrassv2_mixins.CfnDeploymentPropsMixin.IoTJobAbortCriteriaProperty(
                            action="action",
                            failure_type="failureType",
                            min_number_of_executed_things=123,
                            threshold_percentage=123
                        )]
                    ),
                    job_executions_rollout_config=greengrassv2_mixins.CfnDeploymentPropsMixin.IoTJobExecutionsRolloutConfigProperty(
                        exponential_rate=greengrassv2_mixins.CfnDeploymentPropsMixin.IoTJobExponentialRolloutRateProperty(
                            base_rate_per_minute=123,
                            increment_factor=123,
                            rate_increase_criteria=rate_increase_criteria
                        ),
                        maximum_per_minute=123
                    ),
                    timeout_config=greengrassv2_mixins.CfnDeploymentPropsMixin.IoTJobTimeoutConfigProperty(
                        in_progress_timeout_in_minutes=123
                    )
                ),
                parent_target_arn="parentTargetArn",
                tags={
                    "tags_key": "tags"
                },
                target_arn="targetArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da350da614a5bfa776b454fba2fd898e37dc0643e880c821141a7ab6216e091e)
            check_type(argname="argument components", value=components, expected_type=type_hints["components"])
            check_type(argname="argument deployment_name", value=deployment_name, expected_type=type_hints["deployment_name"])
            check_type(argname="argument deployment_policies", value=deployment_policies, expected_type=type_hints["deployment_policies"])
            check_type(argname="argument iot_job_configuration", value=iot_job_configuration, expected_type=type_hints["iot_job_configuration"])
            check_type(argname="argument parent_target_arn", value=parent_target_arn, expected_type=type_hints["parent_target_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if components is not None:
            self._values["components"] = components
        if deployment_name is not None:
            self._values["deployment_name"] = deployment_name
        if deployment_policies is not None:
            self._values["deployment_policies"] = deployment_policies
        if iot_job_configuration is not None:
            self._values["iot_job_configuration"] = iot_job_configuration
        if parent_target_arn is not None:
            self._values["parent_target_arn"] = parent_target_arn
        if tags is not None:
            self._values["tags"] = tags
        if target_arn is not None:
            self._values["target_arn"] = target_arn

    @builtins.property
    def components(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.ComponentDeploymentSpecificationProperty"]]]]:
        '''The components to deploy.

        This is a dictionary, where each key is the name of a component, and each key's value is the version and configuration to deploy for that component.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-deployment.html#cfn-greengrassv2-deployment-components
        '''
        result = self._values.get("components")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.ComponentDeploymentSpecificationProperty"]]]], result)

    @builtins.property
    def deployment_name(self) -> typing.Optional[builtins.str]:
        '''The name of the deployment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-deployment.html#cfn-greengrassv2-deployment-deploymentname
        '''
        result = self._values.get("deployment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_policies(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.DeploymentPoliciesProperty"]]:
        '''The deployment policies for the deployment.

        These policies define how the deployment updates components and handles failure.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-deployment.html#cfn-greengrassv2-deployment-deploymentpolicies
        '''
        result = self._values.get("deployment_policies")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.DeploymentPoliciesProperty"]], result)

    @builtins.property
    def iot_job_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.DeploymentIoTJobConfigurationProperty"]]:
        '''The job configuration for the deployment configuration.

        The job configuration specifies the rollout, timeout, and stop configurations for the deployment configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-deployment.html#cfn-greengrassv2-deployment-iotjobconfiguration
        '''
        result = self._values.get("iot_job_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.DeploymentIoTJobConfigurationProperty"]], result)

    @builtins.property
    def parent_target_arn(self) -> typing.Optional[builtins.str]:
        '''The parent deployment's `ARN <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ for a subdeployment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-deployment.html#cfn-greengrassv2-deployment-parenttargetarn
        '''
        result = self._values.get("parent_target_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Application-specific metadata to attach to the deployment.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tag your AWS IoT Greengrass Version 2 resources <https://docs.aws.amazon.com/greengrass/v2/developerguide/tag-resources.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-deployment.html#cfn-greengrassv2-deployment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def target_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the target AWS IoT thing or thing group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-deployment.html#cfn-greengrassv2-deployment-targetarn
        '''
        result = self._values.get("target_arn")
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
    jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnDeploymentPropsMixin",
):
    '''Creates a continuous deployment for a target, which is a AWS IoT Greengrass core device or group of core devices.

    When you add a new core device to a group of core devices that has a deployment, AWS IoT Greengrass deploys that group's deployment to the new device.

    You can define one deployment for each target. When you create a new deployment for a target that has an existing deployment, you replace the previous deployment. AWS IoT Greengrass applies the new deployment to the target devices.

    You can only add, update, or delete up to 10 deployments at a time to a single target.

    Every deployment has a revision number that indicates how many deployment revisions you define for a target. Use this operation to create a new revision of an existing deployment. This operation returns the revision number of the new deployment when you create it.

    For more information, see the `Create deployments <https://docs.aws.amazon.com/greengrass/v2/developerguide/create-deployments.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* .
    .. epigraph::

       Deployment resources are deleted when you delete stacks. To keep the deployments in a stack, you must specify ``"DeletionPolicy": "Retain"`` on each deployment resource in the stack template that you want to keep. For more information, see `DeletionPolicy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html>`_ .

       You can only delete up to 10 deployment resources at a time. If you delete more than 10 resources, you receive an error.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-deployment.html
    :cloudformationResource: AWS::GreengrassV2::Deployment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
        
        # rate_increase_criteria: Any
        
        cfn_deployment_props_mixin = greengrassv2_mixins.CfnDeploymentPropsMixin(greengrassv2_mixins.CfnDeploymentMixinProps(
            components={
                "components_key": greengrassv2_mixins.CfnDeploymentPropsMixin.ComponentDeploymentSpecificationProperty(
                    component_version="componentVersion",
                    configuration_update=greengrassv2_mixins.CfnDeploymentPropsMixin.ComponentConfigurationUpdateProperty(
                        merge="merge",
                        reset=["reset"]
                    ),
                    run_with=greengrassv2_mixins.CfnDeploymentPropsMixin.ComponentRunWithProperty(
                        posix_user="posixUser",
                        system_resource_limits=greengrassv2_mixins.CfnDeploymentPropsMixin.SystemResourceLimitsProperty(
                            cpus=123,
                            memory=123
                        ),
                        windows_user="windowsUser"
                    )
                )
            },
            deployment_name="deploymentName",
            deployment_policies=greengrassv2_mixins.CfnDeploymentPropsMixin.DeploymentPoliciesProperty(
                component_update_policy=greengrassv2_mixins.CfnDeploymentPropsMixin.DeploymentComponentUpdatePolicyProperty(
                    action="action",
                    timeout_in_seconds=123
                ),
                configuration_validation_policy=greengrassv2_mixins.CfnDeploymentPropsMixin.DeploymentConfigurationValidationPolicyProperty(
                    timeout_in_seconds=123
                ),
                failure_handling_policy="failureHandlingPolicy"
            ),
            iot_job_configuration=greengrassv2_mixins.CfnDeploymentPropsMixin.DeploymentIoTJobConfigurationProperty(
                abort_config=greengrassv2_mixins.CfnDeploymentPropsMixin.IoTJobAbortConfigProperty(
                    criteria_list=[greengrassv2_mixins.CfnDeploymentPropsMixin.IoTJobAbortCriteriaProperty(
                        action="action",
                        failure_type="failureType",
                        min_number_of_executed_things=123,
                        threshold_percentage=123
                    )]
                ),
                job_executions_rollout_config=greengrassv2_mixins.CfnDeploymentPropsMixin.IoTJobExecutionsRolloutConfigProperty(
                    exponential_rate=greengrassv2_mixins.CfnDeploymentPropsMixin.IoTJobExponentialRolloutRateProperty(
                        base_rate_per_minute=123,
                        increment_factor=123,
                        rate_increase_criteria=rate_increase_criteria
                    ),
                    maximum_per_minute=123
                ),
                timeout_config=greengrassv2_mixins.CfnDeploymentPropsMixin.IoTJobTimeoutConfigProperty(
                    in_progress_timeout_in_minutes=123
                )
            ),
            parent_target_arn="parentTargetArn",
            tags={
                "tags_key": "tags"
            },
            target_arn="targetArn"
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
        '''Create a mixin to apply properties to ``AWS::GreengrassV2::Deployment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2641c92c1340bf057e16dc42e381112b2397f037c8235d85a57d4c9935e2cf2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d301051c40f1c24677f2c32d6edab596ac8e052f2743f3e14e337cfeb0c29572)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__231f8d93504e2893f7cc9b0608b581b4dae3db46361c92607acbe86172cd918d)
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
        jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnDeploymentPropsMixin.ComponentConfigurationUpdateProperty",
        jsii_struct_bases=[],
        name_mapping={"merge": "merge", "reset": "reset"},
    )
    class ComponentConfigurationUpdateProperty:
        def __init__(
            self,
            *,
            merge: typing.Optional[builtins.str] = None,
            reset: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Contains information about a deployment's update to a component's configuration on AWS IoT Greengrass core devices.

            For more information, see `Update component configurations <https://docs.aws.amazon.com/greengrass/v2/developerguide/update-component-configurations.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

            :param merge: A serialized JSON string that contains the configuration object to merge to target devices. The core device merges this configuration with the component's existing configuration. If this is the first time a component deploys on a device, the core device merges this configuration with the component's default configuration. This means that the core device keeps it's existing configuration for keys and values that you don't specify in this object. For more information, see `Merge configuration updates <https://docs.aws.amazon.com/greengrass/v2/developerguide/update-component-configurations.html#merge-configuration-update>`_ in the *AWS IoT Greengrass V2 Developer Guide* .
            :param reset: The list of configuration nodes to reset to default values on target devices. Use JSON pointers to specify each node to reset. JSON pointers start with a forward slash ( ``/`` ) and use forward slashes to separate the key for each level in the object. For more information, see the `JSON pointer specification <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc6901>`_ and `Reset configuration updates <https://docs.aws.amazon.com/greengrass/v2/developerguide/update-component-configurations.html#reset-configuration-update>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-componentconfigurationupdate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
                
                component_configuration_update_property = greengrassv2_mixins.CfnDeploymentPropsMixin.ComponentConfigurationUpdateProperty(
                    merge="merge",
                    reset=["reset"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__195e6decfe7525e93fe66c73b3ba0304a97216a1f854407811c9e1f4bf3a83c7)
                check_type(argname="argument merge", value=merge, expected_type=type_hints["merge"])
                check_type(argname="argument reset", value=reset, expected_type=type_hints["reset"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if merge is not None:
                self._values["merge"] = merge
            if reset is not None:
                self._values["reset"] = reset

        @builtins.property
        def merge(self) -> typing.Optional[builtins.str]:
            '''A serialized JSON string that contains the configuration object to merge to target devices.

            The core device merges this configuration with the component's existing configuration. If this is the first time a component deploys on a device, the core device merges this configuration with the component's default configuration. This means that the core device keeps it's existing configuration for keys and values that you don't specify in this object. For more information, see `Merge configuration updates <https://docs.aws.amazon.com/greengrass/v2/developerguide/update-component-configurations.html#merge-configuration-update>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-componentconfigurationupdate.html#cfn-greengrassv2-deployment-componentconfigurationupdate-merge
            '''
            result = self._values.get("merge")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def reset(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of configuration nodes to reset to default values on target devices.

            Use JSON pointers to specify each node to reset. JSON pointers start with a forward slash ( ``/`` ) and use forward slashes to separate the key for each level in the object. For more information, see the `JSON pointer specification <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc6901>`_ and `Reset configuration updates <https://docs.aws.amazon.com/greengrass/v2/developerguide/update-component-configurations.html#reset-configuration-update>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-componentconfigurationupdate.html#cfn-greengrassv2-deployment-componentconfigurationupdate-reset
            '''
            result = self._values.get("reset")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentConfigurationUpdateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnDeploymentPropsMixin.ComponentDeploymentSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component_version": "componentVersion",
            "configuration_update": "configurationUpdate",
            "run_with": "runWith",
        },
    )
    class ComponentDeploymentSpecificationProperty:
        def __init__(
            self,
            *,
            component_version: typing.Optional[builtins.str] = None,
            configuration_update: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentPropsMixin.ComponentConfigurationUpdateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            run_with: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentPropsMixin.ComponentRunWithProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information about a component to deploy.

            :param component_version: The version of the component.
            :param configuration_update: The configuration updates to deploy for the component. You can define reset updates and merge updates. A reset updates the keys that you specify to the default configuration for the component. A merge updates the core device's component configuration with the keys and values that you specify. The AWS IoT Greengrass Core software applies reset updates before it applies merge updates. For more information, see `Update component configuration <https://docs.aws.amazon.com/greengrass/v2/developerguide/update-component-configurations.html>`_ .
            :param run_with: The system user and group that the software uses to run component processes on the core device. If you omit this parameter, the software uses the system user and group that you configure for the core device. For more information, see `Configure the user and group that run components <https://docs.aws.amazon.com/greengrass/v2/developerguide/configure-greengrass-core-v2.html#configure-component-user>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-componentdeploymentspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
                
                component_deployment_specification_property = greengrassv2_mixins.CfnDeploymentPropsMixin.ComponentDeploymentSpecificationProperty(
                    component_version="componentVersion",
                    configuration_update=greengrassv2_mixins.CfnDeploymentPropsMixin.ComponentConfigurationUpdateProperty(
                        merge="merge",
                        reset=["reset"]
                    ),
                    run_with=greengrassv2_mixins.CfnDeploymentPropsMixin.ComponentRunWithProperty(
                        posix_user="posixUser",
                        system_resource_limits=greengrassv2_mixins.CfnDeploymentPropsMixin.SystemResourceLimitsProperty(
                            cpus=123,
                            memory=123
                        ),
                        windows_user="windowsUser"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__55e4800c05b929de121a258acdfbb5be1897bf140fc2a5b308ec8fa3727f52ee)
                check_type(argname="argument component_version", value=component_version, expected_type=type_hints["component_version"])
                check_type(argname="argument configuration_update", value=configuration_update, expected_type=type_hints["configuration_update"])
                check_type(argname="argument run_with", value=run_with, expected_type=type_hints["run_with"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if component_version is not None:
                self._values["component_version"] = component_version
            if configuration_update is not None:
                self._values["configuration_update"] = configuration_update
            if run_with is not None:
                self._values["run_with"] = run_with

        @builtins.property
        def component_version(self) -> typing.Optional[builtins.str]:
            '''The version of the component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-componentdeploymentspecification.html#cfn-greengrassv2-deployment-componentdeploymentspecification-componentversion
            '''
            result = self._values.get("component_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def configuration_update(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.ComponentConfigurationUpdateProperty"]]:
            '''The configuration updates to deploy for the component.

            You can define reset updates and merge updates. A reset updates the keys that you specify to the default configuration for the component. A merge updates the core device's component configuration with the keys and values that you specify. The AWS IoT Greengrass Core software applies reset updates before it applies merge updates. For more information, see `Update component configuration <https://docs.aws.amazon.com/greengrass/v2/developerguide/update-component-configurations.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-componentdeploymentspecification.html#cfn-greengrassv2-deployment-componentdeploymentspecification-configurationupdate
            '''
            result = self._values.get("configuration_update")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.ComponentConfigurationUpdateProperty"]], result)

        @builtins.property
        def run_with(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.ComponentRunWithProperty"]]:
            '''The system user and group that the  software uses to run component processes on the core device.

            If you omit this parameter, the  software uses the system user and group that you configure for the core device. For more information, see `Configure the user and group that run components <https://docs.aws.amazon.com/greengrass/v2/developerguide/configure-greengrass-core-v2.html#configure-component-user>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-componentdeploymentspecification.html#cfn-greengrassv2-deployment-componentdeploymentspecification-runwith
            '''
            result = self._values.get("run_with")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.ComponentRunWithProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentDeploymentSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnDeploymentPropsMixin.ComponentRunWithProperty",
        jsii_struct_bases=[],
        name_mapping={
            "posix_user": "posixUser",
            "system_resource_limits": "systemResourceLimits",
            "windows_user": "windowsUser",
        },
    )
    class ComponentRunWithProperty:
        def __init__(
            self,
            *,
            posix_user: typing.Optional[builtins.str] = None,
            system_resource_limits: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentPropsMixin.SystemResourceLimitsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            windows_user: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information system user and group that the AWS IoT Greengrass Core software uses to run component processes on the core device.

            For more information, see `Configure the user and group that run components <https://docs.aws.amazon.com/greengrass/v2/developerguide/configure-greengrass-core-v2.html#configure-component-user>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

            :param posix_user: The POSIX system user and (optional) group to use to run this component. Specify the user and group separated by a colon ( ``:`` ) in the following format: ``user:group`` . The group is optional. If you don't specify a group, the AWS IoT Greengrass Core software uses the primary user for the group.
            :param system_resource_limits: The system resource limits to apply to this component's process on the core device. AWS IoT Greengrass supports this feature only on Linux core devices. If you omit this parameter, the AWS IoT Greengrass Core software uses the default system resource limits that you configure on the AWS IoT Greengrass nucleus component. For more information, see `Configure system resource limits for components <https://docs.aws.amazon.com/greengrass/v2/developerguide/configure-greengrass-core-v2.html#configure-component-system-resource-limits>`_ .
            :param windows_user: The Windows user to use to run this component on Windows core devices. The user must exist on each Windows core device, and its name and password must be in the LocalSystem account's Credentials Manager instance. If you omit this parameter, the AWS IoT Greengrass Core software uses the default Windows user that you configure on the AWS IoT Greengrass nucleus component. For more information, see `Configure the user and group that run components <https://docs.aws.amazon.com/greengrass/v2/developerguide/configure-greengrass-core-v2.html#configure-component-user>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-componentrunwith.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
                
                component_run_with_property = greengrassv2_mixins.CfnDeploymentPropsMixin.ComponentRunWithProperty(
                    posix_user="posixUser",
                    system_resource_limits=greengrassv2_mixins.CfnDeploymentPropsMixin.SystemResourceLimitsProperty(
                        cpus=123,
                        memory=123
                    ),
                    windows_user="windowsUser"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__619897f7da3f9df0c4588ba74f36001aa8822fd50d1a253033f0a9d276524f03)
                check_type(argname="argument posix_user", value=posix_user, expected_type=type_hints["posix_user"])
                check_type(argname="argument system_resource_limits", value=system_resource_limits, expected_type=type_hints["system_resource_limits"])
                check_type(argname="argument windows_user", value=windows_user, expected_type=type_hints["windows_user"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if posix_user is not None:
                self._values["posix_user"] = posix_user
            if system_resource_limits is not None:
                self._values["system_resource_limits"] = system_resource_limits
            if windows_user is not None:
                self._values["windows_user"] = windows_user

        @builtins.property
        def posix_user(self) -> typing.Optional[builtins.str]:
            '''The POSIX system user and (optional) group to use to run this component.

            Specify the user and group separated by a colon ( ``:`` ) in the following format: ``user:group`` . The group is optional. If you don't specify a group, the AWS IoT Greengrass Core software uses the primary user for the group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-componentrunwith.html#cfn-greengrassv2-deployment-componentrunwith-posixuser
            '''
            result = self._values.get("posix_user")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def system_resource_limits(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.SystemResourceLimitsProperty"]]:
            '''The system resource limits to apply to this component's process on the core device.

            AWS IoT Greengrass supports this feature only on Linux core devices.

            If you omit this parameter, the AWS IoT Greengrass Core software uses the default system resource limits that you configure on the AWS IoT Greengrass nucleus component. For more information, see `Configure system resource limits for components <https://docs.aws.amazon.com/greengrass/v2/developerguide/configure-greengrass-core-v2.html#configure-component-system-resource-limits>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-componentrunwith.html#cfn-greengrassv2-deployment-componentrunwith-systemresourcelimits
            '''
            result = self._values.get("system_resource_limits")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.SystemResourceLimitsProperty"]], result)

        @builtins.property
        def windows_user(self) -> typing.Optional[builtins.str]:
            '''The Windows user to use to run this component on Windows core devices.

            The user must exist on each Windows core device, and its name and password must be in the LocalSystem account's Credentials Manager instance.

            If you omit this parameter, the AWS IoT Greengrass Core software uses the default Windows user that you configure on the AWS IoT Greengrass nucleus component. For more information, see `Configure the user and group that run components <https://docs.aws.amazon.com/greengrass/v2/developerguide/configure-greengrass-core-v2.html#configure-component-user>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-componentrunwith.html#cfn-greengrassv2-deployment-componentrunwith-windowsuser
            '''
            result = self._values.get("windows_user")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentRunWithProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnDeploymentPropsMixin.DeploymentComponentUpdatePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action", "timeout_in_seconds": "timeoutInSeconds"},
    )
    class DeploymentComponentUpdatePolicyProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            timeout_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains information about a deployment's policy that defines when components are safe to update.

            Each component on a device can report whether or not it's ready to update. After a component and its dependencies are ready, they can apply the update in the deployment. You can configure whether or not the deployment notifies components of an update and waits for a response. You specify the amount of time each component has to respond to the update notification.

            :param action: Whether or not to notify components and wait for components to become safe to update. Choose from the following options: - ``NOTIFY_COMPONENTS`` – The deployment notifies each component before it stops and updates that component. Components can use the `SubscribeToComponentUpdates <https://docs.aws.amazon.com/greengrass/v2/developerguide/interprocess-communication.html#ipc-operation-subscribetocomponentupdates>`_ IPC operation to receive these notifications. Then, components can respond with the `DeferComponentUpdate <https://docs.aws.amazon.com/greengrass/v2/developerguide/interprocess-communication.html#ipc-operation-defercomponentupdate>`_ IPC operation. For more information, see the `Create deployments <https://docs.aws.amazon.com/greengrass/v2/developerguide/create-deployments.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* . - ``SKIP_NOTIFY_COMPONENTS`` – The deployment doesn't notify components or wait for them to be safe to update. Default: ``NOTIFY_COMPONENTS``
            :param timeout_in_seconds: The amount of time in seconds that each component on a device has to report that it's safe to update. If the component waits for longer than this timeout, then the deployment proceeds on the device. Default: ``60``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentcomponentupdatepolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
                
                deployment_component_update_policy_property = greengrassv2_mixins.CfnDeploymentPropsMixin.DeploymentComponentUpdatePolicyProperty(
                    action="action",
                    timeout_in_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c1ac0a6808f46598d10b666ea5c0261a97467f049404137f4190a991da85766b)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument timeout_in_seconds", value=timeout_in_seconds, expected_type=type_hints["timeout_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if timeout_in_seconds is not None:
                self._values["timeout_in_seconds"] = timeout_in_seconds

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''Whether or not to notify components and wait for components to become safe to update.

            Choose from the following options:

            - ``NOTIFY_COMPONENTS`` – The deployment notifies each component before it stops and updates that component. Components can use the `SubscribeToComponentUpdates <https://docs.aws.amazon.com/greengrass/v2/developerguide/interprocess-communication.html#ipc-operation-subscribetocomponentupdates>`_ IPC operation to receive these notifications. Then, components can respond with the `DeferComponentUpdate <https://docs.aws.amazon.com/greengrass/v2/developerguide/interprocess-communication.html#ipc-operation-defercomponentupdate>`_ IPC operation. For more information, see the `Create deployments <https://docs.aws.amazon.com/greengrass/v2/developerguide/create-deployments.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* .
            - ``SKIP_NOTIFY_COMPONENTS`` – The deployment doesn't notify components or wait for them to be safe to update.

            Default: ``NOTIFY_COMPONENTS``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentcomponentupdatepolicy.html#cfn-greengrassv2-deployment-deploymentcomponentupdatepolicy-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The amount of time in seconds that each component on a device has to report that it's safe to update.

            If the component waits for longer than this timeout, then the deployment proceeds on the device.

            Default: ``60``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentcomponentupdatepolicy.html#cfn-greengrassv2-deployment-deploymentcomponentupdatepolicy-timeoutinseconds
            '''
            result = self._values.get("timeout_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentComponentUpdatePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnDeploymentPropsMixin.DeploymentConfigurationValidationPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"timeout_in_seconds": "timeoutInSeconds"},
    )
    class DeploymentConfigurationValidationPolicyProperty:
        def __init__(
            self,
            *,
            timeout_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains information about how long a component on a core device can validate its configuration updates before it times out.

            Components can use the `SubscribeToValidateConfigurationUpdates <https://docs.aws.amazon.com/greengrass/v2/developerguide/interprocess-communication.html#ipc-operation-subscribetovalidateconfigurationupdates>`_ IPC operation to receive notifications when a deployment specifies a configuration update. Then, components can respond with the `SendConfigurationValidityReport <https://docs.aws.amazon.com/greengrass/v2/developerguide/interprocess-communication.html#ipc-operation-sendconfigurationvalidityreport>`_ IPC operation. For more information, see the `Create deployments <https://docs.aws.amazon.com/greengrass/v2/developerguide/create-deployments.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

            :param timeout_in_seconds: The amount of time in seconds that a component can validate its configuration updates. If the validation time exceeds this timeout, then the deployment proceeds for the device. Default: ``30``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentconfigurationvalidationpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
                
                deployment_configuration_validation_policy_property = greengrassv2_mixins.CfnDeploymentPropsMixin.DeploymentConfigurationValidationPolicyProperty(
                    timeout_in_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fa868f526d8a831d908cafc69ae913e06af90fbdcfc908b8adaf09a509a5a191)
                check_type(argname="argument timeout_in_seconds", value=timeout_in_seconds, expected_type=type_hints["timeout_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if timeout_in_seconds is not None:
                self._values["timeout_in_seconds"] = timeout_in_seconds

        @builtins.property
        def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The amount of time in seconds that a component can validate its configuration updates.

            If the validation time exceeds this timeout, then the deployment proceeds for the device.

            Default: ``30``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentconfigurationvalidationpolicy.html#cfn-greengrassv2-deployment-deploymentconfigurationvalidationpolicy-timeoutinseconds
            '''
            result = self._values.get("timeout_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentConfigurationValidationPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnDeploymentPropsMixin.DeploymentIoTJobConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "abort_config": "abortConfig",
            "job_executions_rollout_config": "jobExecutionsRolloutConfig",
            "timeout_config": "timeoutConfig",
        },
    )
    class DeploymentIoTJobConfigurationProperty:
        def __init__(
            self,
            *,
            abort_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentPropsMixin.IoTJobAbortConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            job_executions_rollout_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentPropsMixin.IoTJobExecutionsRolloutConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            timeout_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentPropsMixin.IoTJobTimeoutConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information about an AWS IoT job configuration.

            :param abort_config: The stop configuration for the job. This configuration defines when and how to stop a job rollout.
            :param job_executions_rollout_config: The rollout configuration for the job. This configuration defines the rate at which the job rolls out to the fleet of target devices.
            :param timeout_config: The timeout configuration for the job. This configuration defines the amount of time each device has to complete the job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentiotjobconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
                
                # rate_increase_criteria: Any
                
                deployment_io_tJob_configuration_property = greengrassv2_mixins.CfnDeploymentPropsMixin.DeploymentIoTJobConfigurationProperty(
                    abort_config=greengrassv2_mixins.CfnDeploymentPropsMixin.IoTJobAbortConfigProperty(
                        criteria_list=[greengrassv2_mixins.CfnDeploymentPropsMixin.IoTJobAbortCriteriaProperty(
                            action="action",
                            failure_type="failureType",
                            min_number_of_executed_things=123,
                            threshold_percentage=123
                        )]
                    ),
                    job_executions_rollout_config=greengrassv2_mixins.CfnDeploymentPropsMixin.IoTJobExecutionsRolloutConfigProperty(
                        exponential_rate=greengrassv2_mixins.CfnDeploymentPropsMixin.IoTJobExponentialRolloutRateProperty(
                            base_rate_per_minute=123,
                            increment_factor=123,
                            rate_increase_criteria=rate_increase_criteria
                        ),
                        maximum_per_minute=123
                    ),
                    timeout_config=greengrassv2_mixins.CfnDeploymentPropsMixin.IoTJobTimeoutConfigProperty(
                        in_progress_timeout_in_minutes=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c39a110096d914eacd5713bbc50e7976f0d2219cbd4757a089e11a1c4b97e82e)
                check_type(argname="argument abort_config", value=abort_config, expected_type=type_hints["abort_config"])
                check_type(argname="argument job_executions_rollout_config", value=job_executions_rollout_config, expected_type=type_hints["job_executions_rollout_config"])
                check_type(argname="argument timeout_config", value=timeout_config, expected_type=type_hints["timeout_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if abort_config is not None:
                self._values["abort_config"] = abort_config
            if job_executions_rollout_config is not None:
                self._values["job_executions_rollout_config"] = job_executions_rollout_config
            if timeout_config is not None:
                self._values["timeout_config"] = timeout_config

        @builtins.property
        def abort_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.IoTJobAbortConfigProperty"]]:
            '''The stop configuration for the job.

            This configuration defines when and how to stop a job rollout.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentiotjobconfiguration.html#cfn-greengrassv2-deployment-deploymentiotjobconfiguration-abortconfig
            '''
            result = self._values.get("abort_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.IoTJobAbortConfigProperty"]], result)

        @builtins.property
        def job_executions_rollout_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.IoTJobExecutionsRolloutConfigProperty"]]:
            '''The rollout configuration for the job.

            This configuration defines the rate at which the job rolls out to the fleet of target devices.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentiotjobconfiguration.html#cfn-greengrassv2-deployment-deploymentiotjobconfiguration-jobexecutionsrolloutconfig
            '''
            result = self._values.get("job_executions_rollout_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.IoTJobExecutionsRolloutConfigProperty"]], result)

        @builtins.property
        def timeout_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.IoTJobTimeoutConfigProperty"]]:
            '''The timeout configuration for the job.

            This configuration defines the amount of time each device has to complete the job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentiotjobconfiguration.html#cfn-greengrassv2-deployment-deploymentiotjobconfiguration-timeoutconfig
            '''
            result = self._values.get("timeout_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.IoTJobTimeoutConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentIoTJobConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnDeploymentPropsMixin.DeploymentPoliciesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component_update_policy": "componentUpdatePolicy",
            "configuration_validation_policy": "configurationValidationPolicy",
            "failure_handling_policy": "failureHandlingPolicy",
        },
    )
    class DeploymentPoliciesProperty:
        def __init__(
            self,
            *,
            component_update_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentPropsMixin.DeploymentComponentUpdatePolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            configuration_validation_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentPropsMixin.DeploymentConfigurationValidationPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            failure_handling_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about policies that define how a deployment updates components and handles failure.

            :param component_update_policy: The component update policy for the configuration deployment. This policy defines when it's safe to deploy the configuration to devices.
            :param configuration_validation_policy: The configuration validation policy for the configuration deployment. This policy defines how long each component has to validate its configure updates.
            :param failure_handling_policy: The failure handling policy for the configuration deployment. This policy defines what to do if the deployment fails. Default: ``ROLLBACK``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentpolicies.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
                
                deployment_policies_property = greengrassv2_mixins.CfnDeploymentPropsMixin.DeploymentPoliciesProperty(
                    component_update_policy=greengrassv2_mixins.CfnDeploymentPropsMixin.DeploymentComponentUpdatePolicyProperty(
                        action="action",
                        timeout_in_seconds=123
                    ),
                    configuration_validation_policy=greengrassv2_mixins.CfnDeploymentPropsMixin.DeploymentConfigurationValidationPolicyProperty(
                        timeout_in_seconds=123
                    ),
                    failure_handling_policy="failureHandlingPolicy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4b5c29279a641ed80aed59019e2bda5a2df1aec6ae03f190d9a6c02a03da7c7c)
                check_type(argname="argument component_update_policy", value=component_update_policy, expected_type=type_hints["component_update_policy"])
                check_type(argname="argument configuration_validation_policy", value=configuration_validation_policy, expected_type=type_hints["configuration_validation_policy"])
                check_type(argname="argument failure_handling_policy", value=failure_handling_policy, expected_type=type_hints["failure_handling_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if component_update_policy is not None:
                self._values["component_update_policy"] = component_update_policy
            if configuration_validation_policy is not None:
                self._values["configuration_validation_policy"] = configuration_validation_policy
            if failure_handling_policy is not None:
                self._values["failure_handling_policy"] = failure_handling_policy

        @builtins.property
        def component_update_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.DeploymentComponentUpdatePolicyProperty"]]:
            '''The component update policy for the configuration deployment.

            This policy defines when it's safe to deploy the configuration to devices.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentpolicies.html#cfn-greengrassv2-deployment-deploymentpolicies-componentupdatepolicy
            '''
            result = self._values.get("component_update_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.DeploymentComponentUpdatePolicyProperty"]], result)

        @builtins.property
        def configuration_validation_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.DeploymentConfigurationValidationPolicyProperty"]]:
            '''The configuration validation policy for the configuration deployment.

            This policy defines how long each component has to validate its configure updates.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentpolicies.html#cfn-greengrassv2-deployment-deploymentpolicies-configurationvalidationpolicy
            '''
            result = self._values.get("configuration_validation_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.DeploymentConfigurationValidationPolicyProperty"]], result)

        @builtins.property
        def failure_handling_policy(self) -> typing.Optional[builtins.str]:
            '''The failure handling policy for the configuration deployment. This policy defines what to do if the deployment fails.

            Default: ``ROLLBACK``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentpolicies.html#cfn-greengrassv2-deployment-deploymentpolicies-failurehandlingpolicy
            '''
            result = self._values.get("failure_handling_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentPoliciesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnDeploymentPropsMixin.IoTJobAbortConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"criteria_list": "criteriaList"},
    )
    class IoTJobAbortConfigProperty:
        def __init__(
            self,
            *,
            criteria_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentPropsMixin.IoTJobAbortCriteriaProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Contains a list of criteria that define when and how to cancel a configuration deployment.

            :param criteria_list: The list of criteria that define when and how to cancel the configuration deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobabortconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
                
                io_tJob_abort_config_property = greengrassv2_mixins.CfnDeploymentPropsMixin.IoTJobAbortConfigProperty(
                    criteria_list=[greengrassv2_mixins.CfnDeploymentPropsMixin.IoTJobAbortCriteriaProperty(
                        action="action",
                        failure_type="failureType",
                        min_number_of_executed_things=123,
                        threshold_percentage=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__49aab6e06e9b05e4b98495893af7f7e57bbb637a5183c8c9860ab2a76de4850a)
                check_type(argname="argument criteria_list", value=criteria_list, expected_type=type_hints["criteria_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if criteria_list is not None:
                self._values["criteria_list"] = criteria_list

        @builtins.property
        def criteria_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.IoTJobAbortCriteriaProperty"]]]]:
            '''The list of criteria that define when and how to cancel the configuration deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobabortconfig.html#cfn-greengrassv2-deployment-iotjobabortconfig-criterialist
            '''
            result = self._values.get("criteria_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.IoTJobAbortCriteriaProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IoTJobAbortConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnDeploymentPropsMixin.IoTJobAbortCriteriaProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "failure_type": "failureType",
            "min_number_of_executed_things": "minNumberOfExecutedThings",
            "threshold_percentage": "thresholdPercentage",
        },
    )
    class IoTJobAbortCriteriaProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            failure_type: typing.Optional[builtins.str] = None,
            min_number_of_executed_things: typing.Optional[jsii.Number] = None,
            threshold_percentage: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains criteria that define when and how to cancel a job.

            The deployment stops if the following conditions are true:

            - The number of things that receive the deployment exceeds the ``minNumberOfExecutedThings`` .
            - The percentage of failures with type ``failureType`` exceeds the ``thresholdPercentage`` .

            :param action: The action to perform when the criteria are met.
            :param failure_type: The type of job deployment failure that can cancel a job.
            :param min_number_of_executed_things: The minimum number of things that receive the configuration before the job can cancel.
            :param threshold_percentage: The minimum percentage of ``failureType`` failures that occur before the job can cancel. This parameter supports up to two digits after the decimal (for example, you can specify ``10.9`` or ``10.99`` , but not ``10.999`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobabortcriteria.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
                
                io_tJob_abort_criteria_property = greengrassv2_mixins.CfnDeploymentPropsMixin.IoTJobAbortCriteriaProperty(
                    action="action",
                    failure_type="failureType",
                    min_number_of_executed_things=123,
                    threshold_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9aebc203d3d02bbfb95881c463ce5af115e3c679ba010bca9be5ec108b9f719e)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument failure_type", value=failure_type, expected_type=type_hints["failure_type"])
                check_type(argname="argument min_number_of_executed_things", value=min_number_of_executed_things, expected_type=type_hints["min_number_of_executed_things"])
                check_type(argname="argument threshold_percentage", value=threshold_percentage, expected_type=type_hints["threshold_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if failure_type is not None:
                self._values["failure_type"] = failure_type
            if min_number_of_executed_things is not None:
                self._values["min_number_of_executed_things"] = min_number_of_executed_things
            if threshold_percentage is not None:
                self._values["threshold_percentage"] = threshold_percentage

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action to perform when the criteria are met.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobabortcriteria.html#cfn-greengrassv2-deployment-iotjobabortcriteria-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def failure_type(self) -> typing.Optional[builtins.str]:
            '''The type of job deployment failure that can cancel a job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobabortcriteria.html#cfn-greengrassv2-deployment-iotjobabortcriteria-failuretype
            '''
            result = self._values.get("failure_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def min_number_of_executed_things(self) -> typing.Optional[jsii.Number]:
            '''The minimum number of things that receive the configuration before the job can cancel.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobabortcriteria.html#cfn-greengrassv2-deployment-iotjobabortcriteria-minnumberofexecutedthings
            '''
            result = self._values.get("min_number_of_executed_things")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def threshold_percentage(self) -> typing.Optional[jsii.Number]:
            '''The minimum percentage of ``failureType`` failures that occur before the job can cancel.

            This parameter supports up to two digits after the decimal (for example, you can specify ``10.9`` or ``10.99`` , but not ``10.999`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobabortcriteria.html#cfn-greengrassv2-deployment-iotjobabortcriteria-thresholdpercentage
            '''
            result = self._values.get("threshold_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IoTJobAbortCriteriaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnDeploymentPropsMixin.IoTJobExecutionsRolloutConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "exponential_rate": "exponentialRate",
            "maximum_per_minute": "maximumPerMinute",
        },
    )
    class IoTJobExecutionsRolloutConfigProperty:
        def __init__(
            self,
            *,
            exponential_rate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentPropsMixin.IoTJobExponentialRolloutRateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            maximum_per_minute: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains information about the rollout configuration for a job.

            This configuration defines the rate at which the job deploys a configuration to a fleet of target devices.

            :param exponential_rate: The exponential rate to increase the job rollout rate.
            :param maximum_per_minute: The maximum number of devices that receive a pending job notification, per minute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobexecutionsrolloutconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
                
                # rate_increase_criteria: Any
                
                io_tJob_executions_rollout_config_property = greengrassv2_mixins.CfnDeploymentPropsMixin.IoTJobExecutionsRolloutConfigProperty(
                    exponential_rate=greengrassv2_mixins.CfnDeploymentPropsMixin.IoTJobExponentialRolloutRateProperty(
                        base_rate_per_minute=123,
                        increment_factor=123,
                        rate_increase_criteria=rate_increase_criteria
                    ),
                    maximum_per_minute=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f5722ca9b7470d73fa6a332f2c312830feafbf281030624b5289fa6a2d5d7842)
                check_type(argname="argument exponential_rate", value=exponential_rate, expected_type=type_hints["exponential_rate"])
                check_type(argname="argument maximum_per_minute", value=maximum_per_minute, expected_type=type_hints["maximum_per_minute"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exponential_rate is not None:
                self._values["exponential_rate"] = exponential_rate
            if maximum_per_minute is not None:
                self._values["maximum_per_minute"] = maximum_per_minute

        @builtins.property
        def exponential_rate(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.IoTJobExponentialRolloutRateProperty"]]:
            '''The exponential rate to increase the job rollout rate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobexecutionsrolloutconfig.html#cfn-greengrassv2-deployment-iotjobexecutionsrolloutconfig-exponentialrate
            '''
            result = self._values.get("exponential_rate")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.IoTJobExponentialRolloutRateProperty"]], result)

        @builtins.property
        def maximum_per_minute(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of devices that receive a pending job notification, per minute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobexecutionsrolloutconfig.html#cfn-greengrassv2-deployment-iotjobexecutionsrolloutconfig-maximumperminute
            '''
            result = self._values.get("maximum_per_minute")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IoTJobExecutionsRolloutConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnDeploymentPropsMixin.IoTJobExponentialRolloutRateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "base_rate_per_minute": "baseRatePerMinute",
            "increment_factor": "incrementFactor",
            "rate_increase_criteria": "rateIncreaseCriteria",
        },
    )
    class IoTJobExponentialRolloutRateProperty:
        def __init__(
            self,
            *,
            base_rate_per_minute: typing.Optional[jsii.Number] = None,
            increment_factor: typing.Optional[jsii.Number] = None,
            rate_increase_criteria: typing.Any = None,
        ) -> None:
            '''Contains information about an exponential rollout rate for a configuration deployment job.

            :param base_rate_per_minute: The minimum number of devices that receive a pending job notification, per minute, when the job starts. This parameter defines the initial rollout rate of the job.
            :param increment_factor: The exponential factor to increase the rollout rate for the job. This parameter supports up to one digit after the decimal (for example, you can specify ``1.5`` , but not ``1.55`` ).
            :param rate_increase_criteria: The criteria to increase the rollout rate for the job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobexponentialrolloutrate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
                
                # rate_increase_criteria: Any
                
                io_tJob_exponential_rollout_rate_property = greengrassv2_mixins.CfnDeploymentPropsMixin.IoTJobExponentialRolloutRateProperty(
                    base_rate_per_minute=123,
                    increment_factor=123,
                    rate_increase_criteria=rate_increase_criteria
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ef2b744cf8386c218971bf9e1eb83b5a3d56927556b5f24b7a5ca1142291b7ed)
                check_type(argname="argument base_rate_per_minute", value=base_rate_per_minute, expected_type=type_hints["base_rate_per_minute"])
                check_type(argname="argument increment_factor", value=increment_factor, expected_type=type_hints["increment_factor"])
                check_type(argname="argument rate_increase_criteria", value=rate_increase_criteria, expected_type=type_hints["rate_increase_criteria"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if base_rate_per_minute is not None:
                self._values["base_rate_per_minute"] = base_rate_per_minute
            if increment_factor is not None:
                self._values["increment_factor"] = increment_factor
            if rate_increase_criteria is not None:
                self._values["rate_increase_criteria"] = rate_increase_criteria

        @builtins.property
        def base_rate_per_minute(self) -> typing.Optional[jsii.Number]:
            '''The minimum number of devices that receive a pending job notification, per minute, when the job starts.

            This parameter defines the initial rollout rate of the job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobexponentialrolloutrate.html#cfn-greengrassv2-deployment-iotjobexponentialrolloutrate-baserateperminute
            '''
            result = self._values.get("base_rate_per_minute")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def increment_factor(self) -> typing.Optional[jsii.Number]:
            '''The exponential factor to increase the rollout rate for the job.

            This parameter supports up to one digit after the decimal (for example, you can specify ``1.5`` , but not ``1.55`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobexponentialrolloutrate.html#cfn-greengrassv2-deployment-iotjobexponentialrolloutrate-incrementfactor
            '''
            result = self._values.get("increment_factor")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def rate_increase_criteria(self) -> typing.Any:
            '''The criteria to increase the rollout rate for the job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobexponentialrolloutrate.html#cfn-greengrassv2-deployment-iotjobexponentialrolloutrate-rateincreasecriteria
            '''
            result = self._values.get("rate_increase_criteria")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IoTJobExponentialRolloutRateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnDeploymentPropsMixin.IoTJobTimeoutConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"in_progress_timeout_in_minutes": "inProgressTimeoutInMinutes"},
    )
    class IoTJobTimeoutConfigProperty:
        def __init__(
            self,
            *,
            in_progress_timeout_in_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains information about the timeout configuration for a job.

            :param in_progress_timeout_in_minutes: The amount of time, in minutes, that devices have to complete the job. The timer starts when the job status is set to ``IN_PROGRESS`` . If the job status doesn't change to a terminal state before the time expires, then the job status is set to ``TIMED_OUT`` . The timeout interval must be between 1 minute and 7 days (10080 minutes).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobtimeoutconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
                
                io_tJob_timeout_config_property = greengrassv2_mixins.CfnDeploymentPropsMixin.IoTJobTimeoutConfigProperty(
                    in_progress_timeout_in_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__513d353d0179e2b78ba0ad7053566a0259326bfda50ba0ef4e3e8413e6c72390)
                check_type(argname="argument in_progress_timeout_in_minutes", value=in_progress_timeout_in_minutes, expected_type=type_hints["in_progress_timeout_in_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if in_progress_timeout_in_minutes is not None:
                self._values["in_progress_timeout_in_minutes"] = in_progress_timeout_in_minutes

        @builtins.property
        def in_progress_timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''The amount of time, in minutes, that devices have to complete the job.

            The timer starts when the job status is set to ``IN_PROGRESS`` . If the job status doesn't change to a terminal state before the time expires, then the job status is set to ``TIMED_OUT`` .

            The timeout interval must be between 1 minute and 7 days (10080 minutes).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobtimeoutconfig.html#cfn-greengrassv2-deployment-iotjobtimeoutconfig-inprogresstimeoutinminutes
            '''
            result = self._values.get("in_progress_timeout_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IoTJobTimeoutConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_greengrassv2.mixins.CfnDeploymentPropsMixin.SystemResourceLimitsProperty",
        jsii_struct_bases=[],
        name_mapping={"cpus": "cpus", "memory": "memory"},
    )
    class SystemResourceLimitsProperty:
        def __init__(
            self,
            *,
            cpus: typing.Optional[jsii.Number] = None,
            memory: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains information about system resource limits that the  software applies to a component's processes.

            :param cpus: The maximum amount of CPU time that a component's processes can use on the core device. A core device's total CPU time is equivalent to the device's number of CPU cores. For example, on a core device with 4 CPU cores, you can set this value to 2 to limit the component's processes to 50 percent usage of each CPU core. On a device with 1 CPU core, you can set this value to 0.25 to limit the component's processes to 25 percent usage of the CPU. If you set this value to a number greater than the number of CPU cores, the AWS IoT Greengrass Core software doesn't limit the component's CPU usage.
            :param memory: The maximum amount of RAM, expressed in kilobytes, that a component's processes can use on the core device. For more information, see `Configure system resource limits for components <https://docs.aws.amazon.com/greengrass/v2/developerguide/configure-greengrass-core-v2.html#configure-component-system-resource-limits>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-systemresourcelimits.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_greengrassv2 import mixins as greengrassv2_mixins
                
                system_resource_limits_property = greengrassv2_mixins.CfnDeploymentPropsMixin.SystemResourceLimitsProperty(
                    cpus=123,
                    memory=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8f4eb87a756ca48db6ef78ea8815f402344645035952845b98e1cfb52a6932dd)
                check_type(argname="argument cpus", value=cpus, expected_type=type_hints["cpus"])
                check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cpus is not None:
                self._values["cpus"] = cpus
            if memory is not None:
                self._values["memory"] = memory

        @builtins.property
        def cpus(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of CPU time that a component's processes can use on the core device.

            A core device's total CPU time is equivalent to the device's number of CPU cores. For example, on a core device with 4 CPU cores, you can set this value to 2 to limit the component's processes to 50 percent usage of each CPU core. On a device with 1 CPU core, you can set this value to 0.25 to limit the component's processes to 25 percent usage of the CPU. If you set this value to a number greater than the number of CPU cores, the AWS IoT Greengrass Core software doesn't limit the component's CPU usage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-systemresourcelimits.html#cfn-greengrassv2-deployment-systemresourcelimits-cpus
            '''
            result = self._values.get("cpus")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def memory(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of RAM, expressed in kilobytes, that a component's processes can use on the core device.

            For more information, see `Configure system resource limits for components <https://docs.aws.amazon.com/greengrass/v2/developerguide/configure-greengrass-core-v2.html#configure-component-system-resource-limits>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-systemresourcelimits.html#cfn-greengrassv2-deployment-systemresourcelimits-memory
            '''
            result = self._values.get("memory")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SystemResourceLimitsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnComponentVersionMixinProps",
    "CfnComponentVersionPropsMixin",
    "CfnDeploymentMixinProps",
    "CfnDeploymentPropsMixin",
]

publication.publish()

def _typecheckingstub__49df39751f98d5c603e15c210ce1dd5b8c6026e0bce42fdf6b665d9e71f956c0(
    *,
    inline_recipe: typing.Optional[builtins.str] = None,
    lambda_function: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentVersionPropsMixin.LambdaFunctionRecipeSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__663a0ee564d5de028a1bff39802202e8e949ef2c642cff06185e11507f065c8c(
    props: typing.Union[CfnComponentVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4812465db085497d2d562fa36714ca253e015af839126bd5e6098783e8274f93(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b23180d0eff8eaeee65db14cf8db4a03a4014b77b7d2d8c50ff58a4cec862b7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f762a8a78c9621232d4d77bc0d80337cde334b1095f4751b539c5fdc07d0353(
    *,
    dependency_type: typing.Optional[builtins.str] = None,
    version_requirement: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6287916204d51d4cc486ea874e0c3b6dd237d15211c6794f2192d98cdf3c6c83(
    *,
    attributes: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34c477251c4f1700daf571f2b8a89deeb520a40cb3584e52b2b2177b14e58feb(
    *,
    devices: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentVersionPropsMixin.LambdaDeviceMountProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    memory_size_in_kb: typing.Optional[jsii.Number] = None,
    mount_ro_sysfs: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    volumes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentVersionPropsMixin.LambdaVolumeMountProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b4805a6303580a0913041f4fba903b7a6839a4de559ff37013fcd846bb265d3(
    *,
    add_group_owner: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    path: typing.Optional[builtins.str] = None,
    permission: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aef5532273311adf689e9ded57540a9266fea5b493f96a22cd0dbeace8c1c8a(
    *,
    topic: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__893141011743decfde4df8d391b40c6dfb06e2138a976aff0d648188f6775f8b(
    *,
    environment_variables: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    event_sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentVersionPropsMixin.LambdaEventSourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    exec_args: typing.Optional[typing.Sequence[builtins.str]] = None,
    input_payload_encoding_type: typing.Optional[builtins.str] = None,
    linux_process_params: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentVersionPropsMixin.LambdaLinuxProcessParamsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_idle_time_in_seconds: typing.Optional[jsii.Number] = None,
    max_instances_count: typing.Optional[jsii.Number] = None,
    max_queue_size: typing.Optional[jsii.Number] = None,
    pinned: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    status_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    timeout_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b962c84eeba16492d06c3d29e51e15782eaeb8d55a4e60a9b87128b81ab0d12f(
    *,
    component_dependencies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentVersionPropsMixin.ComponentDependencyRequirementProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    component_lambda_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentVersionPropsMixin.LambdaExecutionParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    component_name: typing.Optional[builtins.str] = None,
    component_platforms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentVersionPropsMixin.ComponentPlatformProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    component_version: typing.Optional[builtins.str] = None,
    lambda_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b39a09abb3d306b59503e4d756a25ad7a2771ad4a9ed6558090fb866a4bf5c(
    *,
    container_params: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentVersionPropsMixin.LambdaContainerParamsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    isolation_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2face038fb7858b8dce075d5cee462f3e70d28105ec12176b8ec7e8b9cefcfbd(
    *,
    add_group_owner: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    destination_path: typing.Optional[builtins.str] = None,
    permission: typing.Optional[builtins.str] = None,
    source_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da350da614a5bfa776b454fba2fd898e37dc0643e880c821141a7ab6216e091e(
    *,
    components: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentPropsMixin.ComponentDeploymentSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    deployment_name: typing.Optional[builtins.str] = None,
    deployment_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentPropsMixin.DeploymentPoliciesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    iot_job_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentPropsMixin.DeploymentIoTJobConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parent_target_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    target_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2641c92c1340bf057e16dc42e381112b2397f037c8235d85a57d4c9935e2cf2(
    props: typing.Union[CfnDeploymentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d301051c40f1c24677f2c32d6edab596ac8e052f2743f3e14e337cfeb0c29572(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__231f8d93504e2893f7cc9b0608b581b4dae3db46361c92607acbe86172cd918d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195e6decfe7525e93fe66c73b3ba0304a97216a1f854407811c9e1f4bf3a83c7(
    *,
    merge: typing.Optional[builtins.str] = None,
    reset: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e4800c05b929de121a258acdfbb5be1897bf140fc2a5b308ec8fa3727f52ee(
    *,
    component_version: typing.Optional[builtins.str] = None,
    configuration_update: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentPropsMixin.ComponentConfigurationUpdateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    run_with: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentPropsMixin.ComponentRunWithProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__619897f7da3f9df0c4588ba74f36001aa8822fd50d1a253033f0a9d276524f03(
    *,
    posix_user: typing.Optional[builtins.str] = None,
    system_resource_limits: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentPropsMixin.SystemResourceLimitsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    windows_user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1ac0a6808f46598d10b666ea5c0261a97467f049404137f4190a991da85766b(
    *,
    action: typing.Optional[builtins.str] = None,
    timeout_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa868f526d8a831d908cafc69ae913e06af90fbdcfc908b8adaf09a509a5a191(
    *,
    timeout_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c39a110096d914eacd5713bbc50e7976f0d2219cbd4757a089e11a1c4b97e82e(
    *,
    abort_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentPropsMixin.IoTJobAbortConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    job_executions_rollout_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentPropsMixin.IoTJobExecutionsRolloutConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentPropsMixin.IoTJobTimeoutConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b5c29279a641ed80aed59019e2bda5a2df1aec6ae03f190d9a6c02a03da7c7c(
    *,
    component_update_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentPropsMixin.DeploymentComponentUpdatePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    configuration_validation_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentPropsMixin.DeploymentConfigurationValidationPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    failure_handling_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49aab6e06e9b05e4b98495893af7f7e57bbb637a5183c8c9860ab2a76de4850a(
    *,
    criteria_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentPropsMixin.IoTJobAbortCriteriaProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aebc203d3d02bbfb95881c463ce5af115e3c679ba010bca9be5ec108b9f719e(
    *,
    action: typing.Optional[builtins.str] = None,
    failure_type: typing.Optional[builtins.str] = None,
    min_number_of_executed_things: typing.Optional[jsii.Number] = None,
    threshold_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5722ca9b7470d73fa6a332f2c312830feafbf281030624b5289fa6a2d5d7842(
    *,
    exponential_rate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentPropsMixin.IoTJobExponentialRolloutRateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maximum_per_minute: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef2b744cf8386c218971bf9e1eb83b5a3d56927556b5f24b7a5ca1142291b7ed(
    *,
    base_rate_per_minute: typing.Optional[jsii.Number] = None,
    increment_factor: typing.Optional[jsii.Number] = None,
    rate_increase_criteria: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__513d353d0179e2b78ba0ad7053566a0259326bfda50ba0ef4e3e8413e6c72390(
    *,
    in_progress_timeout_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f4eb87a756ca48db6ef78ea8815f402344645035952845b98e1cfb52a6932dd(
    *,
    cpus: typing.Optional[jsii.Number] = None,
    memory: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
