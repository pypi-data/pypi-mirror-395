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
    jsii_type="@aws-cdk/mixins-preview.aws_resourcegroups.mixins.CfnGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration": "configuration",
        "description": "description",
        "name": "name",
        "resource_query": "resourceQuery",
        "resources": "resources",
        "tags": "tags",
    },
)
class CfnGroupMixinProps:
    def __init__(
        self,
        *,
        configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGroupPropsMixin.ConfigurationItemProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        resource_query: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGroupPropsMixin.ResourceQueryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnGroupPropsMixin.

        :param configuration: The service configuration currently associated with the resource group and in effect for the members of the resource group. A ``Configuration`` consists of one or more ``ConfigurationItem`` entries. For information about service configurations for resource groups and how to construct them, see `Service configurations for resource groups <https://docs.aws.amazon.com//ARG/latest/APIReference/about-slg.html>`_ in the *AWS Resource Groups User Guide* . .. epigraph:: You can include either a ``Configuration`` or a ``ResourceQuery`` , but not both.
        :param description: The description of the resource group.
        :param name: The name of a resource group. The name must be unique within the AWS Region in which you create the resource. To create multiple resource groups based on the same CloudFormation stack, you must generate unique names for each.
        :param resource_query: The resource query structure that is used to dynamically determine which AWS resources are members of the associated resource group. For more information about queries and how to construct them, see `Build queries and groups in AWS Resource Groups <https://docs.aws.amazon.com//ARG/latest/userguide/gettingstarted-query.html>`_ in the *AWS Resource Groups User Guide* .. epigraph:: - You can include either a ``ResourceQuery`` or a ``Configuration`` , but not both. - You can specify the group's membership either by using a ``ResourceQuery`` or by using a list of ``Resources`` , but not both.
        :param resources: A list of the Amazon Resource Names (ARNs) of AWS resources that you want to add to the specified group. .. epigraph:: - You can specify the group membership either by using a list of ``Resources`` or by using a ``ResourceQuery`` , but not both. - You can include a ``Resources`` property only if you also specify a ``Configuration`` property.
        :param tags: The tag key and value pairs that are attached to the resource group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_resourcegroups import mixins as resourcegroups_mixins
            
            cfn_group_mixin_props = resourcegroups_mixins.CfnGroupMixinProps(
                configuration=[resourcegroups_mixins.CfnGroupPropsMixin.ConfigurationItemProperty(
                    parameters=[resourcegroups_mixins.CfnGroupPropsMixin.ConfigurationParameterProperty(
                        name="name",
                        values=["values"]
                    )],
                    type="type"
                )],
                description="description",
                name="name",
                resource_query=resourcegroups_mixins.CfnGroupPropsMixin.ResourceQueryProperty(
                    query=resourcegroups_mixins.CfnGroupPropsMixin.QueryProperty(
                        resource_type_filters=["resourceTypeFilters"],
                        stack_identifier="stackIdentifier",
                        tag_filters=[resourcegroups_mixins.CfnGroupPropsMixin.TagFilterProperty(
                            key="key",
                            values=["values"]
                        )]
                    ),
                    type="type"
                ),
                resources=["resources"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92e4dd43decd8695ecc205b4fa24fd930e6aee107eaa67db44c9a86dede0665f)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_query", value=resource_query, expected_type=type_hints["resource_query"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration is not None:
            self._values["configuration"] = configuration
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if resource_query is not None:
            self._values["resource_query"] = resource_query
        if resources is not None:
            self._values["resources"] = resources
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGroupPropsMixin.ConfigurationItemProperty"]]]]:
        '''The service configuration currently associated with the resource group and in effect for the members of the resource group.

        A ``Configuration`` consists of one or more ``ConfigurationItem`` entries. For information about service configurations for resource groups and how to construct them, see `Service configurations for resource groups <https://docs.aws.amazon.com//ARG/latest/APIReference/about-slg.html>`_ in the *AWS Resource Groups User Guide* .
        .. epigraph::

           You can include either a ``Configuration`` or a ``ResourceQuery`` , but not both.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGroupPropsMixin.ConfigurationItemProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the resource group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of a resource group.

        The name must be unique within the AWS Region in which you create the resource. To create multiple resource groups based on the same CloudFormation stack, you must generate unique names for each.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_query(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGroupPropsMixin.ResourceQueryProperty"]]:
        '''The resource query structure that is used to dynamically determine which AWS resources are members of the associated resource group.

        For more information about queries and how to construct them, see `Build queries and groups in AWS Resource Groups <https://docs.aws.amazon.com//ARG/latest/userguide/gettingstarted-query.html>`_ in the *AWS Resource Groups User Guide*
        .. epigraph::

           - You can include either a ``ResourceQuery`` or a ``Configuration`` , but not both.
           - You can specify the group's membership either by using a ``ResourceQuery`` or by using a list of ``Resources`` , but not both.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-resourcequery
        '''
        result = self._values.get("resource_query")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGroupPropsMixin.ResourceQueryProperty"]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of the Amazon Resource Names (ARNs) of AWS resources that you want to add to the specified group.

        .. epigraph::

           - You can specify the group membership either by using a list of ``Resources`` or by using a ``ResourceQuery`` , but not both.
           - You can include a ``Resources`` property only if you also specify a ``Configuration`` property.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-resources
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tag key and value pairs that are attached to the resource group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_resourcegroups.mixins.CfnGroupPropsMixin",
):
    '''Creates a resource group with the specified name and description.

    You can optionally include either a resource query or a service configuration. For more information about constructing a resource query, see `Build queries and groups in AWS Resource Groups <https://docs.aws.amazon.com//ARG/latest/userguide/getting_started-query.html>`_ in the *AWS Resource Groups User Guide* . For more information about service-linked groups and service configurations, see `Service configurations for Resource Groups <https://docs.aws.amazon.com//ARG/latest/APIReference/about-slg.html>`_ .

    *Minimum permissions*

    To run this command, you must have the following permissions:

    - ``resource-groups:CreateGroup``

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html
    :cloudformationResource: AWS::ResourceGroups::Group
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_resourcegroups import mixins as resourcegroups_mixins
        
        cfn_group_props_mixin = resourcegroups_mixins.CfnGroupPropsMixin(resourcegroups_mixins.CfnGroupMixinProps(
            configuration=[resourcegroups_mixins.CfnGroupPropsMixin.ConfigurationItemProperty(
                parameters=[resourcegroups_mixins.CfnGroupPropsMixin.ConfigurationParameterProperty(
                    name="name",
                    values=["values"]
                )],
                type="type"
            )],
            description="description",
            name="name",
            resource_query=resourcegroups_mixins.CfnGroupPropsMixin.ResourceQueryProperty(
                query=resourcegroups_mixins.CfnGroupPropsMixin.QueryProperty(
                    resource_type_filters=["resourceTypeFilters"],
                    stack_identifier="stackIdentifier",
                    tag_filters=[resourcegroups_mixins.CfnGroupPropsMixin.TagFilterProperty(
                        key="key",
                        values=["values"]
                    )]
                ),
                type="type"
            ),
            resources=["resources"],
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
        props: typing.Union[CfnGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ResourceGroups::Group``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f6f4b7f4145f2293b14765711578d17cde63181d761f18039fc0de42fee7adb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cbc55c57ebb890d0dbb863b4ad7f3f914ca55ecb5d819a0b41f12d459a5a959)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb7a89ed3f00bbe2181dd784f8c08885d66e5323b07bb16891b1b3c4b657b779)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGroupMixinProps:
        return typing.cast(CfnGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_resourcegroups.mixins.CfnGroupPropsMixin.ConfigurationItemProperty",
        jsii_struct_bases=[],
        name_mapping={"parameters": "parameters", "type": "type"},
    )
    class ConfigurationItemProperty:
        def __init__(
            self,
            *,
            parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGroupPropsMixin.ConfigurationParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''One of the items in the service configuration assigned to a resource group.

            A service configuration can consist of one or more items. For details service configurations and how to construct them, see `Service configurations for resource groups <https://docs.aws.amazon.com//ARG/latest/APIReference/about-slg.html>`_ in the *AWS Resource Groups User Guide* .

            :param parameters: A collection of parameters for this configuration item. For the list of parameters that you can use with each configuration item ``Type`` , see `Supported resource types and parameters <https://docs.aws.amazon.com//ARG/latest/APIReference/about-slg.html#about-slg-types>`_ in the *AWS Resource Groups User Guide* .
            :param type: Specifies the type of configuration item. Each item must have a unique value for type. For the list of the types that you can specify for a configuration item, see `Supported resource types and parameters <https://docs.aws.amazon.com//ARG/latest/APIReference/about-slg.html#about-slg-types>`_ in the *AWS Resource Groups User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-configurationitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_resourcegroups import mixins as resourcegroups_mixins
                
                configuration_item_property = resourcegroups_mixins.CfnGroupPropsMixin.ConfigurationItemProperty(
                    parameters=[resourcegroups_mixins.CfnGroupPropsMixin.ConfigurationParameterProperty(
                        name="name",
                        values=["values"]
                    )],
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2ce288b5141677c8e4b70eb54249333cb7cbd9fb62c5b84f23184c372ee04517)
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if parameters is not None:
                self._values["parameters"] = parameters
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGroupPropsMixin.ConfigurationParameterProperty"]]]]:
            '''A collection of parameters for this configuration item.

            For the list of parameters that you can use with each configuration item ``Type`` , see `Supported resource types and parameters <https://docs.aws.amazon.com//ARG/latest/APIReference/about-slg.html#about-slg-types>`_ in the *AWS Resource Groups User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-configurationitem.html#cfn-resourcegroups-group-configurationitem-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGroupPropsMixin.ConfigurationParameterProperty"]]]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of configuration item.

            Each item must have a unique value for type. For the list of the types that you can specify for a configuration item, see `Supported resource types and parameters <https://docs.aws.amazon.com//ARG/latest/APIReference/about-slg.html#about-slg-types>`_ in the *AWS Resource Groups User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-configurationitem.html#cfn-resourcegroups-group-configurationitem-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_resourcegroups.mixins.CfnGroupPropsMixin.ConfigurationParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "values": "values"},
    )
    class ConfigurationParameterProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''One parameter for a group configuration item.

            For details about service configurations and how to construct them, see `Service configurations for resource groups <https://docs.aws.amazon.com//ARG/latest/APIReference/about-slg.html>`_ in the *AWS Resource Groups User Guide* .

            :param name: The name of the group configuration parameter. For the list of parameters that you can use with each configuration item type, see `Supported resource types and parameters <https://docs.aws.amazon.com//ARG/latest/APIReference/about-slg.html#about-slg-types>`_ in the *AWS Resource Groups User Guide* .
            :param values: The value or values to be used for the specified parameter. For the list of values you can use with each parameter, see `Supported resource types and parameters <https://docs.aws.amazon.com//ARG/latest/APIReference/about-slg.html#about-slg-types>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-configurationparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_resourcegroups import mixins as resourcegroups_mixins
                
                configuration_parameter_property = resourcegroups_mixins.CfnGroupPropsMixin.ConfigurationParameterProperty(
                    name="name",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f77b21fe1dea18ade73dab435a86de43e6401a49ac91b97128b22db0b7511e7e)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the group configuration parameter.

            For the list of parameters that you can use with each configuration item type, see `Supported resource types and parameters <https://docs.aws.amazon.com//ARG/latest/APIReference/about-slg.html#about-slg-types>`_ in the *AWS Resource Groups User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-configurationparameter.html#cfn-resourcegroups-group-configurationparameter-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The value or values to be used for the specified parameter.

            For the list of values you can use with each parameter, see `Supported resource types and parameters <https://docs.aws.amazon.com//ARG/latest/APIReference/about-slg.html#about-slg-types>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-configurationparameter.html#cfn-resourcegroups-group-configurationparameter-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_resourcegroups.mixins.CfnGroupPropsMixin.QueryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "resource_type_filters": "resourceTypeFilters",
            "stack_identifier": "stackIdentifier",
            "tag_filters": "tagFilters",
        },
    )
    class QueryProperty:
        def __init__(
            self,
            *,
            resource_type_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
            stack_identifier: typing.Optional[builtins.str] = None,
            tag_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGroupPropsMixin.TagFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies details within a ``ResourceQuery`` structure that determines the membership of the resource group.

            The contents required in the ``Query`` structure are determined by the ``Type`` property of the containing ``ResourceQuery`` structure.

            :param resource_type_filters: Specifies limits to the types of resources that can be included in the resource group. For example, if ``ResourceTypeFilters`` is ``["AWS::EC2::Instance", "AWS::DynamoDB::Table"]`` , only EC2 instances or DynamoDB tables can be members of this resource group. The default value is ``["AWS::AllSupported"]`` .
            :param stack_identifier: Specifies the ARN of a CloudFormation stack. All supported resources of the CloudFormation stack are members of the resource group. If you don't specify an ARN, this parameter defaults to the current stack that you are defining, which means that all the resources of the current stack are grouped. You can specify a value for ``StackIdentifier`` only when the ``ResourceQuery.Type`` property is ``CLOUDFORMATION_STACK_1_0.``
            :param tag_filters: A list of key-value pair objects that limit which resources can be members of the resource group. This property is required when the ``ResourceQuery.Type`` property is ``TAG_FILTERS_1_0`` . A resource must have a tag that matches every filter that is provided in the ``TagFilters`` list.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-query.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_resourcegroups import mixins as resourcegroups_mixins
                
                query_property = resourcegroups_mixins.CfnGroupPropsMixin.QueryProperty(
                    resource_type_filters=["resourceTypeFilters"],
                    stack_identifier="stackIdentifier",
                    tag_filters=[resourcegroups_mixins.CfnGroupPropsMixin.TagFilterProperty(
                        key="key",
                        values=["values"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__89f49d82f98f0afb1d49bd5cecc5c2086adfbc6f37dab2da73c5d7a358fb25d0)
                check_type(argname="argument resource_type_filters", value=resource_type_filters, expected_type=type_hints["resource_type_filters"])
                check_type(argname="argument stack_identifier", value=stack_identifier, expected_type=type_hints["stack_identifier"])
                check_type(argname="argument tag_filters", value=tag_filters, expected_type=type_hints["tag_filters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_type_filters is not None:
                self._values["resource_type_filters"] = resource_type_filters
            if stack_identifier is not None:
                self._values["stack_identifier"] = stack_identifier
            if tag_filters is not None:
                self._values["tag_filters"] = tag_filters

        @builtins.property
        def resource_type_filters(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies limits to the types of resources that can be included in the resource group.

            For example, if ``ResourceTypeFilters`` is ``["AWS::EC2::Instance", "AWS::DynamoDB::Table"]`` , only EC2 instances or DynamoDB tables can be members of this resource group. The default value is ``["AWS::AllSupported"]`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-query.html#cfn-resourcegroups-group-query-resourcetypefilters
            '''
            result = self._values.get("resource_type_filters")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def stack_identifier(self) -> typing.Optional[builtins.str]:
            '''Specifies the ARN of a CloudFormation stack.

            All supported resources of the CloudFormation stack are members of the resource group. If you don't specify an ARN, this parameter defaults to the current stack that you are defining, which means that all the resources of the current stack are grouped.

            You can specify a value for ``StackIdentifier`` only when the ``ResourceQuery.Type`` property is ``CLOUDFORMATION_STACK_1_0.``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-query.html#cfn-resourcegroups-group-query-stackidentifier
            '''
            result = self._values.get("stack_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGroupPropsMixin.TagFilterProperty"]]]]:
            '''A list of key-value pair objects that limit which resources can be members of the resource group.

            This property is required when the ``ResourceQuery.Type`` property is ``TAG_FILTERS_1_0`` .

            A resource must have a tag that matches every filter that is provided in the ``TagFilters`` list.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-query.html#cfn-resourcegroups-group-query-tagfilters
            '''
            result = self._values.get("tag_filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGroupPropsMixin.TagFilterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_resourcegroups.mixins.CfnGroupPropsMixin.ResourceQueryProperty",
        jsii_struct_bases=[],
        name_mapping={"query": "query", "type": "type"},
    )
    class ResourceQueryProperty:
        def __init__(
            self,
            *,
            query: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGroupPropsMixin.QueryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The query used to dynamically define the members of a group.

            For more information about how to construct a query, see `Build queries and groups in AWS Resource Groups <https://docs.aws.amazon.com//ARG/latest/userguide/gettingstarted-query.html>`_ .

            :param query: The query that defines the membership of the group. This is a structure with properties that depend on the ``Type`` . The ``Query`` structure must be included in the following scenarios: - When the ``Type`` is ``TAG_FILTERS_1_0`` , you must specify a ``Query`` structure that contains a ``TagFilters`` list of tags. Resources with tags that match those in the ``TagFilter`` list become members of the resource group. - When the ``Type`` is ``CLOUDFORMATION_STACK_1_0`` then this field is required only when you must specify a CloudFormation stack other than the one you are defining. To do this, the ``Query`` structure must contain the ``StackIdentifier`` property. If you don't specify either a ``Query`` structure or a ``StackIdentifier`` within that ``Query`` , then it defaults to the CloudFormation stack that you're currently constructing.
            :param type: Specifies the type of resource query that determines this group's membership. There are two valid query types:. - ``TAG_FILTERS_1_0`` indicates that the group is a tag-based group. To complete the group membership, you must include the ``TagFilters`` property to specify the tag filters to use in the query. - ``CLOUDFORMATION_STACK_1_0`` , the default, indicates that the group is a CloudFormation stack-based group. Group membership is based on the CloudFormation stack. You must specify the ``StackIdentifier`` property in the query to define which stack to associate the group with, or leave it empty to default to the stack where the group is defined.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-resourcequery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_resourcegroups import mixins as resourcegroups_mixins
                
                resource_query_property = resourcegroups_mixins.CfnGroupPropsMixin.ResourceQueryProperty(
                    query=resourcegroups_mixins.CfnGroupPropsMixin.QueryProperty(
                        resource_type_filters=["resourceTypeFilters"],
                        stack_identifier="stackIdentifier",
                        tag_filters=[resourcegroups_mixins.CfnGroupPropsMixin.TagFilterProperty(
                            key="key",
                            values=["values"]
                        )]
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fbabfc6d2073e09b821a77331ec2128089eb61f23fa5ed48af6a0e63cd525886)
                check_type(argname="argument query", value=query, expected_type=type_hints["query"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if query is not None:
                self._values["query"] = query
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def query(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGroupPropsMixin.QueryProperty"]]:
            '''The query that defines the membership of the group.

            This is a structure with properties that depend on the ``Type`` .

            The ``Query`` structure must be included in the following scenarios:

            - When the ``Type`` is ``TAG_FILTERS_1_0`` , you must specify a ``Query`` structure that contains a ``TagFilters`` list of tags. Resources with tags that match those in the ``TagFilter`` list become members of the resource group.
            - When the ``Type`` is ``CLOUDFORMATION_STACK_1_0`` then this field is required only when you must specify a CloudFormation stack other than the one you are defining. To do this, the ``Query`` structure must contain the ``StackIdentifier`` property. If you don't specify either a ``Query`` structure or a ``StackIdentifier`` within that ``Query`` , then it defaults to the CloudFormation stack that you're currently constructing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-resourcequery.html#cfn-resourcegroups-group-resourcequery-query
            '''
            result = self._values.get("query")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGroupPropsMixin.QueryProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of resource query that determines this group's membership. There are two valid query types:.

            - ``TAG_FILTERS_1_0`` indicates that the group is a tag-based group. To complete the group membership, you must include the ``TagFilters`` property to specify the tag filters to use in the query.
            - ``CLOUDFORMATION_STACK_1_0`` , the default, indicates that the group is a CloudFormation stack-based group. Group membership is based on the CloudFormation stack. You must specify the ``StackIdentifier`` property in the query to define which stack to associate the group with, or leave it empty to default to the stack where the group is defined.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-resourcequery.html#cfn-resourcegroups-group-resourcequery-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceQueryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_resourcegroups.mixins.CfnGroupPropsMixin.TagFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "values": "values"},
    )
    class TagFilterProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies a single tag key and optional values that you can use to specify membership in a tag-based group.

            An AWS resource that doesn't have a matching tag key and value is rejected as a member of the group.

            A ``TagFilter`` object includes two properties: ``Key`` (a string) and ``Values`` (a list of strings). Only resources in the account that are tagged with a matching key-value pair are members of the group. The ``Values`` property of ``TagFilter`` is optional, but specifying it narrows the query results.

            As an example, suppose the ``TagFilters`` string is ``[{"Key": "Stage", "Values": ["Test", "Beta"]}, {"Key": "Storage"}]`` . In this case, only resources with all of the following tags are members of the group:

            - ``Stage`` tag key with a value of either ``Test`` or ``Beta``
            - ``Storage`` tag key with any value

            :param key: A string that defines a tag key. Only resources in the account that are tagged with a specified tag key are members of the tag-based resource group. This field is required when the ``ResourceQuery`` structure's ``Type`` property is ``TAG_FILTERS_1_0`` . You must specify at least one tag key.
            :param values: A list of tag values that can be included in the tag-based resource group. This is optional. If you don't specify a value or values for a key, then an AWS resource with any value for that key is a member.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-tagfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_resourcegroups import mixins as resourcegroups_mixins
                
                tag_filter_property = resourcegroups_mixins.CfnGroupPropsMixin.TagFilterProperty(
                    key="key",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b8f19630188736cb0d85abfb8c47427debd0de372a74f078a2bfcc4a409951c2)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''A string that defines a tag key.

            Only resources in the account that are tagged with a specified tag key are members of the tag-based resource group.

            This field is required when the ``ResourceQuery`` structure's ``Type`` property is ``TAG_FILTERS_1_0`` . You must specify at least one tag key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-tagfilter.html#cfn-resourcegroups-group-tagfilter-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of tag values that can be included in the tag-based resource group.

            This is optional. If you don't specify a value or values for a key, then an AWS resource with any value for that key is a member.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-tagfilter.html#cfn-resourcegroups-group-tagfilter-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_resourcegroups.mixins.CfnTagSyncTaskMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "group": "group",
        "role_arn": "roleArn",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CfnTagSyncTaskMixinProps:
    def __init__(
        self,
        *,
        group: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTagSyncTaskPropsMixin.

        :param group: The Amazon resource name (ARN) or name of the application group for which you want to create a tag-sync task.
        :param role_arn: The Amazon resource name (ARN) of the role assumed by the service to tag and untag resources on your behalf.
        :param tag_key: The tag key.
        :param tag_value: The tag value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-tagsynctask.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_resourcegroups import mixins as resourcegroups_mixins
            
            cfn_tag_sync_task_mixin_props = resourcegroups_mixins.CfnTagSyncTaskMixinProps(
                group="group",
                role_arn="roleArn",
                tag_key="tagKey",
                tag_value="tagValue"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d15586cffecac8218e9424b79facafe9ec7028d10b774d7901108d03780a02cc)
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group is not None:
            self._values["group"] = group
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def group(self) -> typing.Optional[builtins.str]:
        '''The Amazon resource name (ARN) or name of the application group for which you want to create a tag-sync task.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-tagsynctask.html#cfn-resourcegroups-tagsynctask-group
        '''
        result = self._values.get("group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon resource name (ARN) of the role assumed by the service to tag and untag resources on your behalf.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-tagsynctask.html#cfn-resourcegroups-tagsynctask-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''The tag key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-tagsynctask.html#cfn-resourcegroups-tagsynctask-tagkey
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''The tag value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-tagsynctask.html#cfn-resourcegroups-tagsynctask-tagvalue
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTagSyncTaskMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTagSyncTaskPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_resourcegroups.mixins.CfnTagSyncTaskPropsMixin",
):
    '''Onboards and syncs resources tagged with a specific tag key-value pair to an application.

    *Minimum permissions*

    To run this command, you must have the following permissions:

    - ``resource-groups:StartTagSyncTask``
    - ``resource-groups:CreateGroup``
    - ``iam:PassRole`` for the role you provide to create a tag-sync task

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-tagsynctask.html
    :cloudformationResource: AWS::ResourceGroups::TagSyncTask
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_resourcegroups import mixins as resourcegroups_mixins
        
        cfn_tag_sync_task_props_mixin = resourcegroups_mixins.CfnTagSyncTaskPropsMixin(resourcegroups_mixins.CfnTagSyncTaskMixinProps(
            group="group",
            role_arn="roleArn",
            tag_key="tagKey",
            tag_value="tagValue"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTagSyncTaskMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ResourceGroups::TagSyncTask``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4c69846c42b6de7b5403a94c30b1a67b5b1d4489e38ae63ef69bebd8aa66e83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__807a346b869b5ccb9a03660410ad0bf92fbfe17f0773a53bcc60dc16aa3278cf)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32fc907ef4b45a01f5389436611db3f3dd692aed40eebc6953c1dd6a1b02364d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTagSyncTaskMixinProps:
        return typing.cast(CfnTagSyncTaskMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnGroupMixinProps",
    "CfnGroupPropsMixin",
    "CfnTagSyncTaskMixinProps",
    "CfnTagSyncTaskPropsMixin",
]

publication.publish()

def _typecheckingstub__92e4dd43decd8695ecc205b4fa24fd930e6aee107eaa67db44c9a86dede0665f(
    *,
    configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGroupPropsMixin.ConfigurationItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    resource_query: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGroupPropsMixin.ResourceQueryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f6f4b7f4145f2293b14765711578d17cde63181d761f18039fc0de42fee7adb(
    props: typing.Union[CfnGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cbc55c57ebb890d0dbb863b4ad7f3f914ca55ecb5d819a0b41f12d459a5a959(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb7a89ed3f00bbe2181dd784f8c08885d66e5323b07bb16891b1b3c4b657b779(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ce288b5141677c8e4b70eb54249333cb7cbd9fb62c5b84f23184c372ee04517(
    *,
    parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGroupPropsMixin.ConfigurationParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f77b21fe1dea18ade73dab435a86de43e6401a49ac91b97128b22db0b7511e7e(
    *,
    name: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f49d82f98f0afb1d49bd5cecc5c2086adfbc6f37dab2da73c5d7a358fb25d0(
    *,
    resource_type_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
    stack_identifier: typing.Optional[builtins.str] = None,
    tag_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGroupPropsMixin.TagFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbabfc6d2073e09b821a77331ec2128089eb61f23fa5ed48af6a0e63cd525886(
    *,
    query: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGroupPropsMixin.QueryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8f19630188736cb0d85abfb8c47427debd0de372a74f078a2bfcc4a409951c2(
    *,
    key: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d15586cffecac8218e9424b79facafe9ec7028d10b774d7901108d03780a02cc(
    *,
    group: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4c69846c42b6de7b5403a94c30b1a67b5b1d4489e38ae63ef69bebd8aa66e83(
    props: typing.Union[CfnTagSyncTaskMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__807a346b869b5ccb9a03660410ad0bf92fbfe17f0773a53bcc60dc16aa3278cf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32fc907ef4b45a01f5389436611db3f3dd692aed40eebc6953c1dd6a1b02364d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
