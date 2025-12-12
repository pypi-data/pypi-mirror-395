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
    jsii_type="@aws-cdk/mixins-preview.aws_opensearchserverless.mixins.CfnAccessPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "policy": "policy",
        "type": "type",
    },
)
class CfnAccessPolicyMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        policy: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAccessPolicyPropsMixin.

        :param description: The description of the policy.
        :param name: The name of the policy.
        :param policy: The JSON policy document without any whitespaces.
        :param type: The type of access policy. Currently the only option is ``data`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-accesspolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_opensearchserverless import mixins as opensearchserverless_mixins
            
            cfn_access_policy_mixin_props = opensearchserverless_mixins.CfnAccessPolicyMixinProps(
                description="description",
                name="name",
                policy="policy",
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93d12bd44b608e9267911c08fd1a35a5c86f9003f3911695cd4c63dd17e12426)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if policy is not None:
            self._values["policy"] = policy
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-accesspolicy.html#cfn-opensearchserverless-accesspolicy-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-accesspolicy.html#cfn-opensearchserverless-accesspolicy-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''The JSON policy document without any whitespaces.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-accesspolicy.html#cfn-opensearchserverless-accesspolicy-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of access policy.

        Currently the only option is ``data`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-accesspolicy.html#cfn-opensearchserverless-accesspolicy-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAccessPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_opensearchserverless.mixins.CfnAccessPolicyPropsMixin",
):
    '''Creates a data access policy for OpenSearch Serverless.

    Access policies limit access to collections and the resources within them, and allow a user to access that data irrespective of the access mechanism or network source. For more information, see `Data access control for Amazon OpenSearch Serverless <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-data-access.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-accesspolicy.html
    :cloudformationResource: AWS::OpenSearchServerless::AccessPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_opensearchserverless import mixins as opensearchserverless_mixins
        
        cfn_access_policy_props_mixin = opensearchserverless_mixins.CfnAccessPolicyPropsMixin(opensearchserverless_mixins.CfnAccessPolicyMixinProps(
            description="description",
            name="name",
            policy="policy",
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAccessPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::OpenSearchServerless::AccessPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57c5a0d0cf5e4343046d4b7a63c83104044c74e3a25663b82a35284f78aaf7b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bd0e0fdfd17f0f2869c42bcc87c3518c2f280e823edb04e15859557193b1924)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2169b4b30791db85fcd488bc98d73f015efce19a634fe597c1d55026404ca429)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAccessPolicyMixinProps:
        return typing.cast(CfnAccessPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_opensearchserverless.mixins.CfnCollectionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "standby_replicas": "standbyReplicas",
        "tags": "tags",
        "type": "type",
    },
)
class CfnCollectionMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        standby_replicas: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnCollectionPropsMixin.

        :param description: A description of the collection.
        :param name: The name of the collection. Collection names must meet the following criteria: - Starts with a lowercase letter - Unique to your account and AWS Region - Contains between 3 and 28 characters - Contains only lowercase letters a-z, the numbers 0-9, and the hyphen (-)
        :param standby_replicas: Indicates whether to use standby replicas for the collection. You can't update this property after the collection is already created. If you attempt to modify this property, the collection continues to use the original value.
        :param tags: An arbitrary set of tags (key–value pairs) to associate with the collection. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param type: The type of collection. Possible values are ``SEARCH`` , ``TIMESERIES`` , and ``VECTORSEARCH`` . For more information, see `Choosing a collection type <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-overview.html#serverless-usecase>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-collection.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_opensearchserverless import mixins as opensearchserverless_mixins
            
            cfn_collection_mixin_props = opensearchserverless_mixins.CfnCollectionMixinProps(
                description="description",
                name="name",
                standby_replicas="standbyReplicas",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9ee5cdd7ff9c40c1b8e5207d6677cbcccf56774c726b3c4fc1dbc0ef43ccc3f)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument standby_replicas", value=standby_replicas, expected_type=type_hints["standby_replicas"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if standby_replicas is not None:
            self._values["standby_replicas"] = standby_replicas
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the collection.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-collection.html#cfn-opensearchserverless-collection-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the collection.

        Collection names must meet the following criteria:

        - Starts with a lowercase letter
        - Unique to your account and AWS Region
        - Contains between 3 and 28 characters
        - Contains only lowercase letters a-z, the numbers 0-9, and the hyphen (-)

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-collection.html#cfn-opensearchserverless-collection-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def standby_replicas(self) -> typing.Optional[builtins.str]:
        '''Indicates whether to use standby replicas for the collection.

        You can't update this property after the collection is already created. If you attempt to modify this property, the collection continues to use the original value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-collection.html#cfn-opensearchserverless-collection-standbyreplicas
        '''
        result = self._values.get("standby_replicas")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An arbitrary set of tags (key–value pairs) to associate with the collection.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-collection.html#cfn-opensearchserverless-collection-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of collection.

        Possible values are ``SEARCH`` , ``TIMESERIES`` , and ``VECTORSEARCH`` . For more information, see `Choosing a collection type <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-overview.html#serverless-usecase>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-collection.html#cfn-opensearchserverless-collection-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCollectionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCollectionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_opensearchserverless.mixins.CfnCollectionPropsMixin",
):
    '''Specifies an OpenSearch Serverless collection.

    For more information, see `Creating and managing Amazon OpenSearch Serverless collections <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-manage.html>`_ in the *Amazon OpenSearch Service Developer Guide* .
    .. epigraph::

       You must create a matching `encryption policy <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-encryption.html>`_ in order for a collection to be created successfully. You can specify the policy resource within the same CloudFormation template as the collection resource if you use the `DependsOn <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ attribute. See `Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-collection.html#aws-resource-opensearchserverless-collection--examples>`_ for a sample template. Otherwise the encryption policy must already exist before you create the collection.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-collection.html
    :cloudformationResource: AWS::OpenSearchServerless::Collection
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_opensearchserverless import mixins as opensearchserverless_mixins
        
        cfn_collection_props_mixin = opensearchserverless_mixins.CfnCollectionPropsMixin(opensearchserverless_mixins.CfnCollectionMixinProps(
            description="description",
            name="name",
            standby_replicas="standbyReplicas",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCollectionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::OpenSearchServerless::Collection``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d475a66dbd228fe5f772eebabc0027b864856187441d1e7d10e74644a4955bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__87ffcf29ae0e266154f7b6db030603a6d96b03bc1f0d9a5fcea4b70a6bd93b53)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cca9691f5c869d378681d852e79ceda75d4d3e1a6b92e3108818992cc21bd53b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCollectionMixinProps:
        return typing.cast(CfnCollectionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_opensearchserverless.mixins.CfnIndexMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "collection_endpoint": "collectionEndpoint",
        "index_name": "indexName",
        "mappings": "mappings",
        "settings": "settings",
    },
)
class CfnIndexMixinProps:
    def __init__(
        self,
        *,
        collection_endpoint: typing.Optional[builtins.str] = None,
        index_name: typing.Optional[builtins.str] = None,
        mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIndexPropsMixin.MappingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIndexPropsMixin.IndexSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnIndexPropsMixin.

        :param collection_endpoint: The endpoint for the collection.
        :param index_name: The name of the OpenSearch Serverless index.
        :param mappings: Index mappings for the OpenSearch Serverless index.
        :param settings: Index settings for the OpenSearch Serverless index.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-index.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_opensearchserverless import mixins as opensearchserverless_mixins
            
            # property_mapping_property_: opensearchserverless_mixins.CfnIndexPropsMixin.PropertyMappingProperty
            
            cfn_index_mixin_props = opensearchserverless_mixins.CfnIndexMixinProps(
                collection_endpoint="collectionEndpoint",
                index_name="indexName",
                mappings=opensearchserverless_mixins.CfnIndexPropsMixin.MappingsProperty(
                    properties={
                        "properties_key": opensearchserverless_mixins.CfnIndexPropsMixin.PropertyMappingProperty(
                            dimension=123,
                            index=False,
                            method=opensearchserverless_mixins.CfnIndexPropsMixin.MethodProperty(
                                engine="engine",
                                name="name",
                                parameters=opensearchserverless_mixins.CfnIndexPropsMixin.ParametersProperty(
                                    ef_construction=123,
                                    m=123
                                ),
                                space_type="spaceType"
                            ),
                            properties={
                                "properties_key": property_mapping_property_
                            },
                            type="type",
                            value="value"
                        )
                    }
                ),
                settings=opensearchserverless_mixins.CfnIndexPropsMixin.IndexSettingsProperty(
                    index=opensearchserverless_mixins.CfnIndexPropsMixin.IndexProperty(
                        knn=False,
                        knn_algo_param_ef_search=123,
                        refresh_interval="refreshInterval"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebb4d974a179550968f1795693ab1a717d3e039a452e080c0c6d2b5246df867d)
            check_type(argname="argument collection_endpoint", value=collection_endpoint, expected_type=type_hints["collection_endpoint"])
            check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
            check_type(argname="argument mappings", value=mappings, expected_type=type_hints["mappings"])
            check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if collection_endpoint is not None:
            self._values["collection_endpoint"] = collection_endpoint
        if index_name is not None:
            self._values["index_name"] = index_name
        if mappings is not None:
            self._values["mappings"] = mappings
        if settings is not None:
            self._values["settings"] = settings

    @builtins.property
    def collection_endpoint(self) -> typing.Optional[builtins.str]:
        '''The endpoint for the collection.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-index.html#cfn-opensearchserverless-index-collectionendpoint
        '''
        result = self._values.get("collection_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def index_name(self) -> typing.Optional[builtins.str]:
        '''The name of the OpenSearch Serverless index.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-index.html#cfn-opensearchserverless-index-indexname
        '''
        result = self._values.get("index_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mappings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.MappingsProperty"]]:
        '''Index mappings for the OpenSearch Serverless index.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-index.html#cfn-opensearchserverless-index-mappings
        '''
        result = self._values.get("mappings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.MappingsProperty"]], result)

    @builtins.property
    def settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.IndexSettingsProperty"]]:
        '''Index settings for the OpenSearch Serverless index.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-index.html#cfn-opensearchserverless-index-settings
        '''
        result = self._values.get("settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.IndexSettingsProperty"]], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_opensearchserverless.mixins.CfnIndexPropsMixin",
):
    '''An OpenSearch Serverless index resource.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-index.html
    :cloudformationResource: AWS::OpenSearchServerless::Index
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_opensearchserverless import mixins as opensearchserverless_mixins
        
        # property_mapping_property_: opensearchserverless_mixins.CfnIndexPropsMixin.PropertyMappingProperty
        
        cfn_index_props_mixin = opensearchserverless_mixins.CfnIndexPropsMixin(opensearchserverless_mixins.CfnIndexMixinProps(
            collection_endpoint="collectionEndpoint",
            index_name="indexName",
            mappings=opensearchserverless_mixins.CfnIndexPropsMixin.MappingsProperty(
                properties={
                    "properties_key": opensearchserverless_mixins.CfnIndexPropsMixin.PropertyMappingProperty(
                        dimension=123,
                        index=False,
                        method=opensearchserverless_mixins.CfnIndexPropsMixin.MethodProperty(
                            engine="engine",
                            name="name",
                            parameters=opensearchserverless_mixins.CfnIndexPropsMixin.ParametersProperty(
                                ef_construction=123,
                                m=123
                            ),
                            space_type="spaceType"
                        ),
                        properties={
                            "properties_key": property_mapping_property_
                        },
                        type="type",
                        value="value"
                    )
                }
            ),
            settings=opensearchserverless_mixins.CfnIndexPropsMixin.IndexSettingsProperty(
                index=opensearchserverless_mixins.CfnIndexPropsMixin.IndexProperty(
                    knn=False,
                    knn_algo_param_ef_search=123,
                    refresh_interval="refreshInterval"
                )
            )
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
        '''Create a mixin to apply properties to ``AWS::OpenSearchServerless::Index``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__678269ad135eaec0e7e14072ad13728801b94bed85c928a0c4b6de9a4b291fa9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f44ed0254e1153473d18bd41860d1dbf38cccc64d7618cc320f2ffca6558d48)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee3c40d974cc2677a143cf6401ccdfb7dfd9bd1eabc601d013e0eb897132ad0e)
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
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchserverless.mixins.CfnIndexPropsMixin.IndexProperty",
        jsii_struct_bases=[],
        name_mapping={
            "knn": "knn",
            "knn_algo_param_ef_search": "knnAlgoParamEfSearch",
            "refresh_interval": "refreshInterval",
        },
    )
    class IndexProperty:
        def __init__(
            self,
            *,
            knn: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            knn_algo_param_ef_search: typing.Optional[jsii.Number] = None,
            refresh_interval: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An OpenSearch Serverless index resource.

            :param knn: Enable or disable k-nearest neighbor search capability.
            :param knn_algo_param_ef_search: The size of the dynamic list for the nearest neighbors.
            :param refresh_interval: How often to perform a refresh operation. For example, 1s or 5s.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-index-index.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchserverless import mixins as opensearchserverless_mixins
                
                index_property = opensearchserverless_mixins.CfnIndexPropsMixin.IndexProperty(
                    knn=False,
                    knn_algo_param_ef_search=123,
                    refresh_interval="refreshInterval"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__160ea4bdea5dc52d76ed64853499827cdccf231d049aba4c1f617689207b46b8)
                check_type(argname="argument knn", value=knn, expected_type=type_hints["knn"])
                check_type(argname="argument knn_algo_param_ef_search", value=knn_algo_param_ef_search, expected_type=type_hints["knn_algo_param_ef_search"])
                check_type(argname="argument refresh_interval", value=refresh_interval, expected_type=type_hints["refresh_interval"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if knn is not None:
                self._values["knn"] = knn
            if knn_algo_param_ef_search is not None:
                self._values["knn_algo_param_ef_search"] = knn_algo_param_ef_search
            if refresh_interval is not None:
                self._values["refresh_interval"] = refresh_interval

        @builtins.property
        def knn(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enable or disable k-nearest neighbor search capability.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-index-index.html#cfn-opensearchserverless-index-index-knn
            '''
            result = self._values.get("knn")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def knn_algo_param_ef_search(self) -> typing.Optional[jsii.Number]:
            '''The size of the dynamic list for the nearest neighbors.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-index-index.html#cfn-opensearchserverless-index-index-knnalgoparamefsearch
            '''
            result = self._values.get("knn_algo_param_ef_search")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def refresh_interval(self) -> typing.Optional[builtins.str]:
            '''How often to perform a refresh operation.

            For example, 1s or 5s.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-index-index.html#cfn-opensearchserverless-index-index-refreshinterval
            '''
            result = self._values.get("refresh_interval")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IndexProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchserverless.mixins.CfnIndexPropsMixin.IndexSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"index": "index"},
    )
    class IndexSettingsProperty:
        def __init__(
            self,
            *,
            index: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIndexPropsMixin.IndexProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Index settings for the OpenSearch Serverless index.

            :param index: Index settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-index-indexsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchserverless import mixins as opensearchserverless_mixins
                
                index_settings_property = opensearchserverless_mixins.CfnIndexPropsMixin.IndexSettingsProperty(
                    index=opensearchserverless_mixins.CfnIndexPropsMixin.IndexProperty(
                        knn=False,
                        knn_algo_param_ef_search=123,
                        refresh_interval="refreshInterval"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d230bacc640993fa1928eac5978442959c3e4c768030317fbdab284ef450beb)
                check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if index is not None:
                self._values["index"] = index

        @builtins.property
        def index(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.IndexProperty"]]:
            '''Index settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-index-indexsettings.html#cfn-opensearchserverless-index-indexsettings-index
            '''
            result = self._values.get("index")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.IndexProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IndexSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchserverless.mixins.CfnIndexPropsMixin.MappingsProperty",
        jsii_struct_bases=[],
        name_mapping={"properties": "properties"},
    )
    class MappingsProperty:
        def __init__(
            self,
            *,
            properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIndexPropsMixin.PropertyMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Index mappings for the OpenSearch Serverless index.

            :param properties: Nested fields within an object or nested field type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-index-mappings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchserverless import mixins as opensearchserverless_mixins
                
                # property_mapping_property_: opensearchserverless_mixins.CfnIndexPropsMixin.PropertyMappingProperty
                
                mappings_property = opensearchserverless_mixins.CfnIndexPropsMixin.MappingsProperty(
                    properties={
                        "properties_key": opensearchserverless_mixins.CfnIndexPropsMixin.PropertyMappingProperty(
                            dimension=123,
                            index=False,
                            method=opensearchserverless_mixins.CfnIndexPropsMixin.MethodProperty(
                                engine="engine",
                                name="name",
                                parameters=opensearchserverless_mixins.CfnIndexPropsMixin.ParametersProperty(
                                    ef_construction=123,
                                    m=123
                                ),
                                space_type="spaceType"
                            ),
                            properties={
                                "properties_key": property_mapping_property_
                            },
                            type="type",
                            value="value"
                        )
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bc8e3646025a2a03cf73de2b24efbb904d1d5845360cb0973a7fba25cc772760)
                check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if properties is not None:
                self._values["properties"] = properties

        @builtins.property
        def properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.PropertyMappingProperty"]]]]:
            '''Nested fields within an object or nested field type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-index-mappings.html#cfn-opensearchserverless-index-mappings-properties
            '''
            result = self._values.get("properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.PropertyMappingProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MappingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchserverless.mixins.CfnIndexPropsMixin.MethodProperty",
        jsii_struct_bases=[],
        name_mapping={
            "engine": "engine",
            "name": "name",
            "parameters": "parameters",
            "space_type": "spaceType",
        },
    )
    class MethodProperty:
        def __init__(
            self,
            *,
            engine: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIndexPropsMixin.ParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            space_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration for k-NN search method.

            :param engine: The k-NN search engine to use.
            :param name: The algorithm name for k-NN search.
            :param parameters: Additional parameters for the k-NN algorithm.
            :param space_type: The distance function used for k-NN search.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-index-method.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchserverless import mixins as opensearchserverless_mixins
                
                method_property = opensearchserverless_mixins.CfnIndexPropsMixin.MethodProperty(
                    engine="engine",
                    name="name",
                    parameters=opensearchserverless_mixins.CfnIndexPropsMixin.ParametersProperty(
                        ef_construction=123,
                        m=123
                    ),
                    space_type="spaceType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b7fad683bacfe59197547e80ab6b5b5a2bef2c3534f009aaa1f646c1ea4aa78e)
                check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument space_type", value=space_type, expected_type=type_hints["space_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if engine is not None:
                self._values["engine"] = engine
            if name is not None:
                self._values["name"] = name
            if parameters is not None:
                self._values["parameters"] = parameters
            if space_type is not None:
                self._values["space_type"] = space_type

        @builtins.property
        def engine(self) -> typing.Optional[builtins.str]:
            '''The k-NN search engine to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-index-method.html#cfn-opensearchserverless-index-method-engine
            '''
            result = self._values.get("engine")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The algorithm name for k-NN search.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-index-method.html#cfn-opensearchserverless-index-method-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.ParametersProperty"]]:
            '''Additional parameters for the k-NN algorithm.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-index-method.html#cfn-opensearchserverless-index-method-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.ParametersProperty"]], result)

        @builtins.property
        def space_type(self) -> typing.Optional[builtins.str]:
            '''The distance function used for k-NN search.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-index-method.html#cfn-opensearchserverless-index-method-spacetype
            '''
            result = self._values.get("space_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MethodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchserverless.mixins.CfnIndexPropsMixin.ParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"ef_construction": "efConstruction", "m": "m"},
    )
    class ParametersProperty:
        def __init__(
            self,
            *,
            ef_construction: typing.Optional[jsii.Number] = None,
            m: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Additional parameters for the k-NN algorithm.

            :param ef_construction: The size of the dynamic list used during k-NN graph creation.
            :param m: Number of neighbors to consider during k-NN search.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-index-parameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchserverless import mixins as opensearchserverless_mixins
                
                parameters_property = opensearchserverless_mixins.CfnIndexPropsMixin.ParametersProperty(
                    ef_construction=123,
                    m=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3fe484c459932b6000978814a08e8ad4af3c669699da94d3873fcaf734bcf6d3)
                check_type(argname="argument ef_construction", value=ef_construction, expected_type=type_hints["ef_construction"])
                check_type(argname="argument m", value=m, expected_type=type_hints["m"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ef_construction is not None:
                self._values["ef_construction"] = ef_construction
            if m is not None:
                self._values["m"] = m

        @builtins.property
        def ef_construction(self) -> typing.Optional[jsii.Number]:
            '''The size of the dynamic list used during k-NN graph creation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-index-parameters.html#cfn-opensearchserverless-index-parameters-efconstruction
            '''
            result = self._values.get("ef_construction")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def m(self) -> typing.Optional[jsii.Number]:
            '''Number of neighbors to consider during k-NN search.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-index-parameters.html#cfn-opensearchserverless-index-parameters-m
            '''
            result = self._values.get("m")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchserverless.mixins.CfnIndexPropsMixin.PropertyMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dimension": "dimension",
            "index": "index",
            "method": "method",
            "properties": "properties",
            "type": "type",
            "value": "value",
        },
    )
    class PropertyMappingProperty:
        def __init__(
            self,
            *,
            dimension: typing.Optional[jsii.Number] = None,
            index: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            method: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIndexPropsMixin.MethodProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIndexPropsMixin.PropertyMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Property mappings for the OpenSearch Serverless index.

            :param dimension: Dimension size for vector fields, defines the number of dimensions in the vector.
            :param index: Whether a field should be indexed.
            :param method: Configuration for k-NN search method.
            :param properties: Defines the fields within the mapping, including their types and configurations.
            :param type: The field data type. Must be a valid OpenSearch field type.
            :param value: Default value for the field when not specified in a document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-index-propertymapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchserverless import mixins as opensearchserverless_mixins
                
                # property_mapping_property_: opensearchserverless_mixins.CfnIndexPropsMixin.PropertyMappingProperty
                
                property_mapping_property = opensearchserverless_mixins.CfnIndexPropsMixin.PropertyMappingProperty(
                    dimension=123,
                    index=False,
                    method=opensearchserverless_mixins.CfnIndexPropsMixin.MethodProperty(
                        engine="engine",
                        name="name",
                        parameters=opensearchserverless_mixins.CfnIndexPropsMixin.ParametersProperty(
                            ef_construction=123,
                            m=123
                        ),
                        space_type="spaceType"
                    ),
                    properties={
                        "properties_key": property_mapping_property_
                    },
                    type="type",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__942738e992e0462f305b1ce54cfcbbcdb605d712dba3da9028c5ad329c47d5b9)
                check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
                check_type(argname="argument index", value=index, expected_type=type_hints["index"])
                check_type(argname="argument method", value=method, expected_type=type_hints["method"])
                check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimension is not None:
                self._values["dimension"] = dimension
            if index is not None:
                self._values["index"] = index
            if method is not None:
                self._values["method"] = method
            if properties is not None:
                self._values["properties"] = properties
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def dimension(self) -> typing.Optional[jsii.Number]:
            '''Dimension size for vector fields, defines the number of dimensions in the vector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-index-propertymapping.html#cfn-opensearchserverless-index-propertymapping-dimension
            '''
            result = self._values.get("dimension")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def index(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether a field should be indexed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-index-propertymapping.html#cfn-opensearchserverless-index-propertymapping-index
            '''
            result = self._values.get("index")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def method(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.MethodProperty"]]:
            '''Configuration for k-NN search method.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-index-propertymapping.html#cfn-opensearchserverless-index-propertymapping-method
            '''
            result = self._values.get("method")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.MethodProperty"]], result)

        @builtins.property
        def properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.PropertyMappingProperty"]]]]:
            '''Defines the fields within the mapping, including their types and configurations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-index-propertymapping.html#cfn-opensearchserverless-index-propertymapping-properties
            '''
            result = self._values.get("properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.PropertyMappingProperty"]]]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The field data type.

            Must be a valid OpenSearch field type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-index-propertymapping.html#cfn-opensearchserverless-index-propertymapping-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''Default value for the field when not specified in a document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-index-propertymapping.html#cfn-opensearchserverless-index-propertymapping-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertyMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_opensearchserverless.mixins.CfnLifecyclePolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "policy": "policy",
        "type": "type",
    },
)
class CfnLifecyclePolicyMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        policy: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnLifecyclePolicyPropsMixin.

        :param description: The description of the lifecycle policy.
        :param name: The name of the lifecycle policy.
        :param policy: The JSON policy document without any whitespaces.
        :param type: The type of lifecycle policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-lifecyclepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_opensearchserverless import mixins as opensearchserverless_mixins
            
            cfn_lifecycle_policy_mixin_props = opensearchserverless_mixins.CfnLifecyclePolicyMixinProps(
                description="description",
                name="name",
                policy="policy",
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__143a4a062690a109c9629549d6a626dbdbc33057bd0012190cf3199635d5dd30)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if policy is not None:
            self._values["policy"] = policy
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the lifecycle policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-lifecyclepolicy.html#cfn-opensearchserverless-lifecyclepolicy-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the lifecycle policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-lifecyclepolicy.html#cfn-opensearchserverless-lifecyclepolicy-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''The JSON policy document without any whitespaces.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-lifecyclepolicy.html#cfn-opensearchserverless-lifecyclepolicy-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of lifecycle policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-lifecyclepolicy.html#cfn-opensearchserverless-lifecyclepolicy-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_opensearchserverless.mixins.CfnLifecyclePolicyPropsMixin",
):
    '''Creates a lifecyle policy to be applied to OpenSearch Serverless indexes.

    Lifecycle policies define the number of days or hours to retain the data on an OpenSearch Serverless index. For more information, see `Creating data lifecycle policies <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-lifecycle.html#serverless-lifecycle-create>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-lifecyclepolicy.html
    :cloudformationResource: AWS::OpenSearchServerless::LifecyclePolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_opensearchserverless import mixins as opensearchserverless_mixins
        
        cfn_lifecycle_policy_props_mixin = opensearchserverless_mixins.CfnLifecyclePolicyPropsMixin(opensearchserverless_mixins.CfnLifecyclePolicyMixinProps(
            description="description",
            name="name",
            policy="policy",
            type="type"
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
        '''Create a mixin to apply properties to ``AWS::OpenSearchServerless::LifecyclePolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fb3aaf6a7a167c98e611594e35ee5b3a2a2b358f8c19fa8f720f27607ce66bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__004233f47817a132f37cebcead725fec5445c0220a8327e7ff0d1b655821f4f1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8467840c33c255e0569ce1aafe101d7b6e1d26f400f62b78b50aa360275a2ff3)
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
    jsii_type="@aws-cdk/mixins-preview.aws_opensearchserverless.mixins.CfnSecurityConfigMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "iam_federation_options": "iamFederationOptions",
        "iam_identity_center_options": "iamIdentityCenterOptions",
        "name": "name",
        "saml_options": "samlOptions",
        "type": "type",
    },
)
class CfnSecurityConfigMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        iam_federation_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSecurityConfigPropsMixin.IamFederationConfigOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        iam_identity_center_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSecurityConfigPropsMixin.IamIdentityCenterConfigOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        saml_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSecurityConfigPropsMixin.SamlConfigOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSecurityConfigPropsMixin.

        :param description: The description of the security configuration.
        :param iam_federation_options: Describes IAM federation options in the form of a key-value map. Contains configuration details about how OpenSearch Serverless integrates with external identity providers through federation.
        :param iam_identity_center_options: Describes IAM Identity Center options in the form of a key-value map.
        :param name: The name of the security configuration.
        :param saml_options: SAML options for the security configuration in the form of a key-value map.
        :param type: The type of security configuration. Currently the only option is ``saml`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securityconfig.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_opensearchserverless import mixins as opensearchserverless_mixins
            
            cfn_security_config_mixin_props = opensearchserverless_mixins.CfnSecurityConfigMixinProps(
                description="description",
                iam_federation_options=opensearchserverless_mixins.CfnSecurityConfigPropsMixin.IamFederationConfigOptionsProperty(
                    group_attribute="groupAttribute",
                    user_attribute="userAttribute"
                ),
                iam_identity_center_options=opensearchserverless_mixins.CfnSecurityConfigPropsMixin.IamIdentityCenterConfigOptionsProperty(
                    application_arn="applicationArn",
                    application_description="applicationDescription",
                    application_name="applicationName",
                    group_attribute="groupAttribute",
                    instance_arn="instanceArn",
                    user_attribute="userAttribute"
                ),
                name="name",
                saml_options=opensearchserverless_mixins.CfnSecurityConfigPropsMixin.SamlConfigOptionsProperty(
                    group_attribute="groupAttribute",
                    metadata="metadata",
                    open_search_serverless_entity_id="openSearchServerlessEntityId",
                    session_timeout=123,
                    user_attribute="userAttribute"
                ),
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b582e8dbb7d4cf2e015a2d70c19579f5387d304b5e6d5b6f4c2c0b90685e55a)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument iam_federation_options", value=iam_federation_options, expected_type=type_hints["iam_federation_options"])
            check_type(argname="argument iam_identity_center_options", value=iam_identity_center_options, expected_type=type_hints["iam_identity_center_options"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument saml_options", value=saml_options, expected_type=type_hints["saml_options"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if iam_federation_options is not None:
            self._values["iam_federation_options"] = iam_federation_options
        if iam_identity_center_options is not None:
            self._values["iam_identity_center_options"] = iam_identity_center_options
        if name is not None:
            self._values["name"] = name
        if saml_options is not None:
            self._values["saml_options"] = saml_options
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the security configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securityconfig.html#cfn-opensearchserverless-securityconfig-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam_federation_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityConfigPropsMixin.IamFederationConfigOptionsProperty"]]:
        '''Describes IAM federation options in the form of a key-value map.

        Contains configuration details about how OpenSearch Serverless integrates with external identity providers through federation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securityconfig.html#cfn-opensearchserverless-securityconfig-iamfederationoptions
        '''
        result = self._values.get("iam_federation_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityConfigPropsMixin.IamFederationConfigOptionsProperty"]], result)

    @builtins.property
    def iam_identity_center_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityConfigPropsMixin.IamIdentityCenterConfigOptionsProperty"]]:
        '''Describes IAM Identity Center options in the form of a key-value map.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securityconfig.html#cfn-opensearchserverless-securityconfig-iamidentitycenteroptions
        '''
        result = self._values.get("iam_identity_center_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityConfigPropsMixin.IamIdentityCenterConfigOptionsProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the security configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securityconfig.html#cfn-opensearchserverless-securityconfig-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def saml_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityConfigPropsMixin.SamlConfigOptionsProperty"]]:
        '''SAML options for the security configuration in the form of a key-value map.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securityconfig.html#cfn-opensearchserverless-securityconfig-samloptions
        '''
        result = self._values.get("saml_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityConfigPropsMixin.SamlConfigOptionsProperty"]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of security configuration.

        Currently the only option is ``saml`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securityconfig.html#cfn-opensearchserverless-securityconfig-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecurityConfigMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSecurityConfigPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_opensearchserverless.mixins.CfnSecurityConfigPropsMixin",
):
    '''Specifies a security configuration for OpenSearch Serverless.

    For more information, see `SAML authentication for Amazon OpenSearch Serverless <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-saml.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securityconfig.html
    :cloudformationResource: AWS::OpenSearchServerless::SecurityConfig
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_opensearchserverless import mixins as opensearchserverless_mixins
        
        cfn_security_config_props_mixin = opensearchserverless_mixins.CfnSecurityConfigPropsMixin(opensearchserverless_mixins.CfnSecurityConfigMixinProps(
            description="description",
            iam_federation_options=opensearchserverless_mixins.CfnSecurityConfigPropsMixin.IamFederationConfigOptionsProperty(
                group_attribute="groupAttribute",
                user_attribute="userAttribute"
            ),
            iam_identity_center_options=opensearchserverless_mixins.CfnSecurityConfigPropsMixin.IamIdentityCenterConfigOptionsProperty(
                application_arn="applicationArn",
                application_description="applicationDescription",
                application_name="applicationName",
                group_attribute="groupAttribute",
                instance_arn="instanceArn",
                user_attribute="userAttribute"
            ),
            name="name",
            saml_options=opensearchserverless_mixins.CfnSecurityConfigPropsMixin.SamlConfigOptionsProperty(
                group_attribute="groupAttribute",
                metadata="metadata",
                open_search_serverless_entity_id="openSearchServerlessEntityId",
                session_timeout=123,
                user_attribute="userAttribute"
            ),
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSecurityConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::OpenSearchServerless::SecurityConfig``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a83d1513b33597e361e008d707342bb866788743ecf82c028d6f89046fa947f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b47eeb118fc7ce89116fe5aa4441242913fe9fa7411b48e38c7b4ecc0939e285)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c6e3d896091452bdf28cba540d290e94875c2f086cc466f33c01a44f387f80e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSecurityConfigMixinProps:
        return typing.cast(CfnSecurityConfigMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchserverless.mixins.CfnSecurityConfigPropsMixin.IamFederationConfigOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "group_attribute": "groupAttribute",
            "user_attribute": "userAttribute",
        },
    )
    class IamFederationConfigOptionsProperty:
        def __init__(
            self,
            *,
            group_attribute: typing.Optional[builtins.str] = None,
            user_attribute: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes IAM federation options for an OpenSearch Serverless security configuration in the form of a key-value map.

            These options define how OpenSearch Serverless integrates with external identity providers using federation.

            :param group_attribute: The group attribute for this IAM federation integration. This attribute is used to map identity provider groups to OpenSearch Serverless permissions.
            :param user_attribute: The user attribute for this IAM federation integration. This attribute is used to identify users in the federated authentication process.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-securityconfig-iamfederationconfigoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchserverless import mixins as opensearchserverless_mixins
                
                iam_federation_config_options_property = opensearchserverless_mixins.CfnSecurityConfigPropsMixin.IamFederationConfigOptionsProperty(
                    group_attribute="groupAttribute",
                    user_attribute="userAttribute"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bd09d03553acce74dadaae73973bf883704b93df1a2cb7baae812c36b67913dd)
                check_type(argname="argument group_attribute", value=group_attribute, expected_type=type_hints["group_attribute"])
                check_type(argname="argument user_attribute", value=user_attribute, expected_type=type_hints["user_attribute"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group_attribute is not None:
                self._values["group_attribute"] = group_attribute
            if user_attribute is not None:
                self._values["user_attribute"] = user_attribute

        @builtins.property
        def group_attribute(self) -> typing.Optional[builtins.str]:
            '''The group attribute for this IAM federation integration.

            This attribute is used to map identity provider groups to OpenSearch Serverless permissions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-securityconfig-iamfederationconfigoptions.html#cfn-opensearchserverless-securityconfig-iamfederationconfigoptions-groupattribute
            '''
            result = self._values.get("group_attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_attribute(self) -> typing.Optional[builtins.str]:
            '''The user attribute for this IAM federation integration.

            This attribute is used to identify users in the federated authentication process.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-securityconfig-iamfederationconfigoptions.html#cfn-opensearchserverless-securityconfig-iamfederationconfigoptions-userattribute
            '''
            result = self._values.get("user_attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IamFederationConfigOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchserverless.mixins.CfnSecurityConfigPropsMixin.IamIdentityCenterConfigOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_arn": "applicationArn",
            "application_description": "applicationDescription",
            "application_name": "applicationName",
            "group_attribute": "groupAttribute",
            "instance_arn": "instanceArn",
            "user_attribute": "userAttribute",
        },
    )
    class IamIdentityCenterConfigOptionsProperty:
        def __init__(
            self,
            *,
            application_arn: typing.Optional[builtins.str] = None,
            application_description: typing.Optional[builtins.str] = None,
            application_name: typing.Optional[builtins.str] = None,
            group_attribute: typing.Optional[builtins.str] = None,
            instance_arn: typing.Optional[builtins.str] = None,
            user_attribute: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes IAM Identity Center options for an OpenSearch Serverless security configuration in the form of a key-value map.

            :param application_arn: The ARN of the IAM Identity Center application used to integrate with OpenSearch Serverless.
            :param application_description: The description of the IAM Identity Center application used to integrate with OpenSearch Serverless.
            :param application_name: The name of the IAM Identity Center application used to integrate with OpenSearch Serverless.
            :param group_attribute: The group attribute for this IAM Identity Center integration. Defaults to ``GroupId`` .
            :param instance_arn: The ARN of the IAM Identity Center instance used to integrate with OpenSearch Serverless.
            :param user_attribute: The user attribute for this IAM Identity Center integration. Defaults to ``UserId``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-securityconfig-iamidentitycenterconfigoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchserverless import mixins as opensearchserverless_mixins
                
                iam_identity_center_config_options_property = opensearchserverless_mixins.CfnSecurityConfigPropsMixin.IamIdentityCenterConfigOptionsProperty(
                    application_arn="applicationArn",
                    application_description="applicationDescription",
                    application_name="applicationName",
                    group_attribute="groupAttribute",
                    instance_arn="instanceArn",
                    user_attribute="userAttribute"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__303743bb0d86fafe3fd6f8f3a533a8dd7e6877f36fc3666a6a50f4b3032b6595)
                check_type(argname="argument application_arn", value=application_arn, expected_type=type_hints["application_arn"])
                check_type(argname="argument application_description", value=application_description, expected_type=type_hints["application_description"])
                check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
                check_type(argname="argument group_attribute", value=group_attribute, expected_type=type_hints["group_attribute"])
                check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
                check_type(argname="argument user_attribute", value=user_attribute, expected_type=type_hints["user_attribute"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_arn is not None:
                self._values["application_arn"] = application_arn
            if application_description is not None:
                self._values["application_description"] = application_description
            if application_name is not None:
                self._values["application_name"] = application_name
            if group_attribute is not None:
                self._values["group_attribute"] = group_attribute
            if instance_arn is not None:
                self._values["instance_arn"] = instance_arn
            if user_attribute is not None:
                self._values["user_attribute"] = user_attribute

        @builtins.property
        def application_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM Identity Center application used to integrate with OpenSearch Serverless.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-securityconfig-iamidentitycenterconfigoptions.html#cfn-opensearchserverless-securityconfig-iamidentitycenterconfigoptions-applicationarn
            '''
            result = self._values.get("application_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def application_description(self) -> typing.Optional[builtins.str]:
            '''The description of the IAM Identity Center application used to integrate with OpenSearch Serverless.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-securityconfig-iamidentitycenterconfigoptions.html#cfn-opensearchserverless-securityconfig-iamidentitycenterconfigoptions-applicationdescription
            '''
            result = self._values.get("application_description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def application_name(self) -> typing.Optional[builtins.str]:
            '''The name of the IAM Identity Center application used to integrate with OpenSearch Serverless.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-securityconfig-iamidentitycenterconfigoptions.html#cfn-opensearchserverless-securityconfig-iamidentitycenterconfigoptions-applicationname
            '''
            result = self._values.get("application_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def group_attribute(self) -> typing.Optional[builtins.str]:
            '''The group attribute for this IAM Identity Center integration.

            Defaults to ``GroupId`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-securityconfig-iamidentitycenterconfigoptions.html#cfn-opensearchserverless-securityconfig-iamidentitycenterconfigoptions-groupattribute
            '''
            result = self._values.get("group_attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM Identity Center instance used to integrate with OpenSearch Serverless.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-securityconfig-iamidentitycenterconfigoptions.html#cfn-opensearchserverless-securityconfig-iamidentitycenterconfigoptions-instancearn
            '''
            result = self._values.get("instance_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_attribute(self) -> typing.Optional[builtins.str]:
            '''The user attribute for this IAM Identity Center integration.

            Defaults to ``UserId``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-securityconfig-iamidentitycenterconfigoptions.html#cfn-opensearchserverless-securityconfig-iamidentitycenterconfigoptions-userattribute
            '''
            result = self._values.get("user_attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IamIdentityCenterConfigOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchserverless.mixins.CfnSecurityConfigPropsMixin.SamlConfigOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "group_attribute": "groupAttribute",
            "metadata": "metadata",
            "open_search_serverless_entity_id": "openSearchServerlessEntityId",
            "session_timeout": "sessionTimeout",
            "user_attribute": "userAttribute",
        },
    )
    class SamlConfigOptionsProperty:
        def __init__(
            self,
            *,
            group_attribute: typing.Optional[builtins.str] = None,
            metadata: typing.Optional[builtins.str] = None,
            open_search_serverless_entity_id: typing.Optional[builtins.str] = None,
            session_timeout: typing.Optional[jsii.Number] = None,
            user_attribute: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes SAML options for an OpenSearch Serverless security configuration in the form of a key-value map.

            :param group_attribute: The group attribute for this SAML integration.
            :param metadata: The XML IdP metadata file generated from your identity provider.
            :param open_search_serverless_entity_id: Custom entity ID attribute to override the default entity ID for this SAML integration.
            :param session_timeout: The session timeout, in minutes. Default is 60 minutes (12 hours).
            :param user_attribute: A user attribute for this SAML integration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-securityconfig-samlconfigoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchserverless import mixins as opensearchserverless_mixins
                
                saml_config_options_property = opensearchserverless_mixins.CfnSecurityConfigPropsMixin.SamlConfigOptionsProperty(
                    group_attribute="groupAttribute",
                    metadata="metadata",
                    open_search_serverless_entity_id="openSearchServerlessEntityId",
                    session_timeout=123,
                    user_attribute="userAttribute"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1573adfad9fa5297076f73cad51aaf9a107f407faa9d4dd68cecba67cb9fda9f)
                check_type(argname="argument group_attribute", value=group_attribute, expected_type=type_hints["group_attribute"])
                check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
                check_type(argname="argument open_search_serverless_entity_id", value=open_search_serverless_entity_id, expected_type=type_hints["open_search_serverless_entity_id"])
                check_type(argname="argument session_timeout", value=session_timeout, expected_type=type_hints["session_timeout"])
                check_type(argname="argument user_attribute", value=user_attribute, expected_type=type_hints["user_attribute"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group_attribute is not None:
                self._values["group_attribute"] = group_attribute
            if metadata is not None:
                self._values["metadata"] = metadata
            if open_search_serverless_entity_id is not None:
                self._values["open_search_serverless_entity_id"] = open_search_serverless_entity_id
            if session_timeout is not None:
                self._values["session_timeout"] = session_timeout
            if user_attribute is not None:
                self._values["user_attribute"] = user_attribute

        @builtins.property
        def group_attribute(self) -> typing.Optional[builtins.str]:
            '''The group attribute for this SAML integration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-securityconfig-samlconfigoptions.html#cfn-opensearchserverless-securityconfig-samlconfigoptions-groupattribute
            '''
            result = self._values.get("group_attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metadata(self) -> typing.Optional[builtins.str]:
            '''The XML IdP metadata file generated from your identity provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-securityconfig-samlconfigoptions.html#cfn-opensearchserverless-securityconfig-samlconfigoptions-metadata
            '''
            result = self._values.get("metadata")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def open_search_serverless_entity_id(self) -> typing.Optional[builtins.str]:
            '''Custom entity ID attribute to override the default entity ID for this SAML integration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-securityconfig-samlconfigoptions.html#cfn-opensearchserverless-securityconfig-samlconfigoptions-opensearchserverlessentityid
            '''
            result = self._values.get("open_search_serverless_entity_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def session_timeout(self) -> typing.Optional[jsii.Number]:
            '''The session timeout, in minutes.

            Default is 60 minutes (12 hours).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-securityconfig-samlconfigoptions.html#cfn-opensearchserverless-securityconfig-samlconfigoptions-sessiontimeout
            '''
            result = self._values.get("session_timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def user_attribute(self) -> typing.Optional[builtins.str]:
            '''A user attribute for this SAML integration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-securityconfig-samlconfigoptions.html#cfn-opensearchserverless-securityconfig-samlconfigoptions-userattribute
            '''
            result = self._values.get("user_attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SamlConfigOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_opensearchserverless.mixins.CfnSecurityPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "policy": "policy",
        "type": "type",
    },
)
class CfnSecurityPolicyMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        policy: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSecurityPolicyPropsMixin.

        :param description: The description of the security policy.
        :param name: The name of the policy.
        :param policy: The JSON policy document without any whitespaces.
        :param type: The type of security policy. Can be either ``encryption`` or ``network`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securitypolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_opensearchserverless import mixins as opensearchserverless_mixins
            
            cfn_security_policy_mixin_props = opensearchserverless_mixins.CfnSecurityPolicyMixinProps(
                description="description",
                name="name",
                policy="policy",
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e91c9af4e9b2253b94b3822382231dfa2c2db49f7b6b45d66020957ee8e017e)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if policy is not None:
            self._values["policy"] = policy
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the security policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securitypolicy.html#cfn-opensearchserverless-securitypolicy-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securitypolicy.html#cfn-opensearchserverless-securitypolicy-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''The JSON policy document without any whitespaces.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securitypolicy.html#cfn-opensearchserverless-securitypolicy-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of security policy.

        Can be either ``encryption`` or ``network`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securitypolicy.html#cfn-opensearchserverless-securitypolicy-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecurityPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSecurityPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_opensearchserverless.mixins.CfnSecurityPolicyPropsMixin",
):
    '''Creates an encryption or network policy to be used by one or more OpenSearch Serverless collections.

    Network policies specify access to a collection and its OpenSearch Dashboards endpoint from public networks or specific VPC endpoints. For more information, see `Network access for Amazon OpenSearch Serverless <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-network.html>`_ .

    Encryption policies specify a KMS encryption key to assign to particular collections. For more information, see `Encryption at rest for Amazon OpenSearch Serverless <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-encryption.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securitypolicy.html
    :cloudformationResource: AWS::OpenSearchServerless::SecurityPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_opensearchserverless import mixins as opensearchserverless_mixins
        
        cfn_security_policy_props_mixin = opensearchserverless_mixins.CfnSecurityPolicyPropsMixin(opensearchserverless_mixins.CfnSecurityPolicyMixinProps(
            description="description",
            name="name",
            policy="policy",
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSecurityPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::OpenSearchServerless::SecurityPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30542645f61a8b8adc4a9345effd1bfcf60dfa939f94728bf76a1525a33f4755)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5530d71939acb3939019ca861b9217dd905ce01170583bee77c66247e00e0f10)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fbc0159000416adf113113c568e39640a8c117ff0b2dee36b6d86a2c5554b39)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSecurityPolicyMixinProps:
        return typing.cast(CfnSecurityPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_opensearchserverless.mixins.CfnVpcEndpointMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "security_group_ids": "securityGroupIds",
        "subnet_ids": "subnetIds",
        "vpc_id": "vpcId",
    },
)
class CfnVpcEndpointMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnVpcEndpointPropsMixin.

        :param name: The name of the endpoint.
        :param security_group_ids: The unique identifiers of the security groups that define the ports, protocols, and sources for inbound traffic that you are authorizing into your endpoint.
        :param subnet_ids: The ID of the subnets from which you access OpenSearch Serverless.
        :param vpc_id: The ID of the VPC from which you access OpenSearch Serverless.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-vpcendpoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_opensearchserverless import mixins as opensearchserverless_mixins
            
            cfn_vpc_endpoint_mixin_props = opensearchserverless_mixins.CfnVpcEndpointMixinProps(
                name="name",
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"],
                vpc_id="vpcId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2b2c89d9f7e325897442d35223858b8f0bff56e1f0b6b3fd8835055503bf928)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-vpcendpoint.html#cfn-opensearchserverless-vpcendpoint-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The unique identifiers of the security groups that define the ports, protocols, and sources for inbound traffic that you are authorizing into your endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-vpcendpoint.html#cfn-opensearchserverless-vpcendpoint-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ID of the subnets from which you access OpenSearch Serverless.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-vpcendpoint.html#cfn-opensearchserverless-vpcendpoint-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the VPC from which you access OpenSearch Serverless.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-vpcendpoint.html#cfn-opensearchserverless-vpcendpoint-vpcid
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVpcEndpointMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVpcEndpointPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_opensearchserverless.mixins.CfnVpcEndpointPropsMixin",
):
    '''Creates an OpenSearch Serverless-managed interface VPC endpoint.

    For more information, see `Access Amazon OpenSearch Serverless using an interface endpoint <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-vpc.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-vpcendpoint.html
    :cloudformationResource: AWS::OpenSearchServerless::VpcEndpoint
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_opensearchserverless import mixins as opensearchserverless_mixins
        
        cfn_vpc_endpoint_props_mixin = opensearchserverless_mixins.CfnVpcEndpointPropsMixin(opensearchserverless_mixins.CfnVpcEndpointMixinProps(
            name="name",
            security_group_ids=["securityGroupIds"],
            subnet_ids=["subnetIds"],
            vpc_id="vpcId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVpcEndpointMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::OpenSearchServerless::VpcEndpoint``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__509f6ba5d0822fe50610b0d2e831b1dcb04f40a45acfc961805aa1a3139db14a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52086b4b414df6146118127699928ded91f3bb5bf0b04bc3c71c655ab8d9f0c1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63fdce769dd38711fc1be72ec53b57dee05e0d3ba8c6d748bef329bfa7a6b421)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVpcEndpointMixinProps:
        return typing.cast(CfnVpcEndpointMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnAccessPolicyMixinProps",
    "CfnAccessPolicyPropsMixin",
    "CfnCollectionMixinProps",
    "CfnCollectionPropsMixin",
    "CfnIndexMixinProps",
    "CfnIndexPropsMixin",
    "CfnLifecyclePolicyMixinProps",
    "CfnLifecyclePolicyPropsMixin",
    "CfnSecurityConfigMixinProps",
    "CfnSecurityConfigPropsMixin",
    "CfnSecurityPolicyMixinProps",
    "CfnSecurityPolicyPropsMixin",
    "CfnVpcEndpointMixinProps",
    "CfnVpcEndpointPropsMixin",
]

publication.publish()

def _typecheckingstub__93d12bd44b608e9267911c08fd1a35a5c86f9003f3911695cd4c63dd17e12426(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    policy: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c5a0d0cf5e4343046d4b7a63c83104044c74e3a25663b82a35284f78aaf7b3(
    props: typing.Union[CfnAccessPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bd0e0fdfd17f0f2869c42bcc87c3518c2f280e823edb04e15859557193b1924(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2169b4b30791db85fcd488bc98d73f015efce19a634fe597c1d55026404ca429(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9ee5cdd7ff9c40c1b8e5207d6677cbcccf56774c726b3c4fc1dbc0ef43ccc3f(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    standby_replicas: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d475a66dbd228fe5f772eebabc0027b864856187441d1e7d10e74644a4955bd(
    props: typing.Union[CfnCollectionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87ffcf29ae0e266154f7b6db030603a6d96b03bc1f0d9a5fcea4b70a6bd93b53(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cca9691f5c869d378681d852e79ceda75d4d3e1a6b92e3108818992cc21bd53b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebb4d974a179550968f1795693ab1a717d3e039a452e080c0c6d2b5246df867d(
    *,
    collection_endpoint: typing.Optional[builtins.str] = None,
    index_name: typing.Optional[builtins.str] = None,
    mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIndexPropsMixin.MappingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIndexPropsMixin.IndexSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__678269ad135eaec0e7e14072ad13728801b94bed85c928a0c4b6de9a4b291fa9(
    props: typing.Union[CfnIndexMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f44ed0254e1153473d18bd41860d1dbf38cccc64d7618cc320f2ffca6558d48(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee3c40d974cc2677a143cf6401ccdfb7dfd9bd1eabc601d013e0eb897132ad0e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__160ea4bdea5dc52d76ed64853499827cdccf231d049aba4c1f617689207b46b8(
    *,
    knn: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    knn_algo_param_ef_search: typing.Optional[jsii.Number] = None,
    refresh_interval: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d230bacc640993fa1928eac5978442959c3e4c768030317fbdab284ef450beb(
    *,
    index: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIndexPropsMixin.IndexProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc8e3646025a2a03cf73de2b24efbb904d1d5845360cb0973a7fba25cc772760(
    *,
    properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIndexPropsMixin.PropertyMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7fad683bacfe59197547e80ab6b5b5a2bef2c3534f009aaa1f646c1ea4aa78e(
    *,
    engine: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIndexPropsMixin.ParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    space_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe484c459932b6000978814a08e8ad4af3c669699da94d3873fcaf734bcf6d3(
    *,
    ef_construction: typing.Optional[jsii.Number] = None,
    m: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__942738e992e0462f305b1ce54cfcbbcdb605d712dba3da9028c5ad329c47d5b9(
    *,
    dimension: typing.Optional[jsii.Number] = None,
    index: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    method: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIndexPropsMixin.MethodProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIndexPropsMixin.PropertyMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__143a4a062690a109c9629549d6a626dbdbc33057bd0012190cf3199635d5dd30(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    policy: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb3aaf6a7a167c98e611594e35ee5b3a2a2b358f8c19fa8f720f27607ce66bb(
    props: typing.Union[CfnLifecyclePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__004233f47817a132f37cebcead725fec5445c0220a8327e7ff0d1b655821f4f1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8467840c33c255e0569ce1aafe101d7b6e1d26f400f62b78b50aa360275a2ff3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b582e8dbb7d4cf2e015a2d70c19579f5387d304b5e6d5b6f4c2c0b90685e55a(
    *,
    description: typing.Optional[builtins.str] = None,
    iam_federation_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSecurityConfigPropsMixin.IamFederationConfigOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    iam_identity_center_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSecurityConfigPropsMixin.IamIdentityCenterConfigOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    saml_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSecurityConfigPropsMixin.SamlConfigOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a83d1513b33597e361e008d707342bb866788743ecf82c028d6f89046fa947f4(
    props: typing.Union[CfnSecurityConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b47eeb118fc7ce89116fe5aa4441242913fe9fa7411b48e38c7b4ecc0939e285(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6e3d896091452bdf28cba540d290e94875c2f086cc466f33c01a44f387f80e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd09d03553acce74dadaae73973bf883704b93df1a2cb7baae812c36b67913dd(
    *,
    group_attribute: typing.Optional[builtins.str] = None,
    user_attribute: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__303743bb0d86fafe3fd6f8f3a533a8dd7e6877f36fc3666a6a50f4b3032b6595(
    *,
    application_arn: typing.Optional[builtins.str] = None,
    application_description: typing.Optional[builtins.str] = None,
    application_name: typing.Optional[builtins.str] = None,
    group_attribute: typing.Optional[builtins.str] = None,
    instance_arn: typing.Optional[builtins.str] = None,
    user_attribute: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1573adfad9fa5297076f73cad51aaf9a107f407faa9d4dd68cecba67cb9fda9f(
    *,
    group_attribute: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[builtins.str] = None,
    open_search_serverless_entity_id: typing.Optional[builtins.str] = None,
    session_timeout: typing.Optional[jsii.Number] = None,
    user_attribute: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e91c9af4e9b2253b94b3822382231dfa2c2db49f7b6b45d66020957ee8e017e(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    policy: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30542645f61a8b8adc4a9345effd1bfcf60dfa939f94728bf76a1525a33f4755(
    props: typing.Union[CfnSecurityPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5530d71939acb3939019ca861b9217dd905ce01170583bee77c66247e00e0f10(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fbc0159000416adf113113c568e39640a8c117ff0b2dee36b6d86a2c5554b39(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2b2c89d9f7e325897442d35223858b8f0bff56e1f0b6b3fd8835055503bf928(
    *,
    name: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__509f6ba5d0822fe50610b0d2e831b1dcb04f40a45acfc961805aa1a3139db14a(
    props: typing.Union[CfnVpcEndpointMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52086b4b414df6146118127699928ded91f3bb5bf0b04bc3c71c655ab8d9f0c1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63fdce769dd38711fc1be72ec53b57dee05e0d3ba8c6d748bef329bfa7a6b421(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
