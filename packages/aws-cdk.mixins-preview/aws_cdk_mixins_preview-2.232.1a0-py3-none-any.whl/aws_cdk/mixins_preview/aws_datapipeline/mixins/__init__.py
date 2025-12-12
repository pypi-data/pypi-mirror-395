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
    jsii_type="@aws-cdk/mixins-preview.aws_datapipeline.mixins.CfnPipelineMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "activate": "activate",
        "description": "description",
        "name": "name",
        "parameter_objects": "parameterObjects",
        "parameter_values": "parameterValues",
        "pipeline_objects": "pipelineObjects",
        "pipeline_tags": "pipelineTags",
    },
)
class CfnPipelineMixinProps:
    def __init__(
        self,
        *,
        activate: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        parameter_objects: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.ParameterObjectProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        parameter_values: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.ParameterValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        pipeline_objects: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.PipelineObjectProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        pipeline_tags: typing.Optional[typing.Sequence[typing.Union["CfnPipelinePropsMixin.PipelineTagProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPipelinePropsMixin.

        :param activate: Indicates whether to validate and start the pipeline or stop an active pipeline. By default, the value is set to ``true`` .
        :param description: A description of the pipeline.
        :param name: The name of the pipeline.
        :param parameter_objects: The parameter objects used with the pipeline.
        :param parameter_values: The parameter values used with the pipeline.
        :param pipeline_objects: The objects that define the pipeline. These objects overwrite the existing pipeline definition. Not all objects, fields, and values can be updated. For information about restrictions, see `Editing Your Pipeline <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-manage-pipeline-modify-console.html>`_ in the *AWS Data Pipeline Developer Guide* .
        :param pipeline_tags: A list of arbitrary tags (key-value pairs) to associate with the pipeline, which you can use to control permissions. For more information, see `Controlling Access to Pipelines and Resources <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-control-access.html>`_ in the *AWS Data Pipeline Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_datapipeline import mixins as datapipeline_mixins
            
            cfn_pipeline_mixin_props = datapipeline_mixins.CfnPipelineMixinProps(
                activate=False,
                description="description",
                name="name",
                parameter_objects=[datapipeline_mixins.CfnPipelinePropsMixin.ParameterObjectProperty(
                    attributes=[datapipeline_mixins.CfnPipelinePropsMixin.ParameterAttributeProperty(
                        key="key",
                        string_value="stringValue"
                    )],
                    id="id"
                )],
                parameter_values=[datapipeline_mixins.CfnPipelinePropsMixin.ParameterValueProperty(
                    id="id",
                    string_value="stringValue"
                )],
                pipeline_objects=[datapipeline_mixins.CfnPipelinePropsMixin.PipelineObjectProperty(
                    fields=[datapipeline_mixins.CfnPipelinePropsMixin.FieldProperty(
                        key="key",
                        ref_value="refValue",
                        string_value="stringValue"
                    )],
                    id="id",
                    name="name"
                )],
                pipeline_tags=[datapipeline_mixins.CfnPipelinePropsMixin.PipelineTagProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61b1f1b33d9a4c957537270e93e8c44e2819cc0eb8ba7bc6bee57a5c87e936a3)
            check_type(argname="argument activate", value=activate, expected_type=type_hints["activate"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parameter_objects", value=parameter_objects, expected_type=type_hints["parameter_objects"])
            check_type(argname="argument parameter_values", value=parameter_values, expected_type=type_hints["parameter_values"])
            check_type(argname="argument pipeline_objects", value=pipeline_objects, expected_type=type_hints["pipeline_objects"])
            check_type(argname="argument pipeline_tags", value=pipeline_tags, expected_type=type_hints["pipeline_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if activate is not None:
            self._values["activate"] = activate
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if parameter_objects is not None:
            self._values["parameter_objects"] = parameter_objects
        if parameter_values is not None:
            self._values["parameter_values"] = parameter_values
        if pipeline_objects is not None:
            self._values["pipeline_objects"] = pipeline_objects
        if pipeline_tags is not None:
            self._values["pipeline_tags"] = pipeline_tags

    @builtins.property
    def activate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether to validate and start the pipeline or stop an active pipeline.

        By default, the value is set to ``true`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-activate
        '''
        result = self._values.get("activate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the pipeline.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the pipeline.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_objects(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ParameterObjectProperty"]]]]:
        '''The parameter objects used with the pipeline.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-parameterobjects
        '''
        result = self._values.get("parameter_objects")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ParameterObjectProperty"]]]], result)

    @builtins.property
    def parameter_values(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ParameterValueProperty"]]]]:
        '''The parameter values used with the pipeline.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-parametervalues
        '''
        result = self._values.get("parameter_values")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ParameterValueProperty"]]]], result)

    @builtins.property
    def pipeline_objects(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.PipelineObjectProperty"]]]]:
        '''The objects that define the pipeline.

        These objects overwrite the existing pipeline definition. Not all objects, fields, and values can be updated. For information about restrictions, see `Editing Your Pipeline <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-manage-pipeline-modify-console.html>`_ in the *AWS Data Pipeline Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-pipelineobjects
        '''
        result = self._values.get("pipeline_objects")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.PipelineObjectProperty"]]]], result)

    @builtins.property
    def pipeline_tags(
        self,
    ) -> typing.Optional[typing.List["CfnPipelinePropsMixin.PipelineTagProperty"]]:
        '''A list of arbitrary tags (key-value pairs) to associate with the pipeline, which you can use to control permissions.

        For more information, see `Controlling Access to Pipelines and Resources <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-control-access.html>`_ in the *AWS Data Pipeline Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-pipelinetags
        '''
        result = self._values.get("pipeline_tags")
        return typing.cast(typing.Optional[typing.List["CfnPipelinePropsMixin.PipelineTagProperty"]], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_datapipeline.mixins.CfnPipelinePropsMixin",
):
    '''The AWS::DataPipeline::Pipeline resource specifies a data pipeline that you can use to automate the movement and transformation of data.

    .. epigraph::

       AWS Data Pipeline is no longer available to new customers. Existing customers of AWS Data Pipeline can continue to use the service as normal. `Learn more <https://docs.aws.amazon.com/big-data/migrate-workloads-from-aws-data-pipeline/>`_

    In each pipeline, you define pipeline objects, such as activities, schedules, data nodes, and resources.

    The ``AWS::DataPipeline::Pipeline`` resource adds tasks, schedules, and preconditions to the specified pipeline. You can use ``PutPipelineDefinition`` to populate a new pipeline.

    ``PutPipelineDefinition`` also validates the configuration as it adds it to the pipeline. Changes to the pipeline are saved unless one of the following validation errors exist in the pipeline.

    - An object is missing a name or identifier field.
    - A string or reference field is empty.
    - The number of objects in the pipeline exceeds the allowed maximum number of objects.
    - The pipeline is in a FINISHED state.

    Pipeline object definitions are passed to the `PutPipelineDefinition <https://docs.aws.amazon.com/datapipeline/latest/APIReference/API_PutPipelineDefinition.html>`_ action and returned by the `GetPipelineDefinition <https://docs.aws.amazon.com/datapipeline/latest/APIReference/API_GetPipelineDefinition.html>`_ action.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html
    :cloudformationResource: AWS::DataPipeline::Pipeline
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_datapipeline import mixins as datapipeline_mixins
        
        cfn_pipeline_props_mixin = datapipeline_mixins.CfnPipelinePropsMixin(datapipeline_mixins.CfnPipelineMixinProps(
            activate=False,
            description="description",
            name="name",
            parameter_objects=[datapipeline_mixins.CfnPipelinePropsMixin.ParameterObjectProperty(
                attributes=[datapipeline_mixins.CfnPipelinePropsMixin.ParameterAttributeProperty(
                    key="key",
                    string_value="stringValue"
                )],
                id="id"
            )],
            parameter_values=[datapipeline_mixins.CfnPipelinePropsMixin.ParameterValueProperty(
                id="id",
                string_value="stringValue"
            )],
            pipeline_objects=[datapipeline_mixins.CfnPipelinePropsMixin.PipelineObjectProperty(
                fields=[datapipeline_mixins.CfnPipelinePropsMixin.FieldProperty(
                    key="key",
                    ref_value="refValue",
                    string_value="stringValue"
                )],
                id="id",
                name="name"
            )],
            pipeline_tags=[datapipeline_mixins.CfnPipelinePropsMixin.PipelineTagProperty(
                key="key",
                value="value"
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
        '''Create a mixin to apply properties to ``AWS::DataPipeline::Pipeline``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef57e26f702aa98cec63b2be21ffbf5f3f8175a39141ac38105ba8049d14f6cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__98b6844ad8edd693feb715f53a68c7ab282a9ee4d736ae6d7bef659ad8c4586e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb930191198dafd20f3c6450da00c78c858459f26dc696cfddfeed06eb6ded5c)
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
        jsii_type="@aws-cdk/mixins-preview.aws_datapipeline.mixins.CfnPipelinePropsMixin.FieldProperty",
        jsii_struct_bases=[],
        name_mapping={
            "key": "key",
            "ref_value": "refValue",
            "string_value": "stringValue",
        },
    )
    class FieldProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            ref_value: typing.Optional[builtins.str] = None,
            string_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A key-value pair that describes a property of a ``PipelineObject`` .

            The value is specified as either a string value ( ``StringValue`` ) or a reference to another object ( ``RefValue`` ) but not as both. To view fields for a data pipeline object, see `Pipeline Object Reference <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-pipeline-objects.html>`_ in the *AWS Data Pipeline Developer Guide* .

            :param key: Specifies the name of a field for a particular object. To view valid values for a particular field, see `Pipeline Object Reference <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-pipeline-objects.html>`_ in the *AWS Data Pipeline Developer Guide* .
            :param ref_value: A field value that you specify as an identifier of another object in the same pipeline definition. .. epigraph:: You can specify the field value as either a string value ( ``StringValue`` ) or a reference to another object ( ``RefValue`` ), but not both. Required if the key that you are using requires it.
            :param string_value: A field value that you specify as a string. To view valid values for a particular field, see `Pipeline Object Reference <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-pipeline-objects.html>`_ in the *AWS Data Pipeline Developer Guide* . .. epigraph:: You can specify the field value as either a string value ( ``StringValue`` ) or a reference to another object ( ``RefValue`` ), but not both. Required if the key that you are using requires it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-field.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datapipeline import mixins as datapipeline_mixins
                
                field_property = datapipeline_mixins.CfnPipelinePropsMixin.FieldProperty(
                    key="key",
                    ref_value="refValue",
                    string_value="stringValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c1bba0a1fe295e2dd0a3f6f49eb53e7ddc86d002ccbfb3de7c71ac60fb7b0bbb)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument ref_value", value=ref_value, expected_type=type_hints["ref_value"])
                check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if ref_value is not None:
                self._values["ref_value"] = ref_value
            if string_value is not None:
                self._values["string_value"] = string_value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''Specifies the name of a field for a particular object.

            To view valid values for a particular field, see `Pipeline Object Reference <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-pipeline-objects.html>`_ in the *AWS Data Pipeline Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-field.html#cfn-datapipeline-pipeline-field-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ref_value(self) -> typing.Optional[builtins.str]:
            '''A field value that you specify as an identifier of another object in the same pipeline definition.

            .. epigraph::

               You can specify the field value as either a string value ( ``StringValue`` ) or a reference to another object ( ``RefValue`` ), but not both.

            Required if the key that you are using requires it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-field.html#cfn-datapipeline-pipeline-field-refvalue
            '''
            result = self._values.get("ref_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def string_value(self) -> typing.Optional[builtins.str]:
            '''A field value that you specify as a string.

            To view valid values for a particular field, see `Pipeline Object Reference <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-pipeline-objects.html>`_ in the *AWS Data Pipeline Developer Guide* .
            .. epigraph::

               You can specify the field value as either a string value ( ``StringValue`` ) or a reference to another object ( ``RefValue`` ), but not both.

            Required if the key that you are using requires it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-field.html#cfn-datapipeline-pipeline-field-stringvalue
            '''
            result = self._values.get("string_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datapipeline.mixins.CfnPipelinePropsMixin.ParameterAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "string_value": "stringValue"},
    )
    class ParameterAttributeProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            string_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``Attribute`` is a property of ``ParameterObject`` that defines the attributes of a parameter object as key-value pairs.

            :param key: The field identifier.
            :param string_value: The field value, expressed as a String.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parameterattribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datapipeline import mixins as datapipeline_mixins
                
                parameter_attribute_property = datapipeline_mixins.CfnPipelinePropsMixin.ParameterAttributeProperty(
                    key="key",
                    string_value="stringValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__09ec006c2dbbd8ca3952b6335686f755b9fe44fcc5005bc60a509259818498ac)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if string_value is not None:
                self._values["string_value"] = string_value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The field identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parameterattribute.html#cfn-datapipeline-pipeline-parameterattribute-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def string_value(self) -> typing.Optional[builtins.str]:
            '''The field value, expressed as a String.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parameterattribute.html#cfn-datapipeline-pipeline-parameterattribute-stringvalue
            '''
            result = self._values.get("string_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datapipeline.mixins.CfnPipelinePropsMixin.ParameterObjectProperty",
        jsii_struct_bases=[],
        name_mapping={"attributes": "attributes", "id": "id"},
    )
    class ParameterObjectProperty:
        def __init__(
            self,
            *,
            attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.ParameterAttributeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about a parameter object.

            :param attributes: The attributes of the parameter object.
            :param id: The ID of the parameter object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parameterobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datapipeline import mixins as datapipeline_mixins
                
                parameter_object_property = datapipeline_mixins.CfnPipelinePropsMixin.ParameterObjectProperty(
                    attributes=[datapipeline_mixins.CfnPipelinePropsMixin.ParameterAttributeProperty(
                        key="key",
                        string_value="stringValue"
                    )],
                    id="id"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cc30b098c5fe944d3384d314b6e2a09cf08d8bfbe62a42a31e5655763a5d99f3)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if id is not None:
                self._values["id"] = id

        @builtins.property
        def attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ParameterAttributeProperty"]]]]:
            '''The attributes of the parameter object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parameterobject.html#cfn-datapipeline-pipeline-parameterobject-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ParameterAttributeProperty"]]]], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The ID of the parameter object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parameterobject.html#cfn-datapipeline-pipeline-parameterobject-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datapipeline.mixins.CfnPipelinePropsMixin.ParameterValueProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "string_value": "stringValue"},
    )
    class ParameterValueProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[builtins.str] = None,
            string_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A value or list of parameter values.

            :param id: The ID of the parameter value.
            :param string_value: The field value, expressed as a String.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parametervalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datapipeline import mixins as datapipeline_mixins
                
                parameter_value_property = datapipeline_mixins.CfnPipelinePropsMixin.ParameterValueProperty(
                    id="id",
                    string_value="stringValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__de3b0bc53f9299a4fa671b4389b271eebd159a5d75e4c23e6c8b5a32bafe8757)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if string_value is not None:
                self._values["string_value"] = string_value

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The ID of the parameter value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parametervalue.html#cfn-datapipeline-pipeline-parametervalue-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def string_value(self) -> typing.Optional[builtins.str]:
            '''The field value, expressed as a String.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parametervalue.html#cfn-datapipeline-pipeline-parametervalue-stringvalue
            '''
            result = self._values.get("string_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datapipeline.mixins.CfnPipelinePropsMixin.PipelineObjectProperty",
        jsii_struct_bases=[],
        name_mapping={"fields": "fields", "id": "id", "name": "name"},
    )
    class PipelineObjectProperty:
        def __init__(
            self,
            *,
            fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.FieldProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            id: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''PipelineObject is property of the AWS::DataPipeline::Pipeline resource that contains information about a pipeline object.

            This can be a logical, physical, or physical attempt pipeline object. The complete set of components of a pipeline defines the pipeline.

            :param fields: Key-value pairs that define the properties of the object.
            :param id: The ID of the object.
            :param name: The name of the object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelineobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datapipeline import mixins as datapipeline_mixins
                
                pipeline_object_property = datapipeline_mixins.CfnPipelinePropsMixin.PipelineObjectProperty(
                    fields=[datapipeline_mixins.CfnPipelinePropsMixin.FieldProperty(
                        key="key",
                        ref_value="refValue",
                        string_value="stringValue"
                    )],
                    id="id",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c6efa8af8df998bef5372a7b603fa8ce6f380558cbe4913fdf7426698a5f2a63)
                check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if fields is not None:
                self._values["fields"] = fields
            if id is not None:
                self._values["id"] = id
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def fields(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.FieldProperty"]]]]:
            '''Key-value pairs that define the properties of the object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelineobject.html#cfn-datapipeline-pipeline-pipelineobject-fields
            '''
            result = self._values.get("fields")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.FieldProperty"]]]], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The ID of the object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelineobject.html#cfn-datapipeline-pipeline-pipelineobject-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelineobject.html#cfn-datapipeline-pipeline-pipelineobject-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipelineObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_datapipeline.mixins.CfnPipelinePropsMixin.PipelineTagProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class PipelineTagProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A list of arbitrary tags (key-value pairs) to associate with the pipeline, which you can use to control permissions.

            For more information, see `Controlling Access to Pipelines and Resources <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-control-access.html>`_ in the *AWS Data Pipeline Developer Guide* .

            :param key: The key name of a tag.
            :param value: The value to associate with the key name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelinetag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_datapipeline import mixins as datapipeline_mixins
                
                pipeline_tag_property = datapipeline_mixins.CfnPipelinePropsMixin.PipelineTagProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b2c87fee464e7c269d267c36abbe18452fb59b095baaf8d87fd52d4d6157e9f4)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key name of a tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelinetag.html#cfn-datapipeline-pipeline-pipelinetag-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value to associate with the key name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelinetag.html#cfn-datapipeline-pipeline-pipelinetag-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipelineTagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnPipelineMixinProps",
    "CfnPipelinePropsMixin",
]

publication.publish()

def _typecheckingstub__61b1f1b33d9a4c957537270e93e8c44e2819cc0eb8ba7bc6bee57a5c87e936a3(
    *,
    activate: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    parameter_objects: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.ParameterObjectProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    parameter_values: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.ParameterValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    pipeline_objects: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.PipelineObjectProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    pipeline_tags: typing.Optional[typing.Sequence[typing.Union[CfnPipelinePropsMixin.PipelineTagProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef57e26f702aa98cec63b2be21ffbf5f3f8175a39141ac38105ba8049d14f6cf(
    props: typing.Union[CfnPipelineMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b6844ad8edd693feb715f53a68c7ab282a9ee4d736ae6d7bef659ad8c4586e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb930191198dafd20f3c6450da00c78c858459f26dc696cfddfeed06eb6ded5c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1bba0a1fe295e2dd0a3f6f49eb53e7ddc86d002ccbfb3de7c71ac60fb7b0bbb(
    *,
    key: typing.Optional[builtins.str] = None,
    ref_value: typing.Optional[builtins.str] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ec006c2dbbd8ca3952b6335686f755b9fe44fcc5005bc60a509259818498ac(
    *,
    key: typing.Optional[builtins.str] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc30b098c5fe944d3384d314b6e2a09cf08d8bfbe62a42a31e5655763a5d99f3(
    *,
    attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.ParameterAttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3b0bc53f9299a4fa671b4389b271eebd159a5d75e4c23e6c8b5a32bafe8757(
    *,
    id: typing.Optional[builtins.str] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6efa8af8df998bef5372a7b603fa8ce6f380558cbe4913fdf7426698a5f2a63(
    *,
    fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.FieldProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2c87fee464e7c269d267c36abbe18452fb59b095baaf8d87fd52d4d6157e9f4(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
