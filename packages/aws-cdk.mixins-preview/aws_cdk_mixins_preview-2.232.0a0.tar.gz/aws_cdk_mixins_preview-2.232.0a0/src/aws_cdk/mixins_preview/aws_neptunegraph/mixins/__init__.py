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
    jsii_type="@aws-cdk/mixins-preview.aws_neptunegraph.mixins.CfnGraphMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "deletion_protection": "deletionProtection",
        "graph_name": "graphName",
        "provisioned_memory": "provisionedMemory",
        "public_connectivity": "publicConnectivity",
        "replica_count": "replicaCount",
        "tags": "tags",
        "vector_search_configuration": "vectorSearchConfiguration",
    },
)
class CfnGraphMixinProps:
    def __init__(
        self,
        *,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        graph_name: typing.Optional[builtins.str] = None,
        provisioned_memory: typing.Optional[jsii.Number] = None,
        public_connectivity: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        replica_count: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vector_search_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGraphPropsMixin.VectorSearchConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnGraphPropsMixin.

        :param deletion_protection: A value that indicates whether the graph has deletion protection enabled. The graph can't be deleted when deletion protection is enabled.
        :param graph_name: The graph name. For example: ``my-graph-1`` . The name must contain from 1 to 63 letters, numbers, or hyphens, and its first character must be a letter. It cannot end with a hyphen or contain two consecutive hyphens. If you don't specify a graph name, a unique graph name is generated for you using the prefix ``graph-for`` , followed by a combination of ``Stack Name`` and a ``UUID`` .
        :param provisioned_memory: The provisioned memory-optimized Neptune Capacity Units (m-NCUs) to use for the graph. Min = 16
        :param public_connectivity: Specifies whether or not the graph can be reachable over the internet. All access to graphs is IAM authenticated. When the graph is publicly available, its domain name system (DNS) endpoint resolves to the public IP address from the internet. When the graph isn't publicly available, you need to create a ``PrivateGraphEndpoint`` in a given VPC to ensure the DNS name resolves to a private IP address that is reachable from the VPC. Default: If not specified, the default value is false. .. epigraph:: If enabling public connectivity for the first time, there will be a delay while it is enabled.
        :param replica_count: The number of replicas in other AZs. Default: If not specified, the default value is 1.
        :param tags: Adds metadata tags to the new graph. These tags can also be used with cost allocation reporting, or used in a Condition statement in an IAM policy.
        :param vector_search_configuration: Specifies the number of dimensions for vector embeddings that will be loaded into the graph. The value is specified as ``dimension=`` value. Max = 65,535

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptunegraph-graph.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_neptunegraph import mixins as neptunegraph_mixins
            
            cfn_graph_mixin_props = neptunegraph_mixins.CfnGraphMixinProps(
                deletion_protection=False,
                graph_name="graphName",
                provisioned_memory=123,
                public_connectivity=False,
                replica_count=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vector_search_configuration=neptunegraph_mixins.CfnGraphPropsMixin.VectorSearchConfigurationProperty(
                    vector_search_dimension=123
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38f6c6f6ce2eb604dfc074a4728d38df29c9fd88e897b5bab687ff10f82b9916)
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument graph_name", value=graph_name, expected_type=type_hints["graph_name"])
            check_type(argname="argument provisioned_memory", value=provisioned_memory, expected_type=type_hints["provisioned_memory"])
            check_type(argname="argument public_connectivity", value=public_connectivity, expected_type=type_hints["public_connectivity"])
            check_type(argname="argument replica_count", value=replica_count, expected_type=type_hints["replica_count"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vector_search_configuration", value=vector_search_configuration, expected_type=type_hints["vector_search_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if graph_name is not None:
            self._values["graph_name"] = graph_name
        if provisioned_memory is not None:
            self._values["provisioned_memory"] = provisioned_memory
        if public_connectivity is not None:
            self._values["public_connectivity"] = public_connectivity
        if replica_count is not None:
            self._values["replica_count"] = replica_count
        if tags is not None:
            self._values["tags"] = tags
        if vector_search_configuration is not None:
            self._values["vector_search_configuration"] = vector_search_configuration

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A value that indicates whether the graph has deletion protection enabled.

        The graph can't be deleted when deletion protection is enabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptunegraph-graph.html#cfn-neptunegraph-graph-deletionprotection
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def graph_name(self) -> typing.Optional[builtins.str]:
        '''The graph name. For example: ``my-graph-1`` .

        The name must contain from 1 to 63 letters, numbers, or hyphens, and its first character must be a letter. It cannot end with a hyphen or contain two consecutive hyphens.

        If you don't specify a graph name, a unique graph name is generated for you using the prefix ``graph-for`` , followed by a combination of ``Stack Name`` and a ``UUID`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptunegraph-graph.html#cfn-neptunegraph-graph-graphname
        '''
        result = self._values.get("graph_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioned_memory(self) -> typing.Optional[jsii.Number]:
        '''The provisioned memory-optimized Neptune Capacity Units (m-NCUs) to use for the graph.

        Min = 16

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptunegraph-graph.html#cfn-neptunegraph-graph-provisionedmemory
        '''
        result = self._values.get("provisioned_memory")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def public_connectivity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether or not the graph can be reachable over the internet. All access to graphs is IAM authenticated.

        When the graph is publicly available, its domain name system (DNS) endpoint resolves to the public IP address from the internet. When the graph isn't publicly available, you need to create a ``PrivateGraphEndpoint`` in a given VPC to ensure the DNS name resolves to a private IP address that is reachable from the VPC.

        Default: If not specified, the default value is false.
        .. epigraph::

           If enabling public connectivity for the first time, there will be a delay while it is enabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptunegraph-graph.html#cfn-neptunegraph-graph-publicconnectivity
        '''
        result = self._values.get("public_connectivity")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def replica_count(self) -> typing.Optional[jsii.Number]:
        '''The number of replicas in other AZs.

        Default: If not specified, the default value is 1.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptunegraph-graph.html#cfn-neptunegraph-graph-replicacount
        '''
        result = self._values.get("replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Adds metadata tags to the new graph.

        These tags can also be used with cost allocation reporting, or used in a Condition statement in an IAM policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptunegraph-graph.html#cfn-neptunegraph-graph-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vector_search_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGraphPropsMixin.VectorSearchConfigurationProperty"]]:
        '''Specifies the number of dimensions for vector embeddings that will be loaded into the graph.

        The value is specified as ``dimension=`` value. Max = 65,535

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptunegraph-graph.html#cfn-neptunegraph-graph-vectorsearchconfiguration
        '''
        result = self._values.get("vector_search_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGraphPropsMixin.VectorSearchConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGraphMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGraphPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_neptunegraph.mixins.CfnGraphPropsMixin",
):
    '''The ``AWS ::NeptuneGraph::Graph`` resource creates an  graph.

    is a memory-optimized graph database engine for analytics. For more information, see ` <https://docs.aws.amazon.com/neptune-analytics/latest/userguide/what-is-neptune-analytics.html>`_ .

    You can use ``AWS ::NeptuneGraph::Graph.DeletionProtection`` to help guard against unintended deletion of your graph.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptunegraph-graph.html
    :cloudformationResource: AWS::NeptuneGraph::Graph
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_neptunegraph import mixins as neptunegraph_mixins
        
        cfn_graph_props_mixin = neptunegraph_mixins.CfnGraphPropsMixin(neptunegraph_mixins.CfnGraphMixinProps(
            deletion_protection=False,
            graph_name="graphName",
            provisioned_memory=123,
            public_connectivity=False,
            replica_count=123,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vector_search_configuration=neptunegraph_mixins.CfnGraphPropsMixin.VectorSearchConfigurationProperty(
                vector_search_dimension=123
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnGraphMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NeptuneGraph::Graph``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0733df3988cfa1f76a376f9bac31e5472d72da6b2ef5b3d710d4a589e545a51b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cea8af1505d05457552a381b391bec5706ae89b3f91531775562ee38aaba863)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c29cda85bfb8b81bd56c54c9e0a208ca0aa518203145b8499e659afcd4e611f1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGraphMixinProps:
        return typing.cast(CfnGraphMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_neptunegraph.mixins.CfnGraphPropsMixin.VectorSearchConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"vector_search_dimension": "vectorSearchDimension"},
    )
    class VectorSearchConfigurationProperty:
        def __init__(
            self,
            *,
            vector_search_dimension: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The vector-search configuration for the graph, which specifies the vector dimension to use in the vector index, if any.

            :param vector_search_dimension: The number of dimensions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-neptunegraph-graph-vectorsearchconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_neptunegraph import mixins as neptunegraph_mixins
                
                vector_search_configuration_property = neptunegraph_mixins.CfnGraphPropsMixin.VectorSearchConfigurationProperty(
                    vector_search_dimension=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d23e72a124b0affebe1ce34a860bc3bc8b94971ef2bdc44d5ee29fe191c96c13)
                check_type(argname="argument vector_search_dimension", value=vector_search_dimension, expected_type=type_hints["vector_search_dimension"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if vector_search_dimension is not None:
                self._values["vector_search_dimension"] = vector_search_dimension

        @builtins.property
        def vector_search_dimension(self) -> typing.Optional[jsii.Number]:
            '''The number of dimensions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-neptunegraph-graph-vectorsearchconfiguration.html#cfn-neptunegraph-graph-vectorsearchconfiguration-vectorsearchdimension
            '''
            result = self._values.get("vector_search_dimension")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VectorSearchConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_neptunegraph.mixins.CfnPrivateGraphEndpointMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "graph_identifier": "graphIdentifier",
        "security_group_ids": "securityGroupIds",
        "subnet_ids": "subnetIds",
        "vpc_id": "vpcId",
    },
)
class CfnPrivateGraphEndpointMixinProps:
    def __init__(
        self,
        *,
        graph_identifier: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPrivateGraphEndpointPropsMixin.

        :param graph_identifier: The unique identifier of the Neptune Analytics graph.
        :param security_group_ids: Security groups to be attached to the private graph endpoint..
        :param subnet_ids: Subnets in which private graph endpoint ENIs are created.
        :param vpc_id: The VPC in which the private graph endpoint needs to be created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptunegraph-privategraphendpoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_neptunegraph import mixins as neptunegraph_mixins
            
            cfn_private_graph_endpoint_mixin_props = neptunegraph_mixins.CfnPrivateGraphEndpointMixinProps(
                graph_identifier="graphIdentifier",
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"],
                vpc_id="vpcId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f22f099182e8d7b0f4f0bd921c553e0e9a2ce89ff63f0cd711e2324001463f2)
            check_type(argname="argument graph_identifier", value=graph_identifier, expected_type=type_hints["graph_identifier"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if graph_identifier is not None:
            self._values["graph_identifier"] = graph_identifier
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def graph_identifier(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the Neptune Analytics graph.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptunegraph-privategraphendpoint.html#cfn-neptunegraph-privategraphendpoint-graphidentifier
        '''
        result = self._values.get("graph_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Security groups to be attached to the private graph endpoint..

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptunegraph-privategraphendpoint.html#cfn-neptunegraph-privategraphendpoint-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Subnets in which private graph endpoint ENIs are created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptunegraph-privategraphendpoint.html#cfn-neptunegraph-privategraphendpoint-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''The VPC in which the private graph endpoint needs to be created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptunegraph-privategraphendpoint.html#cfn-neptunegraph-privategraphendpoint-vpcid
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPrivateGraphEndpointMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPrivateGraphEndpointPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_neptunegraph.mixins.CfnPrivateGraphEndpointPropsMixin",
):
    '''Create a private graph endpoint to allow private access from to the graph from within a VPC.

    You can attach security groups to the private graph endpoint.
    .. epigraph::

       VPC endpoint charges apply.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptunegraph-privategraphendpoint.html
    :cloudformationResource: AWS::NeptuneGraph::PrivateGraphEndpoint
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_neptunegraph import mixins as neptunegraph_mixins
        
        cfn_private_graph_endpoint_props_mixin = neptunegraph_mixins.CfnPrivateGraphEndpointPropsMixin(neptunegraph_mixins.CfnPrivateGraphEndpointMixinProps(
            graph_identifier="graphIdentifier",
            security_group_ids=["securityGroupIds"],
            subnet_ids=["subnetIds"],
            vpc_id="vpcId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPrivateGraphEndpointMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NeptuneGraph::PrivateGraphEndpoint``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eb621535dc4340db6e70878e558c3140a91d4584d4f3e03b9f494675fa4a777)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86d841dcb9347035745587f36f209a7a9b7b7f7f6cadb2304f126c31e41380e4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d82d3f92a23d083b5330abf6fd6a1ddb7ea343a869cbb6b838a80dfd7805c708)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPrivateGraphEndpointMixinProps:
        return typing.cast(CfnPrivateGraphEndpointMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnGraphMixinProps",
    "CfnGraphPropsMixin",
    "CfnPrivateGraphEndpointMixinProps",
    "CfnPrivateGraphEndpointPropsMixin",
]

publication.publish()

def _typecheckingstub__38f6c6f6ce2eb604dfc074a4728d38df29c9fd88e897b5bab687ff10f82b9916(
    *,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    graph_name: typing.Optional[builtins.str] = None,
    provisioned_memory: typing.Optional[jsii.Number] = None,
    public_connectivity: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    replica_count: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vector_search_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGraphPropsMixin.VectorSearchConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0733df3988cfa1f76a376f9bac31e5472d72da6b2ef5b3d710d4a589e545a51b(
    props: typing.Union[CfnGraphMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cea8af1505d05457552a381b391bec5706ae89b3f91531775562ee38aaba863(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c29cda85bfb8b81bd56c54c9e0a208ca0aa518203145b8499e659afcd4e611f1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23e72a124b0affebe1ce34a860bc3bc8b94971ef2bdc44d5ee29fe191c96c13(
    *,
    vector_search_dimension: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f22f099182e8d7b0f4f0bd921c553e0e9a2ce89ff63f0cd711e2324001463f2(
    *,
    graph_identifier: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eb621535dc4340db6e70878e558c3140a91d4584d4f3e03b9f494675fa4a777(
    props: typing.Union[CfnPrivateGraphEndpointMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d841dcb9347035745587f36f209a7a9b7b7f7f6cadb2304f126c31e41380e4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d82d3f92a23d083b5330abf6fd6a1ddb7ea343a869cbb6b838a80dfd7805c708(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
