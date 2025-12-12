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
    jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnComponentTypeMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "component_type_id": "componentTypeId",
        "composite_component_types": "compositeComponentTypes",
        "description": "description",
        "extends_from": "extendsFrom",
        "functions": "functions",
        "is_singleton": "isSingleton",
        "property_definitions": "propertyDefinitions",
        "property_groups": "propertyGroups",
        "tags": "tags",
        "workspace_id": "workspaceId",
    },
)
class CfnComponentTypeMixinProps:
    def __init__(
        self,
        *,
        component_type_id: typing.Optional[builtins.str] = None,
        composite_component_types: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentTypePropsMixin.CompositeComponentTypeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        extends_from: typing.Optional[typing.Sequence[builtins.str]] = None,
        functions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentTypePropsMixin.FunctionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        is_singleton: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        property_definitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentTypePropsMixin.PropertyDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        property_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentTypePropsMixin.PropertyGroupProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        workspace_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnComponentTypePropsMixin.

        :param component_type_id: The ID of the component type.
        :param composite_component_types: Maps strings to ``compositeComponentTypes`` of the ``componentType`` . ``CompositeComponentType`` is referenced by ``componentTypeId`` .
        :param description: The description of the component type.
        :param extends_from: The name of the parent component type that this component type extends.
        :param functions: An object that maps strings to the functions in the component type. Each string in the mapping must be unique to this object. For information on the FunctionResponse object see the `FunctionResponse <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_FunctionResponse.html>`_ API reference.
        :param is_singleton: A boolean value that specifies whether an entity can have more than one component of this type.
        :param property_definitions: An object that maps strings to the property definitions in the component type. Each string in the mapping must be unique to this object. For information about the PropertyDefinitionResponse object, see the `PropertyDefinitionResponse <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_PropertyDefinitionResponse.html>`_ API reference.
        :param property_groups: An object that maps strings to the property groups in the component type. Each string in the mapping must be unique to this object.
        :param tags: The ComponentType tags.
        :param workspace_id: The ID of the workspace that contains the component type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
            
            # data_type_property_: iottwinmaker_mixins.CfnComponentTypePropsMixin.DataTypeProperty
            # data_value_property_: iottwinmaker_mixins.CfnComponentTypePropsMixin.DataValueProperty
            # relationship_value: Any
            
            cfn_component_type_mixin_props = iottwinmaker_mixins.CfnComponentTypeMixinProps(
                component_type_id="componentTypeId",
                composite_component_types={
                    "composite_component_types_key": iottwinmaker_mixins.CfnComponentTypePropsMixin.CompositeComponentTypeProperty(
                        component_type_id="componentTypeId"
                    )
                },
                description="description",
                extends_from=["extendsFrom"],
                functions={
                    "functions_key": iottwinmaker_mixins.CfnComponentTypePropsMixin.FunctionProperty(
                        implemented_by=iottwinmaker_mixins.CfnComponentTypePropsMixin.DataConnectorProperty(
                            is_native=False,
                            lambda_=iottwinmaker_mixins.CfnComponentTypePropsMixin.LambdaFunctionProperty(
                                arn="arn"
                            )
                        ),
                        required_properties=["requiredProperties"],
                        scope="scope"
                    )
                },
                is_singleton=False,
                property_definitions={
                    "property_definitions_key": iottwinmaker_mixins.CfnComponentTypePropsMixin.PropertyDefinitionProperty(
                        configurations={
                            "configurations_key": "configurations"
                        },
                        data_type=iottwinmaker_mixins.CfnComponentTypePropsMixin.DataTypeProperty(
                            allowed_values=[iottwinmaker_mixins.CfnComponentTypePropsMixin.DataValueProperty(
                                boolean_value=False,
                                double_value=123,
                                expression="expression",
                                integer_value=123,
                                list_value=[data_value_property_],
                                long_value=123,
                                map_value={
                                    "map_value_key": data_value_property_
                                },
                                relationship_value=relationship_value,
                                string_value="stringValue"
                            )],
                            nested_type=data_type_property_,
                            relationship=iottwinmaker_mixins.CfnComponentTypePropsMixin.RelationshipProperty(
                                relationship_type="relationshipType",
                                target_component_type_id="targetComponentTypeId"
                            ),
                            type="type",
                            unit_of_measure="unitOfMeasure"
                        ),
                        default_value=iottwinmaker_mixins.CfnComponentTypePropsMixin.DataValueProperty(
                            boolean_value=False,
                            double_value=123,
                            expression="expression",
                            integer_value=123,
                            list_value=[data_value_property_],
                            long_value=123,
                            map_value={
                                "map_value_key": data_value_property_
                            },
                            relationship_value=relationship_value,
                            string_value="stringValue"
                        ),
                        is_external_id=False,
                        is_required_in_entity=False,
                        is_stored_externally=False,
                        is_time_series=False
                    )
                },
                property_groups={
                    "property_groups_key": iottwinmaker_mixins.CfnComponentTypePropsMixin.PropertyGroupProperty(
                        group_type="groupType",
                        property_names=["propertyNames"]
                    )
                },
                tags={
                    "tags_key": "tags"
                },
                workspace_id="workspaceId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40cf621aff64f677362cf90c617745a2cd195866abfb458b4acc9bef4ab079fd)
            check_type(argname="argument component_type_id", value=component_type_id, expected_type=type_hints["component_type_id"])
            check_type(argname="argument composite_component_types", value=composite_component_types, expected_type=type_hints["composite_component_types"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument extends_from", value=extends_from, expected_type=type_hints["extends_from"])
            check_type(argname="argument functions", value=functions, expected_type=type_hints["functions"])
            check_type(argname="argument is_singleton", value=is_singleton, expected_type=type_hints["is_singleton"])
            check_type(argname="argument property_definitions", value=property_definitions, expected_type=type_hints["property_definitions"])
            check_type(argname="argument property_groups", value=property_groups, expected_type=type_hints["property_groups"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if component_type_id is not None:
            self._values["component_type_id"] = component_type_id
        if composite_component_types is not None:
            self._values["composite_component_types"] = composite_component_types
        if description is not None:
            self._values["description"] = description
        if extends_from is not None:
            self._values["extends_from"] = extends_from
        if functions is not None:
            self._values["functions"] = functions
        if is_singleton is not None:
            self._values["is_singleton"] = is_singleton
        if property_definitions is not None:
            self._values["property_definitions"] = property_definitions
        if property_groups is not None:
            self._values["property_groups"] = property_groups
        if tags is not None:
            self._values["tags"] = tags
        if workspace_id is not None:
            self._values["workspace_id"] = workspace_id

    @builtins.property
    def component_type_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the component type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-componenttypeid
        '''
        result = self._values.get("component_type_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def composite_component_types(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.CompositeComponentTypeProperty"]]]]:
        '''Maps strings to ``compositeComponentTypes`` of the ``componentType`` .

        ``CompositeComponentType`` is referenced by ``componentTypeId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-compositecomponenttypes
        '''
        result = self._values.get("composite_component_types")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.CompositeComponentTypeProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the component type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extends_from(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of the parent component type that this component type extends.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-extendsfrom
        '''
        result = self._values.get("extends_from")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def functions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.FunctionProperty"]]]]:
        '''An object that maps strings to the functions in the component type.

        Each string in the mapping must be unique to this object.

        For information on the FunctionResponse object see the `FunctionResponse <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_FunctionResponse.html>`_ API reference.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-functions
        '''
        result = self._values.get("functions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.FunctionProperty"]]]], result)

    @builtins.property
    def is_singleton(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A boolean value that specifies whether an entity can have more than one component of this type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-issingleton
        '''
        result = self._values.get("is_singleton")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def property_definitions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.PropertyDefinitionProperty"]]]]:
        '''An object that maps strings to the property definitions in the component type.

        Each string in the mapping must be unique to this object.

        For information about the PropertyDefinitionResponse object, see the `PropertyDefinitionResponse <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_PropertyDefinitionResponse.html>`_ API reference.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-propertydefinitions
        '''
        result = self._values.get("property_definitions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.PropertyDefinitionProperty"]]]], result)

    @builtins.property
    def property_groups(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.PropertyGroupProperty"]]]]:
        '''An object that maps strings to the property groups in the component type.

        Each string in the mapping must be unique to this object.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-propertygroups
        '''
        result = self._values.get("property_groups")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.PropertyGroupProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The ComponentType tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def workspace_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the workspace that contains the component type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-workspaceid
        '''
        result = self._values.get("workspace_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnComponentTypeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnComponentTypePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnComponentTypePropsMixin",
):
    '''Use the ``AWS::IoTTwinMaker::ComponentType`` resource to declare a component type.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html
    :cloudformationResource: AWS::IoTTwinMaker::ComponentType
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
        
        # data_type_property_: iottwinmaker_mixins.CfnComponentTypePropsMixin.DataTypeProperty
        # data_value_property_: iottwinmaker_mixins.CfnComponentTypePropsMixin.DataValueProperty
        # relationship_value: Any
        
        cfn_component_type_props_mixin = iottwinmaker_mixins.CfnComponentTypePropsMixin(iottwinmaker_mixins.CfnComponentTypeMixinProps(
            component_type_id="componentTypeId",
            composite_component_types={
                "composite_component_types_key": iottwinmaker_mixins.CfnComponentTypePropsMixin.CompositeComponentTypeProperty(
                    component_type_id="componentTypeId"
                )
            },
            description="description",
            extends_from=["extendsFrom"],
            functions={
                "functions_key": iottwinmaker_mixins.CfnComponentTypePropsMixin.FunctionProperty(
                    implemented_by=iottwinmaker_mixins.CfnComponentTypePropsMixin.DataConnectorProperty(
                        is_native=False,
                        lambda_=iottwinmaker_mixins.CfnComponentTypePropsMixin.LambdaFunctionProperty(
                            arn="arn"
                        )
                    ),
                    required_properties=["requiredProperties"],
                    scope="scope"
                )
            },
            is_singleton=False,
            property_definitions={
                "property_definitions_key": iottwinmaker_mixins.CfnComponentTypePropsMixin.PropertyDefinitionProperty(
                    configurations={
                        "configurations_key": "configurations"
                    },
                    data_type=iottwinmaker_mixins.CfnComponentTypePropsMixin.DataTypeProperty(
                        allowed_values=[iottwinmaker_mixins.CfnComponentTypePropsMixin.DataValueProperty(
                            boolean_value=False,
                            double_value=123,
                            expression="expression",
                            integer_value=123,
                            list_value=[data_value_property_],
                            long_value=123,
                            map_value={
                                "map_value_key": data_value_property_
                            },
                            relationship_value=relationship_value,
                            string_value="stringValue"
                        )],
                        nested_type=data_type_property_,
                        relationship=iottwinmaker_mixins.CfnComponentTypePropsMixin.RelationshipProperty(
                            relationship_type="relationshipType",
                            target_component_type_id="targetComponentTypeId"
                        ),
                        type="type",
                        unit_of_measure="unitOfMeasure"
                    ),
                    default_value=iottwinmaker_mixins.CfnComponentTypePropsMixin.DataValueProperty(
                        boolean_value=False,
                        double_value=123,
                        expression="expression",
                        integer_value=123,
                        list_value=[data_value_property_],
                        long_value=123,
                        map_value={
                            "map_value_key": data_value_property_
                        },
                        relationship_value=relationship_value,
                        string_value="stringValue"
                    ),
                    is_external_id=False,
                    is_required_in_entity=False,
                    is_stored_externally=False,
                    is_time_series=False
                )
            },
            property_groups={
                "property_groups_key": iottwinmaker_mixins.CfnComponentTypePropsMixin.PropertyGroupProperty(
                    group_type="groupType",
                    property_names=["propertyNames"]
                )
            },
            tags={
                "tags_key": "tags"
            },
            workspace_id="workspaceId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnComponentTypeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTTwinMaker::ComponentType``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d61605ac22eeba68baf8579784a3693027acd3632f72e2e94d8dd5fcce686526)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07f10444b09aa48e024f0ea28cdb8063372326ebed680e482d663776c4993c4f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5867a748a88d1093ca8c2b75bfe657229226cc9cb349edeb2a31c05deb97b6a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnComponentTypeMixinProps:
        return typing.cast(CfnComponentTypeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnComponentTypePropsMixin.CompositeComponentTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"component_type_id": "componentTypeId"},
    )
    class CompositeComponentTypeProperty:
        def __init__(
            self,
            *,
            component_type_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the ID of the composite component type.

            :param component_type_id: The ID of the component type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-compositecomponenttype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
                
                composite_component_type_property = iottwinmaker_mixins.CfnComponentTypePropsMixin.CompositeComponentTypeProperty(
                    component_type_id="componentTypeId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1860eeb093ed5fcb5daa7473457a3d237d38be2ab10c38fe195bb7004562133c)
                check_type(argname="argument component_type_id", value=component_type_id, expected_type=type_hints["component_type_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if component_type_id is not None:
                self._values["component_type_id"] = component_type_id

        @builtins.property
        def component_type_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the component type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-compositecomponenttype.html#cfn-iottwinmaker-componenttype-compositecomponenttype-componenttypeid
            '''
            result = self._values.get("component_type_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CompositeComponentTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnComponentTypePropsMixin.DataConnectorProperty",
        jsii_struct_bases=[],
        name_mapping={"is_native": "isNative", "lambda_": "lambda"},
    )
    class DataConnectorProperty:
        def __init__(
            self,
            *,
            is_native: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            lambda_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentTypePropsMixin.LambdaFunctionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The data connector.

            :param is_native: A boolean value that specifies whether the data connector is native to IoT TwinMaker.
            :param lambda_: The Lambda function associated with the data connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-dataconnector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
                
                data_connector_property = iottwinmaker_mixins.CfnComponentTypePropsMixin.DataConnectorProperty(
                    is_native=False,
                    lambda_=iottwinmaker_mixins.CfnComponentTypePropsMixin.LambdaFunctionProperty(
                        arn="arn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c22fd4d85a206643e2ea58d81aea4fe0d833edd2ce1dbae96e55ce069111cba)
                check_type(argname="argument is_native", value=is_native, expected_type=type_hints["is_native"])
                check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_native is not None:
                self._values["is_native"] = is_native
            if lambda_ is not None:
                self._values["lambda_"] = lambda_

        @builtins.property
        def is_native(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A boolean value that specifies whether the data connector is native to IoT TwinMaker.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-dataconnector.html#cfn-iottwinmaker-componenttype-dataconnector-isnative
            '''
            result = self._values.get("is_native")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def lambda_(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.LambdaFunctionProperty"]]:
            '''The Lambda function associated with the data connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-dataconnector.html#cfn-iottwinmaker-componenttype-dataconnector-lambda
            '''
            result = self._values.get("lambda_")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.LambdaFunctionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataConnectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnComponentTypePropsMixin.DataTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_values": "allowedValues",
            "nested_type": "nestedType",
            "relationship": "relationship",
            "type": "type",
            "unit_of_measure": "unitOfMeasure",
        },
    )
    class DataTypeProperty:
        def __init__(
            self,
            *,
            allowed_values: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentTypePropsMixin.DataValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            nested_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentTypePropsMixin.DataTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            relationship: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentTypePropsMixin.RelationshipProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
            unit_of_measure: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that specifies the data type of a property.

            :param allowed_values: The allowed values for this data type.
            :param nested_type: The nested type in the data type.
            :param relationship: A relationship that associates a component with another component.
            :param type: The underlying type of the data type. Valid Values: ``RELATIONSHIP | STRING | LONG | BOOLEAN | INTEGER | DOUBLE | LIST | MAP``
            :param unit_of_measure: The unit of measure used in this data type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datatype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
                
                # data_type_property_: iottwinmaker_mixins.CfnComponentTypePropsMixin.DataTypeProperty
                # data_value_property_: iottwinmaker_mixins.CfnComponentTypePropsMixin.DataValueProperty
                # relationship_value: Any
                
                data_type_property = iottwinmaker_mixins.CfnComponentTypePropsMixin.DataTypeProperty(
                    allowed_values=[iottwinmaker_mixins.CfnComponentTypePropsMixin.DataValueProperty(
                        boolean_value=False,
                        double_value=123,
                        expression="expression",
                        integer_value=123,
                        list_value=[data_value_property_],
                        long_value=123,
                        map_value={
                            "map_value_key": data_value_property_
                        },
                        relationship_value=relationship_value,
                        string_value="stringValue"
                    )],
                    nested_type=data_type_property_,
                    relationship=iottwinmaker_mixins.CfnComponentTypePropsMixin.RelationshipProperty(
                        relationship_type="relationshipType",
                        target_component_type_id="targetComponentTypeId"
                    ),
                    type="type",
                    unit_of_measure="unitOfMeasure"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b7bdac37fe97e04acae426b0c45809482d36adf05896a1ec6bf0f61cac4c1d20)
                check_type(argname="argument allowed_values", value=allowed_values, expected_type=type_hints["allowed_values"])
                check_type(argname="argument nested_type", value=nested_type, expected_type=type_hints["nested_type"])
                check_type(argname="argument relationship", value=relationship, expected_type=type_hints["relationship"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument unit_of_measure", value=unit_of_measure, expected_type=type_hints["unit_of_measure"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_values is not None:
                self._values["allowed_values"] = allowed_values
            if nested_type is not None:
                self._values["nested_type"] = nested_type
            if relationship is not None:
                self._values["relationship"] = relationship
            if type is not None:
                self._values["type"] = type
            if unit_of_measure is not None:
                self._values["unit_of_measure"] = unit_of_measure

        @builtins.property
        def allowed_values(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.DataValueProperty"]]]]:
            '''The allowed values for this data type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datatype.html#cfn-iottwinmaker-componenttype-datatype-allowedvalues
            '''
            result = self._values.get("allowed_values")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.DataValueProperty"]]]], result)

        @builtins.property
        def nested_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.DataTypeProperty"]]:
            '''The nested type in the data type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datatype.html#cfn-iottwinmaker-componenttype-datatype-nestedtype
            '''
            result = self._values.get("nested_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.DataTypeProperty"]], result)

        @builtins.property
        def relationship(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.RelationshipProperty"]]:
            '''A relationship that associates a component with another component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datatype.html#cfn-iottwinmaker-componenttype-datatype-relationship
            '''
            result = self._values.get("relationship")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.RelationshipProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The underlying type of the data type.

            Valid Values: ``RELATIONSHIP | STRING | LONG | BOOLEAN | INTEGER | DOUBLE | LIST | MAP``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datatype.html#cfn-iottwinmaker-componenttype-datatype-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unit_of_measure(self) -> typing.Optional[builtins.str]:
            '''The unit of measure used in this data type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datatype.html#cfn-iottwinmaker-componenttype-datatype-unitofmeasure
            '''
            result = self._values.get("unit_of_measure")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnComponentTypePropsMixin.DataValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "boolean_value": "booleanValue",
            "double_value": "doubleValue",
            "expression": "expression",
            "integer_value": "integerValue",
            "list_value": "listValue",
            "long_value": "longValue",
            "map_value": "mapValue",
            "relationship_value": "relationshipValue",
            "string_value": "stringValue",
        },
    )
    class DataValueProperty:
        def __init__(
            self,
            *,
            boolean_value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            double_value: typing.Optional[jsii.Number] = None,
            expression: typing.Optional[builtins.str] = None,
            integer_value: typing.Optional[jsii.Number] = None,
            list_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentTypePropsMixin.DataValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            long_value: typing.Optional[jsii.Number] = None,
            map_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentTypePropsMixin.DataValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            relationship_value: typing.Any = None,
            string_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that specifies a value for a property.

            :param boolean_value: A boolean value.
            :param double_value: A double value.
            :param expression: An expression that produces the value.
            :param integer_value: An integer value.
            :param list_value: A list of multiple values.
            :param long_value: A long value.
            :param map_value: An object that maps strings to multiple ``DataValue`` objects.
            :param relationship_value: A value that relates a component to another component.
            :param string_value: A string value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
                
                # data_value_property_: iottwinmaker_mixins.CfnComponentTypePropsMixin.DataValueProperty
                # relationship_value: Any
                
                data_value_property = iottwinmaker_mixins.CfnComponentTypePropsMixin.DataValueProperty(
                    boolean_value=False,
                    double_value=123,
                    expression="expression",
                    integer_value=123,
                    list_value=[data_value_property_],
                    long_value=123,
                    map_value={
                        "map_value_key": data_value_property_
                    },
                    relationship_value=relationship_value,
                    string_value="stringValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__50494670e6ff7caca443d9afb5ac6e71d47d63c769145028a6d7d016b15c87ae)
                check_type(argname="argument boolean_value", value=boolean_value, expected_type=type_hints["boolean_value"])
                check_type(argname="argument double_value", value=double_value, expected_type=type_hints["double_value"])
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument integer_value", value=integer_value, expected_type=type_hints["integer_value"])
                check_type(argname="argument list_value", value=list_value, expected_type=type_hints["list_value"])
                check_type(argname="argument long_value", value=long_value, expected_type=type_hints["long_value"])
                check_type(argname="argument map_value", value=map_value, expected_type=type_hints["map_value"])
                check_type(argname="argument relationship_value", value=relationship_value, expected_type=type_hints["relationship_value"])
                check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if boolean_value is not None:
                self._values["boolean_value"] = boolean_value
            if double_value is not None:
                self._values["double_value"] = double_value
            if expression is not None:
                self._values["expression"] = expression
            if integer_value is not None:
                self._values["integer_value"] = integer_value
            if list_value is not None:
                self._values["list_value"] = list_value
            if long_value is not None:
                self._values["long_value"] = long_value
            if map_value is not None:
                self._values["map_value"] = map_value
            if relationship_value is not None:
                self._values["relationship_value"] = relationship_value
            if string_value is not None:
                self._values["string_value"] = string_value

        @builtins.property
        def boolean_value(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A boolean value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-booleanvalue
            '''
            result = self._values.get("boolean_value")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def double_value(self) -> typing.Optional[jsii.Number]:
            '''A double value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-doublevalue
            '''
            result = self._values.get("double_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''An expression that produces the value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def integer_value(self) -> typing.Optional[jsii.Number]:
            '''An integer value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-integervalue
            '''
            result = self._values.get("integer_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def list_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.DataValueProperty"]]]]:
            '''A list of multiple values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-listvalue
            '''
            result = self._values.get("list_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.DataValueProperty"]]]], result)

        @builtins.property
        def long_value(self) -> typing.Optional[jsii.Number]:
            '''A long value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-longvalue
            '''
            result = self._values.get("long_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def map_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.DataValueProperty"]]]]:
            '''An object that maps strings to multiple ``DataValue`` objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-mapvalue
            '''
            result = self._values.get("map_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.DataValueProperty"]]]], result)

        @builtins.property
        def relationship_value(self) -> typing.Any:
            '''A value that relates a component to another component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-relationshipvalue
            '''
            result = self._values.get("relationship_value")
            return typing.cast(typing.Any, result)

        @builtins.property
        def string_value(self) -> typing.Optional[builtins.str]:
            '''A string value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-stringvalue
            '''
            result = self._values.get("string_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnComponentTypePropsMixin.ErrorProperty",
        jsii_struct_bases=[],
        name_mapping={"code": "code", "message": "message"},
    )
    class ErrorProperty:
        def __init__(
            self,
            *,
            code: typing.Optional[builtins.str] = None,
            message: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The component type error.

            :param code: The component type error code.
            :param message: The component type error message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-error.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
                
                error_property = iottwinmaker_mixins.CfnComponentTypePropsMixin.ErrorProperty(
                    code="code",
                    message="message"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eaac20dae8c4680b02d0ace0b7eac5570a345541d8f4abb34ce08b17f25137c2)
                check_type(argname="argument code", value=code, expected_type=type_hints["code"])
                check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code is not None:
                self._values["code"] = code
            if message is not None:
                self._values["message"] = message

        @builtins.property
        def code(self) -> typing.Optional[builtins.str]:
            '''The component type error code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-error.html#cfn-iottwinmaker-componenttype-error-code
            '''
            result = self._values.get("code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message(self) -> typing.Optional[builtins.str]:
            '''The component type error message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-error.html#cfn-iottwinmaker-componenttype-error-message
            '''
            result = self._values.get("message")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ErrorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnComponentTypePropsMixin.FunctionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "implemented_by": "implementedBy",
            "required_properties": "requiredProperties",
            "scope": "scope",
        },
    )
    class FunctionProperty:
        def __init__(
            self,
            *,
            implemented_by: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentTypePropsMixin.DataConnectorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            required_properties: typing.Optional[typing.Sequence[builtins.str]] = None,
            scope: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The function body.

            :param implemented_by: The data connector.
            :param required_properties: The required properties of the function.
            :param scope: The scope of the function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-function.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
                
                function_property = iottwinmaker_mixins.CfnComponentTypePropsMixin.FunctionProperty(
                    implemented_by=iottwinmaker_mixins.CfnComponentTypePropsMixin.DataConnectorProperty(
                        is_native=False,
                        lambda_=iottwinmaker_mixins.CfnComponentTypePropsMixin.LambdaFunctionProperty(
                            arn="arn"
                        )
                    ),
                    required_properties=["requiredProperties"],
                    scope="scope"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ee0641ac907890c747f153d56f95ec9f3e1f3bb6dc7794fc3336d3aa565cba25)
                check_type(argname="argument implemented_by", value=implemented_by, expected_type=type_hints["implemented_by"])
                check_type(argname="argument required_properties", value=required_properties, expected_type=type_hints["required_properties"])
                check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if implemented_by is not None:
                self._values["implemented_by"] = implemented_by
            if required_properties is not None:
                self._values["required_properties"] = required_properties
            if scope is not None:
                self._values["scope"] = scope

        @builtins.property
        def implemented_by(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.DataConnectorProperty"]]:
            '''The data connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-function.html#cfn-iottwinmaker-componenttype-function-implementedby
            '''
            result = self._values.get("implemented_by")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.DataConnectorProperty"]], result)

        @builtins.property
        def required_properties(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The required properties of the function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-function.html#cfn-iottwinmaker-componenttype-function-requiredproperties
            '''
            result = self._values.get("required_properties")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def scope(self) -> typing.Optional[builtins.str]:
            '''The scope of the function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-function.html#cfn-iottwinmaker-componenttype-function-scope
            '''
            result = self._values.get("scope")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnComponentTypePropsMixin.LambdaFunctionProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class LambdaFunctionProperty:
        def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
            '''The Lambda function.

            :param arn: The Lambda function ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-lambdafunction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
                
                lambda_function_property = iottwinmaker_mixins.CfnComponentTypePropsMixin.LambdaFunctionProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e62ebcd3615622d5e483b56db39573301980a60f1c263c83a6585137ee48c5cc)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The Lambda function ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-lambdafunction.html#cfn-iottwinmaker-componenttype-lambdafunction-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaFunctionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnComponentTypePropsMixin.PropertyDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "configurations": "configurations",
            "data_type": "dataType",
            "default_value": "defaultValue",
            "is_external_id": "isExternalId",
            "is_required_in_entity": "isRequiredInEntity",
            "is_stored_externally": "isStoredExternally",
            "is_time_series": "isTimeSeries",
        },
    )
    class PropertyDefinitionProperty:
        def __init__(
            self,
            *,
            configurations: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            data_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentTypePropsMixin.DataTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            default_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentTypePropsMixin.DataValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            is_external_id: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            is_required_in_entity: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            is_stored_externally: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            is_time_series: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''PropertyDefinition is an object that maps strings to the property definitions in the component type.

            :param configurations: A mapping that specifies configuration information about the property.
            :param data_type: An object that specifies the data type of a property.
            :param default_value: A boolean value that specifies whether the property ID comes from an external data store.
            :param is_external_id: A Boolean value that specifies whether the property ID comes from an external data source.
            :param is_required_in_entity: A boolean value that specifies whether the property is required in an entity.
            :param is_stored_externally: A boolean value that specifies whether the property is stored externally.
            :param is_time_series: A boolean value that specifies whether the property consists of time series data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
                
                # data_type_property_: iottwinmaker_mixins.CfnComponentTypePropsMixin.DataTypeProperty
                # data_value_property_: iottwinmaker_mixins.CfnComponentTypePropsMixin.DataValueProperty
                # relationship_value: Any
                
                property_definition_property = iottwinmaker_mixins.CfnComponentTypePropsMixin.PropertyDefinitionProperty(
                    configurations={
                        "configurations_key": "configurations"
                    },
                    data_type=iottwinmaker_mixins.CfnComponentTypePropsMixin.DataTypeProperty(
                        allowed_values=[iottwinmaker_mixins.CfnComponentTypePropsMixin.DataValueProperty(
                            boolean_value=False,
                            double_value=123,
                            expression="expression",
                            integer_value=123,
                            list_value=[data_value_property_],
                            long_value=123,
                            map_value={
                                "map_value_key": data_value_property_
                            },
                            relationship_value=relationship_value,
                            string_value="stringValue"
                        )],
                        nested_type=data_type_property_,
                        relationship=iottwinmaker_mixins.CfnComponentTypePropsMixin.RelationshipProperty(
                            relationship_type="relationshipType",
                            target_component_type_id="targetComponentTypeId"
                        ),
                        type="type",
                        unit_of_measure="unitOfMeasure"
                    ),
                    default_value=iottwinmaker_mixins.CfnComponentTypePropsMixin.DataValueProperty(
                        boolean_value=False,
                        double_value=123,
                        expression="expression",
                        integer_value=123,
                        list_value=[data_value_property_],
                        long_value=123,
                        map_value={
                            "map_value_key": data_value_property_
                        },
                        relationship_value=relationship_value,
                        string_value="stringValue"
                    ),
                    is_external_id=False,
                    is_required_in_entity=False,
                    is_stored_externally=False,
                    is_time_series=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__66a56337c5c93f4952288df19ebfb8d1374e9933a5118dd84a3cbed15c076bb9)
                check_type(argname="argument configurations", value=configurations, expected_type=type_hints["configurations"])
                check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument is_external_id", value=is_external_id, expected_type=type_hints["is_external_id"])
                check_type(argname="argument is_required_in_entity", value=is_required_in_entity, expected_type=type_hints["is_required_in_entity"])
                check_type(argname="argument is_stored_externally", value=is_stored_externally, expected_type=type_hints["is_stored_externally"])
                check_type(argname="argument is_time_series", value=is_time_series, expected_type=type_hints["is_time_series"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if configurations is not None:
                self._values["configurations"] = configurations
            if data_type is not None:
                self._values["data_type"] = data_type
            if default_value is not None:
                self._values["default_value"] = default_value
            if is_external_id is not None:
                self._values["is_external_id"] = is_external_id
            if is_required_in_entity is not None:
                self._values["is_required_in_entity"] = is_required_in_entity
            if is_stored_externally is not None:
                self._values["is_stored_externally"] = is_stored_externally
            if is_time_series is not None:
                self._values["is_time_series"] = is_time_series

        @builtins.property
        def configurations(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''A mapping that specifies configuration information about the property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-configurations
            '''
            result = self._values.get("configurations")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def data_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.DataTypeProperty"]]:
            '''An object that specifies the data type of a property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-datatype
            '''
            result = self._values.get("data_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.DataTypeProperty"]], result)

        @builtins.property
        def default_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.DataValueProperty"]]:
            '''A boolean value that specifies whether the property ID comes from an external data store.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.DataValueProperty"]], result)

        @builtins.property
        def is_external_id(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A Boolean value that specifies whether the property ID comes from an external data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-isexternalid
            '''
            result = self._values.get("is_external_id")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def is_required_in_entity(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A boolean value that specifies whether the property is required in an entity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-isrequiredinentity
            '''
            result = self._values.get("is_required_in_entity")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def is_stored_externally(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A boolean value that specifies whether the property is stored externally.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-isstoredexternally
            '''
            result = self._values.get("is_stored_externally")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def is_time_series(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A boolean value that specifies whether the property consists of time series data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-istimeseries
            '''
            result = self._values.get("is_time_series")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertyDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnComponentTypePropsMixin.PropertyGroupProperty",
        jsii_struct_bases=[],
        name_mapping={"group_type": "groupType", "property_names": "propertyNames"},
    )
    class PropertyGroupProperty:
        def __init__(
            self,
            *,
            group_type: typing.Optional[builtins.str] = None,
            property_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The property group.

            :param group_type: The group type.
            :param property_names: The property names.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertygroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
                
                property_group_property = iottwinmaker_mixins.CfnComponentTypePropsMixin.PropertyGroupProperty(
                    group_type="groupType",
                    property_names=["propertyNames"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f64d4bcf913352007b3d66b24536cc1aeeefddda7262d79dca21366955cf27e6)
                check_type(argname="argument group_type", value=group_type, expected_type=type_hints["group_type"])
                check_type(argname="argument property_names", value=property_names, expected_type=type_hints["property_names"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group_type is not None:
                self._values["group_type"] = group_type
            if property_names is not None:
                self._values["property_names"] = property_names

        @builtins.property
        def group_type(self) -> typing.Optional[builtins.str]:
            '''The group type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertygroup.html#cfn-iottwinmaker-componenttype-propertygroup-grouptype
            '''
            result = self._values.get("group_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The property names.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertygroup.html#cfn-iottwinmaker-componenttype-propertygroup-propertynames
            '''
            result = self._values.get("property_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertyGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnComponentTypePropsMixin.RelationshipProperty",
        jsii_struct_bases=[],
        name_mapping={
            "relationship_type": "relationshipType",
            "target_component_type_id": "targetComponentTypeId",
        },
    )
    class RelationshipProperty:
        def __init__(
            self,
            *,
            relationship_type: typing.Optional[builtins.str] = None,
            target_component_type_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that specifies a relationship with another component type.

            :param relationship_type: The type of the relationship.
            :param target_component_type_id: The ID of the target component type associated with this relationship.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-relationship.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
                
                relationship_property = iottwinmaker_mixins.CfnComponentTypePropsMixin.RelationshipProperty(
                    relationship_type="relationshipType",
                    target_component_type_id="targetComponentTypeId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ae9dc91cc1c2086126b3d696abd4a0a48d5cc3a1cd7ca1c90d0b573e2cd261f3)
                check_type(argname="argument relationship_type", value=relationship_type, expected_type=type_hints["relationship_type"])
                check_type(argname="argument target_component_type_id", value=target_component_type_id, expected_type=type_hints["target_component_type_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if relationship_type is not None:
                self._values["relationship_type"] = relationship_type
            if target_component_type_id is not None:
                self._values["target_component_type_id"] = target_component_type_id

        @builtins.property
        def relationship_type(self) -> typing.Optional[builtins.str]:
            '''The type of the relationship.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-relationship.html#cfn-iottwinmaker-componenttype-relationship-relationshiptype
            '''
            result = self._values.get("relationship_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_component_type_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the target component type associated with this relationship.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-relationship.html#cfn-iottwinmaker-componenttype-relationship-targetcomponenttypeid
            '''
            result = self._values.get("target_component_type_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RelationshipProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnComponentTypePropsMixin.StatusProperty",
        jsii_struct_bases=[],
        name_mapping={"error": "error", "state": "state"},
    )
    class StatusProperty:
        def __init__(
            self,
            *,
            error: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentTypePropsMixin.ErrorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            state: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The component type status.

            :param error: The component type error.
            :param state: The component type status state.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-status.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
                
                status_property = iottwinmaker_mixins.CfnComponentTypePropsMixin.StatusProperty(
                    error=iottwinmaker_mixins.CfnComponentTypePropsMixin.ErrorProperty(
                        code="code",
                        message="message"
                    ),
                    state="state"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e1d24506a7cf4a9883b803f743688ee0aa984ab3e97d7594b344b7511462bf75)
                check_type(argname="argument error", value=error, expected_type=type_hints["error"])
                check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if error is not None:
                self._values["error"] = error
            if state is not None:
                self._values["state"] = state

        @builtins.property
        def error(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.ErrorProperty"]]:
            '''The component type error.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-status.html#cfn-iottwinmaker-componenttype-status-error
            '''
            result = self._values.get("error")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentTypePropsMixin.ErrorProperty"]], result)

        @builtins.property
        def state(self) -> typing.Optional[builtins.str]:
            '''The component type status state.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-status.html#cfn-iottwinmaker-componenttype-status-state
            '''
            result = self._values.get("state")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatusProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnEntityMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "components": "components",
        "composite_components": "compositeComponents",
        "description": "description",
        "entity_id": "entityId",
        "entity_name": "entityName",
        "parent_entity_id": "parentEntityId",
        "tags": "tags",
        "workspace_id": "workspaceId",
    },
)
class CfnEntityMixinProps:
    def __init__(
        self,
        *,
        components: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEntityPropsMixin.ComponentProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        composite_components: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEntityPropsMixin.CompositeComponentProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        entity_id: typing.Optional[builtins.str] = None,
        entity_name: typing.Optional[builtins.str] = None,
        parent_entity_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        workspace_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnEntityPropsMixin.

        :param components: An object that maps strings to the components in the entity. Each string in the mapping must be unique to this object. For information on the component object see the `component <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_ComponentResponse.html>`_ API reference.
        :param composite_components: Maps string to ``compositeComponent`` updates in the request. Each key of the map represents the ``componentPath`` of the ``compositeComponent`` .
        :param description: The description of the entity.
        :param entity_id: The ID of the entity.
        :param entity_name: The entity name.
        :param parent_entity_id: The ID of the parent entity.
        :param tags: Metadata that you can use to manage the entity.
        :param workspace_id: The ID of the workspace that contains the entity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
            
            # data_value_property_: iottwinmaker_mixins.CfnEntityPropsMixin.DataValueProperty
            # definition: Any
            # error: Any
            # relationship_value: Any
            
            cfn_entity_mixin_props = iottwinmaker_mixins.CfnEntityMixinProps(
                components={
                    "components_key": iottwinmaker_mixins.CfnEntityPropsMixin.ComponentProperty(
                        component_name="componentName",
                        component_type_id="componentTypeId",
                        defined_in="definedIn",
                        description="description",
                        properties={
                            "properties_key": iottwinmaker_mixins.CfnEntityPropsMixin.PropertyProperty(
                                definition=definition,
                                value=iottwinmaker_mixins.CfnEntityPropsMixin.DataValueProperty(
                                    boolean_value=False,
                                    double_value=123,
                                    expression="expression",
                                    integer_value=123,
                                    list_value=[data_value_property_],
                                    long_value=123,
                                    map_value={
                                        "map_value_key": data_value_property_
                                    },
                                    relationship_value=relationship_value,
                                    string_value="stringValue"
                                )
                            )
                        },
                        property_groups={
                            "property_groups_key": iottwinmaker_mixins.CfnEntityPropsMixin.PropertyGroupProperty(
                                group_type="groupType",
                                property_names=["propertyNames"]
                            )
                        },
                        status=iottwinmaker_mixins.CfnEntityPropsMixin.StatusProperty(
                            error=error,
                            state="state"
                        )
                    )
                },
                composite_components={
                    "composite_components_key": iottwinmaker_mixins.CfnEntityPropsMixin.CompositeComponentProperty(
                        component_name="componentName",
                        component_path="componentPath",
                        component_type_id="componentTypeId",
                        description="description",
                        properties={
                            "properties_key": iottwinmaker_mixins.CfnEntityPropsMixin.PropertyProperty(
                                definition=definition,
                                value=iottwinmaker_mixins.CfnEntityPropsMixin.DataValueProperty(
                                    boolean_value=False,
                                    double_value=123,
                                    expression="expression",
                                    integer_value=123,
                                    list_value=[data_value_property_],
                                    long_value=123,
                                    map_value={
                                        "map_value_key": data_value_property_
                                    },
                                    relationship_value=relationship_value,
                                    string_value="stringValue"
                                )
                            )
                        },
                        property_groups={
                            "property_groups_key": iottwinmaker_mixins.CfnEntityPropsMixin.PropertyGroupProperty(
                                group_type="groupType",
                                property_names=["propertyNames"]
                            )
                        },
                        status=iottwinmaker_mixins.CfnEntityPropsMixin.StatusProperty(
                            error=error,
                            state="state"
                        )
                    )
                },
                description="description",
                entity_id="entityId",
                entity_name="entityName",
                parent_entity_id="parentEntityId",
                tags={
                    "tags_key": "tags"
                },
                workspace_id="workspaceId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b209bbf87c03890930285bbd8849850348f52f2f29463f8d3b8cd4d5ab7ce7e2)
            check_type(argname="argument components", value=components, expected_type=type_hints["components"])
            check_type(argname="argument composite_components", value=composite_components, expected_type=type_hints["composite_components"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument entity_id", value=entity_id, expected_type=type_hints["entity_id"])
            check_type(argname="argument entity_name", value=entity_name, expected_type=type_hints["entity_name"])
            check_type(argname="argument parent_entity_id", value=parent_entity_id, expected_type=type_hints["parent_entity_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if components is not None:
            self._values["components"] = components
        if composite_components is not None:
            self._values["composite_components"] = composite_components
        if description is not None:
            self._values["description"] = description
        if entity_id is not None:
            self._values["entity_id"] = entity_id
        if entity_name is not None:
            self._values["entity_name"] = entity_name
        if parent_entity_id is not None:
            self._values["parent_entity_id"] = parent_entity_id
        if tags is not None:
            self._values["tags"] = tags
        if workspace_id is not None:
            self._values["workspace_id"] = workspace_id

    @builtins.property
    def components(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEntityPropsMixin.ComponentProperty"]]]]:
        '''An object that maps strings to the components in the entity.

        Each string in the mapping must be unique to this object.

        For information on the component object see the `component <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_ComponentResponse.html>`_ API reference.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-components
        '''
        result = self._values.get("components")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEntityPropsMixin.ComponentProperty"]]]], result)

    @builtins.property
    def composite_components(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEntityPropsMixin.CompositeComponentProperty"]]]]:
        '''Maps string to ``compositeComponent`` updates in the request.

        Each key of the map represents the ``componentPath`` of the ``compositeComponent`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-compositecomponents
        '''
        result = self._values.get("composite_components")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEntityPropsMixin.CompositeComponentProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the entity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entity_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the entity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-entityid
        '''
        result = self._values.get("entity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entity_name(self) -> typing.Optional[builtins.str]:
        '''The entity name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-entityname
        '''
        result = self._values.get("entity_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent_entity_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the parent entity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-parententityid
        '''
        result = self._values.get("parent_entity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata that you can use to manage the entity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def workspace_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the workspace that contains the entity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-workspaceid
        '''
        result = self._values.get("workspace_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEntityMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEntityPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnEntityPropsMixin",
):
    '''Use the ``AWS::IoTTwinMaker::Entity`` resource to declare an entity.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html
    :cloudformationResource: AWS::IoTTwinMaker::Entity
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
        
        # data_value_property_: iottwinmaker_mixins.CfnEntityPropsMixin.DataValueProperty
        # definition: Any
        # error: Any
        # relationship_value: Any
        
        cfn_entity_props_mixin = iottwinmaker_mixins.CfnEntityPropsMixin(iottwinmaker_mixins.CfnEntityMixinProps(
            components={
                "components_key": iottwinmaker_mixins.CfnEntityPropsMixin.ComponentProperty(
                    component_name="componentName",
                    component_type_id="componentTypeId",
                    defined_in="definedIn",
                    description="description",
                    properties={
                        "properties_key": iottwinmaker_mixins.CfnEntityPropsMixin.PropertyProperty(
                            definition=definition,
                            value=iottwinmaker_mixins.CfnEntityPropsMixin.DataValueProperty(
                                boolean_value=False,
                                double_value=123,
                                expression="expression",
                                integer_value=123,
                                list_value=[data_value_property_],
                                long_value=123,
                                map_value={
                                    "map_value_key": data_value_property_
                                },
                                relationship_value=relationship_value,
                                string_value="stringValue"
                            )
                        )
                    },
                    property_groups={
                        "property_groups_key": iottwinmaker_mixins.CfnEntityPropsMixin.PropertyGroupProperty(
                            group_type="groupType",
                            property_names=["propertyNames"]
                        )
                    },
                    status=iottwinmaker_mixins.CfnEntityPropsMixin.StatusProperty(
                        error=error,
                        state="state"
                    )
                )
            },
            composite_components={
                "composite_components_key": iottwinmaker_mixins.CfnEntityPropsMixin.CompositeComponentProperty(
                    component_name="componentName",
                    component_path="componentPath",
                    component_type_id="componentTypeId",
                    description="description",
                    properties={
                        "properties_key": iottwinmaker_mixins.CfnEntityPropsMixin.PropertyProperty(
                            definition=definition,
                            value=iottwinmaker_mixins.CfnEntityPropsMixin.DataValueProperty(
                                boolean_value=False,
                                double_value=123,
                                expression="expression",
                                integer_value=123,
                                list_value=[data_value_property_],
                                long_value=123,
                                map_value={
                                    "map_value_key": data_value_property_
                                },
                                relationship_value=relationship_value,
                                string_value="stringValue"
                            )
                        )
                    },
                    property_groups={
                        "property_groups_key": iottwinmaker_mixins.CfnEntityPropsMixin.PropertyGroupProperty(
                            group_type="groupType",
                            property_names=["propertyNames"]
                        )
                    },
                    status=iottwinmaker_mixins.CfnEntityPropsMixin.StatusProperty(
                        error=error,
                        state="state"
                    )
                )
            },
            description="description",
            entity_id="entityId",
            entity_name="entityName",
            parent_entity_id="parentEntityId",
            tags={
                "tags_key": "tags"
            },
            workspace_id="workspaceId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEntityMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTTwinMaker::Entity``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eea794667beddf96e64d9deda265ed9ec69715d2c64394517fe3e60c25dbeb45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3439f47527fe1f6fc7d9ffc11051b331c3cf4c185f629e02930587e424e91ec)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10976b7680efcf0195c5a96f15658629abfdd30bc4abfea5e35cf0a4f2536a4b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEntityMixinProps:
        return typing.cast(CfnEntityMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnEntityPropsMixin.ComponentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component_name": "componentName",
            "component_type_id": "componentTypeId",
            "defined_in": "definedIn",
            "description": "description",
            "properties": "properties",
            "property_groups": "propertyGroups",
            "status": "status",
        },
    )
    class ComponentProperty:
        def __init__(
            self,
            *,
            component_name: typing.Optional[builtins.str] = None,
            component_type_id: typing.Optional[builtins.str] = None,
            defined_in: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEntityPropsMixin.PropertyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            property_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEntityPropsMixin.PropertyGroupProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            status: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEntityPropsMixin.StatusProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The entity component.

            :param component_name: The name of the component.
            :param component_type_id: The ID of the component type.
            :param defined_in: The name of the property definition set in the request.
            :param description: The description of the component.
            :param properties: An object that maps strings to the properties to set in the component type. Each string in the mapping must be unique to this object.
            :param property_groups: An object that maps strings to the property groups in the component type. Each string in the mapping must be unique to this object.
            :param status: The status of the component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
                
                # data_value_property_: iottwinmaker_mixins.CfnEntityPropsMixin.DataValueProperty
                # definition: Any
                # error: Any
                # relationship_value: Any
                
                component_property = iottwinmaker_mixins.CfnEntityPropsMixin.ComponentProperty(
                    component_name="componentName",
                    component_type_id="componentTypeId",
                    defined_in="definedIn",
                    description="description",
                    properties={
                        "properties_key": iottwinmaker_mixins.CfnEntityPropsMixin.PropertyProperty(
                            definition=definition,
                            value=iottwinmaker_mixins.CfnEntityPropsMixin.DataValueProperty(
                                boolean_value=False,
                                double_value=123,
                                expression="expression",
                                integer_value=123,
                                list_value=[data_value_property_],
                                long_value=123,
                                map_value={
                                    "map_value_key": data_value_property_
                                },
                                relationship_value=relationship_value,
                                string_value="stringValue"
                            )
                        )
                    },
                    property_groups={
                        "property_groups_key": iottwinmaker_mixins.CfnEntityPropsMixin.PropertyGroupProperty(
                            group_type="groupType",
                            property_names=["propertyNames"]
                        )
                    },
                    status=iottwinmaker_mixins.CfnEntityPropsMixin.StatusProperty(
                        error=error,
                        state="state"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e99c6aaced1b2083709bd9c77e28a5a20e3ff97799e4a689ef6d54da17237d2d)
                check_type(argname="argument component_name", value=component_name, expected_type=type_hints["component_name"])
                check_type(argname="argument component_type_id", value=component_type_id, expected_type=type_hints["component_type_id"])
                check_type(argname="argument defined_in", value=defined_in, expected_type=type_hints["defined_in"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
                check_type(argname="argument property_groups", value=property_groups, expected_type=type_hints["property_groups"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if component_name is not None:
                self._values["component_name"] = component_name
            if component_type_id is not None:
                self._values["component_type_id"] = component_type_id
            if defined_in is not None:
                self._values["defined_in"] = defined_in
            if description is not None:
                self._values["description"] = description
            if properties is not None:
                self._values["properties"] = properties
            if property_groups is not None:
                self._values["property_groups"] = property_groups
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def component_name(self) -> typing.Optional[builtins.str]:
            '''The name of the component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html#cfn-iottwinmaker-entity-component-componentname
            '''
            result = self._values.get("component_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def component_type_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the component type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html#cfn-iottwinmaker-entity-component-componenttypeid
            '''
            result = self._values.get("component_type_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def defined_in(self) -> typing.Optional[builtins.str]:
            '''The name of the property definition set in the request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html#cfn-iottwinmaker-entity-component-definedin
            '''
            result = self._values.get("defined_in")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html#cfn-iottwinmaker-entity-component-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEntityPropsMixin.PropertyProperty"]]]]:
            '''An object that maps strings to the properties to set in the component type.

            Each string in the mapping must be unique to this object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html#cfn-iottwinmaker-entity-component-properties
            '''
            result = self._values.get("properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEntityPropsMixin.PropertyProperty"]]]], result)

        @builtins.property
        def property_groups(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEntityPropsMixin.PropertyGroupProperty"]]]]:
            '''An object that maps strings to the property groups in the component type.

            Each string in the mapping must be unique to this object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html#cfn-iottwinmaker-entity-component-propertygroups
            '''
            result = self._values.get("property_groups")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEntityPropsMixin.PropertyGroupProperty"]]]], result)

        @builtins.property
        def status(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEntityPropsMixin.StatusProperty"]]:
            '''The status of the component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html#cfn-iottwinmaker-entity-component-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEntityPropsMixin.StatusProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnEntityPropsMixin.CompositeComponentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component_name": "componentName",
            "component_path": "componentPath",
            "component_type_id": "componentTypeId",
            "description": "description",
            "properties": "properties",
            "property_groups": "propertyGroups",
            "status": "status",
        },
    )
    class CompositeComponentProperty:
        def __init__(
            self,
            *,
            component_name: typing.Optional[builtins.str] = None,
            component_path: typing.Optional[builtins.str] = None,
            component_type_id: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEntityPropsMixin.PropertyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            property_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEntityPropsMixin.PropertyGroupProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            status: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEntityPropsMixin.StatusProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about a composite component.

            :param component_name: The name of the component.
            :param component_path: The path to the composite component, starting from the top-level component.
            :param component_type_id: The ID of the composite component type.
            :param description: The description of the component type.
            :param properties: Map of strings to the properties in the component type. Each string in the mapping must be unique to this component.
            :param property_groups: The property groups.
            :param status: The current status of the composite component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-compositecomponent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
                
                # data_value_property_: iottwinmaker_mixins.CfnEntityPropsMixin.DataValueProperty
                # definition: Any
                # error: Any
                # relationship_value: Any
                
                composite_component_property = iottwinmaker_mixins.CfnEntityPropsMixin.CompositeComponentProperty(
                    component_name="componentName",
                    component_path="componentPath",
                    component_type_id="componentTypeId",
                    description="description",
                    properties={
                        "properties_key": iottwinmaker_mixins.CfnEntityPropsMixin.PropertyProperty(
                            definition=definition,
                            value=iottwinmaker_mixins.CfnEntityPropsMixin.DataValueProperty(
                                boolean_value=False,
                                double_value=123,
                                expression="expression",
                                integer_value=123,
                                list_value=[data_value_property_],
                                long_value=123,
                                map_value={
                                    "map_value_key": data_value_property_
                                },
                                relationship_value=relationship_value,
                                string_value="stringValue"
                            )
                        )
                    },
                    property_groups={
                        "property_groups_key": iottwinmaker_mixins.CfnEntityPropsMixin.PropertyGroupProperty(
                            group_type="groupType",
                            property_names=["propertyNames"]
                        )
                    },
                    status=iottwinmaker_mixins.CfnEntityPropsMixin.StatusProperty(
                        error=error,
                        state="state"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f2360924bf3723dfce159e069b9b75556c2f55c25cd128811402875314fc6b27)
                check_type(argname="argument component_name", value=component_name, expected_type=type_hints["component_name"])
                check_type(argname="argument component_path", value=component_path, expected_type=type_hints["component_path"])
                check_type(argname="argument component_type_id", value=component_type_id, expected_type=type_hints["component_type_id"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
                check_type(argname="argument property_groups", value=property_groups, expected_type=type_hints["property_groups"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if component_name is not None:
                self._values["component_name"] = component_name
            if component_path is not None:
                self._values["component_path"] = component_path
            if component_type_id is not None:
                self._values["component_type_id"] = component_type_id
            if description is not None:
                self._values["description"] = description
            if properties is not None:
                self._values["properties"] = properties
            if property_groups is not None:
                self._values["property_groups"] = property_groups
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def component_name(self) -> typing.Optional[builtins.str]:
            '''The name of the component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-compositecomponent.html#cfn-iottwinmaker-entity-compositecomponent-componentname
            '''
            result = self._values.get("component_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def component_path(self) -> typing.Optional[builtins.str]:
            '''The path to the composite component, starting from the top-level component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-compositecomponent.html#cfn-iottwinmaker-entity-compositecomponent-componentpath
            '''
            result = self._values.get("component_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def component_type_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the composite component type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-compositecomponent.html#cfn-iottwinmaker-entity-compositecomponent-componenttypeid
            '''
            result = self._values.get("component_type_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the component type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-compositecomponent.html#cfn-iottwinmaker-entity-compositecomponent-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEntityPropsMixin.PropertyProperty"]]]]:
            '''Map of strings to the properties in the component type.

            Each string in the mapping must be unique to this component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-compositecomponent.html#cfn-iottwinmaker-entity-compositecomponent-properties
            '''
            result = self._values.get("properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEntityPropsMixin.PropertyProperty"]]]], result)

        @builtins.property
        def property_groups(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEntityPropsMixin.PropertyGroupProperty"]]]]:
            '''The property groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-compositecomponent.html#cfn-iottwinmaker-entity-compositecomponent-propertygroups
            '''
            result = self._values.get("property_groups")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEntityPropsMixin.PropertyGroupProperty"]]]], result)

        @builtins.property
        def status(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEntityPropsMixin.StatusProperty"]]:
            '''The current status of the composite component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-compositecomponent.html#cfn-iottwinmaker-entity-compositecomponent-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEntityPropsMixin.StatusProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CompositeComponentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnEntityPropsMixin.DataValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "boolean_value": "booleanValue",
            "double_value": "doubleValue",
            "expression": "expression",
            "integer_value": "integerValue",
            "list_value": "listValue",
            "long_value": "longValue",
            "map_value": "mapValue",
            "relationship_value": "relationshipValue",
            "string_value": "stringValue",
        },
    )
    class DataValueProperty:
        def __init__(
            self,
            *,
            boolean_value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            double_value: typing.Optional[jsii.Number] = None,
            expression: typing.Optional[builtins.str] = None,
            integer_value: typing.Optional[jsii.Number] = None,
            list_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEntityPropsMixin.DataValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            long_value: typing.Optional[jsii.Number] = None,
            map_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEntityPropsMixin.DataValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            relationship_value: typing.Any = None,
            string_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that specifies a value for a property.

            :param boolean_value: A boolean value.
            :param double_value: A double value.
            :param expression: An expression that produces the value.
            :param integer_value: An integer value.
            :param list_value: A list of multiple values.
            :param long_value: A long value.
            :param map_value: An object that maps strings to multiple DataValue objects.
            :param relationship_value: A value that relates a component to another component.
            :param string_value: A string value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
                
                # data_value_property_: iottwinmaker_mixins.CfnEntityPropsMixin.DataValueProperty
                # relationship_value: Any
                
                data_value_property = iottwinmaker_mixins.CfnEntityPropsMixin.DataValueProperty(
                    boolean_value=False,
                    double_value=123,
                    expression="expression",
                    integer_value=123,
                    list_value=[data_value_property_],
                    long_value=123,
                    map_value={
                        "map_value_key": data_value_property_
                    },
                    relationship_value=relationship_value,
                    string_value="stringValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__65be1328df7681e870681b31454100013829bcb63394f359e09d3aa4785ee394)
                check_type(argname="argument boolean_value", value=boolean_value, expected_type=type_hints["boolean_value"])
                check_type(argname="argument double_value", value=double_value, expected_type=type_hints["double_value"])
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument integer_value", value=integer_value, expected_type=type_hints["integer_value"])
                check_type(argname="argument list_value", value=list_value, expected_type=type_hints["list_value"])
                check_type(argname="argument long_value", value=long_value, expected_type=type_hints["long_value"])
                check_type(argname="argument map_value", value=map_value, expected_type=type_hints["map_value"])
                check_type(argname="argument relationship_value", value=relationship_value, expected_type=type_hints["relationship_value"])
                check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if boolean_value is not None:
                self._values["boolean_value"] = boolean_value
            if double_value is not None:
                self._values["double_value"] = double_value
            if expression is not None:
                self._values["expression"] = expression
            if integer_value is not None:
                self._values["integer_value"] = integer_value
            if list_value is not None:
                self._values["list_value"] = list_value
            if long_value is not None:
                self._values["long_value"] = long_value
            if map_value is not None:
                self._values["map_value"] = map_value
            if relationship_value is not None:
                self._values["relationship_value"] = relationship_value
            if string_value is not None:
                self._values["string_value"] = string_value

        @builtins.property
        def boolean_value(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A boolean value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-booleanvalue
            '''
            result = self._values.get("boolean_value")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def double_value(self) -> typing.Optional[jsii.Number]:
            '''A double value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-doublevalue
            '''
            result = self._values.get("double_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''An expression that produces the value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def integer_value(self) -> typing.Optional[jsii.Number]:
            '''An integer value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-integervalue
            '''
            result = self._values.get("integer_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def list_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEntityPropsMixin.DataValueProperty"]]]]:
            '''A list of multiple values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-listvalue
            '''
            result = self._values.get("list_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEntityPropsMixin.DataValueProperty"]]]], result)

        @builtins.property
        def long_value(self) -> typing.Optional[jsii.Number]:
            '''A long value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-longvalue
            '''
            result = self._values.get("long_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def map_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEntityPropsMixin.DataValueProperty"]]]]:
            '''An object that maps strings to multiple DataValue objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-mapvalue
            '''
            result = self._values.get("map_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEntityPropsMixin.DataValueProperty"]]]], result)

        @builtins.property
        def relationship_value(self) -> typing.Any:
            '''A value that relates a component to another component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-relationshipvalue
            '''
            result = self._values.get("relationship_value")
            return typing.cast(typing.Any, result)

        @builtins.property
        def string_value(self) -> typing.Optional[builtins.str]:
            '''A string value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-stringvalue
            '''
            result = self._values.get("string_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnEntityPropsMixin.ErrorProperty",
        jsii_struct_bases=[],
        name_mapping={"code": "code", "message": "message"},
    )
    class ErrorProperty:
        def __init__(
            self,
            *,
            code: typing.Optional[builtins.str] = None,
            message: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The entity error.

            :param code: The entity error code.
            :param message: The entity error message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-error.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
                
                error_property = iottwinmaker_mixins.CfnEntityPropsMixin.ErrorProperty(
                    code="code",
                    message="message"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a02afd4bf3c57178045ab1dba42110ff67dd5ad564618d1a0ba8d7f28c6fb81c)
                check_type(argname="argument code", value=code, expected_type=type_hints["code"])
                check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code is not None:
                self._values["code"] = code
            if message is not None:
                self._values["message"] = message

        @builtins.property
        def code(self) -> typing.Optional[builtins.str]:
            '''The entity error code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-error.html#cfn-iottwinmaker-entity-error-code
            '''
            result = self._values.get("code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message(self) -> typing.Optional[builtins.str]:
            '''The entity error message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-error.html#cfn-iottwinmaker-entity-error-message
            '''
            result = self._values.get("message")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ErrorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnEntityPropsMixin.PropertyGroupProperty",
        jsii_struct_bases=[],
        name_mapping={"group_type": "groupType", "property_names": "propertyNames"},
    )
    class PropertyGroupProperty:
        def __init__(
            self,
            *,
            group_type: typing.Optional[builtins.str] = None,
            property_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The property group.

            :param group_type: The group type.
            :param property_names: The property names.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-propertygroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
                
                property_group_property = iottwinmaker_mixins.CfnEntityPropsMixin.PropertyGroupProperty(
                    group_type="groupType",
                    property_names=["propertyNames"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__336cbf5ff0dc2edc956a371a0cc5226161e3e7b8e7394517c74953593c49519e)
                check_type(argname="argument group_type", value=group_type, expected_type=type_hints["group_type"])
                check_type(argname="argument property_names", value=property_names, expected_type=type_hints["property_names"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group_type is not None:
                self._values["group_type"] = group_type
            if property_names is not None:
                self._values["property_names"] = property_names

        @builtins.property
        def group_type(self) -> typing.Optional[builtins.str]:
            '''The group type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-propertygroup.html#cfn-iottwinmaker-entity-propertygroup-grouptype
            '''
            result = self._values.get("group_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The property names.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-propertygroup.html#cfn-iottwinmaker-entity-propertygroup-propertynames
            '''
            result = self._values.get("property_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertyGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnEntityPropsMixin.PropertyProperty",
        jsii_struct_bases=[],
        name_mapping={"definition": "definition", "value": "value"},
    )
    class PropertyProperty:
        def __init__(
            self,
            *,
            definition: typing.Any = None,
            value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEntityPropsMixin.DataValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that sets information about a property.

            :param definition: An object that specifies information about a property.
            :param value: An object that contains information about a value for a time series property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-property.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
                
                # data_value_property_: iottwinmaker_mixins.CfnEntityPropsMixin.DataValueProperty
                # definition: Any
                # relationship_value: Any
                
                property_property = iottwinmaker_mixins.CfnEntityPropsMixin.PropertyProperty(
                    definition=definition,
                    value=iottwinmaker_mixins.CfnEntityPropsMixin.DataValueProperty(
                        boolean_value=False,
                        double_value=123,
                        expression="expression",
                        integer_value=123,
                        list_value=[data_value_property_],
                        long_value=123,
                        map_value={
                            "map_value_key": data_value_property_
                        },
                        relationship_value=relationship_value,
                        string_value="stringValue"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__41c6820c18da163b77ac4fd69b16ea2cbfae963977b9ded17ae103c80eee724b)
                check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if definition is not None:
                self._values["definition"] = definition
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def definition(self) -> typing.Any:
            '''An object that specifies information about a property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-property.html#cfn-iottwinmaker-entity-property-definition
            '''
            result = self._values.get("definition")
            return typing.cast(typing.Any, result)

        @builtins.property
        def value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEntityPropsMixin.DataValueProperty"]]:
            '''An object that contains information about a value for a time series property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-property.html#cfn-iottwinmaker-entity-property-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEntityPropsMixin.DataValueProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnEntityPropsMixin.StatusProperty",
        jsii_struct_bases=[],
        name_mapping={"error": "error", "state": "state"},
    )
    class StatusProperty:
        def __init__(
            self,
            *,
            error: typing.Any = None,
            state: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The current status of the entity.

            :param error: The error message.
            :param state: The current state of the entity, component, component type, or workspace. Valid Values: ``CREATING | UPDATING | DELETING | ACTIVE | ERROR``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-status.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
                
                # error: Any
                
                status_property = iottwinmaker_mixins.CfnEntityPropsMixin.StatusProperty(
                    error=error,
                    state="state"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__debaabc732c3e83acaa4bcad63ddd3378c20e1bbfdb931bf4283f349feba4bb7)
                check_type(argname="argument error", value=error, expected_type=type_hints["error"])
                check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if error is not None:
                self._values["error"] = error
            if state is not None:
                self._values["state"] = state

        @builtins.property
        def error(self) -> typing.Any:
            '''The error message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-status.html#cfn-iottwinmaker-entity-status-error
            '''
            result = self._values.get("error")
            return typing.cast(typing.Any, result)

        @builtins.property
        def state(self) -> typing.Optional[builtins.str]:
            '''The current state of the entity, component, component type, or workspace.

            Valid Values: ``CREATING | UPDATING | DELETING | ACTIVE | ERROR``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-status.html#cfn-iottwinmaker-entity-status-state
            '''
            result = self._values.get("state")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatusProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnSceneMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "capabilities": "capabilities",
        "content_location": "contentLocation",
        "description": "description",
        "scene_id": "sceneId",
        "scene_metadata": "sceneMetadata",
        "tags": "tags",
        "workspace_id": "workspaceId",
    },
)
class CfnSceneMixinProps:
    def __init__(
        self,
        *,
        capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        content_location: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        scene_id: typing.Optional[builtins.str] = None,
        scene_metadata: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        workspace_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnScenePropsMixin.

        :param capabilities: A list of capabilities that the scene uses to render.
        :param content_location: The relative path that specifies the location of the content definition file.
        :param description: The description of this scene.
        :param scene_id: The ID of the scene.
        :param scene_metadata: The scene metadata.
        :param tags: The ComponentType tags.
        :param workspace_id: The ID of the workspace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
            
            cfn_scene_mixin_props = iottwinmaker_mixins.CfnSceneMixinProps(
                capabilities=["capabilities"],
                content_location="contentLocation",
                description="description",
                scene_id="sceneId",
                scene_metadata={
                    "scene_metadata_key": "sceneMetadata"
                },
                tags={
                    "tags_key": "tags"
                },
                workspace_id="workspaceId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ea6e82f0df492573d7a655c700ce5a3af410541b1cb7e702c1b06d321bfa75)
            check_type(argname="argument capabilities", value=capabilities, expected_type=type_hints["capabilities"])
            check_type(argname="argument content_location", value=content_location, expected_type=type_hints["content_location"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument scene_id", value=scene_id, expected_type=type_hints["scene_id"])
            check_type(argname="argument scene_metadata", value=scene_metadata, expected_type=type_hints["scene_metadata"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if capabilities is not None:
            self._values["capabilities"] = capabilities
        if content_location is not None:
            self._values["content_location"] = content_location
        if description is not None:
            self._values["description"] = description
        if scene_id is not None:
            self._values["scene_id"] = scene_id
        if scene_metadata is not None:
            self._values["scene_metadata"] = scene_metadata
        if tags is not None:
            self._values["tags"] = tags
        if workspace_id is not None:
            self._values["workspace_id"] = workspace_id

    @builtins.property
    def capabilities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of capabilities that the scene uses to render.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-capabilities
        '''
        result = self._values.get("capabilities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def content_location(self) -> typing.Optional[builtins.str]:
        '''The relative path that specifies the location of the content definition file.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-contentlocation
        '''
        result = self._values.get("content_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of this scene.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scene_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the scene.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-sceneid
        '''
        result = self._values.get("scene_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scene_metadata(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''The scene metadata.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-scenemetadata
        '''
        result = self._values.get("scene_metadata")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The ComponentType tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def workspace_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the workspace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-workspaceid
        '''
        result = self._values.get("workspace_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSceneMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnScenePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnScenePropsMixin",
):
    '''Use the ``AWS::IoTTwinMaker::Scene`` resource to declare a scene.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html
    :cloudformationResource: AWS::IoTTwinMaker::Scene
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
        
        cfn_scene_props_mixin = iottwinmaker_mixins.CfnScenePropsMixin(iottwinmaker_mixins.CfnSceneMixinProps(
            capabilities=["capabilities"],
            content_location="contentLocation",
            description="description",
            scene_id="sceneId",
            scene_metadata={
                "scene_metadata_key": "sceneMetadata"
            },
            tags={
                "tags_key": "tags"
            },
            workspace_id="workspaceId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSceneMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTTwinMaker::Scene``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a345fd499a6f9bb06113a586f2174654969804688cf4c9fb109f34204b977273)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10e811c069b033d8a2296bcc75833196a79c2687334d1a6a0e01a19689d5f9fc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb9e3cb41a626893840f1af20c36ab31a1ac059f5a900b0f8f1c4695fdf645c1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSceneMixinProps:
        return typing.cast(CfnSceneMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnSyncJobMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "sync_role": "syncRole",
        "sync_source": "syncSource",
        "tags": "tags",
        "workspace_id": "workspaceId",
    },
)
class CfnSyncJobMixinProps:
    def __init__(
        self,
        *,
        sync_role: typing.Optional[builtins.str] = None,
        sync_source: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        workspace_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSyncJobPropsMixin.

        :param sync_role: The SyncJob IAM role. This IAM role is used by the sync job to read from the syncSource, and create, update or delete the corresponding resources.
        :param sync_source: The sync source. .. epigraph:: Currently the only supported syncSoucre is ``SITEWISE`` .
        :param tags: Metadata you can use to manage the SyncJob.
        :param workspace_id: The ID of the workspace that contains the sync job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
            
            cfn_sync_job_mixin_props = iottwinmaker_mixins.CfnSyncJobMixinProps(
                sync_role="syncRole",
                sync_source="syncSource",
                tags={
                    "tags_key": "tags"
                },
                workspace_id="workspaceId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f61a4afb533614b6801826098842680023a5d4a51b18b07747ad32cbfa523295)
            check_type(argname="argument sync_role", value=sync_role, expected_type=type_hints["sync_role"])
            check_type(argname="argument sync_source", value=sync_source, expected_type=type_hints["sync_source"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if sync_role is not None:
            self._values["sync_role"] = sync_role
        if sync_source is not None:
            self._values["sync_source"] = sync_source
        if tags is not None:
            self._values["tags"] = tags
        if workspace_id is not None:
            self._values["workspace_id"] = workspace_id

    @builtins.property
    def sync_role(self) -> typing.Optional[builtins.str]:
        '''The SyncJob IAM role.

        This IAM role is used by the sync job to read from the syncSource, and create, update or delete the corresponding resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html#cfn-iottwinmaker-syncjob-syncrole
        '''
        result = self._values.get("sync_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_source(self) -> typing.Optional[builtins.str]:
        '''The sync source.

        .. epigraph::

           Currently the only supported syncSoucre is ``SITEWISE`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html#cfn-iottwinmaker-syncjob-syncsource
        '''
        result = self._values.get("sync_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata you can use to manage the SyncJob.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html#cfn-iottwinmaker-syncjob-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def workspace_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the workspace that contains the sync job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html#cfn-iottwinmaker-syncjob-workspaceid
        '''
        result = self._values.get("workspace_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSyncJobMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSyncJobPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnSyncJobPropsMixin",
):
    '''The SyncJob.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html
    :cloudformationResource: AWS::IoTTwinMaker::SyncJob
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
        
        cfn_sync_job_props_mixin = iottwinmaker_mixins.CfnSyncJobPropsMixin(iottwinmaker_mixins.CfnSyncJobMixinProps(
            sync_role="syncRole",
            sync_source="syncSource",
            tags={
                "tags_key": "tags"
            },
            workspace_id="workspaceId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSyncJobMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTTwinMaker::SyncJob``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12404d596f334665b719346817270d8b1499e13587795df69f89b314b62001e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a50582e57afc45bedb579af267f75552326ae36d0e69e9fde50222ba7db31786)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22d42a9a6c6939576a73441124c70ab299a2e04c9d47a63b156565beed073e13)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSyncJobMixinProps:
        return typing.cast(CfnSyncJobMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnWorkspaceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "role": "role",
        "s3_location": "s3Location",
        "tags": "tags",
        "workspace_id": "workspaceId",
    },
)
class CfnWorkspaceMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        role: typing.Optional[builtins.str] = None,
        s3_location: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        workspace_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnWorkspacePropsMixin.

        :param description: The description of the workspace.
        :param role: The ARN of the execution role associated with the workspace.
        :param s3_location: The ARN of the S3 bucket where resources associated with the workspace are stored.
        :param tags: Metadata that you can use to manage the workspace.
        :param workspace_id: The ID of the workspace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
            
            cfn_workspace_mixin_props = iottwinmaker_mixins.CfnWorkspaceMixinProps(
                description="description",
                role="role",
                s3_location="s3Location",
                tags={
                    "tags_key": "tags"
                },
                workspace_id="workspaceId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6164bd9e21759f92a961b52c380cfe1c584ccc7bba9fa144e401d34de0b22d1b)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument s3_location", value=s3_location, expected_type=type_hints["s3_location"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if role is not None:
            self._values["role"] = role
        if s3_location is not None:
            self._values["s3_location"] = s3_location
        if tags is not None:
            self._values["tags"] = tags
        if workspace_id is not None:
            self._values["workspace_id"] = workspace_id

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the workspace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''The ARN of the execution role associated with the workspace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-role
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_location(self) -> typing.Optional[builtins.str]:
        '''The ARN of the S3 bucket where resources associated with the workspace are stored.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-s3location
        '''
        result = self._values.get("s3_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata that you can use to manage the workspace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def workspace_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the workspace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-workspaceid
        '''
        result = self._values.get("workspace_id")
        return typing.cast(typing.Optional[builtins.str], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_iottwinmaker.mixins.CfnWorkspacePropsMixin",
):
    '''Use the ``AWS::IoTTwinMaker::Workspace`` resource to declare a workspace.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html
    :cloudformationResource: AWS::IoTTwinMaker::Workspace
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iottwinmaker import mixins as iottwinmaker_mixins
        
        cfn_workspace_props_mixin = iottwinmaker_mixins.CfnWorkspacePropsMixin(iottwinmaker_mixins.CfnWorkspaceMixinProps(
            description="description",
            role="role",
            s3_location="s3Location",
            tags={
                "tags_key": "tags"
            },
            workspace_id="workspaceId"
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
        '''Create a mixin to apply properties to ``AWS::IoTTwinMaker::Workspace``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bdb732a83e7aae368caa68b4c44d91cef515daeeef4f9b12dfc6130ecfa9224)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d35a833e5f423fe0314a69caf1ccb03f28ef5dd3bc30d47e471f55243fccf749)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b99654cd7271ea3123343a75bfd7ee512da8a6e4f2388fbbe31c5e1e3d99e341)
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


__all__ = [
    "CfnComponentTypeMixinProps",
    "CfnComponentTypePropsMixin",
    "CfnEntityMixinProps",
    "CfnEntityPropsMixin",
    "CfnSceneMixinProps",
    "CfnScenePropsMixin",
    "CfnSyncJobMixinProps",
    "CfnSyncJobPropsMixin",
    "CfnWorkspaceMixinProps",
    "CfnWorkspacePropsMixin",
]

publication.publish()

def _typecheckingstub__40cf621aff64f677362cf90c617745a2cd195866abfb458b4acc9bef4ab079fd(
    *,
    component_type_id: typing.Optional[builtins.str] = None,
    composite_component_types: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentTypePropsMixin.CompositeComponentTypeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    extends_from: typing.Optional[typing.Sequence[builtins.str]] = None,
    functions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentTypePropsMixin.FunctionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    is_singleton: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    property_definitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentTypePropsMixin.PropertyDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    property_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentTypePropsMixin.PropertyGroupProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    workspace_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d61605ac22eeba68baf8579784a3693027acd3632f72e2e94d8dd5fcce686526(
    props: typing.Union[CfnComponentTypeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f10444b09aa48e024f0ea28cdb8063372326ebed680e482d663776c4993c4f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5867a748a88d1093ca8c2b75bfe657229226cc9cb349edeb2a31c05deb97b6a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1860eeb093ed5fcb5daa7473457a3d237d38be2ab10c38fe195bb7004562133c(
    *,
    component_type_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c22fd4d85a206643e2ea58d81aea4fe0d833edd2ce1dbae96e55ce069111cba(
    *,
    is_native: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    lambda_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentTypePropsMixin.LambdaFunctionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7bdac37fe97e04acae426b0c45809482d36adf05896a1ec6bf0f61cac4c1d20(
    *,
    allowed_values: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentTypePropsMixin.DataValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    nested_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentTypePropsMixin.DataTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    relationship: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentTypePropsMixin.RelationshipProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
    unit_of_measure: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50494670e6ff7caca443d9afb5ac6e71d47d63c769145028a6d7d016b15c87ae(
    *,
    boolean_value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    double_value: typing.Optional[jsii.Number] = None,
    expression: typing.Optional[builtins.str] = None,
    integer_value: typing.Optional[jsii.Number] = None,
    list_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentTypePropsMixin.DataValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    long_value: typing.Optional[jsii.Number] = None,
    map_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentTypePropsMixin.DataValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    relationship_value: typing.Any = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaac20dae8c4680b02d0ace0b7eac5570a345541d8f4abb34ce08b17f25137c2(
    *,
    code: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee0641ac907890c747f153d56f95ec9f3e1f3bb6dc7794fc3336d3aa565cba25(
    *,
    implemented_by: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentTypePropsMixin.DataConnectorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    required_properties: typing.Optional[typing.Sequence[builtins.str]] = None,
    scope: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e62ebcd3615622d5e483b56db39573301980a60f1c263c83a6585137ee48c5cc(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a56337c5c93f4952288df19ebfb8d1374e9933a5118dd84a3cbed15c076bb9(
    *,
    configurations: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    data_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentTypePropsMixin.DataTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentTypePropsMixin.DataValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    is_external_id: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    is_required_in_entity: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    is_stored_externally: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    is_time_series: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f64d4bcf913352007b3d66b24536cc1aeeefddda7262d79dca21366955cf27e6(
    *,
    group_type: typing.Optional[builtins.str] = None,
    property_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae9dc91cc1c2086126b3d696abd4a0a48d5cc3a1cd7ca1c90d0b573e2cd261f3(
    *,
    relationship_type: typing.Optional[builtins.str] = None,
    target_component_type_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d24506a7cf4a9883b803f743688ee0aa984ab3e97d7594b344b7511462bf75(
    *,
    error: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentTypePropsMixin.ErrorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b209bbf87c03890930285bbd8849850348f52f2f29463f8d3b8cd4d5ab7ce7e2(
    *,
    components: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEntityPropsMixin.ComponentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    composite_components: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEntityPropsMixin.CompositeComponentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    entity_id: typing.Optional[builtins.str] = None,
    entity_name: typing.Optional[builtins.str] = None,
    parent_entity_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    workspace_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea794667beddf96e64d9deda265ed9ec69715d2c64394517fe3e60c25dbeb45(
    props: typing.Union[CfnEntityMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3439f47527fe1f6fc7d9ffc11051b331c3cf4c185f629e02930587e424e91ec(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10976b7680efcf0195c5a96f15658629abfdd30bc4abfea5e35cf0a4f2536a4b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99c6aaced1b2083709bd9c77e28a5a20e3ff97799e4a689ef6d54da17237d2d(
    *,
    component_name: typing.Optional[builtins.str] = None,
    component_type_id: typing.Optional[builtins.str] = None,
    defined_in: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEntityPropsMixin.PropertyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    property_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEntityPropsMixin.PropertyGroupProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    status: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEntityPropsMixin.StatusProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2360924bf3723dfce159e069b9b75556c2f55c25cd128811402875314fc6b27(
    *,
    component_name: typing.Optional[builtins.str] = None,
    component_path: typing.Optional[builtins.str] = None,
    component_type_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEntityPropsMixin.PropertyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    property_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEntityPropsMixin.PropertyGroupProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    status: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEntityPropsMixin.StatusProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65be1328df7681e870681b31454100013829bcb63394f359e09d3aa4785ee394(
    *,
    boolean_value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    double_value: typing.Optional[jsii.Number] = None,
    expression: typing.Optional[builtins.str] = None,
    integer_value: typing.Optional[jsii.Number] = None,
    list_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEntityPropsMixin.DataValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    long_value: typing.Optional[jsii.Number] = None,
    map_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEntityPropsMixin.DataValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    relationship_value: typing.Any = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a02afd4bf3c57178045ab1dba42110ff67dd5ad564618d1a0ba8d7f28c6fb81c(
    *,
    code: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__336cbf5ff0dc2edc956a371a0cc5226161e3e7b8e7394517c74953593c49519e(
    *,
    group_type: typing.Optional[builtins.str] = None,
    property_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c6820c18da163b77ac4fd69b16ea2cbfae963977b9ded17ae103c80eee724b(
    *,
    definition: typing.Any = None,
    value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEntityPropsMixin.DataValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__debaabc732c3e83acaa4bcad63ddd3378c20e1bbfdb931bf4283f349feba4bb7(
    *,
    error: typing.Any = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ea6e82f0df492573d7a655c700ce5a3af410541b1cb7e702c1b06d321bfa75(
    *,
    capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
    content_location: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    scene_id: typing.Optional[builtins.str] = None,
    scene_metadata: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    workspace_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a345fd499a6f9bb06113a586f2174654969804688cf4c9fb109f34204b977273(
    props: typing.Union[CfnSceneMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e811c069b033d8a2296bcc75833196a79c2687334d1a6a0e01a19689d5f9fc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb9e3cb41a626893840f1af20c36ab31a1ac059f5a900b0f8f1c4695fdf645c1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f61a4afb533614b6801826098842680023a5d4a51b18b07747ad32cbfa523295(
    *,
    sync_role: typing.Optional[builtins.str] = None,
    sync_source: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    workspace_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12404d596f334665b719346817270d8b1499e13587795df69f89b314b62001e8(
    props: typing.Union[CfnSyncJobMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a50582e57afc45bedb579af267f75552326ae36d0e69e9fde50222ba7db31786(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22d42a9a6c6939576a73441124c70ab299a2e04c9d47a63b156565beed073e13(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6164bd9e21759f92a961b52c380cfe1c584ccc7bba9fa144e401d34de0b22d1b(
    *,
    description: typing.Optional[builtins.str] = None,
    role: typing.Optional[builtins.str] = None,
    s3_location: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    workspace_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bdb732a83e7aae368caa68b4c44d91cef515daeeef4f9b12dfc6130ecfa9224(
    props: typing.Union[CfnWorkspaceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d35a833e5f423fe0314a69caf1ccb03f28ef5dd3bc30d47e471f55243fccf749(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b99654cd7271ea3123343a75bfd7ee512da8a6e4f2388fbbe31c5e1e3d99e341(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
