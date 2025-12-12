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
    jsii_type="@aws-cdk/mixins-preview.aws_gameliftstreams.mixins.CfnApplicationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_log_output_uri": "applicationLogOutputUri",
        "application_log_paths": "applicationLogPaths",
        "application_source_uri": "applicationSourceUri",
        "description": "description",
        "executable_path": "executablePath",
        "runtime_environment": "runtimeEnvironment",
        "tags": "tags",
    },
)
class CfnApplicationMixinProps:
    def __init__(
        self,
        *,
        application_log_output_uri: typing.Optional[builtins.str] = None,
        application_log_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        application_source_uri: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        executable_path: typing.Optional[builtins.str] = None,
        runtime_environment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.RuntimeEnvironmentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnApplicationPropsMixin.

        :param application_log_output_uri: An Amazon S3 URI to a bucket where you would like Amazon GameLift Streams to save application logs. Required if you specify one or more ``ApplicationLogPaths`` .
        :param application_log_paths: Locations of log files that your content generates during a stream session. Enter path values that are relative to the ``ApplicationSourceUri`` location. You can specify up to 10 log paths. Amazon GameLift Streams uploads designated log files to the Amazon S3 bucket that you specify in ``ApplicationLogOutputUri`` at the end of a stream session. To retrieve stored log files, call `GetStreamSession <https://docs.aws.amazon.com/gameliftstreams/latest/apireference/API_GetStreamSession.html>`_ and get the ``LogFileLocationUri`` .
        :param application_source_uri: The location of the content that you want to stream. Enter an Amazon S3 URI to a bucket that contains your game or other application. The location can have a multi-level prefix structure, but it must include all the files needed to run the content. Amazon GameLift Streams copies everything under the specified location. This value is immutable. To designate a different content location, create a new application. .. epigraph:: The Amazon S3 bucket and the Amazon GameLift Streams application must be in the same AWS Region.
        :param description: A human-readable label for the application. You can update this value later.
        :param executable_path: The relative path and file name of the executable file that Amazon GameLift Streams will stream. Specify a path relative to the location set in ``ApplicationSourceUri`` . The file must be contained within the application's root folder. For Windows applications, the file must be a valid Windows executable or batch file with a filename ending in .exe, .cmd, or .bat. For Linux applications, the file must be a valid Linux binary executable or a script that contains an initial interpreter line starting with a shebang (' ``#!`` ').
        :param runtime_environment: A set of configuration settings to run the application on a stream group. This configures the operating system, and can include compatibility layers and other drivers.
        :param tags: A list of labels to assign to the new application resource. Tags are developer-defined key-value pairs. Tagging AWS resources is useful for resource management, access management and cost allocation. See `Tagging AWS Resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in the *AWS General Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gameliftstreams-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_gameliftstreams import mixins as gameliftstreams_mixins
            
            cfn_application_mixin_props = gameliftstreams_mixins.CfnApplicationMixinProps(
                application_log_output_uri="applicationLogOutputUri",
                application_log_paths=["applicationLogPaths"],
                application_source_uri="applicationSourceUri",
                description="description",
                executable_path="executablePath",
                runtime_environment=gameliftstreams_mixins.CfnApplicationPropsMixin.RuntimeEnvironmentProperty(
                    type="type",
                    version="version"
                ),
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f0e24b812a1beb035dbc392bde12095828b744a4e36c76415b011dc596a03a8)
            check_type(argname="argument application_log_output_uri", value=application_log_output_uri, expected_type=type_hints["application_log_output_uri"])
            check_type(argname="argument application_log_paths", value=application_log_paths, expected_type=type_hints["application_log_paths"])
            check_type(argname="argument application_source_uri", value=application_source_uri, expected_type=type_hints["application_source_uri"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument executable_path", value=executable_path, expected_type=type_hints["executable_path"])
            check_type(argname="argument runtime_environment", value=runtime_environment, expected_type=type_hints["runtime_environment"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_log_output_uri is not None:
            self._values["application_log_output_uri"] = application_log_output_uri
        if application_log_paths is not None:
            self._values["application_log_paths"] = application_log_paths
        if application_source_uri is not None:
            self._values["application_source_uri"] = application_source_uri
        if description is not None:
            self._values["description"] = description
        if executable_path is not None:
            self._values["executable_path"] = executable_path
        if runtime_environment is not None:
            self._values["runtime_environment"] = runtime_environment
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def application_log_output_uri(self) -> typing.Optional[builtins.str]:
        '''An Amazon S3 URI to a bucket where you would like Amazon GameLift Streams to save application logs.

        Required if you specify one or more ``ApplicationLogPaths`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gameliftstreams-application.html#cfn-gameliftstreams-application-applicationlogoutputuri
        '''
        result = self._values.get("application_log_output_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_log_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Locations of log files that your content generates during a stream session.

        Enter path values that are relative to the ``ApplicationSourceUri`` location. You can specify up to 10 log paths. Amazon GameLift Streams uploads designated log files to the Amazon S3 bucket that you specify in ``ApplicationLogOutputUri`` at the end of a stream session. To retrieve stored log files, call `GetStreamSession <https://docs.aws.amazon.com/gameliftstreams/latest/apireference/API_GetStreamSession.html>`_ and get the ``LogFileLocationUri`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gameliftstreams-application.html#cfn-gameliftstreams-application-applicationlogpaths
        '''
        result = self._values.get("application_log_paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def application_source_uri(self) -> typing.Optional[builtins.str]:
        '''The location of the content that you want to stream.

        Enter an Amazon S3 URI to a bucket that contains your game or other application. The location can have a multi-level prefix structure, but it must include all the files needed to run the content. Amazon GameLift Streams copies everything under the specified location.

        This value is immutable. To designate a different content location, create a new application.
        .. epigraph::

           The Amazon S3 bucket and the Amazon GameLift Streams application must be in the same AWS Region.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gameliftstreams-application.html#cfn-gameliftstreams-application-applicationsourceuri
        '''
        result = self._values.get("application_source_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable label for the application.

        You can update this value later.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gameliftstreams-application.html#cfn-gameliftstreams-application-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def executable_path(self) -> typing.Optional[builtins.str]:
        '''The relative path and file name of the executable file that Amazon GameLift Streams will stream.

        Specify a path relative to the location set in ``ApplicationSourceUri`` . The file must be contained within the application's root folder. For Windows applications, the file must be a valid Windows executable or batch file with a filename ending in .exe, .cmd, or .bat. For Linux applications, the file must be a valid Linux binary executable or a script that contains an initial interpreter line starting with a shebang (' ``#!`` ').

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gameliftstreams-application.html#cfn-gameliftstreams-application-executablepath
        '''
        result = self._values.get("executable_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_environment(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.RuntimeEnvironmentProperty"]]:
        '''A set of configuration settings to run the application on a stream group.

        This configures the operating system, and can include compatibility layers and other drivers.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gameliftstreams-application.html#cfn-gameliftstreams-application-runtimeenvironment
        '''
        result = self._values.get("runtime_environment")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.RuntimeEnvironmentProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A list of labels to assign to the new application resource.

        Tags are developer-defined key-value pairs. Tagging AWS resources is useful for resource management, access management and cost allocation. See `Tagging AWS Resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in the *AWS General Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gameliftstreams-application.html#cfn-gameliftstreams-application-tags
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
    jsii_type="@aws-cdk/mixins-preview.aws_gameliftstreams.mixins.CfnApplicationPropsMixin",
):
    '''The ``AWS::GameLiftStreams::Application`` resource defines an Amazon GameLift Streams application.

    An application specifies the content that you want to stream, such as a game or other software, and its runtime environment (Microsoft Windows, Ubuntu, or Proton).

    Before you create an Amazon GameLift Streams application, upload your *uncompressed* game files (do not upload a .zip file) to an Amazon Simple Storage Service (Amazon S3) standard bucket.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gameliftstreams-application.html
    :cloudformationResource: AWS::GameLiftStreams::Application
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_gameliftstreams import mixins as gameliftstreams_mixins
        
        cfn_application_props_mixin = gameliftstreams_mixins.CfnApplicationPropsMixin(gameliftstreams_mixins.CfnApplicationMixinProps(
            application_log_output_uri="applicationLogOutputUri",
            application_log_paths=["applicationLogPaths"],
            application_source_uri="applicationSourceUri",
            description="description",
            executable_path="executablePath",
            runtime_environment=gameliftstreams_mixins.CfnApplicationPropsMixin.RuntimeEnvironmentProperty(
                type="type",
                version="version"
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
        props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GameLiftStreams::Application``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4ac0eef9e600d3ab35c70c49dd891f1b383319dc91b53400aa13982a7b2d8e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f3b3f6f5b9f6c0f012862df9dd999c551ad22a236199d107951367286689603)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5232497ceea6ae9ff0ae60090d44a1596a7cb3a7b81c7ec87c7017a8dac03eb0)
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
        jsii_type="@aws-cdk/mixins-preview.aws_gameliftstreams.mixins.CfnApplicationPropsMixin.RuntimeEnvironmentProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "version": "version"},
    )
    class RuntimeEnvironmentProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration settings that identify the operating system for an application resource.

            This can also include a compatibility layer and other drivers.

            A runtime environment can be one of the following:

            - For Linux applications
            - Ubuntu 22.04 LTS ( ``Type=UBUNTU, Version=22_04_LTS`` )
            - For Windows applications
            - Microsoft Windows Server 2022 Base ( ``Type=WINDOWS, Version=2022`` )
            - Proton 9.0-2 ( ``Type=PROTON, Version=20250516`` )
            - Proton 8.0-5 ( ``Type=PROTON, Version=20241007`` )
            - Proton 8.0-2c ( ``Type=PROTON, Version=20230704`` )

            :param type: The operating system and other drivers. For Proton, this also includes the Proton compatibility layer.
            :param version: Versioned container environment for the application operating system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gameliftstreams-application-runtimeenvironment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gameliftstreams import mixins as gameliftstreams_mixins
                
                runtime_environment_property = gameliftstreams_mixins.CfnApplicationPropsMixin.RuntimeEnvironmentProperty(
                    type="type",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ec7918954a7e9baa398ca8840c6f4f4a0267f772b7e58292dfb2b882834cb477)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The operating system and other drivers.

            For Proton, this also includes the Proton compatibility layer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gameliftstreams-application-runtimeenvironment.html#cfn-gameliftstreams-application-runtimeenvironment-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''Versioned container environment for the application operating system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gameliftstreams-application-runtimeenvironment.html#cfn-gameliftstreams-application-runtimeenvironment-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuntimeEnvironmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_gameliftstreams.mixins.CfnStreamGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_application": "defaultApplication",
        "description": "description",
        "location_configurations": "locationConfigurations",
        "stream_class": "streamClass",
        "tags": "tags",
    },
)
class CfnStreamGroupMixinProps:
    def __init__(
        self,
        *,
        default_application: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStreamGroupPropsMixin.DefaultApplicationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        location_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStreamGroupPropsMixin.LocationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        stream_class: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnStreamGroupPropsMixin.

        :param default_application: Object that identifies the Amazon GameLift Streams application to stream with this stream group.
        :param description: A descriptive label for the stream group.
        :param location_configurations: A set of one or more locations and the streaming capacity for each location. One of the locations MUST be your primary location, which is the AWS Region where you are specifying this resource.
        :param stream_class: The target stream quality for sessions that are hosted in this stream group. Set a stream class that is appropriate to the type of content that you're streaming. Stream class determines the type of computing resources Amazon GameLift Streams uses and impacts the cost of streaming. The following options are available: A stream class can be one of the following: - *``gen5n_win2022`` (NVIDIA, ultra)* Supports applications with extremely high 3D scene complexity. Runs applications on Microsoft Windows Server 2022 Base and supports DirectX 12. Compatible with Unreal Engine versions up through 5.4, 32 and 64-bit applications, and anti-cheat technology. Uses NVIDIA A10G Tensor GPU. - Reference resolution: 1080p - Reference frame rate: 60 fps - Workload specifications: 8 vCPUs, 32 GB RAM, 24 GB VRAM - Tenancy: Supports 1 concurrent stream session - *``gen5n_high`` (NVIDIA, high)* Supports applications with moderate to high 3D scene complexity. Uses NVIDIA A10G Tensor GPU. - Reference resolution: 1080p - Reference frame rate: 60 fps - Workload specifications: 4 vCPUs, 16 GB RAM, 12 GB VRAM - Tenancy: Supports up to 2 concurrent stream sessions - *``gen5n_ultra`` (NVIDIA, ultra)* Supports applications with extremely high 3D scene complexity. Uses dedicated NVIDIA A10G Tensor GPU. - Reference resolution: 1080p - Reference frame rate: 60 fps - Workload specifications: 8 vCPUs, 32 GB RAM, 24 GB VRAM - Tenancy: Supports 1 concurrent stream session - *``gen4n_win2022`` (NVIDIA, ultra)* Supports applications with extremely high 3D scene complexity. Runs applications on Microsoft Windows Server 2022 Base and supports DirectX 12. Compatible with Unreal Engine versions up through 5.4, 32 and 64-bit applications, and anti-cheat technology. Uses NVIDIA T4 Tensor GPU. - Reference resolution: 1080p - Reference frame rate: 60 fps - Workload specifications: 8 vCPUs, 32 GB RAM, 16 GB VRAM - Tenancy: Supports 1 concurrent stream session - *``gen4n_high`` (NVIDIA, high)* Supports applications with moderate to high 3D scene complexity. Uses NVIDIA T4 Tensor GPU. - Reference resolution: 1080p - Reference frame rate: 60 fps - Workload specifications: 4 vCPUs, 16 GB RAM, 8 GB VRAM - Tenancy: Supports up to 2 concurrent stream sessions - *``gen4n_ultra`` (NVIDIA, ultra)* Supports applications with high 3D scene complexity. Uses dedicated NVIDIA T4 Tensor GPU. - Reference resolution: 1080p - Reference frame rate: 60 fps - Workload specifications: 8 vCPUs, 32 GB RAM, 16 GB VRAM - Tenancy: Supports 1 concurrent stream session
        :param tags: A list of labels to assign to the new stream group resource. Tags are developer-defined key-value pairs. Tagging AWS resources is useful for resource management, access management and cost allocation. See `Tagging AWS Resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in the *AWS General Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gameliftstreams-streamgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_gameliftstreams import mixins as gameliftstreams_mixins
            
            cfn_stream_group_mixin_props = gameliftstreams_mixins.CfnStreamGroupMixinProps(
                default_application=gameliftstreams_mixins.CfnStreamGroupPropsMixin.DefaultApplicationProperty(
                    arn="arn",
                    id="id"
                ),
                description="description",
                location_configurations=[gameliftstreams_mixins.CfnStreamGroupPropsMixin.LocationConfigurationProperty(
                    always_on_capacity=123,
                    location_name="locationName",
                    on_demand_capacity=123
                )],
                stream_class="streamClass",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__891344e6b5a2779250dc8fb8e87ac5a9ecb8f58e041fbfae60e0a81488ec7128)
            check_type(argname="argument default_application", value=default_application, expected_type=type_hints["default_application"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument location_configurations", value=location_configurations, expected_type=type_hints["location_configurations"])
            check_type(argname="argument stream_class", value=stream_class, expected_type=type_hints["stream_class"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_application is not None:
            self._values["default_application"] = default_application
        if description is not None:
            self._values["description"] = description
        if location_configurations is not None:
            self._values["location_configurations"] = location_configurations
        if stream_class is not None:
            self._values["stream_class"] = stream_class
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def default_application(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamGroupPropsMixin.DefaultApplicationProperty"]]:
        '''Object that identifies the Amazon GameLift Streams application to stream with this stream group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gameliftstreams-streamgroup.html#cfn-gameliftstreams-streamgroup-defaultapplication
        '''
        result = self._values.get("default_application")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamGroupPropsMixin.DefaultApplicationProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A descriptive label for the stream group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gameliftstreams-streamgroup.html#cfn-gameliftstreams-streamgroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamGroupPropsMixin.LocationConfigurationProperty"]]]]:
        '''A set of one or more locations and the streaming capacity for each location.

        One of the locations MUST be your primary location, which is the AWS Region where you are specifying this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gameliftstreams-streamgroup.html#cfn-gameliftstreams-streamgroup-locationconfigurations
        '''
        result = self._values.get("location_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamGroupPropsMixin.LocationConfigurationProperty"]]]], result)

    @builtins.property
    def stream_class(self) -> typing.Optional[builtins.str]:
        '''The target stream quality for sessions that are hosted in this stream group.

        Set a stream class that is appropriate to the type of content that you're streaming. Stream class determines the type of computing resources Amazon GameLift Streams uses and impacts the cost of streaming. The following options are available:

        A stream class can be one of the following:

        - *``gen5n_win2022`` (NVIDIA, ultra)* Supports applications with extremely high 3D scene complexity. Runs applications on Microsoft Windows Server 2022 Base and supports DirectX 12. Compatible with Unreal Engine versions up through 5.4, 32 and 64-bit applications, and anti-cheat technology. Uses NVIDIA A10G Tensor GPU.
        - Reference resolution: 1080p
        - Reference frame rate: 60 fps
        - Workload specifications: 8 vCPUs, 32 GB RAM, 24 GB VRAM
        - Tenancy: Supports 1 concurrent stream session
        - *``gen5n_high`` (NVIDIA, high)* Supports applications with moderate to high 3D scene complexity. Uses NVIDIA A10G Tensor GPU.
        - Reference resolution: 1080p
        - Reference frame rate: 60 fps
        - Workload specifications: 4 vCPUs, 16 GB RAM, 12 GB VRAM
        - Tenancy: Supports up to 2 concurrent stream sessions
        - *``gen5n_ultra`` (NVIDIA, ultra)* Supports applications with extremely high 3D scene complexity. Uses dedicated NVIDIA A10G Tensor GPU.
        - Reference resolution: 1080p
        - Reference frame rate: 60 fps
        - Workload specifications: 8 vCPUs, 32 GB RAM, 24 GB VRAM
        - Tenancy: Supports 1 concurrent stream session
        - *``gen4n_win2022`` (NVIDIA, ultra)* Supports applications with extremely high 3D scene complexity. Runs applications on Microsoft Windows Server 2022 Base and supports DirectX 12. Compatible with Unreal Engine versions up through 5.4, 32 and 64-bit applications, and anti-cheat technology. Uses NVIDIA T4 Tensor GPU.
        - Reference resolution: 1080p
        - Reference frame rate: 60 fps
        - Workload specifications: 8 vCPUs, 32 GB RAM, 16 GB VRAM
        - Tenancy: Supports 1 concurrent stream session
        - *``gen4n_high`` (NVIDIA, high)* Supports applications with moderate to high 3D scene complexity. Uses NVIDIA T4 Tensor GPU.
        - Reference resolution: 1080p
        - Reference frame rate: 60 fps
        - Workload specifications: 4 vCPUs, 16 GB RAM, 8 GB VRAM
        - Tenancy: Supports up to 2 concurrent stream sessions
        - *``gen4n_ultra`` (NVIDIA, ultra)* Supports applications with high 3D scene complexity. Uses dedicated NVIDIA T4 Tensor GPU.
        - Reference resolution: 1080p
        - Reference frame rate: 60 fps
        - Workload specifications: 8 vCPUs, 32 GB RAM, 16 GB VRAM
        - Tenancy: Supports 1 concurrent stream session

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gameliftstreams-streamgroup.html#cfn-gameliftstreams-streamgroup-streamclass
        '''
        result = self._values.get("stream_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A list of labels to assign to the new stream group resource.

        Tags are developer-defined key-value pairs. Tagging AWS resources is useful for resource management, access management and cost allocation. See `Tagging AWS Resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in the *AWS General Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gameliftstreams-streamgroup.html#cfn-gameliftstreams-streamgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStreamGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStreamGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_gameliftstreams.mixins.CfnStreamGroupPropsMixin",
):
    '''The ``AWS::GameLiftStreams::StreamGroup`` resource defines a group of compute resources that will be running and streaming your game.

    When you create a stream group, you specify the hardware configuration (CPU, GPU, RAM) that will run your game (known as the *stream class* ), the geographical locations where your game can run, and the number of streams that can run simultaneously in each location (known as *stream capacity* ). Stream groups manage how Amazon GameLift Streams allocates resources and handles concurrent streams, allowing you to effectively manage capacity and costs.

    There are two types of stream capacity: always-on and on-demand.

    - *Always-on* : The streaming capacity that is allocated and ready to handle stream requests without delay. You pay for this capacity whether it's in use or not. Best for quickest time from streaming request to streaming session. Default is 1 (2 for high stream classes) when creating a stream group or adding a location.
    - *On-demand* : The streaming capacity that Amazon GameLift Streams can allocate in response to stream requests, and then de-allocate when the session has terminated. This offers a cost control measure at the expense of a greater startup time (typically under 5 minutes). Default is 0 when creating a stream group or adding a location.

    Values for capacity must be whole number multiples of the tenancy value of the stream group's stream class.
    .. epigraph::

       Application association is not currently supported in CloudFormation . To link additional applications to a stream group, use the Amazon GameLift Streams console or the AWS CLI .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gameliftstreams-streamgroup.html
    :cloudformationResource: AWS::GameLiftStreams::StreamGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_gameliftstreams import mixins as gameliftstreams_mixins
        
        cfn_stream_group_props_mixin = gameliftstreams_mixins.CfnStreamGroupPropsMixin(gameliftstreams_mixins.CfnStreamGroupMixinProps(
            default_application=gameliftstreams_mixins.CfnStreamGroupPropsMixin.DefaultApplicationProperty(
                arn="arn",
                id="id"
            ),
            description="description",
            location_configurations=[gameliftstreams_mixins.CfnStreamGroupPropsMixin.LocationConfigurationProperty(
                always_on_capacity=123,
                location_name="locationName",
                on_demand_capacity=123
            )],
            stream_class="streamClass",
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnStreamGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GameLiftStreams::StreamGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52101e736b57f6a76192cd8f63f038a956d65342e675854f11e3825ce2eb34b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c0fb3f60616f7cf14dc8a36335be042f8d88e35c30ea3a031b57456c3a48b1f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f69d7a56653793b7291da77679c26cbd129dfb3f72f0eb60e6cb2f085d978e53)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStreamGroupMixinProps:
        return typing.cast(CfnStreamGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gameliftstreams.mixins.CfnStreamGroupPropsMixin.DefaultApplicationProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn", "id": "id"},
    )
    class DefaultApplicationProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents the default Amazon GameLift Streams application that a stream group hosts.

            :param arn: An `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html>`_ that uniquely identifies the application resource. Example ARN: ``arn:aws:gameliftstreams:us-west-2:111122223333:application/a-9ZY8X7Wv6`` .
            :param id: An ID that uniquely identifies the application resource. Example ID: ``a-9ZY8X7Wv6`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gameliftstreams-streamgroup-defaultapplication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gameliftstreams import mixins as gameliftstreams_mixins
                
                default_application_property = gameliftstreams_mixins.CfnStreamGroupPropsMixin.DefaultApplicationProperty(
                    arn="arn",
                    id="id"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__adeb097b316a66bfaf3e0ff4581a01566a79e74081f8feb36f81d934b564f67c)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if id is not None:
                self._values["id"] = id

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''An `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html>`_ that uniquely identifies the application resource. Example ARN: ``arn:aws:gameliftstreams:us-west-2:111122223333:application/a-9ZY8X7Wv6`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gameliftstreams-streamgroup-defaultapplication.html#cfn-gameliftstreams-streamgroup-defaultapplication-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''An ID that uniquely identifies the application resource.

            Example ID: ``a-9ZY8X7Wv6`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gameliftstreams-streamgroup-defaultapplication.html#cfn-gameliftstreams-streamgroup-defaultapplication-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultApplicationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gameliftstreams.mixins.CfnStreamGroupPropsMixin.LocationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "always_on_capacity": "alwaysOnCapacity",
            "location_name": "locationName",
            "on_demand_capacity": "onDemandCapacity",
        },
    )
    class LocationConfigurationProperty:
        def __init__(
            self,
            *,
            always_on_capacity: typing.Optional[jsii.Number] = None,
            location_name: typing.Optional[builtins.str] = None,
            on_demand_capacity: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Configuration settings that define a stream group's stream capacity for a location.

            When configuring a location for the first time, you must specify a numeric value for at least one of the two capacity types.

            :param always_on_capacity: The streaming capacity that is allocated and ready to handle stream requests without delay. You pay for this capacity whether it's in use or not. Best for quickest time from streaming request to streaming session. Default is 1 (2 for high stream classes) when creating a stream group or adding a location.
            :param location_name: A location's name. For example, ``us-east-1`` . For a complete list of locations that Amazon GameLift Streams supports, refer to `Regions, quotas, and limitations <https://docs.aws.amazon.com/gameliftstreams/latest/developerguide/regions-quotas.html>`_ in the *Amazon GameLift Streams Developer Guide* .
            :param on_demand_capacity: The streaming capacity that Amazon GameLift Streams can allocate in response to stream requests, and then de-allocate when the session has terminated. This offers a cost control measure at the expense of a greater startup time (typically under 5 minutes). Default is 0 when creating a stream group or adding a location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gameliftstreams-streamgroup-locationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gameliftstreams import mixins as gameliftstreams_mixins
                
                location_configuration_property = gameliftstreams_mixins.CfnStreamGroupPropsMixin.LocationConfigurationProperty(
                    always_on_capacity=123,
                    location_name="locationName",
                    on_demand_capacity=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__363cbc4a2224e4179666da94e123e776ce2e72ad21593b9d61a010aee7b7bc10)
                check_type(argname="argument always_on_capacity", value=always_on_capacity, expected_type=type_hints["always_on_capacity"])
                check_type(argname="argument location_name", value=location_name, expected_type=type_hints["location_name"])
                check_type(argname="argument on_demand_capacity", value=on_demand_capacity, expected_type=type_hints["on_demand_capacity"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if always_on_capacity is not None:
                self._values["always_on_capacity"] = always_on_capacity
            if location_name is not None:
                self._values["location_name"] = location_name
            if on_demand_capacity is not None:
                self._values["on_demand_capacity"] = on_demand_capacity

        @builtins.property
        def always_on_capacity(self) -> typing.Optional[jsii.Number]:
            '''The streaming capacity that is allocated and ready to handle stream requests without delay.

            You pay for this capacity whether it's in use or not. Best for quickest time from streaming request to streaming session. Default is 1 (2 for high stream classes) when creating a stream group or adding a location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gameliftstreams-streamgroup-locationconfiguration.html#cfn-gameliftstreams-streamgroup-locationconfiguration-alwaysoncapacity
            '''
            result = self._values.get("always_on_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def location_name(self) -> typing.Optional[builtins.str]:
            '''A location's name.

            For example, ``us-east-1`` . For a complete list of locations that Amazon GameLift Streams supports, refer to `Regions, quotas, and limitations <https://docs.aws.amazon.com/gameliftstreams/latest/developerguide/regions-quotas.html>`_ in the *Amazon GameLift Streams Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gameliftstreams-streamgroup-locationconfiguration.html#cfn-gameliftstreams-streamgroup-locationconfiguration-locationname
            '''
            result = self._values.get("location_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def on_demand_capacity(self) -> typing.Optional[jsii.Number]:
            '''The streaming capacity that Amazon GameLift Streams can allocate in response to stream requests, and then de-allocate when the session has terminated.

            This offers a cost control measure at the expense of a greater startup time (typically under 5 minutes). Default is 0 when creating a stream group or adding a location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gameliftstreams-streamgroup-locationconfiguration.html#cfn-gameliftstreams-streamgroup-locationconfiguration-ondemandcapacity
            '''
            result = self._values.get("on_demand_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnApplicationMixinProps",
    "CfnApplicationPropsMixin",
    "CfnStreamGroupMixinProps",
    "CfnStreamGroupPropsMixin",
]

publication.publish()

def _typecheckingstub__4f0e24b812a1beb035dbc392bde12095828b744a4e36c76415b011dc596a03a8(
    *,
    application_log_output_uri: typing.Optional[builtins.str] = None,
    application_log_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    application_source_uri: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    executable_path: typing.Optional[builtins.str] = None,
    runtime_environment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.RuntimeEnvironmentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4ac0eef9e600d3ab35c70c49dd891f1b383319dc91b53400aa13982a7b2d8e2(
    props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f3b3f6f5b9f6c0f012862df9dd999c551ad22a236199d107951367286689603(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5232497ceea6ae9ff0ae60090d44a1596a7cb3a7b81c7ec87c7017a8dac03eb0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec7918954a7e9baa398ca8840c6f4f4a0267f772b7e58292dfb2b882834cb477(
    *,
    type: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__891344e6b5a2779250dc8fb8e87ac5a9ecb8f58e041fbfae60e0a81488ec7128(
    *,
    default_application: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStreamGroupPropsMixin.DefaultApplicationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    location_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStreamGroupPropsMixin.LocationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    stream_class: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52101e736b57f6a76192cd8f63f038a956d65342e675854f11e3825ce2eb34b9(
    props: typing.Union[CfnStreamGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c0fb3f60616f7cf14dc8a36335be042f8d88e35c30ea3a031b57456c3a48b1f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f69d7a56653793b7291da77679c26cbd129dfb3f72f0eb60e6cb2f085d978e53(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adeb097b316a66bfaf3e0ff4581a01566a79e74081f8feb36f81d934b564f67c(
    *,
    arn: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363cbc4a2224e4179666da94e123e776ce2e72ad21593b9d61a010aee7b7bc10(
    *,
    always_on_capacity: typing.Optional[jsii.Number] = None,
    location_name: typing.Optional[builtins.str] = None,
    on_demand_capacity: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
