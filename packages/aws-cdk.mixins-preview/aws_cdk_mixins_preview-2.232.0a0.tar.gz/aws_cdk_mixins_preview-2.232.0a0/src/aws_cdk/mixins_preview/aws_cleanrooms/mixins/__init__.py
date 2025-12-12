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
    jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnAnalysisTemplateMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "analysis_parameters": "analysisParameters",
        "description": "description",
        "error_message_configuration": "errorMessageConfiguration",
        "format": "format",
        "membership_identifier": "membershipIdentifier",
        "name": "name",
        "schema": "schema",
        "source": "source",
        "source_metadata": "sourceMetadata",
        "tags": "tags",
    },
)
class CfnAnalysisTemplateMixinProps:
    def __init__(
        self,
        *,
        analysis_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnalysisTemplatePropsMixin.AnalysisParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        error_message_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnalysisTemplatePropsMixin.ErrorMessageConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        format: typing.Optional[builtins.str] = None,
        membership_identifier: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnalysisTemplatePropsMixin.AnalysisSchemaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnalysisTemplatePropsMixin.AnalysisSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        source_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnalysisTemplatePropsMixin.AnalysisSourceMetadataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAnalysisTemplatePropsMixin.

        :param analysis_parameters: The parameters of the analysis template.
        :param description: The description of the analysis template.
        :param error_message_configuration: The configuration that specifies the level of detail in error messages returned by analyses using this template. When set to ``DETAILED`` , error messages include more information to help troubleshoot issues with PySpark jobs. Detailed error messages may expose underlying data, including sensitive information. Recommended for faster troubleshooting in development and testing environments.
        :param format: The format of the analysis template.
        :param membership_identifier: The identifier for a membership resource.
        :param name: The name of the analysis template.
        :param schema: The entire schema object.
        :param source: The source of the analysis template.
        :param source_metadata: The source metadata for the analysis template.
        :param tags: An optional label that you can assign to a resource when you create it. Each tag consists of a key and an optional value, both of which you define. When you use tagging, you can also use tag-based access control in IAM policies to control access to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-analysistemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
            
            cfn_analysis_template_mixin_props = cleanrooms_mixins.CfnAnalysisTemplateMixinProps(
                analysis_parameters=[cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisParameterProperty(
                    default_value="defaultValue",
                    name="name",
                    type="type"
                )],
                description="description",
                error_message_configuration=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.ErrorMessageConfigurationProperty(
                    type="type"
                ),
                format="format",
                membership_identifier="membershipIdentifier",
                name="name",
                schema=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisSchemaProperty(
                    referenced_tables=["referencedTables"]
                ),
                source=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisSourceProperty(
                    artifacts=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactsProperty(
                        additional_artifacts=[cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactProperty(
                            location=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.S3LocationProperty(
                                bucket="bucket",
                                key="key"
                            )
                        )],
                        entry_point=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactProperty(
                            location=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.S3LocationProperty(
                                bucket="bucket",
                                key="key"
                            )
                        ),
                        role_arn="roleArn"
                    ),
                    text="text"
                ),
                source_metadata=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisSourceMetadataProperty(
                    artifacts=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactMetadataProperty(
                        additional_artifact_hashes=[cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.HashProperty(
                            sha256="sha256"
                        )],
                        entry_point_hash=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.HashProperty(
                            sha256="sha256"
                        )
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffa6818fd5f1b78ae6a1946f32c5bcee7e4bfb3765d06e907b2cccb420af30a0)
            check_type(argname="argument analysis_parameters", value=analysis_parameters, expected_type=type_hints["analysis_parameters"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument error_message_configuration", value=error_message_configuration, expected_type=type_hints["error_message_configuration"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument membership_identifier", value=membership_identifier, expected_type=type_hints["membership_identifier"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument source_metadata", value=source_metadata, expected_type=type_hints["source_metadata"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if analysis_parameters is not None:
            self._values["analysis_parameters"] = analysis_parameters
        if description is not None:
            self._values["description"] = description
        if error_message_configuration is not None:
            self._values["error_message_configuration"] = error_message_configuration
        if format is not None:
            self._values["format"] = format
        if membership_identifier is not None:
            self._values["membership_identifier"] = membership_identifier
        if name is not None:
            self._values["name"] = name
        if schema is not None:
            self._values["schema"] = schema
        if source is not None:
            self._values["source"] = source
        if source_metadata is not None:
            self._values["source_metadata"] = source_metadata
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def analysis_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalysisTemplatePropsMixin.AnalysisParameterProperty"]]]]:
        '''The parameters of the analysis template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-analysistemplate.html#cfn-cleanrooms-analysistemplate-analysisparameters
        '''
        result = self._values.get("analysis_parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalysisTemplatePropsMixin.AnalysisParameterProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the analysis template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-analysistemplate.html#cfn-cleanrooms-analysistemplate-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def error_message_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalysisTemplatePropsMixin.ErrorMessageConfigurationProperty"]]:
        '''The configuration that specifies the level of detail in error messages returned by analyses using this template.

        When set to ``DETAILED`` , error messages include more information to help troubleshoot issues with PySpark jobs. Detailed error messages may expose underlying data, including sensitive information. Recommended for faster troubleshooting in development and testing environments.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-analysistemplate.html#cfn-cleanrooms-analysistemplate-errormessageconfiguration
        '''
        result = self._values.get("error_message_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalysisTemplatePropsMixin.ErrorMessageConfigurationProperty"]], result)

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        '''The format of the analysis template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-analysistemplate.html#cfn-cleanrooms-analysistemplate-format
        '''
        result = self._values.get("format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def membership_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier for a membership resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-analysistemplate.html#cfn-cleanrooms-analysistemplate-membershipidentifier
        '''
        result = self._values.get("membership_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the analysis template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-analysistemplate.html#cfn-cleanrooms-analysistemplate-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalysisTemplatePropsMixin.AnalysisSchemaProperty"]]:
        '''The entire schema object.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-analysistemplate.html#cfn-cleanrooms-analysistemplate-schema
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalysisTemplatePropsMixin.AnalysisSchemaProperty"]], result)

    @builtins.property
    def source(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalysisTemplatePropsMixin.AnalysisSourceProperty"]]:
        '''The source of the analysis template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-analysistemplate.html#cfn-cleanrooms-analysistemplate-source
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalysisTemplatePropsMixin.AnalysisSourceProperty"]], result)

    @builtins.property
    def source_metadata(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalysisTemplatePropsMixin.AnalysisSourceMetadataProperty"]]:
        '''The source metadata for the analysis template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-analysistemplate.html#cfn-cleanrooms-analysistemplate-sourcemetadata
        '''
        result = self._values.get("source_metadata")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalysisTemplatePropsMixin.AnalysisSourceMetadataProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An optional label that you can assign to a resource when you create it.

        Each tag consists of a key and an optional value, both of which you define. When you use tagging, you can also use tag-based access control in IAM policies to control access to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-analysistemplate.html#cfn-cleanrooms-analysistemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAnalysisTemplateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAnalysisTemplatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnAnalysisTemplatePropsMixin",
):
    '''Creates a new analysis template.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-analysistemplate.html
    :cloudformationResource: AWS::CleanRooms::AnalysisTemplate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
        
        cfn_analysis_template_props_mixin = cleanrooms_mixins.CfnAnalysisTemplatePropsMixin(cleanrooms_mixins.CfnAnalysisTemplateMixinProps(
            analysis_parameters=[cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisParameterProperty(
                default_value="defaultValue",
                name="name",
                type="type"
            )],
            description="description",
            error_message_configuration=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.ErrorMessageConfigurationProperty(
                type="type"
            ),
            format="format",
            membership_identifier="membershipIdentifier",
            name="name",
            schema=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisSchemaProperty(
                referenced_tables=["referencedTables"]
            ),
            source=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisSourceProperty(
                artifacts=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactsProperty(
                    additional_artifacts=[cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactProperty(
                        location=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.S3LocationProperty(
                            bucket="bucket",
                            key="key"
                        )
                    )],
                    entry_point=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactProperty(
                        location=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.S3LocationProperty(
                            bucket="bucket",
                            key="key"
                        )
                    ),
                    role_arn="roleArn"
                ),
                text="text"
            ),
            source_metadata=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisSourceMetadataProperty(
                artifacts=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactMetadataProperty(
                    additional_artifact_hashes=[cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.HashProperty(
                        sha256="sha256"
                    )],
                    entry_point_hash=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.HashProperty(
                        sha256="sha256"
                    )
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
        props: typing.Union[CfnAnalysisTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CleanRooms::AnalysisTemplate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cbb17a01aa593fc132f37101caa9ac2e050c5e565d8386b52958c81fd08b7b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ec8c01644712bc30eb846b1c0f03c5031301146315323a74702fb778af6a063)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed42dedacb0000d9b7b016d92919dac513d9c901bac9d9af8b0a6dadaa73b38c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAnalysisTemplateMixinProps:
        return typing.cast(CfnAnalysisTemplateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnAnalysisTemplatePropsMixin.AnalysisParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"default_value": "defaultValue", "name": "name", "type": "type"},
    )
    class AnalysisParameterProperty:
        def __init__(
            self,
            *,
            default_value: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Optional.

            The member who can query can provide this placeholder for a literal data value in an analysis template.

            :param default_value: Optional. The default value that is applied in the analysis template. The member who can query can override this value in the query editor.
            :param name: The name of the parameter. The name must use only alphanumeric, underscore (_), or hyphen (-) characters but cannot start or end with a hyphen.
            :param type: The type of parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-analysisparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                analysis_parameter_property = cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisParameterProperty(
                    default_value="defaultValue",
                    name="name",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f48ec49c97796d97b0f4a192d51a4bff475d97119929c418ec1dfee6cd0cb365)
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_value is not None:
                self._values["default_value"] = default_value
            if name is not None:
                self._values["name"] = name
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            '''Optional.

            The default value that is applied in the analysis template. The member who can query can override this value in the query editor.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-analysisparameter.html#cfn-cleanrooms-analysistemplate-analysisparameter-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the parameter.

            The name must use only alphanumeric, underscore (_), or hyphen (-) characters but cannot start or end with a hyphen.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-analysisparameter.html#cfn-cleanrooms-analysistemplate-analysisparameter-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-analysisparameter.html#cfn-cleanrooms-analysistemplate-analysisparameter-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnalysisParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnAnalysisTemplatePropsMixin.AnalysisSchemaProperty",
        jsii_struct_bases=[],
        name_mapping={"referenced_tables": "referencedTables"},
    )
    class AnalysisSchemaProperty:
        def __init__(
            self,
            *,
            referenced_tables: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A relation within an analysis.

            :param referenced_tables: The tables referenced in the analysis schema.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-analysisschema.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                analysis_schema_property = cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisSchemaProperty(
                    referenced_tables=["referencedTables"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dd1db4b4ba0a9b4913b54debef410a8d7b74d1a88898e46289083b1c2b2d3c9d)
                check_type(argname="argument referenced_tables", value=referenced_tables, expected_type=type_hints["referenced_tables"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if referenced_tables is not None:
                self._values["referenced_tables"] = referenced_tables

        @builtins.property
        def referenced_tables(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The tables referenced in the analysis schema.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-analysisschema.html#cfn-cleanrooms-analysistemplate-analysisschema-referencedtables
            '''
            result = self._values.get("referenced_tables")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnalysisSchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnAnalysisTemplatePropsMixin.AnalysisSourceMetadataProperty",
        jsii_struct_bases=[],
        name_mapping={"artifacts": "artifacts"},
    )
    class AnalysisSourceMetadataProperty:
        def __init__(
            self,
            *,
            artifacts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactMetadataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The analysis source metadata.

            :param artifacts: The artifacts of the analysis source metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-analysissourcemetadata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                analysis_source_metadata_property = cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisSourceMetadataProperty(
                    artifacts=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactMetadataProperty(
                        additional_artifact_hashes=[cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.HashProperty(
                            sha256="sha256"
                        )],
                        entry_point_hash=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.HashProperty(
                            sha256="sha256"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ce037a7fbfad6fe600f72cbafd243bdabd78dd1e696f4bffdadd9f9a663c380f)
                check_type(argname="argument artifacts", value=artifacts, expected_type=type_hints["artifacts"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if artifacts is not None:
                self._values["artifacts"] = artifacts

        @builtins.property
        def artifacts(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactMetadataProperty"]]:
            '''The artifacts of the analysis source metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-analysissourcemetadata.html#cfn-cleanrooms-analysistemplate-analysissourcemetadata-artifacts
            '''
            result = self._values.get("artifacts")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactMetadataProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnalysisSourceMetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnAnalysisTemplatePropsMixin.AnalysisSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"artifacts": "artifacts", "text": "text"},
    )
    class AnalysisSourceProperty:
        def __init__(
            self,
            *,
            artifacts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            text: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The structure that defines the body of the analysis template.

            :param artifacts: The artifacts of the analysis source.
            :param text: The query text.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-analysissource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                analysis_source_property = cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisSourceProperty(
                    artifacts=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactsProperty(
                        additional_artifacts=[cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactProperty(
                            location=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.S3LocationProperty(
                                bucket="bucket",
                                key="key"
                            )
                        )],
                        entry_point=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactProperty(
                            location=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.S3LocationProperty(
                                bucket="bucket",
                                key="key"
                            )
                        ),
                        role_arn="roleArn"
                    ),
                    text="text"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4f862f76358195b0a64d660c53fd47681077d93da442909b3c0e89a530cd5dae)
                check_type(argname="argument artifacts", value=artifacts, expected_type=type_hints["artifacts"])
                check_type(argname="argument text", value=text, expected_type=type_hints["text"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if artifacts is not None:
                self._values["artifacts"] = artifacts
            if text is not None:
                self._values["text"] = text

        @builtins.property
        def artifacts(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactsProperty"]]:
            '''The artifacts of the analysis source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-analysissource.html#cfn-cleanrooms-analysistemplate-analysissource-artifacts
            '''
            result = self._values.get("artifacts")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactsProperty"]], result)

        @builtins.property
        def text(self) -> typing.Optional[builtins.str]:
            '''The query text.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-analysissource.html#cfn-cleanrooms-analysistemplate-analysissource-text
            '''
            result = self._values.get("text")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnalysisSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactMetadataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "additional_artifact_hashes": "additionalArtifactHashes",
            "entry_point_hash": "entryPointHash",
        },
    )
    class AnalysisTemplateArtifactMetadataProperty:
        def __init__(
            self,
            *,
            additional_artifact_hashes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnalysisTemplatePropsMixin.HashProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            entry_point_hash: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnalysisTemplatePropsMixin.HashProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The analysis template artifact metadata.

            :param additional_artifact_hashes: Additional artifact hashes for the analysis template.
            :param entry_point_hash: The hash of the entry point for the analysis template artifact metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-analysistemplateartifactmetadata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                analysis_template_artifact_metadata_property = cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactMetadataProperty(
                    additional_artifact_hashes=[cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.HashProperty(
                        sha256="sha256"
                    )],
                    entry_point_hash=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.HashProperty(
                        sha256="sha256"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f22573795ac7aa34b8f1a1853249d31cba864fcb256f4764f97b90027e7530ac)
                check_type(argname="argument additional_artifact_hashes", value=additional_artifact_hashes, expected_type=type_hints["additional_artifact_hashes"])
                check_type(argname="argument entry_point_hash", value=entry_point_hash, expected_type=type_hints["entry_point_hash"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if additional_artifact_hashes is not None:
                self._values["additional_artifact_hashes"] = additional_artifact_hashes
            if entry_point_hash is not None:
                self._values["entry_point_hash"] = entry_point_hash

        @builtins.property
        def additional_artifact_hashes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalysisTemplatePropsMixin.HashProperty"]]]]:
            '''Additional artifact hashes for the analysis template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-analysistemplateartifactmetadata.html#cfn-cleanrooms-analysistemplate-analysistemplateartifactmetadata-additionalartifacthashes
            '''
            result = self._values.get("additional_artifact_hashes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalysisTemplatePropsMixin.HashProperty"]]]], result)

        @builtins.property
        def entry_point_hash(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalysisTemplatePropsMixin.HashProperty"]]:
            '''The hash of the entry point for the analysis template artifact metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-analysistemplateartifactmetadata.html#cfn-cleanrooms-analysistemplate-analysistemplateartifactmetadata-entrypointhash
            '''
            result = self._values.get("entry_point_hash")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalysisTemplatePropsMixin.HashProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnalysisTemplateArtifactMetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactProperty",
        jsii_struct_bases=[],
        name_mapping={"location": "location"},
    )
    class AnalysisTemplateArtifactProperty:
        def __init__(
            self,
            *,
            location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnalysisTemplatePropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The analysis template artifact.

            :param location: The artifact location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-analysistemplateartifact.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                analysis_template_artifact_property = cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactProperty(
                    location=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.S3LocationProperty(
                        bucket="bucket",
                        key="key"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8a6d69e9122a36d12434b19f82e5608fa8c44727a903bb895c82c0e5af605fa2)
                check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if location is not None:
                self._values["location"] = location

        @builtins.property
        def location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalysisTemplatePropsMixin.S3LocationProperty"]]:
            '''The artifact location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-analysistemplateartifact.html#cfn-cleanrooms-analysistemplate-analysistemplateartifact-location
            '''
            result = self._values.get("location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalysisTemplatePropsMixin.S3LocationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnalysisTemplateArtifactProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "additional_artifacts": "additionalArtifacts",
            "entry_point": "entryPoint",
            "role_arn": "roleArn",
        },
    )
    class AnalysisTemplateArtifactsProperty:
        def __init__(
            self,
            *,
            additional_artifacts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            entry_point: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The analysis template artifacts.

            :param additional_artifacts: Additional artifacts for the analysis template.
            :param entry_point: The entry point for the analysis template artifacts.
            :param role_arn: The role ARN for the analysis template artifacts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-analysistemplateartifacts.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                analysis_template_artifacts_property = cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactsProperty(
                    additional_artifacts=[cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactProperty(
                        location=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.S3LocationProperty(
                            bucket="bucket",
                            key="key"
                        )
                    )],
                    entry_point=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactProperty(
                        location=cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.S3LocationProperty(
                            bucket="bucket",
                            key="key"
                        )
                    ),
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5f5927493f9d2ed2c034725d174bddfafd3c03049d8f5bbe58ad53f96933cb30)
                check_type(argname="argument additional_artifacts", value=additional_artifacts, expected_type=type_hints["additional_artifacts"])
                check_type(argname="argument entry_point", value=entry_point, expected_type=type_hints["entry_point"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if additional_artifacts is not None:
                self._values["additional_artifacts"] = additional_artifacts
            if entry_point is not None:
                self._values["entry_point"] = entry_point
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def additional_artifacts(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactProperty"]]]]:
            '''Additional artifacts for the analysis template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-analysistemplateartifacts.html#cfn-cleanrooms-analysistemplate-analysistemplateartifacts-additionalartifacts
            '''
            result = self._values.get("additional_artifacts")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactProperty"]]]], result)

        @builtins.property
        def entry_point(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactProperty"]]:
            '''The entry point for the analysis template artifacts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-analysistemplateartifacts.html#cfn-cleanrooms-analysistemplate-analysistemplateartifacts-entrypoint
            '''
            result = self._values.get("entry_point")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactProperty"]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The role ARN for the analysis template artifacts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-analysistemplateartifacts.html#cfn-cleanrooms-analysistemplate-analysistemplateartifacts-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnalysisTemplateArtifactsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnAnalysisTemplatePropsMixin.ErrorMessageConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type"},
    )
    class ErrorMessageConfigurationProperty:
        def __init__(self, *, type: typing.Optional[builtins.str] = None) -> None:
            '''A structure that defines the level of detail included in error messages returned by PySpark jobs.

            This configuration allows you to control the verbosity of error messages to help with troubleshooting PySpark jobs while maintaining appropriate security controls.

            :param type: The level of detail for error messages returned by the PySpark job. When set to DETAILED, error messages include more information to help troubleshoot issues with your PySpark job. Because this setting may expose sensitive data, it is recommended for development and testing environments.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-errormessageconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                error_message_configuration_property = cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.ErrorMessageConfigurationProperty(
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__83a27208d4dc7c4a50c728dc58c535f2bda6be35da06ce09ac787df26b43c7b5)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The level of detail for error messages returned by the PySpark job.

            When set to DETAILED, error messages include more information to help troubleshoot issues with your PySpark job.

            Because this setting may expose sensitive data, it is recommended for development and testing environments.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-errormessageconfiguration.html#cfn-cleanrooms-analysistemplate-errormessageconfiguration-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ErrorMessageConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnAnalysisTemplatePropsMixin.HashProperty",
        jsii_struct_bases=[],
        name_mapping={"sha256": "sha256"},
    )
    class HashProperty:
        def __init__(self, *, sha256: typing.Optional[builtins.str] = None) -> None:
            '''Hash.

            :param sha256: The SHA-256 hash value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-hash.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                hash_property = cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.HashProperty(
                    sha256="sha256"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__57cfd23b400b72b074451008debb5927303b44ce2fe336a1a4f67f9dbc94530d)
                check_type(argname="argument sha256", value=sha256, expected_type=type_hints["sha256"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if sha256 is not None:
                self._values["sha256"] = sha256

        @builtins.property
        def sha256(self) -> typing.Optional[builtins.str]:
            '''The SHA-256 hash value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-hash.html#cfn-cleanrooms-analysistemplate-hash-sha256
            '''
            result = self._values.get("sha256")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HashProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnAnalysisTemplatePropsMixin.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The S3 location.

            :param bucket: The bucket name.
            :param key: The object key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                s3_location_property = cleanrooms_mixins.CfnAnalysisTemplatePropsMixin.S3LocationProperty(
                    bucket="bucket",
                    key="key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9b9d13b4a7fdeff35d45b961e6d8a1931a8fae554f2030115d6b34c3a85858d9)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if key is not None:
                self._values["key"] = key

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The bucket name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-s3location.html#cfn-cleanrooms-analysistemplate-s3location-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The object key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-analysistemplate-s3location.html#cfn-cleanrooms-analysistemplate-s3location-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnCollaborationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_result_regions": "allowedResultRegions",
        "analytics_engine": "analyticsEngine",
        "auto_approved_change_types": "autoApprovedChangeTypes",
        "creator_display_name": "creatorDisplayName",
        "creator_member_abilities": "creatorMemberAbilities",
        "creator_ml_member_abilities": "creatorMlMemberAbilities",
        "creator_payment_configuration": "creatorPaymentConfiguration",
        "data_encryption_metadata": "dataEncryptionMetadata",
        "description": "description",
        "job_log_status": "jobLogStatus",
        "members": "members",
        "name": "name",
        "query_log_status": "queryLogStatus",
        "tags": "tags",
    },
)
class CfnCollaborationMixinProps:
    def __init__(
        self,
        *,
        allowed_result_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        analytics_engine: typing.Optional[builtins.str] = None,
        auto_approved_change_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        creator_display_name: typing.Optional[builtins.str] = None,
        creator_member_abilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        creator_ml_member_abilities: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCollaborationPropsMixin.MLMemberAbilitiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        creator_payment_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCollaborationPropsMixin.PaymentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        data_encryption_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCollaborationPropsMixin.DataEncryptionMetadataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        job_log_status: typing.Optional[builtins.str] = None,
        members: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCollaborationPropsMixin.MemberSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        query_log_status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnCollaborationPropsMixin.

        :param allowed_result_regions: The AWS Regions where collaboration query results can be stored. Returns the list of Region identifiers that were specified when the collaboration was created. This list is used to enforce regional storage policies and compliance requirements.
        :param analytics_engine: The analytics engine for the collaboration. .. epigraph:: After July 16, 2025, the ``CLEAN_ROOMS_SQL`` parameter will no longer be available.
        :param auto_approved_change_types: The types of change requests that are automatically approved for this collaboration.
        :param creator_display_name: A display name of the collaboration creator.
        :param creator_member_abilities: The abilities granted to the collaboration creator. *Allowed values* ``CAN_QUERY`` | ``CAN_RECEIVE_RESULTS`` | ``CAN_RUN_JOB``
        :param creator_ml_member_abilities: The ML member abilities for a collaboration member.
        :param creator_payment_configuration: An object representing the collaboration member's payment responsibilities set by the collaboration creator.
        :param data_encryption_metadata: The settings for client-side encryption for cryptographic computing.
        :param description: A description of the collaboration provided by the collaboration owner.
        :param job_log_status: An indicator as to whether job logging has been enabled or disabled for the collaboration. When ``ENABLED`` , AWS Clean Rooms logs details about jobs run within this collaboration and those logs can be viewed in Amazon CloudWatch Logs. The default value is ``DISABLED`` .
        :param members: A list of initial members, not including the creator. This list is immutable.
        :param name: A human-readable identifier provided by the collaboration owner. Display names are not unique.
        :param query_log_status: An indicator as to whether query logging has been enabled or disabled for the collaboration. When ``ENABLED`` , AWS Clean Rooms logs details about queries run within this collaboration and those logs can be viewed in Amazon CloudWatch Logs. The default value is ``DISABLED`` .
        :param tags: An optional label that you can assign to a resource when you create it. Each tag consists of a key and an optional value, both of which you define. When you use tagging, you can also use tag-based access control in IAM policies to control access to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-collaboration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
            
            cfn_collaboration_mixin_props = cleanrooms_mixins.CfnCollaborationMixinProps(
                allowed_result_regions=["allowedResultRegions"],
                analytics_engine="analyticsEngine",
                auto_approved_change_types=["autoApprovedChangeTypes"],
                creator_display_name="creatorDisplayName",
                creator_member_abilities=["creatorMemberAbilities"],
                creator_ml_member_abilities=cleanrooms_mixins.CfnCollaborationPropsMixin.MLMemberAbilitiesProperty(
                    custom_ml_member_abilities=["customMlMemberAbilities"]
                ),
                creator_payment_configuration=cleanrooms_mixins.CfnCollaborationPropsMixin.PaymentConfigurationProperty(
                    job_compute=cleanrooms_mixins.CfnCollaborationPropsMixin.JobComputePaymentConfigProperty(
                        is_responsible=False
                    ),
                    machine_learning=cleanrooms_mixins.CfnCollaborationPropsMixin.MLPaymentConfigProperty(
                        model_inference=cleanrooms_mixins.CfnCollaborationPropsMixin.ModelInferencePaymentConfigProperty(
                            is_responsible=False
                        ),
                        model_training=cleanrooms_mixins.CfnCollaborationPropsMixin.ModelTrainingPaymentConfigProperty(
                            is_responsible=False
                        )
                    ),
                    query_compute=cleanrooms_mixins.CfnCollaborationPropsMixin.QueryComputePaymentConfigProperty(
                        is_responsible=False
                    )
                ),
                data_encryption_metadata=cleanrooms_mixins.CfnCollaborationPropsMixin.DataEncryptionMetadataProperty(
                    allow_cleartext=False,
                    allow_duplicates=False,
                    allow_joins_on_columns_with_different_names=False,
                    preserve_nulls=False
                ),
                description="description",
                job_log_status="jobLogStatus",
                members=[cleanrooms_mixins.CfnCollaborationPropsMixin.MemberSpecificationProperty(
                    account_id="accountId",
                    display_name="displayName",
                    member_abilities=["memberAbilities"],
                    ml_member_abilities=cleanrooms_mixins.CfnCollaborationPropsMixin.MLMemberAbilitiesProperty(
                        custom_ml_member_abilities=["customMlMemberAbilities"]
                    ),
                    payment_configuration=cleanrooms_mixins.CfnCollaborationPropsMixin.PaymentConfigurationProperty(
                        job_compute=cleanrooms_mixins.CfnCollaborationPropsMixin.JobComputePaymentConfigProperty(
                            is_responsible=False
                        ),
                        machine_learning=cleanrooms_mixins.CfnCollaborationPropsMixin.MLPaymentConfigProperty(
                            model_inference=cleanrooms_mixins.CfnCollaborationPropsMixin.ModelInferencePaymentConfigProperty(
                                is_responsible=False
                            ),
                            model_training=cleanrooms_mixins.CfnCollaborationPropsMixin.ModelTrainingPaymentConfigProperty(
                                is_responsible=False
                            )
                        ),
                        query_compute=cleanrooms_mixins.CfnCollaborationPropsMixin.QueryComputePaymentConfigProperty(
                            is_responsible=False
                        )
                    )
                )],
                name="name",
                query_log_status="queryLogStatus",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ea39ff5b61bad787c15e5b50ace1c380909aa708038178017c8f26a7032142f)
            check_type(argname="argument allowed_result_regions", value=allowed_result_regions, expected_type=type_hints["allowed_result_regions"])
            check_type(argname="argument analytics_engine", value=analytics_engine, expected_type=type_hints["analytics_engine"])
            check_type(argname="argument auto_approved_change_types", value=auto_approved_change_types, expected_type=type_hints["auto_approved_change_types"])
            check_type(argname="argument creator_display_name", value=creator_display_name, expected_type=type_hints["creator_display_name"])
            check_type(argname="argument creator_member_abilities", value=creator_member_abilities, expected_type=type_hints["creator_member_abilities"])
            check_type(argname="argument creator_ml_member_abilities", value=creator_ml_member_abilities, expected_type=type_hints["creator_ml_member_abilities"])
            check_type(argname="argument creator_payment_configuration", value=creator_payment_configuration, expected_type=type_hints["creator_payment_configuration"])
            check_type(argname="argument data_encryption_metadata", value=data_encryption_metadata, expected_type=type_hints["data_encryption_metadata"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument job_log_status", value=job_log_status, expected_type=type_hints["job_log_status"])
            check_type(argname="argument members", value=members, expected_type=type_hints["members"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument query_log_status", value=query_log_status, expected_type=type_hints["query_log_status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_result_regions is not None:
            self._values["allowed_result_regions"] = allowed_result_regions
        if analytics_engine is not None:
            self._values["analytics_engine"] = analytics_engine
        if auto_approved_change_types is not None:
            self._values["auto_approved_change_types"] = auto_approved_change_types
        if creator_display_name is not None:
            self._values["creator_display_name"] = creator_display_name
        if creator_member_abilities is not None:
            self._values["creator_member_abilities"] = creator_member_abilities
        if creator_ml_member_abilities is not None:
            self._values["creator_ml_member_abilities"] = creator_ml_member_abilities
        if creator_payment_configuration is not None:
            self._values["creator_payment_configuration"] = creator_payment_configuration
        if data_encryption_metadata is not None:
            self._values["data_encryption_metadata"] = data_encryption_metadata
        if description is not None:
            self._values["description"] = description
        if job_log_status is not None:
            self._values["job_log_status"] = job_log_status
        if members is not None:
            self._values["members"] = members
        if name is not None:
            self._values["name"] = name
        if query_log_status is not None:
            self._values["query_log_status"] = query_log_status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def allowed_result_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The AWS Regions where collaboration query results can be stored.

        Returns the list of Region identifiers that were specified when the collaboration was created. This list is used to enforce regional storage policies and compliance requirements.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-collaboration.html#cfn-cleanrooms-collaboration-allowedresultregions
        '''
        result = self._values.get("allowed_result_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def analytics_engine(self) -> typing.Optional[builtins.str]:
        '''The analytics engine for the collaboration.

        .. epigraph::

           After July 16, 2025, the ``CLEAN_ROOMS_SQL`` parameter will no longer be available.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-collaboration.html#cfn-cleanrooms-collaboration-analyticsengine
        '''
        result = self._values.get("analytics_engine")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_approved_change_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The types of change requests that are automatically approved for this collaboration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-collaboration.html#cfn-cleanrooms-collaboration-autoapprovedchangetypes
        '''
        result = self._values.get("auto_approved_change_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def creator_display_name(self) -> typing.Optional[builtins.str]:
        '''A display name of the collaboration creator.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-collaboration.html#cfn-cleanrooms-collaboration-creatordisplayname
        '''
        result = self._values.get("creator_display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def creator_member_abilities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The abilities granted to the collaboration creator.

        *Allowed values* ``CAN_QUERY`` | ``CAN_RECEIVE_RESULTS`` | ``CAN_RUN_JOB``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-collaboration.html#cfn-cleanrooms-collaboration-creatormemberabilities
        '''
        result = self._values.get("creator_member_abilities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def creator_ml_member_abilities(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCollaborationPropsMixin.MLMemberAbilitiesProperty"]]:
        '''The ML member abilities for a collaboration member.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-collaboration.html#cfn-cleanrooms-collaboration-creatormlmemberabilities
        '''
        result = self._values.get("creator_ml_member_abilities")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCollaborationPropsMixin.MLMemberAbilitiesProperty"]], result)

    @builtins.property
    def creator_payment_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCollaborationPropsMixin.PaymentConfigurationProperty"]]:
        '''An object representing the collaboration member's payment responsibilities set by the collaboration creator.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-collaboration.html#cfn-cleanrooms-collaboration-creatorpaymentconfiguration
        '''
        result = self._values.get("creator_payment_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCollaborationPropsMixin.PaymentConfigurationProperty"]], result)

    @builtins.property
    def data_encryption_metadata(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCollaborationPropsMixin.DataEncryptionMetadataProperty"]]:
        '''The settings for client-side encryption for cryptographic computing.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-collaboration.html#cfn-cleanrooms-collaboration-dataencryptionmetadata
        '''
        result = self._values.get("data_encryption_metadata")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCollaborationPropsMixin.DataEncryptionMetadataProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the collaboration provided by the collaboration owner.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-collaboration.html#cfn-cleanrooms-collaboration-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_log_status(self) -> typing.Optional[builtins.str]:
        '''An indicator as to whether job logging has been enabled or disabled for the collaboration.

        When ``ENABLED`` , AWS Clean Rooms logs details about jobs run within this collaboration and those logs can be viewed in Amazon CloudWatch Logs. The default value is ``DISABLED`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-collaboration.html#cfn-cleanrooms-collaboration-joblogstatus
        '''
        result = self._values.get("job_log_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def members(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCollaborationPropsMixin.MemberSpecificationProperty"]]]]:
        '''A list of initial members, not including the creator.

        This list is immutable.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-collaboration.html#cfn-cleanrooms-collaboration-members
        '''
        result = self._values.get("members")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCollaborationPropsMixin.MemberSpecificationProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A human-readable identifier provided by the collaboration owner.

        Display names are not unique.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-collaboration.html#cfn-cleanrooms-collaboration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_log_status(self) -> typing.Optional[builtins.str]:
        '''An indicator as to whether query logging has been enabled or disabled for the collaboration.

        When ``ENABLED`` , AWS Clean Rooms logs details about queries run within this collaboration and those logs can be viewed in Amazon CloudWatch Logs. The default value is ``DISABLED`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-collaboration.html#cfn-cleanrooms-collaboration-querylogstatus
        '''
        result = self._values.get("query_log_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An optional label that you can assign to a resource when you create it.

        Each tag consists of a key and an optional value, both of which you define. When you use tagging, you can also use tag-based access control in IAM policies to control access to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-collaboration.html#cfn-cleanrooms-collaboration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCollaborationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCollaborationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnCollaborationPropsMixin",
):
    '''Creates a new collaboration.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-collaboration.html
    :cloudformationResource: AWS::CleanRooms::Collaboration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
        
        cfn_collaboration_props_mixin = cleanrooms_mixins.CfnCollaborationPropsMixin(cleanrooms_mixins.CfnCollaborationMixinProps(
            allowed_result_regions=["allowedResultRegions"],
            analytics_engine="analyticsEngine",
            auto_approved_change_types=["autoApprovedChangeTypes"],
            creator_display_name="creatorDisplayName",
            creator_member_abilities=["creatorMemberAbilities"],
            creator_ml_member_abilities=cleanrooms_mixins.CfnCollaborationPropsMixin.MLMemberAbilitiesProperty(
                custom_ml_member_abilities=["customMlMemberAbilities"]
            ),
            creator_payment_configuration=cleanrooms_mixins.CfnCollaborationPropsMixin.PaymentConfigurationProperty(
                job_compute=cleanrooms_mixins.CfnCollaborationPropsMixin.JobComputePaymentConfigProperty(
                    is_responsible=False
                ),
                machine_learning=cleanrooms_mixins.CfnCollaborationPropsMixin.MLPaymentConfigProperty(
                    model_inference=cleanrooms_mixins.CfnCollaborationPropsMixin.ModelInferencePaymentConfigProperty(
                        is_responsible=False
                    ),
                    model_training=cleanrooms_mixins.CfnCollaborationPropsMixin.ModelTrainingPaymentConfigProperty(
                        is_responsible=False
                    )
                ),
                query_compute=cleanrooms_mixins.CfnCollaborationPropsMixin.QueryComputePaymentConfigProperty(
                    is_responsible=False
                )
            ),
            data_encryption_metadata=cleanrooms_mixins.CfnCollaborationPropsMixin.DataEncryptionMetadataProperty(
                allow_cleartext=False,
                allow_duplicates=False,
                allow_joins_on_columns_with_different_names=False,
                preserve_nulls=False
            ),
            description="description",
            job_log_status="jobLogStatus",
            members=[cleanrooms_mixins.CfnCollaborationPropsMixin.MemberSpecificationProperty(
                account_id="accountId",
                display_name="displayName",
                member_abilities=["memberAbilities"],
                ml_member_abilities=cleanrooms_mixins.CfnCollaborationPropsMixin.MLMemberAbilitiesProperty(
                    custom_ml_member_abilities=["customMlMemberAbilities"]
                ),
                payment_configuration=cleanrooms_mixins.CfnCollaborationPropsMixin.PaymentConfigurationProperty(
                    job_compute=cleanrooms_mixins.CfnCollaborationPropsMixin.JobComputePaymentConfigProperty(
                        is_responsible=False
                    ),
                    machine_learning=cleanrooms_mixins.CfnCollaborationPropsMixin.MLPaymentConfigProperty(
                        model_inference=cleanrooms_mixins.CfnCollaborationPropsMixin.ModelInferencePaymentConfigProperty(
                            is_responsible=False
                        ),
                        model_training=cleanrooms_mixins.CfnCollaborationPropsMixin.ModelTrainingPaymentConfigProperty(
                            is_responsible=False
                        )
                    ),
                    query_compute=cleanrooms_mixins.CfnCollaborationPropsMixin.QueryComputePaymentConfigProperty(
                        is_responsible=False
                    )
                )
            )],
            name="name",
            query_log_status="queryLogStatus",
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
        props: typing.Union[CfnCollaborationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CleanRooms::Collaboration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b57a17350d6f93ff651031eac1b1841f452dd9cb466fa2c0cb3b5433a172993e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__319b0642cf2d2d333e0e2f4ff0d4f6a772e15a9fe4d7fc8f00e3c5a826716901)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6f86f8826afca410ea44dd317102b0889e0ae208c345bc9a6dfae9ea3c417d3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCollaborationMixinProps:
        return typing.cast(CfnCollaborationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnCollaborationPropsMixin.DataEncryptionMetadataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_cleartext": "allowCleartext",
            "allow_duplicates": "allowDuplicates",
            "allow_joins_on_columns_with_different_names": "allowJoinsOnColumnsWithDifferentNames",
            "preserve_nulls": "preserveNulls",
        },
    )
    class DataEncryptionMetadataProperty:
        def __init__(
            self,
            *,
            allow_cleartext: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            allow_duplicates: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            allow_joins_on_columns_with_different_names: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            preserve_nulls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The settings for client-side encryption for cryptographic computing.

            :param allow_cleartext: Indicates whether encrypted tables can contain cleartext data ( ``TRUE`` ) or are to cryptographically process every column ( ``FALSE`` ).
            :param allow_duplicates: Indicates whether Fingerprint columns can contain duplicate entries ( ``TRUE`` ) or are to contain only non-repeated values ( ``FALSE`` ).
            :param allow_joins_on_columns_with_different_names: Indicates whether Fingerprint columns can be joined on any other Fingerprint column with a different name ( ``TRUE`` ) or can only be joined on Fingerprint columns of the same name ( ``FALSE`` ).
            :param preserve_nulls: Indicates whether NULL values are to be copied as NULL to encrypted tables ( ``TRUE`` ) or cryptographically processed ( ``FALSE`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-dataencryptionmetadata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                data_encryption_metadata_property = cleanrooms_mixins.CfnCollaborationPropsMixin.DataEncryptionMetadataProperty(
                    allow_cleartext=False,
                    allow_duplicates=False,
                    allow_joins_on_columns_with_different_names=False,
                    preserve_nulls=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b54e2181f6739fcc22c74be7ad2f5ee43eba6e831bdccbe0846c3dc9965f949f)
                check_type(argname="argument allow_cleartext", value=allow_cleartext, expected_type=type_hints["allow_cleartext"])
                check_type(argname="argument allow_duplicates", value=allow_duplicates, expected_type=type_hints["allow_duplicates"])
                check_type(argname="argument allow_joins_on_columns_with_different_names", value=allow_joins_on_columns_with_different_names, expected_type=type_hints["allow_joins_on_columns_with_different_names"])
                check_type(argname="argument preserve_nulls", value=preserve_nulls, expected_type=type_hints["preserve_nulls"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allow_cleartext is not None:
                self._values["allow_cleartext"] = allow_cleartext
            if allow_duplicates is not None:
                self._values["allow_duplicates"] = allow_duplicates
            if allow_joins_on_columns_with_different_names is not None:
                self._values["allow_joins_on_columns_with_different_names"] = allow_joins_on_columns_with_different_names
            if preserve_nulls is not None:
                self._values["preserve_nulls"] = preserve_nulls

        @builtins.property
        def allow_cleartext(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether encrypted tables can contain cleartext data ( ``TRUE`` ) or are to cryptographically process every column ( ``FALSE`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-dataencryptionmetadata.html#cfn-cleanrooms-collaboration-dataencryptionmetadata-allowcleartext
            '''
            result = self._values.get("allow_cleartext")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def allow_duplicates(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether Fingerprint columns can contain duplicate entries ( ``TRUE`` ) or are to contain only non-repeated values ( ``FALSE`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-dataencryptionmetadata.html#cfn-cleanrooms-collaboration-dataencryptionmetadata-allowduplicates
            '''
            result = self._values.get("allow_duplicates")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def allow_joins_on_columns_with_different_names(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether Fingerprint columns can be joined on any other Fingerprint column with a different name ( ``TRUE`` ) or can only be joined on Fingerprint columns of the same name ( ``FALSE`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-dataencryptionmetadata.html#cfn-cleanrooms-collaboration-dataencryptionmetadata-allowjoinsoncolumnswithdifferentnames
            '''
            result = self._values.get("allow_joins_on_columns_with_different_names")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def preserve_nulls(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether NULL values are to be copied as NULL to encrypted tables ( ``TRUE`` ) or cryptographically processed ( ``FALSE`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-dataencryptionmetadata.html#cfn-cleanrooms-collaboration-dataencryptionmetadata-preservenulls
            '''
            result = self._values.get("preserve_nulls")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataEncryptionMetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnCollaborationPropsMixin.JobComputePaymentConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"is_responsible": "isResponsible"},
    )
    class JobComputePaymentConfigProperty:
        def __init__(
            self,
            *,
            is_responsible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''An object representing the collaboration member's payment responsibilities set by the collaboration creator for query and job compute costs.

            :param is_responsible: Indicates whether the collaboration creator has configured the collaboration member to pay for query and job compute costs ( ``TRUE`` ) or has not configured the collaboration member to pay for query and job compute costs ( ``FALSE`` ). Exactly one member can be configured to pay for query and job compute costs. An error is returned if the collaboration creator sets a ``TRUE`` value for more than one member in the collaboration. An error is returned if the collaboration creator sets a ``FALSE`` value for the member who can run queries and jobs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-jobcomputepaymentconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                job_compute_payment_config_property = cleanrooms_mixins.CfnCollaborationPropsMixin.JobComputePaymentConfigProperty(
                    is_responsible=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__49216a932dabffabd427565f11aeadc7b854a7d8e76bf2667680eb917ea77b6a)
                check_type(argname="argument is_responsible", value=is_responsible, expected_type=type_hints["is_responsible"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_responsible is not None:
                self._values["is_responsible"] = is_responsible

        @builtins.property
        def is_responsible(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the collaboration creator has configured the collaboration member to pay for query and job compute costs ( ``TRUE`` ) or has not configured the collaboration member to pay for query and job compute costs ( ``FALSE`` ).

            Exactly one member can be configured to pay for query and job compute costs. An error is returned if the collaboration creator sets a ``TRUE`` value for more than one member in the collaboration.

            An error is returned if the collaboration creator sets a ``FALSE`` value for the member who can run queries and jobs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-jobcomputepaymentconfig.html#cfn-cleanrooms-collaboration-jobcomputepaymentconfig-isresponsible
            '''
            result = self._values.get("is_responsible")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JobComputePaymentConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnCollaborationPropsMixin.MLMemberAbilitiesProperty",
        jsii_struct_bases=[],
        name_mapping={"custom_ml_member_abilities": "customMlMemberAbilities"},
    )
    class MLMemberAbilitiesProperty:
        def __init__(
            self,
            *,
            custom_ml_member_abilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The ML member abilities for a collaboration member.

            :param custom_ml_member_abilities: The custom ML member abilities for a collaboration member.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-mlmemberabilities.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                m_lMember_abilities_property = cleanrooms_mixins.CfnCollaborationPropsMixin.MLMemberAbilitiesProperty(
                    custom_ml_member_abilities=["customMlMemberAbilities"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9c5eab10708d746f456ccf802dad8df554f316684af7a2dc78a602a51335c75e)
                check_type(argname="argument custom_ml_member_abilities", value=custom_ml_member_abilities, expected_type=type_hints["custom_ml_member_abilities"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_ml_member_abilities is not None:
                self._values["custom_ml_member_abilities"] = custom_ml_member_abilities

        @builtins.property
        def custom_ml_member_abilities(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The custom ML member abilities for a collaboration member.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-mlmemberabilities.html#cfn-cleanrooms-collaboration-mlmemberabilities-custommlmemberabilities
            '''
            result = self._values.get("custom_ml_member_abilities")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MLMemberAbilitiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnCollaborationPropsMixin.MLPaymentConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "model_inference": "modelInference",
            "model_training": "modelTraining",
        },
    )
    class MLPaymentConfigProperty:
        def __init__(
            self,
            *,
            model_inference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCollaborationPropsMixin.ModelInferencePaymentConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            model_training: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCollaborationPropsMixin.ModelTrainingPaymentConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object representing the collaboration member's machine learning payment responsibilities set by the collaboration creator.

            :param model_inference: The payment responsibilities accepted by the member for model inference.
            :param model_training: The payment responsibilities accepted by the member for model training.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-mlpaymentconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                m_lPayment_config_property = cleanrooms_mixins.CfnCollaborationPropsMixin.MLPaymentConfigProperty(
                    model_inference=cleanrooms_mixins.CfnCollaborationPropsMixin.ModelInferencePaymentConfigProperty(
                        is_responsible=False
                    ),
                    model_training=cleanrooms_mixins.CfnCollaborationPropsMixin.ModelTrainingPaymentConfigProperty(
                        is_responsible=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__45f13d3f0b6a5dfb7ff97dcf80b12c3c3610e0028ccdfc43954bd73d502e7d92)
                check_type(argname="argument model_inference", value=model_inference, expected_type=type_hints["model_inference"])
                check_type(argname="argument model_training", value=model_training, expected_type=type_hints["model_training"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if model_inference is not None:
                self._values["model_inference"] = model_inference
            if model_training is not None:
                self._values["model_training"] = model_training

        @builtins.property
        def model_inference(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCollaborationPropsMixin.ModelInferencePaymentConfigProperty"]]:
            '''The payment responsibilities accepted by the member for model inference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-mlpaymentconfig.html#cfn-cleanrooms-collaboration-mlpaymentconfig-modelinference
            '''
            result = self._values.get("model_inference")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCollaborationPropsMixin.ModelInferencePaymentConfigProperty"]], result)

        @builtins.property
        def model_training(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCollaborationPropsMixin.ModelTrainingPaymentConfigProperty"]]:
            '''The payment responsibilities accepted by the member for model training.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-mlpaymentconfig.html#cfn-cleanrooms-collaboration-mlpaymentconfig-modeltraining
            '''
            result = self._values.get("model_training")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCollaborationPropsMixin.ModelTrainingPaymentConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MLPaymentConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnCollaborationPropsMixin.MemberSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_id": "accountId",
            "display_name": "displayName",
            "member_abilities": "memberAbilities",
            "ml_member_abilities": "mlMemberAbilities",
            "payment_configuration": "paymentConfiguration",
        },
    )
    class MemberSpecificationProperty:
        def __init__(
            self,
            *,
            account_id: typing.Optional[builtins.str] = None,
            display_name: typing.Optional[builtins.str] = None,
            member_abilities: typing.Optional[typing.Sequence[builtins.str]] = None,
            ml_member_abilities: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCollaborationPropsMixin.MLMemberAbilitiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            payment_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCollaborationPropsMixin.PaymentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Basic metadata used to construct a new member.

            :param account_id: The identifier used to reference members of the collaboration. Currently only supports AWS account ID.
            :param display_name: The member's display name.
            :param member_abilities: The abilities granted to the collaboration member. *Allowed Values* : ``CAN_QUERY`` | ``CAN_RECEIVE_RESULTS``
            :param ml_member_abilities: The ML abilities granted to the collaboration member.
            :param payment_configuration: The collaboration member's payment responsibilities set by the collaboration creator. If the collaboration creator hasn't speciﬁed anyone as the member paying for query compute costs, then the member who can query is the default payer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-memberspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                member_specification_property = cleanrooms_mixins.CfnCollaborationPropsMixin.MemberSpecificationProperty(
                    account_id="accountId",
                    display_name="displayName",
                    member_abilities=["memberAbilities"],
                    ml_member_abilities=cleanrooms_mixins.CfnCollaborationPropsMixin.MLMemberAbilitiesProperty(
                        custom_ml_member_abilities=["customMlMemberAbilities"]
                    ),
                    payment_configuration=cleanrooms_mixins.CfnCollaborationPropsMixin.PaymentConfigurationProperty(
                        job_compute=cleanrooms_mixins.CfnCollaborationPropsMixin.JobComputePaymentConfigProperty(
                            is_responsible=False
                        ),
                        machine_learning=cleanrooms_mixins.CfnCollaborationPropsMixin.MLPaymentConfigProperty(
                            model_inference=cleanrooms_mixins.CfnCollaborationPropsMixin.ModelInferencePaymentConfigProperty(
                                is_responsible=False
                            ),
                            model_training=cleanrooms_mixins.CfnCollaborationPropsMixin.ModelTrainingPaymentConfigProperty(
                                is_responsible=False
                            )
                        ),
                        query_compute=cleanrooms_mixins.CfnCollaborationPropsMixin.QueryComputePaymentConfigProperty(
                            is_responsible=False
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__777b0ec90fb933a78331aec5ae715cab44b79a34d70978b920cadbc03bb2cdb1)
                check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
                check_type(argname="argument member_abilities", value=member_abilities, expected_type=type_hints["member_abilities"])
                check_type(argname="argument ml_member_abilities", value=ml_member_abilities, expected_type=type_hints["ml_member_abilities"])
                check_type(argname="argument payment_configuration", value=payment_configuration, expected_type=type_hints["payment_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_id is not None:
                self._values["account_id"] = account_id
            if display_name is not None:
                self._values["display_name"] = display_name
            if member_abilities is not None:
                self._values["member_abilities"] = member_abilities
            if ml_member_abilities is not None:
                self._values["ml_member_abilities"] = ml_member_abilities
            if payment_configuration is not None:
                self._values["payment_configuration"] = payment_configuration

        @builtins.property
        def account_id(self) -> typing.Optional[builtins.str]:
            '''The identifier used to reference members of the collaboration.

            Currently only supports AWS account ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-memberspecification.html#cfn-cleanrooms-collaboration-memberspecification-accountid
            '''
            result = self._values.get("account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def display_name(self) -> typing.Optional[builtins.str]:
            '''The member's display name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-memberspecification.html#cfn-cleanrooms-collaboration-memberspecification-displayname
            '''
            result = self._values.get("display_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def member_abilities(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The abilities granted to the collaboration member.

            *Allowed Values* : ``CAN_QUERY`` | ``CAN_RECEIVE_RESULTS``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-memberspecification.html#cfn-cleanrooms-collaboration-memberspecification-memberabilities
            '''
            result = self._values.get("member_abilities")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def ml_member_abilities(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCollaborationPropsMixin.MLMemberAbilitiesProperty"]]:
            '''The ML abilities granted to the collaboration member.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-memberspecification.html#cfn-cleanrooms-collaboration-memberspecification-mlmemberabilities
            '''
            result = self._values.get("ml_member_abilities")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCollaborationPropsMixin.MLMemberAbilitiesProperty"]], result)

        @builtins.property
        def payment_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCollaborationPropsMixin.PaymentConfigurationProperty"]]:
            '''The collaboration member's payment responsibilities set by the collaboration creator.

            If the collaboration creator hasn't speciﬁed anyone as the member paying for query compute costs, then the member who can query is the default payer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-memberspecification.html#cfn-cleanrooms-collaboration-memberspecification-paymentconfiguration
            '''
            result = self._values.get("payment_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCollaborationPropsMixin.PaymentConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MemberSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnCollaborationPropsMixin.ModelInferencePaymentConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"is_responsible": "isResponsible"},
    )
    class ModelInferencePaymentConfigProperty:
        def __init__(
            self,
            *,
            is_responsible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''An object representing the collaboration member's model inference payment responsibilities set by the collaboration creator.

            :param is_responsible: Indicates whether the collaboration creator has configured the collaboration member to pay for model inference costs ( ``TRUE`` ) or has not configured the collaboration member to pay for model inference costs ( ``FALSE`` ). Exactly one member can be configured to pay for model inference costs. An error is returned if the collaboration creator sets a ``TRUE`` value for more than one member in the collaboration. If the collaboration creator hasn't specified anyone as the member paying for model inference costs, then the member who can query is the default payer. An error is returned if the collaboration creator sets a ``FALSE`` value for the member who can query.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-modelinferencepaymentconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                model_inference_payment_config_property = cleanrooms_mixins.CfnCollaborationPropsMixin.ModelInferencePaymentConfigProperty(
                    is_responsible=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8edd55504c3bbd2ee7e5bd2d6d6e7fc991c3368944d7885e92bd07c9898b3f4f)
                check_type(argname="argument is_responsible", value=is_responsible, expected_type=type_hints["is_responsible"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_responsible is not None:
                self._values["is_responsible"] = is_responsible

        @builtins.property
        def is_responsible(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the collaboration creator has configured the collaboration member to pay for model inference costs ( ``TRUE`` ) or has not configured the collaboration member to pay for model inference costs ( ``FALSE`` ).

            Exactly one member can be configured to pay for model inference costs. An error is returned if the collaboration creator sets a ``TRUE`` value for more than one member in the collaboration.

            If the collaboration creator hasn't specified anyone as the member paying for model inference costs, then the member who can query is the default payer. An error is returned if the collaboration creator sets a ``FALSE`` value for the member who can query.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-modelinferencepaymentconfig.html#cfn-cleanrooms-collaboration-modelinferencepaymentconfig-isresponsible
            '''
            result = self._values.get("is_responsible")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ModelInferencePaymentConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnCollaborationPropsMixin.ModelTrainingPaymentConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"is_responsible": "isResponsible"},
    )
    class ModelTrainingPaymentConfigProperty:
        def __init__(
            self,
            *,
            is_responsible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''An object representing the collaboration member's model training payment responsibilities set by the collaboration creator.

            :param is_responsible: Indicates whether the collaboration creator has configured the collaboration member to pay for model training costs ( ``TRUE`` ) or has not configured the collaboration member to pay for model training costs ( ``FALSE`` ). Exactly one member can be configured to pay for model training costs. An error is returned if the collaboration creator sets a ``TRUE`` value for more than one member in the collaboration. If the collaboration creator hasn't specified anyone as the member paying for model training costs, then the member who can query is the default payer. An error is returned if the collaboration creator sets a ``FALSE`` value for the member who can query.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-modeltrainingpaymentconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                model_training_payment_config_property = cleanrooms_mixins.CfnCollaborationPropsMixin.ModelTrainingPaymentConfigProperty(
                    is_responsible=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e5cc864fbf6b607d41efe78ecce5c0bae8f008116fbb21064dfa7d6592234aa3)
                check_type(argname="argument is_responsible", value=is_responsible, expected_type=type_hints["is_responsible"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_responsible is not None:
                self._values["is_responsible"] = is_responsible

        @builtins.property
        def is_responsible(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the collaboration creator has configured the collaboration member to pay for model training costs ( ``TRUE`` ) or has not configured the collaboration member to pay for model training costs ( ``FALSE`` ).

            Exactly one member can be configured to pay for model training costs. An error is returned if the collaboration creator sets a ``TRUE`` value for more than one member in the collaboration.

            If the collaboration creator hasn't specified anyone as the member paying for model training costs, then the member who can query is the default payer. An error is returned if the collaboration creator sets a ``FALSE`` value for the member who can query.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-modeltrainingpaymentconfig.html#cfn-cleanrooms-collaboration-modeltrainingpaymentconfig-isresponsible
            '''
            result = self._values.get("is_responsible")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ModelTrainingPaymentConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnCollaborationPropsMixin.PaymentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "job_compute": "jobCompute",
            "machine_learning": "machineLearning",
            "query_compute": "queryCompute",
        },
    )
    class PaymentConfigurationProperty:
        def __init__(
            self,
            *,
            job_compute: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCollaborationPropsMixin.JobComputePaymentConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            machine_learning: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCollaborationPropsMixin.MLPaymentConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            query_compute: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCollaborationPropsMixin.QueryComputePaymentConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object representing the collaboration member's payment responsibilities set by the collaboration creator.

            :param job_compute: The compute configuration for the job.
            :param machine_learning: An object representing the collaboration member's machine learning payment responsibilities set by the collaboration creator.
            :param query_compute: The collaboration member's payment responsibilities set by the collaboration creator for query compute costs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-paymentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                payment_configuration_property = cleanrooms_mixins.CfnCollaborationPropsMixin.PaymentConfigurationProperty(
                    job_compute=cleanrooms_mixins.CfnCollaborationPropsMixin.JobComputePaymentConfigProperty(
                        is_responsible=False
                    ),
                    machine_learning=cleanrooms_mixins.CfnCollaborationPropsMixin.MLPaymentConfigProperty(
                        model_inference=cleanrooms_mixins.CfnCollaborationPropsMixin.ModelInferencePaymentConfigProperty(
                            is_responsible=False
                        ),
                        model_training=cleanrooms_mixins.CfnCollaborationPropsMixin.ModelTrainingPaymentConfigProperty(
                            is_responsible=False
                        )
                    ),
                    query_compute=cleanrooms_mixins.CfnCollaborationPropsMixin.QueryComputePaymentConfigProperty(
                        is_responsible=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7f01c665e99303d0485d4dffc8b5d04bfe8b494e7eba4fa3b4d3972b801b5968)
                check_type(argname="argument job_compute", value=job_compute, expected_type=type_hints["job_compute"])
                check_type(argname="argument machine_learning", value=machine_learning, expected_type=type_hints["machine_learning"])
                check_type(argname="argument query_compute", value=query_compute, expected_type=type_hints["query_compute"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if job_compute is not None:
                self._values["job_compute"] = job_compute
            if machine_learning is not None:
                self._values["machine_learning"] = machine_learning
            if query_compute is not None:
                self._values["query_compute"] = query_compute

        @builtins.property
        def job_compute(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCollaborationPropsMixin.JobComputePaymentConfigProperty"]]:
            '''The compute configuration for the job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-paymentconfiguration.html#cfn-cleanrooms-collaboration-paymentconfiguration-jobcompute
            '''
            result = self._values.get("job_compute")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCollaborationPropsMixin.JobComputePaymentConfigProperty"]], result)

        @builtins.property
        def machine_learning(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCollaborationPropsMixin.MLPaymentConfigProperty"]]:
            '''An object representing the collaboration member's machine learning payment responsibilities set by the collaboration creator.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-paymentconfiguration.html#cfn-cleanrooms-collaboration-paymentconfiguration-machinelearning
            '''
            result = self._values.get("machine_learning")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCollaborationPropsMixin.MLPaymentConfigProperty"]], result)

        @builtins.property
        def query_compute(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCollaborationPropsMixin.QueryComputePaymentConfigProperty"]]:
            '''The collaboration member's payment responsibilities set by the collaboration creator for query compute costs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-paymentconfiguration.html#cfn-cleanrooms-collaboration-paymentconfiguration-querycompute
            '''
            result = self._values.get("query_compute")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCollaborationPropsMixin.QueryComputePaymentConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PaymentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnCollaborationPropsMixin.QueryComputePaymentConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"is_responsible": "isResponsible"},
    )
    class QueryComputePaymentConfigProperty:
        def __init__(
            self,
            *,
            is_responsible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''An object representing the collaboration member's payment responsibilities set by the collaboration creator for query compute costs.

            :param is_responsible: Indicates whether the collaboration creator has configured the collaboration member to pay for query compute costs ( ``TRUE`` ) or has not configured the collaboration member to pay for query compute costs ( ``FALSE`` ). Exactly one member can be configured to pay for query compute costs. An error is returned if the collaboration creator sets a ``TRUE`` value for more than one member in the collaboration. If the collaboration creator hasn't specified anyone as the member paying for query compute costs, then the member who can query is the default payer. An error is returned if the collaboration creator sets a ``FALSE`` value for the member who can query.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-querycomputepaymentconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                query_compute_payment_config_property = cleanrooms_mixins.CfnCollaborationPropsMixin.QueryComputePaymentConfigProperty(
                    is_responsible=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f6fd78b987339570fad670459dbce32144b03581550ec9bff75fcc827539d5ff)
                check_type(argname="argument is_responsible", value=is_responsible, expected_type=type_hints["is_responsible"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_responsible is not None:
                self._values["is_responsible"] = is_responsible

        @builtins.property
        def is_responsible(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the collaboration creator has configured the collaboration member to pay for query compute costs ( ``TRUE`` ) or has not configured the collaboration member to pay for query compute costs ( ``FALSE`` ).

            Exactly one member can be configured to pay for query compute costs. An error is returned if the collaboration creator sets a ``TRUE`` value for more than one member in the collaboration.

            If the collaboration creator hasn't specified anyone as the member paying for query compute costs, then the member who can query is the default payer. An error is returned if the collaboration creator sets a ``FALSE`` value for the member who can query.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-collaboration-querycomputepaymentconfig.html#cfn-cleanrooms-collaboration-querycomputepaymentconfig-isresponsible
            '''
            result = self._values.get("is_responsible")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueryComputePaymentConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTableAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "configured_table_association_analysis_rules": "configuredTableAssociationAnalysisRules",
        "configured_table_identifier": "configuredTableIdentifier",
        "description": "description",
        "membership_identifier": "membershipIdentifier",
        "name": "name",
        "role_arn": "roleArn",
        "tags": "tags",
    },
)
class CfnConfiguredTableAssociationMixinProps:
    def __init__(
        self,
        *,
        configured_table_association_analysis_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        configured_table_identifier: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        membership_identifier: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnConfiguredTableAssociationPropsMixin.

        :param configured_table_association_analysis_rules: An analysis rule for a configured table association. This analysis rule specifies how data from the table can be used within its associated collaboration. In the console, the ``ConfiguredTableAssociationAnalysisRule`` is referred to as the *collaboration analysis rule* .
        :param configured_table_identifier: A unique identifier for the configured table to be associated to. Currently accepts a configured table ID.
        :param description: A description of the configured table association.
        :param membership_identifier: The unique ID for the membership this configured table association belongs to.
        :param name: The name of the configured table association, in lowercase. The table is identified by this name when running protected queries against the underlying data.
        :param role_arn: The service will assume this role to access catalog metadata and query the table.
        :param tags: An optional label that you can assign to a resource when you create it. Each tag consists of a key and an optional value, both of which you define. When you use tagging, you can also use tag-based access control in IAM policies to control access to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-configuredtableassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
            
            cfn_configured_table_association_mixin_props = cleanrooms_mixins.CfnConfiguredTableAssociationMixinProps(
                configured_table_association_analysis_rules=[cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleProperty(
                    policy=cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRulePolicyProperty(
                        v1=cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRulePolicyV1Property(
                            aggregation=cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleAggregationProperty(
                                allowed_additional_analyses=["allowedAdditionalAnalyses"],
                                allowed_result_receivers=["allowedResultReceivers"]
                            ),
                            custom=cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleCustomProperty(
                                allowed_additional_analyses=["allowedAdditionalAnalyses"],
                                allowed_result_receivers=["allowedResultReceivers"]
                            ),
                            list=cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleListProperty(
                                allowed_additional_analyses=["allowedAdditionalAnalyses"],
                                allowed_result_receivers=["allowedResultReceivers"]
                            )
                        )
                    ),
                    type="type"
                )],
                configured_table_identifier="configuredTableIdentifier",
                description="description",
                membership_identifier="membershipIdentifier",
                name="name",
                role_arn="roleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1bc30b270d4a63c962839b563554f1a724a6555136bfbfba7ffa534d64a1ad6)
            check_type(argname="argument configured_table_association_analysis_rules", value=configured_table_association_analysis_rules, expected_type=type_hints["configured_table_association_analysis_rules"])
            check_type(argname="argument configured_table_identifier", value=configured_table_identifier, expected_type=type_hints["configured_table_identifier"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument membership_identifier", value=membership_identifier, expected_type=type_hints["membership_identifier"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configured_table_association_analysis_rules is not None:
            self._values["configured_table_association_analysis_rules"] = configured_table_association_analysis_rules
        if configured_table_identifier is not None:
            self._values["configured_table_identifier"] = configured_table_identifier
        if description is not None:
            self._values["description"] = description
        if membership_identifier is not None:
            self._values["membership_identifier"] = membership_identifier
        if name is not None:
            self._values["name"] = name
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def configured_table_association_analysis_rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleProperty"]]]]:
        '''An analysis rule for a configured table association.

        This analysis rule specifies how data from the table can be used within its associated collaboration. In the console, the ``ConfiguredTableAssociationAnalysisRule`` is referred to as the *collaboration analysis rule* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-configuredtableassociation.html#cfn-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrules
        '''
        result = self._values.get("configured_table_association_analysis_rules")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleProperty"]]]], result)

    @builtins.property
    def configured_table_identifier(self) -> typing.Optional[builtins.str]:
        '''A unique identifier for the configured table to be associated to.

        Currently accepts a configured table ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-configuredtableassociation.html#cfn-cleanrooms-configuredtableassociation-configuredtableidentifier
        '''
        result = self._values.get("configured_table_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the configured table association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-configuredtableassociation.html#cfn-cleanrooms-configuredtableassociation-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def membership_identifier(self) -> typing.Optional[builtins.str]:
        '''The unique ID for the membership this configured table association belongs to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-configuredtableassociation.html#cfn-cleanrooms-configuredtableassociation-membershipidentifier
        '''
        result = self._values.get("membership_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the configured table association, in lowercase.

        The table is identified by this name when running protected queries against the underlying data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-configuredtableassociation.html#cfn-cleanrooms-configuredtableassociation-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The service will assume this role to access catalog metadata and query the table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-configuredtableassociation.html#cfn-cleanrooms-configuredtableassociation-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An optional label that you can assign to a resource when you create it.

        Each tag consists of a key and an optional value, both of which you define. When you use tagging, you can also use tag-based access control in IAM policies to control access to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-configuredtableassociation.html#cfn-cleanrooms-configuredtableassociation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfiguredTableAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConfiguredTableAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTableAssociationPropsMixin",
):
    '''Creates a configured table association.

    A configured table association links a configured table with a collaboration.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-configuredtableassociation.html
    :cloudformationResource: AWS::CleanRooms::ConfiguredTableAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
        
        cfn_configured_table_association_props_mixin = cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin(cleanrooms_mixins.CfnConfiguredTableAssociationMixinProps(
            configured_table_association_analysis_rules=[cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleProperty(
                policy=cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRulePolicyProperty(
                    v1=cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRulePolicyV1Property(
                        aggregation=cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleAggregationProperty(
                            allowed_additional_analyses=["allowedAdditionalAnalyses"],
                            allowed_result_receivers=["allowedResultReceivers"]
                        ),
                        custom=cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleCustomProperty(
                            allowed_additional_analyses=["allowedAdditionalAnalyses"],
                            allowed_result_receivers=["allowedResultReceivers"]
                        ),
                        list=cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleListProperty(
                            allowed_additional_analyses=["allowedAdditionalAnalyses"],
                            allowed_result_receivers=["allowedResultReceivers"]
                        )
                    )
                ),
                type="type"
            )],
            configured_table_identifier="configuredTableIdentifier",
            description="description",
            membership_identifier="membershipIdentifier",
            name="name",
            role_arn="roleArn",
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
        props: typing.Union[CfnConfiguredTableAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CleanRooms::ConfiguredTableAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84ed15b8fc7deddff41af707ea802636f527da6a1ed3fecc2b03bf86ea1bfe35)
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
            type_hints = typing.get_type_hints(_typecheckingstub__58d70560304cc1e39da61c98fde12340d9156a941da6c4b1c6e0b7f5698fcd76)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70eefe73b141466e27d0f136735cc72dd936f871c4cd4faf3a65f7e34a51660d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConfiguredTableAssociationMixinProps:
        return typing.cast(CfnConfiguredTableAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleAggregationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_additional_analyses": "allowedAdditionalAnalyses",
            "allowed_result_receivers": "allowedResultReceivers",
        },
    )
    class ConfiguredTableAssociationAnalysisRuleAggregationProperty:
        def __init__(
            self,
            *,
            allowed_additional_analyses: typing.Optional[typing.Sequence[builtins.str]] = None,
            allowed_result_receivers: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The configured table association analysis rule applied to a configured table with the aggregation analysis rule.

            :param allowed_additional_analyses: The list of resources or wildcards (ARNs) that are allowed to perform additional analysis on query output. The ``allowedAdditionalAnalyses`` parameter is currently supported for the list analysis rule ( ``AnalysisRuleList`` ) and the custom analysis rule ( ``AnalysisRuleCustom`` ).
            :param allowed_result_receivers: The list of collaboration members who are allowed to receive results of queries run with this configured table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtableassociation-configuredtableassociationanalysisruleaggregation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                configured_table_association_analysis_rule_aggregation_property = cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleAggregationProperty(
                    allowed_additional_analyses=["allowedAdditionalAnalyses"],
                    allowed_result_receivers=["allowedResultReceivers"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__94a76d937b91da6d27c28e1aadd59e31fd4120d66c7c95b62f6df64f8b54d89c)
                check_type(argname="argument allowed_additional_analyses", value=allowed_additional_analyses, expected_type=type_hints["allowed_additional_analyses"])
                check_type(argname="argument allowed_result_receivers", value=allowed_result_receivers, expected_type=type_hints["allowed_result_receivers"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_additional_analyses is not None:
                self._values["allowed_additional_analyses"] = allowed_additional_analyses
            if allowed_result_receivers is not None:
                self._values["allowed_result_receivers"] = allowed_result_receivers

        @builtins.property
        def allowed_additional_analyses(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of resources or wildcards (ARNs) that are allowed to perform additional analysis on query output.

            The ``allowedAdditionalAnalyses`` parameter is currently supported for the list analysis rule ( ``AnalysisRuleList`` ) and the custom analysis rule ( ``AnalysisRuleCustom`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtableassociation-configuredtableassociationanalysisruleaggregation.html#cfn-cleanrooms-configuredtableassociation-configuredtableassociationanalysisruleaggregation-allowedadditionalanalyses
            '''
            result = self._values.get("allowed_additional_analyses")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allowed_result_receivers(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of collaboration members who are allowed to receive results of queries run with this configured table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtableassociation-configuredtableassociationanalysisruleaggregation.html#cfn-cleanrooms-configuredtableassociation-configuredtableassociationanalysisruleaggregation-allowedresultreceivers
            '''
            result = self._values.get("allowed_result_receivers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfiguredTableAssociationAnalysisRuleAggregationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleCustomProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_additional_analyses": "allowedAdditionalAnalyses",
            "allowed_result_receivers": "allowedResultReceivers",
        },
    )
    class ConfiguredTableAssociationAnalysisRuleCustomProperty:
        def __init__(
            self,
            *,
            allowed_additional_analyses: typing.Optional[typing.Sequence[builtins.str]] = None,
            allowed_result_receivers: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The configured table association analysis rule applied to a configured table with the custom analysis rule.

            :param allowed_additional_analyses: The list of resources or wildcards (ARNs) that are allowed to perform additional analysis on query output.
            :param allowed_result_receivers: The list of collaboration members who are allowed to receive results of queries run with this configured table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrulecustom.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                configured_table_association_analysis_rule_custom_property = cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleCustomProperty(
                    allowed_additional_analyses=["allowedAdditionalAnalyses"],
                    allowed_result_receivers=["allowedResultReceivers"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__821e4e85fbee1ffe47b53ad675978f2c6adaadbe8c09223dc10c61d2d43294a9)
                check_type(argname="argument allowed_additional_analyses", value=allowed_additional_analyses, expected_type=type_hints["allowed_additional_analyses"])
                check_type(argname="argument allowed_result_receivers", value=allowed_result_receivers, expected_type=type_hints["allowed_result_receivers"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_additional_analyses is not None:
                self._values["allowed_additional_analyses"] = allowed_additional_analyses
            if allowed_result_receivers is not None:
                self._values["allowed_result_receivers"] = allowed_result_receivers

        @builtins.property
        def allowed_additional_analyses(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of resources or wildcards (ARNs) that are allowed to perform additional analysis on query output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrulecustom.html#cfn-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrulecustom-allowedadditionalanalyses
            '''
            result = self._values.get("allowed_additional_analyses")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allowed_result_receivers(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of collaboration members who are allowed to receive results of queries run with this configured table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrulecustom.html#cfn-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrulecustom-allowedresultreceivers
            '''
            result = self._values.get("allowed_result_receivers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfiguredTableAssociationAnalysisRuleCustomProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleListProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_additional_analyses": "allowedAdditionalAnalyses",
            "allowed_result_receivers": "allowedResultReceivers",
        },
    )
    class ConfiguredTableAssociationAnalysisRuleListProperty:
        def __init__(
            self,
            *,
            allowed_additional_analyses: typing.Optional[typing.Sequence[builtins.str]] = None,
            allowed_result_receivers: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The configured table association analysis rule applied to a configured table with the list analysis rule.

            :param allowed_additional_analyses: The list of resources or wildcards (ARNs) that are allowed to perform additional analysis on query output.
            :param allowed_result_receivers: The list of collaboration members who are allowed to receive results of queries run with this configured table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrulelist.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                configured_table_association_analysis_rule_list_property = cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleListProperty(
                    allowed_additional_analyses=["allowedAdditionalAnalyses"],
                    allowed_result_receivers=["allowedResultReceivers"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d64aa56b88d2720f7c37c9b6abc83df0ed086623c2b7da4ebcf5264138452f7)
                check_type(argname="argument allowed_additional_analyses", value=allowed_additional_analyses, expected_type=type_hints["allowed_additional_analyses"])
                check_type(argname="argument allowed_result_receivers", value=allowed_result_receivers, expected_type=type_hints["allowed_result_receivers"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_additional_analyses is not None:
                self._values["allowed_additional_analyses"] = allowed_additional_analyses
            if allowed_result_receivers is not None:
                self._values["allowed_result_receivers"] = allowed_result_receivers

        @builtins.property
        def allowed_additional_analyses(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of resources or wildcards (ARNs) that are allowed to perform additional analysis on query output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrulelist.html#cfn-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrulelist-allowedadditionalanalyses
            '''
            result = self._values.get("allowed_additional_analyses")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allowed_result_receivers(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of collaboration members who are allowed to receive results of queries run with this configured table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrulelist.html#cfn-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrulelist-allowedresultreceivers
            '''
            result = self._values.get("allowed_result_receivers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfiguredTableAssociationAnalysisRuleListProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRulePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"v1": "v1"},
    )
    class ConfiguredTableAssociationAnalysisRulePolicyProperty:
        def __init__(
            self,
            *,
            v1: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRulePolicyV1Property", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Controls on the query specifications that can be run on an associated configured table.

            :param v1: The policy for the configured table association analysis rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrulepolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                configured_table_association_analysis_rule_policy_property = cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRulePolicyProperty(
                    v1=cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRulePolicyV1Property(
                        aggregation=cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleAggregationProperty(
                            allowed_additional_analyses=["allowedAdditionalAnalyses"],
                            allowed_result_receivers=["allowedResultReceivers"]
                        ),
                        custom=cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleCustomProperty(
                            allowed_additional_analyses=["allowedAdditionalAnalyses"],
                            allowed_result_receivers=["allowedResultReceivers"]
                        ),
                        list=cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleListProperty(
                            allowed_additional_analyses=["allowedAdditionalAnalyses"],
                            allowed_result_receivers=["allowedResultReceivers"]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ee5f13a76045707f6f85790aba57f40fcebea341bc3e7c37ca09837ffe1b9116)
                check_type(argname="argument v1", value=v1, expected_type=type_hints["v1"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if v1 is not None:
                self._values["v1"] = v1

        @builtins.property
        def v1(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRulePolicyV1Property"]]:
            '''The policy for the configured table association analysis rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrulepolicy.html#cfn-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrulepolicy-v1
            '''
            result = self._values.get("v1")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRulePolicyV1Property"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfiguredTableAssociationAnalysisRulePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRulePolicyV1Property",
        jsii_struct_bases=[],
        name_mapping={
            "aggregation": "aggregation",
            "custom": "custom",
            "list": "list",
        },
    )
    class ConfiguredTableAssociationAnalysisRulePolicyV1Property:
        def __init__(
            self,
            *,
            aggregation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleAggregationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            custom: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleCustomProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleListProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Controls on the query specifications that can be run on an associated configured table.

            :param aggregation: Analysis rule type that enables only aggregation queries on a configured table.
            :param custom: Analysis rule type that enables the table owner to approve custom SQL queries on their configured tables. It supports differential privacy.
            :param list: Analysis rule type that enables only list queries on a configured table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrulepolicyv1.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                configured_table_association_analysis_rule_policy_v1_property = cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRulePolicyV1Property(
                    aggregation=cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleAggregationProperty(
                        allowed_additional_analyses=["allowedAdditionalAnalyses"],
                        allowed_result_receivers=["allowedResultReceivers"]
                    ),
                    custom=cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleCustomProperty(
                        allowed_additional_analyses=["allowedAdditionalAnalyses"],
                        allowed_result_receivers=["allowedResultReceivers"]
                    ),
                    list=cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleListProperty(
                        allowed_additional_analyses=["allowedAdditionalAnalyses"],
                        allowed_result_receivers=["allowedResultReceivers"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a1697dbe5f38950e949d73b88dc008adde5db7da555146058798496a9acf22e4)
                check_type(argname="argument aggregation", value=aggregation, expected_type=type_hints["aggregation"])
                check_type(argname="argument custom", value=custom, expected_type=type_hints["custom"])
                check_type(argname="argument list", value=list, expected_type=type_hints["list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aggregation is not None:
                self._values["aggregation"] = aggregation
            if custom is not None:
                self._values["custom"] = custom
            if list is not None:
                self._values["list"] = list

        @builtins.property
        def aggregation(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleAggregationProperty"]]:
            '''Analysis rule type that enables only aggregation queries on a configured table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrulepolicyv1.html#cfn-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrulepolicyv1-aggregation
            '''
            result = self._values.get("aggregation")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleAggregationProperty"]], result)

        @builtins.property
        def custom(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleCustomProperty"]]:
            '''Analysis rule type that enables the table owner to approve custom SQL queries on their configured tables.

            It supports differential privacy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrulepolicyv1.html#cfn-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrulepolicyv1-custom
            '''
            result = self._values.get("custom")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleCustomProperty"]], result)

        @builtins.property
        def list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleListProperty"]]:
            '''Analysis rule type that enables only list queries on a configured table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrulepolicyv1.html#cfn-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrulepolicyv1-list
            '''
            result = self._values.get("list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleListProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfiguredTableAssociationAnalysisRulePolicyV1Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"policy": "policy", "type": "type"},
    )
    class ConfiguredTableAssociationAnalysisRuleProperty:
        def __init__(
            self,
            *,
            policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRulePolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An analysis rule for a configured table association.

            This analysis rule specifies how data from the table can be used within its associated collaboration. In the console, the ``ConfiguredTableAssociationAnalysisRule`` is referred to as the *collaboration analysis rule* .

            :param policy: The policy of the configured table association analysis rule.
            :param type: The type of the configured table association analysis rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                configured_table_association_analysis_rule_property = cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleProperty(
                    policy=cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRulePolicyProperty(
                        v1=cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRulePolicyV1Property(
                            aggregation=cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleAggregationProperty(
                                allowed_additional_analyses=["allowedAdditionalAnalyses"],
                                allowed_result_receivers=["allowedResultReceivers"]
                            ),
                            custom=cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleCustomProperty(
                                allowed_additional_analyses=["allowedAdditionalAnalyses"],
                                allowed_result_receivers=["allowedResultReceivers"]
                            ),
                            list=cleanrooms_mixins.CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleListProperty(
                                allowed_additional_analyses=["allowedAdditionalAnalyses"],
                                allowed_result_receivers=["allowedResultReceivers"]
                            )
                        )
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ec00ec22aff657cffa7ec698a79e595ef1b52fb8c075653631489cbdaf4f7d6c)
                check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if policy is not None:
                self._values["policy"] = policy
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRulePolicyProperty"]]:
            '''The policy of the configured table association analysis rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrule.html#cfn-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrule-policy
            '''
            result = self._values.get("policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRulePolicyProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of the configured table association analysis rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrule.html#cfn-cleanrooms-configuredtableassociation-configuredtableassociationanalysisrule-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfiguredTableAssociationAnalysisRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTableMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_columns": "allowedColumns",
        "analysis_method": "analysisMethod",
        "analysis_rules": "analysisRules",
        "description": "description",
        "name": "name",
        "selected_analysis_methods": "selectedAnalysisMethods",
        "table_reference": "tableReference",
        "tags": "tags",
    },
)
class CfnConfiguredTableMixinProps:
    def __init__(
        self,
        *,
        allowed_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
        analysis_method: typing.Optional[builtins.str] = None,
        analysis_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfiguredTablePropsMixin.AnalysisRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        selected_analysis_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
        table_reference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfiguredTablePropsMixin.TableReferenceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnConfiguredTablePropsMixin.

        :param allowed_columns: The columns within the underlying AWS Glue table that can be used within collaborations.
        :param analysis_method: The analysis method for the configured table. ``DIRECT_QUERY`` allows SQL queries to be run directly on this table. ``DIRECT_JOB`` allows PySpark jobs to be run directly on this table. ``MULTIPLE`` allows both SQL queries and PySpark jobs to be run directly on this table.
        :param analysis_rules: The analysis rule that was created for the configured table.
        :param description: A description for the configured table.
        :param name: A name for the configured table.
        :param selected_analysis_methods: The selected analysis methods for the configured table.
        :param table_reference: The table that this configured table represents.
        :param tags: An optional label that you can assign to a resource when you create it. Each tag consists of a key and an optional value, both of which you define. When you use tagging, you can also use tag-based access control in IAM policies to control access to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-configuredtable.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
            
            cfn_configured_table_mixin_props = cleanrooms_mixins.CfnConfiguredTableMixinProps(
                allowed_columns=["allowedColumns"],
                analysis_method="analysisMethod",
                analysis_rules=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.AnalysisRuleProperty(
                    policy=cleanrooms_mixins.CfnConfiguredTablePropsMixin.ConfiguredTableAnalysisRulePolicyProperty(
                        v1=cleanrooms_mixins.CfnConfiguredTablePropsMixin.ConfiguredTableAnalysisRulePolicyV1Property(
                            aggregation=cleanrooms_mixins.CfnConfiguredTablePropsMixin.AnalysisRuleAggregationProperty(
                                additional_analyses="additionalAnalyses",
                                aggregate_columns=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.AggregateColumnProperty(
                                    column_names=["columnNames"],
                                    function="function"
                                )],
                                allowed_join_operators=["allowedJoinOperators"],
                                dimension_columns=["dimensionColumns"],
                                join_columns=["joinColumns"],
                                join_required="joinRequired",
                                output_constraints=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.AggregationConstraintProperty(
                                    column_name="columnName",
                                    minimum=123,
                                    type="type"
                                )],
                                scalar_functions=["scalarFunctions"]
                            ),
                            custom=cleanrooms_mixins.CfnConfiguredTablePropsMixin.AnalysisRuleCustomProperty(
                                additional_analyses="additionalAnalyses",
                                allowed_analyses=["allowedAnalyses"],
                                allowed_analysis_providers=["allowedAnalysisProviders"],
                                differential_privacy=cleanrooms_mixins.CfnConfiguredTablePropsMixin.DifferentialPrivacyProperty(
                                    columns=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.DifferentialPrivacyColumnProperty(
                                        name="name"
                                    )]
                                ),
                                disallowed_output_columns=["disallowedOutputColumns"]
                            ),
                            list=cleanrooms_mixins.CfnConfiguredTablePropsMixin.AnalysisRuleListProperty(
                                additional_analyses="additionalAnalyses",
                                allowed_join_operators=["allowedJoinOperators"],
                                join_columns=["joinColumns"],
                                list_columns=["listColumns"]
                            )
                        )
                    ),
                    type="type"
                )],
                description="description",
                name="name",
                selected_analysis_methods=["selectedAnalysisMethods"],
                table_reference=cleanrooms_mixins.CfnConfiguredTablePropsMixin.TableReferenceProperty(
                    athena=cleanrooms_mixins.CfnConfiguredTablePropsMixin.AthenaTableReferenceProperty(
                        database_name="databaseName",
                        output_location="outputLocation",
                        region="region",
                        table_name="tableName",
                        work_group="workGroup"
                    ),
                    glue=cleanrooms_mixins.CfnConfiguredTablePropsMixin.GlueTableReferenceProperty(
                        database_name="databaseName",
                        region="region",
                        table_name="tableName"
                    ),
                    snowflake=cleanrooms_mixins.CfnConfiguredTablePropsMixin.SnowflakeTableReferenceProperty(
                        account_identifier="accountIdentifier",
                        database_name="databaseName",
                        schema_name="schemaName",
                        secret_arn="secretArn",
                        table_name="tableName",
                        table_schema=cleanrooms_mixins.CfnConfiguredTablePropsMixin.SnowflakeTableSchemaProperty(
                            v1=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.SnowflakeTableSchemaV1Property(
                                column_name="columnName",
                                column_type="columnType"
                            )]
                        )
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1852f6b0d3833435831c19111ba32f71b4d109597ff72574828e2c9b4342baf1)
            check_type(argname="argument allowed_columns", value=allowed_columns, expected_type=type_hints["allowed_columns"])
            check_type(argname="argument analysis_method", value=analysis_method, expected_type=type_hints["analysis_method"])
            check_type(argname="argument analysis_rules", value=analysis_rules, expected_type=type_hints["analysis_rules"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument selected_analysis_methods", value=selected_analysis_methods, expected_type=type_hints["selected_analysis_methods"])
            check_type(argname="argument table_reference", value=table_reference, expected_type=type_hints["table_reference"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_columns is not None:
            self._values["allowed_columns"] = allowed_columns
        if analysis_method is not None:
            self._values["analysis_method"] = analysis_method
        if analysis_rules is not None:
            self._values["analysis_rules"] = analysis_rules
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if selected_analysis_methods is not None:
            self._values["selected_analysis_methods"] = selected_analysis_methods
        if table_reference is not None:
            self._values["table_reference"] = table_reference
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def allowed_columns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The columns within the underlying AWS Glue table that can be used within collaborations.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-configuredtable.html#cfn-cleanrooms-configuredtable-allowedcolumns
        '''
        result = self._values.get("allowed_columns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def analysis_method(self) -> typing.Optional[builtins.str]:
        '''The analysis method for the configured table.

        ``DIRECT_QUERY`` allows SQL queries to be run directly on this table.

        ``DIRECT_JOB`` allows PySpark jobs to be run directly on this table.

        ``MULTIPLE`` allows both SQL queries and PySpark jobs to be run directly on this table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-configuredtable.html#cfn-cleanrooms-configuredtable-analysismethod
        '''
        result = self._values.get("analysis_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def analysis_rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.AnalysisRuleProperty"]]]]:
        '''The analysis rule that was created for the configured table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-configuredtable.html#cfn-cleanrooms-configuredtable-analysisrules
        '''
        result = self._values.get("analysis_rules")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.AnalysisRuleProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the configured table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-configuredtable.html#cfn-cleanrooms-configuredtable-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the configured table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-configuredtable.html#cfn-cleanrooms-configuredtable-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def selected_analysis_methods(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The selected analysis methods for the configured table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-configuredtable.html#cfn-cleanrooms-configuredtable-selectedanalysismethods
        '''
        result = self._values.get("selected_analysis_methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def table_reference(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.TableReferenceProperty"]]:
        '''The table that this configured table represents.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-configuredtable.html#cfn-cleanrooms-configuredtable-tablereference
        '''
        result = self._values.get("table_reference")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.TableReferenceProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An optional label that you can assign to a resource when you create it.

        Each tag consists of a key and an optional value, both of which you define. When you use tagging, you can also use tag-based access control in IAM policies to control access to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-configuredtable.html#cfn-cleanrooms-configuredtable-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfiguredTableMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConfiguredTablePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTablePropsMixin",
):
    '''Creates a new configured table resource.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-configuredtable.html
    :cloudformationResource: AWS::CleanRooms::ConfiguredTable
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
        
        cfn_configured_table_props_mixin = cleanrooms_mixins.CfnConfiguredTablePropsMixin(cleanrooms_mixins.CfnConfiguredTableMixinProps(
            allowed_columns=["allowedColumns"],
            analysis_method="analysisMethod",
            analysis_rules=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.AnalysisRuleProperty(
                policy=cleanrooms_mixins.CfnConfiguredTablePropsMixin.ConfiguredTableAnalysisRulePolicyProperty(
                    v1=cleanrooms_mixins.CfnConfiguredTablePropsMixin.ConfiguredTableAnalysisRulePolicyV1Property(
                        aggregation=cleanrooms_mixins.CfnConfiguredTablePropsMixin.AnalysisRuleAggregationProperty(
                            additional_analyses="additionalAnalyses",
                            aggregate_columns=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.AggregateColumnProperty(
                                column_names=["columnNames"],
                                function="function"
                            )],
                            allowed_join_operators=["allowedJoinOperators"],
                            dimension_columns=["dimensionColumns"],
                            join_columns=["joinColumns"],
                            join_required="joinRequired",
                            output_constraints=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.AggregationConstraintProperty(
                                column_name="columnName",
                                minimum=123,
                                type="type"
                            )],
                            scalar_functions=["scalarFunctions"]
                        ),
                        custom=cleanrooms_mixins.CfnConfiguredTablePropsMixin.AnalysisRuleCustomProperty(
                            additional_analyses="additionalAnalyses",
                            allowed_analyses=["allowedAnalyses"],
                            allowed_analysis_providers=["allowedAnalysisProviders"],
                            differential_privacy=cleanrooms_mixins.CfnConfiguredTablePropsMixin.DifferentialPrivacyProperty(
                                columns=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.DifferentialPrivacyColumnProperty(
                                    name="name"
                                )]
                            ),
                            disallowed_output_columns=["disallowedOutputColumns"]
                        ),
                        list=cleanrooms_mixins.CfnConfiguredTablePropsMixin.AnalysisRuleListProperty(
                            additional_analyses="additionalAnalyses",
                            allowed_join_operators=["allowedJoinOperators"],
                            join_columns=["joinColumns"],
                            list_columns=["listColumns"]
                        )
                    )
                ),
                type="type"
            )],
            description="description",
            name="name",
            selected_analysis_methods=["selectedAnalysisMethods"],
            table_reference=cleanrooms_mixins.CfnConfiguredTablePropsMixin.TableReferenceProperty(
                athena=cleanrooms_mixins.CfnConfiguredTablePropsMixin.AthenaTableReferenceProperty(
                    database_name="databaseName",
                    output_location="outputLocation",
                    region="region",
                    table_name="tableName",
                    work_group="workGroup"
                ),
                glue=cleanrooms_mixins.CfnConfiguredTablePropsMixin.GlueTableReferenceProperty(
                    database_name="databaseName",
                    region="region",
                    table_name="tableName"
                ),
                snowflake=cleanrooms_mixins.CfnConfiguredTablePropsMixin.SnowflakeTableReferenceProperty(
                    account_identifier="accountIdentifier",
                    database_name="databaseName",
                    schema_name="schemaName",
                    secret_arn="secretArn",
                    table_name="tableName",
                    table_schema=cleanrooms_mixins.CfnConfiguredTablePropsMixin.SnowflakeTableSchemaProperty(
                        v1=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.SnowflakeTableSchemaV1Property(
                            column_name="columnName",
                            column_type="columnType"
                        )]
                    )
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
        props: typing.Union[CfnConfiguredTableMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CleanRooms::ConfiguredTable``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6de44d42968467aadb4969d3994a5e0e05c7ba2c8f1c1bac91908f19867be3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fde4af36e3edfb4f8c5e37b93892f5092496df1ceb585834abcc428c8fdaa382)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1920728949b82dbf0b1a56c6c6508d51fcda66c87fc059490f56663480a8ee9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConfiguredTableMixinProps:
        return typing.cast(CfnConfiguredTableMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTablePropsMixin.AggregateColumnProperty",
        jsii_struct_bases=[],
        name_mapping={"column_names": "columnNames", "function": "function"},
    )
    class AggregateColumnProperty:
        def __init__(
            self,
            *,
            column_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            function: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Column in configured table that can be used in aggregate function in query.

            :param column_names: Column names in configured table of aggregate columns.
            :param function: Aggregation function that can be applied to aggregate column in query.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-aggregatecolumn.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                aggregate_column_property = cleanrooms_mixins.CfnConfiguredTablePropsMixin.AggregateColumnProperty(
                    column_names=["columnNames"],
                    function="function"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__278c64695256fb7f06543f75af9bf3d528fe9973dbf414dbd34acfd1b80498e8)
                check_type(argname="argument column_names", value=column_names, expected_type=type_hints["column_names"])
                check_type(argname="argument function", value=function, expected_type=type_hints["function"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if column_names is not None:
                self._values["column_names"] = column_names
            if function is not None:
                self._values["function"] = function

        @builtins.property
        def column_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Column names in configured table of aggregate columns.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-aggregatecolumn.html#cfn-cleanrooms-configuredtable-aggregatecolumn-columnnames
            '''
            result = self._values.get("column_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def function(self) -> typing.Optional[builtins.str]:
            '''Aggregation function that can be applied to aggregate column in query.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-aggregatecolumn.html#cfn-cleanrooms-configuredtable-aggregatecolumn-function
            '''
            result = self._values.get("function")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AggregateColumnProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTablePropsMixin.AggregationConstraintProperty",
        jsii_struct_bases=[],
        name_mapping={
            "column_name": "columnName",
            "minimum": "minimum",
            "type": "type",
        },
    )
    class AggregationConstraintProperty:
        def __init__(
            self,
            *,
            column_name: typing.Optional[builtins.str] = None,
            minimum: typing.Optional[jsii.Number] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Constraint on query output removing output rows that do not meet a minimum number of distinct values of a specified column.

            :param column_name: Column in aggregation constraint for which there must be a minimum number of distinct values in an output row for it to be in the query output.
            :param minimum: The minimum number of distinct values that an output row must be an aggregation of. Minimum threshold of distinct values for a specified column that must exist in an output row for it to be in the query output.
            :param type: The type of aggregation the constraint allows. The only valid value is currently ``COUNT_DISTINCT``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-aggregationconstraint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                aggregation_constraint_property = cleanrooms_mixins.CfnConfiguredTablePropsMixin.AggregationConstraintProperty(
                    column_name="columnName",
                    minimum=123,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c2d2d9f5702176472d6e972b32efebdf4c1c03dfe4badd0a51b780e8e17c915a)
                check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
                check_type(argname="argument minimum", value=minimum, expected_type=type_hints["minimum"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if column_name is not None:
                self._values["column_name"] = column_name
            if minimum is not None:
                self._values["minimum"] = minimum
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def column_name(self) -> typing.Optional[builtins.str]:
            '''Column in aggregation constraint for which there must be a minimum number of distinct values in an output row for it to be in the query output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-aggregationconstraint.html#cfn-cleanrooms-configuredtable-aggregationconstraint-columnname
            '''
            result = self._values.get("column_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def minimum(self) -> typing.Optional[jsii.Number]:
            '''The minimum number of distinct values that an output row must be an aggregation of.

            Minimum threshold of distinct values for a specified column that must exist in an output row for it to be in the query output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-aggregationconstraint.html#cfn-cleanrooms-configuredtable-aggregationconstraint-minimum
            '''
            result = self._values.get("minimum")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of aggregation the constraint allows.

            The only valid value is currently ``COUNT_DISTINCT``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-aggregationconstraint.html#cfn-cleanrooms-configuredtable-aggregationconstraint-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AggregationConstraintProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTablePropsMixin.AnalysisRuleAggregationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "additional_analyses": "additionalAnalyses",
            "aggregate_columns": "aggregateColumns",
            "allowed_join_operators": "allowedJoinOperators",
            "dimension_columns": "dimensionColumns",
            "join_columns": "joinColumns",
            "join_required": "joinRequired",
            "output_constraints": "outputConstraints",
            "scalar_functions": "scalarFunctions",
        },
    )
    class AnalysisRuleAggregationProperty:
        def __init__(
            self,
            *,
            additional_analyses: typing.Optional[builtins.str] = None,
            aggregate_columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfiguredTablePropsMixin.AggregateColumnProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            allowed_join_operators: typing.Optional[typing.Sequence[builtins.str]] = None,
            dimension_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
            join_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
            join_required: typing.Optional[builtins.str] = None,
            output_constraints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfiguredTablePropsMixin.AggregationConstraintProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            scalar_functions: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A type of analysis rule that enables query structure and specified queries that produce aggregate statistics.

            :param additional_analyses: An indicator as to whether additional analyses (such as AWS Clean Rooms ML) can be applied to the output of the direct query. The ``additionalAnalyses`` parameter is currently supported for the list analysis rule ( ``AnalysisRuleList`` ) and the custom analysis rule ( ``AnalysisRuleCustom`` ).
            :param aggregate_columns: The columns that query runners are allowed to use in aggregation queries.
            :param allowed_join_operators: Which logical operators (if any) are to be used in an INNER JOIN match condition. Default is ``AND`` .
            :param dimension_columns: The columns that query runners are allowed to select, group by, or filter by.
            :param join_columns: Columns in configured table that can be used in join statements and/or as aggregate columns. They can never be outputted directly.
            :param join_required: Control that requires member who runs query to do a join with their configured table and/or other configured table in query.
            :param output_constraints: Columns that must meet a specific threshold value (after an aggregation function is applied to it) for each output row to be returned.
            :param scalar_functions: Set of scalar functions that are allowed to be used on dimension columns and the output of aggregation of metrics.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-analysisruleaggregation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                analysis_rule_aggregation_property = cleanrooms_mixins.CfnConfiguredTablePropsMixin.AnalysisRuleAggregationProperty(
                    additional_analyses="additionalAnalyses",
                    aggregate_columns=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.AggregateColumnProperty(
                        column_names=["columnNames"],
                        function="function"
                    )],
                    allowed_join_operators=["allowedJoinOperators"],
                    dimension_columns=["dimensionColumns"],
                    join_columns=["joinColumns"],
                    join_required="joinRequired",
                    output_constraints=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.AggregationConstraintProperty(
                        column_name="columnName",
                        minimum=123,
                        type="type"
                    )],
                    scalar_functions=["scalarFunctions"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b0d7112177d08bb8826720095d9066eb4b79351003477fa10037ace0903e21db)
                check_type(argname="argument additional_analyses", value=additional_analyses, expected_type=type_hints["additional_analyses"])
                check_type(argname="argument aggregate_columns", value=aggregate_columns, expected_type=type_hints["aggregate_columns"])
                check_type(argname="argument allowed_join_operators", value=allowed_join_operators, expected_type=type_hints["allowed_join_operators"])
                check_type(argname="argument dimension_columns", value=dimension_columns, expected_type=type_hints["dimension_columns"])
                check_type(argname="argument join_columns", value=join_columns, expected_type=type_hints["join_columns"])
                check_type(argname="argument join_required", value=join_required, expected_type=type_hints["join_required"])
                check_type(argname="argument output_constraints", value=output_constraints, expected_type=type_hints["output_constraints"])
                check_type(argname="argument scalar_functions", value=scalar_functions, expected_type=type_hints["scalar_functions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if additional_analyses is not None:
                self._values["additional_analyses"] = additional_analyses
            if aggregate_columns is not None:
                self._values["aggregate_columns"] = aggregate_columns
            if allowed_join_operators is not None:
                self._values["allowed_join_operators"] = allowed_join_operators
            if dimension_columns is not None:
                self._values["dimension_columns"] = dimension_columns
            if join_columns is not None:
                self._values["join_columns"] = join_columns
            if join_required is not None:
                self._values["join_required"] = join_required
            if output_constraints is not None:
                self._values["output_constraints"] = output_constraints
            if scalar_functions is not None:
                self._values["scalar_functions"] = scalar_functions

        @builtins.property
        def additional_analyses(self) -> typing.Optional[builtins.str]:
            '''An indicator as to whether additional analyses (such as AWS Clean Rooms ML) can be applied to the output of the direct query.

            The ``additionalAnalyses`` parameter is currently supported for the list analysis rule ( ``AnalysisRuleList`` ) and the custom analysis rule ( ``AnalysisRuleCustom`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-analysisruleaggregation.html#cfn-cleanrooms-configuredtable-analysisruleaggregation-additionalanalyses
            '''
            result = self._values.get("additional_analyses")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def aggregate_columns(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.AggregateColumnProperty"]]]]:
            '''The columns that query runners are allowed to use in aggregation queries.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-analysisruleaggregation.html#cfn-cleanrooms-configuredtable-analysisruleaggregation-aggregatecolumns
            '''
            result = self._values.get("aggregate_columns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.AggregateColumnProperty"]]]], result)

        @builtins.property
        def allowed_join_operators(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Which logical operators (if any) are to be used in an INNER JOIN match condition.

            Default is ``AND`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-analysisruleaggregation.html#cfn-cleanrooms-configuredtable-analysisruleaggregation-allowedjoinoperators
            '''
            result = self._values.get("allowed_join_operators")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def dimension_columns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The columns that query runners are allowed to select, group by, or filter by.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-analysisruleaggregation.html#cfn-cleanrooms-configuredtable-analysisruleaggregation-dimensioncolumns
            '''
            result = self._values.get("dimension_columns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def join_columns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Columns in configured table that can be used in join statements and/or as aggregate columns.

            They can never be outputted directly.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-analysisruleaggregation.html#cfn-cleanrooms-configuredtable-analysisruleaggregation-joincolumns
            '''
            result = self._values.get("join_columns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def join_required(self) -> typing.Optional[builtins.str]:
            '''Control that requires member who runs query to do a join with their configured table and/or other configured table in query.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-analysisruleaggregation.html#cfn-cleanrooms-configuredtable-analysisruleaggregation-joinrequired
            '''
            result = self._values.get("join_required")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def output_constraints(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.AggregationConstraintProperty"]]]]:
            '''Columns that must meet a specific threshold value (after an aggregation function is applied to it) for each output row to be returned.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-analysisruleaggregation.html#cfn-cleanrooms-configuredtable-analysisruleaggregation-outputconstraints
            '''
            result = self._values.get("output_constraints")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.AggregationConstraintProperty"]]]], result)

        @builtins.property
        def scalar_functions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Set of scalar functions that are allowed to be used on dimension columns and the output of aggregation of metrics.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-analysisruleaggregation.html#cfn-cleanrooms-configuredtable-analysisruleaggregation-scalarfunctions
            '''
            result = self._values.get("scalar_functions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnalysisRuleAggregationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTablePropsMixin.AnalysisRuleCustomProperty",
        jsii_struct_bases=[],
        name_mapping={
            "additional_analyses": "additionalAnalyses",
            "allowed_analyses": "allowedAnalyses",
            "allowed_analysis_providers": "allowedAnalysisProviders",
            "differential_privacy": "differentialPrivacy",
            "disallowed_output_columns": "disallowedOutputColumns",
        },
    )
    class AnalysisRuleCustomProperty:
        def __init__(
            self,
            *,
            additional_analyses: typing.Optional[builtins.str] = None,
            allowed_analyses: typing.Optional[typing.Sequence[builtins.str]] = None,
            allowed_analysis_providers: typing.Optional[typing.Sequence[builtins.str]] = None,
            differential_privacy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfiguredTablePropsMixin.DifferentialPrivacyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            disallowed_output_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A type of analysis rule that enables the table owner to approve custom SQL queries on their configured tables.

            It supports differential privacy.

            :param additional_analyses: An indicator as to whether additional analyses (such as AWS Clean Rooms ML) can be applied to the output of the direct query.
            :param allowed_analyses: The ARN of the analysis templates that are allowed by the custom analysis rule.
            :param allowed_analysis_providers: The IDs of the AWS accounts that are allowed to query by the custom analysis rule. Required when ``allowedAnalyses`` is ``ANY_QUERY`` .
            :param differential_privacy: The differential privacy configuration.
            :param disallowed_output_columns: A list of columns that aren't allowed to be shown in the query output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-analysisrulecustom.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                analysis_rule_custom_property = cleanrooms_mixins.CfnConfiguredTablePropsMixin.AnalysisRuleCustomProperty(
                    additional_analyses="additionalAnalyses",
                    allowed_analyses=["allowedAnalyses"],
                    allowed_analysis_providers=["allowedAnalysisProviders"],
                    differential_privacy=cleanrooms_mixins.CfnConfiguredTablePropsMixin.DifferentialPrivacyProperty(
                        columns=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.DifferentialPrivacyColumnProperty(
                            name="name"
                        )]
                    ),
                    disallowed_output_columns=["disallowedOutputColumns"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b71c56f2d626d2bf969f73e8cb4d748d8a4dc29bcfe21d1a6750135f31e283fe)
                check_type(argname="argument additional_analyses", value=additional_analyses, expected_type=type_hints["additional_analyses"])
                check_type(argname="argument allowed_analyses", value=allowed_analyses, expected_type=type_hints["allowed_analyses"])
                check_type(argname="argument allowed_analysis_providers", value=allowed_analysis_providers, expected_type=type_hints["allowed_analysis_providers"])
                check_type(argname="argument differential_privacy", value=differential_privacy, expected_type=type_hints["differential_privacy"])
                check_type(argname="argument disallowed_output_columns", value=disallowed_output_columns, expected_type=type_hints["disallowed_output_columns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if additional_analyses is not None:
                self._values["additional_analyses"] = additional_analyses
            if allowed_analyses is not None:
                self._values["allowed_analyses"] = allowed_analyses
            if allowed_analysis_providers is not None:
                self._values["allowed_analysis_providers"] = allowed_analysis_providers
            if differential_privacy is not None:
                self._values["differential_privacy"] = differential_privacy
            if disallowed_output_columns is not None:
                self._values["disallowed_output_columns"] = disallowed_output_columns

        @builtins.property
        def additional_analyses(self) -> typing.Optional[builtins.str]:
            '''An indicator as to whether additional analyses (such as AWS Clean Rooms ML) can be applied to the output of the direct query.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-analysisrulecustom.html#cfn-cleanrooms-configuredtable-analysisrulecustom-additionalanalyses
            '''
            result = self._values.get("additional_analyses")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def allowed_analyses(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The ARN of the analysis templates that are allowed by the custom analysis rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-analysisrulecustom.html#cfn-cleanrooms-configuredtable-analysisrulecustom-allowedanalyses
            '''
            result = self._values.get("allowed_analyses")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allowed_analysis_providers(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The IDs of the AWS accounts that are allowed to query by the custom analysis rule.

            Required when ``allowedAnalyses`` is ``ANY_QUERY`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-analysisrulecustom.html#cfn-cleanrooms-configuredtable-analysisrulecustom-allowedanalysisproviders
            '''
            result = self._values.get("allowed_analysis_providers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def differential_privacy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.DifferentialPrivacyProperty"]]:
            '''The differential privacy configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-analysisrulecustom.html#cfn-cleanrooms-configuredtable-analysisrulecustom-differentialprivacy
            '''
            result = self._values.get("differential_privacy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.DifferentialPrivacyProperty"]], result)

        @builtins.property
        def disallowed_output_columns(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of columns that aren't allowed to be shown in the query output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-analysisrulecustom.html#cfn-cleanrooms-configuredtable-analysisrulecustom-disallowedoutputcolumns
            '''
            result = self._values.get("disallowed_output_columns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnalysisRuleCustomProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTablePropsMixin.AnalysisRuleListProperty",
        jsii_struct_bases=[],
        name_mapping={
            "additional_analyses": "additionalAnalyses",
            "allowed_join_operators": "allowedJoinOperators",
            "join_columns": "joinColumns",
            "list_columns": "listColumns",
        },
    )
    class AnalysisRuleListProperty:
        def __init__(
            self,
            *,
            additional_analyses: typing.Optional[builtins.str] = None,
            allowed_join_operators: typing.Optional[typing.Sequence[builtins.str]] = None,
            join_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
            list_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A type of analysis rule that enables row-level analysis.

            :param additional_analyses: An indicator as to whether additional analyses (such as AWS Clean Rooms ML) can be applied to the output of the direct query.
            :param allowed_join_operators: The logical operators (if any) that are to be used in an INNER JOIN match condition. Default is ``AND`` .
            :param join_columns: Columns that can be used to join a configured table with the table of the member who can query and other members' configured tables.
            :param list_columns: Columns that can be listed in the output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-analysisrulelist.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                analysis_rule_list_property = cleanrooms_mixins.CfnConfiguredTablePropsMixin.AnalysisRuleListProperty(
                    additional_analyses="additionalAnalyses",
                    allowed_join_operators=["allowedJoinOperators"],
                    join_columns=["joinColumns"],
                    list_columns=["listColumns"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8d224e637db14b34ba8303ca94ac159e9a80e200266c60ad06960eaa0ff46764)
                check_type(argname="argument additional_analyses", value=additional_analyses, expected_type=type_hints["additional_analyses"])
                check_type(argname="argument allowed_join_operators", value=allowed_join_operators, expected_type=type_hints["allowed_join_operators"])
                check_type(argname="argument join_columns", value=join_columns, expected_type=type_hints["join_columns"])
                check_type(argname="argument list_columns", value=list_columns, expected_type=type_hints["list_columns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if additional_analyses is not None:
                self._values["additional_analyses"] = additional_analyses
            if allowed_join_operators is not None:
                self._values["allowed_join_operators"] = allowed_join_operators
            if join_columns is not None:
                self._values["join_columns"] = join_columns
            if list_columns is not None:
                self._values["list_columns"] = list_columns

        @builtins.property
        def additional_analyses(self) -> typing.Optional[builtins.str]:
            '''An indicator as to whether additional analyses (such as AWS Clean Rooms ML) can be applied to the output of the direct query.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-analysisrulelist.html#cfn-cleanrooms-configuredtable-analysisrulelist-additionalanalyses
            '''
            result = self._values.get("additional_analyses")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def allowed_join_operators(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The logical operators (if any) that are to be used in an INNER JOIN match condition.

            Default is ``AND`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-analysisrulelist.html#cfn-cleanrooms-configuredtable-analysisrulelist-allowedjoinoperators
            '''
            result = self._values.get("allowed_join_operators")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def join_columns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Columns that can be used to join a configured table with the table of the member who can query and other members' configured tables.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-analysisrulelist.html#cfn-cleanrooms-configuredtable-analysisrulelist-joincolumns
            '''
            result = self._values.get("join_columns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def list_columns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Columns that can be listed in the output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-analysisrulelist.html#cfn-cleanrooms-configuredtable-analysisrulelist-listcolumns
            '''
            result = self._values.get("list_columns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnalysisRuleListProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTablePropsMixin.AnalysisRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"policy": "policy", "type": "type"},
    )
    class AnalysisRuleProperty:
        def __init__(
            self,
            *,
            policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfiguredTablePropsMixin.ConfiguredTableAnalysisRulePolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A specification about how data from the configured table can be used in a query.

            :param policy: A policy that describes the associated data usage limitations.
            :param type: The type of analysis rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-analysisrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                analysis_rule_property = cleanrooms_mixins.CfnConfiguredTablePropsMixin.AnalysisRuleProperty(
                    policy=cleanrooms_mixins.CfnConfiguredTablePropsMixin.ConfiguredTableAnalysisRulePolicyProperty(
                        v1=cleanrooms_mixins.CfnConfiguredTablePropsMixin.ConfiguredTableAnalysisRulePolicyV1Property(
                            aggregation=cleanrooms_mixins.CfnConfiguredTablePropsMixin.AnalysisRuleAggregationProperty(
                                additional_analyses="additionalAnalyses",
                                aggregate_columns=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.AggregateColumnProperty(
                                    column_names=["columnNames"],
                                    function="function"
                                )],
                                allowed_join_operators=["allowedJoinOperators"],
                                dimension_columns=["dimensionColumns"],
                                join_columns=["joinColumns"],
                                join_required="joinRequired",
                                output_constraints=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.AggregationConstraintProperty(
                                    column_name="columnName",
                                    minimum=123,
                                    type="type"
                                )],
                                scalar_functions=["scalarFunctions"]
                            ),
                            custom=cleanrooms_mixins.CfnConfiguredTablePropsMixin.AnalysisRuleCustomProperty(
                                additional_analyses="additionalAnalyses",
                                allowed_analyses=["allowedAnalyses"],
                                allowed_analysis_providers=["allowedAnalysisProviders"],
                                differential_privacy=cleanrooms_mixins.CfnConfiguredTablePropsMixin.DifferentialPrivacyProperty(
                                    columns=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.DifferentialPrivacyColumnProperty(
                                        name="name"
                                    )]
                                ),
                                disallowed_output_columns=["disallowedOutputColumns"]
                            ),
                            list=cleanrooms_mixins.CfnConfiguredTablePropsMixin.AnalysisRuleListProperty(
                                additional_analyses="additionalAnalyses",
                                allowed_join_operators=["allowedJoinOperators"],
                                join_columns=["joinColumns"],
                                list_columns=["listColumns"]
                            )
                        )
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__89c3b7be1a3c07bf5c4d7fbc882acb1f2c1b43641d175b7f3df1a85433b491b4)
                check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if policy is not None:
                self._values["policy"] = policy
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.ConfiguredTableAnalysisRulePolicyProperty"]]:
            '''A policy that describes the associated data usage limitations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-analysisrule.html#cfn-cleanrooms-configuredtable-analysisrule-policy
            '''
            result = self._values.get("policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.ConfiguredTableAnalysisRulePolicyProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of analysis rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-analysisrule.html#cfn-cleanrooms-configuredtable-analysisrule-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnalysisRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTablePropsMixin.AthenaTableReferenceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "database_name": "databaseName",
            "output_location": "outputLocation",
            "region": "region",
            "table_name": "tableName",
            "work_group": "workGroup",
        },
    )
    class AthenaTableReferenceProperty:
        def __init__(
            self,
            *,
            database_name: typing.Optional[builtins.str] = None,
            output_location: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
            table_name: typing.Optional[builtins.str] = None,
            work_group: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A reference to a table within Athena.

            :param database_name: The database name.
            :param output_location: The output location for the Athena table.
            :param region: The AWS Region where the Athena table is located. This parameter is required to uniquely identify and access tables across different Regions.
            :param table_name: The table reference.
            :param work_group: The workgroup of the Athena table reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-athenatablereference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                athena_table_reference_property = cleanrooms_mixins.CfnConfiguredTablePropsMixin.AthenaTableReferenceProperty(
                    database_name="databaseName",
                    output_location="outputLocation",
                    region="region",
                    table_name="tableName",
                    work_group="workGroup"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__896fcebd74ad584f30058e82d3ddf6ce82d554756d69a7aa17397f27dd8aa499)
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument output_location", value=output_location, expected_type=type_hints["output_location"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
                check_type(argname="argument work_group", value=work_group, expected_type=type_hints["work_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if database_name is not None:
                self._values["database_name"] = database_name
            if output_location is not None:
                self._values["output_location"] = output_location
            if region is not None:
                self._values["region"] = region
            if table_name is not None:
                self._values["table_name"] = table_name
            if work_group is not None:
                self._values["work_group"] = work_group

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The database name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-athenatablereference.html#cfn-cleanrooms-configuredtable-athenatablereference-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def output_location(self) -> typing.Optional[builtins.str]:
            '''The output location for the Athena table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-athenatablereference.html#cfn-cleanrooms-configuredtable-athenatablereference-outputlocation
            '''
            result = self._values.get("output_location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region where the Athena table is located.

            This parameter is required to uniquely identify and access tables across different Regions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-athenatablereference.html#cfn-cleanrooms-configuredtable-athenatablereference-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''The table reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-athenatablereference.html#cfn-cleanrooms-configuredtable-athenatablereference-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def work_group(self) -> typing.Optional[builtins.str]:
            '''The workgroup of the Athena table reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-athenatablereference.html#cfn-cleanrooms-configuredtable-athenatablereference-workgroup
            '''
            result = self._values.get("work_group")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AthenaTableReferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTablePropsMixin.ConfiguredTableAnalysisRulePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"v1": "v1"},
    )
    class ConfiguredTableAnalysisRulePolicyProperty:
        def __init__(
            self,
            *,
            v1: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfiguredTablePropsMixin.ConfiguredTableAnalysisRulePolicyV1Property", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Controls on the query specifications that can be run on a configured table.

            :param v1: Controls on the query specifications that can be run on a configured table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-configuredtableanalysisrulepolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                configured_table_analysis_rule_policy_property = cleanrooms_mixins.CfnConfiguredTablePropsMixin.ConfiguredTableAnalysisRulePolicyProperty(
                    v1=cleanrooms_mixins.CfnConfiguredTablePropsMixin.ConfiguredTableAnalysisRulePolicyV1Property(
                        aggregation=cleanrooms_mixins.CfnConfiguredTablePropsMixin.AnalysisRuleAggregationProperty(
                            additional_analyses="additionalAnalyses",
                            aggregate_columns=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.AggregateColumnProperty(
                                column_names=["columnNames"],
                                function="function"
                            )],
                            allowed_join_operators=["allowedJoinOperators"],
                            dimension_columns=["dimensionColumns"],
                            join_columns=["joinColumns"],
                            join_required="joinRequired",
                            output_constraints=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.AggregationConstraintProperty(
                                column_name="columnName",
                                minimum=123,
                                type="type"
                            )],
                            scalar_functions=["scalarFunctions"]
                        ),
                        custom=cleanrooms_mixins.CfnConfiguredTablePropsMixin.AnalysisRuleCustomProperty(
                            additional_analyses="additionalAnalyses",
                            allowed_analyses=["allowedAnalyses"],
                            allowed_analysis_providers=["allowedAnalysisProviders"],
                            differential_privacy=cleanrooms_mixins.CfnConfiguredTablePropsMixin.DifferentialPrivacyProperty(
                                columns=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.DifferentialPrivacyColumnProperty(
                                    name="name"
                                )]
                            ),
                            disallowed_output_columns=["disallowedOutputColumns"]
                        ),
                        list=cleanrooms_mixins.CfnConfiguredTablePropsMixin.AnalysisRuleListProperty(
                            additional_analyses="additionalAnalyses",
                            allowed_join_operators=["allowedJoinOperators"],
                            join_columns=["joinColumns"],
                            list_columns=["listColumns"]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6f5c05a8fa8165c3e794f2ef3873601e263f55c85373277e517eec03296466ec)
                check_type(argname="argument v1", value=v1, expected_type=type_hints["v1"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if v1 is not None:
                self._values["v1"] = v1

        @builtins.property
        def v1(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.ConfiguredTableAnalysisRulePolicyV1Property"]]:
            '''Controls on the query specifications that can be run on a configured table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-configuredtableanalysisrulepolicy.html#cfn-cleanrooms-configuredtable-configuredtableanalysisrulepolicy-v1
            '''
            result = self._values.get("v1")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.ConfiguredTableAnalysisRulePolicyV1Property"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfiguredTableAnalysisRulePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTablePropsMixin.ConfiguredTableAnalysisRulePolicyV1Property",
        jsii_struct_bases=[],
        name_mapping={
            "aggregation": "aggregation",
            "custom": "custom",
            "list": "list",
        },
    )
    class ConfiguredTableAnalysisRulePolicyV1Property:
        def __init__(
            self,
            *,
            aggregation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfiguredTablePropsMixin.AnalysisRuleAggregationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            custom: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfiguredTablePropsMixin.AnalysisRuleCustomProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfiguredTablePropsMixin.AnalysisRuleListProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Controls on the query specifications that can be run on a configured table.

            :param aggregation: Analysis rule type that enables only aggregation queries on a configured table.
            :param custom: Analysis rule type that enables custom SQL queries on a configured table.
            :param list: Analysis rule type that enables only list queries on a configured table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-configuredtableanalysisrulepolicyv1.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                configured_table_analysis_rule_policy_v1_property = cleanrooms_mixins.CfnConfiguredTablePropsMixin.ConfiguredTableAnalysisRulePolicyV1Property(
                    aggregation=cleanrooms_mixins.CfnConfiguredTablePropsMixin.AnalysisRuleAggregationProperty(
                        additional_analyses="additionalAnalyses",
                        aggregate_columns=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.AggregateColumnProperty(
                            column_names=["columnNames"],
                            function="function"
                        )],
                        allowed_join_operators=["allowedJoinOperators"],
                        dimension_columns=["dimensionColumns"],
                        join_columns=["joinColumns"],
                        join_required="joinRequired",
                        output_constraints=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.AggregationConstraintProperty(
                            column_name="columnName",
                            minimum=123,
                            type="type"
                        )],
                        scalar_functions=["scalarFunctions"]
                    ),
                    custom=cleanrooms_mixins.CfnConfiguredTablePropsMixin.AnalysisRuleCustomProperty(
                        additional_analyses="additionalAnalyses",
                        allowed_analyses=["allowedAnalyses"],
                        allowed_analysis_providers=["allowedAnalysisProviders"],
                        differential_privacy=cleanrooms_mixins.CfnConfiguredTablePropsMixin.DifferentialPrivacyProperty(
                            columns=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.DifferentialPrivacyColumnProperty(
                                name="name"
                            )]
                        ),
                        disallowed_output_columns=["disallowedOutputColumns"]
                    ),
                    list=cleanrooms_mixins.CfnConfiguredTablePropsMixin.AnalysisRuleListProperty(
                        additional_analyses="additionalAnalyses",
                        allowed_join_operators=["allowedJoinOperators"],
                        join_columns=["joinColumns"],
                        list_columns=["listColumns"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a0184d092bc50b96521b708080e7023006564d3dccdc09de995d5d0d792d7f1)
                check_type(argname="argument aggregation", value=aggregation, expected_type=type_hints["aggregation"])
                check_type(argname="argument custom", value=custom, expected_type=type_hints["custom"])
                check_type(argname="argument list", value=list, expected_type=type_hints["list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aggregation is not None:
                self._values["aggregation"] = aggregation
            if custom is not None:
                self._values["custom"] = custom
            if list is not None:
                self._values["list"] = list

        @builtins.property
        def aggregation(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.AnalysisRuleAggregationProperty"]]:
            '''Analysis rule type that enables only aggregation queries on a configured table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-configuredtableanalysisrulepolicyv1.html#cfn-cleanrooms-configuredtable-configuredtableanalysisrulepolicyv1-aggregation
            '''
            result = self._values.get("aggregation")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.AnalysisRuleAggregationProperty"]], result)

        @builtins.property
        def custom(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.AnalysisRuleCustomProperty"]]:
            '''Analysis rule type that enables custom SQL queries on a configured table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-configuredtableanalysisrulepolicyv1.html#cfn-cleanrooms-configuredtable-configuredtableanalysisrulepolicyv1-custom
            '''
            result = self._values.get("custom")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.AnalysisRuleCustomProperty"]], result)

        @builtins.property
        def list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.AnalysisRuleListProperty"]]:
            '''Analysis rule type that enables only list queries on a configured table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-configuredtableanalysisrulepolicyv1.html#cfn-cleanrooms-configuredtable-configuredtableanalysisrulepolicyv1-list
            '''
            result = self._values.get("list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.AnalysisRuleListProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfiguredTableAnalysisRulePolicyV1Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTablePropsMixin.DifferentialPrivacyColumnProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class DifferentialPrivacyColumnProperty:
        def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
            '''Specifies the name of the column that contains the unique identifier of your users, whose privacy you want to protect.

            :param name: The name of the column, such as user_id, that contains the unique identifier of your users, whose privacy you want to protect. If you want to turn on differential privacy for two or more tables in a collaboration, you must configure the same column as the user identifier column in both analysis rules.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-differentialprivacycolumn.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                differential_privacy_column_property = cleanrooms_mixins.CfnConfiguredTablePropsMixin.DifferentialPrivacyColumnProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__019cce3c28d9f2269527fc30aadf7e92f2fec0f2677682b0de125f77e33fcac0)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the column, such as user_id, that contains the unique identifier of your users, whose privacy you want to protect.

            If you want to turn on differential privacy for two or more tables in a collaboration, you must configure the same column as the user identifier column in both analysis rules.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-differentialprivacycolumn.html#cfn-cleanrooms-configuredtable-differentialprivacycolumn-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DifferentialPrivacyColumnProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTablePropsMixin.DifferentialPrivacyProperty",
        jsii_struct_bases=[],
        name_mapping={"columns": "columns"},
    )
    class DifferentialPrivacyProperty:
        def __init__(
            self,
            *,
            columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfiguredTablePropsMixin.DifferentialPrivacyColumnProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The analysis method allowed for the configured tables.

            ``DIRECT_QUERY`` allows SQL queries to be run directly on this table.

            ``DIRECT_JOB`` allows PySpark jobs to be run directly on this table.

            ``MULTIPLE`` allows both SQL queries and PySpark jobs to be run directly on this table.

            :param columns: The name of the column, such as user_id, that contains the unique identifier of your users, whose privacy you want to protect. If you want to turn on differential privacy for two or more tables in a collaboration, you must configure the same column as the user identifier column in both analysis rules.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-differentialprivacy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                differential_privacy_property = cleanrooms_mixins.CfnConfiguredTablePropsMixin.DifferentialPrivacyProperty(
                    columns=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.DifferentialPrivacyColumnProperty(
                        name="name"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2838adb2288d10de8d24f5126c20a534ee3cef6796e1f4093fb2f017e319f5aa)
                check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if columns is not None:
                self._values["columns"] = columns

        @builtins.property
        def columns(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.DifferentialPrivacyColumnProperty"]]]]:
            '''The name of the column, such as user_id, that contains the unique identifier of your users, whose privacy you want to protect.

            If you want to turn on differential privacy for two or more tables in a collaboration, you must configure the same column as the user identifier column in both analysis rules.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-differentialprivacy.html#cfn-cleanrooms-configuredtable-differentialprivacy-columns
            '''
            result = self._values.get("columns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.DifferentialPrivacyColumnProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DifferentialPrivacyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTablePropsMixin.GlueTableReferenceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "database_name": "databaseName",
            "region": "region",
            "table_name": "tableName",
        },
    )
    class GlueTableReferenceProperty:
        def __init__(
            self,
            *,
            database_name: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
            table_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A reference to a table within an AWS Glue data catalog.

            :param database_name: The name of the database the AWS Glue table belongs to.
            :param region: The AWS Region where the AWS Glue table is located. This parameter is required to uniquely identify and access tables across different Regions.
            :param table_name: The name of the AWS Glue table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-gluetablereference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                glue_table_reference_property = cleanrooms_mixins.CfnConfiguredTablePropsMixin.GlueTableReferenceProperty(
                    database_name="databaseName",
                    region="region",
                    table_name="tableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__33d78bb77dcca7a4b0105a2a76e1ea6b732d13c90ede52b2702edbb6a8d56a98)
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if database_name is not None:
                self._values["database_name"] = database_name
            if region is not None:
                self._values["region"] = region
            if table_name is not None:
                self._values["table_name"] = table_name

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The name of the database the AWS Glue table belongs to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-gluetablereference.html#cfn-cleanrooms-configuredtable-gluetablereference-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region where the AWS Glue table is located.

            This parameter is required to uniquely identify and access tables across different Regions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-gluetablereference.html#cfn-cleanrooms-configuredtable-gluetablereference-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''The name of the AWS Glue table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-gluetablereference.html#cfn-cleanrooms-configuredtable-gluetablereference-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GlueTableReferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTablePropsMixin.SnowflakeTableReferenceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_identifier": "accountIdentifier",
            "database_name": "databaseName",
            "schema_name": "schemaName",
            "secret_arn": "secretArn",
            "table_name": "tableName",
            "table_schema": "tableSchema",
        },
    )
    class SnowflakeTableReferenceProperty:
        def __init__(
            self,
            *,
            account_identifier: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            schema_name: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
            table_name: typing.Optional[builtins.str] = None,
            table_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfiguredTablePropsMixin.SnowflakeTableSchemaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A reference to a table within Snowflake.

            :param account_identifier: The account identifier for the Snowflake table reference.
            :param database_name: The name of the database the Snowflake table belongs to.
            :param schema_name: The schema name of the Snowflake table reference.
            :param secret_arn: The secret ARN of the Snowflake table reference.
            :param table_name: The name of the Snowflake table.
            :param table_schema: The schema of the Snowflake table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-snowflaketablereference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                snowflake_table_reference_property = cleanrooms_mixins.CfnConfiguredTablePropsMixin.SnowflakeTableReferenceProperty(
                    account_identifier="accountIdentifier",
                    database_name="databaseName",
                    schema_name="schemaName",
                    secret_arn="secretArn",
                    table_name="tableName",
                    table_schema=cleanrooms_mixins.CfnConfiguredTablePropsMixin.SnowflakeTableSchemaProperty(
                        v1=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.SnowflakeTableSchemaV1Property(
                            column_name="columnName",
                            column_type="columnType"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__58570f2da1b2fbd69f9fb10882b62d580cc17739149e24aaf65c119b285ee4de)
                check_type(argname="argument account_identifier", value=account_identifier, expected_type=type_hints["account_identifier"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument schema_name", value=schema_name, expected_type=type_hints["schema_name"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
                check_type(argname="argument table_schema", value=table_schema, expected_type=type_hints["table_schema"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_identifier is not None:
                self._values["account_identifier"] = account_identifier
            if database_name is not None:
                self._values["database_name"] = database_name
            if schema_name is not None:
                self._values["schema_name"] = schema_name
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn
            if table_name is not None:
                self._values["table_name"] = table_name
            if table_schema is not None:
                self._values["table_schema"] = table_schema

        @builtins.property
        def account_identifier(self) -> typing.Optional[builtins.str]:
            '''The account identifier for the Snowflake table reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-snowflaketablereference.html#cfn-cleanrooms-configuredtable-snowflaketablereference-accountidentifier
            '''
            result = self._values.get("account_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The name of the database the Snowflake table belongs to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-snowflaketablereference.html#cfn-cleanrooms-configuredtable-snowflaketablereference-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schema_name(self) -> typing.Optional[builtins.str]:
            '''The schema name of the Snowflake table reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-snowflaketablereference.html#cfn-cleanrooms-configuredtable-snowflaketablereference-schemaname
            '''
            result = self._values.get("schema_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The secret ARN of the Snowflake table reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-snowflaketablereference.html#cfn-cleanrooms-configuredtable-snowflaketablereference-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''The name of the Snowflake table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-snowflaketablereference.html#cfn-cleanrooms-configuredtable-snowflaketablereference-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_schema(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.SnowflakeTableSchemaProperty"]]:
            '''The schema of the Snowflake table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-snowflaketablereference.html#cfn-cleanrooms-configuredtable-snowflaketablereference-tableschema
            '''
            result = self._values.get("table_schema")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.SnowflakeTableSchemaProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnowflakeTableReferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTablePropsMixin.SnowflakeTableSchemaProperty",
        jsii_struct_bases=[],
        name_mapping={"v1": "v1"},
    )
    class SnowflakeTableSchemaProperty:
        def __init__(
            self,
            *,
            v1: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfiguredTablePropsMixin.SnowflakeTableSchemaV1Property", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The schema of a Snowflake table.

            :param v1: The schema of a Snowflake table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-snowflaketableschema.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                snowflake_table_schema_property = cleanrooms_mixins.CfnConfiguredTablePropsMixin.SnowflakeTableSchemaProperty(
                    v1=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.SnowflakeTableSchemaV1Property(
                        column_name="columnName",
                        column_type="columnType"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eb6add7aca07bdcd3537db50d3bc294e395f9bd8c01c3fe29e06a1327b3545cf)
                check_type(argname="argument v1", value=v1, expected_type=type_hints["v1"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if v1 is not None:
                self._values["v1"] = v1

        @builtins.property
        def v1(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.SnowflakeTableSchemaV1Property"]]]]:
            '''The schema of a Snowflake table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-snowflaketableschema.html#cfn-cleanrooms-configuredtable-snowflaketableschema-v1
            '''
            result = self._values.get("v1")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.SnowflakeTableSchemaV1Property"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnowflakeTableSchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTablePropsMixin.SnowflakeTableSchemaV1Property",
        jsii_struct_bases=[],
        name_mapping={"column_name": "columnName", "column_type": "columnType"},
    )
    class SnowflakeTableSchemaV1Property:
        def __init__(
            self,
            *,
            column_name: typing.Optional[builtins.str] = None,
            column_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Snowflake table schema.

            :param column_name: The column name.
            :param column_type: The column's data type. Supported data types: ``ARRAY`` , ``BIGINT`` , ``BOOLEAN`` , ``CHAR`` , ``DATE`` , ``DECIMAL`` , ``DOUBLE`` , ``DOUBLE PRECISION`` , ``FLOAT`` , ``FLOAT4`` , ``INT`` , ``INTEGER`` , ``MAP`` , ``NUMERIC`` , ``NUMBER`` , ``REAL`` , ``SMALLINT`` , ``STRING`` , ``TIMESTAMP`` , ``TIMESTAMP_LTZ`` , ``TIMESTAMP_NTZ`` , ``DATETIME`` , ``TINYINT`` , ``VARCHAR`` , ``TEXT`` , ``CHARACTER`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-snowflaketableschemav1.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                snowflake_table_schema_v1_property = cleanrooms_mixins.CfnConfiguredTablePropsMixin.SnowflakeTableSchemaV1Property(
                    column_name="columnName",
                    column_type="columnType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3f0a5ff88cac2b3baad86eef31f8f0600a882c22841d017293c23bca8e25a7c0)
                check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
                check_type(argname="argument column_type", value=column_type, expected_type=type_hints["column_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if column_name is not None:
                self._values["column_name"] = column_name
            if column_type is not None:
                self._values["column_type"] = column_type

        @builtins.property
        def column_name(self) -> typing.Optional[builtins.str]:
            '''The column name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-snowflaketableschemav1.html#cfn-cleanrooms-configuredtable-snowflaketableschemav1-columnname
            '''
            result = self._values.get("column_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def column_type(self) -> typing.Optional[builtins.str]:
            '''The column's data type.

            Supported data types: ``ARRAY`` , ``BIGINT`` , ``BOOLEAN`` , ``CHAR`` , ``DATE`` , ``DECIMAL`` , ``DOUBLE`` , ``DOUBLE PRECISION`` , ``FLOAT`` , ``FLOAT4`` , ``INT`` , ``INTEGER`` , ``MAP`` , ``NUMERIC`` , ``NUMBER`` , ``REAL`` , ``SMALLINT`` , ``STRING`` , ``TIMESTAMP`` , ``TIMESTAMP_LTZ`` , ``TIMESTAMP_NTZ`` , ``DATETIME`` , ``TINYINT`` , ``VARCHAR`` , ``TEXT`` , ``CHARACTER`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-snowflaketableschemav1.html#cfn-cleanrooms-configuredtable-snowflaketableschemav1-columntype
            '''
            result = self._values.get("column_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnowflakeTableSchemaV1Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnConfiguredTablePropsMixin.TableReferenceProperty",
        jsii_struct_bases=[],
        name_mapping={"athena": "athena", "glue": "glue", "snowflake": "snowflake"},
    )
    class TableReferenceProperty:
        def __init__(
            self,
            *,
            athena: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfiguredTablePropsMixin.AthenaTableReferenceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            glue: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfiguredTablePropsMixin.GlueTableReferenceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            snowflake: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfiguredTablePropsMixin.SnowflakeTableReferenceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A pointer to the dataset that underlies this table.

            :param athena: If present, a reference to the Athena table referred to by this table reference.
            :param glue: If present, a reference to the AWS Glue table referred to by this table reference.
            :param snowflake: If present, a reference to the Snowflake table referred to by this table reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-tablereference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                table_reference_property = cleanrooms_mixins.CfnConfiguredTablePropsMixin.TableReferenceProperty(
                    athena=cleanrooms_mixins.CfnConfiguredTablePropsMixin.AthenaTableReferenceProperty(
                        database_name="databaseName",
                        output_location="outputLocation",
                        region="region",
                        table_name="tableName",
                        work_group="workGroup"
                    ),
                    glue=cleanrooms_mixins.CfnConfiguredTablePropsMixin.GlueTableReferenceProperty(
                        database_name="databaseName",
                        region="region",
                        table_name="tableName"
                    ),
                    snowflake=cleanrooms_mixins.CfnConfiguredTablePropsMixin.SnowflakeTableReferenceProperty(
                        account_identifier="accountIdentifier",
                        database_name="databaseName",
                        schema_name="schemaName",
                        secret_arn="secretArn",
                        table_name="tableName",
                        table_schema=cleanrooms_mixins.CfnConfiguredTablePropsMixin.SnowflakeTableSchemaProperty(
                            v1=[cleanrooms_mixins.CfnConfiguredTablePropsMixin.SnowflakeTableSchemaV1Property(
                                column_name="columnName",
                                column_type="columnType"
                            )]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__568f0fd57d92f6eb03485908a1b5179c636fe23773da32e9bc0a00a33437ea00)
                check_type(argname="argument athena", value=athena, expected_type=type_hints["athena"])
                check_type(argname="argument glue", value=glue, expected_type=type_hints["glue"])
                check_type(argname="argument snowflake", value=snowflake, expected_type=type_hints["snowflake"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if athena is not None:
                self._values["athena"] = athena
            if glue is not None:
                self._values["glue"] = glue
            if snowflake is not None:
                self._values["snowflake"] = snowflake

        @builtins.property
        def athena(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.AthenaTableReferenceProperty"]]:
            '''If present, a reference to the Athena table referred to by this table reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-tablereference.html#cfn-cleanrooms-configuredtable-tablereference-athena
            '''
            result = self._values.get("athena")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.AthenaTableReferenceProperty"]], result)

        @builtins.property
        def glue(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.GlueTableReferenceProperty"]]:
            '''If present, a reference to the AWS Glue table referred to by this table reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-tablereference.html#cfn-cleanrooms-configuredtable-tablereference-glue
            '''
            result = self._values.get("glue")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.GlueTableReferenceProperty"]], result)

        @builtins.property
        def snowflake(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.SnowflakeTableReferenceProperty"]]:
            '''If present, a reference to the Snowflake table referred to by this table reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-configuredtable-tablereference.html#cfn-cleanrooms-configuredtable-tablereference-snowflake
            '''
            result = self._values.get("snowflake")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfiguredTablePropsMixin.SnowflakeTableReferenceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TableReferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnIdMappingTableMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "input_reference_config": "inputReferenceConfig",
        "kms_key_arn": "kmsKeyArn",
        "membership_identifier": "membershipIdentifier",
        "name": "name",
        "tags": "tags",
    },
)
class CfnIdMappingTableMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        input_reference_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdMappingTablePropsMixin.IdMappingTableInputReferenceConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        membership_identifier: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnIdMappingTablePropsMixin.

        :param description: The description of the ID mapping table.
        :param input_reference_config: The input reference configuration for the ID mapping table.
        :param kms_key_arn: The Amazon Resource Name (ARN) of the AWS KMS key.
        :param membership_identifier: The unique identifier of the membership resource for the ID mapping table.
        :param name: The name of the ID mapping table.
        :param tags: An optional label that you can assign to a resource when you create it. Each tag consists of a key and an optional value, both of which you define. When you use tagging, you can also use tag-based access control in IAM policies to control access to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-idmappingtable.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
            
            cfn_id_mapping_table_mixin_props = cleanrooms_mixins.CfnIdMappingTableMixinProps(
                description="description",
                input_reference_config=cleanrooms_mixins.CfnIdMappingTablePropsMixin.IdMappingTableInputReferenceConfigProperty(
                    input_reference_arn="inputReferenceArn",
                    manage_resource_policies=False
                ),
                kms_key_arn="kmsKeyArn",
                membership_identifier="membershipIdentifier",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c16e8633b5fffb60472154302458843cf0f238c1f84e7e78db78ad7e1d7ed0a3)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument input_reference_config", value=input_reference_config, expected_type=type_hints["input_reference_config"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument membership_identifier", value=membership_identifier, expected_type=type_hints["membership_identifier"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if input_reference_config is not None:
            self._values["input_reference_config"] = input_reference_config
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if membership_identifier is not None:
            self._values["membership_identifier"] = membership_identifier
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the ID mapping table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-idmappingtable.html#cfn-cleanrooms-idmappingtable-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_reference_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdMappingTablePropsMixin.IdMappingTableInputReferenceConfigProperty"]]:
        '''The input reference configuration for the ID mapping table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-idmappingtable.html#cfn-cleanrooms-idmappingtable-inputreferenceconfig
        '''
        result = self._values.get("input_reference_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdMappingTablePropsMixin.IdMappingTableInputReferenceConfigProperty"]], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS KMS key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-idmappingtable.html#cfn-cleanrooms-idmappingtable-kmskeyarn
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def membership_identifier(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the membership resource for the ID mapping table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-idmappingtable.html#cfn-cleanrooms-idmappingtable-membershipidentifier
        '''
        result = self._values.get("membership_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the ID mapping table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-idmappingtable.html#cfn-cleanrooms-idmappingtable-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An optional label that you can assign to a resource when you create it.

        Each tag consists of a key and an optional value, both of which you define. When you use tagging, you can also use tag-based access control in IAM policies to control access to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-idmappingtable.html#cfn-cleanrooms-idmappingtable-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIdMappingTableMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnIdMappingTablePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnIdMappingTablePropsMixin",
):
    '''Describes information about the ID mapping table.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-idmappingtable.html
    :cloudformationResource: AWS::CleanRooms::IdMappingTable
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
        
        cfn_id_mapping_table_props_mixin = cleanrooms_mixins.CfnIdMappingTablePropsMixin(cleanrooms_mixins.CfnIdMappingTableMixinProps(
            description="description",
            input_reference_config=cleanrooms_mixins.CfnIdMappingTablePropsMixin.IdMappingTableInputReferenceConfigProperty(
                input_reference_arn="inputReferenceArn",
                manage_resource_policies=False
            ),
            kms_key_arn="kmsKeyArn",
            membership_identifier="membershipIdentifier",
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
        props: typing.Union[CfnIdMappingTableMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CleanRooms::IdMappingTable``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7e83be1f4cf0d28e39081f102bcf027ef9a5c20d52d097f1ab01414a3963c93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__661443a722bbad9b59ae10c8faee898b22fb7db320b76afc1a27093a0f185088)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c48e6a7c609464c1f43b62433a41c06e94f575245ed7a3d6457523ba4d070f2c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIdMappingTableMixinProps:
        return typing.cast(CfnIdMappingTableMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnIdMappingTablePropsMixin.IdMappingTableInputReferenceConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "input_reference_arn": "inputReferenceArn",
            "manage_resource_policies": "manageResourcePolicies",
        },
    )
    class IdMappingTableInputReferenceConfigProperty:
        def __init__(
            self,
            *,
            input_reference_arn: typing.Optional[builtins.str] = None,
            manage_resource_policies: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Provides the input reference configuration for the ID mapping table.

            :param input_reference_arn: The Amazon Resource Name (ARN) of the referenced resource in AWS Entity Resolution . Valid values are ID mapping workflow ARNs.
            :param manage_resource_policies: When ``TRUE`` , AWS Clean Rooms manages permissions for the ID mapping table resource. When ``FALSE`` , the resource owner manages permissions for the ID mapping table resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-idmappingtable-idmappingtableinputreferenceconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                id_mapping_table_input_reference_config_property = cleanrooms_mixins.CfnIdMappingTablePropsMixin.IdMappingTableInputReferenceConfigProperty(
                    input_reference_arn="inputReferenceArn",
                    manage_resource_policies=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5a2cade96148ba4fa402d47e6e647bded6e1be7ab7f53ac0c92edb8c3055311b)
                check_type(argname="argument input_reference_arn", value=input_reference_arn, expected_type=type_hints["input_reference_arn"])
                check_type(argname="argument manage_resource_policies", value=manage_resource_policies, expected_type=type_hints["manage_resource_policies"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if input_reference_arn is not None:
                self._values["input_reference_arn"] = input_reference_arn
            if manage_resource_policies is not None:
                self._values["manage_resource_policies"] = manage_resource_policies

        @builtins.property
        def input_reference_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the referenced resource in AWS Entity Resolution .

            Valid values are ID mapping workflow ARNs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-idmappingtable-idmappingtableinputreferenceconfig.html#cfn-cleanrooms-idmappingtable-idmappingtableinputreferenceconfig-inputreferencearn
            '''
            result = self._values.get("input_reference_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def manage_resource_policies(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When ``TRUE`` , AWS Clean Rooms manages permissions for the ID mapping table resource.

            When ``FALSE`` , the resource owner manages permissions for the ID mapping table resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-idmappingtable-idmappingtableinputreferenceconfig.html#cfn-cleanrooms-idmappingtable-idmappingtableinputreferenceconfig-manageresourcepolicies
            '''
            result = self._values.get("manage_resource_policies")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdMappingTableInputReferenceConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnIdMappingTablePropsMixin.IdMappingTableInputReferencePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"id_mapping_table_input_source": "idMappingTableInputSource"},
    )
    class IdMappingTableInputReferencePropertiesProperty:
        def __init__(
            self,
            *,
            id_mapping_table_input_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdMappingTablePropsMixin.IdMappingTableInputSourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The input reference properties for the ID mapping table.

            :param id_mapping_table_input_source: The input source of the ID mapping table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-idmappingtable-idmappingtableinputreferenceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                id_mapping_table_input_reference_properties_property = cleanrooms_mixins.CfnIdMappingTablePropsMixin.IdMappingTableInputReferencePropertiesProperty(
                    id_mapping_table_input_source=[cleanrooms_mixins.CfnIdMappingTablePropsMixin.IdMappingTableInputSourceProperty(
                        id_namespace_association_id="idNamespaceAssociationId",
                        type="type"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6ee5fc381d8f22739291fd8fa1647786829bf45bebf1ee7d2da9c2a662d9f8c0)
                check_type(argname="argument id_mapping_table_input_source", value=id_mapping_table_input_source, expected_type=type_hints["id_mapping_table_input_source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id_mapping_table_input_source is not None:
                self._values["id_mapping_table_input_source"] = id_mapping_table_input_source

        @builtins.property
        def id_mapping_table_input_source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdMappingTablePropsMixin.IdMappingTableInputSourceProperty"]]]]:
            '''The input source of the ID mapping table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-idmappingtable-idmappingtableinputreferenceproperties.html#cfn-cleanrooms-idmappingtable-idmappingtableinputreferenceproperties-idmappingtableinputsource
            '''
            result = self._values.get("id_mapping_table_input_source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdMappingTablePropsMixin.IdMappingTableInputSourceProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdMappingTableInputReferencePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnIdMappingTablePropsMixin.IdMappingTableInputSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id_namespace_association_id": "idNamespaceAssociationId",
            "type": "type",
        },
    )
    class IdMappingTableInputSourceProperty:
        def __init__(
            self,
            *,
            id_namespace_association_id: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The input source of the ID mapping table.

            :param id_namespace_association_id: The unique identifier of the ID namespace association.
            :param type: The type of the input source of the ID mapping table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-idmappingtable-idmappingtableinputsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                id_mapping_table_input_source_property = cleanrooms_mixins.CfnIdMappingTablePropsMixin.IdMappingTableInputSourceProperty(
                    id_namespace_association_id="idNamespaceAssociationId",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fb174d0740f9b4e77ec4765e8fc4c3db508b50141732b8e06872e3654a8422ea)
                check_type(argname="argument id_namespace_association_id", value=id_namespace_association_id, expected_type=type_hints["id_namespace_association_id"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id_namespace_association_id is not None:
                self._values["id_namespace_association_id"] = id_namespace_association_id
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def id_namespace_association_id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier of the ID namespace association.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-idmappingtable-idmappingtableinputsource.html#cfn-cleanrooms-idmappingtable-idmappingtableinputsource-idnamespaceassociationid
            '''
            result = self._values.get("id_namespace_association_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of the input source of the ID mapping table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-idmappingtable-idmappingtableinputsource.html#cfn-cleanrooms-idmappingtable-idmappingtableinputsource-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdMappingTableInputSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnIdNamespaceAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "id_mapping_config": "idMappingConfig",
        "input_reference_config": "inputReferenceConfig",
        "membership_identifier": "membershipIdentifier",
        "name": "name",
        "tags": "tags",
    },
)
class CfnIdNamespaceAssociationMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        id_mapping_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdNamespaceAssociationPropsMixin.IdMappingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        input_reference_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdNamespaceAssociationPropsMixin.IdNamespaceAssociationInputReferenceConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        membership_identifier: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnIdNamespaceAssociationPropsMixin.

        :param description: The description of the ID namespace association.
        :param id_mapping_config: The configuration settings for the ID mapping table.
        :param input_reference_config: The input reference configuration for the ID namespace association.
        :param membership_identifier: The unique identifier of the membership that contains the ID namespace association.
        :param name: The name of this ID namespace association.
        :param tags: An optional label that you can assign to a resource when you create it. Each tag consists of a key and an optional value, both of which you define. When you use tagging, you can also use tag-based access control in IAM policies to control access to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-idnamespaceassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
            
            cfn_id_namespace_association_mixin_props = cleanrooms_mixins.CfnIdNamespaceAssociationMixinProps(
                description="description",
                id_mapping_config=cleanrooms_mixins.CfnIdNamespaceAssociationPropsMixin.IdMappingConfigProperty(
                    allow_use_as_dimension_column=False
                ),
                input_reference_config=cleanrooms_mixins.CfnIdNamespaceAssociationPropsMixin.IdNamespaceAssociationInputReferenceConfigProperty(
                    input_reference_arn="inputReferenceArn",
                    manage_resource_policies=False
                ),
                membership_identifier="membershipIdentifier",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceb46343d68e0576604f4a78e71ed5e3374cb417543472cb5f58cee0ebf00221)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id_mapping_config", value=id_mapping_config, expected_type=type_hints["id_mapping_config"])
            check_type(argname="argument input_reference_config", value=input_reference_config, expected_type=type_hints["input_reference_config"])
            check_type(argname="argument membership_identifier", value=membership_identifier, expected_type=type_hints["membership_identifier"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if id_mapping_config is not None:
            self._values["id_mapping_config"] = id_mapping_config
        if input_reference_config is not None:
            self._values["input_reference_config"] = input_reference_config
        if membership_identifier is not None:
            self._values["membership_identifier"] = membership_identifier
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the ID namespace association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-idnamespaceassociation.html#cfn-cleanrooms-idnamespaceassociation-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id_mapping_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdNamespaceAssociationPropsMixin.IdMappingConfigProperty"]]:
        '''The configuration settings for the ID mapping table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-idnamespaceassociation.html#cfn-cleanrooms-idnamespaceassociation-idmappingconfig
        '''
        result = self._values.get("id_mapping_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdNamespaceAssociationPropsMixin.IdMappingConfigProperty"]], result)

    @builtins.property
    def input_reference_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdNamespaceAssociationPropsMixin.IdNamespaceAssociationInputReferenceConfigProperty"]]:
        '''The input reference configuration for the ID namespace association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-idnamespaceassociation.html#cfn-cleanrooms-idnamespaceassociation-inputreferenceconfig
        '''
        result = self._values.get("input_reference_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdNamespaceAssociationPropsMixin.IdNamespaceAssociationInputReferenceConfigProperty"]], result)

    @builtins.property
    def membership_identifier(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the membership that contains the ID namespace association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-idnamespaceassociation.html#cfn-cleanrooms-idnamespaceassociation-membershipidentifier
        '''
        result = self._values.get("membership_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of this ID namespace association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-idnamespaceassociation.html#cfn-cleanrooms-idnamespaceassociation-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An optional label that you can assign to a resource when you create it.

        Each tag consists of a key and an optional value, both of which you define. When you use tagging, you can also use tag-based access control in IAM policies to control access to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-idnamespaceassociation.html#cfn-cleanrooms-idnamespaceassociation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIdNamespaceAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnIdNamespaceAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnIdNamespaceAssociationPropsMixin",
):
    '''Provides information to create the ID namespace association.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-idnamespaceassociation.html
    :cloudformationResource: AWS::CleanRooms::IdNamespaceAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
        
        cfn_id_namespace_association_props_mixin = cleanrooms_mixins.CfnIdNamespaceAssociationPropsMixin(cleanrooms_mixins.CfnIdNamespaceAssociationMixinProps(
            description="description",
            id_mapping_config=cleanrooms_mixins.CfnIdNamespaceAssociationPropsMixin.IdMappingConfigProperty(
                allow_use_as_dimension_column=False
            ),
            input_reference_config=cleanrooms_mixins.CfnIdNamespaceAssociationPropsMixin.IdNamespaceAssociationInputReferenceConfigProperty(
                input_reference_arn="inputReferenceArn",
                manage_resource_policies=False
            ),
            membership_identifier="membershipIdentifier",
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
        props: typing.Union[CfnIdNamespaceAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CleanRooms::IdNamespaceAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f6f2f64f9efa54a385dbe1f9c2df7350509e83f431a7957a76eddf5bd86148e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80987e59e3261460c8662490e25380be5a3ba44ad02860b733eb44a6d9173111)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0123604dae230849746ed9a05dfb3a5da24c895cb7882f5805a48c337af6dff3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIdNamespaceAssociationMixinProps:
        return typing.cast(CfnIdNamespaceAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnIdNamespaceAssociationPropsMixin.IdMappingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"allow_use_as_dimension_column": "allowUseAsDimensionColumn"},
    )
    class IdMappingConfigProperty:
        def __init__(
            self,
            *,
            allow_use_as_dimension_column: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The configuration settings for the ID mapping table.

            :param allow_use_as_dimension_column: An indicator as to whether you can use your column as a dimension column in the ID mapping table ( ``TRUE`` ) or not ( ``FALSE`` ). Default is ``FALSE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-idnamespaceassociation-idmappingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                id_mapping_config_property = cleanrooms_mixins.CfnIdNamespaceAssociationPropsMixin.IdMappingConfigProperty(
                    allow_use_as_dimension_column=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__081ade3703339bd624be6a082a4b9967601a0efa5bb53c2582345a1c827aa02c)
                check_type(argname="argument allow_use_as_dimension_column", value=allow_use_as_dimension_column, expected_type=type_hints["allow_use_as_dimension_column"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allow_use_as_dimension_column is not None:
                self._values["allow_use_as_dimension_column"] = allow_use_as_dimension_column

        @builtins.property
        def allow_use_as_dimension_column(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''An indicator as to whether you can use your column as a dimension column in the ID mapping table ( ``TRUE`` ) or not ( ``FALSE`` ).

            Default is ``FALSE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-idnamespaceassociation-idmappingconfig.html#cfn-cleanrooms-idnamespaceassociation-idmappingconfig-allowuseasdimensioncolumn
            '''
            result = self._values.get("allow_use_as_dimension_column")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdMappingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnIdNamespaceAssociationPropsMixin.IdNamespaceAssociationInputReferenceConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "input_reference_arn": "inputReferenceArn",
            "manage_resource_policies": "manageResourcePolicies",
        },
    )
    class IdNamespaceAssociationInputReferenceConfigProperty:
        def __init__(
            self,
            *,
            input_reference_arn: typing.Optional[builtins.str] = None,
            manage_resource_policies: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Provides the information for the ID namespace association input reference configuration.

            :param input_reference_arn: The Amazon Resource Name (ARN) of the AWS Entity Resolution resource that is being associated to the collaboration. Valid resource ARNs are from the ID namespaces that you own.
            :param manage_resource_policies: When ``TRUE`` , AWS Clean Rooms manages permissions for the ID namespace association resource. When ``FALSE`` , the resource owner manages permissions for the ID namespace association resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-idnamespaceassociation-idnamespaceassociationinputreferenceconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                id_namespace_association_input_reference_config_property = cleanrooms_mixins.CfnIdNamespaceAssociationPropsMixin.IdNamespaceAssociationInputReferenceConfigProperty(
                    input_reference_arn="inputReferenceArn",
                    manage_resource_policies=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b4a611a40d62f659c1f802c916d534b2992de816e4d224fd6b0bb1ede48eb2ad)
                check_type(argname="argument input_reference_arn", value=input_reference_arn, expected_type=type_hints["input_reference_arn"])
                check_type(argname="argument manage_resource_policies", value=manage_resource_policies, expected_type=type_hints["manage_resource_policies"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if input_reference_arn is not None:
                self._values["input_reference_arn"] = input_reference_arn
            if manage_resource_policies is not None:
                self._values["manage_resource_policies"] = manage_resource_policies

        @builtins.property
        def input_reference_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the AWS Entity Resolution resource that is being associated to the collaboration.

            Valid resource ARNs are from the ID namespaces that you own.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-idnamespaceassociation-idnamespaceassociationinputreferenceconfig.html#cfn-cleanrooms-idnamespaceassociation-idnamespaceassociationinputreferenceconfig-inputreferencearn
            '''
            result = self._values.get("input_reference_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def manage_resource_policies(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When ``TRUE`` , AWS Clean Rooms manages permissions for the ID namespace association resource.

            When ``FALSE`` , the resource owner manages permissions for the ID namespace association resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-idnamespaceassociation-idnamespaceassociationinputreferenceconfig.html#cfn-cleanrooms-idnamespaceassociation-idnamespaceassociationinputreferenceconfig-manageresourcepolicies
            '''
            result = self._values.get("manage_resource_policies")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdNamespaceAssociationInputReferenceConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnIdNamespaceAssociationPropsMixin.IdNamespaceAssociationInputReferencePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id_mapping_workflows_supported": "idMappingWorkflowsSupported",
            "id_namespace_type": "idNamespaceType",
        },
    )
    class IdNamespaceAssociationInputReferencePropertiesProperty:
        def __init__(
            self,
            *,
            id_mapping_workflows_supported: typing.Optional[typing.Union[typing.Sequence[typing.Any], _aws_cdk_ceddda9d.IResolvable]] = None,
            id_namespace_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides the information for the ID namespace association input reference properties.

            :param id_mapping_workflows_supported: Defines how ID mapping workflows are supported for this ID namespace association.
            :param id_namespace_type: The ID namespace type for this ID namespace association.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-idnamespaceassociation-idnamespaceassociationinputreferenceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                # id_mapping_workflows_supported: Any
                
                id_namespace_association_input_reference_properties_property = cleanrooms_mixins.CfnIdNamespaceAssociationPropsMixin.IdNamespaceAssociationInputReferencePropertiesProperty(
                    id_mapping_workflows_supported=[id_mapping_workflows_supported],
                    id_namespace_type="idNamespaceType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b1fe87c90ffd0ecd3c95ac20529bbcc5ee8fabcd34bdd113db50b41784990e3f)
                check_type(argname="argument id_mapping_workflows_supported", value=id_mapping_workflows_supported, expected_type=type_hints["id_mapping_workflows_supported"])
                check_type(argname="argument id_namespace_type", value=id_namespace_type, expected_type=type_hints["id_namespace_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id_mapping_workflows_supported is not None:
                self._values["id_mapping_workflows_supported"] = id_mapping_workflows_supported
            if id_namespace_type is not None:
                self._values["id_namespace_type"] = id_namespace_type

        @builtins.property
        def id_mapping_workflows_supported(
            self,
        ) -> typing.Optional[typing.Union[typing.List[typing.Any], _aws_cdk_ceddda9d.IResolvable]]:
            '''Defines how ID mapping workflows are supported for this ID namespace association.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-idnamespaceassociation-idnamespaceassociationinputreferenceproperties.html#cfn-cleanrooms-idnamespaceassociation-idnamespaceassociationinputreferenceproperties-idmappingworkflowssupported
            '''
            result = self._values.get("id_mapping_workflows_supported")
            return typing.cast(typing.Optional[typing.Union[typing.List[typing.Any], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def id_namespace_type(self) -> typing.Optional[builtins.str]:
            '''The ID namespace type for this ID namespace association.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-idnamespaceassociation-idnamespaceassociationinputreferenceproperties.html#cfn-cleanrooms-idnamespaceassociation-idnamespaceassociationinputreferenceproperties-idnamespacetype
            '''
            result = self._values.get("id_namespace_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdNamespaceAssociationInputReferencePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnMembershipAnalysisLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnMembershipAnalysisLogs",
):
    '''Builder for CfnMembershipLogsMixin to generate ANALYSIS_LOGS for CfnMembership.

    :cloudformationResource: AWS::CleanRooms::Membership
    :logType: ANALYSIS_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
        
        cfn_membership_analysis_logs = cleanrooms_mixins.CfnMembershipAnalysisLogs()
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
    ) -> "CfnMembershipLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a99d254945ebe75f18b9c6744f79268100007fa03ea43d7bad4cea618cb6384)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnMembershipLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnMembershipLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__557fc0134db14836940c9ba6663a4598dd697247255719e23206d1a0888123e3)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnMembershipLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnMembershipLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__619e80545e76c81f022c51943009be042dbe34e05825d45de958fc877f31c23c)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnMembershipLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnMembershipLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnMembershipLogsMixin",
):
    '''Creates a membership for a specific collaboration identifier and joins the collaboration.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-membership.html
    :cloudformationResource: AWS::CleanRooms::Membership
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_membership_logs_mixin = cleanrooms_mixins.CfnMembershipLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::CleanRooms::Membership``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07e6aa00347d026a01fba88516718e8bc1446c9932f86a585dd04d5c7e350e02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b181bfeb4b4b6e45f5dd053a8e43a2de7b0038dc0a8295046d322124df1a2a51)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aacf87856fc439810adc28f10f9e54dd94e5e71bf3eaa0468bee0a5fc5b266d0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANALYSIS_LOGS")
    def ANALYSIS_LOGS(cls) -> CfnMembershipAnalysisLogs:
        return typing.cast(CfnMembershipAnalysisLogs, jsii.sget(cls, "ANALYSIS_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnMembershipMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "collaboration_identifier": "collaborationIdentifier",
        "default_job_result_configuration": "defaultJobResultConfiguration",
        "default_result_configuration": "defaultResultConfiguration",
        "job_log_status": "jobLogStatus",
        "payment_configuration": "paymentConfiguration",
        "query_log_status": "queryLogStatus",
        "tags": "tags",
    },
)
class CfnMembershipMixinProps:
    def __init__(
        self,
        *,
        collaboration_identifier: typing.Optional[builtins.str] = None,
        default_job_result_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMembershipPropsMixin.MembershipProtectedJobResultConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        default_result_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMembershipPropsMixin.MembershipProtectedQueryResultConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        job_log_status: typing.Optional[builtins.str] = None,
        payment_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMembershipPropsMixin.MembershipPaymentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        query_log_status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnMembershipPropsMixin.

        :param collaboration_identifier: The unique ID for the associated collaboration.
        :param default_job_result_configuration: The default job result configuration for the membership.
        :param default_result_configuration: The default protected query result configuration as specified by the member who can receive results.
        :param job_log_status: An indicator as to whether job logging has been enabled or disabled for the collaboration. When ``ENABLED`` , AWS Clean Rooms logs details about jobs run within this collaboration and those logs can be viewed in Amazon CloudWatch Logs. The default value is ``DISABLED`` .
        :param payment_configuration: The payment responsibilities accepted by the collaboration member.
        :param query_log_status: An indicator as to whether query logging has been enabled or disabled for the membership. When ``ENABLED`` , AWS Clean Rooms logs details about queries run within this collaboration and those logs can be viewed in Amazon CloudWatch Logs. The default value is ``DISABLED`` .
        :param tags: An optional label that you can assign to a resource when you create it. Each tag consists of a key and an optional value, both of which you define. When you use tagging, you can also use tag-based access control in IAM policies to control access to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-membership.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
            
            cfn_membership_mixin_props = cleanrooms_mixins.CfnMembershipMixinProps(
                collaboration_identifier="collaborationIdentifier",
                default_job_result_configuration=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipProtectedJobResultConfigurationProperty(
                    output_configuration=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipProtectedJobOutputConfigurationProperty(
                        s3=cleanrooms_mixins.CfnMembershipPropsMixin.ProtectedJobS3OutputConfigurationInputProperty(
                            bucket="bucket",
                            key_prefix="keyPrefix"
                        )
                    ),
                    role_arn="roleArn"
                ),
                default_result_configuration=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipProtectedQueryResultConfigurationProperty(
                    output_configuration=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipProtectedQueryOutputConfigurationProperty(
                        s3=cleanrooms_mixins.CfnMembershipPropsMixin.ProtectedQueryS3OutputConfigurationProperty(
                            bucket="bucket",
                            key_prefix="keyPrefix",
                            result_format="resultFormat",
                            single_file_output=False
                        )
                    ),
                    role_arn="roleArn"
                ),
                job_log_status="jobLogStatus",
                payment_configuration=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipPaymentConfigurationProperty(
                    job_compute=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipJobComputePaymentConfigProperty(
                        is_responsible=False
                    ),
                    machine_learning=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipMLPaymentConfigProperty(
                        model_inference=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipModelInferencePaymentConfigProperty(
                            is_responsible=False
                        ),
                        model_training=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipModelTrainingPaymentConfigProperty(
                            is_responsible=False
                        )
                    ),
                    query_compute=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipQueryComputePaymentConfigProperty(
                        is_responsible=False
                    )
                ),
                query_log_status="queryLogStatus",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__733d1150d35b389246bbcee2eb6f1f9ce233b0fe8a52b76cab43df8727213a4c)
            check_type(argname="argument collaboration_identifier", value=collaboration_identifier, expected_type=type_hints["collaboration_identifier"])
            check_type(argname="argument default_job_result_configuration", value=default_job_result_configuration, expected_type=type_hints["default_job_result_configuration"])
            check_type(argname="argument default_result_configuration", value=default_result_configuration, expected_type=type_hints["default_result_configuration"])
            check_type(argname="argument job_log_status", value=job_log_status, expected_type=type_hints["job_log_status"])
            check_type(argname="argument payment_configuration", value=payment_configuration, expected_type=type_hints["payment_configuration"])
            check_type(argname="argument query_log_status", value=query_log_status, expected_type=type_hints["query_log_status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if collaboration_identifier is not None:
            self._values["collaboration_identifier"] = collaboration_identifier
        if default_job_result_configuration is not None:
            self._values["default_job_result_configuration"] = default_job_result_configuration
        if default_result_configuration is not None:
            self._values["default_result_configuration"] = default_result_configuration
        if job_log_status is not None:
            self._values["job_log_status"] = job_log_status
        if payment_configuration is not None:
            self._values["payment_configuration"] = payment_configuration
        if query_log_status is not None:
            self._values["query_log_status"] = query_log_status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def collaboration_identifier(self) -> typing.Optional[builtins.str]:
        '''The unique ID for the associated collaboration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-membership.html#cfn-cleanrooms-membership-collaborationidentifier
        '''
        result = self._values.get("collaboration_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_job_result_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMembershipPropsMixin.MembershipProtectedJobResultConfigurationProperty"]]:
        '''The default job result configuration for the membership.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-membership.html#cfn-cleanrooms-membership-defaultjobresultconfiguration
        '''
        result = self._values.get("default_job_result_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMembershipPropsMixin.MembershipProtectedJobResultConfigurationProperty"]], result)

    @builtins.property
    def default_result_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMembershipPropsMixin.MembershipProtectedQueryResultConfigurationProperty"]]:
        '''The default protected query result configuration as specified by the member who can receive results.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-membership.html#cfn-cleanrooms-membership-defaultresultconfiguration
        '''
        result = self._values.get("default_result_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMembershipPropsMixin.MembershipProtectedQueryResultConfigurationProperty"]], result)

    @builtins.property
    def job_log_status(self) -> typing.Optional[builtins.str]:
        '''An indicator as to whether job logging has been enabled or disabled for the collaboration.

        When ``ENABLED`` , AWS Clean Rooms logs details about jobs run within this collaboration and those logs can be viewed in Amazon CloudWatch Logs. The default value is ``DISABLED`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-membership.html#cfn-cleanrooms-membership-joblogstatus
        '''
        result = self._values.get("job_log_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def payment_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMembershipPropsMixin.MembershipPaymentConfigurationProperty"]]:
        '''The payment responsibilities accepted by the collaboration member.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-membership.html#cfn-cleanrooms-membership-paymentconfiguration
        '''
        result = self._values.get("payment_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMembershipPropsMixin.MembershipPaymentConfigurationProperty"]], result)

    @builtins.property
    def query_log_status(self) -> typing.Optional[builtins.str]:
        '''An indicator as to whether query logging has been enabled or disabled for the membership.

        When ``ENABLED`` , AWS Clean Rooms logs details about queries run within this collaboration and those logs can be viewed in Amazon CloudWatch Logs. The default value is ``DISABLED`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-membership.html#cfn-cleanrooms-membership-querylogstatus
        '''
        result = self._values.get("query_log_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An optional label that you can assign to a resource when you create it.

        Each tag consists of a key and an optional value, both of which you define. When you use tagging, you can also use tag-based access control in IAM policies to control access to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-membership.html#cfn-cleanrooms-membership-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMembershipMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMembershipPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnMembershipPropsMixin",
):
    '''Creates a membership for a specific collaboration identifier and joins the collaboration.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-membership.html
    :cloudformationResource: AWS::CleanRooms::Membership
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
        
        cfn_membership_props_mixin = cleanrooms_mixins.CfnMembershipPropsMixin(cleanrooms_mixins.CfnMembershipMixinProps(
            collaboration_identifier="collaborationIdentifier",
            default_job_result_configuration=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipProtectedJobResultConfigurationProperty(
                output_configuration=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipProtectedJobOutputConfigurationProperty(
                    s3=cleanrooms_mixins.CfnMembershipPropsMixin.ProtectedJobS3OutputConfigurationInputProperty(
                        bucket="bucket",
                        key_prefix="keyPrefix"
                    )
                ),
                role_arn="roleArn"
            ),
            default_result_configuration=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipProtectedQueryResultConfigurationProperty(
                output_configuration=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipProtectedQueryOutputConfigurationProperty(
                    s3=cleanrooms_mixins.CfnMembershipPropsMixin.ProtectedQueryS3OutputConfigurationProperty(
                        bucket="bucket",
                        key_prefix="keyPrefix",
                        result_format="resultFormat",
                        single_file_output=False
                    )
                ),
                role_arn="roleArn"
            ),
            job_log_status="jobLogStatus",
            payment_configuration=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipPaymentConfigurationProperty(
                job_compute=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipJobComputePaymentConfigProperty(
                    is_responsible=False
                ),
                machine_learning=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipMLPaymentConfigProperty(
                    model_inference=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipModelInferencePaymentConfigProperty(
                        is_responsible=False
                    ),
                    model_training=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipModelTrainingPaymentConfigProperty(
                        is_responsible=False
                    )
                ),
                query_compute=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipQueryComputePaymentConfigProperty(
                    is_responsible=False
                )
            ),
            query_log_status="queryLogStatus",
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
        props: typing.Union[CfnMembershipMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CleanRooms::Membership``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95e00d211a861d5590a23208702ded2e0c7821a09a8f6777058fd8f3f92a2aa2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e203b593c6d790437a7ca7c786b1eb679bdaf8d0de979a73ec24ce31aa3f81c2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eecec1528d668a785f39f0bc3ff1e4bab0705212476972a7ab5ef5929c730b6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMembershipMixinProps:
        return typing.cast(CfnMembershipMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnMembershipPropsMixin.MembershipJobComputePaymentConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"is_responsible": "isResponsible"},
    )
    class MembershipJobComputePaymentConfigProperty:
        def __init__(
            self,
            *,
            is_responsible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''An object representing the payment responsibilities accepted by the collaboration member for query and job compute costs.

            :param is_responsible: Indicates whether the collaboration member has accepted to pay for job compute costs ( ``TRUE`` ) or has not accepted to pay for query and job compute costs ( ``FALSE`` ). There is only one member who pays for queries and jobs. An error message is returned for the following reasons: - If you set the value to ``FALSE`` but you are responsible to pay for query and job compute costs. - If you set the value to ``TRUE`` but you are not responsible to pay for query and job compute costs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershipjobcomputepaymentconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                membership_job_compute_payment_config_property = cleanrooms_mixins.CfnMembershipPropsMixin.MembershipJobComputePaymentConfigProperty(
                    is_responsible=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__96f13b8e87c2c2e57b6884b793df4e37046f006c1ead2b0d25eebd4e4fba7029)
                check_type(argname="argument is_responsible", value=is_responsible, expected_type=type_hints["is_responsible"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_responsible is not None:
                self._values["is_responsible"] = is_responsible

        @builtins.property
        def is_responsible(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the collaboration member has accepted to pay for job compute costs ( ``TRUE`` ) or has not accepted to pay for query and job compute costs ( ``FALSE`` ).

            There is only one member who pays for queries and jobs.

            An error message is returned for the following reasons:

            - If you set the value to ``FALSE`` but you are responsible to pay for query and job compute costs.
            - If you set the value to ``TRUE`` but you are not responsible to pay for query and job compute costs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershipjobcomputepaymentconfig.html#cfn-cleanrooms-membership-membershipjobcomputepaymentconfig-isresponsible
            '''
            result = self._values.get("is_responsible")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MembershipJobComputePaymentConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnMembershipPropsMixin.MembershipMLPaymentConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "model_inference": "modelInference",
            "model_training": "modelTraining",
        },
    )
    class MembershipMLPaymentConfigProperty:
        def __init__(
            self,
            *,
            model_inference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMembershipPropsMixin.MembershipModelInferencePaymentConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            model_training: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMembershipPropsMixin.MembershipModelTrainingPaymentConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object representing the collaboration member's machine learning payment responsibilities set by the collaboration creator.

            :param model_inference: The payment responsibilities accepted by the member for model inference.
            :param model_training: The payment responsibilities accepted by the member for model training.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershipmlpaymentconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                membership_mLPayment_config_property = cleanrooms_mixins.CfnMembershipPropsMixin.MembershipMLPaymentConfigProperty(
                    model_inference=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipModelInferencePaymentConfigProperty(
                        is_responsible=False
                    ),
                    model_training=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipModelTrainingPaymentConfigProperty(
                        is_responsible=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f8a4e2a3d52fa9945125e593d45b4528735676da08ff447a0dc8724a5681fabc)
                check_type(argname="argument model_inference", value=model_inference, expected_type=type_hints["model_inference"])
                check_type(argname="argument model_training", value=model_training, expected_type=type_hints["model_training"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if model_inference is not None:
                self._values["model_inference"] = model_inference
            if model_training is not None:
                self._values["model_training"] = model_training

        @builtins.property
        def model_inference(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMembershipPropsMixin.MembershipModelInferencePaymentConfigProperty"]]:
            '''The payment responsibilities accepted by the member for model inference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershipmlpaymentconfig.html#cfn-cleanrooms-membership-membershipmlpaymentconfig-modelinference
            '''
            result = self._values.get("model_inference")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMembershipPropsMixin.MembershipModelInferencePaymentConfigProperty"]], result)

        @builtins.property
        def model_training(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMembershipPropsMixin.MembershipModelTrainingPaymentConfigProperty"]]:
            '''The payment responsibilities accepted by the member for model training.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershipmlpaymentconfig.html#cfn-cleanrooms-membership-membershipmlpaymentconfig-modeltraining
            '''
            result = self._values.get("model_training")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMembershipPropsMixin.MembershipModelTrainingPaymentConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MembershipMLPaymentConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnMembershipPropsMixin.MembershipModelInferencePaymentConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"is_responsible": "isResponsible"},
    )
    class MembershipModelInferencePaymentConfigProperty:
        def __init__(
            self,
            *,
            is_responsible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''An object representing the collaboration member's model inference payment responsibilities set by the collaboration creator.

            :param is_responsible: Indicates whether the collaboration member has accepted to pay for model inference costs ( ``TRUE`` ) or has not accepted to pay for model inference costs ( ``FALSE`` ). If the collaboration creator has not specified anyone to pay for model inference costs, then the member who can query is the default payer. An error message is returned for the following reasons: - If you set the value to ``FALSE`` but you are responsible to pay for model inference costs. - If you set the value to ``TRUE`` but you are not responsible to pay for model inference costs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershipmodelinferencepaymentconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                membership_model_inference_payment_config_property = cleanrooms_mixins.CfnMembershipPropsMixin.MembershipModelInferencePaymentConfigProperty(
                    is_responsible=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c44f66063d7194a49938e4f8ae099beb2de0912e9296a7260b5bdfffe23c6efa)
                check_type(argname="argument is_responsible", value=is_responsible, expected_type=type_hints["is_responsible"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_responsible is not None:
                self._values["is_responsible"] = is_responsible

        @builtins.property
        def is_responsible(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the collaboration member has accepted to pay for model inference costs ( ``TRUE`` ) or has not accepted to pay for model inference costs ( ``FALSE`` ).

            If the collaboration creator has not specified anyone to pay for model inference costs, then the member who can query is the default payer.

            An error message is returned for the following reasons:

            - If you set the value to ``FALSE`` but you are responsible to pay for model inference costs.
            - If you set the value to ``TRUE`` but you are not responsible to pay for model inference costs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershipmodelinferencepaymentconfig.html#cfn-cleanrooms-membership-membershipmodelinferencepaymentconfig-isresponsible
            '''
            result = self._values.get("is_responsible")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MembershipModelInferencePaymentConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnMembershipPropsMixin.MembershipModelTrainingPaymentConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"is_responsible": "isResponsible"},
    )
    class MembershipModelTrainingPaymentConfigProperty:
        def __init__(
            self,
            *,
            is_responsible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''An object representing the collaboration member's model training payment responsibilities set by the collaboration creator.

            :param is_responsible: Indicates whether the collaboration member has accepted to pay for model training costs ( ``TRUE`` ) or has not accepted to pay for model training costs ( ``FALSE`` ). If the collaboration creator has not specified anyone to pay for model training costs, then the member who can query is the default payer. An error message is returned for the following reasons: - If you set the value to ``FALSE`` but you are responsible to pay for model training costs. - If you set the value to ``TRUE`` but you are not responsible to pay for model training costs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershipmodeltrainingpaymentconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                membership_model_training_payment_config_property = cleanrooms_mixins.CfnMembershipPropsMixin.MembershipModelTrainingPaymentConfigProperty(
                    is_responsible=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__15660588d3021ee15df3b1456a8052cfb14ff5fc82383048a3c17527b9d3240e)
                check_type(argname="argument is_responsible", value=is_responsible, expected_type=type_hints["is_responsible"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_responsible is not None:
                self._values["is_responsible"] = is_responsible

        @builtins.property
        def is_responsible(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the collaboration member has accepted to pay for model training costs ( ``TRUE`` ) or has not accepted to pay for model training costs ( ``FALSE`` ).

            If the collaboration creator has not specified anyone to pay for model training costs, then the member who can query is the default payer.

            An error message is returned for the following reasons:

            - If you set the value to ``FALSE`` but you are responsible to pay for model training costs.
            - If you set the value to ``TRUE`` but you are not responsible to pay for model training costs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershipmodeltrainingpaymentconfig.html#cfn-cleanrooms-membership-membershipmodeltrainingpaymentconfig-isresponsible
            '''
            result = self._values.get("is_responsible")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MembershipModelTrainingPaymentConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnMembershipPropsMixin.MembershipPaymentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "job_compute": "jobCompute",
            "machine_learning": "machineLearning",
            "query_compute": "queryCompute",
        },
    )
    class MembershipPaymentConfigurationProperty:
        def __init__(
            self,
            *,
            job_compute: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMembershipPropsMixin.MembershipJobComputePaymentConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            machine_learning: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMembershipPropsMixin.MembershipMLPaymentConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            query_compute: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMembershipPropsMixin.MembershipQueryComputePaymentConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object representing the payment responsibilities accepted by the collaboration member.

            :param job_compute: The payment responsibilities accepted by the collaboration member for job compute costs.
            :param machine_learning: The payment responsibilities accepted by the collaboration member for machine learning costs.
            :param query_compute: The payment responsibilities accepted by the collaboration member for query compute costs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershippaymentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                membership_payment_configuration_property = cleanrooms_mixins.CfnMembershipPropsMixin.MembershipPaymentConfigurationProperty(
                    job_compute=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipJobComputePaymentConfigProperty(
                        is_responsible=False
                    ),
                    machine_learning=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipMLPaymentConfigProperty(
                        model_inference=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipModelInferencePaymentConfigProperty(
                            is_responsible=False
                        ),
                        model_training=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipModelTrainingPaymentConfigProperty(
                            is_responsible=False
                        )
                    ),
                    query_compute=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipQueryComputePaymentConfigProperty(
                        is_responsible=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cd537c19fd8126f3f78c665caf619ace4ab111371f2f74dda5e33ee9e06e6fd9)
                check_type(argname="argument job_compute", value=job_compute, expected_type=type_hints["job_compute"])
                check_type(argname="argument machine_learning", value=machine_learning, expected_type=type_hints["machine_learning"])
                check_type(argname="argument query_compute", value=query_compute, expected_type=type_hints["query_compute"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if job_compute is not None:
                self._values["job_compute"] = job_compute
            if machine_learning is not None:
                self._values["machine_learning"] = machine_learning
            if query_compute is not None:
                self._values["query_compute"] = query_compute

        @builtins.property
        def job_compute(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMembershipPropsMixin.MembershipJobComputePaymentConfigProperty"]]:
            '''The payment responsibilities accepted by the collaboration member for job compute costs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershippaymentconfiguration.html#cfn-cleanrooms-membership-membershippaymentconfiguration-jobcompute
            '''
            result = self._values.get("job_compute")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMembershipPropsMixin.MembershipJobComputePaymentConfigProperty"]], result)

        @builtins.property
        def machine_learning(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMembershipPropsMixin.MembershipMLPaymentConfigProperty"]]:
            '''The payment responsibilities accepted by the collaboration member for machine learning costs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershippaymentconfiguration.html#cfn-cleanrooms-membership-membershippaymentconfiguration-machinelearning
            '''
            result = self._values.get("machine_learning")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMembershipPropsMixin.MembershipMLPaymentConfigProperty"]], result)

        @builtins.property
        def query_compute(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMembershipPropsMixin.MembershipQueryComputePaymentConfigProperty"]]:
            '''The payment responsibilities accepted by the collaboration member for query compute costs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershippaymentconfiguration.html#cfn-cleanrooms-membership-membershippaymentconfiguration-querycompute
            '''
            result = self._values.get("query_compute")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMembershipPropsMixin.MembershipQueryComputePaymentConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MembershipPaymentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnMembershipPropsMixin.MembershipProtectedJobOutputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3": "s3"},
    )
    class MembershipProtectedJobOutputConfigurationProperty:
        def __init__(
            self,
            *,
            s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMembershipPropsMixin.ProtectedJobS3OutputConfigurationInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains configurations for protected job results.

            :param s3: Contains the configuration to write the job results to S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershipprotectedjoboutputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                membership_protected_job_output_configuration_property = cleanrooms_mixins.CfnMembershipPropsMixin.MembershipProtectedJobOutputConfigurationProperty(
                    s3=cleanrooms_mixins.CfnMembershipPropsMixin.ProtectedJobS3OutputConfigurationInputProperty(
                        bucket="bucket",
                        key_prefix="keyPrefix"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7883a681c698f481835ce2608ba4091aa8e8c8bf9b03a6481d8b3947148aa47e)
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3 is not None:
                self._values["s3"] = s3

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMembershipPropsMixin.ProtectedJobS3OutputConfigurationInputProperty"]]:
            '''Contains the configuration to write the job results to S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershipprotectedjoboutputconfiguration.html#cfn-cleanrooms-membership-membershipprotectedjoboutputconfiguration-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMembershipPropsMixin.ProtectedJobS3OutputConfigurationInputProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MembershipProtectedJobOutputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnMembershipPropsMixin.MembershipProtectedJobResultConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "output_configuration": "outputConfiguration",
            "role_arn": "roleArn",
        },
    )
    class MembershipProtectedJobResultConfigurationProperty:
        def __init__(
            self,
            *,
            output_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMembershipPropsMixin.MembershipProtectedJobOutputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains configurations for protected job results.

            :param output_configuration: The output configuration for a protected job result.
            :param role_arn: The unique ARN for an IAM role that is used by AWS Clean Rooms to write protected job results to the result location, given by the member who can receive results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershipprotectedjobresultconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                membership_protected_job_result_configuration_property = cleanrooms_mixins.CfnMembershipPropsMixin.MembershipProtectedJobResultConfigurationProperty(
                    output_configuration=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipProtectedJobOutputConfigurationProperty(
                        s3=cleanrooms_mixins.CfnMembershipPropsMixin.ProtectedJobS3OutputConfigurationInputProperty(
                            bucket="bucket",
                            key_prefix="keyPrefix"
                        )
                    ),
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1c2bf16f9ec3fdabd81e653cc284809b45f746aede382bf247ff1b845b0b327b)
                check_type(argname="argument output_configuration", value=output_configuration, expected_type=type_hints["output_configuration"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if output_configuration is not None:
                self._values["output_configuration"] = output_configuration
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def output_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMembershipPropsMixin.MembershipProtectedJobOutputConfigurationProperty"]]:
            '''The output configuration for a protected job result.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershipprotectedjobresultconfiguration.html#cfn-cleanrooms-membership-membershipprotectedjobresultconfiguration-outputconfiguration
            '''
            result = self._values.get("output_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMembershipPropsMixin.MembershipProtectedJobOutputConfigurationProperty"]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The unique ARN for an IAM role that is used by AWS Clean Rooms to write protected job results to the result location, given by the member who can receive results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershipprotectedjobresultconfiguration.html#cfn-cleanrooms-membership-membershipprotectedjobresultconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MembershipProtectedJobResultConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnMembershipPropsMixin.MembershipProtectedQueryOutputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3": "s3"},
    )
    class MembershipProtectedQueryOutputConfigurationProperty:
        def __init__(
            self,
            *,
            s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMembershipPropsMixin.ProtectedQueryS3OutputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains configurations for protected query results.

            :param s3: Required configuration for a protected query with an ``s3`` output type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershipprotectedqueryoutputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                membership_protected_query_output_configuration_property = cleanrooms_mixins.CfnMembershipPropsMixin.MembershipProtectedQueryOutputConfigurationProperty(
                    s3=cleanrooms_mixins.CfnMembershipPropsMixin.ProtectedQueryS3OutputConfigurationProperty(
                        bucket="bucket",
                        key_prefix="keyPrefix",
                        result_format="resultFormat",
                        single_file_output=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__24ddbbcfe391cff98d0af563a1eb130e8ad41590bfceca06f3579a8d4d074109)
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3 is not None:
                self._values["s3"] = s3

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMembershipPropsMixin.ProtectedQueryS3OutputConfigurationProperty"]]:
            '''Required configuration for a protected query with an ``s3`` output type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershipprotectedqueryoutputconfiguration.html#cfn-cleanrooms-membership-membershipprotectedqueryoutputconfiguration-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMembershipPropsMixin.ProtectedQueryS3OutputConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MembershipProtectedQueryOutputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnMembershipPropsMixin.MembershipProtectedQueryResultConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "output_configuration": "outputConfiguration",
            "role_arn": "roleArn",
        },
    )
    class MembershipProtectedQueryResultConfigurationProperty:
        def __init__(
            self,
            *,
            output_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMembershipPropsMixin.MembershipProtectedQueryOutputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains configurations for protected query results.

            :param output_configuration: Configuration for protected query results.
            :param role_arn: The unique ARN for an IAM role that is used by AWS Clean Rooms to write protected query results to the result location, given by the member who can receive results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershipprotectedqueryresultconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                membership_protected_query_result_configuration_property = cleanrooms_mixins.CfnMembershipPropsMixin.MembershipProtectedQueryResultConfigurationProperty(
                    output_configuration=cleanrooms_mixins.CfnMembershipPropsMixin.MembershipProtectedQueryOutputConfigurationProperty(
                        s3=cleanrooms_mixins.CfnMembershipPropsMixin.ProtectedQueryS3OutputConfigurationProperty(
                            bucket="bucket",
                            key_prefix="keyPrefix",
                            result_format="resultFormat",
                            single_file_output=False
                        )
                    ),
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4b90ab72d5ecfc8e44940125909ebeecca400f0685b39f8e9f18f8373b4e2f0e)
                check_type(argname="argument output_configuration", value=output_configuration, expected_type=type_hints["output_configuration"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if output_configuration is not None:
                self._values["output_configuration"] = output_configuration
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def output_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMembershipPropsMixin.MembershipProtectedQueryOutputConfigurationProperty"]]:
            '''Configuration for protected query results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershipprotectedqueryresultconfiguration.html#cfn-cleanrooms-membership-membershipprotectedqueryresultconfiguration-outputconfiguration
            '''
            result = self._values.get("output_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMembershipPropsMixin.MembershipProtectedQueryOutputConfigurationProperty"]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The unique ARN for an IAM role that is used by AWS Clean Rooms to write protected query results to the result location, given by the member who can receive results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershipprotectedqueryresultconfiguration.html#cfn-cleanrooms-membership-membershipprotectedqueryresultconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MembershipProtectedQueryResultConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnMembershipPropsMixin.MembershipQueryComputePaymentConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"is_responsible": "isResponsible"},
    )
    class MembershipQueryComputePaymentConfigProperty:
        def __init__(
            self,
            *,
            is_responsible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''An object representing the payment responsibilities accepted by the collaboration member for query compute costs.

            :param is_responsible: Indicates whether the collaboration member has accepted to pay for query compute costs ( ``TRUE`` ) or has not accepted to pay for query compute costs ( ``FALSE`` ). If the collaboration creator has not specified anyone to pay for query compute costs, then the member who can query is the default payer. An error message is returned for the following reasons: - If you set the value to ``FALSE`` but you are responsible to pay for query compute costs. - If you set the value to ``TRUE`` but you are not responsible to pay for query compute costs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershipquerycomputepaymentconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                membership_query_compute_payment_config_property = cleanrooms_mixins.CfnMembershipPropsMixin.MembershipQueryComputePaymentConfigProperty(
                    is_responsible=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1b6b1718ad2e99476716752605057e9b17fe81870b4156750e4659edb630c159)
                check_type(argname="argument is_responsible", value=is_responsible, expected_type=type_hints["is_responsible"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_responsible is not None:
                self._values["is_responsible"] = is_responsible

        @builtins.property
        def is_responsible(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the collaboration member has accepted to pay for query compute costs ( ``TRUE`` ) or has not accepted to pay for query compute costs ( ``FALSE`` ).

            If the collaboration creator has not specified anyone to pay for query compute costs, then the member who can query is the default payer.

            An error message is returned for the following reasons:

            - If you set the value to ``FALSE`` but you are responsible to pay for query compute costs.
            - If you set the value to ``TRUE`` but you are not responsible to pay for query compute costs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-membershipquerycomputepaymentconfig.html#cfn-cleanrooms-membership-membershipquerycomputepaymentconfig-isresponsible
            '''
            result = self._values.get("is_responsible")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MembershipQueryComputePaymentConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnMembershipPropsMixin.ProtectedJobS3OutputConfigurationInputProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key_prefix": "keyPrefix"},
    )
    class ProtectedJobS3OutputConfigurationInputProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            key_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains input information for protected jobs with an S3 output type.

            :param bucket: The S3 bucket for job output.
            :param key_prefix: The S3 prefix to unload the protected job results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-protectedjobs3outputconfigurationinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                protected_job_s3_output_configuration_input_property = cleanrooms_mixins.CfnMembershipPropsMixin.ProtectedJobS3OutputConfigurationInputProperty(
                    bucket="bucket",
                    key_prefix="keyPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cc6a92eed991e3e08998eb3383c76d6374281cfb102b984a97c768bfa1976e8c)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key_prefix", value=key_prefix, expected_type=type_hints["key_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if key_prefix is not None:
                self._values["key_prefix"] = key_prefix

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The S3 bucket for job output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-protectedjobs3outputconfigurationinput.html#cfn-cleanrooms-membership-protectedjobs3outputconfigurationinput-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_prefix(self) -> typing.Optional[builtins.str]:
            '''The S3 prefix to unload the protected job results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-protectedjobs3outputconfigurationinput.html#cfn-cleanrooms-membership-protectedjobs3outputconfigurationinput-keyprefix
            '''
            result = self._values.get("key_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProtectedJobS3OutputConfigurationInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnMembershipPropsMixin.ProtectedQueryS3OutputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "key_prefix": "keyPrefix",
            "result_format": "resultFormat",
            "single_file_output": "singleFileOutput",
        },
    )
    class ProtectedQueryS3OutputConfigurationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            key_prefix: typing.Optional[builtins.str] = None,
            result_format: typing.Optional[builtins.str] = None,
            single_file_output: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Contains the configuration to write the query results to S3.

            :param bucket: The S3 bucket to unload the protected query results.
            :param key_prefix: The S3 prefix to unload the protected query results.
            :param result_format: Intended file format of the result.
            :param single_file_output: Indicates whether files should be output as a single file ( ``TRUE`` ) or output as multiple files ( ``FALSE`` ). This parameter is only supported for analyses with the Spark analytics engine.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-protectedquerys3outputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                protected_query_s3_output_configuration_property = cleanrooms_mixins.CfnMembershipPropsMixin.ProtectedQueryS3OutputConfigurationProperty(
                    bucket="bucket",
                    key_prefix="keyPrefix",
                    result_format="resultFormat",
                    single_file_output=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__01e0c30135fbee9dc35e2927dc326b92960a54816262b3c282f1efb66a279b17)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key_prefix", value=key_prefix, expected_type=type_hints["key_prefix"])
                check_type(argname="argument result_format", value=result_format, expected_type=type_hints["result_format"])
                check_type(argname="argument single_file_output", value=single_file_output, expected_type=type_hints["single_file_output"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if key_prefix is not None:
                self._values["key_prefix"] = key_prefix
            if result_format is not None:
                self._values["result_format"] = result_format
            if single_file_output is not None:
                self._values["single_file_output"] = single_file_output

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The S3 bucket to unload the protected query results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-protectedquerys3outputconfiguration.html#cfn-cleanrooms-membership-protectedquerys3outputconfiguration-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_prefix(self) -> typing.Optional[builtins.str]:
            '''The S3 prefix to unload the protected query results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-protectedquerys3outputconfiguration.html#cfn-cleanrooms-membership-protectedquerys3outputconfiguration-keyprefix
            '''
            result = self._values.get("key_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def result_format(self) -> typing.Optional[builtins.str]:
            '''Intended file format of the result.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-protectedquerys3outputconfiguration.html#cfn-cleanrooms-membership-protectedquerys3outputconfiguration-resultformat
            '''
            result = self._values.get("result_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def single_file_output(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether files should be output as a single file ( ``TRUE`` ) or output as multiple files ( ``FALSE`` ).

            This parameter is only supported for analyses with the Spark analytics engine.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-membership-protectedquerys3outputconfiguration.html#cfn-cleanrooms-membership-protectedquerys3outputconfiguration-singlefileoutput
            '''
            result = self._values.get("single_file_output")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProtectedQueryS3OutputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnPrivacyBudgetTemplateMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_refresh": "autoRefresh",
        "membership_identifier": "membershipIdentifier",
        "parameters": "parameters",
        "privacy_budget_type": "privacyBudgetType",
        "tags": "tags",
    },
)
class CfnPrivacyBudgetTemplateMixinProps:
    def __init__(
        self,
        *,
        auto_refresh: typing.Optional[builtins.str] = None,
        membership_identifier: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPrivacyBudgetTemplatePropsMixin.ParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        privacy_budget_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPrivacyBudgetTemplatePropsMixin.

        :param auto_refresh: How often the privacy budget refreshes. .. epigraph:: If you plan to regularly bring new data into the collaboration, use ``CALENDAR_MONTH`` to automatically get a new privacy budget for the collaboration every calendar month. Choosing this option allows arbitrary amounts of information to be revealed about rows of the data when repeatedly queried across refreshes. Avoid choosing this if the same rows will be repeatedly queried between privacy budget refreshes.
        :param membership_identifier: The identifier for a membership resource.
        :param parameters: Specifies the epsilon and noise parameters for the privacy budget template.
        :param privacy_budget_type: Specifies the type of the privacy budget template.
        :param tags: An optional label that you can assign to a resource when you create it. Each tag consists of a key and an optional value, both of which you define. When you use tagging, you can also use tag-based access control in IAM policies to control access to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-privacybudgettemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
            
            cfn_privacy_budget_template_mixin_props = cleanrooms_mixins.CfnPrivacyBudgetTemplateMixinProps(
                auto_refresh="autoRefresh",
                membership_identifier="membershipIdentifier",
                parameters=cleanrooms_mixins.CfnPrivacyBudgetTemplatePropsMixin.ParametersProperty(
                    budget_parameters=[cleanrooms_mixins.CfnPrivacyBudgetTemplatePropsMixin.BudgetParameterProperty(
                        auto_refresh="autoRefresh",
                        budget=123,
                        type="type"
                    )],
                    epsilon=123,
                    resource_arn="resourceArn",
                    users_noise_per_query=123
                ),
                privacy_budget_type="privacyBudgetType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59ecd5fabefb1d78a3558b3cb91a6815d6a586e510712682e42af1228c93d3e7)
            check_type(argname="argument auto_refresh", value=auto_refresh, expected_type=type_hints["auto_refresh"])
            check_type(argname="argument membership_identifier", value=membership_identifier, expected_type=type_hints["membership_identifier"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument privacy_budget_type", value=privacy_budget_type, expected_type=type_hints["privacy_budget_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_refresh is not None:
            self._values["auto_refresh"] = auto_refresh
        if membership_identifier is not None:
            self._values["membership_identifier"] = membership_identifier
        if parameters is not None:
            self._values["parameters"] = parameters
        if privacy_budget_type is not None:
            self._values["privacy_budget_type"] = privacy_budget_type
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def auto_refresh(self) -> typing.Optional[builtins.str]:
        '''How often the privacy budget refreshes.

        .. epigraph::

           If you plan to regularly bring new data into the collaboration, use ``CALENDAR_MONTH`` to automatically get a new privacy budget for the collaboration every calendar month. Choosing this option allows arbitrary amounts of information to be revealed about rows of the data when repeatedly queried across refreshes. Avoid choosing this if the same rows will be repeatedly queried between privacy budget refreshes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-privacybudgettemplate.html#cfn-cleanrooms-privacybudgettemplate-autorefresh
        '''
        result = self._values.get("auto_refresh")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def membership_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier for a membership resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-privacybudgettemplate.html#cfn-cleanrooms-privacybudgettemplate-membershipidentifier
        '''
        result = self._values.get("membership_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrivacyBudgetTemplatePropsMixin.ParametersProperty"]]:
        '''Specifies the epsilon and noise parameters for the privacy budget template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-privacybudgettemplate.html#cfn-cleanrooms-privacybudgettemplate-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrivacyBudgetTemplatePropsMixin.ParametersProperty"]], result)

    @builtins.property
    def privacy_budget_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of the privacy budget template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-privacybudgettemplate.html#cfn-cleanrooms-privacybudgettemplate-privacybudgettype
        '''
        result = self._values.get("privacy_budget_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An optional label that you can assign to a resource when you create it.

        Each tag consists of a key and an optional value, both of which you define. When you use tagging, you can also use tag-based access control in IAM policies to control access to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-privacybudgettemplate.html#cfn-cleanrooms-privacybudgettemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPrivacyBudgetTemplateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPrivacyBudgetTemplatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnPrivacyBudgetTemplatePropsMixin",
):
    '''An object that defines the privacy budget template.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanrooms-privacybudgettemplate.html
    :cloudformationResource: AWS::CleanRooms::PrivacyBudgetTemplate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
        
        cfn_privacy_budget_template_props_mixin = cleanrooms_mixins.CfnPrivacyBudgetTemplatePropsMixin(cleanrooms_mixins.CfnPrivacyBudgetTemplateMixinProps(
            auto_refresh="autoRefresh",
            membership_identifier="membershipIdentifier",
            parameters=cleanrooms_mixins.CfnPrivacyBudgetTemplatePropsMixin.ParametersProperty(
                budget_parameters=[cleanrooms_mixins.CfnPrivacyBudgetTemplatePropsMixin.BudgetParameterProperty(
                    auto_refresh="autoRefresh",
                    budget=123,
                    type="type"
                )],
                epsilon=123,
                resource_arn="resourceArn",
                users_noise_per_query=123
            ),
            privacy_budget_type="privacyBudgetType",
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
        props: typing.Union[CfnPrivacyBudgetTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CleanRooms::PrivacyBudgetTemplate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffe2e44ad3945ed1233c7c0a781606a8e0e47c71a39f6dd0bd4dad60aba7e0dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d16a0cf366e7c1bdee6d877c6f286c928c48d30c17743235d2e547b4051a72f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5d742002c520de0f51b3a7100aadb77853b187107ec7dbc62b5300aa27d64b0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPrivacyBudgetTemplateMixinProps:
        return typing.cast(CfnPrivacyBudgetTemplateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnPrivacyBudgetTemplatePropsMixin.BudgetParameterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_refresh": "autoRefresh",
            "budget": "budget",
            "type": "type",
        },
    )
    class BudgetParameterProperty:
        def __init__(
            self,
            *,
            auto_refresh: typing.Optional[builtins.str] = None,
            budget: typing.Optional[jsii.Number] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Individual budget parameter configuration that defines specific budget allocation settings for access budgets.

            :param auto_refresh: Whether this individual budget parameter automatically refreshes when the budget period resets.
            :param budget: The budget allocation amount for this specific parameter.
            :param type: The type of budget parameter being configured.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-privacybudgettemplate-budgetparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                budget_parameter_property = cleanrooms_mixins.CfnPrivacyBudgetTemplatePropsMixin.BudgetParameterProperty(
                    auto_refresh="autoRefresh",
                    budget=123,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__56fbc0dfe70bb57cea8d17f82fddcdc382f686140e52ab76f7bdd92bacd8d234)
                check_type(argname="argument auto_refresh", value=auto_refresh, expected_type=type_hints["auto_refresh"])
                check_type(argname="argument budget", value=budget, expected_type=type_hints["budget"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_refresh is not None:
                self._values["auto_refresh"] = auto_refresh
            if budget is not None:
                self._values["budget"] = budget
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def auto_refresh(self) -> typing.Optional[builtins.str]:
            '''Whether this individual budget parameter automatically refreshes when the budget period resets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-privacybudgettemplate-budgetparameter.html#cfn-cleanrooms-privacybudgettemplate-budgetparameter-autorefresh
            '''
            result = self._values.get("auto_refresh")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def budget(self) -> typing.Optional[jsii.Number]:
            '''The budget allocation amount for this specific parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-privacybudgettemplate-budgetparameter.html#cfn-cleanrooms-privacybudgettemplate-budgetparameter-budget
            '''
            result = self._values.get("budget")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of budget parameter being configured.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-privacybudgettemplate-budgetparameter.html#cfn-cleanrooms-privacybudgettemplate-budgetparameter-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BudgetParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanrooms.mixins.CfnPrivacyBudgetTemplatePropsMixin.ParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "budget_parameters": "budgetParameters",
            "epsilon": "epsilon",
            "resource_arn": "resourceArn",
            "users_noise_per_query": "usersNoisePerQuery",
        },
    )
    class ParametersProperty:
        def __init__(
            self,
            *,
            budget_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPrivacyBudgetTemplatePropsMixin.BudgetParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            epsilon: typing.Optional[jsii.Number] = None,
            resource_arn: typing.Optional[builtins.str] = None,
            users_noise_per_query: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the epsilon and noise parameters for the privacy budget template.

            :param budget_parameters: 
            :param epsilon: The epsilon value that you want to use.
            :param resource_arn: 
            :param users_noise_per_query: Noise added per query is measured in terms of the number of users whose contributions you want to obscure. This value governs the rate at which the privacy budget is depleted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-privacybudgettemplate-parameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanrooms import mixins as cleanrooms_mixins
                
                parameters_property = cleanrooms_mixins.CfnPrivacyBudgetTemplatePropsMixin.ParametersProperty(
                    budget_parameters=[cleanrooms_mixins.CfnPrivacyBudgetTemplatePropsMixin.BudgetParameterProperty(
                        auto_refresh="autoRefresh",
                        budget=123,
                        type="type"
                    )],
                    epsilon=123,
                    resource_arn="resourceArn",
                    users_noise_per_query=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__230ead0a52c62f9622badbb9f96cb4365ea39d07b7997ceb8ca995aa688d95e2)
                check_type(argname="argument budget_parameters", value=budget_parameters, expected_type=type_hints["budget_parameters"])
                check_type(argname="argument epsilon", value=epsilon, expected_type=type_hints["epsilon"])
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
                check_type(argname="argument users_noise_per_query", value=users_noise_per_query, expected_type=type_hints["users_noise_per_query"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if budget_parameters is not None:
                self._values["budget_parameters"] = budget_parameters
            if epsilon is not None:
                self._values["epsilon"] = epsilon
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn
            if users_noise_per_query is not None:
                self._values["users_noise_per_query"] = users_noise_per_query

        @builtins.property
        def budget_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrivacyBudgetTemplatePropsMixin.BudgetParameterProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-privacybudgettemplate-parameters.html#cfn-cleanrooms-privacybudgettemplate-parameters-budgetparameters
            '''
            result = self._values.get("budget_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrivacyBudgetTemplatePropsMixin.BudgetParameterProperty"]]]], result)

        @builtins.property
        def epsilon(self) -> typing.Optional[jsii.Number]:
            '''The epsilon value that you want to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-privacybudgettemplate-parameters.html#cfn-cleanrooms-privacybudgettemplate-parameters-epsilon
            '''
            result = self._values.get("epsilon")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-privacybudgettemplate-parameters.html#cfn-cleanrooms-privacybudgettemplate-parameters-resourcearn
            '''
            result = self._values.get("resource_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def users_noise_per_query(self) -> typing.Optional[jsii.Number]:
            '''Noise added per query is measured in terms of the number of users whose contributions you want to obscure.

            This value governs the rate at which the privacy budget is depleted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanrooms-privacybudgettemplate-parameters.html#cfn-cleanrooms-privacybudgettemplate-parameters-usersnoiseperquery
            '''
            result = self._values.get("users_noise_per_query")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAnalysisTemplateMixinProps",
    "CfnAnalysisTemplatePropsMixin",
    "CfnCollaborationMixinProps",
    "CfnCollaborationPropsMixin",
    "CfnConfiguredTableAssociationMixinProps",
    "CfnConfiguredTableAssociationPropsMixin",
    "CfnConfiguredTableMixinProps",
    "CfnConfiguredTablePropsMixin",
    "CfnIdMappingTableMixinProps",
    "CfnIdMappingTablePropsMixin",
    "CfnIdNamespaceAssociationMixinProps",
    "CfnIdNamespaceAssociationPropsMixin",
    "CfnMembershipAnalysisLogs",
    "CfnMembershipLogsMixin",
    "CfnMembershipMixinProps",
    "CfnMembershipPropsMixin",
    "CfnPrivacyBudgetTemplateMixinProps",
    "CfnPrivacyBudgetTemplatePropsMixin",
]

publication.publish()

def _typecheckingstub__ffa6818fd5f1b78ae6a1946f32c5bcee7e4bfb3765d06e907b2cccb420af30a0(
    *,
    analysis_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnalysisTemplatePropsMixin.AnalysisParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    error_message_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnalysisTemplatePropsMixin.ErrorMessageConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    format: typing.Optional[builtins.str] = None,
    membership_identifier: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnalysisTemplatePropsMixin.AnalysisSchemaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnalysisTemplatePropsMixin.AnalysisSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnalysisTemplatePropsMixin.AnalysisSourceMetadataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cbb17a01aa593fc132f37101caa9ac2e050c5e565d8386b52958c81fd08b7b0(
    props: typing.Union[CfnAnalysisTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec8c01644712bc30eb846b1c0f03c5031301146315323a74702fb778af6a063(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed42dedacb0000d9b7b016d92919dac513d9c901bac9d9af8b0a6dadaa73b38c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f48ec49c97796d97b0f4a192d51a4bff475d97119929c418ec1dfee6cd0cb365(
    *,
    default_value: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd1db4b4ba0a9b4913b54debef410a8d7b74d1a88898e46289083b1c2b2d3c9d(
    *,
    referenced_tables: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce037a7fbfad6fe600f72cbafd243bdabd78dd1e696f4bffdadd9f9a663c380f(
    *,
    artifacts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactMetadataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f862f76358195b0a64d660c53fd47681077d93da442909b3c0e89a530cd5dae(
    *,
    artifacts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f22573795ac7aa34b8f1a1853249d31cba864fcb256f4764f97b90027e7530ac(
    *,
    additional_artifact_hashes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnalysisTemplatePropsMixin.HashProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    entry_point_hash: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnalysisTemplatePropsMixin.HashProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a6d69e9122a36d12434b19f82e5608fa8c44727a903bb895c82c0e5af605fa2(
    *,
    location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnalysisTemplatePropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f5927493f9d2ed2c034725d174bddfafd3c03049d8f5bbe58ad53f96933cb30(
    *,
    additional_artifacts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    entry_point: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnalysisTemplatePropsMixin.AnalysisTemplateArtifactProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a27208d4dc7c4a50c728dc58c535f2bda6be35da06ce09ac787df26b43c7b5(
    *,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57cfd23b400b72b074451008debb5927303b44ce2fe336a1a4f67f9dbc94530d(
    *,
    sha256: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b9d13b4a7fdeff35d45b961e6d8a1931a8fae554f2030115d6b34c3a85858d9(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ea39ff5b61bad787c15e5b50ace1c380909aa708038178017c8f26a7032142f(
    *,
    allowed_result_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    analytics_engine: typing.Optional[builtins.str] = None,
    auto_approved_change_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    creator_display_name: typing.Optional[builtins.str] = None,
    creator_member_abilities: typing.Optional[typing.Sequence[builtins.str]] = None,
    creator_ml_member_abilities: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCollaborationPropsMixin.MLMemberAbilitiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    creator_payment_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCollaborationPropsMixin.PaymentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    data_encryption_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCollaborationPropsMixin.DataEncryptionMetadataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    job_log_status: typing.Optional[builtins.str] = None,
    members: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCollaborationPropsMixin.MemberSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    query_log_status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b57a17350d6f93ff651031eac1b1841f452dd9cb466fa2c0cb3b5433a172993e(
    props: typing.Union[CfnCollaborationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__319b0642cf2d2d333e0e2f4ff0d4f6a772e15a9fe4d7fc8f00e3c5a826716901(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6f86f8826afca410ea44dd317102b0889e0ae208c345bc9a6dfae9ea3c417d3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b54e2181f6739fcc22c74be7ad2f5ee43eba6e831bdccbe0846c3dc9965f949f(
    *,
    allow_cleartext: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    allow_duplicates: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    allow_joins_on_columns_with_different_names: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    preserve_nulls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49216a932dabffabd427565f11aeadc7b854a7d8e76bf2667680eb917ea77b6a(
    *,
    is_responsible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c5eab10708d746f456ccf802dad8df554f316684af7a2dc78a602a51335c75e(
    *,
    custom_ml_member_abilities: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f13d3f0b6a5dfb7ff97dcf80b12c3c3610e0028ccdfc43954bd73d502e7d92(
    *,
    model_inference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCollaborationPropsMixin.ModelInferencePaymentConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    model_training: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCollaborationPropsMixin.ModelTrainingPaymentConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__777b0ec90fb933a78331aec5ae715cab44b79a34d70978b920cadbc03bb2cdb1(
    *,
    account_id: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    member_abilities: typing.Optional[typing.Sequence[builtins.str]] = None,
    ml_member_abilities: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCollaborationPropsMixin.MLMemberAbilitiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    payment_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCollaborationPropsMixin.PaymentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8edd55504c3bbd2ee7e5bd2d6d6e7fc991c3368944d7885e92bd07c9898b3f4f(
    *,
    is_responsible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5cc864fbf6b607d41efe78ecce5c0bae8f008116fbb21064dfa7d6592234aa3(
    *,
    is_responsible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f01c665e99303d0485d4dffc8b5d04bfe8b494e7eba4fa3b4d3972b801b5968(
    *,
    job_compute: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCollaborationPropsMixin.JobComputePaymentConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    machine_learning: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCollaborationPropsMixin.MLPaymentConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    query_compute: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCollaborationPropsMixin.QueryComputePaymentConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6fd78b987339570fad670459dbce32144b03581550ec9bff75fcc827539d5ff(
    *,
    is_responsible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1bc30b270d4a63c962839b563554f1a724a6555136bfbfba7ffa534d64a1ad6(
    *,
    configured_table_association_analysis_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    configured_table_identifier: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    membership_identifier: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ed15b8fc7deddff41af707ea802636f527da6a1ed3fecc2b03bf86ea1bfe35(
    props: typing.Union[CfnConfiguredTableAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58d70560304cc1e39da61c98fde12340d9156a941da6c4b1c6e0b7f5698fcd76(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70eefe73b141466e27d0f136735cc72dd936f871c4cd4faf3a65f7e34a51660d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a76d937b91da6d27c28e1aadd59e31fd4120d66c7c95b62f6df64f8b54d89c(
    *,
    allowed_additional_analyses: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_result_receivers: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__821e4e85fbee1ffe47b53ad675978f2c6adaadbe8c09223dc10c61d2d43294a9(
    *,
    allowed_additional_analyses: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_result_receivers: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d64aa56b88d2720f7c37c9b6abc83df0ed086623c2b7da4ebcf5264138452f7(
    *,
    allowed_additional_analyses: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_result_receivers: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee5f13a76045707f6f85790aba57f40fcebea341bc3e7c37ca09837ffe1b9116(
    *,
    v1: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRulePolicyV1Property, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1697dbe5f38950e949d73b88dc008adde5db7da555146058798496a9acf22e4(
    *,
    aggregation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleAggregationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleCustomProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRuleListProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec00ec22aff657cffa7ec698a79e595ef1b52fb8c075653631489cbdaf4f7d6c(
    *,
    policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfiguredTableAssociationPropsMixin.ConfiguredTableAssociationAnalysisRulePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1852f6b0d3833435831c19111ba32f71b4d109597ff72574828e2c9b4342baf1(
    *,
    allowed_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
    analysis_method: typing.Optional[builtins.str] = None,
    analysis_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfiguredTablePropsMixin.AnalysisRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    selected_analysis_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    table_reference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfiguredTablePropsMixin.TableReferenceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6de44d42968467aadb4969d3994a5e0e05c7ba2c8f1c1bac91908f19867be3c(
    props: typing.Union[CfnConfiguredTableMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fde4af36e3edfb4f8c5e37b93892f5092496df1ceb585834abcc428c8fdaa382(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1920728949b82dbf0b1a56c6c6508d51fcda66c87fc059490f56663480a8ee9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__278c64695256fb7f06543f75af9bf3d528fe9973dbf414dbd34acfd1b80498e8(
    *,
    column_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    function: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d2d9f5702176472d6e972b32efebdf4c1c03dfe4badd0a51b780e8e17c915a(
    *,
    column_name: typing.Optional[builtins.str] = None,
    minimum: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0d7112177d08bb8826720095d9066eb4b79351003477fa10037ace0903e21db(
    *,
    additional_analyses: typing.Optional[builtins.str] = None,
    aggregate_columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfiguredTablePropsMixin.AggregateColumnProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    allowed_join_operators: typing.Optional[typing.Sequence[builtins.str]] = None,
    dimension_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
    join_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
    join_required: typing.Optional[builtins.str] = None,
    output_constraints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfiguredTablePropsMixin.AggregationConstraintProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    scalar_functions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b71c56f2d626d2bf969f73e8cb4d748d8a4dc29bcfe21d1a6750135f31e283fe(
    *,
    additional_analyses: typing.Optional[builtins.str] = None,
    allowed_analyses: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_analysis_providers: typing.Optional[typing.Sequence[builtins.str]] = None,
    differential_privacy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfiguredTablePropsMixin.DifferentialPrivacyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    disallowed_output_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d224e637db14b34ba8303ca94ac159e9a80e200266c60ad06960eaa0ff46764(
    *,
    additional_analyses: typing.Optional[builtins.str] = None,
    allowed_join_operators: typing.Optional[typing.Sequence[builtins.str]] = None,
    join_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
    list_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c3b7be1a3c07bf5c4d7fbc882acb1f2c1b43641d175b7f3df1a85433b491b4(
    *,
    policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfiguredTablePropsMixin.ConfiguredTableAnalysisRulePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__896fcebd74ad584f30058e82d3ddf6ce82d554756d69a7aa17397f27dd8aa499(
    *,
    database_name: typing.Optional[builtins.str] = None,
    output_location: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
    work_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f5c05a8fa8165c3e794f2ef3873601e263f55c85373277e517eec03296466ec(
    *,
    v1: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfiguredTablePropsMixin.ConfiguredTableAnalysisRulePolicyV1Property, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a0184d092bc50b96521b708080e7023006564d3dccdc09de995d5d0d792d7f1(
    *,
    aggregation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfiguredTablePropsMixin.AnalysisRuleAggregationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfiguredTablePropsMixin.AnalysisRuleCustomProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfiguredTablePropsMixin.AnalysisRuleListProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__019cce3c28d9f2269527fc30aadf7e92f2fec0f2677682b0de125f77e33fcac0(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2838adb2288d10de8d24f5126c20a534ee3cef6796e1f4093fb2f017e319f5aa(
    *,
    columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfiguredTablePropsMixin.DifferentialPrivacyColumnProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33d78bb77dcca7a4b0105a2a76e1ea6b732d13c90ede52b2702edbb6a8d56a98(
    *,
    database_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58570f2da1b2fbd69f9fb10882b62d580cc17739149e24aaf65c119b285ee4de(
    *,
    account_identifier: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    schema_name: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
    table_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfiguredTablePropsMixin.SnowflakeTableSchemaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb6add7aca07bdcd3537db50d3bc294e395f9bd8c01c3fe29e06a1327b3545cf(
    *,
    v1: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfiguredTablePropsMixin.SnowflakeTableSchemaV1Property, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0a5ff88cac2b3baad86eef31f8f0600a882c22841d017293c23bca8e25a7c0(
    *,
    column_name: typing.Optional[builtins.str] = None,
    column_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__568f0fd57d92f6eb03485908a1b5179c636fe23773da32e9bc0a00a33437ea00(
    *,
    athena: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfiguredTablePropsMixin.AthenaTableReferenceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    glue: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfiguredTablePropsMixin.GlueTableReferenceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    snowflake: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfiguredTablePropsMixin.SnowflakeTableReferenceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16e8633b5fffb60472154302458843cf0f238c1f84e7e78db78ad7e1d7ed0a3(
    *,
    description: typing.Optional[builtins.str] = None,
    input_reference_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdMappingTablePropsMixin.IdMappingTableInputReferenceConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    membership_identifier: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7e83be1f4cf0d28e39081f102bcf027ef9a5c20d52d097f1ab01414a3963c93(
    props: typing.Union[CfnIdMappingTableMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__661443a722bbad9b59ae10c8faee898b22fb7db320b76afc1a27093a0f185088(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c48e6a7c609464c1f43b62433a41c06e94f575245ed7a3d6457523ba4d070f2c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a2cade96148ba4fa402d47e6e647bded6e1be7ab7f53ac0c92edb8c3055311b(
    *,
    input_reference_arn: typing.Optional[builtins.str] = None,
    manage_resource_policies: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ee5fc381d8f22739291fd8fa1647786829bf45bebf1ee7d2da9c2a662d9f8c0(
    *,
    id_mapping_table_input_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdMappingTablePropsMixin.IdMappingTableInputSourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb174d0740f9b4e77ec4765e8fc4c3db508b50141732b8e06872e3654a8422ea(
    *,
    id_namespace_association_id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceb46343d68e0576604f4a78e71ed5e3374cb417543472cb5f58cee0ebf00221(
    *,
    description: typing.Optional[builtins.str] = None,
    id_mapping_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdNamespaceAssociationPropsMixin.IdMappingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    input_reference_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdNamespaceAssociationPropsMixin.IdNamespaceAssociationInputReferenceConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    membership_identifier: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f6f2f64f9efa54a385dbe1f9c2df7350509e83f431a7957a76eddf5bd86148e(
    props: typing.Union[CfnIdNamespaceAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80987e59e3261460c8662490e25380be5a3ba44ad02860b733eb44a6d9173111(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0123604dae230849746ed9a05dfb3a5da24c895cb7882f5805a48c337af6dff3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081ade3703339bd624be6a082a4b9967601a0efa5bb53c2582345a1c827aa02c(
    *,
    allow_use_as_dimension_column: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a611a40d62f659c1f802c916d534b2992de816e4d224fd6b0bb1ede48eb2ad(
    *,
    input_reference_arn: typing.Optional[builtins.str] = None,
    manage_resource_policies: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1fe87c90ffd0ecd3c95ac20529bbcc5ee8fabcd34bdd113db50b41784990e3f(
    *,
    id_mapping_workflows_supported: typing.Optional[typing.Union[typing.Sequence[typing.Any], _aws_cdk_ceddda9d.IResolvable]] = None,
    id_namespace_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a99d254945ebe75f18b9c6744f79268100007fa03ea43d7bad4cea618cb6384(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__557fc0134db14836940c9ba6663a4598dd697247255719e23206d1a0888123e3(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__619e80545e76c81f022c51943009be042dbe34e05825d45de958fc877f31c23c(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07e6aa00347d026a01fba88516718e8bc1446c9932f86a585dd04d5c7e350e02(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b181bfeb4b4b6e45f5dd053a8e43a2de7b0038dc0a8295046d322124df1a2a51(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aacf87856fc439810adc28f10f9e54dd94e5e71bf3eaa0468bee0a5fc5b266d0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__733d1150d35b389246bbcee2eb6f1f9ce233b0fe8a52b76cab43df8727213a4c(
    *,
    collaboration_identifier: typing.Optional[builtins.str] = None,
    default_job_result_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMembershipPropsMixin.MembershipProtectedJobResultConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_result_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMembershipPropsMixin.MembershipProtectedQueryResultConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    job_log_status: typing.Optional[builtins.str] = None,
    payment_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMembershipPropsMixin.MembershipPaymentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    query_log_status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95e00d211a861d5590a23208702ded2e0c7821a09a8f6777058fd8f3f92a2aa2(
    props: typing.Union[CfnMembershipMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e203b593c6d790437a7ca7c786b1eb679bdaf8d0de979a73ec24ce31aa3f81c2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eecec1528d668a785f39f0bc3ff1e4bab0705212476972a7ab5ef5929c730b6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96f13b8e87c2c2e57b6884b793df4e37046f006c1ead2b0d25eebd4e4fba7029(
    *,
    is_responsible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8a4e2a3d52fa9945125e593d45b4528735676da08ff447a0dc8724a5681fabc(
    *,
    model_inference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMembershipPropsMixin.MembershipModelInferencePaymentConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    model_training: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMembershipPropsMixin.MembershipModelTrainingPaymentConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c44f66063d7194a49938e4f8ae099beb2de0912e9296a7260b5bdfffe23c6efa(
    *,
    is_responsible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15660588d3021ee15df3b1456a8052cfb14ff5fc82383048a3c17527b9d3240e(
    *,
    is_responsible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd537c19fd8126f3f78c665caf619ace4ab111371f2f74dda5e33ee9e06e6fd9(
    *,
    job_compute: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMembershipPropsMixin.MembershipJobComputePaymentConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    machine_learning: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMembershipPropsMixin.MembershipMLPaymentConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    query_compute: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMembershipPropsMixin.MembershipQueryComputePaymentConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7883a681c698f481835ce2608ba4091aa8e8c8bf9b03a6481d8b3947148aa47e(
    *,
    s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMembershipPropsMixin.ProtectedJobS3OutputConfigurationInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c2bf16f9ec3fdabd81e653cc284809b45f746aede382bf247ff1b845b0b327b(
    *,
    output_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMembershipPropsMixin.MembershipProtectedJobOutputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24ddbbcfe391cff98d0af563a1eb130e8ad41590bfceca06f3579a8d4d074109(
    *,
    s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMembershipPropsMixin.ProtectedQueryS3OutputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b90ab72d5ecfc8e44940125909ebeecca400f0685b39f8e9f18f8373b4e2f0e(
    *,
    output_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMembershipPropsMixin.MembershipProtectedQueryOutputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6b1718ad2e99476716752605057e9b17fe81870b4156750e4659edb630c159(
    *,
    is_responsible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6a92eed991e3e08998eb3383c76d6374281cfb102b984a97c768bfa1976e8c(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01e0c30135fbee9dc35e2927dc326b92960a54816262b3c282f1efb66a279b17(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key_prefix: typing.Optional[builtins.str] = None,
    result_format: typing.Optional[builtins.str] = None,
    single_file_output: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ecd5fabefb1d78a3558b3cb91a6815d6a586e510712682e42af1228c93d3e7(
    *,
    auto_refresh: typing.Optional[builtins.str] = None,
    membership_identifier: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPrivacyBudgetTemplatePropsMixin.ParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    privacy_budget_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffe2e44ad3945ed1233c7c0a781606a8e0e47c71a39f6dd0bd4dad60aba7e0dd(
    props: typing.Union[CfnPrivacyBudgetTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d16a0cf366e7c1bdee6d877c6f286c928c48d30c17743235d2e547b4051a72f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d742002c520de0f51b3a7100aadb77853b187107ec7dbc62b5300aa27d64b0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56fbc0dfe70bb57cea8d17f82fddcdc382f686140e52ab76f7bdd92bacd8d234(
    *,
    auto_refresh: typing.Optional[builtins.str] = None,
    budget: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__230ead0a52c62f9622badbb9f96cb4365ea39d07b7997ceb8ca995aa688d95e2(
    *,
    budget_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPrivacyBudgetTemplatePropsMixin.BudgetParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    epsilon: typing.Optional[jsii.Number] = None,
    resource_arn: typing.Optional[builtins.str] = None,
    users_noise_per_query: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
