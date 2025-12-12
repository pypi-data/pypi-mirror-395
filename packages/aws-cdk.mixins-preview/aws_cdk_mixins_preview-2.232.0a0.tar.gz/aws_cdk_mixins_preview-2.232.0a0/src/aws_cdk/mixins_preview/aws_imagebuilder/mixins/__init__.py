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
    jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnComponentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "change_description": "changeDescription",
        "data": "data",
        "description": "description",
        "kms_key_id": "kmsKeyId",
        "name": "name",
        "platform": "platform",
        "supported_os_versions": "supportedOsVersions",
        "tags": "tags",
        "uri": "uri",
        "version": "version",
    },
)
class CfnComponentMixinProps:
    def __init__(
        self,
        *,
        change_description: typing.Optional[builtins.str] = None,
        data: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        platform: typing.Optional[builtins.str] = None,
        supported_os_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        uri: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnComponentPropsMixin.

        :param change_description: The change description of the component. Describes what change has been made in this version, or what makes this version different from other versions of the component.
        :param data: Component ``data`` contains inline YAML document content for the component. Alternatively, you can specify the ``uri`` of a YAML document file stored in Amazon S3. However, you cannot specify both properties.
        :param description: Describes the contents of the component.
        :param kms_key_id: The Amazon Resource Name (ARN) that uniquely identifies the KMS key used to encrypt this component. This can be either the Key ARN or the Alias ARN. For more information, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id-key-ARN>`_ in the *AWS Key Management Service Developer Guide* .
        :param name: The name of the component.
        :param platform: The operating system platform of the component.
        :param supported_os_versions: The operating system (OS) version supported by the component. If the OS information is available, a prefix match is performed against the base image OS version during image recipe creation.
        :param tags: The tags that apply to the component.
        :param uri: The ``uri`` of a YAML component document file. This must be an S3 URL ( ``s3://bucket/key`` ), and the requester must have permission to access the S3 bucket it points to. If you use Amazon S3, you can specify component content up to your service quota. Alternatively, you can specify the YAML document inline, using the component ``data`` property. You cannot specify both properties.
        :param version: The component version. For example, ``1.0.0`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
            
            cfn_component_mixin_props = imagebuilder_mixins.CfnComponentMixinProps(
                change_description="changeDescription",
                data="data",
                description="description",
                kms_key_id="kmsKeyId",
                name="name",
                platform="platform",
                supported_os_versions=["supportedOsVersions"],
                tags={
                    "tags_key": "tags"
                },
                uri="uri",
                version="version"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbd742a0a2b3f62fc52804adac37346d59927c582d59534d8f5fbf63d957eeeb)
            check_type(argname="argument change_description", value=change_description, expected_type=type_hints["change_description"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument supported_os_versions", value=supported_os_versions, expected_type=type_hints["supported_os_versions"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if change_description is not None:
            self._values["change_description"] = change_description
        if data is not None:
            self._values["data"] = data
        if description is not None:
            self._values["description"] = description
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if name is not None:
            self._values["name"] = name
        if platform is not None:
            self._values["platform"] = platform
        if supported_os_versions is not None:
            self._values["supported_os_versions"] = supported_os_versions
        if tags is not None:
            self._values["tags"] = tags
        if uri is not None:
            self._values["uri"] = uri
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def change_description(self) -> typing.Optional[builtins.str]:
        '''The change description of the component.

        Describes what change has been made in this version, or what makes this version different from other versions of the component.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-changedescription
        '''
        result = self._values.get("change_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data(self) -> typing.Optional[builtins.str]:
        '''Component ``data`` contains inline YAML document content for the component.

        Alternatively, you can specify the ``uri`` of a YAML document file stored in Amazon S3. However, you cannot specify both properties.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-data
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Describes the contents of the component.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) that uniquely identifies the KMS key used to encrypt this component.

        This can be either the Key ARN or the Alias ARN. For more information, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id-key-ARN>`_ in the *AWS Key Management Service Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the component.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''The operating system platform of the component.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-platform
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def supported_os_versions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The operating system (OS) version supported by the component.

        If the OS information is available, a prefix match is performed against the base image OS version during image recipe creation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-supportedosversions
        '''
        result = self._values.get("supported_os_versions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags that apply to the component.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''The ``uri`` of a YAML component document file.

        This must be an S3 URL ( ``s3://bucket/key`` ), and the requester must have permission to access the S3 bucket it points to. If you use Amazon S3, you can specify component content up to your service quota.

        Alternatively, you can specify the YAML document inline, using the component ``data`` property. You cannot specify both properties.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-uri
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The component version.

        For example, ``1.0.0`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html#cfn-imagebuilder-component-version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnComponentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnComponentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnComponentPropsMixin",
):
    '''Creates a new component that can be used to build, validate, test, and assess your image.

    The component is based on a YAML document that you specify using exactly one of the following methods:

    - Inline, using the ``data`` property in the request body.
    - A URL that points to a YAML document file stored in Amazon S3, using the ``uri`` property in the request body.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-component.html
    :cloudformationResource: AWS::ImageBuilder::Component
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
        
        cfn_component_props_mixin = imagebuilder_mixins.CfnComponentPropsMixin(imagebuilder_mixins.CfnComponentMixinProps(
            change_description="changeDescription",
            data="data",
            description="description",
            kms_key_id="kmsKeyId",
            name="name",
            platform="platform",
            supported_os_versions=["supportedOsVersions"],
            tags={
                "tags_key": "tags"
            },
            uri="uri",
            version="version"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnComponentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ImageBuilder::Component``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60231d7f5888d03666bdb3a335a3eb60f9275631560fcc0ed71af4b8e8ba5012)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bdf603cc6909a72de9be1f0432018d3150a4159030d3235c6a3a869b7f6b494)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e35fba1b2f90fac495ecbdc43876485e39852939f10763327703c0612c02d0c3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnComponentMixinProps:
        return typing.cast(CfnComponentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnComponentPropsMixin.LatestVersionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "major": "major",
            "minor": "minor",
            "patch": "patch",
        },
    )
    class LatestVersionProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            major: typing.Optional[builtins.str] = None,
            minor: typing.Optional[builtins.str] = None,
            patch: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The latest version references of the component.

            :param arn: The Amazon Resource Name (ARN) of the component.
            :param major: The latest version ARN of the created component, with the same major version.
            :param minor: The latest version ARN of the created component, with the same minor version.
            :param patch: The latest version ARN of the created component, with the same patch version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-component-latestversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                latest_version_property = imagebuilder_mixins.CfnComponentPropsMixin.LatestVersionProperty(
                    arn="arn",
                    major="major",
                    minor="minor",
                    patch="patch"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fbd8333bbfddaa60f3ce110cd311442d47e7ef04ce8d5633414fa74acfacb857)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument major", value=major, expected_type=type_hints["major"])
                check_type(argname="argument minor", value=minor, expected_type=type_hints["minor"])
                check_type(argname="argument patch", value=patch, expected_type=type_hints["patch"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if major is not None:
                self._values["major"] = major
            if minor is not None:
                self._values["minor"] = minor
            if patch is not None:
                self._values["patch"] = patch

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-component-latestversion.html#cfn-imagebuilder-component-latestversion-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def major(self) -> typing.Optional[builtins.str]:
            '''The latest version ARN of the created component, with the same major version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-component-latestversion.html#cfn-imagebuilder-component-latestversion-major
            '''
            result = self._values.get("major")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def minor(self) -> typing.Optional[builtins.str]:
            '''The latest version ARN of the created component, with the same minor version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-component-latestversion.html#cfn-imagebuilder-component-latestversion-minor
            '''
            result = self._values.get("minor")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def patch(self) -> typing.Optional[builtins.str]:
            '''The latest version ARN of the created component, with the same patch version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-component-latestversion.html#cfn-imagebuilder-component-latestversion-patch
            '''
            result = self._values.get("patch")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LatestVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnContainerRecipeMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "components": "components",
        "container_type": "containerType",
        "description": "description",
        "dockerfile_template_data": "dockerfileTemplateData",
        "dockerfile_template_uri": "dockerfileTemplateUri",
        "image_os_version_override": "imageOsVersionOverride",
        "instance_configuration": "instanceConfiguration",
        "kms_key_id": "kmsKeyId",
        "name": "name",
        "parent_image": "parentImage",
        "platform_override": "platformOverride",
        "tags": "tags",
        "target_repository": "targetRepository",
        "version": "version",
        "working_directory": "workingDirectory",
    },
)
class CfnContainerRecipeMixinProps:
    def __init__(
        self,
        *,
        components: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerRecipePropsMixin.ComponentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        container_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        dockerfile_template_data: typing.Optional[builtins.str] = None,
        dockerfile_template_uri: typing.Optional[builtins.str] = None,
        image_os_version_override: typing.Optional[builtins.str] = None,
        instance_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerRecipePropsMixin.InstanceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        parent_image: typing.Optional[builtins.str] = None,
        platform_override: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        target_repository: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerRecipePropsMixin.TargetContainerRepositoryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        version: typing.Optional[builtins.str] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnContainerRecipePropsMixin.

        :param components: Build and test components that are included in the container recipe. Recipes require a minimum of one build component, and can have a maximum of 20 build and test components in any combination.
        :param container_type: Specifies the type of container, such as Docker.
        :param description: The description of the container recipe.
        :param dockerfile_template_data: Dockerfiles are text documents that are used to build Docker containers, and ensure that they contain all of the elements required by the application running inside. The template data consists of contextual variables where Image Builder places build information or scripts, based on your container image recipe.
        :param dockerfile_template_uri: The S3 URI for the Dockerfile that will be used to build your container image.
        :param image_os_version_override: Specifies the operating system version for the base image.
        :param instance_configuration: A group of options that can be used to configure an instance for building and testing container images.
        :param kms_key_id: The Amazon Resource Name (ARN) that uniquely identifies which KMS key is used to encrypt the container image for distribution to the target Region. This can be either the Key ARN or the Alias ARN. For more information, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id-key-ARN>`_ in the *AWS Key Management Service Developer Guide* .
        :param name: The name of the container recipe.
        :param parent_image: The base image for customizations specified in the container recipe. This can contain an Image Builder image resource ARN or a container image URI, for example ``amazonlinux:latest`` .
        :param platform_override: Specifies the operating system platform when you use a custom base image.
        :param tags: Tags that are attached to the container recipe.
        :param target_repository: The destination repository for the container image.
        :param version: The semantic version of the container recipe. .. epigraph:: The semantic version has four nodes: ../. You can assign values for the first three, and can filter on all of them. *Assignment:* For the first three nodes you can assign any positive integer value, including zero, with an upper limit of 2^30-1, or 1073741823 for each node. Image Builder automatically assigns the build number to the fourth node. *Patterns:* You can use any numeric pattern that adheres to the assignment requirements for the nodes that you can assign. For example, you might choose a software version pattern, such as 1.0.0, or a date, such as 2021.01.01. *Filtering:* With semantic versioning, you have the flexibility to use wildcards (x) to specify the most recent versions or nodes when selecting the base image or components for your recipe. When you use a wildcard in any node, all nodes to the right of the first wildcard must also be wildcards.
        :param working_directory: The working directory for use during build and test workflows.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-containerrecipe.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
            
            cfn_container_recipe_mixin_props = imagebuilder_mixins.CfnContainerRecipeMixinProps(
                components=[imagebuilder_mixins.CfnContainerRecipePropsMixin.ComponentConfigurationProperty(
                    component_arn="componentArn",
                    parameters=[imagebuilder_mixins.CfnContainerRecipePropsMixin.ComponentParameterProperty(
                        name="name",
                        value=["value"]
                    )]
                )],
                container_type="containerType",
                description="description",
                dockerfile_template_data="dockerfileTemplateData",
                dockerfile_template_uri="dockerfileTemplateUri",
                image_os_version_override="imageOsVersionOverride",
                instance_configuration=imagebuilder_mixins.CfnContainerRecipePropsMixin.InstanceConfigurationProperty(
                    block_device_mappings=[imagebuilder_mixins.CfnContainerRecipePropsMixin.InstanceBlockDeviceMappingProperty(
                        device_name="deviceName",
                        ebs=imagebuilder_mixins.CfnContainerRecipePropsMixin.EbsInstanceBlockDeviceSpecificationProperty(
                            delete_on_termination=False,
                            encrypted=False,
                            iops=123,
                            kms_key_id="kmsKeyId",
                            snapshot_id="snapshotId",
                            throughput=123,
                            volume_size=123,
                            volume_type="volumeType"
                        ),
                        no_device="noDevice",
                        virtual_name="virtualName"
                    )],
                    image="image"
                ),
                kms_key_id="kmsKeyId",
                name="name",
                parent_image="parentImage",
                platform_override="platformOverride",
                tags={
                    "tags_key": "tags"
                },
                target_repository=imagebuilder_mixins.CfnContainerRecipePropsMixin.TargetContainerRepositoryProperty(
                    repository_name="repositoryName",
                    service="service"
                ),
                version="version",
                working_directory="workingDirectory"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb847caa035aac599de42b693db87703e24afb291316622ba170faf93af35552)
            check_type(argname="argument components", value=components, expected_type=type_hints["components"])
            check_type(argname="argument container_type", value=container_type, expected_type=type_hints["container_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dockerfile_template_data", value=dockerfile_template_data, expected_type=type_hints["dockerfile_template_data"])
            check_type(argname="argument dockerfile_template_uri", value=dockerfile_template_uri, expected_type=type_hints["dockerfile_template_uri"])
            check_type(argname="argument image_os_version_override", value=image_os_version_override, expected_type=type_hints["image_os_version_override"])
            check_type(argname="argument instance_configuration", value=instance_configuration, expected_type=type_hints["instance_configuration"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parent_image", value=parent_image, expected_type=type_hints["parent_image"])
            check_type(argname="argument platform_override", value=platform_override, expected_type=type_hints["platform_override"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_repository", value=target_repository, expected_type=type_hints["target_repository"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if components is not None:
            self._values["components"] = components
        if container_type is not None:
            self._values["container_type"] = container_type
        if description is not None:
            self._values["description"] = description
        if dockerfile_template_data is not None:
            self._values["dockerfile_template_data"] = dockerfile_template_data
        if dockerfile_template_uri is not None:
            self._values["dockerfile_template_uri"] = dockerfile_template_uri
        if image_os_version_override is not None:
            self._values["image_os_version_override"] = image_os_version_override
        if instance_configuration is not None:
            self._values["instance_configuration"] = instance_configuration
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if name is not None:
            self._values["name"] = name
        if parent_image is not None:
            self._values["parent_image"] = parent_image
        if platform_override is not None:
            self._values["platform_override"] = platform_override
        if tags is not None:
            self._values["tags"] = tags
        if target_repository is not None:
            self._values["target_repository"] = target_repository
        if version is not None:
            self._values["version"] = version
        if working_directory is not None:
            self._values["working_directory"] = working_directory

    @builtins.property
    def components(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerRecipePropsMixin.ComponentConfigurationProperty"]]]]:
        '''Build and test components that are included in the container recipe.

        Recipes require a minimum of one build component, and can have a maximum of 20 build and test components in any combination.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-containerrecipe.html#cfn-imagebuilder-containerrecipe-components
        '''
        result = self._values.get("components")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerRecipePropsMixin.ComponentConfigurationProperty"]]]], result)

    @builtins.property
    def container_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of container, such as Docker.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-containerrecipe.html#cfn-imagebuilder-containerrecipe-containertype
        '''
        result = self._values.get("container_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the container recipe.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-containerrecipe.html#cfn-imagebuilder-containerrecipe-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dockerfile_template_data(self) -> typing.Optional[builtins.str]:
        '''Dockerfiles are text documents that are used to build Docker containers, and ensure that they contain all of the elements required by the application running inside.

        The template data consists of contextual variables where Image Builder places build information or scripts, based on your container image recipe.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-containerrecipe.html#cfn-imagebuilder-containerrecipe-dockerfiletemplatedata
        '''
        result = self._values.get("dockerfile_template_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dockerfile_template_uri(self) -> typing.Optional[builtins.str]:
        '''The S3 URI for the Dockerfile that will be used to build your container image.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-containerrecipe.html#cfn-imagebuilder-containerrecipe-dockerfiletemplateuri
        '''
        result = self._values.get("dockerfile_template_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_os_version_override(self) -> typing.Optional[builtins.str]:
        '''Specifies the operating system version for the base image.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-containerrecipe.html#cfn-imagebuilder-containerrecipe-imageosversionoverride
        '''
        result = self._values.get("image_os_version_override")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerRecipePropsMixin.InstanceConfigurationProperty"]]:
        '''A group of options that can be used to configure an instance for building and testing container images.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-containerrecipe.html#cfn-imagebuilder-containerrecipe-instanceconfiguration
        '''
        result = self._values.get("instance_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerRecipePropsMixin.InstanceConfigurationProperty"]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) that uniquely identifies which KMS key is used to encrypt the container image for distribution to the target Region.

        This can be either the Key ARN or the Alias ARN. For more information, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id-key-ARN>`_ in the *AWS Key Management Service Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-containerrecipe.html#cfn-imagebuilder-containerrecipe-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the container recipe.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-containerrecipe.html#cfn-imagebuilder-containerrecipe-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent_image(self) -> typing.Optional[builtins.str]:
        '''The base image for customizations specified in the container recipe.

        This can contain an Image Builder image resource ARN or a container image URI, for example ``amazonlinux:latest`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-containerrecipe.html#cfn-imagebuilder-containerrecipe-parentimage
        '''
        result = self._values.get("parent_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def platform_override(self) -> typing.Optional[builtins.str]:
        '''Specifies the operating system platform when you use a custom base image.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-containerrecipe.html#cfn-imagebuilder-containerrecipe-platformoverride
        '''
        result = self._values.get("platform_override")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags that are attached to the container recipe.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-containerrecipe.html#cfn-imagebuilder-containerrecipe-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def target_repository(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerRecipePropsMixin.TargetContainerRepositoryProperty"]]:
        '''The destination repository for the container image.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-containerrecipe.html#cfn-imagebuilder-containerrecipe-targetrepository
        '''
        result = self._values.get("target_repository")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerRecipePropsMixin.TargetContainerRepositoryProperty"]], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The semantic version of the container recipe.

        .. epigraph::

           The semantic version has four nodes: ../. You can assign values for the first three, and can filter on all of them.

           *Assignment:* For the first three nodes you can assign any positive integer value, including zero, with an upper limit of 2^30-1, or 1073741823 for each node. Image Builder automatically assigns the build number to the fourth node.

           *Patterns:* You can use any numeric pattern that adheres to the assignment requirements for the nodes that you can assign. For example, you might choose a software version pattern, such as 1.0.0, or a date, such as 2021.01.01.

           *Filtering:* With semantic versioning, you have the flexibility to use wildcards (x) to specify the most recent versions or nodes when selecting the base image or components for your recipe. When you use a wildcard in any node, all nodes to the right of the first wildcard must also be wildcards.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-containerrecipe.html#cfn-imagebuilder-containerrecipe-version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def working_directory(self) -> typing.Optional[builtins.str]:
        '''The working directory for use during build and test workflows.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-containerrecipe.html#cfn-imagebuilder-containerrecipe-workingdirectory
        '''
        result = self._values.get("working_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnContainerRecipeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnContainerRecipePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnContainerRecipePropsMixin",
):
    '''Creates a new container recipe.

    Container recipes define how images are configured, tested, and assessed.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-containerrecipe.html
    :cloudformationResource: AWS::ImageBuilder::ContainerRecipe
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
        
        cfn_container_recipe_props_mixin = imagebuilder_mixins.CfnContainerRecipePropsMixin(imagebuilder_mixins.CfnContainerRecipeMixinProps(
            components=[imagebuilder_mixins.CfnContainerRecipePropsMixin.ComponentConfigurationProperty(
                component_arn="componentArn",
                parameters=[imagebuilder_mixins.CfnContainerRecipePropsMixin.ComponentParameterProperty(
                    name="name",
                    value=["value"]
                )]
            )],
            container_type="containerType",
            description="description",
            dockerfile_template_data="dockerfileTemplateData",
            dockerfile_template_uri="dockerfileTemplateUri",
            image_os_version_override="imageOsVersionOverride",
            instance_configuration=imagebuilder_mixins.CfnContainerRecipePropsMixin.InstanceConfigurationProperty(
                block_device_mappings=[imagebuilder_mixins.CfnContainerRecipePropsMixin.InstanceBlockDeviceMappingProperty(
                    device_name="deviceName",
                    ebs=imagebuilder_mixins.CfnContainerRecipePropsMixin.EbsInstanceBlockDeviceSpecificationProperty(
                        delete_on_termination=False,
                        encrypted=False,
                        iops=123,
                        kms_key_id="kmsKeyId",
                        snapshot_id="snapshotId",
                        throughput=123,
                        volume_size=123,
                        volume_type="volumeType"
                    ),
                    no_device="noDevice",
                    virtual_name="virtualName"
                )],
                image="image"
            ),
            kms_key_id="kmsKeyId",
            name="name",
            parent_image="parentImage",
            platform_override="platformOverride",
            tags={
                "tags_key": "tags"
            },
            target_repository=imagebuilder_mixins.CfnContainerRecipePropsMixin.TargetContainerRepositoryProperty(
                repository_name="repositoryName",
                service="service"
            ),
            version="version",
            working_directory="workingDirectory"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnContainerRecipeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ImageBuilder::ContainerRecipe``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9bdacb971719c6eb23ce759ee448bfac400e6d55f35c67726be642d982f24a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84111cf6fdb84022f94e69a0780b925ce8249842ec710ebcb53679a8b2e65b82)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__332fd52633ffd8eae8424c70dafb0b6258e353999523357b635b61afc465186b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnContainerRecipeMixinProps:
        return typing.cast(CfnContainerRecipeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnContainerRecipePropsMixin.ComponentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"component_arn": "componentArn", "parameters": "parameters"},
    )
    class ComponentConfigurationProperty:
        def __init__(
            self,
            *,
            component_arn: typing.Optional[builtins.str] = None,
            parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerRecipePropsMixin.ComponentParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Configuration details of the component.

            :param component_arn: The Amazon Resource Name (ARN) of the component.
            :param parameters: A group of parameter settings that Image Builder uses to configure the component for a specific recipe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-componentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                component_configuration_property = imagebuilder_mixins.CfnContainerRecipePropsMixin.ComponentConfigurationProperty(
                    component_arn="componentArn",
                    parameters=[imagebuilder_mixins.CfnContainerRecipePropsMixin.ComponentParameterProperty(
                        name="name",
                        value=["value"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__305fd1216bc344263315e22c2363af13b5338719e435fbc18232574075d7ed18)
                check_type(argname="argument component_arn", value=component_arn, expected_type=type_hints["component_arn"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if component_arn is not None:
                self._values["component_arn"] = component_arn
            if parameters is not None:
                self._values["parameters"] = parameters

        @builtins.property
        def component_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-componentconfiguration.html#cfn-imagebuilder-containerrecipe-componentconfiguration-componentarn
            '''
            result = self._values.get("component_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerRecipePropsMixin.ComponentParameterProperty"]]]]:
            '''A group of parameter settings that Image Builder uses to configure the component for a specific recipe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-componentconfiguration.html#cfn-imagebuilder-containerrecipe-componentconfiguration-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerRecipePropsMixin.ComponentParameterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnContainerRecipePropsMixin.ComponentParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class ComponentParameterProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Contains a key/value pair that sets the named component parameter.

            :param name: The name of the component parameter to set.
            :param value: Sets the value for the named component parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-componentparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                component_parameter_property = imagebuilder_mixins.CfnContainerRecipePropsMixin.ComponentParameterProperty(
                    name="name",
                    value=["value"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9f49826fb7d32cb4b27e303ca608466b0c67057e0f5b00034eb6ef4fd6a1b713)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the component parameter to set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-componentparameter.html#cfn-imagebuilder-containerrecipe-componentparameter-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Sets the value for the named component parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-componentparameter.html#cfn-imagebuilder-containerrecipe-componentparameter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnContainerRecipePropsMixin.EbsInstanceBlockDeviceSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delete_on_termination": "deleteOnTermination",
            "encrypted": "encrypted",
            "iops": "iops",
            "kms_key_id": "kmsKeyId",
            "snapshot_id": "snapshotId",
            "throughput": "throughput",
            "volume_size": "volumeSize",
            "volume_type": "volumeType",
        },
    )
    class EbsInstanceBlockDeviceSpecificationProperty:
        def __init__(
            self,
            *,
            delete_on_termination: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            iops: typing.Optional[jsii.Number] = None,
            kms_key_id: typing.Optional[builtins.str] = None,
            snapshot_id: typing.Optional[builtins.str] = None,
            throughput: typing.Optional[jsii.Number] = None,
            volume_size: typing.Optional[jsii.Number] = None,
            volume_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Amazon EBS-specific block device mapping specifications.

            :param delete_on_termination: Use to configure delete on termination of the associated device.
            :param encrypted: Use to configure device encryption.
            :param iops: Use to configure device IOPS.
            :param kms_key_id: The Amazon Resource Name (ARN) that uniquely identifies the KMS key to use when encrypting the device. This can be either the Key ARN or the Alias ARN. For more information, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id-key-ARN>`_ in the *AWS Key Management Service Developer Guide* .
            :param snapshot_id: The snapshot that defines the device contents.
            :param throughput: *For GP3 volumes only* – The throughput in MiB/s that the volume supports.
            :param volume_size: Use to override the device's volume size.
            :param volume_type: Use to override the device's volume type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-ebsinstanceblockdevicespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                ebs_instance_block_device_specification_property = imagebuilder_mixins.CfnContainerRecipePropsMixin.EbsInstanceBlockDeviceSpecificationProperty(
                    delete_on_termination=False,
                    encrypted=False,
                    iops=123,
                    kms_key_id="kmsKeyId",
                    snapshot_id="snapshotId",
                    throughput=123,
                    volume_size=123,
                    volume_type="volumeType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d9cd28b75ff4890d493041602d0d795edacc4e0a7f4755b31e68ac5c19096202)
                check_type(argname="argument delete_on_termination", value=delete_on_termination, expected_type=type_hints["delete_on_termination"])
                check_type(argname="argument encrypted", value=encrypted, expected_type=type_hints["encrypted"])
                check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
                check_type(argname="argument snapshot_id", value=snapshot_id, expected_type=type_hints["snapshot_id"])
                check_type(argname="argument throughput", value=throughput, expected_type=type_hints["throughput"])
                check_type(argname="argument volume_size", value=volume_size, expected_type=type_hints["volume_size"])
                check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delete_on_termination is not None:
                self._values["delete_on_termination"] = delete_on_termination
            if encrypted is not None:
                self._values["encrypted"] = encrypted
            if iops is not None:
                self._values["iops"] = iops
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id
            if snapshot_id is not None:
                self._values["snapshot_id"] = snapshot_id
            if throughput is not None:
                self._values["throughput"] = throughput
            if volume_size is not None:
                self._values["volume_size"] = volume_size
            if volume_type is not None:
                self._values["volume_type"] = volume_type

        @builtins.property
        def delete_on_termination(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Use to configure delete on termination of the associated device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-ebsinstanceblockdevicespecification.html#cfn-imagebuilder-containerrecipe-ebsinstanceblockdevicespecification-deleteontermination
            '''
            result = self._values.get("delete_on_termination")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def encrypted(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Use to configure device encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-ebsinstanceblockdevicespecification.html#cfn-imagebuilder-containerrecipe-ebsinstanceblockdevicespecification-encrypted
            '''
            result = self._values.get("encrypted")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            '''Use to configure device IOPS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-ebsinstanceblockdevicespecification.html#cfn-imagebuilder-containerrecipe-ebsinstanceblockdevicespecification-iops
            '''
            result = self._values.get("iops")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) that uniquely identifies the KMS key to use when encrypting the device.

            This can be either the Key ARN or the Alias ARN. For more information, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id-key-ARN>`_ in the *AWS Key Management Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-ebsinstanceblockdevicespecification.html#cfn-imagebuilder-containerrecipe-ebsinstanceblockdevicespecification-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def snapshot_id(self) -> typing.Optional[builtins.str]:
            '''The snapshot that defines the device contents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-ebsinstanceblockdevicespecification.html#cfn-imagebuilder-containerrecipe-ebsinstanceblockdevicespecification-snapshotid
            '''
            result = self._values.get("snapshot_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def throughput(self) -> typing.Optional[jsii.Number]:
            '''*For GP3 volumes only* – The throughput in MiB/s that the volume supports.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-ebsinstanceblockdevicespecification.html#cfn-imagebuilder-containerrecipe-ebsinstanceblockdevicespecification-throughput
            '''
            result = self._values.get("throughput")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def volume_size(self) -> typing.Optional[jsii.Number]:
            '''Use to override the device's volume size.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-ebsinstanceblockdevicespecification.html#cfn-imagebuilder-containerrecipe-ebsinstanceblockdevicespecification-volumesize
            '''
            result = self._values.get("volume_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def volume_type(self) -> typing.Optional[builtins.str]:
            '''Use to override the device's volume type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-ebsinstanceblockdevicespecification.html#cfn-imagebuilder-containerrecipe-ebsinstanceblockdevicespecification-volumetype
            '''
            result = self._values.get("volume_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EbsInstanceBlockDeviceSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnContainerRecipePropsMixin.InstanceBlockDeviceMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "device_name": "deviceName",
            "ebs": "ebs",
            "no_device": "noDevice",
            "virtual_name": "virtualName",
        },
    )
    class InstanceBlockDeviceMappingProperty:
        def __init__(
            self,
            *,
            device_name: typing.Optional[builtins.str] = None,
            ebs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerRecipePropsMixin.EbsInstanceBlockDeviceSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            no_device: typing.Optional[builtins.str] = None,
            virtual_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines block device mappings for the instance used to configure your image.

            :param device_name: The device to which these mappings apply.
            :param ebs: Use to manage Amazon EBS-specific configuration for this mapping.
            :param no_device: Use to remove a mapping from the base image.
            :param virtual_name: Use to manage instance ephemeral devices.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-instanceblockdevicemapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                instance_block_device_mapping_property = imagebuilder_mixins.CfnContainerRecipePropsMixin.InstanceBlockDeviceMappingProperty(
                    device_name="deviceName",
                    ebs=imagebuilder_mixins.CfnContainerRecipePropsMixin.EbsInstanceBlockDeviceSpecificationProperty(
                        delete_on_termination=False,
                        encrypted=False,
                        iops=123,
                        kms_key_id="kmsKeyId",
                        snapshot_id="snapshotId",
                        throughput=123,
                        volume_size=123,
                        volume_type="volumeType"
                    ),
                    no_device="noDevice",
                    virtual_name="virtualName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cf06f10e08ce3e71d700dd051246985c2819b35d4dafaeb962d460100c9582b8)
                check_type(argname="argument device_name", value=device_name, expected_type=type_hints["device_name"])
                check_type(argname="argument ebs", value=ebs, expected_type=type_hints["ebs"])
                check_type(argname="argument no_device", value=no_device, expected_type=type_hints["no_device"])
                check_type(argname="argument virtual_name", value=virtual_name, expected_type=type_hints["virtual_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if device_name is not None:
                self._values["device_name"] = device_name
            if ebs is not None:
                self._values["ebs"] = ebs
            if no_device is not None:
                self._values["no_device"] = no_device
            if virtual_name is not None:
                self._values["virtual_name"] = virtual_name

        @builtins.property
        def device_name(self) -> typing.Optional[builtins.str]:
            '''The device to which these mappings apply.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-instanceblockdevicemapping.html#cfn-imagebuilder-containerrecipe-instanceblockdevicemapping-devicename
            '''
            result = self._values.get("device_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ebs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerRecipePropsMixin.EbsInstanceBlockDeviceSpecificationProperty"]]:
            '''Use to manage Amazon EBS-specific configuration for this mapping.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-instanceblockdevicemapping.html#cfn-imagebuilder-containerrecipe-instanceblockdevicemapping-ebs
            '''
            result = self._values.get("ebs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerRecipePropsMixin.EbsInstanceBlockDeviceSpecificationProperty"]], result)

        @builtins.property
        def no_device(self) -> typing.Optional[builtins.str]:
            '''Use to remove a mapping from the base image.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-instanceblockdevicemapping.html#cfn-imagebuilder-containerrecipe-instanceblockdevicemapping-nodevice
            '''
            result = self._values.get("no_device")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def virtual_name(self) -> typing.Optional[builtins.str]:
            '''Use to manage instance ephemeral devices.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-instanceblockdevicemapping.html#cfn-imagebuilder-containerrecipe-instanceblockdevicemapping-virtualname
            '''
            result = self._values.get("virtual_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceBlockDeviceMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnContainerRecipePropsMixin.InstanceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "block_device_mappings": "blockDeviceMappings",
            "image": "image",
        },
    )
    class InstanceConfigurationProperty:
        def __init__(
            self,
            *,
            block_device_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerRecipePropsMixin.InstanceBlockDeviceMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            image: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines a custom base AMI and block device mapping configurations of an instance used for building and testing container images.

            :param block_device_mappings: Defines the block devices to attach for building an instance from this Image Builder AMI.
            :param image: The base image for a container build and test instance. This can contain an AMI ID or it can specify an AWS Systems Manager (SSM) Parameter Store Parameter, prefixed by ``ssm:`` , followed by the parameter name or ARN. If not specified, Image Builder uses the appropriate ECS-optimized AMI as a base image.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-instanceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                instance_configuration_property = imagebuilder_mixins.CfnContainerRecipePropsMixin.InstanceConfigurationProperty(
                    block_device_mappings=[imagebuilder_mixins.CfnContainerRecipePropsMixin.InstanceBlockDeviceMappingProperty(
                        device_name="deviceName",
                        ebs=imagebuilder_mixins.CfnContainerRecipePropsMixin.EbsInstanceBlockDeviceSpecificationProperty(
                            delete_on_termination=False,
                            encrypted=False,
                            iops=123,
                            kms_key_id="kmsKeyId",
                            snapshot_id="snapshotId",
                            throughput=123,
                            volume_size=123,
                            volume_type="volumeType"
                        ),
                        no_device="noDevice",
                        virtual_name="virtualName"
                    )],
                    image="image"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f2544d6afb790471e477d386eec39fb0b051308e21e08b6e281f402a662fa48d)
                check_type(argname="argument block_device_mappings", value=block_device_mappings, expected_type=type_hints["block_device_mappings"])
                check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if block_device_mappings is not None:
                self._values["block_device_mappings"] = block_device_mappings
            if image is not None:
                self._values["image"] = image

        @builtins.property
        def block_device_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerRecipePropsMixin.InstanceBlockDeviceMappingProperty"]]]]:
            '''Defines the block devices to attach for building an instance from this Image Builder AMI.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-instanceconfiguration.html#cfn-imagebuilder-containerrecipe-instanceconfiguration-blockdevicemappings
            '''
            result = self._values.get("block_device_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerRecipePropsMixin.InstanceBlockDeviceMappingProperty"]]]], result)

        @builtins.property
        def image(self) -> typing.Optional[builtins.str]:
            '''The base image for a container build and test instance.

            This can contain an AMI ID or it can specify an AWS Systems Manager (SSM) Parameter Store Parameter, prefixed by ``ssm:`` , followed by the parameter name or ARN.

            If not specified, Image Builder uses the appropriate ECS-optimized AMI as a base image.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-instanceconfiguration.html#cfn-imagebuilder-containerrecipe-instanceconfiguration-image
            '''
            result = self._values.get("image")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnContainerRecipePropsMixin.LatestVersionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "major": "major",
            "minor": "minor",
            "patch": "patch",
        },
    )
    class LatestVersionProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            major: typing.Optional[builtins.str] = None,
            minor: typing.Optional[builtins.str] = None,
            patch: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The latest version references of the container recipe.

            :param arn: The Amazon Resource Name (ARN) of the container recipe. .. epigraph:: Semantic versioning is included in each object's Amazon Resource Name (ARN), at the level that applies to that object as follows: - Versionless ARNs and Name ARNs do not include specific values in any of the nodes. The nodes are either left off entirely, or they are specified as wildcards, for example: x.x.x. - Version ARNs have only the first three nodes: .. - Build version ARNs have all four nodes, and point to a specific build for a specific version of an object.
            :param major: The latest version ARN of the created container recipe, with the same major version.
            :param minor: The latest version ARN of the created container recipe, with the same minor version.
            :param patch: The latest version ARN of the created container recipe, with the same patch version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-latestversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                latest_version_property = imagebuilder_mixins.CfnContainerRecipePropsMixin.LatestVersionProperty(
                    arn="arn",
                    major="major",
                    minor="minor",
                    patch="patch"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8908054bb81c05fa34d32d72af4b393061d9e70dae351d1064ec90299eabcd2b)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument major", value=major, expected_type=type_hints["major"])
                check_type(argname="argument minor", value=minor, expected_type=type_hints["minor"])
                check_type(argname="argument patch", value=patch, expected_type=type_hints["patch"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if major is not None:
                self._values["major"] = major
            if minor is not None:
                self._values["minor"] = minor
            if patch is not None:
                self._values["patch"] = patch

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the container recipe.

            .. epigraph::

               Semantic versioning is included in each object's Amazon Resource Name (ARN), at the level that applies to that object as follows:

               - Versionless ARNs and Name ARNs do not include specific values in any of the nodes. The nodes are either left off entirely, or they are specified as wildcards, for example: x.x.x.
               - Version ARNs have only the first three nodes: ..
               - Build version ARNs have all four nodes, and point to a specific build for a specific version of an object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-latestversion.html#cfn-imagebuilder-containerrecipe-latestversion-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def major(self) -> typing.Optional[builtins.str]:
            '''The latest version ARN of the created container recipe, with the same major version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-latestversion.html#cfn-imagebuilder-containerrecipe-latestversion-major
            '''
            result = self._values.get("major")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def minor(self) -> typing.Optional[builtins.str]:
            '''The latest version ARN of the created container recipe, with the same minor version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-latestversion.html#cfn-imagebuilder-containerrecipe-latestversion-minor
            '''
            result = self._values.get("minor")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def patch(self) -> typing.Optional[builtins.str]:
            '''The latest version ARN of the created container recipe, with the same patch version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-latestversion.html#cfn-imagebuilder-containerrecipe-latestversion-patch
            '''
            result = self._values.get("patch")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LatestVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnContainerRecipePropsMixin.TargetContainerRepositoryProperty",
        jsii_struct_bases=[],
        name_mapping={"repository_name": "repositoryName", "service": "service"},
    )
    class TargetContainerRepositoryProperty:
        def __init__(
            self,
            *,
            repository_name: typing.Optional[builtins.str] = None,
            service: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The container repository where the output container image is stored.

            :param repository_name: The name of the container repository where the output container image is stored. This name is prefixed by the repository location. For example, ``<repository location url>/repository_name`` .
            :param service: Specifies the service in which this image was registered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-targetcontainerrepository.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                target_container_repository_property = imagebuilder_mixins.CfnContainerRecipePropsMixin.TargetContainerRepositoryProperty(
                    repository_name="repositoryName",
                    service="service"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3a11d0a86c7bf94dae19bc1e958caf487349d8272b06bf288512007c7d508d34)
                check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
                check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if repository_name is not None:
                self._values["repository_name"] = repository_name
            if service is not None:
                self._values["service"] = service

        @builtins.property
        def repository_name(self) -> typing.Optional[builtins.str]:
            '''The name of the container repository where the output container image is stored.

            This name is prefixed by the repository location. For example, ``<repository location url>/repository_name`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-targetcontainerrepository.html#cfn-imagebuilder-containerrecipe-targetcontainerrepository-repositoryname
            '''
            result = self._values.get("repository_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service(self) -> typing.Optional[builtins.str]:
            '''Specifies the service in which this image was registered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-containerrecipe-targetcontainerrepository.html#cfn-imagebuilder-containerrecipe-targetcontainerrepository-service
            '''
            result = self._values.get("service")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetContainerRepositoryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnDistributionConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "distributions": "distributions",
        "name": "name",
        "tags": "tags",
    },
)
class CfnDistributionConfigurationMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        distributions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDistributionConfigurationPropsMixin.DistributionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnDistributionConfigurationPropsMixin.

        :param description: The description of this distribution configuration.
        :param distributions: The distributions of this distribution configuration formatted as an array of Distribution objects.
        :param name: The name of this distribution configuration.
        :param tags: The tags of this distribution configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-distributionconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
            
            # ami_distribution_configuration: Any
            # container_distribution_configuration: Any
            
            cfn_distribution_configuration_mixin_props = imagebuilder_mixins.CfnDistributionConfigurationMixinProps(
                description="description",
                distributions=[imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.DistributionProperty(
                    ami_distribution_configuration=ami_distribution_configuration,
                    container_distribution_configuration=container_distribution_configuration,
                    fast_launch_configurations=[imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.FastLaunchConfigurationProperty(
                        account_id="accountId",
                        enabled=False,
                        launch_template=imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.FastLaunchLaunchTemplateSpecificationProperty(
                            launch_template_id="launchTemplateId",
                            launch_template_name="launchTemplateName",
                            launch_template_version="launchTemplateVersion"
                        ),
                        max_parallel_launches=123,
                        snapshot_configuration=imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.FastLaunchSnapshotConfigurationProperty(
                            target_resource_count=123
                        )
                    )],
                    launch_template_configurations=[imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.LaunchTemplateConfigurationProperty(
                        account_id="accountId",
                        launch_template_id="launchTemplateId",
                        set_default_version=False
                    )],
                    license_configuration_arns=["licenseConfigurationArns"],
                    region="region",
                    ssm_parameter_configurations=[imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.SsmParameterConfigurationProperty(
                        ami_account_id="amiAccountId",
                        data_type="dataType",
                        parameter_name="parameterName"
                    )]
                )],
                name="name",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a343519e497d7ac5b5c113d0bc8760207a24cd629f687d0f119c3c117e689048)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument distributions", value=distributions, expected_type=type_hints["distributions"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if distributions is not None:
            self._values["distributions"] = distributions
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of this distribution configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-distributionconfiguration.html#cfn-imagebuilder-distributionconfiguration-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def distributions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionConfigurationPropsMixin.DistributionProperty"]]]]:
        '''The distributions of this distribution configuration formatted as an array of Distribution objects.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-distributionconfiguration.html#cfn-imagebuilder-distributionconfiguration-distributions
        '''
        result = self._values.get("distributions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionConfigurationPropsMixin.DistributionProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of this distribution configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-distributionconfiguration.html#cfn-imagebuilder-distributionconfiguration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags of this distribution configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-distributionconfiguration.html#cfn-imagebuilder-distributionconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDistributionConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDistributionConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnDistributionConfigurationPropsMixin",
):
    '''A distribution configuration allows you to specify the name and description of your output AMI, authorize other AWS account s to launch the AMI, and replicate the AMI to other AWS Regions .

    It also allows you to export the AMI to Amazon S3 .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-distributionconfiguration.html
    :cloudformationResource: AWS::ImageBuilder::DistributionConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
        
        # ami_distribution_configuration: Any
        # container_distribution_configuration: Any
        
        cfn_distribution_configuration_props_mixin = imagebuilder_mixins.CfnDistributionConfigurationPropsMixin(imagebuilder_mixins.CfnDistributionConfigurationMixinProps(
            description="description",
            distributions=[imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.DistributionProperty(
                ami_distribution_configuration=ami_distribution_configuration,
                container_distribution_configuration=container_distribution_configuration,
                fast_launch_configurations=[imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.FastLaunchConfigurationProperty(
                    account_id="accountId",
                    enabled=False,
                    launch_template=imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.FastLaunchLaunchTemplateSpecificationProperty(
                        launch_template_id="launchTemplateId",
                        launch_template_name="launchTemplateName",
                        launch_template_version="launchTemplateVersion"
                    ),
                    max_parallel_launches=123,
                    snapshot_configuration=imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.FastLaunchSnapshotConfigurationProperty(
                        target_resource_count=123
                    )
                )],
                launch_template_configurations=[imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.LaunchTemplateConfigurationProperty(
                    account_id="accountId",
                    launch_template_id="launchTemplateId",
                    set_default_version=False
                )],
                license_configuration_arns=["licenseConfigurationArns"],
                region="region",
                ssm_parameter_configurations=[imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.SsmParameterConfigurationProperty(
                    ami_account_id="amiAccountId",
                    data_type="dataType",
                    parameter_name="parameterName"
                )]
            )],
            name="name",
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDistributionConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ImageBuilder::DistributionConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__931511f93eb221d393140d26e63c9cb8ef03da9d60a13afd49d00b11fdf2d511)
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
            type_hints = typing.get_type_hints(_typecheckingstub__176c4d269f0ca75453856aa6011e2f007d5f35ba8a16918d8692468b3efff454)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36365b3bc852b3084790bf3dfaa791cb2ec291c416e6c80e765332abb0565895)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDistributionConfigurationMixinProps:
        return typing.cast(CfnDistributionConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnDistributionConfigurationPropsMixin.DistributionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ami_distribution_configuration": "amiDistributionConfiguration",
            "container_distribution_configuration": "containerDistributionConfiguration",
            "fast_launch_configurations": "fastLaunchConfigurations",
            "launch_template_configurations": "launchTemplateConfigurations",
            "license_configuration_arns": "licenseConfigurationArns",
            "region": "region",
            "ssm_parameter_configurations": "ssmParameterConfigurations",
        },
    )
    class DistributionProperty:
        def __init__(
            self,
            *,
            ami_distribution_configuration: typing.Any = None,
            container_distribution_configuration: typing.Any = None,
            fast_launch_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDistributionConfigurationPropsMixin.FastLaunchConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            launch_template_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDistributionConfigurationPropsMixin.LaunchTemplateConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            license_configuration_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
            region: typing.Optional[builtins.str] = None,
            ssm_parameter_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDistributionConfigurationPropsMixin.SsmParameterConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The distribution configuration distribution defines the settings for a specific Region in the Distribution Configuration.

            You must specify whether the distribution is for an AMI or a container image. To do so, include exactly one of the following data types for your distribution:

            - amiDistributionConfiguration
            - containerDistributionConfiguration

            :param ami_distribution_configuration: The specific AMI settings, such as launch permissions and AMI tags. For details, see example schema below.
            :param container_distribution_configuration: Container distribution settings for encryption, licensing, and sharing in a specific Region. For details, see example schema below.
            :param fast_launch_configurations: The Windows faster-launching configurations to use for AMI distribution.
            :param launch_template_configurations: A group of launchTemplateConfiguration settings that apply to image distribution for specified accounts.
            :param license_configuration_arns: The License Manager Configuration to associate with the AMI in the specified Region. For more information, see the `LicenseConfiguration API <https://docs.aws.amazon.com/license-manager/latest/APIReference/API_LicenseConfiguration.html>`_ .
            :param region: The target Region for the Distribution Configuration. For example, ``eu-west-1`` .
            :param ssm_parameter_configurations: Contains settings to update AWS Systems Manager (SSM) Parameter Store Parameters with output AMI IDs from the build by target Region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-distribution.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                # ami_distribution_configuration: Any
                # container_distribution_configuration: Any
                
                distribution_property = imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.DistributionProperty(
                    ami_distribution_configuration=ami_distribution_configuration,
                    container_distribution_configuration=container_distribution_configuration,
                    fast_launch_configurations=[imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.FastLaunchConfigurationProperty(
                        account_id="accountId",
                        enabled=False,
                        launch_template=imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.FastLaunchLaunchTemplateSpecificationProperty(
                            launch_template_id="launchTemplateId",
                            launch_template_name="launchTemplateName",
                            launch_template_version="launchTemplateVersion"
                        ),
                        max_parallel_launches=123,
                        snapshot_configuration=imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.FastLaunchSnapshotConfigurationProperty(
                            target_resource_count=123
                        )
                    )],
                    launch_template_configurations=[imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.LaunchTemplateConfigurationProperty(
                        account_id="accountId",
                        launch_template_id="launchTemplateId",
                        set_default_version=False
                    )],
                    license_configuration_arns=["licenseConfigurationArns"],
                    region="region",
                    ssm_parameter_configurations=[imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.SsmParameterConfigurationProperty(
                        ami_account_id="amiAccountId",
                        data_type="dataType",
                        parameter_name="parameterName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bff2af02862e582d91f05198f5dd6e059c900122b200f836f459723f32fc904b)
                check_type(argname="argument ami_distribution_configuration", value=ami_distribution_configuration, expected_type=type_hints["ami_distribution_configuration"])
                check_type(argname="argument container_distribution_configuration", value=container_distribution_configuration, expected_type=type_hints["container_distribution_configuration"])
                check_type(argname="argument fast_launch_configurations", value=fast_launch_configurations, expected_type=type_hints["fast_launch_configurations"])
                check_type(argname="argument launch_template_configurations", value=launch_template_configurations, expected_type=type_hints["launch_template_configurations"])
                check_type(argname="argument license_configuration_arns", value=license_configuration_arns, expected_type=type_hints["license_configuration_arns"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
                check_type(argname="argument ssm_parameter_configurations", value=ssm_parameter_configurations, expected_type=type_hints["ssm_parameter_configurations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ami_distribution_configuration is not None:
                self._values["ami_distribution_configuration"] = ami_distribution_configuration
            if container_distribution_configuration is not None:
                self._values["container_distribution_configuration"] = container_distribution_configuration
            if fast_launch_configurations is not None:
                self._values["fast_launch_configurations"] = fast_launch_configurations
            if launch_template_configurations is not None:
                self._values["launch_template_configurations"] = launch_template_configurations
            if license_configuration_arns is not None:
                self._values["license_configuration_arns"] = license_configuration_arns
            if region is not None:
                self._values["region"] = region
            if ssm_parameter_configurations is not None:
                self._values["ssm_parameter_configurations"] = ssm_parameter_configurations

        @builtins.property
        def ami_distribution_configuration(self) -> typing.Any:
            '''The specific AMI settings, such as launch permissions and AMI tags.

            For details, see example schema below.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-distribution.html#cfn-imagebuilder-distributionconfiguration-distribution-amidistributionconfiguration
            '''
            result = self._values.get("ami_distribution_configuration")
            return typing.cast(typing.Any, result)

        @builtins.property
        def container_distribution_configuration(self) -> typing.Any:
            '''Container distribution settings for encryption, licensing, and sharing in a specific Region.

            For details, see example schema below.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-distribution.html#cfn-imagebuilder-distributionconfiguration-distribution-containerdistributionconfiguration
            '''
            result = self._values.get("container_distribution_configuration")
            return typing.cast(typing.Any, result)

        @builtins.property
        def fast_launch_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionConfigurationPropsMixin.FastLaunchConfigurationProperty"]]]]:
            '''The Windows faster-launching configurations to use for AMI distribution.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-distribution.html#cfn-imagebuilder-distributionconfiguration-distribution-fastlaunchconfigurations
            '''
            result = self._values.get("fast_launch_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionConfigurationPropsMixin.FastLaunchConfigurationProperty"]]]], result)

        @builtins.property
        def launch_template_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionConfigurationPropsMixin.LaunchTemplateConfigurationProperty"]]]]:
            '''A group of launchTemplateConfiguration settings that apply to image distribution for specified accounts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-distribution.html#cfn-imagebuilder-distributionconfiguration-distribution-launchtemplateconfigurations
            '''
            result = self._values.get("launch_template_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionConfigurationPropsMixin.LaunchTemplateConfigurationProperty"]]]], result)

        @builtins.property
        def license_configuration_arns(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The License Manager Configuration to associate with the AMI in the specified Region.

            For more information, see the `LicenseConfiguration API <https://docs.aws.amazon.com/license-manager/latest/APIReference/API_LicenseConfiguration.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-distribution.html#cfn-imagebuilder-distributionconfiguration-distribution-licenseconfigurationarns
            '''
            result = self._values.get("license_configuration_arns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The target Region for the Distribution Configuration.

            For example, ``eu-west-1`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-distribution.html#cfn-imagebuilder-distributionconfiguration-distribution-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ssm_parameter_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionConfigurationPropsMixin.SsmParameterConfigurationProperty"]]]]:
            '''Contains settings to update AWS Systems Manager (SSM) Parameter Store Parameters with output AMI IDs from the build by target Region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-distribution.html#cfn-imagebuilder-distributionconfiguration-distribution-ssmparameterconfigurations
            '''
            result = self._values.get("ssm_parameter_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionConfigurationPropsMixin.SsmParameterConfigurationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DistributionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnDistributionConfigurationPropsMixin.FastLaunchConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_id": "accountId",
            "enabled": "enabled",
            "launch_template": "launchTemplate",
            "max_parallel_launches": "maxParallelLaunches",
            "snapshot_configuration": "snapshotConfiguration",
        },
    )
    class FastLaunchConfigurationProperty:
        def __init__(
            self,
            *,
            account_id: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            launch_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDistributionConfigurationPropsMixin.FastLaunchLaunchTemplateSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            max_parallel_launches: typing.Optional[jsii.Number] = None,
            snapshot_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDistributionConfigurationPropsMixin.FastLaunchSnapshotConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Define and configure faster launching for output Windows AMIs.

            :param account_id: The owner account ID for the fast-launch enabled Windows AMI.
            :param enabled: A Boolean that represents the current state of faster launching for the Windows AMI. Set to ``true`` to start using Windows faster launching, or ``false`` to stop using it.
            :param launch_template: The launch template that the fast-launch enabled Windows AMI uses when it launches Windows instances to create pre-provisioned snapshots.
            :param max_parallel_launches: The maximum number of parallel instances that are launched for creating resources.
            :param snapshot_configuration: Configuration settings for managing the number of snapshots that are created from pre-provisioned instances for the Windows AMI when faster launching is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-fastlaunchconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                fast_launch_configuration_property = imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.FastLaunchConfigurationProperty(
                    account_id="accountId",
                    enabled=False,
                    launch_template=imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.FastLaunchLaunchTemplateSpecificationProperty(
                        launch_template_id="launchTemplateId",
                        launch_template_name="launchTemplateName",
                        launch_template_version="launchTemplateVersion"
                    ),
                    max_parallel_launches=123,
                    snapshot_configuration=imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.FastLaunchSnapshotConfigurationProperty(
                        target_resource_count=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1d4e0cd215be1dd530816ab499c882bdbe68e22922053d767a9a6f7379755d77)
                check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument launch_template", value=launch_template, expected_type=type_hints["launch_template"])
                check_type(argname="argument max_parallel_launches", value=max_parallel_launches, expected_type=type_hints["max_parallel_launches"])
                check_type(argname="argument snapshot_configuration", value=snapshot_configuration, expected_type=type_hints["snapshot_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_id is not None:
                self._values["account_id"] = account_id
            if enabled is not None:
                self._values["enabled"] = enabled
            if launch_template is not None:
                self._values["launch_template"] = launch_template
            if max_parallel_launches is not None:
                self._values["max_parallel_launches"] = max_parallel_launches
            if snapshot_configuration is not None:
                self._values["snapshot_configuration"] = snapshot_configuration

        @builtins.property
        def account_id(self) -> typing.Optional[builtins.str]:
            '''The owner account ID for the fast-launch enabled Windows AMI.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-fastlaunchconfiguration.html#cfn-imagebuilder-distributionconfiguration-fastlaunchconfiguration-accountid
            '''
            result = self._values.get("account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A Boolean that represents the current state of faster launching for the Windows AMI.

            Set to ``true`` to start using Windows faster launching, or ``false`` to stop using it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-fastlaunchconfiguration.html#cfn-imagebuilder-distributionconfiguration-fastlaunchconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def launch_template(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionConfigurationPropsMixin.FastLaunchLaunchTemplateSpecificationProperty"]]:
            '''The launch template that the fast-launch enabled Windows AMI uses when it launches Windows instances to create pre-provisioned snapshots.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-fastlaunchconfiguration.html#cfn-imagebuilder-distributionconfiguration-fastlaunchconfiguration-launchtemplate
            '''
            result = self._values.get("launch_template")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionConfigurationPropsMixin.FastLaunchLaunchTemplateSpecificationProperty"]], result)

        @builtins.property
        def max_parallel_launches(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of parallel instances that are launched for creating resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-fastlaunchconfiguration.html#cfn-imagebuilder-distributionconfiguration-fastlaunchconfiguration-maxparallellaunches
            '''
            result = self._values.get("max_parallel_launches")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def snapshot_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionConfigurationPropsMixin.FastLaunchSnapshotConfigurationProperty"]]:
            '''Configuration settings for managing the number of snapshots that are created from pre-provisioned instances for the Windows AMI when faster launching is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-fastlaunchconfiguration.html#cfn-imagebuilder-distributionconfiguration-fastlaunchconfiguration-snapshotconfiguration
            '''
            result = self._values.get("snapshot_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionConfigurationPropsMixin.FastLaunchSnapshotConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FastLaunchConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnDistributionConfigurationPropsMixin.FastLaunchLaunchTemplateSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "launch_template_id": "launchTemplateId",
            "launch_template_name": "launchTemplateName",
            "launch_template_version": "launchTemplateVersion",
        },
    )
    class FastLaunchLaunchTemplateSpecificationProperty:
        def __init__(
            self,
            *,
            launch_template_id: typing.Optional[builtins.str] = None,
            launch_template_name: typing.Optional[builtins.str] = None,
            launch_template_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Identifies the launch template that the associated Windows AMI uses for launching an instance when faster launching is enabled.

            .. epigraph::

               You can specify either the ``launchTemplateName`` or the ``launchTemplateId`` , but not both.

            :param launch_template_id: The ID of the launch template to use for faster launching for a Windows AMI.
            :param launch_template_name: The name of the launch template to use for faster launching for a Windows AMI.
            :param launch_template_version: The version of the launch template to use for faster launching for a Windows AMI.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-fastlaunchlaunchtemplatespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                fast_launch_launch_template_specification_property = imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.FastLaunchLaunchTemplateSpecificationProperty(
                    launch_template_id="launchTemplateId",
                    launch_template_name="launchTemplateName",
                    launch_template_version="launchTemplateVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1294d8fb286a1c21dac84af00709b9ca7f3f65e37912f4f25917b94b385799ae)
                check_type(argname="argument launch_template_id", value=launch_template_id, expected_type=type_hints["launch_template_id"])
                check_type(argname="argument launch_template_name", value=launch_template_name, expected_type=type_hints["launch_template_name"])
                check_type(argname="argument launch_template_version", value=launch_template_version, expected_type=type_hints["launch_template_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if launch_template_id is not None:
                self._values["launch_template_id"] = launch_template_id
            if launch_template_name is not None:
                self._values["launch_template_name"] = launch_template_name
            if launch_template_version is not None:
                self._values["launch_template_version"] = launch_template_version

        @builtins.property
        def launch_template_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the launch template to use for faster launching for a Windows AMI.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-fastlaunchlaunchtemplatespecification.html#cfn-imagebuilder-distributionconfiguration-fastlaunchlaunchtemplatespecification-launchtemplateid
            '''
            result = self._values.get("launch_template_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def launch_template_name(self) -> typing.Optional[builtins.str]:
            '''The name of the launch template to use for faster launching for a Windows AMI.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-fastlaunchlaunchtemplatespecification.html#cfn-imagebuilder-distributionconfiguration-fastlaunchlaunchtemplatespecification-launchtemplatename
            '''
            result = self._values.get("launch_template_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def launch_template_version(self) -> typing.Optional[builtins.str]:
            '''The version of the launch template to use for faster launching for a Windows AMI.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-fastlaunchlaunchtemplatespecification.html#cfn-imagebuilder-distributionconfiguration-fastlaunchlaunchtemplatespecification-launchtemplateversion
            '''
            result = self._values.get("launch_template_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FastLaunchLaunchTemplateSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnDistributionConfigurationPropsMixin.FastLaunchSnapshotConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"target_resource_count": "targetResourceCount"},
    )
    class FastLaunchSnapshotConfigurationProperty:
        def __init__(
            self,
            *,
            target_resource_count: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Configuration settings for creating and managing pre-provisioned snapshots for a fast-launch enabled Windows AMI.

            :param target_resource_count: The number of pre-provisioned snapshots to keep on hand for a fast-launch enabled Windows AMI.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-fastlaunchsnapshotconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                fast_launch_snapshot_configuration_property = imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.FastLaunchSnapshotConfigurationProperty(
                    target_resource_count=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9fa27c56308268a00e11b85db59fe0c73d50dd1538749392fbcb29ac71467e4b)
                check_type(argname="argument target_resource_count", value=target_resource_count, expected_type=type_hints["target_resource_count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_resource_count is not None:
                self._values["target_resource_count"] = target_resource_count

        @builtins.property
        def target_resource_count(self) -> typing.Optional[jsii.Number]:
            '''The number of pre-provisioned snapshots to keep on hand for a fast-launch enabled Windows AMI.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-fastlaunchsnapshotconfiguration.html#cfn-imagebuilder-distributionconfiguration-fastlaunchsnapshotconfiguration-targetresourcecount
            '''
            result = self._values.get("target_resource_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FastLaunchSnapshotConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnDistributionConfigurationPropsMixin.LaunchTemplateConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_id": "accountId",
            "launch_template_id": "launchTemplateId",
            "set_default_version": "setDefaultVersion",
        },
    )
    class LaunchTemplateConfigurationProperty:
        def __init__(
            self,
            *,
            account_id: typing.Optional[builtins.str] = None,
            launch_template_id: typing.Optional[builtins.str] = None,
            set_default_version: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Identifies an Amazon EC2 launch template to use for a specific account.

            :param account_id: The account ID that this configuration applies to.
            :param launch_template_id: Identifies the Amazon EC2 launch template to use.
            :param set_default_version: Set the specified Amazon EC2 launch template as the default launch template for the specified account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-launchtemplateconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                launch_template_configuration_property = imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.LaunchTemplateConfigurationProperty(
                    account_id="accountId",
                    launch_template_id="launchTemplateId",
                    set_default_version=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__689fdbedc3ad7fb3e0fa20c4acc83271d70a94eda4a2bd89be5a7f3087614654)
                check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                check_type(argname="argument launch_template_id", value=launch_template_id, expected_type=type_hints["launch_template_id"])
                check_type(argname="argument set_default_version", value=set_default_version, expected_type=type_hints["set_default_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_id is not None:
                self._values["account_id"] = account_id
            if launch_template_id is not None:
                self._values["launch_template_id"] = launch_template_id
            if set_default_version is not None:
                self._values["set_default_version"] = set_default_version

        @builtins.property
        def account_id(self) -> typing.Optional[builtins.str]:
            '''The account ID that this configuration applies to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-launchtemplateconfiguration.html#cfn-imagebuilder-distributionconfiguration-launchtemplateconfiguration-accountid
            '''
            result = self._values.get("account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def launch_template_id(self) -> typing.Optional[builtins.str]:
            '''Identifies the Amazon EC2 launch template to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-launchtemplateconfiguration.html#cfn-imagebuilder-distributionconfiguration-launchtemplateconfiguration-launchtemplateid
            '''
            result = self._values.get("launch_template_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def set_default_version(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set the specified Amazon EC2 launch template as the default launch template for the specified account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-launchtemplateconfiguration.html#cfn-imagebuilder-distributionconfiguration-launchtemplateconfiguration-setdefaultversion
            '''
            result = self._values.get("set_default_version")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LaunchTemplateConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnDistributionConfigurationPropsMixin.SsmParameterConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ami_account_id": "amiAccountId",
            "data_type": "dataType",
            "parameter_name": "parameterName",
        },
    )
    class SsmParameterConfigurationProperty:
        def __init__(
            self,
            *,
            ami_account_id: typing.Optional[builtins.str] = None,
            data_type: typing.Optional[builtins.str] = None,
            parameter_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration for a single Parameter in the AWS Systems Manager (SSM) Parameter Store in a given Region.

            :param ami_account_id: Specify the account that will own the Parameter in a given Region. During distribution, this account must be specified in distribution settings as a target account for the Region.
            :param data_type: The data type specifies what type of value the Parameter contains. We recommend that you use data type ``aws:ec2:image`` .
            :param parameter_name: This is the name of the Parameter in the target Region or account. The image distribution creates the Parameter if it doesn't already exist. Otherwise, it updates the parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-ssmparameterconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                ssm_parameter_configuration_property = imagebuilder_mixins.CfnDistributionConfigurationPropsMixin.SsmParameterConfigurationProperty(
                    ami_account_id="amiAccountId",
                    data_type="dataType",
                    parameter_name="parameterName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5f2ea63e846ef3726049680e85103917f844d0422a8088e3cb2a639dec6b384e)
                check_type(argname="argument ami_account_id", value=ami_account_id, expected_type=type_hints["ami_account_id"])
                check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
                check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ami_account_id is not None:
                self._values["ami_account_id"] = ami_account_id
            if data_type is not None:
                self._values["data_type"] = data_type
            if parameter_name is not None:
                self._values["parameter_name"] = parameter_name

        @builtins.property
        def ami_account_id(self) -> typing.Optional[builtins.str]:
            '''Specify the account that will own the Parameter in a given Region.

            During distribution, this account must be specified in distribution settings as a target account for the Region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-ssmparameterconfiguration.html#cfn-imagebuilder-distributionconfiguration-ssmparameterconfiguration-amiaccountid
            '''
            result = self._values.get("ami_account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_type(self) -> typing.Optional[builtins.str]:
            '''The data type specifies what type of value the Parameter contains.

            We recommend that you use data type ``aws:ec2:image`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-ssmparameterconfiguration.html#cfn-imagebuilder-distributionconfiguration-ssmparameterconfiguration-datatype
            '''
            result = self._values.get("data_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameter_name(self) -> typing.Optional[builtins.str]:
            '''This is the name of the Parameter in the target Region or account.

            The image distribution creates the Parameter if it doesn't already exist. Otherwise, it updates the parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-distributionconfiguration-ssmparameterconfiguration.html#cfn-imagebuilder-distributionconfiguration-ssmparameterconfiguration-parametername
            '''
            result = self._values.get("parameter_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SsmParameterConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImageMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "container_recipe_arn": "containerRecipeArn",
        "deletion_settings": "deletionSettings",
        "distribution_configuration_arn": "distributionConfigurationArn",
        "enhanced_image_metadata_enabled": "enhancedImageMetadataEnabled",
        "execution_role": "executionRole",
        "image_pipeline_execution_settings": "imagePipelineExecutionSettings",
        "image_recipe_arn": "imageRecipeArn",
        "image_scanning_configuration": "imageScanningConfiguration",
        "image_tests_configuration": "imageTestsConfiguration",
        "infrastructure_configuration_arn": "infrastructureConfigurationArn",
        "logging_configuration": "loggingConfiguration",
        "tags": "tags",
        "workflows": "workflows",
    },
)
class CfnImageMixinProps:
    def __init__(
        self,
        *,
        container_recipe_arn: typing.Optional[builtins.str] = None,
        deletion_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImagePropsMixin.DeletionSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        distribution_configuration_arn: typing.Optional[builtins.str] = None,
        enhanced_image_metadata_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        execution_role: typing.Optional[builtins.str] = None,
        image_pipeline_execution_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImagePropsMixin.ImagePipelineExecutionSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        image_recipe_arn: typing.Optional[builtins.str] = None,
        image_scanning_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImagePropsMixin.ImageScanningConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        image_tests_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImagePropsMixin.ImageTestsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        infrastructure_configuration_arn: typing.Optional[builtins.str] = None,
        logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImagePropsMixin.ImageLoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        workflows: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImagePropsMixin.WorkflowConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnImagePropsMixin.

        :param container_recipe_arn: The Amazon Resource Name (ARN) of the container recipe that defines how images are configured and tested.
        :param deletion_settings: The deletion settings of the image, indicating whether to delete the underlying resources in addition to the image.
        :param distribution_configuration_arn: The Amazon Resource Name (ARN) of the distribution configuration that defines and configures the outputs of your pipeline.
        :param enhanced_image_metadata_enabled: Collects additional information about the image being created, including the operating system (OS) version and package list. This information is used to enhance the overall experience of using EC2 Image Builder. Enabled by default.
        :param execution_role: The name or Amazon Resource Name (ARN) for the IAM role you create that grants Image Builder access to perform workflow actions.
        :param image_pipeline_execution_settings: The settings for starting an image pipeline execution.
        :param image_recipe_arn: The Amazon Resource Name (ARN) of the image recipe that defines how images are configured, tested, and assessed.
        :param image_scanning_configuration: Contains settings for vulnerability scans.
        :param image_tests_configuration: The image tests configuration of the image.
        :param infrastructure_configuration_arn: The Amazon Resource Name (ARN) of the infrastructure configuration that defines the environment in which your image will be built and tested.
        :param logging_configuration: The logging configuration that's defined for the image. Image Builder uses the defined settings to direct execution log output during image creation.
        :param tags: The tags of the image.
        :param workflows: Contains an array of workflow configuration objects.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
            
            cfn_image_mixin_props = imagebuilder_mixins.CfnImageMixinProps(
                container_recipe_arn="containerRecipeArn",
                deletion_settings=imagebuilder_mixins.CfnImagePropsMixin.DeletionSettingsProperty(
                    execution_role="executionRole"
                ),
                distribution_configuration_arn="distributionConfigurationArn",
                enhanced_image_metadata_enabled=False,
                execution_role="executionRole",
                image_pipeline_execution_settings=imagebuilder_mixins.CfnImagePropsMixin.ImagePipelineExecutionSettingsProperty(
                    deployment_id="deploymentId",
                    on_update=False
                ),
                image_recipe_arn="imageRecipeArn",
                image_scanning_configuration=imagebuilder_mixins.CfnImagePropsMixin.ImageScanningConfigurationProperty(
                    ecr_configuration=imagebuilder_mixins.CfnImagePropsMixin.EcrConfigurationProperty(
                        container_tags=["containerTags"],
                        repository_name="repositoryName"
                    ),
                    image_scanning_enabled=False
                ),
                image_tests_configuration=imagebuilder_mixins.CfnImagePropsMixin.ImageTestsConfigurationProperty(
                    image_tests_enabled=False,
                    timeout_minutes=123
                ),
                infrastructure_configuration_arn="infrastructureConfigurationArn",
                logging_configuration=imagebuilder_mixins.CfnImagePropsMixin.ImageLoggingConfigurationProperty(
                    log_group_name="logGroupName"
                ),
                tags={
                    "tags_key": "tags"
                },
                workflows=[imagebuilder_mixins.CfnImagePropsMixin.WorkflowConfigurationProperty(
                    on_failure="onFailure",
                    parallel_group="parallelGroup",
                    parameters=[imagebuilder_mixins.CfnImagePropsMixin.WorkflowParameterProperty(
                        name="name",
                        value=["value"]
                    )],
                    workflow_arn="workflowArn"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0c4dc3e6deea4f5e57c5497fea60eaabdf6133ae8f3793257be0207f9649ac7)
            check_type(argname="argument container_recipe_arn", value=container_recipe_arn, expected_type=type_hints["container_recipe_arn"])
            check_type(argname="argument deletion_settings", value=deletion_settings, expected_type=type_hints["deletion_settings"])
            check_type(argname="argument distribution_configuration_arn", value=distribution_configuration_arn, expected_type=type_hints["distribution_configuration_arn"])
            check_type(argname="argument enhanced_image_metadata_enabled", value=enhanced_image_metadata_enabled, expected_type=type_hints["enhanced_image_metadata_enabled"])
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument image_pipeline_execution_settings", value=image_pipeline_execution_settings, expected_type=type_hints["image_pipeline_execution_settings"])
            check_type(argname="argument image_recipe_arn", value=image_recipe_arn, expected_type=type_hints["image_recipe_arn"])
            check_type(argname="argument image_scanning_configuration", value=image_scanning_configuration, expected_type=type_hints["image_scanning_configuration"])
            check_type(argname="argument image_tests_configuration", value=image_tests_configuration, expected_type=type_hints["image_tests_configuration"])
            check_type(argname="argument infrastructure_configuration_arn", value=infrastructure_configuration_arn, expected_type=type_hints["infrastructure_configuration_arn"])
            check_type(argname="argument logging_configuration", value=logging_configuration, expected_type=type_hints["logging_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument workflows", value=workflows, expected_type=type_hints["workflows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container_recipe_arn is not None:
            self._values["container_recipe_arn"] = container_recipe_arn
        if deletion_settings is not None:
            self._values["deletion_settings"] = deletion_settings
        if distribution_configuration_arn is not None:
            self._values["distribution_configuration_arn"] = distribution_configuration_arn
        if enhanced_image_metadata_enabled is not None:
            self._values["enhanced_image_metadata_enabled"] = enhanced_image_metadata_enabled
        if execution_role is not None:
            self._values["execution_role"] = execution_role
        if image_pipeline_execution_settings is not None:
            self._values["image_pipeline_execution_settings"] = image_pipeline_execution_settings
        if image_recipe_arn is not None:
            self._values["image_recipe_arn"] = image_recipe_arn
        if image_scanning_configuration is not None:
            self._values["image_scanning_configuration"] = image_scanning_configuration
        if image_tests_configuration is not None:
            self._values["image_tests_configuration"] = image_tests_configuration
        if infrastructure_configuration_arn is not None:
            self._values["infrastructure_configuration_arn"] = infrastructure_configuration_arn
        if logging_configuration is not None:
            self._values["logging_configuration"] = logging_configuration
        if tags is not None:
            self._values["tags"] = tags
        if workflows is not None:
            self._values["workflows"] = workflows

    @builtins.property
    def container_recipe_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the container recipe that defines how images are configured and tested.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html#cfn-imagebuilder-image-containerrecipearn
        '''
        result = self._values.get("container_recipe_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deletion_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePropsMixin.DeletionSettingsProperty"]]:
        '''The deletion settings of the image, indicating whether to delete the underlying resources in addition to the image.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html#cfn-imagebuilder-image-deletionsettings
        '''
        result = self._values.get("deletion_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePropsMixin.DeletionSettingsProperty"]], result)

    @builtins.property
    def distribution_configuration_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the distribution configuration that defines and configures the outputs of your pipeline.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html#cfn-imagebuilder-image-distributionconfigurationarn
        '''
        result = self._values.get("distribution_configuration_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enhanced_image_metadata_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Collects additional information about the image being created, including the operating system (OS) version and package list.

        This information is used to enhance the overall experience of using EC2 Image Builder. Enabled by default.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html#cfn-imagebuilder-image-enhancedimagemetadataenabled
        '''
        result = self._values.get("enhanced_image_metadata_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def execution_role(self) -> typing.Optional[builtins.str]:
        '''The name or Amazon Resource Name (ARN) for the IAM role you create that grants Image Builder access to perform workflow actions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html#cfn-imagebuilder-image-executionrole
        '''
        result = self._values.get("execution_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_pipeline_execution_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePropsMixin.ImagePipelineExecutionSettingsProperty"]]:
        '''The settings for starting an image pipeline execution.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html#cfn-imagebuilder-image-imagepipelineexecutionsettings
        '''
        result = self._values.get("image_pipeline_execution_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePropsMixin.ImagePipelineExecutionSettingsProperty"]], result)

    @builtins.property
    def image_recipe_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the image recipe that defines how images are configured, tested, and assessed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html#cfn-imagebuilder-image-imagerecipearn
        '''
        result = self._values.get("image_recipe_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_scanning_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePropsMixin.ImageScanningConfigurationProperty"]]:
        '''Contains settings for vulnerability scans.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html#cfn-imagebuilder-image-imagescanningconfiguration
        '''
        result = self._values.get("image_scanning_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePropsMixin.ImageScanningConfigurationProperty"]], result)

    @builtins.property
    def image_tests_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePropsMixin.ImageTestsConfigurationProperty"]]:
        '''The image tests configuration of the image.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html#cfn-imagebuilder-image-imagetestsconfiguration
        '''
        result = self._values.get("image_tests_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePropsMixin.ImageTestsConfigurationProperty"]], result)

    @builtins.property
    def infrastructure_configuration_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the infrastructure configuration that defines the environment in which your image will be built and tested.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html#cfn-imagebuilder-image-infrastructureconfigurationarn
        '''
        result = self._values.get("infrastructure_configuration_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePropsMixin.ImageLoggingConfigurationProperty"]]:
        '''The logging configuration that's defined for the image.

        Image Builder uses the defined settings to direct execution log output during image creation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html#cfn-imagebuilder-image-loggingconfiguration
        '''
        result = self._values.get("logging_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePropsMixin.ImageLoggingConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags of the image.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html#cfn-imagebuilder-image-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def workflows(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePropsMixin.WorkflowConfigurationProperty"]]]]:
        '''Contains an array of workflow configuration objects.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html#cfn-imagebuilder-image-workflows
        '''
        result = self._values.get("workflows")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePropsMixin.WorkflowConfigurationProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnImageMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImagePipelineMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "container_recipe_arn": "containerRecipeArn",
        "description": "description",
        "distribution_configuration_arn": "distributionConfigurationArn",
        "enhanced_image_metadata_enabled": "enhancedImageMetadataEnabled",
        "execution_role": "executionRole",
        "image_recipe_arn": "imageRecipeArn",
        "image_scanning_configuration": "imageScanningConfiguration",
        "image_tests_configuration": "imageTestsConfiguration",
        "infrastructure_configuration_arn": "infrastructureConfigurationArn",
        "logging_configuration": "loggingConfiguration",
        "name": "name",
        "schedule": "schedule",
        "status": "status",
        "tags": "tags",
        "workflows": "workflows",
    },
)
class CfnImagePipelineMixinProps:
    def __init__(
        self,
        *,
        container_recipe_arn: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        distribution_configuration_arn: typing.Optional[builtins.str] = None,
        enhanced_image_metadata_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        execution_role: typing.Optional[builtins.str] = None,
        image_recipe_arn: typing.Optional[builtins.str] = None,
        image_scanning_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImagePipelinePropsMixin.ImageScanningConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        image_tests_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImagePipelinePropsMixin.ImageTestsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        infrastructure_configuration_arn: typing.Optional[builtins.str] = None,
        logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImagePipelinePropsMixin.PipelineLoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImagePipelinePropsMixin.ScheduleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        workflows: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImagePipelinePropsMixin.WorkflowConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnImagePipelinePropsMixin.

        :param container_recipe_arn: The Amazon Resource Name (ARN) of the container recipe that is used for this pipeline.
        :param description: The description of this image pipeline.
        :param distribution_configuration_arn: The Amazon Resource Name (ARN) of the distribution configuration associated with this image pipeline.
        :param enhanced_image_metadata_enabled: Collects additional information about the image being created, including the operating system (OS) version and package list. This information is used to enhance the overall experience of using EC2 Image Builder. Enabled by default.
        :param execution_role: The name or Amazon Resource Name (ARN) for the IAM role you create that grants Image Builder access to perform workflow actions.
        :param image_recipe_arn: The Amazon Resource Name (ARN) of the image recipe associated with this image pipeline.
        :param image_scanning_configuration: Contains settings for vulnerability scans.
        :param image_tests_configuration: The configuration of the image tests that run after image creation to ensure the quality of the image that was created.
        :param infrastructure_configuration_arn: The Amazon Resource Name (ARN) of the infrastructure configuration associated with this image pipeline.
        :param logging_configuration: Defines logging configuration for the output image.
        :param name: The name of the image pipeline.
        :param schedule: The schedule of the image pipeline. A schedule configures how often and when a pipeline automatically creates a new image.
        :param status: The status of the image pipeline.
        :param tags: The tags of this image pipeline.
        :param workflows: Contains the workflows that run for the image pipeline.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
            
            cfn_image_pipeline_mixin_props = imagebuilder_mixins.CfnImagePipelineMixinProps(
                container_recipe_arn="containerRecipeArn",
                description="description",
                distribution_configuration_arn="distributionConfigurationArn",
                enhanced_image_metadata_enabled=False,
                execution_role="executionRole",
                image_recipe_arn="imageRecipeArn",
                image_scanning_configuration=imagebuilder_mixins.CfnImagePipelinePropsMixin.ImageScanningConfigurationProperty(
                    ecr_configuration=imagebuilder_mixins.CfnImagePipelinePropsMixin.EcrConfigurationProperty(
                        container_tags=["containerTags"],
                        repository_name="repositoryName"
                    ),
                    image_scanning_enabled=False
                ),
                image_tests_configuration=imagebuilder_mixins.CfnImagePipelinePropsMixin.ImageTestsConfigurationProperty(
                    image_tests_enabled=False,
                    timeout_minutes=123
                ),
                infrastructure_configuration_arn="infrastructureConfigurationArn",
                logging_configuration=imagebuilder_mixins.CfnImagePipelinePropsMixin.PipelineLoggingConfigurationProperty(
                    image_log_group_name="imageLogGroupName",
                    pipeline_log_group_name="pipelineLogGroupName"
                ),
                name="name",
                schedule=imagebuilder_mixins.CfnImagePipelinePropsMixin.ScheduleProperty(
                    auto_disable_policy=imagebuilder_mixins.CfnImagePipelinePropsMixin.AutoDisablePolicyProperty(
                        failure_count=123
                    ),
                    pipeline_execution_start_condition="pipelineExecutionStartCondition",
                    schedule_expression="scheduleExpression"
                ),
                status="status",
                tags={
                    "tags_key": "tags"
                },
                workflows=[imagebuilder_mixins.CfnImagePipelinePropsMixin.WorkflowConfigurationProperty(
                    on_failure="onFailure",
                    parallel_group="parallelGroup",
                    parameters=[imagebuilder_mixins.CfnImagePipelinePropsMixin.WorkflowParameterProperty(
                        name="name",
                        value=["value"]
                    )],
                    workflow_arn="workflowArn"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71fea23c7a9600260786b2594ea3c73328b1471e6508013b7723ebcae900389d)
            check_type(argname="argument container_recipe_arn", value=container_recipe_arn, expected_type=type_hints["container_recipe_arn"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument distribution_configuration_arn", value=distribution_configuration_arn, expected_type=type_hints["distribution_configuration_arn"])
            check_type(argname="argument enhanced_image_metadata_enabled", value=enhanced_image_metadata_enabled, expected_type=type_hints["enhanced_image_metadata_enabled"])
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument image_recipe_arn", value=image_recipe_arn, expected_type=type_hints["image_recipe_arn"])
            check_type(argname="argument image_scanning_configuration", value=image_scanning_configuration, expected_type=type_hints["image_scanning_configuration"])
            check_type(argname="argument image_tests_configuration", value=image_tests_configuration, expected_type=type_hints["image_tests_configuration"])
            check_type(argname="argument infrastructure_configuration_arn", value=infrastructure_configuration_arn, expected_type=type_hints["infrastructure_configuration_arn"])
            check_type(argname="argument logging_configuration", value=logging_configuration, expected_type=type_hints["logging_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument workflows", value=workflows, expected_type=type_hints["workflows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container_recipe_arn is not None:
            self._values["container_recipe_arn"] = container_recipe_arn
        if description is not None:
            self._values["description"] = description
        if distribution_configuration_arn is not None:
            self._values["distribution_configuration_arn"] = distribution_configuration_arn
        if enhanced_image_metadata_enabled is not None:
            self._values["enhanced_image_metadata_enabled"] = enhanced_image_metadata_enabled
        if execution_role is not None:
            self._values["execution_role"] = execution_role
        if image_recipe_arn is not None:
            self._values["image_recipe_arn"] = image_recipe_arn
        if image_scanning_configuration is not None:
            self._values["image_scanning_configuration"] = image_scanning_configuration
        if image_tests_configuration is not None:
            self._values["image_tests_configuration"] = image_tests_configuration
        if infrastructure_configuration_arn is not None:
            self._values["infrastructure_configuration_arn"] = infrastructure_configuration_arn
        if logging_configuration is not None:
            self._values["logging_configuration"] = logging_configuration
        if name is not None:
            self._values["name"] = name
        if schedule is not None:
            self._values["schedule"] = schedule
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags
        if workflows is not None:
            self._values["workflows"] = workflows

    @builtins.property
    def container_recipe_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the container recipe that is used for this pipeline.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-containerrecipearn
        '''
        result = self._values.get("container_recipe_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of this image pipeline.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def distribution_configuration_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the distribution configuration associated with this image pipeline.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-distributionconfigurationarn
        '''
        result = self._values.get("distribution_configuration_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enhanced_image_metadata_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Collects additional information about the image being created, including the operating system (OS) version and package list.

        This information is used to enhance the overall experience of using EC2 Image Builder. Enabled by default.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-enhancedimagemetadataenabled
        '''
        result = self._values.get("enhanced_image_metadata_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def execution_role(self) -> typing.Optional[builtins.str]:
        '''The name or Amazon Resource Name (ARN) for the IAM role you create that grants Image Builder access to perform workflow actions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-executionrole
        '''
        result = self._values.get("execution_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_recipe_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the image recipe associated with this image pipeline.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-imagerecipearn
        '''
        result = self._values.get("image_recipe_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_scanning_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePipelinePropsMixin.ImageScanningConfigurationProperty"]]:
        '''Contains settings for vulnerability scans.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-imagescanningconfiguration
        '''
        result = self._values.get("image_scanning_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePipelinePropsMixin.ImageScanningConfigurationProperty"]], result)

    @builtins.property
    def image_tests_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePipelinePropsMixin.ImageTestsConfigurationProperty"]]:
        '''The configuration of the image tests that run after image creation to ensure the quality of the image that was created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-imagetestsconfiguration
        '''
        result = self._values.get("image_tests_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePipelinePropsMixin.ImageTestsConfigurationProperty"]], result)

    @builtins.property
    def infrastructure_configuration_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the infrastructure configuration associated with this image pipeline.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-infrastructureconfigurationarn
        '''
        result = self._values.get("infrastructure_configuration_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePipelinePropsMixin.PipelineLoggingConfigurationProperty"]]:
        '''Defines logging configuration for the output image.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-loggingconfiguration
        '''
        result = self._values.get("logging_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePipelinePropsMixin.PipelineLoggingConfigurationProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the image pipeline.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePipelinePropsMixin.ScheduleProperty"]]:
        '''The schedule of the image pipeline.

        A schedule configures how often and when a pipeline automatically creates a new image.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-schedule
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePipelinePropsMixin.ScheduleProperty"]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of the image pipeline.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags of this image pipeline.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def workflows(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePipelinePropsMixin.WorkflowConfigurationProperty"]]]]:
        '''Contains the workflows that run for the image pipeline.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html#cfn-imagebuilder-imagepipeline-workflows
        '''
        result = self._values.get("workflows")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePipelinePropsMixin.WorkflowConfigurationProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnImagePipelineMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnImagePipelinePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImagePipelinePropsMixin",
):
    '''An image pipeline is the automation configuration for building secure OS images on AWS .

    The Image Builder image pipeline is associated with an image recipe that defines the build, validation, and test phases for an image build lifecycle. An image pipeline can be associated with an infrastructure configuration that defines where your image is built. You can define attributes, such as instance types, a subnet for your VPC, security groups, logging, and other infrastructure-related configurations. You can also associate your image pipeline with a distribution configuration to define how you would like to deploy your image.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagepipeline.html
    :cloudformationResource: AWS::ImageBuilder::ImagePipeline
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
        
        cfn_image_pipeline_props_mixin = imagebuilder_mixins.CfnImagePipelinePropsMixin(imagebuilder_mixins.CfnImagePipelineMixinProps(
            container_recipe_arn="containerRecipeArn",
            description="description",
            distribution_configuration_arn="distributionConfigurationArn",
            enhanced_image_metadata_enabled=False,
            execution_role="executionRole",
            image_recipe_arn="imageRecipeArn",
            image_scanning_configuration=imagebuilder_mixins.CfnImagePipelinePropsMixin.ImageScanningConfigurationProperty(
                ecr_configuration=imagebuilder_mixins.CfnImagePipelinePropsMixin.EcrConfigurationProperty(
                    container_tags=["containerTags"],
                    repository_name="repositoryName"
                ),
                image_scanning_enabled=False
            ),
            image_tests_configuration=imagebuilder_mixins.CfnImagePipelinePropsMixin.ImageTestsConfigurationProperty(
                image_tests_enabled=False,
                timeout_minutes=123
            ),
            infrastructure_configuration_arn="infrastructureConfigurationArn",
            logging_configuration=imagebuilder_mixins.CfnImagePipelinePropsMixin.PipelineLoggingConfigurationProperty(
                image_log_group_name="imageLogGroupName",
                pipeline_log_group_name="pipelineLogGroupName"
            ),
            name="name",
            schedule=imagebuilder_mixins.CfnImagePipelinePropsMixin.ScheduleProperty(
                auto_disable_policy=imagebuilder_mixins.CfnImagePipelinePropsMixin.AutoDisablePolicyProperty(
                    failure_count=123
                ),
                pipeline_execution_start_condition="pipelineExecutionStartCondition",
                schedule_expression="scheduleExpression"
            ),
            status="status",
            tags={
                "tags_key": "tags"
            },
            workflows=[imagebuilder_mixins.CfnImagePipelinePropsMixin.WorkflowConfigurationProperty(
                on_failure="onFailure",
                parallel_group="parallelGroup",
                parameters=[imagebuilder_mixins.CfnImagePipelinePropsMixin.WorkflowParameterProperty(
                    name="name",
                    value=["value"]
                )],
                workflow_arn="workflowArn"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnImagePipelineMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ImageBuilder::ImagePipeline``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__088b1151cdd817229b45c6ce883ec8496c99da45c77cd4f403b0a0b4bb78cd61)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97497d8c097f532b75195c9d99edfcdb00c0302b9d024c1cbbdf3e657d26fa0b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5c10a1989638f9b6f88b2bc85167ca724bb71b66aa9fb44778d654de5855f51)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnImagePipelineMixinProps:
        return typing.cast(CfnImagePipelineMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImagePipelinePropsMixin.AutoDisablePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"failure_count": "failureCount"},
    )
    class AutoDisablePolicyProperty:
        def __init__(
            self,
            *,
            failure_count: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Defines the rules by which an image pipeline is automatically disabled when it fails.

            :param failure_count: The number of consecutive scheduled image pipeline executions that must fail before Image Builder automatically disables the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-autodisablepolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                auto_disable_policy_property = imagebuilder_mixins.CfnImagePipelinePropsMixin.AutoDisablePolicyProperty(
                    failure_count=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b6e63d5158a4c5c169c79c6b4e2a49bd3d4328dd626301a0af7d4acadd1c2eb1)
                check_type(argname="argument failure_count", value=failure_count, expected_type=type_hints["failure_count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if failure_count is not None:
                self._values["failure_count"] = failure_count

        @builtins.property
        def failure_count(self) -> typing.Optional[jsii.Number]:
            '''The number of consecutive scheduled image pipeline executions that must fail before Image Builder automatically disables the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-autodisablepolicy.html#cfn-imagebuilder-imagepipeline-autodisablepolicy-failurecount
            '''
            result = self._values.get("failure_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoDisablePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImagePipelinePropsMixin.EcrConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "container_tags": "containerTags",
            "repository_name": "repositoryName",
        },
    )
    class EcrConfigurationProperty:
        def __init__(
            self,
            *,
            container_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
            repository_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings that Image Builder uses to configure the ECR repository and the output container images that Amazon Inspector scans.

            :param container_tags: Tags for Image Builder to apply to the output container image that Amazon Inspector scans. Tags can help you identify and manage your scanned images.
            :param repository_name: The name of the container repository that Amazon Inspector scans to identify findings for your container images. The name includes the path for the repository location. If you don’t provide this information, Image Builder creates a repository in your account named ``image-builder-image-scanning-repository`` for vulnerability scans of your output container images.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-ecrconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                ecr_configuration_property = imagebuilder_mixins.CfnImagePipelinePropsMixin.EcrConfigurationProperty(
                    container_tags=["containerTags"],
                    repository_name="repositoryName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f4ffbd60e601ffdd6bf391308e4aeb9babd1ab26c698e5385cf1ff8badff244c)
                check_type(argname="argument container_tags", value=container_tags, expected_type=type_hints["container_tags"])
                check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if container_tags is not None:
                self._values["container_tags"] = container_tags
            if repository_name is not None:
                self._values["repository_name"] = repository_name

        @builtins.property
        def container_tags(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Tags for Image Builder to apply to the output container image that Amazon Inspector scans.

            Tags can help you identify and manage your scanned images.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-ecrconfiguration.html#cfn-imagebuilder-imagepipeline-ecrconfiguration-containertags
            '''
            result = self._values.get("container_tags")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def repository_name(self) -> typing.Optional[builtins.str]:
            '''The name of the container repository that Amazon Inspector scans to identify findings for your container images.

            The name includes the path for the repository location. If you don’t provide this information, Image Builder creates a repository in your account named ``image-builder-image-scanning-repository`` for vulnerability scans of your output container images.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-ecrconfiguration.html#cfn-imagebuilder-imagepipeline-ecrconfiguration-repositoryname
            '''
            result = self._values.get("repository_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EcrConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImagePipelinePropsMixin.ImageScanningConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ecr_configuration": "ecrConfiguration",
            "image_scanning_enabled": "imageScanningEnabled",
        },
    )
    class ImageScanningConfigurationProperty:
        def __init__(
            self,
            *,
            ecr_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImagePipelinePropsMixin.EcrConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            image_scanning_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Contains settings for Image Builder image resource and container image scans.

            :param ecr_configuration: Contains Amazon ECR settings for vulnerability scans.
            :param image_scanning_enabled: A setting that indicates whether Image Builder keeps a snapshot of the vulnerability scans that Amazon Inspector runs against the build instance when you create a new image.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-imagescanningconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                image_scanning_configuration_property = imagebuilder_mixins.CfnImagePipelinePropsMixin.ImageScanningConfigurationProperty(
                    ecr_configuration=imagebuilder_mixins.CfnImagePipelinePropsMixin.EcrConfigurationProperty(
                        container_tags=["containerTags"],
                        repository_name="repositoryName"
                    ),
                    image_scanning_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1de29f4f60c4e5df61d1306f6cabb4daeb0e5a7c2084ea47552c03dfcd74f8b8)
                check_type(argname="argument ecr_configuration", value=ecr_configuration, expected_type=type_hints["ecr_configuration"])
                check_type(argname="argument image_scanning_enabled", value=image_scanning_enabled, expected_type=type_hints["image_scanning_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ecr_configuration is not None:
                self._values["ecr_configuration"] = ecr_configuration
            if image_scanning_enabled is not None:
                self._values["image_scanning_enabled"] = image_scanning_enabled

        @builtins.property
        def ecr_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePipelinePropsMixin.EcrConfigurationProperty"]]:
            '''Contains Amazon ECR settings for vulnerability scans.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-imagescanningconfiguration.html#cfn-imagebuilder-imagepipeline-imagescanningconfiguration-ecrconfiguration
            '''
            result = self._values.get("ecr_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePipelinePropsMixin.EcrConfigurationProperty"]], result)

        @builtins.property
        def image_scanning_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A setting that indicates whether Image Builder keeps a snapshot of the vulnerability scans that Amazon Inspector runs against the build instance when you create a new image.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-imagescanningconfiguration.html#cfn-imagebuilder-imagepipeline-imagescanningconfiguration-imagescanningenabled
            '''
            result = self._values.get("image_scanning_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImageScanningConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImagePipelinePropsMixin.ImageTestsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "image_tests_enabled": "imageTestsEnabled",
            "timeout_minutes": "timeoutMinutes",
        },
    )
    class ImageTestsConfigurationProperty:
        def __init__(
            self,
            *,
            image_tests_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            timeout_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''When you create an image or container recipe with Image Builder , you can add the build or test components that your image pipeline uses to create the final image.

            You must have at least one build component to create a recipe, but test components are not required. Your pipeline runs tests after it builds the image, to ensure that the target image is functional and can be used reliably for launching Amazon EC2 instances.

            :param image_tests_enabled: Defines if tests should be executed when building this image. For example, ``true`` or ``false`` .
            :param timeout_minutes: The maximum time in minutes that tests are permitted to run. .. epigraph:: The timeout property is not currently active. This value is ignored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-imagetestsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                image_tests_configuration_property = imagebuilder_mixins.CfnImagePipelinePropsMixin.ImageTestsConfigurationProperty(
                    image_tests_enabled=False,
                    timeout_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a549f62e8294116c837891dca0b8e1b7e96c758b8d559b44ab71fd32f4ee4fb9)
                check_type(argname="argument image_tests_enabled", value=image_tests_enabled, expected_type=type_hints["image_tests_enabled"])
                check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if image_tests_enabled is not None:
                self._values["image_tests_enabled"] = image_tests_enabled
            if timeout_minutes is not None:
                self._values["timeout_minutes"] = timeout_minutes

        @builtins.property
        def image_tests_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Defines if tests should be executed when building this image.

            For example, ``true`` or ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-imagetestsconfiguration.html#cfn-imagebuilder-imagepipeline-imagetestsconfiguration-imagetestsenabled
            '''
            result = self._values.get("image_tests_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def timeout_minutes(self) -> typing.Optional[jsii.Number]:
            '''The maximum time in minutes that tests are permitted to run.

            .. epigraph::

               The timeout property is not currently active. This value is ignored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-imagetestsconfiguration.html#cfn-imagebuilder-imagepipeline-imagetestsconfiguration-timeoutminutes
            '''
            result = self._values.get("timeout_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImageTestsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImagePipelinePropsMixin.PipelineLoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "image_log_group_name": "imageLogGroupName",
            "pipeline_log_group_name": "pipelineLogGroupName",
        },
    )
    class PipelineLoggingConfigurationProperty:
        def __init__(
            self,
            *,
            image_log_group_name: typing.Optional[builtins.str] = None,
            pipeline_log_group_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The logging configuration that's defined for pipeline execution.

            :param image_log_group_name: The log group name that Image Builder uses for image creation. If not specified, the log group name defaults to ``/aws/imagebuilder/image-name`` .
            :param pipeline_log_group_name: The log group name that Image Builder uses for the log output during creation of a new pipeline. If not specified, the pipeline log group name defaults to ``/aws/imagebuilder/pipeline/pipeline-name`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-pipelineloggingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                pipeline_logging_configuration_property = imagebuilder_mixins.CfnImagePipelinePropsMixin.PipelineLoggingConfigurationProperty(
                    image_log_group_name="imageLogGroupName",
                    pipeline_log_group_name="pipelineLogGroupName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3ad6a071c1a7b53111dbfc9d97e8e79a41ad6d0da1e47ad39514c2766f676726)
                check_type(argname="argument image_log_group_name", value=image_log_group_name, expected_type=type_hints["image_log_group_name"])
                check_type(argname="argument pipeline_log_group_name", value=pipeline_log_group_name, expected_type=type_hints["pipeline_log_group_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if image_log_group_name is not None:
                self._values["image_log_group_name"] = image_log_group_name
            if pipeline_log_group_name is not None:
                self._values["pipeline_log_group_name"] = pipeline_log_group_name

        @builtins.property
        def image_log_group_name(self) -> typing.Optional[builtins.str]:
            '''The log group name that Image Builder uses for image creation.

            If not specified, the log group name defaults to ``/aws/imagebuilder/image-name`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-pipelineloggingconfiguration.html#cfn-imagebuilder-imagepipeline-pipelineloggingconfiguration-imageloggroupname
            '''
            result = self._values.get("image_log_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pipeline_log_group_name(self) -> typing.Optional[builtins.str]:
            '''The log group name that Image Builder uses for the log output during creation of a new pipeline.

            If not specified, the pipeline log group name defaults to ``/aws/imagebuilder/pipeline/pipeline-name`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-pipelineloggingconfiguration.html#cfn-imagebuilder-imagepipeline-pipelineloggingconfiguration-pipelineloggroupname
            '''
            result = self._values.get("pipeline_log_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipelineLoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImagePipelinePropsMixin.ScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_disable_policy": "autoDisablePolicy",
            "pipeline_execution_start_condition": "pipelineExecutionStartCondition",
            "schedule_expression": "scheduleExpression",
        },
    )
    class ScheduleProperty:
        def __init__(
            self,
            *,
            auto_disable_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImagePipelinePropsMixin.AutoDisablePolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            pipeline_execution_start_condition: typing.Optional[builtins.str] = None,
            schedule_expression: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A schedule configures when and how often a pipeline will automatically create a new image.

            :param auto_disable_policy: The policy that configures when Image Builder should automatically disable a pipeline that is failing.
            :param pipeline_execution_start_condition: The condition configures when the pipeline should trigger a new image build. When the ``pipelineExecutionStartCondition`` is set to ``EXPRESSION_MATCH_AND_DEPENDENCY_UPDATES_AVAILABLE`` , and you use semantic version filters on the base image or components in your image recipe, Image Builder will build a new image only when there are new versions of the image or components in your recipe that match the semantic version filter. When it is set to ``EXPRESSION_MATCH_ONLY`` , it will build a new image every time the CRON expression matches the current time. For semantic version syntax, see `CreateComponent <https://docs.aws.amazon.com/imagebuilder/latest/APIReference/API_CreateComponent.html>`_ in the *Image Builder API Reference* .
            :param schedule_expression: The cron expression determines how often EC2 Image Builder evaluates your ``pipelineExecutionStartCondition`` . For information on how to format a cron expression in Image Builder, see `Use cron expressions in EC2 Image Builder <https://docs.aws.amazon.com/imagebuilder/latest/userguide/image-builder-cron.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-schedule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                schedule_property = imagebuilder_mixins.CfnImagePipelinePropsMixin.ScheduleProperty(
                    auto_disable_policy=imagebuilder_mixins.CfnImagePipelinePropsMixin.AutoDisablePolicyProperty(
                        failure_count=123
                    ),
                    pipeline_execution_start_condition="pipelineExecutionStartCondition",
                    schedule_expression="scheduleExpression"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__737e7c96e267e0ae414be9646fc10a4a8ec15ae75dfac2b1d8bc71866cfd631f)
                check_type(argname="argument auto_disable_policy", value=auto_disable_policy, expected_type=type_hints["auto_disable_policy"])
                check_type(argname="argument pipeline_execution_start_condition", value=pipeline_execution_start_condition, expected_type=type_hints["pipeline_execution_start_condition"])
                check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_disable_policy is not None:
                self._values["auto_disable_policy"] = auto_disable_policy
            if pipeline_execution_start_condition is not None:
                self._values["pipeline_execution_start_condition"] = pipeline_execution_start_condition
            if schedule_expression is not None:
                self._values["schedule_expression"] = schedule_expression

        @builtins.property
        def auto_disable_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePipelinePropsMixin.AutoDisablePolicyProperty"]]:
            '''The policy that configures when Image Builder should automatically disable a pipeline that is failing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-schedule.html#cfn-imagebuilder-imagepipeline-schedule-autodisablepolicy
            '''
            result = self._values.get("auto_disable_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePipelinePropsMixin.AutoDisablePolicyProperty"]], result)

        @builtins.property
        def pipeline_execution_start_condition(self) -> typing.Optional[builtins.str]:
            '''The condition configures when the pipeline should trigger a new image build.

            When the ``pipelineExecutionStartCondition`` is set to ``EXPRESSION_MATCH_AND_DEPENDENCY_UPDATES_AVAILABLE`` , and you use semantic version filters on the base image or components in your image recipe, Image Builder will build a new image only when there are new versions of the image or components in your recipe that match the semantic version filter. When it is set to ``EXPRESSION_MATCH_ONLY`` , it will build a new image every time the CRON expression matches the current time. For semantic version syntax, see `CreateComponent <https://docs.aws.amazon.com/imagebuilder/latest/APIReference/API_CreateComponent.html>`_ in the *Image Builder API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-schedule.html#cfn-imagebuilder-imagepipeline-schedule-pipelineexecutionstartcondition
            '''
            result = self._values.get("pipeline_execution_start_condition")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schedule_expression(self) -> typing.Optional[builtins.str]:
            '''The cron expression determines how often EC2 Image Builder evaluates your ``pipelineExecutionStartCondition`` .

            For information on how to format a cron expression in Image Builder, see `Use cron expressions in EC2 Image Builder <https://docs.aws.amazon.com/imagebuilder/latest/userguide/image-builder-cron.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-schedule.html#cfn-imagebuilder-imagepipeline-schedule-scheduleexpression
            '''
            result = self._values.get("schedule_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImagePipelinePropsMixin.WorkflowConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "on_failure": "onFailure",
            "parallel_group": "parallelGroup",
            "parameters": "parameters",
            "workflow_arn": "workflowArn",
        },
    )
    class WorkflowConfigurationProperty:
        def __init__(
            self,
            *,
            on_failure: typing.Optional[builtins.str] = None,
            parallel_group: typing.Optional[builtins.str] = None,
            parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImagePipelinePropsMixin.WorkflowParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            workflow_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains control settings and configurable inputs for a workflow resource.

            :param on_failure: The action to take if the workflow fails.
            :param parallel_group: Test workflows are defined within named runtime groups called parallel groups. The parallel group is the named group that contains this test workflow. Test workflows within a parallel group can run at the same time. Image Builder starts up to five test workflows in the group at the same time, and starts additional workflows as others complete, until all workflows in the group have completed. This field only applies for test workflows.
            :param parameters: Contains parameter values for each of the parameters that the workflow document defined for the workflow resource.
            :param workflow_arn: The Amazon Resource Name (ARN) of the workflow resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-workflowconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                workflow_configuration_property = imagebuilder_mixins.CfnImagePipelinePropsMixin.WorkflowConfigurationProperty(
                    on_failure="onFailure",
                    parallel_group="parallelGroup",
                    parameters=[imagebuilder_mixins.CfnImagePipelinePropsMixin.WorkflowParameterProperty(
                        name="name",
                        value=["value"]
                    )],
                    workflow_arn="workflowArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__43b55874d0c4c966a148f44d76664fbd2658b7027aeaf661c4194cfd19b312c0)
                check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
                check_type(argname="argument parallel_group", value=parallel_group, expected_type=type_hints["parallel_group"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument workflow_arn", value=workflow_arn, expected_type=type_hints["workflow_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if on_failure is not None:
                self._values["on_failure"] = on_failure
            if parallel_group is not None:
                self._values["parallel_group"] = parallel_group
            if parameters is not None:
                self._values["parameters"] = parameters
            if workflow_arn is not None:
                self._values["workflow_arn"] = workflow_arn

        @builtins.property
        def on_failure(self) -> typing.Optional[builtins.str]:
            '''The action to take if the workflow fails.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-workflowconfiguration.html#cfn-imagebuilder-imagepipeline-workflowconfiguration-onfailure
            '''
            result = self._values.get("on_failure")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parallel_group(self) -> typing.Optional[builtins.str]:
            '''Test workflows are defined within named runtime groups called parallel groups.

            The parallel group is the named group that contains this test workflow. Test workflows within a parallel group can run at the same time. Image Builder starts up to five test workflows in the group at the same time, and starts additional workflows as others complete, until all workflows in the group have completed. This field only applies for test workflows.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-workflowconfiguration.html#cfn-imagebuilder-imagepipeline-workflowconfiguration-parallelgroup
            '''
            result = self._values.get("parallel_group")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePipelinePropsMixin.WorkflowParameterProperty"]]]]:
            '''Contains parameter values for each of the parameters that the workflow document defined for the workflow resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-workflowconfiguration.html#cfn-imagebuilder-imagepipeline-workflowconfiguration-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePipelinePropsMixin.WorkflowParameterProperty"]]]], result)

        @builtins.property
        def workflow_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the workflow resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-workflowconfiguration.html#cfn-imagebuilder-imagepipeline-workflowconfiguration-workflowarn
            '''
            result = self._values.get("workflow_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkflowConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImagePipelinePropsMixin.WorkflowParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class WorkflowParameterProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Contains a key/value pair that sets the named workflow parameter.

            :param name: The name of the workflow parameter to set.
            :param value: Sets the value for the named workflow parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-workflowparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                workflow_parameter_property = imagebuilder_mixins.CfnImagePipelinePropsMixin.WorkflowParameterProperty(
                    name="name",
                    value=["value"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e0917cb8fff1393da8eca6d7429090fea91faff83082def182c5512d1a846990)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the workflow parameter to set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-workflowparameter.html#cfn-imagebuilder-imagepipeline-workflowparameter-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Sets the value for the named workflow parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagepipeline-workflowparameter.html#cfn-imagebuilder-imagepipeline-workflowparameter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkflowParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IMixin_11e4b965)
class CfnImagePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImagePropsMixin",
):
    '''Creates a new image.

    This request will create a new image along with all of the configured output resources defined in the distribution configuration. You must specify exactly one recipe for your image, using either a ContainerRecipeArn or an ImageRecipeArn.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-image.html
    :cloudformationResource: AWS::ImageBuilder::Image
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
        
        cfn_image_props_mixin = imagebuilder_mixins.CfnImagePropsMixin(imagebuilder_mixins.CfnImageMixinProps(
            container_recipe_arn="containerRecipeArn",
            deletion_settings=imagebuilder_mixins.CfnImagePropsMixin.DeletionSettingsProperty(
                execution_role="executionRole"
            ),
            distribution_configuration_arn="distributionConfigurationArn",
            enhanced_image_metadata_enabled=False,
            execution_role="executionRole",
            image_pipeline_execution_settings=imagebuilder_mixins.CfnImagePropsMixin.ImagePipelineExecutionSettingsProperty(
                deployment_id="deploymentId",
                on_update=False
            ),
            image_recipe_arn="imageRecipeArn",
            image_scanning_configuration=imagebuilder_mixins.CfnImagePropsMixin.ImageScanningConfigurationProperty(
                ecr_configuration=imagebuilder_mixins.CfnImagePropsMixin.EcrConfigurationProperty(
                    container_tags=["containerTags"],
                    repository_name="repositoryName"
                ),
                image_scanning_enabled=False
            ),
            image_tests_configuration=imagebuilder_mixins.CfnImagePropsMixin.ImageTestsConfigurationProperty(
                image_tests_enabled=False,
                timeout_minutes=123
            ),
            infrastructure_configuration_arn="infrastructureConfigurationArn",
            logging_configuration=imagebuilder_mixins.CfnImagePropsMixin.ImageLoggingConfigurationProperty(
                log_group_name="logGroupName"
            ),
            tags={
                "tags_key": "tags"
            },
            workflows=[imagebuilder_mixins.CfnImagePropsMixin.WorkflowConfigurationProperty(
                on_failure="onFailure",
                parallel_group="parallelGroup",
                parameters=[imagebuilder_mixins.CfnImagePropsMixin.WorkflowParameterProperty(
                    name="name",
                    value=["value"]
                )],
                workflow_arn="workflowArn"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnImageMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ImageBuilder::Image``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fec1826dc052f5bdb15d385f235beae833e076ef0fbaf2f898ea4f12e3fe2120)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cc7bfc7febc932c3ea6162c319b6e39f305bc2db72b83a6299439018ee83dd7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa0f00e7759be2a88a7b9629ba90f51b36ca17906931a4d7fe05b084ec31b73)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnImageMixinProps:
        return typing.cast(CfnImageMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImagePropsMixin.DeletionSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"execution_role": "executionRole"},
    )
    class DeletionSettingsProperty:
        def __init__(
            self,
            *,
            execution_role: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The deletion settings of the image, indicating whether to delete the underlying resources in addition to the image.

            :param execution_role: The execution role to use for deleting the image, as well as underlying resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-deletionsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                deletion_settings_property = imagebuilder_mixins.CfnImagePropsMixin.DeletionSettingsProperty(
                    execution_role="executionRole"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2949760e8d6926b2f23e40a6e6b2ea6b9bd57777efeaae6140868208df75b9cb)
                check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if execution_role is not None:
                self._values["execution_role"] = execution_role

        @builtins.property
        def execution_role(self) -> typing.Optional[builtins.str]:
            '''The execution role to use for deleting the image, as well as underlying resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-deletionsettings.html#cfn-imagebuilder-image-deletionsettings-executionrole
            '''
            result = self._values.get("execution_role")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeletionSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImagePropsMixin.EcrConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "container_tags": "containerTags",
            "repository_name": "repositoryName",
        },
    )
    class EcrConfigurationProperty:
        def __init__(
            self,
            *,
            container_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
            repository_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings that Image Builder uses to configure the ECR repository and the output container images that Amazon Inspector scans.

            :param container_tags: Tags for Image Builder to apply to the output container image that Amazon Inspector scans. Tags can help you identify and manage your scanned images.
            :param repository_name: The name of the container repository that Amazon Inspector scans to identify findings for your container images. The name includes the path for the repository location. If you don’t provide this information, Image Builder creates a repository in your account named ``image-builder-image-scanning-repository`` for vulnerability scans of your output container images.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-ecrconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                ecr_configuration_property = imagebuilder_mixins.CfnImagePropsMixin.EcrConfigurationProperty(
                    container_tags=["containerTags"],
                    repository_name="repositoryName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9f279c26cca45e2bc94c97157e8d10bf918dc1ba231cd2575af8aca69f3f803b)
                check_type(argname="argument container_tags", value=container_tags, expected_type=type_hints["container_tags"])
                check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if container_tags is not None:
                self._values["container_tags"] = container_tags
            if repository_name is not None:
                self._values["repository_name"] = repository_name

        @builtins.property
        def container_tags(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Tags for Image Builder to apply to the output container image that Amazon Inspector scans.

            Tags can help you identify and manage your scanned images.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-ecrconfiguration.html#cfn-imagebuilder-image-ecrconfiguration-containertags
            '''
            result = self._values.get("container_tags")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def repository_name(self) -> typing.Optional[builtins.str]:
            '''The name of the container repository that Amazon Inspector scans to identify findings for your container images.

            The name includes the path for the repository location. If you don’t provide this information, Image Builder creates a repository in your account named ``image-builder-image-scanning-repository`` for vulnerability scans of your output container images.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-ecrconfiguration.html#cfn-imagebuilder-image-ecrconfiguration-repositoryname
            '''
            result = self._values.get("repository_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EcrConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImagePropsMixin.ImageLoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_name": "logGroupName"},
    )
    class ImageLoggingConfigurationProperty:
        def __init__(
            self,
            *,
            log_group_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The logging configuration that's defined for the image.

            Image Builder uses the defined settings to direct execution log output during image creation.

            :param log_group_name: The log group name that Image Builder uses for image creation. If not specified, the log group name defaults to ``/aws/imagebuilder/image-name`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-imageloggingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                image_logging_configuration_property = imagebuilder_mixins.CfnImagePropsMixin.ImageLoggingConfigurationProperty(
                    log_group_name="logGroupName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__18ca6049f95efb283b98ebba3e5690737e756345fa6d54187edf56e76d0601df)
                check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_group_name is not None:
                self._values["log_group_name"] = log_group_name

        @builtins.property
        def log_group_name(self) -> typing.Optional[builtins.str]:
            '''The log group name that Image Builder uses for image creation.

            If not specified, the log group name defaults to ``/aws/imagebuilder/image-name`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-imageloggingconfiguration.html#cfn-imagebuilder-image-imageloggingconfiguration-loggroupname
            '''
            result = self._values.get("log_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImageLoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImagePropsMixin.ImagePipelineExecutionSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"deployment_id": "deploymentId", "on_update": "onUpdate"},
    )
    class ImagePipelineExecutionSettingsProperty:
        def __init__(
            self,
            *,
            deployment_id: typing.Optional[builtins.str] = None,
            on_update: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The settings for starting an image pipeline execution.

            :param deployment_id: The deployment ID of the pipeline, used to trigger new image pipeline executions.
            :param on_update: Whether to trigger the image pipeline when the pipeline is updated. False by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-imagepipelineexecutionsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                image_pipeline_execution_settings_property = imagebuilder_mixins.CfnImagePropsMixin.ImagePipelineExecutionSettingsProperty(
                    deployment_id="deploymentId",
                    on_update=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4cb6c93e67f67335d07de8e8ed01ecfa21335ea11cc5d8037f747706798814db)
                check_type(argname="argument deployment_id", value=deployment_id, expected_type=type_hints["deployment_id"])
                check_type(argname="argument on_update", value=on_update, expected_type=type_hints["on_update"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if deployment_id is not None:
                self._values["deployment_id"] = deployment_id
            if on_update is not None:
                self._values["on_update"] = on_update

        @builtins.property
        def deployment_id(self) -> typing.Optional[builtins.str]:
            '''The deployment ID of the pipeline, used to trigger new image pipeline executions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-imagepipelineexecutionsettings.html#cfn-imagebuilder-image-imagepipelineexecutionsettings-deploymentid
            '''
            result = self._values.get("deployment_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def on_update(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether to trigger the image pipeline when the pipeline is updated.

            False by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-imagepipelineexecutionsettings.html#cfn-imagebuilder-image-imagepipelineexecutionsettings-onupdate
            '''
            result = self._values.get("on_update")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImagePipelineExecutionSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImagePropsMixin.ImageScanningConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ecr_configuration": "ecrConfiguration",
            "image_scanning_enabled": "imageScanningEnabled",
        },
    )
    class ImageScanningConfigurationProperty:
        def __init__(
            self,
            *,
            ecr_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImagePropsMixin.EcrConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            image_scanning_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Contains settings for Image Builder image resource and container image scans.

            :param ecr_configuration: Contains Amazon ECR settings for vulnerability scans.
            :param image_scanning_enabled: A setting that indicates whether Image Builder keeps a snapshot of the vulnerability scans that Amazon Inspector runs against the build instance when you create a new image.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-imagescanningconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                image_scanning_configuration_property = imagebuilder_mixins.CfnImagePropsMixin.ImageScanningConfigurationProperty(
                    ecr_configuration=imagebuilder_mixins.CfnImagePropsMixin.EcrConfigurationProperty(
                        container_tags=["containerTags"],
                        repository_name="repositoryName"
                    ),
                    image_scanning_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__237d0fe6eb6d9d225cd163e4576a58703b3b930e96b29a0a5c213c90ae0f3d9d)
                check_type(argname="argument ecr_configuration", value=ecr_configuration, expected_type=type_hints["ecr_configuration"])
                check_type(argname="argument image_scanning_enabled", value=image_scanning_enabled, expected_type=type_hints["image_scanning_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ecr_configuration is not None:
                self._values["ecr_configuration"] = ecr_configuration
            if image_scanning_enabled is not None:
                self._values["image_scanning_enabled"] = image_scanning_enabled

        @builtins.property
        def ecr_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePropsMixin.EcrConfigurationProperty"]]:
            '''Contains Amazon ECR settings for vulnerability scans.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-imagescanningconfiguration.html#cfn-imagebuilder-image-imagescanningconfiguration-ecrconfiguration
            '''
            result = self._values.get("ecr_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePropsMixin.EcrConfigurationProperty"]], result)

        @builtins.property
        def image_scanning_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A setting that indicates whether Image Builder keeps a snapshot of the vulnerability scans that Amazon Inspector runs against the build instance when you create a new image.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-imagescanningconfiguration.html#cfn-imagebuilder-image-imagescanningconfiguration-imagescanningenabled
            '''
            result = self._values.get("image_scanning_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImageScanningConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImagePropsMixin.ImageTestsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "image_tests_enabled": "imageTestsEnabled",
            "timeout_minutes": "timeoutMinutes",
        },
    )
    class ImageTestsConfigurationProperty:
        def __init__(
            self,
            *,
            image_tests_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            timeout_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''When you create an image or container recipe with Image Builder , you can add the build or test components that are used to create the final image.

            You must have at least one build component to create a recipe, but test components are not required. If you have added tests, they run after the image is created, to ensure that the target image is functional and can be used reliably for launching Amazon EC2 instances.

            :param image_tests_enabled: Determines if tests should run after building the image. Image Builder defaults to enable tests to run following the image build, before image distribution.
            :param timeout_minutes: The maximum time in minutes that tests are permitted to run. .. epigraph:: The timeout property is not currently active. This value is ignored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-imagetestsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                image_tests_configuration_property = imagebuilder_mixins.CfnImagePropsMixin.ImageTestsConfigurationProperty(
                    image_tests_enabled=False,
                    timeout_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0e7d928f26b38f98a2fa6d8caa4c5afa3af5c311e918aeac9c826c8b1ec38273)
                check_type(argname="argument image_tests_enabled", value=image_tests_enabled, expected_type=type_hints["image_tests_enabled"])
                check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if image_tests_enabled is not None:
                self._values["image_tests_enabled"] = image_tests_enabled
            if timeout_minutes is not None:
                self._values["timeout_minutes"] = timeout_minutes

        @builtins.property
        def image_tests_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines if tests should run after building the image.

            Image Builder defaults to enable tests to run following the image build, before image distribution.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-imagetestsconfiguration.html#cfn-imagebuilder-image-imagetestsconfiguration-imagetestsenabled
            '''
            result = self._values.get("image_tests_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def timeout_minutes(self) -> typing.Optional[jsii.Number]:
            '''The maximum time in minutes that tests are permitted to run.

            .. epigraph::

               The timeout property is not currently active. This value is ignored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-imagetestsconfiguration.html#cfn-imagebuilder-image-imagetestsconfiguration-timeoutminutes
            '''
            result = self._values.get("timeout_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImageTestsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImagePropsMixin.LatestVersionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "major": "major",
            "minor": "minor",
            "patch": "patch",
        },
    )
    class LatestVersionProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            major: typing.Optional[builtins.str] = None,
            minor: typing.Optional[builtins.str] = None,
            patch: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The latest version references of the image.

            :param arn: The Amazon Resource Name (ARN) of the image. .. epigraph:: Semantic versioning is included in each object's Amazon Resource Name (ARN), at the level that applies to that object as follows: - Versionless ARNs and Name ARNs do not include specific values in any of the nodes. The nodes are either left off entirely, or they are specified as wildcards, for example: x.x.x. - Version ARNs have only the first three nodes: .. - Build version ARNs have all four nodes, and point to a specific build for a specific version of an object.
            :param major: The latest version ARN of the created image, with the same major version.
            :param minor: The latest version ARN of the created image, with the same minor version.
            :param patch: The latest version ARN of the created image, with the same patch version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-latestversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                latest_version_property = imagebuilder_mixins.CfnImagePropsMixin.LatestVersionProperty(
                    arn="arn",
                    major="major",
                    minor="minor",
                    patch="patch"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d1e94e14b0acf3493afb70e1f191435d5ba3950a28547a43b05fea865550170c)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument major", value=major, expected_type=type_hints["major"])
                check_type(argname="argument minor", value=minor, expected_type=type_hints["minor"])
                check_type(argname="argument patch", value=patch, expected_type=type_hints["patch"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if major is not None:
                self._values["major"] = major
            if minor is not None:
                self._values["minor"] = minor
            if patch is not None:
                self._values["patch"] = patch

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the image.

            .. epigraph::

               Semantic versioning is included in each object's Amazon Resource Name (ARN), at the level that applies to that object as follows:

               - Versionless ARNs and Name ARNs do not include specific values in any of the nodes. The nodes are either left off entirely, or they are specified as wildcards, for example: x.x.x.
               - Version ARNs have only the first three nodes: ..
               - Build version ARNs have all four nodes, and point to a specific build for a specific version of an object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-latestversion.html#cfn-imagebuilder-image-latestversion-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def major(self) -> typing.Optional[builtins.str]:
            '''The latest version ARN of the created image, with the same major version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-latestversion.html#cfn-imagebuilder-image-latestversion-major
            '''
            result = self._values.get("major")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def minor(self) -> typing.Optional[builtins.str]:
            '''The latest version ARN of the created image, with the same minor version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-latestversion.html#cfn-imagebuilder-image-latestversion-minor
            '''
            result = self._values.get("minor")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def patch(self) -> typing.Optional[builtins.str]:
            '''The latest version ARN of the created image, with the same patch version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-latestversion.html#cfn-imagebuilder-image-latestversion-patch
            '''
            result = self._values.get("patch")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LatestVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImagePropsMixin.WorkflowConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "on_failure": "onFailure",
            "parallel_group": "parallelGroup",
            "parameters": "parameters",
            "workflow_arn": "workflowArn",
        },
    )
    class WorkflowConfigurationProperty:
        def __init__(
            self,
            *,
            on_failure: typing.Optional[builtins.str] = None,
            parallel_group: typing.Optional[builtins.str] = None,
            parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImagePropsMixin.WorkflowParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            workflow_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains control settings and configurable inputs for a workflow resource.

            :param on_failure: The action to take if the workflow fails.
            :param parallel_group: Test workflows are defined within named runtime groups called parallel groups. The parallel group is the named group that contains this test workflow. Test workflows within a parallel group can run at the same time. Image Builder starts up to five test workflows in the group at the same time, and starts additional workflows as others complete, until all workflows in the group have completed. This field only applies for test workflows.
            :param parameters: Contains parameter values for each of the parameters that the workflow document defined for the workflow resource.
            :param workflow_arn: The Amazon Resource Name (ARN) of the workflow resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-workflowconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                workflow_configuration_property = imagebuilder_mixins.CfnImagePropsMixin.WorkflowConfigurationProperty(
                    on_failure="onFailure",
                    parallel_group="parallelGroup",
                    parameters=[imagebuilder_mixins.CfnImagePropsMixin.WorkflowParameterProperty(
                        name="name",
                        value=["value"]
                    )],
                    workflow_arn="workflowArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cfecb272dd58294c75966e07b9b7a15e5d7da357229726bb1d080df36163d187)
                check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
                check_type(argname="argument parallel_group", value=parallel_group, expected_type=type_hints["parallel_group"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument workflow_arn", value=workflow_arn, expected_type=type_hints["workflow_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if on_failure is not None:
                self._values["on_failure"] = on_failure
            if parallel_group is not None:
                self._values["parallel_group"] = parallel_group
            if parameters is not None:
                self._values["parameters"] = parameters
            if workflow_arn is not None:
                self._values["workflow_arn"] = workflow_arn

        @builtins.property
        def on_failure(self) -> typing.Optional[builtins.str]:
            '''The action to take if the workflow fails.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-workflowconfiguration.html#cfn-imagebuilder-image-workflowconfiguration-onfailure
            '''
            result = self._values.get("on_failure")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parallel_group(self) -> typing.Optional[builtins.str]:
            '''Test workflows are defined within named runtime groups called parallel groups.

            The parallel group is the named group that contains this test workflow. Test workflows within a parallel group can run at the same time. Image Builder starts up to five test workflows in the group at the same time, and starts additional workflows as others complete, until all workflows in the group have completed. This field only applies for test workflows.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-workflowconfiguration.html#cfn-imagebuilder-image-workflowconfiguration-parallelgroup
            '''
            result = self._values.get("parallel_group")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePropsMixin.WorkflowParameterProperty"]]]]:
            '''Contains parameter values for each of the parameters that the workflow document defined for the workflow resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-workflowconfiguration.html#cfn-imagebuilder-image-workflowconfiguration-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImagePropsMixin.WorkflowParameterProperty"]]]], result)

        @builtins.property
        def workflow_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the workflow resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-workflowconfiguration.html#cfn-imagebuilder-image-workflowconfiguration-workflowarn
            '''
            result = self._values.get("workflow_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkflowConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImagePropsMixin.WorkflowParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class WorkflowParameterProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Contains a key/value pair that sets the named workflow parameter.

            :param name: The name of the workflow parameter to set.
            :param value: Sets the value for the named workflow parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-workflowparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                workflow_parameter_property = imagebuilder_mixins.CfnImagePropsMixin.WorkflowParameterProperty(
                    name="name",
                    value=["value"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__35f4ee175cbfb950dc02c53f270ef6e361abcbb05defe578e4d860b81c9ee07d)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the workflow parameter to set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-workflowparameter.html#cfn-imagebuilder-image-workflowparameter-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Sets the value for the named workflow parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-image-workflowparameter.html#cfn-imagebuilder-image-workflowparameter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkflowParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImageRecipeMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "additional_instance_configuration": "additionalInstanceConfiguration",
        "ami_tags": "amiTags",
        "block_device_mappings": "blockDeviceMappings",
        "components": "components",
        "description": "description",
        "name": "name",
        "parent_image": "parentImage",
        "tags": "tags",
        "version": "version",
        "working_directory": "workingDirectory",
    },
)
class CfnImageRecipeMixinProps:
    def __init__(
        self,
        *,
        additional_instance_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImageRecipePropsMixin.AdditionalInstanceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ami_tags: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        block_device_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImageRecipePropsMixin.InstanceBlockDeviceMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        components: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImageRecipePropsMixin.ComponentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        parent_image: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        version: typing.Optional[builtins.str] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnImageRecipePropsMixin.

        :param additional_instance_configuration: Before you create a new AMI, Image Builder launches temporary Amazon EC2 instances to build and test your image configuration. Instance configuration adds a layer of control over those instances. You can define settings and add scripts to run when an instance is launched from your AMI.
        :param ami_tags: Tags that are applied to the AMI that Image Builder creates during the Build phase prior to image distribution.
        :param block_device_mappings: The block device mappings to apply when creating images from this recipe.
        :param components: The components that are included in the image recipe. Recipes require a minimum of one build component, and can have a maximum of 20 build and test components in any combination.
        :param description: The description of the image recipe.
        :param name: The name of the image recipe.
        :param parent_image: The base image for customizations specified in the image recipe. You can specify the parent image using one of the following options: - AMI ID - Image Builder image Amazon Resource Name (ARN) - AWS Systems Manager (SSM) Parameter Store Parameter, prefixed by ``ssm:`` , followed by the parameter name or ARN. - AWS Marketplace product ID
        :param tags: The tags of the image recipe.
        :param version: The version of the image recipe.
        :param working_directory: The working directory to be used during build and test workflows.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
            
            cfn_image_recipe_mixin_props = imagebuilder_mixins.CfnImageRecipeMixinProps(
                additional_instance_configuration=imagebuilder_mixins.CfnImageRecipePropsMixin.AdditionalInstanceConfigurationProperty(
                    systems_manager_agent=imagebuilder_mixins.CfnImageRecipePropsMixin.SystemsManagerAgentProperty(
                        uninstall_after_build=False
                    ),
                    user_data_override="userDataOverride"
                ),
                ami_tags={
                    "ami_tags_key": "amiTags"
                },
                block_device_mappings=[imagebuilder_mixins.CfnImageRecipePropsMixin.InstanceBlockDeviceMappingProperty(
                    device_name="deviceName",
                    ebs=imagebuilder_mixins.CfnImageRecipePropsMixin.EbsInstanceBlockDeviceSpecificationProperty(
                        delete_on_termination=False,
                        encrypted=False,
                        iops=123,
                        kms_key_id="kmsKeyId",
                        snapshot_id="snapshotId",
                        throughput=123,
                        volume_size=123,
                        volume_type="volumeType"
                    ),
                    no_device="noDevice",
                    virtual_name="virtualName"
                )],
                components=[imagebuilder_mixins.CfnImageRecipePropsMixin.ComponentConfigurationProperty(
                    component_arn="componentArn",
                    parameters=[imagebuilder_mixins.CfnImageRecipePropsMixin.ComponentParameterProperty(
                        name="name",
                        value=["value"]
                    )]
                )],
                description="description",
                name="name",
                parent_image="parentImage",
                tags={
                    "tags_key": "tags"
                },
                version="version",
                working_directory="workingDirectory"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce929e277d6ba31bdb8ff37d76af55403c0e4454344f7fba64059a2f657a09db)
            check_type(argname="argument additional_instance_configuration", value=additional_instance_configuration, expected_type=type_hints["additional_instance_configuration"])
            check_type(argname="argument ami_tags", value=ami_tags, expected_type=type_hints["ami_tags"])
            check_type(argname="argument block_device_mappings", value=block_device_mappings, expected_type=type_hints["block_device_mappings"])
            check_type(argname="argument components", value=components, expected_type=type_hints["components"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parent_image", value=parent_image, expected_type=type_hints["parent_image"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_instance_configuration is not None:
            self._values["additional_instance_configuration"] = additional_instance_configuration
        if ami_tags is not None:
            self._values["ami_tags"] = ami_tags
        if block_device_mappings is not None:
            self._values["block_device_mappings"] = block_device_mappings
        if components is not None:
            self._values["components"] = components
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if parent_image is not None:
            self._values["parent_image"] = parent_image
        if tags is not None:
            self._values["tags"] = tags
        if version is not None:
            self._values["version"] = version
        if working_directory is not None:
            self._values["working_directory"] = working_directory

    @builtins.property
    def additional_instance_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImageRecipePropsMixin.AdditionalInstanceConfigurationProperty"]]:
        '''Before you create a new AMI, Image Builder launches temporary Amazon EC2 instances to build and test your image configuration.

        Instance configuration adds a layer of control over those instances. You can define settings and add scripts to run when an instance is launched from your AMI.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html#cfn-imagebuilder-imagerecipe-additionalinstanceconfiguration
        '''
        result = self._values.get("additional_instance_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImageRecipePropsMixin.AdditionalInstanceConfigurationProperty"]], result)

    @builtins.property
    def ami_tags(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''Tags that are applied to the AMI that Image Builder creates during the Build phase prior to image distribution.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html#cfn-imagebuilder-imagerecipe-amitags
        '''
        result = self._values.get("ami_tags")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def block_device_mappings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImageRecipePropsMixin.InstanceBlockDeviceMappingProperty"]]]]:
        '''The block device mappings to apply when creating images from this recipe.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html#cfn-imagebuilder-imagerecipe-blockdevicemappings
        '''
        result = self._values.get("block_device_mappings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImageRecipePropsMixin.InstanceBlockDeviceMappingProperty"]]]], result)

    @builtins.property
    def components(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImageRecipePropsMixin.ComponentConfigurationProperty"]]]]:
        '''The components that are included in the image recipe.

        Recipes require a minimum of one build component, and can have a maximum of 20 build and test components in any combination.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html#cfn-imagebuilder-imagerecipe-components
        '''
        result = self._values.get("components")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImageRecipePropsMixin.ComponentConfigurationProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the image recipe.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html#cfn-imagebuilder-imagerecipe-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the image recipe.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html#cfn-imagebuilder-imagerecipe-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent_image(self) -> typing.Optional[builtins.str]:
        '''The base image for customizations specified in the image recipe.

        You can specify the parent image using one of the following options:

        - AMI ID
        - Image Builder image Amazon Resource Name (ARN)
        - AWS Systems Manager (SSM) Parameter Store Parameter, prefixed by ``ssm:`` , followed by the parameter name or ARN.
        - AWS Marketplace product ID

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html#cfn-imagebuilder-imagerecipe-parentimage
        '''
        result = self._values.get("parent_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags of the image recipe.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html#cfn-imagebuilder-imagerecipe-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The version of the image recipe.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html#cfn-imagebuilder-imagerecipe-version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def working_directory(self) -> typing.Optional[builtins.str]:
        '''The working directory to be used during build and test workflows.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html#cfn-imagebuilder-imagerecipe-workingdirectory
        '''
        result = self._values.get("working_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnImageRecipeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnImageRecipePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImageRecipePropsMixin",
):
    '''Creates a new image recipe.

    Image recipes define how images are configured, tested, and assessed.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-imagerecipe.html
    :cloudformationResource: AWS::ImageBuilder::ImageRecipe
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
        
        cfn_image_recipe_props_mixin = imagebuilder_mixins.CfnImageRecipePropsMixin(imagebuilder_mixins.CfnImageRecipeMixinProps(
            additional_instance_configuration=imagebuilder_mixins.CfnImageRecipePropsMixin.AdditionalInstanceConfigurationProperty(
                systems_manager_agent=imagebuilder_mixins.CfnImageRecipePropsMixin.SystemsManagerAgentProperty(
                    uninstall_after_build=False
                ),
                user_data_override="userDataOverride"
            ),
            ami_tags={
                "ami_tags_key": "amiTags"
            },
            block_device_mappings=[imagebuilder_mixins.CfnImageRecipePropsMixin.InstanceBlockDeviceMappingProperty(
                device_name="deviceName",
                ebs=imagebuilder_mixins.CfnImageRecipePropsMixin.EbsInstanceBlockDeviceSpecificationProperty(
                    delete_on_termination=False,
                    encrypted=False,
                    iops=123,
                    kms_key_id="kmsKeyId",
                    snapshot_id="snapshotId",
                    throughput=123,
                    volume_size=123,
                    volume_type="volumeType"
                ),
                no_device="noDevice",
                virtual_name="virtualName"
            )],
            components=[imagebuilder_mixins.CfnImageRecipePropsMixin.ComponentConfigurationProperty(
                component_arn="componentArn",
                parameters=[imagebuilder_mixins.CfnImageRecipePropsMixin.ComponentParameterProperty(
                    name="name",
                    value=["value"]
                )]
            )],
            description="description",
            name="name",
            parent_image="parentImage",
            tags={
                "tags_key": "tags"
            },
            version="version",
            working_directory="workingDirectory"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnImageRecipeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ImageBuilder::ImageRecipe``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a03d8128c946f0dcf2b1a794676a822ae30b24819edd7e2a3bf3af60cd0e35d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53ec6d7d9fa8cc9e24f44b480170fd94251f1dbab1e08bd9a5e19a87f858c1af)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__321997575748627861ff20436d43801bf9660c25fa3ec75d737de9fab88349d2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnImageRecipeMixinProps:
        return typing.cast(CfnImageRecipeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImageRecipePropsMixin.AdditionalInstanceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "systems_manager_agent": "systemsManagerAgent",
            "user_data_override": "userDataOverride",
        },
    )
    class AdditionalInstanceConfigurationProperty:
        def __init__(
            self,
            *,
            systems_manager_agent: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImageRecipePropsMixin.SystemsManagerAgentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            user_data_override: typing.Optional[builtins.str] = None,
        ) -> None:
            '''In addition to your infrastructure configuration, these settings provide an extra layer of control over your build instances.

            You can also specify commands to run on launch for all of your build instances.

            Image Builder does not automatically install the Systems Manager agent on Windows instances. If your base image includes the Systems Manager agent, then the AMI that you create will also include the agent. For Linux instances, if the base image does not already include the Systems Manager agent, Image Builder installs it. For Linux instances where Image Builder installs the Systems Manager agent, you can choose whether to keep it for the AMI that you create.

            :param systems_manager_agent: Contains settings for the Systems Manager agent on your build instance.
            :param user_data_override: Use this property to provide commands or a command script to run when you launch your build instance. The userDataOverride property replaces any commands that Image Builder might have added to ensure that Systems Manager is installed on your Linux build instance. If you override the user data, make sure that you add commands to install Systems Manager, if it is not pre-installed on your base image. .. epigraph:: The user data is always base 64 encoded. For example, the following commands are encoded as ``IyEvYmluL2Jhc2gKbWtkaXIgLXAgL3Zhci9iYi8KdG91Y2ggL3Zhci$`` : *#!/bin/bash* mkdir -p /var/bb/ touch /var

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-additionalinstanceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                additional_instance_configuration_property = imagebuilder_mixins.CfnImageRecipePropsMixin.AdditionalInstanceConfigurationProperty(
                    systems_manager_agent=imagebuilder_mixins.CfnImageRecipePropsMixin.SystemsManagerAgentProperty(
                        uninstall_after_build=False
                    ),
                    user_data_override="userDataOverride"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2ea1555ded0d1fe96d1f1c5ac0769af6a2534a244e716586f432cb789a2d64db)
                check_type(argname="argument systems_manager_agent", value=systems_manager_agent, expected_type=type_hints["systems_manager_agent"])
                check_type(argname="argument user_data_override", value=user_data_override, expected_type=type_hints["user_data_override"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if systems_manager_agent is not None:
                self._values["systems_manager_agent"] = systems_manager_agent
            if user_data_override is not None:
                self._values["user_data_override"] = user_data_override

        @builtins.property
        def systems_manager_agent(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImageRecipePropsMixin.SystemsManagerAgentProperty"]]:
            '''Contains settings for the Systems Manager agent on your build instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-additionalinstanceconfiguration.html#cfn-imagebuilder-imagerecipe-additionalinstanceconfiguration-systemsmanageragent
            '''
            result = self._values.get("systems_manager_agent")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImageRecipePropsMixin.SystemsManagerAgentProperty"]], result)

        @builtins.property
        def user_data_override(self) -> typing.Optional[builtins.str]:
            '''Use this property to provide commands or a command script to run when you launch your build instance.

            The userDataOverride property replaces any commands that Image Builder might have added to ensure that Systems Manager is installed on your Linux build instance. If you override the user data, make sure that you add commands to install Systems Manager, if it is not pre-installed on your base image.
            .. epigraph::

               The user data is always base 64 encoded. For example, the following commands are encoded as ``IyEvYmluL2Jhc2gKbWtkaXIgLXAgL3Zhci9iYi8KdG91Y2ggL3Zhci$`` :

               *#!/bin/bash*

               mkdir -p /var/bb/

               touch /var

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-additionalinstanceconfiguration.html#cfn-imagebuilder-imagerecipe-additionalinstanceconfiguration-userdataoverride
            '''
            result = self._values.get("user_data_override")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdditionalInstanceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImageRecipePropsMixin.ComponentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"component_arn": "componentArn", "parameters": "parameters"},
    )
    class ComponentConfigurationProperty:
        def __init__(
            self,
            *,
            component_arn: typing.Optional[builtins.str] = None,
            parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImageRecipePropsMixin.ComponentParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Configuration details of the component.

            :param component_arn: The Amazon Resource Name (ARN) of the component.
            :param parameters: A group of parameter settings that Image Builder uses to configure the component for a specific recipe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-componentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                component_configuration_property = imagebuilder_mixins.CfnImageRecipePropsMixin.ComponentConfigurationProperty(
                    component_arn="componentArn",
                    parameters=[imagebuilder_mixins.CfnImageRecipePropsMixin.ComponentParameterProperty(
                        name="name",
                        value=["value"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6809c8c3e6425e9a779a29f87bdfc3ab9460f54ae8f3d7d24315d54bf921027f)
                check_type(argname="argument component_arn", value=component_arn, expected_type=type_hints["component_arn"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if component_arn is not None:
                self._values["component_arn"] = component_arn
            if parameters is not None:
                self._values["parameters"] = parameters

        @builtins.property
        def component_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-componentconfiguration.html#cfn-imagebuilder-imagerecipe-componentconfiguration-componentarn
            '''
            result = self._values.get("component_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImageRecipePropsMixin.ComponentParameterProperty"]]]]:
            '''A group of parameter settings that Image Builder uses to configure the component for a specific recipe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-componentconfiguration.html#cfn-imagebuilder-imagerecipe-componentconfiguration-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImageRecipePropsMixin.ComponentParameterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImageRecipePropsMixin.ComponentParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class ComponentParameterProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Contains a key/value pair that sets the named component parameter.

            :param name: The name of the component parameter to set.
            :param value: Sets the value for the named component parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-componentparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                component_parameter_property = imagebuilder_mixins.CfnImageRecipePropsMixin.ComponentParameterProperty(
                    name="name",
                    value=["value"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__145da444f4cdf0a2a8f173f89f416ac19403ff2e07baadf2a2d0015e5f04325e)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the component parameter to set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-componentparameter.html#cfn-imagebuilder-imagerecipe-componentparameter-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Sets the value for the named component parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-componentparameter.html#cfn-imagebuilder-imagerecipe-componentparameter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImageRecipePropsMixin.EbsInstanceBlockDeviceSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delete_on_termination": "deleteOnTermination",
            "encrypted": "encrypted",
            "iops": "iops",
            "kms_key_id": "kmsKeyId",
            "snapshot_id": "snapshotId",
            "throughput": "throughput",
            "volume_size": "volumeSize",
            "volume_type": "volumeType",
        },
    )
    class EbsInstanceBlockDeviceSpecificationProperty:
        def __init__(
            self,
            *,
            delete_on_termination: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            iops: typing.Optional[jsii.Number] = None,
            kms_key_id: typing.Optional[builtins.str] = None,
            snapshot_id: typing.Optional[builtins.str] = None,
            throughput: typing.Optional[jsii.Number] = None,
            volume_size: typing.Optional[jsii.Number] = None,
            volume_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The image recipe EBS instance block device specification includes the Amazon EBS-specific block device mapping specifications for the image.

            :param delete_on_termination: Configures delete on termination of the associated device.
            :param encrypted: Use to configure device encryption.
            :param iops: Use to configure device IOPS.
            :param kms_key_id: The Amazon Resource Name (ARN) that uniquely identifies the KMS key to use when encrypting the device. This can be either the Key ARN or the Alias ARN. For more information, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id-key-ARN>`_ in the *AWS Key Management Service Developer Guide* .
            :param snapshot_id: The snapshot that defines the device contents.
            :param throughput: *For GP3 volumes only* – The throughput in MiB/s that the volume supports.
            :param volume_size: Overrides the volume size of the device.
            :param volume_type: Overrides the volume type of the device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                ebs_instance_block_device_specification_property = imagebuilder_mixins.CfnImageRecipePropsMixin.EbsInstanceBlockDeviceSpecificationProperty(
                    delete_on_termination=False,
                    encrypted=False,
                    iops=123,
                    kms_key_id="kmsKeyId",
                    snapshot_id="snapshotId",
                    throughput=123,
                    volume_size=123,
                    volume_type="volumeType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__859a2bdb2df5bbc7446556ccdaa2099bb1fed1b3a7ad8f8f78f758924cb3f5a3)
                check_type(argname="argument delete_on_termination", value=delete_on_termination, expected_type=type_hints["delete_on_termination"])
                check_type(argname="argument encrypted", value=encrypted, expected_type=type_hints["encrypted"])
                check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
                check_type(argname="argument snapshot_id", value=snapshot_id, expected_type=type_hints["snapshot_id"])
                check_type(argname="argument throughput", value=throughput, expected_type=type_hints["throughput"])
                check_type(argname="argument volume_size", value=volume_size, expected_type=type_hints["volume_size"])
                check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delete_on_termination is not None:
                self._values["delete_on_termination"] = delete_on_termination
            if encrypted is not None:
                self._values["encrypted"] = encrypted
            if iops is not None:
                self._values["iops"] = iops
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id
            if snapshot_id is not None:
                self._values["snapshot_id"] = snapshot_id
            if throughput is not None:
                self._values["throughput"] = throughput
            if volume_size is not None:
                self._values["volume_size"] = volume_size
            if volume_type is not None:
                self._values["volume_type"] = volume_type

        @builtins.property
        def delete_on_termination(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Configures delete on termination of the associated device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification.html#cfn-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification-deleteontermination
            '''
            result = self._values.get("delete_on_termination")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def encrypted(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Use to configure device encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification.html#cfn-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification-encrypted
            '''
            result = self._values.get("encrypted")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            '''Use to configure device IOPS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification.html#cfn-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification-iops
            '''
            result = self._values.get("iops")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) that uniquely identifies the KMS key to use when encrypting the device.

            This can be either the Key ARN or the Alias ARN. For more information, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id-key-ARN>`_ in the *AWS Key Management Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification.html#cfn-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def snapshot_id(self) -> typing.Optional[builtins.str]:
            '''The snapshot that defines the device contents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification.html#cfn-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification-snapshotid
            '''
            result = self._values.get("snapshot_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def throughput(self) -> typing.Optional[jsii.Number]:
            '''*For GP3 volumes only* – The throughput in MiB/s that the volume supports.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification.html#cfn-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification-throughput
            '''
            result = self._values.get("throughput")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def volume_size(self) -> typing.Optional[jsii.Number]:
            '''Overrides the volume size of the device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification.html#cfn-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification-volumesize
            '''
            result = self._values.get("volume_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def volume_type(self) -> typing.Optional[builtins.str]:
            '''Overrides the volume type of the device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification.html#cfn-imagebuilder-imagerecipe-ebsinstanceblockdevicespecification-volumetype
            '''
            result = self._values.get("volume_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EbsInstanceBlockDeviceSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImageRecipePropsMixin.InstanceBlockDeviceMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "device_name": "deviceName",
            "ebs": "ebs",
            "no_device": "noDevice",
            "virtual_name": "virtualName",
        },
    )
    class InstanceBlockDeviceMappingProperty:
        def __init__(
            self,
            *,
            device_name: typing.Optional[builtins.str] = None,
            ebs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnImageRecipePropsMixin.EbsInstanceBlockDeviceSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            no_device: typing.Optional[builtins.str] = None,
            virtual_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines block device mappings for the instance used to configure your image.

            :param device_name: The device to which these mappings apply.
            :param ebs: Use to manage Amazon EBS-specific configuration for this mapping.
            :param no_device: Enter an empty string to remove a mapping from the parent image. The following is an example of an empty string value in the ``NoDevice`` field. ``NoDevice:""``
            :param virtual_name: Manages the instance ephemeral devices.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-instanceblockdevicemapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                instance_block_device_mapping_property = imagebuilder_mixins.CfnImageRecipePropsMixin.InstanceBlockDeviceMappingProperty(
                    device_name="deviceName",
                    ebs=imagebuilder_mixins.CfnImageRecipePropsMixin.EbsInstanceBlockDeviceSpecificationProperty(
                        delete_on_termination=False,
                        encrypted=False,
                        iops=123,
                        kms_key_id="kmsKeyId",
                        snapshot_id="snapshotId",
                        throughput=123,
                        volume_size=123,
                        volume_type="volumeType"
                    ),
                    no_device="noDevice",
                    virtual_name="virtualName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__57b065cf628c2f3726b15f1545f48ba6122a4f5622daada22f6962523e6d631c)
                check_type(argname="argument device_name", value=device_name, expected_type=type_hints["device_name"])
                check_type(argname="argument ebs", value=ebs, expected_type=type_hints["ebs"])
                check_type(argname="argument no_device", value=no_device, expected_type=type_hints["no_device"])
                check_type(argname="argument virtual_name", value=virtual_name, expected_type=type_hints["virtual_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if device_name is not None:
                self._values["device_name"] = device_name
            if ebs is not None:
                self._values["ebs"] = ebs
            if no_device is not None:
                self._values["no_device"] = no_device
            if virtual_name is not None:
                self._values["virtual_name"] = virtual_name

        @builtins.property
        def device_name(self) -> typing.Optional[builtins.str]:
            '''The device to which these mappings apply.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-instanceblockdevicemapping.html#cfn-imagebuilder-imagerecipe-instanceblockdevicemapping-devicename
            '''
            result = self._values.get("device_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ebs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImageRecipePropsMixin.EbsInstanceBlockDeviceSpecificationProperty"]]:
            '''Use to manage Amazon EBS-specific configuration for this mapping.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-instanceblockdevicemapping.html#cfn-imagebuilder-imagerecipe-instanceblockdevicemapping-ebs
            '''
            result = self._values.get("ebs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnImageRecipePropsMixin.EbsInstanceBlockDeviceSpecificationProperty"]], result)

        @builtins.property
        def no_device(self) -> typing.Optional[builtins.str]:
            '''Enter an empty string to remove a mapping from the parent image.

            The following is an example of an empty string value in the ``NoDevice`` field.

            ``NoDevice:""``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-instanceblockdevicemapping.html#cfn-imagebuilder-imagerecipe-instanceblockdevicemapping-nodevice
            '''
            result = self._values.get("no_device")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def virtual_name(self) -> typing.Optional[builtins.str]:
            '''Manages the instance ephemeral devices.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-instanceblockdevicemapping.html#cfn-imagebuilder-imagerecipe-instanceblockdevicemapping-virtualname
            '''
            result = self._values.get("virtual_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceBlockDeviceMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImageRecipePropsMixin.LatestVersionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "major": "major",
            "minor": "minor",
            "patch": "patch",
        },
    )
    class LatestVersionProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            major: typing.Optional[builtins.str] = None,
            minor: typing.Optional[builtins.str] = None,
            patch: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The latest version references of the image recipe.

            :param arn: The Amazon Resource Name (ARN) of the image recipe.
            :param major: The latest version ARN of the created image recipe, with the same major version.
            :param minor: The latest version ARN of the created image recipe, with the same minor version.
            :param patch: The latest version ARN of the created image recipe, with the same patch version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-latestversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                latest_version_property = imagebuilder_mixins.CfnImageRecipePropsMixin.LatestVersionProperty(
                    arn="arn",
                    major="major",
                    minor="minor",
                    patch="patch"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__885f8989970d10e9349c326a26f89622ce2a05fe5ea3c57a113a45311f382206)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument major", value=major, expected_type=type_hints["major"])
                check_type(argname="argument minor", value=minor, expected_type=type_hints["minor"])
                check_type(argname="argument patch", value=patch, expected_type=type_hints["patch"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if major is not None:
                self._values["major"] = major
            if minor is not None:
                self._values["minor"] = minor
            if patch is not None:
                self._values["patch"] = patch

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the image recipe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-latestversion.html#cfn-imagebuilder-imagerecipe-latestversion-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def major(self) -> typing.Optional[builtins.str]:
            '''The latest version ARN of the created image recipe, with the same major version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-latestversion.html#cfn-imagebuilder-imagerecipe-latestversion-major
            '''
            result = self._values.get("major")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def minor(self) -> typing.Optional[builtins.str]:
            '''The latest version ARN of the created image recipe, with the same minor version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-latestversion.html#cfn-imagebuilder-imagerecipe-latestversion-minor
            '''
            result = self._values.get("minor")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def patch(self) -> typing.Optional[builtins.str]:
            '''The latest version ARN of the created image recipe, with the same patch version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-latestversion.html#cfn-imagebuilder-imagerecipe-latestversion-patch
            '''
            result = self._values.get("patch")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LatestVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnImageRecipePropsMixin.SystemsManagerAgentProperty",
        jsii_struct_bases=[],
        name_mapping={"uninstall_after_build": "uninstallAfterBuild"},
    )
    class SystemsManagerAgentProperty:
        def __init__(
            self,
            *,
            uninstall_after_build: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Contains settings for the Systems Manager agent on your build instance.

            :param uninstall_after_build: Controls whether the Systems Manager agent is removed from your final build image, prior to creating the new AMI. If this is set to true, then the agent is removed from the final image. If it's set to false, then the agent is left in, so that it is included in the new AMI. default value is false. The default behavior of uninstallAfterBuild is to remove the SSM Agent if it was installed by EC2 Image Builder

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-systemsmanageragent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                systems_manager_agent_property = imagebuilder_mixins.CfnImageRecipePropsMixin.SystemsManagerAgentProperty(
                    uninstall_after_build=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7097147b04dd06e0365924ffb180772fa651964b1747a45c2cd873e7f560ac0f)
                check_type(argname="argument uninstall_after_build", value=uninstall_after_build, expected_type=type_hints["uninstall_after_build"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if uninstall_after_build is not None:
                self._values["uninstall_after_build"] = uninstall_after_build

        @builtins.property
        def uninstall_after_build(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Controls whether the Systems Manager agent is removed from your final build image, prior to creating the new AMI.

            If this is set to true, then the agent is removed from the final image. If it's set to false, then the agent is left in, so that it is included in the new AMI. default value is false.

            The default behavior of uninstallAfterBuild is to remove the SSM Agent if it was installed by EC2 Image Builder

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-imagerecipe-systemsmanageragent.html#cfn-imagebuilder-imagerecipe-systemsmanageragent-uninstallafterbuild
            '''
            result = self._values.get("uninstall_after_build")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SystemsManagerAgentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnInfrastructureConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "instance_metadata_options": "instanceMetadataOptions",
        "instance_profile_name": "instanceProfileName",
        "instance_types": "instanceTypes",
        "key_pair": "keyPair",
        "logging": "logging",
        "name": "name",
        "placement": "placement",
        "resource_tags": "resourceTags",
        "security_group_ids": "securityGroupIds",
        "sns_topic_arn": "snsTopicArn",
        "subnet_id": "subnetId",
        "tags": "tags",
        "terminate_instance_on_failure": "terminateInstanceOnFailure",
    },
)
class CfnInfrastructureConfigurationMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        instance_metadata_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInfrastructureConfigurationPropsMixin.InstanceMetadataOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_profile_name: typing.Optional[builtins.str] = None,
        instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        key_pair: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInfrastructureConfigurationPropsMixin.LoggingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        placement: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInfrastructureConfigurationPropsMixin.PlacementProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        resource_tags: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        sns_topic_arn: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        terminate_instance_on_failure: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ) -> None:
        '''Properties for CfnInfrastructureConfigurationPropsMixin.

        :param description: The description of the infrastructure configuration.
        :param instance_metadata_options: The instance metadata options that you can set for the HTTP requests that pipeline builds use to launch EC2 build and test instances.
        :param instance_profile_name: The instance profile to associate with the instance used to customize your Amazon EC2 AMI.
        :param instance_types: The instance types of the infrastructure configuration. You can specify one or more instance types to use for this build. The service will pick one of these instance types based on availability.
        :param key_pair: The key pair of the infrastructure configuration. You can use this to log on to and debug the instance used to create your image.
        :param logging: The logging configuration of the infrastructure configuration.
        :param name: The name of the infrastructure configuration.
        :param placement: The instance placement settings that define where the instances that are launched from your image will run.
        :param resource_tags: The metadata tags to assign to the Amazon EC2 instance that Image Builder launches during the build process. Tags are formatted as key value pairs.
        :param security_group_ids: The security group IDs to associate with the instance used to customize your Amazon EC2 AMI.
        :param sns_topic_arn: The Amazon Resource Name (ARN) for the SNS topic to which we send image build event notifications. .. epigraph:: EC2 Image Builder is unable to send notifications to SNS topics that are encrypted using keys from other accounts. The key that is used to encrypt the SNS topic must reside in the account that the Image Builder service runs under.
        :param subnet_id: The subnet ID in which to place the instance used to customize your Amazon EC2 AMI.
        :param tags: The metadata tags to assign to the infrastructure configuration resource that Image Builder creates as output. Tags are formatted as key value pairs.
        :param terminate_instance_on_failure: The terminate instance on failure setting of the infrastructure configuration. Set to false if you want Image Builder to retain the instance used to configure your AMI if the build or test phase of your workflow fails.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
            
            cfn_infrastructure_configuration_mixin_props = imagebuilder_mixins.CfnInfrastructureConfigurationMixinProps(
                description="description",
                instance_metadata_options=imagebuilder_mixins.CfnInfrastructureConfigurationPropsMixin.InstanceMetadataOptionsProperty(
                    http_put_response_hop_limit=123,
                    http_tokens="httpTokens"
                ),
                instance_profile_name="instanceProfileName",
                instance_types=["instanceTypes"],
                key_pair="keyPair",
                logging=imagebuilder_mixins.CfnInfrastructureConfigurationPropsMixin.LoggingProperty(
                    s3_logs=imagebuilder_mixins.CfnInfrastructureConfigurationPropsMixin.S3LogsProperty(
                        s3_bucket_name="s3BucketName",
                        s3_key_prefix="s3KeyPrefix"
                    )
                ),
                name="name",
                placement=imagebuilder_mixins.CfnInfrastructureConfigurationPropsMixin.PlacementProperty(
                    availability_zone="availabilityZone",
                    host_id="hostId",
                    host_resource_group_arn="hostResourceGroupArn",
                    tenancy="tenancy"
                ),
                resource_tags={
                    "resource_tags_key": "resourceTags"
                },
                security_group_ids=["securityGroupIds"],
                sns_topic_arn="snsTopicArn",
                subnet_id="subnetId",
                tags={
                    "tags_key": "tags"
                },
                terminate_instance_on_failure=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78c63423ae164fc6c1ae635513bf7685937d20c543ecc658ad8c8d712ebcc70a)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument instance_metadata_options", value=instance_metadata_options, expected_type=type_hints["instance_metadata_options"])
            check_type(argname="argument instance_profile_name", value=instance_profile_name, expected_type=type_hints["instance_profile_name"])
            check_type(argname="argument instance_types", value=instance_types, expected_type=type_hints["instance_types"])
            check_type(argname="argument key_pair", value=key_pair, expected_type=type_hints["key_pair"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument placement", value=placement, expected_type=type_hints["placement"])
            check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument sns_topic_arn", value=sns_topic_arn, expected_type=type_hints["sns_topic_arn"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument terminate_instance_on_failure", value=terminate_instance_on_failure, expected_type=type_hints["terminate_instance_on_failure"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if instance_metadata_options is not None:
            self._values["instance_metadata_options"] = instance_metadata_options
        if instance_profile_name is not None:
            self._values["instance_profile_name"] = instance_profile_name
        if instance_types is not None:
            self._values["instance_types"] = instance_types
        if key_pair is not None:
            self._values["key_pair"] = key_pair
        if logging is not None:
            self._values["logging"] = logging
        if name is not None:
            self._values["name"] = name
        if placement is not None:
            self._values["placement"] = placement
        if resource_tags is not None:
            self._values["resource_tags"] = resource_tags
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if sns_topic_arn is not None:
            self._values["sns_topic_arn"] = sns_topic_arn
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if tags is not None:
            self._values["tags"] = tags
        if terminate_instance_on_failure is not None:
            self._values["terminate_instance_on_failure"] = terminate_instance_on_failure

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the infrastructure configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_metadata_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInfrastructureConfigurationPropsMixin.InstanceMetadataOptionsProperty"]]:
        '''The instance metadata options that you can set for the HTTP requests that pipeline builds use to launch EC2 build and test instances.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-instancemetadataoptions
        '''
        result = self._values.get("instance_metadata_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInfrastructureConfigurationPropsMixin.InstanceMetadataOptionsProperty"]], result)

    @builtins.property
    def instance_profile_name(self) -> typing.Optional[builtins.str]:
        '''The instance profile to associate with the instance used to customize your Amazon EC2 AMI.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-instanceprofilename
        '''
        result = self._values.get("instance_profile_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The instance types of the infrastructure configuration.

        You can specify one or more instance types to use for this build. The service will pick one of these instance types based on availability.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-instancetypes
        '''
        result = self._values.get("instance_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def key_pair(self) -> typing.Optional[builtins.str]:
        '''The key pair of the infrastructure configuration.

        You can use this to log on to and debug the instance used to create your image.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-keypair
        '''
        result = self._values.get("key_pair")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInfrastructureConfigurationPropsMixin.LoggingProperty"]]:
        '''The logging configuration of the infrastructure configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-logging
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInfrastructureConfigurationPropsMixin.LoggingProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the infrastructure configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def placement(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInfrastructureConfigurationPropsMixin.PlacementProperty"]]:
        '''The instance placement settings that define where the instances that are launched from your image will run.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-placement
        '''
        result = self._values.get("placement")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInfrastructureConfigurationPropsMixin.PlacementProperty"]], result)

    @builtins.property
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''The metadata tags to assign to the Amazon EC2 instance that Image Builder launches during the build process.

        Tags are formatted as key value pairs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-resourcetags
        '''
        result = self._values.get("resource_tags")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The security group IDs to associate with the instance used to customize your Amazon EC2 AMI.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sns_topic_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) for the SNS topic to which we send image build event notifications.

        .. epigraph::

           EC2 Image Builder is unable to send notifications to SNS topics that are encrypted using keys from other accounts. The key that is used to encrypt the SNS topic must reside in the account that the Image Builder service runs under.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-snstopicarn
        '''
        result = self._values.get("sns_topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''The subnet ID in which to place the instance used to customize your Amazon EC2 AMI.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-subnetid
        '''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The metadata tags to assign to the infrastructure configuration resource that Image Builder creates as output.

        Tags are formatted as key value pairs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def terminate_instance_on_failure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''The terminate instance on failure setting of the infrastructure configuration.

        Set to false if you want Image Builder to retain the instance used to configure your AMI if the build or test phase of your workflow fails.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html#cfn-imagebuilder-infrastructureconfiguration-terminateinstanceonfailure
        '''
        result = self._values.get("terminate_instance_on_failure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInfrastructureConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnInfrastructureConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnInfrastructureConfigurationPropsMixin",
):
    '''Creates a new infrastructure configuration.

    An infrastructure configuration defines the environment in which your image will be built and tested.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-infrastructureconfiguration.html
    :cloudformationResource: AWS::ImageBuilder::InfrastructureConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
        
        cfn_infrastructure_configuration_props_mixin = imagebuilder_mixins.CfnInfrastructureConfigurationPropsMixin(imagebuilder_mixins.CfnInfrastructureConfigurationMixinProps(
            description="description",
            instance_metadata_options=imagebuilder_mixins.CfnInfrastructureConfigurationPropsMixin.InstanceMetadataOptionsProperty(
                http_put_response_hop_limit=123,
                http_tokens="httpTokens"
            ),
            instance_profile_name="instanceProfileName",
            instance_types=["instanceTypes"],
            key_pair="keyPair",
            logging=imagebuilder_mixins.CfnInfrastructureConfigurationPropsMixin.LoggingProperty(
                s3_logs=imagebuilder_mixins.CfnInfrastructureConfigurationPropsMixin.S3LogsProperty(
                    s3_bucket_name="s3BucketName",
                    s3_key_prefix="s3KeyPrefix"
                )
            ),
            name="name",
            placement=imagebuilder_mixins.CfnInfrastructureConfigurationPropsMixin.PlacementProperty(
                availability_zone="availabilityZone",
                host_id="hostId",
                host_resource_group_arn="hostResourceGroupArn",
                tenancy="tenancy"
            ),
            resource_tags={
                "resource_tags_key": "resourceTags"
            },
            security_group_ids=["securityGroupIds"],
            sns_topic_arn="snsTopicArn",
            subnet_id="subnetId",
            tags={
                "tags_key": "tags"
            },
            terminate_instance_on_failure=False
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnInfrastructureConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ImageBuilder::InfrastructureConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__467564eb33c2fda88db762c1819250a37bc28063ba9f9d1157ea47dd291f8324)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7929a7a642870b8e6801b84b61402f351314058882ae948c56e8a51ed61630c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e02913d58db423cbf45bdcac6d40301596e32f1769256321eacf13355f5d31bb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnInfrastructureConfigurationMixinProps:
        return typing.cast(CfnInfrastructureConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnInfrastructureConfigurationPropsMixin.InstanceMetadataOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "http_put_response_hop_limit": "httpPutResponseHopLimit",
            "http_tokens": "httpTokens",
        },
    )
    class InstanceMetadataOptionsProperty:
        def __init__(
            self,
            *,
            http_put_response_hop_limit: typing.Optional[jsii.Number] = None,
            http_tokens: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The instance metadata options that apply to the HTTP requests that pipeline builds use to launch EC2 build and test instances.

            For more information about instance metadata options, see `Configure the instance metadata options <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-options.html>`_ in the **Amazon EC2 User Guide** for Linux instances, or `Configure the instance metadata options <https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/configuring-instance-metadata-options.html>`_ in the **Amazon EC2 Windows Guide** for Windows instances.

            :param http_put_response_hop_limit: Limit the number of hops that an instance metadata request can traverse to reach its destination. The default is one hop. However, if HTTP tokens are required, container image builds need a minimum of two hops.
            :param http_tokens: Indicates whether a signed token header is required for instance metadata retrieval requests. The values affect the response as follows: - *required* – When you retrieve the IAM role credentials, version 2.0 credentials are returned in all cases. - *optional* – You can include a signed token header in your request to retrieve instance metadata, or you can leave it out. If you include it, version 2.0 credentials are returned for the IAM role. Otherwise, version 1.0 credentials are returned. The default setting is *optional* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-infrastructureconfiguration-instancemetadataoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                instance_metadata_options_property = imagebuilder_mixins.CfnInfrastructureConfigurationPropsMixin.InstanceMetadataOptionsProperty(
                    http_put_response_hop_limit=123,
                    http_tokens="httpTokens"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4666cf57df0442cccb6a0521437243b6566be0ca42637d8516f35c28347d4990)
                check_type(argname="argument http_put_response_hop_limit", value=http_put_response_hop_limit, expected_type=type_hints["http_put_response_hop_limit"])
                check_type(argname="argument http_tokens", value=http_tokens, expected_type=type_hints["http_tokens"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if http_put_response_hop_limit is not None:
                self._values["http_put_response_hop_limit"] = http_put_response_hop_limit
            if http_tokens is not None:
                self._values["http_tokens"] = http_tokens

        @builtins.property
        def http_put_response_hop_limit(self) -> typing.Optional[jsii.Number]:
            '''Limit the number of hops that an instance metadata request can traverse to reach its destination.

            The default is one hop. However, if HTTP tokens are required, container image builds need a minimum of two hops.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-infrastructureconfiguration-instancemetadataoptions.html#cfn-imagebuilder-infrastructureconfiguration-instancemetadataoptions-httpputresponsehoplimit
            '''
            result = self._values.get("http_put_response_hop_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def http_tokens(self) -> typing.Optional[builtins.str]:
            '''Indicates whether a signed token header is required for instance metadata retrieval requests.

            The values affect the response as follows:

            - *required* – When you retrieve the IAM role credentials, version 2.0 credentials are returned in all cases.
            - *optional* – You can include a signed token header in your request to retrieve instance metadata, or you can leave it out. If you include it, version 2.0 credentials are returned for the IAM role. Otherwise, version 1.0 credentials are returned.

            The default setting is *optional* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-infrastructureconfiguration-instancemetadataoptions.html#cfn-imagebuilder-infrastructureconfiguration-instancemetadataoptions-httptokens
            '''
            result = self._values.get("http_tokens")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceMetadataOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnInfrastructureConfigurationPropsMixin.LoggingProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_logs": "s3Logs"},
    )
    class LoggingProperty:
        def __init__(
            self,
            *,
            s3_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInfrastructureConfigurationPropsMixin.S3LogsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Logging configuration defines where Image Builder uploads your logs.

            :param s3_logs: The Amazon S3 logging configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-infrastructureconfiguration-logging.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                logging_property = imagebuilder_mixins.CfnInfrastructureConfigurationPropsMixin.LoggingProperty(
                    s3_logs=imagebuilder_mixins.CfnInfrastructureConfigurationPropsMixin.S3LogsProperty(
                        s3_bucket_name="s3BucketName",
                        s3_key_prefix="s3KeyPrefix"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5725c4b3ecc329dce53380d11a5d22471b6e23740b298a6a3f9aab272a5bbad1)
                check_type(argname="argument s3_logs", value=s3_logs, expected_type=type_hints["s3_logs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_logs is not None:
                self._values["s3_logs"] = s3_logs

        @builtins.property
        def s3_logs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInfrastructureConfigurationPropsMixin.S3LogsProperty"]]:
            '''The Amazon S3 logging configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-infrastructureconfiguration-logging.html#cfn-imagebuilder-infrastructureconfiguration-logging-s3logs
            '''
            result = self._values.get("s3_logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInfrastructureConfigurationPropsMixin.S3LogsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnInfrastructureConfigurationPropsMixin.PlacementProperty",
        jsii_struct_bases=[],
        name_mapping={
            "availability_zone": "availabilityZone",
            "host_id": "hostId",
            "host_resource_group_arn": "hostResourceGroupArn",
            "tenancy": "tenancy",
        },
    )
    class PlacementProperty:
        def __init__(
            self,
            *,
            availability_zone: typing.Optional[builtins.str] = None,
            host_id: typing.Optional[builtins.str] = None,
            host_resource_group_arn: typing.Optional[builtins.str] = None,
            tenancy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''By default, EC2 instances run on shared tenancy hardware.

            This means that multiple AWS accounts might share the same physical hardware. When you use dedicated hardware, the physical server that hosts your instances is dedicated to your AWS account . Instance placement settings contain the details for the physical hardware where instances that Image Builder launches during image creation will run.

            :param availability_zone: The Availability Zone where your build and test instances will launch.
            :param host_id: The ID of the Dedicated Host on which build and test instances run. This only applies if ``tenancy`` is ``host`` . If you specify the host ID, you must not specify the resource group ARN. If you specify both, Image Builder returns an error.
            :param host_resource_group_arn: The Amazon Resource Name (ARN) of the host resource group in which to launch build and test instances. This only applies if ``tenancy`` is ``host`` . If you specify the resource group ARN, you must not specify the host ID. If you specify both, Image Builder returns an error.
            :param tenancy: The tenancy of the instance. An instance with a tenancy of ``dedicated`` runs on single-tenant hardware. An instance with a tenancy of ``host`` runs on a Dedicated Host. If tenancy is set to ``host`` , then you can optionally specify one target for placement – either host ID or host resource group ARN. If automatic placement is enabled for your host, and you don't specify any placement target, Amazon EC2 will try to find an available host for your build and test instances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-infrastructureconfiguration-placement.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                placement_property = imagebuilder_mixins.CfnInfrastructureConfigurationPropsMixin.PlacementProperty(
                    availability_zone="availabilityZone",
                    host_id="hostId",
                    host_resource_group_arn="hostResourceGroupArn",
                    tenancy="tenancy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fcb492305265ff21d45a7ef5795f6308db2b230c21864a7c8aaecdb6d2f26c5f)
                check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                check_type(argname="argument host_id", value=host_id, expected_type=type_hints["host_id"])
                check_type(argname="argument host_resource_group_arn", value=host_resource_group_arn, expected_type=type_hints["host_resource_group_arn"])
                check_type(argname="argument tenancy", value=tenancy, expected_type=type_hints["tenancy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if availability_zone is not None:
                self._values["availability_zone"] = availability_zone
            if host_id is not None:
                self._values["host_id"] = host_id
            if host_resource_group_arn is not None:
                self._values["host_resource_group_arn"] = host_resource_group_arn
            if tenancy is not None:
                self._values["tenancy"] = tenancy

        @builtins.property
        def availability_zone(self) -> typing.Optional[builtins.str]:
            '''The Availability Zone where your build and test instances will launch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-infrastructureconfiguration-placement.html#cfn-imagebuilder-infrastructureconfiguration-placement-availabilityzone
            '''
            result = self._values.get("availability_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def host_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the Dedicated Host on which build and test instances run.

            This only applies if ``tenancy`` is ``host`` . If you specify the host ID, you must not specify the resource group ARN. If you specify both, Image Builder returns an error.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-infrastructureconfiguration-placement.html#cfn-imagebuilder-infrastructureconfiguration-placement-hostid
            '''
            result = self._values.get("host_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def host_resource_group_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the host resource group in which to launch build and test instances.

            This only applies if ``tenancy`` is ``host`` . If you specify the resource group ARN, you must not specify the host ID. If you specify both, Image Builder returns an error.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-infrastructureconfiguration-placement.html#cfn-imagebuilder-infrastructureconfiguration-placement-hostresourcegrouparn
            '''
            result = self._values.get("host_resource_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tenancy(self) -> typing.Optional[builtins.str]:
            '''The tenancy of the instance.

            An instance with a tenancy of ``dedicated`` runs on single-tenant hardware. An instance with a tenancy of ``host`` runs on a Dedicated Host.

            If tenancy is set to ``host`` , then you can optionally specify one target for placement – either host ID or host resource group ARN. If automatic placement is enabled for your host, and you don't specify any placement target, Amazon EC2 will try to find an available host for your build and test instances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-infrastructureconfiguration-placement.html#cfn-imagebuilder-infrastructureconfiguration-placement-tenancy
            '''
            result = self._values.get("tenancy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PlacementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnInfrastructureConfigurationPropsMixin.S3LogsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "s3_bucket_name": "s3BucketName",
            "s3_key_prefix": "s3KeyPrefix",
        },
    )
    class S3LogsProperty:
        def __init__(
            self,
            *,
            s3_bucket_name: typing.Optional[builtins.str] = None,
            s3_key_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Amazon S3 logging configuration.

            :param s3_bucket_name: The S3 bucket in which to store the logs.
            :param s3_key_prefix: The Amazon S3 path to the bucket where the logs are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-infrastructureconfiguration-s3logs.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                s3_logs_property = imagebuilder_mixins.CfnInfrastructureConfigurationPropsMixin.S3LogsProperty(
                    s3_bucket_name="s3BucketName",
                    s3_key_prefix="s3KeyPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f71e3a3b862bab3d496b58bad48667d7a7ca7e8acd1dd90dfaf8e39b8092a084)
                check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
                check_type(argname="argument s3_key_prefix", value=s3_key_prefix, expected_type=type_hints["s3_key_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_bucket_name is not None:
                self._values["s3_bucket_name"] = s3_bucket_name
            if s3_key_prefix is not None:
                self._values["s3_key_prefix"] = s3_key_prefix

        @builtins.property
        def s3_bucket_name(self) -> typing.Optional[builtins.str]:
            '''The S3 bucket in which to store the logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-infrastructureconfiguration-s3logs.html#cfn-imagebuilder-infrastructureconfiguration-s3logs-s3bucketname
            '''
            result = self._values.get("s3_bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_key_prefix(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 path to the bucket where the logs are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-infrastructureconfiguration-s3logs.html#cfn-imagebuilder-infrastructureconfiguration-s3logs-s3keyprefix
            '''
            result = self._values.get("s3_key_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LogsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnLifecyclePolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "execution_role": "executionRole",
        "name": "name",
        "policy_details": "policyDetails",
        "resource_selection": "resourceSelection",
        "resource_type": "resourceType",
        "status": "status",
        "tags": "tags",
    },
)
class CfnLifecyclePolicyMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        execution_role: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        policy_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.PolicyDetailProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        resource_selection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.ResourceSelectionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        resource_type: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnLifecyclePolicyPropsMixin.

        :param description: Optional description for the lifecycle policy.
        :param execution_role: The name or Amazon Resource Name (ARN) for the IAM role you create that grants Image Builder access to run lifecycle actions.
        :param name: The name of the lifecycle policy to create.
        :param policy_details: Configuration details for the lifecycle policy rules.
        :param resource_selection: Selection criteria for the resources that the lifecycle policy applies to.
        :param resource_type: The type of Image Builder resource that the lifecycle policy applies to.
        :param status: Indicates whether the lifecycle policy resource is enabled.
        :param tags: Tags to apply to the lifecycle policy resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-lifecyclepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
            
            cfn_lifecycle_policy_mixin_props = imagebuilder_mixins.CfnLifecyclePolicyMixinProps(
                description="description",
                execution_role="executionRole",
                name="name",
                policy_details=[imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.PolicyDetailProperty(
                    action=imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.ActionProperty(
                        include_resources=imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.IncludeResourcesProperty(
                            amis=False,
                            containers=False,
                            snapshots=False
                        ),
                        type="type"
                    ),
                    exclusion_rules=imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.ExclusionRulesProperty(
                        amis=imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.AmiExclusionRulesProperty(
                            is_public=False,
                            last_launched=imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.LastLaunchedProperty(
                                unit="unit",
                                value=123
                            ),
                            regions=["regions"],
                            shared_accounts=["sharedAccounts"],
                            tag_map={
                                "tag_map_key": "tagMap"
                            }
                        ),
                        tag_map={
                            "tag_map_key": "tagMap"
                        }
                    ),
                    filter=imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.FilterProperty(
                        retain_at_least=123,
                        type="type",
                        unit="unit",
                        value=123
                    )
                )],
                resource_selection=imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.ResourceSelectionProperty(
                    recipes=[imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.RecipeSelectionProperty(
                        name="name",
                        semantic_version="semanticVersion"
                    )],
                    tag_map={
                        "tag_map_key": "tagMap"
                    }
                ),
                resource_type="resourceType",
                status="status",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__015d17620a4eaae526ba4c8dac69e0d8d21add3a2301acd4255ae7c9827da202)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy_details", value=policy_details, expected_type=type_hints["policy_details"])
            check_type(argname="argument resource_selection", value=resource_selection, expected_type=type_hints["resource_selection"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if execution_role is not None:
            self._values["execution_role"] = execution_role
        if name is not None:
            self._values["name"] = name
        if policy_details is not None:
            self._values["policy_details"] = policy_details
        if resource_selection is not None:
            self._values["resource_selection"] = resource_selection
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional description for the lifecycle policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-lifecyclepolicy.html#cfn-imagebuilder-lifecyclepolicy-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_role(self) -> typing.Optional[builtins.str]:
        '''The name or Amazon Resource Name (ARN) for the IAM role you create that grants Image Builder access to run lifecycle actions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-lifecyclepolicy.html#cfn-imagebuilder-lifecyclepolicy-executionrole
        '''
        result = self._values.get("execution_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the lifecycle policy to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-lifecyclepolicy.html#cfn-imagebuilder-lifecyclepolicy-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_details(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.PolicyDetailProperty"]]]]:
        '''Configuration details for the lifecycle policy rules.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-lifecyclepolicy.html#cfn-imagebuilder-lifecyclepolicy-policydetails
        '''
        result = self._values.get("policy_details")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.PolicyDetailProperty"]]]], result)

    @builtins.property
    def resource_selection(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.ResourceSelectionProperty"]]:
        '''Selection criteria for the resources that the lifecycle policy applies to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-lifecyclepolicy.html#cfn-imagebuilder-lifecyclepolicy-resourceselection
        '''
        result = self._values.get("resource_selection")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.ResourceSelectionProperty"]], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''The type of Image Builder resource that the lifecycle policy applies to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-lifecyclepolicy.html#cfn-imagebuilder-lifecyclepolicy-resourcetype
        '''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Indicates whether the lifecycle policy resource is enabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-lifecyclepolicy.html#cfn-imagebuilder-lifecyclepolicy-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags to apply to the lifecycle policy resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-lifecyclepolicy.html#cfn-imagebuilder-lifecyclepolicy-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLifecyclePolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLifecyclePolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnLifecyclePolicyPropsMixin",
):
    '''Create a lifecycle policy resource.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-lifecyclepolicy.html
    :cloudformationResource: AWS::ImageBuilder::LifecyclePolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
        
        cfn_lifecycle_policy_props_mixin = imagebuilder_mixins.CfnLifecyclePolicyPropsMixin(imagebuilder_mixins.CfnLifecyclePolicyMixinProps(
            description="description",
            execution_role="executionRole",
            name="name",
            policy_details=[imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.PolicyDetailProperty(
                action=imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.ActionProperty(
                    include_resources=imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.IncludeResourcesProperty(
                        amis=False,
                        containers=False,
                        snapshots=False
                    ),
                    type="type"
                ),
                exclusion_rules=imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.ExclusionRulesProperty(
                    amis=imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.AmiExclusionRulesProperty(
                        is_public=False,
                        last_launched=imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.LastLaunchedProperty(
                            unit="unit",
                            value=123
                        ),
                        regions=["regions"],
                        shared_accounts=["sharedAccounts"],
                        tag_map={
                            "tag_map_key": "tagMap"
                        }
                    ),
                    tag_map={
                        "tag_map_key": "tagMap"
                    }
                ),
                filter=imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.FilterProperty(
                    retain_at_least=123,
                    type="type",
                    unit="unit",
                    value=123
                )
            )],
            resource_selection=imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.ResourceSelectionProperty(
                recipes=[imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.RecipeSelectionProperty(
                    name="name",
                    semantic_version="semanticVersion"
                )],
                tag_map={
                    "tag_map_key": "tagMap"
                }
            ),
            resource_type="resourceType",
            status="status",
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLifecyclePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ImageBuilder::LifecyclePolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__361f4940d98fc0b13cb6be371417805028f9c2b3693ab348cf803320abfda867)
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
            type_hints = typing.get_type_hints(_typecheckingstub__957936708cadcb27c2b64b529d5698ce55ee769edb50c332f4e4373b92876235)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69cb6c8c1895aea3ff899cc56f815d951b0e8a87a24a9a2304a8c86515ebf293)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLifecyclePolicyMixinProps:
        return typing.cast(CfnLifecyclePolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnLifecyclePolicyPropsMixin.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={"include_resources": "includeResources", "type": "type"},
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            include_resources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.IncludeResourcesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains selection criteria for the lifecycle policy.

            :param include_resources: Specifies the resources that the lifecycle policy applies to.
            :param type: Specifies the lifecycle action to take.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                action_property = imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.ActionProperty(
                    include_resources=imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.IncludeResourcesProperty(
                        amis=False,
                        containers=False,
                        snapshots=False
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3e50bcee9bf47ce2810780205fe4a7cd1bf412f46da3d649b7f3b79c0c442ec4)
                check_type(argname="argument include_resources", value=include_resources, expected_type=type_hints["include_resources"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if include_resources is not None:
                self._values["include_resources"] = include_resources
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def include_resources(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.IncludeResourcesProperty"]]:
            '''Specifies the resources that the lifecycle policy applies to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-action.html#cfn-imagebuilder-lifecyclepolicy-action-includeresources
            '''
            result = self._values.get("include_resources")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.IncludeResourcesProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Specifies the lifecycle action to take.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-action.html#cfn-imagebuilder-lifecyclepolicy-action-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnLifecyclePolicyPropsMixin.AmiExclusionRulesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "is_public": "isPublic",
            "last_launched": "lastLaunched",
            "regions": "regions",
            "shared_accounts": "sharedAccounts",
            "tag_map": "tagMap",
        },
    )
    class AmiExclusionRulesProperty:
        def __init__(
            self,
            *,
            is_public: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            last_launched: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.LastLaunchedProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            regions: typing.Optional[typing.Sequence[builtins.str]] = None,
            shared_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
            tag_map: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Defines criteria for AMIs that are excluded from lifecycle actions.

            :param is_public: Configures whether public AMIs are excluded from the lifecycle action.
            :param last_launched: Specifies configuration details for Image Builder to exclude the most recent resources from lifecycle actions.
            :param regions: Configures AWS Region s that are excluded from the lifecycle action.
            :param shared_accounts: Specifies AWS account s whose resources are excluded from the lifecycle action.
            :param tag_map: Lists tags that should be excluded from lifecycle actions for the AMIs that have them.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-amiexclusionrules.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                ami_exclusion_rules_property = imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.AmiExclusionRulesProperty(
                    is_public=False,
                    last_launched=imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.LastLaunchedProperty(
                        unit="unit",
                        value=123
                    ),
                    regions=["regions"],
                    shared_accounts=["sharedAccounts"],
                    tag_map={
                        "tag_map_key": "tagMap"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8293546a98390c3d67c314a430ea0d2b19b0c0f67a45c99996c7afa3e6fbc51c)
                check_type(argname="argument is_public", value=is_public, expected_type=type_hints["is_public"])
                check_type(argname="argument last_launched", value=last_launched, expected_type=type_hints["last_launched"])
                check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
                check_type(argname="argument shared_accounts", value=shared_accounts, expected_type=type_hints["shared_accounts"])
                check_type(argname="argument tag_map", value=tag_map, expected_type=type_hints["tag_map"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_public is not None:
                self._values["is_public"] = is_public
            if last_launched is not None:
                self._values["last_launched"] = last_launched
            if regions is not None:
                self._values["regions"] = regions
            if shared_accounts is not None:
                self._values["shared_accounts"] = shared_accounts
            if tag_map is not None:
                self._values["tag_map"] = tag_map

        @builtins.property
        def is_public(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Configures whether public AMIs are excluded from the lifecycle action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-amiexclusionrules.html#cfn-imagebuilder-lifecyclepolicy-amiexclusionrules-ispublic
            '''
            result = self._values.get("is_public")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def last_launched(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.LastLaunchedProperty"]]:
            '''Specifies configuration details for Image Builder to exclude the most recent resources from lifecycle actions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-amiexclusionrules.html#cfn-imagebuilder-lifecyclepolicy-amiexclusionrules-lastlaunched
            '''
            result = self._values.get("last_launched")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.LastLaunchedProperty"]], result)

        @builtins.property
        def regions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Configures AWS Region s that are excluded from the lifecycle action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-amiexclusionrules.html#cfn-imagebuilder-lifecyclepolicy-amiexclusionrules-regions
            '''
            result = self._values.get("regions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def shared_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies AWS account s whose resources are excluded from the lifecycle action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-amiexclusionrules.html#cfn-imagebuilder-lifecyclepolicy-amiexclusionrules-sharedaccounts
            '''
            result = self._values.get("shared_accounts")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def tag_map(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Lists tags that should be excluded from lifecycle actions for the AMIs that have them.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-amiexclusionrules.html#cfn-imagebuilder-lifecyclepolicy-amiexclusionrules-tagmap
            '''
            result = self._values.get("tag_map")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AmiExclusionRulesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnLifecyclePolicyPropsMixin.ExclusionRulesProperty",
        jsii_struct_bases=[],
        name_mapping={"amis": "amis", "tag_map": "tagMap"},
    )
    class ExclusionRulesProperty:
        def __init__(
            self,
            *,
            amis: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.AmiExclusionRulesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            tag_map: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Specifies resources that lifecycle policy actions should not apply to.

            :param amis: Lists configuration values that apply to AMIs that Image Builder should exclude from the lifecycle action.
            :param tag_map: Contains a list of tags that Image Builder uses to skip lifecycle actions for Image Builder image resources that have them.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-exclusionrules.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                exclusion_rules_property = imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.ExclusionRulesProperty(
                    amis=imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.AmiExclusionRulesProperty(
                        is_public=False,
                        last_launched=imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.LastLaunchedProperty(
                            unit="unit",
                            value=123
                        ),
                        regions=["regions"],
                        shared_accounts=["sharedAccounts"],
                        tag_map={
                            "tag_map_key": "tagMap"
                        }
                    ),
                    tag_map={
                        "tag_map_key": "tagMap"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9a8d550560a69596c3694eab04b6996ac014bcb79c28fafdd42a2825a669c3a3)
                check_type(argname="argument amis", value=amis, expected_type=type_hints["amis"])
                check_type(argname="argument tag_map", value=tag_map, expected_type=type_hints["tag_map"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if amis is not None:
                self._values["amis"] = amis
            if tag_map is not None:
                self._values["tag_map"] = tag_map

        @builtins.property
        def amis(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.AmiExclusionRulesProperty"]]:
            '''Lists configuration values that apply to AMIs that Image Builder should exclude from the lifecycle action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-exclusionrules.html#cfn-imagebuilder-lifecyclepolicy-exclusionrules-amis
            '''
            result = self._values.get("amis")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.AmiExclusionRulesProperty"]], result)

        @builtins.property
        def tag_map(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Contains a list of tags that Image Builder uses to skip lifecycle actions for Image Builder image resources that have them.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-exclusionrules.html#cfn-imagebuilder-lifecyclepolicy-exclusionrules-tagmap
            '''
            result = self._values.get("tag_map")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExclusionRulesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnLifecyclePolicyPropsMixin.FilterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "retain_at_least": "retainAtLeast",
            "type": "type",
            "unit": "unit",
            "value": "value",
        },
    )
    class FilterProperty:
        def __init__(
            self,
            *,
            retain_at_least: typing.Optional[jsii.Number] = None,
            type: typing.Optional[builtins.str] = None,
            unit: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Defines filters that the lifecycle policy uses to determine impacted resource.

            :param retain_at_least: For age-based filters, this is the number of resources to keep on hand after the lifecycle ``DELETE`` action is applied. Impacted resources are only deleted if you have more than this number of resources. If you have fewer resources than this number, the impacted resource is not deleted.
            :param type: Filter resources based on either ``age`` or ``count`` .
            :param unit: Defines the unit of time that the lifecycle policy uses to determine impacted resources. This is required for age-based rules.
            :param value: The number of units for the time period or for the count. For example, a value of ``6`` might refer to six months or six AMIs. .. epigraph:: For count-based filters, this value represents the minimum number of resources to keep on hand. If you have fewer resources than this number, the resource is excluded from lifecycle actions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-filter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                filter_property = imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.FilterProperty(
                    retain_at_least=123,
                    type="type",
                    unit="unit",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c0e1435caaa8311a027e4feab38468ad39b2d9a15a9a2c0fbf09740a2491f42b)
                check_type(argname="argument retain_at_least", value=retain_at_least, expected_type=type_hints["retain_at_least"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if retain_at_least is not None:
                self._values["retain_at_least"] = retain_at_least
            if type is not None:
                self._values["type"] = type
            if unit is not None:
                self._values["unit"] = unit
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def retain_at_least(self) -> typing.Optional[jsii.Number]:
            '''For age-based filters, this is the number of resources to keep on hand after the lifecycle ``DELETE`` action is applied.

            Impacted resources are only deleted if you have more than this number of resources. If you have fewer resources than this number, the impacted resource is not deleted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-filter.html#cfn-imagebuilder-lifecyclepolicy-filter-retainatleast
            '''
            result = self._values.get("retain_at_least")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Filter resources based on either ``age`` or ``count`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-filter.html#cfn-imagebuilder-lifecyclepolicy-filter-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''Defines the unit of time that the lifecycle policy uses to determine impacted resources.

            This is required for age-based rules.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-filter.html#cfn-imagebuilder-lifecyclepolicy-filter-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''The number of units for the time period or for the count.

            For example, a value of ``6`` might refer to six months or six AMIs.
            .. epigraph::

               For count-based filters, this value represents the minimum number of resources to keep on hand. If you have fewer resources than this number, the resource is excluded from lifecycle actions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-filter.html#cfn-imagebuilder-lifecyclepolicy-filter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnLifecyclePolicyPropsMixin.IncludeResourcesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "amis": "amis",
            "containers": "containers",
            "snapshots": "snapshots",
        },
    )
    class IncludeResourcesProperty:
        def __init__(
            self,
            *,
            amis: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            containers: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            snapshots: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Specifies how the lifecycle policy should apply actions to selected resources.

            :param amis: Specifies whether the lifecycle action should apply to distributed AMIs.
            :param containers: Specifies whether the lifecycle action should apply to distributed containers.
            :param snapshots: Specifies whether the lifecycle action should apply to snapshots associated with distributed AMIs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-includeresources.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                include_resources_property = imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.IncludeResourcesProperty(
                    amis=False,
                    containers=False,
                    snapshots=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c2550652a0c4430ff9fa93688d96f09a134f3a3e900e7050af8f69674f94267c)
                check_type(argname="argument amis", value=amis, expected_type=type_hints["amis"])
                check_type(argname="argument containers", value=containers, expected_type=type_hints["containers"])
                check_type(argname="argument snapshots", value=snapshots, expected_type=type_hints["snapshots"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if amis is not None:
                self._values["amis"] = amis
            if containers is not None:
                self._values["containers"] = containers
            if snapshots is not None:
                self._values["snapshots"] = snapshots

        @builtins.property
        def amis(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the lifecycle action should apply to distributed AMIs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-includeresources.html#cfn-imagebuilder-lifecyclepolicy-includeresources-amis
            '''
            result = self._values.get("amis")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def containers(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the lifecycle action should apply to distributed containers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-includeresources.html#cfn-imagebuilder-lifecyclepolicy-includeresources-containers
            '''
            result = self._values.get("containers")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def snapshots(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the lifecycle action should apply to snapshots associated with distributed AMIs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-includeresources.html#cfn-imagebuilder-lifecyclepolicy-includeresources-snapshots
            '''
            result = self._values.get("snapshots")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IncludeResourcesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnLifecyclePolicyPropsMixin.LastLaunchedProperty",
        jsii_struct_bases=[],
        name_mapping={"unit": "unit", "value": "value"},
    )
    class LastLaunchedProperty:
        def __init__(
            self,
            *,
            unit: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Defines criteria to exclude AMIs from lifecycle actions based on the last time they were used to launch an instance.

            :param unit: Defines the unit of time that the lifecycle policy uses to calculate elapsed time since the last instance launched from the AMI. For example: days, weeks, months, or years.
            :param value: The integer number of units for the time period. For example ``6`` (months).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-lastlaunched.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                last_launched_property = imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.LastLaunchedProperty(
                    unit="unit",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9ca748e7952ccfcbea63270107505b04c46577a306466d4a5861ea8f28f0c459)
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if unit is not None:
                self._values["unit"] = unit
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''Defines the unit of time that the lifecycle policy uses to calculate elapsed time since the last instance launched from the AMI.

            For example: days, weeks, months, or years.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-lastlaunched.html#cfn-imagebuilder-lifecyclepolicy-lastlaunched-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''The integer number of units for the time period.

            For example ``6`` (months).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-lastlaunched.html#cfn-imagebuilder-lifecyclepolicy-lastlaunched-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LastLaunchedProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnLifecyclePolicyPropsMixin.PolicyDetailProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "exclusion_rules": "exclusionRules",
            "filter": "filter",
        },
    )
    class PolicyDetailProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.ActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            exclusion_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.ExclusionRulesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.FilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration details for a lifecycle policy resource.

            :param action: Configuration details for the policy action.
            :param exclusion_rules: Additional rules to specify resources that should be exempt from policy actions.
            :param filter: Specifies the resources that the lifecycle policy applies to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-policydetail.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                policy_detail_property = imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.PolicyDetailProperty(
                    action=imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.ActionProperty(
                        include_resources=imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.IncludeResourcesProperty(
                            amis=False,
                            containers=False,
                            snapshots=False
                        ),
                        type="type"
                    ),
                    exclusion_rules=imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.ExclusionRulesProperty(
                        amis=imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.AmiExclusionRulesProperty(
                            is_public=False,
                            last_launched=imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.LastLaunchedProperty(
                                unit="unit",
                                value=123
                            ),
                            regions=["regions"],
                            shared_accounts=["sharedAccounts"],
                            tag_map={
                                "tag_map_key": "tagMap"
                            }
                        ),
                        tag_map={
                            "tag_map_key": "tagMap"
                        }
                    ),
                    filter=imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.FilterProperty(
                        retain_at_least=123,
                        type="type",
                        unit="unit",
                        value=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__72eed8acb87233ff7a859e84c828f5c50a5aabfe1e00826bb4746f49ebb117d2)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument exclusion_rules", value=exclusion_rules, expected_type=type_hints["exclusion_rules"])
                check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if exclusion_rules is not None:
                self._values["exclusion_rules"] = exclusion_rules
            if filter is not None:
                self._values["filter"] = filter

        @builtins.property
        def action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.ActionProperty"]]:
            '''Configuration details for the policy action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-policydetail.html#cfn-imagebuilder-lifecyclepolicy-policydetail-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.ActionProperty"]], result)

        @builtins.property
        def exclusion_rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.ExclusionRulesProperty"]]:
            '''Additional rules to specify resources that should be exempt from policy actions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-policydetail.html#cfn-imagebuilder-lifecyclepolicy-policydetail-exclusionrules
            '''
            result = self._values.get("exclusion_rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.ExclusionRulesProperty"]], result)

        @builtins.property
        def filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.FilterProperty"]]:
            '''Specifies the resources that the lifecycle policy applies to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-policydetail.html#cfn-imagebuilder-lifecyclepolicy-policydetail-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.FilterProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyDetailProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnLifecyclePolicyPropsMixin.RecipeSelectionProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "semantic_version": "semanticVersion"},
    )
    class RecipeSelectionProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            semantic_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an Image Builder recipe that the lifecycle policy uses for resource selection.

            :param name: The name of an Image Builder recipe that the lifecycle policy uses for resource selection.
            :param semantic_version: The version of the Image Builder recipe specified by the ``name`` field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-recipeselection.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                recipe_selection_property = imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.RecipeSelectionProperty(
                    name="name",
                    semantic_version="semanticVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d5f52a2498b86a32736569c9fceffae6db083e09bf192cdd418e257600677d7d)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument semantic_version", value=semantic_version, expected_type=type_hints["semantic_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if semantic_version is not None:
                self._values["semantic_version"] = semantic_version

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of an Image Builder recipe that the lifecycle policy uses for resource selection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-recipeselection.html#cfn-imagebuilder-lifecyclepolicy-recipeselection-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def semantic_version(self) -> typing.Optional[builtins.str]:
            '''The version of the Image Builder recipe specified by the ``name`` field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-recipeselection.html#cfn-imagebuilder-lifecyclepolicy-recipeselection-semanticversion
            '''
            result = self._values.get("semantic_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecipeSelectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnLifecyclePolicyPropsMixin.ResourceSelectionProperty",
        jsii_struct_bases=[],
        name_mapping={"recipes": "recipes", "tag_map": "tagMap"},
    )
    class ResourceSelectionProperty:
        def __init__(
            self,
            *,
            recipes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLifecyclePolicyPropsMixin.RecipeSelectionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            tag_map: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Resource selection criteria for the lifecycle policy.

            :param recipes: A list of recipes that are used as selection criteria for the output images that the lifecycle policy applies to.
            :param tag_map: A list of tags that are used as selection criteria for the Image Builder image resources that the lifecycle policy applies to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-resourceselection.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                resource_selection_property = imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.ResourceSelectionProperty(
                    recipes=[imagebuilder_mixins.CfnLifecyclePolicyPropsMixin.RecipeSelectionProperty(
                        name="name",
                        semantic_version="semanticVersion"
                    )],
                    tag_map={
                        "tag_map_key": "tagMap"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c37b796085843596595c4daa8a7962359a26f6a09c61834692e237940188610d)
                check_type(argname="argument recipes", value=recipes, expected_type=type_hints["recipes"])
                check_type(argname="argument tag_map", value=tag_map, expected_type=type_hints["tag_map"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if recipes is not None:
                self._values["recipes"] = recipes
            if tag_map is not None:
                self._values["tag_map"] = tag_map

        @builtins.property
        def recipes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.RecipeSelectionProperty"]]]]:
            '''A list of recipes that are used as selection criteria for the output images that the lifecycle policy applies to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-resourceselection.html#cfn-imagebuilder-lifecyclepolicy-resourceselection-recipes
            '''
            result = self._values.get("recipes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLifecyclePolicyPropsMixin.RecipeSelectionProperty"]]]], result)

        @builtins.property
        def tag_map(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''A list of tags that are used as selection criteria for the Image Builder image resources that the lifecycle policy applies to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-lifecyclepolicy-resourceselection.html#cfn-imagebuilder-lifecyclepolicy-resourceselection-tagmap
            '''
            result = self._values.get("tag_map")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceSelectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnWorkflowMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "change_description": "changeDescription",
        "data": "data",
        "description": "description",
        "kms_key_id": "kmsKeyId",
        "name": "name",
        "tags": "tags",
        "type": "type",
        "uri": "uri",
        "version": "version",
    },
)
class CfnWorkflowMixinProps:
    def __init__(
        self,
        *,
        change_description: typing.Optional[builtins.str] = None,
        data: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        type: typing.Optional[builtins.str] = None,
        uri: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnWorkflowPropsMixin.

        :param change_description: Describes what change has been made in this version of the workflow, or what makes this version different from other versions of the workflow.
        :param data: Contains the UTF-8 encoded YAML document content for the workflow. Alternatively, you can specify the ``uri`` of a YAML document file stored in Amazon S3. However, you cannot specify both properties.
        :param description: Describes the workflow.
        :param kms_key_id: The Amazon Resource Name (ARN) that uniquely identifies the KMS key used to encrypt this workflow resource. This can be either the Key ARN or the Alias ARN. For more information, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id-key-ARN>`_ in the *AWS Key Management Service Developer Guide* .
        :param name: The name of the workflow to create.
        :param tags: Tags that apply to the workflow resource.
        :param type: The phase in the image build process for which the workflow resource is responsible.
        :param uri: The ``uri`` of a YAML component document file. This must be an S3 URL ( ``s3://bucket/key`` ), and the requester must have permission to access the S3 bucket it points to. If you use Amazon S3, you can specify component content up to your service quota. Alternatively, you can specify the YAML document inline, using the component ``data`` property. You cannot specify both properties.
        :param version: The semantic version of this workflow resource. The semantic version syntax adheres to the following rules. .. epigraph:: The semantic version has four nodes: ../. You can assign values for the first three, and can filter on all of them. *Assignment:* For the first three nodes you can assign any positive integer value, including zero, with an upper limit of 2^30-1, or 1073741823 for each node. Image Builder automatically assigns the build number to the fourth node. *Patterns:* You can use any numeric pattern that adheres to the assignment requirements for the nodes that you can assign. For example, you might choose a software version pattern, such as 1.0.0, or a date, such as 2021.01.01.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-workflow.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
            
            cfn_workflow_mixin_props = imagebuilder_mixins.CfnWorkflowMixinProps(
                change_description="changeDescription",
                data="data",
                description="description",
                kms_key_id="kmsKeyId",
                name="name",
                tags={
                    "tags_key": "tags"
                },
                type="type",
                uri="uri",
                version="version"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef6fded30405ecee20dab2e2f87530e7d5e1e3d5051066348817acad1ce88fae)
            check_type(argname="argument change_description", value=change_description, expected_type=type_hints["change_description"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if change_description is not None:
            self._values["change_description"] = change_description
        if data is not None:
            self._values["data"] = data
        if description is not None:
            self._values["description"] = description
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type
        if uri is not None:
            self._values["uri"] = uri
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def change_description(self) -> typing.Optional[builtins.str]:
        '''Describes what change has been made in this version of the workflow, or what makes this version different from other versions of the workflow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-workflow.html#cfn-imagebuilder-workflow-changedescription
        '''
        result = self._values.get("change_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data(self) -> typing.Optional[builtins.str]:
        '''Contains the UTF-8 encoded YAML document content for the workflow.

        Alternatively, you can specify the ``uri`` of a YAML document file stored in Amazon S3. However, you cannot specify both properties.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-workflow.html#cfn-imagebuilder-workflow-data
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Describes the workflow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-workflow.html#cfn-imagebuilder-workflow-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) that uniquely identifies the KMS key used to encrypt this workflow resource.

        This can be either the Key ARN or the Alias ARN. For more information, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id-key-ARN>`_ in the *AWS Key Management Service Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-workflow.html#cfn-imagebuilder-workflow-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the workflow to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-workflow.html#cfn-imagebuilder-workflow-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags that apply to the workflow resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-workflow.html#cfn-imagebuilder-workflow-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The phase in the image build process for which the workflow resource is responsible.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-workflow.html#cfn-imagebuilder-workflow-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''The ``uri`` of a YAML component document file.

        This must be an S3 URL ( ``s3://bucket/key`` ), and the requester must have permission to access the S3 bucket it points to. If you use Amazon S3, you can specify component content up to your service quota.

        Alternatively, you can specify the YAML document inline, using the component ``data`` property. You cannot specify both properties.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-workflow.html#cfn-imagebuilder-workflow-uri
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The semantic version of this workflow resource. The semantic version syntax adheres to the following rules.

        .. epigraph::

           The semantic version has four nodes: ../. You can assign values for the first three, and can filter on all of them.

           *Assignment:* For the first three nodes you can assign any positive integer value, including zero, with an upper limit of 2^30-1, or 1073741823 for each node. Image Builder automatically assigns the build number to the fourth node.

           *Patterns:* You can use any numeric pattern that adheres to the assignment requirements for the nodes that you can assign. For example, you might choose a software version pattern, such as 1.0.0, or a date, such as 2021.01.01.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-workflow.html#cfn-imagebuilder-workflow-version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkflowMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWorkflowPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnWorkflowPropsMixin",
):
    '''Create a new workflow or a new version of an existing workflow.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-imagebuilder-workflow.html
    :cloudformationResource: AWS::ImageBuilder::Workflow
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
        
        cfn_workflow_props_mixin = imagebuilder_mixins.CfnWorkflowPropsMixin(imagebuilder_mixins.CfnWorkflowMixinProps(
            change_description="changeDescription",
            data="data",
            description="description",
            kms_key_id="kmsKeyId",
            name="name",
            tags={
                "tags_key": "tags"
            },
            type="type",
            uri="uri",
            version="version"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnWorkflowMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ImageBuilder::Workflow``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a42aa86483eac9f8b2dfd70f756e35abc34e2f71a20964257fce2672bbfd4bee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9d9c15569f55912b2c5cbaf1ddcf4fdb68dba454ad5590f16df44fc6a30d7b8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46dc11b2640a711f76862077da0c86d96790f6e76ab454d62a5ea1b1eb100d58)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWorkflowMixinProps:
        return typing.cast(CfnWorkflowMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_imagebuilder.mixins.CfnWorkflowPropsMixin.LatestVersionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "major": "major",
            "minor": "minor",
            "patch": "patch",
        },
    )
    class LatestVersionProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            major: typing.Optional[builtins.str] = None,
            minor: typing.Optional[builtins.str] = None,
            patch: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The latest version references of the workflow.

            :param arn: The Amazon Resource Name (ARN) of the workflow resource.
            :param major: The latest version ARN of the created workflow, with the same major version.
            :param minor: The latest version ARN of the created workflow, with the same minor version.
            :param patch: The latest version ARN of the created workflow, with the same patch version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-workflow-latestversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_imagebuilder import mixins as imagebuilder_mixins
                
                latest_version_property = imagebuilder_mixins.CfnWorkflowPropsMixin.LatestVersionProperty(
                    arn="arn",
                    major="major",
                    minor="minor",
                    patch="patch"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6ed7ec9c106a806c59511c7d2234aa615766bee6f3c7f62e12aa10c8eb27d021)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument major", value=major, expected_type=type_hints["major"])
                check_type(argname="argument minor", value=minor, expected_type=type_hints["minor"])
                check_type(argname="argument patch", value=patch, expected_type=type_hints["patch"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if major is not None:
                self._values["major"] = major
            if minor is not None:
                self._values["minor"] = minor
            if patch is not None:
                self._values["patch"] = patch

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the workflow resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-workflow-latestversion.html#cfn-imagebuilder-workflow-latestversion-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def major(self) -> typing.Optional[builtins.str]:
            '''The latest version ARN of the created workflow, with the same major version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-workflow-latestversion.html#cfn-imagebuilder-workflow-latestversion-major
            '''
            result = self._values.get("major")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def minor(self) -> typing.Optional[builtins.str]:
            '''The latest version ARN of the created workflow, with the same minor version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-workflow-latestversion.html#cfn-imagebuilder-workflow-latestversion-minor
            '''
            result = self._values.get("minor")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def patch(self) -> typing.Optional[builtins.str]:
            '''The latest version ARN of the created workflow, with the same patch version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-imagebuilder-workflow-latestversion.html#cfn-imagebuilder-workflow-latestversion-patch
            '''
            result = self._values.get("patch")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LatestVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnComponentMixinProps",
    "CfnComponentPropsMixin",
    "CfnContainerRecipeMixinProps",
    "CfnContainerRecipePropsMixin",
    "CfnDistributionConfigurationMixinProps",
    "CfnDistributionConfigurationPropsMixin",
    "CfnImageMixinProps",
    "CfnImagePipelineMixinProps",
    "CfnImagePipelinePropsMixin",
    "CfnImagePropsMixin",
    "CfnImageRecipeMixinProps",
    "CfnImageRecipePropsMixin",
    "CfnInfrastructureConfigurationMixinProps",
    "CfnInfrastructureConfigurationPropsMixin",
    "CfnLifecyclePolicyMixinProps",
    "CfnLifecyclePolicyPropsMixin",
    "CfnWorkflowMixinProps",
    "CfnWorkflowPropsMixin",
]

publication.publish()

def _typecheckingstub__fbd742a0a2b3f62fc52804adac37346d59927c582d59534d8f5fbf63d957eeeb(
    *,
    change_description: typing.Optional[builtins.str] = None,
    data: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    platform: typing.Optional[builtins.str] = None,
    supported_os_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    uri: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60231d7f5888d03666bdb3a335a3eb60f9275631560fcc0ed71af4b8e8ba5012(
    props: typing.Union[CfnComponentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bdf603cc6909a72de9be1f0432018d3150a4159030d3235c6a3a869b7f6b494(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e35fba1b2f90fac495ecbdc43876485e39852939f10763327703c0612c02d0c3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbd8333bbfddaa60f3ce110cd311442d47e7ef04ce8d5633414fa74acfacb857(
    *,
    arn: typing.Optional[builtins.str] = None,
    major: typing.Optional[builtins.str] = None,
    minor: typing.Optional[builtins.str] = None,
    patch: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb847caa035aac599de42b693db87703e24afb291316622ba170faf93af35552(
    *,
    components: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerRecipePropsMixin.ComponentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    container_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    dockerfile_template_data: typing.Optional[builtins.str] = None,
    dockerfile_template_uri: typing.Optional[builtins.str] = None,
    image_os_version_override: typing.Optional[builtins.str] = None,
    instance_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerRecipePropsMixin.InstanceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    parent_image: typing.Optional[builtins.str] = None,
    platform_override: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    target_repository: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerRecipePropsMixin.TargetContainerRepositoryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    version: typing.Optional[builtins.str] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9bdacb971719c6eb23ce759ee448bfac400e6d55f35c67726be642d982f24a4(
    props: typing.Union[CfnContainerRecipeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84111cf6fdb84022f94e69a0780b925ce8249842ec710ebcb53679a8b2e65b82(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__332fd52633ffd8eae8424c70dafb0b6258e353999523357b635b61afc465186b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__305fd1216bc344263315e22c2363af13b5338719e435fbc18232574075d7ed18(
    *,
    component_arn: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerRecipePropsMixin.ComponentParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f49826fb7d32cb4b27e303ca608466b0c67057e0f5b00034eb6ef4fd6a1b713(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9cd28b75ff4890d493041602d0d795edacc4e0a7f4755b31e68ac5c19096202(
    *,
    delete_on_termination: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    iops: typing.Optional[jsii.Number] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    snapshot_id: typing.Optional[builtins.str] = None,
    throughput: typing.Optional[jsii.Number] = None,
    volume_size: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf06f10e08ce3e71d700dd051246985c2819b35d4dafaeb962d460100c9582b8(
    *,
    device_name: typing.Optional[builtins.str] = None,
    ebs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerRecipePropsMixin.EbsInstanceBlockDeviceSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    no_device: typing.Optional[builtins.str] = None,
    virtual_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2544d6afb790471e477d386eec39fb0b051308e21e08b6e281f402a662fa48d(
    *,
    block_device_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerRecipePropsMixin.InstanceBlockDeviceMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    image: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8908054bb81c05fa34d32d72af4b393061d9e70dae351d1064ec90299eabcd2b(
    *,
    arn: typing.Optional[builtins.str] = None,
    major: typing.Optional[builtins.str] = None,
    minor: typing.Optional[builtins.str] = None,
    patch: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a11d0a86c7bf94dae19bc1e958caf487349d8272b06bf288512007c7d508d34(
    *,
    repository_name: typing.Optional[builtins.str] = None,
    service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a343519e497d7ac5b5c113d0bc8760207a24cd629f687d0f119c3c117e689048(
    *,
    description: typing.Optional[builtins.str] = None,
    distributions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDistributionConfigurationPropsMixin.DistributionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__931511f93eb221d393140d26e63c9cb8ef03da9d60a13afd49d00b11fdf2d511(
    props: typing.Union[CfnDistributionConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__176c4d269f0ca75453856aa6011e2f007d5f35ba8a16918d8692468b3efff454(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36365b3bc852b3084790bf3dfaa791cb2ec291c416e6c80e765332abb0565895(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bff2af02862e582d91f05198f5dd6e059c900122b200f836f459723f32fc904b(
    *,
    ami_distribution_configuration: typing.Any = None,
    container_distribution_configuration: typing.Any = None,
    fast_launch_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDistributionConfigurationPropsMixin.FastLaunchConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    launch_template_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDistributionConfigurationPropsMixin.LaunchTemplateConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    license_configuration_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    ssm_parameter_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDistributionConfigurationPropsMixin.SsmParameterConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d4e0cd215be1dd530816ab499c882bdbe68e22922053d767a9a6f7379755d77(
    *,
    account_id: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    launch_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDistributionConfigurationPropsMixin.FastLaunchLaunchTemplateSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_parallel_launches: typing.Optional[jsii.Number] = None,
    snapshot_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDistributionConfigurationPropsMixin.FastLaunchSnapshotConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1294d8fb286a1c21dac84af00709b9ca7f3f65e37912f4f25917b94b385799ae(
    *,
    launch_template_id: typing.Optional[builtins.str] = None,
    launch_template_name: typing.Optional[builtins.str] = None,
    launch_template_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa27c56308268a00e11b85db59fe0c73d50dd1538749392fbcb29ac71467e4b(
    *,
    target_resource_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__689fdbedc3ad7fb3e0fa20c4acc83271d70a94eda4a2bd89be5a7f3087614654(
    *,
    account_id: typing.Optional[builtins.str] = None,
    launch_template_id: typing.Optional[builtins.str] = None,
    set_default_version: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f2ea63e846ef3726049680e85103917f844d0422a8088e3cb2a639dec6b384e(
    *,
    ami_account_id: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[builtins.str] = None,
    parameter_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c4dc3e6deea4f5e57c5497fea60eaabdf6133ae8f3793257be0207f9649ac7(
    *,
    container_recipe_arn: typing.Optional[builtins.str] = None,
    deletion_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImagePropsMixin.DeletionSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    distribution_configuration_arn: typing.Optional[builtins.str] = None,
    enhanced_image_metadata_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    execution_role: typing.Optional[builtins.str] = None,
    image_pipeline_execution_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImagePropsMixin.ImagePipelineExecutionSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_recipe_arn: typing.Optional[builtins.str] = None,
    image_scanning_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImagePropsMixin.ImageScanningConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_tests_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImagePropsMixin.ImageTestsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    infrastructure_configuration_arn: typing.Optional[builtins.str] = None,
    logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImagePropsMixin.ImageLoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    workflows: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImagePropsMixin.WorkflowConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71fea23c7a9600260786b2594ea3c73328b1471e6508013b7723ebcae900389d(
    *,
    container_recipe_arn: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    distribution_configuration_arn: typing.Optional[builtins.str] = None,
    enhanced_image_metadata_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    execution_role: typing.Optional[builtins.str] = None,
    image_recipe_arn: typing.Optional[builtins.str] = None,
    image_scanning_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImagePipelinePropsMixin.ImageScanningConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_tests_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImagePipelinePropsMixin.ImageTestsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    infrastructure_configuration_arn: typing.Optional[builtins.str] = None,
    logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImagePipelinePropsMixin.PipelineLoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImagePipelinePropsMixin.ScheduleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    workflows: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImagePipelinePropsMixin.WorkflowConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__088b1151cdd817229b45c6ce883ec8496c99da45c77cd4f403b0a0b4bb78cd61(
    props: typing.Union[CfnImagePipelineMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97497d8c097f532b75195c9d99edfcdb00c0302b9d024c1cbbdf3e657d26fa0b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5c10a1989638f9b6f88b2bc85167ca724bb71b66aa9fb44778d654de5855f51(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6e63d5158a4c5c169c79c6b4e2a49bd3d4328dd626301a0af7d4acadd1c2eb1(
    *,
    failure_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4ffbd60e601ffdd6bf391308e4aeb9babd1ab26c698e5385cf1ff8badff244c(
    *,
    container_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    repository_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de29f4f60c4e5df61d1306f6cabb4daeb0e5a7c2084ea47552c03dfcd74f8b8(
    *,
    ecr_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImagePipelinePropsMixin.EcrConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_scanning_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a549f62e8294116c837891dca0b8e1b7e96c758b8d559b44ab71fd32f4ee4fb9(
    *,
    image_tests_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad6a071c1a7b53111dbfc9d97e8e79a41ad6d0da1e47ad39514c2766f676726(
    *,
    image_log_group_name: typing.Optional[builtins.str] = None,
    pipeline_log_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__737e7c96e267e0ae414be9646fc10a4a8ec15ae75dfac2b1d8bc71866cfd631f(
    *,
    auto_disable_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImagePipelinePropsMixin.AutoDisablePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    pipeline_execution_start_condition: typing.Optional[builtins.str] = None,
    schedule_expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b55874d0c4c966a148f44d76664fbd2658b7027aeaf661c4194cfd19b312c0(
    *,
    on_failure: typing.Optional[builtins.str] = None,
    parallel_group: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImagePipelinePropsMixin.WorkflowParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    workflow_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0917cb8fff1393da8eca6d7429090fea91faff83082def182c5512d1a846990(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec1826dc052f5bdb15d385f235beae833e076ef0fbaf2f898ea4f12e3fe2120(
    props: typing.Union[CfnImageMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc7bfc7febc932c3ea6162c319b6e39f305bc2db72b83a6299439018ee83dd7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa0f00e7759be2a88a7b9629ba90f51b36ca17906931a4d7fe05b084ec31b73(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2949760e8d6926b2f23e40a6e6b2ea6b9bd57777efeaae6140868208df75b9cb(
    *,
    execution_role: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f279c26cca45e2bc94c97157e8d10bf918dc1ba231cd2575af8aca69f3f803b(
    *,
    container_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    repository_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18ca6049f95efb283b98ebba3e5690737e756345fa6d54187edf56e76d0601df(
    *,
    log_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb6c93e67f67335d07de8e8ed01ecfa21335ea11cc5d8037f747706798814db(
    *,
    deployment_id: typing.Optional[builtins.str] = None,
    on_update: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__237d0fe6eb6d9d225cd163e4576a58703b3b930e96b29a0a5c213c90ae0f3d9d(
    *,
    ecr_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImagePropsMixin.EcrConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_scanning_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e7d928f26b38f98a2fa6d8caa4c5afa3af5c311e918aeac9c826c8b1ec38273(
    *,
    image_tests_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e94e14b0acf3493afb70e1f191435d5ba3950a28547a43b05fea865550170c(
    *,
    arn: typing.Optional[builtins.str] = None,
    major: typing.Optional[builtins.str] = None,
    minor: typing.Optional[builtins.str] = None,
    patch: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfecb272dd58294c75966e07b9b7a15e5d7da357229726bb1d080df36163d187(
    *,
    on_failure: typing.Optional[builtins.str] = None,
    parallel_group: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImagePropsMixin.WorkflowParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    workflow_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35f4ee175cbfb950dc02c53f270ef6e361abcbb05defe578e4d860b81c9ee07d(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce929e277d6ba31bdb8ff37d76af55403c0e4454344f7fba64059a2f657a09db(
    *,
    additional_instance_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImageRecipePropsMixin.AdditionalInstanceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ami_tags: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    block_device_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImageRecipePropsMixin.InstanceBlockDeviceMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    components: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImageRecipePropsMixin.ComponentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    parent_image: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    version: typing.Optional[builtins.str] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a03d8128c946f0dcf2b1a794676a822ae30b24819edd7e2a3bf3af60cd0e35d(
    props: typing.Union[CfnImageRecipeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ec6d7d9fa8cc9e24f44b480170fd94251f1dbab1e08bd9a5e19a87f858c1af(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__321997575748627861ff20436d43801bf9660c25fa3ec75d737de9fab88349d2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ea1555ded0d1fe96d1f1c5ac0769af6a2534a244e716586f432cb789a2d64db(
    *,
    systems_manager_agent: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImageRecipePropsMixin.SystemsManagerAgentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_data_override: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6809c8c3e6425e9a779a29f87bdfc3ab9460f54ae8f3d7d24315d54bf921027f(
    *,
    component_arn: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImageRecipePropsMixin.ComponentParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__145da444f4cdf0a2a8f173f89f416ac19403ff2e07baadf2a2d0015e5f04325e(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__859a2bdb2df5bbc7446556ccdaa2099bb1fed1b3a7ad8f8f78f758924cb3f5a3(
    *,
    delete_on_termination: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    iops: typing.Optional[jsii.Number] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    snapshot_id: typing.Optional[builtins.str] = None,
    throughput: typing.Optional[jsii.Number] = None,
    volume_size: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b065cf628c2f3726b15f1545f48ba6122a4f5622daada22f6962523e6d631c(
    *,
    device_name: typing.Optional[builtins.str] = None,
    ebs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnImageRecipePropsMixin.EbsInstanceBlockDeviceSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    no_device: typing.Optional[builtins.str] = None,
    virtual_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__885f8989970d10e9349c326a26f89622ce2a05fe5ea3c57a113a45311f382206(
    *,
    arn: typing.Optional[builtins.str] = None,
    major: typing.Optional[builtins.str] = None,
    minor: typing.Optional[builtins.str] = None,
    patch: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7097147b04dd06e0365924ffb180772fa651964b1747a45c2cd873e7f560ac0f(
    *,
    uninstall_after_build: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78c63423ae164fc6c1ae635513bf7685937d20c543ecc658ad8c8d712ebcc70a(
    *,
    description: typing.Optional[builtins.str] = None,
    instance_metadata_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInfrastructureConfigurationPropsMixin.InstanceMetadataOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_profile_name: typing.Optional[builtins.str] = None,
    instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    key_pair: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInfrastructureConfigurationPropsMixin.LoggingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    placement: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInfrastructureConfigurationPropsMixin.PlacementProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_tags: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    sns_topic_arn: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    terminate_instance_on_failure: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__467564eb33c2fda88db762c1819250a37bc28063ba9f9d1157ea47dd291f8324(
    props: typing.Union[CfnInfrastructureConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7929a7a642870b8e6801b84b61402f351314058882ae948c56e8a51ed61630c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e02913d58db423cbf45bdcac6d40301596e32f1769256321eacf13355f5d31bb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4666cf57df0442cccb6a0521437243b6566be0ca42637d8516f35c28347d4990(
    *,
    http_put_response_hop_limit: typing.Optional[jsii.Number] = None,
    http_tokens: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5725c4b3ecc329dce53380d11a5d22471b6e23740b298a6a3f9aab272a5bbad1(
    *,
    s3_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInfrastructureConfigurationPropsMixin.S3LogsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcb492305265ff21d45a7ef5795f6308db2b230c21864a7c8aaecdb6d2f26c5f(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    host_id: typing.Optional[builtins.str] = None,
    host_resource_group_arn: typing.Optional[builtins.str] = None,
    tenancy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f71e3a3b862bab3d496b58bad48667d7a7ca7e8acd1dd90dfaf8e39b8092a084(
    *,
    s3_bucket_name: typing.Optional[builtins.str] = None,
    s3_key_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015d17620a4eaae526ba4c8dac69e0d8d21add3a2301acd4255ae7c9827da202(
    *,
    description: typing.Optional[builtins.str] = None,
    execution_role: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    policy_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.PolicyDetailProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_selection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.ResourceSelectionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_type: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361f4940d98fc0b13cb6be371417805028f9c2b3693ab348cf803320abfda867(
    props: typing.Union[CfnLifecyclePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__957936708cadcb27c2b64b529d5698ce55ee769edb50c332f4e4373b92876235(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69cb6c8c1895aea3ff899cc56f815d951b0e8a87a24a9a2304a8c86515ebf293(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e50bcee9bf47ce2810780205fe4a7cd1bf412f46da3d649b7f3b79c0c442ec4(
    *,
    include_resources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.IncludeResourcesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8293546a98390c3d67c314a430ea0d2b19b0c0f67a45c99996c7afa3e6fbc51c(
    *,
    is_public: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    last_launched: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.LastLaunchedProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    shared_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag_map: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a8d550560a69596c3694eab04b6996ac014bcb79c28fafdd42a2825a669c3a3(
    *,
    amis: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.AmiExclusionRulesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tag_map: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0e1435caaa8311a027e4feab38468ad39b2d9a15a9a2c0fbf09740a2491f42b(
    *,
    retain_at_least: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
    unit: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2550652a0c4430ff9fa93688d96f09a134f3a3e900e7050af8f69674f94267c(
    *,
    amis: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    containers: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    snapshots: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ca748e7952ccfcbea63270107505b04c46577a306466d4a5861ea8f28f0c459(
    *,
    unit: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72eed8acb87233ff7a859e84c828f5c50a5aabfe1e00826bb4746f49ebb117d2(
    *,
    action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.ActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    exclusion_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.ExclusionRulesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.FilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f52a2498b86a32736569c9fceffae6db083e09bf192cdd418e257600677d7d(
    *,
    name: typing.Optional[builtins.str] = None,
    semantic_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37b796085843596595c4daa8a7962359a26f6a09c61834692e237940188610d(
    *,
    recipes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLifecyclePolicyPropsMixin.RecipeSelectionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tag_map: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef6fded30405ecee20dab2e2f87530e7d5e1e3d5051066348817acad1ce88fae(
    *,
    change_description: typing.Optional[builtins.str] = None,
    data: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
    uri: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a42aa86483eac9f8b2dfd70f756e35abc34e2f71a20964257fce2672bbfd4bee(
    props: typing.Union[CfnWorkflowMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9d9c15569f55912b2c5cbaf1ddcf4fdb68dba454ad5590f16df44fc6a30d7b8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46dc11b2640a711f76862077da0c86d96790f6e76ab454d62a5ea1b1eb100d58(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed7ec9c106a806c59511c7d2234aa615766bee6f3c7f62e12aa10c8eb27d021(
    *,
    arn: typing.Optional[builtins.str] = None,
    major: typing.Optional[builtins.str] = None,
    minor: typing.Optional[builtins.str] = None,
    patch: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
