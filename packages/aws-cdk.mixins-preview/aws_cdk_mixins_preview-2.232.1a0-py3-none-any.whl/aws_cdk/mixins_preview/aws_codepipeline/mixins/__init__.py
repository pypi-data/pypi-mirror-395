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
    jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnCustomActionTypeMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "category": "category",
        "configuration_properties": "configurationProperties",
        "input_artifact_details": "inputArtifactDetails",
        "output_artifact_details": "outputArtifactDetails",
        "provider": "provider",
        "settings": "settings",
        "tags": "tags",
        "version": "version",
    },
)
class CfnCustomActionTypeMixinProps:
    def __init__(
        self,
        *,
        category: typing.Optional[builtins.str] = None,
        configuration_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCustomActionTypePropsMixin.ConfigurationPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        input_artifact_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCustomActionTypePropsMixin.ArtifactDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        output_artifact_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCustomActionTypePropsMixin.ArtifactDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        provider: typing.Optional[builtins.str] = None,
        settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCustomActionTypePropsMixin.SettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnCustomActionTypePropsMixin.

        :param category: The category of the custom action, such as a build action or a test action.
        :param configuration_properties: The configuration properties for the custom action. .. epigraph:: You can refer to a name in the configuration properties of the custom action within the URL templates by following the format of {Config:name}, as long as the configuration property is both required and not secret. For more information, see `Create a Custom Action for a Pipeline <https://docs.aws.amazon.com/codepipeline/latest/userguide/how-to-create-custom-action.html>`_ .
        :param input_artifact_details: The details of the input artifact for the action, such as its commit ID.
        :param output_artifact_details: The details of the output artifact of the action, such as its commit ID.
        :param provider: The provider of the service used in the custom action, such as CodeDeploy.
        :param settings: URLs that provide users information about this custom action.
        :param tags: The tags for the custom action.
        :param version: The version identifier of the custom action.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
            
            cfn_custom_action_type_mixin_props = codepipeline_mixins.CfnCustomActionTypeMixinProps(
                category="category",
                configuration_properties=[codepipeline_mixins.CfnCustomActionTypePropsMixin.ConfigurationPropertiesProperty(
                    description="description",
                    key=False,
                    name="name",
                    queryable=False,
                    required=False,
                    secret=False,
                    type="type"
                )],
                input_artifact_details=codepipeline_mixins.CfnCustomActionTypePropsMixin.ArtifactDetailsProperty(
                    maximum_count=123,
                    minimum_count=123
                ),
                output_artifact_details=codepipeline_mixins.CfnCustomActionTypePropsMixin.ArtifactDetailsProperty(
                    maximum_count=123,
                    minimum_count=123
                ),
                provider="provider",
                settings=codepipeline_mixins.CfnCustomActionTypePropsMixin.SettingsProperty(
                    entity_url_template="entityUrlTemplate",
                    execution_url_template="executionUrlTemplate",
                    revision_url_template="revisionUrlTemplate",
                    third_party_configuration_url="thirdPartyConfigurationUrl"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                version="version"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c92149a4045c439fc1e60bd1689096f2e074364601078bd24dc81425b76e5d7)
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
            check_type(argname="argument configuration_properties", value=configuration_properties, expected_type=type_hints["configuration_properties"])
            check_type(argname="argument input_artifact_details", value=input_artifact_details, expected_type=type_hints["input_artifact_details"])
            check_type(argname="argument output_artifact_details", value=output_artifact_details, expected_type=type_hints["output_artifact_details"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if category is not None:
            self._values["category"] = category
        if configuration_properties is not None:
            self._values["configuration_properties"] = configuration_properties
        if input_artifact_details is not None:
            self._values["input_artifact_details"] = input_artifact_details
        if output_artifact_details is not None:
            self._values["output_artifact_details"] = output_artifact_details
        if provider is not None:
            self._values["provider"] = provider
        if settings is not None:
            self._values["settings"] = settings
        if tags is not None:
            self._values["tags"] = tags
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def category(self) -> typing.Optional[builtins.str]:
        '''The category of the custom action, such as a build action or a test action.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-category
        '''
        result = self._values.get("category")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomActionTypePropsMixin.ConfigurationPropertiesProperty"]]]]:
        '''The configuration properties for the custom action.

        .. epigraph::

           You can refer to a name in the configuration properties of the custom action within the URL templates by following the format of {Config:name}, as long as the configuration property is both required and not secret. For more information, see `Create a Custom Action for a Pipeline <https://docs.aws.amazon.com/codepipeline/latest/userguide/how-to-create-custom-action.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-configurationproperties
        '''
        result = self._values.get("configuration_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomActionTypePropsMixin.ConfigurationPropertiesProperty"]]]], result)

    @builtins.property
    def input_artifact_details(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomActionTypePropsMixin.ArtifactDetailsProperty"]]:
        '''The details of the input artifact for the action, such as its commit ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-inputartifactdetails
        '''
        result = self._values.get("input_artifact_details")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomActionTypePropsMixin.ArtifactDetailsProperty"]], result)

    @builtins.property
    def output_artifact_details(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomActionTypePropsMixin.ArtifactDetailsProperty"]]:
        '''The details of the output artifact of the action, such as its commit ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-outputartifactdetails
        '''
        result = self._values.get("output_artifact_details")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomActionTypePropsMixin.ArtifactDetailsProperty"]], result)

    @builtins.property
    def provider(self) -> typing.Optional[builtins.str]:
        '''The provider of the service used in the custom action, such as CodeDeploy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-provider
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomActionTypePropsMixin.SettingsProperty"]]:
        '''URLs that provide users information about this custom action.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-settings
        '''
        result = self._values.get("settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomActionTypePropsMixin.SettingsProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags for the custom action.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The version identifier of the custom action.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCustomActionTypeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCustomActionTypePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnCustomActionTypePropsMixin",
):
    '''The ``AWS::CodePipeline::CustomActionType`` resource creates a custom action for activities that aren't included in the CodePipeline default actions, such as running an internally developed build process or a test suite.

    You can use these custom actions in the stage of a pipeline. For more information, see `Create and Add a Custom Action in AWS CodePipeline <https://docs.aws.amazon.com/codepipeline/latest/userguide/how-to-create-custom-action.html>`_ in the *AWS CodePipeline User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html
    :cloudformationResource: AWS::CodePipeline::CustomActionType
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
        
        cfn_custom_action_type_props_mixin = codepipeline_mixins.CfnCustomActionTypePropsMixin(codepipeline_mixins.CfnCustomActionTypeMixinProps(
            category="category",
            configuration_properties=[codepipeline_mixins.CfnCustomActionTypePropsMixin.ConfigurationPropertiesProperty(
                description="description",
                key=False,
                name="name",
                queryable=False,
                required=False,
                secret=False,
                type="type"
            )],
            input_artifact_details=codepipeline_mixins.CfnCustomActionTypePropsMixin.ArtifactDetailsProperty(
                maximum_count=123,
                minimum_count=123
            ),
            output_artifact_details=codepipeline_mixins.CfnCustomActionTypePropsMixin.ArtifactDetailsProperty(
                maximum_count=123,
                minimum_count=123
            ),
            provider="provider",
            settings=codepipeline_mixins.CfnCustomActionTypePropsMixin.SettingsProperty(
                entity_url_template="entityUrlTemplate",
                execution_url_template="executionUrlTemplate",
                revision_url_template="revisionUrlTemplate",
                third_party_configuration_url="thirdPartyConfigurationUrl"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            version="version"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCustomActionTypeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CodePipeline::CustomActionType``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__509030bc71f54a422b1ea8fdfd3f242709375838b41049d8d5213b9088bb4a40)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ff54688372e804ce1131b5be865b9b14dab6b500a3880d96c29edba64d1f9de)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eb2527394974bdb067233feb44fa441424dac85bf84fb143da6a5d2ff3ca5c9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCustomActionTypeMixinProps:
        return typing.cast(CfnCustomActionTypeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnCustomActionTypePropsMixin.ArtifactDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "maximum_count": "maximumCount",
            "minimum_count": "minimumCount",
        },
    )
    class ArtifactDetailsProperty:
        def __init__(
            self,
            *,
            maximum_count: typing.Optional[jsii.Number] = None,
            minimum_count: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Returns information about the details of an artifact.

            :param maximum_count: The maximum number of artifacts allowed for the action type.
            :param minimum_count: The minimum number of artifacts allowed for the action type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-artifactdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                artifact_details_property = codepipeline_mixins.CfnCustomActionTypePropsMixin.ArtifactDetailsProperty(
                    maximum_count=123,
                    minimum_count=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__88ec54a4077d4d556cd35c3c3dd5d2a7487f588ad33308b3114d86ac1bc401d9)
                check_type(argname="argument maximum_count", value=maximum_count, expected_type=type_hints["maximum_count"])
                check_type(argname="argument minimum_count", value=minimum_count, expected_type=type_hints["minimum_count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if maximum_count is not None:
                self._values["maximum_count"] = maximum_count
            if minimum_count is not None:
                self._values["minimum_count"] = minimum_count

        @builtins.property
        def maximum_count(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of artifacts allowed for the action type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-artifactdetails.html#cfn-codepipeline-customactiontype-artifactdetails-maximumcount
            '''
            result = self._values.get("maximum_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def minimum_count(self) -> typing.Optional[jsii.Number]:
            '''The minimum number of artifacts allowed for the action type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-artifactdetails.html#cfn-codepipeline-customactiontype-artifactdetails-minimumcount
            '''
            result = self._values.get("minimum_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ArtifactDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnCustomActionTypePropsMixin.ConfigurationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "key": "key",
            "name": "name",
            "queryable": "queryable",
            "required": "required",
            "secret": "secret",
            "type": "type",
        },
    )
    class ConfigurationPropertiesProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            key: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            name: typing.Optional[builtins.str] = None,
            queryable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            secret: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration properties for the custom action.

            .. epigraph::

               You can refer to a name in the configuration properties of the custom action within the URL templates by following the format of {Config:name}, as long as the configuration property is both required and not secret. For more information, see `Create a Custom Action for a Pipeline <https://docs.aws.amazon.com/codepipeline/latest/userguide/how-to-create-custom-action.html>`_ .

            :param description: The description of the action configuration property that is displayed to users.
            :param key: Whether the configuration property is a key.
            :param name: The name of the action configuration property.
            :param queryable: Indicates that the property is used with ``PollForJobs`` . When creating a custom action, an action can have up to one queryable property. If it has one, that property must be both required and not secret. If you create a pipeline with a custom action type, and that custom action contains a queryable property, the value for that configuration property is subject to other restrictions. The value must be less than or equal to twenty (20) characters. The value can contain only alphanumeric characters, underscores, and hyphens.
            :param required: Whether the configuration property is a required value.
            :param secret: Whether the configuration property is secret. Secrets are hidden from all calls except for ``GetJobDetails`` , ``GetThirdPartyJobDetails`` , ``PollForJobs`` , and ``PollForThirdPartyJobs`` . When updating a pipeline, passing * * * * * without changing any other values of the action preserves the previous value of the secret.
            :param type: The type of the configuration property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-configurationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                configuration_properties_property = codepipeline_mixins.CfnCustomActionTypePropsMixin.ConfigurationPropertiesProperty(
                    description="description",
                    key=False,
                    name="name",
                    queryable=False,
                    required=False,
                    secret=False,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d113fc1b4caaa269a3e6c0f0ee786de343932d53c3545a24f6791ff70ac073a2)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument queryable", value=queryable, expected_type=type_hints["queryable"])
                check_type(argname="argument required", value=required, expected_type=type_hints["required"])
                check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if key is not None:
                self._values["key"] = key
            if name is not None:
                self._values["name"] = name
            if queryable is not None:
                self._values["queryable"] = queryable
            if required is not None:
                self._values["required"] = required
            if secret is not None:
                self._values["secret"] = secret
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the action configuration property that is displayed to users.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-configurationproperties.html#cfn-codepipeline-customactiontype-configurationproperties-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether the configuration property is a key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-configurationproperties.html#cfn-codepipeline-customactiontype-configurationproperties-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the action configuration property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-configurationproperties.html#cfn-codepipeline-customactiontype-configurationproperties-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def queryable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates that the property is used with ``PollForJobs`` .

            When creating a custom action, an action can have up to one queryable property. If it has one, that property must be both required and not secret.

            If you create a pipeline with a custom action type, and that custom action contains a queryable property, the value for that configuration property is subject to other restrictions. The value must be less than or equal to twenty (20) characters. The value can contain only alphanumeric characters, underscores, and hyphens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-configurationproperties.html#cfn-codepipeline-customactiontype-configurationproperties-queryable
            '''
            result = self._values.get("queryable")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def required(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether the configuration property is a required value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-configurationproperties.html#cfn-codepipeline-customactiontype-configurationproperties-required
            '''
            result = self._values.get("required")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def secret(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether the configuration property is secret.

            Secrets are hidden from all calls except for ``GetJobDetails`` , ``GetThirdPartyJobDetails`` , ``PollForJobs`` , and ``PollForThirdPartyJobs`` .

            When updating a pipeline, passing * * * * * without changing any other values of the action preserves the previous value of the secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-configurationproperties.html#cfn-codepipeline-customactiontype-configurationproperties-secret
            '''
            result = self._values.get("secret")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of the configuration property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-configurationproperties.html#cfn-codepipeline-customactiontype-configurationproperties-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnCustomActionTypePropsMixin.SettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "entity_url_template": "entityUrlTemplate",
            "execution_url_template": "executionUrlTemplate",
            "revision_url_template": "revisionUrlTemplate",
            "third_party_configuration_url": "thirdPartyConfigurationUrl",
        },
    )
    class SettingsProperty:
        def __init__(
            self,
            *,
            entity_url_template: typing.Optional[builtins.str] = None,
            execution_url_template: typing.Optional[builtins.str] = None,
            revision_url_template: typing.Optional[builtins.str] = None,
            third_party_configuration_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``Settings`` is a property of the ``AWS::CodePipeline::CustomActionType`` resource that provides URLs that users can access to view information about the CodePipeline custom action.

            :param entity_url_template: The URL returned to the CodePipeline console that provides a deep link to the resources of the external system, such as the configuration page for a CodeDeploy deployment group. This link is provided as part of the action display in the pipeline.
            :param execution_url_template: The URL returned to the CodePipeline console that contains a link to the top-level landing page for the external system, such as the console page for CodeDeploy. This link is shown on the pipeline view page in the CodePipeline console and provides a link to the execution entity of the external action.
            :param revision_url_template: The URL returned to the CodePipeline console that contains a link to the page where customers can update or change the configuration of the external action.
            :param third_party_configuration_url: The URL of a sign-up page where users can sign up for an external service and perform initial configuration of the action provided by that service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-settings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                settings_property = codepipeline_mixins.CfnCustomActionTypePropsMixin.SettingsProperty(
                    entity_url_template="entityUrlTemplate",
                    execution_url_template="executionUrlTemplate",
                    revision_url_template="revisionUrlTemplate",
                    third_party_configuration_url="thirdPartyConfigurationUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__40fde3f62227cf15cc8fb663750da29accd9b51254e4a1f94437792097f92373)
                check_type(argname="argument entity_url_template", value=entity_url_template, expected_type=type_hints["entity_url_template"])
                check_type(argname="argument execution_url_template", value=execution_url_template, expected_type=type_hints["execution_url_template"])
                check_type(argname="argument revision_url_template", value=revision_url_template, expected_type=type_hints["revision_url_template"])
                check_type(argname="argument third_party_configuration_url", value=third_party_configuration_url, expected_type=type_hints["third_party_configuration_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if entity_url_template is not None:
                self._values["entity_url_template"] = entity_url_template
            if execution_url_template is not None:
                self._values["execution_url_template"] = execution_url_template
            if revision_url_template is not None:
                self._values["revision_url_template"] = revision_url_template
            if third_party_configuration_url is not None:
                self._values["third_party_configuration_url"] = third_party_configuration_url

        @builtins.property
        def entity_url_template(self) -> typing.Optional[builtins.str]:
            '''The URL returned to the CodePipeline console that provides a deep link to the resources of the external system, such as the configuration page for a CodeDeploy deployment group.

            This link is provided as part of the action display in the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-settings.html#cfn-codepipeline-customactiontype-settings-entityurltemplate
            '''
            result = self._values.get("entity_url_template")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def execution_url_template(self) -> typing.Optional[builtins.str]:
            '''The URL returned to the CodePipeline console that contains a link to the top-level landing page for the external system, such as the console page for CodeDeploy.

            This link is shown on the pipeline view page in the CodePipeline console and provides a link to the execution entity of the external action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-settings.html#cfn-codepipeline-customactiontype-settings-executionurltemplate
            '''
            result = self._values.get("execution_url_template")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def revision_url_template(self) -> typing.Optional[builtins.str]:
            '''The URL returned to the CodePipeline console that contains a link to the page where customers can update or change the configuration of the external action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-settings.html#cfn-codepipeline-customactiontype-settings-revisionurltemplate
            '''
            result = self._values.get("revision_url_template")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def third_party_configuration_url(self) -> typing.Optional[builtins.str]:
            '''The URL of a sign-up page where users can sign up for an external service and perform initial configuration of the action provided by that service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-settings.html#cfn-codepipeline-customactiontype-settings-thirdpartyconfigurationurl
            '''
            result = self._values.get("third_party_configuration_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelineMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "artifact_store": "artifactStore",
        "artifact_stores": "artifactStores",
        "disable_inbound_stage_transitions": "disableInboundStageTransitions",
        "execution_mode": "executionMode",
        "name": "name",
        "pipeline_type": "pipelineType",
        "restart_execution_on_update": "restartExecutionOnUpdate",
        "role_arn": "roleArn",
        "stages": "stages",
        "tags": "tags",
        "triggers": "triggers",
        "variables": "variables",
    },
)
class CfnPipelineMixinProps:
    def __init__(
        self,
        *,
        artifact_store: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.ArtifactStoreProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        artifact_stores: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.ArtifactStoreMapProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        disable_inbound_stage_transitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.StageTransitionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        execution_mode: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        pipeline_type: typing.Optional[builtins.str] = None,
        restart_execution_on_update: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        stages: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.StageDeclarationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        triggers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.PipelineTriggerDeclarationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.VariableDeclarationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnPipelinePropsMixin.

        :param artifact_store: The S3 bucket where artifacts for the pipeline are stored. .. epigraph:: You must include either ``artifactStore`` or ``artifactStores`` in your pipeline, but you cannot use both. If you create a cross-region action in your pipeline, you must use ``artifactStores`` .
        :param artifact_stores: A mapping of ``artifactStore`` objects and their corresponding AWS Regions. There must be an artifact store for the pipeline Region and for each cross-region action in the pipeline. .. epigraph:: You must include either ``artifactStore`` or ``artifactStores`` in your pipeline, but you cannot use both. If you create a cross-region action in your pipeline, you must use ``artifactStores`` .
        :param disable_inbound_stage_transitions: Represents the input of a ``DisableStageTransition`` action.
        :param execution_mode: The method that the pipeline will use to handle multiple executions. The default mode is SUPERSEDED. Default: - "SUPERSEDED"
        :param name: The name of the pipeline.
        :param pipeline_type: CodePipeline provides the following pipeline types, which differ in characteristics and price, so that you can tailor your pipeline features and cost to the needs of your applications. - V1 type pipelines have a JSON structure that contains standard pipeline, stage, and action-level parameters. - V2 type pipelines have the same structure as a V1 type, along with additional parameters for release safety and trigger configuration. .. epigraph:: Including V2 parameters, such as triggers on Git tags, in the pipeline JSON when creating or updating a pipeline will result in the pipeline having the V2 type of pipeline and the associated costs. For information about pricing for CodePipeline, see `Pricing <https://docs.aws.amazon.com/codepipeline/pricing/>`_ . For information about which type of pipeline to choose, see `What type of pipeline is right for me? <https://docs.aws.amazon.com/codepipeline/latest/userguide/pipeline-types-planning.html>`_ .
        :param restart_execution_on_update: Indicates whether to rerun the CodePipeline pipeline after you update it.
        :param role_arn: The Amazon Resource Name (ARN) for CodePipeline to use to either perform actions with no ``actionRoleArn`` , or to use to assume roles for actions with an ``actionRoleArn`` .
        :param stages: Represents information about a stage and its definition.
        :param tags: Specifies the tags applied to the pipeline.
        :param triggers: The trigger configuration specifying a type of event, such as Git tags, that starts the pipeline. .. epigraph:: When a trigger configuration is specified, default change detection for repository and branch commits is disabled.
        :param variables: A list that defines the pipeline variables for a pipeline resource. Variable names can have alphanumeric and underscore characters, and the values must match ``[A-Za-z0-9@\\-_]+`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
            
            # configuration: Any
            
            cfn_pipeline_mixin_props = codepipeline_mixins.CfnPipelineMixinProps(
                artifact_store=codepipeline_mixins.CfnPipelinePropsMixin.ArtifactStoreProperty(
                    encryption_key=codepipeline_mixins.CfnPipelinePropsMixin.EncryptionKeyProperty(
                        id="id",
                        type="type"
                    ),
                    location="location",
                    type="type"
                ),
                artifact_stores=[codepipeline_mixins.CfnPipelinePropsMixin.ArtifactStoreMapProperty(
                    artifact_store=codepipeline_mixins.CfnPipelinePropsMixin.ArtifactStoreProperty(
                        encryption_key=codepipeline_mixins.CfnPipelinePropsMixin.EncryptionKeyProperty(
                            id="id",
                            type="type"
                        ),
                        location="location",
                        type="type"
                    ),
                    region="region"
                )],
                disable_inbound_stage_transitions=[codepipeline_mixins.CfnPipelinePropsMixin.StageTransitionProperty(
                    reason="reason",
                    stage_name="stageName"
                )],
                execution_mode="executionMode",
                name="name",
                pipeline_type="pipelineType",
                restart_execution_on_update=False,
                role_arn="roleArn",
                stages=[codepipeline_mixins.CfnPipelinePropsMixin.StageDeclarationProperty(
                    actions=[codepipeline_mixins.CfnPipelinePropsMixin.ActionDeclarationProperty(
                        action_type_id=codepipeline_mixins.CfnPipelinePropsMixin.ActionTypeIdProperty(
                            category="category",
                            owner="owner",
                            provider="provider",
                            version="version"
                        ),
                        commands=["commands"],
                        configuration=configuration,
                        environment_variables=[codepipeline_mixins.CfnPipelinePropsMixin.EnvironmentVariableProperty(
                            name="name",
                            type="type",
                            value="value"
                        )],
                        input_artifacts=[codepipeline_mixins.CfnPipelinePropsMixin.InputArtifactProperty(
                            name="name"
                        )],
                        name="name",
                        namespace="namespace",
                        output_artifacts=[codepipeline_mixins.CfnPipelinePropsMixin.OutputArtifactProperty(
                            files=["files"],
                            name="name"
                        )],
                        output_variables=["outputVariables"],
                        region="region",
                        role_arn="roleArn",
                        run_order=123,
                        timeout_in_minutes=123
                    )],
                    before_entry=codepipeline_mixins.CfnPipelinePropsMixin.BeforeEntryConditionsProperty(
                        conditions=[codepipeline_mixins.CfnPipelinePropsMixin.ConditionProperty(
                            result="result",
                            rules=[codepipeline_mixins.CfnPipelinePropsMixin.RuleDeclarationProperty(
                                commands=["commands"],
                                configuration=configuration,
                                input_artifacts=[codepipeline_mixins.CfnPipelinePropsMixin.InputArtifactProperty(
                                    name="name"
                                )],
                                name="name",
                                region="region",
                                role_arn="roleArn",
                                rule_type_id=codepipeline_mixins.CfnPipelinePropsMixin.RuleTypeIdProperty(
                                    category="category",
                                    owner="owner",
                                    provider="provider",
                                    version="version"
                                )
                            )]
                        )]
                    ),
                    blockers=[codepipeline_mixins.CfnPipelinePropsMixin.BlockerDeclarationProperty(
                        name="name",
                        type="type"
                    )],
                    name="name",
                    on_failure=codepipeline_mixins.CfnPipelinePropsMixin.FailureConditionsProperty(
                        conditions=[codepipeline_mixins.CfnPipelinePropsMixin.ConditionProperty(
                            result="result",
                            rules=[codepipeline_mixins.CfnPipelinePropsMixin.RuleDeclarationProperty(
                                commands=["commands"],
                                configuration=configuration,
                                input_artifacts=[codepipeline_mixins.CfnPipelinePropsMixin.InputArtifactProperty(
                                    name="name"
                                )],
                                name="name",
                                region="region",
                                role_arn="roleArn",
                                rule_type_id=codepipeline_mixins.CfnPipelinePropsMixin.RuleTypeIdProperty(
                                    category="category",
                                    owner="owner",
                                    provider="provider",
                                    version="version"
                                )
                            )]
                        )],
                        result="result",
                        retry_configuration=codepipeline_mixins.CfnPipelinePropsMixin.RetryConfigurationProperty(
                            retry_mode="retryMode"
                        )
                    ),
                    on_success=codepipeline_mixins.CfnPipelinePropsMixin.SuccessConditionsProperty(
                        conditions=[codepipeline_mixins.CfnPipelinePropsMixin.ConditionProperty(
                            result="result",
                            rules=[codepipeline_mixins.CfnPipelinePropsMixin.RuleDeclarationProperty(
                                commands=["commands"],
                                configuration=configuration,
                                input_artifacts=[codepipeline_mixins.CfnPipelinePropsMixin.InputArtifactProperty(
                                    name="name"
                                )],
                                name="name",
                                region="region",
                                role_arn="roleArn",
                                rule_type_id=codepipeline_mixins.CfnPipelinePropsMixin.RuleTypeIdProperty(
                                    category="category",
                                    owner="owner",
                                    provider="provider",
                                    version="version"
                                )
                            )]
                        )]
                    )
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                triggers=[codepipeline_mixins.CfnPipelinePropsMixin.PipelineTriggerDeclarationProperty(
                    git_configuration=codepipeline_mixins.CfnPipelinePropsMixin.GitConfigurationProperty(
                        pull_request=[codepipeline_mixins.CfnPipelinePropsMixin.GitPullRequestFilterProperty(
                            branches=codepipeline_mixins.CfnPipelinePropsMixin.GitBranchFilterCriteriaProperty(
                                excludes=["excludes"],
                                includes=["includes"]
                            ),
                            events=["events"],
                            file_paths=codepipeline_mixins.CfnPipelinePropsMixin.GitFilePathFilterCriteriaProperty(
                                excludes=["excludes"],
                                includes=["includes"]
                            )
                        )],
                        push=[codepipeline_mixins.CfnPipelinePropsMixin.GitPushFilterProperty(
                            branches=codepipeline_mixins.CfnPipelinePropsMixin.GitBranchFilterCriteriaProperty(
                                excludes=["excludes"],
                                includes=["includes"]
                            ),
                            file_paths=codepipeline_mixins.CfnPipelinePropsMixin.GitFilePathFilterCriteriaProperty(
                                excludes=["excludes"],
                                includes=["includes"]
                            ),
                            tags=codepipeline_mixins.CfnPipelinePropsMixin.GitTagFilterCriteriaProperty(
                                excludes=["excludes"],
                                includes=["includes"]
                            )
                        )],
                        source_action_name="sourceActionName"
                    ),
                    provider_type="providerType"
                )],
                variables=[codepipeline_mixins.CfnPipelinePropsMixin.VariableDeclarationProperty(
                    default_value="defaultValue",
                    description="description",
                    name="name"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a1d9e0584770e83d01526637baa64f80d21cf6414caff8df087494978dfe62)
            check_type(argname="argument artifact_store", value=artifact_store, expected_type=type_hints["artifact_store"])
            check_type(argname="argument artifact_stores", value=artifact_stores, expected_type=type_hints["artifact_stores"])
            check_type(argname="argument disable_inbound_stage_transitions", value=disable_inbound_stage_transitions, expected_type=type_hints["disable_inbound_stage_transitions"])
            check_type(argname="argument execution_mode", value=execution_mode, expected_type=type_hints["execution_mode"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument pipeline_type", value=pipeline_type, expected_type=type_hints["pipeline_type"])
            check_type(argname="argument restart_execution_on_update", value=restart_execution_on_update, expected_type=type_hints["restart_execution_on_update"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument stages", value=stages, expected_type=type_hints["stages"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument triggers", value=triggers, expected_type=type_hints["triggers"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if artifact_store is not None:
            self._values["artifact_store"] = artifact_store
        if artifact_stores is not None:
            self._values["artifact_stores"] = artifact_stores
        if disable_inbound_stage_transitions is not None:
            self._values["disable_inbound_stage_transitions"] = disable_inbound_stage_transitions
        if execution_mode is not None:
            self._values["execution_mode"] = execution_mode
        if name is not None:
            self._values["name"] = name
        if pipeline_type is not None:
            self._values["pipeline_type"] = pipeline_type
        if restart_execution_on_update is not None:
            self._values["restart_execution_on_update"] = restart_execution_on_update
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if stages is not None:
            self._values["stages"] = stages
        if tags is not None:
            self._values["tags"] = tags
        if triggers is not None:
            self._values["triggers"] = triggers
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def artifact_store(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ArtifactStoreProperty"]]:
        '''The S3 bucket where artifacts for the pipeline are stored.

        .. epigraph::

           You must include either ``artifactStore`` or ``artifactStores`` in your pipeline, but you cannot use both. If you create a cross-region action in your pipeline, you must use ``artifactStores`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-artifactstore
        '''
        result = self._values.get("artifact_store")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ArtifactStoreProperty"]], result)

    @builtins.property
    def artifact_stores(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ArtifactStoreMapProperty"]]]]:
        '''A mapping of ``artifactStore`` objects and their corresponding AWS Regions.

        There must be an artifact store for the pipeline Region and for each cross-region action in the pipeline.
        .. epigraph::

           You must include either ``artifactStore`` or ``artifactStores`` in your pipeline, but you cannot use both. If you create a cross-region action in your pipeline, you must use ``artifactStores`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-artifactstores
        '''
        result = self._values.get("artifact_stores")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ArtifactStoreMapProperty"]]]], result)

    @builtins.property
    def disable_inbound_stage_transitions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.StageTransitionProperty"]]]]:
        '''Represents the input of a ``DisableStageTransition`` action.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-disableinboundstagetransitions
        '''
        result = self._values.get("disable_inbound_stage_transitions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.StageTransitionProperty"]]]], result)

    @builtins.property
    def execution_mode(self) -> typing.Optional[builtins.str]:
        '''The method that the pipeline will use to handle multiple executions.

        The default mode is SUPERSEDED.

        :default: - "SUPERSEDED"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-executionmode
        '''
        result = self._values.get("execution_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the pipeline.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pipeline_type(self) -> typing.Optional[builtins.str]:
        '''CodePipeline provides the following pipeline types, which differ in characteristics and price, so that you can tailor your pipeline features and cost to the needs of your applications.

        - V1 type pipelines have a JSON structure that contains standard pipeline, stage, and action-level parameters.
        - V2 type pipelines have the same structure as a V1 type, along with additional parameters for release safety and trigger configuration.

        .. epigraph::

           Including V2 parameters, such as triggers on Git tags, in the pipeline JSON when creating or updating a pipeline will result in the pipeline having the V2 type of pipeline and the associated costs.

        For information about pricing for CodePipeline, see `Pricing <https://docs.aws.amazon.com/codepipeline/pricing/>`_ .

        For information about which type of pipeline to choose, see `What type of pipeline is right for me? <https://docs.aws.amazon.com/codepipeline/latest/userguide/pipeline-types-planning.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-pipelinetype
        '''
        result = self._values.get("pipeline_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restart_execution_on_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether to rerun the CodePipeline pipeline after you update it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-restartexecutiononupdate
        '''
        result = self._values.get("restart_execution_on_update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) for CodePipeline to use to either perform actions with no ``actionRoleArn`` , or to use to assume roles for actions with an ``actionRoleArn`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stages(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.StageDeclarationProperty"]]]]:
        '''Represents information about a stage and its definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-stages
        '''
        result = self._values.get("stages")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.StageDeclarationProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Specifies the tags applied to the pipeline.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def triggers(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.PipelineTriggerDeclarationProperty"]]]]:
        '''The trigger configuration specifying a type of event, such as Git tags, that starts the pipeline.

        .. epigraph::

           When a trigger configuration is specified, default change detection for repository and branch commits is disabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-triggers
        '''
        result = self._values.get("triggers")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.PipelineTriggerDeclarationProperty"]]]], result)

    @builtins.property
    def variables(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.VariableDeclarationProperty"]]]]:
        '''A list that defines the pipeline variables for a pipeline resource.

        Variable names can have alphanumeric and underscore characters, and the values must match ``[A-Za-z0-9@\\-_]+`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-variables
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.VariableDeclarationProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPipelineMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPipelinePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin",
):
    '''The ``AWS::CodePipeline::Pipeline`` resource creates a CodePipeline pipeline that describes how software changes go through a release process.

    For more information, see `What Is CodePipeline? <https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html>`_ in the *CodePipeline User Guide* .

    For an example in YAML and JSON that contains the parameters in this reference, see `Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#aws-resource-codepipeline-pipeline--examples>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html
    :cloudformationResource: AWS::CodePipeline::Pipeline
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
        
        # configuration: Any
        
        cfn_pipeline_props_mixin = codepipeline_mixins.CfnPipelinePropsMixin(codepipeline_mixins.CfnPipelineMixinProps(
            artifact_store=codepipeline_mixins.CfnPipelinePropsMixin.ArtifactStoreProperty(
                encryption_key=codepipeline_mixins.CfnPipelinePropsMixin.EncryptionKeyProperty(
                    id="id",
                    type="type"
                ),
                location="location",
                type="type"
            ),
            artifact_stores=[codepipeline_mixins.CfnPipelinePropsMixin.ArtifactStoreMapProperty(
                artifact_store=codepipeline_mixins.CfnPipelinePropsMixin.ArtifactStoreProperty(
                    encryption_key=codepipeline_mixins.CfnPipelinePropsMixin.EncryptionKeyProperty(
                        id="id",
                        type="type"
                    ),
                    location="location",
                    type="type"
                ),
                region="region"
            )],
            disable_inbound_stage_transitions=[codepipeline_mixins.CfnPipelinePropsMixin.StageTransitionProperty(
                reason="reason",
                stage_name="stageName"
            )],
            execution_mode="executionMode",
            name="name",
            pipeline_type="pipelineType",
            restart_execution_on_update=False,
            role_arn="roleArn",
            stages=[codepipeline_mixins.CfnPipelinePropsMixin.StageDeclarationProperty(
                actions=[codepipeline_mixins.CfnPipelinePropsMixin.ActionDeclarationProperty(
                    action_type_id=codepipeline_mixins.CfnPipelinePropsMixin.ActionTypeIdProperty(
                        category="category",
                        owner="owner",
                        provider="provider",
                        version="version"
                    ),
                    commands=["commands"],
                    configuration=configuration,
                    environment_variables=[codepipeline_mixins.CfnPipelinePropsMixin.EnvironmentVariableProperty(
                        name="name",
                        type="type",
                        value="value"
                    )],
                    input_artifacts=[codepipeline_mixins.CfnPipelinePropsMixin.InputArtifactProperty(
                        name="name"
                    )],
                    name="name",
                    namespace="namespace",
                    output_artifacts=[codepipeline_mixins.CfnPipelinePropsMixin.OutputArtifactProperty(
                        files=["files"],
                        name="name"
                    )],
                    output_variables=["outputVariables"],
                    region="region",
                    role_arn="roleArn",
                    run_order=123,
                    timeout_in_minutes=123
                )],
                before_entry=codepipeline_mixins.CfnPipelinePropsMixin.BeforeEntryConditionsProperty(
                    conditions=[codepipeline_mixins.CfnPipelinePropsMixin.ConditionProperty(
                        result="result",
                        rules=[codepipeline_mixins.CfnPipelinePropsMixin.RuleDeclarationProperty(
                            commands=["commands"],
                            configuration=configuration,
                            input_artifacts=[codepipeline_mixins.CfnPipelinePropsMixin.InputArtifactProperty(
                                name="name"
                            )],
                            name="name",
                            region="region",
                            role_arn="roleArn",
                            rule_type_id=codepipeline_mixins.CfnPipelinePropsMixin.RuleTypeIdProperty(
                                category="category",
                                owner="owner",
                                provider="provider",
                                version="version"
                            )
                        )]
                    )]
                ),
                blockers=[codepipeline_mixins.CfnPipelinePropsMixin.BlockerDeclarationProperty(
                    name="name",
                    type="type"
                )],
                name="name",
                on_failure=codepipeline_mixins.CfnPipelinePropsMixin.FailureConditionsProperty(
                    conditions=[codepipeline_mixins.CfnPipelinePropsMixin.ConditionProperty(
                        result="result",
                        rules=[codepipeline_mixins.CfnPipelinePropsMixin.RuleDeclarationProperty(
                            commands=["commands"],
                            configuration=configuration,
                            input_artifacts=[codepipeline_mixins.CfnPipelinePropsMixin.InputArtifactProperty(
                                name="name"
                            )],
                            name="name",
                            region="region",
                            role_arn="roleArn",
                            rule_type_id=codepipeline_mixins.CfnPipelinePropsMixin.RuleTypeIdProperty(
                                category="category",
                                owner="owner",
                                provider="provider",
                                version="version"
                            )
                        )]
                    )],
                    result="result",
                    retry_configuration=codepipeline_mixins.CfnPipelinePropsMixin.RetryConfigurationProperty(
                        retry_mode="retryMode"
                    )
                ),
                on_success=codepipeline_mixins.CfnPipelinePropsMixin.SuccessConditionsProperty(
                    conditions=[codepipeline_mixins.CfnPipelinePropsMixin.ConditionProperty(
                        result="result",
                        rules=[codepipeline_mixins.CfnPipelinePropsMixin.RuleDeclarationProperty(
                            commands=["commands"],
                            configuration=configuration,
                            input_artifacts=[codepipeline_mixins.CfnPipelinePropsMixin.InputArtifactProperty(
                                name="name"
                            )],
                            name="name",
                            region="region",
                            role_arn="roleArn",
                            rule_type_id=codepipeline_mixins.CfnPipelinePropsMixin.RuleTypeIdProperty(
                                category="category",
                                owner="owner",
                                provider="provider",
                                version="version"
                            )
                        )]
                    )]
                )
            )],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            triggers=[codepipeline_mixins.CfnPipelinePropsMixin.PipelineTriggerDeclarationProperty(
                git_configuration=codepipeline_mixins.CfnPipelinePropsMixin.GitConfigurationProperty(
                    pull_request=[codepipeline_mixins.CfnPipelinePropsMixin.GitPullRequestFilterProperty(
                        branches=codepipeline_mixins.CfnPipelinePropsMixin.GitBranchFilterCriteriaProperty(
                            excludes=["excludes"],
                            includes=["includes"]
                        ),
                        events=["events"],
                        file_paths=codepipeline_mixins.CfnPipelinePropsMixin.GitFilePathFilterCriteriaProperty(
                            excludes=["excludes"],
                            includes=["includes"]
                        )
                    )],
                    push=[codepipeline_mixins.CfnPipelinePropsMixin.GitPushFilterProperty(
                        branches=codepipeline_mixins.CfnPipelinePropsMixin.GitBranchFilterCriteriaProperty(
                            excludes=["excludes"],
                            includes=["includes"]
                        ),
                        file_paths=codepipeline_mixins.CfnPipelinePropsMixin.GitFilePathFilterCriteriaProperty(
                            excludes=["excludes"],
                            includes=["includes"]
                        ),
                        tags=codepipeline_mixins.CfnPipelinePropsMixin.GitTagFilterCriteriaProperty(
                            excludes=["excludes"],
                            includes=["includes"]
                        )
                    )],
                    source_action_name="sourceActionName"
                ),
                provider_type="providerType"
            )],
            variables=[codepipeline_mixins.CfnPipelinePropsMixin.VariableDeclarationProperty(
                default_value="defaultValue",
                description="description",
                name="name"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPipelineMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CodePipeline::Pipeline``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af084dc027d24553278d49c55455e8a7f1326e045152be9fd1064f9d646e17d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69b41fa00dd293d3b0574abc42111af62258d3835aaae5ca581420a3185bf9d4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__425c78f8f04f915c0f66b725dd69af6f042d6228b194eeef703b9c0fb4e563c5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPipelineMixinProps:
        return typing.cast(CfnPipelineMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.ActionDeclarationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_type_id": "actionTypeId",
            "commands": "commands",
            "configuration": "configuration",
            "environment_variables": "environmentVariables",
            "input_artifacts": "inputArtifacts",
            "name": "name",
            "namespace": "namespace",
            "output_artifacts": "outputArtifacts",
            "output_variables": "outputVariables",
            "region": "region",
            "role_arn": "roleArn",
            "run_order": "runOrder",
            "timeout_in_minutes": "timeoutInMinutes",
        },
    )
    class ActionDeclarationProperty:
        def __init__(
            self,
            *,
            action_type_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.ActionTypeIdProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            commands: typing.Optional[typing.Sequence[builtins.str]] = None,
            configuration: typing.Any = None,
            environment_variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.EnvironmentVariableProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            input_artifacts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.InputArtifactProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            name: typing.Optional[builtins.str] = None,
            namespace: typing.Optional[builtins.str] = None,
            output_artifacts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.OutputArtifactProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            output_variables: typing.Optional[typing.Sequence[builtins.str]] = None,
            region: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            run_order: typing.Optional[jsii.Number] = None,
            timeout_in_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Represents information about an action declaration.

            :param action_type_id: Specifies the action type and the provider of the action.
            :param commands: The shell commands to run with your compute action in CodePipeline. All commands are supported except multi-line formats. While CodeBuild logs and permissions are used, you do not need to create any resources in CodeBuild. .. epigraph:: Using compute time for this action will incur separate charges in AWS CodeBuild .
            :param configuration: The action's configuration. These are key-value pairs that specify input values for an action. For more information, see `Action Structure Requirements in CodePipeline <https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html#action-requirements>`_ . For the list of configuration properties for the AWS CloudFormation action type in CodePipeline, see `Configuration Properties Reference <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-action-reference.html>`_ in the *AWS CloudFormation User Guide* . For template snippets with examples, see `Using Parameter Override Functions with CodePipeline Pipelines <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-parameter-override-functions.html>`_ in the *AWS CloudFormation User Guide* . The values can be represented in either JSON or YAML format. For example, the JSON configuration item format is as follows: *JSON:* ``"Configuration" : { Key : Value },``
            :param environment_variables: The environment variables for the action.
            :param input_artifacts: The name or ID of the artifact consumed by the action, such as a test or build artifact. While the field is not a required parameter, most actions have an action configuration that requires a specified quantity of input artifacts. To refer to the action configuration specification by action provider, see the `Action structure reference <https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference.html>`_ in the *AWS CodePipeline User Guide* . .. epigraph:: For a CodeBuild action with multiple input artifacts, one of your input sources must be designated the PrimarySource. For more information, see the `CodeBuild action reference page <https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-CodeBuild.html>`_ in the *AWS CodePipeline User Guide* .
            :param name: The action declaration's name.
            :param namespace: The variable namespace associated with the action. All variables produced as output by this action fall under this namespace.
            :param output_artifacts: The name or ID of the result of the action declaration, such as a test or build artifact. While the field is not a required parameter, most actions have an action configuration that requires a specified quantity of output artifacts. To refer to the action configuration specification by action provider, see the `Action structure reference <https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference.html>`_ in the *AWS CodePipeline User Guide* .
            :param output_variables: The list of variables that are to be exported from the compute action. This is specifically CodeBuild environment variables as used for that action.
            :param region: The action declaration's AWS Region, such as us-east-1.
            :param role_arn: The ARN of the IAM service role that performs the declared action. This is assumed through the roleArn for the pipeline.
            :param run_order: The order in which actions are run.
            :param timeout_in_minutes: A timeout duration in minutes that can be applied against the ActionType’s default timeout value specified in `Quotas for AWS CodePipeline <https://docs.aws.amazon.com/codepipeline/latest/userguide/limits.html>`_ . This attribute is available only to the manual approval ActionType.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-actiondeclaration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                # configuration: Any
                
                action_declaration_property = codepipeline_mixins.CfnPipelinePropsMixin.ActionDeclarationProperty(
                    action_type_id=codepipeline_mixins.CfnPipelinePropsMixin.ActionTypeIdProperty(
                        category="category",
                        owner="owner",
                        provider="provider",
                        version="version"
                    ),
                    commands=["commands"],
                    configuration=configuration,
                    environment_variables=[codepipeline_mixins.CfnPipelinePropsMixin.EnvironmentVariableProperty(
                        name="name",
                        type="type",
                        value="value"
                    )],
                    input_artifacts=[codepipeline_mixins.CfnPipelinePropsMixin.InputArtifactProperty(
                        name="name"
                    )],
                    name="name",
                    namespace="namespace",
                    output_artifacts=[codepipeline_mixins.CfnPipelinePropsMixin.OutputArtifactProperty(
                        files=["files"],
                        name="name"
                    )],
                    output_variables=["outputVariables"],
                    region="region",
                    role_arn="roleArn",
                    run_order=123,
                    timeout_in_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9d433e1125bd269371b29aff4978048a5c92cc3708e352333a25b776b645b207)
                check_type(argname="argument action_type_id", value=action_type_id, expected_type=type_hints["action_type_id"])
                check_type(argname="argument commands", value=commands, expected_type=type_hints["commands"])
                check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
                check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
                check_type(argname="argument input_artifacts", value=input_artifacts, expected_type=type_hints["input_artifacts"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
                check_type(argname="argument output_artifacts", value=output_artifacts, expected_type=type_hints["output_artifacts"])
                check_type(argname="argument output_variables", value=output_variables, expected_type=type_hints["output_variables"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument run_order", value=run_order, expected_type=type_hints["run_order"])
                check_type(argname="argument timeout_in_minutes", value=timeout_in_minutes, expected_type=type_hints["timeout_in_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action_type_id is not None:
                self._values["action_type_id"] = action_type_id
            if commands is not None:
                self._values["commands"] = commands
            if configuration is not None:
                self._values["configuration"] = configuration
            if environment_variables is not None:
                self._values["environment_variables"] = environment_variables
            if input_artifacts is not None:
                self._values["input_artifacts"] = input_artifacts
            if name is not None:
                self._values["name"] = name
            if namespace is not None:
                self._values["namespace"] = namespace
            if output_artifacts is not None:
                self._values["output_artifacts"] = output_artifacts
            if output_variables is not None:
                self._values["output_variables"] = output_variables
            if region is not None:
                self._values["region"] = region
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if run_order is not None:
                self._values["run_order"] = run_order
            if timeout_in_minutes is not None:
                self._values["timeout_in_minutes"] = timeout_in_minutes

        @builtins.property
        def action_type_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ActionTypeIdProperty"]]:
            '''Specifies the action type and the provider of the action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-actiondeclaration.html#cfn-codepipeline-pipeline-actiondeclaration-actiontypeid
            '''
            result = self._values.get("action_type_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ActionTypeIdProperty"]], result)

        @builtins.property
        def commands(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The shell commands to run with your compute action in CodePipeline.

            All commands are supported except multi-line formats. While CodeBuild logs and permissions are used, you do not need to create any resources in CodeBuild.
            .. epigraph::

               Using compute time for this action will incur separate charges in AWS CodeBuild .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-actiondeclaration.html#cfn-codepipeline-pipeline-actiondeclaration-commands
            '''
            result = self._values.get("commands")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def configuration(self) -> typing.Any:
            '''The action's configuration.

            These are key-value pairs that specify input values for an action. For more information, see `Action Structure Requirements in CodePipeline <https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html#action-requirements>`_ . For the list of configuration properties for the AWS CloudFormation action type in CodePipeline, see `Configuration Properties Reference <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-action-reference.html>`_ in the *AWS CloudFormation User Guide* . For template snippets with examples, see `Using Parameter Override Functions with CodePipeline Pipelines <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-parameter-override-functions.html>`_ in the *AWS CloudFormation User Guide* .

            The values can be represented in either JSON or YAML format. For example, the JSON configuration item format is as follows:

            *JSON:*

            ``"Configuration" : { Key : Value },``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-actiondeclaration.html#cfn-codepipeline-pipeline-actiondeclaration-configuration
            '''
            result = self._values.get("configuration")
            return typing.cast(typing.Any, result)

        @builtins.property
        def environment_variables(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.EnvironmentVariableProperty"]]]]:
            '''The environment variables for the action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-actiondeclaration.html#cfn-codepipeline-pipeline-actiondeclaration-environmentvariables
            '''
            result = self._values.get("environment_variables")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.EnvironmentVariableProperty"]]]], result)

        @builtins.property
        def input_artifacts(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.InputArtifactProperty"]]]]:
            '''The name or ID of the artifact consumed by the action, such as a test or build artifact.

            While the field is not a required parameter, most actions have an action configuration that requires a specified quantity of input artifacts. To refer to the action configuration specification by action provider, see the `Action structure reference <https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference.html>`_ in the *AWS CodePipeline User Guide* .
            .. epigraph::

               For a CodeBuild action with multiple input artifacts, one of your input sources must be designated the PrimarySource. For more information, see the `CodeBuild action reference page <https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-CodeBuild.html>`_ in the *AWS CodePipeline User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-actiondeclaration.html#cfn-codepipeline-pipeline-actiondeclaration-inputartifacts
            '''
            result = self._values.get("input_artifacts")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.InputArtifactProperty"]]]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The action declaration's name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-actiondeclaration.html#cfn-codepipeline-pipeline-actiondeclaration-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''The variable namespace associated with the action.

            All variables produced as output by this action fall under this namespace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-actiondeclaration.html#cfn-codepipeline-pipeline-actiondeclaration-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def output_artifacts(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.OutputArtifactProperty"]]]]:
            '''The name or ID of the result of the action declaration, such as a test or build artifact.

            While the field is not a required parameter, most actions have an action configuration that requires a specified quantity of output artifacts. To refer to the action configuration specification by action provider, see the `Action structure reference <https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference.html>`_ in the *AWS CodePipeline User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-actiondeclaration.html#cfn-codepipeline-pipeline-actiondeclaration-outputartifacts
            '''
            result = self._values.get("output_artifacts")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.OutputArtifactProperty"]]]], result)

        @builtins.property
        def output_variables(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of variables that are to be exported from the compute action.

            This is specifically CodeBuild environment variables as used for that action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-actiondeclaration.html#cfn-codepipeline-pipeline-actiondeclaration-outputvariables
            '''
            result = self._values.get("output_variables")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The action declaration's AWS Region, such as us-east-1.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-actiondeclaration.html#cfn-codepipeline-pipeline-actiondeclaration-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM service role that performs the declared action.

            This is assumed through the roleArn for the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-actiondeclaration.html#cfn-codepipeline-pipeline-actiondeclaration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def run_order(self) -> typing.Optional[jsii.Number]:
            '''The order in which actions are run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-actiondeclaration.html#cfn-codepipeline-pipeline-actiondeclaration-runorder
            '''
            result = self._values.get("run_order")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''A timeout duration in minutes that can be applied against the ActionType’s default timeout value specified in `Quotas for AWS CodePipeline <https://docs.aws.amazon.com/codepipeline/latest/userguide/limits.html>`_ . This attribute is available only to the manual approval ActionType.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-actiondeclaration.html#cfn-codepipeline-pipeline-actiondeclaration-timeoutinminutes
            '''
            result = self._values.get("timeout_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionDeclarationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.ActionTypeIdProperty",
        jsii_struct_bases=[],
        name_mapping={
            "category": "category",
            "owner": "owner",
            "provider": "provider",
            "version": "version",
        },
    )
    class ActionTypeIdProperty:
        def __init__(
            self,
            *,
            category: typing.Optional[builtins.str] = None,
            owner: typing.Optional[builtins.str] = None,
            provider: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents information about an action type.

            :param category: A category defines what kind of action can be taken in the stage, and constrains the provider type for the action. Valid categories are limited to one of the values below. - ``Source`` - ``Build`` - ``Test`` - ``Deploy`` - ``Invoke`` - ``Approval`` - ``Compute``
            :param owner: The creator of the action being called. There are three valid values for the ``Owner`` field in the action category section within your pipeline structure: ``AWS`` , ``ThirdParty`` , and ``Custom`` . For more information, see `Valid Action Types and Providers in CodePipeline <https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html#actions-valid-providers>`_ .
            :param provider: The provider of the service being called by the action. Valid providers are determined by the action category. For example, an action in the Deploy category type might have a provider of CodeDeploy, which would be specified as ``CodeDeploy`` . For more information, see `Valid Action Types and Providers in CodePipeline <https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html#actions-valid-providers>`_ .
            :param version: A string that describes the action version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-actiontypeid.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                action_type_id_property = codepipeline_mixins.CfnPipelinePropsMixin.ActionTypeIdProperty(
                    category="category",
                    owner="owner",
                    provider="provider",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f965b3a23aff9ce371ff0d47df50a4b81d5912d5f0986e69338c87c80c39b716)
                check_type(argname="argument category", value=category, expected_type=type_hints["category"])
                check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
                check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if category is not None:
                self._values["category"] = category
            if owner is not None:
                self._values["owner"] = owner
            if provider is not None:
                self._values["provider"] = provider
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def category(self) -> typing.Optional[builtins.str]:
            '''A category defines what kind of action can be taken in the stage, and constrains the provider type for the action.

            Valid categories are limited to one of the values below.

            - ``Source``
            - ``Build``
            - ``Test``
            - ``Deploy``
            - ``Invoke``
            - ``Approval``
            - ``Compute``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-actiontypeid.html#cfn-codepipeline-pipeline-actiontypeid-category
            '''
            result = self._values.get("category")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def owner(self) -> typing.Optional[builtins.str]:
            '''The creator of the action being called.

            There are three valid values for the ``Owner`` field in the action category section within your pipeline structure: ``AWS`` , ``ThirdParty`` , and ``Custom`` . For more information, see `Valid Action Types and Providers in CodePipeline <https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html#actions-valid-providers>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-actiontypeid.html#cfn-codepipeline-pipeline-actiontypeid-owner
            '''
            result = self._values.get("owner")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def provider(self) -> typing.Optional[builtins.str]:
            '''The provider of the service being called by the action.

            Valid providers are determined by the action category. For example, an action in the Deploy category type might have a provider of CodeDeploy, which would be specified as ``CodeDeploy`` . For more information, see `Valid Action Types and Providers in CodePipeline <https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html#actions-valid-providers>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-actiontypeid.html#cfn-codepipeline-pipeline-actiontypeid-provider
            '''
            result = self._values.get("provider")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''A string that describes the action version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-actiontypeid.html#cfn-codepipeline-pipeline-actiontypeid-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionTypeIdProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.ArtifactStoreMapProperty",
        jsii_struct_bases=[],
        name_mapping={"artifact_store": "artifactStore", "region": "region"},
    )
    class ArtifactStoreMapProperty:
        def __init__(
            self,
            *,
            artifact_store: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.ArtifactStoreProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A mapping of ``artifactStore`` objects and their corresponding AWS Regions.

            There must be an artifact store for the pipeline Region and for each cross-region action in the pipeline.
            .. epigraph::

               You must include either ``artifactStore`` or ``artifactStores`` in your pipeline, but you cannot use both. If you create a cross-region action in your pipeline, you must use ``artifactStores`` .

            :param artifact_store: Represents information about the S3 bucket where artifacts are stored for the pipeline. .. epigraph:: You must include either ``artifactStore`` or ``artifactStores`` in your pipeline, but you cannot use both. If you create a cross-region action in your pipeline, you must use ``artifactStores`` .
            :param region: The action declaration's AWS Region, such as us-east-1.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstoremap.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                artifact_store_map_property = codepipeline_mixins.CfnPipelinePropsMixin.ArtifactStoreMapProperty(
                    artifact_store=codepipeline_mixins.CfnPipelinePropsMixin.ArtifactStoreProperty(
                        encryption_key=codepipeline_mixins.CfnPipelinePropsMixin.EncryptionKeyProperty(
                            id="id",
                            type="type"
                        ),
                        location="location",
                        type="type"
                    ),
                    region="region"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6e260480aa2bb682c65b5e475ac050756c0f85c28d8d26073536c8c79a08ade3)
                check_type(argname="argument artifact_store", value=artifact_store, expected_type=type_hints["artifact_store"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if artifact_store is not None:
                self._values["artifact_store"] = artifact_store
            if region is not None:
                self._values["region"] = region

        @builtins.property
        def artifact_store(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ArtifactStoreProperty"]]:
            '''Represents information about the S3 bucket where artifacts are stored for the pipeline.

            .. epigraph::

               You must include either ``artifactStore`` or ``artifactStores`` in your pipeline, but you cannot use both. If you create a cross-region action in your pipeline, you must use ``artifactStores`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstoremap.html#cfn-codepipeline-pipeline-artifactstoremap-artifactstore
            '''
            result = self._values.get("artifact_store")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ArtifactStoreProperty"]], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The action declaration's AWS Region, such as us-east-1.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstoremap.html#cfn-codepipeline-pipeline-artifactstoremap-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ArtifactStoreMapProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.ArtifactStoreProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption_key": "encryptionKey",
            "location": "location",
            "type": "type",
        },
    )
    class ArtifactStoreProperty:
        def __init__(
            self,
            *,
            encryption_key: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.EncryptionKeyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            location: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The S3 bucket where artifacts for the pipeline are stored.

            .. epigraph::

               You must include either ``artifactStore`` or ``artifactStores`` in your pipeline, but you cannot use both. If you create a cross-region action in your pipeline, you must use ``artifactStores`` .

            :param encryption_key: The encryption key used to encrypt the data in the artifact store, such as an AWS Key Management Service ( AWS KMS) key. If this is undefined, the default key for Amazon S3 is used. To see an example artifact store encryption key field, see the example structure here: `AWS::CodePipeline::Pipeline <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html>`_ .
            :param location: The S3 bucket used for storing the artifacts for a pipeline. You can specify the name of an S3 bucket but not a folder in the bucket. A folder to contain the pipeline artifacts is created for you based on the name of the pipeline. You can use any S3 bucket in the same AWS Region as the pipeline to store your pipeline artifacts.
            :param type: The type of the artifact store, such as S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstore.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                artifact_store_property = codepipeline_mixins.CfnPipelinePropsMixin.ArtifactStoreProperty(
                    encryption_key=codepipeline_mixins.CfnPipelinePropsMixin.EncryptionKeyProperty(
                        id="id",
                        type="type"
                    ),
                    location="location",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f227a9f1f148c71e2964f7c596cc4d1f7b302e0550d4c3a4185332e898611230)
                check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
                check_type(argname="argument location", value=location, expected_type=type_hints["location"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_key is not None:
                self._values["encryption_key"] = encryption_key
            if location is not None:
                self._values["location"] = location
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def encryption_key(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.EncryptionKeyProperty"]]:
            '''The encryption key used to encrypt the data in the artifact store, such as an AWS Key Management Service ( AWS KMS) key.

            If this is undefined, the default key for Amazon S3 is used. To see an example artifact store encryption key field, see the example structure here: `AWS::CodePipeline::Pipeline <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstore.html#cfn-codepipeline-pipeline-artifactstore-encryptionkey
            '''
            result = self._values.get("encryption_key")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.EncryptionKeyProperty"]], result)

        @builtins.property
        def location(self) -> typing.Optional[builtins.str]:
            '''The S3 bucket used for storing the artifacts for a pipeline.

            You can specify the name of an S3 bucket but not a folder in the bucket. A folder to contain the pipeline artifacts is created for you based on the name of the pipeline. You can use any S3 bucket in the same AWS Region as the pipeline to store your pipeline artifacts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstore.html#cfn-codepipeline-pipeline-artifactstore-location
            '''
            result = self._values.get("location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of the artifact store, such as S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstore.html#cfn-codepipeline-pipeline-artifactstore-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ArtifactStoreProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.BeforeEntryConditionsProperty",
        jsii_struct_bases=[],
        name_mapping={"conditions": "conditions"},
    )
    class BeforeEntryConditionsProperty:
        def __init__(
            self,
            *,
            conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.ConditionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The conditions for making checks for entry to a stage.

            For more information about conditions, see `Stage conditions <https://docs.aws.amazon.com/codepipeline/latest/userguide/stage-conditions.html>`_ and `How do stage conditions work? <https://docs.aws.amazon.com/codepipeline/latest/userguide/concepts-how-it-works-conditions.html>`_ .

            :param conditions: The conditions that are configured as entry conditions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-beforeentryconditions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                # configuration: Any
                
                before_entry_conditions_property = codepipeline_mixins.CfnPipelinePropsMixin.BeforeEntryConditionsProperty(
                    conditions=[codepipeline_mixins.CfnPipelinePropsMixin.ConditionProperty(
                        result="result",
                        rules=[codepipeline_mixins.CfnPipelinePropsMixin.RuleDeclarationProperty(
                            commands=["commands"],
                            configuration=configuration,
                            input_artifacts=[codepipeline_mixins.CfnPipelinePropsMixin.InputArtifactProperty(
                                name="name"
                            )],
                            name="name",
                            region="region",
                            role_arn="roleArn",
                            rule_type_id=codepipeline_mixins.CfnPipelinePropsMixin.RuleTypeIdProperty(
                                category="category",
                                owner="owner",
                                provider="provider",
                                version="version"
                            )
                        )]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2aacaec593dbfd9dd29f9c66358264650201d6d9ad1019bd4fc87694a0c3a621)
                check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if conditions is not None:
                self._values["conditions"] = conditions

        @builtins.property
        def conditions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ConditionProperty"]]]]:
            '''The conditions that are configured as entry conditions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-beforeentryconditions.html#cfn-codepipeline-pipeline-beforeentryconditions-conditions
            '''
            result = self._values.get("conditions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ConditionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BeforeEntryConditionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.BlockerDeclarationProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "type": "type"},
    )
    class BlockerDeclarationProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Reserved for future use.

            :param name: Reserved for future use.
            :param type: Reserved for future use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-blockerdeclaration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                blocker_declaration_property = codepipeline_mixins.CfnPipelinePropsMixin.BlockerDeclarationProperty(
                    name="name",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__abb36ad50ae375f0766204e0a077c8fda8caeb34570c5b8183027103587d3b1f)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''Reserved for future use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-blockerdeclaration.html#cfn-codepipeline-pipeline-blockerdeclaration-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Reserved for future use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-blockerdeclaration.html#cfn-codepipeline-pipeline-blockerdeclaration-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BlockerDeclarationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.ConditionProperty",
        jsii_struct_bases=[],
        name_mapping={"result": "result", "rules": "rules"},
    )
    class ConditionProperty:
        def __init__(
            self,
            *,
            result: typing.Optional[builtins.str] = None,
            rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.RuleDeclarationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The condition for the stage.

            A condition is made up of the rules and the result for the condition. For more information about conditions, see `Stage conditions <https://docs.aws.amazon.com/codepipeline/latest/userguide/stage-conditions.html>`_ and `How do stage conditions work? <https://docs.aws.amazon.com/codepipeline/latest/userguide/concepts-how-it-works-conditions.html>`_ .. For more information about rules, see the `AWS CodePipeline rule reference <https://docs.aws.amazon.com/codepipeline/latest/userguide/rule-reference.html>`_ .

            :param result: The action to be done when the condition is met. For example, rolling back an execution for a failure condition.
            :param rules: The rules that make up the condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-condition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                # configuration: Any
                
                condition_property = codepipeline_mixins.CfnPipelinePropsMixin.ConditionProperty(
                    result="result",
                    rules=[codepipeline_mixins.CfnPipelinePropsMixin.RuleDeclarationProperty(
                        commands=["commands"],
                        configuration=configuration,
                        input_artifacts=[codepipeline_mixins.CfnPipelinePropsMixin.InputArtifactProperty(
                            name="name"
                        )],
                        name="name",
                        region="region",
                        role_arn="roleArn",
                        rule_type_id=codepipeline_mixins.CfnPipelinePropsMixin.RuleTypeIdProperty(
                            category="category",
                            owner="owner",
                            provider="provider",
                            version="version"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__572957f44fc3462421e016a13546f972e73c2b8e88a2a64da961a9d09cd46838)
                check_type(argname="argument result", value=result, expected_type=type_hints["result"])
                check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if result is not None:
                self._values["result"] = result
            if rules is not None:
                self._values["rules"] = rules

        @builtins.property
        def result(self) -> typing.Optional[builtins.str]:
            '''The action to be done when the condition is met.

            For example, rolling back an execution for a failure condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-condition.html#cfn-codepipeline-pipeline-condition-result
            '''
            result = self._values.get("result")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.RuleDeclarationProperty"]]]]:
            '''The rules that make up the condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-condition.html#cfn-codepipeline-pipeline-condition-rules
            '''
            result = self._values.get("rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.RuleDeclarationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.EncryptionKeyProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "type": "type"},
    )
    class EncryptionKeyProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents information about the key used to encrypt data in the artifact store, such as an AWS Key Management Service ( AWS KMS) key.

            ``EncryptionKey`` is a property of the `ArtifactStore <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstore.html>`_ property type.

            :param id: The ID used to identify the key. For an AWS KMS key, you can use the key ID, the key ARN, or the alias ARN. .. epigraph:: Aliases are recognized only in the account that created the AWS key. For cross-account actions, you can only use the key ID or key ARN to identify the key. Cross-account actions involve using the role from the other account (AccountB), so specifying the key ID will use the key from the other account (AccountB).
            :param type: The type of encryption key, such as an AWS KMS key. When creating or updating a pipeline, the value must be set to 'KMS'.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-encryptionkey.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                encryption_key_property = codepipeline_mixins.CfnPipelinePropsMixin.EncryptionKeyProperty(
                    id="id",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__82109c33648c199a02180b3de9ea7130fea6437804f30fca3c910d77f45f4d75)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The ID used to identify the key.

            For an AWS KMS key, you can use the key ID, the key ARN, or the alias ARN.
            .. epigraph::

               Aliases are recognized only in the account that created the AWS  key. For cross-account actions, you can only use the key ID or key ARN to identify the key. Cross-account actions involve using the role from the other account (AccountB), so specifying the key ID will use the key from the other account (AccountB).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-encryptionkey.html#cfn-codepipeline-pipeline-encryptionkey-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of encryption key, such as an AWS KMS key.

            When creating or updating a pipeline, the value must be set to 'KMS'.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-encryptionkey.html#cfn-codepipeline-pipeline-encryptionkey-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionKeyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.EnvironmentVariableProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "type": "type", "value": "value"},
    )
    class EnvironmentVariableProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The environment variables for the action.

            :param name: The environment variable name in the key-value pair.
            :param type: Specifies the type of use for the environment variable value. The value can be either ``PLAINTEXT`` or ``SECRETS_MANAGER`` . If the value is ``SECRETS_MANAGER`` , provide the Secrets reference in the EnvironmentVariable value.
            :param value: The environment variable value in the key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-environmentvariable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                environment_variable_property = codepipeline_mixins.CfnPipelinePropsMixin.EnvironmentVariableProperty(
                    name="name",
                    type="type",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3d65dc39e16a4d9d70b9371d81c28f393ae655dc6c965d13d73872554e4b9b18)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The environment variable name in the key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-environmentvariable.html#cfn-codepipeline-pipeline-environmentvariable-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of use for the environment variable value.

            The value can be either ``PLAINTEXT`` or ``SECRETS_MANAGER`` . If the value is ``SECRETS_MANAGER`` , provide the Secrets reference in the EnvironmentVariable value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-environmentvariable.html#cfn-codepipeline-pipeline-environmentvariable-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The environment variable value in the key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-environmentvariable.html#cfn-codepipeline-pipeline-environmentvariable-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentVariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.FailureConditionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "conditions": "conditions",
            "result": "result",
            "retry_configuration": "retryConfiguration",
        },
    )
    class FailureConditionsProperty:
        def __init__(
            self,
            *,
            conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.ConditionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            result: typing.Optional[builtins.str] = None,
            retry_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.RetryConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration that specifies the result, such as rollback, to occur upon stage failure.

            For more information about conditions, see `Stage conditions <https://docs.aws.amazon.com/codepipeline/latest/userguide/stage-conditions.html>`_ and `How do stage conditions work? <https://docs.aws.amazon.com/codepipeline/latest/userguide/concepts-how-it-works-conditions.html>`_ .

            :param conditions: The conditions that are configured as failure conditions. For more information about conditions, see `Stage conditions <https://docs.aws.amazon.com/codepipeline/latest/userguide/stage-conditions.html>`_ and `How do stage conditions work? <https://docs.aws.amazon.com/codepipeline/latest/userguide/concepts-how-it-works-conditions.html>`_ .
            :param result: The specified result for when the failure conditions are met, such as rolling back the stage.
            :param retry_configuration: The retry configuration specifies automatic retry for a failed stage, along with the configured retry mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-failureconditions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                # configuration: Any
                
                failure_conditions_property = codepipeline_mixins.CfnPipelinePropsMixin.FailureConditionsProperty(
                    conditions=[codepipeline_mixins.CfnPipelinePropsMixin.ConditionProperty(
                        result="result",
                        rules=[codepipeline_mixins.CfnPipelinePropsMixin.RuleDeclarationProperty(
                            commands=["commands"],
                            configuration=configuration,
                            input_artifacts=[codepipeline_mixins.CfnPipelinePropsMixin.InputArtifactProperty(
                                name="name"
                            )],
                            name="name",
                            region="region",
                            role_arn="roleArn",
                            rule_type_id=codepipeline_mixins.CfnPipelinePropsMixin.RuleTypeIdProperty(
                                category="category",
                                owner="owner",
                                provider="provider",
                                version="version"
                            )
                        )]
                    )],
                    result="result",
                    retry_configuration=codepipeline_mixins.CfnPipelinePropsMixin.RetryConfigurationProperty(
                        retry_mode="retryMode"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__71f3996b49de5892b88e7157ef423a32d80597dc638cdef577efd10bc302ab00)
                check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
                check_type(argname="argument result", value=result, expected_type=type_hints["result"])
                check_type(argname="argument retry_configuration", value=retry_configuration, expected_type=type_hints["retry_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if conditions is not None:
                self._values["conditions"] = conditions
            if result is not None:
                self._values["result"] = result
            if retry_configuration is not None:
                self._values["retry_configuration"] = retry_configuration

        @builtins.property
        def conditions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ConditionProperty"]]]]:
            '''The conditions that are configured as failure conditions.

            For more information about conditions, see `Stage conditions <https://docs.aws.amazon.com/codepipeline/latest/userguide/stage-conditions.html>`_ and `How do stage conditions work? <https://docs.aws.amazon.com/codepipeline/latest/userguide/concepts-how-it-works-conditions.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-failureconditions.html#cfn-codepipeline-pipeline-failureconditions-conditions
            '''
            result = self._values.get("conditions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ConditionProperty"]]]], result)

        @builtins.property
        def result(self) -> typing.Optional[builtins.str]:
            '''The specified result for when the failure conditions are met, such as rolling back the stage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-failureconditions.html#cfn-codepipeline-pipeline-failureconditions-result
            '''
            result = self._values.get("result")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def retry_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.RetryConfigurationProperty"]]:
            '''The retry configuration specifies automatic retry for a failed stage, along with the configured retry mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-failureconditions.html#cfn-codepipeline-pipeline-failureconditions-retryconfiguration
            '''
            result = self._values.get("retry_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.RetryConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FailureConditionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.GitBranchFilterCriteriaProperty",
        jsii_struct_bases=[],
        name_mapping={"excludes": "excludes", "includes": "includes"},
    )
    class GitBranchFilterCriteriaProperty:
        def __init__(
            self,
            *,
            excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
            includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The Git repository branches specified as filter criteria to start the pipeline.

            :param excludes: The list of patterns of Git branches that, when a commit is pushed, are to be excluded from starting the pipeline.
            :param includes: The list of patterns of Git branches that, when a commit is pushed, are to be included as criteria that starts the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitbranchfiltercriteria.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                git_branch_filter_criteria_property = codepipeline_mixins.CfnPipelinePropsMixin.GitBranchFilterCriteriaProperty(
                    excludes=["excludes"],
                    includes=["includes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2baf1be6ecb656bb9a9ced289a5a4c192e57b2255865c32e2c92e3f6df7f82a7)
                check_type(argname="argument excludes", value=excludes, expected_type=type_hints["excludes"])
                check_type(argname="argument includes", value=includes, expected_type=type_hints["includes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if excludes is not None:
                self._values["excludes"] = excludes
            if includes is not None:
                self._values["includes"] = includes

        @builtins.property
        def excludes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of patterns of Git branches that, when a commit is pushed, are to be excluded from starting the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitbranchfiltercriteria.html#cfn-codepipeline-pipeline-gitbranchfiltercriteria-excludes
            '''
            result = self._values.get("excludes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def includes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of patterns of Git branches that, when a commit is pushed, are to be included as criteria that starts the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitbranchfiltercriteria.html#cfn-codepipeline-pipeline-gitbranchfiltercriteria-includes
            '''
            result = self._values.get("includes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GitBranchFilterCriteriaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.GitConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "pull_request": "pullRequest",
            "push": "push",
            "source_action_name": "sourceActionName",
        },
    )
    class GitConfigurationProperty:
        def __init__(
            self,
            *,
            pull_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.GitPullRequestFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            push: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.GitPushFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            source_action_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A type of trigger configuration for Git-based source actions.

            .. epigraph::

               You can specify the Git configuration trigger type for all third-party Git-based source actions that are supported by the ``CodeStarSourceConnection`` action type.

            :param pull_request: The field where the repository event that will start the pipeline is specified as pull requests.
            :param push: The field where the repository event that will start the pipeline, such as pushing Git tags, is specified with details.
            :param source_action_name: The name of the pipeline source action where the trigger configuration, such as Git tags, is specified. The trigger configuration will start the pipeline upon the specified change only. .. epigraph:: You can only specify one trigger configuration per source action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                git_configuration_property = codepipeline_mixins.CfnPipelinePropsMixin.GitConfigurationProperty(
                    pull_request=[codepipeline_mixins.CfnPipelinePropsMixin.GitPullRequestFilterProperty(
                        branches=codepipeline_mixins.CfnPipelinePropsMixin.GitBranchFilterCriteriaProperty(
                            excludes=["excludes"],
                            includes=["includes"]
                        ),
                        events=["events"],
                        file_paths=codepipeline_mixins.CfnPipelinePropsMixin.GitFilePathFilterCriteriaProperty(
                            excludes=["excludes"],
                            includes=["includes"]
                        )
                    )],
                    push=[codepipeline_mixins.CfnPipelinePropsMixin.GitPushFilterProperty(
                        branches=codepipeline_mixins.CfnPipelinePropsMixin.GitBranchFilterCriteriaProperty(
                            excludes=["excludes"],
                            includes=["includes"]
                        ),
                        file_paths=codepipeline_mixins.CfnPipelinePropsMixin.GitFilePathFilterCriteriaProperty(
                            excludes=["excludes"],
                            includes=["includes"]
                        ),
                        tags=codepipeline_mixins.CfnPipelinePropsMixin.GitTagFilterCriteriaProperty(
                            excludes=["excludes"],
                            includes=["includes"]
                        )
                    )],
                    source_action_name="sourceActionName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c5825ed32f11fc92cc69832820cff29da074394b40492a8b1e4c7e644e4ab7ac)
                check_type(argname="argument pull_request", value=pull_request, expected_type=type_hints["pull_request"])
                check_type(argname="argument push", value=push, expected_type=type_hints["push"])
                check_type(argname="argument source_action_name", value=source_action_name, expected_type=type_hints["source_action_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if pull_request is not None:
                self._values["pull_request"] = pull_request
            if push is not None:
                self._values["push"] = push
            if source_action_name is not None:
                self._values["source_action_name"] = source_action_name

        @builtins.property
        def pull_request(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.GitPullRequestFilterProperty"]]]]:
            '''The field where the repository event that will start the pipeline is specified as pull requests.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitconfiguration.html#cfn-codepipeline-pipeline-gitconfiguration-pullrequest
            '''
            result = self._values.get("pull_request")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.GitPullRequestFilterProperty"]]]], result)

        @builtins.property
        def push(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.GitPushFilterProperty"]]]]:
            '''The field where the repository event that will start the pipeline, such as pushing Git tags, is specified with details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitconfiguration.html#cfn-codepipeline-pipeline-gitconfiguration-push
            '''
            result = self._values.get("push")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.GitPushFilterProperty"]]]], result)

        @builtins.property
        def source_action_name(self) -> typing.Optional[builtins.str]:
            '''The name of the pipeline source action where the trigger configuration, such as Git tags, is specified.

            The trigger configuration will start the pipeline upon the specified change only.
            .. epigraph::

               You can only specify one trigger configuration per source action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitconfiguration.html#cfn-codepipeline-pipeline-gitconfiguration-sourceactionname
            '''
            result = self._values.get("source_action_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GitConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.GitFilePathFilterCriteriaProperty",
        jsii_struct_bases=[],
        name_mapping={"excludes": "excludes", "includes": "includes"},
    )
    class GitFilePathFilterCriteriaProperty:
        def __init__(
            self,
            *,
            excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
            includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The Git repository file paths specified as filter criteria to start the pipeline.

            :param excludes: The list of patterns of Git repository file paths that, when a commit is pushed, are to be excluded from starting the pipeline.
            :param includes: The list of patterns of Git repository file paths that, when a commit is pushed, are to be included as criteria that starts the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitfilepathfiltercriteria.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                git_file_path_filter_criteria_property = codepipeline_mixins.CfnPipelinePropsMixin.GitFilePathFilterCriteriaProperty(
                    excludes=["excludes"],
                    includes=["includes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__52413dc4a7cbaaea180d735d2d681723caed88e3b8222b09875b4ed74ffa726e)
                check_type(argname="argument excludes", value=excludes, expected_type=type_hints["excludes"])
                check_type(argname="argument includes", value=includes, expected_type=type_hints["includes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if excludes is not None:
                self._values["excludes"] = excludes
            if includes is not None:
                self._values["includes"] = includes

        @builtins.property
        def excludes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of patterns of Git repository file paths that, when a commit is pushed, are to be excluded from starting the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitfilepathfiltercriteria.html#cfn-codepipeline-pipeline-gitfilepathfiltercriteria-excludes
            '''
            result = self._values.get("excludes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def includes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of patterns of Git repository file paths that, when a commit is pushed, are to be included as criteria that starts the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitfilepathfiltercriteria.html#cfn-codepipeline-pipeline-gitfilepathfiltercriteria-includes
            '''
            result = self._values.get("includes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GitFilePathFilterCriteriaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.GitPullRequestFilterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "branches": "branches",
            "events": "events",
            "file_paths": "filePaths",
        },
    )
    class GitPullRequestFilterProperty:
        def __init__(
            self,
            *,
            branches: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.GitBranchFilterCriteriaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            events: typing.Optional[typing.Sequence[builtins.str]] = None,
            file_paths: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.GitFilePathFilterCriteriaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The event criteria for the pull request trigger configuration, such as the lists of branches or file paths to include and exclude.

            The following are valid values for the events for this filter:

            - CLOSED
            - OPEN
            - UPDATED

            :param branches: The field that specifies to filter on branches for the pull request trigger configuration.
            :param events: The field that specifies which pull request events to filter on (OPEN, UPDATED, CLOSED) for the trigger configuration.
            :param file_paths: The field that specifies to filter on file paths for the pull request trigger configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitpullrequestfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                git_pull_request_filter_property = codepipeline_mixins.CfnPipelinePropsMixin.GitPullRequestFilterProperty(
                    branches=codepipeline_mixins.CfnPipelinePropsMixin.GitBranchFilterCriteriaProperty(
                        excludes=["excludes"],
                        includes=["includes"]
                    ),
                    events=["events"],
                    file_paths=codepipeline_mixins.CfnPipelinePropsMixin.GitFilePathFilterCriteriaProperty(
                        excludes=["excludes"],
                        includes=["includes"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ed91e4ded9d738cf24838b3d2cddc1c86fb9be7bc1a138bf12f052be2460bed9)
                check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
                check_type(argname="argument events", value=events, expected_type=type_hints["events"])
                check_type(argname="argument file_paths", value=file_paths, expected_type=type_hints["file_paths"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if branches is not None:
                self._values["branches"] = branches
            if events is not None:
                self._values["events"] = events
            if file_paths is not None:
                self._values["file_paths"] = file_paths

        @builtins.property
        def branches(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.GitBranchFilterCriteriaProperty"]]:
            '''The field that specifies to filter on branches for the pull request trigger configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitpullrequestfilter.html#cfn-codepipeline-pipeline-gitpullrequestfilter-branches
            '''
            result = self._values.get("branches")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.GitBranchFilterCriteriaProperty"]], result)

        @builtins.property
        def events(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The field that specifies which pull request events to filter on (OPEN, UPDATED, CLOSED) for the trigger configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitpullrequestfilter.html#cfn-codepipeline-pipeline-gitpullrequestfilter-events
            '''
            result = self._values.get("events")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def file_paths(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.GitFilePathFilterCriteriaProperty"]]:
            '''The field that specifies to filter on file paths for the pull request trigger configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitpullrequestfilter.html#cfn-codepipeline-pipeline-gitpullrequestfilter-filepaths
            '''
            result = self._values.get("file_paths")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.GitFilePathFilterCriteriaProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GitPullRequestFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.GitPushFilterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "branches": "branches",
            "file_paths": "filePaths",
            "tags": "tags",
        },
    )
    class GitPushFilterProperty:
        def __init__(
            self,
            *,
            branches: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.GitBranchFilterCriteriaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            file_paths: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.GitFilePathFilterCriteriaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            tags: typing.Optional[typing.Union["CfnPipelinePropsMixin.GitTagFilterCriteriaProperty", typing.Dict[builtins.str, typing.Any]]] = None,
        ) -> None:
            '''The event criteria that specify when a specified repository event will start the pipeline for the specified trigger configuration, such as the lists of Git tags to include and exclude.

            :param branches: The field that specifies to filter on branches for the push trigger configuration.
            :param file_paths: The field that specifies to filter on file paths for the push trigger configuration.
            :param tags: The field that contains the details for the Git tags trigger configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitpushfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                git_push_filter_property = codepipeline_mixins.CfnPipelinePropsMixin.GitPushFilterProperty(
                    branches=codepipeline_mixins.CfnPipelinePropsMixin.GitBranchFilterCriteriaProperty(
                        excludes=["excludes"],
                        includes=["includes"]
                    ),
                    file_paths=codepipeline_mixins.CfnPipelinePropsMixin.GitFilePathFilterCriteriaProperty(
                        excludes=["excludes"],
                        includes=["includes"]
                    ),
                    tags=codepipeline_mixins.CfnPipelinePropsMixin.GitTagFilterCriteriaProperty(
                        excludes=["excludes"],
                        includes=["includes"]
                    )
                )
            '''
            if isinstance(tags, dict):
                tags = CfnPipelinePropsMixin.GitTagFilterCriteriaProperty(**tags)
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0d17368bc8b95e790f7e0c6291d0def51730b456fed52d6ebd0f9f9d8be56517)
                check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
                check_type(argname="argument file_paths", value=file_paths, expected_type=type_hints["file_paths"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if branches is not None:
                self._values["branches"] = branches
            if file_paths is not None:
                self._values["file_paths"] = file_paths
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def branches(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.GitBranchFilterCriteriaProperty"]]:
            '''The field that specifies to filter on branches for the push trigger configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitpushfilter.html#cfn-codepipeline-pipeline-gitpushfilter-branches
            '''
            result = self._values.get("branches")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.GitBranchFilterCriteriaProperty"]], result)

        @builtins.property
        def file_paths(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.GitFilePathFilterCriteriaProperty"]]:
            '''The field that specifies to filter on file paths for the push trigger configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitpushfilter.html#cfn-codepipeline-pipeline-gitpushfilter-filepaths
            '''
            result = self._values.get("file_paths")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.GitFilePathFilterCriteriaProperty"]], result)

        @builtins.property
        def tags(
            self,
        ) -> typing.Optional["CfnPipelinePropsMixin.GitTagFilterCriteriaProperty"]:
            '''The field that contains the details for the Git tags trigger configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitpushfilter.html#cfn-codepipeline-pipeline-gitpushfilter-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional["CfnPipelinePropsMixin.GitTagFilterCriteriaProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GitPushFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.GitTagFilterCriteriaProperty",
        jsii_struct_bases=[],
        name_mapping={"excludes": "excludes", "includes": "includes"},
    )
    class GitTagFilterCriteriaProperty:
        def __init__(
            self,
            *,
            excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
            includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The Git tags specified as filter criteria for whether a Git tag repository event will start the pipeline.

            :param excludes: The list of patterns of Git tags that, when pushed, are to be excluded from starting the pipeline.
            :param includes: The list of patterns of Git tags that, when pushed, are to be included as criteria that starts the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gittagfiltercriteria.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                git_tag_filter_criteria_property = codepipeline_mixins.CfnPipelinePropsMixin.GitTagFilterCriteriaProperty(
                    excludes=["excludes"],
                    includes=["includes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6d1aee072db1e02d1514989aa4aaddc5e2895e46fafdb0928a83586c5b962aa6)
                check_type(argname="argument excludes", value=excludes, expected_type=type_hints["excludes"])
                check_type(argname="argument includes", value=includes, expected_type=type_hints["includes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if excludes is not None:
                self._values["excludes"] = excludes
            if includes is not None:
                self._values["includes"] = includes

        @builtins.property
        def excludes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of patterns of Git tags that, when pushed, are to be excluded from starting the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gittagfiltercriteria.html#cfn-codepipeline-pipeline-gittagfiltercriteria-excludes
            '''
            result = self._values.get("excludes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def includes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of patterns of Git tags that, when pushed, are to be included as criteria that starts the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gittagfiltercriteria.html#cfn-codepipeline-pipeline-gittagfiltercriteria-includes
            '''
            result = self._values.get("includes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GitTagFilterCriteriaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.InputArtifactProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class InputArtifactProperty:
        def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
            '''Represents information about an artifact to be worked on, such as a test or build artifact.

            :param name: The name of the artifact to be worked on (for example, "My App"). Artifacts are the files that are worked on by actions in the pipeline. See the action configuration for each action for details about artifact parameters. For example, the S3 source action input artifact is a file name (or file path), and the files are generally provided as a ZIP file. Example artifact name: SampleApp_Windows.zip The input artifact of an action must exactly match the output artifact declared in a preceding action, but the input artifact does not have to be the next action in strict sequence from the action that provided the output artifact. Actions in parallel can declare different output artifacts, which are in turn consumed by different following actions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-inputartifact.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                input_artifact_property = codepipeline_mixins.CfnPipelinePropsMixin.InputArtifactProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8f86ae5d58a5949eae6a38c4ad6f740cdb04becb1ce081c21f4e8209da67eeb2)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the artifact to be worked on (for example, "My App").

            Artifacts are the files that are worked on by actions in the pipeline. See the action configuration for each action for details about artifact parameters. For example, the S3 source action input artifact is a file name (or file path), and the files are generally provided as a ZIP file. Example artifact name: SampleApp_Windows.zip

            The input artifact of an action must exactly match the output artifact declared in a preceding action, but the input artifact does not have to be the next action in strict sequence from the action that provided the output artifact. Actions in parallel can declare different output artifacts, which are in turn consumed by different following actions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-inputartifact.html#cfn-codepipeline-pipeline-inputartifact-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputArtifactProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.OutputArtifactProperty",
        jsii_struct_bases=[],
        name_mapping={"files": "files", "name": "name"},
    )
    class OutputArtifactProperty:
        def __init__(
            self,
            *,
            files: typing.Optional[typing.Sequence[builtins.str]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents information about the output of an action.

            :param files: The files that you want to associate with the output artifact that will be exported from the compute action.
            :param name: The name of the output of an artifact, such as "My App". The output artifact name must exactly match the input artifact declared for a downstream action. However, the downstream action's input artifact does not have to be the next action in strict sequence from the action that provided the output artifact. Actions in parallel can declare different output artifacts, which are in turn consumed by different following actions. Output artifact names must be unique within a pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-outputartifact.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                output_artifact_property = codepipeline_mixins.CfnPipelinePropsMixin.OutputArtifactProperty(
                    files=["files"],
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2375ade5cb5617a526aff9d4a439aef228dd84203e53fe0c868ea68ba59e8f54)
                check_type(argname="argument files", value=files, expected_type=type_hints["files"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if files is not None:
                self._values["files"] = files
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def files(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The files that you want to associate with the output artifact that will be exported from the compute action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-outputartifact.html#cfn-codepipeline-pipeline-outputartifact-files
            '''
            result = self._values.get("files")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the output of an artifact, such as "My App".

            The output artifact name must exactly match the input artifact declared for a downstream action. However, the downstream action's input artifact does not have to be the next action in strict sequence from the action that provided the output artifact. Actions in parallel can declare different output artifacts, which are in turn consumed by different following actions.

            Output artifact names must be unique within a pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-outputartifact.html#cfn-codepipeline-pipeline-outputartifact-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputArtifactProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.PipelineTriggerDeclarationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "git_configuration": "gitConfiguration",
            "provider_type": "providerType",
        },
    )
    class PipelineTriggerDeclarationProperty:
        def __init__(
            self,
            *,
            git_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.GitConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            provider_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents information about the specified trigger configuration, such as the filter criteria and the source stage for the action that contains the trigger.

            .. epigraph::

               This is only supported for the ``CodeStarSourceConnection`` action type. > When a trigger configuration is specified, default change detection for repository and branch commits is disabled.

            :param git_configuration: Provides the filter criteria and the source stage for the repository event that starts the pipeline, such as Git tags.
            :param provider_type: The source provider for the event, such as connections configured for a repository with Git tags, for the specified trigger configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-pipelinetriggerdeclaration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                pipeline_trigger_declaration_property = codepipeline_mixins.CfnPipelinePropsMixin.PipelineTriggerDeclarationProperty(
                    git_configuration=codepipeline_mixins.CfnPipelinePropsMixin.GitConfigurationProperty(
                        pull_request=[codepipeline_mixins.CfnPipelinePropsMixin.GitPullRequestFilterProperty(
                            branches=codepipeline_mixins.CfnPipelinePropsMixin.GitBranchFilterCriteriaProperty(
                                excludes=["excludes"],
                                includes=["includes"]
                            ),
                            events=["events"],
                            file_paths=codepipeline_mixins.CfnPipelinePropsMixin.GitFilePathFilterCriteriaProperty(
                                excludes=["excludes"],
                                includes=["includes"]
                            )
                        )],
                        push=[codepipeline_mixins.CfnPipelinePropsMixin.GitPushFilterProperty(
                            branches=codepipeline_mixins.CfnPipelinePropsMixin.GitBranchFilterCriteriaProperty(
                                excludes=["excludes"],
                                includes=["includes"]
                            ),
                            file_paths=codepipeline_mixins.CfnPipelinePropsMixin.GitFilePathFilterCriteriaProperty(
                                excludes=["excludes"],
                                includes=["includes"]
                            ),
                            tags=codepipeline_mixins.CfnPipelinePropsMixin.GitTagFilterCriteriaProperty(
                                excludes=["excludes"],
                                includes=["includes"]
                            )
                        )],
                        source_action_name="sourceActionName"
                    ),
                    provider_type="providerType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__011ad311a92b5938e0fd14244243920b2eac55fb62de2aa28ff2bd5b1c3e1ea4)
                check_type(argname="argument git_configuration", value=git_configuration, expected_type=type_hints["git_configuration"])
                check_type(argname="argument provider_type", value=provider_type, expected_type=type_hints["provider_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if git_configuration is not None:
                self._values["git_configuration"] = git_configuration
            if provider_type is not None:
                self._values["provider_type"] = provider_type

        @builtins.property
        def git_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.GitConfigurationProperty"]]:
            '''Provides the filter criteria and the source stage for the repository event that starts the pipeline, such as Git tags.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-pipelinetriggerdeclaration.html#cfn-codepipeline-pipeline-pipelinetriggerdeclaration-gitconfiguration
            '''
            result = self._values.get("git_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.GitConfigurationProperty"]], result)

        @builtins.property
        def provider_type(self) -> typing.Optional[builtins.str]:
            '''The source provider for the event, such as connections configured for a repository with Git tags, for the specified trigger configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-pipelinetriggerdeclaration.html#cfn-codepipeline-pipeline-pipelinetriggerdeclaration-providertype
            '''
            result = self._values.get("provider_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipelineTriggerDeclarationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.RetryConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"retry_mode": "retryMode"},
    )
    class RetryConfigurationProperty:
        def __init__(self, *, retry_mode: typing.Optional[builtins.str] = None) -> None:
            '''The retry configuration specifies automatic retry for a failed stage, along with the configured retry mode.

            :param retry_mode: The method that you want to configure for automatic stage retry on stage failure. You can specify to retry only failed action in the stage or all actions in the stage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-retryconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                retry_configuration_property = codepipeline_mixins.CfnPipelinePropsMixin.RetryConfigurationProperty(
                    retry_mode="retryMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__11593123dd8387e94ef588f422b085b6d05c8f05af1ceed4d638f35d5be13ee2)
                check_type(argname="argument retry_mode", value=retry_mode, expected_type=type_hints["retry_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if retry_mode is not None:
                self._values["retry_mode"] = retry_mode

        @builtins.property
        def retry_mode(self) -> typing.Optional[builtins.str]:
            '''The method that you want to configure for automatic stage retry on stage failure.

            You can specify to retry only failed action in the stage or all actions in the stage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-retryconfiguration.html#cfn-codepipeline-pipeline-retryconfiguration-retrymode
            '''
            result = self._values.get("retry_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetryConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.RuleDeclarationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "commands": "commands",
            "configuration": "configuration",
            "input_artifacts": "inputArtifacts",
            "name": "name",
            "region": "region",
            "role_arn": "roleArn",
            "rule_type_id": "ruleTypeId",
        },
    )
    class RuleDeclarationProperty:
        def __init__(
            self,
            *,
            commands: typing.Optional[typing.Sequence[builtins.str]] = None,
            configuration: typing.Any = None,
            input_artifacts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.InputArtifactProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            name: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            rule_type_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.RuleTypeIdProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Represents information about the rule to be created for an associated condition.

            An example would be creating a new rule for an entry condition, such as a rule that checks for a test result before allowing the run to enter the deployment stage. For more information about conditions, see `Stage conditions <https://docs.aws.amazon.com/codepipeline/latest/userguide/stage-conditions.html>`_ and `How do stage conditions work? <https://docs.aws.amazon.com/codepipeline/latest/userguide/concepts-how-it-works-conditions.html>`_ . For more information about rules, see the `AWS CodePipeline rule reference <https://docs.aws.amazon.com/codepipeline/latest/userguide/rule-reference.html>`_ .

            :param commands: The shell commands to run with your commands rule in CodePipeline. All commands are supported except multi-line formats. While CodeBuild logs and permissions are used, you do not need to create any resources in CodeBuild. .. epigraph:: Using compute time for this action will incur separate charges in AWS CodeBuild .
            :param configuration: The action configuration fields for the rule.
            :param input_artifacts: The input artifacts fields for the rule, such as specifying an input file for the rule.
            :param name: The name of the rule that is created for the condition, such as ``VariableCheck`` .
            :param region: The Region for the condition associated with the rule.
            :param role_arn: The pipeline role ARN associated with the rule.
            :param rule_type_id: The ID for the rule type, which is made up of the combined values for category, owner, provider, and version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-ruledeclaration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                # configuration: Any
                
                rule_declaration_property = codepipeline_mixins.CfnPipelinePropsMixin.RuleDeclarationProperty(
                    commands=["commands"],
                    configuration=configuration,
                    input_artifacts=[codepipeline_mixins.CfnPipelinePropsMixin.InputArtifactProperty(
                        name="name"
                    )],
                    name="name",
                    region="region",
                    role_arn="roleArn",
                    rule_type_id=codepipeline_mixins.CfnPipelinePropsMixin.RuleTypeIdProperty(
                        category="category",
                        owner="owner",
                        provider="provider",
                        version="version"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f44b906f1669efc2ed7c13b1293a812e849b9d9957ab002d4b3d331960c5f7b6)
                check_type(argname="argument commands", value=commands, expected_type=type_hints["commands"])
                check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
                check_type(argname="argument input_artifacts", value=input_artifacts, expected_type=type_hints["input_artifacts"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument rule_type_id", value=rule_type_id, expected_type=type_hints["rule_type_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if commands is not None:
                self._values["commands"] = commands
            if configuration is not None:
                self._values["configuration"] = configuration
            if input_artifacts is not None:
                self._values["input_artifacts"] = input_artifacts
            if name is not None:
                self._values["name"] = name
            if region is not None:
                self._values["region"] = region
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if rule_type_id is not None:
                self._values["rule_type_id"] = rule_type_id

        @builtins.property
        def commands(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The shell commands to run with your commands rule in CodePipeline.

            All commands are supported except multi-line formats. While CodeBuild logs and permissions are used, you do not need to create any resources in CodeBuild.
            .. epigraph::

               Using compute time for this action will incur separate charges in AWS CodeBuild .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-ruledeclaration.html#cfn-codepipeline-pipeline-ruledeclaration-commands
            '''
            result = self._values.get("commands")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def configuration(self) -> typing.Any:
            '''The action configuration fields for the rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-ruledeclaration.html#cfn-codepipeline-pipeline-ruledeclaration-configuration
            '''
            result = self._values.get("configuration")
            return typing.cast(typing.Any, result)

        @builtins.property
        def input_artifacts(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.InputArtifactProperty"]]]]:
            '''The input artifacts fields for the rule, such as specifying an input file for the rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-ruledeclaration.html#cfn-codepipeline-pipeline-ruledeclaration-inputartifacts
            '''
            result = self._values.get("input_artifacts")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.InputArtifactProperty"]]]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the rule that is created for the condition, such as ``VariableCheck`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-ruledeclaration.html#cfn-codepipeline-pipeline-ruledeclaration-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The Region for the condition associated with the rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-ruledeclaration.html#cfn-codepipeline-pipeline-ruledeclaration-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The pipeline role ARN associated with the rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-ruledeclaration.html#cfn-codepipeline-pipeline-ruledeclaration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rule_type_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.RuleTypeIdProperty"]]:
            '''The ID for the rule type, which is made up of the combined values for category, owner, provider, and version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-ruledeclaration.html#cfn-codepipeline-pipeline-ruledeclaration-ruletypeid
            '''
            result = self._values.get("rule_type_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.RuleTypeIdProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleDeclarationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.RuleTypeIdProperty",
        jsii_struct_bases=[],
        name_mapping={
            "category": "category",
            "owner": "owner",
            "provider": "provider",
            "version": "version",
        },
    )
    class RuleTypeIdProperty:
        def __init__(
            self,
            *,
            category: typing.Optional[builtins.str] = None,
            owner: typing.Optional[builtins.str] = None,
            provider: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ID for the rule type, which is made up of the combined values for category, owner, provider, and version.

            For more information about conditions, see `Stage conditions <https://docs.aws.amazon.com/codepipeline/latest/userguide/stage-conditions.html>`_ . For more information about rules, see the `AWS CodePipeline rule reference <https://docs.aws.amazon.com/codepipeline/latest/userguide/rule-reference.html>`_ .

            :param category: A category defines what kind of rule can be run in the stage, and constrains the provider type for the rule. The valid category is ``Rule`` .
            :param owner: The creator of the rule being called. The valid value for the ``Owner`` field in the rule category is ``AWS`` .
            :param provider: The rule provider, such as the ``DeploymentWindow`` rule. For a list of rule provider names, see the rules listed in the `AWS CodePipeline rule reference <https://docs.aws.amazon.com/codepipeline/latest/userguide/rule-reference.html>`_ .
            :param version: A string that describes the rule version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-ruletypeid.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                rule_type_id_property = codepipeline_mixins.CfnPipelinePropsMixin.RuleTypeIdProperty(
                    category="category",
                    owner="owner",
                    provider="provider",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__48fdfb0e67382bc702fda940d1fed6983c556a18d7fd11d46ee556424a1009ee)
                check_type(argname="argument category", value=category, expected_type=type_hints["category"])
                check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
                check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if category is not None:
                self._values["category"] = category
            if owner is not None:
                self._values["owner"] = owner
            if provider is not None:
                self._values["provider"] = provider
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def category(self) -> typing.Optional[builtins.str]:
            '''A category defines what kind of rule can be run in the stage, and constrains the provider type for the rule.

            The valid category is ``Rule`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-ruletypeid.html#cfn-codepipeline-pipeline-ruletypeid-category
            '''
            result = self._values.get("category")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def owner(self) -> typing.Optional[builtins.str]:
            '''The creator of the rule being called.

            The valid value for the ``Owner`` field in the rule category is ``AWS`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-ruletypeid.html#cfn-codepipeline-pipeline-ruletypeid-owner
            '''
            result = self._values.get("owner")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def provider(self) -> typing.Optional[builtins.str]:
            '''The rule provider, such as the ``DeploymentWindow`` rule.

            For a list of rule provider names, see the rules listed in the `AWS CodePipeline rule reference <https://docs.aws.amazon.com/codepipeline/latest/userguide/rule-reference.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-ruletypeid.html#cfn-codepipeline-pipeline-ruletypeid-provider
            '''
            result = self._values.get("provider")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''A string that describes the rule version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-ruletypeid.html#cfn-codepipeline-pipeline-ruletypeid-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleTypeIdProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.StageDeclarationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "actions": "actions",
            "before_entry": "beforeEntry",
            "blockers": "blockers",
            "name": "name",
            "on_failure": "onFailure",
            "on_success": "onSuccess",
        },
    )
    class StageDeclarationProperty:
        def __init__(
            self,
            *,
            actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.ActionDeclarationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            before_entry: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.BeforeEntryConditionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            blockers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.BlockerDeclarationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            name: typing.Optional[builtins.str] = None,
            on_failure: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.FailureConditionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            on_success: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.SuccessConditionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Represents information about a stage and its definition.

            :param actions: The actions included in a stage.
            :param before_entry: The method to use when a stage allows entry. For example, configuring this field for conditions will allow entry to the stage when the conditions are met.
            :param blockers: Reserved for future use.
            :param name: The name of the stage.
            :param on_failure: The method to use when a stage has not completed successfully. For example, configuring this field for rollback will roll back a failed stage automatically to the last successful pipeline execution in the stage.
            :param on_success: The method to use when a stage has succeeded. For example, configuring this field for conditions will allow the stage to succeed when the conditions are met.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stagedeclaration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                # configuration: Any
                
                stage_declaration_property = codepipeline_mixins.CfnPipelinePropsMixin.StageDeclarationProperty(
                    actions=[codepipeline_mixins.CfnPipelinePropsMixin.ActionDeclarationProperty(
                        action_type_id=codepipeline_mixins.CfnPipelinePropsMixin.ActionTypeIdProperty(
                            category="category",
                            owner="owner",
                            provider="provider",
                            version="version"
                        ),
                        commands=["commands"],
                        configuration=configuration,
                        environment_variables=[codepipeline_mixins.CfnPipelinePropsMixin.EnvironmentVariableProperty(
                            name="name",
                            type="type",
                            value="value"
                        )],
                        input_artifacts=[codepipeline_mixins.CfnPipelinePropsMixin.InputArtifactProperty(
                            name="name"
                        )],
                        name="name",
                        namespace="namespace",
                        output_artifacts=[codepipeline_mixins.CfnPipelinePropsMixin.OutputArtifactProperty(
                            files=["files"],
                            name="name"
                        )],
                        output_variables=["outputVariables"],
                        region="region",
                        role_arn="roleArn",
                        run_order=123,
                        timeout_in_minutes=123
                    )],
                    before_entry=codepipeline_mixins.CfnPipelinePropsMixin.BeforeEntryConditionsProperty(
                        conditions=[codepipeline_mixins.CfnPipelinePropsMixin.ConditionProperty(
                            result="result",
                            rules=[codepipeline_mixins.CfnPipelinePropsMixin.RuleDeclarationProperty(
                                commands=["commands"],
                                configuration=configuration,
                                input_artifacts=[codepipeline_mixins.CfnPipelinePropsMixin.InputArtifactProperty(
                                    name="name"
                                )],
                                name="name",
                                region="region",
                                role_arn="roleArn",
                                rule_type_id=codepipeline_mixins.CfnPipelinePropsMixin.RuleTypeIdProperty(
                                    category="category",
                                    owner="owner",
                                    provider="provider",
                                    version="version"
                                )
                            )]
                        )]
                    ),
                    blockers=[codepipeline_mixins.CfnPipelinePropsMixin.BlockerDeclarationProperty(
                        name="name",
                        type="type"
                    )],
                    name="name",
                    on_failure=codepipeline_mixins.CfnPipelinePropsMixin.FailureConditionsProperty(
                        conditions=[codepipeline_mixins.CfnPipelinePropsMixin.ConditionProperty(
                            result="result",
                            rules=[codepipeline_mixins.CfnPipelinePropsMixin.RuleDeclarationProperty(
                                commands=["commands"],
                                configuration=configuration,
                                input_artifacts=[codepipeline_mixins.CfnPipelinePropsMixin.InputArtifactProperty(
                                    name="name"
                                )],
                                name="name",
                                region="region",
                                role_arn="roleArn",
                                rule_type_id=codepipeline_mixins.CfnPipelinePropsMixin.RuleTypeIdProperty(
                                    category="category",
                                    owner="owner",
                                    provider="provider",
                                    version="version"
                                )
                            )]
                        )],
                        result="result",
                        retry_configuration=codepipeline_mixins.CfnPipelinePropsMixin.RetryConfigurationProperty(
                            retry_mode="retryMode"
                        )
                    ),
                    on_success=codepipeline_mixins.CfnPipelinePropsMixin.SuccessConditionsProperty(
                        conditions=[codepipeline_mixins.CfnPipelinePropsMixin.ConditionProperty(
                            result="result",
                            rules=[codepipeline_mixins.CfnPipelinePropsMixin.RuleDeclarationProperty(
                                commands=["commands"],
                                configuration=configuration,
                                input_artifacts=[codepipeline_mixins.CfnPipelinePropsMixin.InputArtifactProperty(
                                    name="name"
                                )],
                                name="name",
                                region="region",
                                role_arn="roleArn",
                                rule_type_id=codepipeline_mixins.CfnPipelinePropsMixin.RuleTypeIdProperty(
                                    category="category",
                                    owner="owner",
                                    provider="provider",
                                    version="version"
                                )
                            )]
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4c59fa2091f594821163fdbe0243988cbc9c1bd82964376f67af992993f28b8b)
                check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
                check_type(argname="argument before_entry", value=before_entry, expected_type=type_hints["before_entry"])
                check_type(argname="argument blockers", value=blockers, expected_type=type_hints["blockers"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
                check_type(argname="argument on_success", value=on_success, expected_type=type_hints["on_success"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if actions is not None:
                self._values["actions"] = actions
            if before_entry is not None:
                self._values["before_entry"] = before_entry
            if blockers is not None:
                self._values["blockers"] = blockers
            if name is not None:
                self._values["name"] = name
            if on_failure is not None:
                self._values["on_failure"] = on_failure
            if on_success is not None:
                self._values["on_success"] = on_success

        @builtins.property
        def actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ActionDeclarationProperty"]]]]:
            '''The actions included in a stage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stagedeclaration.html#cfn-codepipeline-pipeline-stagedeclaration-actions
            '''
            result = self._values.get("actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ActionDeclarationProperty"]]]], result)

        @builtins.property
        def before_entry(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.BeforeEntryConditionsProperty"]]:
            '''The method to use when a stage allows entry.

            For example, configuring this field for conditions will allow entry to the stage when the conditions are met.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stagedeclaration.html#cfn-codepipeline-pipeline-stagedeclaration-beforeentry
            '''
            result = self._values.get("before_entry")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.BeforeEntryConditionsProperty"]], result)

        @builtins.property
        def blockers(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.BlockerDeclarationProperty"]]]]:
            '''Reserved for future use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stagedeclaration.html#cfn-codepipeline-pipeline-stagedeclaration-blockers
            '''
            result = self._values.get("blockers")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.BlockerDeclarationProperty"]]]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the stage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stagedeclaration.html#cfn-codepipeline-pipeline-stagedeclaration-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def on_failure(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.FailureConditionsProperty"]]:
            '''The method to use when a stage has not completed successfully.

            For example, configuring this field for rollback will roll back a failed stage automatically to the last successful pipeline execution in the stage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stagedeclaration.html#cfn-codepipeline-pipeline-stagedeclaration-onfailure
            '''
            result = self._values.get("on_failure")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.FailureConditionsProperty"]], result)

        @builtins.property
        def on_success(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.SuccessConditionsProperty"]]:
            '''The method to use when a stage has succeeded.

            For example, configuring this field for conditions will allow the stage to succeed when the conditions are met.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stagedeclaration.html#cfn-codepipeline-pipeline-stagedeclaration-onsuccess
            '''
            result = self._values.get("on_success")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.SuccessConditionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StageDeclarationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.StageTransitionProperty",
        jsii_struct_bases=[],
        name_mapping={"reason": "reason", "stage_name": "stageName"},
    )
    class StageTransitionProperty:
        def __init__(
            self,
            *,
            reason: typing.Optional[builtins.str] = None,
            stage_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The name of the pipeline in which you want to disable the flow of artifacts from one stage to another.

            :param reason: The reason given to the user that a stage is disabled, such as waiting for manual approval or manual tests. This message is displayed in the pipeline console UI.
            :param stage_name: The name of the stage where you want to disable the inbound or outbound transition of artifacts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stagetransition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                stage_transition_property = codepipeline_mixins.CfnPipelinePropsMixin.StageTransitionProperty(
                    reason="reason",
                    stage_name="stageName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__025b47339b17e0c4ded72205aa05a1b8df511bfc80dd3fea4e91d67db6ec4262)
                check_type(argname="argument reason", value=reason, expected_type=type_hints["reason"])
                check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if reason is not None:
                self._values["reason"] = reason
            if stage_name is not None:
                self._values["stage_name"] = stage_name

        @builtins.property
        def reason(self) -> typing.Optional[builtins.str]:
            '''The reason given to the user that a stage is disabled, such as waiting for manual approval or manual tests.

            This message is displayed in the pipeline console UI.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stagetransition.html#cfn-codepipeline-pipeline-stagetransition-reason
            '''
            result = self._values.get("reason")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stage_name(self) -> typing.Optional[builtins.str]:
            '''The name of the stage where you want to disable the inbound or outbound transition of artifacts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stagetransition.html#cfn-codepipeline-pipeline-stagetransition-stagename
            '''
            result = self._values.get("stage_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StageTransitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.SuccessConditionsProperty",
        jsii_struct_bases=[],
        name_mapping={"conditions": "conditions"},
    )
    class SuccessConditionsProperty:
        def __init__(
            self,
            *,
            conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.ConditionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The conditions for making checks that, if met, succeed a stage.

            For more information about conditions, see `Stage conditions <https://docs.aws.amazon.com/codepipeline/latest/userguide/stage-conditions.html>`_ and `How do stage conditions work? <https://docs.aws.amazon.com/codepipeline/latest/userguide/concepts-how-it-works-conditions.html>`_ .

            :param conditions: The conditions that are success conditions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-successconditions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                # configuration: Any
                
                success_conditions_property = codepipeline_mixins.CfnPipelinePropsMixin.SuccessConditionsProperty(
                    conditions=[codepipeline_mixins.CfnPipelinePropsMixin.ConditionProperty(
                        result="result",
                        rules=[codepipeline_mixins.CfnPipelinePropsMixin.RuleDeclarationProperty(
                            commands=["commands"],
                            configuration=configuration,
                            input_artifacts=[codepipeline_mixins.CfnPipelinePropsMixin.InputArtifactProperty(
                                name="name"
                            )],
                            name="name",
                            region="region",
                            role_arn="roleArn",
                            rule_type_id=codepipeline_mixins.CfnPipelinePropsMixin.RuleTypeIdProperty(
                                category="category",
                                owner="owner",
                                provider="provider",
                                version="version"
                            )
                        )]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bb5d7e8a50c53cacad8a7d5d7ed4324da3d05222b87497f24edc54d8f480d222)
                check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if conditions is not None:
                self._values["conditions"] = conditions

        @builtins.property
        def conditions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ConditionProperty"]]]]:
            '''The conditions that are success conditions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-successconditions.html#cfn-codepipeline-pipeline-successconditions-conditions
            '''
            result = self._values.get("conditions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ConditionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SuccessConditionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnPipelinePropsMixin.VariableDeclarationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "default_value": "defaultValue",
            "description": "description",
            "name": "name",
        },
    )
    class VariableDeclarationProperty:
        def __init__(
            self,
            *,
            default_value: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A variable declared at the pipeline level.

            :param default_value: The value of a pipeline-level variable.
            :param description: The description of a pipeline-level variable. It's used to add additional context about the variable, and not being used at time when pipeline executes.
            :param name: The name of a pipeline-level variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-variabledeclaration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                variable_declaration_property = codepipeline_mixins.CfnPipelinePropsMixin.VariableDeclarationProperty(
                    default_value="defaultValue",
                    description="description",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3babaf0916a21847bf4e724811c4f7f281c216f109b9351eb3f3f34afff3861f)
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_value is not None:
                self._values["default_value"] = default_value
            if description is not None:
                self._values["description"] = description
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            '''The value of a pipeline-level variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-variabledeclaration.html#cfn-codepipeline-pipeline-variabledeclaration-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of a pipeline-level variable.

            It's used to add additional context about the variable, and not being used at time when pipeline executes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-variabledeclaration.html#cfn-codepipeline-pipeline-variabledeclaration-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of a pipeline-level variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-variabledeclaration.html#cfn-codepipeline-pipeline-variabledeclaration-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VariableDeclarationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnWebhookMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "authentication": "authentication",
        "authentication_configuration": "authenticationConfiguration",
        "filters": "filters",
        "name": "name",
        "register_with_third_party": "registerWithThirdParty",
        "target_action": "targetAction",
        "target_pipeline": "targetPipeline",
        "target_pipeline_version": "targetPipelineVersion",
    },
)
class CfnWebhookMixinProps:
    def __init__(
        self,
        *,
        authentication: typing.Optional[builtins.str] = None,
        authentication_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWebhookPropsMixin.WebhookAuthConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWebhookPropsMixin.WebhookFilterRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        register_with_third_party: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        target_action: typing.Optional[builtins.str] = None,
        target_pipeline: typing.Optional[builtins.str] = None,
        target_pipeline_version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for CfnWebhookPropsMixin.

        :param authentication: Supported options are GITHUB_HMAC, IP, and UNAUTHENTICATED. .. epigraph:: When creating CodePipeline webhooks, do not use your own credentials or reuse the same secret token across multiple webhooks. For optimal security, generate a unique secret token for each webhook you create. The secret token is an arbitrary string that you provide, which GitHub uses to compute and sign the webhook payloads sent to CodePipeline, for protecting the integrity and authenticity of the webhook payloads. Using your own credentials or reusing the same token across multiple webhooks can lead to security vulnerabilities. > If a secret token was provided, it will be redacted in the response. - For information about the authentication scheme implemented by GITHUB_HMAC, see `Securing your webhooks <https://docs.aws.amazon.com/https://developer.github.com/webhooks/securing/>`_ on the GitHub Developer website. - IP rejects webhooks trigger requests unless they originate from an IP address in the IP range whitelisted in the authentication configuration. - UNAUTHENTICATED accepts all webhook trigger requests regardless of origin.
        :param authentication_configuration: Properties that configure the authentication applied to incoming webhook trigger requests. The required properties depend on the authentication type. For GITHUB_HMAC, only the ``SecretToken`` property must be set. For IP, only the ``AllowedIPRange`` property must be set to a valid CIDR range. For UNAUTHENTICATED, no properties can be set.
        :param filters: A list of rules applied to the body/payload sent in the POST request to a webhook URL. All defined rules must pass for the request to be accepted and the pipeline started.
        :param name: The name of the webhook.
        :param register_with_third_party: Configures a connection between the webhook that was created and the external tool with events to be detected.
        :param target_action: The name of the action in a pipeline you want to connect to the webhook. The action must be from the source (first) stage of the pipeline.
        :param target_pipeline: The name of the pipeline you want to connect to the webhook.
        :param target_pipeline_version: The version number of the pipeline to be connected to the trigger request. Required: Yes Type: Integer Update requires: `No interruption <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
            
            cfn_webhook_mixin_props = codepipeline_mixins.CfnWebhookMixinProps(
                authentication="authentication",
                authentication_configuration=codepipeline_mixins.CfnWebhookPropsMixin.WebhookAuthConfigurationProperty(
                    allowed_ip_range="allowedIpRange",
                    secret_token="secretToken"
                ),
                filters=[codepipeline_mixins.CfnWebhookPropsMixin.WebhookFilterRuleProperty(
                    json_path="jsonPath",
                    match_equals="matchEquals"
                )],
                name="name",
                register_with_third_party=False,
                target_action="targetAction",
                target_pipeline="targetPipeline",
                target_pipeline_version=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6ef02b143152f4f3e62063f1914ece62191382b6ab84a0579020fcb8dc20e42)
            check_type(argname="argument authentication", value=authentication, expected_type=type_hints["authentication"])
            check_type(argname="argument authentication_configuration", value=authentication_configuration, expected_type=type_hints["authentication_configuration"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument register_with_third_party", value=register_with_third_party, expected_type=type_hints["register_with_third_party"])
            check_type(argname="argument target_action", value=target_action, expected_type=type_hints["target_action"])
            check_type(argname="argument target_pipeline", value=target_pipeline, expected_type=type_hints["target_pipeline"])
            check_type(argname="argument target_pipeline_version", value=target_pipeline_version, expected_type=type_hints["target_pipeline_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authentication is not None:
            self._values["authentication"] = authentication
        if authentication_configuration is not None:
            self._values["authentication_configuration"] = authentication_configuration
        if filters is not None:
            self._values["filters"] = filters
        if name is not None:
            self._values["name"] = name
        if register_with_third_party is not None:
            self._values["register_with_third_party"] = register_with_third_party
        if target_action is not None:
            self._values["target_action"] = target_action
        if target_pipeline is not None:
            self._values["target_pipeline"] = target_pipeline
        if target_pipeline_version is not None:
            self._values["target_pipeline_version"] = target_pipeline_version

    @builtins.property
    def authentication(self) -> typing.Optional[builtins.str]:
        '''Supported options are GITHUB_HMAC, IP, and UNAUTHENTICATED.

        .. epigraph::

           When creating CodePipeline webhooks, do not use your own credentials or reuse the same secret token across multiple webhooks. For optimal security, generate a unique secret token for each webhook you create. The secret token is an arbitrary string that you provide, which GitHub uses to compute and sign the webhook payloads sent to CodePipeline, for protecting the integrity and authenticity of the webhook payloads. Using your own credentials or reusing the same token across multiple webhooks can lead to security vulnerabilities. > If a secret token was provided, it will be redacted in the response.

        - For information about the authentication scheme implemented by GITHUB_HMAC, see `Securing your webhooks <https://docs.aws.amazon.com/https://developer.github.com/webhooks/securing/>`_ on the GitHub Developer website.
        - IP rejects webhooks trigger requests unless they originate from an IP address in the IP range whitelisted in the authentication configuration.
        - UNAUTHENTICATED accepts all webhook trigger requests regardless of origin.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-authentication
        '''
        result = self._values.get("authentication")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authentication_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebhookPropsMixin.WebhookAuthConfigurationProperty"]]:
        '''Properties that configure the authentication applied to incoming webhook trigger requests.

        The required properties depend on the authentication type. For GITHUB_HMAC, only the ``SecretToken`` property must be set. For IP, only the ``AllowedIPRange`` property must be set to a valid CIDR range. For UNAUTHENTICATED, no properties can be set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-authenticationconfiguration
        '''
        result = self._values.get("authentication_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebhookPropsMixin.WebhookAuthConfigurationProperty"]], result)

    @builtins.property
    def filters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebhookPropsMixin.WebhookFilterRuleProperty"]]]]:
        '''A list of rules applied to the body/payload sent in the POST request to a webhook URL.

        All defined rules must pass for the request to be accepted and the pipeline started.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-filters
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebhookPropsMixin.WebhookFilterRuleProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the webhook.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def register_with_third_party(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Configures a connection between the webhook that was created and the external tool with events to be detected.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-registerwiththirdparty
        '''
        result = self._values.get("register_with_third_party")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def target_action(self) -> typing.Optional[builtins.str]:
        '''The name of the action in a pipeline you want to connect to the webhook.

        The action must be from the source (first) stage of the pipeline.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-targetaction
        '''
        result = self._values.get("target_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_pipeline(self) -> typing.Optional[builtins.str]:
        '''The name of the pipeline you want to connect to the webhook.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-targetpipeline
        '''
        result = self._values.get("target_pipeline")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_pipeline_version(self) -> typing.Optional[jsii.Number]:
        '''The version number of the pipeline to be connected to the trigger request.

        Required: Yes

        Type: Integer

        Update requires: `No interruption <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-targetpipelineversion
        '''
        result = self._values.get("target_pipeline_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWebhookMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWebhookPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnWebhookPropsMixin",
):
    '''The ``AWS::CodePipeline::Webhook`` resource creates and registers your webhook.

    After the webhook is created and registered, it triggers your pipeline to start every time an external event occurs. For more information, see `Migrate polling pipelines to use event-based change detection <https://docs.aws.amazon.com/codepipeline/latest/userguide/update-change-detection.html>`_ in the *AWS CodePipeline User Guide* .

    We strongly recommend that you use AWS Secrets Manager to store your credentials. If you use Secrets Manager, you must have already configured and stored your secret parameters in Secrets Manager. For more information, see `Using Dynamic References to Specify Template Values <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html#dynamic-references-secretsmanager>`_ .
    .. epigraph::

       When passing secret parameters, do not enter the value directly into the template. The value is rendered as plaintext and is therefore readable. For security reasons, do not use plaintext in your AWS CloudFormation template to store your credentials.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html
    :cloudformationResource: AWS::CodePipeline::Webhook
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
        
        cfn_webhook_props_mixin = codepipeline_mixins.CfnWebhookPropsMixin(codepipeline_mixins.CfnWebhookMixinProps(
            authentication="authentication",
            authentication_configuration=codepipeline_mixins.CfnWebhookPropsMixin.WebhookAuthConfigurationProperty(
                allowed_ip_range="allowedIpRange",
                secret_token="secretToken"
            ),
            filters=[codepipeline_mixins.CfnWebhookPropsMixin.WebhookFilterRuleProperty(
                json_path="jsonPath",
                match_equals="matchEquals"
            )],
            name="name",
            register_with_third_party=False,
            target_action="targetAction",
            target_pipeline="targetPipeline",
            target_pipeline_version=123
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnWebhookMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CodePipeline::Webhook``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3576758a281d723e73b5fef26f5614e5ee702cc85a7061155b1925da54579238)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba00d7d646251cea892d93234145c321d5866eb2deaf8462db9406e482dae885)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92cdc20b7f3cbe5f349d0f18df70ac06446ae2d495761b7dcad8fef7843c0217)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWebhookMixinProps:
        return typing.cast(CfnWebhookMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnWebhookPropsMixin.WebhookAuthConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_ip_range": "allowedIpRange",
            "secret_token": "secretToken",
        },
    )
    class WebhookAuthConfigurationProperty:
        def __init__(
            self,
            *,
            allowed_ip_range: typing.Optional[builtins.str] = None,
            secret_token: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The authentication applied to incoming webhook trigger requests.

            :param allowed_ip_range: The property used to configure acceptance of webhooks in an IP address range. For IP, only the ``AllowedIPRange`` property must be set. This property must be set to a valid CIDR range.
            :param secret_token: The property used to configure GitHub authentication. For GITHUB_HMAC, only the ``SecretToken`` property must be set. .. epigraph:: When creating CodePipeline webhooks, do not use your own credentials or reuse the same secret token across multiple webhooks. For optimal security, generate a unique secret token for each webhook you create. The secret token is an arbitrary string that you provide, which GitHub uses to compute and sign the webhook payloads sent to CodePipeline, for protecting the integrity and authenticity of the webhook payloads. Using your own credentials or reusing the same token across multiple webhooks can lead to security vulnerabilities. > If a secret token was provided, it will be redacted in the response.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-webhook-webhookauthconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                webhook_auth_configuration_property = codepipeline_mixins.CfnWebhookPropsMixin.WebhookAuthConfigurationProperty(
                    allowed_ip_range="allowedIpRange",
                    secret_token="secretToken"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__74597bd56ad5da07d0911bb73688e0d7efcd5575be1f1f97b77fa519f0b74fed)
                check_type(argname="argument allowed_ip_range", value=allowed_ip_range, expected_type=type_hints["allowed_ip_range"])
                check_type(argname="argument secret_token", value=secret_token, expected_type=type_hints["secret_token"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_ip_range is not None:
                self._values["allowed_ip_range"] = allowed_ip_range
            if secret_token is not None:
                self._values["secret_token"] = secret_token

        @builtins.property
        def allowed_ip_range(self) -> typing.Optional[builtins.str]:
            '''The property used to configure acceptance of webhooks in an IP address range.

            For IP, only the ``AllowedIPRange`` property must be set. This property must be set to a valid CIDR range.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-webhook-webhookauthconfiguration.html#cfn-codepipeline-webhook-webhookauthconfiguration-allowediprange
            '''
            result = self._values.get("allowed_ip_range")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_token(self) -> typing.Optional[builtins.str]:
            '''The property used to configure GitHub authentication. For GITHUB_HMAC, only the ``SecretToken`` property must be set.

            .. epigraph::

               When creating CodePipeline webhooks, do not use your own credentials or reuse the same secret token across multiple webhooks. For optimal security, generate a unique secret token for each webhook you create. The secret token is an arbitrary string that you provide, which GitHub uses to compute and sign the webhook payloads sent to CodePipeline, for protecting the integrity and authenticity of the webhook payloads. Using your own credentials or reusing the same token across multiple webhooks can lead to security vulnerabilities. > If a secret token was provided, it will be redacted in the response.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-webhook-webhookauthconfiguration.html#cfn-codepipeline-webhook-webhookauthconfiguration-secrettoken
            '''
            result = self._values.get("secret_token")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebhookAuthConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codepipeline.mixins.CfnWebhookPropsMixin.WebhookFilterRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"json_path": "jsonPath", "match_equals": "matchEquals"},
    )
    class WebhookFilterRuleProperty:
        def __init__(
            self,
            *,
            json_path: typing.Optional[builtins.str] = None,
            match_equals: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The event criteria that specify when a webhook notification is sent to your URL.

            :param json_path: A JsonPath expression that is applied to the body/payload of the webhook. The value selected by the JsonPath expression must match the value specified in the ``MatchEquals`` field. Otherwise, the request is ignored. For more information, see `Java JsonPath implementation <https://docs.aws.amazon.com/https://github.com/json-path/JsonPath>`_ in GitHub.
            :param match_equals: The value selected by the ``JsonPath`` expression must match what is supplied in the ``MatchEquals`` field. Otherwise, the request is ignored. Properties from the target action configuration can be included as placeholders in this value by surrounding the action configuration key with curly brackets. For example, if the value supplied here is "refs/heads/{Branch}" and the target action has an action configuration property called "Branch" with a value of "main", the ``MatchEquals`` value is evaluated as "refs/heads/main". For a list of action configuration properties for built-in action types, see `Pipeline Structure Reference Action Requirements <https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html#action-requirements>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-webhook-webhookfilterrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codepipeline import mixins as codepipeline_mixins
                
                webhook_filter_rule_property = codepipeline_mixins.CfnWebhookPropsMixin.WebhookFilterRuleProperty(
                    json_path="jsonPath",
                    match_equals="matchEquals"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7bc385bea7fac8436fe78081ba388fddc1b19d1cec82f0e7e6380058943d5bb0)
                check_type(argname="argument json_path", value=json_path, expected_type=type_hints["json_path"])
                check_type(argname="argument match_equals", value=match_equals, expected_type=type_hints["match_equals"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if json_path is not None:
                self._values["json_path"] = json_path
            if match_equals is not None:
                self._values["match_equals"] = match_equals

        @builtins.property
        def json_path(self) -> typing.Optional[builtins.str]:
            '''A JsonPath expression that is applied to the body/payload of the webhook.

            The value selected by the JsonPath expression must match the value specified in the ``MatchEquals`` field. Otherwise, the request is ignored. For more information, see `Java JsonPath implementation <https://docs.aws.amazon.com/https://github.com/json-path/JsonPath>`_ in GitHub.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-webhook-webhookfilterrule.html#cfn-codepipeline-webhook-webhookfilterrule-jsonpath
            '''
            result = self._values.get("json_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def match_equals(self) -> typing.Optional[builtins.str]:
            '''The value selected by the ``JsonPath`` expression must match what is supplied in the ``MatchEquals`` field.

            Otherwise, the request is ignored. Properties from the target action configuration can be included as placeholders in this value by surrounding the action configuration key with curly brackets. For example, if the value supplied here is "refs/heads/{Branch}" and the target action has an action configuration property called "Branch" with a value of "main", the ``MatchEquals`` value is evaluated as "refs/heads/main". For a list of action configuration properties for built-in action types, see `Pipeline Structure Reference Action Requirements <https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html#action-requirements>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-webhook-webhookfilterrule.html#cfn-codepipeline-webhook-webhookfilterrule-matchequals
            '''
            result = self._values.get("match_equals")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebhookFilterRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnCustomActionTypeMixinProps",
    "CfnCustomActionTypePropsMixin",
    "CfnPipelineMixinProps",
    "CfnPipelinePropsMixin",
    "CfnWebhookMixinProps",
    "CfnWebhookPropsMixin",
]

publication.publish()

def _typecheckingstub__1c92149a4045c439fc1e60bd1689096f2e074364601078bd24dc81425b76e5d7(
    *,
    category: typing.Optional[builtins.str] = None,
    configuration_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCustomActionTypePropsMixin.ConfigurationPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    input_artifact_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCustomActionTypePropsMixin.ArtifactDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    output_artifact_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCustomActionTypePropsMixin.ArtifactDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    provider: typing.Optional[builtins.str] = None,
    settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCustomActionTypePropsMixin.SettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__509030bc71f54a422b1ea8fdfd3f242709375838b41049d8d5213b9088bb4a40(
    props: typing.Union[CfnCustomActionTypeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ff54688372e804ce1131b5be865b9b14dab6b500a3880d96c29edba64d1f9de(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb2527394974bdb067233feb44fa441424dac85bf84fb143da6a5d2ff3ca5c9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88ec54a4077d4d556cd35c3c3dd5d2a7487f588ad33308b3114d86ac1bc401d9(
    *,
    maximum_count: typing.Optional[jsii.Number] = None,
    minimum_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d113fc1b4caaa269a3e6c0f0ee786de343932d53c3545a24f6791ff70ac073a2(
    *,
    description: typing.Optional[builtins.str] = None,
    key: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    queryable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    secret: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40fde3f62227cf15cc8fb663750da29accd9b51254e4a1f94437792097f92373(
    *,
    entity_url_template: typing.Optional[builtins.str] = None,
    execution_url_template: typing.Optional[builtins.str] = None,
    revision_url_template: typing.Optional[builtins.str] = None,
    third_party_configuration_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a1d9e0584770e83d01526637baa64f80d21cf6414caff8df087494978dfe62(
    *,
    artifact_store: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.ArtifactStoreProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    artifact_stores: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.ArtifactStoreMapProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    disable_inbound_stage_transitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.StageTransitionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    execution_mode: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    pipeline_type: typing.Optional[builtins.str] = None,
    restart_execution_on_update: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    stages: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.StageDeclarationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    triggers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.PipelineTriggerDeclarationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.VariableDeclarationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af084dc027d24553278d49c55455e8a7f1326e045152be9fd1064f9d646e17d(
    props: typing.Union[CfnPipelineMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b41fa00dd293d3b0574abc42111af62258d3835aaae5ca581420a3185bf9d4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__425c78f8f04f915c0f66b725dd69af6f042d6228b194eeef703b9c0fb4e563c5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d433e1125bd269371b29aff4978048a5c92cc3708e352333a25b776b645b207(
    *,
    action_type_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.ActionTypeIdProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    configuration: typing.Any = None,
    environment_variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.EnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    input_artifacts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.InputArtifactProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    output_artifacts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.OutputArtifactProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    output_variables: typing.Optional[typing.Sequence[builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    run_order: typing.Optional[jsii.Number] = None,
    timeout_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f965b3a23aff9ce371ff0d47df50a4b81d5912d5f0986e69338c87c80c39b716(
    *,
    category: typing.Optional[builtins.str] = None,
    owner: typing.Optional[builtins.str] = None,
    provider: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e260480aa2bb682c65b5e475ac050756c0f85c28d8d26073536c8c79a08ade3(
    *,
    artifact_store: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.ArtifactStoreProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f227a9f1f148c71e2964f7c596cc4d1f7b302e0550d4c3a4185332e898611230(
    *,
    encryption_key: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.EncryptionKeyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    location: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aacaec593dbfd9dd29f9c66358264650201d6d9ad1019bd4fc87694a0c3a621(
    *,
    conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.ConditionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abb36ad50ae375f0766204e0a077c8fda8caeb34570c5b8183027103587d3b1f(
    *,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572957f44fc3462421e016a13546f972e73c2b8e88a2a64da961a9d09cd46838(
    *,
    result: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.RuleDeclarationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82109c33648c199a02180b3de9ea7130fea6437804f30fca3c910d77f45f4d75(
    *,
    id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d65dc39e16a4d9d70b9371d81c28f393ae655dc6c965d13d73872554e4b9b18(
    *,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f3996b49de5892b88e7157ef423a32d80597dc638cdef577efd10bc302ab00(
    *,
    conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.ConditionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    result: typing.Optional[builtins.str] = None,
    retry_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.RetryConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2baf1be6ecb656bb9a9ced289a5a4c192e57b2255865c32e2c92e3f6df7f82a7(
    *,
    excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    includes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5825ed32f11fc92cc69832820cff29da074394b40492a8b1e4c7e644e4ab7ac(
    *,
    pull_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.GitPullRequestFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    push: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.GitPushFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    source_action_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52413dc4a7cbaaea180d735d2d681723caed88e3b8222b09875b4ed74ffa726e(
    *,
    excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    includes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed91e4ded9d738cf24838b3d2cddc1c86fb9be7bc1a138bf12f052be2460bed9(
    *,
    branches: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.GitBranchFilterCriteriaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    events: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_paths: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.GitFilePathFilterCriteriaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d17368bc8b95e790f7e0c6291d0def51730b456fed52d6ebd0f9f9d8be56517(
    *,
    branches: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.GitBranchFilterCriteriaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    file_paths: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.GitFilePathFilterCriteriaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Union[CfnPipelinePropsMixin.GitTagFilterCriteriaProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d1aee072db1e02d1514989aa4aaddc5e2895e46fafdb0928a83586c5b962aa6(
    *,
    excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    includes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f86ae5d58a5949eae6a38c4ad6f740cdb04becb1ce081c21f4e8209da67eeb2(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2375ade5cb5617a526aff9d4a439aef228dd84203e53fe0c868ea68ba59e8f54(
    *,
    files: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__011ad311a92b5938e0fd14244243920b2eac55fb62de2aa28ff2bd5b1c3e1ea4(
    *,
    git_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.GitConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    provider_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11593123dd8387e94ef588f422b085b6d05c8f05af1ceed4d638f35d5be13ee2(
    *,
    retry_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f44b906f1669efc2ed7c13b1293a812e849b9d9957ab002d4b3d331960c5f7b6(
    *,
    commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    configuration: typing.Any = None,
    input_artifacts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.InputArtifactProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    rule_type_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.RuleTypeIdProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48fdfb0e67382bc702fda940d1fed6983c556a18d7fd11d46ee556424a1009ee(
    *,
    category: typing.Optional[builtins.str] = None,
    owner: typing.Optional[builtins.str] = None,
    provider: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c59fa2091f594821163fdbe0243988cbc9c1bd82964376f67af992993f28b8b(
    *,
    actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.ActionDeclarationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    before_entry: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.BeforeEntryConditionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    blockers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.BlockerDeclarationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    on_failure: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.FailureConditionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    on_success: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.SuccessConditionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__025b47339b17e0c4ded72205aa05a1b8df511bfc80dd3fea4e91d67db6ec4262(
    *,
    reason: typing.Optional[builtins.str] = None,
    stage_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb5d7e8a50c53cacad8a7d5d7ed4324da3d05222b87497f24edc54d8f480d222(
    *,
    conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.ConditionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3babaf0916a21847bf4e724811c4f7f281c216f109b9351eb3f3f34afff3861f(
    *,
    default_value: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ef02b143152f4f3e62063f1914ece62191382b6ab84a0579020fcb8dc20e42(
    *,
    authentication: typing.Optional[builtins.str] = None,
    authentication_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWebhookPropsMixin.WebhookAuthConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWebhookPropsMixin.WebhookFilterRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    register_with_third_party: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    target_action: typing.Optional[builtins.str] = None,
    target_pipeline: typing.Optional[builtins.str] = None,
    target_pipeline_version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3576758a281d723e73b5fef26f5614e5ee702cc85a7061155b1925da54579238(
    props: typing.Union[CfnWebhookMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba00d7d646251cea892d93234145c321d5866eb2deaf8462db9406e482dae885(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92cdc20b7f3cbe5f349d0f18df70ac06446ae2d495761b7dcad8fef7843c0217(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74597bd56ad5da07d0911bb73688e0d7efcd5575be1f1f97b77fa519f0b74fed(
    *,
    allowed_ip_range: typing.Optional[builtins.str] = None,
    secret_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc385bea7fac8436fe78081ba388fddc1b19d1cec82f0e7e6380058943d5bb0(
    *,
    json_path: typing.Optional[builtins.str] = None,
    match_equals: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
