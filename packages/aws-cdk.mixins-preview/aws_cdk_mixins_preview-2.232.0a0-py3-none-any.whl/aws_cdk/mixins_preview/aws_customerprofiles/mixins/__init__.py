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
    jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnCalculatedAttributeDefinitionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "attribute_details": "attributeDetails",
        "calculated_attribute_name": "calculatedAttributeName",
        "conditions": "conditions",
        "description": "description",
        "display_name": "displayName",
        "domain_name": "domainName",
        "statistic": "statistic",
        "tags": "tags",
        "use_historical_data": "useHistoricalData",
    },
)
class CfnCalculatedAttributeDefinitionMixinProps:
    def __init__(
        self,
        *,
        attribute_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCalculatedAttributeDefinitionPropsMixin.AttributeDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        calculated_attribute_name: typing.Optional[builtins.str] = None,
        conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCalculatedAttributeDefinitionPropsMixin.ConditionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        use_historical_data: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ) -> None:
        '''Properties for CfnCalculatedAttributeDefinitionPropsMixin.

        :param attribute_details: Mathematical expression and a list of attribute items specified in that expression.
        :param calculated_attribute_name: The name of an attribute defined in a profile object type.
        :param conditions: The conditions including range, object count, and threshold for the calculated attribute.
        :param description: The description of the calculated attribute.
        :param display_name: The display name of the calculated attribute.
        :param domain_name: The unique name of the domain.
        :param statistic: The aggregation operation to perform for the calculated attribute.
        :param tags: An array of key-value pairs to apply to this resource.
        :param use_historical_data: Whether historical data ingested before the Calculated Attribute was created should be included in calculations.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-calculatedattributedefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
            
            cfn_calculated_attribute_definition_mixin_props = customerprofiles_mixins.CfnCalculatedAttributeDefinitionMixinProps(
                attribute_details=customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin.AttributeDetailsProperty(
                    attributes=[customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin.AttributeItemProperty(
                        name="name"
                    )],
                    expression="expression"
                ),
                calculated_attribute_name="calculatedAttributeName",
                conditions=customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin.ConditionsProperty(
                    object_count=123,
                    range=customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin.RangeProperty(
                        timestamp_format="timestampFormat",
                        timestamp_source="timestampSource",
                        unit="unit",
                        value=123,
                        value_range=customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin.ValueRangeProperty(
                            end=123,
                            start=123
                        )
                    ),
                    threshold=customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin.ThresholdProperty(
                        operator="operator",
                        value="value"
                    )
                ),
                description="description",
                display_name="displayName",
                domain_name="domainName",
                statistic="statistic",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                use_historical_data=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11c8c27e084e0280eea7f2225b5f1894a6b9117d79deecf4c9c861221243df04)
            check_type(argname="argument attribute_details", value=attribute_details, expected_type=type_hints["attribute_details"])
            check_type(argname="argument calculated_attribute_name", value=calculated_attribute_name, expected_type=type_hints["calculated_attribute_name"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument use_historical_data", value=use_historical_data, expected_type=type_hints["use_historical_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attribute_details is not None:
            self._values["attribute_details"] = attribute_details
        if calculated_attribute_name is not None:
            self._values["calculated_attribute_name"] = calculated_attribute_name
        if conditions is not None:
            self._values["conditions"] = conditions
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if statistic is not None:
            self._values["statistic"] = statistic
        if tags is not None:
            self._values["tags"] = tags
        if use_historical_data is not None:
            self._values["use_historical_data"] = use_historical_data

    @builtins.property
    def attribute_details(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCalculatedAttributeDefinitionPropsMixin.AttributeDetailsProperty"]]:
        '''Mathematical expression and a list of attribute items specified in that expression.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-calculatedattributedefinition.html#cfn-customerprofiles-calculatedattributedefinition-attributedetails
        '''
        result = self._values.get("attribute_details")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCalculatedAttributeDefinitionPropsMixin.AttributeDetailsProperty"]], result)

    @builtins.property
    def calculated_attribute_name(self) -> typing.Optional[builtins.str]:
        '''The name of an attribute defined in a profile object type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-calculatedattributedefinition.html#cfn-customerprofiles-calculatedattributedefinition-calculatedattributename
        '''
        result = self._values.get("calculated_attribute_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def conditions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCalculatedAttributeDefinitionPropsMixin.ConditionsProperty"]]:
        '''The conditions including range, object count, and threshold for the calculated attribute.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-calculatedattributedefinition.html#cfn-customerprofiles-calculatedattributedefinition-conditions
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCalculatedAttributeDefinitionPropsMixin.ConditionsProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the calculated attribute.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-calculatedattributedefinition.html#cfn-customerprofiles-calculatedattributedefinition-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the calculated attribute.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-calculatedattributedefinition.html#cfn-customerprofiles-calculatedattributedefinition-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The unique name of the domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-calculatedattributedefinition.html#cfn-customerprofiles-calculatedattributedefinition-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statistic(self) -> typing.Optional[builtins.str]:
        '''The aggregation operation to perform for the calculated attribute.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-calculatedattributedefinition.html#cfn-customerprofiles-calculatedattributedefinition-statistic
        '''
        result = self._values.get("statistic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-calculatedattributedefinition.html#cfn-customerprofiles-calculatedattributedefinition-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def use_historical_data(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether historical data ingested before the Calculated Attribute was created should be included in calculations.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-calculatedattributedefinition.html#cfn-customerprofiles-calculatedattributedefinition-usehistoricaldata
        '''
        result = self._values.get("use_historical_data")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCalculatedAttributeDefinitionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCalculatedAttributeDefinitionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnCalculatedAttributeDefinitionPropsMixin",
):
    '''A calculated attribute definition for Customer Profiles.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-calculatedattributedefinition.html
    :cloudformationResource: AWS::CustomerProfiles::CalculatedAttributeDefinition
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
        
        cfn_calculated_attribute_definition_props_mixin = customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin(customerprofiles_mixins.CfnCalculatedAttributeDefinitionMixinProps(
            attribute_details=customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin.AttributeDetailsProperty(
                attributes=[customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin.AttributeItemProperty(
                    name="name"
                )],
                expression="expression"
            ),
            calculated_attribute_name="calculatedAttributeName",
            conditions=customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin.ConditionsProperty(
                object_count=123,
                range=customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin.RangeProperty(
                    timestamp_format="timestampFormat",
                    timestamp_source="timestampSource",
                    unit="unit",
                    value=123,
                    value_range=customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin.ValueRangeProperty(
                        end=123,
                        start=123
                    )
                ),
                threshold=customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin.ThresholdProperty(
                    operator="operator",
                    value="value"
                )
            ),
            description="description",
            display_name="displayName",
            domain_name="domainName",
            statistic="statistic",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            use_historical_data=False
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCalculatedAttributeDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CustomerProfiles::CalculatedAttributeDefinition``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d2fee4a3f678c50fccf2867468ff926f644f701ab9d58070cf1667621dc8194)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c4c378bcc003988d06041c9d86a3479efde9c8f7585dde78b2a47e3e5060585)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9cdbe5700c0d4f0cadf18e6639b5ffa709125e54b1f4b6b5f1b5250274c73e9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCalculatedAttributeDefinitionMixinProps:
        return typing.cast(CfnCalculatedAttributeDefinitionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnCalculatedAttributeDefinitionPropsMixin.AttributeDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"attributes": "attributes", "expression": "expression"},
    )
    class AttributeDetailsProperty:
        def __init__(
            self,
            *,
            attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCalculatedAttributeDefinitionPropsMixin.AttributeItemProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            expression: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Mathematical expression and a list of attribute items specified in that expression.

            :param attributes: Mathematical expression and a list of attribute items specified in that expression.
            :param expression: Mathematical expression that is performed on attribute items provided in the attribute list. Each element in the expression should follow the structure of "{ObjectTypeName.AttributeName}".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-calculatedattributedefinition-attributedetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                attribute_details_property = customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin.AttributeDetailsProperty(
                    attributes=[customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin.AttributeItemProperty(
                        name="name"
                    )],
                    expression="expression"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9eba6d4d6be12624c49ef763235f2e205bd01b05d66a3be22bb0670ee10640ec)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if expression is not None:
                self._values["expression"] = expression

        @builtins.property
        def attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCalculatedAttributeDefinitionPropsMixin.AttributeItemProperty"]]]]:
            '''Mathematical expression and a list of attribute items specified in that expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-calculatedattributedefinition-attributedetails.html#cfn-customerprofiles-calculatedattributedefinition-attributedetails-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCalculatedAttributeDefinitionPropsMixin.AttributeItemProperty"]]]], result)

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''Mathematical expression that is performed on attribute items provided in the attribute list.

            Each element in the expression should follow the structure of "{ObjectTypeName.AttributeName}".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-calculatedattributedefinition-attributedetails.html#cfn-customerprofiles-calculatedattributedefinition-attributedetails-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnCalculatedAttributeDefinitionPropsMixin.AttributeItemProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class AttributeItemProperty:
        def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
            '''The details of a single attribute item specified in the mathematical expression.

            :param name: The unique name of the calculated attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-calculatedattributedefinition-attributeitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                attribute_item_property = customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin.AttributeItemProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__154d920b67d4ddc5e56bc53287d3041fc15f6110453e1db82b750f43712fc279)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The unique name of the calculated attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-calculatedattributedefinition-attributeitem.html#cfn-customerprofiles-calculatedattributedefinition-attributeitem-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnCalculatedAttributeDefinitionPropsMixin.ConditionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "object_count": "objectCount",
            "range": "range",
            "threshold": "threshold",
        },
    )
    class ConditionsProperty:
        def __init__(
            self,
            *,
            object_count: typing.Optional[jsii.Number] = None,
            range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCalculatedAttributeDefinitionPropsMixin.RangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            threshold: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCalculatedAttributeDefinitionPropsMixin.ThresholdProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The conditions including range, object count, and threshold for the calculated attribute.

            :param object_count: The number of profile objects used for the calculated attribute.
            :param range: The relative time period over which data is included in the aggregation.
            :param threshold: The threshold for the calculated attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-calculatedattributedefinition-conditions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                conditions_property = customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin.ConditionsProperty(
                    object_count=123,
                    range=customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin.RangeProperty(
                        timestamp_format="timestampFormat",
                        timestamp_source="timestampSource",
                        unit="unit",
                        value=123,
                        value_range=customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin.ValueRangeProperty(
                            end=123,
                            start=123
                        )
                    ),
                    threshold=customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin.ThresholdProperty(
                        operator="operator",
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__41f9d576465dff29534c34b52f6cd729ad8b301849cdfd028ec335f2da551b08)
                check_type(argname="argument object_count", value=object_count, expected_type=type_hints["object_count"])
                check_type(argname="argument range", value=range, expected_type=type_hints["range"])
                check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object_count is not None:
                self._values["object_count"] = object_count
            if range is not None:
                self._values["range"] = range
            if threshold is not None:
                self._values["threshold"] = threshold

        @builtins.property
        def object_count(self) -> typing.Optional[jsii.Number]:
            '''The number of profile objects used for the calculated attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-calculatedattributedefinition-conditions.html#cfn-customerprofiles-calculatedattributedefinition-conditions-objectcount
            '''
            result = self._values.get("object_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def range(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCalculatedAttributeDefinitionPropsMixin.RangeProperty"]]:
            '''The relative time period over which data is included in the aggregation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-calculatedattributedefinition-conditions.html#cfn-customerprofiles-calculatedattributedefinition-conditions-range
            '''
            result = self._values.get("range")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCalculatedAttributeDefinitionPropsMixin.RangeProperty"]], result)

        @builtins.property
        def threshold(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCalculatedAttributeDefinitionPropsMixin.ThresholdProperty"]]:
            '''The threshold for the calculated attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-calculatedattributedefinition-conditions.html#cfn-customerprofiles-calculatedattributedefinition-conditions-threshold
            '''
            result = self._values.get("threshold")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCalculatedAttributeDefinitionPropsMixin.ThresholdProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConditionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnCalculatedAttributeDefinitionPropsMixin.RangeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "timestamp_format": "timestampFormat",
            "timestamp_source": "timestampSource",
            "unit": "unit",
            "value": "value",
            "value_range": "valueRange",
        },
    )
    class RangeProperty:
        def __init__(
            self,
            *,
            timestamp_format: typing.Optional[builtins.str] = None,
            timestamp_source: typing.Optional[builtins.str] = None,
            unit: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
            value_range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCalculatedAttributeDefinitionPropsMixin.ValueRangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The relative time period over which data is included in the aggregation.

            :param timestamp_format: The format the timestamp field in your JSON object is specified. This value should be one of EPOCHMILLI (for Unix epoch timestamps with second/millisecond level precision) or ISO_8601 (following ISO_8601 format with second/millisecond level precision, with an optional offset of Z or in the format HH:MM or HHMM.). E.g. if your object type is MyType and source JSON is {"generatedAt": {"timestamp": "2001-07-04T12:08:56.235-0700"}}, then TimestampFormat should be "ISO_8601"
            :param timestamp_source: An expression specifying the field in your JSON object from which the date should be parsed. The expression should follow the structure of "{ObjectTypeName.}". E.g. if your object type is MyType and source JSON is {"generatedAt": {"timestamp": "1737587945945"}}, then TimestampSource should be "{MyType.generatedAt.timestamp}"
            :param unit: The unit of time.
            :param value: The amount of time of the specified unit.
            :param value_range: A structure letting customers specify a relative time window over which over which data is included in the Calculated Attribute. Use positive numbers to indicate that the endpoint is in the past, and negative numbers to indicate it is in the future. ValueRange overrides Value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-calculatedattributedefinition-range.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                range_property = customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin.RangeProperty(
                    timestamp_format="timestampFormat",
                    timestamp_source="timestampSource",
                    unit="unit",
                    value=123,
                    value_range=customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin.ValueRangeProperty(
                        end=123,
                        start=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__85eaa2a7b18f3d0b4cdb430cba87b765606116c7f2262083ba220d5039a0e409)
                check_type(argname="argument timestamp_format", value=timestamp_format, expected_type=type_hints["timestamp_format"])
                check_type(argname="argument timestamp_source", value=timestamp_source, expected_type=type_hints["timestamp_source"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                check_type(argname="argument value_range", value=value_range, expected_type=type_hints["value_range"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if timestamp_format is not None:
                self._values["timestamp_format"] = timestamp_format
            if timestamp_source is not None:
                self._values["timestamp_source"] = timestamp_source
            if unit is not None:
                self._values["unit"] = unit
            if value is not None:
                self._values["value"] = value
            if value_range is not None:
                self._values["value_range"] = value_range

        @builtins.property
        def timestamp_format(self) -> typing.Optional[builtins.str]:
            '''The format the timestamp field in your JSON object is specified.

            This value should be one of EPOCHMILLI (for Unix epoch timestamps with second/millisecond level precision) or ISO_8601 (following ISO_8601 format with second/millisecond level precision, with an optional offset of Z or in the format HH:MM or HHMM.). E.g. if your object type is MyType and source JSON is {"generatedAt": {"timestamp": "2001-07-04T12:08:56.235-0700"}}, then TimestampFormat should be "ISO_8601"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-calculatedattributedefinition-range.html#cfn-customerprofiles-calculatedattributedefinition-range-timestampformat
            '''
            result = self._values.get("timestamp_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timestamp_source(self) -> typing.Optional[builtins.str]:
            '''An expression specifying the field in your JSON object from which the date should be parsed.

            The expression should follow the structure of "{ObjectTypeName.}". E.g. if your object type is MyType and source JSON is {"generatedAt": {"timestamp": "1737587945945"}}, then TimestampSource should be "{MyType.generatedAt.timestamp}"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-calculatedattributedefinition-range.html#cfn-customerprofiles-calculatedattributedefinition-range-timestampsource
            '''
            result = self._values.get("timestamp_source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The unit of time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-calculatedattributedefinition-range.html#cfn-customerprofiles-calculatedattributedefinition-range-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''The amount of time of the specified unit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-calculatedattributedefinition-range.html#cfn-customerprofiles-calculatedattributedefinition-range-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def value_range(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCalculatedAttributeDefinitionPropsMixin.ValueRangeProperty"]]:
            '''A structure letting customers specify a relative time window over which over which data is included in the Calculated Attribute.

            Use positive numbers to indicate that the endpoint is in the past, and negative numbers to indicate it is in the future. ValueRange overrides Value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-calculatedattributedefinition-range.html#cfn-customerprofiles-calculatedattributedefinition-range-valuerange
            '''
            result = self._values.get("value_range")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCalculatedAttributeDefinitionPropsMixin.ValueRangeProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnCalculatedAttributeDefinitionPropsMixin.ReadinessProperty",
        jsii_struct_bases=[],
        name_mapping={
            "message": "message",
            "progress_percentage": "progressPercentage",
        },
    )
    class ReadinessProperty:
        def __init__(
            self,
            *,
            message: typing.Optional[builtins.str] = None,
            progress_percentage: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information indicating if the Calculated Attribute is ready for use by confirming all historical data has been processed and reflected.

            :param message: Any customer messaging.
            :param progress_percentage: Approximately how far the Calculated Attribute creation is from completion.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-calculatedattributedefinition-readiness.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                readiness_property = customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin.ReadinessProperty(
                    message="message",
                    progress_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1d31f1f20b14d079d19997980b1fcbc49f0d2be08cc9f8a50b4c604fb07ff0a6)
                check_type(argname="argument message", value=message, expected_type=type_hints["message"])
                check_type(argname="argument progress_percentage", value=progress_percentage, expected_type=type_hints["progress_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if message is not None:
                self._values["message"] = message
            if progress_percentage is not None:
                self._values["progress_percentage"] = progress_percentage

        @builtins.property
        def message(self) -> typing.Optional[builtins.str]:
            '''Any customer messaging.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-calculatedattributedefinition-readiness.html#cfn-customerprofiles-calculatedattributedefinition-readiness-message
            '''
            result = self._values.get("message")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def progress_percentage(self) -> typing.Optional[jsii.Number]:
            '''Approximately how far the Calculated Attribute creation is from completion.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-calculatedattributedefinition-readiness.html#cfn-customerprofiles-calculatedattributedefinition-readiness-progresspercentage
            '''
            result = self._values.get("progress_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReadinessProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnCalculatedAttributeDefinitionPropsMixin.ThresholdProperty",
        jsii_struct_bases=[],
        name_mapping={"operator": "operator", "value": "value"},
    )
    class ThresholdProperty:
        def __init__(
            self,
            *,
            operator: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The threshold for the calculated attribute.

            :param operator: The operator of the threshold.
            :param value: The value of the threshold.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-calculatedattributedefinition-threshold.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                threshold_property = customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin.ThresholdProperty(
                    operator="operator",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fbfded726a559f79af6296226a05180016e2bdf1c60ad88792e22e1e10a8de54)
                check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if operator is not None:
                self._values["operator"] = operator
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def operator(self) -> typing.Optional[builtins.str]:
            '''The operator of the threshold.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-calculatedattributedefinition-threshold.html#cfn-customerprofiles-calculatedattributedefinition-threshold-operator
            '''
            result = self._values.get("operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the threshold.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-calculatedattributedefinition-threshold.html#cfn-customerprofiles-calculatedattributedefinition-threshold-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ThresholdProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnCalculatedAttributeDefinitionPropsMixin.ValueRangeProperty",
        jsii_struct_bases=[],
        name_mapping={"end": "end", "start": "start"},
    )
    class ValueRangeProperty:
        def __init__(
            self,
            *,
            end: typing.Optional[jsii.Number] = None,
            start: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A structure letting customers specify a relative time window over which over which data is included in the Calculated Attribute.

            Use positive numbers to indicate that the endpoint is in the past, and negative numbers to indicate it is in the future. ValueRange overrides Value.

            :param end: The ending point for this overridden range. Positive numbers indicate how many days in the past data should be included, and negative numbers indicate how many days in the future.
            :param start: The starting point for this overridden range. Positive numbers indicate how many days in the past data should be included, and negative numbers indicate how many days in the future.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-calculatedattributedefinition-valuerange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                value_range_property = customerprofiles_mixins.CfnCalculatedAttributeDefinitionPropsMixin.ValueRangeProperty(
                    end=123,
                    start=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ade600d52dd25af62412db0b6788b50fd3ea4af58656fef41ebed45405ae1fb0)
                check_type(argname="argument end", value=end, expected_type=type_hints["end"])
                check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if end is not None:
                self._values["end"] = end
            if start is not None:
                self._values["start"] = start

        @builtins.property
        def end(self) -> typing.Optional[jsii.Number]:
            '''The ending point for this overridden range.

            Positive numbers indicate how many days in the past data should be included, and negative numbers indicate how many days in the future.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-calculatedattributedefinition-valuerange.html#cfn-customerprofiles-calculatedattributedefinition-valuerange-end
            '''
            result = self._values.get("end")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def start(self) -> typing.Optional[jsii.Number]:
            '''The starting point for this overridden range.

            Positive numbers indicate how many days in the past data should be included, and negative numbers indicate how many days in the future.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-calculatedattributedefinition-valuerange.html#cfn-customerprofiles-calculatedattributedefinition-valuerange-start
            '''
            result = self._values.get("start")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ValueRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnDomainMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_store": "dataStore",
        "dead_letter_queue_url": "deadLetterQueueUrl",
        "default_encryption_key": "defaultEncryptionKey",
        "default_expiration_days": "defaultExpirationDays",
        "domain_name": "domainName",
        "matching": "matching",
        "rule_based_matching": "ruleBasedMatching",
        "tags": "tags",
    },
)
class CfnDomainMixinProps:
    def __init__(
        self,
        *,
        data_store: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.DataStoreProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        dead_letter_queue_url: typing.Optional[builtins.str] = None,
        default_encryption_key: typing.Optional[builtins.str] = None,
        default_expiration_days: typing.Optional[jsii.Number] = None,
        domain_name: typing.Optional[builtins.str] = None,
        matching: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.MatchingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        rule_based_matching: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.RuleBasedMatchingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDomainPropsMixin.

        :param data_store: Configuration and status of the data store for the domain.
        :param dead_letter_queue_url: The URL of the SQS dead letter queue, which is used for reporting errors associated with ingesting data from third party applications. You must set up a policy on the ``DeadLetterQueue`` for the ``SendMessage`` operation to enable Amazon Connect Customer Profiles to send messages to the ``DeadLetterQueue`` .
        :param default_encryption_key: The default encryption key, which is an AWS managed key, is used when no specific type of encryption key is specified. It is used to encrypt all data before it is placed in permanent or semi-permanent storage.
        :param default_expiration_days: The default number of days until the data within the domain expires.
        :param domain_name: The unique name of the domain.
        :param matching: The process of matching duplicate profiles.
        :param rule_based_matching: The process of matching duplicate profiles using Rule-Based matching.
        :param tags: The tags used to organize, track, or control access for this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-domain.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
            
            cfn_domain_mixin_props = customerprofiles_mixins.CfnDomainMixinProps(
                data_store=customerprofiles_mixins.CfnDomainPropsMixin.DataStoreProperty(
                    enabled=False,
                    readiness=customerprofiles_mixins.CfnDomainPropsMixin.ReadinessProperty(
                        message="message",
                        progress_percentage=123
                    )
                ),
                dead_letter_queue_url="deadLetterQueueUrl",
                default_encryption_key="defaultEncryptionKey",
                default_expiration_days=123,
                domain_name="domainName",
                matching=customerprofiles_mixins.CfnDomainPropsMixin.MatchingProperty(
                    auto_merging=customerprofiles_mixins.CfnDomainPropsMixin.AutoMergingProperty(
                        conflict_resolution=customerprofiles_mixins.CfnDomainPropsMixin.ConflictResolutionProperty(
                            conflict_resolving_model="conflictResolvingModel",
                            source_name="sourceName"
                        ),
                        consolidation=customerprofiles_mixins.CfnDomainPropsMixin.ConsolidationProperty(
                            matching_attributes_list=[["matchingAttributesList"]]
                        ),
                        enabled=False,
                        min_allowed_confidence_score_for_merging=123
                    ),
                    enabled=False,
                    exporting_config=customerprofiles_mixins.CfnDomainPropsMixin.ExportingConfigProperty(
                        s3_exporting=customerprofiles_mixins.CfnDomainPropsMixin.S3ExportingConfigProperty(
                            s3_bucket_name="s3BucketName",
                            s3_key_name="s3KeyName"
                        )
                    ),
                    job_schedule=customerprofiles_mixins.CfnDomainPropsMixin.JobScheduleProperty(
                        day_of_the_week="dayOfTheWeek",
                        time="time"
                    )
                ),
                rule_based_matching=customerprofiles_mixins.CfnDomainPropsMixin.RuleBasedMatchingProperty(
                    attribute_types_selector=customerprofiles_mixins.CfnDomainPropsMixin.AttributeTypesSelectorProperty(
                        address=["address"],
                        attribute_matching_model="attributeMatchingModel",
                        email_address=["emailAddress"],
                        phone_number=["phoneNumber"]
                    ),
                    conflict_resolution=customerprofiles_mixins.CfnDomainPropsMixin.ConflictResolutionProperty(
                        conflict_resolving_model="conflictResolvingModel",
                        source_name="sourceName"
                    ),
                    enabled=False,
                    exporting_config=customerprofiles_mixins.CfnDomainPropsMixin.ExportingConfigProperty(
                        s3_exporting=customerprofiles_mixins.CfnDomainPropsMixin.S3ExportingConfigProperty(
                            s3_bucket_name="s3BucketName",
                            s3_key_name="s3KeyName"
                        )
                    ),
                    matching_rules=[customerprofiles_mixins.CfnDomainPropsMixin.MatchingRuleProperty(
                        rule=["rule"]
                    )],
                    max_allowed_rule_level_for_matching=123,
                    max_allowed_rule_level_for_merging=123,
                    status="status"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21f2e43cdf2518c0f94f582ba5191398d2e1bf5181360a4cb3ce715238cc087e)
            check_type(argname="argument data_store", value=data_store, expected_type=type_hints["data_store"])
            check_type(argname="argument dead_letter_queue_url", value=dead_letter_queue_url, expected_type=type_hints["dead_letter_queue_url"])
            check_type(argname="argument default_encryption_key", value=default_encryption_key, expected_type=type_hints["default_encryption_key"])
            check_type(argname="argument default_expiration_days", value=default_expiration_days, expected_type=type_hints["default_expiration_days"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument matching", value=matching, expected_type=type_hints["matching"])
            check_type(argname="argument rule_based_matching", value=rule_based_matching, expected_type=type_hints["rule_based_matching"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_store is not None:
            self._values["data_store"] = data_store
        if dead_letter_queue_url is not None:
            self._values["dead_letter_queue_url"] = dead_letter_queue_url
        if default_encryption_key is not None:
            self._values["default_encryption_key"] = default_encryption_key
        if default_expiration_days is not None:
            self._values["default_expiration_days"] = default_expiration_days
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if matching is not None:
            self._values["matching"] = matching
        if rule_based_matching is not None:
            self._values["rule_based_matching"] = rule_based_matching
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def data_store(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.DataStoreProperty"]]:
        '''Configuration and status of the data store for the domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-domain.html#cfn-customerprofiles-domain-datastore
        '''
        result = self._values.get("data_store")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.DataStoreProperty"]], result)

    @builtins.property
    def dead_letter_queue_url(self) -> typing.Optional[builtins.str]:
        '''The URL of the SQS dead letter queue, which is used for reporting errors associated with ingesting data from third party applications.

        You must set up a policy on the ``DeadLetterQueue`` for the ``SendMessage`` operation to enable Amazon Connect Customer Profiles to send messages to the ``DeadLetterQueue`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-domain.html#cfn-customerprofiles-domain-deadletterqueueurl
        '''
        result = self._values.get("dead_letter_queue_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_encryption_key(self) -> typing.Optional[builtins.str]:
        '''The default encryption key, which is an AWS managed key, is used when no specific type of encryption key is specified.

        It is used to encrypt all data before it is placed in permanent or semi-permanent storage.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-domain.html#cfn-customerprofiles-domain-defaultencryptionkey
        '''
        result = self._values.get("default_encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_expiration_days(self) -> typing.Optional[jsii.Number]:
        '''The default number of days until the data within the domain expires.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-domain.html#cfn-customerprofiles-domain-defaultexpirationdays
        '''
        result = self._values.get("default_expiration_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The unique name of the domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-domain.html#cfn-customerprofiles-domain-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def matching(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.MatchingProperty"]]:
        '''The process of matching duplicate profiles.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-domain.html#cfn-customerprofiles-domain-matching
        '''
        result = self._values.get("matching")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.MatchingProperty"]], result)

    @builtins.property
    def rule_based_matching(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.RuleBasedMatchingProperty"]]:
        '''The process of matching duplicate profiles using Rule-Based matching.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-domain.html#cfn-customerprofiles-domain-rulebasedmatching
        '''
        result = self._values.get("rule_based_matching")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.RuleBasedMatchingProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-domain.html#cfn-customerprofiles-domain-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDomainPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnDomainPropsMixin",
):
    '''Specifies an Amazon Connect Customer Profiles Domain.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-domain.html
    :cloudformationResource: AWS::CustomerProfiles::Domain
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
        
        cfn_domain_props_mixin = customerprofiles_mixins.CfnDomainPropsMixin(customerprofiles_mixins.CfnDomainMixinProps(
            data_store=customerprofiles_mixins.CfnDomainPropsMixin.DataStoreProperty(
                enabled=False,
                readiness=customerprofiles_mixins.CfnDomainPropsMixin.ReadinessProperty(
                    message="message",
                    progress_percentage=123
                )
            ),
            dead_letter_queue_url="deadLetterQueueUrl",
            default_encryption_key="defaultEncryptionKey",
            default_expiration_days=123,
            domain_name="domainName",
            matching=customerprofiles_mixins.CfnDomainPropsMixin.MatchingProperty(
                auto_merging=customerprofiles_mixins.CfnDomainPropsMixin.AutoMergingProperty(
                    conflict_resolution=customerprofiles_mixins.CfnDomainPropsMixin.ConflictResolutionProperty(
                        conflict_resolving_model="conflictResolvingModel",
                        source_name="sourceName"
                    ),
                    consolidation=customerprofiles_mixins.CfnDomainPropsMixin.ConsolidationProperty(
                        matching_attributes_list=[["matchingAttributesList"]]
                    ),
                    enabled=False,
                    min_allowed_confidence_score_for_merging=123
                ),
                enabled=False,
                exporting_config=customerprofiles_mixins.CfnDomainPropsMixin.ExportingConfigProperty(
                    s3_exporting=customerprofiles_mixins.CfnDomainPropsMixin.S3ExportingConfigProperty(
                        s3_bucket_name="s3BucketName",
                        s3_key_name="s3KeyName"
                    )
                ),
                job_schedule=customerprofiles_mixins.CfnDomainPropsMixin.JobScheduleProperty(
                    day_of_the_week="dayOfTheWeek",
                    time="time"
                )
            ),
            rule_based_matching=customerprofiles_mixins.CfnDomainPropsMixin.RuleBasedMatchingProperty(
                attribute_types_selector=customerprofiles_mixins.CfnDomainPropsMixin.AttributeTypesSelectorProperty(
                    address=["address"],
                    attribute_matching_model="attributeMatchingModel",
                    email_address=["emailAddress"],
                    phone_number=["phoneNumber"]
                ),
                conflict_resolution=customerprofiles_mixins.CfnDomainPropsMixin.ConflictResolutionProperty(
                    conflict_resolving_model="conflictResolvingModel",
                    source_name="sourceName"
                ),
                enabled=False,
                exporting_config=customerprofiles_mixins.CfnDomainPropsMixin.ExportingConfigProperty(
                    s3_exporting=customerprofiles_mixins.CfnDomainPropsMixin.S3ExportingConfigProperty(
                        s3_bucket_name="s3BucketName",
                        s3_key_name="s3KeyName"
                    )
                ),
                matching_rules=[customerprofiles_mixins.CfnDomainPropsMixin.MatchingRuleProperty(
                    rule=["rule"]
                )],
                max_allowed_rule_level_for_matching=123,
                max_allowed_rule_level_for_merging=123,
                status="status"
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
        props: typing.Union[CfnDomainMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CustomerProfiles::Domain``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fa94f2a366916f67cd6f67160d52e43db017a8280a49ac449609fe5a8bd209f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ead32f2b9c6380696b5191ef4d2a96604a726e89b9a83914c420b13d10c75936)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2412f77e51e66f72b8957429ec17d802f55e9ce8fdec365869ec741d1a659de0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDomainMixinProps:
        return typing.cast(CfnDomainMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnDomainPropsMixin.AttributeTypesSelectorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "address": "address",
            "attribute_matching_model": "attributeMatchingModel",
            "email_address": "emailAddress",
            "phone_number": "phoneNumber",
        },
    )
    class AttributeTypesSelectorProperty:
        def __init__(
            self,
            *,
            address: typing.Optional[typing.Sequence[builtins.str]] = None,
            attribute_matching_model: typing.Optional[builtins.str] = None,
            email_address: typing.Optional[typing.Sequence[builtins.str]] = None,
            phone_number: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Configures information about the ``AttributeTypesSelector`` which rule-based identity resolution uses to match profiles.

            :param address: The ``Address`` type. You can choose from ``Address`` , ``BusinessAddress`` , ``MaillingAddress`` , and ``ShippingAddress`` . You only can use the ``Address`` type in the ``MatchingRule`` . For example, if you want to match a profile based on ``BusinessAddress.City`` or ``MaillingAddress.City`` , you can choose the ``BusinessAddress`` and the ``MaillingAddress`` to represent the ``Address`` type and specify the ``Address.City`` on the matching rule.
            :param attribute_matching_model: Configures the ``AttributeMatchingModel`` , you can either choose ``ONE_TO_ONE`` or ``MANY_TO_MANY`` .
            :param email_address: The Email type. You can choose from ``EmailAddress`` , ``BusinessEmailAddress`` and ``PersonalEmailAddress`` . You only can use the ``EmailAddress`` type in the ``MatchingRule`` . For example, if you want to match profile based on ``PersonalEmailAddress`` or ``BusinessEmailAddress`` , you can choose the ``PersonalEmailAddress`` and the ``BusinessEmailAddress`` to represent the ``EmailAddress`` type and only specify the ``EmailAddress`` on the matching rule.
            :param phone_number: The ``PhoneNumber`` type. You can choose from ``PhoneNumber`` , ``HomePhoneNumber`` , and ``MobilePhoneNumber`` . You only can use the ``PhoneNumber`` type in the ``MatchingRule`` . For example, if you want to match a profile based on ``Phone`` or ``HomePhone`` , you can choose the ``Phone`` and the ``HomePhone`` to represent the ``PhoneNumber`` type and only specify the ``PhoneNumber`` on the matching rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-attributetypesselector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                attribute_types_selector_property = customerprofiles_mixins.CfnDomainPropsMixin.AttributeTypesSelectorProperty(
                    address=["address"],
                    attribute_matching_model="attributeMatchingModel",
                    email_address=["emailAddress"],
                    phone_number=["phoneNumber"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b3992a9a90bdf739ebd239292fc7f9dc82a7b48ac43bd1cc89b0b8c516ae96d6)
                check_type(argname="argument address", value=address, expected_type=type_hints["address"])
                check_type(argname="argument attribute_matching_model", value=attribute_matching_model, expected_type=type_hints["attribute_matching_model"])
                check_type(argname="argument email_address", value=email_address, expected_type=type_hints["email_address"])
                check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address is not None:
                self._values["address"] = address
            if attribute_matching_model is not None:
                self._values["attribute_matching_model"] = attribute_matching_model
            if email_address is not None:
                self._values["email_address"] = email_address
            if phone_number is not None:
                self._values["phone_number"] = phone_number

        @builtins.property
        def address(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The ``Address`` type.

            You can choose from ``Address`` , ``BusinessAddress`` , ``MaillingAddress`` , and ``ShippingAddress`` . You only can use the ``Address`` type in the ``MatchingRule`` . For example, if you want to match a profile based on ``BusinessAddress.City`` or ``MaillingAddress.City`` , you can choose the ``BusinessAddress`` and the ``MaillingAddress`` to represent the ``Address`` type and specify the ``Address.City`` on the matching rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-attributetypesselector.html#cfn-customerprofiles-domain-attributetypesselector-address
            '''
            result = self._values.get("address")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def attribute_matching_model(self) -> typing.Optional[builtins.str]:
            '''Configures the ``AttributeMatchingModel`` , you can either choose ``ONE_TO_ONE`` or ``MANY_TO_MANY`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-attributetypesselector.html#cfn-customerprofiles-domain-attributetypesselector-attributematchingmodel
            '''
            result = self._values.get("attribute_matching_model")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def email_address(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The Email type.

            You can choose from ``EmailAddress`` , ``BusinessEmailAddress`` and ``PersonalEmailAddress`` . You only can use the ``EmailAddress`` type in the ``MatchingRule`` . For example, if you want to match profile based on ``PersonalEmailAddress`` or ``BusinessEmailAddress`` , you can choose the ``PersonalEmailAddress`` and the ``BusinessEmailAddress`` to represent the ``EmailAddress`` type and only specify the ``EmailAddress`` on the matching rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-attributetypesselector.html#cfn-customerprofiles-domain-attributetypesselector-emailaddress
            '''
            result = self._values.get("email_address")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def phone_number(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The ``PhoneNumber`` type.

            You can choose from ``PhoneNumber`` , ``HomePhoneNumber`` , and ``MobilePhoneNumber`` . You only can use the ``PhoneNumber`` type in the ``MatchingRule`` . For example, if you want to match a profile based on ``Phone`` or ``HomePhone`` , you can choose the ``Phone`` and the ``HomePhone`` to represent the ``PhoneNumber`` type and only specify the ``PhoneNumber`` on the matching rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-attributetypesselector.html#cfn-customerprofiles-domain-attributetypesselector-phonenumber
            '''
            result = self._values.get("phone_number")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeTypesSelectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnDomainPropsMixin.AutoMergingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "conflict_resolution": "conflictResolution",
            "consolidation": "consolidation",
            "enabled": "enabled",
            "min_allowed_confidence_score_for_merging": "minAllowedConfidenceScoreForMerging",
        },
    )
    class AutoMergingProperty:
        def __init__(
            self,
            *,
            conflict_resolution: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.ConflictResolutionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            consolidation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.ConsolidationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            min_allowed_confidence_score_for_merging: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Configuration information about the auto-merging process.

            :param conflict_resolution: Determines how the auto-merging process should resolve conflicts between different profiles. For example, if Profile A and Profile B have the same ``FirstName`` and ``LastName`` , ``ConflictResolution`` specifies which ``EmailAddress`` should be used.
            :param consolidation: A list of matching attributes that represent matching criteria. If two profiles meet at least one of the requirements in the matching attributes list, they will be merged.
            :param enabled: The flag that enables the auto-merging of duplicate profiles.
            :param min_allowed_confidence_score_for_merging: A number between 0 and 1 that represents the minimum confidence score required for profiles within a matching group to be merged during the auto-merge process. A higher score means that a higher similarity is required to merge profiles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-automerging.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                auto_merging_property = customerprofiles_mixins.CfnDomainPropsMixin.AutoMergingProperty(
                    conflict_resolution=customerprofiles_mixins.CfnDomainPropsMixin.ConflictResolutionProperty(
                        conflict_resolving_model="conflictResolvingModel",
                        source_name="sourceName"
                    ),
                    consolidation=customerprofiles_mixins.CfnDomainPropsMixin.ConsolidationProperty(
                        matching_attributes_list=[["matchingAttributesList"]]
                    ),
                    enabled=False,
                    min_allowed_confidence_score_for_merging=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a3c1b0f1494d30267ee9ca52019662e1858c13d75fe5949d86ed877a012f9128)
                check_type(argname="argument conflict_resolution", value=conflict_resolution, expected_type=type_hints["conflict_resolution"])
                check_type(argname="argument consolidation", value=consolidation, expected_type=type_hints["consolidation"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument min_allowed_confidence_score_for_merging", value=min_allowed_confidence_score_for_merging, expected_type=type_hints["min_allowed_confidence_score_for_merging"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if conflict_resolution is not None:
                self._values["conflict_resolution"] = conflict_resolution
            if consolidation is not None:
                self._values["consolidation"] = consolidation
            if enabled is not None:
                self._values["enabled"] = enabled
            if min_allowed_confidence_score_for_merging is not None:
                self._values["min_allowed_confidence_score_for_merging"] = min_allowed_confidence_score_for_merging

        @builtins.property
        def conflict_resolution(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.ConflictResolutionProperty"]]:
            '''Determines how the auto-merging process should resolve conflicts between different profiles.

            For example, if Profile A and Profile B have the same ``FirstName`` and ``LastName`` , ``ConflictResolution`` specifies which ``EmailAddress`` should be used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-automerging.html#cfn-customerprofiles-domain-automerging-conflictresolution
            '''
            result = self._values.get("conflict_resolution")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.ConflictResolutionProperty"]], result)

        @builtins.property
        def consolidation(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.ConsolidationProperty"]]:
            '''A list of matching attributes that represent matching criteria.

            If two profiles meet at least one of the requirements in the matching attributes list, they will be merged.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-automerging.html#cfn-customerprofiles-domain-automerging-consolidation
            '''
            result = self._values.get("consolidation")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.ConsolidationProperty"]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The flag that enables the auto-merging of duplicate profiles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-automerging.html#cfn-customerprofiles-domain-automerging-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def min_allowed_confidence_score_for_merging(
            self,
        ) -> typing.Optional[jsii.Number]:
            '''A number between 0 and 1 that represents the minimum confidence score required for profiles within a matching group to be merged during the auto-merge process.

            A higher score means that a higher similarity is required to merge profiles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-automerging.html#cfn-customerprofiles-domain-automerging-minallowedconfidencescoreformerging
            '''
            result = self._values.get("min_allowed_confidence_score_for_merging")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoMergingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnDomainPropsMixin.ConflictResolutionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "conflict_resolving_model": "conflictResolvingModel",
            "source_name": "sourceName",
        },
    )
    class ConflictResolutionProperty:
        def __init__(
            self,
            *,
            conflict_resolving_model: typing.Optional[builtins.str] = None,
            source_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Determines how the auto-merging process should resolve conflicts between different profiles.

            For example, if Profile A and Profile B have the same ``FirstName`` and ``LastName`` , ``ConflictResolution`` specifies which ``EmailAddress`` should be used.

            :param conflict_resolving_model: How the auto-merging process should resolve conflicts between different profiles.
            :param source_name: The ``ObjectType`` name that is used to resolve profile merging conflicts when choosing ``SOURCE`` as the ``ConflictResolvingModel`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-conflictresolution.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                conflict_resolution_property = customerprofiles_mixins.CfnDomainPropsMixin.ConflictResolutionProperty(
                    conflict_resolving_model="conflictResolvingModel",
                    source_name="sourceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9ee9d5e273dfb493ccc1d8d0df265f232ec1cc3743f511d4b5c2ae93296323ba)
                check_type(argname="argument conflict_resolving_model", value=conflict_resolving_model, expected_type=type_hints["conflict_resolving_model"])
                check_type(argname="argument source_name", value=source_name, expected_type=type_hints["source_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if conflict_resolving_model is not None:
                self._values["conflict_resolving_model"] = conflict_resolving_model
            if source_name is not None:
                self._values["source_name"] = source_name

        @builtins.property
        def conflict_resolving_model(self) -> typing.Optional[builtins.str]:
            '''How the auto-merging process should resolve conflicts between different profiles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-conflictresolution.html#cfn-customerprofiles-domain-conflictresolution-conflictresolvingmodel
            '''
            result = self._values.get("conflict_resolving_model")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_name(self) -> typing.Optional[builtins.str]:
            '''The ``ObjectType`` name that is used to resolve profile merging conflicts when choosing ``SOURCE`` as the ``ConflictResolvingModel`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-conflictresolution.html#cfn-customerprofiles-domain-conflictresolution-sourcename
            '''
            result = self._values.get("source_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConflictResolutionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnDomainPropsMixin.ConsolidationProperty",
        jsii_struct_bases=[],
        name_mapping={"matching_attributes_list": "matchingAttributesList"},
    )
    class ConsolidationProperty:
        def __init__(
            self,
            *,
            matching_attributes_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Sequence[builtins.str]]]] = None,
        ) -> None:
            '''A list of matching attributes that represent matching criteria.

            If two profiles meet at least one of the requirements in the matching attributes list, they will be merged.

            :param matching_attributes_list: A list of matching criteria.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-consolidation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                consolidation_property = customerprofiles_mixins.CfnDomainPropsMixin.ConsolidationProperty(
                    matching_attributes_list=[["matchingAttributesList"]]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b483c12a548196810d64b15ac46b308e8b03b8fc132935284c8faabf47fc2b30)
                check_type(argname="argument matching_attributes_list", value=matching_attributes_list, expected_type=type_hints["matching_attributes_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if matching_attributes_list is not None:
                self._values["matching_attributes_list"] = matching_attributes_list

        @builtins.property
        def matching_attributes_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.List[builtins.str]]]]:
            '''A list of matching criteria.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-consolidation.html#cfn-customerprofiles-domain-consolidation-matchingattributeslist
            '''
            result = self._values.get("matching_attributes_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.List[builtins.str]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConsolidationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnDomainPropsMixin.DataStoreProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "readiness": "readiness"},
    )
    class DataStoreProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            readiness: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.ReadinessProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration and status of the data store for the domain.

            :param enabled: Whether the data store is enabled.
            :param readiness: Progress information for data store setup.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-datastore.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                data_store_property = customerprofiles_mixins.CfnDomainPropsMixin.DataStoreProperty(
                    enabled=False,
                    readiness=customerprofiles_mixins.CfnDomainPropsMixin.ReadinessProperty(
                        message="message",
                        progress_percentage=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e0ed067c428bc0c8a8860941a8c62a3772a06ac1e365c7cc1cbadc4afdfd0f74)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument readiness", value=readiness, expected_type=type_hints["readiness"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if readiness is not None:
                self._values["readiness"] = readiness

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether the data store is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-datastore.html#cfn-customerprofiles-domain-datastore-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def readiness(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.ReadinessProperty"]]:
            '''Progress information for data store setup.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-datastore.html#cfn-customerprofiles-domain-datastore-readiness
            '''
            result = self._values.get("readiness")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.ReadinessProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataStoreProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnDomainPropsMixin.DomainStatsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "metering_profile_count": "meteringProfileCount",
            "object_count": "objectCount",
            "profile_count": "profileCount",
            "total_size": "totalSize",
        },
    )
    class DomainStatsProperty:
        def __init__(
            self,
            *,
            metering_profile_count: typing.Optional[jsii.Number] = None,
            object_count: typing.Optional[jsii.Number] = None,
            profile_count: typing.Optional[jsii.Number] = None,
            total_size: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Usage-specific statistics about the domain.

            :param metering_profile_count: The number of profiles that you are currently paying for in the domain. If you have more than 100 objects associated with a single profile, that profile counts as two profiles. If you have more than 200 objects, that profile counts as three, and so on.
            :param object_count: The total number of objects in domain.
            :param profile_count: The total number of profiles currently in the domain.
            :param total_size: The total size, in bytes, of all objects in the domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-domainstats.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                domain_stats_property = customerprofiles_mixins.CfnDomainPropsMixin.DomainStatsProperty(
                    metering_profile_count=123,
                    object_count=123,
                    profile_count=123,
                    total_size=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f2e538ec103a4b76473caf3164f2ec8cb73e5f6ffdcfbf69285bfc36930ba1fd)
                check_type(argname="argument metering_profile_count", value=metering_profile_count, expected_type=type_hints["metering_profile_count"])
                check_type(argname="argument object_count", value=object_count, expected_type=type_hints["object_count"])
                check_type(argname="argument profile_count", value=profile_count, expected_type=type_hints["profile_count"])
                check_type(argname="argument total_size", value=total_size, expected_type=type_hints["total_size"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metering_profile_count is not None:
                self._values["metering_profile_count"] = metering_profile_count
            if object_count is not None:
                self._values["object_count"] = object_count
            if profile_count is not None:
                self._values["profile_count"] = profile_count
            if total_size is not None:
                self._values["total_size"] = total_size

        @builtins.property
        def metering_profile_count(self) -> typing.Optional[jsii.Number]:
            '''The number of profiles that you are currently paying for in the domain.

            If you have more than 100 objects associated with a single profile, that profile counts as two profiles. If you have more than 200 objects, that profile counts as three, and so on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-domainstats.html#cfn-customerprofiles-domain-domainstats-meteringprofilecount
            '''
            result = self._values.get("metering_profile_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def object_count(self) -> typing.Optional[jsii.Number]:
            '''The total number of objects in domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-domainstats.html#cfn-customerprofiles-domain-domainstats-objectcount
            '''
            result = self._values.get("object_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def profile_count(self) -> typing.Optional[jsii.Number]:
            '''The total number of profiles currently in the domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-domainstats.html#cfn-customerprofiles-domain-domainstats-profilecount
            '''
            result = self._values.get("profile_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def total_size(self) -> typing.Optional[jsii.Number]:
            '''The total size, in bytes, of all objects in the domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-domainstats.html#cfn-customerprofiles-domain-domainstats-totalsize
            '''
            result = self._values.get("total_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainStatsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnDomainPropsMixin.ExportingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_exporting": "s3Exporting"},
    )
    class ExportingConfigProperty:
        def __init__(
            self,
            *,
            s3_exporting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.S3ExportingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration information for exporting Identity Resolution results, for example, to an S3 bucket.

            :param s3_exporting: The S3 location where Identity Resolution Jobs write result files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-exportingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                exporting_config_property = customerprofiles_mixins.CfnDomainPropsMixin.ExportingConfigProperty(
                    s3_exporting=customerprofiles_mixins.CfnDomainPropsMixin.S3ExportingConfigProperty(
                        s3_bucket_name="s3BucketName",
                        s3_key_name="s3KeyName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b2d0943c6471c7ac09873208dec5e990667fd5844be85093225b0c53bcb15b7c)
                check_type(argname="argument s3_exporting", value=s3_exporting, expected_type=type_hints["s3_exporting"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_exporting is not None:
                self._values["s3_exporting"] = s3_exporting

        @builtins.property
        def s3_exporting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.S3ExportingConfigProperty"]]:
            '''The S3 location where Identity Resolution Jobs write result files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-exportingconfig.html#cfn-customerprofiles-domain-exportingconfig-s3exporting
            '''
            result = self._values.get("s3_exporting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.S3ExportingConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExportingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnDomainPropsMixin.JobScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={"day_of_the_week": "dayOfTheWeek", "time": "time"},
    )
    class JobScheduleProperty:
        def __init__(
            self,
            *,
            day_of_the_week: typing.Optional[builtins.str] = None,
            time: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The day and time when do you want to start the Identity Resolution Job every week.

            :param day_of_the_week: The day when the Identity Resolution Job should run every week.
            :param time: The time when the Identity Resolution Job should run every week.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-jobschedule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                job_schedule_property = customerprofiles_mixins.CfnDomainPropsMixin.JobScheduleProperty(
                    day_of_the_week="dayOfTheWeek",
                    time="time"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a9ba44c236a989e2c3c18eb190764f7a61ee755d6fdedb29f8c8fe52877b0ed3)
                check_type(argname="argument day_of_the_week", value=day_of_the_week, expected_type=type_hints["day_of_the_week"])
                check_type(argname="argument time", value=time, expected_type=type_hints["time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if day_of_the_week is not None:
                self._values["day_of_the_week"] = day_of_the_week
            if time is not None:
                self._values["time"] = time

        @builtins.property
        def day_of_the_week(self) -> typing.Optional[builtins.str]:
            '''The day when the Identity Resolution Job should run every week.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-jobschedule.html#cfn-customerprofiles-domain-jobschedule-dayoftheweek
            '''
            result = self._values.get("day_of_the_week")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def time(self) -> typing.Optional[builtins.str]:
            '''The time when the Identity Resolution Job should run every week.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-jobschedule.html#cfn-customerprofiles-domain-jobschedule-time
            '''
            result = self._values.get("time")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JobScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnDomainPropsMixin.MatchingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_merging": "autoMerging",
            "enabled": "enabled",
            "exporting_config": "exportingConfig",
            "job_schedule": "jobSchedule",
        },
    )
    class MatchingProperty:
        def __init__(
            self,
            *,
            auto_merging: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.AutoMergingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            exporting_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.ExportingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            job_schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.JobScheduleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The process of matching duplicate profiles.

            If ``Matching = true`` , Amazon Connect Customer Profiles starts a weekly batch process called *Identity Resolution Job* . If you do not specify a date and time for the *Identity Resolution Job* to run, by default it runs every Saturday at 12AM UTC to detect duplicate profiles in your domains. After the *Identity Resolution Job* completes, use the ``GetMatches`` API to return and review the results. Or, if you have configured ``ExportingConfig`` in the ``MatchingRequest`` , you can download the results from S3.

            :param auto_merging: Configuration information about the auto-merging process.
            :param enabled: The flag that enables the matching process of duplicate profiles.
            :param exporting_config: The S3 location where Identity Resolution Jobs write result files.
            :param job_schedule: The day and time when do you want to start the Identity Resolution Job every week.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-matching.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                matching_property = customerprofiles_mixins.CfnDomainPropsMixin.MatchingProperty(
                    auto_merging=customerprofiles_mixins.CfnDomainPropsMixin.AutoMergingProperty(
                        conflict_resolution=customerprofiles_mixins.CfnDomainPropsMixin.ConflictResolutionProperty(
                            conflict_resolving_model="conflictResolvingModel",
                            source_name="sourceName"
                        ),
                        consolidation=customerprofiles_mixins.CfnDomainPropsMixin.ConsolidationProperty(
                            matching_attributes_list=[["matchingAttributesList"]]
                        ),
                        enabled=False,
                        min_allowed_confidence_score_for_merging=123
                    ),
                    enabled=False,
                    exporting_config=customerprofiles_mixins.CfnDomainPropsMixin.ExportingConfigProperty(
                        s3_exporting=customerprofiles_mixins.CfnDomainPropsMixin.S3ExportingConfigProperty(
                            s3_bucket_name="s3BucketName",
                            s3_key_name="s3KeyName"
                        )
                    ),
                    job_schedule=customerprofiles_mixins.CfnDomainPropsMixin.JobScheduleProperty(
                        day_of_the_week="dayOfTheWeek",
                        time="time"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c20ffd5d6a6b082a4dc00316178a09554280c7d416f41693bb23d656678f02f9)
                check_type(argname="argument auto_merging", value=auto_merging, expected_type=type_hints["auto_merging"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument exporting_config", value=exporting_config, expected_type=type_hints["exporting_config"])
                check_type(argname="argument job_schedule", value=job_schedule, expected_type=type_hints["job_schedule"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_merging is not None:
                self._values["auto_merging"] = auto_merging
            if enabled is not None:
                self._values["enabled"] = enabled
            if exporting_config is not None:
                self._values["exporting_config"] = exporting_config
            if job_schedule is not None:
                self._values["job_schedule"] = job_schedule

        @builtins.property
        def auto_merging(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.AutoMergingProperty"]]:
            '''Configuration information about the auto-merging process.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-matching.html#cfn-customerprofiles-domain-matching-automerging
            '''
            result = self._values.get("auto_merging")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.AutoMergingProperty"]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The flag that enables the matching process of duplicate profiles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-matching.html#cfn-customerprofiles-domain-matching-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def exporting_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.ExportingConfigProperty"]]:
            '''The S3 location where Identity Resolution Jobs write result files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-matching.html#cfn-customerprofiles-domain-matching-exportingconfig
            '''
            result = self._values.get("exporting_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.ExportingConfigProperty"]], result)

        @builtins.property
        def job_schedule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.JobScheduleProperty"]]:
            '''The day and time when do you want to start the Identity Resolution Job every week.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-matching.html#cfn-customerprofiles-domain-matching-jobschedule
            '''
            result = self._values.get("job_schedule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.JobScheduleProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MatchingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnDomainPropsMixin.MatchingRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"rule": "rule"},
    )
    class MatchingRuleProperty:
        def __init__(
            self,
            *,
            rule: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies how the rule-based matching process should match profiles.

            :param rule: A single rule level of the ``MatchRules`` . Configures how the rule-based matching process should match profiles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-matchingrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                matching_rule_property = customerprofiles_mixins.CfnDomainPropsMixin.MatchingRuleProperty(
                    rule=["rule"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6b3cb437b2fd7948f12b1fac47ad3ef7ed8bbeb5359981642efa4730c735891c)
                check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rule is not None:
                self._values["rule"] = rule

        @builtins.property
        def rule(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A single rule level of the ``MatchRules`` .

            Configures how the rule-based matching process should match profiles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-matchingrule.html#cfn-customerprofiles-domain-matchingrule-rule
            '''
            result = self._values.get("rule")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MatchingRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnDomainPropsMixin.ReadinessProperty",
        jsii_struct_bases=[],
        name_mapping={
            "message": "message",
            "progress_percentage": "progressPercentage",
        },
    )
    class ReadinessProperty:
        def __init__(
            self,
            *,
            message: typing.Optional[builtins.str] = None,
            progress_percentage: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Progress information for data store setup.

            :param message: A message describing the current progress.
            :param progress_percentage: The percentage of progress completed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-readiness.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                readiness_property = customerprofiles_mixins.CfnDomainPropsMixin.ReadinessProperty(
                    message="message",
                    progress_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c4be92d96a40955ddd84b92186525ce0b8c0ac8ac85f48beb6765122a3c0fe34)
                check_type(argname="argument message", value=message, expected_type=type_hints["message"])
                check_type(argname="argument progress_percentage", value=progress_percentage, expected_type=type_hints["progress_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if message is not None:
                self._values["message"] = message
            if progress_percentage is not None:
                self._values["progress_percentage"] = progress_percentage

        @builtins.property
        def message(self) -> typing.Optional[builtins.str]:
            '''A message describing the current progress.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-readiness.html#cfn-customerprofiles-domain-readiness-message
            '''
            result = self._values.get("message")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def progress_percentage(self) -> typing.Optional[jsii.Number]:
            '''The percentage of progress completed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-readiness.html#cfn-customerprofiles-domain-readiness-progresspercentage
            '''
            result = self._values.get("progress_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReadinessProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnDomainPropsMixin.RuleBasedMatchingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute_types_selector": "attributeTypesSelector",
            "conflict_resolution": "conflictResolution",
            "enabled": "enabled",
            "exporting_config": "exportingConfig",
            "matching_rules": "matchingRules",
            "max_allowed_rule_level_for_matching": "maxAllowedRuleLevelForMatching",
            "max_allowed_rule_level_for_merging": "maxAllowedRuleLevelForMerging",
            "status": "status",
        },
    )
    class RuleBasedMatchingProperty:
        def __init__(
            self,
            *,
            attribute_types_selector: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.AttributeTypesSelectorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            conflict_resolution: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.ConflictResolutionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            exporting_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.ExportingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            matching_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.MatchingRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            max_allowed_rule_level_for_matching: typing.Optional[jsii.Number] = None,
            max_allowed_rule_level_for_merging: typing.Optional[jsii.Number] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The process of matching duplicate profiles using Rule-Based matching.

            If ``RuleBasedMatching = true`` , Amazon Connect Customer Profiles will start to match and merge your profiles according to your configuration in the ``RuleBasedMatchingRequest`` . You can use the ``ListRuleBasedMatches`` and ``GetSimilarProfiles`` API to return and review the results. Also, if you have configured ``ExportingConfig`` in the ``RuleBasedMatchingRequest`` , you can download the results from S3.

            :param attribute_types_selector: Configures information about the ``AttributeTypesSelector`` where the rule-based identity resolution uses to match profiles.
            :param conflict_resolution: Determines how the auto-merging process should resolve conflicts between different profiles. For example, if Profile A and Profile B have the same ``FirstName`` and ``LastName`` , ``ConflictResolution`` specifies which ``EmailAddress`` should be used.
            :param enabled: The flag that enables the matching process of duplicate profiles.
            :param exporting_config: The S3 location where Identity Resolution Jobs write result files.
            :param matching_rules: Configures how the rule-based matching process should match profiles. You can have up to 15 ``MatchingRule`` in the ``MatchingRules`` .
            :param max_allowed_rule_level_for_matching: Indicates the maximum allowed rule level for matching.
            :param max_allowed_rule_level_for_merging: Indicates the maximum allowed rule level for merging.
            :param status: The status of rule-based matching rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-rulebasedmatching.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                rule_based_matching_property = customerprofiles_mixins.CfnDomainPropsMixin.RuleBasedMatchingProperty(
                    attribute_types_selector=customerprofiles_mixins.CfnDomainPropsMixin.AttributeTypesSelectorProperty(
                        address=["address"],
                        attribute_matching_model="attributeMatchingModel",
                        email_address=["emailAddress"],
                        phone_number=["phoneNumber"]
                    ),
                    conflict_resolution=customerprofiles_mixins.CfnDomainPropsMixin.ConflictResolutionProperty(
                        conflict_resolving_model="conflictResolvingModel",
                        source_name="sourceName"
                    ),
                    enabled=False,
                    exporting_config=customerprofiles_mixins.CfnDomainPropsMixin.ExportingConfigProperty(
                        s3_exporting=customerprofiles_mixins.CfnDomainPropsMixin.S3ExportingConfigProperty(
                            s3_bucket_name="s3BucketName",
                            s3_key_name="s3KeyName"
                        )
                    ),
                    matching_rules=[customerprofiles_mixins.CfnDomainPropsMixin.MatchingRuleProperty(
                        rule=["rule"]
                    )],
                    max_allowed_rule_level_for_matching=123,
                    max_allowed_rule_level_for_merging=123,
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bbca0175e3a2739a4e91d6d773afb25ee508bddddcd1fa2e2e8861ed708b9e78)
                check_type(argname="argument attribute_types_selector", value=attribute_types_selector, expected_type=type_hints["attribute_types_selector"])
                check_type(argname="argument conflict_resolution", value=conflict_resolution, expected_type=type_hints["conflict_resolution"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument exporting_config", value=exporting_config, expected_type=type_hints["exporting_config"])
                check_type(argname="argument matching_rules", value=matching_rules, expected_type=type_hints["matching_rules"])
                check_type(argname="argument max_allowed_rule_level_for_matching", value=max_allowed_rule_level_for_matching, expected_type=type_hints["max_allowed_rule_level_for_matching"])
                check_type(argname="argument max_allowed_rule_level_for_merging", value=max_allowed_rule_level_for_merging, expected_type=type_hints["max_allowed_rule_level_for_merging"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute_types_selector is not None:
                self._values["attribute_types_selector"] = attribute_types_selector
            if conflict_resolution is not None:
                self._values["conflict_resolution"] = conflict_resolution
            if enabled is not None:
                self._values["enabled"] = enabled
            if exporting_config is not None:
                self._values["exporting_config"] = exporting_config
            if matching_rules is not None:
                self._values["matching_rules"] = matching_rules
            if max_allowed_rule_level_for_matching is not None:
                self._values["max_allowed_rule_level_for_matching"] = max_allowed_rule_level_for_matching
            if max_allowed_rule_level_for_merging is not None:
                self._values["max_allowed_rule_level_for_merging"] = max_allowed_rule_level_for_merging
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def attribute_types_selector(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.AttributeTypesSelectorProperty"]]:
            '''Configures information about the ``AttributeTypesSelector`` where the rule-based identity resolution uses to match profiles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-rulebasedmatching.html#cfn-customerprofiles-domain-rulebasedmatching-attributetypesselector
            '''
            result = self._values.get("attribute_types_selector")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.AttributeTypesSelectorProperty"]], result)

        @builtins.property
        def conflict_resolution(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.ConflictResolutionProperty"]]:
            '''Determines how the auto-merging process should resolve conflicts between different profiles.

            For example, if Profile A and Profile B have the same ``FirstName`` and ``LastName`` , ``ConflictResolution`` specifies which ``EmailAddress`` should be used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-rulebasedmatching.html#cfn-customerprofiles-domain-rulebasedmatching-conflictresolution
            '''
            result = self._values.get("conflict_resolution")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.ConflictResolutionProperty"]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The flag that enables the matching process of duplicate profiles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-rulebasedmatching.html#cfn-customerprofiles-domain-rulebasedmatching-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def exporting_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.ExportingConfigProperty"]]:
            '''The S3 location where Identity Resolution Jobs write result files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-rulebasedmatching.html#cfn-customerprofiles-domain-rulebasedmatching-exportingconfig
            '''
            result = self._values.get("exporting_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.ExportingConfigProperty"]], result)

        @builtins.property
        def matching_rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.MatchingRuleProperty"]]]]:
            '''Configures how the rule-based matching process should match profiles.

            You can have up to 15 ``MatchingRule`` in the ``MatchingRules`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-rulebasedmatching.html#cfn-customerprofiles-domain-rulebasedmatching-matchingrules
            '''
            result = self._values.get("matching_rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.MatchingRuleProperty"]]]], result)

        @builtins.property
        def max_allowed_rule_level_for_matching(self) -> typing.Optional[jsii.Number]:
            '''Indicates the maximum allowed rule level for matching.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-rulebasedmatching.html#cfn-customerprofiles-domain-rulebasedmatching-maxallowedrulelevelformatching
            '''
            result = self._values.get("max_allowed_rule_level_for_matching")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_allowed_rule_level_for_merging(self) -> typing.Optional[jsii.Number]:
            '''Indicates the maximum allowed rule level for merging.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-rulebasedmatching.html#cfn-customerprofiles-domain-rulebasedmatching-maxallowedrulelevelformerging
            '''
            result = self._values.get("max_allowed_rule_level_for_merging")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of rule-based matching rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-rulebasedmatching.html#cfn-customerprofiles-domain-rulebasedmatching-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleBasedMatchingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnDomainPropsMixin.S3ExportingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_bucket_name": "s3BucketName", "s3_key_name": "s3KeyName"},
    )
    class S3ExportingConfigProperty:
        def __init__(
            self,
            *,
            s3_bucket_name: typing.Optional[builtins.str] = None,
            s3_key_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The S3 location where Identity Resolution Jobs write result files.

            :param s3_bucket_name: The name of the S3 bucket where Identity Resolution Jobs write result files.
            :param s3_key_name: The S3 key name of the location where Identity Resolution Jobs write result files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-s3exportingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                s3_exporting_config_property = customerprofiles_mixins.CfnDomainPropsMixin.S3ExportingConfigProperty(
                    s3_bucket_name="s3BucketName",
                    s3_key_name="s3KeyName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b6cc0efdfd4d85083ee99a850dfd71ac1e40a5187777fe07e572705a0da40f84)
                check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
                check_type(argname="argument s3_key_name", value=s3_key_name, expected_type=type_hints["s3_key_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_bucket_name is not None:
                self._values["s3_bucket_name"] = s3_bucket_name
            if s3_key_name is not None:
                self._values["s3_key_name"] = s3_key_name

        @builtins.property
        def s3_bucket_name(self) -> typing.Optional[builtins.str]:
            '''The name of the S3 bucket where Identity Resolution Jobs write result files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-s3exportingconfig.html#cfn-customerprofiles-domain-s3exportingconfig-s3bucketname
            '''
            result = self._values.get("s3_bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_key_name(self) -> typing.Optional[builtins.str]:
            '''The S3 key name of the location where Identity Resolution Jobs write result files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-domain-s3exportingconfig.html#cfn-customerprofiles-domain-s3exportingconfig-s3keyname
            '''
            result = self._values.get("s3_key_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ExportingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnEventStreamMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "event_stream_name": "eventStreamName",
        "tags": "tags",
        "uri": "uri",
    },
)
class CfnEventStreamMixinProps:
    def __init__(
        self,
        *,
        domain_name: typing.Optional[builtins.str] = None,
        event_stream_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnEventStreamPropsMixin.

        :param domain_name: The unique name of the domain.
        :param event_stream_name: The name of the event stream.
        :param tags: The tags used to organize, track, or control access for this resource.
        :param uri: The StreamARN of the destination to deliver profile events to. For example, arn:aws:kinesis:region:account-id:stream/stream-name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-eventstream.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
            
            cfn_event_stream_mixin_props = customerprofiles_mixins.CfnEventStreamMixinProps(
                domain_name="domainName",
                event_stream_name="eventStreamName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                uri="uri"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b764b6cb778f30e7e4ab007beb82d68096b20f7370187293c74a1f9493bd41bf)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument event_stream_name", value=event_stream_name, expected_type=type_hints["event_stream_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if event_stream_name is not None:
            self._values["event_stream_name"] = event_stream_name
        if tags is not None:
            self._values["tags"] = tags
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The unique name of the domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-eventstream.html#cfn-customerprofiles-eventstream-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_stream_name(self) -> typing.Optional[builtins.str]:
        '''The name of the event stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-eventstream.html#cfn-customerprofiles-eventstream-eventstreamname
        '''
        result = self._values.get("event_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-eventstream.html#cfn-customerprofiles-eventstream-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''The StreamARN of the destination to deliver profile events to.

        For example, arn:aws:kinesis:region:account-id:stream/stream-name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-eventstream.html#cfn-customerprofiles-eventstream-uri
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEventStreamMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEventStreamPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnEventStreamPropsMixin",
):
    '''An Event Stream resource of Amazon Connect Customer Profiles.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-eventstream.html
    :cloudformationResource: AWS::CustomerProfiles::EventStream
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
        
        cfn_event_stream_props_mixin = customerprofiles_mixins.CfnEventStreamPropsMixin(customerprofiles_mixins.CfnEventStreamMixinProps(
            domain_name="domainName",
            event_stream_name="eventStreamName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            uri="uri"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEventStreamMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CustomerProfiles::EventStream``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb6fb2781e80d57cdd21e259c236e6bdfae2f8684a1e074af4493c6678949e1d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a3c4cb30ca4d9a0f56c43787fc9ec6638a91c05e44264150eddf3e2d0728342)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32c13f19d5ab3cc1a44102224a82a6e921a1d254c50843ad244a54ca23955452)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEventStreamMixinProps:
        return typing.cast(CfnEventStreamMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnEventStreamPropsMixin.DestinationDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status", "uri": "uri"},
    )
    class DestinationDetailsProperty:
        def __init__(
            self,
            *,
            status: typing.Optional[builtins.str] = None,
            uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Details regarding the Kinesis stream.

            :param status: The status of enabling the Kinesis stream as a destination for export.
            :param uri: The StreamARN of the destination to deliver profile events to. For example, arn:aws:kinesis:region:account-id:stream/stream-name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-eventstream-destinationdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                destination_details_property = customerprofiles_mixins.CfnEventStreamPropsMixin.DestinationDetailsProperty(
                    status="status",
                    uri="uri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fa832c273e05b31f1cea288406119d23523ec6050210209f617b715fc88d0a8e)
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if status is not None:
                self._values["status"] = status
            if uri is not None:
                self._values["uri"] = uri

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of enabling the Kinesis stream as a destination for export.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-eventstream-destinationdetails.html#cfn-customerprofiles-eventstream-destinationdetails-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def uri(self) -> typing.Optional[builtins.str]:
            '''The StreamARN of the destination to deliver profile events to.

            For example, arn:aws:kinesis:region:account-id:stream/stream-name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-eventstream-destinationdetails.html#cfn-customerprofiles-eventstream-destinationdetails-uri
            '''
            result = self._values.get("uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnEventTriggerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "domain_name": "domainName",
        "event_trigger_conditions": "eventTriggerConditions",
        "event_trigger_limits": "eventTriggerLimits",
        "event_trigger_name": "eventTriggerName",
        "object_type_name": "objectTypeName",
        "segment_filter": "segmentFilter",
        "tags": "tags",
    },
)
class CfnEventTriggerMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        event_trigger_conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventTriggerPropsMixin.EventTriggerConditionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        event_trigger_limits: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventTriggerPropsMixin.EventTriggerLimitsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        event_trigger_name: typing.Optional[builtins.str] = None,
        object_type_name: typing.Optional[builtins.str] = None,
        segment_filter: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnEventTriggerPropsMixin.

        :param description: The description of the event trigger.
        :param domain_name: The unique name of the domain.
        :param event_trigger_conditions: A list of conditions that determine when an event should trigger the destination.
        :param event_trigger_limits: Defines limits controlling whether an event triggers the destination, based on ingestion latency and the number of invocations per profile over specific time periods.
        :param event_trigger_name: The unique name of the event trigger.
        :param object_type_name: The unique name of the object type.
        :param segment_filter: The destination is triggered only for profiles that meet the criteria of a segment definition.
        :param tags: An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-eventtrigger.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
            
            cfn_event_trigger_mixin_props = customerprofiles_mixins.CfnEventTriggerMixinProps(
                description="description",
                domain_name="domainName",
                event_trigger_conditions=[customerprofiles_mixins.CfnEventTriggerPropsMixin.EventTriggerConditionProperty(
                    event_trigger_dimensions=[customerprofiles_mixins.CfnEventTriggerPropsMixin.EventTriggerDimensionProperty(
                        object_attributes=[customerprofiles_mixins.CfnEventTriggerPropsMixin.ObjectAttributeProperty(
                            comparison_operator="comparisonOperator",
                            field_name="fieldName",
                            source="source",
                            values=["values"]
                        )]
                    )],
                    logical_operator="logicalOperator"
                )],
                event_trigger_limits=customerprofiles_mixins.CfnEventTriggerPropsMixin.EventTriggerLimitsProperty(
                    event_expiration=123,
                    periods=[customerprofiles_mixins.CfnEventTriggerPropsMixin.PeriodProperty(
                        max_invocations_per_profile=123,
                        unit="unit",
                        unlimited=False,
                        value=123
                    )]
                ),
                event_trigger_name="eventTriggerName",
                object_type_name="objectTypeName",
                segment_filter="segmentFilter",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90f6a4ce1a172abebd980c146669766e9afd341ff57c455ca519492dc55e7abb)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument event_trigger_conditions", value=event_trigger_conditions, expected_type=type_hints["event_trigger_conditions"])
            check_type(argname="argument event_trigger_limits", value=event_trigger_limits, expected_type=type_hints["event_trigger_limits"])
            check_type(argname="argument event_trigger_name", value=event_trigger_name, expected_type=type_hints["event_trigger_name"])
            check_type(argname="argument object_type_name", value=object_type_name, expected_type=type_hints["object_type_name"])
            check_type(argname="argument segment_filter", value=segment_filter, expected_type=type_hints["segment_filter"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if event_trigger_conditions is not None:
            self._values["event_trigger_conditions"] = event_trigger_conditions
        if event_trigger_limits is not None:
            self._values["event_trigger_limits"] = event_trigger_limits
        if event_trigger_name is not None:
            self._values["event_trigger_name"] = event_trigger_name
        if object_type_name is not None:
            self._values["object_type_name"] = object_type_name
        if segment_filter is not None:
            self._values["segment_filter"] = segment_filter
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the event trigger.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-eventtrigger.html#cfn-customerprofiles-eventtrigger-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The unique name of the domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-eventtrigger.html#cfn-customerprofiles-eventtrigger-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_trigger_conditions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventTriggerPropsMixin.EventTriggerConditionProperty"]]]]:
        '''A list of conditions that determine when an event should trigger the destination.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-eventtrigger.html#cfn-customerprofiles-eventtrigger-eventtriggerconditions
        '''
        result = self._values.get("event_trigger_conditions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventTriggerPropsMixin.EventTriggerConditionProperty"]]]], result)

    @builtins.property
    def event_trigger_limits(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventTriggerPropsMixin.EventTriggerLimitsProperty"]]:
        '''Defines limits controlling whether an event triggers the destination, based on ingestion latency and the number of invocations per profile over specific time periods.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-eventtrigger.html#cfn-customerprofiles-eventtrigger-eventtriggerlimits
        '''
        result = self._values.get("event_trigger_limits")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventTriggerPropsMixin.EventTriggerLimitsProperty"]], result)

    @builtins.property
    def event_trigger_name(self) -> typing.Optional[builtins.str]:
        '''The unique name of the event trigger.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-eventtrigger.html#cfn-customerprofiles-eventtrigger-eventtriggername
        '''
        result = self._values.get("event_trigger_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_type_name(self) -> typing.Optional[builtins.str]:
        '''The unique name of the object type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-eventtrigger.html#cfn-customerprofiles-eventtrigger-objecttypename
        '''
        result = self._values.get("object_type_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def segment_filter(self) -> typing.Optional[builtins.str]:
        '''The destination is triggered only for profiles that meet the criteria of a segment definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-eventtrigger.html#cfn-customerprofiles-eventtrigger-segmentfilter
        '''
        result = self._values.get("segment_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-eventtrigger.html#cfn-customerprofiles-eventtrigger-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEventTriggerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEventTriggerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnEventTriggerPropsMixin",
):
    '''Specifies the rules to perform an action based on customer ingested data.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-eventtrigger.html
    :cloudformationResource: AWS::CustomerProfiles::EventTrigger
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
        
        cfn_event_trigger_props_mixin = customerprofiles_mixins.CfnEventTriggerPropsMixin(customerprofiles_mixins.CfnEventTriggerMixinProps(
            description="description",
            domain_name="domainName",
            event_trigger_conditions=[customerprofiles_mixins.CfnEventTriggerPropsMixin.EventTriggerConditionProperty(
                event_trigger_dimensions=[customerprofiles_mixins.CfnEventTriggerPropsMixin.EventTriggerDimensionProperty(
                    object_attributes=[customerprofiles_mixins.CfnEventTriggerPropsMixin.ObjectAttributeProperty(
                        comparison_operator="comparisonOperator",
                        field_name="fieldName",
                        source="source",
                        values=["values"]
                    )]
                )],
                logical_operator="logicalOperator"
            )],
            event_trigger_limits=customerprofiles_mixins.CfnEventTriggerPropsMixin.EventTriggerLimitsProperty(
                event_expiration=123,
                periods=[customerprofiles_mixins.CfnEventTriggerPropsMixin.PeriodProperty(
                    max_invocations_per_profile=123,
                    unit="unit",
                    unlimited=False,
                    value=123
                )]
            ),
            event_trigger_name="eventTriggerName",
            object_type_name="objectTypeName",
            segment_filter="segmentFilter",
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
        props: typing.Union[CfnEventTriggerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CustomerProfiles::EventTrigger``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb9fac16bd914b5707c22659bafdec4b3a4b8b0babf40133fdfbd195eeb57245)
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
            type_hints = typing.get_type_hints(_typecheckingstub__511c8b9fe27cfd375cf0d2cfb4f107812c15177f359f9b212981e42af2dcf67d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e937d73370d337142ae9d6dfc59b3af266761c751383c89aeed387dc9d3698a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEventTriggerMixinProps:
        return typing.cast(CfnEventTriggerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnEventTriggerPropsMixin.EventTriggerConditionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "event_trigger_dimensions": "eventTriggerDimensions",
            "logical_operator": "logicalOperator",
        },
    )
    class EventTriggerConditionProperty:
        def __init__(
            self,
            *,
            event_trigger_dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventTriggerPropsMixin.EventTriggerDimensionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            logical_operator: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the circumstances under which the event should trigger the destination.

            :param event_trigger_dimensions: A list of dimensions to be evaluated for the event.
            :param logical_operator: The operator used to combine multiple dimensions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-eventtrigger-eventtriggercondition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                event_trigger_condition_property = customerprofiles_mixins.CfnEventTriggerPropsMixin.EventTriggerConditionProperty(
                    event_trigger_dimensions=[customerprofiles_mixins.CfnEventTriggerPropsMixin.EventTriggerDimensionProperty(
                        object_attributes=[customerprofiles_mixins.CfnEventTriggerPropsMixin.ObjectAttributeProperty(
                            comparison_operator="comparisonOperator",
                            field_name="fieldName",
                            source="source",
                            values=["values"]
                        )]
                    )],
                    logical_operator="logicalOperator"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a9974cd57fe093dcc44e2d7cfcec568b7ed72a3c3e84b050adc9988392012d82)
                check_type(argname="argument event_trigger_dimensions", value=event_trigger_dimensions, expected_type=type_hints["event_trigger_dimensions"])
                check_type(argname="argument logical_operator", value=logical_operator, expected_type=type_hints["logical_operator"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if event_trigger_dimensions is not None:
                self._values["event_trigger_dimensions"] = event_trigger_dimensions
            if logical_operator is not None:
                self._values["logical_operator"] = logical_operator

        @builtins.property
        def event_trigger_dimensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventTriggerPropsMixin.EventTriggerDimensionProperty"]]]]:
            '''A list of dimensions to be evaluated for the event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-eventtrigger-eventtriggercondition.html#cfn-customerprofiles-eventtrigger-eventtriggercondition-eventtriggerdimensions
            '''
            result = self._values.get("event_trigger_dimensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventTriggerPropsMixin.EventTriggerDimensionProperty"]]]], result)

        @builtins.property
        def logical_operator(self) -> typing.Optional[builtins.str]:
            '''The operator used to combine multiple dimensions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-eventtrigger-eventtriggercondition.html#cfn-customerprofiles-eventtrigger-eventtriggercondition-logicaloperator
            '''
            result = self._values.get("logical_operator")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventTriggerConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnEventTriggerPropsMixin.EventTriggerDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"object_attributes": "objectAttributes"},
    )
    class EventTriggerDimensionProperty:
        def __init__(
            self,
            *,
            object_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventTriggerPropsMixin.ObjectAttributeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A specific event dimension to be assessed.

            :param object_attributes: A list of object attributes to be evaluated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-eventtrigger-eventtriggerdimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                event_trigger_dimension_property = customerprofiles_mixins.CfnEventTriggerPropsMixin.EventTriggerDimensionProperty(
                    object_attributes=[customerprofiles_mixins.CfnEventTriggerPropsMixin.ObjectAttributeProperty(
                        comparison_operator="comparisonOperator",
                        field_name="fieldName",
                        source="source",
                        values=["values"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c2c1d961471f12a049513cf55e93a58191657ecfd2986607dda747ca9b172acb)
                check_type(argname="argument object_attributes", value=object_attributes, expected_type=type_hints["object_attributes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object_attributes is not None:
                self._values["object_attributes"] = object_attributes

        @builtins.property
        def object_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventTriggerPropsMixin.ObjectAttributeProperty"]]]]:
            '''A list of object attributes to be evaluated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-eventtrigger-eventtriggerdimension.html#cfn-customerprofiles-eventtrigger-eventtriggerdimension-objectattributes
            '''
            result = self._values.get("object_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventTriggerPropsMixin.ObjectAttributeProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventTriggerDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnEventTriggerPropsMixin.EventTriggerLimitsProperty",
        jsii_struct_bases=[],
        name_mapping={"event_expiration": "eventExpiration", "periods": "periods"},
    )
    class EventTriggerLimitsProperty:
        def __init__(
            self,
            *,
            event_expiration: typing.Optional[jsii.Number] = None,
            periods: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventTriggerPropsMixin.PeriodProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Defines limits controlling whether an event triggers the destination, based on ingestion latency and the number of invocations per profile over specific time periods.

            :param event_expiration: Specifies that an event will only trigger the destination if it is processed within a certain latency period.
            :param periods: A list of time periods during which the limits apply.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-eventtrigger-eventtriggerlimits.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                event_trigger_limits_property = customerprofiles_mixins.CfnEventTriggerPropsMixin.EventTriggerLimitsProperty(
                    event_expiration=123,
                    periods=[customerprofiles_mixins.CfnEventTriggerPropsMixin.PeriodProperty(
                        max_invocations_per_profile=123,
                        unit="unit",
                        unlimited=False,
                        value=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__74c4636c1ce207d50ac76829f142d4bb24f094e43b90cc04843c84ae2c1a3648)
                check_type(argname="argument event_expiration", value=event_expiration, expected_type=type_hints["event_expiration"])
                check_type(argname="argument periods", value=periods, expected_type=type_hints["periods"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if event_expiration is not None:
                self._values["event_expiration"] = event_expiration
            if periods is not None:
                self._values["periods"] = periods

        @builtins.property
        def event_expiration(self) -> typing.Optional[jsii.Number]:
            '''Specifies that an event will only trigger the destination if it is processed within a certain latency period.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-eventtrigger-eventtriggerlimits.html#cfn-customerprofiles-eventtrigger-eventtriggerlimits-eventexpiration
            '''
            result = self._values.get("event_expiration")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def periods(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventTriggerPropsMixin.PeriodProperty"]]]]:
            '''A list of time periods during which the limits apply.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-eventtrigger-eventtriggerlimits.html#cfn-customerprofiles-eventtrigger-eventtriggerlimits-periods
            '''
            result = self._values.get("periods")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventTriggerPropsMixin.PeriodProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventTriggerLimitsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnEventTriggerPropsMixin.ObjectAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "comparison_operator": "comparisonOperator",
            "field_name": "fieldName",
            "source": "source",
            "values": "values",
        },
    )
    class ObjectAttributeProperty:
        def __init__(
            self,
            *,
            comparison_operator: typing.Optional[builtins.str] = None,
            field_name: typing.Optional[builtins.str] = None,
            source: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The criteria that a specific object attribute must meet to trigger the destination.

            :param comparison_operator: The operator used to compare an attribute against a list of values.
            :param field_name: A field defined within an object type.
            :param source: An attribute contained within a source object.
            :param values: The amount of time of the specified unit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-eventtrigger-objectattribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                object_attribute_property = customerprofiles_mixins.CfnEventTriggerPropsMixin.ObjectAttributeProperty(
                    comparison_operator="comparisonOperator",
                    field_name="fieldName",
                    source="source",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5d3b7eb87d48dd7856f13c914e93e06184ed55f035c73e31175d714154e5363c)
                check_type(argname="argument comparison_operator", value=comparison_operator, expected_type=type_hints["comparison_operator"])
                check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comparison_operator is not None:
                self._values["comparison_operator"] = comparison_operator
            if field_name is not None:
                self._values["field_name"] = field_name
            if source is not None:
                self._values["source"] = source
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def comparison_operator(self) -> typing.Optional[builtins.str]:
            '''The operator used to compare an attribute against a list of values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-eventtrigger-objectattribute.html#cfn-customerprofiles-eventtrigger-objectattribute-comparisonoperator
            '''
            result = self._values.get("comparison_operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def field_name(self) -> typing.Optional[builtins.str]:
            '''A field defined within an object type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-eventtrigger-objectattribute.html#cfn-customerprofiles-eventtrigger-objectattribute-fieldname
            '''
            result = self._values.get("field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''An attribute contained within a source object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-eventtrigger-objectattribute.html#cfn-customerprofiles-eventtrigger-objectattribute-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The amount of time of the specified unit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-eventtrigger-objectattribute.html#cfn-customerprofiles-eventtrigger-objectattribute-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ObjectAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnEventTriggerPropsMixin.PeriodProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_invocations_per_profile": "maxInvocationsPerProfile",
            "unit": "unit",
            "unlimited": "unlimited",
            "value": "value",
        },
    )
    class PeriodProperty:
        def __init__(
            self,
            *,
            max_invocations_per_profile: typing.Optional[jsii.Number] = None,
            unit: typing.Optional[builtins.str] = None,
            unlimited: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Defines a limit and the time period during which it is enforced.

            :param max_invocations_per_profile: The maximum allowed number of destination invocations per profile.
            :param unit: The unit of time.
            :param unlimited: If set to true, there is no limit on the number of destination invocations per profile. The default is false.
            :param value: The amount of time of the specified unit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-eventtrigger-period.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                period_property = customerprofiles_mixins.CfnEventTriggerPropsMixin.PeriodProperty(
                    max_invocations_per_profile=123,
                    unit="unit",
                    unlimited=False,
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__95a8f3360908208d60458656fdcc69c2b08a547364680e8a9b5a213534114817)
                check_type(argname="argument max_invocations_per_profile", value=max_invocations_per_profile, expected_type=type_hints["max_invocations_per_profile"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
                check_type(argname="argument unlimited", value=unlimited, expected_type=type_hints["unlimited"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_invocations_per_profile is not None:
                self._values["max_invocations_per_profile"] = max_invocations_per_profile
            if unit is not None:
                self._values["unit"] = unit
            if unlimited is not None:
                self._values["unlimited"] = unlimited
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def max_invocations_per_profile(self) -> typing.Optional[jsii.Number]:
            '''The maximum allowed number of destination invocations per profile.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-eventtrigger-period.html#cfn-customerprofiles-eventtrigger-period-maxinvocationsperprofile
            '''
            result = self._values.get("max_invocations_per_profile")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The unit of time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-eventtrigger-period.html#cfn-customerprofiles-eventtrigger-period-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unlimited(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If set to true, there is no limit on the number of destination invocations per profile.

            The default is false.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-eventtrigger-period.html#cfn-customerprofiles-eventtrigger-period-unlimited
            '''
            result = self._values.get("unlimited")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''The amount of time of the specified unit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-eventtrigger-period.html#cfn-customerprofiles-eventtrigger-period-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PeriodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnIntegrationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "event_trigger_names": "eventTriggerNames",
        "flow_definition": "flowDefinition",
        "object_type_name": "objectTypeName",
        "object_type_names": "objectTypeNames",
        "tags": "tags",
        "uri": "uri",
    },
)
class CfnIntegrationMixinProps:
    def __init__(
        self,
        *,
        domain_name: typing.Optional[builtins.str] = None,
        event_trigger_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        flow_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIntegrationPropsMixin.FlowDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        object_type_name: typing.Optional[builtins.str] = None,
        object_type_names: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIntegrationPropsMixin.ObjectTypeMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnIntegrationPropsMixin.

        :param domain_name: The unique name of the domain.
        :param event_trigger_names: A list of unique names for active event triggers associated with the integration.
        :param flow_definition: The configuration that controls how Customer Profiles retrieves data from the source.
        :param object_type_name: The name of the profile object type mapping to use.
        :param object_type_names: The object type mapping.
        :param tags: The tags used to organize, track, or control access for this resource.
        :param uri: The URI of the S3 bucket or any other type of data source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-integration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
            
            cfn_integration_mixin_props = customerprofiles_mixins.CfnIntegrationMixinProps(
                domain_name="domainName",
                event_trigger_names=["eventTriggerNames"],
                flow_definition=customerprofiles_mixins.CfnIntegrationPropsMixin.FlowDefinitionProperty(
                    description="description",
                    flow_name="flowName",
                    kms_arn="kmsArn",
                    source_flow_config=customerprofiles_mixins.CfnIntegrationPropsMixin.SourceFlowConfigProperty(
                        connector_profile_name="connectorProfileName",
                        connector_type="connectorType",
                        incremental_pull_config=customerprofiles_mixins.CfnIntegrationPropsMixin.IncrementalPullConfigProperty(
                            datetime_type_field_name="datetimeTypeFieldName"
                        ),
                        source_connector_properties=customerprofiles_mixins.CfnIntegrationPropsMixin.SourceConnectorPropertiesProperty(
                            marketo=customerprofiles_mixins.CfnIntegrationPropsMixin.MarketoSourcePropertiesProperty(
                                object="object"
                            ),
                            s3=customerprofiles_mixins.CfnIntegrationPropsMixin.S3SourcePropertiesProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix"
                            ),
                            salesforce=customerprofiles_mixins.CfnIntegrationPropsMixin.SalesforceSourcePropertiesProperty(
                                enable_dynamic_field_update=False,
                                include_deleted_records=False,
                                object="object"
                            ),
                            service_now=customerprofiles_mixins.CfnIntegrationPropsMixin.ServiceNowSourcePropertiesProperty(
                                object="object"
                            ),
                            zendesk=customerprofiles_mixins.CfnIntegrationPropsMixin.ZendeskSourcePropertiesProperty(
                                object="object"
                            )
                        )
                    ),
                    tasks=[customerprofiles_mixins.CfnIntegrationPropsMixin.TaskProperty(
                        connector_operator=customerprofiles_mixins.CfnIntegrationPropsMixin.ConnectorOperatorProperty(
                            marketo="marketo",
                            s3="s3",
                            salesforce="salesforce",
                            service_now="serviceNow",
                            zendesk="zendesk"
                        ),
                        destination_field="destinationField",
                        source_fields=["sourceFields"],
                        task_properties=[customerprofiles_mixins.CfnIntegrationPropsMixin.TaskPropertiesMapProperty(
                            operator_property_key="operatorPropertyKey",
                            property="property"
                        )],
                        task_type="taskType"
                    )],
                    trigger_config=customerprofiles_mixins.CfnIntegrationPropsMixin.TriggerConfigProperty(
                        trigger_properties=customerprofiles_mixins.CfnIntegrationPropsMixin.TriggerPropertiesProperty(
                            scheduled=customerprofiles_mixins.CfnIntegrationPropsMixin.ScheduledTriggerPropertiesProperty(
                                data_pull_mode="dataPullMode",
                                first_execution_from=123,
                                schedule_end_time=123,
                                schedule_expression="scheduleExpression",
                                schedule_offset=123,
                                schedule_start_time=123,
                                timezone="timezone"
                            )
                        ),
                        trigger_type="triggerType"
                    )
                ),
                object_type_name="objectTypeName",
                object_type_names=[customerprofiles_mixins.CfnIntegrationPropsMixin.ObjectTypeMappingProperty(
                    key="key",
                    value="value"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                uri="uri"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6fc3f999ba26c704a86766316ac389a0f0dc4ac0e4b192c45da2856aef8f743)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument event_trigger_names", value=event_trigger_names, expected_type=type_hints["event_trigger_names"])
            check_type(argname="argument flow_definition", value=flow_definition, expected_type=type_hints["flow_definition"])
            check_type(argname="argument object_type_name", value=object_type_name, expected_type=type_hints["object_type_name"])
            check_type(argname="argument object_type_names", value=object_type_names, expected_type=type_hints["object_type_names"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if event_trigger_names is not None:
            self._values["event_trigger_names"] = event_trigger_names
        if flow_definition is not None:
            self._values["flow_definition"] = flow_definition
        if object_type_name is not None:
            self._values["object_type_name"] = object_type_name
        if object_type_names is not None:
            self._values["object_type_names"] = object_type_names
        if tags is not None:
            self._values["tags"] = tags
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The unique name of the domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-integration.html#cfn-customerprofiles-integration-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_trigger_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of unique names for active event triggers associated with the integration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-integration.html#cfn-customerprofiles-integration-eventtriggernames
        '''
        result = self._values.get("event_trigger_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def flow_definition(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.FlowDefinitionProperty"]]:
        '''The configuration that controls how Customer Profiles retrieves data from the source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-integration.html#cfn-customerprofiles-integration-flowdefinition
        '''
        result = self._values.get("flow_definition")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.FlowDefinitionProperty"]], result)

    @builtins.property
    def object_type_name(self) -> typing.Optional[builtins.str]:
        '''The name of the profile object type mapping to use.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-integration.html#cfn-customerprofiles-integration-objecttypename
        '''
        result = self._values.get("object_type_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_type_names(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.ObjectTypeMappingProperty"]]]]:
        '''The object type mapping.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-integration.html#cfn-customerprofiles-integration-objecttypenames
        '''
        result = self._values.get("object_type_names")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.ObjectTypeMappingProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-integration.html#cfn-customerprofiles-integration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''The URI of the S3 bucket or any other type of data source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-integration.html#cfn-customerprofiles-integration-uri
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIntegrationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnIntegrationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnIntegrationPropsMixin",
):
    '''Specifies an Amazon Connect Customer Profiles Integration.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-integration.html
    :cloudformationResource: AWS::CustomerProfiles::Integration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
        
        cfn_integration_props_mixin = customerprofiles_mixins.CfnIntegrationPropsMixin(customerprofiles_mixins.CfnIntegrationMixinProps(
            domain_name="domainName",
            event_trigger_names=["eventTriggerNames"],
            flow_definition=customerprofiles_mixins.CfnIntegrationPropsMixin.FlowDefinitionProperty(
                description="description",
                flow_name="flowName",
                kms_arn="kmsArn",
                source_flow_config=customerprofiles_mixins.CfnIntegrationPropsMixin.SourceFlowConfigProperty(
                    connector_profile_name="connectorProfileName",
                    connector_type="connectorType",
                    incremental_pull_config=customerprofiles_mixins.CfnIntegrationPropsMixin.IncrementalPullConfigProperty(
                        datetime_type_field_name="datetimeTypeFieldName"
                    ),
                    source_connector_properties=customerprofiles_mixins.CfnIntegrationPropsMixin.SourceConnectorPropertiesProperty(
                        marketo=customerprofiles_mixins.CfnIntegrationPropsMixin.MarketoSourcePropertiesProperty(
                            object="object"
                        ),
                        s3=customerprofiles_mixins.CfnIntegrationPropsMixin.S3SourcePropertiesProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix"
                        ),
                        salesforce=customerprofiles_mixins.CfnIntegrationPropsMixin.SalesforceSourcePropertiesProperty(
                            enable_dynamic_field_update=False,
                            include_deleted_records=False,
                            object="object"
                        ),
                        service_now=customerprofiles_mixins.CfnIntegrationPropsMixin.ServiceNowSourcePropertiesProperty(
                            object="object"
                        ),
                        zendesk=customerprofiles_mixins.CfnIntegrationPropsMixin.ZendeskSourcePropertiesProperty(
                            object="object"
                        )
                    )
                ),
                tasks=[customerprofiles_mixins.CfnIntegrationPropsMixin.TaskProperty(
                    connector_operator=customerprofiles_mixins.CfnIntegrationPropsMixin.ConnectorOperatorProperty(
                        marketo="marketo",
                        s3="s3",
                        salesforce="salesforce",
                        service_now="serviceNow",
                        zendesk="zendesk"
                    ),
                    destination_field="destinationField",
                    source_fields=["sourceFields"],
                    task_properties=[customerprofiles_mixins.CfnIntegrationPropsMixin.TaskPropertiesMapProperty(
                        operator_property_key="operatorPropertyKey",
                        property="property"
                    )],
                    task_type="taskType"
                )],
                trigger_config=customerprofiles_mixins.CfnIntegrationPropsMixin.TriggerConfigProperty(
                    trigger_properties=customerprofiles_mixins.CfnIntegrationPropsMixin.TriggerPropertiesProperty(
                        scheduled=customerprofiles_mixins.CfnIntegrationPropsMixin.ScheduledTriggerPropertiesProperty(
                            data_pull_mode="dataPullMode",
                            first_execution_from=123,
                            schedule_end_time=123,
                            schedule_expression="scheduleExpression",
                            schedule_offset=123,
                            schedule_start_time=123,
                            timezone="timezone"
                        )
                    ),
                    trigger_type="triggerType"
                )
            ),
            object_type_name="objectTypeName",
            object_type_names=[customerprofiles_mixins.CfnIntegrationPropsMixin.ObjectTypeMappingProperty(
                key="key",
                value="value"
            )],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            uri="uri"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnIntegrationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CustomerProfiles::Integration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a4b35bc21a498eb5e7850f4428e95e57d05d20fef138de431be08557bf84907)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b541ddc166354967acf3d11257fad37e3b4b78d03843b97f34461333ee783e76)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a41c801ffdb9f84f20fdb22bf4baa692aae7bab9095f77bc010f39f18f0f9cdc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIntegrationMixinProps:
        return typing.cast(CfnIntegrationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnIntegrationPropsMixin.ConnectorOperatorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "marketo": "marketo",
            "s3": "s3",
            "salesforce": "salesforce",
            "service_now": "serviceNow",
            "zendesk": "zendesk",
        },
    )
    class ConnectorOperatorProperty:
        def __init__(
            self,
            *,
            marketo: typing.Optional[builtins.str] = None,
            s3: typing.Optional[builtins.str] = None,
            salesforce: typing.Optional[builtins.str] = None,
            service_now: typing.Optional[builtins.str] = None,
            zendesk: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The operation to be performed on the provided source fields.

            :param marketo: The operation to be performed on the provided Marketo source fields.
            :param s3: The operation to be performed on the provided Amazon S3 source fields.
            :param salesforce: The operation to be performed on the provided Salesforce source fields.
            :param service_now: The operation to be performed on the provided ServiceNow source fields.
            :param zendesk: The operation to be performed on the provided Zendesk source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-connectoroperator.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                connector_operator_property = customerprofiles_mixins.CfnIntegrationPropsMixin.ConnectorOperatorProperty(
                    marketo="marketo",
                    s3="s3",
                    salesforce="salesforce",
                    service_now="serviceNow",
                    zendesk="zendesk"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__93a396c389f656efc8c1cab75fac2dd65f123b5fd00e539bf8a2d50bd2181dbb)
                check_type(argname="argument marketo", value=marketo, expected_type=type_hints["marketo"])
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
                check_type(argname="argument salesforce", value=salesforce, expected_type=type_hints["salesforce"])
                check_type(argname="argument service_now", value=service_now, expected_type=type_hints["service_now"])
                check_type(argname="argument zendesk", value=zendesk, expected_type=type_hints["zendesk"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if marketo is not None:
                self._values["marketo"] = marketo
            if s3 is not None:
                self._values["s3"] = s3
            if salesforce is not None:
                self._values["salesforce"] = salesforce
            if service_now is not None:
                self._values["service_now"] = service_now
            if zendesk is not None:
                self._values["zendesk"] = zendesk

        @builtins.property
        def marketo(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Marketo source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-connectoroperator.html#cfn-customerprofiles-integration-connectoroperator-marketo
            '''
            result = self._values.get("marketo")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Amazon S3 source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-connectoroperator.html#cfn-customerprofiles-integration-connectoroperator-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def salesforce(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Salesforce source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-connectoroperator.html#cfn-customerprofiles-integration-connectoroperator-salesforce
            '''
            result = self._values.get("salesforce")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_now(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided ServiceNow source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-connectoroperator.html#cfn-customerprofiles-integration-connectoroperator-servicenow
            '''
            result = self._values.get("service_now")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def zendesk(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Zendesk source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-connectoroperator.html#cfn-customerprofiles-integration-connectoroperator-zendesk
            '''
            result = self._values.get("zendesk")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorOperatorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnIntegrationPropsMixin.FlowDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "flow_name": "flowName",
            "kms_arn": "kmsArn",
            "source_flow_config": "sourceFlowConfig",
            "tasks": "tasks",
            "trigger_config": "triggerConfig",
        },
    )
    class FlowDefinitionProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            flow_name: typing.Optional[builtins.str] = None,
            kms_arn: typing.Optional[builtins.str] = None,
            source_flow_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIntegrationPropsMixin.SourceFlowConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            tasks: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIntegrationPropsMixin.TaskProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            trigger_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIntegrationPropsMixin.TriggerConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configurations that control how Customer Profiles retrieves data from the source, Amazon AppFlow.

            Customer Profiles uses this information to create an AppFlow flow on behalf of customers.

            :param description: A description of the flow you want to create.
            :param flow_name: The specified name of the flow. Use underscores (_) or hyphens (-) only. Spaces are not allowed.
            :param kms_arn: The Amazon Resource Name (ARN) of the AWS Key Management Service (KMS) key you provide for encryption.
            :param source_flow_config: The configuration that controls how Customer Profiles retrieves data from the source.
            :param tasks: A list of tasks that Customer Profiles performs while transferring the data in the flow run.
            :param trigger_config: The trigger settings that determine how and when the flow runs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-flowdefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                flow_definition_property = customerprofiles_mixins.CfnIntegrationPropsMixin.FlowDefinitionProperty(
                    description="description",
                    flow_name="flowName",
                    kms_arn="kmsArn",
                    source_flow_config=customerprofiles_mixins.CfnIntegrationPropsMixin.SourceFlowConfigProperty(
                        connector_profile_name="connectorProfileName",
                        connector_type="connectorType",
                        incremental_pull_config=customerprofiles_mixins.CfnIntegrationPropsMixin.IncrementalPullConfigProperty(
                            datetime_type_field_name="datetimeTypeFieldName"
                        ),
                        source_connector_properties=customerprofiles_mixins.CfnIntegrationPropsMixin.SourceConnectorPropertiesProperty(
                            marketo=customerprofiles_mixins.CfnIntegrationPropsMixin.MarketoSourcePropertiesProperty(
                                object="object"
                            ),
                            s3=customerprofiles_mixins.CfnIntegrationPropsMixin.S3SourcePropertiesProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix"
                            ),
                            salesforce=customerprofiles_mixins.CfnIntegrationPropsMixin.SalesforceSourcePropertiesProperty(
                                enable_dynamic_field_update=False,
                                include_deleted_records=False,
                                object="object"
                            ),
                            service_now=customerprofiles_mixins.CfnIntegrationPropsMixin.ServiceNowSourcePropertiesProperty(
                                object="object"
                            ),
                            zendesk=customerprofiles_mixins.CfnIntegrationPropsMixin.ZendeskSourcePropertiesProperty(
                                object="object"
                            )
                        )
                    ),
                    tasks=[customerprofiles_mixins.CfnIntegrationPropsMixin.TaskProperty(
                        connector_operator=customerprofiles_mixins.CfnIntegrationPropsMixin.ConnectorOperatorProperty(
                            marketo="marketo",
                            s3="s3",
                            salesforce="salesforce",
                            service_now="serviceNow",
                            zendesk="zendesk"
                        ),
                        destination_field="destinationField",
                        source_fields=["sourceFields"],
                        task_properties=[customerprofiles_mixins.CfnIntegrationPropsMixin.TaskPropertiesMapProperty(
                            operator_property_key="operatorPropertyKey",
                            property="property"
                        )],
                        task_type="taskType"
                    )],
                    trigger_config=customerprofiles_mixins.CfnIntegrationPropsMixin.TriggerConfigProperty(
                        trigger_properties=customerprofiles_mixins.CfnIntegrationPropsMixin.TriggerPropertiesProperty(
                            scheduled=customerprofiles_mixins.CfnIntegrationPropsMixin.ScheduledTriggerPropertiesProperty(
                                data_pull_mode="dataPullMode",
                                first_execution_from=123,
                                schedule_end_time=123,
                                schedule_expression="scheduleExpression",
                                schedule_offset=123,
                                schedule_start_time=123,
                                timezone="timezone"
                            )
                        ),
                        trigger_type="triggerType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f07f9f35d6777798cd1f3e63f7fa40bd4159c25bc542cb28857ca6dfc51c8ef3)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument flow_name", value=flow_name, expected_type=type_hints["flow_name"])
                check_type(argname="argument kms_arn", value=kms_arn, expected_type=type_hints["kms_arn"])
                check_type(argname="argument source_flow_config", value=source_flow_config, expected_type=type_hints["source_flow_config"])
                check_type(argname="argument tasks", value=tasks, expected_type=type_hints["tasks"])
                check_type(argname="argument trigger_config", value=trigger_config, expected_type=type_hints["trigger_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if flow_name is not None:
                self._values["flow_name"] = flow_name
            if kms_arn is not None:
                self._values["kms_arn"] = kms_arn
            if source_flow_config is not None:
                self._values["source_flow_config"] = source_flow_config
            if tasks is not None:
                self._values["tasks"] = tasks
            if trigger_config is not None:
                self._values["trigger_config"] = trigger_config

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description of the flow you want to create.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-flowdefinition.html#cfn-customerprofiles-integration-flowdefinition-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def flow_name(self) -> typing.Optional[builtins.str]:
            '''The specified name of the flow.

            Use underscores (_) or hyphens (-) only. Spaces are not allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-flowdefinition.html#cfn-customerprofiles-integration-flowdefinition-flowname
            '''
            result = self._values.get("flow_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the AWS Key Management Service (KMS) key you provide for encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-flowdefinition.html#cfn-customerprofiles-integration-flowdefinition-kmsarn
            '''
            result = self._values.get("kms_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_flow_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.SourceFlowConfigProperty"]]:
            '''The configuration that controls how Customer Profiles retrieves data from the source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-flowdefinition.html#cfn-customerprofiles-integration-flowdefinition-sourceflowconfig
            '''
            result = self._values.get("source_flow_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.SourceFlowConfigProperty"]], result)

        @builtins.property
        def tasks(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.TaskProperty"]]]]:
            '''A list of tasks that Customer Profiles performs while transferring the data in the flow run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-flowdefinition.html#cfn-customerprofiles-integration-flowdefinition-tasks
            '''
            result = self._values.get("tasks")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.TaskProperty"]]]], result)

        @builtins.property
        def trigger_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.TriggerConfigProperty"]]:
            '''The trigger settings that determine how and when the flow runs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-flowdefinition.html#cfn-customerprofiles-integration-flowdefinition-triggerconfig
            '''
            result = self._values.get("trigger_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.TriggerConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FlowDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnIntegrationPropsMixin.IncrementalPullConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"datetime_type_field_name": "datetimeTypeFieldName"},
    )
    class IncrementalPullConfigProperty:
        def __init__(
            self,
            *,
            datetime_type_field_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration used when importing incremental records from the source.

            :param datetime_type_field_name: A field that specifies the date time or timestamp field as the criteria to use when importing incremental records from the source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-incrementalpullconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                incremental_pull_config_property = customerprofiles_mixins.CfnIntegrationPropsMixin.IncrementalPullConfigProperty(
                    datetime_type_field_name="datetimeTypeFieldName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__433e066febc112e4f4c212769645f432bd3b0d6e2f031b7bf8db48548c659608)
                check_type(argname="argument datetime_type_field_name", value=datetime_type_field_name, expected_type=type_hints["datetime_type_field_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if datetime_type_field_name is not None:
                self._values["datetime_type_field_name"] = datetime_type_field_name

        @builtins.property
        def datetime_type_field_name(self) -> typing.Optional[builtins.str]:
            '''A field that specifies the date time or timestamp field as the criteria to use when importing incremental records from the source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-incrementalpullconfig.html#cfn-customerprofiles-integration-incrementalpullconfig-datetimetypefieldname
            '''
            result = self._values.get("datetime_type_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IncrementalPullConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnIntegrationPropsMixin.MarketoSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class MarketoSourcePropertiesProperty:
        def __init__(self, *, object: typing.Optional[builtins.str] = None) -> None:
            '''The properties that are applied when Marketo is being used as a source.

            :param object: The object specified in the Marketo flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-marketosourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                marketo_source_properties_property = customerprofiles_mixins.CfnIntegrationPropsMixin.MarketoSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4ccdf500f0d6150bced9105cd438f59c30b76b2d42687fcafc2fdb6fef42d305)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the Marketo flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-marketosourceproperties.html#cfn-customerprofiles-integration-marketosourceproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MarketoSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnIntegrationPropsMixin.ObjectTypeMappingProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class ObjectTypeMappingProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A map in which each key is an event type from an external application such as Segment or Shopify, and each value is an ``ObjectTypeName`` (template) used to ingest the event.

            :param key: The key.
            :param value: The value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-objecttypemapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                object_type_mapping_property = customerprofiles_mixins.CfnIntegrationPropsMixin.ObjectTypeMappingProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0dbd7bd13bf311c10b0322cc4afa8c4d0f41237e43230b124aece81a42703ddf)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-objecttypemapping.html#cfn-customerprofiles-integration-objecttypemapping-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-objecttypemapping.html#cfn-customerprofiles-integration-objecttypemapping-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ObjectTypeMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnIntegrationPropsMixin.S3SourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName", "bucket_prefix": "bucketPrefix"},
    )
    class S3SourcePropertiesProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            bucket_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The properties that are applied when Amazon S3 is being used as the flow source.

            :param bucket_name: The Amazon S3 bucket name where the source files are stored.
            :param bucket_prefix: The object key for the Amazon S3 bucket in which the source files are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-s3sourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                s3_source_properties_property = customerprofiles_mixins.CfnIntegrationPropsMixin.S3SourcePropertiesProperty(
                    bucket_name="bucketName",
                    bucket_prefix="bucketPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__df75a4a797c99ec5ec7d95b756aab744c1fca4c18b05924a8f339435326f7449)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 bucket name where the source files are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-s3sourceproperties.html#cfn-customerprofiles-integration-s3sourceproperties-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''The object key for the Amazon S3 bucket in which the source files are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-s3sourceproperties.html#cfn-customerprofiles-integration-s3sourceproperties-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3SourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnIntegrationPropsMixin.SalesforceSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enable_dynamic_field_update": "enableDynamicFieldUpdate",
            "include_deleted_records": "includeDeletedRecords",
            "object": "object",
        },
    )
    class SalesforceSourcePropertiesProperty:
        def __init__(
            self,
            *,
            enable_dynamic_field_update: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_deleted_records: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            object: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The properties that are applied when Salesforce is being used as a source.

            :param enable_dynamic_field_update: The flag that enables dynamic fetching of new (recently added) fields in the Salesforce objects while running a flow.
            :param include_deleted_records: Indicates whether Amazon AppFlow includes deleted files in the flow run.
            :param object: The object specified in the Salesforce flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-salesforcesourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                salesforce_source_properties_property = customerprofiles_mixins.CfnIntegrationPropsMixin.SalesforceSourcePropertiesProperty(
                    enable_dynamic_field_update=False,
                    include_deleted_records=False,
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9a8a6757763a15724208911044320817cd5571b25d315b8c1c0a4a7c492c0d2f)
                check_type(argname="argument enable_dynamic_field_update", value=enable_dynamic_field_update, expected_type=type_hints["enable_dynamic_field_update"])
                check_type(argname="argument include_deleted_records", value=include_deleted_records, expected_type=type_hints["include_deleted_records"])
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable_dynamic_field_update is not None:
                self._values["enable_dynamic_field_update"] = enable_dynamic_field_update
            if include_deleted_records is not None:
                self._values["include_deleted_records"] = include_deleted_records
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def enable_dynamic_field_update(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The flag that enables dynamic fetching of new (recently added) fields in the Salesforce objects while running a flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-salesforcesourceproperties.html#cfn-customerprofiles-integration-salesforcesourceproperties-enabledynamicfieldupdate
            '''
            result = self._values.get("enable_dynamic_field_update")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_deleted_records(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether Amazon AppFlow includes deleted files in the flow run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-salesforcesourceproperties.html#cfn-customerprofiles-integration-salesforcesourceproperties-includedeletedrecords
            '''
            result = self._values.get("include_deleted_records")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the Salesforce flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-salesforcesourceproperties.html#cfn-customerprofiles-integration-salesforcesourceproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnIntegrationPropsMixin.ScheduledTriggerPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_pull_mode": "dataPullMode",
            "first_execution_from": "firstExecutionFrom",
            "schedule_end_time": "scheduleEndTime",
            "schedule_expression": "scheduleExpression",
            "schedule_offset": "scheduleOffset",
            "schedule_start_time": "scheduleStartTime",
            "timezone": "timezone",
        },
    )
    class ScheduledTriggerPropertiesProperty:
        def __init__(
            self,
            *,
            data_pull_mode: typing.Optional[builtins.str] = None,
            first_execution_from: typing.Optional[jsii.Number] = None,
            schedule_end_time: typing.Optional[jsii.Number] = None,
            schedule_expression: typing.Optional[builtins.str] = None,
            schedule_offset: typing.Optional[jsii.Number] = None,
            schedule_start_time: typing.Optional[jsii.Number] = None,
            timezone: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration details of a scheduled-trigger flow that you define.

            Currently, these settings only apply to the scheduled-trigger type.

            :param data_pull_mode: Specifies whether a scheduled flow has an incremental data transfer or a complete data transfer for each flow run.
            :param first_execution_from: Specifies the date range for the records to import from the connector in the first flow run.
            :param schedule_end_time: Specifies the scheduled end time for a scheduled-trigger flow.
            :param schedule_expression: The scheduling expression that determines the rate at which the schedule will run, for example rate (5 minutes).
            :param schedule_offset: Specifies the optional offset that is added to the time interval for a schedule-triggered flow.
            :param schedule_start_time: Specifies the scheduled start time for a scheduled-trigger flow. The value must be a date/time value in EPOCH format.
            :param timezone: Specifies the time zone used when referring to the date and time of a scheduled-triggered flow, such as America/New_York.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-scheduledtriggerproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                scheduled_trigger_properties_property = customerprofiles_mixins.CfnIntegrationPropsMixin.ScheduledTriggerPropertiesProperty(
                    data_pull_mode="dataPullMode",
                    first_execution_from=123,
                    schedule_end_time=123,
                    schedule_expression="scheduleExpression",
                    schedule_offset=123,
                    schedule_start_time=123,
                    timezone="timezone"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__abed88269dff4d554864e53d5ce25267e17ea4a7a34ab55c56583a7510f2d89f)
                check_type(argname="argument data_pull_mode", value=data_pull_mode, expected_type=type_hints["data_pull_mode"])
                check_type(argname="argument first_execution_from", value=first_execution_from, expected_type=type_hints["first_execution_from"])
                check_type(argname="argument schedule_end_time", value=schedule_end_time, expected_type=type_hints["schedule_end_time"])
                check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
                check_type(argname="argument schedule_offset", value=schedule_offset, expected_type=type_hints["schedule_offset"])
                check_type(argname="argument schedule_start_time", value=schedule_start_time, expected_type=type_hints["schedule_start_time"])
                check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_pull_mode is not None:
                self._values["data_pull_mode"] = data_pull_mode
            if first_execution_from is not None:
                self._values["first_execution_from"] = first_execution_from
            if schedule_end_time is not None:
                self._values["schedule_end_time"] = schedule_end_time
            if schedule_expression is not None:
                self._values["schedule_expression"] = schedule_expression
            if schedule_offset is not None:
                self._values["schedule_offset"] = schedule_offset
            if schedule_start_time is not None:
                self._values["schedule_start_time"] = schedule_start_time
            if timezone is not None:
                self._values["timezone"] = timezone

        @builtins.property
        def data_pull_mode(self) -> typing.Optional[builtins.str]:
            '''Specifies whether a scheduled flow has an incremental data transfer or a complete data transfer for each flow run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-scheduledtriggerproperties.html#cfn-customerprofiles-integration-scheduledtriggerproperties-datapullmode
            '''
            result = self._values.get("data_pull_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def first_execution_from(self) -> typing.Optional[jsii.Number]:
            '''Specifies the date range for the records to import from the connector in the first flow run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-scheduledtriggerproperties.html#cfn-customerprofiles-integration-scheduledtriggerproperties-firstexecutionfrom
            '''
            result = self._values.get("first_execution_from")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def schedule_end_time(self) -> typing.Optional[jsii.Number]:
            '''Specifies the scheduled end time for a scheduled-trigger flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-scheduledtriggerproperties.html#cfn-customerprofiles-integration-scheduledtriggerproperties-scheduleendtime
            '''
            result = self._values.get("schedule_end_time")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def schedule_expression(self) -> typing.Optional[builtins.str]:
            '''The scheduling expression that determines the rate at which the schedule will run, for example rate (5 minutes).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-scheduledtriggerproperties.html#cfn-customerprofiles-integration-scheduledtriggerproperties-scheduleexpression
            '''
            result = self._values.get("schedule_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schedule_offset(self) -> typing.Optional[jsii.Number]:
            '''Specifies the optional offset that is added to the time interval for a schedule-triggered flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-scheduledtriggerproperties.html#cfn-customerprofiles-integration-scheduledtriggerproperties-scheduleoffset
            '''
            result = self._values.get("schedule_offset")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def schedule_start_time(self) -> typing.Optional[jsii.Number]:
            '''Specifies the scheduled start time for a scheduled-trigger flow.

            The value must be a date/time value in EPOCH format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-scheduledtriggerproperties.html#cfn-customerprofiles-integration-scheduledtriggerproperties-schedulestarttime
            '''
            result = self._values.get("schedule_start_time")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def timezone(self) -> typing.Optional[builtins.str]:
            '''Specifies the time zone used when referring to the date and time of a scheduled-triggered flow, such as America/New_York.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-scheduledtriggerproperties.html#cfn-customerprofiles-integration-scheduledtriggerproperties-timezone
            '''
            result = self._values.get("timezone")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduledTriggerPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnIntegrationPropsMixin.ServiceNowSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class ServiceNowSourcePropertiesProperty:
        def __init__(self, *, object: typing.Optional[builtins.str] = None) -> None:
            '''The properties that are applied when ServiceNow is being used as a source.

            :param object: The object specified in the ServiceNow flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-servicenowsourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                service_now_source_properties_property = customerprofiles_mixins.CfnIntegrationPropsMixin.ServiceNowSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b5678bc2f83d5f365dff36236b0547a76e736de1779da31cc57df828233455e2)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the ServiceNow flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-servicenowsourceproperties.html#cfn-customerprofiles-integration-servicenowsourceproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceNowSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnIntegrationPropsMixin.SourceConnectorPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "marketo": "marketo",
            "s3": "s3",
            "salesforce": "salesforce",
            "service_now": "serviceNow",
            "zendesk": "zendesk",
        },
    )
    class SourceConnectorPropertiesProperty:
        def __init__(
            self,
            *,
            marketo: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIntegrationPropsMixin.MarketoSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIntegrationPropsMixin.S3SourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            salesforce: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIntegrationPropsMixin.SalesforceSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            service_now: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIntegrationPropsMixin.ServiceNowSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            zendesk: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIntegrationPropsMixin.ZendeskSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the information that is required to query a particular Amazon AppFlow connector.

            Customer Profiles supports Salesforce, Zendesk, Marketo, ServiceNow and Amazon S3.

            :param marketo: The properties that are applied when Marketo is being used as a source.
            :param s3: The properties that are applied when Amazon S3 is being used as the flow source.
            :param salesforce: The properties that are applied when Salesforce is being used as a source.
            :param service_now: The properties that are applied when ServiceNow is being used as a source.
            :param zendesk: The properties that are applied when using Zendesk as a flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-sourceconnectorproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                source_connector_properties_property = customerprofiles_mixins.CfnIntegrationPropsMixin.SourceConnectorPropertiesProperty(
                    marketo=customerprofiles_mixins.CfnIntegrationPropsMixin.MarketoSourcePropertiesProperty(
                        object="object"
                    ),
                    s3=customerprofiles_mixins.CfnIntegrationPropsMixin.S3SourcePropertiesProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix"
                    ),
                    salesforce=customerprofiles_mixins.CfnIntegrationPropsMixin.SalesforceSourcePropertiesProperty(
                        enable_dynamic_field_update=False,
                        include_deleted_records=False,
                        object="object"
                    ),
                    service_now=customerprofiles_mixins.CfnIntegrationPropsMixin.ServiceNowSourcePropertiesProperty(
                        object="object"
                    ),
                    zendesk=customerprofiles_mixins.CfnIntegrationPropsMixin.ZendeskSourcePropertiesProperty(
                        object="object"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__961ca362c64e5c873b0af570bfd01c535ce51326ba10a933123f4055d1a7f829)
                check_type(argname="argument marketo", value=marketo, expected_type=type_hints["marketo"])
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
                check_type(argname="argument salesforce", value=salesforce, expected_type=type_hints["salesforce"])
                check_type(argname="argument service_now", value=service_now, expected_type=type_hints["service_now"])
                check_type(argname="argument zendesk", value=zendesk, expected_type=type_hints["zendesk"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if marketo is not None:
                self._values["marketo"] = marketo
            if s3 is not None:
                self._values["s3"] = s3
            if salesforce is not None:
                self._values["salesforce"] = salesforce
            if service_now is not None:
                self._values["service_now"] = service_now
            if zendesk is not None:
                self._values["zendesk"] = zendesk

        @builtins.property
        def marketo(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.MarketoSourcePropertiesProperty"]]:
            '''The properties that are applied when Marketo is being used as a source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-sourceconnectorproperties.html#cfn-customerprofiles-integration-sourceconnectorproperties-marketo
            '''
            result = self._values.get("marketo")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.MarketoSourcePropertiesProperty"]], result)

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.S3SourcePropertiesProperty"]]:
            '''The properties that are applied when Amazon S3 is being used as the flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-sourceconnectorproperties.html#cfn-customerprofiles-integration-sourceconnectorproperties-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.S3SourcePropertiesProperty"]], result)

        @builtins.property
        def salesforce(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.SalesforceSourcePropertiesProperty"]]:
            '''The properties that are applied when Salesforce is being used as a source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-sourceconnectorproperties.html#cfn-customerprofiles-integration-sourceconnectorproperties-salesforce
            '''
            result = self._values.get("salesforce")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.SalesforceSourcePropertiesProperty"]], result)

        @builtins.property
        def service_now(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.ServiceNowSourcePropertiesProperty"]]:
            '''The properties that are applied when ServiceNow is being used as a source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-sourceconnectorproperties.html#cfn-customerprofiles-integration-sourceconnectorproperties-servicenow
            '''
            result = self._values.get("service_now")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.ServiceNowSourcePropertiesProperty"]], result)

        @builtins.property
        def zendesk(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.ZendeskSourcePropertiesProperty"]]:
            '''The properties that are applied when using Zendesk as a flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-sourceconnectorproperties.html#cfn-customerprofiles-integration-sourceconnectorproperties-zendesk
            '''
            result = self._values.get("zendesk")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.ZendeskSourcePropertiesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceConnectorPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnIntegrationPropsMixin.SourceFlowConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connector_profile_name": "connectorProfileName",
            "connector_type": "connectorType",
            "incremental_pull_config": "incrementalPullConfig",
            "source_connector_properties": "sourceConnectorProperties",
        },
    )
    class SourceFlowConfigProperty:
        def __init__(
            self,
            *,
            connector_profile_name: typing.Optional[builtins.str] = None,
            connector_type: typing.Optional[builtins.str] = None,
            incremental_pull_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIntegrationPropsMixin.IncrementalPullConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            source_connector_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIntegrationPropsMixin.SourceConnectorPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration that controls how Customer Profiles retrieves data from the source.

            :param connector_profile_name: The name of the Amazon AppFlow connector profile. This name must be unique for each connector profile in the AWS account .
            :param connector_type: The type of connector, such as Salesforce, Marketo, and so on.
            :param incremental_pull_config: Defines the configuration for a scheduled incremental data pull. If a valid configuration is provided, the fields specified in the configuration are used when querying for the incremental data pull.
            :param source_connector_properties: Specifies the information that is required to query a particular source connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-sourceflowconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                source_flow_config_property = customerprofiles_mixins.CfnIntegrationPropsMixin.SourceFlowConfigProperty(
                    connector_profile_name="connectorProfileName",
                    connector_type="connectorType",
                    incremental_pull_config=customerprofiles_mixins.CfnIntegrationPropsMixin.IncrementalPullConfigProperty(
                        datetime_type_field_name="datetimeTypeFieldName"
                    ),
                    source_connector_properties=customerprofiles_mixins.CfnIntegrationPropsMixin.SourceConnectorPropertiesProperty(
                        marketo=customerprofiles_mixins.CfnIntegrationPropsMixin.MarketoSourcePropertiesProperty(
                            object="object"
                        ),
                        s3=customerprofiles_mixins.CfnIntegrationPropsMixin.S3SourcePropertiesProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix"
                        ),
                        salesforce=customerprofiles_mixins.CfnIntegrationPropsMixin.SalesforceSourcePropertiesProperty(
                            enable_dynamic_field_update=False,
                            include_deleted_records=False,
                            object="object"
                        ),
                        service_now=customerprofiles_mixins.CfnIntegrationPropsMixin.ServiceNowSourcePropertiesProperty(
                            object="object"
                        ),
                        zendesk=customerprofiles_mixins.CfnIntegrationPropsMixin.ZendeskSourcePropertiesProperty(
                            object="object"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6bac69a847098b72dbe7bbd718c7f40c0a0a2ef4ad3c8127eb36356ea3867cad)
                check_type(argname="argument connector_profile_name", value=connector_profile_name, expected_type=type_hints["connector_profile_name"])
                check_type(argname="argument connector_type", value=connector_type, expected_type=type_hints["connector_type"])
                check_type(argname="argument incremental_pull_config", value=incremental_pull_config, expected_type=type_hints["incremental_pull_config"])
                check_type(argname="argument source_connector_properties", value=source_connector_properties, expected_type=type_hints["source_connector_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connector_profile_name is not None:
                self._values["connector_profile_name"] = connector_profile_name
            if connector_type is not None:
                self._values["connector_type"] = connector_type
            if incremental_pull_config is not None:
                self._values["incremental_pull_config"] = incremental_pull_config
            if source_connector_properties is not None:
                self._values["source_connector_properties"] = source_connector_properties

        @builtins.property
        def connector_profile_name(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon AppFlow connector profile.

            This name must be unique for each connector profile in the AWS account .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-sourceflowconfig.html#cfn-customerprofiles-integration-sourceflowconfig-connectorprofilename
            '''
            result = self._values.get("connector_profile_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_type(self) -> typing.Optional[builtins.str]:
            '''The type of connector, such as Salesforce, Marketo, and so on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-sourceflowconfig.html#cfn-customerprofiles-integration-sourceflowconfig-connectortype
            '''
            result = self._values.get("connector_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def incremental_pull_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.IncrementalPullConfigProperty"]]:
            '''Defines the configuration for a scheduled incremental data pull.

            If a valid configuration is provided, the fields specified in the configuration are used when querying for the incremental data pull.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-sourceflowconfig.html#cfn-customerprofiles-integration-sourceflowconfig-incrementalpullconfig
            '''
            result = self._values.get("incremental_pull_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.IncrementalPullConfigProperty"]], result)

        @builtins.property
        def source_connector_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.SourceConnectorPropertiesProperty"]]:
            '''Specifies the information that is required to query a particular source connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-sourceflowconfig.html#cfn-customerprofiles-integration-sourceflowconfig-sourceconnectorproperties
            '''
            result = self._values.get("source_connector_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.SourceConnectorPropertiesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceFlowConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnIntegrationPropsMixin.TaskPropertiesMapProperty",
        jsii_struct_bases=[],
        name_mapping={
            "operator_property_key": "operatorPropertyKey",
            "property": "property",
        },
    )
    class TaskPropertiesMapProperty:
        def __init__(
            self,
            *,
            operator_property_key: typing.Optional[builtins.str] = None,
            property: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A map used to store task-related information.

            The execution service looks for particular information based on the ``TaskType`` .

            :param operator_property_key: The task property key.
            :param property: The task property value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-taskpropertiesmap.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                task_properties_map_property = customerprofiles_mixins.CfnIntegrationPropsMixin.TaskPropertiesMapProperty(
                    operator_property_key="operatorPropertyKey",
                    property="property"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__44bfd8ffbef037891005b023cae5220db8f0970b68d7a01484d0c48ac86774b0)
                check_type(argname="argument operator_property_key", value=operator_property_key, expected_type=type_hints["operator_property_key"])
                check_type(argname="argument property", value=property, expected_type=type_hints["property"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if operator_property_key is not None:
                self._values["operator_property_key"] = operator_property_key
            if property is not None:
                self._values["property"] = property

        @builtins.property
        def operator_property_key(self) -> typing.Optional[builtins.str]:
            '''The task property key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-taskpropertiesmap.html#cfn-customerprofiles-integration-taskpropertiesmap-operatorpropertykey
            '''
            result = self._values.get("operator_property_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property(self) -> typing.Optional[builtins.str]:
            '''The task property value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-taskpropertiesmap.html#cfn-customerprofiles-integration-taskpropertiesmap-property
            '''
            result = self._values.get("property")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TaskPropertiesMapProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnIntegrationPropsMixin.TaskProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connector_operator": "connectorOperator",
            "destination_field": "destinationField",
            "source_fields": "sourceFields",
            "task_properties": "taskProperties",
            "task_type": "taskType",
        },
    )
    class TaskProperty:
        def __init__(
            self,
            *,
            connector_operator: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIntegrationPropsMixin.ConnectorOperatorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            destination_field: typing.Optional[builtins.str] = None,
            source_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
            task_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIntegrationPropsMixin.TaskPropertiesMapProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            task_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``Task`` property type specifies the class for modeling different type of tasks.

            Task implementation varies based on the TaskType.

            :param connector_operator: The operation to be performed on the provided source fields.
            :param destination_field: A field in a destination connector, or a field value against which Amazon AppFlow validates a source field.
            :param source_fields: The source fields to which a particular task is applied.
            :param task_properties: A map used to store task-related information. The service looks for particular information based on the TaskType.
            :param task_type: Specifies the particular task implementation that Amazon AppFlow performs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-task.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                task_property = customerprofiles_mixins.CfnIntegrationPropsMixin.TaskProperty(
                    connector_operator=customerprofiles_mixins.CfnIntegrationPropsMixin.ConnectorOperatorProperty(
                        marketo="marketo",
                        s3="s3",
                        salesforce="salesforce",
                        service_now="serviceNow",
                        zendesk="zendesk"
                    ),
                    destination_field="destinationField",
                    source_fields=["sourceFields"],
                    task_properties=[customerprofiles_mixins.CfnIntegrationPropsMixin.TaskPropertiesMapProperty(
                        operator_property_key="operatorPropertyKey",
                        property="property"
                    )],
                    task_type="taskType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__14ab73542dfd9a8116688204f8f4a88edecc26a1bde03a20824254443710a5b5)
                check_type(argname="argument connector_operator", value=connector_operator, expected_type=type_hints["connector_operator"])
                check_type(argname="argument destination_field", value=destination_field, expected_type=type_hints["destination_field"])
                check_type(argname="argument source_fields", value=source_fields, expected_type=type_hints["source_fields"])
                check_type(argname="argument task_properties", value=task_properties, expected_type=type_hints["task_properties"])
                check_type(argname="argument task_type", value=task_type, expected_type=type_hints["task_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connector_operator is not None:
                self._values["connector_operator"] = connector_operator
            if destination_field is not None:
                self._values["destination_field"] = destination_field
            if source_fields is not None:
                self._values["source_fields"] = source_fields
            if task_properties is not None:
                self._values["task_properties"] = task_properties
            if task_type is not None:
                self._values["task_type"] = task_type

        @builtins.property
        def connector_operator(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.ConnectorOperatorProperty"]]:
            '''The operation to be performed on the provided source fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-task.html#cfn-customerprofiles-integration-task-connectoroperator
            '''
            result = self._values.get("connector_operator")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.ConnectorOperatorProperty"]], result)

        @builtins.property
        def destination_field(self) -> typing.Optional[builtins.str]:
            '''A field in a destination connector, or a field value against which Amazon AppFlow validates a source field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-task.html#cfn-customerprofiles-integration-task-destinationfield
            '''
            result = self._values.get("destination_field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_fields(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The source fields to which a particular task is applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-task.html#cfn-customerprofiles-integration-task-sourcefields
            '''
            result = self._values.get("source_fields")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def task_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.TaskPropertiesMapProperty"]]]]:
            '''A map used to store task-related information.

            The service looks for particular information based on the TaskType.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-task.html#cfn-customerprofiles-integration-task-taskproperties
            '''
            result = self._values.get("task_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.TaskPropertiesMapProperty"]]]], result)

        @builtins.property
        def task_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the particular task implementation that Amazon AppFlow performs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-task.html#cfn-customerprofiles-integration-task-tasktype
            '''
            result = self._values.get("task_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TaskProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnIntegrationPropsMixin.TriggerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "trigger_properties": "triggerProperties",
            "trigger_type": "triggerType",
        },
    )
    class TriggerConfigProperty:
        def __init__(
            self,
            *,
            trigger_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIntegrationPropsMixin.TriggerPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            trigger_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The trigger settings that determine how and when Amazon AppFlow runs the specified flow.

            :param trigger_properties: Specifies the configuration details of a schedule-triggered flow that you define. Currently, these settings only apply to the Scheduled trigger type.
            :param trigger_type: Specifies the type of flow trigger. It can be OnDemand, Scheduled, or Event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-triggerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                trigger_config_property = customerprofiles_mixins.CfnIntegrationPropsMixin.TriggerConfigProperty(
                    trigger_properties=customerprofiles_mixins.CfnIntegrationPropsMixin.TriggerPropertiesProperty(
                        scheduled=customerprofiles_mixins.CfnIntegrationPropsMixin.ScheduledTriggerPropertiesProperty(
                            data_pull_mode="dataPullMode",
                            first_execution_from=123,
                            schedule_end_time=123,
                            schedule_expression="scheduleExpression",
                            schedule_offset=123,
                            schedule_start_time=123,
                            timezone="timezone"
                        )
                    ),
                    trigger_type="triggerType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c91ec52bcdb596cf3423656e96b8130b9d2645c20afd718eeffc0bb7a8123970)
                check_type(argname="argument trigger_properties", value=trigger_properties, expected_type=type_hints["trigger_properties"])
                check_type(argname="argument trigger_type", value=trigger_type, expected_type=type_hints["trigger_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if trigger_properties is not None:
                self._values["trigger_properties"] = trigger_properties
            if trigger_type is not None:
                self._values["trigger_type"] = trigger_type

        @builtins.property
        def trigger_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.TriggerPropertiesProperty"]]:
            '''Specifies the configuration details of a schedule-triggered flow that you define.

            Currently, these settings only apply to the Scheduled trigger type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-triggerconfig.html#cfn-customerprofiles-integration-triggerconfig-triggerproperties
            '''
            result = self._values.get("trigger_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.TriggerPropertiesProperty"]], result)

        @builtins.property
        def trigger_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of flow trigger.

            It can be OnDemand, Scheduled, or Event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-triggerconfig.html#cfn-customerprofiles-integration-triggerconfig-triggertype
            '''
            result = self._values.get("trigger_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TriggerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnIntegrationPropsMixin.TriggerPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"scheduled": "scheduled"},
    )
    class TriggerPropertiesProperty:
        def __init__(
            self,
            *,
            scheduled: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIntegrationPropsMixin.ScheduledTriggerPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the configuration details that control the trigger for a flow.

            Currently, these settings only apply to the Scheduled trigger type.

            :param scheduled: Specifies the configuration details of a schedule-triggered flow that you define.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-triggerproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                trigger_properties_property = customerprofiles_mixins.CfnIntegrationPropsMixin.TriggerPropertiesProperty(
                    scheduled=customerprofiles_mixins.CfnIntegrationPropsMixin.ScheduledTriggerPropertiesProperty(
                        data_pull_mode="dataPullMode",
                        first_execution_from=123,
                        schedule_end_time=123,
                        schedule_expression="scheduleExpression",
                        schedule_offset=123,
                        schedule_start_time=123,
                        timezone="timezone"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__03f526f13bf48fccad76d805393d943949053ea3e404828cc32d86bf49b54345)
                check_type(argname="argument scheduled", value=scheduled, expected_type=type_hints["scheduled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if scheduled is not None:
                self._values["scheduled"] = scheduled

        @builtins.property
        def scheduled(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.ScheduledTriggerPropertiesProperty"]]:
            '''Specifies the configuration details of a schedule-triggered flow that you define.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-triggerproperties.html#cfn-customerprofiles-integration-triggerproperties-scheduled
            '''
            result = self._values.get("scheduled")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.ScheduledTriggerPropertiesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TriggerPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnIntegrationPropsMixin.ZendeskSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class ZendeskSourcePropertiesProperty:
        def __init__(self, *, object: typing.Optional[builtins.str] = None) -> None:
            '''The properties that are applied when using Zendesk as a flow source.

            :param object: The object specified in the Zendesk flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-zendesksourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                zendesk_source_properties_property = customerprofiles_mixins.CfnIntegrationPropsMixin.ZendeskSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__db8e236c701ef4156612d9cf0ff12efc4b984f811ab387225fc3650e34fd2c26)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the Zendesk flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-integration-zendesksourceproperties.html#cfn-customerprofiles-integration-zendesksourceproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ZendeskSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnObjectTypeMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "allow_profile_creation": "allowProfileCreation",
        "description": "description",
        "domain_name": "domainName",
        "encryption_key": "encryptionKey",
        "expiration_days": "expirationDays",
        "fields": "fields",
        "keys": "keys",
        "max_profile_object_count": "maxProfileObjectCount",
        "object_type_name": "objectTypeName",
        "source_last_updated_timestamp_format": "sourceLastUpdatedTimestampFormat",
        "tags": "tags",
        "template_id": "templateId",
    },
)
class CfnObjectTypeMixinProps:
    def __init__(
        self,
        *,
        allow_profile_creation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        expiration_days: typing.Optional[jsii.Number] = None,
        fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnObjectTypePropsMixin.FieldMapProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        keys: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnObjectTypePropsMixin.KeyMapProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        max_profile_object_count: typing.Optional[jsii.Number] = None,
        object_type_name: typing.Optional[builtins.str] = None,
        source_last_updated_timestamp_format: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        template_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnObjectTypePropsMixin.

        :param allow_profile_creation: Indicates whether a profile should be created when data is received if one doesn’t exist for an object of this type. The default is ``FALSE`` . If the AllowProfileCreation flag is set to ``FALSE`` , then the service tries to fetch a standard profile and associate this object with the profile. If it is set to ``TRUE`` , and if no match is found, then the service creates a new standard profile.
        :param description: The description of the profile object type mapping.
        :param domain_name: The unique name of the domain.
        :param encryption_key: The customer-provided key to encrypt the profile object that will be created in this profile object type mapping. If not specified the system will use the encryption key of the domain.
        :param expiration_days: The number of days until the data of this type expires.
        :param fields: A list of field definitions for the object type mapping.
        :param keys: A list of keys that can be used to map data to the profile or search for the profile.
        :param max_profile_object_count: The amount of profile object max count assigned to the object type.
        :param object_type_name: The name of the profile object type.
        :param source_last_updated_timestamp_format: The format of your sourceLastUpdatedTimestamp that was previously set up.
        :param tags: The tags used to organize, track, or control access for this resource.
        :param template_id: A unique identifier for the template mapping. This can be used instead of specifying the Keys and Fields properties directly.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-objecttype.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
            
            cfn_object_type_mixin_props = customerprofiles_mixins.CfnObjectTypeMixinProps(
                allow_profile_creation=False,
                description="description",
                domain_name="domainName",
                encryption_key="encryptionKey",
                expiration_days=123,
                fields=[customerprofiles_mixins.CfnObjectTypePropsMixin.FieldMapProperty(
                    name="name",
                    object_type_field=customerprofiles_mixins.CfnObjectTypePropsMixin.ObjectTypeFieldProperty(
                        content_type="contentType",
                        source="source",
                        target="target"
                    )
                )],
                keys=[customerprofiles_mixins.CfnObjectTypePropsMixin.KeyMapProperty(
                    name="name",
                    object_type_key_list=[customerprofiles_mixins.CfnObjectTypePropsMixin.ObjectTypeKeyProperty(
                        field_names=["fieldNames"],
                        standard_identifiers=["standardIdentifiers"]
                    )]
                )],
                max_profile_object_count=123,
                object_type_name="objectTypeName",
                source_last_updated_timestamp_format="sourceLastUpdatedTimestampFormat",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                template_id="templateId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77765cdf237179e7418145f933935b4f5bc5e312389dadbb09f4e4fd6170b0b0)
            check_type(argname="argument allow_profile_creation", value=allow_profile_creation, expected_type=type_hints["allow_profile_creation"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument expiration_days", value=expiration_days, expected_type=type_hints["expiration_days"])
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
            check_type(argname="argument keys", value=keys, expected_type=type_hints["keys"])
            check_type(argname="argument max_profile_object_count", value=max_profile_object_count, expected_type=type_hints["max_profile_object_count"])
            check_type(argname="argument object_type_name", value=object_type_name, expected_type=type_hints["object_type_name"])
            check_type(argname="argument source_last_updated_timestamp_format", value=source_last_updated_timestamp_format, expected_type=type_hints["source_last_updated_timestamp_format"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_id", value=template_id, expected_type=type_hints["template_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_profile_creation is not None:
            self._values["allow_profile_creation"] = allow_profile_creation
        if description is not None:
            self._values["description"] = description
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if expiration_days is not None:
            self._values["expiration_days"] = expiration_days
        if fields is not None:
            self._values["fields"] = fields
        if keys is not None:
            self._values["keys"] = keys
        if max_profile_object_count is not None:
            self._values["max_profile_object_count"] = max_profile_object_count
        if object_type_name is not None:
            self._values["object_type_name"] = object_type_name
        if source_last_updated_timestamp_format is not None:
            self._values["source_last_updated_timestamp_format"] = source_last_updated_timestamp_format
        if tags is not None:
            self._values["tags"] = tags
        if template_id is not None:
            self._values["template_id"] = template_id

    @builtins.property
    def allow_profile_creation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether a profile should be created when data is received if one doesn’t exist for an object of this type.

        The default is ``FALSE`` . If the AllowProfileCreation flag is set to ``FALSE`` , then the service tries to fetch a standard profile and associate this object with the profile. If it is set to ``TRUE`` , and if no match is found, then the service creates a new standard profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-objecttype.html#cfn-customerprofiles-objecttype-allowprofilecreation
        '''
        result = self._values.get("allow_profile_creation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the profile object type mapping.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-objecttype.html#cfn-customerprofiles-objecttype-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The unique name of the domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-objecttype.html#cfn-customerprofiles-objecttype-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[builtins.str]:
        '''The customer-provided key to encrypt the profile object that will be created in this profile object type mapping.

        If not specified the system will use the encryption key of the domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-objecttype.html#cfn-customerprofiles-objecttype-encryptionkey
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expiration_days(self) -> typing.Optional[jsii.Number]:
        '''The number of days until the data of this type expires.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-objecttype.html#cfn-customerprofiles-objecttype-expirationdays
        '''
        result = self._values.get("expiration_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fields(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnObjectTypePropsMixin.FieldMapProperty"]]]]:
        '''A list of field definitions for the object type mapping.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-objecttype.html#cfn-customerprofiles-objecttype-fields
        '''
        result = self._values.get("fields")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnObjectTypePropsMixin.FieldMapProperty"]]]], result)

    @builtins.property
    def keys(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnObjectTypePropsMixin.KeyMapProperty"]]]]:
        '''A list of keys that can be used to map data to the profile or search for the profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-objecttype.html#cfn-customerprofiles-objecttype-keys
        '''
        result = self._values.get("keys")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnObjectTypePropsMixin.KeyMapProperty"]]]], result)

    @builtins.property
    def max_profile_object_count(self) -> typing.Optional[jsii.Number]:
        '''The amount of profile object max count assigned to the object type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-objecttype.html#cfn-customerprofiles-objecttype-maxprofileobjectcount
        '''
        result = self._values.get("max_profile_object_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def object_type_name(self) -> typing.Optional[builtins.str]:
        '''The name of the profile object type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-objecttype.html#cfn-customerprofiles-objecttype-objecttypename
        '''
        result = self._values.get("object_type_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_last_updated_timestamp_format(self) -> typing.Optional[builtins.str]:
        '''The format of your sourceLastUpdatedTimestamp that was previously set up.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-objecttype.html#cfn-customerprofiles-objecttype-sourcelastupdatedtimestampformat
        '''
        result = self._values.get("source_last_updated_timestamp_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-objecttype.html#cfn-customerprofiles-objecttype-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def template_id(self) -> typing.Optional[builtins.str]:
        '''A unique identifier for the template mapping.

        This can be used instead of specifying the Keys and Fields properties directly.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-objecttype.html#cfn-customerprofiles-objecttype-templateid
        '''
        result = self._values.get("template_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnObjectTypeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnObjectTypePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnObjectTypePropsMixin",
):
    '''Specifies an Amazon Connect Customer Profiles Object Type Mapping.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-objecttype.html
    :cloudformationResource: AWS::CustomerProfiles::ObjectType
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
        
        cfn_object_type_props_mixin = customerprofiles_mixins.CfnObjectTypePropsMixin(customerprofiles_mixins.CfnObjectTypeMixinProps(
            allow_profile_creation=False,
            description="description",
            domain_name="domainName",
            encryption_key="encryptionKey",
            expiration_days=123,
            fields=[customerprofiles_mixins.CfnObjectTypePropsMixin.FieldMapProperty(
                name="name",
                object_type_field=customerprofiles_mixins.CfnObjectTypePropsMixin.ObjectTypeFieldProperty(
                    content_type="contentType",
                    source="source",
                    target="target"
                )
            )],
            keys=[customerprofiles_mixins.CfnObjectTypePropsMixin.KeyMapProperty(
                name="name",
                object_type_key_list=[customerprofiles_mixins.CfnObjectTypePropsMixin.ObjectTypeKeyProperty(
                    field_names=["fieldNames"],
                    standard_identifiers=["standardIdentifiers"]
                )]
            )],
            max_profile_object_count=123,
            object_type_name="objectTypeName",
            source_last_updated_timestamp_format="sourceLastUpdatedTimestampFormat",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            template_id="templateId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnObjectTypeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CustomerProfiles::ObjectType``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66bd2de7b076f7567a5dd83628f2181e57c7b59fffe8cf2aa4e0c3a02be2fe10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2492da61bfe358b2d63d046120f16ee300b151a4bf1086bc79b566d18206a3e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7bf2fdc9860f25afbba02e3c8d1c444ba3d0a0b71c7ac83f393bdf25c4095d7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnObjectTypeMixinProps:
        return typing.cast(CfnObjectTypeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnObjectTypePropsMixin.FieldMapProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "object_type_field": "objectTypeField"},
    )
    class FieldMapProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            object_type_field: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnObjectTypePropsMixin.ObjectTypeFieldProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A map of the name and ObjectType field.

            :param name: Name of the field.
            :param object_type_field: Represents a field in a ProfileObjectType.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-objecttype-fieldmap.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                field_map_property = customerprofiles_mixins.CfnObjectTypePropsMixin.FieldMapProperty(
                    name="name",
                    object_type_field=customerprofiles_mixins.CfnObjectTypePropsMixin.ObjectTypeFieldProperty(
                        content_type="contentType",
                        source="source",
                        target="target"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9a46f3406482fb31a3f2aed4f272fbc66ff7723896e0976132932eed73a30780)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument object_type_field", value=object_type_field, expected_type=type_hints["object_type_field"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if object_type_field is not None:
                self._values["object_type_field"] = object_type_field

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''Name of the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-objecttype-fieldmap.html#cfn-customerprofiles-objecttype-fieldmap-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_type_field(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnObjectTypePropsMixin.ObjectTypeFieldProperty"]]:
            '''Represents a field in a ProfileObjectType.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-objecttype-fieldmap.html#cfn-customerprofiles-objecttype-fieldmap-objecttypefield
            '''
            result = self._values.get("object_type_field")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnObjectTypePropsMixin.ObjectTypeFieldProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldMapProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnObjectTypePropsMixin.KeyMapProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "object_type_key_list": "objectTypeKeyList"},
    )
    class KeyMapProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            object_type_key_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnObjectTypePropsMixin.ObjectTypeKeyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A unique key map that can be used to map data to the profile.

            :param name: Name of the key.
            :param object_type_key_list: A list of ObjectTypeKey.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-objecttype-keymap.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                key_map_property = customerprofiles_mixins.CfnObjectTypePropsMixin.KeyMapProperty(
                    name="name",
                    object_type_key_list=[customerprofiles_mixins.CfnObjectTypePropsMixin.ObjectTypeKeyProperty(
                        field_names=["fieldNames"],
                        standard_identifiers=["standardIdentifiers"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2b3f898f102b0e8ee3dfcf77c841c3a52bfff6b29d6a00c2dc8437c7afd10455)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument object_type_key_list", value=object_type_key_list, expected_type=type_hints["object_type_key_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if object_type_key_list is not None:
                self._values["object_type_key_list"] = object_type_key_list

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''Name of the key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-objecttype-keymap.html#cfn-customerprofiles-objecttype-keymap-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_type_key_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnObjectTypePropsMixin.ObjectTypeKeyProperty"]]]]:
            '''A list of ObjectTypeKey.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-objecttype-keymap.html#cfn-customerprofiles-objecttype-keymap-objecttypekeylist
            '''
            result = self._values.get("object_type_key_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnObjectTypePropsMixin.ObjectTypeKeyProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeyMapProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnObjectTypePropsMixin.ObjectTypeFieldProperty",
        jsii_struct_bases=[],
        name_mapping={
            "content_type": "contentType",
            "source": "source",
            "target": "target",
        },
    )
    class ObjectTypeFieldProperty:
        def __init__(
            self,
            *,
            content_type: typing.Optional[builtins.str] = None,
            source: typing.Optional[builtins.str] = None,
            target: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents a field in a ProfileObjectType.

            :param content_type: The content type of the field. Used for determining equality when searching.
            :param source: A field of a ProfileObject. For example: _source.FirstName, where “_source” is a ProfileObjectType of a Zendesk user and “FirstName” is a field in that ObjectType.
            :param target: The location of the data in the standard ProfileObject model. For example: _profile.Address.PostalCode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-objecttype-objecttypefield.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                object_type_field_property = customerprofiles_mixins.CfnObjectTypePropsMixin.ObjectTypeFieldProperty(
                    content_type="contentType",
                    source="source",
                    target="target"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__427722cf4bccdf5231eb05ed80283e5c3f89a64a71a483f60d878b0f312aa3df)
                check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if content_type is not None:
                self._values["content_type"] = content_type
            if source is not None:
                self._values["source"] = source
            if target is not None:
                self._values["target"] = target

        @builtins.property
        def content_type(self) -> typing.Optional[builtins.str]:
            '''The content type of the field.

            Used for determining equality when searching.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-objecttype-objecttypefield.html#cfn-customerprofiles-objecttype-objecttypefield-contenttype
            '''
            result = self._values.get("content_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''A field of a ProfileObject.

            For example: _source.FirstName, where “_source” is a ProfileObjectType of a Zendesk user and “FirstName” is a field in that ObjectType.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-objecttype-objecttypefield.html#cfn-customerprofiles-objecttype-objecttypefield-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target(self) -> typing.Optional[builtins.str]:
            '''The location of the data in the standard ProfileObject model.

            For example: _profile.Address.PostalCode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-objecttype-objecttypefield.html#cfn-customerprofiles-objecttype-objecttypefield-target
            '''
            result = self._values.get("target")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ObjectTypeFieldProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnObjectTypePropsMixin.ObjectTypeKeyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "field_names": "fieldNames",
            "standard_identifiers": "standardIdentifiers",
        },
    )
    class ObjectTypeKeyProperty:
        def __init__(
            self,
            *,
            field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            standard_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''An object that defines the Key element of a ProfileObject.

            A Key is a special element that can be used to search for a customer profile.

            :param field_names: The reference for the key name of the fields map.
            :param standard_identifiers: The types of keys that a ProfileObject can have. Each ProfileObject can have only 1 UNIQUE key but multiple PROFILE keys. PROFILE means that this key can be used to tie an object to a PROFILE. UNIQUE means that it can be used to uniquely identify an object. If a key a is marked as SECONDARY, it will be used to search for profiles after all other PROFILE keys have been searched. A LOOKUP_ONLY key is only used to match a profile but is not persisted to be used for searching of the profile. A NEW_ONLY key is only used if the profile does not already exist before the object is ingested, otherwise it is only used for matching objects to profiles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-objecttype-objecttypekey.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                object_type_key_property = customerprofiles_mixins.CfnObjectTypePropsMixin.ObjectTypeKeyProperty(
                    field_names=["fieldNames"],
                    standard_identifiers=["standardIdentifiers"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cd0133edb4f69b6d8c33eaf135711274d5a6045521457c747a3db1e99e19af80)
                check_type(argname="argument field_names", value=field_names, expected_type=type_hints["field_names"])
                check_type(argname="argument standard_identifiers", value=standard_identifiers, expected_type=type_hints["standard_identifiers"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if field_names is not None:
                self._values["field_names"] = field_names
            if standard_identifiers is not None:
                self._values["standard_identifiers"] = standard_identifiers

        @builtins.property
        def field_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The reference for the key name of the fields map.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-objecttype-objecttypekey.html#cfn-customerprofiles-objecttype-objecttypekey-fieldnames
            '''
            result = self._values.get("field_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def standard_identifiers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The types of keys that a ProfileObject can have.

            Each ProfileObject can have only 1 UNIQUE key but multiple PROFILE keys. PROFILE means that this key can be used to tie an object to a PROFILE. UNIQUE means that it can be used to uniquely identify an object. If a key a is marked as SECONDARY, it will be used to search for profiles after all other PROFILE keys have been searched. A LOOKUP_ONLY key is only used to match a profile but is not persisted to be used for searching of the profile. A NEW_ONLY key is only used if the profile does not already exist before the object is ingested, otherwise it is only used for matching objects to profiles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-objecttype-objecttypekey.html#cfn-customerprofiles-objecttype-objecttypekey-standardidentifiers
            '''
            result = self._values.get("standard_identifiers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ObjectTypeKeyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnSegmentDefinitionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "display_name": "displayName",
        "domain_name": "domainName",
        "segment_definition_name": "segmentDefinitionName",
        "segment_groups": "segmentGroups",
        "segment_sql_query": "segmentSqlQuery",
        "tags": "tags",
    },
)
class CfnSegmentDefinitionMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        segment_definition_name: typing.Optional[builtins.str] = None,
        segment_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.SegmentGroupProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        segment_sql_query: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnSegmentDefinitionPropsMixin.

        :param description: The description of the segment definition.
        :param display_name: Display name of the segment definition.
        :param domain_name: The name of the domain.
        :param segment_definition_name: Name of the segment definition.
        :param segment_groups: Contains all groups of the segment definition.
        :param segment_sql_query: The SQL query that defines the segment criteria.
        :param tags: The tags belonging to the segment definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-segmentdefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
            
            cfn_segment_definition_mixin_props = customerprofiles_mixins.CfnSegmentDefinitionMixinProps(
                description="description",
                display_name="displayName",
                domain_name="domainName",
                segment_definition_name="segmentDefinitionName",
                segment_groups=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.SegmentGroupProperty(
                    groups=[customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.GroupProperty(
                        dimensions=[customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.DimensionProperty(
                            calculated_attributes={
                                "calculated_attributes_key": customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.CalculatedAttributeDimensionProperty(
                                    condition_overrides=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ConditionOverridesProperty(
                                        range=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.RangeOverrideProperty(
                                            end=123,
                                            start=123,
                                            unit="unit"
                                        )
                                    ),
                                    dimension_type="dimensionType",
                                    values=["values"]
                                )
                            },
                            profile_attributes=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileAttributesProperty(
                                account_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                additional_information=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ExtraLengthValueProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                                    city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    )
                                ),
                                attributes={
                                    "attributes_key": customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AttributeDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    )
                                },
                                billing_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                                    city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    )
                                ),
                                birth_date=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.DateDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                business_email_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                business_name=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                business_phone_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                email_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                first_name=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                gender_string=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                home_phone_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                last_name=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                mailing_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                                    city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    )
                                ),
                                middle_name=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                mobile_phone_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                party_type_string=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                personal_email_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                phone_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                profile_type=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileTypeDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                shipping_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                                    city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    )
                                )
                            )
                        )],
                        source_segments=[customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.SourceSegmentProperty(
                            segment_definition_name="segmentDefinitionName"
                        )],
                        source_type="sourceType",
                        type="type"
                    )],
                    include="include"
                ),
                segment_sql_query="segmentSqlQuery",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f0d23a33dd3e6f2f44c6c2eef350e130d31c812ecb7a831f59e1b81530693ec)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument segment_definition_name", value=segment_definition_name, expected_type=type_hints["segment_definition_name"])
            check_type(argname="argument segment_groups", value=segment_groups, expected_type=type_hints["segment_groups"])
            check_type(argname="argument segment_sql_query", value=segment_sql_query, expected_type=type_hints["segment_sql_query"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if segment_definition_name is not None:
            self._values["segment_definition_name"] = segment_definition_name
        if segment_groups is not None:
            self._values["segment_groups"] = segment_groups
        if segment_sql_query is not None:
            self._values["segment_sql_query"] = segment_sql_query
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the segment definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-segmentdefinition.html#cfn-customerprofiles-segmentdefinition-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Display name of the segment definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-segmentdefinition.html#cfn-customerprofiles-segmentdefinition-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The name of the domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-segmentdefinition.html#cfn-customerprofiles-segmentdefinition-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def segment_definition_name(self) -> typing.Optional[builtins.str]:
        '''Name of the segment definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-segmentdefinition.html#cfn-customerprofiles-segmentdefinition-segmentdefinitionname
        '''
        result = self._values.get("segment_definition_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def segment_groups(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.SegmentGroupProperty"]]:
        '''Contains all groups of the segment definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-segmentdefinition.html#cfn-customerprofiles-segmentdefinition-segmentgroups
        '''
        result = self._values.get("segment_groups")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.SegmentGroupProperty"]], result)

    @builtins.property
    def segment_sql_query(self) -> typing.Optional[builtins.str]:
        '''The SQL query that defines the segment criteria.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-segmentdefinition.html#cfn-customerprofiles-segmentdefinition-segmentsqlquery
        '''
        result = self._values.get("segment_sql_query")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags belonging to the segment definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-segmentdefinition.html#cfn-customerprofiles-segmentdefinition-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSegmentDefinitionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSegmentDefinitionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnSegmentDefinitionPropsMixin",
):
    '''A segment definition resource of Amazon Connect Customer Profiles.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-customerprofiles-segmentdefinition.html
    :cloudformationResource: AWS::CustomerProfiles::SegmentDefinition
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
        
        cfn_segment_definition_props_mixin = customerprofiles_mixins.CfnSegmentDefinitionPropsMixin(customerprofiles_mixins.CfnSegmentDefinitionMixinProps(
            description="description",
            display_name="displayName",
            domain_name="domainName",
            segment_definition_name="segmentDefinitionName",
            segment_groups=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.SegmentGroupProperty(
                groups=[customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.GroupProperty(
                    dimensions=[customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.DimensionProperty(
                        calculated_attributes={
                            "calculated_attributes_key": customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.CalculatedAttributeDimensionProperty(
                                condition_overrides=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ConditionOverridesProperty(
                                    range=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.RangeOverrideProperty(
                                        end=123,
                                        start=123,
                                        unit="unit"
                                    )
                                ),
                                dimension_type="dimensionType",
                                values=["values"]
                            )
                        },
                        profile_attributes=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileAttributesProperty(
                            account_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            additional_information=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ExtraLengthValueProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                                city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                )
                            ),
                            attributes={
                                "attributes_key": customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AttributeDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                )
                            },
                            billing_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                                city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                )
                            ),
                            birth_date=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.DateDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            business_email_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            business_name=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            business_phone_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            email_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            first_name=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            gender_string=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            home_phone_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            last_name=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            mailing_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                                city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                )
                            ),
                            middle_name=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            mobile_phone_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            party_type_string=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            personal_email_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            phone_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            profile_type=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileTypeDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            shipping_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                                city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                )
                            )
                        )
                    )],
                    source_segments=[customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.SourceSegmentProperty(
                        segment_definition_name="segmentDefinitionName"
                    )],
                    source_type="sourceType",
                    type="type"
                )],
                include="include"
            ),
            segment_sql_query="segmentSqlQuery",
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
        props: typing.Union[CfnSegmentDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CustomerProfiles::SegmentDefinition``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00500b5560a614be2bb333f85c9b18246808421c85c21214ca2284fb36f73f56)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba0938a90e3064d58e1156d750eca2f7eb21e469397f287fd3f84640acad69f8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff586cdfffd66d3196e5d1ede83f1b33062a59924eadd5f641dfff57443b7b54)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSegmentDefinitionMixinProps:
        return typing.cast(CfnSegmentDefinitionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "city": "city",
            "country": "country",
            "county": "county",
            "postal_code": "postalCode",
            "province": "province",
            "state": "state",
        },
    )
    class AddressDimensionProperty:
        def __init__(
            self,
            *,
            city: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            country: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            county: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            postal_code: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            province: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            state: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Object that segments on Customer Profile's address object.

            :param city: The city belonging to the address.
            :param country: The country belonging to the address.
            :param county: The county belonging to the address.
            :param postal_code: The postal code belonging to the address.
            :param province: The province belonging to the address.
            :param state: The state belonging to the address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-addressdimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                address_dimension_property = customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                    city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d558178ff48b875ddaa027d3ff20d101224c88976637179a39a510f7f270f3c)
                check_type(argname="argument city", value=city, expected_type=type_hints["city"])
                check_type(argname="argument country", value=country, expected_type=type_hints["country"])
                check_type(argname="argument county", value=county, expected_type=type_hints["county"])
                check_type(argname="argument postal_code", value=postal_code, expected_type=type_hints["postal_code"])
                check_type(argname="argument province", value=province, expected_type=type_hints["province"])
                check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if city is not None:
                self._values["city"] = city
            if country is not None:
                self._values["country"] = country
            if county is not None:
                self._values["county"] = county
            if postal_code is not None:
                self._values["postal_code"] = postal_code
            if province is not None:
                self._values["province"] = province
            if state is not None:
                self._values["state"] = state

        @builtins.property
        def city(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]]:
            '''The city belonging to the address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-addressdimension.html#cfn-customerprofiles-segmentdefinition-addressdimension-city
            '''
            result = self._values.get("city")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]], result)

        @builtins.property
        def country(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]]:
            '''The country belonging to the address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-addressdimension.html#cfn-customerprofiles-segmentdefinition-addressdimension-country
            '''
            result = self._values.get("country")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]], result)

        @builtins.property
        def county(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]]:
            '''The county belonging to the address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-addressdimension.html#cfn-customerprofiles-segmentdefinition-addressdimension-county
            '''
            result = self._values.get("county")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]], result)

        @builtins.property
        def postal_code(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]]:
            '''The postal code belonging to the address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-addressdimension.html#cfn-customerprofiles-segmentdefinition-addressdimension-postalcode
            '''
            result = self._values.get("postal_code")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]], result)

        @builtins.property
        def province(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]]:
            '''The province belonging to the address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-addressdimension.html#cfn-customerprofiles-segmentdefinition-addressdimension-province
            '''
            result = self._values.get("province")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]], result)

        @builtins.property
        def state(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]]:
            '''The state belonging to the address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-addressdimension.html#cfn-customerprofiles-segmentdefinition-addressdimension-state
            '''
            result = self._values.get("state")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AddressDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnSegmentDefinitionPropsMixin.AttributeDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"dimension_type": "dimensionType", "values": "values"},
    )
    class AttributeDimensionProperty:
        def __init__(
            self,
            *,
            dimension_type: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Object that defines how to filter the incoming objects for the calculated attribute.

            :param dimension_type: The action to segment with.
            :param values: The values to apply the DimensionType on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-attributedimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                attribute_dimension_property = customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AttributeDimensionProperty(
                    dimension_type="dimensionType",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7213b4f320a8f516919ec9a0da67cd7710340925506721ab3a6f9614870909e8)
                check_type(argname="argument dimension_type", value=dimension_type, expected_type=type_hints["dimension_type"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimension_type is not None:
                self._values["dimension_type"] = dimension_type
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def dimension_type(self) -> typing.Optional[builtins.str]:
            '''The action to segment with.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-attributedimension.html#cfn-customerprofiles-segmentdefinition-attributedimension-dimensiontype
            '''
            result = self._values.get("dimension_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The values to apply the DimensionType on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-attributedimension.html#cfn-customerprofiles-segmentdefinition-attributedimension-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnSegmentDefinitionPropsMixin.CalculatedAttributeDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "condition_overrides": "conditionOverrides",
            "dimension_type": "dimensionType",
            "values": "values",
        },
    )
    class CalculatedAttributeDimensionProperty:
        def __init__(
            self,
            *,
            condition_overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.ConditionOverridesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dimension_type: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Object that segments on Customer Profile's Calculated Attributes.

            :param condition_overrides: Applies the given condition over the initial Calculated Attribute's definition.
            :param dimension_type: The action to segment with.
            :param values: The values to apply the DimensionType with.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-calculatedattributedimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                calculated_attribute_dimension_property = customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.CalculatedAttributeDimensionProperty(
                    condition_overrides=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ConditionOverridesProperty(
                        range=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.RangeOverrideProperty(
                            end=123,
                            start=123,
                            unit="unit"
                        )
                    ),
                    dimension_type="dimensionType",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5f42037e0602e9d443b7ecd37ad3ea4dfd6fa322337f1125338e9bc871f1dc37)
                check_type(argname="argument condition_overrides", value=condition_overrides, expected_type=type_hints["condition_overrides"])
                check_type(argname="argument dimension_type", value=dimension_type, expected_type=type_hints["dimension_type"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if condition_overrides is not None:
                self._values["condition_overrides"] = condition_overrides
            if dimension_type is not None:
                self._values["dimension_type"] = dimension_type
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def condition_overrides(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ConditionOverridesProperty"]]:
            '''Applies the given condition over the initial Calculated Attribute's definition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-calculatedattributedimension.html#cfn-customerprofiles-segmentdefinition-calculatedattributedimension-conditionoverrides
            '''
            result = self._values.get("condition_overrides")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ConditionOverridesProperty"]], result)

        @builtins.property
        def dimension_type(self) -> typing.Optional[builtins.str]:
            '''The action to segment with.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-calculatedattributedimension.html#cfn-customerprofiles-segmentdefinition-calculatedattributedimension-dimensiontype
            '''
            result = self._values.get("dimension_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The values to apply the DimensionType with.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-calculatedattributedimension.html#cfn-customerprofiles-segmentdefinition-calculatedattributedimension-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CalculatedAttributeDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnSegmentDefinitionPropsMixin.ConditionOverridesProperty",
        jsii_struct_bases=[],
        name_mapping={"range": "range"},
    )
    class ConditionOverridesProperty:
        def __init__(
            self,
            *,
            range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.RangeOverrideProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object to override the original condition block of a calculated attribute.

            :param range: The relative time period over which data is included in the aggregation for this override.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-conditionoverrides.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                condition_overrides_property = customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ConditionOverridesProperty(
                    range=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.RangeOverrideProperty(
                        end=123,
                        start=123,
                        unit="unit"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__41454fa1226f1a0faa067f437d0aac1832a7f52781c08b5cca8c8aa89a5f80d0)
                check_type(argname="argument range", value=range, expected_type=type_hints["range"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if range is not None:
                self._values["range"] = range

        @builtins.property
        def range(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.RangeOverrideProperty"]]:
            '''The relative time period over which data is included in the aggregation for this override.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-conditionoverrides.html#cfn-customerprofiles-segmentdefinition-conditionoverrides-range
            '''
            result = self._values.get("range")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.RangeOverrideProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConditionOverridesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnSegmentDefinitionPropsMixin.DateDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"dimension_type": "dimensionType", "values": "values"},
    )
    class DateDimensionProperty:
        def __init__(
            self,
            *,
            dimension_type: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Object that segments on various Customer Profile's date fields.

            :param dimension_type: The action to segment on.
            :param values: The values to apply the DimensionType on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-datedimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                date_dimension_property = customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.DateDimensionProperty(
                    dimension_type="dimensionType",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b255036d861283aaf04ff796582c4cdb40671b5c070c069825348913fb8dd56a)
                check_type(argname="argument dimension_type", value=dimension_type, expected_type=type_hints["dimension_type"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimension_type is not None:
                self._values["dimension_type"] = dimension_type
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def dimension_type(self) -> typing.Optional[builtins.str]:
            '''The action to segment on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-datedimension.html#cfn-customerprofiles-segmentdefinition-datedimension-dimensiontype
            '''
            result = self._values.get("dimension_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The values to apply the DimensionType on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-datedimension.html#cfn-customerprofiles-segmentdefinition-datedimension-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DateDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnSegmentDefinitionPropsMixin.DimensionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "calculated_attributes": "calculatedAttributes",
            "profile_attributes": "profileAttributes",
        },
    )
    class DimensionProperty:
        def __init__(
            self,
            *,
            calculated_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.CalculatedAttributeDimensionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            profile_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.ProfileAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Defines the attribute to segment on.

            :param calculated_attributes: Object that holds the calculated attributes to segment on.
            :param profile_attributes: Object that holds the profile attributes to segment on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-dimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                dimension_property = customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.DimensionProperty(
                    calculated_attributes={
                        "calculated_attributes_key": customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.CalculatedAttributeDimensionProperty(
                            condition_overrides=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ConditionOverridesProperty(
                                range=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.RangeOverrideProperty(
                                    end=123,
                                    start=123,
                                    unit="unit"
                                )
                            ),
                            dimension_type="dimensionType",
                            values=["values"]
                        )
                    },
                    profile_attributes=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileAttributesProperty(
                        account_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        additional_information=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ExtraLengthValueProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                            city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            )
                        ),
                        attributes={
                            "attributes_key": customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AttributeDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            )
                        },
                        billing_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                            city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            )
                        ),
                        birth_date=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.DateDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        business_email_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        business_name=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        business_phone_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        email_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        first_name=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        gender_string=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        home_phone_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        last_name=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        mailing_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                            city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            )
                        ),
                        middle_name=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        mobile_phone_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        party_type_string=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        personal_email_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        phone_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        profile_type=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileTypeDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        shipping_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                            city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f045e8c7371e85b640098bf6c5e52c892cd3452c4e41f9e5285cd2eacfbda9d4)
                check_type(argname="argument calculated_attributes", value=calculated_attributes, expected_type=type_hints["calculated_attributes"])
                check_type(argname="argument profile_attributes", value=profile_attributes, expected_type=type_hints["profile_attributes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if calculated_attributes is not None:
                self._values["calculated_attributes"] = calculated_attributes
            if profile_attributes is not None:
                self._values["profile_attributes"] = profile_attributes

        @builtins.property
        def calculated_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.CalculatedAttributeDimensionProperty"]]]]:
            '''Object that holds the calculated attributes to segment on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-dimension.html#cfn-customerprofiles-segmentdefinition-dimension-calculatedattributes
            '''
            result = self._values.get("calculated_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.CalculatedAttributeDimensionProperty"]]]], result)

        @builtins.property
        def profile_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileAttributesProperty"]]:
            '''Object that holds the profile attributes to segment on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-dimension.html#cfn-customerprofiles-segmentdefinition-dimension-profileattributes
            '''
            result = self._values.get("profile_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileAttributesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnSegmentDefinitionPropsMixin.ExtraLengthValueProfileDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"dimension_type": "dimensionType", "values": "values"},
    )
    class ExtraLengthValueProfileDimensionProperty:
        def __init__(
            self,
            *,
            dimension_type: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Object that segments on various Customer profile's fields that are larger than normal.

            :param dimension_type: The action to segment with.
            :param values: The values to apply the DimensionType on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-extralengthvalueprofiledimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                extra_length_value_profile_dimension_property = customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ExtraLengthValueProfileDimensionProperty(
                    dimension_type="dimensionType",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bd47e75d0901a808c66015f575fec85ba6cd05860b42a0cd72ae89a6cfc9fa96)
                check_type(argname="argument dimension_type", value=dimension_type, expected_type=type_hints["dimension_type"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimension_type is not None:
                self._values["dimension_type"] = dimension_type
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def dimension_type(self) -> typing.Optional[builtins.str]:
            '''The action to segment with.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-extralengthvalueprofiledimension.html#cfn-customerprofiles-segmentdefinition-extralengthvalueprofiledimension-dimensiontype
            '''
            result = self._values.get("dimension_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The values to apply the DimensionType on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-extralengthvalueprofiledimension.html#cfn-customerprofiles-segmentdefinition-extralengthvalueprofiledimension-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExtraLengthValueProfileDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnSegmentDefinitionPropsMixin.GroupProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dimensions": "dimensions",
            "source_segments": "sourceSegments",
            "source_type": "sourceType",
            "type": "type",
        },
    )
    class GroupProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.DimensionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            source_segments: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.SourceSegmentProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            source_type: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains dimensions that determine what to segment on.

            :param dimensions: Defines the attributes to segment on.
            :param source_segments: Defines the starting source of data.
            :param source_type: Defines how to interact with the source data.
            :param type: Defines how to interact with the profiles found in the current filtering.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-group.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                group_property = customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.GroupProperty(
                    dimensions=[customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.DimensionProperty(
                        calculated_attributes={
                            "calculated_attributes_key": customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.CalculatedAttributeDimensionProperty(
                                condition_overrides=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ConditionOverridesProperty(
                                    range=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.RangeOverrideProperty(
                                        end=123,
                                        start=123,
                                        unit="unit"
                                    )
                                ),
                                dimension_type="dimensionType",
                                values=["values"]
                            )
                        },
                        profile_attributes=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileAttributesProperty(
                            account_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            additional_information=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ExtraLengthValueProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                                city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                )
                            ),
                            attributes={
                                "attributes_key": customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AttributeDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                )
                            },
                            billing_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                                city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                )
                            ),
                            birth_date=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.DateDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            business_email_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            business_name=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            business_phone_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            email_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            first_name=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            gender_string=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            home_phone_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            last_name=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            mailing_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                                city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                )
                            ),
                            middle_name=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            mobile_phone_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            party_type_string=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            personal_email_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            phone_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            profile_type=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileTypeDimensionProperty(
                                dimension_type="dimensionType",
                                values=["values"]
                            ),
                            shipping_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                                city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                )
                            )
                        )
                    )],
                    source_segments=[customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.SourceSegmentProperty(
                        segment_definition_name="segmentDefinitionName"
                    )],
                    source_type="sourceType",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c304abc4b76df3fbfe7a152032a13a8297cfe39e91b847342f79d8a3aad081fd)
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                check_type(argname="argument source_segments", value=source_segments, expected_type=type_hints["source_segments"])
                check_type(argname="argument source_type", value=source_type, expected_type=type_hints["source_type"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if source_segments is not None:
                self._values["source_segments"] = source_segments
            if source_type is not None:
                self._values["source_type"] = source_type
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.DimensionProperty"]]]]:
            '''Defines the attributes to segment on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-group.html#cfn-customerprofiles-segmentdefinition-group-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.DimensionProperty"]]]], result)

        @builtins.property
        def source_segments(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.SourceSegmentProperty"]]]]:
            '''Defines the starting source of data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-group.html#cfn-customerprofiles-segmentdefinition-group-sourcesegments
            '''
            result = self._values.get("source_segments")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.SourceSegmentProperty"]]]], result)

        @builtins.property
        def source_type(self) -> typing.Optional[builtins.str]:
            '''Defines how to interact with the source data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-group.html#cfn-customerprofiles-segmentdefinition-group-sourcetype
            '''
            result = self._values.get("source_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Defines how to interact with the profiles found in the current filtering.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-group.html#cfn-customerprofiles-segmentdefinition-group-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnSegmentDefinitionPropsMixin.ProfileAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_number": "accountNumber",
            "additional_information": "additionalInformation",
            "address": "address",
            "attributes": "attributes",
            "billing_address": "billingAddress",
            "birth_date": "birthDate",
            "business_email_address": "businessEmailAddress",
            "business_name": "businessName",
            "business_phone_number": "businessPhoneNumber",
            "email_address": "emailAddress",
            "first_name": "firstName",
            "gender_string": "genderString",
            "home_phone_number": "homePhoneNumber",
            "last_name": "lastName",
            "mailing_address": "mailingAddress",
            "middle_name": "middleName",
            "mobile_phone_number": "mobilePhoneNumber",
            "party_type_string": "partyTypeString",
            "personal_email_address": "personalEmailAddress",
            "phone_number": "phoneNumber",
            "profile_type": "profileType",
            "shipping_address": "shippingAddress",
        },
    )
    class ProfileAttributesProperty:
        def __init__(
            self,
            *,
            account_number: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            additional_information: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.ExtraLengthValueProfileDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            address: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.AddressDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.AttributeDimensionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            billing_address: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.AddressDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            birth_date: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.DateDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            business_email_address: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            business_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            business_phone_number: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            email_address: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            first_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            gender_string: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            home_phone_number: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            last_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            mailing_address: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.AddressDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            middle_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            mobile_phone_number: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            party_type_string: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            personal_email_address: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            phone_number: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            profile_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.ProfileTypeDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            shipping_address: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.AddressDimensionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The object used to segment on attributes within the customer profile.

            :param account_number: A field to describe values to segment on within account number.
            :param additional_information: A field to describe values to segment on within additional information.
            :param address: A field to describe values to segment on within address.
            :param attributes: A field to describe values to segment on within attributes.
            :param billing_address: A field to describe values to segment on within billing address.
            :param birth_date: A field to describe values to segment on within birthDate.
            :param business_email_address: A field to describe values to segment on within business email address.
            :param business_name: A field to describe values to segment on within business name.
            :param business_phone_number: A field to describe values to segment on within business phone number.
            :param email_address: A field to describe values to segment on within email address.
            :param first_name: A field to describe values to segment on within first name.
            :param gender_string: A field to describe values to segment on within genderString.
            :param home_phone_number: A field to describe values to segment on within home phone number.
            :param last_name: A field to describe values to segment on within last name.
            :param mailing_address: A field to describe values to segment on within mailing address.
            :param middle_name: A field to describe values to segment on within middle name.
            :param mobile_phone_number: A field to describe values to segment on within mobile phone number.
            :param party_type_string: A field to describe values to segment on within partyTypeString.
            :param personal_email_address: A field to describe values to segment on within personal email address.
            :param phone_number: A field to describe values to segment on within phone number.
            :param profile_type: The type of profile.
            :param shipping_address: A field to describe values to segment on within shipping address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profileattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                profile_attributes_property = customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileAttributesProperty(
                    account_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    additional_information=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ExtraLengthValueProfileDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                        city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        )
                    ),
                    attributes={
                        "attributes_key": customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AttributeDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        )
                    },
                    billing_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                        city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        )
                    ),
                    birth_date=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.DateDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    business_email_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    business_name=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    business_phone_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    email_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    first_name=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    gender_string=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    home_phone_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    last_name=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    mailing_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                        city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        )
                    ),
                    middle_name=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    mobile_phone_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    party_type_string=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    personal_email_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    phone_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    profile_type=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileTypeDimensionProperty(
                        dimension_type="dimensionType",
                        values=["values"]
                    ),
                    shipping_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                        city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        ),
                        state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                            dimension_type="dimensionType",
                            values=["values"]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5a1ac6d9f8b75be7fe36715b225066d9dc5f8e691a354f0a4f22ebd300fae36a)
                check_type(argname="argument account_number", value=account_number, expected_type=type_hints["account_number"])
                check_type(argname="argument additional_information", value=additional_information, expected_type=type_hints["additional_information"])
                check_type(argname="argument address", value=address, expected_type=type_hints["address"])
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                check_type(argname="argument billing_address", value=billing_address, expected_type=type_hints["billing_address"])
                check_type(argname="argument birth_date", value=birth_date, expected_type=type_hints["birth_date"])
                check_type(argname="argument business_email_address", value=business_email_address, expected_type=type_hints["business_email_address"])
                check_type(argname="argument business_name", value=business_name, expected_type=type_hints["business_name"])
                check_type(argname="argument business_phone_number", value=business_phone_number, expected_type=type_hints["business_phone_number"])
                check_type(argname="argument email_address", value=email_address, expected_type=type_hints["email_address"])
                check_type(argname="argument first_name", value=first_name, expected_type=type_hints["first_name"])
                check_type(argname="argument gender_string", value=gender_string, expected_type=type_hints["gender_string"])
                check_type(argname="argument home_phone_number", value=home_phone_number, expected_type=type_hints["home_phone_number"])
                check_type(argname="argument last_name", value=last_name, expected_type=type_hints["last_name"])
                check_type(argname="argument mailing_address", value=mailing_address, expected_type=type_hints["mailing_address"])
                check_type(argname="argument middle_name", value=middle_name, expected_type=type_hints["middle_name"])
                check_type(argname="argument mobile_phone_number", value=mobile_phone_number, expected_type=type_hints["mobile_phone_number"])
                check_type(argname="argument party_type_string", value=party_type_string, expected_type=type_hints["party_type_string"])
                check_type(argname="argument personal_email_address", value=personal_email_address, expected_type=type_hints["personal_email_address"])
                check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
                check_type(argname="argument profile_type", value=profile_type, expected_type=type_hints["profile_type"])
                check_type(argname="argument shipping_address", value=shipping_address, expected_type=type_hints["shipping_address"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_number is not None:
                self._values["account_number"] = account_number
            if additional_information is not None:
                self._values["additional_information"] = additional_information
            if address is not None:
                self._values["address"] = address
            if attributes is not None:
                self._values["attributes"] = attributes
            if billing_address is not None:
                self._values["billing_address"] = billing_address
            if birth_date is not None:
                self._values["birth_date"] = birth_date
            if business_email_address is not None:
                self._values["business_email_address"] = business_email_address
            if business_name is not None:
                self._values["business_name"] = business_name
            if business_phone_number is not None:
                self._values["business_phone_number"] = business_phone_number
            if email_address is not None:
                self._values["email_address"] = email_address
            if first_name is not None:
                self._values["first_name"] = first_name
            if gender_string is not None:
                self._values["gender_string"] = gender_string
            if home_phone_number is not None:
                self._values["home_phone_number"] = home_phone_number
            if last_name is not None:
                self._values["last_name"] = last_name
            if mailing_address is not None:
                self._values["mailing_address"] = mailing_address
            if middle_name is not None:
                self._values["middle_name"] = middle_name
            if mobile_phone_number is not None:
                self._values["mobile_phone_number"] = mobile_phone_number
            if party_type_string is not None:
                self._values["party_type_string"] = party_type_string
            if personal_email_address is not None:
                self._values["personal_email_address"] = personal_email_address
            if phone_number is not None:
                self._values["phone_number"] = phone_number
            if profile_type is not None:
                self._values["profile_type"] = profile_type
            if shipping_address is not None:
                self._values["shipping_address"] = shipping_address

        @builtins.property
        def account_number(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]]:
            '''A field to describe values to segment on within account number.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profileattributes.html#cfn-customerprofiles-segmentdefinition-profileattributes-accountnumber
            '''
            result = self._values.get("account_number")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]], result)

        @builtins.property
        def additional_information(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ExtraLengthValueProfileDimensionProperty"]]:
            '''A field to describe values to segment on within additional information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profileattributes.html#cfn-customerprofiles-segmentdefinition-profileattributes-additionalinformation
            '''
            result = self._values.get("additional_information")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ExtraLengthValueProfileDimensionProperty"]], result)

        @builtins.property
        def address(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.AddressDimensionProperty"]]:
            '''A field to describe values to segment on within address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profileattributes.html#cfn-customerprofiles-segmentdefinition-profileattributes-address
            '''
            result = self._values.get("address")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.AddressDimensionProperty"]], result)

        @builtins.property
        def attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.AttributeDimensionProperty"]]]]:
            '''A field to describe values to segment on within attributes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profileattributes.html#cfn-customerprofiles-segmentdefinition-profileattributes-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.AttributeDimensionProperty"]]]], result)

        @builtins.property
        def billing_address(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.AddressDimensionProperty"]]:
            '''A field to describe values to segment on within billing address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profileattributes.html#cfn-customerprofiles-segmentdefinition-profileattributes-billingaddress
            '''
            result = self._values.get("billing_address")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.AddressDimensionProperty"]], result)

        @builtins.property
        def birth_date(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.DateDimensionProperty"]]:
            '''A field to describe values to segment on within birthDate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profileattributes.html#cfn-customerprofiles-segmentdefinition-profileattributes-birthdate
            '''
            result = self._values.get("birth_date")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.DateDimensionProperty"]], result)

        @builtins.property
        def business_email_address(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]]:
            '''A field to describe values to segment on within business email address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profileattributes.html#cfn-customerprofiles-segmentdefinition-profileattributes-businessemailaddress
            '''
            result = self._values.get("business_email_address")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]], result)

        @builtins.property
        def business_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]]:
            '''A field to describe values to segment on within business name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profileattributes.html#cfn-customerprofiles-segmentdefinition-profileattributes-businessname
            '''
            result = self._values.get("business_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]], result)

        @builtins.property
        def business_phone_number(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]]:
            '''A field to describe values to segment on within business phone number.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profileattributes.html#cfn-customerprofiles-segmentdefinition-profileattributes-businessphonenumber
            '''
            result = self._values.get("business_phone_number")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]], result)

        @builtins.property
        def email_address(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]]:
            '''A field to describe values to segment on within email address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profileattributes.html#cfn-customerprofiles-segmentdefinition-profileattributes-emailaddress
            '''
            result = self._values.get("email_address")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]], result)

        @builtins.property
        def first_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]]:
            '''A field to describe values to segment on within first name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profileattributes.html#cfn-customerprofiles-segmentdefinition-profileattributes-firstname
            '''
            result = self._values.get("first_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]], result)

        @builtins.property
        def gender_string(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]]:
            '''A field to describe values to segment on within genderString.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profileattributes.html#cfn-customerprofiles-segmentdefinition-profileattributes-genderstring
            '''
            result = self._values.get("gender_string")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]], result)

        @builtins.property
        def home_phone_number(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]]:
            '''A field to describe values to segment on within home phone number.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profileattributes.html#cfn-customerprofiles-segmentdefinition-profileattributes-homephonenumber
            '''
            result = self._values.get("home_phone_number")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]], result)

        @builtins.property
        def last_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]]:
            '''A field to describe values to segment on within last name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profileattributes.html#cfn-customerprofiles-segmentdefinition-profileattributes-lastname
            '''
            result = self._values.get("last_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]], result)

        @builtins.property
        def mailing_address(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.AddressDimensionProperty"]]:
            '''A field to describe values to segment on within mailing address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profileattributes.html#cfn-customerprofiles-segmentdefinition-profileattributes-mailingaddress
            '''
            result = self._values.get("mailing_address")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.AddressDimensionProperty"]], result)

        @builtins.property
        def middle_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]]:
            '''A field to describe values to segment on within middle name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profileattributes.html#cfn-customerprofiles-segmentdefinition-profileattributes-middlename
            '''
            result = self._values.get("middle_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]], result)

        @builtins.property
        def mobile_phone_number(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]]:
            '''A field to describe values to segment on within mobile phone number.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profileattributes.html#cfn-customerprofiles-segmentdefinition-profileattributes-mobilephonenumber
            '''
            result = self._values.get("mobile_phone_number")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]], result)

        @builtins.property
        def party_type_string(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]]:
            '''A field to describe values to segment on within partyTypeString.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profileattributes.html#cfn-customerprofiles-segmentdefinition-profileattributes-partytypestring
            '''
            result = self._values.get("party_type_string")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]], result)

        @builtins.property
        def personal_email_address(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]]:
            '''A field to describe values to segment on within personal email address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profileattributes.html#cfn-customerprofiles-segmentdefinition-profileattributes-personalemailaddress
            '''
            result = self._values.get("personal_email_address")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]], result)

        @builtins.property
        def phone_number(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]]:
            '''A field to describe values to segment on within phone number.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profileattributes.html#cfn-customerprofiles-segmentdefinition-profileattributes-phonenumber
            '''
            result = self._values.get("phone_number")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty"]], result)

        @builtins.property
        def profile_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileTypeDimensionProperty"]]:
            '''The type of profile.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profileattributes.html#cfn-customerprofiles-segmentdefinition-profileattributes-profiletype
            '''
            result = self._values.get("profile_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.ProfileTypeDimensionProperty"]], result)

        @builtins.property
        def shipping_address(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.AddressDimensionProperty"]]:
            '''A field to describe values to segment on within shipping address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profileattributes.html#cfn-customerprofiles-segmentdefinition-profileattributes-shippingaddress
            '''
            result = self._values.get("shipping_address")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.AddressDimensionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProfileAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"dimension_type": "dimensionType", "values": "values"},
    )
    class ProfileDimensionProperty:
        def __init__(
            self,
            *,
            dimension_type: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Object that segments on various Customer profile's fields that are larger than normal.

            :param dimension_type: The action to segment on.
            :param values: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profiledimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                profile_dimension_property = customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                    dimension_type="dimensionType",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6b59999d000bced90e77bd4f27e42343b2909d8a46f4197a097200e39b4ffefc)
                check_type(argname="argument dimension_type", value=dimension_type, expected_type=type_hints["dimension_type"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimension_type is not None:
                self._values["dimension_type"] = dimension_type
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def dimension_type(self) -> typing.Optional[builtins.str]:
            '''The action to segment on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profiledimension.html#cfn-customerprofiles-segmentdefinition-profiledimension-dimensiontype
            '''
            result = self._values.get("dimension_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profiledimension.html#cfn-customerprofiles-segmentdefinition-profiledimension-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProfileDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnSegmentDefinitionPropsMixin.ProfileTypeDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"dimension_type": "dimensionType", "values": "values"},
    )
    class ProfileTypeDimensionProperty:
        def __init__(
            self,
            *,
            dimension_type: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies profile type based criteria for a segment.

            :param dimension_type: The action to segment on.
            :param values: The values to apply the DimensionType on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profiletypedimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                profile_type_dimension_property = customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileTypeDimensionProperty(
                    dimension_type="dimensionType",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bc05df38bf4e7ac3184372f70b7c0f53b94bbe8a32adac284f7035ca8ac6503a)
                check_type(argname="argument dimension_type", value=dimension_type, expected_type=type_hints["dimension_type"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimension_type is not None:
                self._values["dimension_type"] = dimension_type
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def dimension_type(self) -> typing.Optional[builtins.str]:
            '''The action to segment on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profiletypedimension.html#cfn-customerprofiles-segmentdefinition-profiletypedimension-dimensiontype
            '''
            result = self._values.get("dimension_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The values to apply the DimensionType on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-profiletypedimension.html#cfn-customerprofiles-segmentdefinition-profiletypedimension-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProfileTypeDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnSegmentDefinitionPropsMixin.RangeOverrideProperty",
        jsii_struct_bases=[],
        name_mapping={"end": "end", "start": "start", "unit": "unit"},
    )
    class RangeOverrideProperty:
        def __init__(
            self,
            *,
            end: typing.Optional[jsii.Number] = None,
            start: typing.Optional[jsii.Number] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Overrides the original range on a calculated attribute definition.

            :param end: The end time of when to include objects.
            :param start: The start time of when to include objects.
            :param unit: The unit for start and end.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-rangeoverride.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                range_override_property = customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.RangeOverrideProperty(
                    end=123,
                    start=123,
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ef2e93bdf237bf8571bb65c1ebfd0e23eb44a5c3fbd9ca4941f238fe7b988156)
                check_type(argname="argument end", value=end, expected_type=type_hints["end"])
                check_type(argname="argument start", value=start, expected_type=type_hints["start"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if end is not None:
                self._values["end"] = end
            if start is not None:
                self._values["start"] = start
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def end(self) -> typing.Optional[jsii.Number]:
            '''The end time of when to include objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-rangeoverride.html#cfn-customerprofiles-segmentdefinition-rangeoverride-end
            '''
            result = self._values.get("end")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def start(self) -> typing.Optional[jsii.Number]:
            '''The start time of when to include objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-rangeoverride.html#cfn-customerprofiles-segmentdefinition-rangeoverride-start
            '''
            result = self._values.get("start")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The unit for start and end.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-rangeoverride.html#cfn-customerprofiles-segmentdefinition-rangeoverride-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RangeOverrideProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnSegmentDefinitionPropsMixin.SegmentGroupProperty",
        jsii_struct_bases=[],
        name_mapping={"groups": "groups", "include": "include"},
    )
    class SegmentGroupProperty:
        def __init__(
            self,
            *,
            groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSegmentDefinitionPropsMixin.GroupProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            include: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains all groups of the segment definition.

            :param groups: Holds the list of groups within the segment definition.
            :param include: Defines whether to include or exclude the profiles that fit the segment criteria.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-segmentgroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                segment_group_property = customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.SegmentGroupProperty(
                    groups=[customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.GroupProperty(
                        dimensions=[customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.DimensionProperty(
                            calculated_attributes={
                                "calculated_attributes_key": customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.CalculatedAttributeDimensionProperty(
                                    condition_overrides=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ConditionOverridesProperty(
                                        range=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.RangeOverrideProperty(
                                            end=123,
                                            start=123,
                                            unit="unit"
                                        )
                                    ),
                                    dimension_type="dimensionType",
                                    values=["values"]
                                )
                            },
                            profile_attributes=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileAttributesProperty(
                                account_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                additional_information=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ExtraLengthValueProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                                    city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    )
                                ),
                                attributes={
                                    "attributes_key": customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AttributeDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    )
                                },
                                billing_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                                    city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    )
                                ),
                                birth_date=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.DateDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                business_email_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                business_name=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                business_phone_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                email_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                first_name=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                gender_string=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                home_phone_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                last_name=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                mailing_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                                    city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    )
                                ),
                                middle_name=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                mobile_phone_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                party_type_string=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                personal_email_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                phone_number=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                profile_type=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileTypeDimensionProperty(
                                    dimension_type="dimensionType",
                                    values=["values"]
                                ),
                                shipping_address=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.AddressDimensionProperty(
                                    city=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    country=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    county=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    postal_code=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    province=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    ),
                                    state=customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty(
                                        dimension_type="dimensionType",
                                        values=["values"]
                                    )
                                )
                            )
                        )],
                        source_segments=[customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.SourceSegmentProperty(
                            segment_definition_name="segmentDefinitionName"
                        )],
                        source_type="sourceType",
                        type="type"
                    )],
                    include="include"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4185fe1ae46a8e08ec9ab9894e1bb05386e051f5949ff89dd3c8d113908609f2)
                check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
                check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if groups is not None:
                self._values["groups"] = groups
            if include is not None:
                self._values["include"] = include

        @builtins.property
        def groups(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.GroupProperty"]]]]:
            '''Holds the list of groups within the segment definition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-segmentgroup.html#cfn-customerprofiles-segmentdefinition-segmentgroup-groups
            '''
            result = self._values.get("groups")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSegmentDefinitionPropsMixin.GroupProperty"]]]], result)

        @builtins.property
        def include(self) -> typing.Optional[builtins.str]:
            '''Defines whether to include or exclude the profiles that fit the segment criteria.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-segmentgroup.html#cfn-customerprofiles-segmentdefinition-segmentgroup-include
            '''
            result = self._values.get("include")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SegmentGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_customerprofiles.mixins.CfnSegmentDefinitionPropsMixin.SourceSegmentProperty",
        jsii_struct_bases=[],
        name_mapping={"segment_definition_name": "segmentDefinitionName"},
    )
    class SourceSegmentProperty:
        def __init__(
            self,
            *,
            segment_definition_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The source segments to build off of.

            :param segment_definition_name: The name of the source segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-sourcesegment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_customerprofiles import mixins as customerprofiles_mixins
                
                source_segment_property = customerprofiles_mixins.CfnSegmentDefinitionPropsMixin.SourceSegmentProperty(
                    segment_definition_name="segmentDefinitionName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__70249a72a5538b69122cb0dc282d9d6a7f417ee2828cb3fdfb8c12111b7e533b)
                check_type(argname="argument segment_definition_name", value=segment_definition_name, expected_type=type_hints["segment_definition_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if segment_definition_name is not None:
                self._values["segment_definition_name"] = segment_definition_name

        @builtins.property
        def segment_definition_name(self) -> typing.Optional[builtins.str]:
            '''The name of the source segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-customerprofiles-segmentdefinition-sourcesegment.html#cfn-customerprofiles-segmentdefinition-sourcesegment-segmentdefinitionname
            '''
            result = self._values.get("segment_definition_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceSegmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnCalculatedAttributeDefinitionMixinProps",
    "CfnCalculatedAttributeDefinitionPropsMixin",
    "CfnDomainMixinProps",
    "CfnDomainPropsMixin",
    "CfnEventStreamMixinProps",
    "CfnEventStreamPropsMixin",
    "CfnEventTriggerMixinProps",
    "CfnEventTriggerPropsMixin",
    "CfnIntegrationMixinProps",
    "CfnIntegrationPropsMixin",
    "CfnObjectTypeMixinProps",
    "CfnObjectTypePropsMixin",
    "CfnSegmentDefinitionMixinProps",
    "CfnSegmentDefinitionPropsMixin",
]

publication.publish()

def _typecheckingstub__11c8c27e084e0280eea7f2225b5f1894a6b9117d79deecf4c9c861221243df04(
    *,
    attribute_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCalculatedAttributeDefinitionPropsMixin.AttributeDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    calculated_attribute_name: typing.Optional[builtins.str] = None,
    conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCalculatedAttributeDefinitionPropsMixin.ConditionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    use_historical_data: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d2fee4a3f678c50fccf2867468ff926f644f701ab9d58070cf1667621dc8194(
    props: typing.Union[CfnCalculatedAttributeDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c4c378bcc003988d06041c9d86a3479efde9c8f7585dde78b2a47e3e5060585(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9cdbe5700c0d4f0cadf18e6639b5ffa709125e54b1f4b6b5f1b5250274c73e9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eba6d4d6be12624c49ef763235f2e205bd01b05d66a3be22bb0670ee10640ec(
    *,
    attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCalculatedAttributeDefinitionPropsMixin.AttributeItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__154d920b67d4ddc5e56bc53287d3041fc15f6110453e1db82b750f43712fc279(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41f9d576465dff29534c34b52f6cd729ad8b301849cdfd028ec335f2da551b08(
    *,
    object_count: typing.Optional[jsii.Number] = None,
    range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCalculatedAttributeDefinitionPropsMixin.RangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    threshold: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCalculatedAttributeDefinitionPropsMixin.ThresholdProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85eaa2a7b18f3d0b4cdb430cba87b765606116c7f2262083ba220d5039a0e409(
    *,
    timestamp_format: typing.Optional[builtins.str] = None,
    timestamp_source: typing.Optional[builtins.str] = None,
    unit: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
    value_range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCalculatedAttributeDefinitionPropsMixin.ValueRangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d31f1f20b14d079d19997980b1fcbc49f0d2be08cc9f8a50b4c604fb07ff0a6(
    *,
    message: typing.Optional[builtins.str] = None,
    progress_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbfded726a559f79af6296226a05180016e2bdf1c60ad88792e22e1e10a8de54(
    *,
    operator: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ade600d52dd25af62412db0b6788b50fd3ea4af58656fef41ebed45405ae1fb0(
    *,
    end: typing.Optional[jsii.Number] = None,
    start: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21f2e43cdf2518c0f94f582ba5191398d2e1bf5181360a4cb3ce715238cc087e(
    *,
    data_store: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.DataStoreProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dead_letter_queue_url: typing.Optional[builtins.str] = None,
    default_encryption_key: typing.Optional[builtins.str] = None,
    default_expiration_days: typing.Optional[jsii.Number] = None,
    domain_name: typing.Optional[builtins.str] = None,
    matching: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.MatchingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rule_based_matching: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.RuleBasedMatchingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa94f2a366916f67cd6f67160d52e43db017a8280a49ac449609fe5a8bd209f(
    props: typing.Union[CfnDomainMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ead32f2b9c6380696b5191ef4d2a96604a726e89b9a83914c420b13d10c75936(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2412f77e51e66f72b8957429ec17d802f55e9ce8fdec365869ec741d1a659de0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3992a9a90bdf739ebd239292fc7f9dc82a7b48ac43bd1cc89b0b8c516ae96d6(
    *,
    address: typing.Optional[typing.Sequence[builtins.str]] = None,
    attribute_matching_model: typing.Optional[builtins.str] = None,
    email_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    phone_number: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c1b0f1494d30267ee9ca52019662e1858c13d75fe5949d86ed877a012f9128(
    *,
    conflict_resolution: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.ConflictResolutionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    consolidation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.ConsolidationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    min_allowed_confidence_score_for_merging: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ee9d5e273dfb493ccc1d8d0df265f232ec1cc3743f511d4b5c2ae93296323ba(
    *,
    conflict_resolving_model: typing.Optional[builtins.str] = None,
    source_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b483c12a548196810d64b15ac46b308e8b03b8fc132935284c8faabf47fc2b30(
    *,
    matching_attributes_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Sequence[builtins.str]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0ed067c428bc0c8a8860941a8c62a3772a06ac1e365c7cc1cbadc4afdfd0f74(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    readiness: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.ReadinessProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2e538ec103a4b76473caf3164f2ec8cb73e5f6ffdcfbf69285bfc36930ba1fd(
    *,
    metering_profile_count: typing.Optional[jsii.Number] = None,
    object_count: typing.Optional[jsii.Number] = None,
    profile_count: typing.Optional[jsii.Number] = None,
    total_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2d0943c6471c7ac09873208dec5e990667fd5844be85093225b0c53bcb15b7c(
    *,
    s3_exporting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.S3ExportingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9ba44c236a989e2c3c18eb190764f7a61ee755d6fdedb29f8c8fe52877b0ed3(
    *,
    day_of_the_week: typing.Optional[builtins.str] = None,
    time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c20ffd5d6a6b082a4dc00316178a09554280c7d416f41693bb23d656678f02f9(
    *,
    auto_merging: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.AutoMergingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    exporting_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.ExportingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    job_schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.JobScheduleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b3cb437b2fd7948f12b1fac47ad3ef7ed8bbeb5359981642efa4730c735891c(
    *,
    rule: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4be92d96a40955ddd84b92186525ce0b8c0ac8ac85f48beb6765122a3c0fe34(
    *,
    message: typing.Optional[builtins.str] = None,
    progress_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbca0175e3a2739a4e91d6d773afb25ee508bddddcd1fa2e2e8861ed708b9e78(
    *,
    attribute_types_selector: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.AttributeTypesSelectorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    conflict_resolution: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.ConflictResolutionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    exporting_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.ExportingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    matching_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.MatchingRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    max_allowed_rule_level_for_matching: typing.Optional[jsii.Number] = None,
    max_allowed_rule_level_for_merging: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6cc0efdfd4d85083ee99a850dfd71ac1e40a5187777fe07e572705a0da40f84(
    *,
    s3_bucket_name: typing.Optional[builtins.str] = None,
    s3_key_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b764b6cb778f30e7e4ab007beb82d68096b20f7370187293c74a1f9493bd41bf(
    *,
    domain_name: typing.Optional[builtins.str] = None,
    event_stream_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb6fb2781e80d57cdd21e259c236e6bdfae2f8684a1e074af4493c6678949e1d(
    props: typing.Union[CfnEventStreamMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a3c4cb30ca4d9a0f56c43787fc9ec6638a91c05e44264150eddf3e2d0728342(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32c13f19d5ab3cc1a44102224a82a6e921a1d254c50843ad244a54ca23955452(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa832c273e05b31f1cea288406119d23523ec6050210209f617b715fc88d0a8e(
    *,
    status: typing.Optional[builtins.str] = None,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90f6a4ce1a172abebd980c146669766e9afd341ff57c455ca519492dc55e7abb(
    *,
    description: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    event_trigger_conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventTriggerPropsMixin.EventTriggerConditionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    event_trigger_limits: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventTriggerPropsMixin.EventTriggerLimitsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    event_trigger_name: typing.Optional[builtins.str] = None,
    object_type_name: typing.Optional[builtins.str] = None,
    segment_filter: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb9fac16bd914b5707c22659bafdec4b3a4b8b0babf40133fdfbd195eeb57245(
    props: typing.Union[CfnEventTriggerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__511c8b9fe27cfd375cf0d2cfb4f107812c15177f359f9b212981e42af2dcf67d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e937d73370d337142ae9d6dfc59b3af266761c751383c89aeed387dc9d3698a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9974cd57fe093dcc44e2d7cfcec568b7ed72a3c3e84b050adc9988392012d82(
    *,
    event_trigger_dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventTriggerPropsMixin.EventTriggerDimensionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    logical_operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2c1d961471f12a049513cf55e93a58191657ecfd2986607dda747ca9b172acb(
    *,
    object_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventTriggerPropsMixin.ObjectAttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c4636c1ce207d50ac76829f142d4bb24f094e43b90cc04843c84ae2c1a3648(
    *,
    event_expiration: typing.Optional[jsii.Number] = None,
    periods: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventTriggerPropsMixin.PeriodProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d3b7eb87d48dd7856f13c914e93e06184ed55f035c73e31175d714154e5363c(
    *,
    comparison_operator: typing.Optional[builtins.str] = None,
    field_name: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95a8f3360908208d60458656fdcc69c2b08a547364680e8a9b5a213534114817(
    *,
    max_invocations_per_profile: typing.Optional[jsii.Number] = None,
    unit: typing.Optional[builtins.str] = None,
    unlimited: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6fc3f999ba26c704a86766316ac389a0f0dc4ac0e4b192c45da2856aef8f743(
    *,
    domain_name: typing.Optional[builtins.str] = None,
    event_trigger_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    flow_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIntegrationPropsMixin.FlowDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    object_type_name: typing.Optional[builtins.str] = None,
    object_type_names: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIntegrationPropsMixin.ObjectTypeMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a4b35bc21a498eb5e7850f4428e95e57d05d20fef138de431be08557bf84907(
    props: typing.Union[CfnIntegrationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b541ddc166354967acf3d11257fad37e3b4b78d03843b97f34461333ee783e76(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41c801ffdb9f84f20fdb22bf4baa692aae7bab9095f77bc010f39f18f0f9cdc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a396c389f656efc8c1cab75fac2dd65f123b5fd00e539bf8a2d50bd2181dbb(
    *,
    marketo: typing.Optional[builtins.str] = None,
    s3: typing.Optional[builtins.str] = None,
    salesforce: typing.Optional[builtins.str] = None,
    service_now: typing.Optional[builtins.str] = None,
    zendesk: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f07f9f35d6777798cd1f3e63f7fa40bd4159c25bc542cb28857ca6dfc51c8ef3(
    *,
    description: typing.Optional[builtins.str] = None,
    flow_name: typing.Optional[builtins.str] = None,
    kms_arn: typing.Optional[builtins.str] = None,
    source_flow_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIntegrationPropsMixin.SourceFlowConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tasks: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIntegrationPropsMixin.TaskProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    trigger_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIntegrationPropsMixin.TriggerConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433e066febc112e4f4c212769645f432bd3b0d6e2f031b7bf8db48548c659608(
    *,
    datetime_type_field_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ccdf500f0d6150bced9105cd438f59c30b76b2d42687fcafc2fdb6fef42d305(
    *,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dbd7bd13bf311c10b0322cc4afa8c4d0f41237e43230b124aece81a42703ddf(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df75a4a797c99ec5ec7d95b756aab744c1fca4c18b05924a8f339435326f7449(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a8a6757763a15724208911044320817cd5571b25d315b8c1c0a4a7c492c0d2f(
    *,
    enable_dynamic_field_update: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_deleted_records: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abed88269dff4d554864e53d5ce25267e17ea4a7a34ab55c56583a7510f2d89f(
    *,
    data_pull_mode: typing.Optional[builtins.str] = None,
    first_execution_from: typing.Optional[jsii.Number] = None,
    schedule_end_time: typing.Optional[jsii.Number] = None,
    schedule_expression: typing.Optional[builtins.str] = None,
    schedule_offset: typing.Optional[jsii.Number] = None,
    schedule_start_time: typing.Optional[jsii.Number] = None,
    timezone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5678bc2f83d5f365dff36236b0547a76e736de1779da31cc57df828233455e2(
    *,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__961ca362c64e5c873b0af570bfd01c535ce51326ba10a933123f4055d1a7f829(
    *,
    marketo: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIntegrationPropsMixin.MarketoSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIntegrationPropsMixin.S3SourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    salesforce: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIntegrationPropsMixin.SalesforceSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_now: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIntegrationPropsMixin.ServiceNowSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    zendesk: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIntegrationPropsMixin.ZendeskSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bac69a847098b72dbe7bbd718c7f40c0a0a2ef4ad3c8127eb36356ea3867cad(
    *,
    connector_profile_name: typing.Optional[builtins.str] = None,
    connector_type: typing.Optional[builtins.str] = None,
    incremental_pull_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIntegrationPropsMixin.IncrementalPullConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_connector_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIntegrationPropsMixin.SourceConnectorPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44bfd8ffbef037891005b023cae5220db8f0970b68d7a01484d0c48ac86774b0(
    *,
    operator_property_key: typing.Optional[builtins.str] = None,
    property: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14ab73542dfd9a8116688204f8f4a88edecc26a1bde03a20824254443710a5b5(
    *,
    connector_operator: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIntegrationPropsMixin.ConnectorOperatorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    destination_field: typing.Optional[builtins.str] = None,
    source_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    task_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIntegrationPropsMixin.TaskPropertiesMapProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    task_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c91ec52bcdb596cf3423656e96b8130b9d2645c20afd718eeffc0bb7a8123970(
    *,
    trigger_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIntegrationPropsMixin.TriggerPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    trigger_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f526f13bf48fccad76d805393d943949053ea3e404828cc32d86bf49b54345(
    *,
    scheduled: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIntegrationPropsMixin.ScheduledTriggerPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db8e236c701ef4156612d9cf0ff12efc4b984f811ab387225fc3650e34fd2c26(
    *,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77765cdf237179e7418145f933935b4f5bc5e312389dadbb09f4e4fd6170b0b0(
    *,
    allow_profile_creation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[builtins.str] = None,
    expiration_days: typing.Optional[jsii.Number] = None,
    fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnObjectTypePropsMixin.FieldMapProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    keys: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnObjectTypePropsMixin.KeyMapProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    max_profile_object_count: typing.Optional[jsii.Number] = None,
    object_type_name: typing.Optional[builtins.str] = None,
    source_last_updated_timestamp_format: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    template_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66bd2de7b076f7567a5dd83628f2181e57c7b59fffe8cf2aa4e0c3a02be2fe10(
    props: typing.Union[CfnObjectTypeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2492da61bfe358b2d63d046120f16ee300b151a4bf1086bc79b566d18206a3e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7bf2fdc9860f25afbba02e3c8d1c444ba3d0a0b71c7ac83f393bdf25c4095d7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a46f3406482fb31a3f2aed4f272fbc66ff7723896e0976132932eed73a30780(
    *,
    name: typing.Optional[builtins.str] = None,
    object_type_field: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnObjectTypePropsMixin.ObjectTypeFieldProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b3f898f102b0e8ee3dfcf77c841c3a52bfff6b29d6a00c2dc8437c7afd10455(
    *,
    name: typing.Optional[builtins.str] = None,
    object_type_key_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnObjectTypePropsMixin.ObjectTypeKeyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__427722cf4bccdf5231eb05ed80283e5c3f89a64a71a483f60d878b0f312aa3df(
    *,
    content_type: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd0133edb4f69b6d8c33eaf135711274d5a6045521457c747a3db1e99e19af80(
    *,
    field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    standard_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f0d23a33dd3e6f2f44c6c2eef350e130d31c812ecb7a831f59e1b81530693ec(
    *,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    segment_definition_name: typing.Optional[builtins.str] = None,
    segment_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.SegmentGroupProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    segment_sql_query: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00500b5560a614be2bb333f85c9b18246808421c85c21214ca2284fb36f73f56(
    props: typing.Union[CfnSegmentDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba0938a90e3064d58e1156d750eca2f7eb21e469397f287fd3f84640acad69f8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff586cdfffd66d3196e5d1ede83f1b33062a59924eadd5f641dfff57443b7b54(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d558178ff48b875ddaa027d3ff20d101224c88976637179a39a510f7f270f3c(
    *,
    city: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    country: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    county: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    postal_code: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    province: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    state: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7213b4f320a8f516919ec9a0da67cd7710340925506721ab3a6f9614870909e8(
    *,
    dimension_type: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f42037e0602e9d443b7ecd37ad3ea4dfd6fa322337f1125338e9bc871f1dc37(
    *,
    condition_overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.ConditionOverridesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dimension_type: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41454fa1226f1a0faa067f437d0aac1832a7f52781c08b5cca8c8aa89a5f80d0(
    *,
    range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.RangeOverrideProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b255036d861283aaf04ff796582c4cdb40671b5c070c069825348913fb8dd56a(
    *,
    dimension_type: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f045e8c7371e85b640098bf6c5e52c892cd3452c4e41f9e5285cd2eacfbda9d4(
    *,
    calculated_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.CalculatedAttributeDimensionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    profile_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.ProfileAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd47e75d0901a808c66015f575fec85ba6cd05860b42a0cd72ae89a6cfc9fa96(
    *,
    dimension_type: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c304abc4b76df3fbfe7a152032a13a8297cfe39e91b847342f79d8a3aad081fd(
    *,
    dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.DimensionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    source_segments: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.SourceSegmentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    source_type: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a1ac6d9f8b75be7fe36715b225066d9dc5f8e691a354f0a4f22ebd300fae36a(
    *,
    account_number: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    additional_information: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.ExtraLengthValueProfileDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    address: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.AddressDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.AttributeDimensionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    billing_address: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.AddressDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    birth_date: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.DateDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    business_email_address: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    business_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    business_phone_number: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    email_address: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    first_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    gender_string: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    home_phone_number: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    last_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mailing_address: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.AddressDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    middle_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mobile_phone_number: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    party_type_string: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    personal_email_address: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    phone_number: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.ProfileDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    profile_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.ProfileTypeDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    shipping_address: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.AddressDimensionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b59999d000bced90e77bd4f27e42343b2909d8a46f4197a097200e39b4ffefc(
    *,
    dimension_type: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc05df38bf4e7ac3184372f70b7c0f53b94bbe8a32adac284f7035ca8ac6503a(
    *,
    dimension_type: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef2e93bdf237bf8571bb65c1ebfd0e23eb44a5c3fbd9ca4941f238fe7b988156(
    *,
    end: typing.Optional[jsii.Number] = None,
    start: typing.Optional[jsii.Number] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4185fe1ae46a8e08ec9ab9894e1bb05386e051f5949ff89dd3c8d113908609f2(
    *,
    groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSegmentDefinitionPropsMixin.GroupProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    include: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70249a72a5538b69122cb0dc282d9d6a7f417ee2828cb3fdfb8c12111b7e533b(
    *,
    segment_definition_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
