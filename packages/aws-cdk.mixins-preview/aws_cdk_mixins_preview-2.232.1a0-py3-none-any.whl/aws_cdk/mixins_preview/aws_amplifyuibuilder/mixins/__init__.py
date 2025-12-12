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
    jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnComponentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_id": "appId",
        "binding_properties": "bindingProperties",
        "children": "children",
        "collection_properties": "collectionProperties",
        "component_type": "componentType",
        "environment_name": "environmentName",
        "events": "events",
        "name": "name",
        "overrides": "overrides",
        "properties": "properties",
        "schema_version": "schemaVersion",
        "source_id": "sourceId",
        "tags": "tags",
        "variants": "variants",
    },
)
class CfnComponentMixinProps:
    def __init__(
        self,
        *,
        app_id: typing.Optional[builtins.str] = None,
        binding_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ComponentBindingPropertiesValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        children: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ComponentChildProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        collection_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ComponentDataConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        component_type: typing.Optional[builtins.str] = None,
        environment_name: typing.Optional[builtins.str] = None,
        events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ComponentEventProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        overrides: typing.Any = None,
        properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        schema_version: typing.Optional[builtins.str] = None,
        source_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        variants: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ComponentVariantProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnComponentPropsMixin.

        :param app_id: The unique ID of the Amplify app associated with the component.
        :param binding_properties: The information to connect a component's properties to data at runtime. You can't specify ``tags`` as a valid property for ``bindingProperties`` .
        :param children: A list of the component's ``ComponentChild`` instances.
        :param collection_properties: The data binding configuration for the component's properties. Use this for a collection component. You can't specify ``tags`` as a valid property for ``collectionProperties`` .
        :param component_type: The type of the component. This can be an Amplify custom UI component or another custom component.
        :param environment_name: The name of the backend environment that is a part of the Amplify app.
        :param events: Describes the events that can be raised on the component. Use for the workflow feature in Amplify Studio that allows you to bind events and actions to components.
        :param name: The name of the component.
        :param overrides: Describes the component's properties that can be overriden in a customized instance of the component. You can't specify ``tags`` as a valid property for ``overrides`` .
        :param properties: Describes the component's properties. You can't specify ``tags`` as a valid property for ``properties`` .
        :param schema_version: The schema version of the component when it was imported.
        :param source_id: The unique ID of the component in its original source system, such as Figma.
        :param tags: One or more key-value pairs to use when tagging the component.
        :param variants: A list of the component's variants. A variant is a unique style configuration of a main component.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html
        :exampleMetadata: fixture=_generated

        Example::

            
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb0992d109d1306a672dcaf87b9d036aa9c294ae6dacf8237f97f70830f8b0ea)
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
            check_type(argname="argument binding_properties", value=binding_properties, expected_type=type_hints["binding_properties"])
            check_type(argname="argument children", value=children, expected_type=type_hints["children"])
            check_type(argname="argument collection_properties", value=collection_properties, expected_type=type_hints["collection_properties"])
            check_type(argname="argument component_type", value=component_type, expected_type=type_hints["component_type"])
            check_type(argname="argument environment_name", value=environment_name, expected_type=type_hints["environment_name"])
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument schema_version", value=schema_version, expected_type=type_hints["schema_version"])
            check_type(argname="argument source_id", value=source_id, expected_type=type_hints["source_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument variants", value=variants, expected_type=type_hints["variants"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if app_id is not None:
            self._values["app_id"] = app_id
        if binding_properties is not None:
            self._values["binding_properties"] = binding_properties
        if children is not None:
            self._values["children"] = children
        if collection_properties is not None:
            self._values["collection_properties"] = collection_properties
        if component_type is not None:
            self._values["component_type"] = component_type
        if environment_name is not None:
            self._values["environment_name"] = environment_name
        if events is not None:
            self._values["events"] = events
        if name is not None:
            self._values["name"] = name
        if overrides is not None:
            self._values["overrides"] = overrides
        if properties is not None:
            self._values["properties"] = properties
        if schema_version is not None:
            self._values["schema_version"] = schema_version
        if source_id is not None:
            self._values["source_id"] = source_id
        if tags is not None:
            self._values["tags"] = tags
        if variants is not None:
            self._values["variants"] = variants

    @builtins.property
    def app_id(self) -> typing.Optional[builtins.str]:
        '''The unique ID of the Amplify app associated with the component.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-appid
        '''
        result = self._values.get("app_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def binding_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentBindingPropertiesValueProperty"]]]]:
        '''The information to connect a component's properties to data at runtime.

        You can't specify ``tags`` as a valid property for ``bindingProperties`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-bindingproperties
        '''
        result = self._values.get("binding_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentBindingPropertiesValueProperty"]]]], result)

    @builtins.property
    def children(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentChildProperty"]]]]:
        '''A list of the component's ``ComponentChild`` instances.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-children
        '''
        result = self._values.get("children")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentChildProperty"]]]], result)

    @builtins.property
    def collection_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentDataConfigurationProperty"]]]]:
        '''The data binding configuration for the component's properties.

        Use this for a collection component. You can't specify ``tags`` as a valid property for ``collectionProperties`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-collectionproperties
        '''
        result = self._values.get("collection_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentDataConfigurationProperty"]]]], result)

    @builtins.property
    def component_type(self) -> typing.Optional[builtins.str]:
        '''The type of the component.

        This can be an Amplify custom UI component or another custom component.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-componenttype
        '''
        result = self._values.get("component_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_name(self) -> typing.Optional[builtins.str]:
        '''The name of the backend environment that is a part of the Amplify app.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-environmentname
        '''
        result = self._values.get("environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def events(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentEventProperty"]]]]:
        '''Describes the events that can be raised on the component.

        Use for the workflow feature in Amplify Studio that allows you to bind events and actions to components.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-events
        '''
        result = self._values.get("events")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentEventProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the component.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def overrides(self) -> typing.Any:
        '''Describes the component's properties that can be overriden in a customized instance of the component.

        You can't specify ``tags`` as a valid property for ``overrides`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-overrides
        '''
        result = self._values.get("overrides")
        return typing.cast(typing.Any, result)

    @builtins.property
    def properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]]]]:
        '''Describes the component's properties.

        You can't specify ``tags`` as a valid property for ``properties`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]]]], result)

    @builtins.property
    def schema_version(self) -> typing.Optional[builtins.str]:
        '''The schema version of the component when it was imported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-schemaversion
        '''
        result = self._values.get("schema_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_id(self) -> typing.Optional[builtins.str]:
        '''The unique ID of the component in its original source system, such as Figma.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-sourceid
        '''
        result = self._values.get("source_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''One or more key-value pairs to use when tagging the component.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def variants(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentVariantProperty"]]]]:
        '''A list of the component's variants.

        A variant is a unique style configuration of a main component.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-variants
        '''
        result = self._values.get("variants")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentVariantProperty"]]]], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnComponentPropsMixin",
):
    '''The AWS::AmplifyUIBuilder::Component resource specifies a component within an Amplify app.

    A component is a user interface (UI) element that you can customize. Use ``ComponentChild`` to configure an instance of a ``Component`` . A ``ComponentChild`` instance inherits the configuration of the main ``Component`` .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html
    :cloudformationResource: AWS::AmplifyUIBuilder::Component
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        
    '''

    def __init__(
        self,
        props: typing.Union[CfnComponentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AmplifyUIBuilder::Component``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76b10e835be1c61a1cb925c5ac2a98579c7f3f15aa1e127cbc2a6d779daecf78)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f06e5f860dfe448712fec8a92c9be65373de771cf832e44f14c2b56de4aa381f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68a333f46df9ad5ca01373d28ce44c2eccc12100e6cf4810ddae04cb1e8dadb8)
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
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnComponentPropsMixin.ActionParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "anchor": "anchor",
            "fields": "fields",
            "global_": "global",
            "id": "id",
            "model": "model",
            "state": "state",
            "target": "target",
            "type": "type",
            "url": "url",
        },
    )
    class ActionParametersProperty:
        def __init__(
            self,
            *,
            anchor: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            global_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            model: typing.Optional[builtins.str] = None,
            state: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.MutationActionSetStateParameterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            url: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Represents the event action configuration for an element of a ``Component`` or ``ComponentChild`` .

            Use for the workflow feature in Amplify Studio that allows you to bind events and actions to components. ``ActionParameters`` defines the action that is performed when an event occurs on the component.

            :param anchor: The HTML anchor link to the location to open. Specify this value for a navigation action.
            :param fields: A dictionary of key-value pairs mapping Amplify Studio properties to fields in a data model. Use when the action performs an operation on an Amplify DataStore model.
            :param global_: Specifies whether the user should be signed out globally. Specify this value for an auth sign out action.
            :param id: The unique ID of the component that the ``ActionParameters`` apply to.
            :param model: The name of the data model. Use when the action performs an operation on an Amplify DataStore model.
            :param state: A key-value pair that specifies the state property name and its initial value.
            :param target: The element within the same component to modify when the action occurs.
            :param type: The type of navigation action. Valid values are ``url`` and ``anchor`` . This value is required for a navigation action.
            :param url: The URL to the location to open. Specify this value for a navigation action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-actionparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                # component_property_property_: amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty
                
                action_parameters_property = amplifyuibuilder_mixins.CfnComponentPropsMixin.ActionParametersProperty(
                    anchor=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                            field="field",
                            property="property"
                        ),
                        bindings={
                            "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                element="element",
                                property="property"
                            )
                        },
                        collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                            field="field",
                            property="property"
                        ),
                        component_name="componentName",
                        concat=[component_property_property_],
                        condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                            else=component_property_property_,
                            field="field",
                            operand="operand",
                            operand_type="operandType",
                            operator="operator",
                            property="property",
                            then=component_property_property_
                        ),
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        property="property",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    ),
                    fields={
                        "fields_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                field="field",
                                property="property"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                field="field",
                                property="property"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        )
                    },
                    global=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                            field="field",
                            property="property"
                        ),
                        bindings={
                            "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                element="element",
                                property="property"
                            )
                        },
                        collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                            field="field",
                            property="property"
                        ),
                        component_name="componentName",
                        concat=[component_property_property_],
                        condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                            else=component_property_property_,
                            field="field",
                            operand="operand",
                            operand_type="operandType",
                            operator="operator",
                            property="property",
                            then=component_property_property_
                        ),
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        property="property",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    ),
                    id=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                            field="field",
                            property="property"
                        ),
                        bindings={
                            "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                element="element",
                                property="property"
                            )
                        },
                        collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                            field="field",
                            property="property"
                        ),
                        component_name="componentName",
                        concat=[component_property_property_],
                        condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                            else=component_property_property_,
                            field="field",
                            operand="operand",
                            operand_type="operandType",
                            operator="operator",
                            property="property",
                            then=component_property_property_
                        ),
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        property="property",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    ),
                    model="model",
                    state=amplifyuibuilder_mixins.CfnComponentPropsMixin.MutationActionSetStateParameterProperty(
                        component_name="componentName",
                        property="property",
                        set=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                field="field",
                                property="property"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                field="field",
                                property="property"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        )
                    ),
                    target=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                            field="field",
                            property="property"
                        ),
                        bindings={
                            "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                element="element",
                                property="property"
                            )
                        },
                        collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                            field="field",
                            property="property"
                        ),
                        component_name="componentName",
                        concat=[component_property_property_],
                        condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                            else=component_property_property_,
                            field="field",
                            operand="operand",
                            operand_type="operandType",
                            operator="operator",
                            property="property",
                            then=component_property_property_
                        ),
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        property="property",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    ),
                    type=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                            field="field",
                            property="property"
                        ),
                        bindings={
                            "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                element="element",
                                property="property"
                            )
                        },
                        collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                            field="field",
                            property="property"
                        ),
                        component_name="componentName",
                        concat=[component_property_property_],
                        condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                            else=component_property_property_,
                            field="field",
                            operand="operand",
                            operand_type="operandType",
                            operator="operator",
                            property="property",
                            then=component_property_property_
                        ),
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        property="property",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    ),
                    url=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                            field="field",
                            property="property"
                        ),
                        bindings={
                            "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                element="element",
                                property="property"
                            )
                        },
                        collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                            field="field",
                            property="property"
                        ),
                        component_name="componentName",
                        concat=[component_property_property_],
                        condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                            else=component_property_property_,
                            field="field",
                            operand="operand",
                            operand_type="operandType",
                            operator="operator",
                            property="property",
                            then=component_property_property_
                        ),
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        property="property",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d5f11c49c91638ca3b1da4850aa07f77af6422d8b757f6c07afef2554b23e3c4)
                check_type(argname="argument anchor", value=anchor, expected_type=type_hints["anchor"])
                check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
                check_type(argname="argument global_", value=global_, expected_type=type_hints["global_"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument model", value=model, expected_type=type_hints["model"])
                check_type(argname="argument state", value=state, expected_type=type_hints["state"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if anchor is not None:
                self._values["anchor"] = anchor
            if fields is not None:
                self._values["fields"] = fields
            if global_ is not None:
                self._values["global_"] = global_
            if id is not None:
                self._values["id"] = id
            if model is not None:
                self._values["model"] = model
            if state is not None:
                self._values["state"] = state
            if target is not None:
                self._values["target"] = target
            if type is not None:
                self._values["type"] = type
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def anchor(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]]:
            '''The HTML anchor link to the location to open.

            Specify this value for a navigation action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-actionparameters.html#cfn-amplifyuibuilder-component-actionparameters-anchor
            '''
            result = self._values.get("anchor")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]], result)

        @builtins.property
        def fields(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]]]]:
            '''A dictionary of key-value pairs mapping Amplify Studio properties to fields in a data model.

            Use when the action performs an operation on an Amplify DataStore model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-actionparameters.html#cfn-amplifyuibuilder-component-actionparameters-fields
            '''
            result = self._values.get("fields")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]]]], result)

        @builtins.property
        def global_(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]]:
            '''Specifies whether the user should be signed out globally.

            Specify this value for an auth sign out action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-actionparameters.html#cfn-amplifyuibuilder-component-actionparameters-global
            '''
            result = self._values.get("global_")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]], result)

        @builtins.property
        def id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]]:
            '''The unique ID of the component that the ``ActionParameters`` apply to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-actionparameters.html#cfn-amplifyuibuilder-component-actionparameters-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]], result)

        @builtins.property
        def model(self) -> typing.Optional[builtins.str]:
            '''The name of the data model.

            Use when the action performs an operation on an Amplify DataStore model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-actionparameters.html#cfn-amplifyuibuilder-component-actionparameters-model
            '''
            result = self._values.get("model")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def state(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.MutationActionSetStateParameterProperty"]]:
            '''A key-value pair that specifies the state property name and its initial value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-actionparameters.html#cfn-amplifyuibuilder-component-actionparameters-state
            '''
            result = self._values.get("state")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.MutationActionSetStateParameterProperty"]], result)

        @builtins.property
        def target(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]]:
            '''The element within the same component to modify when the action occurs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-actionparameters.html#cfn-amplifyuibuilder-component-actionparameters-target
            '''
            result = self._values.get("target")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]], result)

        @builtins.property
        def type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]]:
            '''The type of navigation action.

            Valid values are ``url`` and ``anchor`` . This value is required for a navigation action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-actionparameters.html#cfn-amplifyuibuilder-component-actionparameters-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]], result)

        @builtins.property
        def url(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]]:
            '''The URL to the location to open.

            Specify this value for a navigation action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-actionparameters.html#cfn-amplifyuibuilder-component-actionparameters-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnComponentPropsMixin.ComponentBindingPropertiesValuePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "default_value": "defaultValue",
            "field": "field",
            "key": "key",
            "model": "model",
            "predicates": "predicates",
            "slot_name": "slotName",
            "user_attribute": "userAttribute",
        },
    )
    class ComponentBindingPropertiesValuePropertiesProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            default_value: typing.Optional[builtins.str] = None,
            field: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
            model: typing.Optional[builtins.str] = None,
            predicates: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.PredicateProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            slot_name: typing.Optional[builtins.str] = None,
            user_attribute: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``ComponentBindingPropertiesValueProperties`` property specifies the data binding configuration for a specific property using data stored in AWS .

            For AWS connected properties, you can bind a property to data stored in an Amazon S3 bucket, an Amplify DataStore model or an authenticated user attribute.

            :param bucket: An Amazon S3 bucket.
            :param default_value: The default value to assign to the property.
            :param field: The field to bind the data to.
            :param key: The storage key for an Amazon S3 bucket.
            :param model: An Amplify DataStore model.
            :param predicates: A list of predicates for binding a component's properties to data.
            :param slot_name: The name of a component slot.
            :param user_attribute: An authenticated user attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                # predicate_property_: amplifyuibuilder_mixins.CfnComponentPropsMixin.PredicateProperty
                
                component_binding_properties_value_properties_property = amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentBindingPropertiesValuePropertiesProperty(
                    bucket="bucket",
                    default_value="defaultValue",
                    field="field",
                    key="key",
                    model="model",
                    predicates=[amplifyuibuilder_mixins.CfnComponentPropsMixin.PredicateProperty(
                        and=[predicate_property_],
                        field="field",
                        operand="operand",
                        operand_type="operandType",
                        operator="operator",
                        or=[predicate_property_]
                    )],
                    slot_name="slotName",
                    user_attribute="userAttribute"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9b48edb398bcce45e30c68f2e0c03078482e850efbacbfcec93d8278e9bf5dc1)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument field", value=field, expected_type=type_hints["field"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument model", value=model, expected_type=type_hints["model"])
                check_type(argname="argument predicates", value=predicates, expected_type=type_hints["predicates"])
                check_type(argname="argument slot_name", value=slot_name, expected_type=type_hints["slot_name"])
                check_type(argname="argument user_attribute", value=user_attribute, expected_type=type_hints["user_attribute"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if default_value is not None:
                self._values["default_value"] = default_value
            if field is not None:
                self._values["field"] = field
            if key is not None:
                self._values["key"] = key
            if model is not None:
                self._values["model"] = model
            if predicates is not None:
                self._values["predicates"] = predicates
            if slot_name is not None:
                self._values["slot_name"] = slot_name
            if user_attribute is not None:
                self._values["user_attribute"] = user_attribute

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''An Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalueproperties-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            '''The default value to assign to the property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalueproperties-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def field(self) -> typing.Optional[builtins.str]:
            '''The field to bind the data to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalueproperties-field
            '''
            result = self._values.get("field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The storage key for an Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalueproperties-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def model(self) -> typing.Optional[builtins.str]:
            '''An Amplify DataStore model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalueproperties-model
            '''
            result = self._values.get("model")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def predicates(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.PredicateProperty"]]]]:
            '''A list of predicates for binding a component's properties to data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalueproperties-predicates
            '''
            result = self._values.get("predicates")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.PredicateProperty"]]]], result)

        @builtins.property
        def slot_name(self) -> typing.Optional[builtins.str]:
            '''The name of a component slot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalueproperties-slotname
            '''
            result = self._values.get("slot_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_attribute(self) -> typing.Optional[builtins.str]:
            '''An authenticated user attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalueproperties-userattribute
            '''
            result = self._values.get("user_attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentBindingPropertiesValuePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnComponentPropsMixin.ComponentBindingPropertiesValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "binding_properties": "bindingProperties",
            "default_value": "defaultValue",
            "type": "type",
        },
    )
    class ComponentBindingPropertiesValueProperty:
        def __init__(
            self,
            *,
            binding_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ComponentBindingPropertiesValuePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            default_value: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``ComponentBindingPropertiesValue`` property specifies the data binding configuration for a component at runtime.

            You can use ``ComponentBindingPropertiesValue`` to add exposed properties to a component to allow different values to be entered when a component is reused in different places in an app.

            :param binding_properties: Describes the properties to customize with data at runtime.
            :param default_value: The default value of the property.
            :param type: The property type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                # predicate_property_: amplifyuibuilder_mixins.CfnComponentPropsMixin.PredicateProperty
                
                component_binding_properties_value_property = amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentBindingPropertiesValueProperty(
                    binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentBindingPropertiesValuePropertiesProperty(
                        bucket="bucket",
                        default_value="defaultValue",
                        field="field",
                        key="key",
                        model="model",
                        predicates=[amplifyuibuilder_mixins.CfnComponentPropsMixin.PredicateProperty(
                            and=[predicate_property_],
                            field="field",
                            operand="operand",
                            operand_type="operandType",
                            operator="operator",
                            or=[predicate_property_]
                        )],
                        slot_name="slotName",
                        user_attribute="userAttribute"
                    ),
                    default_value="defaultValue",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e41677d59bd5ee17f2ca9efc81445682eab9fa6996fdf3bb6360ce680189d7c8)
                check_type(argname="argument binding_properties", value=binding_properties, expected_type=type_hints["binding_properties"])
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if binding_properties is not None:
                self._values["binding_properties"] = binding_properties
            if default_value is not None:
                self._values["default_value"] = default_value
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def binding_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentBindingPropertiesValuePropertiesProperty"]]:
            '''Describes the properties to customize with data at runtime.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalue.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalue-bindingproperties
            '''
            result = self._values.get("binding_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentBindingPropertiesValuePropertiesProperty"]], result)

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            '''The default value of the property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalue.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalue-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The property type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalue.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalue-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentBindingPropertiesValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnComponentPropsMixin.ComponentChildProperty",
        jsii_struct_bases=[],
        name_mapping={
            "children": "children",
            "component_type": "componentType",
            "events": "events",
            "name": "name",
            "properties": "properties",
            "source_id": "sourceId",
        },
    )
    class ComponentChildProperty:
        def __init__(
            self,
            *,
            children: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ComponentChildProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            component_type: typing.Optional[builtins.str] = None,
            events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ComponentEventProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            name: typing.Optional[builtins.str] = None,
            properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            source_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``ComponentChild`` property specifies a nested UI configuration within a parent ``Component`` .

            :param children: The list of ``ComponentChild`` instances for this component.
            :param component_type: The type of the child component.
            :param events: Describes the events that can be raised on the child component. Use for the workflow feature in Amplify Studio that allows you to bind events and actions to components.
            :param name: The name of the child component.
            :param properties: Describes the properties of the child component. You can't specify ``tags`` as a valid property for ``properties`` .
            :param source_id: The unique ID of the child component in its original source system, such as Figma.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentchild.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                # component_child_property_: amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentChildProperty
                # component_property_property_: amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty
                
                component_child_property = amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentChildProperty(
                    children=[component_child_property_],
                    component_type="componentType",
                    events={
                        "events_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentEventProperty(
                            action="action",
                            binding_event="bindingEvent",
                            parameters=amplifyuibuilder_mixins.CfnComponentPropsMixin.ActionParametersProperty(
                                anchor=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                                    binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                        field="field",
                                        property="property"
                                    ),
                                    bindings={
                                        "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                            element="element",
                                            property="property"
                                        )
                                    },
                                    collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                        field="field",
                                        property="property"
                                    ),
                                    component_name="componentName",
                                    concat=[component_property_property_],
                                    condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                                        else=component_property_property_,
                                        field="field",
                                        operand="operand",
                                        operand_type="operandType",
                                        operator="operator",
                                        property="property",
                                        then=component_property_property_
                                    ),
                                    configured=False,
                                    default_value="defaultValue",
                                    event="event",
                                    imported_value="importedValue",
                                    model="model",
                                    property="property",
                                    type="type",
                                    user_attribute="userAttribute",
                                    value="value"
                                ),
                                fields={
                                    "fields_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                                        binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                            field="field",
                                            property="property"
                                        ),
                                        bindings={
                                            "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                                element="element",
                                                property="property"
                                            )
                                        },
                                        collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                            field="field",
                                            property="property"
                                        ),
                                        component_name="componentName",
                                        concat=[component_property_property_],
                                        condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                                            else=component_property_property_,
                                            field="field",
                                            operand="operand",
                                            operand_type="operandType",
                                            operator="operator",
                                            property="property",
                                            then=component_property_property_
                                        ),
                                        configured=False,
                                        default_value="defaultValue",
                                        event="event",
                                        imported_value="importedValue",
                                        model="model",
                                        property="property",
                                        type="type",
                                        user_attribute="userAttribute",
                                        value="value"
                                    )
                                },
                                global=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                                    binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                        field="field",
                                        property="property"
                                    ),
                                    bindings={
                                        "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                            element="element",
                                            property="property"
                                        )
                                    },
                                    collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                        field="field",
                                        property="property"
                                    ),
                                    component_name="componentName",
                                    concat=[component_property_property_],
                                    condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                                        else=component_property_property_,
                                        field="field",
                                        operand="operand",
                                        operand_type="operandType",
                                        operator="operator",
                                        property="property",
                                        then=component_property_property_
                                    ),
                                    configured=False,
                                    default_value="defaultValue",
                                    event="event",
                                    imported_value="importedValue",
                                    model="model",
                                    property="property",
                                    type="type",
                                    user_attribute="userAttribute",
                                    value="value"
                                ),
                                id=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                                    binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                        field="field",
                                        property="property"
                                    ),
                                    bindings={
                                        "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                            element="element",
                                            property="property"
                                        )
                                    },
                                    collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                        field="field",
                                        property="property"
                                    ),
                                    component_name="componentName",
                                    concat=[component_property_property_],
                                    condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                                        else=component_property_property_,
                                        field="field",
                                        operand="operand",
                                        operand_type="operandType",
                                        operator="operator",
                                        property="property",
                                        then=component_property_property_
                                    ),
                                    configured=False,
                                    default_value="defaultValue",
                                    event="event",
                                    imported_value="importedValue",
                                    model="model",
                                    property="property",
                                    type="type",
                                    user_attribute="userAttribute",
                                    value="value"
                                ),
                                model="model",
                                state=amplifyuibuilder_mixins.CfnComponentPropsMixin.MutationActionSetStateParameterProperty(
                                    component_name="componentName",
                                    property="property",
                                    set=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                                        binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                            field="field",
                                            property="property"
                                        ),
                                        bindings={
                                            "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                                element="element",
                                                property="property"
                                            )
                                        },
                                        collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                            field="field",
                                            property="property"
                                        ),
                                        component_name="componentName",
                                        concat=[component_property_property_],
                                        condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                                            else=component_property_property_,
                                            field="field",
                                            operand="operand",
                                            operand_type="operandType",
                                            operator="operator",
                                            property="property",
                                            then=component_property_property_
                                        ),
                                        configured=False,
                                        default_value="defaultValue",
                                        event="event",
                                        imported_value="importedValue",
                                        model="model",
                                        property="property",
                                        type="type",
                                        user_attribute="userAttribute",
                                        value="value"
                                    )
                                ),
                                target=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                                    binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                        field="field",
                                        property="property"
                                    ),
                                    bindings={
                                        "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                            element="element",
                                            property="property"
                                        )
                                    },
                                    collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                        field="field",
                                        property="property"
                                    ),
                                    component_name="componentName",
                                    concat=[component_property_property_],
                                    condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                                        else=component_property_property_,
                                        field="field",
                                        operand="operand",
                                        operand_type="operandType",
                                        operator="operator",
                                        property="property",
                                        then=component_property_property_
                                    ),
                                    configured=False,
                                    default_value="defaultValue",
                                    event="event",
                                    imported_value="importedValue",
                                    model="model",
                                    property="property",
                                    type="type",
                                    user_attribute="userAttribute",
                                    value="value"
                                ),
                                type=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                                    binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                        field="field",
                                        property="property"
                                    ),
                                    bindings={
                                        "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                            element="element",
                                            property="property"
                                        )
                                    },
                                    collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                        field="field",
                                        property="property"
                                    ),
                                    component_name="componentName",
                                    concat=[component_property_property_],
                                    condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                                        else=component_property_property_,
                                        field="field",
                                        operand="operand",
                                        operand_type="operandType",
                                        operator="operator",
                                        property="property",
                                        then=component_property_property_
                                    ),
                                    configured=False,
                                    default_value="defaultValue",
                                    event="event",
                                    imported_value="importedValue",
                                    model="model",
                                    property="property",
                                    type="type",
                                    user_attribute="userAttribute",
                                    value="value"
                                ),
                                url=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                                    binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                        field="field",
                                        property="property"
                                    ),
                                    bindings={
                                        "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                            element="element",
                                            property="property"
                                        )
                                    },
                                    collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                        field="field",
                                        property="property"
                                    ),
                                    component_name="componentName",
                                    concat=[component_property_property_],
                                    condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                                        else=component_property_property_,
                                        field="field",
                                        operand="operand",
                                        operand_type="operandType",
                                        operator="operator",
                                        property="property",
                                        then=component_property_property_
                                    ),
                                    configured=False,
                                    default_value="defaultValue",
                                    event="event",
                                    imported_value="importedValue",
                                    model="model",
                                    property="property",
                                    type="type",
                                    user_attribute="userAttribute",
                                    value="value"
                                )
                            )
                        )
                    },
                    name="name",
                    properties={
                        "properties_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                field="field",
                                property="property"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                field="field",
                                property="property"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        )
                    },
                    source_id="sourceId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__433c5b4722fc814fa37ee9bda5cacae13692011d8f07374896954a86f0492e96)
                check_type(argname="argument children", value=children, expected_type=type_hints["children"])
                check_type(argname="argument component_type", value=component_type, expected_type=type_hints["component_type"])
                check_type(argname="argument events", value=events, expected_type=type_hints["events"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
                check_type(argname="argument source_id", value=source_id, expected_type=type_hints["source_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if children is not None:
                self._values["children"] = children
            if component_type is not None:
                self._values["component_type"] = component_type
            if events is not None:
                self._values["events"] = events
            if name is not None:
                self._values["name"] = name
            if properties is not None:
                self._values["properties"] = properties
            if source_id is not None:
                self._values["source_id"] = source_id

        @builtins.property
        def children(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentChildProperty"]]]]:
            '''The list of ``ComponentChild`` instances for this component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentchild.html#cfn-amplifyuibuilder-component-componentchild-children
            '''
            result = self._values.get("children")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentChildProperty"]]]], result)

        @builtins.property
        def component_type(self) -> typing.Optional[builtins.str]:
            '''The type of the child component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentchild.html#cfn-amplifyuibuilder-component-componentchild-componenttype
            '''
            result = self._values.get("component_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def events(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentEventProperty"]]]]:
            '''Describes the events that can be raised on the child component.

            Use for the workflow feature in Amplify Studio that allows you to bind events and actions to components.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentchild.html#cfn-amplifyuibuilder-component-componentchild-events
            '''
            result = self._values.get("events")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentEventProperty"]]]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the child component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentchild.html#cfn-amplifyuibuilder-component-componentchild-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]]]]:
            '''Describes the properties of the child component.

            You can't specify ``tags`` as a valid property for ``properties`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentchild.html#cfn-amplifyuibuilder-component-componentchild-properties
            '''
            result = self._values.get("properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]]]], result)

        @builtins.property
        def source_id(self) -> typing.Optional[builtins.str]:
            '''The unique ID of the child component in its original source system, such as Figma.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentchild.html#cfn-amplifyuibuilder-component-componentchild-sourceid
            '''
            result = self._values.get("source_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentChildProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "else_": "else",
            "field": "field",
            "operand": "operand",
            "operand_type": "operandType",
            "operator": "operator",
            "property": "property",
            "then": "then",
        },
    )
    class ComponentConditionPropertyProperty:
        def __init__(
            self,
            *,
            else_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            field: typing.Optional[builtins.str] = None,
            operand: typing.Optional[builtins.str] = None,
            operand_type: typing.Optional[builtins.str] = None,
            operator: typing.Optional[builtins.str] = None,
            property: typing.Optional[builtins.str] = None,
            then: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The ``ComponentConditionProperty`` property specifies a conditional expression for setting a component property.

            Use ``ComponentConditionProperty`` to set a property to different values conditionally, based on the value of another property.

            :param else_: The value to assign to the property if the condition is not met.
            :param field: The name of a field. Specify this when the property is a data model.
            :param operand: The value of the property to evaluate.
            :param operand_type: The type of the property to evaluate.
            :param operator: The operator to use to perform the evaluation, such as ``eq`` to represent equals.
            :param property: The name of the conditional property.
            :param then: The value to assign to the property if the condition is met.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentconditionproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                # component_condition_property_property_: amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty
                # component_property_property_: amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty
                
                component_condition_property_property = amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                    else=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                            field="field",
                            property="property"
                        ),
                        bindings={
                            "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                element="element",
                                property="property"
                            )
                        },
                        collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                            field="field",
                            property="property"
                        ),
                        component_name="componentName",
                        concat=[component_property_property_],
                        condition=component_condition_property_property_,
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        property="property",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    ),
                    field="field",
                    operand="operand",
                    operand_type="operandType",
                    operator="operator",
                    property="property",
                    then=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                            field="field",
                            property="property"
                        ),
                        bindings={
                            "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                element="element",
                                property="property"
                            )
                        },
                        collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                            field="field",
                            property="property"
                        ),
                        component_name="componentName",
                        concat=[component_property_property_],
                        condition=component_condition_property_property_,
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        property="property",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a0cd03e39b58710890ee87a8093cd0564ba3758144c38a0ccd920847cc7cdebc)
                check_type(argname="argument else_", value=else_, expected_type=type_hints["else_"])
                check_type(argname="argument field", value=field, expected_type=type_hints["field"])
                check_type(argname="argument operand", value=operand, expected_type=type_hints["operand"])
                check_type(argname="argument operand_type", value=operand_type, expected_type=type_hints["operand_type"])
                check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
                check_type(argname="argument property", value=property, expected_type=type_hints["property"])
                check_type(argname="argument then", value=then, expected_type=type_hints["then"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if else_ is not None:
                self._values["else_"] = else_
            if field is not None:
                self._values["field"] = field
            if operand is not None:
                self._values["operand"] = operand
            if operand_type is not None:
                self._values["operand_type"] = operand_type
            if operator is not None:
                self._values["operator"] = operator
            if property is not None:
                self._values["property"] = property
            if then is not None:
                self._values["then"] = then

        @builtins.property
        def else_(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]]:
            '''The value to assign to the property if the condition is not met.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentconditionproperty.html#cfn-amplifyuibuilder-component-componentconditionproperty-else
            '''
            result = self._values.get("else_")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]], result)

        @builtins.property
        def field(self) -> typing.Optional[builtins.str]:
            '''The name of a field.

            Specify this when the property is a data model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentconditionproperty.html#cfn-amplifyuibuilder-component-componentconditionproperty-field
            '''
            result = self._values.get("field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operand(self) -> typing.Optional[builtins.str]:
            '''The value of the property to evaluate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentconditionproperty.html#cfn-amplifyuibuilder-component-componentconditionproperty-operand
            '''
            result = self._values.get("operand")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operand_type(self) -> typing.Optional[builtins.str]:
            '''The type of the property to evaluate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentconditionproperty.html#cfn-amplifyuibuilder-component-componentconditionproperty-operandtype
            '''
            result = self._values.get("operand_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operator(self) -> typing.Optional[builtins.str]:
            '''The operator to use to perform the evaluation, such as ``eq`` to represent equals.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentconditionproperty.html#cfn-amplifyuibuilder-component-componentconditionproperty-operator
            '''
            result = self._values.get("operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property(self) -> typing.Optional[builtins.str]:
            '''The name of the conditional property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentconditionproperty.html#cfn-amplifyuibuilder-component-componentconditionproperty-property
            '''
            result = self._values.get("property")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def then(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]]:
            '''The value to assign to the property if the condition is met.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentconditionproperty.html#cfn-amplifyuibuilder-component-componentconditionproperty-then
            '''
            result = self._values.get("then")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentConditionPropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnComponentPropsMixin.ComponentDataConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "identifiers": "identifiers",
            "model": "model",
            "predicate": "predicate",
            "sort": "sort",
        },
    )
    class ComponentDataConfigurationProperty:
        def __init__(
            self,
            *,
            identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
            model: typing.Optional[builtins.str] = None,
            predicate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.PredicateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sort: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.SortPropertyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``ComponentDataConfiguration`` property specifies the configuration for binding a component's properties to data.

            :param identifiers: A list of IDs to use to bind data to a component. Use this property to bind specifically chosen data, rather than data retrieved from a query.
            :param model: The name of the data model to use to bind data to a component.
            :param predicate: Represents the conditional logic to use when binding data to a component. Use this property to retrieve only a subset of the data in a collection.
            :param sort: Describes how to sort the component's properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentdataconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                # predicate_property_: amplifyuibuilder_mixins.CfnComponentPropsMixin.PredicateProperty
                
                component_data_configuration_property = amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentDataConfigurationProperty(
                    identifiers=["identifiers"],
                    model="model",
                    predicate=amplifyuibuilder_mixins.CfnComponentPropsMixin.PredicateProperty(
                        and=[predicate_property_],
                        field="field",
                        operand="operand",
                        operand_type="operandType",
                        operator="operator",
                        or=[predicate_property_]
                    ),
                    sort=[amplifyuibuilder_mixins.CfnComponentPropsMixin.SortPropertyProperty(
                        direction="direction",
                        field="field"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dc270cb61a77580fbc488b8f23b00de458a1c89d5c6b16e81dcde6ebfed1c00a)
                check_type(argname="argument identifiers", value=identifiers, expected_type=type_hints["identifiers"])
                check_type(argname="argument model", value=model, expected_type=type_hints["model"])
                check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
                check_type(argname="argument sort", value=sort, expected_type=type_hints["sort"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if identifiers is not None:
                self._values["identifiers"] = identifiers
            if model is not None:
                self._values["model"] = model
            if predicate is not None:
                self._values["predicate"] = predicate
            if sort is not None:
                self._values["sort"] = sort

        @builtins.property
        def identifiers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of IDs to use to bind data to a component.

            Use this property to bind specifically chosen data, rather than data retrieved from a query.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentdataconfiguration.html#cfn-amplifyuibuilder-component-componentdataconfiguration-identifiers
            '''
            result = self._values.get("identifiers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def model(self) -> typing.Optional[builtins.str]:
            '''The name of the data model to use to bind data to a component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentdataconfiguration.html#cfn-amplifyuibuilder-component-componentdataconfiguration-model
            '''
            result = self._values.get("model")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def predicate(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.PredicateProperty"]]:
            '''Represents the conditional logic to use when binding data to a component.

            Use this property to retrieve only a subset of the data in a collection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentdataconfiguration.html#cfn-amplifyuibuilder-component-componentdataconfiguration-predicate
            '''
            result = self._values.get("predicate")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.PredicateProperty"]], result)

        @builtins.property
        def sort(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.SortPropertyProperty"]]]]:
            '''Describes how to sort the component's properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentdataconfiguration.html#cfn-amplifyuibuilder-component-componentdataconfiguration-sort
            '''
            result = self._values.get("sort")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.SortPropertyProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentDataConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnComponentPropsMixin.ComponentEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "binding_event": "bindingEvent",
            "parameters": "parameters",
        },
    )
    class ComponentEventProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            binding_event: typing.Optional[builtins.str] = None,
            parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ActionParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The ``ComponentEvent`` property specifies the configuration of an event.

            You can bind an event and a corresponding action to a ``Component`` or a ``ComponentChild`` . A button click is an example of an event.

            :param action: The action to perform when a specific event is raised.
            :param binding_event: Binds an event to an action on a component. When you specify a ``bindingEvent`` , the event is called when the action is performed.
            :param parameters: Describes information about the action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentevent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                # component_property_property_: amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty
                
                component_event_property = amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentEventProperty(
                    action="action",
                    binding_event="bindingEvent",
                    parameters=amplifyuibuilder_mixins.CfnComponentPropsMixin.ActionParametersProperty(
                        anchor=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                field="field",
                                property="property"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                field="field",
                                property="property"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        ),
                        fields={
                            "fields_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                                binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                    field="field",
                                    property="property"
                                ),
                                bindings={
                                    "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                        element="element",
                                        property="property"
                                    )
                                },
                                collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                    field="field",
                                    property="property"
                                ),
                                component_name="componentName",
                                concat=[component_property_property_],
                                condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                                    else=component_property_property_,
                                    field="field",
                                    operand="operand",
                                    operand_type="operandType",
                                    operator="operator",
                                    property="property",
                                    then=component_property_property_
                                ),
                                configured=False,
                                default_value="defaultValue",
                                event="event",
                                imported_value="importedValue",
                                model="model",
                                property="property",
                                type="type",
                                user_attribute="userAttribute",
                                value="value"
                            )
                        },
                        global=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                field="field",
                                property="property"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                field="field",
                                property="property"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        ),
                        id=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                field="field",
                                property="property"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                field="field",
                                property="property"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        ),
                        model="model",
                        state=amplifyuibuilder_mixins.CfnComponentPropsMixin.MutationActionSetStateParameterProperty(
                            component_name="componentName",
                            property="property",
                            set=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                                binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                    field="field",
                                    property="property"
                                ),
                                bindings={
                                    "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                        element="element",
                                        property="property"
                                    )
                                },
                                collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                    field="field",
                                    property="property"
                                ),
                                component_name="componentName",
                                concat=[component_property_property_],
                                condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                                    else=component_property_property_,
                                    field="field",
                                    operand="operand",
                                    operand_type="operandType",
                                    operator="operator",
                                    property="property",
                                    then=component_property_property_
                                ),
                                configured=False,
                                default_value="defaultValue",
                                event="event",
                                imported_value="importedValue",
                                model="model",
                                property="property",
                                type="type",
                                user_attribute="userAttribute",
                                value="value"
                            )
                        ),
                        target=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                field="field",
                                property="property"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                field="field",
                                property="property"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        ),
                        type=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                field="field",
                                property="property"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                field="field",
                                property="property"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        ),
                        url=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                field="field",
                                property="property"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                                field="field",
                                property="property"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__826e4fd2c0ed9b0db220022a029e44013b8170b28594d9d19e287c0d1e6d2adc)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument binding_event", value=binding_event, expected_type=type_hints["binding_event"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if binding_event is not None:
                self._values["binding_event"] = binding_event
            if parameters is not None:
                self._values["parameters"] = parameters

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action to perform when a specific event is raised.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentevent.html#cfn-amplifyuibuilder-component-componentevent-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def binding_event(self) -> typing.Optional[builtins.str]:
            '''Binds an event to an action on a component.

            When you specify a ``bindingEvent`` , the event is called when the action is performed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentevent.html#cfn-amplifyuibuilder-component-componentevent-bindingevent
            '''
            result = self._values.get("binding_event")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ActionParametersProperty"]]:
            '''Describes information about the action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentevent.html#cfn-amplifyuibuilder-component-componentevent-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ActionParametersProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"field": "field", "property": "property"},
    )
    class ComponentPropertyBindingPropertiesProperty:
        def __init__(
            self,
            *,
            field: typing.Optional[builtins.str] = None,
            property: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``ComponentPropertyBindingProperties`` property specifies a component property to associate with a binding property.

            This enables exposed properties on the top level component to propagate data to the component's property values.

            :param field: The data field to bind the property to.
            :param property: The component property to bind to the data field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentpropertybindingproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                component_property_binding_properties_property = amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                    field="field",
                    property="property"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a8ff393316f25d9f8f8a37a68e4fe1d35f183a32edd31e2bd8f69857815c022a)
                check_type(argname="argument field", value=field, expected_type=type_hints["field"])
                check_type(argname="argument property", value=property, expected_type=type_hints["property"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if field is not None:
                self._values["field"] = field
            if property is not None:
                self._values["property"] = property

        @builtins.property
        def field(self) -> typing.Optional[builtins.str]:
            '''The data field to bind the property to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentpropertybindingproperties.html#cfn-amplifyuibuilder-component-componentpropertybindingproperties-field
            '''
            result = self._values.get("field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property(self) -> typing.Optional[builtins.str]:
            '''The component property to bind to the data field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentpropertybindingproperties.html#cfn-amplifyuibuilder-component-componentpropertybindingproperties-property
            '''
            result = self._values.get("property")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentPropertyBindingPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnComponentPropsMixin.ComponentPropertyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "binding_properties": "bindingProperties",
            "bindings": "bindings",
            "collection_binding_properties": "collectionBindingProperties",
            "component_name": "componentName",
            "concat": "concat",
            "condition": "condition",
            "configured": "configured",
            "default_value": "defaultValue",
            "event": "event",
            "imported_value": "importedValue",
            "model": "model",
            "property": "property",
            "type": "type",
            "user_attribute": "userAttribute",
            "value": "value",
        },
    )
    class ComponentPropertyProperty:
        def __init__(
            self,
            *,
            binding_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            bindings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.FormBindingElementProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            collection_binding_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            component_name: typing.Optional[builtins.str] = None,
            concat: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            condition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ComponentConditionPropertyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            configured: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            default_value: typing.Optional[builtins.str] = None,
            event: typing.Optional[builtins.str] = None,
            imported_value: typing.Optional[builtins.str] = None,
            model: typing.Optional[builtins.str] = None,
            property: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            user_attribute: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``ComponentProperty`` property specifies the configuration for all of a component's properties.

            Use ``ComponentProperty`` to specify the values to render or bind by default.

            :param binding_properties: The information to bind the component property to data at runtime.
            :param bindings: The information to bind the component property to form data.
            :param collection_binding_properties: The information to bind the component property to data at runtime. Use this for collection components.
            :param component_name: The name of the component that is affected by an event.
            :param concat: A list of component properties to concatenate to create the value to assign to this component property.
            :param condition: The conditional expression to use to assign a value to the component property.
            :param configured: Specifies whether the user configured the property in Amplify Studio after importing it.
            :param default_value: The default value to assign to the component property.
            :param event: An event that occurs in your app. Use this for workflow data binding.
            :param imported_value: The default value assigned to the property when the component is imported into an app.
            :param model: The data model to use to assign a value to the component property.
            :param property: The name of the component's property that is affected by an event.
            :param type: The component type.
            :param user_attribute: An authenticated user attribute to use to assign a value to the component property.
            :param value: The value to assign to the component property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                # component_property_property_: amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty
                
                component_property_property = amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                    binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                        field="field",
                        property="property"
                    ),
                    bindings={
                        "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                            element="element",
                            property="property"
                        )
                    },
                    collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                        field="field",
                        property="property"
                    ),
                    component_name="componentName",
                    concat=[component_property_property_],
                    condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                        else=component_property_property_,
                        field="field",
                        operand="operand",
                        operand_type="operandType",
                        operator="operator",
                        property="property",
                        then=component_property_property_
                    ),
                    configured=False,
                    default_value="defaultValue",
                    event="event",
                    imported_value="importedValue",
                    model="model",
                    property="property",
                    type="type",
                    user_attribute="userAttribute",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__729c6ed5dec61997a562352acac9da23bfc007d47ced61f521c0df39f7debda0)
                check_type(argname="argument binding_properties", value=binding_properties, expected_type=type_hints["binding_properties"])
                check_type(argname="argument bindings", value=bindings, expected_type=type_hints["bindings"])
                check_type(argname="argument collection_binding_properties", value=collection_binding_properties, expected_type=type_hints["collection_binding_properties"])
                check_type(argname="argument component_name", value=component_name, expected_type=type_hints["component_name"])
                check_type(argname="argument concat", value=concat, expected_type=type_hints["concat"])
                check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
                check_type(argname="argument configured", value=configured, expected_type=type_hints["configured"])
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument event", value=event, expected_type=type_hints["event"])
                check_type(argname="argument imported_value", value=imported_value, expected_type=type_hints["imported_value"])
                check_type(argname="argument model", value=model, expected_type=type_hints["model"])
                check_type(argname="argument property", value=property, expected_type=type_hints["property"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument user_attribute", value=user_attribute, expected_type=type_hints["user_attribute"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if binding_properties is not None:
                self._values["binding_properties"] = binding_properties
            if bindings is not None:
                self._values["bindings"] = bindings
            if collection_binding_properties is not None:
                self._values["collection_binding_properties"] = collection_binding_properties
            if component_name is not None:
                self._values["component_name"] = component_name
            if concat is not None:
                self._values["concat"] = concat
            if condition is not None:
                self._values["condition"] = condition
            if configured is not None:
                self._values["configured"] = configured
            if default_value is not None:
                self._values["default_value"] = default_value
            if event is not None:
                self._values["event"] = event
            if imported_value is not None:
                self._values["imported_value"] = imported_value
            if model is not None:
                self._values["model"] = model
            if property is not None:
                self._values["property"] = property
            if type is not None:
                self._values["type"] = type
            if user_attribute is not None:
                self._values["user_attribute"] = user_attribute
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def binding_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty"]]:
            '''The information to bind the component property to data at runtime.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-bindingproperties
            '''
            result = self._values.get("binding_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty"]], result)

        @builtins.property
        def bindings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.FormBindingElementProperty"]]]]:
            '''The information to bind the component property to form data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-bindings
            '''
            result = self._values.get("bindings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.FormBindingElementProperty"]]]], result)

        @builtins.property
        def collection_binding_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty"]]:
            '''The information to bind the component property to data at runtime.

            Use this for collection components.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-collectionbindingproperties
            '''
            result = self._values.get("collection_binding_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty"]], result)

        @builtins.property
        def component_name(self) -> typing.Optional[builtins.str]:
            '''The name of the component that is affected by an event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-componentname
            '''
            result = self._values.get("component_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def concat(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]]]]:
            '''A list of component properties to concatenate to create the value to assign to this component property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-concat
            '''
            result = self._values.get("concat")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]]]], result)

        @builtins.property
        def condition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentConditionPropertyProperty"]]:
            '''The conditional expression to use to assign a value to the component property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-condition
            '''
            result = self._values.get("condition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentConditionPropertyProperty"]], result)

        @builtins.property
        def configured(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the user configured the property in Amplify Studio after importing it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-configured
            '''
            result = self._values.get("configured")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            '''The default value to assign to the component property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def event(self) -> typing.Optional[builtins.str]:
            '''An event that occurs in your app.

            Use this for workflow data binding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-event
            '''
            result = self._values.get("event")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def imported_value(self) -> typing.Optional[builtins.str]:
            '''The default value assigned to the property when the component is imported into an app.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-importedvalue
            '''
            result = self._values.get("imported_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def model(self) -> typing.Optional[builtins.str]:
            '''The data model to use to assign a value to the component property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-model
            '''
            result = self._values.get("model")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property(self) -> typing.Optional[builtins.str]:
            '''The name of the component's property that is affected by an event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-property
            '''
            result = self._values.get("property")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The component type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_attribute(self) -> typing.Optional[builtins.str]:
            '''An authenticated user attribute to use to assign a value to the component property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-userattribute
            '''
            result = self._values.get("user_attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value to assign to the component property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentPropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnComponentPropsMixin.ComponentVariantProperty",
        jsii_struct_bases=[],
        name_mapping={"overrides": "overrides", "variant_values": "variantValues"},
    )
    class ComponentVariantProperty:
        def __init__(
            self,
            *,
            overrides: typing.Any = None,
            variant_values: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The ``ComponentVariant`` property specifies the style configuration of a unique variation of a main component.

            :param overrides: The properties of the component variant that can be overriden when customizing an instance of the component. You can't specify ``tags`` as a valid property for ``overrides`` .
            :param variant_values: The combination of variants that comprise this variant.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentvariant.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                # overrides: Any
                
                component_variant_property = amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentVariantProperty(
                    overrides=overrides,
                    variant_values={
                        "variant_values_key": "variantValues"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5e16561f49623cbbc176fd841a3b4470aa08e6b88b3dd07110e603ba4c5b468c)
                check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
                check_type(argname="argument variant_values", value=variant_values, expected_type=type_hints["variant_values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if overrides is not None:
                self._values["overrides"] = overrides
            if variant_values is not None:
                self._values["variant_values"] = variant_values

        @builtins.property
        def overrides(self) -> typing.Any:
            '''The properties of the component variant that can be overriden when customizing an instance of the component.

            You can't specify ``tags`` as a valid property for ``overrides`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentvariant.html#cfn-amplifyuibuilder-component-componentvariant-overrides
            '''
            result = self._values.get("overrides")
            return typing.cast(typing.Any, result)

        @builtins.property
        def variant_values(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The combination of variants that comprise this variant.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentvariant.html#cfn-amplifyuibuilder-component-componentvariant-variantvalues
            '''
            result = self._values.get("variant_values")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentVariantProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnComponentPropsMixin.FormBindingElementProperty",
        jsii_struct_bases=[],
        name_mapping={"element": "element", "property": "property"},
    )
    class FormBindingElementProperty:
        def __init__(
            self,
            *,
            element: typing.Optional[builtins.str] = None,
            property: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes how to bind a component property to form data.

            :param element: The name of the component to retrieve a value from.
            :param property: The property to retrieve a value from.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-formbindingelement.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                form_binding_element_property = amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                    element="element",
                    property="property"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cf96a78f2a8ccf6cbeeed185ed40fe6aacc8f6983b397b703bc385ac66d841ed)
                check_type(argname="argument element", value=element, expected_type=type_hints["element"])
                check_type(argname="argument property", value=property, expected_type=type_hints["property"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if element is not None:
                self._values["element"] = element
            if property is not None:
                self._values["property"] = property

        @builtins.property
        def element(self) -> typing.Optional[builtins.str]:
            '''The name of the component to retrieve a value from.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-formbindingelement.html#cfn-amplifyuibuilder-component-formbindingelement-element
            '''
            result = self._values.get("element")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property(self) -> typing.Optional[builtins.str]:
            '''The property to retrieve a value from.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-formbindingelement.html#cfn-amplifyuibuilder-component-formbindingelement-property
            '''
            result = self._values.get("property")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FormBindingElementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnComponentPropsMixin.MutationActionSetStateParameterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component_name": "componentName",
            "property": "property",
            "set": "set",
        },
    )
    class MutationActionSetStateParameterProperty:
        def __init__(
            self,
            *,
            component_name: typing.Optional[builtins.str] = None,
            property: typing.Optional[builtins.str] = None,
            set: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Represents the state configuration when an action modifies a property of another element within the same component.

            :param component_name: The name of the component that is being modified.
            :param property: The name of the component property to apply the state configuration to.
            :param set: The state configuration to assign to the property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-mutationactionsetstateparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                # component_property_property_: amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty
                
                mutation_action_set_state_parameter_property = amplifyuibuilder_mixins.CfnComponentPropsMixin.MutationActionSetStateParameterProperty(
                    component_name="componentName",
                    property="property",
                    set=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                            field="field",
                            property="property"
                        ),
                        bindings={
                            "bindings_key": amplifyuibuilder_mixins.CfnComponentPropsMixin.FormBindingElementProperty(
                                element="element",
                                property="property"
                            )
                        },
                        collection_binding_properties=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty(
                            field="field",
                            property="property"
                        ),
                        component_name="componentName",
                        concat=[component_property_property_],
                        condition=amplifyuibuilder_mixins.CfnComponentPropsMixin.ComponentConditionPropertyProperty(
                            else=component_property_property_,
                            field="field",
                            operand="operand",
                            operand_type="operandType",
                            operator="operator",
                            property="property",
                            then=component_property_property_
                        ),
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        property="property",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__844937e0d4915ca6748b956c6cfaa7d7e423fba5288e063c8e8d5e1ee786c384)
                check_type(argname="argument component_name", value=component_name, expected_type=type_hints["component_name"])
                check_type(argname="argument property", value=property, expected_type=type_hints["property"])
                check_type(argname="argument set", value=set, expected_type=type_hints["set"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if component_name is not None:
                self._values["component_name"] = component_name
            if property is not None:
                self._values["property"] = property
            if set is not None:
                self._values["set"] = set

        @builtins.property
        def component_name(self) -> typing.Optional[builtins.str]:
            '''The name of the component that is being modified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-mutationactionsetstateparameter.html#cfn-amplifyuibuilder-component-mutationactionsetstateparameter-componentname
            '''
            result = self._values.get("component_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property(self) -> typing.Optional[builtins.str]:
            '''The name of the component property to apply the state configuration to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-mutationactionsetstateparameter.html#cfn-amplifyuibuilder-component-mutationactionsetstateparameter-property
            '''
            result = self._values.get("property")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def set(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]]:
            '''The state configuration to assign to the property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-mutationactionsetstateparameter.html#cfn-amplifyuibuilder-component-mutationactionsetstateparameter-set
            '''
            result = self._values.get("set")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.ComponentPropertyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MutationActionSetStateParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnComponentPropsMixin.PredicateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "and_": "and",
            "field": "field",
            "operand": "operand",
            "operand_type": "operandType",
            "operator": "operator",
            "or_": "or",
        },
    )
    class PredicateProperty:
        def __init__(
            self,
            *,
            and_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.PredicateProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            field: typing.Optional[builtins.str] = None,
            operand: typing.Optional[builtins.str] = None,
            operand_type: typing.Optional[builtins.str] = None,
            operator: typing.Optional[builtins.str] = None,
            or_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComponentPropsMixin.PredicateProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``Predicate`` property specifies information for generating Amplify DataStore queries.

            Use ``Predicate`` to retrieve a subset of the data in a collection.

            :param and_: A list of predicates to combine logically.
            :param field: The field to query.
            :param operand: The value to use when performing the evaluation.
            :param operand_type: The type of value to use when performing the evaluation.
            :param operator: The operator to use to perform the evaluation.
            :param or_: A list of predicates to combine logically.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-predicate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                # predicate_property_: amplifyuibuilder_mixins.CfnComponentPropsMixin.PredicateProperty
                
                predicate_property = amplifyuibuilder_mixins.CfnComponentPropsMixin.PredicateProperty(
                    and=[predicate_property_],
                    field="field",
                    operand="operand",
                    operand_type="operandType",
                    operator="operator",
                    or=[predicate_property_]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1902498166b75004689994263c0751f658219e841bb1e6989e9d84cf36f4e4d9)
                check_type(argname="argument and_", value=and_, expected_type=type_hints["and_"])
                check_type(argname="argument field", value=field, expected_type=type_hints["field"])
                check_type(argname="argument operand", value=operand, expected_type=type_hints["operand"])
                check_type(argname="argument operand_type", value=operand_type, expected_type=type_hints["operand_type"])
                check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
                check_type(argname="argument or_", value=or_, expected_type=type_hints["or_"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if and_ is not None:
                self._values["and_"] = and_
            if field is not None:
                self._values["field"] = field
            if operand is not None:
                self._values["operand"] = operand
            if operand_type is not None:
                self._values["operand_type"] = operand_type
            if operator is not None:
                self._values["operator"] = operator
            if or_ is not None:
                self._values["or_"] = or_

        @builtins.property
        def and_(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.PredicateProperty"]]]]:
            '''A list of predicates to combine logically.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-predicate.html#cfn-amplifyuibuilder-component-predicate-and
            '''
            result = self._values.get("and_")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.PredicateProperty"]]]], result)

        @builtins.property
        def field(self) -> typing.Optional[builtins.str]:
            '''The field to query.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-predicate.html#cfn-amplifyuibuilder-component-predicate-field
            '''
            result = self._values.get("field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operand(self) -> typing.Optional[builtins.str]:
            '''The value to use when performing the evaluation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-predicate.html#cfn-amplifyuibuilder-component-predicate-operand
            '''
            result = self._values.get("operand")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operand_type(self) -> typing.Optional[builtins.str]:
            '''The type of value to use when performing the evaluation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-predicate.html#cfn-amplifyuibuilder-component-predicate-operandtype
            '''
            result = self._values.get("operand_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operator(self) -> typing.Optional[builtins.str]:
            '''The operator to use to perform the evaluation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-predicate.html#cfn-amplifyuibuilder-component-predicate-operator
            '''
            result = self._values.get("operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def or_(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.PredicateProperty"]]]]:
            '''A list of predicates to combine logically.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-predicate.html#cfn-amplifyuibuilder-component-predicate-or
            '''
            result = self._values.get("or_")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComponentPropsMixin.PredicateProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredicateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnComponentPropsMixin.SortPropertyProperty",
        jsii_struct_bases=[],
        name_mapping={"direction": "direction", "field": "field"},
    )
    class SortPropertyProperty:
        def __init__(
            self,
            *,
            direction: typing.Optional[builtins.str] = None,
            field: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``SortProperty`` property specifies how to sort the data that you bind to a component.

            :param direction: The direction of the sort, either ascending or descending.
            :param field: The field to perform the sort on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-sortproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                sort_property_property = amplifyuibuilder_mixins.CfnComponentPropsMixin.SortPropertyProperty(
                    direction="direction",
                    field="field"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6a59648f6b1da5cfeaf152d2c9b3cca475cd4a984d20725b40b62020235e2621)
                check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
                check_type(argname="argument field", value=field, expected_type=type_hints["field"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if direction is not None:
                self._values["direction"] = direction
            if field is not None:
                self._values["field"] = field

        @builtins.property
        def direction(self) -> typing.Optional[builtins.str]:
            '''The direction of the sort, either ascending or descending.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-sortproperty.html#cfn-amplifyuibuilder-component-sortproperty-direction
            '''
            result = self._values.get("direction")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def field(self) -> typing.Optional[builtins.str]:
            '''The field to perform the sort on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-sortproperty.html#cfn-amplifyuibuilder-component-sortproperty-field
            '''
            result = self._values.get("field")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SortPropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnFormMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_id": "appId",
        "cta": "cta",
        "data_type": "dataType",
        "environment_name": "environmentName",
        "fields": "fields",
        "form_action_type": "formActionType",
        "label_decorator": "labelDecorator",
        "name": "name",
        "schema_version": "schemaVersion",
        "sectional_elements": "sectionalElements",
        "style": "style",
        "tags": "tags",
    },
)
class CfnFormMixinProps:
    def __init__(
        self,
        *,
        app_id: typing.Optional[builtins.str] = None,
        cta: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.FormCTAProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        data_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.FormDataTypeConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        environment_name: typing.Optional[builtins.str] = None,
        fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.FieldConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        form_action_type: typing.Optional[builtins.str] = None,
        label_decorator: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        schema_version: typing.Optional[builtins.str] = None,
        sectional_elements: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.SectionalElementProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        style: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.FormStyleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnFormPropsMixin.

        :param app_id: The unique ID of the Amplify app associated with the form.
        :param cta: The ``FormCTA`` object that stores the call to action configuration for the form.
        :param data_type: The type of data source to use to create the form.
        :param environment_name: The name of the backend environment that is a part of the Amplify app.
        :param fields: The configuration information for the form's fields.
        :param form_action_type: Specifies whether to perform a create or update action on the form.
        :param label_decorator: Specifies an icon or decoration to display on the form.
        :param name: The name of the form.
        :param schema_version: The schema version of the form.
        :param sectional_elements: The configuration information for the visual helper elements for the form. These elements are not associated with any data.
        :param style: The configuration for the form's style.
        :param tags: One or more key-value pairs to use when tagging the form data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
            
            # form_input_value_property_property_: amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyProperty
            
            cfn_form_mixin_props = amplifyuibuilder_mixins.CfnFormMixinProps(
                app_id="appId",
                cta=amplifyuibuilder_mixins.CfnFormPropsMixin.FormCTAProperty(
                    cancel=amplifyuibuilder_mixins.CfnFormPropsMixin.FormButtonProperty(
                        children="children",
                        excluded=False,
                        position=amplifyuibuilder_mixins.CfnFormPropsMixin.FieldPositionProperty(
                            below="below",
                            fixed="fixed",
                            right_of="rightOf"
                        )
                    ),
                    clear=amplifyuibuilder_mixins.CfnFormPropsMixin.FormButtonProperty(
                        children="children",
                        excluded=False,
                        position=amplifyuibuilder_mixins.CfnFormPropsMixin.FieldPositionProperty(
                            below="below",
                            fixed="fixed",
                            right_of="rightOf"
                        )
                    ),
                    position="position",
                    submit=amplifyuibuilder_mixins.CfnFormPropsMixin.FormButtonProperty(
                        children="children",
                        excluded=False,
                        position=amplifyuibuilder_mixins.CfnFormPropsMixin.FieldPositionProperty(
                            below="below",
                            fixed="fixed",
                            right_of="rightOf"
                        )
                    )
                ),
                data_type=amplifyuibuilder_mixins.CfnFormPropsMixin.FormDataTypeConfigProperty(
                    data_source_type="dataSourceType",
                    data_type_name="dataTypeName"
                ),
                environment_name="environmentName",
                fields={
                    "fields_key": amplifyuibuilder_mixins.CfnFormPropsMixin.FieldConfigProperty(
                        excluded=False,
                        input_type=amplifyuibuilder_mixins.CfnFormPropsMixin.FieldInputConfigProperty(
                            default_checked=False,
                            default_country_code="defaultCountryCode",
                            default_value="defaultValue",
                            descriptive_text="descriptiveText",
                            file_uploader_config=amplifyuibuilder_mixins.CfnFormPropsMixin.FileUploaderFieldConfigProperty(
                                accepted_file_types=["acceptedFileTypes"],
                                access_level="accessLevel",
                                is_resumable=False,
                                max_file_count=123,
                                max_size=123,
                                show_thumbnails=False
                            ),
                            is_array=False,
                            max_value=123,
                            min_value=123,
                            name="name",
                            placeholder="placeholder",
                            read_only=False,
                            required=False,
                            step=123,
                            type="type",
                            value="value",
                            value_mappings=amplifyuibuilder_mixins.CfnFormPropsMixin.ValueMappingsProperty(
                                binding_properties={
                                    "binding_properties_key": amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputBindingPropertiesValueProperty(
                                        binding_properties=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputBindingPropertiesValuePropertiesProperty(
                                            model="model"
                                        ),
                                        type="type"
                                    )
                                },
                                values=[amplifyuibuilder_mixins.CfnFormPropsMixin.ValueMappingProperty(
                                    display_value=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyProperty(
                                        binding_properties=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyBindingPropertiesProperty(
                                            field="field",
                                            property="property"
                                        ),
                                        concat=[form_input_value_property_property_],
                                        value="value"
                                    ),
                                    value=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyProperty(
                                        binding_properties=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyBindingPropertiesProperty(
                                            field="field",
                                            property="property"
                                        ),
                                        concat=[form_input_value_property_property_],
                                        value="value"
                                    )
                                )]
                            )
                        ),
                        label="label",
                        position=amplifyuibuilder_mixins.CfnFormPropsMixin.FieldPositionProperty(
                            below="below",
                            fixed="fixed",
                            right_of="rightOf"
                        ),
                        validations=[amplifyuibuilder_mixins.CfnFormPropsMixin.FieldValidationConfigurationProperty(
                            num_values=[123],
                            str_values=["strValues"],
                            type="type",
                            validation_message="validationMessage"
                        )]
                    )
                },
                form_action_type="formActionType",
                label_decorator="labelDecorator",
                name="name",
                schema_version="schemaVersion",
                sectional_elements={
                    "sectional_elements_key": amplifyuibuilder_mixins.CfnFormPropsMixin.SectionalElementProperty(
                        excluded=False,
                        level=123,
                        orientation="orientation",
                        position=amplifyuibuilder_mixins.CfnFormPropsMixin.FieldPositionProperty(
                            below="below",
                            fixed="fixed",
                            right_of="rightOf"
                        ),
                        text="text",
                        type="type"
                    )
                },
                style=amplifyuibuilder_mixins.CfnFormPropsMixin.FormStyleProperty(
                    horizontal_gap=amplifyuibuilder_mixins.CfnFormPropsMixin.FormStyleConfigProperty(
                        token_reference="tokenReference",
                        value="value"
                    ),
                    outer_padding=amplifyuibuilder_mixins.CfnFormPropsMixin.FormStyleConfigProperty(
                        token_reference="tokenReference",
                        value="value"
                    ),
                    vertical_gap=amplifyuibuilder_mixins.CfnFormPropsMixin.FormStyleConfigProperty(
                        token_reference="tokenReference",
                        value="value"
                    )
                ),
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7546b57c976bb5f3375bd76419a6f691c3bbaf5e246311406054c5fbf7f8e48)
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
            check_type(argname="argument cta", value=cta, expected_type=type_hints["cta"])
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
            check_type(argname="argument environment_name", value=environment_name, expected_type=type_hints["environment_name"])
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
            check_type(argname="argument form_action_type", value=form_action_type, expected_type=type_hints["form_action_type"])
            check_type(argname="argument label_decorator", value=label_decorator, expected_type=type_hints["label_decorator"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schema_version", value=schema_version, expected_type=type_hints["schema_version"])
            check_type(argname="argument sectional_elements", value=sectional_elements, expected_type=type_hints["sectional_elements"])
            check_type(argname="argument style", value=style, expected_type=type_hints["style"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if app_id is not None:
            self._values["app_id"] = app_id
        if cta is not None:
            self._values["cta"] = cta
        if data_type is not None:
            self._values["data_type"] = data_type
        if environment_name is not None:
            self._values["environment_name"] = environment_name
        if fields is not None:
            self._values["fields"] = fields
        if form_action_type is not None:
            self._values["form_action_type"] = form_action_type
        if label_decorator is not None:
            self._values["label_decorator"] = label_decorator
        if name is not None:
            self._values["name"] = name
        if schema_version is not None:
            self._values["schema_version"] = schema_version
        if sectional_elements is not None:
            self._values["sectional_elements"] = sectional_elements
        if style is not None:
            self._values["style"] = style
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def app_id(self) -> typing.Optional[builtins.str]:
        '''The unique ID of the Amplify app associated with the form.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-appid
        '''
        result = self._values.get("app_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cta(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormCTAProperty"]]:
        '''The ``FormCTA`` object that stores the call to action configuration for the form.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-cta
        '''
        result = self._values.get("cta")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormCTAProperty"]], result)

    @builtins.property
    def data_type(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormDataTypeConfigProperty"]]:
        '''The type of data source to use to create the form.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-datatype
        '''
        result = self._values.get("data_type")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormDataTypeConfigProperty"]], result)

    @builtins.property
    def environment_name(self) -> typing.Optional[builtins.str]:
        '''The name of the backend environment that is a part of the Amplify app.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-environmentname
        '''
        result = self._values.get("environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fields(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FieldConfigProperty"]]]]:
        '''The configuration information for the form's fields.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-fields
        '''
        result = self._values.get("fields")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FieldConfigProperty"]]]], result)

    @builtins.property
    def form_action_type(self) -> typing.Optional[builtins.str]:
        '''Specifies whether to perform a create or update action on the form.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-formactiontype
        '''
        result = self._values.get("form_action_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def label_decorator(self) -> typing.Optional[builtins.str]:
        '''Specifies an icon or decoration to display on the form.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-labeldecorator
        '''
        result = self._values.get("label_decorator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the form.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_version(self) -> typing.Optional[builtins.str]:
        '''The schema version of the form.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-schemaversion
        '''
        result = self._values.get("schema_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sectional_elements(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.SectionalElementProperty"]]]]:
        '''The configuration information for the visual helper elements for the form.

        These elements are not associated with any data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-sectionalelements
        '''
        result = self._values.get("sectional_elements")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.SectionalElementProperty"]]]], result)

    @builtins.property
    def style(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormStyleProperty"]]:
        '''The configuration for the form's style.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-style
        '''
        result = self._values.get("style")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormStyleProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''One or more key-value pairs to use when tagging the form data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFormMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFormPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnFormPropsMixin",
):
    '''The AWS::AmplifyUIBuilder::Form resource specifies all of the information that is required to create a form.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html
    :cloudformationResource: AWS::AmplifyUIBuilder::Form
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
        
        # form_input_value_property_property_: amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyProperty
        
        cfn_form_props_mixin = amplifyuibuilder_mixins.CfnFormPropsMixin(amplifyuibuilder_mixins.CfnFormMixinProps(
            app_id="appId",
            cta=amplifyuibuilder_mixins.CfnFormPropsMixin.FormCTAProperty(
                cancel=amplifyuibuilder_mixins.CfnFormPropsMixin.FormButtonProperty(
                    children="children",
                    excluded=False,
                    position=amplifyuibuilder_mixins.CfnFormPropsMixin.FieldPositionProperty(
                        below="below",
                        fixed="fixed",
                        right_of="rightOf"
                    )
                ),
                clear=amplifyuibuilder_mixins.CfnFormPropsMixin.FormButtonProperty(
                    children="children",
                    excluded=False,
                    position=amplifyuibuilder_mixins.CfnFormPropsMixin.FieldPositionProperty(
                        below="below",
                        fixed="fixed",
                        right_of="rightOf"
                    )
                ),
                position="position",
                submit=amplifyuibuilder_mixins.CfnFormPropsMixin.FormButtonProperty(
                    children="children",
                    excluded=False,
                    position=amplifyuibuilder_mixins.CfnFormPropsMixin.FieldPositionProperty(
                        below="below",
                        fixed="fixed",
                        right_of="rightOf"
                    )
                )
            ),
            data_type=amplifyuibuilder_mixins.CfnFormPropsMixin.FormDataTypeConfigProperty(
                data_source_type="dataSourceType",
                data_type_name="dataTypeName"
            ),
            environment_name="environmentName",
            fields={
                "fields_key": amplifyuibuilder_mixins.CfnFormPropsMixin.FieldConfigProperty(
                    excluded=False,
                    input_type=amplifyuibuilder_mixins.CfnFormPropsMixin.FieldInputConfigProperty(
                        default_checked=False,
                        default_country_code="defaultCountryCode",
                        default_value="defaultValue",
                        descriptive_text="descriptiveText",
                        file_uploader_config=amplifyuibuilder_mixins.CfnFormPropsMixin.FileUploaderFieldConfigProperty(
                            accepted_file_types=["acceptedFileTypes"],
                            access_level="accessLevel",
                            is_resumable=False,
                            max_file_count=123,
                            max_size=123,
                            show_thumbnails=False
                        ),
                        is_array=False,
                        max_value=123,
                        min_value=123,
                        name="name",
                        placeholder="placeholder",
                        read_only=False,
                        required=False,
                        step=123,
                        type="type",
                        value="value",
                        value_mappings=amplifyuibuilder_mixins.CfnFormPropsMixin.ValueMappingsProperty(
                            binding_properties={
                                "binding_properties_key": amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputBindingPropertiesValueProperty(
                                    binding_properties=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputBindingPropertiesValuePropertiesProperty(
                                        model="model"
                                    ),
                                    type="type"
                                )
                            },
                            values=[amplifyuibuilder_mixins.CfnFormPropsMixin.ValueMappingProperty(
                                display_value=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyProperty(
                                    binding_properties=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyBindingPropertiesProperty(
                                        field="field",
                                        property="property"
                                    ),
                                    concat=[form_input_value_property_property_],
                                    value="value"
                                ),
                                value=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyProperty(
                                    binding_properties=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyBindingPropertiesProperty(
                                        field="field",
                                        property="property"
                                    ),
                                    concat=[form_input_value_property_property_],
                                    value="value"
                                )
                            )]
                        )
                    ),
                    label="label",
                    position=amplifyuibuilder_mixins.CfnFormPropsMixin.FieldPositionProperty(
                        below="below",
                        fixed="fixed",
                        right_of="rightOf"
                    ),
                    validations=[amplifyuibuilder_mixins.CfnFormPropsMixin.FieldValidationConfigurationProperty(
                        num_values=[123],
                        str_values=["strValues"],
                        type="type",
                        validation_message="validationMessage"
                    )]
                )
            },
            form_action_type="formActionType",
            label_decorator="labelDecorator",
            name="name",
            schema_version="schemaVersion",
            sectional_elements={
                "sectional_elements_key": amplifyuibuilder_mixins.CfnFormPropsMixin.SectionalElementProperty(
                    excluded=False,
                    level=123,
                    orientation="orientation",
                    position=amplifyuibuilder_mixins.CfnFormPropsMixin.FieldPositionProperty(
                        below="below",
                        fixed="fixed",
                        right_of="rightOf"
                    ),
                    text="text",
                    type="type"
                )
            },
            style=amplifyuibuilder_mixins.CfnFormPropsMixin.FormStyleProperty(
                horizontal_gap=amplifyuibuilder_mixins.CfnFormPropsMixin.FormStyleConfigProperty(
                    token_reference="tokenReference",
                    value="value"
                ),
                outer_padding=amplifyuibuilder_mixins.CfnFormPropsMixin.FormStyleConfigProperty(
                    token_reference="tokenReference",
                    value="value"
                ),
                vertical_gap=amplifyuibuilder_mixins.CfnFormPropsMixin.FormStyleConfigProperty(
                    token_reference="tokenReference",
                    value="value"
                )
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
        props: typing.Union[CfnFormMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AmplifyUIBuilder::Form``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca3ee1cc4a7e681f7240b71db5b94853bcf9b69e05d9e1e142438015c2b37b67)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8600180f97a48dc6e94cad53d793f4d9190b76d198e1c5d45b29cc51ccbc733)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7907a142c9a6019e213cc424ba9ebaba3a1f4db42fa263d3c1be6ce9b349916b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFormMixinProps:
        return typing.cast(CfnFormMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnFormPropsMixin.FieldConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "excluded": "excluded",
            "input_type": "inputType",
            "label": "label",
            "position": "position",
            "validations": "validations",
        },
    )
    class FieldConfigProperty:
        def __init__(
            self,
            *,
            excluded: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            input_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.FieldInputConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            label: typing.Optional[builtins.str] = None,
            position: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.FieldPositionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            validations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.FieldValidationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``FieldConfig`` property specifies the configuration information for a field in a table.

            :param excluded: Specifies whether to hide a field.
            :param input_type: Describes the configuration for the default input value to display for a field.
            :param label: The label for the field.
            :param position: Specifies the field position.
            :param validations: The validations to perform on the value in the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                # form_input_value_property_property_: amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyProperty
                
                field_config_property = amplifyuibuilder_mixins.CfnFormPropsMixin.FieldConfigProperty(
                    excluded=False,
                    input_type=amplifyuibuilder_mixins.CfnFormPropsMixin.FieldInputConfigProperty(
                        default_checked=False,
                        default_country_code="defaultCountryCode",
                        default_value="defaultValue",
                        descriptive_text="descriptiveText",
                        file_uploader_config=amplifyuibuilder_mixins.CfnFormPropsMixin.FileUploaderFieldConfigProperty(
                            accepted_file_types=["acceptedFileTypes"],
                            access_level="accessLevel",
                            is_resumable=False,
                            max_file_count=123,
                            max_size=123,
                            show_thumbnails=False
                        ),
                        is_array=False,
                        max_value=123,
                        min_value=123,
                        name="name",
                        placeholder="placeholder",
                        read_only=False,
                        required=False,
                        step=123,
                        type="type",
                        value="value",
                        value_mappings=amplifyuibuilder_mixins.CfnFormPropsMixin.ValueMappingsProperty(
                            binding_properties={
                                "binding_properties_key": amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputBindingPropertiesValueProperty(
                                    binding_properties=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputBindingPropertiesValuePropertiesProperty(
                                        model="model"
                                    ),
                                    type="type"
                                )
                            },
                            values=[amplifyuibuilder_mixins.CfnFormPropsMixin.ValueMappingProperty(
                                display_value=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyProperty(
                                    binding_properties=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyBindingPropertiesProperty(
                                        field="field",
                                        property="property"
                                    ),
                                    concat=[form_input_value_property_property_],
                                    value="value"
                                ),
                                value=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyProperty(
                                    binding_properties=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyBindingPropertiesProperty(
                                        field="field",
                                        property="property"
                                    ),
                                    concat=[form_input_value_property_property_],
                                    value="value"
                                )
                            )]
                        )
                    ),
                    label="label",
                    position=amplifyuibuilder_mixins.CfnFormPropsMixin.FieldPositionProperty(
                        below="below",
                        fixed="fixed",
                        right_of="rightOf"
                    ),
                    validations=[amplifyuibuilder_mixins.CfnFormPropsMixin.FieldValidationConfigurationProperty(
                        num_values=[123],
                        str_values=["strValues"],
                        type="type",
                        validation_message="validationMessage"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9d34a95e86d2f1bd28dc984f8908c8befdaacb7ac4e9d12808a2c52d6f1ee2c5)
                check_type(argname="argument excluded", value=excluded, expected_type=type_hints["excluded"])
                check_type(argname="argument input_type", value=input_type, expected_type=type_hints["input_type"])
                check_type(argname="argument label", value=label, expected_type=type_hints["label"])
                check_type(argname="argument position", value=position, expected_type=type_hints["position"])
                check_type(argname="argument validations", value=validations, expected_type=type_hints["validations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if excluded is not None:
                self._values["excluded"] = excluded
            if input_type is not None:
                self._values["input_type"] = input_type
            if label is not None:
                self._values["label"] = label
            if position is not None:
                self._values["position"] = position
            if validations is not None:
                self._values["validations"] = validations

        @builtins.property
        def excluded(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to hide a field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldconfig.html#cfn-amplifyuibuilder-form-fieldconfig-excluded
            '''
            result = self._values.get("excluded")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def input_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FieldInputConfigProperty"]]:
            '''Describes the configuration for the default input value to display for a field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldconfig.html#cfn-amplifyuibuilder-form-fieldconfig-inputtype
            '''
            result = self._values.get("input_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FieldInputConfigProperty"]], result)

        @builtins.property
        def label(self) -> typing.Optional[builtins.str]:
            '''The label for the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldconfig.html#cfn-amplifyuibuilder-form-fieldconfig-label
            '''
            result = self._values.get("label")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def position(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FieldPositionProperty"]]:
            '''Specifies the field position.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldconfig.html#cfn-amplifyuibuilder-form-fieldconfig-position
            '''
            result = self._values.get("position")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FieldPositionProperty"]], result)

        @builtins.property
        def validations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FieldValidationConfigurationProperty"]]]]:
            '''The validations to perform on the value in the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldconfig.html#cfn-amplifyuibuilder-form-fieldconfig-validations
            '''
            result = self._values.get("validations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FieldValidationConfigurationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnFormPropsMixin.FieldInputConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "default_checked": "defaultChecked",
            "default_country_code": "defaultCountryCode",
            "default_value": "defaultValue",
            "descriptive_text": "descriptiveText",
            "file_uploader_config": "fileUploaderConfig",
            "is_array": "isArray",
            "max_value": "maxValue",
            "min_value": "minValue",
            "name": "name",
            "placeholder": "placeholder",
            "read_only": "readOnly",
            "required": "required",
            "step": "step",
            "type": "type",
            "value": "value",
            "value_mappings": "valueMappings",
        },
    )
    class FieldInputConfigProperty:
        def __init__(
            self,
            *,
            default_checked: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            default_country_code: typing.Optional[builtins.str] = None,
            default_value: typing.Optional[builtins.str] = None,
            descriptive_text: typing.Optional[builtins.str] = None,
            file_uploader_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.FileUploaderFieldConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            is_array: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            max_value: typing.Optional[jsii.Number] = None,
            min_value: typing.Optional[jsii.Number] = None,
            name: typing.Optional[builtins.str] = None,
            placeholder: typing.Optional[builtins.str] = None,
            read_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            step: typing.Optional[jsii.Number] = None,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
            value_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.ValueMappingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The ``FieldInputConfig`` property specifies the configuration for the default input values to display for a field.

            :param default_checked: Specifies whether a field has a default value.
            :param default_country_code: The default country code for a phone number.
            :param default_value: The default value for the field.
            :param descriptive_text: The text to display to describe the field.
            :param file_uploader_config: The configuration for the file uploader field.
            :param is_array: Specifies whether to render the field as an array. This property is ignored if the ``dataSourceType`` for the form is a Data Store.
            :param max_value: The maximum value to display for the field.
            :param min_value: The minimum value to display for the field.
            :param name: The name of the field.
            :param placeholder: The text to display as a placeholder for the field.
            :param read_only: Specifies a read only field.
            :param required: Specifies a field that requires input.
            :param step: The stepping increment for a numeric value in a field.
            :param type: The input type for the field.
            :param value: The value for the field.
            :param value_mappings: The information to use to customize the input fields with data at runtime.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                # form_input_value_property_property_: amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyProperty
                
                field_input_config_property = amplifyuibuilder_mixins.CfnFormPropsMixin.FieldInputConfigProperty(
                    default_checked=False,
                    default_country_code="defaultCountryCode",
                    default_value="defaultValue",
                    descriptive_text="descriptiveText",
                    file_uploader_config=amplifyuibuilder_mixins.CfnFormPropsMixin.FileUploaderFieldConfigProperty(
                        accepted_file_types=["acceptedFileTypes"],
                        access_level="accessLevel",
                        is_resumable=False,
                        max_file_count=123,
                        max_size=123,
                        show_thumbnails=False
                    ),
                    is_array=False,
                    max_value=123,
                    min_value=123,
                    name="name",
                    placeholder="placeholder",
                    read_only=False,
                    required=False,
                    step=123,
                    type="type",
                    value="value",
                    value_mappings=amplifyuibuilder_mixins.CfnFormPropsMixin.ValueMappingsProperty(
                        binding_properties={
                            "binding_properties_key": amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputBindingPropertiesValueProperty(
                                binding_properties=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputBindingPropertiesValuePropertiesProperty(
                                    model="model"
                                ),
                                type="type"
                            )
                        },
                        values=[amplifyuibuilder_mixins.CfnFormPropsMixin.ValueMappingProperty(
                            display_value=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyProperty(
                                binding_properties=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyBindingPropertiesProperty(
                                    field="field",
                                    property="property"
                                ),
                                concat=[form_input_value_property_property_],
                                value="value"
                            ),
                            value=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyProperty(
                                binding_properties=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyBindingPropertiesProperty(
                                    field="field",
                                    property="property"
                                ),
                                concat=[form_input_value_property_property_],
                                value="value"
                            )
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a467e35b1e71c829d4a1d316c4445aad268511f47c3d09e076289ad491175795)
                check_type(argname="argument default_checked", value=default_checked, expected_type=type_hints["default_checked"])
                check_type(argname="argument default_country_code", value=default_country_code, expected_type=type_hints["default_country_code"])
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument descriptive_text", value=descriptive_text, expected_type=type_hints["descriptive_text"])
                check_type(argname="argument file_uploader_config", value=file_uploader_config, expected_type=type_hints["file_uploader_config"])
                check_type(argname="argument is_array", value=is_array, expected_type=type_hints["is_array"])
                check_type(argname="argument max_value", value=max_value, expected_type=type_hints["max_value"])
                check_type(argname="argument min_value", value=min_value, expected_type=type_hints["min_value"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument placeholder", value=placeholder, expected_type=type_hints["placeholder"])
                check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
                check_type(argname="argument required", value=required, expected_type=type_hints["required"])
                check_type(argname="argument step", value=step, expected_type=type_hints["step"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                check_type(argname="argument value_mappings", value=value_mappings, expected_type=type_hints["value_mappings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_checked is not None:
                self._values["default_checked"] = default_checked
            if default_country_code is not None:
                self._values["default_country_code"] = default_country_code
            if default_value is not None:
                self._values["default_value"] = default_value
            if descriptive_text is not None:
                self._values["descriptive_text"] = descriptive_text
            if file_uploader_config is not None:
                self._values["file_uploader_config"] = file_uploader_config
            if is_array is not None:
                self._values["is_array"] = is_array
            if max_value is not None:
                self._values["max_value"] = max_value
            if min_value is not None:
                self._values["min_value"] = min_value
            if name is not None:
                self._values["name"] = name
            if placeholder is not None:
                self._values["placeholder"] = placeholder
            if read_only is not None:
                self._values["read_only"] = read_only
            if required is not None:
                self._values["required"] = required
            if step is not None:
                self._values["step"] = step
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value
            if value_mappings is not None:
                self._values["value_mappings"] = value_mappings

        @builtins.property
        def default_checked(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether a field has a default value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-defaultchecked
            '''
            result = self._values.get("default_checked")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def default_country_code(self) -> typing.Optional[builtins.str]:
            '''The default country code for a phone number.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-defaultcountrycode
            '''
            result = self._values.get("default_country_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            '''The default value for the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def descriptive_text(self) -> typing.Optional[builtins.str]:
            '''The text to display to describe the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-descriptivetext
            '''
            result = self._values.get("descriptive_text")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def file_uploader_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FileUploaderFieldConfigProperty"]]:
            '''The configuration for the file uploader field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-fileuploaderconfig
            '''
            result = self._values.get("file_uploader_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FileUploaderFieldConfigProperty"]], result)

        @builtins.property
        def is_array(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to render the field as an array.

            This property is ignored if the ``dataSourceType`` for the form is a Data Store.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-isarray
            '''
            result = self._values.get("is_array")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def max_value(self) -> typing.Optional[jsii.Number]:
            '''The maximum value to display for the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-maxvalue
            '''
            result = self._values.get("max_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_value(self) -> typing.Optional[jsii.Number]:
            '''The minimum value to display for the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-minvalue
            '''
            result = self._values.get("min_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def placeholder(self) -> typing.Optional[builtins.str]:
            '''The text to display as a placeholder for the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-placeholder
            '''
            result = self._values.get("placeholder")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def read_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies a read only field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-readonly
            '''
            result = self._values.get("read_only")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def required(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies a field that requires input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-required
            '''
            result = self._values.get("required")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def step(self) -> typing.Optional[jsii.Number]:
            '''The stepping increment for a numeric value in a field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-step
            '''
            result = self._values.get("step")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The input type for the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value for the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.ValueMappingsProperty"]]:
            '''The information to use to customize the input fields with data at runtime.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-valuemappings
            '''
            result = self._values.get("value_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.ValueMappingsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldInputConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnFormPropsMixin.FieldPositionProperty",
        jsii_struct_bases=[],
        name_mapping={"below": "below", "fixed": "fixed", "right_of": "rightOf"},
    )
    class FieldPositionProperty:
        def __init__(
            self,
            *,
            below: typing.Optional[builtins.str] = None,
            fixed: typing.Optional[builtins.str] = None,
            right_of: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``FieldPosition`` property specifies the field position.

            :param below: The field position is below the field specified by the string.
            :param fixed: The field position is fixed and doesn't change in relation to other fields.
            :param right_of: The field position is to the right of the field specified by the string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldposition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                field_position_property = amplifyuibuilder_mixins.CfnFormPropsMixin.FieldPositionProperty(
                    below="below",
                    fixed="fixed",
                    right_of="rightOf"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c2ee358e41d0004cf0f1cb46098a87b83c4a0a57e923e84d38ce0b18e8553595)
                check_type(argname="argument below", value=below, expected_type=type_hints["below"])
                check_type(argname="argument fixed", value=fixed, expected_type=type_hints["fixed"])
                check_type(argname="argument right_of", value=right_of, expected_type=type_hints["right_of"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if below is not None:
                self._values["below"] = below
            if fixed is not None:
                self._values["fixed"] = fixed
            if right_of is not None:
                self._values["right_of"] = right_of

        @builtins.property
        def below(self) -> typing.Optional[builtins.str]:
            '''The field position is below the field specified by the string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldposition.html#cfn-amplifyuibuilder-form-fieldposition-below
            '''
            result = self._values.get("below")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def fixed(self) -> typing.Optional[builtins.str]:
            '''The field position is fixed and doesn't change in relation to other fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldposition.html#cfn-amplifyuibuilder-form-fieldposition-fixed
            '''
            result = self._values.get("fixed")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def right_of(self) -> typing.Optional[builtins.str]:
            '''The field position is to the right of the field specified by the string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldposition.html#cfn-amplifyuibuilder-form-fieldposition-rightof
            '''
            result = self._values.get("right_of")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldPositionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnFormPropsMixin.FieldValidationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "num_values": "numValues",
            "str_values": "strValues",
            "type": "type",
            "validation_message": "validationMessage",
        },
    )
    class FieldValidationConfigurationProperty:
        def __init__(
            self,
            *,
            num_values: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
            str_values: typing.Optional[typing.Sequence[builtins.str]] = None,
            type: typing.Optional[builtins.str] = None,
            validation_message: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``FieldValidationConfiguration`` property specifies the validation configuration for a field.

            :param num_values: The validation to perform on a number value.
            :param str_values: The validation to perform on a string value.
            :param type: The validation to perform on an object type. ``
            :param validation_message: The validation message to display.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldvalidationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                field_validation_configuration_property = amplifyuibuilder_mixins.CfnFormPropsMixin.FieldValidationConfigurationProperty(
                    num_values=[123],
                    str_values=["strValues"],
                    type="type",
                    validation_message="validationMessage"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ea302a6eadbb701d3ed34e2cd0403bc6ccedd673d82086cf59cf3c9b084817c2)
                check_type(argname="argument num_values", value=num_values, expected_type=type_hints["num_values"])
                check_type(argname="argument str_values", value=str_values, expected_type=type_hints["str_values"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument validation_message", value=validation_message, expected_type=type_hints["validation_message"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if num_values is not None:
                self._values["num_values"] = num_values
            if str_values is not None:
                self._values["str_values"] = str_values
            if type is not None:
                self._values["type"] = type
            if validation_message is not None:
                self._values["validation_message"] = validation_message

        @builtins.property
        def num_values(
            self,
        ) -> typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]]:
            '''The validation to perform on a number value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldvalidationconfiguration.html#cfn-amplifyuibuilder-form-fieldvalidationconfiguration-numvalues
            '''
            result = self._values.get("num_values")
            return typing.cast(typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def str_values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The validation to perform on a string value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldvalidationconfiguration.html#cfn-amplifyuibuilder-form-fieldvalidationconfiguration-strvalues
            '''
            result = self._values.get("str_values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The validation to perform on an object type.

            ``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldvalidationconfiguration.html#cfn-amplifyuibuilder-form-fieldvalidationconfiguration-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def validation_message(self) -> typing.Optional[builtins.str]:
            '''The validation message to display.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldvalidationconfiguration.html#cfn-amplifyuibuilder-form-fieldvalidationconfiguration-validationmessage
            '''
            result = self._values.get("validation_message")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldValidationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnFormPropsMixin.FileUploaderFieldConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "accepted_file_types": "acceptedFileTypes",
            "access_level": "accessLevel",
            "is_resumable": "isResumable",
            "max_file_count": "maxFileCount",
            "max_size": "maxSize",
            "show_thumbnails": "showThumbnails",
        },
    )
    class FileUploaderFieldConfigProperty:
        def __init__(
            self,
            *,
            accepted_file_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            access_level: typing.Optional[builtins.str] = None,
            is_resumable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            max_file_count: typing.Optional[jsii.Number] = None,
            max_size: typing.Optional[jsii.Number] = None,
            show_thumbnails: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Describes the configuration for the file uploader field.

            :param accepted_file_types: The file types that are allowed to be uploaded by the file uploader. Provide this information in an array of strings specifying the valid file extensions.
            :param access_level: The access level to assign to the uploaded files in the Amazon S3 bucket where they are stored. The valid values for this property are ``private`` , ``protected`` , or ``public`` . For detailed information about the permissions associated with each access level, see `File access levels <https://docs.aws.amazon.com/https://docs.amplify.aws/lib/storage/configureaccess/q/platform/js/>`_ in the *Amplify documentation* .
            :param is_resumable: Allows the file upload operation to be paused and resumed. The default value is ``false`` . When ``isResumable`` is set to ``true`` , the file uploader uses a multipart upload to break the files into chunks before upload. The progress of the upload isn't continuous, because the file uploader uploads a chunk at a time.
            :param max_file_count: Specifies the maximum number of files that can be selected to upload. The default value is an unlimited number of files.
            :param max_size: The maximum file size in bytes that the file uploader will accept. The default value is an unlimited file size.
            :param show_thumbnails: Specifies whether to display or hide the image preview after selecting a file for upload. The default value is ``true`` to display the image preview.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fileuploaderfieldconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                file_uploader_field_config_property = amplifyuibuilder_mixins.CfnFormPropsMixin.FileUploaderFieldConfigProperty(
                    accepted_file_types=["acceptedFileTypes"],
                    access_level="accessLevel",
                    is_resumable=False,
                    max_file_count=123,
                    max_size=123,
                    show_thumbnails=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__257d526dab3fe8801e9a519843956fb9b24c245717a9b4526e26ffa1ffec8aa9)
                check_type(argname="argument accepted_file_types", value=accepted_file_types, expected_type=type_hints["accepted_file_types"])
                check_type(argname="argument access_level", value=access_level, expected_type=type_hints["access_level"])
                check_type(argname="argument is_resumable", value=is_resumable, expected_type=type_hints["is_resumable"])
                check_type(argname="argument max_file_count", value=max_file_count, expected_type=type_hints["max_file_count"])
                check_type(argname="argument max_size", value=max_size, expected_type=type_hints["max_size"])
                check_type(argname="argument show_thumbnails", value=show_thumbnails, expected_type=type_hints["show_thumbnails"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if accepted_file_types is not None:
                self._values["accepted_file_types"] = accepted_file_types
            if access_level is not None:
                self._values["access_level"] = access_level
            if is_resumable is not None:
                self._values["is_resumable"] = is_resumable
            if max_file_count is not None:
                self._values["max_file_count"] = max_file_count
            if max_size is not None:
                self._values["max_size"] = max_size
            if show_thumbnails is not None:
                self._values["show_thumbnails"] = show_thumbnails

        @builtins.property
        def accepted_file_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The file types that are allowed to be uploaded by the file uploader.

            Provide this information in an array of strings specifying the valid file extensions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fileuploaderfieldconfig.html#cfn-amplifyuibuilder-form-fileuploaderfieldconfig-acceptedfiletypes
            '''
            result = self._values.get("accepted_file_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def access_level(self) -> typing.Optional[builtins.str]:
            '''The access level to assign to the uploaded files in the Amazon S3 bucket where they are stored.

            The valid values for this property are ``private`` , ``protected`` , or ``public`` . For detailed information about the permissions associated with each access level, see `File access levels <https://docs.aws.amazon.com/https://docs.amplify.aws/lib/storage/configureaccess/q/platform/js/>`_ in the *Amplify documentation* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fileuploaderfieldconfig.html#cfn-amplifyuibuilder-form-fileuploaderfieldconfig-accesslevel
            '''
            result = self._values.get("access_level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def is_resumable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Allows the file upload operation to be paused and resumed. The default value is ``false`` .

            When ``isResumable`` is set to ``true`` , the file uploader uses a multipart upload to break the files into chunks before upload. The progress of the upload isn't continuous, because the file uploader uploads a chunk at a time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fileuploaderfieldconfig.html#cfn-amplifyuibuilder-form-fileuploaderfieldconfig-isresumable
            '''
            result = self._values.get("is_resumable")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def max_file_count(self) -> typing.Optional[jsii.Number]:
            '''Specifies the maximum number of files that can be selected to upload.

            The default value is an unlimited number of files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fileuploaderfieldconfig.html#cfn-amplifyuibuilder-form-fileuploaderfieldconfig-maxfilecount
            '''
            result = self._values.get("max_file_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_size(self) -> typing.Optional[jsii.Number]:
            '''The maximum file size in bytes that the file uploader will accept.

            The default value is an unlimited file size.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fileuploaderfieldconfig.html#cfn-amplifyuibuilder-form-fileuploaderfieldconfig-maxsize
            '''
            result = self._values.get("max_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def show_thumbnails(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to display or hide the image preview after selecting a file for upload.

            The default value is ``true`` to display the image preview.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fileuploaderfieldconfig.html#cfn-amplifyuibuilder-form-fileuploaderfieldconfig-showthumbnails
            '''
            result = self._values.get("show_thumbnails")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FileUploaderFieldConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnFormPropsMixin.FormButtonProperty",
        jsii_struct_bases=[],
        name_mapping={
            "children": "children",
            "excluded": "excluded",
            "position": "position",
        },
    )
    class FormButtonProperty:
        def __init__(
            self,
            *,
            children: typing.Optional[builtins.str] = None,
            excluded: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            position: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.FieldPositionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The ``FormButton`` property specifies the configuration for a button UI element that is a part of a form.

            :param children: Describes the button's properties.
            :param excluded: Specifies whether the button is visible on the form.
            :param position: The position of the button.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formbutton.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                form_button_property = amplifyuibuilder_mixins.CfnFormPropsMixin.FormButtonProperty(
                    children="children",
                    excluded=False,
                    position=amplifyuibuilder_mixins.CfnFormPropsMixin.FieldPositionProperty(
                        below="below",
                        fixed="fixed",
                        right_of="rightOf"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__25d643d5ca32cabc836a640d31c39e6db2825861cc2d9bc86f7545e04ce0ccad)
                check_type(argname="argument children", value=children, expected_type=type_hints["children"])
                check_type(argname="argument excluded", value=excluded, expected_type=type_hints["excluded"])
                check_type(argname="argument position", value=position, expected_type=type_hints["position"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if children is not None:
                self._values["children"] = children
            if excluded is not None:
                self._values["excluded"] = excluded
            if position is not None:
                self._values["position"] = position

        @builtins.property
        def children(self) -> typing.Optional[builtins.str]:
            '''Describes the button's properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formbutton.html#cfn-amplifyuibuilder-form-formbutton-children
            '''
            result = self._values.get("children")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def excluded(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the button is visible on the form.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formbutton.html#cfn-amplifyuibuilder-form-formbutton-excluded
            '''
            result = self._values.get("excluded")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def position(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FieldPositionProperty"]]:
            '''The position of the button.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formbutton.html#cfn-amplifyuibuilder-form-formbutton-position
            '''
            result = self._values.get("position")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FieldPositionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FormButtonProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnFormPropsMixin.FormCTAProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cancel": "cancel",
            "clear": "clear",
            "position": "position",
            "submit": "submit",
        },
    )
    class FormCTAProperty:
        def __init__(
            self,
            *,
            cancel: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.FormButtonProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            clear: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.FormButtonProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            position: typing.Optional[builtins.str] = None,
            submit: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.FormButtonProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The ``FormCTA`` property specifies the call to action button configuration for the form.

            :param cancel: Displays a cancel button.
            :param clear: Displays a clear button.
            :param position: The position of the button.
            :param submit: Displays a submit button.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formcta.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                form_cTAProperty = amplifyuibuilder_mixins.CfnFormPropsMixin.FormCTAProperty(
                    cancel=amplifyuibuilder_mixins.CfnFormPropsMixin.FormButtonProperty(
                        children="children",
                        excluded=False,
                        position=amplifyuibuilder_mixins.CfnFormPropsMixin.FieldPositionProperty(
                            below="below",
                            fixed="fixed",
                            right_of="rightOf"
                        )
                    ),
                    clear=amplifyuibuilder_mixins.CfnFormPropsMixin.FormButtonProperty(
                        children="children",
                        excluded=False,
                        position=amplifyuibuilder_mixins.CfnFormPropsMixin.FieldPositionProperty(
                            below="below",
                            fixed="fixed",
                            right_of="rightOf"
                        )
                    ),
                    position="position",
                    submit=amplifyuibuilder_mixins.CfnFormPropsMixin.FormButtonProperty(
                        children="children",
                        excluded=False,
                        position=amplifyuibuilder_mixins.CfnFormPropsMixin.FieldPositionProperty(
                            below="below",
                            fixed="fixed",
                            right_of="rightOf"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ba45c3535b85b8c19e511a6a54efc9bd3db28f9e81f9504959b067f157f2745e)
                check_type(argname="argument cancel", value=cancel, expected_type=type_hints["cancel"])
                check_type(argname="argument clear", value=clear, expected_type=type_hints["clear"])
                check_type(argname="argument position", value=position, expected_type=type_hints["position"])
                check_type(argname="argument submit", value=submit, expected_type=type_hints["submit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cancel is not None:
                self._values["cancel"] = cancel
            if clear is not None:
                self._values["clear"] = clear
            if position is not None:
                self._values["position"] = position
            if submit is not None:
                self._values["submit"] = submit

        @builtins.property
        def cancel(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormButtonProperty"]]:
            '''Displays a cancel button.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formcta.html#cfn-amplifyuibuilder-form-formcta-cancel
            '''
            result = self._values.get("cancel")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormButtonProperty"]], result)

        @builtins.property
        def clear(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormButtonProperty"]]:
            '''Displays a clear button.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formcta.html#cfn-amplifyuibuilder-form-formcta-clear
            '''
            result = self._values.get("clear")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormButtonProperty"]], result)

        @builtins.property
        def position(self) -> typing.Optional[builtins.str]:
            '''The position of the button.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formcta.html#cfn-amplifyuibuilder-form-formcta-position
            '''
            result = self._values.get("position")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def submit(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormButtonProperty"]]:
            '''Displays a submit button.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formcta.html#cfn-amplifyuibuilder-form-formcta-submit
            '''
            result = self._values.get("submit")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormButtonProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FormCTAProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnFormPropsMixin.FormDataTypeConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_source_type": "dataSourceType",
            "data_type_name": "dataTypeName",
        },
    )
    class FormDataTypeConfigProperty:
        def __init__(
            self,
            *,
            data_source_type: typing.Optional[builtins.str] = None,
            data_type_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``FormDataTypeConfig`` property specifies the data type configuration for the data source associated with a form.

            :param data_source_type: The data source type, either an Amplify DataStore model or a custom data type.
            :param data_type_name: The unique name of the data type you are using as the data source for the form.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formdatatypeconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                form_data_type_config_property = amplifyuibuilder_mixins.CfnFormPropsMixin.FormDataTypeConfigProperty(
                    data_source_type="dataSourceType",
                    data_type_name="dataTypeName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c6655352a521b2883ea7cebd1c33e1dd36a63478b2573796e281f71c6a7ad9ff)
                check_type(argname="argument data_source_type", value=data_source_type, expected_type=type_hints["data_source_type"])
                check_type(argname="argument data_type_name", value=data_type_name, expected_type=type_hints["data_type_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_source_type is not None:
                self._values["data_source_type"] = data_source_type
            if data_type_name is not None:
                self._values["data_type_name"] = data_type_name

        @builtins.property
        def data_source_type(self) -> typing.Optional[builtins.str]:
            '''The data source type, either an Amplify DataStore model or a custom data type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formdatatypeconfig.html#cfn-amplifyuibuilder-form-formdatatypeconfig-datasourcetype
            '''
            result = self._values.get("data_source_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_type_name(self) -> typing.Optional[builtins.str]:
            '''The unique name of the data type you are using as the data source for the form.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formdatatypeconfig.html#cfn-amplifyuibuilder-form-formdatatypeconfig-datatypename
            '''
            result = self._values.get("data_type_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FormDataTypeConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnFormPropsMixin.FormInputBindingPropertiesValuePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"model": "model"},
    )
    class FormInputBindingPropertiesValuePropertiesProperty:
        def __init__(self, *, model: typing.Optional[builtins.str] = None) -> None:
            '''Represents the data binding configuration for a specific property using data stored in AWS .

            For AWS connected properties, you can bind a property to data stored in an Amplify DataStore model.

            :param model: An Amplify DataStore model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-forminputbindingpropertiesvalueproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                form_input_binding_properties_value_properties_property = amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputBindingPropertiesValuePropertiesProperty(
                    model="model"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d68e1b5b79c9ca5b8a30a3ce0f42c6cb77fded8bf1fbdcedbc1646e1b392c1ec)
                check_type(argname="argument model", value=model, expected_type=type_hints["model"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if model is not None:
                self._values["model"] = model

        @builtins.property
        def model(self) -> typing.Optional[builtins.str]:
            '''An Amplify DataStore model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-forminputbindingpropertiesvalueproperties.html#cfn-amplifyuibuilder-form-forminputbindingpropertiesvalueproperties-model
            '''
            result = self._values.get("model")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FormInputBindingPropertiesValuePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnFormPropsMixin.FormInputBindingPropertiesValueProperty",
        jsii_struct_bases=[],
        name_mapping={"binding_properties": "bindingProperties", "type": "type"},
    )
    class FormInputBindingPropertiesValueProperty:
        def __init__(
            self,
            *,
            binding_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.FormInputBindingPropertiesValuePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents the data binding configuration for a form's input fields at runtime.You can use ``FormInputBindingPropertiesValue`` to add exposed properties to a form to allow different values to be entered when a form is reused in different places in an app.

            :param binding_properties: Describes the properties to customize with data at runtime.
            :param type: The property type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-forminputbindingpropertiesvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                form_input_binding_properties_value_property = amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputBindingPropertiesValueProperty(
                    binding_properties=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputBindingPropertiesValuePropertiesProperty(
                        model="model"
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8f8ee3343832160c597d13f17df33e7f16741aaa320e092fc78699398cd7f92c)
                check_type(argname="argument binding_properties", value=binding_properties, expected_type=type_hints["binding_properties"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if binding_properties is not None:
                self._values["binding_properties"] = binding_properties
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def binding_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormInputBindingPropertiesValuePropertiesProperty"]]:
            '''Describes the properties to customize with data at runtime.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-forminputbindingpropertiesvalue.html#cfn-amplifyuibuilder-form-forminputbindingpropertiesvalue-bindingproperties
            '''
            result = self._values.get("binding_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormInputBindingPropertiesValuePropertiesProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The property type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-forminputbindingpropertiesvalue.html#cfn-amplifyuibuilder-form-forminputbindingpropertiesvalue-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FormInputBindingPropertiesValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnFormPropsMixin.FormInputValuePropertyBindingPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"field": "field", "property": "property"},
    )
    class FormInputValuePropertyBindingPropertiesProperty:
        def __init__(
            self,
            *,
            field: typing.Optional[builtins.str] = None,
            property: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Associates a form property to a binding property.

            This enables exposed properties on the top level form to propagate data to the form's property values.

            :param field: The data field to bind the property to.
            :param property: The form property to bind to the data field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-forminputvaluepropertybindingproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                form_input_value_property_binding_properties_property = amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyBindingPropertiesProperty(
                    field="field",
                    property="property"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__894df7000885b009bb3829053da05bc9f7217b816c07f39c4d430413fa5d032f)
                check_type(argname="argument field", value=field, expected_type=type_hints["field"])
                check_type(argname="argument property", value=property, expected_type=type_hints["property"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if field is not None:
                self._values["field"] = field
            if property is not None:
                self._values["property"] = property

        @builtins.property
        def field(self) -> typing.Optional[builtins.str]:
            '''The data field to bind the property to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-forminputvaluepropertybindingproperties.html#cfn-amplifyuibuilder-form-forminputvaluepropertybindingproperties-field
            '''
            result = self._values.get("field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property(self) -> typing.Optional[builtins.str]:
            '''The form property to bind to the data field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-forminputvaluepropertybindingproperties.html#cfn-amplifyuibuilder-form-forminputvaluepropertybindingproperties-property
            '''
            result = self._values.get("property")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FormInputValuePropertyBindingPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnFormPropsMixin.FormInputValuePropertyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "binding_properties": "bindingProperties",
            "concat": "concat",
            "value": "value",
        },
    )
    class FormInputValuePropertyProperty:
        def __init__(
            self,
            *,
            binding_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.FormInputValuePropertyBindingPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            concat: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.FormInputValuePropertyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``FormInputValueProperty`` property specifies the configuration for an input field on a form.

            Use ``FormInputValueProperty`` to specify the values to render or bind by default.

            :param binding_properties: The information to bind fields to data at runtime.
            :param concat: A list of form properties to concatenate to create the value to assign to this field property.
            :param value: The value to assign to the input field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-forminputvalueproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                # form_input_value_property_property_: amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyProperty
                
                form_input_value_property_property = amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyProperty(
                    binding_properties=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyBindingPropertiesProperty(
                        field="field",
                        property="property"
                    ),
                    concat=[form_input_value_property_property_],
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__61c5c2e5ba0a1c3a879bec3c62eff7b28b2dfd404b9e7e7c0e21344d78a14aba)
                check_type(argname="argument binding_properties", value=binding_properties, expected_type=type_hints["binding_properties"])
                check_type(argname="argument concat", value=concat, expected_type=type_hints["concat"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if binding_properties is not None:
                self._values["binding_properties"] = binding_properties
            if concat is not None:
                self._values["concat"] = concat
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def binding_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormInputValuePropertyBindingPropertiesProperty"]]:
            '''The information to bind fields to data at runtime.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-forminputvalueproperty.html#cfn-amplifyuibuilder-form-forminputvalueproperty-bindingproperties
            '''
            result = self._values.get("binding_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormInputValuePropertyBindingPropertiesProperty"]], result)

        @builtins.property
        def concat(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormInputValuePropertyProperty"]]]]:
            '''A list of form properties to concatenate to create the value to assign to this field property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-forminputvalueproperty.html#cfn-amplifyuibuilder-form-forminputvalueproperty-concat
            '''
            result = self._values.get("concat")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormInputValuePropertyProperty"]]]], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value to assign to the input field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-forminputvalueproperty.html#cfn-amplifyuibuilder-form-forminputvalueproperty-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FormInputValuePropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnFormPropsMixin.FormStyleConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"token_reference": "tokenReference", "value": "value"},
    )
    class FormStyleConfigProperty:
        def __init__(
            self,
            *,
            token_reference: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``FormStyleConfig`` property specifies the configuration settings for the form's style properties.

            :param token_reference: A reference to a design token to use to bind the form's style properties to an existing theme.
            :param value: The value of the style setting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formstyleconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                form_style_config_property = amplifyuibuilder_mixins.CfnFormPropsMixin.FormStyleConfigProperty(
                    token_reference="tokenReference",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ab642873ab5056a0b5075302f4a99c0cf8d948f6f27fed41fddbbf236c19859d)
                check_type(argname="argument token_reference", value=token_reference, expected_type=type_hints["token_reference"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if token_reference is not None:
                self._values["token_reference"] = token_reference
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def token_reference(self) -> typing.Optional[builtins.str]:
            '''A reference to a design token to use to bind the form's style properties to an existing theme.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formstyleconfig.html#cfn-amplifyuibuilder-form-formstyleconfig-tokenreference
            '''
            result = self._values.get("token_reference")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the style setting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formstyleconfig.html#cfn-amplifyuibuilder-form-formstyleconfig-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FormStyleConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnFormPropsMixin.FormStyleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "horizontal_gap": "horizontalGap",
            "outer_padding": "outerPadding",
            "vertical_gap": "verticalGap",
        },
    )
    class FormStyleProperty:
        def __init__(
            self,
            *,
            horizontal_gap: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.FormStyleConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            outer_padding: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.FormStyleConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            vertical_gap: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.FormStyleConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The ``FormStyle`` property specifies the configuration for the form's style.

            :param horizontal_gap: The spacing for the horizontal gap.
            :param outer_padding: The size of the outer padding for the form.
            :param vertical_gap: The spacing for the vertical gap.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formstyle.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                form_style_property = amplifyuibuilder_mixins.CfnFormPropsMixin.FormStyleProperty(
                    horizontal_gap=amplifyuibuilder_mixins.CfnFormPropsMixin.FormStyleConfigProperty(
                        token_reference="tokenReference",
                        value="value"
                    ),
                    outer_padding=amplifyuibuilder_mixins.CfnFormPropsMixin.FormStyleConfigProperty(
                        token_reference="tokenReference",
                        value="value"
                    ),
                    vertical_gap=amplifyuibuilder_mixins.CfnFormPropsMixin.FormStyleConfigProperty(
                        token_reference="tokenReference",
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__524ff15f750a9eb0ecf255e4cd063f9e1d6b4773421d674582d7f6e7ea87e6dd)
                check_type(argname="argument horizontal_gap", value=horizontal_gap, expected_type=type_hints["horizontal_gap"])
                check_type(argname="argument outer_padding", value=outer_padding, expected_type=type_hints["outer_padding"])
                check_type(argname="argument vertical_gap", value=vertical_gap, expected_type=type_hints["vertical_gap"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if horizontal_gap is not None:
                self._values["horizontal_gap"] = horizontal_gap
            if outer_padding is not None:
                self._values["outer_padding"] = outer_padding
            if vertical_gap is not None:
                self._values["vertical_gap"] = vertical_gap

        @builtins.property
        def horizontal_gap(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormStyleConfigProperty"]]:
            '''The spacing for the horizontal gap.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formstyle.html#cfn-amplifyuibuilder-form-formstyle-horizontalgap
            '''
            result = self._values.get("horizontal_gap")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormStyleConfigProperty"]], result)

        @builtins.property
        def outer_padding(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormStyleConfigProperty"]]:
            '''The size of the outer padding for the form.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formstyle.html#cfn-amplifyuibuilder-form-formstyle-outerpadding
            '''
            result = self._values.get("outer_padding")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormStyleConfigProperty"]], result)

        @builtins.property
        def vertical_gap(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormStyleConfigProperty"]]:
            '''The spacing for the vertical gap.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formstyle.html#cfn-amplifyuibuilder-form-formstyle-verticalgap
            '''
            result = self._values.get("vertical_gap")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormStyleConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FormStyleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnFormPropsMixin.SectionalElementProperty",
        jsii_struct_bases=[],
        name_mapping={
            "excluded": "excluded",
            "level": "level",
            "orientation": "orientation",
            "position": "position",
            "text": "text",
            "type": "type",
        },
    )
    class SectionalElementProperty:
        def __init__(
            self,
            *,
            excluded: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            level: typing.Optional[jsii.Number] = None,
            orientation: typing.Optional[builtins.str] = None,
            position: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.FieldPositionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            text: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``SectionalElement`` property specifies the configuration information for a visual helper element for a form.

            A sectional element can be a header, a text block, or a divider. These elements are static and not associated with any data.

            :param excluded: Excludes a sectional element that was generated by default for a specified data model.
            :param level: Specifies the size of the font for a ``Heading`` sectional element. Valid values are ``1 | 2 | 3 | 4 | 5 | 6`` .
            :param orientation: Specifies the orientation for a ``Divider`` sectional element. Valid values are ``horizontal`` or ``vertical`` .
            :param position: Specifies the position of the text in a field for a ``Text`` sectional element.
            :param text: The text for a ``Text`` sectional element.
            :param type: The type of sectional element. Valid values are ``Heading`` , ``Text`` , and ``Divider`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-sectionalelement.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                sectional_element_property = amplifyuibuilder_mixins.CfnFormPropsMixin.SectionalElementProperty(
                    excluded=False,
                    level=123,
                    orientation="orientation",
                    position=amplifyuibuilder_mixins.CfnFormPropsMixin.FieldPositionProperty(
                        below="below",
                        fixed="fixed",
                        right_of="rightOf"
                    ),
                    text="text",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3f7ea88dead93d2f519412d4fb3b7e160430ef1db716ed76d7e88495597b4710)
                check_type(argname="argument excluded", value=excluded, expected_type=type_hints["excluded"])
                check_type(argname="argument level", value=level, expected_type=type_hints["level"])
                check_type(argname="argument orientation", value=orientation, expected_type=type_hints["orientation"])
                check_type(argname="argument position", value=position, expected_type=type_hints["position"])
                check_type(argname="argument text", value=text, expected_type=type_hints["text"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if excluded is not None:
                self._values["excluded"] = excluded
            if level is not None:
                self._values["level"] = level
            if orientation is not None:
                self._values["orientation"] = orientation
            if position is not None:
                self._values["position"] = position
            if text is not None:
                self._values["text"] = text
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def excluded(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Excludes a sectional element that was generated by default for a specified data model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-sectionalelement.html#cfn-amplifyuibuilder-form-sectionalelement-excluded
            '''
            result = self._values.get("excluded")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def level(self) -> typing.Optional[jsii.Number]:
            '''Specifies the size of the font for a ``Heading`` sectional element.

            Valid values are ``1 | 2 | 3 | 4 | 5 | 6`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-sectionalelement.html#cfn-amplifyuibuilder-form-sectionalelement-level
            '''
            result = self._values.get("level")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def orientation(self) -> typing.Optional[builtins.str]:
            '''Specifies the orientation for a ``Divider`` sectional element.

            Valid values are ``horizontal`` or ``vertical`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-sectionalelement.html#cfn-amplifyuibuilder-form-sectionalelement-orientation
            '''
            result = self._values.get("orientation")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def position(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FieldPositionProperty"]]:
            '''Specifies the position of the text in a field for a ``Text`` sectional element.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-sectionalelement.html#cfn-amplifyuibuilder-form-sectionalelement-position
            '''
            result = self._values.get("position")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FieldPositionProperty"]], result)

        @builtins.property
        def text(self) -> typing.Optional[builtins.str]:
            '''The text for a ``Text`` sectional element.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-sectionalelement.html#cfn-amplifyuibuilder-form-sectionalelement-text
            '''
            result = self._values.get("text")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of sectional element.

            Valid values are ``Heading`` , ``Text`` , and ``Divider`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-sectionalelement.html#cfn-amplifyuibuilder-form-sectionalelement-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SectionalElementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnFormPropsMixin.ValueMappingProperty",
        jsii_struct_bases=[],
        name_mapping={"display_value": "displayValue", "value": "value"},
    )
    class ValueMappingProperty:
        def __init__(
            self,
            *,
            display_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.FormInputValuePropertyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.FormInputValuePropertyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The ``ValueMapping`` property specifies the association between a complex object and a display value.

            Use ``ValueMapping`` to store how to represent complex objects when they are displayed.

            :param display_value: The value to display for the complex object.
            :param value: The complex object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-valuemapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                # form_input_value_property_property_: amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyProperty
                
                value_mapping_property = amplifyuibuilder_mixins.CfnFormPropsMixin.ValueMappingProperty(
                    display_value=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyProperty(
                        binding_properties=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyBindingPropertiesProperty(
                            field="field",
                            property="property"
                        ),
                        concat=[form_input_value_property_property_],
                        value="value"
                    ),
                    value=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyProperty(
                        binding_properties=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyBindingPropertiesProperty(
                            field="field",
                            property="property"
                        ),
                        concat=[form_input_value_property_property_],
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fec3af6a6f004dc8595aa679fca3ba974f2ff5e584f355dd140b3d7d736287fa)
                check_type(argname="argument display_value", value=display_value, expected_type=type_hints["display_value"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if display_value is not None:
                self._values["display_value"] = display_value
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def display_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormInputValuePropertyProperty"]]:
            '''The value to display for the complex object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-valuemapping.html#cfn-amplifyuibuilder-form-valuemapping-displayvalue
            '''
            result = self._values.get("display_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormInputValuePropertyProperty"]], result)

        @builtins.property
        def value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormInputValuePropertyProperty"]]:
            '''The complex object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-valuemapping.html#cfn-amplifyuibuilder-form-valuemapping-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormInputValuePropertyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ValueMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnFormPropsMixin.ValueMappingsProperty",
        jsii_struct_bases=[],
        name_mapping={"binding_properties": "bindingProperties", "values": "values"},
    )
    class ValueMappingsProperty:
        def __init__(
            self,
            *,
            binding_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.FormInputBindingPropertiesValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            values: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFormPropsMixin.ValueMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``ValueMappings`` property specifies the data binding configuration for a value map.

            :param binding_properties: The information to bind fields to data at runtime.
            :param values: The value and display value pairs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-valuemappings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                # form_input_value_property_property_: amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyProperty
                
                value_mappings_property = amplifyuibuilder_mixins.CfnFormPropsMixin.ValueMappingsProperty(
                    binding_properties={
                        "binding_properties_key": amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputBindingPropertiesValueProperty(
                            binding_properties=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputBindingPropertiesValuePropertiesProperty(
                                model="model"
                            ),
                            type="type"
                        )
                    },
                    values=[amplifyuibuilder_mixins.CfnFormPropsMixin.ValueMappingProperty(
                        display_value=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyProperty(
                            binding_properties=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyBindingPropertiesProperty(
                                field="field",
                                property="property"
                            ),
                            concat=[form_input_value_property_property_],
                            value="value"
                        ),
                        value=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyProperty(
                            binding_properties=amplifyuibuilder_mixins.CfnFormPropsMixin.FormInputValuePropertyBindingPropertiesProperty(
                                field="field",
                                property="property"
                            ),
                            concat=[form_input_value_property_property_],
                            value="value"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__106ab4707f83b4f05f958601cbc625ca6c9d11fac4a718f05cbacf8834b9bc32)
                check_type(argname="argument binding_properties", value=binding_properties, expected_type=type_hints["binding_properties"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if binding_properties is not None:
                self._values["binding_properties"] = binding_properties
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def binding_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormInputBindingPropertiesValueProperty"]]]]:
            '''The information to bind fields to data at runtime.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-valuemappings.html#cfn-amplifyuibuilder-form-valuemappings-bindingproperties
            '''
            result = self._values.get("binding_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.FormInputBindingPropertiesValueProperty"]]]], result)

        @builtins.property
        def values(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.ValueMappingProperty"]]]]:
            '''The value and display value pairs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-valuemappings.html#cfn-amplifyuibuilder-form-valuemappings-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFormPropsMixin.ValueMappingProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ValueMappingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnThemeMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_id": "appId",
        "environment_name": "environmentName",
        "name": "name",
        "overrides": "overrides",
        "tags": "tags",
        "values": "values",
    },
)
class CfnThemeMixinProps:
    def __init__(
        self,
        *,
        app_id: typing.Optional[builtins.str] = None,
        environment_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnThemePropsMixin.ThemeValuesProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        values: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnThemePropsMixin.ThemeValuesProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnThemePropsMixin.

        :param app_id: The unique ID for the Amplify app associated with the theme.
        :param environment_name: The name of the backend environment that is a part of the Amplify app.
        :param name: The name of the theme.
        :param overrides: Describes the properties that can be overriden to customize a theme.
        :param tags: One or more key-value pairs to use when tagging the theme.
        :param values: A list of key-value pairs that defines the properties of the theme.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
            
            # theme_values_property_: amplifyuibuilder_mixins.CfnThemePropsMixin.ThemeValuesProperty
            
            cfn_theme_mixin_props = amplifyuibuilder_mixins.CfnThemeMixinProps(
                app_id="appId",
                environment_name="environmentName",
                name="name",
                overrides=[amplifyuibuilder_mixins.CfnThemePropsMixin.ThemeValuesProperty(
                    key="key",
                    value=amplifyuibuilder_mixins.CfnThemePropsMixin.ThemeValueProperty(
                        children=[theme_values_property_],
                        value="value"
                    )
                )],
                tags={
                    "tags_key": "tags"
                },
                values=[amplifyuibuilder_mixins.CfnThemePropsMixin.ThemeValuesProperty(
                    key="key",
                    value=amplifyuibuilder_mixins.CfnThemePropsMixin.ThemeValueProperty(
                        children=[theme_values_property_],
                        value="value"
                    )
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__260a9d2b27341e20784bcbcedaf1e472ff12526c4ca455f38e47dba5d3b00dd1)
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
            check_type(argname="argument environment_name", value=environment_name, expected_type=type_hints["environment_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if app_id is not None:
            self._values["app_id"] = app_id
        if environment_name is not None:
            self._values["environment_name"] = environment_name
        if name is not None:
            self._values["name"] = name
        if overrides is not None:
            self._values["overrides"] = overrides
        if tags is not None:
            self._values["tags"] = tags
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def app_id(self) -> typing.Optional[builtins.str]:
        '''The unique ID for the Amplify app associated with the theme.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html#cfn-amplifyuibuilder-theme-appid
        '''
        result = self._values.get("app_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_name(self) -> typing.Optional[builtins.str]:
        '''The name of the backend environment that is a part of the Amplify app.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html#cfn-amplifyuibuilder-theme-environmentname
        '''
        result = self._values.get("environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the theme.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html#cfn-amplifyuibuilder-theme-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def overrides(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnThemePropsMixin.ThemeValuesProperty"]]]]:
        '''Describes the properties that can be overriden to customize a theme.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html#cfn-amplifyuibuilder-theme-overrides
        '''
        result = self._values.get("overrides")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnThemePropsMixin.ThemeValuesProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''One or more key-value pairs to use when tagging the theme.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html#cfn-amplifyuibuilder-theme-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def values(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnThemePropsMixin.ThemeValuesProperty"]]]]:
        '''A list of key-value pairs that defines the properties of the theme.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html#cfn-amplifyuibuilder-theme-values
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnThemePropsMixin.ThemeValuesProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnThemeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnThemePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnThemePropsMixin",
):
    '''The AWS::AmplifyUIBuilder::Theme resource specifies a theme within an Amplify app.

    A theme is a collection of style settings that apply globally to the components associated with the app.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html
    :cloudformationResource: AWS::AmplifyUIBuilder::Theme
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
        
        # theme_values_property_: amplifyuibuilder_mixins.CfnThemePropsMixin.ThemeValuesProperty
        
        cfn_theme_props_mixin = amplifyuibuilder_mixins.CfnThemePropsMixin(amplifyuibuilder_mixins.CfnThemeMixinProps(
            app_id="appId",
            environment_name="environmentName",
            name="name",
            overrides=[amplifyuibuilder_mixins.CfnThemePropsMixin.ThemeValuesProperty(
                key="key",
                value=amplifyuibuilder_mixins.CfnThemePropsMixin.ThemeValueProperty(
                    children=[theme_values_property_],
                    value="value"
                )
            )],
            tags={
                "tags_key": "tags"
            },
            values=[amplifyuibuilder_mixins.CfnThemePropsMixin.ThemeValuesProperty(
                key="key",
                value=amplifyuibuilder_mixins.CfnThemePropsMixin.ThemeValueProperty(
                    children=[theme_values_property_],
                    value="value"
                )
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnThemeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AmplifyUIBuilder::Theme``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__935284a973e72598b24fdc3be5a17dde28d6fc2646d6d57dc265a248956aa46f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23984a2612dc86401c9322e48d8ff824c0f3f30d7a1232a108382096bff84796)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83d389a9167a7b227220c1010ed6906060c374f0fc0b283b340fc443a32b8103)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnThemeMixinProps:
        return typing.cast(CfnThemeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnThemePropsMixin.ThemeValueProperty",
        jsii_struct_bases=[],
        name_mapping={"children": "children", "value": "value"},
    )
    class ThemeValueProperty:
        def __init__(
            self,
            *,
            children: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnThemePropsMixin.ThemeValuesProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``ThemeValue`` property specifies the configuration of a theme's properties.

            :param children: A list of key-value pairs that define the theme's properties.
            :param value: The value of a theme property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-theme-themevalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                # theme_value_property_: amplifyuibuilder_mixins.CfnThemePropsMixin.ThemeValueProperty
                
                theme_value_property = amplifyuibuilder_mixins.CfnThemePropsMixin.ThemeValueProperty(
                    children=[amplifyuibuilder_mixins.CfnThemePropsMixin.ThemeValuesProperty(
                        key="key",
                        value=theme_value_property_
                    )],
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2fe1230dac989fcbd90896d529894c3abfdf9cf0aabdecb436a3fe14ffee2445)
                check_type(argname="argument children", value=children, expected_type=type_hints["children"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if children is not None:
                self._values["children"] = children
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def children(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnThemePropsMixin.ThemeValuesProperty"]]]]:
            '''A list of key-value pairs that define the theme's properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-theme-themevalue.html#cfn-amplifyuibuilder-theme-themevalue-children
            '''
            result = self._values.get("children")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnThemePropsMixin.ThemeValuesProperty"]]]], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of a theme property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-theme-themevalue.html#cfn-amplifyuibuilder-theme-themevalue-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ThemeValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplifyuibuilder.mixins.CfnThemePropsMixin.ThemeValuesProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class ThemeValuesProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnThemePropsMixin.ThemeValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The ``ThemeValues`` property specifies key-value pair that defines a property of a theme.

            :param key: The name of the property.
            :param value: The value of the property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-theme-themevalues.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplifyuibuilder import mixins as amplifyuibuilder_mixins
                
                # theme_values_property_: amplifyuibuilder_mixins.CfnThemePropsMixin.ThemeValuesProperty
                
                theme_values_property = amplifyuibuilder_mixins.CfnThemePropsMixin.ThemeValuesProperty(
                    key="key",
                    value=amplifyuibuilder_mixins.CfnThemePropsMixin.ThemeValueProperty(
                        children=[theme_values_property_],
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__55e5cb1c151c19253ed918fb6731bede24f46314c0d983d428f9892d48dea6a7)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The name of the property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-theme-themevalues.html#cfn-amplifyuibuilder-theme-themevalues-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnThemePropsMixin.ThemeValueProperty"]]:
            '''The value of the property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-theme-themevalues.html#cfn-amplifyuibuilder-theme-themevalues-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnThemePropsMixin.ThemeValueProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ThemeValuesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnComponentMixinProps",
    "CfnComponentPropsMixin",
    "CfnFormMixinProps",
    "CfnFormPropsMixin",
    "CfnThemeMixinProps",
    "CfnThemePropsMixin",
]

publication.publish()

def _typecheckingstub__fb0992d109d1306a672dcaf87b9d036aa9c294ae6dacf8237f97f70830f8b0ea(
    *,
    app_id: typing.Optional[builtins.str] = None,
    binding_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ComponentBindingPropertiesValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    children: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ComponentChildProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    collection_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ComponentDataConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    component_type: typing.Optional[builtins.str] = None,
    environment_name: typing.Optional[builtins.str] = None,
    events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ComponentEventProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    overrides: typing.Any = None,
    properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    schema_version: typing.Optional[builtins.str] = None,
    source_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    variants: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ComponentVariantProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76b10e835be1c61a1cb925c5ac2a98579c7f3f15aa1e127cbc2a6d779daecf78(
    props: typing.Union[CfnComponentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f06e5f860dfe448712fec8a92c9be65373de771cf832e44f14c2b56de4aa381f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68a333f46df9ad5ca01373d28ce44c2eccc12100e6cf4810ddae04cb1e8dadb8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f11c49c91638ca3b1da4850aa07f77af6422d8b757f6c07afef2554b23e3c4(
    *,
    anchor: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    global_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    model: typing.Optional[builtins.str] = None,
    state: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.MutationActionSetStateParameterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    url: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b48edb398bcce45e30c68f2e0c03078482e850efbacbfcec93d8278e9bf5dc1(
    *,
    bucket: typing.Optional[builtins.str] = None,
    default_value: typing.Optional[builtins.str] = None,
    field: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    model: typing.Optional[builtins.str] = None,
    predicates: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.PredicateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    slot_name: typing.Optional[builtins.str] = None,
    user_attribute: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e41677d59bd5ee17f2ca9efc81445682eab9fa6996fdf3bb6360ce680189d7c8(
    *,
    binding_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ComponentBindingPropertiesValuePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_value: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433c5b4722fc814fa37ee9bda5cacae13692011d8f07374896954a86f0492e96(
    *,
    children: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ComponentChildProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    component_type: typing.Optional[builtins.str] = None,
    events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ComponentEventProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    source_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0cd03e39b58710890ee87a8093cd0564ba3758144c38a0ccd920847cc7cdebc(
    *,
    else_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    field: typing.Optional[builtins.str] = None,
    operand: typing.Optional[builtins.str] = None,
    operand_type: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    property: typing.Optional[builtins.str] = None,
    then: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc270cb61a77580fbc488b8f23b00de458a1c89d5c6b16e81dcde6ebfed1c00a(
    *,
    identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    model: typing.Optional[builtins.str] = None,
    predicate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.PredicateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sort: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.SortPropertyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__826e4fd2c0ed9b0db220022a029e44013b8170b28594d9d19e287c0d1e6d2adc(
    *,
    action: typing.Optional[builtins.str] = None,
    binding_event: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ActionParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ff393316f25d9f8f8a37a68e4fe1d35f183a32edd31e2bd8f69857815c022a(
    *,
    field: typing.Optional[builtins.str] = None,
    property: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__729c6ed5dec61997a562352acac9da23bfc007d47ced61f521c0df39f7debda0(
    *,
    binding_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    bindings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.FormBindingElementProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    collection_binding_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ComponentPropertyBindingPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    component_name: typing.Optional[builtins.str] = None,
    concat: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    condition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ComponentConditionPropertyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    configured: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    default_value: typing.Optional[builtins.str] = None,
    event: typing.Optional[builtins.str] = None,
    imported_value: typing.Optional[builtins.str] = None,
    model: typing.Optional[builtins.str] = None,
    property: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    user_attribute: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e16561f49623cbbc176fd841a3b4470aa08e6b88b3dd07110e603ba4c5b468c(
    *,
    overrides: typing.Any = None,
    variant_values: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf96a78f2a8ccf6cbeeed185ed40fe6aacc8f6983b397b703bc385ac66d841ed(
    *,
    element: typing.Optional[builtins.str] = None,
    property: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844937e0d4915ca6748b956c6cfaa7d7e423fba5288e063c8e8d5e1ee786c384(
    *,
    component_name: typing.Optional[builtins.str] = None,
    property: typing.Optional[builtins.str] = None,
    set: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1902498166b75004689994263c0751f658219e841bb1e6989e9d84cf36f4e4d9(
    *,
    and_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.PredicateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    field: typing.Optional[builtins.str] = None,
    operand: typing.Optional[builtins.str] = None,
    operand_type: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    or_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComponentPropsMixin.PredicateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a59648f6b1da5cfeaf152d2c9b3cca475cd4a984d20725b40b62020235e2621(
    *,
    direction: typing.Optional[builtins.str] = None,
    field: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7546b57c976bb5f3375bd76419a6f691c3bbaf5e246311406054c5fbf7f8e48(
    *,
    app_id: typing.Optional[builtins.str] = None,
    cta: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.FormCTAProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    data_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.FormDataTypeConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    environment_name: typing.Optional[builtins.str] = None,
    fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.FieldConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    form_action_type: typing.Optional[builtins.str] = None,
    label_decorator: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    schema_version: typing.Optional[builtins.str] = None,
    sectional_elements: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.SectionalElementProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    style: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.FormStyleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca3ee1cc4a7e681f7240b71db5b94853bcf9b69e05d9e1e142438015c2b37b67(
    props: typing.Union[CfnFormMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8600180f97a48dc6e94cad53d793f4d9190b76d198e1c5d45b29cc51ccbc733(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7907a142c9a6019e213cc424ba9ebaba3a1f4db42fa263d3c1be6ce9b349916b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d34a95e86d2f1bd28dc984f8908c8befdaacb7ac4e9d12808a2c52d6f1ee2c5(
    *,
    excluded: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    input_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.FieldInputConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    label: typing.Optional[builtins.str] = None,
    position: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.FieldPositionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    validations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.FieldValidationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a467e35b1e71c829d4a1d316c4445aad268511f47c3d09e076289ad491175795(
    *,
    default_checked: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    default_country_code: typing.Optional[builtins.str] = None,
    default_value: typing.Optional[builtins.str] = None,
    descriptive_text: typing.Optional[builtins.str] = None,
    file_uploader_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.FileUploaderFieldConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    is_array: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    max_value: typing.Optional[jsii.Number] = None,
    min_value: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    placeholder: typing.Optional[builtins.str] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    step: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
    value_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.ValueMappingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ee358e41d0004cf0f1cb46098a87b83c4a0a57e923e84d38ce0b18e8553595(
    *,
    below: typing.Optional[builtins.str] = None,
    fixed: typing.Optional[builtins.str] = None,
    right_of: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea302a6eadbb701d3ed34e2cd0403bc6ccedd673d82086cf59cf3c9b084817c2(
    *,
    num_values: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
    str_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
    validation_message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__257d526dab3fe8801e9a519843956fb9b24c245717a9b4526e26ffa1ffec8aa9(
    *,
    accepted_file_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    access_level: typing.Optional[builtins.str] = None,
    is_resumable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    max_file_count: typing.Optional[jsii.Number] = None,
    max_size: typing.Optional[jsii.Number] = None,
    show_thumbnails: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d643d5ca32cabc836a640d31c39e6db2825861cc2d9bc86f7545e04ce0ccad(
    *,
    children: typing.Optional[builtins.str] = None,
    excluded: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    position: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.FieldPositionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba45c3535b85b8c19e511a6a54efc9bd3db28f9e81f9504959b067f157f2745e(
    *,
    cancel: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.FormButtonProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    clear: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.FormButtonProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    position: typing.Optional[builtins.str] = None,
    submit: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.FormButtonProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6655352a521b2883ea7cebd1c33e1dd36a63478b2573796e281f71c6a7ad9ff(
    *,
    data_source_type: typing.Optional[builtins.str] = None,
    data_type_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d68e1b5b79c9ca5b8a30a3ce0f42c6cb77fded8bf1fbdcedbc1646e1b392c1ec(
    *,
    model: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f8ee3343832160c597d13f17df33e7f16741aaa320e092fc78699398cd7f92c(
    *,
    binding_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.FormInputBindingPropertiesValuePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__894df7000885b009bb3829053da05bc9f7217b816c07f39c4d430413fa5d032f(
    *,
    field: typing.Optional[builtins.str] = None,
    property: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61c5c2e5ba0a1c3a879bec3c62eff7b28b2dfd404b9e7e7c0e21344d78a14aba(
    *,
    binding_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.FormInputValuePropertyBindingPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    concat: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.FormInputValuePropertyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab642873ab5056a0b5075302f4a99c0cf8d948f6f27fed41fddbbf236c19859d(
    *,
    token_reference: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__524ff15f750a9eb0ecf255e4cd063f9e1d6b4773421d674582d7f6e7ea87e6dd(
    *,
    horizontal_gap: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.FormStyleConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    outer_padding: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.FormStyleConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vertical_gap: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.FormStyleConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f7ea88dead93d2f519412d4fb3b7e160430ef1db716ed76d7e88495597b4710(
    *,
    excluded: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    level: typing.Optional[jsii.Number] = None,
    orientation: typing.Optional[builtins.str] = None,
    position: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.FieldPositionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    text: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec3af6a6f004dc8595aa679fca3ba974f2ff5e584f355dd140b3d7d736287fa(
    *,
    display_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.FormInputValuePropertyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.FormInputValuePropertyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__106ab4707f83b4f05f958601cbc625ca6c9d11fac4a718f05cbacf8834b9bc32(
    *,
    binding_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.FormInputBindingPropertiesValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    values: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFormPropsMixin.ValueMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__260a9d2b27341e20784bcbcedaf1e472ff12526c4ca455f38e47dba5d3b00dd1(
    *,
    app_id: typing.Optional[builtins.str] = None,
    environment_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnThemePropsMixin.ThemeValuesProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    values: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnThemePropsMixin.ThemeValuesProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__935284a973e72598b24fdc3be5a17dde28d6fc2646d6d57dc265a248956aa46f(
    props: typing.Union[CfnThemeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23984a2612dc86401c9322e48d8ff824c0f3f30d7a1232a108382096bff84796(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83d389a9167a7b227220c1010ed6906060c374f0fc0b283b340fc443a32b8103(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe1230dac989fcbd90896d529894c3abfdf9cf0aabdecb436a3fe14ffee2445(
    *,
    children: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnThemePropsMixin.ThemeValuesProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e5cb1c151c19253ed918fb6731bede24f46314c0d983d428f9892d48dea6a7(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnThemePropsMixin.ThemeValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
