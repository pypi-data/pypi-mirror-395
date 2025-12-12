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

import constructs as _constructs_77d1e7e8
from ...core import IMixin as _IMixin_11e4b965, Mixin as _Mixin_a69446c0
from ...mixins import (
    CfnPropertyMixinOptions as _CfnPropertyMixinOptions_9cbff649,
    PropertyMergeStrategy as _PropertyMergeStrategy_49c157e8,
)


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalogappregistry.mixins.CfnApplicationMixinProps",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "name": "name", "tags": "tags"},
)
class CfnApplicationMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnApplicationPropsMixin.

        :param description: The description of the application.
        :param name: The name of the application. The name must be unique in the region in which you are creating the application.
        :param tags: Key-value pairs you can use to associate with the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicecatalogappregistry import mixins as servicecatalogappregistry_mixins
            
            cfn_application_mixin_props = servicecatalogappregistry_mixins.CfnApplicationMixinProps(
                description="description",
                name="name",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0422872a99f55b29b922acd2920e5606b564f970753a42e5efc38e12e27afd0a)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-application.html#cfn-servicecatalogappregistry-application-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the application.

        The name must be unique in the region in which you are creating the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-application.html#cfn-servicecatalogappregistry-application-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Key-value pairs you can use to associate with the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-application.html#cfn-servicecatalogappregistry-application-tags
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
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalogappregistry.mixins.CfnApplicationPropsMixin",
):
    '''Represents a AWS Service Catalog AppRegistry application that is the top-level node in a hierarchy of related cloud resource abstractions.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-application.html
    :cloudformationResource: AWS::ServiceCatalogAppRegistry::Application
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicecatalogappregistry import mixins as servicecatalogappregistry_mixins
        
        cfn_application_props_mixin = servicecatalogappregistry_mixins.CfnApplicationPropsMixin(servicecatalogappregistry_mixins.CfnApplicationMixinProps(
            description="description",
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
        props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceCatalogAppRegistry::Application``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4742f54e85fef5b2999bb8c623fd9fdad5e8d6eab3daf4956394081ead38e3d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46772f1029c6d033e5e9641e0fd8cace862bf15407a7af044496551c1ff6db2e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d85943edf0298e2216f9bd3488748df2a429d5ffb42ddfa853e1d1d30b4cbfcc)
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
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalogappregistry.mixins.CfnAttributeGroupAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={"application": "application", "attribute_group": "attributeGroup"},
)
class CfnAttributeGroupAssociationMixinProps:
    def __init__(
        self,
        *,
        application: typing.Optional[builtins.str] = None,
        attribute_group: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAttributeGroupAssociationPropsMixin.

        :param application: The name or ID of the application.
        :param attribute_group: The name or ID of the attribute group which holds the attributes that describe the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroupassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicecatalogappregistry import mixins as servicecatalogappregistry_mixins
            
            cfn_attribute_group_association_mixin_props = servicecatalogappregistry_mixins.CfnAttributeGroupAssociationMixinProps(
                application="application",
                attribute_group="attributeGroup"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0d794ce4872f9b2eae7a7fc6ce9b2143244534a4f446b39f5ff98ad4c544812)
            check_type(argname="argument application", value=application, expected_type=type_hints["application"])
            check_type(argname="argument attribute_group", value=attribute_group, expected_type=type_hints["attribute_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application is not None:
            self._values["application"] = application
        if attribute_group is not None:
            self._values["attribute_group"] = attribute_group

    @builtins.property
    def application(self) -> typing.Optional[builtins.str]:
        '''The name or ID of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroupassociation.html#cfn-servicecatalogappregistry-attributegroupassociation-application
        '''
        result = self._values.get("application")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attribute_group(self) -> typing.Optional[builtins.str]:
        '''The name or ID of the attribute group which holds the attributes that describe the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroupassociation.html#cfn-servicecatalogappregistry-attributegroupassociation-attributegroup
        '''
        result = self._values.get("attribute_group")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAttributeGroupAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAttributeGroupAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalogappregistry.mixins.CfnAttributeGroupAssociationPropsMixin",
):
    '''Associates an attribute group with an application to augment the application's metadata with the group's attributes.

    This feature enables applications to be described with user-defined details that are machine-readable, such as third-party integrations.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroupassociation.html
    :cloudformationResource: AWS::ServiceCatalogAppRegistry::AttributeGroupAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicecatalogappregistry import mixins as servicecatalogappregistry_mixins
        
        cfn_attribute_group_association_props_mixin = servicecatalogappregistry_mixins.CfnAttributeGroupAssociationPropsMixin(servicecatalogappregistry_mixins.CfnAttributeGroupAssociationMixinProps(
            application="application",
            attribute_group="attributeGroup"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAttributeGroupAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceCatalogAppRegistry::AttributeGroupAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c01b491ebbfb54647b7e308eedab094f305d55ac42faaa5d18147190b2b3784)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78dddf83b3d087c96e94b566b682b6a9ddf813615dc289ee3cda2497500ec237)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87f843e234939e53bb79f51be327b6bdeb506c0619696b1612151614a7040d3b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAttributeGroupAssociationMixinProps:
        return typing.cast(CfnAttributeGroupAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalogappregistry.mixins.CfnAttributeGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "attributes": "attributes",
        "description": "description",
        "name": "name",
        "tags": "tags",
    },
)
class CfnAttributeGroupMixinProps:
    def __init__(
        self,
        *,
        attributes: typing.Any = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnAttributeGroupPropsMixin.

        :param attributes: A nested object in a JSON or YAML template that supports arbitrary definitions. Represents the attributes in an attribute group that describes an application and its components.
        :param description: The description of the attribute group that the user provides.
        :param name: The name of the attribute group.
        :param tags: Key-value pairs you can use to associate with the attribute group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicecatalogappregistry import mixins as servicecatalogappregistry_mixins
            
            # attributes: Any
            
            cfn_attribute_group_mixin_props = servicecatalogappregistry_mixins.CfnAttributeGroupMixinProps(
                attributes=attributes,
                description="description",
                name="name",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a0a0297b55537ca7ead767c0d93747ae35626fac59bd8352a5b1b2726118f33)
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attributes is not None:
            self._values["attributes"] = attributes
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def attributes(self) -> typing.Any:
        '''A nested object in a JSON or YAML template that supports arbitrary definitions.

        Represents the attributes in an attribute group that describes an application and its components.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html#cfn-servicecatalogappregistry-attributegroup-attributes
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Any, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the attribute group that the user provides.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html#cfn-servicecatalogappregistry-attributegroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the attribute group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html#cfn-servicecatalogappregistry-attributegroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Key-value pairs you can use to associate with the attribute group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html#cfn-servicecatalogappregistry-attributegroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAttributeGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAttributeGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalogappregistry.mixins.CfnAttributeGroupPropsMixin",
):
    '''Creates a new attribute group as a container for user-defined attributes.

    This feature enables users to have full control over their cloud application's metadata in a rich machine-readable format to facilitate integration with automated workflows and third-party tools.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html
    :cloudformationResource: AWS::ServiceCatalogAppRegistry::AttributeGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicecatalogappregistry import mixins as servicecatalogappregistry_mixins
        
        # attributes: Any
        
        cfn_attribute_group_props_mixin = servicecatalogappregistry_mixins.CfnAttributeGroupPropsMixin(servicecatalogappregistry_mixins.CfnAttributeGroupMixinProps(
            attributes=attributes,
            description="description",
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
        props: typing.Union[CfnAttributeGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceCatalogAppRegistry::AttributeGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37e388395376872b6aea372cea0cf7fddc4fea05bbf1a3fac0024acd5827e48c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__96ad12fcc5af1f09f539539c35f7e90ab88868b50c68aa6b6dd9c6e0875b54f9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__207910721846f126ac642b683390b97157325bf8e5e7ffc2a47b31cdff521dba)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAttributeGroupMixinProps:
        return typing.cast(CfnAttributeGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalogappregistry.mixins.CfnResourceAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application": "application",
        "resource": "resource",
        "resource_type": "resourceType",
    },
)
class CfnResourceAssociationMixinProps:
    def __init__(
        self,
        *,
        application: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnResourceAssociationPropsMixin.

        :param application: The name or ID of the application.
        :param resource: The name or ID of the resource of which the application will be associated.
        :param resource_type: The type of resource of which the application will be associated.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-resourceassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicecatalogappregistry import mixins as servicecatalogappregistry_mixins
            
            cfn_resource_association_mixin_props = servicecatalogappregistry_mixins.CfnResourceAssociationMixinProps(
                application="application",
                resource="resource",
                resource_type="resourceType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d2e66d890e42393ed33708b3eb9868e2cba217718f8458053e3c2682fb9f831)
            check_type(argname="argument application", value=application, expected_type=type_hints["application"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application is not None:
            self._values["application"] = application
        if resource is not None:
            self._values["resource"] = resource
        if resource_type is not None:
            self._values["resource_type"] = resource_type

    @builtins.property
    def application(self) -> typing.Optional[builtins.str]:
        '''The name or ID of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-resourceassociation.html#cfn-servicecatalogappregistry-resourceassociation-application
        '''
        result = self._values.get("application")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.str]:
        '''The name or ID of the resource of which the application will be associated.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-resourceassociation.html#cfn-servicecatalogappregistry-resourceassociation-resource
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''The type of resource of which the application will be associated.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-resourceassociation.html#cfn-servicecatalogappregistry-resourceassociation-resourcetype
        '''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResourceAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalogappregistry.mixins.CfnResourceAssociationPropsMixin",
):
    '''Associates a resource with an application.

    Both the resource and the application can be specified either by ID or name.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-resourceassociation.html
    :cloudformationResource: AWS::ServiceCatalogAppRegistry::ResourceAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicecatalogappregistry import mixins as servicecatalogappregistry_mixins
        
        cfn_resource_association_props_mixin = servicecatalogappregistry_mixins.CfnResourceAssociationPropsMixin(servicecatalogappregistry_mixins.CfnResourceAssociationMixinProps(
            application="application",
            resource="resource",
            resource_type="resourceType"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResourceAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceCatalogAppRegistry::ResourceAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14a3cf655a323e90c3c4bff59a85e6cfc6baab81e8954d5c2516a3ed0d7f12db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__faa2e73ac064d1a6bfd902e02dfb550cba30f3cc41eb00f5ab3aeeb457631e01)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2387aeb48a3e7bc94a9afa55fe4032ad1c6a67ab17782f5d3e64548785ef30c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResourceAssociationMixinProps:
        return typing.cast(CfnResourceAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnApplicationMixinProps",
    "CfnApplicationPropsMixin",
    "CfnAttributeGroupAssociationMixinProps",
    "CfnAttributeGroupAssociationPropsMixin",
    "CfnAttributeGroupMixinProps",
    "CfnAttributeGroupPropsMixin",
    "CfnResourceAssociationMixinProps",
    "CfnResourceAssociationPropsMixin",
]

publication.publish()

def _typecheckingstub__0422872a99f55b29b922acd2920e5606b564f970753a42e5efc38e12e27afd0a(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4742f54e85fef5b2999bb8c623fd9fdad5e8d6eab3daf4956394081ead38e3d1(
    props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46772f1029c6d033e5e9641e0fd8cace862bf15407a7af044496551c1ff6db2e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d85943edf0298e2216f9bd3488748df2a429d5ffb42ddfa853e1d1d30b4cbfcc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0d794ce4872f9b2eae7a7fc6ce9b2143244534a4f446b39f5ff98ad4c544812(
    *,
    application: typing.Optional[builtins.str] = None,
    attribute_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c01b491ebbfb54647b7e308eedab094f305d55ac42faaa5d18147190b2b3784(
    props: typing.Union[CfnAttributeGroupAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78dddf83b3d087c96e94b566b682b6a9ddf813615dc289ee3cda2497500ec237(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f843e234939e53bb79f51be327b6bdeb506c0619696b1612151614a7040d3b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a0a0297b55537ca7ead767c0d93747ae35626fac59bd8352a5b1b2726118f33(
    *,
    attributes: typing.Any = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e388395376872b6aea372cea0cf7fddc4fea05bbf1a3fac0024acd5827e48c(
    props: typing.Union[CfnAttributeGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ad12fcc5af1f09f539539c35f7e90ab88868b50c68aa6b6dd9c6e0875b54f9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__207910721846f126ac642b683390b97157325bf8e5e7ffc2a47b31cdff521dba(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d2e66d890e42393ed33708b3eb9868e2cba217718f8458053e3c2682fb9f831(
    *,
    application: typing.Optional[builtins.str] = None,
    resource: typing.Optional[builtins.str] = None,
    resource_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14a3cf655a323e90c3c4bff59a85e6cfc6baab81e8954d5c2516a3ed0d7f12db(
    props: typing.Union[CfnResourceAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faa2e73ac064d1a6bfd902e02dfb550cba30f3cc41eb00f5ab3aeeb457631e01(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2387aeb48a3e7bc94a9afa55fe4032ad1c6a67ab17782f5d3e64548785ef30c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
