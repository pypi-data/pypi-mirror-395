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
    jsii_type="@aws-cdk/mixins-preview.aws_resourceexplorer2.mixins.CfnDefaultViewAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={"view_arn": "viewArn"},
)
class CfnDefaultViewAssociationMixinProps:
    def __init__(self, *, view_arn: typing.Optional[builtins.str] = None) -> None:
        '''Properties for CfnDefaultViewAssociationPropsMixin.

        :param view_arn: The ARN of the view to set as the default for the AWS Region and AWS account in which you call this operation. The specified view must already exist in the specified Region.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-defaultviewassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_resourceexplorer2 import mixins as resourceexplorer2_mixins
            
            cfn_default_view_association_mixin_props = resourceexplorer2_mixins.CfnDefaultViewAssociationMixinProps(
                view_arn="viewArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ac709a1d8129c1d3608e276be5220d31df8e5b5f8d6fd3f14418021fd8dbe46)
            check_type(argname="argument view_arn", value=view_arn, expected_type=type_hints["view_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if view_arn is not None:
            self._values["view_arn"] = view_arn

    @builtins.property
    def view_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the view to set as the default for the AWS Region and AWS account in which you call this operation.

        The specified view must already exist in the specified Region.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-defaultviewassociation.html#cfn-resourceexplorer2-defaultviewassociation-viewarn
        '''
        result = self._values.get("view_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDefaultViewAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDefaultViewAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_resourceexplorer2.mixins.CfnDefaultViewAssociationPropsMixin",
):
    '''Sets the specified view as the default for the AWS Region in which you call this operation.

    If a user makes a search query that doesn't explicitly specify the view to use, Resource Explorer chooses this default view automatically for searches performed in this AWS Region .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-defaultviewassociation.html
    :cloudformationResource: AWS::ResourceExplorer2::DefaultViewAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_resourceexplorer2 import mixins as resourceexplorer2_mixins
        
        cfn_default_view_association_props_mixin = resourceexplorer2_mixins.CfnDefaultViewAssociationPropsMixin(resourceexplorer2_mixins.CfnDefaultViewAssociationMixinProps(
            view_arn="viewArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDefaultViewAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ResourceExplorer2::DefaultViewAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6212f64dcb5da554a55e7452eb6dbb9138bcf9bdfc9e8d63e4446b9fe5b2add9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a548c6357fc377c6e6c46652935fee277ca6fab349c51e9ff0cc80e7a2e748c8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d50dfa833d8d648dbc4f3b7c4619029e5a4791a0baa6212aac8b1d67abaa6a73)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDefaultViewAssociationMixinProps:
        return typing.cast(CfnDefaultViewAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_resourceexplorer2.mixins.CfnIndexMixinProps",
    jsii_struct_bases=[],
    name_mapping={"tags": "tags", "type": "type"},
)
class CfnIndexMixinProps:
    def __init__(
        self,
        *,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnIndexPropsMixin.

        :param tags: The specified tags are attached to only the index created in this AWS Region . The tags don't attach to any of the resources listed in the index.
        :param type: Specifies the type of the index in this Region. For information about the aggregator index and how it differs from a local index, see `Turning on cross-Region search by creating an aggregator index <https://docs.aws.amazon.com/resource-explorer/latest/userguide/manage-aggregator-region.html>`_ in the *AWS Resource Explorer User Guide.* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-index.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_resourceexplorer2 import mixins as resourceexplorer2_mixins
            
            cfn_index_mixin_props = resourceexplorer2_mixins.CfnIndexMixinProps(
                tags={
                    "tags_key": "tags"
                },
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f831a0f1d08403397dbf30306e72956b48c90b42ec3e307654d8c07a300442e)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The specified tags are attached to only the index created in this AWS Region .

        The tags don't attach to any of the resources listed in the index.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-index.html#cfn-resourceexplorer2-index-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of the index in this Region.

        For information about the aggregator index and how it differs from a local index, see `Turning on cross-Region search by creating an aggregator index <https://docs.aws.amazon.com/resource-explorer/latest/userguide/manage-aggregator-region.html>`_ in the *AWS Resource Explorer User Guide.* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-index.html#cfn-resourceexplorer2-index-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIndexMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnIndexPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_resourceexplorer2.mixins.CfnIndexPropsMixin",
):
    '''Turns on Resource Explorer in the AWS Region in which you called this operation by creating an index.

    Resource Explorer begins discovering the resources in this Region and stores the details about the resources in the index so that they can be queried by using the `Search <https://docs.aws.amazon.com/resource-explorer/latest/apireference/API_Search.html>`_ operation.

    You can create either a local index that returns search results from only the AWS Region in which the index exists, or you can create an aggregator index that returns search results from all AWS Regions in the AWS account .

    For more details about what happens when you turn on Resource Explorer in an AWS Region , see `Turning on Resource Explorer to index your resources in an AWS Region <https://docs.aws.amazon.com/resource-explorer/latest/userguide/manage-service-activate.html>`_ in the *AWS Resource Explorer User Guide.*

    If this is the first AWS Region in which you've created an index for Resource Explorer, this operation also creates a service-linked role in your AWS account that allows Resource Explorer to search for your resources and populate the index.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-index.html
    :cloudformationResource: AWS::ResourceExplorer2::Index
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_resourceexplorer2 import mixins as resourceexplorer2_mixins
        
        cfn_index_props_mixin = resourceexplorer2_mixins.CfnIndexPropsMixin(resourceexplorer2_mixins.CfnIndexMixinProps(
            tags={
                "tags_key": "tags"
            },
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnIndexMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ResourceExplorer2::Index``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fbf37a909b7c15b694b31650d8fb3b55cffc41006cb12278442abf8d059d1d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__048cfb00d305a080d7cc71b5d02f10dafca3dfa4089a24f6203c6daea64736f6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ed18047eb3eab32c957244424ed2c520b9b5fc091f523cc67ec7cea0b8eb5d4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIndexMixinProps:
        return typing.cast(CfnIndexMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_resourceexplorer2.mixins.CfnViewMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "filters": "filters",
        "included_properties": "includedProperties",
        "scope": "scope",
        "tags": "tags",
        "view_name": "viewName",
    },
)
class CfnViewMixinProps:
    def __init__(
        self,
        *,
        filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnViewPropsMixin.FiltersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        included_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnViewPropsMixin.IncludedPropertyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        scope: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        view_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnViewPropsMixin.

        :param filters: An array of strings that include search keywords, prefixes, and operators that filter the results that are returned for queries made using this view. When you use this view in a `Search <https://docs.aws.amazon.com/resource-explorer/latest/apireference/API_Search.html>`_ operation, the filter string is combined with the search's ``QueryString`` parameter using a logical ``AND`` operator. For information about the supported syntax, see `Search query reference for Resource Explorer <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html>`_ in the *AWS Resource Explorer User Guide* . .. epigraph:: This query string in the context of this operation supports only `filter prefixes <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html#query-syntax-filters>`_ with optional `operators <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html#query-syntax-operators>`_ . It doesn't support free-form text. For example, the string ``region:us* service:ec2 -tag:stage=prod`` includes all Amazon EC2 resources in any AWS Region that begin with the letters ``us`` and are *not* tagged with a key ``Stage`` that has the value ``prod`` .
        :param included_properties: A list of fields that provide additional information about the view.
        :param scope: The root ARN of the account, an organizational unit (OU), or an organization ARN. If left empty, the default is account.
        :param tags: Tag key and value pairs that are attached to the view.
        :param view_name: The name of the new view.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-view.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_resourceexplorer2 import mixins as resourceexplorer2_mixins
            
            cfn_view_mixin_props = resourceexplorer2_mixins.CfnViewMixinProps(
                filters=resourceexplorer2_mixins.CfnViewPropsMixin.FiltersProperty(
                    filter_string="filterString"
                ),
                included_properties=[resourceexplorer2_mixins.CfnViewPropsMixin.IncludedPropertyProperty(
                    name="name"
                )],
                scope="scope",
                tags={
                    "tags_key": "tags"
                },
                view_name="viewName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b1307221aff5cbb6eb7ea3438bde3cc0090edb94d8c195b0aade35632c83a08)
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument included_properties", value=included_properties, expected_type=type_hints["included_properties"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument view_name", value=view_name, expected_type=type_hints["view_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filters is not None:
            self._values["filters"] = filters
        if included_properties is not None:
            self._values["included_properties"] = included_properties
        if scope is not None:
            self._values["scope"] = scope
        if tags is not None:
            self._values["tags"] = tags
        if view_name is not None:
            self._values["view_name"] = view_name

    @builtins.property
    def filters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnViewPropsMixin.FiltersProperty"]]:
        '''An array of strings that include search keywords, prefixes, and operators that filter the results that are returned for queries made using this view.

        When you use this view in a `Search <https://docs.aws.amazon.com/resource-explorer/latest/apireference/API_Search.html>`_ operation, the filter string is combined with the search's ``QueryString`` parameter using a logical ``AND`` operator.

        For information about the supported syntax, see `Search query reference for Resource Explorer <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html>`_ in the *AWS Resource Explorer User Guide* .
        .. epigraph::

           This query string in the context of this operation supports only `filter prefixes <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html#query-syntax-filters>`_ with optional `operators <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html#query-syntax-operators>`_ . It doesn't support free-form text. For example, the string ``region:us* service:ec2 -tag:stage=prod`` includes all Amazon EC2 resources in any AWS Region that begin with the letters ``us`` and are *not* tagged with a key ``Stage`` that has the value ``prod`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-view.html#cfn-resourceexplorer2-view-filters
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnViewPropsMixin.FiltersProperty"]], result)

    @builtins.property
    def included_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnViewPropsMixin.IncludedPropertyProperty"]]]]:
        '''A list of fields that provide additional information about the view.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-view.html#cfn-resourceexplorer2-view-includedproperties
        '''
        result = self._values.get("included_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnViewPropsMixin.IncludedPropertyProperty"]]]], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''The root ARN of the account, an organizational unit (OU), or an organization ARN.

        If left empty, the default is account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-view.html#cfn-resourceexplorer2-view-scope
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tag key and value pairs that are attached to the view.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-view.html#cfn-resourceexplorer2-view-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def view_name(self) -> typing.Optional[builtins.str]:
        '''The name of the new view.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-view.html#cfn-resourceexplorer2-view-viewname
        '''
        result = self._values.get("view_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnViewMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnViewPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_resourceexplorer2.mixins.CfnViewPropsMixin",
):
    '''Creates a view that users can query by using the `Search <https://docs.aws.amazon.com/resource-explorer/latest/apireference/API_Search.html>`_ operation. Results from queries that you make using this view include only resources that match the view's ``Filters`` .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-view.html
    :cloudformationResource: AWS::ResourceExplorer2::View
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_resourceexplorer2 import mixins as resourceexplorer2_mixins
        
        cfn_view_props_mixin = resourceexplorer2_mixins.CfnViewPropsMixin(resourceexplorer2_mixins.CfnViewMixinProps(
            filters=resourceexplorer2_mixins.CfnViewPropsMixin.FiltersProperty(
                filter_string="filterString"
            ),
            included_properties=[resourceexplorer2_mixins.CfnViewPropsMixin.IncludedPropertyProperty(
                name="name"
            )],
            scope="scope",
            tags={
                "tags_key": "tags"
            },
            view_name="viewName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnViewMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ResourceExplorer2::View``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__213868267eb5928a3aa5040440c8b7700360493363dbda9af7cb17942ad6dfec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be7395b55c1376ba6f645e01aa2fc958844791987776f03da6316d7d4b04a45b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11e2fc45a4c5715c0cdd0ad99285b7e473de0ac95201472cdccd35782be9f826)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnViewMixinProps:
        return typing.cast(CfnViewMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_resourceexplorer2.mixins.CfnViewPropsMixin.FiltersProperty",
        jsii_struct_bases=[],
        name_mapping={"filter_string": "filterString"},
    )
    class FiltersProperty:
        def __init__(
            self,
            *,
            filter_string: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param filter_string: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourceexplorer2-view-filters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_resourceexplorer2 import mixins as resourceexplorer2_mixins
                
                filters_property = resourceexplorer2_mixins.CfnViewPropsMixin.FiltersProperty(
                    filter_string="filterString"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c3c6b56cc0794b909db067c81a1eaf3dd5c0b5a68798ff7d82addcbe13348ced)
                check_type(argname="argument filter_string", value=filter_string, expected_type=type_hints["filter_string"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if filter_string is not None:
                self._values["filter_string"] = filter_string

        @builtins.property
        def filter_string(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourceexplorer2-view-filters.html#cfn-resourceexplorer2-view-filters-filterstring
            '''
            result = self._values.get("filter_string")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FiltersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_resourceexplorer2.mixins.CfnViewPropsMixin.IncludedPropertyProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class IncludedPropertyProperty:
        def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
            '''Information about an additional property that describes a resource, that you can optionally include in a view.

            :param name: The name of the property that is included in this view.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourceexplorer2-view-includedproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_resourceexplorer2 import mixins as resourceexplorer2_mixins
                
                included_property_property = resourceexplorer2_mixins.CfnViewPropsMixin.IncludedPropertyProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__de7befbe373e84ca9e8034ed4f0ab9cff77bdd4e52de2f9259056aa988bef718)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the property that is included in this view.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourceexplorer2-view-includedproperty.html#cfn-resourceexplorer2-view-includedproperty-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IncludedPropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_resourceexplorer2.mixins.CfnViewPropsMixin.SearchFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"filter_string": "filterString"},
    )
    class SearchFilterProperty:
        def __init__(
            self,
            *,
            filter_string: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A search filter defines which resources can be part of a search query result set.

            :param filter_string: The string that contains the search keywords, prefixes, and operators to control the results that can be returned by a Search operation. For information about the supported syntax, see `Search query reference <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html>`_ in the *AWS Resource Explorer User Guide* . .. epigraph:: This query string in the context of this operation supports only `filter prefixes <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html#query-syntax-filters>`_ with optional `operators <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html#query-syntax-operators>`_ . It doesn't support free-form text. For example, the string ``region:us* service:ec2 -tag:stage=prod`` includes all Amazon EC2 resources in any AWS Region that begin with the letters ``us`` and are *not* tagged with a key ``Stage`` that has the value ``prod`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourceexplorer2-view-searchfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_resourceexplorer2 import mixins as resourceexplorer2_mixins
                
                search_filter_property = resourceexplorer2_mixins.CfnViewPropsMixin.SearchFilterProperty(
                    filter_string="filterString"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b6bee09c30987492f107d87d9f25240f063098335a29300ff0f588b23fc29798)
                check_type(argname="argument filter_string", value=filter_string, expected_type=type_hints["filter_string"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if filter_string is not None:
                self._values["filter_string"] = filter_string

        @builtins.property
        def filter_string(self) -> typing.Optional[builtins.str]:
            '''The string that contains the search keywords, prefixes, and operators to control the results that can be returned by a Search operation.

            For information about the supported syntax, see `Search query reference <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html>`_ in the *AWS Resource Explorer User Guide* .
            .. epigraph::

               This query string in the context of this operation supports only `filter prefixes <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html#query-syntax-filters>`_ with optional `operators <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html#query-syntax-operators>`_ . It doesn't support free-form text. For example, the string ``region:us* service:ec2 -tag:stage=prod`` includes all Amazon EC2 resources in any AWS Region that begin with the letters ``us`` and are *not* tagged with a key ``Stage`` that has the value ``prod`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourceexplorer2-view-searchfilter.html#cfn-resourceexplorer2-view-searchfilter-filterstring
            '''
            result = self._values.get("filter_string")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SearchFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnDefaultViewAssociationMixinProps",
    "CfnDefaultViewAssociationPropsMixin",
    "CfnIndexMixinProps",
    "CfnIndexPropsMixin",
    "CfnViewMixinProps",
    "CfnViewPropsMixin",
]

publication.publish()

def _typecheckingstub__4ac709a1d8129c1d3608e276be5220d31df8e5b5f8d6fd3f14418021fd8dbe46(
    *,
    view_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6212f64dcb5da554a55e7452eb6dbb9138bcf9bdfc9e8d63e4446b9fe5b2add9(
    props: typing.Union[CfnDefaultViewAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a548c6357fc377c6e6c46652935fee277ca6fab349c51e9ff0cc80e7a2e748c8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d50dfa833d8d648dbc4f3b7c4619029e5a4791a0baa6212aac8b1d67abaa6a73(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f831a0f1d08403397dbf30306e72956b48c90b42ec3e307654d8c07a300442e(
    *,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fbf37a909b7c15b694b31650d8fb3b55cffc41006cb12278442abf8d059d1d4(
    props: typing.Union[CfnIndexMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__048cfb00d305a080d7cc71b5d02f10dafca3dfa4089a24f6203c6daea64736f6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed18047eb3eab32c957244424ed2c520b9b5fc091f523cc67ec7cea0b8eb5d4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b1307221aff5cbb6eb7ea3438bde3cc0090edb94d8c195b0aade35632c83a08(
    *,
    filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnViewPropsMixin.FiltersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    included_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnViewPropsMixin.IncludedPropertyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    scope: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    view_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__213868267eb5928a3aa5040440c8b7700360493363dbda9af7cb17942ad6dfec(
    props: typing.Union[CfnViewMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be7395b55c1376ba6f645e01aa2fc958844791987776f03da6316d7d4b04a45b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e2fc45a4c5715c0cdd0ad99285b7e473de0ac95201472cdccd35782be9f826(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3c6b56cc0794b909db067c81a1eaf3dd5c0b5a68798ff7d82addcbe13348ced(
    *,
    filter_string: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de7befbe373e84ca9e8034ed4f0ab9cff77bdd4e52de2f9259056aa988bef718(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6bee09c30987492f107d87d9f25240f063098335a29300ff0f588b23fc29798(
    *,
    filter_string: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
