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
    jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRouteMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "gateway_route_name": "gatewayRouteName",
        "mesh_name": "meshName",
        "mesh_owner": "meshOwner",
        "spec": "spec",
        "tags": "tags",
        "virtual_gateway_name": "virtualGatewayName",
    },
)
class CfnGatewayRouteMixinProps:
    def __init__(
        self,
        *,
        gateway_route_name: typing.Optional[builtins.str] = None,
        mesh_name: typing.Optional[builtins.str] = None,
        mesh_owner: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.GatewayRouteSpecProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        virtual_gateway_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnGatewayRoutePropsMixin.

        :param gateway_route_name: The name of the gateway route.
        :param mesh_name: The name of the service mesh that the resource resides in.
        :param mesh_owner: The AWS IAM account ID of the service mesh owner. If the account ID is not your own, then it's the ID of the account that shared the mesh with your account. For more information about mesh sharing, see `Working with shared meshes <https://docs.aws.amazon.com/app-mesh/latest/userguide/sharing.html>`_ .
        :param spec: The specifications of the gateway route.
        :param tags: Optional metadata that you can apply to the gateway route to assist with categorization and organization. Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.
        :param virtual_gateway_name: The virtual gateway that the gateway route is associated with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-gatewayroute.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
            
            cfn_gateway_route_mixin_props = appmesh_mixins.CfnGatewayRouteMixinProps(
                gateway_route_name="gatewayRouteName",
                mesh_name="meshName",
                mesh_owner="meshOwner",
                spec=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteSpecProperty(
                    grpc_route=appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteProperty(
                        action=appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteActionProperty(
                            rewrite=appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteRewriteProperty(
                                hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty(
                                    default_target_hostname="defaultTargetHostname"
                                )
                            ),
                            target=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteTargetProperty(
                                port=123,
                                virtual_service=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteVirtualServiceProperty(
                                    virtual_service_name="virtualServiceName"
                                )
                            )
                        ),
                        match=appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteMatchProperty(
                            hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameMatchProperty(
                                exact="exact",
                                suffix="suffix"
                            ),
                            metadata=[appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteMetadataProperty(
                                invert=False,
                                match=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteMetadataMatchProperty(
                                    exact="exact",
                                    prefix="prefix",
                                    range=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty(
                                        end=123,
                                        start=123
                                    ),
                                    regex="regex",
                                    suffix="suffix"
                                ),
                                name="name"
                            )],
                            port=123,
                            service_name="serviceName"
                        )
                    ),
                    http2_route=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteProperty(
                        action=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteActionProperty(
                            rewrite=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteRewriteProperty(
                                hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty(
                                    default_target_hostname="defaultTargetHostname"
                                ),
                                path=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRoutePathRewriteProperty(
                                    exact="exact"
                                ),
                                prefix=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRoutePrefixRewriteProperty(
                                    default_prefix="defaultPrefix",
                                    value="value"
                                )
                            ),
                            target=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteTargetProperty(
                                port=123,
                                virtual_service=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteVirtualServiceProperty(
                                    virtual_service_name="virtualServiceName"
                                )
                            )
                        ),
                        match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteMatchProperty(
                            headers=[appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderProperty(
                                invert=False,
                                match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderMatchProperty(
                                    exact="exact",
                                    prefix="prefix",
                                    range=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty(
                                        end=123,
                                        start=123
                                    ),
                                    regex="regex",
                                    suffix="suffix"
                                ),
                                name="name"
                            )],
                            hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameMatchProperty(
                                exact="exact",
                                suffix="suffix"
                            ),
                            method="method",
                            path=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpPathMatchProperty(
                                exact="exact",
                                regex="regex"
                            ),
                            port=123,
                            prefix="prefix",
                            query_parameters=[appmesh_mixins.CfnGatewayRoutePropsMixin.QueryParameterProperty(
                                match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpQueryParameterMatchProperty(
                                    exact="exact"
                                ),
                                name="name"
                            )]
                        )
                    ),
                    http_route=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteProperty(
                        action=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteActionProperty(
                            rewrite=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteRewriteProperty(
                                hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty(
                                    default_target_hostname="defaultTargetHostname"
                                ),
                                path=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRoutePathRewriteProperty(
                                    exact="exact"
                                ),
                                prefix=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRoutePrefixRewriteProperty(
                                    default_prefix="defaultPrefix",
                                    value="value"
                                )
                            ),
                            target=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteTargetProperty(
                                port=123,
                                virtual_service=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteVirtualServiceProperty(
                                    virtual_service_name="virtualServiceName"
                                )
                            )
                        ),
                        match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteMatchProperty(
                            headers=[appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderProperty(
                                invert=False,
                                match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderMatchProperty(
                                    exact="exact",
                                    prefix="prefix",
                                    range=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty(
                                        end=123,
                                        start=123
                                    ),
                                    regex="regex",
                                    suffix="suffix"
                                ),
                                name="name"
                            )],
                            hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameMatchProperty(
                                exact="exact",
                                suffix="suffix"
                            ),
                            method="method",
                            path=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpPathMatchProperty(
                                exact="exact",
                                regex="regex"
                            ),
                            port=123,
                            prefix="prefix",
                            query_parameters=[appmesh_mixins.CfnGatewayRoutePropsMixin.QueryParameterProperty(
                                match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpQueryParameterMatchProperty(
                                    exact="exact"
                                ),
                                name="name"
                            )]
                        )
                    ),
                    priority=123
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                virtual_gateway_name="virtualGatewayName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02220d748b1d3ce373730b5de1cc9ff04fc32ef7f876b552de1281509ec60cad)
            check_type(argname="argument gateway_route_name", value=gateway_route_name, expected_type=type_hints["gateway_route_name"])
            check_type(argname="argument mesh_name", value=mesh_name, expected_type=type_hints["mesh_name"])
            check_type(argname="argument mesh_owner", value=mesh_owner, expected_type=type_hints["mesh_owner"])
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument virtual_gateway_name", value=virtual_gateway_name, expected_type=type_hints["virtual_gateway_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gateway_route_name is not None:
            self._values["gateway_route_name"] = gateway_route_name
        if mesh_name is not None:
            self._values["mesh_name"] = mesh_name
        if mesh_owner is not None:
            self._values["mesh_owner"] = mesh_owner
        if spec is not None:
            self._values["spec"] = spec
        if tags is not None:
            self._values["tags"] = tags
        if virtual_gateway_name is not None:
            self._values["virtual_gateway_name"] = virtual_gateway_name

    @builtins.property
    def gateway_route_name(self) -> typing.Optional[builtins.str]:
        '''The name of the gateway route.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-gatewayroute.html#cfn-appmesh-gatewayroute-gatewayroutename
        '''
        result = self._values.get("gateway_route_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mesh_name(self) -> typing.Optional[builtins.str]:
        '''The name of the service mesh that the resource resides in.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-gatewayroute.html#cfn-appmesh-gatewayroute-meshname
        '''
        result = self._values.get("mesh_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mesh_owner(self) -> typing.Optional[builtins.str]:
        '''The AWS IAM account ID of the service mesh owner.

        If the account ID is not your own, then it's the ID of the account that shared the mesh with your account. For more information about mesh sharing, see `Working with shared meshes <https://docs.aws.amazon.com/app-mesh/latest/userguide/sharing.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-gatewayroute.html#cfn-appmesh-gatewayroute-meshowner
        '''
        result = self._values.get("mesh_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spec(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GatewayRouteSpecProperty"]]:
        '''The specifications of the gateway route.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-gatewayroute.html#cfn-appmesh-gatewayroute-spec
        '''
        result = self._values.get("spec")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GatewayRouteSpecProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Optional metadata that you can apply to the gateway route to assist with categorization and organization.

        Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-gatewayroute.html#cfn-appmesh-gatewayroute-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def virtual_gateway_name(self) -> typing.Optional[builtins.str]:
        '''The virtual gateway that the gateway route is associated with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-gatewayroute.html#cfn-appmesh-gatewayroute-virtualgatewayname
        '''
        result = self._values.get("virtual_gateway_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGatewayRouteMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGatewayRoutePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRoutePropsMixin",
):
    '''Creates a gateway route.

    A gateway route is attached to a virtual gateway and routes traffic to an existing virtual service. If a route matches a request, it can distribute traffic to a target virtual service.

    For more information about gateway routes, see `Gateway routes <https://docs.aws.amazon.com/app-mesh/latest/userguide/gateway-routes.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-gatewayroute.html
    :cloudformationResource: AWS::AppMesh::GatewayRoute
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
        
        cfn_gateway_route_props_mixin = appmesh_mixins.CfnGatewayRoutePropsMixin(appmesh_mixins.CfnGatewayRouteMixinProps(
            gateway_route_name="gatewayRouteName",
            mesh_name="meshName",
            mesh_owner="meshOwner",
            spec=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteSpecProperty(
                grpc_route=appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteProperty(
                    action=appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteActionProperty(
                        rewrite=appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteRewriteProperty(
                            hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty(
                                default_target_hostname="defaultTargetHostname"
                            )
                        ),
                        target=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteTargetProperty(
                            port=123,
                            virtual_service=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteVirtualServiceProperty(
                                virtual_service_name="virtualServiceName"
                            )
                        )
                    ),
                    match=appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteMatchProperty(
                        hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameMatchProperty(
                            exact="exact",
                            suffix="suffix"
                        ),
                        metadata=[appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteMetadataProperty(
                            invert=False,
                            match=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteMetadataMatchProperty(
                                exact="exact",
                                prefix="prefix",
                                range=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty(
                                    end=123,
                                    start=123
                                ),
                                regex="regex",
                                suffix="suffix"
                            ),
                            name="name"
                        )],
                        port=123,
                        service_name="serviceName"
                    )
                ),
                http2_route=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteProperty(
                    action=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteActionProperty(
                        rewrite=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteRewriteProperty(
                            hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty(
                                default_target_hostname="defaultTargetHostname"
                            ),
                            path=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRoutePathRewriteProperty(
                                exact="exact"
                            ),
                            prefix=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRoutePrefixRewriteProperty(
                                default_prefix="defaultPrefix",
                                value="value"
                            )
                        ),
                        target=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteTargetProperty(
                            port=123,
                            virtual_service=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteVirtualServiceProperty(
                                virtual_service_name="virtualServiceName"
                            )
                        )
                    ),
                    match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteMatchProperty(
                        headers=[appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderProperty(
                            invert=False,
                            match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderMatchProperty(
                                exact="exact",
                                prefix="prefix",
                                range=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty(
                                    end=123,
                                    start=123
                                ),
                                regex="regex",
                                suffix="suffix"
                            ),
                            name="name"
                        )],
                        hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameMatchProperty(
                            exact="exact",
                            suffix="suffix"
                        ),
                        method="method",
                        path=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpPathMatchProperty(
                            exact="exact",
                            regex="regex"
                        ),
                        port=123,
                        prefix="prefix",
                        query_parameters=[appmesh_mixins.CfnGatewayRoutePropsMixin.QueryParameterProperty(
                            match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpQueryParameterMatchProperty(
                                exact="exact"
                            ),
                            name="name"
                        )]
                    )
                ),
                http_route=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteProperty(
                    action=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteActionProperty(
                        rewrite=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteRewriteProperty(
                            hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty(
                                default_target_hostname="defaultTargetHostname"
                            ),
                            path=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRoutePathRewriteProperty(
                                exact="exact"
                            ),
                            prefix=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRoutePrefixRewriteProperty(
                                default_prefix="defaultPrefix",
                                value="value"
                            )
                        ),
                        target=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteTargetProperty(
                            port=123,
                            virtual_service=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteVirtualServiceProperty(
                                virtual_service_name="virtualServiceName"
                            )
                        )
                    ),
                    match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteMatchProperty(
                        headers=[appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderProperty(
                            invert=False,
                            match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderMatchProperty(
                                exact="exact",
                                prefix="prefix",
                                range=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty(
                                    end=123,
                                    start=123
                                ),
                                regex="regex",
                                suffix="suffix"
                            ),
                            name="name"
                        )],
                        hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameMatchProperty(
                            exact="exact",
                            suffix="suffix"
                        ),
                        method="method",
                        path=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpPathMatchProperty(
                            exact="exact",
                            regex="regex"
                        ),
                        port=123,
                        prefix="prefix",
                        query_parameters=[appmesh_mixins.CfnGatewayRoutePropsMixin.QueryParameterProperty(
                            match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpQueryParameterMatchProperty(
                                exact="exact"
                            ),
                            name="name"
                        )]
                    )
                ),
                priority=123
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            virtual_gateway_name="virtualGatewayName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnGatewayRouteMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppMesh::GatewayRoute``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__824815bb481bc192658fa154ae4913585ab614fc94aa6db1672cc5574d4656be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dd45f06390e9438c7bbd15fcd523edd72623ac2a7618e5e3a0c415a043c9e65)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7e75eed816174686d03f17c653294e26b79bb76f0d3c00b267ea69c65054bf8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGatewayRouteMixinProps:
        return typing.cast(CfnGatewayRouteMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameMatchProperty",
        jsii_struct_bases=[],
        name_mapping={"exact": "exact", "suffix": "suffix"},
    )
    class GatewayRouteHostnameMatchProperty:
        def __init__(
            self,
            *,
            exact: typing.Optional[builtins.str] = None,
            suffix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object representing the gateway route host name to match.

            :param exact: The exact host name to match on.
            :param suffix: The specified ending characters of the host name to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutehostnamematch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                gateway_route_hostname_match_property = appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameMatchProperty(
                    exact="exact",
                    suffix="suffix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__75918f333f411933786a1d7aa898cfdb1853ea25c538a5e6e0bac525ed9a15fc)
                check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
                check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exact is not None:
                self._values["exact"] = exact
            if suffix is not None:
                self._values["suffix"] = suffix

        @builtins.property
        def exact(self) -> typing.Optional[builtins.str]:
            '''The exact host name to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutehostnamematch.html#cfn-appmesh-gatewayroute-gatewayroutehostnamematch-exact
            '''
            result = self._values.get("exact")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def suffix(self) -> typing.Optional[builtins.str]:
            '''The specified ending characters of the host name to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutehostnamematch.html#cfn-appmesh-gatewayroute-gatewayroutehostnamematch-suffix
            '''
            result = self._values.get("suffix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GatewayRouteHostnameMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty",
        jsii_struct_bases=[],
        name_mapping={"default_target_hostname": "defaultTargetHostname"},
    )
    class GatewayRouteHostnameRewriteProperty:
        def __init__(
            self,
            *,
            default_target_hostname: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object representing the gateway route host name to rewrite.

            :param default_target_hostname: The default target host name to write to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutehostnamerewrite.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                gateway_route_hostname_rewrite_property = appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty(
                    default_target_hostname="defaultTargetHostname"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__59db7ca4152bf931bb6755d75236138d746dae95d8bdac9cb2dba0e838c1ee68)
                check_type(argname="argument default_target_hostname", value=default_target_hostname, expected_type=type_hints["default_target_hostname"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_target_hostname is not None:
                self._values["default_target_hostname"] = default_target_hostname

        @builtins.property
        def default_target_hostname(self) -> typing.Optional[builtins.str]:
            '''The default target host name to write to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutehostnamerewrite.html#cfn-appmesh-gatewayroute-gatewayroutehostnamerewrite-defaulttargethostname
            '''
            result = self._values.get("default_target_hostname")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GatewayRouteHostnameRewriteProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRoutePropsMixin.GatewayRouteMetadataMatchProperty",
        jsii_struct_bases=[],
        name_mapping={
            "exact": "exact",
            "prefix": "prefix",
            "range": "range",
            "regex": "regex",
            "suffix": "suffix",
        },
    )
    class GatewayRouteMetadataMatchProperty:
        def __init__(
            self,
            *,
            exact: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
            range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            regex: typing.Optional[builtins.str] = None,
            suffix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object representing the method header to be matched.

            :param exact: The exact method header to be matched on.
            :param prefix: The specified beginning characters of the method header to be matched on.
            :param range: An object that represents the range of values to match on.
            :param regex: The regex used to match the method header.
            :param suffix: The specified ending characters of the method header to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutemetadatamatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                gateway_route_metadata_match_property = appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteMetadataMatchProperty(
                    exact="exact",
                    prefix="prefix",
                    range=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty(
                        end=123,
                        start=123
                    ),
                    regex="regex",
                    suffix="suffix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c92bca337c042136c5dc91af7a0cc84a37012ed9ebb829dc9b55d12461bc4c28)
                check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument range", value=range, expected_type=type_hints["range"])
                check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
                check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exact is not None:
                self._values["exact"] = exact
            if prefix is not None:
                self._values["prefix"] = prefix
            if range is not None:
                self._values["range"] = range
            if regex is not None:
                self._values["regex"] = regex
            if suffix is not None:
                self._values["suffix"] = suffix

        @builtins.property
        def exact(self) -> typing.Optional[builtins.str]:
            '''The exact method header to be matched on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutemetadatamatch.html#cfn-appmesh-gatewayroute-gatewayroutemetadatamatch-exact
            '''
            result = self._values.get("exact")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''The specified beginning characters of the method header to be matched on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutemetadatamatch.html#cfn-appmesh-gatewayroute-gatewayroutemetadatamatch-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def range(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty"]]:
            '''An object that represents the range of values to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutemetadatamatch.html#cfn-appmesh-gatewayroute-gatewayroutemetadatamatch-range
            '''
            result = self._values.get("range")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty"]], result)

        @builtins.property
        def regex(self) -> typing.Optional[builtins.str]:
            '''The regex used to match the method header.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutemetadatamatch.html#cfn-appmesh-gatewayroute-gatewayroutemetadatamatch-regex
            '''
            result = self._values.get("regex")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def suffix(self) -> typing.Optional[builtins.str]:
            '''The specified ending characters of the method header to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutemetadatamatch.html#cfn-appmesh-gatewayroute-gatewayroutemetadatamatch-suffix
            '''
            result = self._values.get("suffix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GatewayRouteMetadataMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty",
        jsii_struct_bases=[],
        name_mapping={"end": "end", "start": "start"},
    )
    class GatewayRouteRangeMatchProperty:
        def __init__(
            self,
            *,
            end: typing.Optional[jsii.Number] = None,
            start: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An object that represents the range of values to match on.

            The first character of the range is included in the range, though the last character is not. For example, if the range specified were 1-100, only values 1-99 would be matched.

            :param end: The end of the range.
            :param start: The start of the range.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayrouterangematch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                gateway_route_range_match_property = appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty(
                    end=123,
                    start=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9f4fd3d3ebfdb363d188788bcd6d1800e4a73c8208b64d4869b4d27b09be2d62)
                check_type(argname="argument end", value=end, expected_type=type_hints["end"])
                check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if end is not None:
                self._values["end"] = end
            if start is not None:
                self._values["start"] = start

        @builtins.property
        def end(self) -> typing.Optional[jsii.Number]:
            '''The end of the range.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayrouterangematch.html#cfn-appmesh-gatewayroute-gatewayrouterangematch-end
            '''
            result = self._values.get("end")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def start(self) -> typing.Optional[jsii.Number]:
            '''The start of the range.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayrouterangematch.html#cfn-appmesh-gatewayroute-gatewayrouterangematch-start
            '''
            result = self._values.get("start")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GatewayRouteRangeMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRoutePropsMixin.GatewayRouteSpecProperty",
        jsii_struct_bases=[],
        name_mapping={
            "grpc_route": "grpcRoute",
            "http2_route": "http2Route",
            "http_route": "httpRoute",
            "priority": "priority",
        },
    )
    class GatewayRouteSpecProperty:
        def __init__(
            self,
            *,
            grpc_route: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.GrpcGatewayRouteProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            http2_route: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.HttpGatewayRouteProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            http_route: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.HttpGatewayRouteProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            priority: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An object that represents a gateway route specification.

            Specify one gateway route type.

            :param grpc_route: An object that represents the specification of a gRPC gateway route.
            :param http2_route: An object that represents the specification of an HTTP/2 gateway route.
            :param http_route: An object that represents the specification of an HTTP gateway route.
            :param priority: The ordering of the gateway routes spec.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutespec.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                gateway_route_spec_property = appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteSpecProperty(
                    grpc_route=appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteProperty(
                        action=appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteActionProperty(
                            rewrite=appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteRewriteProperty(
                                hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty(
                                    default_target_hostname="defaultTargetHostname"
                                )
                            ),
                            target=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteTargetProperty(
                                port=123,
                                virtual_service=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteVirtualServiceProperty(
                                    virtual_service_name="virtualServiceName"
                                )
                            )
                        ),
                        match=appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteMatchProperty(
                            hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameMatchProperty(
                                exact="exact",
                                suffix="suffix"
                            ),
                            metadata=[appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteMetadataProperty(
                                invert=False,
                                match=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteMetadataMatchProperty(
                                    exact="exact",
                                    prefix="prefix",
                                    range=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty(
                                        end=123,
                                        start=123
                                    ),
                                    regex="regex",
                                    suffix="suffix"
                                ),
                                name="name"
                            )],
                            port=123,
                            service_name="serviceName"
                        )
                    ),
                    http2_route=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteProperty(
                        action=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteActionProperty(
                            rewrite=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteRewriteProperty(
                                hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty(
                                    default_target_hostname="defaultTargetHostname"
                                ),
                                path=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRoutePathRewriteProperty(
                                    exact="exact"
                                ),
                                prefix=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRoutePrefixRewriteProperty(
                                    default_prefix="defaultPrefix",
                                    value="value"
                                )
                            ),
                            target=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteTargetProperty(
                                port=123,
                                virtual_service=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteVirtualServiceProperty(
                                    virtual_service_name="virtualServiceName"
                                )
                            )
                        ),
                        match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteMatchProperty(
                            headers=[appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderProperty(
                                invert=False,
                                match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderMatchProperty(
                                    exact="exact",
                                    prefix="prefix",
                                    range=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty(
                                        end=123,
                                        start=123
                                    ),
                                    regex="regex",
                                    suffix="suffix"
                                ),
                                name="name"
                            )],
                            hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameMatchProperty(
                                exact="exact",
                                suffix="suffix"
                            ),
                            method="method",
                            path=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpPathMatchProperty(
                                exact="exact",
                                regex="regex"
                            ),
                            port=123,
                            prefix="prefix",
                            query_parameters=[appmesh_mixins.CfnGatewayRoutePropsMixin.QueryParameterProperty(
                                match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpQueryParameterMatchProperty(
                                    exact="exact"
                                ),
                                name="name"
                            )]
                        )
                    ),
                    http_route=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteProperty(
                        action=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteActionProperty(
                            rewrite=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteRewriteProperty(
                                hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty(
                                    default_target_hostname="defaultTargetHostname"
                                ),
                                path=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRoutePathRewriteProperty(
                                    exact="exact"
                                ),
                                prefix=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRoutePrefixRewriteProperty(
                                    default_prefix="defaultPrefix",
                                    value="value"
                                )
                            ),
                            target=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteTargetProperty(
                                port=123,
                                virtual_service=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteVirtualServiceProperty(
                                    virtual_service_name="virtualServiceName"
                                )
                            )
                        ),
                        match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteMatchProperty(
                            headers=[appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderProperty(
                                invert=False,
                                match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderMatchProperty(
                                    exact="exact",
                                    prefix="prefix",
                                    range=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty(
                                        end=123,
                                        start=123
                                    ),
                                    regex="regex",
                                    suffix="suffix"
                                ),
                                name="name"
                            )],
                            hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameMatchProperty(
                                exact="exact",
                                suffix="suffix"
                            ),
                            method="method",
                            path=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpPathMatchProperty(
                                exact="exact",
                                regex="regex"
                            ),
                            port=123,
                            prefix="prefix",
                            query_parameters=[appmesh_mixins.CfnGatewayRoutePropsMixin.QueryParameterProperty(
                                match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpQueryParameterMatchProperty(
                                    exact="exact"
                                ),
                                name="name"
                            )]
                        )
                    ),
                    priority=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__42f7865292d581f7869900f67d04fcdf60b372c947488bbd33853c25c4fff9e2)
                check_type(argname="argument grpc_route", value=grpc_route, expected_type=type_hints["grpc_route"])
                check_type(argname="argument http2_route", value=http2_route, expected_type=type_hints["http2_route"])
                check_type(argname="argument http_route", value=http_route, expected_type=type_hints["http_route"])
                check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if grpc_route is not None:
                self._values["grpc_route"] = grpc_route
            if http2_route is not None:
                self._values["http2_route"] = http2_route
            if http_route is not None:
                self._values["http_route"] = http_route
            if priority is not None:
                self._values["priority"] = priority

        @builtins.property
        def grpc_route(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GrpcGatewayRouteProperty"]]:
            '''An object that represents the specification of a gRPC gateway route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutespec.html#cfn-appmesh-gatewayroute-gatewayroutespec-grpcroute
            '''
            result = self._values.get("grpc_route")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GrpcGatewayRouteProperty"]], result)

        @builtins.property
        def http2_route(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.HttpGatewayRouteProperty"]]:
            '''An object that represents the specification of an HTTP/2 gateway route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutespec.html#cfn-appmesh-gatewayroute-gatewayroutespec-http2route
            '''
            result = self._values.get("http2_route")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.HttpGatewayRouteProperty"]], result)

        @builtins.property
        def http_route(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.HttpGatewayRouteProperty"]]:
            '''An object that represents the specification of an HTTP gateway route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutespec.html#cfn-appmesh-gatewayroute-gatewayroutespec-httproute
            '''
            result = self._values.get("http_route")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.HttpGatewayRouteProperty"]], result)

        @builtins.property
        def priority(self) -> typing.Optional[jsii.Number]:
            '''The ordering of the gateway routes spec.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutespec.html#cfn-appmesh-gatewayroute-gatewayroutespec-priority
            '''
            result = self._values.get("priority")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GatewayRouteSpecProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRoutePropsMixin.GatewayRouteTargetProperty",
        jsii_struct_bases=[],
        name_mapping={"port": "port", "virtual_service": "virtualService"},
    )
    class GatewayRouteTargetProperty:
        def __init__(
            self,
            *,
            port: typing.Optional[jsii.Number] = None,
            virtual_service: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.GatewayRouteVirtualServiceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents a gateway route target.

            :param port: The port number of the gateway route target.
            :param virtual_service: An object that represents a virtual service gateway route target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutetarget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                gateway_route_target_property = appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteTargetProperty(
                    port=123,
                    virtual_service=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteVirtualServiceProperty(
                        virtual_service_name="virtualServiceName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d95014113505684b46029e5828143d1d6c91bf915dab819476ac94b9e878f0f3)
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument virtual_service", value=virtual_service, expected_type=type_hints["virtual_service"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if port is not None:
                self._values["port"] = port
            if virtual_service is not None:
                self._values["virtual_service"] = virtual_service

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port number of the gateway route target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutetarget.html#cfn-appmesh-gatewayroute-gatewayroutetarget-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def virtual_service(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GatewayRouteVirtualServiceProperty"]]:
            '''An object that represents a virtual service gateway route target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutetarget.html#cfn-appmesh-gatewayroute-gatewayroutetarget-virtualservice
            '''
            result = self._values.get("virtual_service")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GatewayRouteVirtualServiceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GatewayRouteTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRoutePropsMixin.GatewayRouteVirtualServiceProperty",
        jsii_struct_bases=[],
        name_mapping={"virtual_service_name": "virtualServiceName"},
    )
    class GatewayRouteVirtualServiceProperty:
        def __init__(
            self,
            *,
            virtual_service_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the virtual service that traffic is routed to.

            :param virtual_service_name: The name of the virtual service that traffic is routed to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutevirtualservice.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                gateway_route_virtual_service_property = appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteVirtualServiceProperty(
                    virtual_service_name="virtualServiceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__94b71d5d22533990ba0fe2bb2773d917822ca24dff5d5d11fbb36625056d887a)
                check_type(argname="argument virtual_service_name", value=virtual_service_name, expected_type=type_hints["virtual_service_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if virtual_service_name is not None:
                self._values["virtual_service_name"] = virtual_service_name

        @builtins.property
        def virtual_service_name(self) -> typing.Optional[builtins.str]:
            '''The name of the virtual service that traffic is routed to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-gatewayroutevirtualservice.html#cfn-appmesh-gatewayroute-gatewayroutevirtualservice-virtualservicename
            '''
            result = self._values.get("virtual_service_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GatewayRouteVirtualServiceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteActionProperty",
        jsii_struct_bases=[],
        name_mapping={"rewrite": "rewrite", "target": "target"},
    )
    class GrpcGatewayRouteActionProperty:
        def __init__(
            self,
            *,
            rewrite: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.GrpcGatewayRouteRewriteProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.GatewayRouteTargetProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents the action to take if a match is determined.

            :param rewrite: The gateway route action to rewrite.
            :param target: An object that represents the target that traffic is routed to when a request matches the gateway route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-grpcgatewayrouteaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                grpc_gateway_route_action_property = appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteActionProperty(
                    rewrite=appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteRewriteProperty(
                        hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty(
                            default_target_hostname="defaultTargetHostname"
                        )
                    ),
                    target=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteTargetProperty(
                        port=123,
                        virtual_service=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteVirtualServiceProperty(
                            virtual_service_name="virtualServiceName"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6ff18074936ef15630b969bdc52affcb8c82195dcb58f2559782be8b317f7e6f)
                check_type(argname="argument rewrite", value=rewrite, expected_type=type_hints["rewrite"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rewrite is not None:
                self._values["rewrite"] = rewrite
            if target is not None:
                self._values["target"] = target

        @builtins.property
        def rewrite(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GrpcGatewayRouteRewriteProperty"]]:
            '''The gateway route action to rewrite.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-grpcgatewayrouteaction.html#cfn-appmesh-gatewayroute-grpcgatewayrouteaction-rewrite
            '''
            result = self._values.get("rewrite")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GrpcGatewayRouteRewriteProperty"]], result)

        @builtins.property
        def target(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GatewayRouteTargetProperty"]]:
            '''An object that represents the target that traffic is routed to when a request matches the gateway route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-grpcgatewayrouteaction.html#cfn-appmesh-gatewayroute-grpcgatewayrouteaction-target
            '''
            result = self._values.get("target")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GatewayRouteTargetProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrpcGatewayRouteActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteMatchProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hostname": "hostname",
            "metadata": "metadata",
            "port": "port",
            "service_name": "serviceName",
        },
    )
    class GrpcGatewayRouteMatchProperty:
        def __init__(
            self,
            *,
            hostname: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.GatewayRouteHostnameMatchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.GrpcGatewayRouteMetadataProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            port: typing.Optional[jsii.Number] = None,
            service_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the criteria for determining a request match.

            :param hostname: The gateway route host name to be matched on.
            :param metadata: The gateway route metadata to be matched on.
            :param port: The gateway route port to be matched on.
            :param service_name: The fully qualified domain name for the service to match from the request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-grpcgatewayroutematch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                grpc_gateway_route_match_property = appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteMatchProperty(
                    hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameMatchProperty(
                        exact="exact",
                        suffix="suffix"
                    ),
                    metadata=[appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteMetadataProperty(
                        invert=False,
                        match=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteMetadataMatchProperty(
                            exact="exact",
                            prefix="prefix",
                            range=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty(
                                end=123,
                                start=123
                            ),
                            regex="regex",
                            suffix="suffix"
                        ),
                        name="name"
                    )],
                    port=123,
                    service_name="serviceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1f539f6a6f4327f223e298867504bf62411180e5b432a02ccbef6be29b2d901a)
                check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
                check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if hostname is not None:
                self._values["hostname"] = hostname
            if metadata is not None:
                self._values["metadata"] = metadata
            if port is not None:
                self._values["port"] = port
            if service_name is not None:
                self._values["service_name"] = service_name

        @builtins.property
        def hostname(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GatewayRouteHostnameMatchProperty"]]:
            '''The gateway route host name to be matched on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-grpcgatewayroutematch.html#cfn-appmesh-gatewayroute-grpcgatewayroutematch-hostname
            '''
            result = self._values.get("hostname")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GatewayRouteHostnameMatchProperty"]], result)

        @builtins.property
        def metadata(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GrpcGatewayRouteMetadataProperty"]]]]:
            '''The gateway route metadata to be matched on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-grpcgatewayroutematch.html#cfn-appmesh-gatewayroute-grpcgatewayroutematch-metadata
            '''
            result = self._values.get("metadata")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GrpcGatewayRouteMetadataProperty"]]]], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The gateway route port to be matched on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-grpcgatewayroutematch.html#cfn-appmesh-gatewayroute-grpcgatewayroutematch-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def service_name(self) -> typing.Optional[builtins.str]:
            '''The fully qualified domain name for the service to match from the request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-grpcgatewayroutematch.html#cfn-appmesh-gatewayroute-grpcgatewayroutematch-servicename
            '''
            result = self._values.get("service_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrpcGatewayRouteMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteMetadataProperty",
        jsii_struct_bases=[],
        name_mapping={"invert": "invert", "match": "match", "name": "name"},
    )
    class GrpcGatewayRouteMetadataProperty:
        def __init__(
            self,
            *,
            invert: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.GatewayRouteMetadataMatchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object representing the metadata of the gateway route.

            :param invert: Specify ``True`` to match anything except the match criteria. The default value is ``False`` .
            :param match: The criteria for determining a metadata match.
            :param name: A name for the gateway route metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-grpcgatewayroutemetadata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                grpc_gateway_route_metadata_property = appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteMetadataProperty(
                    invert=False,
                    match=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteMetadataMatchProperty(
                        exact="exact",
                        prefix="prefix",
                        range=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty(
                            end=123,
                            start=123
                        ),
                        regex="regex",
                        suffix="suffix"
                    ),
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__da54e85a564a9f4d5877af87fa3fa6a57d44cd2d7581b76a8f7fa69c33a7fa41)
                check_type(argname="argument invert", value=invert, expected_type=type_hints["invert"])
                check_type(argname="argument match", value=match, expected_type=type_hints["match"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if invert is not None:
                self._values["invert"] = invert
            if match is not None:
                self._values["match"] = match
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def invert(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specify ``True`` to match anything except the match criteria.

            The default value is ``False`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-grpcgatewayroutemetadata.html#cfn-appmesh-gatewayroute-grpcgatewayroutemetadata-invert
            '''
            result = self._values.get("invert")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def match(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GatewayRouteMetadataMatchProperty"]]:
            '''The criteria for determining a metadata match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-grpcgatewayroutemetadata.html#cfn-appmesh-gatewayroute-grpcgatewayroutemetadata-match
            '''
            result = self._values.get("match")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GatewayRouteMetadataMatchProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''A name for the gateway route metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-grpcgatewayroutemetadata.html#cfn-appmesh-gatewayroute-grpcgatewayroutemetadata-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrpcGatewayRouteMetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action", "match": "match"},
    )
    class GrpcGatewayRouteProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.GrpcGatewayRouteActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.GrpcGatewayRouteMatchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents a gRPC gateway route.

            :param action: An object that represents the action to take if a match is determined.
            :param match: An object that represents the criteria for determining a request match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-grpcgatewayroute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                grpc_gateway_route_property = appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteProperty(
                    action=appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteActionProperty(
                        rewrite=appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteRewriteProperty(
                            hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty(
                                default_target_hostname="defaultTargetHostname"
                            )
                        ),
                        target=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteTargetProperty(
                            port=123,
                            virtual_service=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteVirtualServiceProperty(
                                virtual_service_name="virtualServiceName"
                            )
                        )
                    ),
                    match=appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteMatchProperty(
                        hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameMatchProperty(
                            exact="exact",
                            suffix="suffix"
                        ),
                        metadata=[appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteMetadataProperty(
                            invert=False,
                            match=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteMetadataMatchProperty(
                                exact="exact",
                                prefix="prefix",
                                range=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty(
                                    end=123,
                                    start=123
                                ),
                                regex="regex",
                                suffix="suffix"
                            ),
                            name="name"
                        )],
                        port=123,
                        service_name="serviceName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c698a9386688ea28533b8cab57a73b041eda410a08c67498b30eca63ad829359)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if match is not None:
                self._values["match"] = match

        @builtins.property
        def action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GrpcGatewayRouteActionProperty"]]:
            '''An object that represents the action to take if a match is determined.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-grpcgatewayroute.html#cfn-appmesh-gatewayroute-grpcgatewayroute-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GrpcGatewayRouteActionProperty"]], result)

        @builtins.property
        def match(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GrpcGatewayRouteMatchProperty"]]:
            '''An object that represents the criteria for determining a request match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-grpcgatewayroute.html#cfn-appmesh-gatewayroute-grpcgatewayroute-match
            '''
            result = self._values.get("match")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GrpcGatewayRouteMatchProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrpcGatewayRouteProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteRewriteProperty",
        jsii_struct_bases=[],
        name_mapping={"hostname": "hostname"},
    )
    class GrpcGatewayRouteRewriteProperty:
        def __init__(
            self,
            *,
            hostname: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents the gateway route to rewrite.

            :param hostname: The host name of the gateway route to rewrite.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-grpcgatewayrouterewrite.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                grpc_gateway_route_rewrite_property = appmesh_mixins.CfnGatewayRoutePropsMixin.GrpcGatewayRouteRewriteProperty(
                    hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty(
                        default_target_hostname="defaultTargetHostname"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7399d3106fc9d4da4ebbedbe08e200603fd70d48ef7e175a72d72df0986bf22d)
                check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if hostname is not None:
                self._values["hostname"] = hostname

        @builtins.property
        def hostname(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty"]]:
            '''The host name of the gateway route to rewrite.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-grpcgatewayrouterewrite.html#cfn-appmesh-gatewayroute-grpcgatewayrouterewrite-hostname
            '''
            result = self._values.get("hostname")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrpcGatewayRouteRewriteProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteActionProperty",
        jsii_struct_bases=[],
        name_mapping={"rewrite": "rewrite", "target": "target"},
    )
    class HttpGatewayRouteActionProperty:
        def __init__(
            self,
            *,
            rewrite: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.HttpGatewayRouteRewriteProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.GatewayRouteTargetProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents the action to take if a match is determined.

            :param rewrite: The gateway route action to rewrite.
            :param target: An object that represents the target that traffic is routed to when a request matches the gateway route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayrouteaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                http_gateway_route_action_property = appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteActionProperty(
                    rewrite=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteRewriteProperty(
                        hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty(
                            default_target_hostname="defaultTargetHostname"
                        ),
                        path=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRoutePathRewriteProperty(
                            exact="exact"
                        ),
                        prefix=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRoutePrefixRewriteProperty(
                            default_prefix="defaultPrefix",
                            value="value"
                        )
                    ),
                    target=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteTargetProperty(
                        port=123,
                        virtual_service=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteVirtualServiceProperty(
                            virtual_service_name="virtualServiceName"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cf1cc8bca4777e191079c1ee7dfdf05f35856eb4f421c65ba275a15d497ca56f)
                check_type(argname="argument rewrite", value=rewrite, expected_type=type_hints["rewrite"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rewrite is not None:
                self._values["rewrite"] = rewrite
            if target is not None:
                self._values["target"] = target

        @builtins.property
        def rewrite(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.HttpGatewayRouteRewriteProperty"]]:
            '''The gateway route action to rewrite.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayrouteaction.html#cfn-appmesh-gatewayroute-httpgatewayrouteaction-rewrite
            '''
            result = self._values.get("rewrite")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.HttpGatewayRouteRewriteProperty"]], result)

        @builtins.property
        def target(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GatewayRouteTargetProperty"]]:
            '''An object that represents the target that traffic is routed to when a request matches the gateway route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayrouteaction.html#cfn-appmesh-gatewayroute-httpgatewayrouteaction-target
            '''
            result = self._values.get("target")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GatewayRouteTargetProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpGatewayRouteActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderMatchProperty",
        jsii_struct_bases=[],
        name_mapping={
            "exact": "exact",
            "prefix": "prefix",
            "range": "range",
            "regex": "regex",
            "suffix": "suffix",
        },
    )
    class HttpGatewayRouteHeaderMatchProperty:
        def __init__(
            self,
            *,
            exact: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
            range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            regex: typing.Optional[builtins.str] = None,
            suffix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the method and value to match with the header value sent in a request.

            Specify one match method.

            :param exact: The value sent by the client must match the specified value exactly.
            :param prefix: The value sent by the client must begin with the specified characters.
            :param range: An object that represents the range of values to match on.
            :param regex: The value sent by the client must include the specified characters.
            :param suffix: The value sent by the client must end with the specified characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayrouteheadermatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                http_gateway_route_header_match_property = appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderMatchProperty(
                    exact="exact",
                    prefix="prefix",
                    range=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty(
                        end=123,
                        start=123
                    ),
                    regex="regex",
                    suffix="suffix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aae92b2663765c3565ee413d5d8fcedbcc542fa6b5e291d5f454409496410291)
                check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument range", value=range, expected_type=type_hints["range"])
                check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
                check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exact is not None:
                self._values["exact"] = exact
            if prefix is not None:
                self._values["prefix"] = prefix
            if range is not None:
                self._values["range"] = range
            if regex is not None:
                self._values["regex"] = regex
            if suffix is not None:
                self._values["suffix"] = suffix

        @builtins.property
        def exact(self) -> typing.Optional[builtins.str]:
            '''The value sent by the client must match the specified value exactly.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayrouteheadermatch.html#cfn-appmesh-gatewayroute-httpgatewayrouteheadermatch-exact
            '''
            result = self._values.get("exact")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''The value sent by the client must begin with the specified characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayrouteheadermatch.html#cfn-appmesh-gatewayroute-httpgatewayrouteheadermatch-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def range(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty"]]:
            '''An object that represents the range of values to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayrouteheadermatch.html#cfn-appmesh-gatewayroute-httpgatewayrouteheadermatch-range
            '''
            result = self._values.get("range")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty"]], result)

        @builtins.property
        def regex(self) -> typing.Optional[builtins.str]:
            '''The value sent by the client must include the specified characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayrouteheadermatch.html#cfn-appmesh-gatewayroute-httpgatewayrouteheadermatch-regex
            '''
            result = self._values.get("regex")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def suffix(self) -> typing.Optional[builtins.str]:
            '''The value sent by the client must end with the specified characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayrouteheadermatch.html#cfn-appmesh-gatewayroute-httpgatewayrouteheadermatch-suffix
            '''
            result = self._values.get("suffix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpGatewayRouteHeaderMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderProperty",
        jsii_struct_bases=[],
        name_mapping={"invert": "invert", "match": "match", "name": "name"},
    )
    class HttpGatewayRouteHeaderProperty:
        def __init__(
            self,
            *,
            invert: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderMatchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the HTTP header in the gateway route.

            :param invert: Specify ``True`` to match anything except the match criteria. The default value is ``False`` .
            :param match: An object that represents the method and value to match with the header value sent in a request. Specify one match method.
            :param name: A name for the HTTP header in the gateway route that will be matched on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayrouteheader.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                http_gateway_route_header_property = appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderProperty(
                    invert=False,
                    match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderMatchProperty(
                        exact="exact",
                        prefix="prefix",
                        range=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty(
                            end=123,
                            start=123
                        ),
                        regex="regex",
                        suffix="suffix"
                    ),
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__40c869f289d76ad24fd802ea67417e00b60c18dd28bda825231cb5e7fe0d04cb)
                check_type(argname="argument invert", value=invert, expected_type=type_hints["invert"])
                check_type(argname="argument match", value=match, expected_type=type_hints["match"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if invert is not None:
                self._values["invert"] = invert
            if match is not None:
                self._values["match"] = match
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def invert(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specify ``True`` to match anything except the match criteria.

            The default value is ``False`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayrouteheader.html#cfn-appmesh-gatewayroute-httpgatewayrouteheader-invert
            '''
            result = self._values.get("invert")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def match(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderMatchProperty"]]:
            '''An object that represents the method and value to match with the header value sent in a request.

            Specify one match method.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayrouteheader.html#cfn-appmesh-gatewayroute-httpgatewayrouteheader-match
            '''
            result = self._values.get("match")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderMatchProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''A name for the HTTP header in the gateway route that will be matched on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayrouteheader.html#cfn-appmesh-gatewayroute-httpgatewayrouteheader-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpGatewayRouteHeaderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteMatchProperty",
        jsii_struct_bases=[],
        name_mapping={
            "headers": "headers",
            "hostname": "hostname",
            "method": "method",
            "path": "path",
            "port": "port",
            "prefix": "prefix",
            "query_parameters": "queryParameters",
        },
    )
    class HttpGatewayRouteMatchProperty:
        def __init__(
            self,
            *,
            headers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            hostname: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.GatewayRouteHostnameMatchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            method: typing.Optional[builtins.str] = None,
            path: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.HttpPathMatchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            port: typing.Optional[jsii.Number] = None,
            prefix: typing.Optional[builtins.str] = None,
            query_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.QueryParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''An object that represents the criteria for determining a request match.

            :param headers: The client request headers to match on.
            :param hostname: The host name to match on.
            :param method: The method to match on.
            :param path: The path to match on.
            :param port: The port number to match on.
            :param prefix: Specifies the path to match requests with. This parameter must always start with ``/`` , which by itself matches all requests to the virtual service name. You can also match for path-based routing of requests. For example, if your virtual service name is ``my-service.local`` and you want the route to match requests to ``my-service.local/metrics`` , your prefix should be ``/metrics`` .
            :param query_parameters: The query parameter to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayroutematch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                http_gateway_route_match_property = appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteMatchProperty(
                    headers=[appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderProperty(
                        invert=False,
                        match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderMatchProperty(
                            exact="exact",
                            prefix="prefix",
                            range=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty(
                                end=123,
                                start=123
                            ),
                            regex="regex",
                            suffix="suffix"
                        ),
                        name="name"
                    )],
                    hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameMatchProperty(
                        exact="exact",
                        suffix="suffix"
                    ),
                    method="method",
                    path=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpPathMatchProperty(
                        exact="exact",
                        regex="regex"
                    ),
                    port=123,
                    prefix="prefix",
                    query_parameters=[appmesh_mixins.CfnGatewayRoutePropsMixin.QueryParameterProperty(
                        match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpQueryParameterMatchProperty(
                            exact="exact"
                        ),
                        name="name"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e484985e46dfe5059ea5c4169c64547e91e31a8d98a03d967fdb16c07305f055)
                check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
                check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
                check_type(argname="argument method", value=method, expected_type=type_hints["method"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument query_parameters", value=query_parameters, expected_type=type_hints["query_parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if headers is not None:
                self._values["headers"] = headers
            if hostname is not None:
                self._values["hostname"] = hostname
            if method is not None:
                self._values["method"] = method
            if path is not None:
                self._values["path"] = path
            if port is not None:
                self._values["port"] = port
            if prefix is not None:
                self._values["prefix"] = prefix
            if query_parameters is not None:
                self._values["query_parameters"] = query_parameters

        @builtins.property
        def headers(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderProperty"]]]]:
            '''The client request headers to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayroutematch.html#cfn-appmesh-gatewayroute-httpgatewayroutematch-headers
            '''
            result = self._values.get("headers")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderProperty"]]]], result)

        @builtins.property
        def hostname(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GatewayRouteHostnameMatchProperty"]]:
            '''The host name to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayroutematch.html#cfn-appmesh-gatewayroute-httpgatewayroutematch-hostname
            '''
            result = self._values.get("hostname")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GatewayRouteHostnameMatchProperty"]], result)

        @builtins.property
        def method(self) -> typing.Optional[builtins.str]:
            '''The method to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayroutematch.html#cfn-appmesh-gatewayroute-httpgatewayroutematch-method
            '''
            result = self._values.get("method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def path(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.HttpPathMatchProperty"]]:
            '''The path to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayroutematch.html#cfn-appmesh-gatewayroute-httpgatewayroutematch-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.HttpPathMatchProperty"]], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port number to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayroutematch.html#cfn-appmesh-gatewayroute-httpgatewayroutematch-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''Specifies the path to match requests with.

            This parameter must always start with ``/`` , which by itself matches all requests to the virtual service name. You can also match for path-based routing of requests. For example, if your virtual service name is ``my-service.local`` and you want the route to match requests to ``my-service.local/metrics`` , your prefix should be ``/metrics`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayroutematch.html#cfn-appmesh-gatewayroute-httpgatewayroutematch-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def query_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.QueryParameterProperty"]]]]:
            '''The query parameter to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayroutematch.html#cfn-appmesh-gatewayroute-httpgatewayroutematch-queryparameters
            '''
            result = self._values.get("query_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.QueryParameterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpGatewayRouteMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRoutePropsMixin.HttpGatewayRoutePathRewriteProperty",
        jsii_struct_bases=[],
        name_mapping={"exact": "exact"},
    )
    class HttpGatewayRoutePathRewriteProperty:
        def __init__(self, *, exact: typing.Optional[builtins.str] = None) -> None:
            '''An object that represents the path to rewrite.

            :param exact: The exact path to rewrite.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayroutepathrewrite.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                http_gateway_route_path_rewrite_property = appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRoutePathRewriteProperty(
                    exact="exact"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__41ee552e5eadbfaa9486e7824612c936f5518f2eb41c2127ab68fae2ac493797)
                check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exact is not None:
                self._values["exact"] = exact

        @builtins.property
        def exact(self) -> typing.Optional[builtins.str]:
            '''The exact path to rewrite.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayroutepathrewrite.html#cfn-appmesh-gatewayroute-httpgatewayroutepathrewrite-exact
            '''
            result = self._values.get("exact")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpGatewayRoutePathRewriteProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRoutePropsMixin.HttpGatewayRoutePrefixRewriteProperty",
        jsii_struct_bases=[],
        name_mapping={"default_prefix": "defaultPrefix", "value": "value"},
    )
    class HttpGatewayRoutePrefixRewriteProperty:
        def __init__(
            self,
            *,
            default_prefix: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object representing the beginning characters of the route to rewrite.

            :param default_prefix: The default prefix used to replace the incoming route prefix when rewritten.
            :param value: The value used to replace the incoming route prefix when rewritten.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayrouteprefixrewrite.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                http_gateway_route_prefix_rewrite_property = appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRoutePrefixRewriteProperty(
                    default_prefix="defaultPrefix",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ba5921c074e3cbe5adb35393fb7d26b7bc5a70fef2033904fc4d728c72ffd1df)
                check_type(argname="argument default_prefix", value=default_prefix, expected_type=type_hints["default_prefix"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_prefix is not None:
                self._values["default_prefix"] = default_prefix
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def default_prefix(self) -> typing.Optional[builtins.str]:
            '''The default prefix used to replace the incoming route prefix when rewritten.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayrouteprefixrewrite.html#cfn-appmesh-gatewayroute-httpgatewayrouteprefixrewrite-defaultprefix
            '''
            result = self._values.get("default_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value used to replace the incoming route prefix when rewritten.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayrouteprefixrewrite.html#cfn-appmesh-gatewayroute-httpgatewayrouteprefixrewrite-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpGatewayRoutePrefixRewriteProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action", "match": "match"},
    )
    class HttpGatewayRouteProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.HttpGatewayRouteActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.HttpGatewayRouteMatchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents an HTTP gateway route.

            :param action: An object that represents the action to take if a match is determined.
            :param match: An object that represents the criteria for determining a request match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayroute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                http_gateway_route_property = appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteProperty(
                    action=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteActionProperty(
                        rewrite=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteRewriteProperty(
                            hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty(
                                default_target_hostname="defaultTargetHostname"
                            ),
                            path=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRoutePathRewriteProperty(
                                exact="exact"
                            ),
                            prefix=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRoutePrefixRewriteProperty(
                                default_prefix="defaultPrefix",
                                value="value"
                            )
                        ),
                        target=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteTargetProperty(
                            port=123,
                            virtual_service=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteVirtualServiceProperty(
                                virtual_service_name="virtualServiceName"
                            )
                        )
                    ),
                    match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteMatchProperty(
                        headers=[appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderProperty(
                            invert=False,
                            match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderMatchProperty(
                                exact="exact",
                                prefix="prefix",
                                range=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty(
                                    end=123,
                                    start=123
                                ),
                                regex="regex",
                                suffix="suffix"
                            ),
                            name="name"
                        )],
                        hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameMatchProperty(
                            exact="exact",
                            suffix="suffix"
                        ),
                        method="method",
                        path=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpPathMatchProperty(
                            exact="exact",
                            regex="regex"
                        ),
                        port=123,
                        prefix="prefix",
                        query_parameters=[appmesh_mixins.CfnGatewayRoutePropsMixin.QueryParameterProperty(
                            match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpQueryParameterMatchProperty(
                                exact="exact"
                            ),
                            name="name"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__584426435c8e1fe53b80bb6669d777a3775afa420766e2ec6a898388413d135a)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if match is not None:
                self._values["match"] = match

        @builtins.property
        def action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.HttpGatewayRouteActionProperty"]]:
            '''An object that represents the action to take if a match is determined.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayroute.html#cfn-appmesh-gatewayroute-httpgatewayroute-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.HttpGatewayRouteActionProperty"]], result)

        @builtins.property
        def match(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.HttpGatewayRouteMatchProperty"]]:
            '''An object that represents the criteria for determining a request match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayroute.html#cfn-appmesh-gatewayroute-httpgatewayroute-match
            '''
            result = self._values.get("match")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.HttpGatewayRouteMatchProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpGatewayRouteProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteRewriteProperty",
        jsii_struct_bases=[],
        name_mapping={"hostname": "hostname", "path": "path", "prefix": "prefix"},
    )
    class HttpGatewayRouteRewriteProperty:
        def __init__(
            self,
            *,
            hostname: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            path: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.HttpGatewayRoutePathRewriteProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            prefix: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.HttpGatewayRoutePrefixRewriteProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object representing the gateway route to rewrite.

            :param hostname: The host name to rewrite.
            :param path: The path to rewrite.
            :param prefix: The specified beginning characters to rewrite.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayrouterewrite.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                http_gateway_route_rewrite_property = appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRouteRewriteProperty(
                    hostname=appmesh_mixins.CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty(
                        default_target_hostname="defaultTargetHostname"
                    ),
                    path=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRoutePathRewriteProperty(
                        exact="exact"
                    ),
                    prefix=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpGatewayRoutePrefixRewriteProperty(
                        default_prefix="defaultPrefix",
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4f834b65b4d3728bd244d982bdd6f2d4fa7220798dadf80dc9ea11d825961f45)
                check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if hostname is not None:
                self._values["hostname"] = hostname
            if path is not None:
                self._values["path"] = path
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def hostname(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty"]]:
            '''The host name to rewrite.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayrouterewrite.html#cfn-appmesh-gatewayroute-httpgatewayrouterewrite-hostname
            '''
            result = self._values.get("hostname")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty"]], result)

        @builtins.property
        def path(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.HttpGatewayRoutePathRewriteProperty"]]:
            '''The path to rewrite.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayrouterewrite.html#cfn-appmesh-gatewayroute-httpgatewayrouterewrite-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.HttpGatewayRoutePathRewriteProperty"]], result)

        @builtins.property
        def prefix(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.HttpGatewayRoutePrefixRewriteProperty"]]:
            '''The specified beginning characters to rewrite.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpgatewayrouterewrite.html#cfn-appmesh-gatewayroute-httpgatewayrouterewrite-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.HttpGatewayRoutePrefixRewriteProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpGatewayRouteRewriteProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRoutePropsMixin.HttpPathMatchProperty",
        jsii_struct_bases=[],
        name_mapping={"exact": "exact", "regex": "regex"},
    )
    class HttpPathMatchProperty:
        def __init__(
            self,
            *,
            exact: typing.Optional[builtins.str] = None,
            regex: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object representing the path to match in the request.

            :param exact: The exact path to match on.
            :param regex: The regex used to match the path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httppathmatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                http_path_match_property = appmesh_mixins.CfnGatewayRoutePropsMixin.HttpPathMatchProperty(
                    exact="exact",
                    regex="regex"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__42cff14877bf3df452c9706e1e7971708b48c22ea01ea901df8161e1a32831a9)
                check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
                check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exact is not None:
                self._values["exact"] = exact
            if regex is not None:
                self._values["regex"] = regex

        @builtins.property
        def exact(self) -> typing.Optional[builtins.str]:
            '''The exact path to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httppathmatch.html#cfn-appmesh-gatewayroute-httppathmatch-exact
            '''
            result = self._values.get("exact")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def regex(self) -> typing.Optional[builtins.str]:
            '''The regex used to match the path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httppathmatch.html#cfn-appmesh-gatewayroute-httppathmatch-regex
            '''
            result = self._values.get("regex")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpPathMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRoutePropsMixin.HttpQueryParameterMatchProperty",
        jsii_struct_bases=[],
        name_mapping={"exact": "exact"},
    )
    class HttpQueryParameterMatchProperty:
        def __init__(self, *, exact: typing.Optional[builtins.str] = None) -> None:
            '''An object representing the query parameter to match.

            :param exact: The exact query parameter to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpqueryparametermatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                http_query_parameter_match_property = appmesh_mixins.CfnGatewayRoutePropsMixin.HttpQueryParameterMatchProperty(
                    exact="exact"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__971737ac4879c289ff9ed417d1943adf958257f470d189cc43b129f6b9302a26)
                check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exact is not None:
                self._values["exact"] = exact

        @builtins.property
        def exact(self) -> typing.Optional[builtins.str]:
            '''The exact query parameter to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-httpqueryparametermatch.html#cfn-appmesh-gatewayroute-httpqueryparametermatch-exact
            '''
            result = self._values.get("exact")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpQueryParameterMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnGatewayRoutePropsMixin.QueryParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"match": "match", "name": "name"},
    )
    class QueryParameterProperty:
        def __init__(
            self,
            *,
            match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayRoutePropsMixin.HttpQueryParameterMatchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the query parameter in the request.

            :param match: The query parameter to match on.
            :param name: A name for the query parameter that will be matched on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-queryparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                query_parameter_property = appmesh_mixins.CfnGatewayRoutePropsMixin.QueryParameterProperty(
                    match=appmesh_mixins.CfnGatewayRoutePropsMixin.HttpQueryParameterMatchProperty(
                        exact="exact"
                    ),
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fc61063112ba05ef4237e6e233f26c76679e4526a3d106dc66ebc2dcdde8cee8)
                check_type(argname="argument match", value=match, expected_type=type_hints["match"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if match is not None:
                self._values["match"] = match
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def match(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.HttpQueryParameterMatchProperty"]]:
            '''The query parameter to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-queryparameter.html#cfn-appmesh-gatewayroute-queryparameter-match
            '''
            result = self._values.get("match")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayRoutePropsMixin.HttpQueryParameterMatchProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''A name for the query parameter that will be matched on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-gatewayroute-queryparameter.html#cfn-appmesh-gatewayroute-queryparameter-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueryParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnMeshMixinProps",
    jsii_struct_bases=[],
    name_mapping={"mesh_name": "meshName", "spec": "spec", "tags": "tags"},
)
class CfnMeshMixinProps:
    def __init__(
        self,
        *,
        mesh_name: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMeshPropsMixin.MeshSpecProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnMeshPropsMixin.

        :param mesh_name: The name to use for the service mesh.
        :param spec: The service mesh specification to apply.
        :param tags: Optional metadata that you can apply to the service mesh to assist with categorization and organization. Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
            
            cfn_mesh_mixin_props = appmesh_mixins.CfnMeshMixinProps(
                mesh_name="meshName",
                spec=appmesh_mixins.CfnMeshPropsMixin.MeshSpecProperty(
                    egress_filter=appmesh_mixins.CfnMeshPropsMixin.EgressFilterProperty(
                        type="type"
                    ),
                    service_discovery=appmesh_mixins.CfnMeshPropsMixin.MeshServiceDiscoveryProperty(
                        ip_preference="ipPreference"
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ede588460c02f14a65d5a08355c1e35f0b9781189d2daf3545d87b338333faa)
            check_type(argname="argument mesh_name", value=mesh_name, expected_type=type_hints["mesh_name"])
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mesh_name is not None:
            self._values["mesh_name"] = mesh_name
        if spec is not None:
            self._values["spec"] = spec
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def mesh_name(self) -> typing.Optional[builtins.str]:
        '''The name to use for the service mesh.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html#cfn-appmesh-mesh-meshname
        '''
        result = self._values.get("mesh_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spec(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMeshPropsMixin.MeshSpecProperty"]]:
        '''The service mesh specification to apply.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html#cfn-appmesh-mesh-spec
        '''
        result = self._values.get("spec")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMeshPropsMixin.MeshSpecProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Optional metadata that you can apply to the service mesh to assist with categorization and organization.

        Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html#cfn-appmesh-mesh-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMeshMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMeshPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnMeshPropsMixin",
):
    '''Creates a service mesh.

    A service mesh is a logical boundary for network traffic between services that are represented by resources within the mesh. After you create your service mesh, you can create virtual services, virtual nodes, virtual routers, and routes to distribute traffic between the applications in your mesh.

    For more information about service meshes, see `Service meshes <https://docs.aws.amazon.com/app-mesh/latest/userguide/meshes.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html
    :cloudformationResource: AWS::AppMesh::Mesh
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
        
        cfn_mesh_props_mixin = appmesh_mixins.CfnMeshPropsMixin(appmesh_mixins.CfnMeshMixinProps(
            mesh_name="meshName",
            spec=appmesh_mixins.CfnMeshPropsMixin.MeshSpecProperty(
                egress_filter=appmesh_mixins.CfnMeshPropsMixin.EgressFilterProperty(
                    type="type"
                ),
                service_discovery=appmesh_mixins.CfnMeshPropsMixin.MeshServiceDiscoveryProperty(
                    ip_preference="ipPreference"
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
        props: typing.Union[CfnMeshMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppMesh::Mesh``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38988e149440e331305117981b0163aac32331899fa0dfecdf03d9b6d7639e04)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e24d4fc2d18e51dc70aa7fc6a8c9ff2980fcf5eda014d1400112ba7e0baec65d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dad8738b17f3c4d095489e3a2f86f6ce09b943b371fa39a5d83f8b91f5e8f119)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMeshMixinProps:
        return typing.cast(CfnMeshMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnMeshPropsMixin.EgressFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type"},
    )
    class EgressFilterProperty:
        def __init__(self, *, type: typing.Optional[builtins.str] = None) -> None:
            '''An object that represents the egress filter rules for a service mesh.

            :param type: The egress filter type. By default, the type is ``DROP_ALL`` , which allows egress only from virtual nodes to other defined resources in the service mesh (and any traffic to ``*.amazonaws.com`` for AWS API calls). You can set the egress filter type to ``ALLOW_ALL`` to allow egress to any endpoint inside or outside of the service mesh. .. epigraph:: If you specify any backends on a virtual node when using ``ALLOW_ALL`` , you must specifiy all egress for that virtual node as backends. Otherwise, ``ALLOW_ALL`` will no longer work for that virtual node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-egressfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                egress_filter_property = appmesh_mixins.CfnMeshPropsMixin.EgressFilterProperty(
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__247c8d72590c3d60b581a988314731c8c3b736fe1a3b39d0c2fe62f020ecaac9)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The egress filter type.

            By default, the type is ``DROP_ALL`` , which allows egress only from virtual nodes to other defined resources in the service mesh (and any traffic to ``*.amazonaws.com`` for AWS API calls). You can set the egress filter type to ``ALLOW_ALL`` to allow egress to any endpoint inside or outside of the service mesh.
            .. epigraph::

               If you specify any backends on a virtual node when using ``ALLOW_ALL`` , you must specifiy all egress for that virtual node as backends. Otherwise, ``ALLOW_ALL`` will no longer work for that virtual node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-egressfilter.html#cfn-appmesh-mesh-egressfilter-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EgressFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnMeshPropsMixin.MeshServiceDiscoveryProperty",
        jsii_struct_bases=[],
        name_mapping={"ip_preference": "ipPreference"},
    )
    class MeshServiceDiscoveryProperty:
        def __init__(
            self,
            *,
            ip_preference: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the service discovery information for a service mesh.

            :param ip_preference: The IP version to use to control traffic within the mesh.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-meshservicediscovery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                mesh_service_discovery_property = appmesh_mixins.CfnMeshPropsMixin.MeshServiceDiscoveryProperty(
                    ip_preference="ipPreference"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__420e85c30af43109e64606d3de454108e54dad7d2405f4e31607248ef6af0656)
                check_type(argname="argument ip_preference", value=ip_preference, expected_type=type_hints["ip_preference"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ip_preference is not None:
                self._values["ip_preference"] = ip_preference

        @builtins.property
        def ip_preference(self) -> typing.Optional[builtins.str]:
            '''The IP version to use to control traffic within the mesh.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-meshservicediscovery.html#cfn-appmesh-mesh-meshservicediscovery-ippreference
            '''
            result = self._values.get("ip_preference")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MeshServiceDiscoveryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnMeshPropsMixin.MeshSpecProperty",
        jsii_struct_bases=[],
        name_mapping={
            "egress_filter": "egressFilter",
            "service_discovery": "serviceDiscovery",
        },
    )
    class MeshSpecProperty:
        def __init__(
            self,
            *,
            egress_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMeshPropsMixin.EgressFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            service_discovery: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMeshPropsMixin.MeshServiceDiscoveryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents the specification of a service mesh.

            :param egress_filter: The egress filter rules for the service mesh.
            :param service_discovery: An object that represents the service discovery information for a service mesh.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-meshspec.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                mesh_spec_property = appmesh_mixins.CfnMeshPropsMixin.MeshSpecProperty(
                    egress_filter=appmesh_mixins.CfnMeshPropsMixin.EgressFilterProperty(
                        type="type"
                    ),
                    service_discovery=appmesh_mixins.CfnMeshPropsMixin.MeshServiceDiscoveryProperty(
                        ip_preference="ipPreference"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ada24799cffe2f70dd3ae1a628145539ec1364546be71000b7e5917e51b2d9ec)
                check_type(argname="argument egress_filter", value=egress_filter, expected_type=type_hints["egress_filter"])
                check_type(argname="argument service_discovery", value=service_discovery, expected_type=type_hints["service_discovery"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if egress_filter is not None:
                self._values["egress_filter"] = egress_filter
            if service_discovery is not None:
                self._values["service_discovery"] = service_discovery

        @builtins.property
        def egress_filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMeshPropsMixin.EgressFilterProperty"]]:
            '''The egress filter rules for the service mesh.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-meshspec.html#cfn-appmesh-mesh-meshspec-egressfilter
            '''
            result = self._values.get("egress_filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMeshPropsMixin.EgressFilterProperty"]], result)

        @builtins.property
        def service_discovery(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMeshPropsMixin.MeshServiceDiscoveryProperty"]]:
            '''An object that represents the service discovery information for a service mesh.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-meshspec.html#cfn-appmesh-mesh-meshspec-servicediscovery
            '''
            result = self._values.get("service_discovery")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMeshPropsMixin.MeshServiceDiscoveryProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MeshSpecProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRouteMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "mesh_name": "meshName",
        "mesh_owner": "meshOwner",
        "route_name": "routeName",
        "spec": "spec",
        "tags": "tags",
        "virtual_router_name": "virtualRouterName",
    },
)
class CfnRouteMixinProps:
    def __init__(
        self,
        *,
        mesh_name: typing.Optional[builtins.str] = None,
        mesh_owner: typing.Optional[builtins.str] = None,
        route_name: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.RouteSpecProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        virtual_router_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnRoutePropsMixin.

        :param mesh_name: The name of the service mesh to create the route in.
        :param mesh_owner: The AWS IAM account ID of the service mesh owner. If the account ID is not your own, then the account that you specify must share the mesh with your account before you can create the resource in the service mesh. For more information about mesh sharing, see `Working with shared meshes <https://docs.aws.amazon.com/app-mesh/latest/userguide/sharing.html>`_ .
        :param route_name: The name to use for the route.
        :param spec: The route specification to apply.
        :param tags: Optional metadata that you can apply to the route to assist with categorization and organization. Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.
        :param virtual_router_name: The name of the virtual router in which to create the route. If the virtual router is in a shared mesh, then you must be the owner of the virtual router resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
            
            cfn_route_mixin_props = appmesh_mixins.CfnRouteMixinProps(
                mesh_name="meshName",
                mesh_owner="meshOwner",
                route_name="routeName",
                spec=appmesh_mixins.CfnRoutePropsMixin.RouteSpecProperty(
                    grpc_route=appmesh_mixins.CfnRoutePropsMixin.GrpcRouteProperty(
                        action=appmesh_mixins.CfnRoutePropsMixin.GrpcRouteActionProperty(
                            weighted_targets=[appmesh_mixins.CfnRoutePropsMixin.WeightedTargetProperty(
                                port=123,
                                virtual_node="virtualNode",
                                weight=123
                            )]
                        ),
                        match=appmesh_mixins.CfnRoutePropsMixin.GrpcRouteMatchProperty(
                            metadata=[appmesh_mixins.CfnRoutePropsMixin.GrpcRouteMetadataProperty(
                                invert=False,
                                match=appmesh_mixins.CfnRoutePropsMixin.GrpcRouteMetadataMatchMethodProperty(
                                    exact="exact",
                                    prefix="prefix",
                                    range=appmesh_mixins.CfnRoutePropsMixin.MatchRangeProperty(
                                        end=123,
                                        start=123
                                    ),
                                    regex="regex",
                                    suffix="suffix"
                                ),
                                name="name"
                            )],
                            method_name="methodName",
                            port=123,
                            service_name="serviceName"
                        ),
                        retry_policy=appmesh_mixins.CfnRoutePropsMixin.GrpcRetryPolicyProperty(
                            grpc_retry_events=["grpcRetryEvents"],
                            http_retry_events=["httpRetryEvents"],
                            max_retries=123,
                            per_retry_timeout=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            ),
                            tcp_retry_events=["tcpRetryEvents"]
                        ),
                        timeout=appmesh_mixins.CfnRoutePropsMixin.GrpcTimeoutProperty(
                            idle=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            ),
                            per_request=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            )
                        )
                    ),
                    http2_route=appmesh_mixins.CfnRoutePropsMixin.HttpRouteProperty(
                        action=appmesh_mixins.CfnRoutePropsMixin.HttpRouteActionProperty(
                            weighted_targets=[appmesh_mixins.CfnRoutePropsMixin.WeightedTargetProperty(
                                port=123,
                                virtual_node="virtualNode",
                                weight=123
                            )]
                        ),
                        match=appmesh_mixins.CfnRoutePropsMixin.HttpRouteMatchProperty(
                            headers=[appmesh_mixins.CfnRoutePropsMixin.HttpRouteHeaderProperty(
                                invert=False,
                                match=appmesh_mixins.CfnRoutePropsMixin.HeaderMatchMethodProperty(
                                    exact="exact",
                                    prefix="prefix",
                                    range=appmesh_mixins.CfnRoutePropsMixin.MatchRangeProperty(
                                        end=123,
                                        start=123
                                    ),
                                    regex="regex",
                                    suffix="suffix"
                                ),
                                name="name"
                            )],
                            method="method",
                            path=appmesh_mixins.CfnRoutePropsMixin.HttpPathMatchProperty(
                                exact="exact",
                                regex="regex"
                            ),
                            port=123,
                            prefix="prefix",
                            query_parameters=[appmesh_mixins.CfnRoutePropsMixin.QueryParameterProperty(
                                match=appmesh_mixins.CfnRoutePropsMixin.HttpQueryParameterMatchProperty(
                                    exact="exact"
                                ),
                                name="name"
                            )],
                            scheme="scheme"
                        ),
                        retry_policy=appmesh_mixins.CfnRoutePropsMixin.HttpRetryPolicyProperty(
                            http_retry_events=["httpRetryEvents"],
                            max_retries=123,
                            per_retry_timeout=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            ),
                            tcp_retry_events=["tcpRetryEvents"]
                        ),
                        timeout=appmesh_mixins.CfnRoutePropsMixin.HttpTimeoutProperty(
                            idle=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            ),
                            per_request=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            )
                        )
                    ),
                    http_route=appmesh_mixins.CfnRoutePropsMixin.HttpRouteProperty(
                        action=appmesh_mixins.CfnRoutePropsMixin.HttpRouteActionProperty(
                            weighted_targets=[appmesh_mixins.CfnRoutePropsMixin.WeightedTargetProperty(
                                port=123,
                                virtual_node="virtualNode",
                                weight=123
                            )]
                        ),
                        match=appmesh_mixins.CfnRoutePropsMixin.HttpRouteMatchProperty(
                            headers=[appmesh_mixins.CfnRoutePropsMixin.HttpRouteHeaderProperty(
                                invert=False,
                                match=appmesh_mixins.CfnRoutePropsMixin.HeaderMatchMethodProperty(
                                    exact="exact",
                                    prefix="prefix",
                                    range=appmesh_mixins.CfnRoutePropsMixin.MatchRangeProperty(
                                        end=123,
                                        start=123
                                    ),
                                    regex="regex",
                                    suffix="suffix"
                                ),
                                name="name"
                            )],
                            method="method",
                            path=appmesh_mixins.CfnRoutePropsMixin.HttpPathMatchProperty(
                                exact="exact",
                                regex="regex"
                            ),
                            port=123,
                            prefix="prefix",
                            query_parameters=[appmesh_mixins.CfnRoutePropsMixin.QueryParameterProperty(
                                match=appmesh_mixins.CfnRoutePropsMixin.HttpQueryParameterMatchProperty(
                                    exact="exact"
                                ),
                                name="name"
                            )],
                            scheme="scheme"
                        ),
                        retry_policy=appmesh_mixins.CfnRoutePropsMixin.HttpRetryPolicyProperty(
                            http_retry_events=["httpRetryEvents"],
                            max_retries=123,
                            per_retry_timeout=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            ),
                            tcp_retry_events=["tcpRetryEvents"]
                        ),
                        timeout=appmesh_mixins.CfnRoutePropsMixin.HttpTimeoutProperty(
                            idle=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            ),
                            per_request=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            )
                        )
                    ),
                    priority=123,
                    tcp_route=appmesh_mixins.CfnRoutePropsMixin.TcpRouteProperty(
                        action=appmesh_mixins.CfnRoutePropsMixin.TcpRouteActionProperty(
                            weighted_targets=[appmesh_mixins.CfnRoutePropsMixin.WeightedTargetProperty(
                                port=123,
                                virtual_node="virtualNode",
                                weight=123
                            )]
                        ),
                        match=appmesh_mixins.CfnRoutePropsMixin.TcpRouteMatchProperty(
                            port=123
                        ),
                        timeout=appmesh_mixins.CfnRoutePropsMixin.TcpTimeoutProperty(
                            idle=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            )
                        )
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                virtual_router_name="virtualRouterName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__380dc81cd3a8ca265e7db3d5907e58d4e8315f6da184eb4b7bac7da49f0c293f)
            check_type(argname="argument mesh_name", value=mesh_name, expected_type=type_hints["mesh_name"])
            check_type(argname="argument mesh_owner", value=mesh_owner, expected_type=type_hints["mesh_owner"])
            check_type(argname="argument route_name", value=route_name, expected_type=type_hints["route_name"])
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument virtual_router_name", value=virtual_router_name, expected_type=type_hints["virtual_router_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mesh_name is not None:
            self._values["mesh_name"] = mesh_name
        if mesh_owner is not None:
            self._values["mesh_owner"] = mesh_owner
        if route_name is not None:
            self._values["route_name"] = route_name
        if spec is not None:
            self._values["spec"] = spec
        if tags is not None:
            self._values["tags"] = tags
        if virtual_router_name is not None:
            self._values["virtual_router_name"] = virtual_router_name

    @builtins.property
    def mesh_name(self) -> typing.Optional[builtins.str]:
        '''The name of the service mesh to create the route in.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-meshname
        '''
        result = self._values.get("mesh_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mesh_owner(self) -> typing.Optional[builtins.str]:
        '''The AWS IAM account ID of the service mesh owner.

        If the account ID is not your own, then the account that you specify must share the mesh with your account before you can create the resource in the service mesh. For more information about mesh sharing, see `Working with shared meshes <https://docs.aws.amazon.com/app-mesh/latest/userguide/sharing.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-meshowner
        '''
        result = self._values.get("mesh_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route_name(self) -> typing.Optional[builtins.str]:
        '''The name to use for the route.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-routename
        '''
        result = self._values.get("route_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spec(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.RouteSpecProperty"]]:
        '''The route specification to apply.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-spec
        '''
        result = self._values.get("spec")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.RouteSpecProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Optional metadata that you can apply to the route to assist with categorization and organization.

        Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def virtual_router_name(self) -> typing.Optional[builtins.str]:
        '''The name of the virtual router in which to create the route.

        If the virtual router is in a shared mesh, then you must be the owner of the virtual router resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-virtualroutername
        '''
        result = self._values.get("virtual_router_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRouteMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRoutePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin",
):
    '''Creates a route that is associated with a virtual router.

    You can route several different protocols and define a retry policy for a route. Traffic can be routed to one or more virtual nodes.

    For more information about routes, see `Routes <https://docs.aws.amazon.com/app-mesh/latest/userguide/routes.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html
    :cloudformationResource: AWS::AppMesh::Route
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
        
        cfn_route_props_mixin = appmesh_mixins.CfnRoutePropsMixin(appmesh_mixins.CfnRouteMixinProps(
            mesh_name="meshName",
            mesh_owner="meshOwner",
            route_name="routeName",
            spec=appmesh_mixins.CfnRoutePropsMixin.RouteSpecProperty(
                grpc_route=appmesh_mixins.CfnRoutePropsMixin.GrpcRouteProperty(
                    action=appmesh_mixins.CfnRoutePropsMixin.GrpcRouteActionProperty(
                        weighted_targets=[appmesh_mixins.CfnRoutePropsMixin.WeightedTargetProperty(
                            port=123,
                            virtual_node="virtualNode",
                            weight=123
                        )]
                    ),
                    match=appmesh_mixins.CfnRoutePropsMixin.GrpcRouteMatchProperty(
                        metadata=[appmesh_mixins.CfnRoutePropsMixin.GrpcRouteMetadataProperty(
                            invert=False,
                            match=appmesh_mixins.CfnRoutePropsMixin.GrpcRouteMetadataMatchMethodProperty(
                                exact="exact",
                                prefix="prefix",
                                range=appmesh_mixins.CfnRoutePropsMixin.MatchRangeProperty(
                                    end=123,
                                    start=123
                                ),
                                regex="regex",
                                suffix="suffix"
                            ),
                            name="name"
                        )],
                        method_name="methodName",
                        port=123,
                        service_name="serviceName"
                    ),
                    retry_policy=appmesh_mixins.CfnRoutePropsMixin.GrpcRetryPolicyProperty(
                        grpc_retry_events=["grpcRetryEvents"],
                        http_retry_events=["httpRetryEvents"],
                        max_retries=123,
                        per_retry_timeout=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        ),
                        tcp_retry_events=["tcpRetryEvents"]
                    ),
                    timeout=appmesh_mixins.CfnRoutePropsMixin.GrpcTimeoutProperty(
                        idle=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        ),
                        per_request=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        )
                    )
                ),
                http2_route=appmesh_mixins.CfnRoutePropsMixin.HttpRouteProperty(
                    action=appmesh_mixins.CfnRoutePropsMixin.HttpRouteActionProperty(
                        weighted_targets=[appmesh_mixins.CfnRoutePropsMixin.WeightedTargetProperty(
                            port=123,
                            virtual_node="virtualNode",
                            weight=123
                        )]
                    ),
                    match=appmesh_mixins.CfnRoutePropsMixin.HttpRouteMatchProperty(
                        headers=[appmesh_mixins.CfnRoutePropsMixin.HttpRouteHeaderProperty(
                            invert=False,
                            match=appmesh_mixins.CfnRoutePropsMixin.HeaderMatchMethodProperty(
                                exact="exact",
                                prefix="prefix",
                                range=appmesh_mixins.CfnRoutePropsMixin.MatchRangeProperty(
                                    end=123,
                                    start=123
                                ),
                                regex="regex",
                                suffix="suffix"
                            ),
                            name="name"
                        )],
                        method="method",
                        path=appmesh_mixins.CfnRoutePropsMixin.HttpPathMatchProperty(
                            exact="exact",
                            regex="regex"
                        ),
                        port=123,
                        prefix="prefix",
                        query_parameters=[appmesh_mixins.CfnRoutePropsMixin.QueryParameterProperty(
                            match=appmesh_mixins.CfnRoutePropsMixin.HttpQueryParameterMatchProperty(
                                exact="exact"
                            ),
                            name="name"
                        )],
                        scheme="scheme"
                    ),
                    retry_policy=appmesh_mixins.CfnRoutePropsMixin.HttpRetryPolicyProperty(
                        http_retry_events=["httpRetryEvents"],
                        max_retries=123,
                        per_retry_timeout=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        ),
                        tcp_retry_events=["tcpRetryEvents"]
                    ),
                    timeout=appmesh_mixins.CfnRoutePropsMixin.HttpTimeoutProperty(
                        idle=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        ),
                        per_request=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        )
                    )
                ),
                http_route=appmesh_mixins.CfnRoutePropsMixin.HttpRouteProperty(
                    action=appmesh_mixins.CfnRoutePropsMixin.HttpRouteActionProperty(
                        weighted_targets=[appmesh_mixins.CfnRoutePropsMixin.WeightedTargetProperty(
                            port=123,
                            virtual_node="virtualNode",
                            weight=123
                        )]
                    ),
                    match=appmesh_mixins.CfnRoutePropsMixin.HttpRouteMatchProperty(
                        headers=[appmesh_mixins.CfnRoutePropsMixin.HttpRouteHeaderProperty(
                            invert=False,
                            match=appmesh_mixins.CfnRoutePropsMixin.HeaderMatchMethodProperty(
                                exact="exact",
                                prefix="prefix",
                                range=appmesh_mixins.CfnRoutePropsMixin.MatchRangeProperty(
                                    end=123,
                                    start=123
                                ),
                                regex="regex",
                                suffix="suffix"
                            ),
                            name="name"
                        )],
                        method="method",
                        path=appmesh_mixins.CfnRoutePropsMixin.HttpPathMatchProperty(
                            exact="exact",
                            regex="regex"
                        ),
                        port=123,
                        prefix="prefix",
                        query_parameters=[appmesh_mixins.CfnRoutePropsMixin.QueryParameterProperty(
                            match=appmesh_mixins.CfnRoutePropsMixin.HttpQueryParameterMatchProperty(
                                exact="exact"
                            ),
                            name="name"
                        )],
                        scheme="scheme"
                    ),
                    retry_policy=appmesh_mixins.CfnRoutePropsMixin.HttpRetryPolicyProperty(
                        http_retry_events=["httpRetryEvents"],
                        max_retries=123,
                        per_retry_timeout=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        ),
                        tcp_retry_events=["tcpRetryEvents"]
                    ),
                    timeout=appmesh_mixins.CfnRoutePropsMixin.HttpTimeoutProperty(
                        idle=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        ),
                        per_request=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        )
                    )
                ),
                priority=123,
                tcp_route=appmesh_mixins.CfnRoutePropsMixin.TcpRouteProperty(
                    action=appmesh_mixins.CfnRoutePropsMixin.TcpRouteActionProperty(
                        weighted_targets=[appmesh_mixins.CfnRoutePropsMixin.WeightedTargetProperty(
                            port=123,
                            virtual_node="virtualNode",
                            weight=123
                        )]
                    ),
                    match=appmesh_mixins.CfnRoutePropsMixin.TcpRouteMatchProperty(
                        port=123
                    ),
                    timeout=appmesh_mixins.CfnRoutePropsMixin.TcpTimeoutProperty(
                        idle=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        )
                    )
                )
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            virtual_router_name="virtualRouterName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRouteMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppMesh::Route``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2ace25a5fbe16cbb365b0c047337a65dc5675b8962d8c3c20dca0a9c43a9320)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9840fac11943daaedeed56900f2fa43b14dd85ccc93a3aead15205ebb6a712b2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d6729a0eeead997d1d959ccece17867809b05e964aef02af2439d289fcb3771)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRouteMixinProps:
        return typing.cast(CfnRouteMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.DurationProperty",
        jsii_struct_bases=[],
        name_mapping={"unit": "unit", "value": "value"},
    )
    class DurationProperty:
        def __init__(
            self,
            *,
            unit: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An object that represents a duration of time.

            :param unit: A unit of time.
            :param value: A number of time units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-duration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                duration_property = appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                    unit="unit",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f9739fe72b9053b266b9558682b97664b473da34cac8ef11b9e338484d0ca1d7)
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if unit is not None:
                self._values["unit"] = unit
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''A unit of time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-duration.html#cfn-appmesh-route-duration-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''A number of time units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-duration.html#cfn-appmesh-route-duration-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.GrpcRetryPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "grpc_retry_events": "grpcRetryEvents",
            "http_retry_events": "httpRetryEvents",
            "max_retries": "maxRetries",
            "per_retry_timeout": "perRetryTimeout",
            "tcp_retry_events": "tcpRetryEvents",
        },
    )
    class GrpcRetryPolicyProperty:
        def __init__(
            self,
            *,
            grpc_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
            http_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
            max_retries: typing.Optional[jsii.Number] = None,
            per_retry_timeout: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.DurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            tcp_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''An object that represents a retry policy.

            Specify at least one value for at least one of the types of ``RetryEvents`` , a value for ``maxRetries`` , and a value for ``perRetryTimeout`` . Both ``server-error`` and ``gateway-error`` under ``httpRetryEvents`` include the Envoy ``reset`` policy. For more information on the ``reset`` policy, see the `Envoy documentation <https://docs.aws.amazon.com/https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/router_filter#x-envoy-retry-on>`_ .

            :param grpc_retry_events: Specify at least one of the valid values.
            :param http_retry_events: Specify at least one of the following values. - *server-error* – HTTP status codes 500, 501, 502, 503, 504, 505, 506, 507, 508, 510, and 511 - *gateway-error* – HTTP status codes 502, 503, and 504 - *client-error* – HTTP status code 409 - *stream-error* – Retry on refused stream
            :param max_retries: The maximum number of retry attempts.
            :param per_retry_timeout: The timeout for each retry attempt.
            :param tcp_retry_events: Specify a valid value. The event occurs before any processing of a request has started and is encountered when the upstream is temporarily or permanently unavailable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcretrypolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                grpc_retry_policy_property = appmesh_mixins.CfnRoutePropsMixin.GrpcRetryPolicyProperty(
                    grpc_retry_events=["grpcRetryEvents"],
                    http_retry_events=["httpRetryEvents"],
                    max_retries=123,
                    per_retry_timeout=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                        unit="unit",
                        value=123
                    ),
                    tcp_retry_events=["tcpRetryEvents"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__534f2777100a90426395c1c15b0bb009037fbd3d3da2fb4ee0583a74c6ddedb3)
                check_type(argname="argument grpc_retry_events", value=grpc_retry_events, expected_type=type_hints["grpc_retry_events"])
                check_type(argname="argument http_retry_events", value=http_retry_events, expected_type=type_hints["http_retry_events"])
                check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
                check_type(argname="argument per_retry_timeout", value=per_retry_timeout, expected_type=type_hints["per_retry_timeout"])
                check_type(argname="argument tcp_retry_events", value=tcp_retry_events, expected_type=type_hints["tcp_retry_events"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if grpc_retry_events is not None:
                self._values["grpc_retry_events"] = grpc_retry_events
            if http_retry_events is not None:
                self._values["http_retry_events"] = http_retry_events
            if max_retries is not None:
                self._values["max_retries"] = max_retries
            if per_retry_timeout is not None:
                self._values["per_retry_timeout"] = per_retry_timeout
            if tcp_retry_events is not None:
                self._values["tcp_retry_events"] = tcp_retry_events

        @builtins.property
        def grpc_retry_events(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specify at least one of the valid values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcretrypolicy.html#cfn-appmesh-route-grpcretrypolicy-grpcretryevents
            '''
            result = self._values.get("grpc_retry_events")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def http_retry_events(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specify at least one of the following values.

            - *server-error* – HTTP status codes 500, 501, 502, 503, 504, 505, 506, 507, 508, 510, and 511
            - *gateway-error* – HTTP status codes 502, 503, and 504
            - *client-error* – HTTP status code 409
            - *stream-error* – Retry on refused stream

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcretrypolicy.html#cfn-appmesh-route-grpcretrypolicy-httpretryevents
            '''
            result = self._values.get("http_retry_events")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def max_retries(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of retry attempts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcretrypolicy.html#cfn-appmesh-route-grpcretrypolicy-maxretries
            '''
            result = self._values.get("max_retries")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def per_retry_timeout(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.DurationProperty"]]:
            '''The timeout for each retry attempt.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcretrypolicy.html#cfn-appmesh-route-grpcretrypolicy-perretrytimeout
            '''
            result = self._values.get("per_retry_timeout")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.DurationProperty"]], result)

        @builtins.property
        def tcp_retry_events(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specify a valid value.

            The event occurs before any processing of a request has started and is encountered when the upstream is temporarily or permanently unavailable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcretrypolicy.html#cfn-appmesh-route-grpcretrypolicy-tcpretryevents
            '''
            result = self._values.get("tcp_retry_events")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrpcRetryPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.GrpcRouteActionProperty",
        jsii_struct_bases=[],
        name_mapping={"weighted_targets": "weightedTargets"},
    )
    class GrpcRouteActionProperty:
        def __init__(
            self,
            *,
            weighted_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.WeightedTargetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''An object that represents the action to take if a match is determined.

            :param weighted_targets: An object that represents the targets that traffic is routed to when a request matches the route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcrouteaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                grpc_route_action_property = appmesh_mixins.CfnRoutePropsMixin.GrpcRouteActionProperty(
                    weighted_targets=[appmesh_mixins.CfnRoutePropsMixin.WeightedTargetProperty(
                        port=123,
                        virtual_node="virtualNode",
                        weight=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2a9f1b261c2f7ff65b0d808955cd61314656539cac5423c1ee5f7294a2c6bf36)
                check_type(argname="argument weighted_targets", value=weighted_targets, expected_type=type_hints["weighted_targets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if weighted_targets is not None:
                self._values["weighted_targets"] = weighted_targets

        @builtins.property
        def weighted_targets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.WeightedTargetProperty"]]]]:
            '''An object that represents the targets that traffic is routed to when a request matches the route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcrouteaction.html#cfn-appmesh-route-grpcrouteaction-weightedtargets
            '''
            result = self._values.get("weighted_targets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.WeightedTargetProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrpcRouteActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.GrpcRouteMatchProperty",
        jsii_struct_bases=[],
        name_mapping={
            "metadata": "metadata",
            "method_name": "methodName",
            "port": "port",
            "service_name": "serviceName",
        },
    )
    class GrpcRouteMatchProperty:
        def __init__(
            self,
            *,
            metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.GrpcRouteMetadataProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            method_name: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            service_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the criteria for determining a request match.

            :param metadata: An object that represents the data to match from the request.
            :param method_name: The method name to match from the request. If you specify a name, you must also specify a ``serviceName`` .
            :param port: The port number to match on.
            :param service_name: The fully qualified domain name for the service to match from the request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutematch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                grpc_route_match_property = appmesh_mixins.CfnRoutePropsMixin.GrpcRouteMatchProperty(
                    metadata=[appmesh_mixins.CfnRoutePropsMixin.GrpcRouteMetadataProperty(
                        invert=False,
                        match=appmesh_mixins.CfnRoutePropsMixin.GrpcRouteMetadataMatchMethodProperty(
                            exact="exact",
                            prefix="prefix",
                            range=appmesh_mixins.CfnRoutePropsMixin.MatchRangeProperty(
                                end=123,
                                start=123
                            ),
                            regex="regex",
                            suffix="suffix"
                        ),
                        name="name"
                    )],
                    method_name="methodName",
                    port=123,
                    service_name="serviceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ba8a6ff32ecb6a4d80e5c960e535f2cff39e99761891fc0469b8fa21cda9ffa6)
                check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
                check_type(argname="argument method_name", value=method_name, expected_type=type_hints["method_name"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metadata is not None:
                self._values["metadata"] = metadata
            if method_name is not None:
                self._values["method_name"] = method_name
            if port is not None:
                self._values["port"] = port
            if service_name is not None:
                self._values["service_name"] = service_name

        @builtins.property
        def metadata(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.GrpcRouteMetadataProperty"]]]]:
            '''An object that represents the data to match from the request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutematch.html#cfn-appmesh-route-grpcroutematch-metadata
            '''
            result = self._values.get("metadata")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.GrpcRouteMetadataProperty"]]]], result)

        @builtins.property
        def method_name(self) -> typing.Optional[builtins.str]:
            '''The method name to match from the request.

            If you specify a name, you must also specify a ``serviceName`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutematch.html#cfn-appmesh-route-grpcroutematch-methodname
            '''
            result = self._values.get("method_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port number to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutematch.html#cfn-appmesh-route-grpcroutematch-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def service_name(self) -> typing.Optional[builtins.str]:
            '''The fully qualified domain name for the service to match from the request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutematch.html#cfn-appmesh-route-grpcroutematch-servicename
            '''
            result = self._values.get("service_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrpcRouteMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.GrpcRouteMetadataMatchMethodProperty",
        jsii_struct_bases=[],
        name_mapping={
            "exact": "exact",
            "prefix": "prefix",
            "range": "range",
            "regex": "regex",
            "suffix": "suffix",
        },
    )
    class GrpcRouteMetadataMatchMethodProperty:
        def __init__(
            self,
            *,
            exact: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
            range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.MatchRangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            regex: typing.Optional[builtins.str] = None,
            suffix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the match method.

            Specify one of the match values.

            :param exact: The value sent by the client must match the specified value exactly.
            :param prefix: The value sent by the client must begin with the specified characters.
            :param range: An object that represents the range of values to match on.
            :param regex: The value sent by the client must include the specified characters.
            :param suffix: The value sent by the client must end with the specified characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadatamatchmethod.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                grpc_route_metadata_match_method_property = appmesh_mixins.CfnRoutePropsMixin.GrpcRouteMetadataMatchMethodProperty(
                    exact="exact",
                    prefix="prefix",
                    range=appmesh_mixins.CfnRoutePropsMixin.MatchRangeProperty(
                        end=123,
                        start=123
                    ),
                    regex="regex",
                    suffix="suffix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fe1d8fa3aa5693a918069a8d878364530f46344f45f9fe7425fcd23ac60e24dc)
                check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument range", value=range, expected_type=type_hints["range"])
                check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
                check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exact is not None:
                self._values["exact"] = exact
            if prefix is not None:
                self._values["prefix"] = prefix
            if range is not None:
                self._values["range"] = range
            if regex is not None:
                self._values["regex"] = regex
            if suffix is not None:
                self._values["suffix"] = suffix

        @builtins.property
        def exact(self) -> typing.Optional[builtins.str]:
            '''The value sent by the client must match the specified value exactly.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadatamatchmethod.html#cfn-appmesh-route-grpcroutemetadatamatchmethod-exact
            '''
            result = self._values.get("exact")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''The value sent by the client must begin with the specified characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadatamatchmethod.html#cfn-appmesh-route-grpcroutemetadatamatchmethod-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def range(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.MatchRangeProperty"]]:
            '''An object that represents the range of values to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadatamatchmethod.html#cfn-appmesh-route-grpcroutemetadatamatchmethod-range
            '''
            result = self._values.get("range")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.MatchRangeProperty"]], result)

        @builtins.property
        def regex(self) -> typing.Optional[builtins.str]:
            '''The value sent by the client must include the specified characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadatamatchmethod.html#cfn-appmesh-route-grpcroutemetadatamatchmethod-regex
            '''
            result = self._values.get("regex")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def suffix(self) -> typing.Optional[builtins.str]:
            '''The value sent by the client must end with the specified characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadatamatchmethod.html#cfn-appmesh-route-grpcroutemetadatamatchmethod-suffix
            '''
            result = self._values.get("suffix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrpcRouteMetadataMatchMethodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.GrpcRouteMetadataProperty",
        jsii_struct_bases=[],
        name_mapping={"invert": "invert", "match": "match", "name": "name"},
    )
    class GrpcRouteMetadataProperty:
        def __init__(
            self,
            *,
            invert: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.GrpcRouteMetadataMatchMethodProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the match metadata for the route.

            :param invert: Specify ``True`` to match anything except the match criteria. The default value is ``False`` .
            :param match: An object that represents the data to match from the request.
            :param name: The name of the route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                grpc_route_metadata_property = appmesh_mixins.CfnRoutePropsMixin.GrpcRouteMetadataProperty(
                    invert=False,
                    match=appmesh_mixins.CfnRoutePropsMixin.GrpcRouteMetadataMatchMethodProperty(
                        exact="exact",
                        prefix="prefix",
                        range=appmesh_mixins.CfnRoutePropsMixin.MatchRangeProperty(
                            end=123,
                            start=123
                        ),
                        regex="regex",
                        suffix="suffix"
                    ),
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__856862a2c802347bc125b1593a042f29e5ee7bca46127ac03464c209e8700f81)
                check_type(argname="argument invert", value=invert, expected_type=type_hints["invert"])
                check_type(argname="argument match", value=match, expected_type=type_hints["match"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if invert is not None:
                self._values["invert"] = invert
            if match is not None:
                self._values["match"] = match
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def invert(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specify ``True`` to match anything except the match criteria.

            The default value is ``False`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadata.html#cfn-appmesh-route-grpcroutemetadata-invert
            '''
            result = self._values.get("invert")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def match(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.GrpcRouteMetadataMatchMethodProperty"]]:
            '''An object that represents the data to match from the request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadata.html#cfn-appmesh-route-grpcroutemetadata-match
            '''
            result = self._values.get("match")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.GrpcRouteMetadataMatchMethodProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadata.html#cfn-appmesh-route-grpcroutemetadata-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrpcRouteMetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.GrpcRouteProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "match": "match",
            "retry_policy": "retryPolicy",
            "timeout": "timeout",
        },
    )
    class GrpcRouteProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.GrpcRouteActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.GrpcRouteMatchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            retry_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.GrpcRetryPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            timeout: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.GrpcTimeoutProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents a gRPC route type.

            :param action: An object that represents the action to take if a match is determined.
            :param match: An object that represents the criteria for determining a request match.
            :param retry_policy: An object that represents a retry policy.
            :param timeout: An object that represents types of timeouts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                grpc_route_property = appmesh_mixins.CfnRoutePropsMixin.GrpcRouteProperty(
                    action=appmesh_mixins.CfnRoutePropsMixin.GrpcRouteActionProperty(
                        weighted_targets=[appmesh_mixins.CfnRoutePropsMixin.WeightedTargetProperty(
                            port=123,
                            virtual_node="virtualNode",
                            weight=123
                        )]
                    ),
                    match=appmesh_mixins.CfnRoutePropsMixin.GrpcRouteMatchProperty(
                        metadata=[appmesh_mixins.CfnRoutePropsMixin.GrpcRouteMetadataProperty(
                            invert=False,
                            match=appmesh_mixins.CfnRoutePropsMixin.GrpcRouteMetadataMatchMethodProperty(
                                exact="exact",
                                prefix="prefix",
                                range=appmesh_mixins.CfnRoutePropsMixin.MatchRangeProperty(
                                    end=123,
                                    start=123
                                ),
                                regex="regex",
                                suffix="suffix"
                            ),
                            name="name"
                        )],
                        method_name="methodName",
                        port=123,
                        service_name="serviceName"
                    ),
                    retry_policy=appmesh_mixins.CfnRoutePropsMixin.GrpcRetryPolicyProperty(
                        grpc_retry_events=["grpcRetryEvents"],
                        http_retry_events=["httpRetryEvents"],
                        max_retries=123,
                        per_retry_timeout=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        ),
                        tcp_retry_events=["tcpRetryEvents"]
                    ),
                    timeout=appmesh_mixins.CfnRoutePropsMixin.GrpcTimeoutProperty(
                        idle=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        ),
                        per_request=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fd126076857fa450bd1ed943a84eb2e5fdb352a5d26cfd11a516e18b06286b57)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument match", value=match, expected_type=type_hints["match"])
                check_type(argname="argument retry_policy", value=retry_policy, expected_type=type_hints["retry_policy"])
                check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if match is not None:
                self._values["match"] = match
            if retry_policy is not None:
                self._values["retry_policy"] = retry_policy
            if timeout is not None:
                self._values["timeout"] = timeout

        @builtins.property
        def action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.GrpcRouteActionProperty"]]:
            '''An object that represents the action to take if a match is determined.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroute.html#cfn-appmesh-route-grpcroute-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.GrpcRouteActionProperty"]], result)

        @builtins.property
        def match(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.GrpcRouteMatchProperty"]]:
            '''An object that represents the criteria for determining a request match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroute.html#cfn-appmesh-route-grpcroute-match
            '''
            result = self._values.get("match")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.GrpcRouteMatchProperty"]], result)

        @builtins.property
        def retry_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.GrpcRetryPolicyProperty"]]:
            '''An object that represents a retry policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroute.html#cfn-appmesh-route-grpcroute-retrypolicy
            '''
            result = self._values.get("retry_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.GrpcRetryPolicyProperty"]], result)

        @builtins.property
        def timeout(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.GrpcTimeoutProperty"]]:
            '''An object that represents types of timeouts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroute.html#cfn-appmesh-route-grpcroute-timeout
            '''
            result = self._values.get("timeout")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.GrpcTimeoutProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrpcRouteProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.GrpcTimeoutProperty",
        jsii_struct_bases=[],
        name_mapping={"idle": "idle", "per_request": "perRequest"},
    )
    class GrpcTimeoutProperty:
        def __init__(
            self,
            *,
            idle: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.DurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            per_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.DurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents types of timeouts.

            :param idle: An object that represents an idle timeout. An idle timeout bounds the amount of time that a connection may be idle. The default value is none.
            :param per_request: An object that represents a per request timeout. The default value is 15 seconds. If you set a higher timeout, then make sure that the higher value is set for each App Mesh resource in a conversation. For example, if a virtual node backend uses a virtual router provider to route to another virtual node, then the timeout should be greater than 15 seconds for the source and destination virtual node and the route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpctimeout.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                grpc_timeout_property = appmesh_mixins.CfnRoutePropsMixin.GrpcTimeoutProperty(
                    idle=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                        unit="unit",
                        value=123
                    ),
                    per_request=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                        unit="unit",
                        value=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fdc78059caf2e60ddcd161336c6264cce762998af9c2a973f30f7f5192b954f3)
                check_type(argname="argument idle", value=idle, expected_type=type_hints["idle"])
                check_type(argname="argument per_request", value=per_request, expected_type=type_hints["per_request"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if idle is not None:
                self._values["idle"] = idle
            if per_request is not None:
                self._values["per_request"] = per_request

        @builtins.property
        def idle(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.DurationProperty"]]:
            '''An object that represents an idle timeout.

            An idle timeout bounds the amount of time that a connection may be idle. The default value is none.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpctimeout.html#cfn-appmesh-route-grpctimeout-idle
            '''
            result = self._values.get("idle")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.DurationProperty"]], result)

        @builtins.property
        def per_request(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.DurationProperty"]]:
            '''An object that represents a per request timeout.

            The default value is 15 seconds. If you set a higher timeout, then make sure that the higher value is set for each App Mesh resource in a conversation. For example, if a virtual node backend uses a virtual router provider to route to another virtual node, then the timeout should be greater than 15 seconds for the source and destination virtual node and the route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpctimeout.html#cfn-appmesh-route-grpctimeout-perrequest
            '''
            result = self._values.get("per_request")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.DurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrpcTimeoutProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.HeaderMatchMethodProperty",
        jsii_struct_bases=[],
        name_mapping={
            "exact": "exact",
            "prefix": "prefix",
            "range": "range",
            "regex": "regex",
            "suffix": "suffix",
        },
    )
    class HeaderMatchMethodProperty:
        def __init__(
            self,
            *,
            exact: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
            range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.MatchRangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            regex: typing.Optional[builtins.str] = None,
            suffix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the method and value to match with the header value sent in a request.

            Specify one match method.

            :param exact: The value sent by the client must match the specified value exactly.
            :param prefix: The value sent by the client must begin with the specified characters.
            :param range: An object that represents the range of values to match on.
            :param regex: The value sent by the client must include the specified characters.
            :param suffix: The value sent by the client must end with the specified characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-headermatchmethod.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                header_match_method_property = appmesh_mixins.CfnRoutePropsMixin.HeaderMatchMethodProperty(
                    exact="exact",
                    prefix="prefix",
                    range=appmesh_mixins.CfnRoutePropsMixin.MatchRangeProperty(
                        end=123,
                        start=123
                    ),
                    regex="regex",
                    suffix="suffix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7b443f29d591e03dc7e0be1dfb72bff3d845970069e2738f8e64010ed1d44834)
                check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument range", value=range, expected_type=type_hints["range"])
                check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
                check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exact is not None:
                self._values["exact"] = exact
            if prefix is not None:
                self._values["prefix"] = prefix
            if range is not None:
                self._values["range"] = range
            if regex is not None:
                self._values["regex"] = regex
            if suffix is not None:
                self._values["suffix"] = suffix

        @builtins.property
        def exact(self) -> typing.Optional[builtins.str]:
            '''The value sent by the client must match the specified value exactly.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-headermatchmethod.html#cfn-appmesh-route-headermatchmethod-exact
            '''
            result = self._values.get("exact")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''The value sent by the client must begin with the specified characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-headermatchmethod.html#cfn-appmesh-route-headermatchmethod-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def range(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.MatchRangeProperty"]]:
            '''An object that represents the range of values to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-headermatchmethod.html#cfn-appmesh-route-headermatchmethod-range
            '''
            result = self._values.get("range")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.MatchRangeProperty"]], result)

        @builtins.property
        def regex(self) -> typing.Optional[builtins.str]:
            '''The value sent by the client must include the specified characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-headermatchmethod.html#cfn-appmesh-route-headermatchmethod-regex
            '''
            result = self._values.get("regex")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def suffix(self) -> typing.Optional[builtins.str]:
            '''The value sent by the client must end with the specified characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-headermatchmethod.html#cfn-appmesh-route-headermatchmethod-suffix
            '''
            result = self._values.get("suffix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HeaderMatchMethodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.HttpPathMatchProperty",
        jsii_struct_bases=[],
        name_mapping={"exact": "exact", "regex": "regex"},
    )
    class HttpPathMatchProperty:
        def __init__(
            self,
            *,
            exact: typing.Optional[builtins.str] = None,
            regex: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object representing the path to match in the request.

            :param exact: The exact path to match on.
            :param regex: The regex used to match the path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httppathmatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                http_path_match_property = appmesh_mixins.CfnRoutePropsMixin.HttpPathMatchProperty(
                    exact="exact",
                    regex="regex"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c1d6d14bf06eeec0d9a61b2e2283c0f869d5ca67287c0c9156321ac2ed1e749f)
                check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
                check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exact is not None:
                self._values["exact"] = exact
            if regex is not None:
                self._values["regex"] = regex

        @builtins.property
        def exact(self) -> typing.Optional[builtins.str]:
            '''The exact path to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httppathmatch.html#cfn-appmesh-route-httppathmatch-exact
            '''
            result = self._values.get("exact")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def regex(self) -> typing.Optional[builtins.str]:
            '''The regex used to match the path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httppathmatch.html#cfn-appmesh-route-httppathmatch-regex
            '''
            result = self._values.get("regex")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpPathMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.HttpQueryParameterMatchProperty",
        jsii_struct_bases=[],
        name_mapping={"exact": "exact"},
    )
    class HttpQueryParameterMatchProperty:
        def __init__(self, *, exact: typing.Optional[builtins.str] = None) -> None:
            '''An object representing the query parameter to match.

            :param exact: The exact query parameter to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httpqueryparametermatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                http_query_parameter_match_property = appmesh_mixins.CfnRoutePropsMixin.HttpQueryParameterMatchProperty(
                    exact="exact"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2d052604a1bc5ceef83c2701f45eb7a2be1a2c3088484a88104b99e69cc2630e)
                check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exact is not None:
                self._values["exact"] = exact

        @builtins.property
        def exact(self) -> typing.Optional[builtins.str]:
            '''The exact query parameter to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httpqueryparametermatch.html#cfn-appmesh-route-httpqueryparametermatch-exact
            '''
            result = self._values.get("exact")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpQueryParameterMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.HttpRetryPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "http_retry_events": "httpRetryEvents",
            "max_retries": "maxRetries",
            "per_retry_timeout": "perRetryTimeout",
            "tcp_retry_events": "tcpRetryEvents",
        },
    )
    class HttpRetryPolicyProperty:
        def __init__(
            self,
            *,
            http_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
            max_retries: typing.Optional[jsii.Number] = None,
            per_retry_timeout: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.DurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            tcp_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''An object that represents a retry policy.

            Specify at least one value for at least one of the types of ``RetryEvents`` , a value for ``maxRetries`` , and a value for ``perRetryTimeout`` . Both ``server-error`` and ``gateway-error`` under ``httpRetryEvents`` include the Envoy ``reset`` policy. For more information on the ``reset`` policy, see the `Envoy documentation <https://docs.aws.amazon.com/https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/router_filter#x-envoy-retry-on>`_ .

            :param http_retry_events: Specify at least one of the following values. - *server-error* – HTTP status codes 500, 501, 502, 503, 504, 505, 506, 507, 508, 510, and 511 - *gateway-error* – HTTP status codes 502, 503, and 504 - *client-error* – HTTP status code 409 - *stream-error* – Retry on refused stream
            :param max_retries: The maximum number of retry attempts.
            :param per_retry_timeout: The timeout for each retry attempt.
            :param tcp_retry_events: Specify a valid value. The event occurs before any processing of a request has started and is encountered when the upstream is temporarily or permanently unavailable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httpretrypolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                http_retry_policy_property = appmesh_mixins.CfnRoutePropsMixin.HttpRetryPolicyProperty(
                    http_retry_events=["httpRetryEvents"],
                    max_retries=123,
                    per_retry_timeout=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                        unit="unit",
                        value=123
                    ),
                    tcp_retry_events=["tcpRetryEvents"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d2bc3973892b2942553d996dba395c5f93a7a886aed811ac347853b0d444aed5)
                check_type(argname="argument http_retry_events", value=http_retry_events, expected_type=type_hints["http_retry_events"])
                check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
                check_type(argname="argument per_retry_timeout", value=per_retry_timeout, expected_type=type_hints["per_retry_timeout"])
                check_type(argname="argument tcp_retry_events", value=tcp_retry_events, expected_type=type_hints["tcp_retry_events"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if http_retry_events is not None:
                self._values["http_retry_events"] = http_retry_events
            if max_retries is not None:
                self._values["max_retries"] = max_retries
            if per_retry_timeout is not None:
                self._values["per_retry_timeout"] = per_retry_timeout
            if tcp_retry_events is not None:
                self._values["tcp_retry_events"] = tcp_retry_events

        @builtins.property
        def http_retry_events(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specify at least one of the following values.

            - *server-error* – HTTP status codes 500, 501, 502, 503, 504, 505, 506, 507, 508, 510, and 511
            - *gateway-error* – HTTP status codes 502, 503, and 504
            - *client-error* – HTTP status code 409
            - *stream-error* – Retry on refused stream

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httpretrypolicy.html#cfn-appmesh-route-httpretrypolicy-httpretryevents
            '''
            result = self._values.get("http_retry_events")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def max_retries(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of retry attempts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httpretrypolicy.html#cfn-appmesh-route-httpretrypolicy-maxretries
            '''
            result = self._values.get("max_retries")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def per_retry_timeout(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.DurationProperty"]]:
            '''The timeout for each retry attempt.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httpretrypolicy.html#cfn-appmesh-route-httpretrypolicy-perretrytimeout
            '''
            result = self._values.get("per_retry_timeout")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.DurationProperty"]], result)

        @builtins.property
        def tcp_retry_events(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specify a valid value.

            The event occurs before any processing of a request has started and is encountered when the upstream is temporarily or permanently unavailable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httpretrypolicy.html#cfn-appmesh-route-httpretrypolicy-tcpretryevents
            '''
            result = self._values.get("tcp_retry_events")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpRetryPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.HttpRouteActionProperty",
        jsii_struct_bases=[],
        name_mapping={"weighted_targets": "weightedTargets"},
    )
    class HttpRouteActionProperty:
        def __init__(
            self,
            *,
            weighted_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.WeightedTargetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''An object that represents the action to take if a match is determined.

            :param weighted_targets: An object that represents the targets that traffic is routed to when a request matches the route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httprouteaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                http_route_action_property = appmesh_mixins.CfnRoutePropsMixin.HttpRouteActionProperty(
                    weighted_targets=[appmesh_mixins.CfnRoutePropsMixin.WeightedTargetProperty(
                        port=123,
                        virtual_node="virtualNode",
                        weight=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f0f54fc69b9ec86220a891f774c462e1e7e0d04594529bbe37616c7d98f07110)
                check_type(argname="argument weighted_targets", value=weighted_targets, expected_type=type_hints["weighted_targets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if weighted_targets is not None:
                self._values["weighted_targets"] = weighted_targets

        @builtins.property
        def weighted_targets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.WeightedTargetProperty"]]]]:
            '''An object that represents the targets that traffic is routed to when a request matches the route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httprouteaction.html#cfn-appmesh-route-httprouteaction-weightedtargets
            '''
            result = self._values.get("weighted_targets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.WeightedTargetProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpRouteActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.HttpRouteHeaderProperty",
        jsii_struct_bases=[],
        name_mapping={"invert": "invert", "match": "match", "name": "name"},
    )
    class HttpRouteHeaderProperty:
        def __init__(
            self,
            *,
            invert: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.HeaderMatchMethodProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the HTTP header in the request.

            :param invert: Specify ``True`` to match anything except the match criteria. The default value is ``False`` .
            :param match: The ``HeaderMatchMethod`` object.
            :param name: A name for the HTTP header in the client request that will be matched on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httprouteheader.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                http_route_header_property = appmesh_mixins.CfnRoutePropsMixin.HttpRouteHeaderProperty(
                    invert=False,
                    match=appmesh_mixins.CfnRoutePropsMixin.HeaderMatchMethodProperty(
                        exact="exact",
                        prefix="prefix",
                        range=appmesh_mixins.CfnRoutePropsMixin.MatchRangeProperty(
                            end=123,
                            start=123
                        ),
                        regex="regex",
                        suffix="suffix"
                    ),
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b7c00db7ac1357b00f58860b6e568d5c380a7d1b56525356482fe45b023356ee)
                check_type(argname="argument invert", value=invert, expected_type=type_hints["invert"])
                check_type(argname="argument match", value=match, expected_type=type_hints["match"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if invert is not None:
                self._values["invert"] = invert
            if match is not None:
                self._values["match"] = match
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def invert(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specify ``True`` to match anything except the match criteria.

            The default value is ``False`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httprouteheader.html#cfn-appmesh-route-httprouteheader-invert
            '''
            result = self._values.get("invert")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def match(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.HeaderMatchMethodProperty"]]:
            '''The ``HeaderMatchMethod`` object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httprouteheader.html#cfn-appmesh-route-httprouteheader-match
            '''
            result = self._values.get("match")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.HeaderMatchMethodProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''A name for the HTTP header in the client request that will be matched on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httprouteheader.html#cfn-appmesh-route-httprouteheader-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpRouteHeaderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.HttpRouteMatchProperty",
        jsii_struct_bases=[],
        name_mapping={
            "headers": "headers",
            "method": "method",
            "path": "path",
            "port": "port",
            "prefix": "prefix",
            "query_parameters": "queryParameters",
            "scheme": "scheme",
        },
    )
    class HttpRouteMatchProperty:
        def __init__(
            self,
            *,
            headers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.HttpRouteHeaderProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            method: typing.Optional[builtins.str] = None,
            path: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.HttpPathMatchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            port: typing.Optional[jsii.Number] = None,
            prefix: typing.Optional[builtins.str] = None,
            query_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.QueryParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            scheme: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the requirements for a route to match HTTP requests for a virtual router.

            :param headers: The client request headers to match on.
            :param method: The client request method to match on. Specify only one.
            :param path: The client request path to match on.
            :param port: The port number to match on.
            :param prefix: Specifies the path to match requests with. This parameter must always start with ``/`` , which by itself matches all requests to the virtual service name. You can also match for path-based routing of requests. For example, if your virtual service name is ``my-service.local`` and you want the route to match requests to ``my-service.local/metrics`` , your prefix should be ``/metrics`` .
            :param query_parameters: The client request query parameters to match on.
            :param scheme: The client request scheme to match on. Specify only one. Applicable only for HTTP2 routes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproutematch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                http_route_match_property = appmesh_mixins.CfnRoutePropsMixin.HttpRouteMatchProperty(
                    headers=[appmesh_mixins.CfnRoutePropsMixin.HttpRouteHeaderProperty(
                        invert=False,
                        match=appmesh_mixins.CfnRoutePropsMixin.HeaderMatchMethodProperty(
                            exact="exact",
                            prefix="prefix",
                            range=appmesh_mixins.CfnRoutePropsMixin.MatchRangeProperty(
                                end=123,
                                start=123
                            ),
                            regex="regex",
                            suffix="suffix"
                        ),
                        name="name"
                    )],
                    method="method",
                    path=appmesh_mixins.CfnRoutePropsMixin.HttpPathMatchProperty(
                        exact="exact",
                        regex="regex"
                    ),
                    port=123,
                    prefix="prefix",
                    query_parameters=[appmesh_mixins.CfnRoutePropsMixin.QueryParameterProperty(
                        match=appmesh_mixins.CfnRoutePropsMixin.HttpQueryParameterMatchProperty(
                            exact="exact"
                        ),
                        name="name"
                    )],
                    scheme="scheme"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9a80a552d6625a1445dd867a171840b3cb800154e27ce1d80c7fbae3b5f2f949)
                check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
                check_type(argname="argument method", value=method, expected_type=type_hints["method"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument query_parameters", value=query_parameters, expected_type=type_hints["query_parameters"])
                check_type(argname="argument scheme", value=scheme, expected_type=type_hints["scheme"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if headers is not None:
                self._values["headers"] = headers
            if method is not None:
                self._values["method"] = method
            if path is not None:
                self._values["path"] = path
            if port is not None:
                self._values["port"] = port
            if prefix is not None:
                self._values["prefix"] = prefix
            if query_parameters is not None:
                self._values["query_parameters"] = query_parameters
            if scheme is not None:
                self._values["scheme"] = scheme

        @builtins.property
        def headers(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.HttpRouteHeaderProperty"]]]]:
            '''The client request headers to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproutematch.html#cfn-appmesh-route-httproutematch-headers
            '''
            result = self._values.get("headers")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.HttpRouteHeaderProperty"]]]], result)

        @builtins.property
        def method(self) -> typing.Optional[builtins.str]:
            '''The client request method to match on.

            Specify only one.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproutematch.html#cfn-appmesh-route-httproutematch-method
            '''
            result = self._values.get("method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def path(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.HttpPathMatchProperty"]]:
            '''The client request path to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproutematch.html#cfn-appmesh-route-httproutematch-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.HttpPathMatchProperty"]], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port number to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproutematch.html#cfn-appmesh-route-httproutematch-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''Specifies the path to match requests with.

            This parameter must always start with ``/`` , which by itself matches all requests to the virtual service name. You can also match for path-based routing of requests. For example, if your virtual service name is ``my-service.local`` and you want the route to match requests to ``my-service.local/metrics`` , your prefix should be ``/metrics`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproutematch.html#cfn-appmesh-route-httproutematch-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def query_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.QueryParameterProperty"]]]]:
            '''The client request query parameters to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproutematch.html#cfn-appmesh-route-httproutematch-queryparameters
            '''
            result = self._values.get("query_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.QueryParameterProperty"]]]], result)

        @builtins.property
        def scheme(self) -> typing.Optional[builtins.str]:
            '''The client request scheme to match on.

            Specify only one. Applicable only for HTTP2 routes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproutematch.html#cfn-appmesh-route-httproutematch-scheme
            '''
            result = self._values.get("scheme")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpRouteMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.HttpRouteProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "match": "match",
            "retry_policy": "retryPolicy",
            "timeout": "timeout",
        },
    )
    class HttpRouteProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.HttpRouteActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.HttpRouteMatchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            retry_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.HttpRetryPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            timeout: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.HttpTimeoutProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents an HTTP or HTTP/2 route type.

            :param action: An object that represents the action to take if a match is determined.
            :param match: An object that represents the criteria for determining a request match.
            :param retry_policy: An object that represents a retry policy.
            :param timeout: An object that represents types of timeouts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                http_route_property = appmesh_mixins.CfnRoutePropsMixin.HttpRouteProperty(
                    action=appmesh_mixins.CfnRoutePropsMixin.HttpRouteActionProperty(
                        weighted_targets=[appmesh_mixins.CfnRoutePropsMixin.WeightedTargetProperty(
                            port=123,
                            virtual_node="virtualNode",
                            weight=123
                        )]
                    ),
                    match=appmesh_mixins.CfnRoutePropsMixin.HttpRouteMatchProperty(
                        headers=[appmesh_mixins.CfnRoutePropsMixin.HttpRouteHeaderProperty(
                            invert=False,
                            match=appmesh_mixins.CfnRoutePropsMixin.HeaderMatchMethodProperty(
                                exact="exact",
                                prefix="prefix",
                                range=appmesh_mixins.CfnRoutePropsMixin.MatchRangeProperty(
                                    end=123,
                                    start=123
                                ),
                                regex="regex",
                                suffix="suffix"
                            ),
                            name="name"
                        )],
                        method="method",
                        path=appmesh_mixins.CfnRoutePropsMixin.HttpPathMatchProperty(
                            exact="exact",
                            regex="regex"
                        ),
                        port=123,
                        prefix="prefix",
                        query_parameters=[appmesh_mixins.CfnRoutePropsMixin.QueryParameterProperty(
                            match=appmesh_mixins.CfnRoutePropsMixin.HttpQueryParameterMatchProperty(
                                exact="exact"
                            ),
                            name="name"
                        )],
                        scheme="scheme"
                    ),
                    retry_policy=appmesh_mixins.CfnRoutePropsMixin.HttpRetryPolicyProperty(
                        http_retry_events=["httpRetryEvents"],
                        max_retries=123,
                        per_retry_timeout=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        ),
                        tcp_retry_events=["tcpRetryEvents"]
                    ),
                    timeout=appmesh_mixins.CfnRoutePropsMixin.HttpTimeoutProperty(
                        idle=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        ),
                        per_request=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8dea564eab35874062f3d94e97241597f932e139ec844324c45c6d8543f78711)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument match", value=match, expected_type=type_hints["match"])
                check_type(argname="argument retry_policy", value=retry_policy, expected_type=type_hints["retry_policy"])
                check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if match is not None:
                self._values["match"] = match
            if retry_policy is not None:
                self._values["retry_policy"] = retry_policy
            if timeout is not None:
                self._values["timeout"] = timeout

        @builtins.property
        def action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.HttpRouteActionProperty"]]:
            '''An object that represents the action to take if a match is determined.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproute.html#cfn-appmesh-route-httproute-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.HttpRouteActionProperty"]], result)

        @builtins.property
        def match(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.HttpRouteMatchProperty"]]:
            '''An object that represents the criteria for determining a request match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproute.html#cfn-appmesh-route-httproute-match
            '''
            result = self._values.get("match")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.HttpRouteMatchProperty"]], result)

        @builtins.property
        def retry_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.HttpRetryPolicyProperty"]]:
            '''An object that represents a retry policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproute.html#cfn-appmesh-route-httproute-retrypolicy
            '''
            result = self._values.get("retry_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.HttpRetryPolicyProperty"]], result)

        @builtins.property
        def timeout(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.HttpTimeoutProperty"]]:
            '''An object that represents types of timeouts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproute.html#cfn-appmesh-route-httproute-timeout
            '''
            result = self._values.get("timeout")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.HttpTimeoutProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpRouteProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.HttpTimeoutProperty",
        jsii_struct_bases=[],
        name_mapping={"idle": "idle", "per_request": "perRequest"},
    )
    class HttpTimeoutProperty:
        def __init__(
            self,
            *,
            idle: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.DurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            per_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.DurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents types of timeouts.

            :param idle: An object that represents an idle timeout. An idle timeout bounds the amount of time that a connection may be idle. The default value is none.
            :param per_request: An object that represents a per request timeout. The default value is 15 seconds. If you set a higher timeout, then make sure that the higher value is set for each App Mesh resource in a conversation. For example, if a virtual node backend uses a virtual router provider to route to another virtual node, then the timeout should be greater than 15 seconds for the source and destination virtual node and the route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httptimeout.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                http_timeout_property = appmesh_mixins.CfnRoutePropsMixin.HttpTimeoutProperty(
                    idle=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                        unit="unit",
                        value=123
                    ),
                    per_request=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                        unit="unit",
                        value=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7f758495b8a7f27ee7f6ad8563c608931255315b4a0e3fff6127d9aae62e6988)
                check_type(argname="argument idle", value=idle, expected_type=type_hints["idle"])
                check_type(argname="argument per_request", value=per_request, expected_type=type_hints["per_request"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if idle is not None:
                self._values["idle"] = idle
            if per_request is not None:
                self._values["per_request"] = per_request

        @builtins.property
        def idle(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.DurationProperty"]]:
            '''An object that represents an idle timeout.

            An idle timeout bounds the amount of time that a connection may be idle. The default value is none.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httptimeout.html#cfn-appmesh-route-httptimeout-idle
            '''
            result = self._values.get("idle")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.DurationProperty"]], result)

        @builtins.property
        def per_request(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.DurationProperty"]]:
            '''An object that represents a per request timeout.

            The default value is 15 seconds. If you set a higher timeout, then make sure that the higher value is set for each App Mesh resource in a conversation. For example, if a virtual node backend uses a virtual router provider to route to another virtual node, then the timeout should be greater than 15 seconds for the source and destination virtual node and the route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httptimeout.html#cfn-appmesh-route-httptimeout-perrequest
            '''
            result = self._values.get("per_request")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.DurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpTimeoutProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.MatchRangeProperty",
        jsii_struct_bases=[],
        name_mapping={"end": "end", "start": "start"},
    )
    class MatchRangeProperty:
        def __init__(
            self,
            *,
            end: typing.Optional[jsii.Number] = None,
            start: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An object that represents the range of values to match on.

            The first character of the range is included in the range, though the last character is not. For example, if the range specified were 1-100, only values 1-99 would be matched.

            :param end: The end of the range.
            :param start: The start of the range.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-matchrange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                match_range_property = appmesh_mixins.CfnRoutePropsMixin.MatchRangeProperty(
                    end=123,
                    start=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3261160f35311a128618b6756cafb8819443c5d64a2beb7f4acef40b3c0c0d4b)
                check_type(argname="argument end", value=end, expected_type=type_hints["end"])
                check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if end is not None:
                self._values["end"] = end
            if start is not None:
                self._values["start"] = start

        @builtins.property
        def end(self) -> typing.Optional[jsii.Number]:
            '''The end of the range.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-matchrange.html#cfn-appmesh-route-matchrange-end
            '''
            result = self._values.get("end")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def start(self) -> typing.Optional[jsii.Number]:
            '''The start of the range.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-matchrange.html#cfn-appmesh-route-matchrange-start
            '''
            result = self._values.get("start")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MatchRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.QueryParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"match": "match", "name": "name"},
    )
    class QueryParameterProperty:
        def __init__(
            self,
            *,
            match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.HttpQueryParameterMatchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the query parameter in the request.

            :param match: The query parameter to match on.
            :param name: A name for the query parameter that will be matched on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-queryparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                query_parameter_property = appmesh_mixins.CfnRoutePropsMixin.QueryParameterProperty(
                    match=appmesh_mixins.CfnRoutePropsMixin.HttpQueryParameterMatchProperty(
                        exact="exact"
                    ),
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__db84a1b5f6eb35537f3ef5ed0a541f82680ef6cca0c3f9005cea5dad447f7518)
                check_type(argname="argument match", value=match, expected_type=type_hints["match"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if match is not None:
                self._values["match"] = match
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def match(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.HttpQueryParameterMatchProperty"]]:
            '''The query parameter to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-queryparameter.html#cfn-appmesh-route-queryparameter-match
            '''
            result = self._values.get("match")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.HttpQueryParameterMatchProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''A name for the query parameter that will be matched on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-queryparameter.html#cfn-appmesh-route-queryparameter-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueryParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.RouteSpecProperty",
        jsii_struct_bases=[],
        name_mapping={
            "grpc_route": "grpcRoute",
            "http2_route": "http2Route",
            "http_route": "httpRoute",
            "priority": "priority",
            "tcp_route": "tcpRoute",
        },
    )
    class RouteSpecProperty:
        def __init__(
            self,
            *,
            grpc_route: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.GrpcRouteProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            http2_route: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.HttpRouteProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            http_route: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.HttpRouteProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            priority: typing.Optional[jsii.Number] = None,
            tcp_route: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.TcpRouteProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents a route specification.

            Specify one route type.

            :param grpc_route: An object that represents the specification of a gRPC route.
            :param http2_route: An object that represents the specification of an HTTP/2 route.
            :param http_route: An object that represents the specification of an HTTP route.
            :param priority: The priority for the route. Routes are matched based on the specified value, where 0 is the highest priority.
            :param tcp_route: An object that represents the specification of a TCP route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-routespec.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                route_spec_property = appmesh_mixins.CfnRoutePropsMixin.RouteSpecProperty(
                    grpc_route=appmesh_mixins.CfnRoutePropsMixin.GrpcRouteProperty(
                        action=appmesh_mixins.CfnRoutePropsMixin.GrpcRouteActionProperty(
                            weighted_targets=[appmesh_mixins.CfnRoutePropsMixin.WeightedTargetProperty(
                                port=123,
                                virtual_node="virtualNode",
                                weight=123
                            )]
                        ),
                        match=appmesh_mixins.CfnRoutePropsMixin.GrpcRouteMatchProperty(
                            metadata=[appmesh_mixins.CfnRoutePropsMixin.GrpcRouteMetadataProperty(
                                invert=False,
                                match=appmesh_mixins.CfnRoutePropsMixin.GrpcRouteMetadataMatchMethodProperty(
                                    exact="exact",
                                    prefix="prefix",
                                    range=appmesh_mixins.CfnRoutePropsMixin.MatchRangeProperty(
                                        end=123,
                                        start=123
                                    ),
                                    regex="regex",
                                    suffix="suffix"
                                ),
                                name="name"
                            )],
                            method_name="methodName",
                            port=123,
                            service_name="serviceName"
                        ),
                        retry_policy=appmesh_mixins.CfnRoutePropsMixin.GrpcRetryPolicyProperty(
                            grpc_retry_events=["grpcRetryEvents"],
                            http_retry_events=["httpRetryEvents"],
                            max_retries=123,
                            per_retry_timeout=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            ),
                            tcp_retry_events=["tcpRetryEvents"]
                        ),
                        timeout=appmesh_mixins.CfnRoutePropsMixin.GrpcTimeoutProperty(
                            idle=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            ),
                            per_request=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            )
                        )
                    ),
                    http2_route=appmesh_mixins.CfnRoutePropsMixin.HttpRouteProperty(
                        action=appmesh_mixins.CfnRoutePropsMixin.HttpRouteActionProperty(
                            weighted_targets=[appmesh_mixins.CfnRoutePropsMixin.WeightedTargetProperty(
                                port=123,
                                virtual_node="virtualNode",
                                weight=123
                            )]
                        ),
                        match=appmesh_mixins.CfnRoutePropsMixin.HttpRouteMatchProperty(
                            headers=[appmesh_mixins.CfnRoutePropsMixin.HttpRouteHeaderProperty(
                                invert=False,
                                match=appmesh_mixins.CfnRoutePropsMixin.HeaderMatchMethodProperty(
                                    exact="exact",
                                    prefix="prefix",
                                    range=appmesh_mixins.CfnRoutePropsMixin.MatchRangeProperty(
                                        end=123,
                                        start=123
                                    ),
                                    regex="regex",
                                    suffix="suffix"
                                ),
                                name="name"
                            )],
                            method="method",
                            path=appmesh_mixins.CfnRoutePropsMixin.HttpPathMatchProperty(
                                exact="exact",
                                regex="regex"
                            ),
                            port=123,
                            prefix="prefix",
                            query_parameters=[appmesh_mixins.CfnRoutePropsMixin.QueryParameterProperty(
                                match=appmesh_mixins.CfnRoutePropsMixin.HttpQueryParameterMatchProperty(
                                    exact="exact"
                                ),
                                name="name"
                            )],
                            scheme="scheme"
                        ),
                        retry_policy=appmesh_mixins.CfnRoutePropsMixin.HttpRetryPolicyProperty(
                            http_retry_events=["httpRetryEvents"],
                            max_retries=123,
                            per_retry_timeout=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            ),
                            tcp_retry_events=["tcpRetryEvents"]
                        ),
                        timeout=appmesh_mixins.CfnRoutePropsMixin.HttpTimeoutProperty(
                            idle=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            ),
                            per_request=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            )
                        )
                    ),
                    http_route=appmesh_mixins.CfnRoutePropsMixin.HttpRouteProperty(
                        action=appmesh_mixins.CfnRoutePropsMixin.HttpRouteActionProperty(
                            weighted_targets=[appmesh_mixins.CfnRoutePropsMixin.WeightedTargetProperty(
                                port=123,
                                virtual_node="virtualNode",
                                weight=123
                            )]
                        ),
                        match=appmesh_mixins.CfnRoutePropsMixin.HttpRouteMatchProperty(
                            headers=[appmesh_mixins.CfnRoutePropsMixin.HttpRouteHeaderProperty(
                                invert=False,
                                match=appmesh_mixins.CfnRoutePropsMixin.HeaderMatchMethodProperty(
                                    exact="exact",
                                    prefix="prefix",
                                    range=appmesh_mixins.CfnRoutePropsMixin.MatchRangeProperty(
                                        end=123,
                                        start=123
                                    ),
                                    regex="regex",
                                    suffix="suffix"
                                ),
                                name="name"
                            )],
                            method="method",
                            path=appmesh_mixins.CfnRoutePropsMixin.HttpPathMatchProperty(
                                exact="exact",
                                regex="regex"
                            ),
                            port=123,
                            prefix="prefix",
                            query_parameters=[appmesh_mixins.CfnRoutePropsMixin.QueryParameterProperty(
                                match=appmesh_mixins.CfnRoutePropsMixin.HttpQueryParameterMatchProperty(
                                    exact="exact"
                                ),
                                name="name"
                            )],
                            scheme="scheme"
                        ),
                        retry_policy=appmesh_mixins.CfnRoutePropsMixin.HttpRetryPolicyProperty(
                            http_retry_events=["httpRetryEvents"],
                            max_retries=123,
                            per_retry_timeout=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            ),
                            tcp_retry_events=["tcpRetryEvents"]
                        ),
                        timeout=appmesh_mixins.CfnRoutePropsMixin.HttpTimeoutProperty(
                            idle=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            ),
                            per_request=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            )
                        )
                    ),
                    priority=123,
                    tcp_route=appmesh_mixins.CfnRoutePropsMixin.TcpRouteProperty(
                        action=appmesh_mixins.CfnRoutePropsMixin.TcpRouteActionProperty(
                            weighted_targets=[appmesh_mixins.CfnRoutePropsMixin.WeightedTargetProperty(
                                port=123,
                                virtual_node="virtualNode",
                                weight=123
                            )]
                        ),
                        match=appmesh_mixins.CfnRoutePropsMixin.TcpRouteMatchProperty(
                            port=123
                        ),
                        timeout=appmesh_mixins.CfnRoutePropsMixin.TcpTimeoutProperty(
                            idle=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__969748cb4ed84b92b91063106557f7f4e4c41321bdaddef6c656de418c47166d)
                check_type(argname="argument grpc_route", value=grpc_route, expected_type=type_hints["grpc_route"])
                check_type(argname="argument http2_route", value=http2_route, expected_type=type_hints["http2_route"])
                check_type(argname="argument http_route", value=http_route, expected_type=type_hints["http_route"])
                check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
                check_type(argname="argument tcp_route", value=tcp_route, expected_type=type_hints["tcp_route"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if grpc_route is not None:
                self._values["grpc_route"] = grpc_route
            if http2_route is not None:
                self._values["http2_route"] = http2_route
            if http_route is not None:
                self._values["http_route"] = http_route
            if priority is not None:
                self._values["priority"] = priority
            if tcp_route is not None:
                self._values["tcp_route"] = tcp_route

        @builtins.property
        def grpc_route(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.GrpcRouteProperty"]]:
            '''An object that represents the specification of a gRPC route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-routespec.html#cfn-appmesh-route-routespec-grpcroute
            '''
            result = self._values.get("grpc_route")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.GrpcRouteProperty"]], result)

        @builtins.property
        def http2_route(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.HttpRouteProperty"]]:
            '''An object that represents the specification of an HTTP/2 route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-routespec.html#cfn-appmesh-route-routespec-http2route
            '''
            result = self._values.get("http2_route")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.HttpRouteProperty"]], result)

        @builtins.property
        def http_route(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.HttpRouteProperty"]]:
            '''An object that represents the specification of an HTTP route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-routespec.html#cfn-appmesh-route-routespec-httproute
            '''
            result = self._values.get("http_route")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.HttpRouteProperty"]], result)

        @builtins.property
        def priority(self) -> typing.Optional[jsii.Number]:
            '''The priority for the route.

            Routes are matched based on the specified value, where 0 is the highest priority.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-routespec.html#cfn-appmesh-route-routespec-priority
            '''
            result = self._values.get("priority")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def tcp_route(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.TcpRouteProperty"]]:
            '''An object that represents the specification of a TCP route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-routespec.html#cfn-appmesh-route-routespec-tcproute
            '''
            result = self._values.get("tcp_route")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.TcpRouteProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RouteSpecProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.TcpRouteActionProperty",
        jsii_struct_bases=[],
        name_mapping={"weighted_targets": "weightedTargets"},
    )
    class TcpRouteActionProperty:
        def __init__(
            self,
            *,
            weighted_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.WeightedTargetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''An object that represents the action to take if a match is determined.

            :param weighted_targets: An object that represents the targets that traffic is routed to when a request matches the route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcprouteaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                tcp_route_action_property = appmesh_mixins.CfnRoutePropsMixin.TcpRouteActionProperty(
                    weighted_targets=[appmesh_mixins.CfnRoutePropsMixin.WeightedTargetProperty(
                        port=123,
                        virtual_node="virtualNode",
                        weight=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fecabe504f895a904eb8e9f6e7d1680054868f50bd5b11ea58a3ecd0b79e461b)
                check_type(argname="argument weighted_targets", value=weighted_targets, expected_type=type_hints["weighted_targets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if weighted_targets is not None:
                self._values["weighted_targets"] = weighted_targets

        @builtins.property
        def weighted_targets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.WeightedTargetProperty"]]]]:
            '''An object that represents the targets that traffic is routed to when a request matches the route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcprouteaction.html#cfn-appmesh-route-tcprouteaction-weightedtargets
            '''
            result = self._values.get("weighted_targets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.WeightedTargetProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TcpRouteActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.TcpRouteMatchProperty",
        jsii_struct_bases=[],
        name_mapping={"port": "port"},
    )
    class TcpRouteMatchProperty:
        def __init__(self, *, port: typing.Optional[jsii.Number] = None) -> None:
            '''An object representing the TCP route to match.

            :param port: The port number to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcproutematch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                tcp_route_match_property = appmesh_mixins.CfnRoutePropsMixin.TcpRouteMatchProperty(
                    port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a51fb7fd19811ba2edee4d36a69d6ef46c0cb9ef9efb300735ea489feb15445)
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if port is not None:
                self._values["port"] = port

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port number to match on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcproutematch.html#cfn-appmesh-route-tcproutematch-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TcpRouteMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.TcpRouteProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action", "match": "match", "timeout": "timeout"},
    )
    class TcpRouteProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.TcpRouteActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.TcpRouteMatchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            timeout: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.TcpTimeoutProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents a TCP route type.

            :param action: The action to take if a match is determined.
            :param match: An object that represents the criteria for determining a request match.
            :param timeout: An object that represents types of timeouts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcproute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                tcp_route_property = appmesh_mixins.CfnRoutePropsMixin.TcpRouteProperty(
                    action=appmesh_mixins.CfnRoutePropsMixin.TcpRouteActionProperty(
                        weighted_targets=[appmesh_mixins.CfnRoutePropsMixin.WeightedTargetProperty(
                            port=123,
                            virtual_node="virtualNode",
                            weight=123
                        )]
                    ),
                    match=appmesh_mixins.CfnRoutePropsMixin.TcpRouteMatchProperty(
                        port=123
                    ),
                    timeout=appmesh_mixins.CfnRoutePropsMixin.TcpTimeoutProperty(
                        idle=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8c00c22a2844428260cd1b1d28fb183ce50334852d452105465cb1cf02bf213b)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument match", value=match, expected_type=type_hints["match"])
                check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if match is not None:
                self._values["match"] = match
            if timeout is not None:
                self._values["timeout"] = timeout

        @builtins.property
        def action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.TcpRouteActionProperty"]]:
            '''The action to take if a match is determined.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcproute.html#cfn-appmesh-route-tcproute-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.TcpRouteActionProperty"]], result)

        @builtins.property
        def match(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.TcpRouteMatchProperty"]]:
            '''An object that represents the criteria for determining a request match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcproute.html#cfn-appmesh-route-tcproute-match
            '''
            result = self._values.get("match")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.TcpRouteMatchProperty"]], result)

        @builtins.property
        def timeout(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.TcpTimeoutProperty"]]:
            '''An object that represents types of timeouts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcproute.html#cfn-appmesh-route-tcproute-timeout
            '''
            result = self._values.get("timeout")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.TcpTimeoutProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TcpRouteProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.TcpTimeoutProperty",
        jsii_struct_bases=[],
        name_mapping={"idle": "idle"},
    )
    class TcpTimeoutProperty:
        def __init__(
            self,
            *,
            idle: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.DurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents types of timeouts.

            :param idle: An object that represents an idle timeout. An idle timeout bounds the amount of time that a connection may be idle. The default value is none.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcptimeout.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                tcp_timeout_property = appmesh_mixins.CfnRoutePropsMixin.TcpTimeoutProperty(
                    idle=appmesh_mixins.CfnRoutePropsMixin.DurationProperty(
                        unit="unit",
                        value=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__67f687c66c46623faf9d998aa3ca2d481380a1f7c5169511e2fcdf210a1bc4d6)
                check_type(argname="argument idle", value=idle, expected_type=type_hints["idle"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if idle is not None:
                self._values["idle"] = idle

        @builtins.property
        def idle(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.DurationProperty"]]:
            '''An object that represents an idle timeout.

            An idle timeout bounds the amount of time that a connection may be idle. The default value is none.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcptimeout.html#cfn-appmesh-route-tcptimeout-idle
            '''
            result = self._values.get("idle")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.DurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TcpTimeoutProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnRoutePropsMixin.WeightedTargetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "port": "port",
            "virtual_node": "virtualNode",
            "weight": "weight",
        },
    )
    class WeightedTargetProperty:
        def __init__(
            self,
            *,
            port: typing.Optional[jsii.Number] = None,
            virtual_node: typing.Optional[builtins.str] = None,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An object that represents a target and its relative weight.

            Traffic is distributed across targets according to their relative weight. For example, a weighted target with a relative weight of 50 receives five times as much traffic as one with a relative weight of 10. The total weight for all targets combined must be less than or equal to 100.

            :param port: The targeted port of the weighted object.
            :param virtual_node: The virtual node to associate with the weighted target.
            :param weight: The relative weight of the weighted target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-weightedtarget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                weighted_target_property = appmesh_mixins.CfnRoutePropsMixin.WeightedTargetProperty(
                    port=123,
                    virtual_node="virtualNode",
                    weight=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ca6cdbb43dc4ee6471ec355d819922265e065bf77a6877952325416d2a4fec95)
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument virtual_node", value=virtual_node, expected_type=type_hints["virtual_node"])
                check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if port is not None:
                self._values["port"] = port
            if virtual_node is not None:
                self._values["virtual_node"] = virtual_node
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The targeted port of the weighted object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-weightedtarget.html#cfn-appmesh-route-weightedtarget-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def virtual_node(self) -> typing.Optional[builtins.str]:
            '''The virtual node to associate with the weighted target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-weightedtarget.html#cfn-appmesh-route-weightedtarget-virtualnode
            '''
            result = self._values.get("virtual_node")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            '''The relative weight of the weighted target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-weightedtarget.html#cfn-appmesh-route-weightedtarget-weight
            '''
            result = self._values.get("weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WeightedTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "mesh_name": "meshName",
        "mesh_owner": "meshOwner",
        "spec": "spec",
        "tags": "tags",
        "virtual_gateway_name": "virtualGatewayName",
    },
)
class CfnVirtualGatewayMixinProps:
    def __init__(
        self,
        *,
        mesh_name: typing.Optional[builtins.str] = None,
        mesh_owner: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewaySpecProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        virtual_gateway_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnVirtualGatewayPropsMixin.

        :param mesh_name: The name of the service mesh that the virtual gateway resides in.
        :param mesh_owner: The AWS IAM account ID of the service mesh owner. If the account ID is not your own, then it's the ID of the account that shared the mesh with your account. For more information about mesh sharing, see `Working with shared meshes <https://docs.aws.amazon.com/app-mesh/latest/userguide/sharing.html>`_ .
        :param spec: The specifications of the virtual gateway.
        :param tags: Optional metadata that you can apply to the virtual gateway to assist with categorization and organization. Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.
        :param virtual_gateway_name: The name of the virtual gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualgateway.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
            
            cfn_virtual_gateway_mixin_props = appmesh_mixins.CfnVirtualGatewayMixinProps(
                mesh_name="meshName",
                mesh_owner="meshOwner",
                spec=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewaySpecProperty(
                    backend_defaults=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayBackendDefaultsProperty(
                        client_policy=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayClientPolicyProperty(
                            tls=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayClientPolicyTlsProperty(
                                certificate=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayClientTlsCertificateProperty(
                                    file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsFileCertificateProperty(
                                        certificate_chain="certificateChain",
                                        private_key="privateKey"
                                    ),
                                    sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsSdsCertificateProperty(
                                        secret_name="secretName"
                                    )
                                ),
                                enforce=False,
                                ports=[123],
                                validation=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextProperty(
                                    subject_alternative_names=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNamesProperty(
                                        match=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNameMatchersProperty(
                                            exact=["exact"]
                                        )
                                    ),
                                    trust=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextTrustProperty(
                                        acm=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextAcmTrustProperty(
                                            certificate_authority_arns=["certificateAuthorityArns"]
                                        ),
                                        file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty(
                                            certificate_chain="certificateChain"
                                        ),
                                        sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty(
                                            secret_name="secretName"
                                        )
                                    )
                                )
                            )
                        )
                    ),
                    listeners=[appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerProperty(
                        connection_pool=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayConnectionPoolProperty(
                            grpc=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayGrpcConnectionPoolProperty(
                                max_requests=123
                            ),
                            http=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayHttpConnectionPoolProperty(
                                max_connections=123,
                                max_pending_requests=123
                            ),
                            http2=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayHttp2ConnectionPoolProperty(
                                max_requests=123
                            )
                        ),
                        health_check=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayHealthCheckPolicyProperty(
                            healthy_threshold=123,
                            interval_millis=123,
                            path="path",
                            port=123,
                            protocol="protocol",
                            timeout_millis=123,
                            unhealthy_threshold=123
                        ),
                        port_mapping=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayPortMappingProperty(
                            port=123,
                            protocol="protocol"
                        ),
                        tls=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsProperty(
                            certificate=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsCertificateProperty(
                                acm=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsAcmCertificateProperty(
                                    certificate_arn="certificateArn"
                                ),
                                file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsFileCertificateProperty(
                                    certificate_chain="certificateChain",
                                    private_key="privateKey"
                                ),
                                sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsSdsCertificateProperty(
                                    secret_name="secretName"
                                )
                            ),
                            mode="mode",
                            validation=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsValidationContextProperty(
                                subject_alternative_names=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNamesProperty(
                                    match=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNameMatchersProperty(
                                        exact=["exact"]
                                    )
                                ),
                                trust=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsValidationContextTrustProperty(
                                    file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty(
                                        certificate_chain="certificateChain"
                                    ),
                                    sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty(
                                        secret_name="secretName"
                                    )
                                )
                            )
                        )
                    )],
                    logging=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayLoggingProperty(
                        access_log=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayAccessLogProperty(
                            file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayFileAccessLogProperty(
                                format=appmesh_mixins.CfnVirtualGatewayPropsMixin.LoggingFormatProperty(
                                    json=[appmesh_mixins.CfnVirtualGatewayPropsMixin.JsonFormatRefProperty(
                                        key="key",
                                        value="value"
                                    )],
                                    text="text"
                                ),
                                path="path"
                            )
                        )
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                virtual_gateway_name="virtualGatewayName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54c092b126e546ab6267aba59fd5f6ab8c5fbf596612a287ef4c82488349ba2d)
            check_type(argname="argument mesh_name", value=mesh_name, expected_type=type_hints["mesh_name"])
            check_type(argname="argument mesh_owner", value=mesh_owner, expected_type=type_hints["mesh_owner"])
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument virtual_gateway_name", value=virtual_gateway_name, expected_type=type_hints["virtual_gateway_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mesh_name is not None:
            self._values["mesh_name"] = mesh_name
        if mesh_owner is not None:
            self._values["mesh_owner"] = mesh_owner
        if spec is not None:
            self._values["spec"] = spec
        if tags is not None:
            self._values["tags"] = tags
        if virtual_gateway_name is not None:
            self._values["virtual_gateway_name"] = virtual_gateway_name

    @builtins.property
    def mesh_name(self) -> typing.Optional[builtins.str]:
        '''The name of the service mesh that the virtual gateway resides in.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualgateway.html#cfn-appmesh-virtualgateway-meshname
        '''
        result = self._values.get("mesh_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mesh_owner(self) -> typing.Optional[builtins.str]:
        '''The AWS IAM account ID of the service mesh owner.

        If the account ID is not your own, then it's the ID of the account that shared the mesh with your account. For more information about mesh sharing, see `Working with shared meshes <https://docs.aws.amazon.com/app-mesh/latest/userguide/sharing.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualgateway.html#cfn-appmesh-virtualgateway-meshowner
        '''
        result = self._values.get("mesh_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spec(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewaySpecProperty"]]:
        '''The specifications of the virtual gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualgateway.html#cfn-appmesh-virtualgateway-spec
        '''
        result = self._values.get("spec")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewaySpecProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Optional metadata that you can apply to the virtual gateway to assist with categorization and organization.

        Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualgateway.html#cfn-appmesh-virtualgateway-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def virtual_gateway_name(self) -> typing.Optional[builtins.str]:
        '''The name of the virtual gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualgateway.html#cfn-appmesh-virtualgateway-virtualgatewayname
        '''
        result = self._values.get("virtual_gateway_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVirtualGatewayMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVirtualGatewayPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin",
):
    '''Creates a virtual gateway.

    A virtual gateway allows resources outside your mesh to communicate to resources that are inside your mesh. The virtual gateway represents an Envoy proxy running in an Amazon ECS task, in a Kubernetes service, or on an Amazon EC2 instance. Unlike a virtual node, which represents an Envoy running with an application, a virtual gateway represents Envoy deployed by itself.

    For more information about virtual gateways, see `Virtual gateways <https://docs.aws.amazon.com/app-mesh/latest/userguide/virtual_gateways.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualgateway.html
    :cloudformationResource: AWS::AppMesh::VirtualGateway
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
        
        cfn_virtual_gateway_props_mixin = appmesh_mixins.CfnVirtualGatewayPropsMixin(appmesh_mixins.CfnVirtualGatewayMixinProps(
            mesh_name="meshName",
            mesh_owner="meshOwner",
            spec=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewaySpecProperty(
                backend_defaults=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayBackendDefaultsProperty(
                    client_policy=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayClientPolicyProperty(
                        tls=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayClientPolicyTlsProperty(
                            certificate=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayClientTlsCertificateProperty(
                                file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsFileCertificateProperty(
                                    certificate_chain="certificateChain",
                                    private_key="privateKey"
                                ),
                                sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsSdsCertificateProperty(
                                    secret_name="secretName"
                                )
                            ),
                            enforce=False,
                            ports=[123],
                            validation=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextProperty(
                                subject_alternative_names=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNamesProperty(
                                    match=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNameMatchersProperty(
                                        exact=["exact"]
                                    )
                                ),
                                trust=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextTrustProperty(
                                    acm=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextAcmTrustProperty(
                                        certificate_authority_arns=["certificateAuthorityArns"]
                                    ),
                                    file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty(
                                        certificate_chain="certificateChain"
                                    ),
                                    sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty(
                                        secret_name="secretName"
                                    )
                                )
                            )
                        )
                    )
                ),
                listeners=[appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerProperty(
                    connection_pool=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayConnectionPoolProperty(
                        grpc=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayGrpcConnectionPoolProperty(
                            max_requests=123
                        ),
                        http=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayHttpConnectionPoolProperty(
                            max_connections=123,
                            max_pending_requests=123
                        ),
                        http2=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayHttp2ConnectionPoolProperty(
                            max_requests=123
                        )
                    ),
                    health_check=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayHealthCheckPolicyProperty(
                        healthy_threshold=123,
                        interval_millis=123,
                        path="path",
                        port=123,
                        protocol="protocol",
                        timeout_millis=123,
                        unhealthy_threshold=123
                    ),
                    port_mapping=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayPortMappingProperty(
                        port=123,
                        protocol="protocol"
                    ),
                    tls=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsProperty(
                        certificate=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsCertificateProperty(
                            acm=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsAcmCertificateProperty(
                                certificate_arn="certificateArn"
                            ),
                            file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsFileCertificateProperty(
                                certificate_chain="certificateChain",
                                private_key="privateKey"
                            ),
                            sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsSdsCertificateProperty(
                                secret_name="secretName"
                            )
                        ),
                        mode="mode",
                        validation=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsValidationContextProperty(
                            subject_alternative_names=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNamesProperty(
                                match=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNameMatchersProperty(
                                    exact=["exact"]
                                )
                            ),
                            trust=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsValidationContextTrustProperty(
                                file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty(
                                    certificate_chain="certificateChain"
                                ),
                                sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty(
                                    secret_name="secretName"
                                )
                            )
                        )
                    )
                )],
                logging=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayLoggingProperty(
                    access_log=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayAccessLogProperty(
                        file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayFileAccessLogProperty(
                            format=appmesh_mixins.CfnVirtualGatewayPropsMixin.LoggingFormatProperty(
                                json=[appmesh_mixins.CfnVirtualGatewayPropsMixin.JsonFormatRefProperty(
                                    key="key",
                                    value="value"
                                )],
                                text="text"
                            ),
                            path="path"
                        )
                    )
                )
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            virtual_gateway_name="virtualGatewayName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVirtualGatewayMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppMesh::VirtualGateway``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5b68f06aa5ab5e21d0272579938d90073efddd2b7d6299e8c3a48ddc0a8dea4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb6ae3f8cf3281678918935ba2f2cc4203efe503f5b28d18ab8db0fb39cc4b0c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89dc0b6ffb01d584ed4d965d88a3aa08e4e8fc979881255f872a3fa498d6f041)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVirtualGatewayMixinProps:
        return typing.cast(CfnVirtualGatewayMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.JsonFormatRefProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class JsonFormatRefProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the key value pairs for the JSON.

            :param key: The specified key for the JSON.
            :param value: The specified value for the JSON.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-jsonformatref.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                json_format_ref_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.JsonFormatRefProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b9dff69307973e6e0f48bd7408eb775f4812b851b059453d76e2a121d6500967)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The specified key for the JSON.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-jsonformatref.html#cfn-appmesh-virtualgateway-jsonformatref-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The specified value for the JSON.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-jsonformatref.html#cfn-appmesh-virtualgateway-jsonformatref-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JsonFormatRefProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.LoggingFormatProperty",
        jsii_struct_bases=[],
        name_mapping={"json": "json", "text": "text"},
    )
    class LoggingFormatProperty:
        def __init__(
            self,
            *,
            json: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.JsonFormatRefProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            text: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the format for the logs.

            :param json: The logging format for JSON.
            :param text: The logging format for text.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-loggingformat.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                logging_format_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.LoggingFormatProperty(
                    json=[appmesh_mixins.CfnVirtualGatewayPropsMixin.JsonFormatRefProperty(
                        key="key",
                        value="value"
                    )],
                    text="text"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b5b7e949e24c5c302823facaf85aee2c66b846c6d21e0cfbda87b80521f1c872)
                check_type(argname="argument json", value=json, expected_type=type_hints["json"])
                check_type(argname="argument text", value=text, expected_type=type_hints["text"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if json is not None:
                self._values["json"] = json
            if text is not None:
                self._values["text"] = text

        @builtins.property
        def json(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.JsonFormatRefProperty"]]]]:
            '''The logging format for JSON.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-loggingformat.html#cfn-appmesh-virtualgateway-loggingformat-json
            '''
            result = self._values.get("json")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.JsonFormatRefProperty"]]]], result)

        @builtins.property
        def text(self) -> typing.Optional[builtins.str]:
            '''The logging format for text.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-loggingformat.html#cfn-appmesh-virtualgateway-loggingformat-text
            '''
            result = self._values.get("text")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingFormatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNameMatchersProperty",
        jsii_struct_bases=[],
        name_mapping={"exact": "exact"},
    )
    class SubjectAlternativeNameMatchersProperty:
        def __init__(
            self,
            *,
            exact: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''An object that represents the methods by which a subject alternative name on a peer Transport Layer Security (TLS) certificate can be matched.

            :param exact: The values sent must match the specified values exactly.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-subjectalternativenamematchers.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                subject_alternative_name_matchers_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNameMatchersProperty(
                    exact=["exact"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__63488c3c35559d285260ece554d163fc761200e9e79aa5edc3c3604934ad7ed0)
                check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exact is not None:
                self._values["exact"] = exact

        @builtins.property
        def exact(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The values sent must match the specified values exactly.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-subjectalternativenamematchers.html#cfn-appmesh-virtualgateway-subjectalternativenamematchers-exact
            '''
            result = self._values.get("exact")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubjectAlternativeNameMatchersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNamesProperty",
        jsii_struct_bases=[],
        name_mapping={"match": "match"},
    )
    class SubjectAlternativeNamesProperty:
        def __init__(
            self,
            *,
            match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.SubjectAlternativeNameMatchersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents the subject alternative names secured by the certificate.

            :param match: An object that represents the criteria for determining a SANs match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-subjectalternativenames.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                subject_alternative_names_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNamesProperty(
                    match=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNameMatchersProperty(
                        exact=["exact"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fe060ac466f802655e1e286fc6ea6aa24f9330e85528b0f978030c67e5633d56)
                check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if match is not None:
                self._values["match"] = match

        @builtins.property
        def match(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.SubjectAlternativeNameMatchersProperty"]]:
            '''An object that represents the criteria for determining a SANs match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-subjectalternativenames.html#cfn-appmesh-virtualgateway-subjectalternativenames-match
            '''
            result = self._values.get("match")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.SubjectAlternativeNameMatchersProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubjectAlternativeNamesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayAccessLogProperty",
        jsii_struct_bases=[],
        name_mapping={"file": "file"},
    )
    class VirtualGatewayAccessLogProperty:
        def __init__(
            self,
            *,
            file: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayFileAccessLogProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The access log configuration for a virtual gateway.

            :param file: The file object to send virtual gateway access logs to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayaccesslog.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_access_log_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayAccessLogProperty(
                    file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayFileAccessLogProperty(
                        format=appmesh_mixins.CfnVirtualGatewayPropsMixin.LoggingFormatProperty(
                            json=[appmesh_mixins.CfnVirtualGatewayPropsMixin.JsonFormatRefProperty(
                                key="key",
                                value="value"
                            )],
                            text="text"
                        ),
                        path="path"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c96a2d0eb43598f42303a9cee3c32bbab4440c2e45d10d721f0aef912d58d9bc)
                check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if file is not None:
                self._values["file"] = file

        @builtins.property
        def file(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayFileAccessLogProperty"]]:
            '''The file object to send virtual gateway access logs to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayaccesslog.html#cfn-appmesh-virtualgateway-virtualgatewayaccesslog-file
            '''
            result = self._values.get("file")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayFileAccessLogProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayAccessLogProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayBackendDefaultsProperty",
        jsii_struct_bases=[],
        name_mapping={"client_policy": "clientPolicy"},
    )
    class VirtualGatewayBackendDefaultsProperty:
        def __init__(
            self,
            *,
            client_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayClientPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents the default properties for a backend.

            :param client_policy: A reference to an object that represents a client policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaybackenddefaults.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_backend_defaults_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayBackendDefaultsProperty(
                    client_policy=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayClientPolicyProperty(
                        tls=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayClientPolicyTlsProperty(
                            certificate=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayClientTlsCertificateProperty(
                                file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsFileCertificateProperty(
                                    certificate_chain="certificateChain",
                                    private_key="privateKey"
                                ),
                                sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsSdsCertificateProperty(
                                    secret_name="secretName"
                                )
                            ),
                            enforce=False,
                            ports=[123],
                            validation=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextProperty(
                                subject_alternative_names=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNamesProperty(
                                    match=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNameMatchersProperty(
                                        exact=["exact"]
                                    )
                                ),
                                trust=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextTrustProperty(
                                    acm=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextAcmTrustProperty(
                                        certificate_authority_arns=["certificateAuthorityArns"]
                                    ),
                                    file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty(
                                        certificate_chain="certificateChain"
                                    ),
                                    sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty(
                                        secret_name="secretName"
                                    )
                                )
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b25612fffcbf3a43865f982d8fe8d43d4b8a9dae599b604a77baa8c516ad8a8a)
                check_type(argname="argument client_policy", value=client_policy, expected_type=type_hints["client_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if client_policy is not None:
                self._values["client_policy"] = client_policy

        @builtins.property
        def client_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayClientPolicyProperty"]]:
            '''A reference to an object that represents a client policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaybackenddefaults.html#cfn-appmesh-virtualgateway-virtualgatewaybackenddefaults-clientpolicy
            '''
            result = self._values.get("client_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayClientPolicyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayBackendDefaultsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayClientPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"tls": "tls"},
    )
    class VirtualGatewayClientPolicyProperty:
        def __init__(
            self,
            *,
            tls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayClientPolicyTlsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents a client policy.

            :param tls: A reference to an object that represents a Transport Layer Security (TLS) client policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayclientpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_client_policy_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayClientPolicyProperty(
                    tls=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayClientPolicyTlsProperty(
                        certificate=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayClientTlsCertificateProperty(
                            file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsFileCertificateProperty(
                                certificate_chain="certificateChain",
                                private_key="privateKey"
                            ),
                            sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsSdsCertificateProperty(
                                secret_name="secretName"
                            )
                        ),
                        enforce=False,
                        ports=[123],
                        validation=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextProperty(
                            subject_alternative_names=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNamesProperty(
                                match=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNameMatchersProperty(
                                    exact=["exact"]
                                )
                            ),
                            trust=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextTrustProperty(
                                acm=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextAcmTrustProperty(
                                    certificate_authority_arns=["certificateAuthorityArns"]
                                ),
                                file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty(
                                    certificate_chain="certificateChain"
                                ),
                                sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty(
                                    secret_name="secretName"
                                )
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a17f061547a4deb7a85c30bfb7fd8734db8378d2cf3a4d4fab3a51b72f3f39ad)
                check_type(argname="argument tls", value=tls, expected_type=type_hints["tls"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if tls is not None:
                self._values["tls"] = tls

        @builtins.property
        def tls(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayClientPolicyTlsProperty"]]:
            '''A reference to an object that represents a Transport Layer Security (TLS) client policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayclientpolicy.html#cfn-appmesh-virtualgateway-virtualgatewayclientpolicy-tls
            '''
            result = self._values.get("tls")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayClientPolicyTlsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayClientPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayClientPolicyTlsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate": "certificate",
            "enforce": "enforce",
            "ports": "ports",
            "validation": "validation",
        },
    )
    class VirtualGatewayClientPolicyTlsProperty:
        def __init__(
            self,
            *,
            certificate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayClientTlsCertificateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enforce: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            ports: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
            validation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents a Transport Layer Security (TLS) client policy.

            :param certificate: A reference to an object that represents a virtual gateway's client's Transport Layer Security (TLS) certificate.
            :param enforce: Whether the policy is enforced. The default is ``True`` , if a value isn't specified.
            :param ports: One or more ports that the policy is enforced for.
            :param validation: A reference to an object that represents a Transport Layer Security (TLS) validation context.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayclientpolicytls.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_client_policy_tls_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayClientPolicyTlsProperty(
                    certificate=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayClientTlsCertificateProperty(
                        file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsFileCertificateProperty(
                            certificate_chain="certificateChain",
                            private_key="privateKey"
                        ),
                        sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsSdsCertificateProperty(
                            secret_name="secretName"
                        )
                    ),
                    enforce=False,
                    ports=[123],
                    validation=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextProperty(
                        subject_alternative_names=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNamesProperty(
                            match=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNameMatchersProperty(
                                exact=["exact"]
                            )
                        ),
                        trust=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextTrustProperty(
                            acm=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextAcmTrustProperty(
                                certificate_authority_arns=["certificateAuthorityArns"]
                            ),
                            file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty(
                                certificate_chain="certificateChain"
                            ),
                            sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty(
                                secret_name="secretName"
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5e02956780ee50b7300761df8505f4cc2619e09f0e7aeae077ceac09e3ee8dee)
                check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
                check_type(argname="argument enforce", value=enforce, expected_type=type_hints["enforce"])
                check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
                check_type(argname="argument validation", value=validation, expected_type=type_hints["validation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate is not None:
                self._values["certificate"] = certificate
            if enforce is not None:
                self._values["enforce"] = enforce
            if ports is not None:
                self._values["ports"] = ports
            if validation is not None:
                self._values["validation"] = validation

        @builtins.property
        def certificate(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayClientTlsCertificateProperty"]]:
            '''A reference to an object that represents a virtual gateway's client's Transport Layer Security (TLS) certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayclientpolicytls.html#cfn-appmesh-virtualgateway-virtualgatewayclientpolicytls-certificate
            '''
            result = self._values.get("certificate")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayClientTlsCertificateProperty"]], result)

        @builtins.property
        def enforce(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether the policy is enforced.

            The default is ``True`` , if a value isn't specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayclientpolicytls.html#cfn-appmesh-virtualgateway-virtualgatewayclientpolicytls-enforce
            '''
            result = self._values.get("enforce")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def ports(
            self,
        ) -> typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]]:
            '''One or more ports that the policy is enforced for.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayclientpolicytls.html#cfn-appmesh-virtualgateway-virtualgatewayclientpolicytls-ports
            '''
            result = self._values.get("ports")
            return typing.cast(typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def validation(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextProperty"]]:
            '''A reference to an object that represents a Transport Layer Security (TLS) validation context.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayclientpolicytls.html#cfn-appmesh-virtualgateway-virtualgatewayclientpolicytls-validation
            '''
            result = self._values.get("validation")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayClientPolicyTlsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayClientTlsCertificateProperty",
        jsii_struct_bases=[],
        name_mapping={"file": "file", "sds": "sds"},
    )
    class VirtualGatewayClientTlsCertificateProperty:
        def __init__(
            self,
            *,
            file: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsFileCertificateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sds: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsSdsCertificateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents the virtual gateway's client's Transport Layer Security (TLS) certificate.

            :param file: An object that represents a local file certificate. The certificate must meet specific requirements and you must have proxy authorization enabled. For more information, see `Transport Layer Security (TLS) <https://docs.aws.amazon.com/app-mesh/latest/userguide/tls.html>`_ .
            :param sds: A reference to an object that represents a virtual gateway's client's Secret Discovery Service certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayclienttlscertificate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_client_tls_certificate_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayClientTlsCertificateProperty(
                    file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsFileCertificateProperty(
                        certificate_chain="certificateChain",
                        private_key="privateKey"
                    ),
                    sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsSdsCertificateProperty(
                        secret_name="secretName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cef7f08ea3c70dcbeb5aaa0588db8826193653c4a0a04331f83f5325d5047632)
                check_type(argname="argument file", value=file, expected_type=type_hints["file"])
                check_type(argname="argument sds", value=sds, expected_type=type_hints["sds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if file is not None:
                self._values["file"] = file
            if sds is not None:
                self._values["sds"] = sds

        @builtins.property
        def file(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsFileCertificateProperty"]]:
            '''An object that represents a local file certificate.

            The certificate must meet specific requirements and you must have proxy authorization enabled. For more information, see `Transport Layer Security (TLS) <https://docs.aws.amazon.com/app-mesh/latest/userguide/tls.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayclienttlscertificate.html#cfn-appmesh-virtualgateway-virtualgatewayclienttlscertificate-file
            '''
            result = self._values.get("file")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsFileCertificateProperty"]], result)

        @builtins.property
        def sds(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsSdsCertificateProperty"]]:
            '''A reference to an object that represents a virtual gateway's client's Secret Discovery Service certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayclienttlscertificate.html#cfn-appmesh-virtualgateway-virtualgatewayclienttlscertificate-sds
            '''
            result = self._values.get("sds")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsSdsCertificateProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayClientTlsCertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayConnectionPoolProperty",
        jsii_struct_bases=[],
        name_mapping={"grpc": "grpc", "http": "http", "http2": "http2"},
    )
    class VirtualGatewayConnectionPoolProperty:
        def __init__(
            self,
            *,
            grpc: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayGrpcConnectionPoolProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            http: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayHttpConnectionPoolProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            http2: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayHttp2ConnectionPoolProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents the type of virtual gateway connection pool.

            Only one protocol is used at a time and should be the same protocol as the one chosen under port mapping.

            If not present the default value for ``maxPendingRequests`` is ``2147483647`` .

            :param grpc: An object that represents a type of connection pool.
            :param http: An object that represents a type of connection pool.
            :param http2: An object that represents a type of connection pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayconnectionpool.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_connection_pool_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayConnectionPoolProperty(
                    grpc=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayGrpcConnectionPoolProperty(
                        max_requests=123
                    ),
                    http=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayHttpConnectionPoolProperty(
                        max_connections=123,
                        max_pending_requests=123
                    ),
                    http2=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayHttp2ConnectionPoolProperty(
                        max_requests=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__92a0963aa8130ae3414efb903786c295f5257dabb8f01ec3dea7831957c5a362)
                check_type(argname="argument grpc", value=grpc, expected_type=type_hints["grpc"])
                check_type(argname="argument http", value=http, expected_type=type_hints["http"])
                check_type(argname="argument http2", value=http2, expected_type=type_hints["http2"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if grpc is not None:
                self._values["grpc"] = grpc
            if http is not None:
                self._values["http"] = http
            if http2 is not None:
                self._values["http2"] = http2

        @builtins.property
        def grpc(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayGrpcConnectionPoolProperty"]]:
            '''An object that represents a type of connection pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayconnectionpool.html#cfn-appmesh-virtualgateway-virtualgatewayconnectionpool-grpc
            '''
            result = self._values.get("grpc")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayGrpcConnectionPoolProperty"]], result)

        @builtins.property
        def http(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayHttpConnectionPoolProperty"]]:
            '''An object that represents a type of connection pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayconnectionpool.html#cfn-appmesh-virtualgateway-virtualgatewayconnectionpool-http
            '''
            result = self._values.get("http")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayHttpConnectionPoolProperty"]], result)

        @builtins.property
        def http2(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayHttp2ConnectionPoolProperty"]]:
            '''An object that represents a type of connection pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayconnectionpool.html#cfn-appmesh-virtualgateway-virtualgatewayconnectionpool-http2
            '''
            result = self._values.get("http2")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayHttp2ConnectionPoolProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayConnectionPoolProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayFileAccessLogProperty",
        jsii_struct_bases=[],
        name_mapping={"format": "format", "path": "path"},
    )
    class VirtualGatewayFileAccessLogProperty:
        def __init__(
            self,
            *,
            format: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.LoggingFormatProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents an access log file.

            :param format: The specified format for the virtual gateway access logs. It can be either ``json_format`` or ``text_format`` .
            :param path: The file path to write access logs to. You can use ``/dev/stdout`` to send access logs to standard out and configure your Envoy container to use a log driver, such as ``awslogs`` , to export the access logs to a log storage service such as Amazon CloudWatch Logs. You can also specify a path in the Envoy container's file system to write the files to disk.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayfileaccesslog.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_file_access_log_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayFileAccessLogProperty(
                    format=appmesh_mixins.CfnVirtualGatewayPropsMixin.LoggingFormatProperty(
                        json=[appmesh_mixins.CfnVirtualGatewayPropsMixin.JsonFormatRefProperty(
                            key="key",
                            value="value"
                        )],
                        text="text"
                    ),
                    path="path"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e69d128d7886283801eb1b9b867c191d16ae1729510ac08df15ae58383904542)
                check_type(argname="argument format", value=format, expected_type=type_hints["format"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if format is not None:
                self._values["format"] = format
            if path is not None:
                self._values["path"] = path

        @builtins.property
        def format(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.LoggingFormatProperty"]]:
            '''The specified format for the virtual gateway access logs.

            It can be either ``json_format`` or ``text_format`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayfileaccesslog.html#cfn-appmesh-virtualgateway-virtualgatewayfileaccesslog-format
            '''
            result = self._values.get("format")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.LoggingFormatProperty"]], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The file path to write access logs to.

            You can use ``/dev/stdout`` to send access logs to standard out and configure your Envoy container to use a log driver, such as ``awslogs`` , to export the access logs to a log storage service such as Amazon CloudWatch Logs. You can also specify a path in the Envoy container's file system to write the files to disk.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayfileaccesslog.html#cfn-appmesh-virtualgateway-virtualgatewayfileaccesslog-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayFileAccessLogProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayGrpcConnectionPoolProperty",
        jsii_struct_bases=[],
        name_mapping={"max_requests": "maxRequests"},
    )
    class VirtualGatewayGrpcConnectionPoolProperty:
        def __init__(
            self,
            *,
            max_requests: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An object that represents a type of connection pool.

            :param max_requests: Maximum number of inflight requests Envoy can concurrently support across hosts in upstream cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaygrpcconnectionpool.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_grpc_connection_pool_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayGrpcConnectionPoolProperty(
                    max_requests=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e6fe8c8de12c6bac97d6552635118fe68dc1c4e7b2cfc0c02e7d504f0ac26242)
                check_type(argname="argument max_requests", value=max_requests, expected_type=type_hints["max_requests"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_requests is not None:
                self._values["max_requests"] = max_requests

        @builtins.property
        def max_requests(self) -> typing.Optional[jsii.Number]:
            '''Maximum number of inflight requests Envoy can concurrently support across hosts in upstream cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaygrpcconnectionpool.html#cfn-appmesh-virtualgateway-virtualgatewaygrpcconnectionpool-maxrequests
            '''
            result = self._values.get("max_requests")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayGrpcConnectionPoolProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayHealthCheckPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "healthy_threshold": "healthyThreshold",
            "interval_millis": "intervalMillis",
            "path": "path",
            "port": "port",
            "protocol": "protocol",
            "timeout_millis": "timeoutMillis",
            "unhealthy_threshold": "unhealthyThreshold",
        },
    )
    class VirtualGatewayHealthCheckPolicyProperty:
        def __init__(
            self,
            *,
            healthy_threshold: typing.Optional[jsii.Number] = None,
            interval_millis: typing.Optional[jsii.Number] = None,
            path: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            protocol: typing.Optional[builtins.str] = None,
            timeout_millis: typing.Optional[jsii.Number] = None,
            unhealthy_threshold: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An object that represents the health check policy for a virtual gateway's listener.

            :param healthy_threshold: The number of consecutive successful health checks that must occur before declaring the listener healthy.
            :param interval_millis: The time period in milliseconds between each health check execution.
            :param path: The destination path for the health check request. This value is only used if the specified protocol is HTTP or HTTP/2. For any other protocol, this value is ignored.
            :param port: The destination port for the health check request. This port must match the port defined in the ``PortMapping`` for the listener.
            :param protocol: The protocol for the health check request. If you specify ``grpc`` , then your service must conform to the `GRPC Health Checking Protocol <https://docs.aws.amazon.com/https://github.com/grpc/grpc/blob/master/doc/health-checking.md>`_ .
            :param timeout_millis: The amount of time to wait when receiving a response from the health check, in milliseconds.
            :param unhealthy_threshold: The number of consecutive failed health checks that must occur before declaring a virtual gateway unhealthy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_health_check_policy_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayHealthCheckPolicyProperty(
                    healthy_threshold=123,
                    interval_millis=123,
                    path="path",
                    port=123,
                    protocol="protocol",
                    timeout_millis=123,
                    unhealthy_threshold=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e0f44b10c062825f1cf6bf3d828678e8a8954e66d99652a2834bcbc3f174a3de)
                check_type(argname="argument healthy_threshold", value=healthy_threshold, expected_type=type_hints["healthy_threshold"])
                check_type(argname="argument interval_millis", value=interval_millis, expected_type=type_hints["interval_millis"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument timeout_millis", value=timeout_millis, expected_type=type_hints["timeout_millis"])
                check_type(argname="argument unhealthy_threshold", value=unhealthy_threshold, expected_type=type_hints["unhealthy_threshold"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if healthy_threshold is not None:
                self._values["healthy_threshold"] = healthy_threshold
            if interval_millis is not None:
                self._values["interval_millis"] = interval_millis
            if path is not None:
                self._values["path"] = path
            if port is not None:
                self._values["port"] = port
            if protocol is not None:
                self._values["protocol"] = protocol
            if timeout_millis is not None:
                self._values["timeout_millis"] = timeout_millis
            if unhealthy_threshold is not None:
                self._values["unhealthy_threshold"] = unhealthy_threshold

        @builtins.property
        def healthy_threshold(self) -> typing.Optional[jsii.Number]:
            '''The number of consecutive successful health checks that must occur before declaring the listener healthy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy.html#cfn-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy-healthythreshold
            '''
            result = self._values.get("healthy_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval_millis(self) -> typing.Optional[jsii.Number]:
            '''The time period in milliseconds between each health check execution.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy.html#cfn-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy-intervalmillis
            '''
            result = self._values.get("interval_millis")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The destination path for the health check request.

            This value is only used if the specified protocol is HTTP or HTTP/2. For any other protocol, this value is ignored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy.html#cfn-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The destination port for the health check request.

            This port must match the port defined in the ``PortMapping`` for the listener.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy.html#cfn-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The protocol for the health check request.

            If you specify ``grpc`` , then your service must conform to the `GRPC Health Checking Protocol <https://docs.aws.amazon.com/https://github.com/grpc/grpc/blob/master/doc/health-checking.md>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy.html#cfn-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timeout_millis(self) -> typing.Optional[jsii.Number]:
            '''The amount of time to wait when receiving a response from the health check, in milliseconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy.html#cfn-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy-timeoutmillis
            '''
            result = self._values.get("timeout_millis")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unhealthy_threshold(self) -> typing.Optional[jsii.Number]:
            '''The number of consecutive failed health checks that must occur before declaring a virtual gateway unhealthy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy.html#cfn-appmesh-virtualgateway-virtualgatewayhealthcheckpolicy-unhealthythreshold
            '''
            result = self._values.get("unhealthy_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayHealthCheckPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayHttp2ConnectionPoolProperty",
        jsii_struct_bases=[],
        name_mapping={"max_requests": "maxRequests"},
    )
    class VirtualGatewayHttp2ConnectionPoolProperty:
        def __init__(
            self,
            *,
            max_requests: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An object that represents a type of connection pool.

            :param max_requests: Maximum number of inflight requests Envoy can concurrently support across hosts in upstream cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhttp2connectionpool.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_http2_connection_pool_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayHttp2ConnectionPoolProperty(
                    max_requests=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__989c903cc0210c67e0f9b3b072f769b8b948b0b1d6cade5c00c17e817de390a7)
                check_type(argname="argument max_requests", value=max_requests, expected_type=type_hints["max_requests"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_requests is not None:
                self._values["max_requests"] = max_requests

        @builtins.property
        def max_requests(self) -> typing.Optional[jsii.Number]:
            '''Maximum number of inflight requests Envoy can concurrently support across hosts in upstream cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhttp2connectionpool.html#cfn-appmesh-virtualgateway-virtualgatewayhttp2connectionpool-maxrequests
            '''
            result = self._values.get("max_requests")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayHttp2ConnectionPoolProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayHttpConnectionPoolProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_connections": "maxConnections",
            "max_pending_requests": "maxPendingRequests",
        },
    )
    class VirtualGatewayHttpConnectionPoolProperty:
        def __init__(
            self,
            *,
            max_connections: typing.Optional[jsii.Number] = None,
            max_pending_requests: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An object that represents a type of connection pool.

            :param max_connections: Maximum number of outbound TCP connections Envoy can establish concurrently with all hosts in upstream cluster.
            :param max_pending_requests: Number of overflowing requests after ``max_connections`` Envoy will queue to upstream cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhttpconnectionpool.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_http_connection_pool_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayHttpConnectionPoolProperty(
                    max_connections=123,
                    max_pending_requests=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fbc2869b582807a92e57d445e14735218faaf37d7106c5e5d3476f1967b8d24d)
                check_type(argname="argument max_connections", value=max_connections, expected_type=type_hints["max_connections"])
                check_type(argname="argument max_pending_requests", value=max_pending_requests, expected_type=type_hints["max_pending_requests"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_connections is not None:
                self._values["max_connections"] = max_connections
            if max_pending_requests is not None:
                self._values["max_pending_requests"] = max_pending_requests

        @builtins.property
        def max_connections(self) -> typing.Optional[jsii.Number]:
            '''Maximum number of outbound TCP connections Envoy can establish concurrently with all hosts in upstream cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhttpconnectionpool.html#cfn-appmesh-virtualgateway-virtualgatewayhttpconnectionpool-maxconnections
            '''
            result = self._values.get("max_connections")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_pending_requests(self) -> typing.Optional[jsii.Number]:
            '''Number of overflowing requests after ``max_connections`` Envoy will queue to upstream cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayhttpconnectionpool.html#cfn-appmesh-virtualgateway-virtualgatewayhttpconnectionpool-maxpendingrequests
            '''
            result = self._values.get("max_pending_requests")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayHttpConnectionPoolProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connection_pool": "connectionPool",
            "health_check": "healthCheck",
            "port_mapping": "portMapping",
            "tls": "tls",
        },
    )
    class VirtualGatewayListenerProperty:
        def __init__(
            self,
            *,
            connection_pool: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayConnectionPoolProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            health_check: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayHealthCheckPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            port_mapping: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayPortMappingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            tls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents a listener for a virtual gateway.

            :param connection_pool: The connection pool information for the listener.
            :param health_check: The health check information for the listener.
            :param port_mapping: The port mapping information for the listener.
            :param tls: A reference to an object that represents the Transport Layer Security (TLS) properties for the listener.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistener.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_listener_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerProperty(
                    connection_pool=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayConnectionPoolProperty(
                        grpc=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayGrpcConnectionPoolProperty(
                            max_requests=123
                        ),
                        http=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayHttpConnectionPoolProperty(
                            max_connections=123,
                            max_pending_requests=123
                        ),
                        http2=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayHttp2ConnectionPoolProperty(
                            max_requests=123
                        )
                    ),
                    health_check=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayHealthCheckPolicyProperty(
                        healthy_threshold=123,
                        interval_millis=123,
                        path="path",
                        port=123,
                        protocol="protocol",
                        timeout_millis=123,
                        unhealthy_threshold=123
                    ),
                    port_mapping=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayPortMappingProperty(
                        port=123,
                        protocol="protocol"
                    ),
                    tls=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsProperty(
                        certificate=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsCertificateProperty(
                            acm=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsAcmCertificateProperty(
                                certificate_arn="certificateArn"
                            ),
                            file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsFileCertificateProperty(
                                certificate_chain="certificateChain",
                                private_key="privateKey"
                            ),
                            sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsSdsCertificateProperty(
                                secret_name="secretName"
                            )
                        ),
                        mode="mode",
                        validation=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsValidationContextProperty(
                            subject_alternative_names=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNamesProperty(
                                match=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNameMatchersProperty(
                                    exact=["exact"]
                                )
                            ),
                            trust=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsValidationContextTrustProperty(
                                file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty(
                                    certificate_chain="certificateChain"
                                ),
                                sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty(
                                    secret_name="secretName"
                                )
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0bba8b91f0be203864d48e987c3a3f690db144c10dc76c1910fa2452260bb5dd)
                check_type(argname="argument connection_pool", value=connection_pool, expected_type=type_hints["connection_pool"])
                check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
                check_type(argname="argument port_mapping", value=port_mapping, expected_type=type_hints["port_mapping"])
                check_type(argname="argument tls", value=tls, expected_type=type_hints["tls"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connection_pool is not None:
                self._values["connection_pool"] = connection_pool
            if health_check is not None:
                self._values["health_check"] = health_check
            if port_mapping is not None:
                self._values["port_mapping"] = port_mapping
            if tls is not None:
                self._values["tls"] = tls

        @builtins.property
        def connection_pool(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayConnectionPoolProperty"]]:
            '''The connection pool information for the listener.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistener.html#cfn-appmesh-virtualgateway-virtualgatewaylistener-connectionpool
            '''
            result = self._values.get("connection_pool")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayConnectionPoolProperty"]], result)

        @builtins.property
        def health_check(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayHealthCheckPolicyProperty"]]:
            '''The health check information for the listener.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistener.html#cfn-appmesh-virtualgateway-virtualgatewaylistener-healthcheck
            '''
            result = self._values.get("health_check")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayHealthCheckPolicyProperty"]], result)

        @builtins.property
        def port_mapping(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayPortMappingProperty"]]:
            '''The port mapping information for the listener.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistener.html#cfn-appmesh-virtualgateway-virtualgatewaylistener-portmapping
            '''
            result = self._values.get("port_mapping")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayPortMappingProperty"]], result)

        @builtins.property
        def tls(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsProperty"]]:
            '''A reference to an object that represents the Transport Layer Security (TLS) properties for the listener.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistener.html#cfn-appmesh-virtualgateway-virtualgatewaylistener-tls
            '''
            result = self._values.get("tls")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayListenerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsAcmCertificateProperty",
        jsii_struct_bases=[],
        name_mapping={"certificate_arn": "certificateArn"},
    )
    class VirtualGatewayListenerTlsAcmCertificateProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents an Certificate Manager certificate.

            :param certificate_arn: The Amazon Resource Name (ARN) for the certificate. The certificate must meet specific requirements and you must have proxy authorization enabled. For more information, see `Transport Layer Security (TLS) <https://docs.aws.amazon.com/app-mesh/latest/userguide/tls.html#virtual-node-tls-prerequisites>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlsacmcertificate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_listener_tls_acm_certificate_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsAcmCertificateProperty(
                    certificate_arn="certificateArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ec50e08fcff89f1426a40ac016e2320babb9d09533d19acf309bbdbb194ed0a0)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the certificate.

            The certificate must meet specific requirements and you must have proxy authorization enabled. For more information, see `Transport Layer Security (TLS) <https://docs.aws.amazon.com/app-mesh/latest/userguide/tls.html#virtual-node-tls-prerequisites>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlsacmcertificate.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertlsacmcertificate-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayListenerTlsAcmCertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsCertificateProperty",
        jsii_struct_bases=[],
        name_mapping={"acm": "acm", "file": "file", "sds": "sds"},
    )
    class VirtualGatewayListenerTlsCertificateProperty:
        def __init__(
            self,
            *,
            acm: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsAcmCertificateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            file: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsFileCertificateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sds: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsSdsCertificateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents a listener's Transport Layer Security (TLS) certificate.

            :param acm: A reference to an object that represents an Certificate Manager certificate.
            :param file: A reference to an object that represents a local file certificate.
            :param sds: A reference to an object that represents a virtual gateway's listener's Secret Discovery Service certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlscertificate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_listener_tls_certificate_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsCertificateProperty(
                    acm=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsAcmCertificateProperty(
                        certificate_arn="certificateArn"
                    ),
                    file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsFileCertificateProperty(
                        certificate_chain="certificateChain",
                        private_key="privateKey"
                    ),
                    sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsSdsCertificateProperty(
                        secret_name="secretName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d55e039896ad1c1db7bfbdbda0a74d5c21177cc5de6deaabed33f28b2576ff5c)
                check_type(argname="argument acm", value=acm, expected_type=type_hints["acm"])
                check_type(argname="argument file", value=file, expected_type=type_hints["file"])
                check_type(argname="argument sds", value=sds, expected_type=type_hints["sds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if acm is not None:
                self._values["acm"] = acm
            if file is not None:
                self._values["file"] = file
            if sds is not None:
                self._values["sds"] = sds

        @builtins.property
        def acm(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsAcmCertificateProperty"]]:
            '''A reference to an object that represents an Certificate Manager certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlscertificate.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertlscertificate-acm
            '''
            result = self._values.get("acm")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsAcmCertificateProperty"]], result)

        @builtins.property
        def file(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsFileCertificateProperty"]]:
            '''A reference to an object that represents a local file certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlscertificate.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertlscertificate-file
            '''
            result = self._values.get("file")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsFileCertificateProperty"]], result)

        @builtins.property
        def sds(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsSdsCertificateProperty"]]:
            '''A reference to an object that represents a virtual gateway's listener's Secret Discovery Service certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlscertificate.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertlscertificate-sds
            '''
            result = self._values.get("sds")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsSdsCertificateProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayListenerTlsCertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsFileCertificateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_chain": "certificateChain",
            "private_key": "privateKey",
        },
    )
    class VirtualGatewayListenerTlsFileCertificateProperty:
        def __init__(
            self,
            *,
            certificate_chain: typing.Optional[builtins.str] = None,
            private_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents a local file certificate.

            The certificate must meet specific requirements and you must have proxy authorization enabled. For more information, see `Transport Layer Security (TLS) <https://docs.aws.amazon.com/app-mesh/latest/userguide/tls.html#virtual-node-tls-prerequisites>`_ .

            :param certificate_chain: The certificate chain for the certificate.
            :param private_key: The private key for a certificate stored on the file system of the mesh endpoint that the proxy is running on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlsfilecertificate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_listener_tls_file_certificate_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsFileCertificateProperty(
                    certificate_chain="certificateChain",
                    private_key="privateKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8856d353187133ab04e43cab724b298a4eaf52e5d105f148efaa42bad6e1d1e9)
                check_type(argname="argument certificate_chain", value=certificate_chain, expected_type=type_hints["certificate_chain"])
                check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_chain is not None:
                self._values["certificate_chain"] = certificate_chain
            if private_key is not None:
                self._values["private_key"] = private_key

        @builtins.property
        def certificate_chain(self) -> typing.Optional[builtins.str]:
            '''The certificate chain for the certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlsfilecertificate.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertlsfilecertificate-certificatechain
            '''
            result = self._values.get("certificate_chain")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def private_key(self) -> typing.Optional[builtins.str]:
            '''The private key for a certificate stored on the file system of the mesh endpoint that the proxy is running on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlsfilecertificate.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertlsfilecertificate-privatekey
            '''
            result = self._values.get("private_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayListenerTlsFileCertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate": "certificate",
            "mode": "mode",
            "validation": "validation",
        },
    )
    class VirtualGatewayListenerTlsProperty:
        def __init__(
            self,
            *,
            certificate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsCertificateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            mode: typing.Optional[builtins.str] = None,
            validation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsValidationContextProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents the Transport Layer Security (TLS) properties for a listener.

            :param certificate: An object that represents a Transport Layer Security (TLS) certificate.
            :param mode: Specify one of the following modes. - ** STRICT – Listener only accepts connections with TLS enabled. - ** PERMISSIVE – Listener accepts connections with or without TLS enabled. - ** DISABLED – Listener only accepts connections without TLS.
            :param validation: A reference to an object that represents a virtual gateway's listener's Transport Layer Security (TLS) validation context.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertls.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_listener_tls_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsProperty(
                    certificate=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsCertificateProperty(
                        acm=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsAcmCertificateProperty(
                            certificate_arn="certificateArn"
                        ),
                        file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsFileCertificateProperty(
                            certificate_chain="certificateChain",
                            private_key="privateKey"
                        ),
                        sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsSdsCertificateProperty(
                            secret_name="secretName"
                        )
                    ),
                    mode="mode",
                    validation=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsValidationContextProperty(
                        subject_alternative_names=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNamesProperty(
                            match=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNameMatchersProperty(
                                exact=["exact"]
                            )
                        ),
                        trust=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsValidationContextTrustProperty(
                            file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty(
                                certificate_chain="certificateChain"
                            ),
                            sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty(
                                secret_name="secretName"
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__11b4c004cb2a2117b7432d7888157aedcbce57c8de51ff785e42ad1fe57d44d0)
                check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
                check_type(argname="argument validation", value=validation, expected_type=type_hints["validation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate is not None:
                self._values["certificate"] = certificate
            if mode is not None:
                self._values["mode"] = mode
            if validation is not None:
                self._values["validation"] = validation

        @builtins.property
        def certificate(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsCertificateProperty"]]:
            '''An object that represents a Transport Layer Security (TLS) certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertls.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertls-certificate
            '''
            result = self._values.get("certificate")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsCertificateProperty"]], result)

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''Specify one of the following modes.

            - ** STRICT – Listener only accepts connections with TLS enabled.
            - ** PERMISSIVE – Listener accepts connections with or without TLS enabled.
            - ** DISABLED – Listener only accepts connections without TLS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertls.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertls-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def validation(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsValidationContextProperty"]]:
            '''A reference to an object that represents a virtual gateway's listener's Transport Layer Security (TLS) validation context.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertls.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertls-validation
            '''
            result = self._values.get("validation")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsValidationContextProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayListenerTlsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsSdsCertificateProperty",
        jsii_struct_bases=[],
        name_mapping={"secret_name": "secretName"},
    )
    class VirtualGatewayListenerTlsSdsCertificateProperty:
        def __init__(
            self,
            *,
            secret_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the virtual gateway's listener's Secret Discovery Service certificate.The proxy must be configured with a local SDS provider via a Unix Domain Socket. See App Mesh `TLS documentation <https://docs.aws.amazon.com/app-mesh/latest/userguide/tls.html>`_ for more info.

            :param secret_name: A reference to an object that represents the name of the secret secret requested from the Secret Discovery Service provider representing Transport Layer Security (TLS) materials like a certificate or certificate chain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlssdscertificate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_listener_tls_sds_certificate_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsSdsCertificateProperty(
                    secret_name="secretName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e7e424ce7cc3b803db8b2a6fe3f7b3f4cf967740d15158c25c8bcff1e65a3534)
                check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if secret_name is not None:
                self._values["secret_name"] = secret_name

        @builtins.property
        def secret_name(self) -> typing.Optional[builtins.str]:
            '''A reference to an object that represents the name of the secret secret requested from the Secret Discovery Service provider representing Transport Layer Security (TLS) materials like a certificate or certificate chain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlssdscertificate.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertlssdscertificate-secretname
            '''
            result = self._values.get("secret_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayListenerTlsSdsCertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsValidationContextProperty",
        jsii_struct_bases=[],
        name_mapping={
            "subject_alternative_names": "subjectAlternativeNames",
            "trust": "trust",
        },
    )
    class VirtualGatewayListenerTlsValidationContextProperty:
        def __init__(
            self,
            *,
            subject_alternative_names: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.SubjectAlternativeNamesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            trust: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsValidationContextTrustProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents a virtual gateway's listener's Transport Layer Security (TLS) validation context.

            :param subject_alternative_names: A reference to an object that represents the SANs for a virtual gateway listener's Transport Layer Security (TLS) validation context.
            :param trust: A reference to where to retrieve the trust chain when validating a peer’s Transport Layer Security (TLS) certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlsvalidationcontext.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_listener_tls_validation_context_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsValidationContextProperty(
                    subject_alternative_names=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNamesProperty(
                        match=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNameMatchersProperty(
                            exact=["exact"]
                        )
                    ),
                    trust=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsValidationContextTrustProperty(
                        file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty(
                            certificate_chain="certificateChain"
                        ),
                        sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty(
                            secret_name="secretName"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b1c8666942dc61834d2499847d82d3ec219caacac64afa4cf1975c4caf97bd9e)
                check_type(argname="argument subject_alternative_names", value=subject_alternative_names, expected_type=type_hints["subject_alternative_names"])
                check_type(argname="argument trust", value=trust, expected_type=type_hints["trust"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if subject_alternative_names is not None:
                self._values["subject_alternative_names"] = subject_alternative_names
            if trust is not None:
                self._values["trust"] = trust

        @builtins.property
        def subject_alternative_names(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.SubjectAlternativeNamesProperty"]]:
            '''A reference to an object that represents the SANs for a virtual gateway listener's Transport Layer Security (TLS) validation context.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlsvalidationcontext.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertlsvalidationcontext-subjectalternativenames
            '''
            result = self._values.get("subject_alternative_names")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.SubjectAlternativeNamesProperty"]], result)

        @builtins.property
        def trust(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsValidationContextTrustProperty"]]:
            '''A reference to where to retrieve the trust chain when validating a peer’s Transport Layer Security (TLS) certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlsvalidationcontext.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertlsvalidationcontext-trust
            '''
            result = self._values.get("trust")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsValidationContextTrustProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayListenerTlsValidationContextProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsValidationContextTrustProperty",
        jsii_struct_bases=[],
        name_mapping={"file": "file", "sds": "sds"},
    )
    class VirtualGatewayListenerTlsValidationContextTrustProperty:
        def __init__(
            self,
            *,
            file: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sds: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents a virtual gateway's listener's Transport Layer Security (TLS) validation context trust.

            :param file: An object that represents a Transport Layer Security (TLS) validation context trust for a local file.
            :param sds: A reference to an object that represents a virtual gateway's listener's Transport Layer Security (TLS) Secret Discovery Service validation context trust.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlsvalidationcontexttrust.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_listener_tls_validation_context_trust_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsValidationContextTrustProperty(
                    file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty(
                        certificate_chain="certificateChain"
                    ),
                    sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty(
                        secret_name="secretName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9ea3d358965268381dc1c68035b2b3870d2b1a1db913e25fa19d1e170f287fdb)
                check_type(argname="argument file", value=file, expected_type=type_hints["file"])
                check_type(argname="argument sds", value=sds, expected_type=type_hints["sds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if file is not None:
                self._values["file"] = file
            if sds is not None:
                self._values["sds"] = sds

        @builtins.property
        def file(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty"]]:
            '''An object that represents a Transport Layer Security (TLS) validation context trust for a local file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlsvalidationcontexttrust.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertlsvalidationcontexttrust-file
            '''
            result = self._values.get("file")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty"]], result)

        @builtins.property
        def sds(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty"]]:
            '''A reference to an object that represents a virtual gateway's listener's Transport Layer Security (TLS) Secret Discovery Service validation context trust.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylistenertlsvalidationcontexttrust.html#cfn-appmesh-virtualgateway-virtualgatewaylistenertlsvalidationcontexttrust-sds
            '''
            result = self._values.get("sds")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayListenerTlsValidationContextTrustProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayLoggingProperty",
        jsii_struct_bases=[],
        name_mapping={"access_log": "accessLog"},
    )
    class VirtualGatewayLoggingProperty:
        def __init__(
            self,
            *,
            access_log: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayAccessLogProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents logging information.

            :param access_log: The access log configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylogging.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_logging_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayLoggingProperty(
                    access_log=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayAccessLogProperty(
                        file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayFileAccessLogProperty(
                            format=appmesh_mixins.CfnVirtualGatewayPropsMixin.LoggingFormatProperty(
                                json=[appmesh_mixins.CfnVirtualGatewayPropsMixin.JsonFormatRefProperty(
                                    key="key",
                                    value="value"
                                )],
                                text="text"
                            ),
                            path="path"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a5240ecef3695aeecd28e7d86c2cb9a0a2b5600d1aa50b055d23b7d7015f643a)
                check_type(argname="argument access_log", value=access_log, expected_type=type_hints["access_log"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_log is not None:
                self._values["access_log"] = access_log

        @builtins.property
        def access_log(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayAccessLogProperty"]]:
            '''The access log configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaylogging.html#cfn-appmesh-virtualgateway-virtualgatewaylogging-accesslog
            '''
            result = self._values.get("access_log")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayAccessLogProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayLoggingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayPortMappingProperty",
        jsii_struct_bases=[],
        name_mapping={"port": "port", "protocol": "protocol"},
    )
    class VirtualGatewayPortMappingProperty:
        def __init__(
            self,
            *,
            port: typing.Optional[jsii.Number] = None,
            protocol: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents a port mapping.

            :param port: The port used for the port mapping. Specify one protocol.
            :param protocol: The protocol used for the port mapping.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayportmapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_port_mapping_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayPortMappingProperty(
                    port=123,
                    protocol="protocol"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__13c2ea7ab18467fe47760390f35dd8530500f232a3881e2c62b93e2fe91896db)
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if port is not None:
                self._values["port"] = port
            if protocol is not None:
                self._values["protocol"] = protocol

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port used for the port mapping.

            Specify one protocol.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayportmapping.html#cfn-appmesh-virtualgateway-virtualgatewayportmapping-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The protocol used for the port mapping.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayportmapping.html#cfn-appmesh-virtualgateway-virtualgatewayportmapping-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayPortMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewaySpecProperty",
        jsii_struct_bases=[],
        name_mapping={
            "backend_defaults": "backendDefaults",
            "listeners": "listeners",
            "logging": "logging",
        },
    )
    class VirtualGatewaySpecProperty:
        def __init__(
            self,
            *,
            backend_defaults: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayBackendDefaultsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            listeners: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayListenerProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            logging: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayLoggingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents the specification of a service mesh resource.

            :param backend_defaults: A reference to an object that represents the defaults for backends.
            :param listeners: The listeners that the mesh endpoint is expected to receive inbound traffic from. You can specify one listener.
            :param logging: An object that represents logging information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayspec.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_spec_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewaySpecProperty(
                    backend_defaults=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayBackendDefaultsProperty(
                        client_policy=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayClientPolicyProperty(
                            tls=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayClientPolicyTlsProperty(
                                certificate=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayClientTlsCertificateProperty(
                                    file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsFileCertificateProperty(
                                        certificate_chain="certificateChain",
                                        private_key="privateKey"
                                    ),
                                    sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsSdsCertificateProperty(
                                        secret_name="secretName"
                                    )
                                ),
                                enforce=False,
                                ports=[123],
                                validation=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextProperty(
                                    subject_alternative_names=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNamesProperty(
                                        match=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNameMatchersProperty(
                                            exact=["exact"]
                                        )
                                    ),
                                    trust=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextTrustProperty(
                                        acm=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextAcmTrustProperty(
                                            certificate_authority_arns=["certificateAuthorityArns"]
                                        ),
                                        file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty(
                                            certificate_chain="certificateChain"
                                        ),
                                        sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty(
                                            secret_name="secretName"
                                        )
                                    )
                                )
                            )
                        )
                    ),
                    listeners=[appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerProperty(
                        connection_pool=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayConnectionPoolProperty(
                            grpc=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayGrpcConnectionPoolProperty(
                                max_requests=123
                            ),
                            http=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayHttpConnectionPoolProperty(
                                max_connections=123,
                                max_pending_requests=123
                            ),
                            http2=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayHttp2ConnectionPoolProperty(
                                max_requests=123
                            )
                        ),
                        health_check=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayHealthCheckPolicyProperty(
                            healthy_threshold=123,
                            interval_millis=123,
                            path="path",
                            port=123,
                            protocol="protocol",
                            timeout_millis=123,
                            unhealthy_threshold=123
                        ),
                        port_mapping=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayPortMappingProperty(
                            port=123,
                            protocol="protocol"
                        ),
                        tls=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsProperty(
                            certificate=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsCertificateProperty(
                                acm=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsAcmCertificateProperty(
                                    certificate_arn="certificateArn"
                                ),
                                file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsFileCertificateProperty(
                                    certificate_chain="certificateChain",
                                    private_key="privateKey"
                                ),
                                sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsSdsCertificateProperty(
                                    secret_name="secretName"
                                )
                            ),
                            mode="mode",
                            validation=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsValidationContextProperty(
                                subject_alternative_names=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNamesProperty(
                                    match=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNameMatchersProperty(
                                        exact=["exact"]
                                    )
                                ),
                                trust=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsValidationContextTrustProperty(
                                    file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty(
                                        certificate_chain="certificateChain"
                                    ),
                                    sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty(
                                        secret_name="secretName"
                                    )
                                )
                            )
                        )
                    )],
                    logging=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayLoggingProperty(
                        access_log=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayAccessLogProperty(
                            file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayFileAccessLogProperty(
                                format=appmesh_mixins.CfnVirtualGatewayPropsMixin.LoggingFormatProperty(
                                    json=[appmesh_mixins.CfnVirtualGatewayPropsMixin.JsonFormatRefProperty(
                                        key="key",
                                        value="value"
                                    )],
                                    text="text"
                                ),
                                path="path"
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9d90e7d7f3d066c21a06e0fc8fd14366d9d103281156735e706d0ef451359f01)
                check_type(argname="argument backend_defaults", value=backend_defaults, expected_type=type_hints["backend_defaults"])
                check_type(argname="argument listeners", value=listeners, expected_type=type_hints["listeners"])
                check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if backend_defaults is not None:
                self._values["backend_defaults"] = backend_defaults
            if listeners is not None:
                self._values["listeners"] = listeners
            if logging is not None:
                self._values["logging"] = logging

        @builtins.property
        def backend_defaults(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayBackendDefaultsProperty"]]:
            '''A reference to an object that represents the defaults for backends.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayspec.html#cfn-appmesh-virtualgateway-virtualgatewayspec-backenddefaults
            '''
            result = self._values.get("backend_defaults")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayBackendDefaultsProperty"]], result)

        @builtins.property
        def listeners(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayListenerProperty"]]]]:
            '''The listeners that the mesh endpoint is expected to receive inbound traffic from.

            You can specify one listener.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayspec.html#cfn-appmesh-virtualgateway-virtualgatewayspec-listeners
            '''
            result = self._values.get("listeners")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayListenerProperty"]]]], result)

        @builtins.property
        def logging(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayLoggingProperty"]]:
            '''An object that represents logging information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewayspec.html#cfn-appmesh-virtualgateway-virtualgatewayspec-logging
            '''
            result = self._values.get("logging")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayLoggingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewaySpecProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextAcmTrustProperty",
        jsii_struct_bases=[],
        name_mapping={"certificate_authority_arns": "certificateAuthorityArns"},
    )
    class VirtualGatewayTlsValidationContextAcmTrustProperty:
        def __init__(
            self,
            *,
            certificate_authority_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''An object that represents a Transport Layer Security (TLS) validation context trust for an Certificate Manager certificate.

            :param certificate_authority_arns: One or more ACM Amazon Resource Name (ARN)s.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontextacmtrust.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_tls_validation_context_acm_trust_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextAcmTrustProperty(
                    certificate_authority_arns=["certificateAuthorityArns"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__59b8bfc6e58191c4517054cc4c6625bedadfe3390464d3ae6e08d9961fe5ce7a)
                check_type(argname="argument certificate_authority_arns", value=certificate_authority_arns, expected_type=type_hints["certificate_authority_arns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_authority_arns is not None:
                self._values["certificate_authority_arns"] = certificate_authority_arns

        @builtins.property
        def certificate_authority_arns(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''One or more ACM Amazon Resource Name (ARN)s.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontextacmtrust.html#cfn-appmesh-virtualgateway-virtualgatewaytlsvalidationcontextacmtrust-certificateauthorityarns
            '''
            result = self._values.get("certificate_authority_arns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayTlsValidationContextAcmTrustProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty",
        jsii_struct_bases=[],
        name_mapping={"certificate_chain": "certificateChain"},
    )
    class VirtualGatewayTlsValidationContextFileTrustProperty:
        def __init__(
            self,
            *,
            certificate_chain: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents a Transport Layer Security (TLS) validation context trust for a local file.

            :param certificate_chain: The certificate trust chain for a certificate stored on the file system of the virtual node that the proxy is running on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontextfiletrust.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_tls_validation_context_file_trust_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty(
                    certificate_chain="certificateChain"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6b3a53215488a26ea2218229137343873a082fbf03c0a1a8d9525b1d445ffa2f)
                check_type(argname="argument certificate_chain", value=certificate_chain, expected_type=type_hints["certificate_chain"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_chain is not None:
                self._values["certificate_chain"] = certificate_chain

        @builtins.property
        def certificate_chain(self) -> typing.Optional[builtins.str]:
            '''The certificate trust chain for a certificate stored on the file system of the virtual node that the proxy is running on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontextfiletrust.html#cfn-appmesh-virtualgateway-virtualgatewaytlsvalidationcontextfiletrust-certificatechain
            '''
            result = self._values.get("certificate_chain")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayTlsValidationContextFileTrustProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextProperty",
        jsii_struct_bases=[],
        name_mapping={
            "subject_alternative_names": "subjectAlternativeNames",
            "trust": "trust",
        },
    )
    class VirtualGatewayTlsValidationContextProperty:
        def __init__(
            self,
            *,
            subject_alternative_names: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.SubjectAlternativeNamesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            trust: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextTrustProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents a Transport Layer Security (TLS) validation context.

            :param subject_alternative_names: A reference to an object that represents the SANs for a virtual gateway's listener's Transport Layer Security (TLS) validation context.
            :param trust: A reference to where to retrieve the trust chain when validating a peer’s Transport Layer Security (TLS) certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontext.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_tls_validation_context_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextProperty(
                    subject_alternative_names=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNamesProperty(
                        match=appmesh_mixins.CfnVirtualGatewayPropsMixin.SubjectAlternativeNameMatchersProperty(
                            exact=["exact"]
                        )
                    ),
                    trust=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextTrustProperty(
                        acm=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextAcmTrustProperty(
                            certificate_authority_arns=["certificateAuthorityArns"]
                        ),
                        file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty(
                            certificate_chain="certificateChain"
                        ),
                        sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty(
                            secret_name="secretName"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5448d5705f0e09591386f16b13d2358565b55075f71178e23d04b7e096305d87)
                check_type(argname="argument subject_alternative_names", value=subject_alternative_names, expected_type=type_hints["subject_alternative_names"])
                check_type(argname="argument trust", value=trust, expected_type=type_hints["trust"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if subject_alternative_names is not None:
                self._values["subject_alternative_names"] = subject_alternative_names
            if trust is not None:
                self._values["trust"] = trust

        @builtins.property
        def subject_alternative_names(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.SubjectAlternativeNamesProperty"]]:
            '''A reference to an object that represents the SANs for a virtual gateway's listener's Transport Layer Security (TLS) validation context.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontext.html#cfn-appmesh-virtualgateway-virtualgatewaytlsvalidationcontext-subjectalternativenames
            '''
            result = self._values.get("subject_alternative_names")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.SubjectAlternativeNamesProperty"]], result)

        @builtins.property
        def trust(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextTrustProperty"]]:
            '''A reference to where to retrieve the trust chain when validating a peer’s Transport Layer Security (TLS) certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontext.html#cfn-appmesh-virtualgateway-virtualgatewaytlsvalidationcontext-trust
            '''
            result = self._values.get("trust")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextTrustProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayTlsValidationContextProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty",
        jsii_struct_bases=[],
        name_mapping={"secret_name": "secretName"},
    )
    class VirtualGatewayTlsValidationContextSdsTrustProperty:
        def __init__(
            self,
            *,
            secret_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents a virtual gateway's listener's Transport Layer Security (TLS) Secret Discovery Service validation context trust.

            The proxy must be configured with a local SDS provider via a Unix Domain Socket. See App Mesh `TLS documentation <https://docs.aws.amazon.com/app-mesh/latest/userguide/tls.html>`_ for more info.

            :param secret_name: A reference to an object that represents the name of the secret for a virtual gateway's Transport Layer Security (TLS) Secret Discovery Service validation context trust.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontextsdstrust.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_tls_validation_context_sds_trust_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty(
                    secret_name="secretName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a8c011b92c19f87ffbea532f0e3f3b2baad0b2bbc397daccd95c4e8da3da40fc)
                check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if secret_name is not None:
                self._values["secret_name"] = secret_name

        @builtins.property
        def secret_name(self) -> typing.Optional[builtins.str]:
            '''A reference to an object that represents the name of the secret for a virtual gateway's Transport Layer Security (TLS) Secret Discovery Service validation context trust.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontextsdstrust.html#cfn-appmesh-virtualgateway-virtualgatewaytlsvalidationcontextsdstrust-secretname
            '''
            result = self._values.get("secret_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayTlsValidationContextSdsTrustProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextTrustProperty",
        jsii_struct_bases=[],
        name_mapping={"acm": "acm", "file": "file", "sds": "sds"},
    )
    class VirtualGatewayTlsValidationContextTrustProperty:
        def __init__(
            self,
            *,
            acm: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextAcmTrustProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            file: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sds: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents a Transport Layer Security (TLS) validation context trust.

            :param acm: A reference to an object that represents a Transport Layer Security (TLS) validation context trust for an Certificate Manager certificate.
            :param file: An object that represents a Transport Layer Security (TLS) validation context trust for a local file.
            :param sds: A reference to an object that represents a virtual gateway's Transport Layer Security (TLS) Secret Discovery Service validation context trust.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontexttrust.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_gateway_tls_validation_context_trust_property = appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextTrustProperty(
                    acm=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextAcmTrustProperty(
                        certificate_authority_arns=["certificateAuthorityArns"]
                    ),
                    file=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty(
                        certificate_chain="certificateChain"
                    ),
                    sds=appmesh_mixins.CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty(
                        secret_name="secretName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2d3d25d307ceb9c1c522f83a3c3e2560fc7de837192f45e5f5df395ece7e999e)
                check_type(argname="argument acm", value=acm, expected_type=type_hints["acm"])
                check_type(argname="argument file", value=file, expected_type=type_hints["file"])
                check_type(argname="argument sds", value=sds, expected_type=type_hints["sds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if acm is not None:
                self._values["acm"] = acm
            if file is not None:
                self._values["file"] = file
            if sds is not None:
                self._values["sds"] = sds

        @builtins.property
        def acm(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextAcmTrustProperty"]]:
            '''A reference to an object that represents a Transport Layer Security (TLS) validation context trust for an Certificate Manager certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontexttrust.html#cfn-appmesh-virtualgateway-virtualgatewaytlsvalidationcontexttrust-acm
            '''
            result = self._values.get("acm")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextAcmTrustProperty"]], result)

        @builtins.property
        def file(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty"]]:
            '''An object that represents a Transport Layer Security (TLS) validation context trust for a local file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontexttrust.html#cfn-appmesh-virtualgateway-virtualgatewaytlsvalidationcontexttrust-file
            '''
            result = self._values.get("file")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty"]], result)

        @builtins.property
        def sds(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty"]]:
            '''A reference to an object that represents a virtual gateway's Transport Layer Security (TLS) Secret Discovery Service validation context trust.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualgateway-virtualgatewaytlsvalidationcontexttrust.html#cfn-appmesh-virtualgateway-virtualgatewaytlsvalidationcontexttrust-sds
            '''
            result = self._values.get("sds")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualGatewayTlsValidationContextTrustProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodeMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "mesh_name": "meshName",
        "mesh_owner": "meshOwner",
        "spec": "spec",
        "tags": "tags",
        "virtual_node_name": "virtualNodeName",
    },
)
class CfnVirtualNodeMixinProps:
    def __init__(
        self,
        *,
        mesh_name: typing.Optional[builtins.str] = None,
        mesh_owner: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.VirtualNodeSpecProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        virtual_node_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnVirtualNodePropsMixin.

        :param mesh_name: The name of the service mesh to create the virtual node in.
        :param mesh_owner: The AWS IAM account ID of the service mesh owner. If the account ID is not your own, then the account that you specify must share the mesh with your account before you can create the resource in the service mesh. For more information about mesh sharing, see `Working with shared meshes <https://docs.aws.amazon.com/app-mesh/latest/userguide/sharing.html>`_ .
        :param spec: The virtual node specification to apply.
        :param tags: Optional metadata that you can apply to the virtual node to assist with categorization and organization. Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.
        :param virtual_node_name: The name to use for the virtual node.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
            
            cfn_virtual_node_mixin_props = appmesh_mixins.CfnVirtualNodeMixinProps(
                mesh_name="meshName",
                mesh_owner="meshOwner",
                spec=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeSpecProperty(
                    backend_defaults=appmesh_mixins.CfnVirtualNodePropsMixin.BackendDefaultsProperty(
                        client_policy=appmesh_mixins.CfnVirtualNodePropsMixin.ClientPolicyProperty(
                            tls=appmesh_mixins.CfnVirtualNodePropsMixin.ClientPolicyTlsProperty(
                                certificate=appmesh_mixins.CfnVirtualNodePropsMixin.ClientTlsCertificateProperty(
                                    file=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty(
                                        certificate_chain="certificateChain",
                                        private_key="privateKey"
                                    ),
                                    sds=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty(
                                        secret_name="secretName"
                                    )
                                ),
                                enforce=False,
                                ports=[123],
                                validation=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextProperty(
                                    subject_alternative_names=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty(
                                        match=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty(
                                            exact=["exact"]
                                        )
                                    ),
                                    trust=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextTrustProperty(
                                        acm=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextAcmTrustProperty(
                                            certificate_authority_arns=["certificateAuthorityArns"]
                                        ),
                                        file=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty(
                                            certificate_chain="certificateChain"
                                        ),
                                        sds=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty(
                                            secret_name="secretName"
                                        )
                                    )
                                )
                            )
                        )
                    ),
                    backends=[appmesh_mixins.CfnVirtualNodePropsMixin.BackendProperty(
                        virtual_service=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualServiceBackendProperty(
                            client_policy=appmesh_mixins.CfnVirtualNodePropsMixin.ClientPolicyProperty(
                                tls=appmesh_mixins.CfnVirtualNodePropsMixin.ClientPolicyTlsProperty(
                                    certificate=appmesh_mixins.CfnVirtualNodePropsMixin.ClientTlsCertificateProperty(
                                        file=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty(
                                            certificate_chain="certificateChain",
                                            private_key="privateKey"
                                        ),
                                        sds=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty(
                                            secret_name="secretName"
                                        )
                                    ),
                                    enforce=False,
                                    ports=[123],
                                    validation=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextProperty(
                                        subject_alternative_names=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty(
                                            match=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty(
                                                exact=["exact"]
                                            )
                                        ),
                                        trust=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextTrustProperty(
                                            acm=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextAcmTrustProperty(
                                                certificate_authority_arns=["certificateAuthorityArns"]
                                            ),
                                            file=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty(
                                                certificate_chain="certificateChain"
                                            ),
                                            sds=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty(
                                                secret_name="secretName"
                                            )
                                        )
                                    )
                                )
                            ),
                            virtual_service_name="virtualServiceName"
                        )
                    )],
                    listeners=[appmesh_mixins.CfnVirtualNodePropsMixin.ListenerProperty(
                        connection_pool=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeConnectionPoolProperty(
                            grpc=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeGrpcConnectionPoolProperty(
                                max_requests=123
                            ),
                            http=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeHttpConnectionPoolProperty(
                                max_connections=123,
                                max_pending_requests=123
                            ),
                            http2=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeHttp2ConnectionPoolProperty(
                                max_requests=123
                            ),
                            tcp=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeTcpConnectionPoolProperty(
                                max_connections=123
                            )
                        ),
                        health_check=appmesh_mixins.CfnVirtualNodePropsMixin.HealthCheckProperty(
                            healthy_threshold=123,
                            interval_millis=123,
                            path="path",
                            port=123,
                            protocol="protocol",
                            timeout_millis=123,
                            unhealthy_threshold=123
                        ),
                        outlier_detection=appmesh_mixins.CfnVirtualNodePropsMixin.OutlierDetectionProperty(
                            base_ejection_duration=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            ),
                            interval=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            ),
                            max_ejection_percent=123,
                            max_server_errors=123
                        ),
                        port_mapping=appmesh_mixins.CfnVirtualNodePropsMixin.PortMappingProperty(
                            port=123,
                            protocol="protocol"
                        ),
                        timeout=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTimeoutProperty(
                            grpc=appmesh_mixins.CfnVirtualNodePropsMixin.GrpcTimeoutProperty(
                                idle=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                    unit="unit",
                                    value=123
                                ),
                                per_request=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                    unit="unit",
                                    value=123
                                )
                            ),
                            http=appmesh_mixins.CfnVirtualNodePropsMixin.HttpTimeoutProperty(
                                idle=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                    unit="unit",
                                    value=123
                                ),
                                per_request=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                    unit="unit",
                                    value=123
                                )
                            ),
                            http2=appmesh_mixins.CfnVirtualNodePropsMixin.HttpTimeoutProperty(
                                idle=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                    unit="unit",
                                    value=123
                                ),
                                per_request=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                    unit="unit",
                                    value=123
                                )
                            ),
                            tcp=appmesh_mixins.CfnVirtualNodePropsMixin.TcpTimeoutProperty(
                                idle=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                    unit="unit",
                                    value=123
                                )
                            )
                        ),
                        tls=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsProperty(
                            certificate=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsCertificateProperty(
                                acm=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsAcmCertificateProperty(
                                    certificate_arn="certificateArn"
                                ),
                                file=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty(
                                    certificate_chain="certificateChain",
                                    private_key="privateKey"
                                ),
                                sds=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty(
                                    secret_name="secretName"
                                )
                            ),
                            mode="mode",
                            validation=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsValidationContextProperty(
                                subject_alternative_names=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty(
                                    match=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty(
                                        exact=["exact"]
                                    )
                                ),
                                trust=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsValidationContextTrustProperty(
                                    file=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty(
                                        certificate_chain="certificateChain"
                                    ),
                                    sds=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty(
                                        secret_name="secretName"
                                    )
                                )
                            )
                        )
                    )],
                    logging=appmesh_mixins.CfnVirtualNodePropsMixin.LoggingProperty(
                        access_log=appmesh_mixins.CfnVirtualNodePropsMixin.AccessLogProperty(
                            file=appmesh_mixins.CfnVirtualNodePropsMixin.FileAccessLogProperty(
                                format=appmesh_mixins.CfnVirtualNodePropsMixin.LoggingFormatProperty(
                                    json=[appmesh_mixins.CfnVirtualNodePropsMixin.JsonFormatRefProperty(
                                        key="key",
                                        value="value"
                                    )],
                                    text="text"
                                ),
                                path="path"
                            )
                        )
                    ),
                    service_discovery=appmesh_mixins.CfnVirtualNodePropsMixin.ServiceDiscoveryProperty(
                        aws_cloud_map=appmesh_mixins.CfnVirtualNodePropsMixin.AwsCloudMapServiceDiscoveryProperty(
                            attributes=[appmesh_mixins.CfnVirtualNodePropsMixin.AwsCloudMapInstanceAttributeProperty(
                                key="key",
                                value="value"
                            )],
                            ip_preference="ipPreference",
                            namespace_name="namespaceName",
                            service_name="serviceName"
                        ),
                        dns=appmesh_mixins.CfnVirtualNodePropsMixin.DnsServiceDiscoveryProperty(
                            hostname="hostname",
                            ip_preference="ipPreference",
                            response_type="responseType"
                        )
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                virtual_node_name="virtualNodeName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c250c8231c076d8813fc05af396a6b02bfc5651780ab66e786939020f4b15c8)
            check_type(argname="argument mesh_name", value=mesh_name, expected_type=type_hints["mesh_name"])
            check_type(argname="argument mesh_owner", value=mesh_owner, expected_type=type_hints["mesh_owner"])
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument virtual_node_name", value=virtual_node_name, expected_type=type_hints["virtual_node_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mesh_name is not None:
            self._values["mesh_name"] = mesh_name
        if mesh_owner is not None:
            self._values["mesh_owner"] = mesh_owner
        if spec is not None:
            self._values["spec"] = spec
        if tags is not None:
            self._values["tags"] = tags
        if virtual_node_name is not None:
            self._values["virtual_node_name"] = virtual_node_name

    @builtins.property
    def mesh_name(self) -> typing.Optional[builtins.str]:
        '''The name of the service mesh to create the virtual node in.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-meshname
        '''
        result = self._values.get("mesh_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mesh_owner(self) -> typing.Optional[builtins.str]:
        '''The AWS IAM account ID of the service mesh owner.

        If the account ID is not your own, then the account that you specify must share the mesh with your account before you can create the resource in the service mesh. For more information about mesh sharing, see `Working with shared meshes <https://docs.aws.amazon.com/app-mesh/latest/userguide/sharing.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-meshowner
        '''
        result = self._values.get("mesh_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spec(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.VirtualNodeSpecProperty"]]:
        '''The virtual node specification to apply.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-spec
        '''
        result = self._values.get("spec")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.VirtualNodeSpecProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Optional metadata that you can apply to the virtual node to assist with categorization and organization.

        Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def virtual_node_name(self) -> typing.Optional[builtins.str]:
        '''The name to use for the virtual node.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-virtualnodename
        '''
        result = self._values.get("virtual_node_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVirtualNodeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVirtualNodePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin",
):
    '''Creates a virtual node within a service mesh.

    A virtual node acts as a logical pointer to a particular task group, such as an Amazon ECS service or a Kubernetes deployment. When you create a virtual node, you can specify the service discovery information for your task group, and whether the proxy running in a task group will communicate with other proxies using Transport Layer Security (TLS).

    You define a ``listener`` for any inbound traffic that your virtual node expects. Any virtual service that your virtual node expects to communicate to is specified as a ``backend`` .

    The response metadata for your new virtual node contains the ``arn`` that is associated with the virtual node. Set this value to the full ARN; for example, ``arn:aws:appmesh:us-west-2:123456789012:myMesh/default/virtualNode/myApp`` ) as the ``APPMESH_RESOURCE_ARN`` environment variable for your task group's Envoy proxy container in your task definition or pod spec. This is then mapped to the ``node.id`` and ``node.cluster`` Envoy parameters.
    .. epigraph::

       By default, App Mesh uses the name of the resource you specified in ``APPMESH_RESOURCE_ARN`` when Envoy is referring to itself in metrics and traces. You can override this behavior by setting the ``APPMESH_RESOURCE_CLUSTER`` environment variable with your own name.

    For more information about virtual nodes, see `Virtual nodes <https://docs.aws.amazon.com/app-mesh/latest/userguide/virtual_nodes.html>`_ . You must be using ``1.15.0`` or later of the Envoy image when setting these variables. For more information aboutApp Mesh Envoy variables, see `Envoy image <https://docs.aws.amazon.com/app-mesh/latest/userguide/envoy.html>`_ in the AWS App Mesh User Guide.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html
    :cloudformationResource: AWS::AppMesh::VirtualNode
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
        
        cfn_virtual_node_props_mixin = appmesh_mixins.CfnVirtualNodePropsMixin(appmesh_mixins.CfnVirtualNodeMixinProps(
            mesh_name="meshName",
            mesh_owner="meshOwner",
            spec=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeSpecProperty(
                backend_defaults=appmesh_mixins.CfnVirtualNodePropsMixin.BackendDefaultsProperty(
                    client_policy=appmesh_mixins.CfnVirtualNodePropsMixin.ClientPolicyProperty(
                        tls=appmesh_mixins.CfnVirtualNodePropsMixin.ClientPolicyTlsProperty(
                            certificate=appmesh_mixins.CfnVirtualNodePropsMixin.ClientTlsCertificateProperty(
                                file=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty(
                                    certificate_chain="certificateChain",
                                    private_key="privateKey"
                                ),
                                sds=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty(
                                    secret_name="secretName"
                                )
                            ),
                            enforce=False,
                            ports=[123],
                            validation=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextProperty(
                                subject_alternative_names=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty(
                                    match=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty(
                                        exact=["exact"]
                                    )
                                ),
                                trust=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextTrustProperty(
                                    acm=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextAcmTrustProperty(
                                        certificate_authority_arns=["certificateAuthorityArns"]
                                    ),
                                    file=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty(
                                        certificate_chain="certificateChain"
                                    ),
                                    sds=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty(
                                        secret_name="secretName"
                                    )
                                )
                            )
                        )
                    )
                ),
                backends=[appmesh_mixins.CfnVirtualNodePropsMixin.BackendProperty(
                    virtual_service=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualServiceBackendProperty(
                        client_policy=appmesh_mixins.CfnVirtualNodePropsMixin.ClientPolicyProperty(
                            tls=appmesh_mixins.CfnVirtualNodePropsMixin.ClientPolicyTlsProperty(
                                certificate=appmesh_mixins.CfnVirtualNodePropsMixin.ClientTlsCertificateProperty(
                                    file=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty(
                                        certificate_chain="certificateChain",
                                        private_key="privateKey"
                                    ),
                                    sds=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty(
                                        secret_name="secretName"
                                    )
                                ),
                                enforce=False,
                                ports=[123],
                                validation=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextProperty(
                                    subject_alternative_names=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty(
                                        match=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty(
                                            exact=["exact"]
                                        )
                                    ),
                                    trust=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextTrustProperty(
                                        acm=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextAcmTrustProperty(
                                            certificate_authority_arns=["certificateAuthorityArns"]
                                        ),
                                        file=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty(
                                            certificate_chain="certificateChain"
                                        ),
                                        sds=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty(
                                            secret_name="secretName"
                                        )
                                    )
                                )
                            )
                        ),
                        virtual_service_name="virtualServiceName"
                    )
                )],
                listeners=[appmesh_mixins.CfnVirtualNodePropsMixin.ListenerProperty(
                    connection_pool=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeConnectionPoolProperty(
                        grpc=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeGrpcConnectionPoolProperty(
                            max_requests=123
                        ),
                        http=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeHttpConnectionPoolProperty(
                            max_connections=123,
                            max_pending_requests=123
                        ),
                        http2=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeHttp2ConnectionPoolProperty(
                            max_requests=123
                        ),
                        tcp=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeTcpConnectionPoolProperty(
                            max_connections=123
                        )
                    ),
                    health_check=appmesh_mixins.CfnVirtualNodePropsMixin.HealthCheckProperty(
                        healthy_threshold=123,
                        interval_millis=123,
                        path="path",
                        port=123,
                        protocol="protocol",
                        timeout_millis=123,
                        unhealthy_threshold=123
                    ),
                    outlier_detection=appmesh_mixins.CfnVirtualNodePropsMixin.OutlierDetectionProperty(
                        base_ejection_duration=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        ),
                        interval=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        ),
                        max_ejection_percent=123,
                        max_server_errors=123
                    ),
                    port_mapping=appmesh_mixins.CfnVirtualNodePropsMixin.PortMappingProperty(
                        port=123,
                        protocol="protocol"
                    ),
                    timeout=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTimeoutProperty(
                        grpc=appmesh_mixins.CfnVirtualNodePropsMixin.GrpcTimeoutProperty(
                            idle=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            ),
                            per_request=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            )
                        ),
                        http=appmesh_mixins.CfnVirtualNodePropsMixin.HttpTimeoutProperty(
                            idle=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            ),
                            per_request=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            )
                        ),
                        http2=appmesh_mixins.CfnVirtualNodePropsMixin.HttpTimeoutProperty(
                            idle=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            ),
                            per_request=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            )
                        ),
                        tcp=appmesh_mixins.CfnVirtualNodePropsMixin.TcpTimeoutProperty(
                            idle=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            )
                        )
                    ),
                    tls=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsProperty(
                        certificate=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsCertificateProperty(
                            acm=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsAcmCertificateProperty(
                                certificate_arn="certificateArn"
                            ),
                            file=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty(
                                certificate_chain="certificateChain",
                                private_key="privateKey"
                            ),
                            sds=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty(
                                secret_name="secretName"
                            )
                        ),
                        mode="mode",
                        validation=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsValidationContextProperty(
                            subject_alternative_names=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty(
                                match=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty(
                                    exact=["exact"]
                                )
                            ),
                            trust=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsValidationContextTrustProperty(
                                file=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty(
                                    certificate_chain="certificateChain"
                                ),
                                sds=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty(
                                    secret_name="secretName"
                                )
                            )
                        )
                    )
                )],
                logging=appmesh_mixins.CfnVirtualNodePropsMixin.LoggingProperty(
                    access_log=appmesh_mixins.CfnVirtualNodePropsMixin.AccessLogProperty(
                        file=appmesh_mixins.CfnVirtualNodePropsMixin.FileAccessLogProperty(
                            format=appmesh_mixins.CfnVirtualNodePropsMixin.LoggingFormatProperty(
                                json=[appmesh_mixins.CfnVirtualNodePropsMixin.JsonFormatRefProperty(
                                    key="key",
                                    value="value"
                                )],
                                text="text"
                            ),
                            path="path"
                        )
                    )
                ),
                service_discovery=appmesh_mixins.CfnVirtualNodePropsMixin.ServiceDiscoveryProperty(
                    aws_cloud_map=appmesh_mixins.CfnVirtualNodePropsMixin.AwsCloudMapServiceDiscoveryProperty(
                        attributes=[appmesh_mixins.CfnVirtualNodePropsMixin.AwsCloudMapInstanceAttributeProperty(
                            key="key",
                            value="value"
                        )],
                        ip_preference="ipPreference",
                        namespace_name="namespaceName",
                        service_name="serviceName"
                    ),
                    dns=appmesh_mixins.CfnVirtualNodePropsMixin.DnsServiceDiscoveryProperty(
                        hostname="hostname",
                        ip_preference="ipPreference",
                        response_type="responseType"
                    )
                )
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            virtual_node_name="virtualNodeName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVirtualNodeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppMesh::VirtualNode``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe5580f7aa2a4dc20f82281aa6278fdf9c8554786913aee6b4b8a0bc8f5c767e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb9334bdff07c5981e6161ae821521b7cf8dc820e73d94e324cb8d7ab0f310ab)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb2e407202864b10aa5e0ba461e2cf4d3bcb5cef88ca7097855550deababc2b8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVirtualNodeMixinProps:
        return typing.cast(CfnVirtualNodeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.AccessLogProperty",
        jsii_struct_bases=[],
        name_mapping={"file": "file"},
    )
    class AccessLogProperty:
        def __init__(
            self,
            *,
            file: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.FileAccessLogProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents the access logging information for a virtual node.

            :param file: The file object to send virtual node access logs to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-accesslog.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                access_log_property = appmesh_mixins.CfnVirtualNodePropsMixin.AccessLogProperty(
                    file=appmesh_mixins.CfnVirtualNodePropsMixin.FileAccessLogProperty(
                        format=appmesh_mixins.CfnVirtualNodePropsMixin.LoggingFormatProperty(
                            json=[appmesh_mixins.CfnVirtualNodePropsMixin.JsonFormatRefProperty(
                                key="key",
                                value="value"
                            )],
                            text="text"
                        ),
                        path="path"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__47a3888e48ad2be64155a9f6c448a252efbf7c7dc9cfaeea935112216f6bb4ea)
                check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if file is not None:
                self._values["file"] = file

        @builtins.property
        def file(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.FileAccessLogProperty"]]:
            '''The file object to send virtual node access logs to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-accesslog.html#cfn-appmesh-virtualnode-accesslog-file
            '''
            result = self._values.get("file")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.FileAccessLogProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessLogProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.AwsCloudMapInstanceAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class AwsCloudMapInstanceAttributeProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the AWS Cloud Map attribute information for your virtual node.

            .. epigraph::

               AWS Cloud Map is not available in the eu-south-1 Region.

            :param key: The name of an AWS Cloud Map service instance attribute key. Any AWS Cloud Map service instance that contains the specified key and value is returned.
            :param value: The value of an AWS Cloud Map service instance attribute key. Any AWS Cloud Map service instance that contains the specified key and value is returned.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-awscloudmapinstanceattribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                aws_cloud_map_instance_attribute_property = appmesh_mixins.CfnVirtualNodePropsMixin.AwsCloudMapInstanceAttributeProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1ef3cd9d2db477050cfc8000a7cb178d67cb79bd372a69c333f484565c254683)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The name of an AWS Cloud Map service instance attribute key.

            Any AWS Cloud Map service instance that contains the specified key and value is returned.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-awscloudmapinstanceattribute.html#cfn-appmesh-virtualnode-awscloudmapinstanceattribute-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of an AWS Cloud Map service instance attribute key.

            Any AWS Cloud Map service instance that contains the specified key and value is returned.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-awscloudmapinstanceattribute.html#cfn-appmesh-virtualnode-awscloudmapinstanceattribute-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AwsCloudMapInstanceAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.AwsCloudMapServiceDiscoveryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attributes": "attributes",
            "ip_preference": "ipPreference",
            "namespace_name": "namespaceName",
            "service_name": "serviceName",
        },
    )
    class AwsCloudMapServiceDiscoveryProperty:
        def __init__(
            self,
            *,
            attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.AwsCloudMapInstanceAttributeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ip_preference: typing.Optional[builtins.str] = None,
            namespace_name: typing.Optional[builtins.str] = None,
            service_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the AWS Cloud Map service discovery information for your virtual node.

            .. epigraph::

               AWS Cloud Map is not available in the eu-south-1 Region.

            :param attributes: A string map that contains attributes with values that you can use to filter instances by any custom attribute that you specified when you registered the instance. Only instances that match all of the specified key/value pairs will be returned.
            :param ip_preference: The preferred IP version that this virtual node uses. Setting the IP preference on the virtual node only overrides the IP preference set for the mesh on this specific node.
            :param namespace_name: The HTTP name of the AWS Cloud Map namespace to use.
            :param service_name: The name of the AWS Cloud Map service to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-awscloudmapservicediscovery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                aws_cloud_map_service_discovery_property = appmesh_mixins.CfnVirtualNodePropsMixin.AwsCloudMapServiceDiscoveryProperty(
                    attributes=[appmesh_mixins.CfnVirtualNodePropsMixin.AwsCloudMapInstanceAttributeProperty(
                        key="key",
                        value="value"
                    )],
                    ip_preference="ipPreference",
                    namespace_name="namespaceName",
                    service_name="serviceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8f0143c1bab6c6f6274125f8bfbfc76be1091a897b7027550514debc042779a3)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                check_type(argname="argument ip_preference", value=ip_preference, expected_type=type_hints["ip_preference"])
                check_type(argname="argument namespace_name", value=namespace_name, expected_type=type_hints["namespace_name"])
                check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if ip_preference is not None:
                self._values["ip_preference"] = ip_preference
            if namespace_name is not None:
                self._values["namespace_name"] = namespace_name
            if service_name is not None:
                self._values["service_name"] = service_name

        @builtins.property
        def attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.AwsCloudMapInstanceAttributeProperty"]]]]:
            '''A string map that contains attributes with values that you can use to filter instances by any custom attribute that you specified when you registered the instance.

            Only instances that match all of the specified key/value pairs will be returned.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-awscloudmapservicediscovery.html#cfn-appmesh-virtualnode-awscloudmapservicediscovery-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.AwsCloudMapInstanceAttributeProperty"]]]], result)

        @builtins.property
        def ip_preference(self) -> typing.Optional[builtins.str]:
            '''The preferred IP version that this virtual node uses.

            Setting the IP preference on the virtual node only overrides the IP preference set for the mesh on this specific node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-awscloudmapservicediscovery.html#cfn-appmesh-virtualnode-awscloudmapservicediscovery-ippreference
            '''
            result = self._values.get("ip_preference")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespace_name(self) -> typing.Optional[builtins.str]:
            '''The HTTP name of the AWS Cloud Map namespace to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-awscloudmapservicediscovery.html#cfn-appmesh-virtualnode-awscloudmapservicediscovery-namespacename
            '''
            result = self._values.get("namespace_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_name(self) -> typing.Optional[builtins.str]:
            '''The name of the AWS Cloud Map service to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-awscloudmapservicediscovery.html#cfn-appmesh-virtualnode-awscloudmapservicediscovery-servicename
            '''
            result = self._values.get("service_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AwsCloudMapServiceDiscoveryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.BackendDefaultsProperty",
        jsii_struct_bases=[],
        name_mapping={"client_policy": "clientPolicy"},
    )
    class BackendDefaultsProperty:
        def __init__(
            self,
            *,
            client_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.ClientPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents the default properties for a backend.

            :param client_policy: A reference to an object that represents a client policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-backenddefaults.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                backend_defaults_property = appmesh_mixins.CfnVirtualNodePropsMixin.BackendDefaultsProperty(
                    client_policy=appmesh_mixins.CfnVirtualNodePropsMixin.ClientPolicyProperty(
                        tls=appmesh_mixins.CfnVirtualNodePropsMixin.ClientPolicyTlsProperty(
                            certificate=appmesh_mixins.CfnVirtualNodePropsMixin.ClientTlsCertificateProperty(
                                file=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty(
                                    certificate_chain="certificateChain",
                                    private_key="privateKey"
                                ),
                                sds=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty(
                                    secret_name="secretName"
                                )
                            ),
                            enforce=False,
                            ports=[123],
                            validation=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextProperty(
                                subject_alternative_names=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty(
                                    match=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty(
                                        exact=["exact"]
                                    )
                                ),
                                trust=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextTrustProperty(
                                    acm=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextAcmTrustProperty(
                                        certificate_authority_arns=["certificateAuthorityArns"]
                                    ),
                                    file=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty(
                                        certificate_chain="certificateChain"
                                    ),
                                    sds=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty(
                                        secret_name="secretName"
                                    )
                                )
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2dd7534d6b589caba59b900a64475b823510735c68b6ad654c3c020f9046303d)
                check_type(argname="argument client_policy", value=client_policy, expected_type=type_hints["client_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if client_policy is not None:
                self._values["client_policy"] = client_policy

        @builtins.property
        def client_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ClientPolicyProperty"]]:
            '''A reference to an object that represents a client policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-backenddefaults.html#cfn-appmesh-virtualnode-backenddefaults-clientpolicy
            '''
            result = self._values.get("client_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ClientPolicyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BackendDefaultsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.BackendProperty",
        jsii_struct_bases=[],
        name_mapping={"virtual_service": "virtualService"},
    )
    class BackendProperty:
        def __init__(
            self,
            *,
            virtual_service: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.VirtualServiceBackendProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents the backends that a virtual node is expected to send outbound traffic to.

            :param virtual_service: Specifies a virtual service to use as a backend.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-backend.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                backend_property = appmesh_mixins.CfnVirtualNodePropsMixin.BackendProperty(
                    virtual_service=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualServiceBackendProperty(
                        client_policy=appmesh_mixins.CfnVirtualNodePropsMixin.ClientPolicyProperty(
                            tls=appmesh_mixins.CfnVirtualNodePropsMixin.ClientPolicyTlsProperty(
                                certificate=appmesh_mixins.CfnVirtualNodePropsMixin.ClientTlsCertificateProperty(
                                    file=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty(
                                        certificate_chain="certificateChain",
                                        private_key="privateKey"
                                    ),
                                    sds=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty(
                                        secret_name="secretName"
                                    )
                                ),
                                enforce=False,
                                ports=[123],
                                validation=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextProperty(
                                    subject_alternative_names=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty(
                                        match=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty(
                                            exact=["exact"]
                                        )
                                    ),
                                    trust=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextTrustProperty(
                                        acm=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextAcmTrustProperty(
                                            certificate_authority_arns=["certificateAuthorityArns"]
                                        ),
                                        file=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty(
                                            certificate_chain="certificateChain"
                                        ),
                                        sds=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty(
                                            secret_name="secretName"
                                        )
                                    )
                                )
                            )
                        ),
                        virtual_service_name="virtualServiceName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__548f88788ddf1750033f10b15a8ef9b56cd9c60200ecc2b54fed2a1ce371a334)
                check_type(argname="argument virtual_service", value=virtual_service, expected_type=type_hints["virtual_service"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if virtual_service is not None:
                self._values["virtual_service"] = virtual_service

        @builtins.property
        def virtual_service(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.VirtualServiceBackendProperty"]]:
            '''Specifies a virtual service to use as a backend.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-backend.html#cfn-appmesh-virtualnode-backend-virtualservice
            '''
            result = self._values.get("virtual_service")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.VirtualServiceBackendProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BackendProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.ClientPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"tls": "tls"},
    )
    class ClientPolicyProperty:
        def __init__(
            self,
            *,
            tls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.ClientPolicyTlsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents a client policy.

            :param tls: A reference to an object that represents a Transport Layer Security (TLS) client policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clientpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                client_policy_property = appmesh_mixins.CfnVirtualNodePropsMixin.ClientPolicyProperty(
                    tls=appmesh_mixins.CfnVirtualNodePropsMixin.ClientPolicyTlsProperty(
                        certificate=appmesh_mixins.CfnVirtualNodePropsMixin.ClientTlsCertificateProperty(
                            file=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty(
                                certificate_chain="certificateChain",
                                private_key="privateKey"
                            ),
                            sds=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty(
                                secret_name="secretName"
                            )
                        ),
                        enforce=False,
                        ports=[123],
                        validation=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextProperty(
                            subject_alternative_names=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty(
                                match=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty(
                                    exact=["exact"]
                                )
                            ),
                            trust=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextTrustProperty(
                                acm=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextAcmTrustProperty(
                                    certificate_authority_arns=["certificateAuthorityArns"]
                                ),
                                file=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty(
                                    certificate_chain="certificateChain"
                                ),
                                sds=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty(
                                    secret_name="secretName"
                                )
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d8c1c33504fcc327c062cc07213644ae1d90f7ac626d6ebf2362368da2c6568)
                check_type(argname="argument tls", value=tls, expected_type=type_hints["tls"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if tls is not None:
                self._values["tls"] = tls

        @builtins.property
        def tls(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ClientPolicyTlsProperty"]]:
            '''A reference to an object that represents a Transport Layer Security (TLS) client policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clientpolicy.html#cfn-appmesh-virtualnode-clientpolicy-tls
            '''
            result = self._values.get("tls")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ClientPolicyTlsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ClientPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.ClientPolicyTlsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate": "certificate",
            "enforce": "enforce",
            "ports": "ports",
            "validation": "validation",
        },
    )
    class ClientPolicyTlsProperty:
        def __init__(
            self,
            *,
            certificate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.ClientTlsCertificateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enforce: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            ports: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
            validation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.TlsValidationContextProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A reference to an object that represents a Transport Layer Security (TLS) client policy.

            :param certificate: A reference to an object that represents a client's TLS certificate.
            :param enforce: Whether the policy is enforced. The default is ``True`` , if a value isn't specified.
            :param ports: One or more ports that the policy is enforced for.
            :param validation: A reference to an object that represents a TLS validation context.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clientpolicytls.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                client_policy_tls_property = appmesh_mixins.CfnVirtualNodePropsMixin.ClientPolicyTlsProperty(
                    certificate=appmesh_mixins.CfnVirtualNodePropsMixin.ClientTlsCertificateProperty(
                        file=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty(
                            certificate_chain="certificateChain",
                            private_key="privateKey"
                        ),
                        sds=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty(
                            secret_name="secretName"
                        )
                    ),
                    enforce=False,
                    ports=[123],
                    validation=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextProperty(
                        subject_alternative_names=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty(
                            match=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty(
                                exact=["exact"]
                            )
                        ),
                        trust=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextTrustProperty(
                            acm=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextAcmTrustProperty(
                                certificate_authority_arns=["certificateAuthorityArns"]
                            ),
                            file=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty(
                                certificate_chain="certificateChain"
                            ),
                            sds=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty(
                                secret_name="secretName"
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ab8a44a9bef26852f33da3725c56e1327362b4c0aab5561d13ca6cbd7d7e8785)
                check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
                check_type(argname="argument enforce", value=enforce, expected_type=type_hints["enforce"])
                check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
                check_type(argname="argument validation", value=validation, expected_type=type_hints["validation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate is not None:
                self._values["certificate"] = certificate
            if enforce is not None:
                self._values["enforce"] = enforce
            if ports is not None:
                self._values["ports"] = ports
            if validation is not None:
                self._values["validation"] = validation

        @builtins.property
        def certificate(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ClientTlsCertificateProperty"]]:
            '''A reference to an object that represents a client's TLS certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clientpolicytls.html#cfn-appmesh-virtualnode-clientpolicytls-certificate
            '''
            result = self._values.get("certificate")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ClientTlsCertificateProperty"]], result)

        @builtins.property
        def enforce(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether the policy is enforced.

            The default is ``True`` , if a value isn't specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clientpolicytls.html#cfn-appmesh-virtualnode-clientpolicytls-enforce
            '''
            result = self._values.get("enforce")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def ports(
            self,
        ) -> typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]]:
            '''One or more ports that the policy is enforced for.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clientpolicytls.html#cfn-appmesh-virtualnode-clientpolicytls-ports
            '''
            result = self._values.get("ports")
            return typing.cast(typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def validation(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.TlsValidationContextProperty"]]:
            '''A reference to an object that represents a TLS validation context.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clientpolicytls.html#cfn-appmesh-virtualnode-clientpolicytls-validation
            '''
            result = self._values.get("validation")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.TlsValidationContextProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ClientPolicyTlsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.ClientTlsCertificateProperty",
        jsii_struct_bases=[],
        name_mapping={"file": "file", "sds": "sds"},
    )
    class ClientTlsCertificateProperty:
        def __init__(
            self,
            *,
            file: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sds: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents the client's certificate.

            :param file: An object that represents a local file certificate. The certificate must meet specific requirements and you must have proxy authorization enabled. For more information, see `Transport Layer Security (TLS) <https://docs.aws.amazon.com/app-mesh/latest/userguide/tls.html>`_ .
            :param sds: A reference to an object that represents a client's TLS Secret Discovery Service certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clienttlscertificate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                client_tls_certificate_property = appmesh_mixins.CfnVirtualNodePropsMixin.ClientTlsCertificateProperty(
                    file=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty(
                        certificate_chain="certificateChain",
                        private_key="privateKey"
                    ),
                    sds=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty(
                        secret_name="secretName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5de98cba585287eb3247475dc8b6f1b6c2419a1ee83bafa6c00f42d27d1ff2f1)
                check_type(argname="argument file", value=file, expected_type=type_hints["file"])
                check_type(argname="argument sds", value=sds, expected_type=type_hints["sds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if file is not None:
                self._values["file"] = file
            if sds is not None:
                self._values["sds"] = sds

        @builtins.property
        def file(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty"]]:
            '''An object that represents a local file certificate.

            The certificate must meet specific requirements and you must have proxy authorization enabled. For more information, see `Transport Layer Security (TLS) <https://docs.aws.amazon.com/app-mesh/latest/userguide/tls.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clienttlscertificate.html#cfn-appmesh-virtualnode-clienttlscertificate-file
            '''
            result = self._values.get("file")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty"]], result)

        @builtins.property
        def sds(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty"]]:
            '''A reference to an object that represents a client's TLS Secret Discovery Service certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clienttlscertificate.html#cfn-appmesh-virtualnode-clienttlscertificate-sds
            '''
            result = self._values.get("sds")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ClientTlsCertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.DnsServiceDiscoveryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hostname": "hostname",
            "ip_preference": "ipPreference",
            "response_type": "responseType",
        },
    )
    class DnsServiceDiscoveryProperty:
        def __init__(
            self,
            *,
            hostname: typing.Optional[builtins.str] = None,
            ip_preference: typing.Optional[builtins.str] = None,
            response_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the DNS service discovery information for your virtual node.

            :param hostname: Specifies the DNS service discovery hostname for the virtual node.
            :param ip_preference: The preferred IP version that this virtual node uses. Setting the IP preference on the virtual node only overrides the IP preference set for the mesh on this specific node.
            :param response_type: Specifies the DNS response type for the virtual node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-dnsservicediscovery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                dns_service_discovery_property = appmesh_mixins.CfnVirtualNodePropsMixin.DnsServiceDiscoveryProperty(
                    hostname="hostname",
                    ip_preference="ipPreference",
                    response_type="responseType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3a07881c1e18cdd403f5968e06d9cbecd212d6b7c8c6b34766fc8cd148df9a4f)
                check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
                check_type(argname="argument ip_preference", value=ip_preference, expected_type=type_hints["ip_preference"])
                check_type(argname="argument response_type", value=response_type, expected_type=type_hints["response_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if hostname is not None:
                self._values["hostname"] = hostname
            if ip_preference is not None:
                self._values["ip_preference"] = ip_preference
            if response_type is not None:
                self._values["response_type"] = response_type

        @builtins.property
        def hostname(self) -> typing.Optional[builtins.str]:
            '''Specifies the DNS service discovery hostname for the virtual node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-dnsservicediscovery.html#cfn-appmesh-virtualnode-dnsservicediscovery-hostname
            '''
            result = self._values.get("hostname")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ip_preference(self) -> typing.Optional[builtins.str]:
            '''The preferred IP version that this virtual node uses.

            Setting the IP preference on the virtual node only overrides the IP preference set for the mesh on this specific node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-dnsservicediscovery.html#cfn-appmesh-virtualnode-dnsservicediscovery-ippreference
            '''
            result = self._values.get("ip_preference")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def response_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the DNS response type for the virtual node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-dnsservicediscovery.html#cfn-appmesh-virtualnode-dnsservicediscovery-responsetype
            '''
            result = self._values.get("response_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DnsServiceDiscoveryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.DurationProperty",
        jsii_struct_bases=[],
        name_mapping={"unit": "unit", "value": "value"},
    )
    class DurationProperty:
        def __init__(
            self,
            *,
            unit: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An object that represents a duration of time.

            :param unit: A unit of time.
            :param value: A number of time units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-duration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                duration_property = appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                    unit="unit",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e3a50646cb43e85fbf3c0e4792d85e1a439f4c2e9be0b147bd576d728a181c8b)
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if unit is not None:
                self._values["unit"] = unit
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''A unit of time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-duration.html#cfn-appmesh-virtualnode-duration-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''A number of time units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-duration.html#cfn-appmesh-virtualnode-duration-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.FileAccessLogProperty",
        jsii_struct_bases=[],
        name_mapping={"format": "format", "path": "path"},
    )
    class FileAccessLogProperty:
        def __init__(
            self,
            *,
            format: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.LoggingFormatProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents an access log file.

            :param format: The specified format for the logs. The format is either ``json_format`` or ``text_format`` .
            :param path: The file path to write access logs to. You can use ``/dev/stdout`` to send access logs to standard out and configure your Envoy container to use a log driver, such as ``awslogs`` , to export the access logs to a log storage service such as Amazon CloudWatch Logs. You can also specify a path in the Envoy container's file system to write the files to disk. .. epigraph:: The Envoy process must have write permissions to the path that you specify here. Otherwise, Envoy fails to bootstrap properly.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-fileaccesslog.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                file_access_log_property = appmesh_mixins.CfnVirtualNodePropsMixin.FileAccessLogProperty(
                    format=appmesh_mixins.CfnVirtualNodePropsMixin.LoggingFormatProperty(
                        json=[appmesh_mixins.CfnVirtualNodePropsMixin.JsonFormatRefProperty(
                            key="key",
                            value="value"
                        )],
                        text="text"
                    ),
                    path="path"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0e159e002948d1bce060e9fd8d1830790747e4ba9a78a1ccd3aa866c6bff2eee)
                check_type(argname="argument format", value=format, expected_type=type_hints["format"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if format is not None:
                self._values["format"] = format
            if path is not None:
                self._values["path"] = path

        @builtins.property
        def format(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.LoggingFormatProperty"]]:
            '''The specified format for the logs.

            The format is either ``json_format`` or ``text_format`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-fileaccesslog.html#cfn-appmesh-virtualnode-fileaccesslog-format
            '''
            result = self._values.get("format")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.LoggingFormatProperty"]], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The file path to write access logs to.

            You can use ``/dev/stdout`` to send access logs to standard out and configure your Envoy container to use a log driver, such as ``awslogs`` , to export the access logs to a log storage service such as Amazon CloudWatch Logs. You can also specify a path in the Envoy container's file system to write the files to disk.
            .. epigraph::

               The Envoy process must have write permissions to the path that you specify here. Otherwise, Envoy fails to bootstrap properly.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-fileaccesslog.html#cfn-appmesh-virtualnode-fileaccesslog-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FileAccessLogProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.GrpcTimeoutProperty",
        jsii_struct_bases=[],
        name_mapping={"idle": "idle", "per_request": "perRequest"},
    )
    class GrpcTimeoutProperty:
        def __init__(
            self,
            *,
            idle: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.DurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            per_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.DurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents types of timeouts.

            :param idle: An object that represents an idle timeout. An idle timeout bounds the amount of time that a connection may be idle. The default value is none.
            :param per_request: An object that represents a per request timeout. The default value is 15 seconds. If you set a higher timeout, then make sure that the higher value is set for each App Mesh resource in a conversation. For example, if a virtual node backend uses a virtual router provider to route to another virtual node, then the timeout should be greater than 15 seconds for the source and destination virtual node and the route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-grpctimeout.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                grpc_timeout_property = appmesh_mixins.CfnVirtualNodePropsMixin.GrpcTimeoutProperty(
                    idle=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                        unit="unit",
                        value=123
                    ),
                    per_request=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                        unit="unit",
                        value=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e9edd7a465c0661af9f30f3b658c9a929c9af8649a65d26cca281430e137cb70)
                check_type(argname="argument idle", value=idle, expected_type=type_hints["idle"])
                check_type(argname="argument per_request", value=per_request, expected_type=type_hints["per_request"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if idle is not None:
                self._values["idle"] = idle
            if per_request is not None:
                self._values["per_request"] = per_request

        @builtins.property
        def idle(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.DurationProperty"]]:
            '''An object that represents an idle timeout.

            An idle timeout bounds the amount of time that a connection may be idle. The default value is none.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-grpctimeout.html#cfn-appmesh-virtualnode-grpctimeout-idle
            '''
            result = self._values.get("idle")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.DurationProperty"]], result)

        @builtins.property
        def per_request(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.DurationProperty"]]:
            '''An object that represents a per request timeout.

            The default value is 15 seconds. If you set a higher timeout, then make sure that the higher value is set for each App Mesh resource in a conversation. For example, if a virtual node backend uses a virtual router provider to route to another virtual node, then the timeout should be greater than 15 seconds for the source and destination virtual node and the route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-grpctimeout.html#cfn-appmesh-virtualnode-grpctimeout-perrequest
            '''
            result = self._values.get("per_request")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.DurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrpcTimeoutProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.HealthCheckProperty",
        jsii_struct_bases=[],
        name_mapping={
            "healthy_threshold": "healthyThreshold",
            "interval_millis": "intervalMillis",
            "path": "path",
            "port": "port",
            "protocol": "protocol",
            "timeout_millis": "timeoutMillis",
            "unhealthy_threshold": "unhealthyThreshold",
        },
    )
    class HealthCheckProperty:
        def __init__(
            self,
            *,
            healthy_threshold: typing.Optional[jsii.Number] = None,
            interval_millis: typing.Optional[jsii.Number] = None,
            path: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            protocol: typing.Optional[builtins.str] = None,
            timeout_millis: typing.Optional[jsii.Number] = None,
            unhealthy_threshold: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An object that represents the health check policy for a virtual node's listener.

            :param healthy_threshold: The number of consecutive successful health checks that must occur before declaring listener healthy.
            :param interval_millis: The time period in milliseconds between each health check execution.
            :param path: The destination path for the health check request. This value is only used if the specified protocol is HTTP or HTTP/2. For any other protocol, this value is ignored.
            :param port: The destination port for the health check request. This port must match the port defined in the ``PortMapping`` for the listener.
            :param protocol: The protocol for the health check request. If you specify ``grpc`` , then your service must conform to the `GRPC Health Checking Protocol <https://docs.aws.amazon.com/https://github.com/grpc/grpc/blob/master/doc/health-checking.md>`_ .
            :param timeout_millis: The amount of time to wait when receiving a response from the health check, in milliseconds.
            :param unhealthy_threshold: The number of consecutive failed health checks that must occur before declaring a virtual node unhealthy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                health_check_property = appmesh_mixins.CfnVirtualNodePropsMixin.HealthCheckProperty(
                    healthy_threshold=123,
                    interval_millis=123,
                    path="path",
                    port=123,
                    protocol="protocol",
                    timeout_millis=123,
                    unhealthy_threshold=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c2b7c53f4477c10813973da806c68f381d7faa49b8e8237a98a39f0224d3b3bb)
                check_type(argname="argument healthy_threshold", value=healthy_threshold, expected_type=type_hints["healthy_threshold"])
                check_type(argname="argument interval_millis", value=interval_millis, expected_type=type_hints["interval_millis"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument timeout_millis", value=timeout_millis, expected_type=type_hints["timeout_millis"])
                check_type(argname="argument unhealthy_threshold", value=unhealthy_threshold, expected_type=type_hints["unhealthy_threshold"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if healthy_threshold is not None:
                self._values["healthy_threshold"] = healthy_threshold
            if interval_millis is not None:
                self._values["interval_millis"] = interval_millis
            if path is not None:
                self._values["path"] = path
            if port is not None:
                self._values["port"] = port
            if protocol is not None:
                self._values["protocol"] = protocol
            if timeout_millis is not None:
                self._values["timeout_millis"] = timeout_millis
            if unhealthy_threshold is not None:
                self._values["unhealthy_threshold"] = unhealthy_threshold

        @builtins.property
        def healthy_threshold(self) -> typing.Optional[jsii.Number]:
            '''The number of consecutive successful health checks that must occur before declaring listener healthy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-healthythreshold
            '''
            result = self._values.get("healthy_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval_millis(self) -> typing.Optional[jsii.Number]:
            '''The time period in milliseconds between each health check execution.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-intervalmillis
            '''
            result = self._values.get("interval_millis")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The destination path for the health check request.

            This value is only used if the specified protocol is HTTP or HTTP/2. For any other protocol, this value is ignored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The destination port for the health check request.

            This port must match the port defined in the ``PortMapping`` for the listener.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The protocol for the health check request.

            If you specify ``grpc`` , then your service must conform to the `GRPC Health Checking Protocol <https://docs.aws.amazon.com/https://github.com/grpc/grpc/blob/master/doc/health-checking.md>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timeout_millis(self) -> typing.Optional[jsii.Number]:
            '''The amount of time to wait when receiving a response from the health check, in milliseconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-timeoutmillis
            '''
            result = self._values.get("timeout_millis")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unhealthy_threshold(self) -> typing.Optional[jsii.Number]:
            '''The number of consecutive failed health checks that must occur before declaring a virtual node unhealthy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-unhealthythreshold
            '''
            result = self._values.get("unhealthy_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HealthCheckProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.HttpTimeoutProperty",
        jsii_struct_bases=[],
        name_mapping={"idle": "idle", "per_request": "perRequest"},
    )
    class HttpTimeoutProperty:
        def __init__(
            self,
            *,
            idle: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.DurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            per_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.DurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents types of timeouts.

            :param idle: An object that represents an idle timeout. An idle timeout bounds the amount of time that a connection may be idle. The default value is none.
            :param per_request: An object that represents a per request timeout. The default value is 15 seconds. If you set a higher timeout, then make sure that the higher value is set for each App Mesh resource in a conversation. For example, if a virtual node backend uses a virtual router provider to route to another virtual node, then the timeout should be greater than 15 seconds for the source and destination virtual node and the route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-httptimeout.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                http_timeout_property = appmesh_mixins.CfnVirtualNodePropsMixin.HttpTimeoutProperty(
                    idle=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                        unit="unit",
                        value=123
                    ),
                    per_request=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                        unit="unit",
                        value=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a348b72c89b283b5562e2526128023dcdc2005b6c22e414229d4a8400c21d5bb)
                check_type(argname="argument idle", value=idle, expected_type=type_hints["idle"])
                check_type(argname="argument per_request", value=per_request, expected_type=type_hints["per_request"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if idle is not None:
                self._values["idle"] = idle
            if per_request is not None:
                self._values["per_request"] = per_request

        @builtins.property
        def idle(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.DurationProperty"]]:
            '''An object that represents an idle timeout.

            An idle timeout bounds the amount of time that a connection may be idle. The default value is none.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-httptimeout.html#cfn-appmesh-virtualnode-httptimeout-idle
            '''
            result = self._values.get("idle")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.DurationProperty"]], result)

        @builtins.property
        def per_request(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.DurationProperty"]]:
            '''An object that represents a per request timeout.

            The default value is 15 seconds. If you set a higher timeout, then make sure that the higher value is set for each App Mesh resource in a conversation. For example, if a virtual node backend uses a virtual router provider to route to another virtual node, then the timeout should be greater than 15 seconds for the source and destination virtual node and the route.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-httptimeout.html#cfn-appmesh-virtualnode-httptimeout-perrequest
            '''
            result = self._values.get("per_request")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.DurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpTimeoutProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.JsonFormatRefProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class JsonFormatRefProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the key value pairs for the JSON.

            :param key: The specified key for the JSON.
            :param value: The specified value for the JSON.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-jsonformatref.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                json_format_ref_property = appmesh_mixins.CfnVirtualNodePropsMixin.JsonFormatRefProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e19f4234049604dc90ee0187fd04d5563d9dcf21ef61d2d49efba465332e8f7f)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The specified key for the JSON.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-jsonformatref.html#cfn-appmesh-virtualnode-jsonformatref-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The specified value for the JSON.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-jsonformatref.html#cfn-appmesh-virtualnode-jsonformatref-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JsonFormatRefProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.ListenerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connection_pool": "connectionPool",
            "health_check": "healthCheck",
            "outlier_detection": "outlierDetection",
            "port_mapping": "portMapping",
            "timeout": "timeout",
            "tls": "tls",
        },
    )
    class ListenerProperty:
        def __init__(
            self,
            *,
            connection_pool: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.VirtualNodeConnectionPoolProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            health_check: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.HealthCheckProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            outlier_detection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.OutlierDetectionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            port_mapping: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.PortMappingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            timeout: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.ListenerTimeoutProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            tls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.ListenerTlsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents a listener for a virtual node.

            :param connection_pool: The connection pool information for the listener.
            :param health_check: The health check information for the listener.
            :param outlier_detection: The outlier detection information for the listener.
            :param port_mapping: The port mapping information for the listener.
            :param timeout: An object that represents timeouts for different protocols.
            :param tls: A reference to an object that represents the Transport Layer Security (TLS) properties for a listener.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listener.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                listener_property = appmesh_mixins.CfnVirtualNodePropsMixin.ListenerProperty(
                    connection_pool=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeConnectionPoolProperty(
                        grpc=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeGrpcConnectionPoolProperty(
                            max_requests=123
                        ),
                        http=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeHttpConnectionPoolProperty(
                            max_connections=123,
                            max_pending_requests=123
                        ),
                        http2=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeHttp2ConnectionPoolProperty(
                            max_requests=123
                        ),
                        tcp=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeTcpConnectionPoolProperty(
                            max_connections=123
                        )
                    ),
                    health_check=appmesh_mixins.CfnVirtualNodePropsMixin.HealthCheckProperty(
                        healthy_threshold=123,
                        interval_millis=123,
                        path="path",
                        port=123,
                        protocol="protocol",
                        timeout_millis=123,
                        unhealthy_threshold=123
                    ),
                    outlier_detection=appmesh_mixins.CfnVirtualNodePropsMixin.OutlierDetectionProperty(
                        base_ejection_duration=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        ),
                        interval=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        ),
                        max_ejection_percent=123,
                        max_server_errors=123
                    ),
                    port_mapping=appmesh_mixins.CfnVirtualNodePropsMixin.PortMappingProperty(
                        port=123,
                        protocol="protocol"
                    ),
                    timeout=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTimeoutProperty(
                        grpc=appmesh_mixins.CfnVirtualNodePropsMixin.GrpcTimeoutProperty(
                            idle=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            ),
                            per_request=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            )
                        ),
                        http=appmesh_mixins.CfnVirtualNodePropsMixin.HttpTimeoutProperty(
                            idle=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            ),
                            per_request=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            )
                        ),
                        http2=appmesh_mixins.CfnVirtualNodePropsMixin.HttpTimeoutProperty(
                            idle=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            ),
                            per_request=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            )
                        ),
                        tcp=appmesh_mixins.CfnVirtualNodePropsMixin.TcpTimeoutProperty(
                            idle=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            )
                        )
                    ),
                    tls=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsProperty(
                        certificate=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsCertificateProperty(
                            acm=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsAcmCertificateProperty(
                                certificate_arn="certificateArn"
                            ),
                            file=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty(
                                certificate_chain="certificateChain",
                                private_key="privateKey"
                            ),
                            sds=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty(
                                secret_name="secretName"
                            )
                        ),
                        mode="mode",
                        validation=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsValidationContextProperty(
                            subject_alternative_names=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty(
                                match=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty(
                                    exact=["exact"]
                                )
                            ),
                            trust=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsValidationContextTrustProperty(
                                file=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty(
                                    certificate_chain="certificateChain"
                                ),
                                sds=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty(
                                    secret_name="secretName"
                                )
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b5eebb7cea0b369f30552306a60d6e93f7e3fb93a6902ea5a36f7cc28634be3f)
                check_type(argname="argument connection_pool", value=connection_pool, expected_type=type_hints["connection_pool"])
                check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
                check_type(argname="argument outlier_detection", value=outlier_detection, expected_type=type_hints["outlier_detection"])
                check_type(argname="argument port_mapping", value=port_mapping, expected_type=type_hints["port_mapping"])
                check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
                check_type(argname="argument tls", value=tls, expected_type=type_hints["tls"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connection_pool is not None:
                self._values["connection_pool"] = connection_pool
            if health_check is not None:
                self._values["health_check"] = health_check
            if outlier_detection is not None:
                self._values["outlier_detection"] = outlier_detection
            if port_mapping is not None:
                self._values["port_mapping"] = port_mapping
            if timeout is not None:
                self._values["timeout"] = timeout
            if tls is not None:
                self._values["tls"] = tls

        @builtins.property
        def connection_pool(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.VirtualNodeConnectionPoolProperty"]]:
            '''The connection pool information for the listener.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listener.html#cfn-appmesh-virtualnode-listener-connectionpool
            '''
            result = self._values.get("connection_pool")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.VirtualNodeConnectionPoolProperty"]], result)

        @builtins.property
        def health_check(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.HealthCheckProperty"]]:
            '''The health check information for the listener.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listener.html#cfn-appmesh-virtualnode-listener-healthcheck
            '''
            result = self._values.get("health_check")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.HealthCheckProperty"]], result)

        @builtins.property
        def outlier_detection(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.OutlierDetectionProperty"]]:
            '''The outlier detection information for the listener.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listener.html#cfn-appmesh-virtualnode-listener-outlierdetection
            '''
            result = self._values.get("outlier_detection")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.OutlierDetectionProperty"]], result)

        @builtins.property
        def port_mapping(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.PortMappingProperty"]]:
            '''The port mapping information for the listener.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listener.html#cfn-appmesh-virtualnode-listener-portmapping
            '''
            result = self._values.get("port_mapping")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.PortMappingProperty"]], result)

        @builtins.property
        def timeout(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ListenerTimeoutProperty"]]:
            '''An object that represents timeouts for different protocols.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listener.html#cfn-appmesh-virtualnode-listener-timeout
            '''
            result = self._values.get("timeout")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ListenerTimeoutProperty"]], result)

        @builtins.property
        def tls(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ListenerTlsProperty"]]:
            '''A reference to an object that represents the Transport Layer Security (TLS) properties for a listener.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listener.html#cfn-appmesh-virtualnode-listener-tls
            '''
            result = self._values.get("tls")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ListenerTlsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ListenerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.ListenerTimeoutProperty",
        jsii_struct_bases=[],
        name_mapping={"grpc": "grpc", "http": "http", "http2": "http2", "tcp": "tcp"},
    )
    class ListenerTimeoutProperty:
        def __init__(
            self,
            *,
            grpc: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.GrpcTimeoutProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            http: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.HttpTimeoutProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            http2: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.HttpTimeoutProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            tcp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.TcpTimeoutProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents timeouts for different protocols.

            :param grpc: An object that represents types of timeouts.
            :param http: An object that represents types of timeouts.
            :param http2: An object that represents types of timeouts.
            :param tcp: An object that represents types of timeouts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertimeout.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                listener_timeout_property = appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTimeoutProperty(
                    grpc=appmesh_mixins.CfnVirtualNodePropsMixin.GrpcTimeoutProperty(
                        idle=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        ),
                        per_request=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        )
                    ),
                    http=appmesh_mixins.CfnVirtualNodePropsMixin.HttpTimeoutProperty(
                        idle=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        ),
                        per_request=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        )
                    ),
                    http2=appmesh_mixins.CfnVirtualNodePropsMixin.HttpTimeoutProperty(
                        idle=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        ),
                        per_request=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        )
                    ),
                    tcp=appmesh_mixins.CfnVirtualNodePropsMixin.TcpTimeoutProperty(
                        idle=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                            unit="unit",
                            value=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fdd5e829e00c02bb52a3441a2aaa71ab53d0babc4cb7212b0109e9da9b875996)
                check_type(argname="argument grpc", value=grpc, expected_type=type_hints["grpc"])
                check_type(argname="argument http", value=http, expected_type=type_hints["http"])
                check_type(argname="argument http2", value=http2, expected_type=type_hints["http2"])
                check_type(argname="argument tcp", value=tcp, expected_type=type_hints["tcp"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if grpc is not None:
                self._values["grpc"] = grpc
            if http is not None:
                self._values["http"] = http
            if http2 is not None:
                self._values["http2"] = http2
            if tcp is not None:
                self._values["tcp"] = tcp

        @builtins.property
        def grpc(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.GrpcTimeoutProperty"]]:
            '''An object that represents types of timeouts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertimeout.html#cfn-appmesh-virtualnode-listenertimeout-grpc
            '''
            result = self._values.get("grpc")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.GrpcTimeoutProperty"]], result)

        @builtins.property
        def http(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.HttpTimeoutProperty"]]:
            '''An object that represents types of timeouts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertimeout.html#cfn-appmesh-virtualnode-listenertimeout-http
            '''
            result = self._values.get("http")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.HttpTimeoutProperty"]], result)

        @builtins.property
        def http2(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.HttpTimeoutProperty"]]:
            '''An object that represents types of timeouts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertimeout.html#cfn-appmesh-virtualnode-listenertimeout-http2
            '''
            result = self._values.get("http2")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.HttpTimeoutProperty"]], result)

        @builtins.property
        def tcp(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.TcpTimeoutProperty"]]:
            '''An object that represents types of timeouts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertimeout.html#cfn-appmesh-virtualnode-listenertimeout-tcp
            '''
            result = self._values.get("tcp")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.TcpTimeoutProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ListenerTimeoutProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.ListenerTlsAcmCertificateProperty",
        jsii_struct_bases=[],
        name_mapping={"certificate_arn": "certificateArn"},
    )
    class ListenerTlsAcmCertificateProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents an Certificate Manager certificate.

            :param certificate_arn: The Amazon Resource Name (ARN) for the certificate. The certificate must meet specific requirements and you must have proxy authorization enabled. For more information, see `Transport Layer Security (TLS) <https://docs.aws.amazon.com/app-mesh/latest/userguide/tls.html#virtual-node-tls-prerequisites>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsacmcertificate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                listener_tls_acm_certificate_property = appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsAcmCertificateProperty(
                    certificate_arn="certificateArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__16dedb89d53efb87fb4701ae94bdaf782f719aa6df13ac7e6f261d01004b4c64)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the certificate.

            The certificate must meet specific requirements and you must have proxy authorization enabled. For more information, see `Transport Layer Security (TLS) <https://docs.aws.amazon.com/app-mesh/latest/userguide/tls.html#virtual-node-tls-prerequisites>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsacmcertificate.html#cfn-appmesh-virtualnode-listenertlsacmcertificate-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ListenerTlsAcmCertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.ListenerTlsCertificateProperty",
        jsii_struct_bases=[],
        name_mapping={"acm": "acm", "file": "file", "sds": "sds"},
    )
    class ListenerTlsCertificateProperty:
        def __init__(
            self,
            *,
            acm: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.ListenerTlsAcmCertificateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            file: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sds: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents a listener's Transport Layer Security (TLS) certificate.

            :param acm: A reference to an object that represents an Certificate Manager certificate.
            :param file: A reference to an object that represents a local file certificate.
            :param sds: A reference to an object that represents a listener's Secret Discovery Service certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlscertificate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                listener_tls_certificate_property = appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsCertificateProperty(
                    acm=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsAcmCertificateProperty(
                        certificate_arn="certificateArn"
                    ),
                    file=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty(
                        certificate_chain="certificateChain",
                        private_key="privateKey"
                    ),
                    sds=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty(
                        secret_name="secretName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__755b6167a2cb65cc0bd0ce2d0c36cda44ccc9514325b1e960254540f6aaccae4)
                check_type(argname="argument acm", value=acm, expected_type=type_hints["acm"])
                check_type(argname="argument file", value=file, expected_type=type_hints["file"])
                check_type(argname="argument sds", value=sds, expected_type=type_hints["sds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if acm is not None:
                self._values["acm"] = acm
            if file is not None:
                self._values["file"] = file
            if sds is not None:
                self._values["sds"] = sds

        @builtins.property
        def acm(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ListenerTlsAcmCertificateProperty"]]:
            '''A reference to an object that represents an Certificate Manager certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlscertificate.html#cfn-appmesh-virtualnode-listenertlscertificate-acm
            '''
            result = self._values.get("acm")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ListenerTlsAcmCertificateProperty"]], result)

        @builtins.property
        def file(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty"]]:
            '''A reference to an object that represents a local file certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlscertificate.html#cfn-appmesh-virtualnode-listenertlscertificate-file
            '''
            result = self._values.get("file")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty"]], result)

        @builtins.property
        def sds(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty"]]:
            '''A reference to an object that represents a listener's Secret Discovery Service certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlscertificate.html#cfn-appmesh-virtualnode-listenertlscertificate-sds
            '''
            result = self._values.get("sds")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ListenerTlsCertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_chain": "certificateChain",
            "private_key": "privateKey",
        },
    )
    class ListenerTlsFileCertificateProperty:
        def __init__(
            self,
            *,
            certificate_chain: typing.Optional[builtins.str] = None,
            private_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents a local file certificate.

            The certificate must meet specific requirements and you must have proxy authorization enabled. For more information, see `Transport Layer Security (TLS) <https://docs.aws.amazon.com/app-mesh/latest/userguide/tls.html#virtual-node-tls-prerequisites>`_ .

            :param certificate_chain: The certificate chain for the certificate.
            :param private_key: The private key for a certificate stored on the file system of the virtual node that the proxy is running on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsfilecertificate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                listener_tls_file_certificate_property = appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty(
                    certificate_chain="certificateChain",
                    private_key="privateKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0fda26973849660276dc0aadaaaa5982ce92bfce0b61d4e5338d92850d4e09c6)
                check_type(argname="argument certificate_chain", value=certificate_chain, expected_type=type_hints["certificate_chain"])
                check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_chain is not None:
                self._values["certificate_chain"] = certificate_chain
            if private_key is not None:
                self._values["private_key"] = private_key

        @builtins.property
        def certificate_chain(self) -> typing.Optional[builtins.str]:
            '''The certificate chain for the certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsfilecertificate.html#cfn-appmesh-virtualnode-listenertlsfilecertificate-certificatechain
            '''
            result = self._values.get("certificate_chain")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def private_key(self) -> typing.Optional[builtins.str]:
            '''The private key for a certificate stored on the file system of the virtual node that the proxy is running on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsfilecertificate.html#cfn-appmesh-virtualnode-listenertlsfilecertificate-privatekey
            '''
            result = self._values.get("private_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ListenerTlsFileCertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.ListenerTlsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate": "certificate",
            "mode": "mode",
            "validation": "validation",
        },
    )
    class ListenerTlsProperty:
        def __init__(
            self,
            *,
            certificate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.ListenerTlsCertificateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            mode: typing.Optional[builtins.str] = None,
            validation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.ListenerTlsValidationContextProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents the Transport Layer Security (TLS) properties for a listener.

            :param certificate: A reference to an object that represents a listener's Transport Layer Security (TLS) certificate.
            :param mode: Specify one of the following modes. - ** STRICT – Listener only accepts connections with TLS enabled. - ** PERMISSIVE – Listener accepts connections with or without TLS enabled. - ** DISABLED – Listener only accepts connections without TLS.
            :param validation: A reference to an object that represents a listener's Transport Layer Security (TLS) validation context.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertls.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                listener_tls_property = appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsProperty(
                    certificate=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsCertificateProperty(
                        acm=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsAcmCertificateProperty(
                            certificate_arn="certificateArn"
                        ),
                        file=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty(
                            certificate_chain="certificateChain",
                            private_key="privateKey"
                        ),
                        sds=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty(
                            secret_name="secretName"
                        )
                    ),
                    mode="mode",
                    validation=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsValidationContextProperty(
                        subject_alternative_names=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty(
                            match=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty(
                                exact=["exact"]
                            )
                        ),
                        trust=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsValidationContextTrustProperty(
                            file=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty(
                                certificate_chain="certificateChain"
                            ),
                            sds=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty(
                                secret_name="secretName"
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cf3a164dadee2d1eba6ae7831e2dad8048ebea0285735b0cea1859a03c531a53)
                check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
                check_type(argname="argument validation", value=validation, expected_type=type_hints["validation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate is not None:
                self._values["certificate"] = certificate
            if mode is not None:
                self._values["mode"] = mode
            if validation is not None:
                self._values["validation"] = validation

        @builtins.property
        def certificate(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ListenerTlsCertificateProperty"]]:
            '''A reference to an object that represents a listener's Transport Layer Security (TLS) certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertls.html#cfn-appmesh-virtualnode-listenertls-certificate
            '''
            result = self._values.get("certificate")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ListenerTlsCertificateProperty"]], result)

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''Specify one of the following modes.

            - ** STRICT – Listener only accepts connections with TLS enabled.
            - ** PERMISSIVE – Listener accepts connections with or without TLS enabled.
            - ** DISABLED – Listener only accepts connections without TLS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertls.html#cfn-appmesh-virtualnode-listenertls-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def validation(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ListenerTlsValidationContextProperty"]]:
            '''A reference to an object that represents a listener's Transport Layer Security (TLS) validation context.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertls.html#cfn-appmesh-virtualnode-listenertls-validation
            '''
            result = self._values.get("validation")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ListenerTlsValidationContextProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ListenerTlsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty",
        jsii_struct_bases=[],
        name_mapping={"secret_name": "secretName"},
    )
    class ListenerTlsSdsCertificateProperty:
        def __init__(
            self,
            *,
            secret_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the listener's Secret Discovery Service certificate.

            The proxy must be configured with a local SDS provider via a Unix Domain Socket. See App Mesh `TLS documentation <https://docs.aws.amazon.com/app-mesh/latest/userguide/tls.html>`_ for more info.

            :param secret_name: A reference to an object that represents the name of the secret requested from the Secret Discovery Service provider representing Transport Layer Security (TLS) materials like a certificate or certificate chain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlssdscertificate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                listener_tls_sds_certificate_property = appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty(
                    secret_name="secretName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1f2cfd36495c99b1fb07b2270c98842140d71294550352e5cc2cbbb37d57e367)
                check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if secret_name is not None:
                self._values["secret_name"] = secret_name

        @builtins.property
        def secret_name(self) -> typing.Optional[builtins.str]:
            '''A reference to an object that represents the name of the secret requested from the Secret Discovery Service provider representing Transport Layer Security (TLS) materials like a certificate or certificate chain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlssdscertificate.html#cfn-appmesh-virtualnode-listenertlssdscertificate-secretname
            '''
            result = self._values.get("secret_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ListenerTlsSdsCertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.ListenerTlsValidationContextProperty",
        jsii_struct_bases=[],
        name_mapping={
            "subject_alternative_names": "subjectAlternativeNames",
            "trust": "trust",
        },
    )
    class ListenerTlsValidationContextProperty:
        def __init__(
            self,
            *,
            subject_alternative_names: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            trust: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.ListenerTlsValidationContextTrustProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents a listener's Transport Layer Security (TLS) validation context.

            :param subject_alternative_names: A reference to an object that represents the SANs for a listener's Transport Layer Security (TLS) validation context.
            :param trust: A reference to where to retrieve the trust chain when validating a peer’s Transport Layer Security (TLS) certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsvalidationcontext.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                listener_tls_validation_context_property = appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsValidationContextProperty(
                    subject_alternative_names=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty(
                        match=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty(
                            exact=["exact"]
                        )
                    ),
                    trust=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsValidationContextTrustProperty(
                        file=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty(
                            certificate_chain="certificateChain"
                        ),
                        sds=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty(
                            secret_name="secretName"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__058125a2840f6d0acf72bea68b127ce7af01e5f856ccdfd0aa9eef0ea9d94f54)
                check_type(argname="argument subject_alternative_names", value=subject_alternative_names, expected_type=type_hints["subject_alternative_names"])
                check_type(argname="argument trust", value=trust, expected_type=type_hints["trust"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if subject_alternative_names is not None:
                self._values["subject_alternative_names"] = subject_alternative_names
            if trust is not None:
                self._values["trust"] = trust

        @builtins.property
        def subject_alternative_names(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty"]]:
            '''A reference to an object that represents the SANs for a listener's Transport Layer Security (TLS) validation context.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsvalidationcontext.html#cfn-appmesh-virtualnode-listenertlsvalidationcontext-subjectalternativenames
            '''
            result = self._values.get("subject_alternative_names")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty"]], result)

        @builtins.property
        def trust(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ListenerTlsValidationContextTrustProperty"]]:
            '''A reference to where to retrieve the trust chain when validating a peer’s Transport Layer Security (TLS) certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsvalidationcontext.html#cfn-appmesh-virtualnode-listenertlsvalidationcontext-trust
            '''
            result = self._values.get("trust")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ListenerTlsValidationContextTrustProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ListenerTlsValidationContextProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.ListenerTlsValidationContextTrustProperty",
        jsii_struct_bases=[],
        name_mapping={"file": "file", "sds": "sds"},
    )
    class ListenerTlsValidationContextTrustProperty:
        def __init__(
            self,
            *,
            file: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sds: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents a listener's Transport Layer Security (TLS) validation context trust.

            :param file: An object that represents a Transport Layer Security (TLS) validation context trust for a local file.
            :param sds: A reference to an object that represents a listener's Transport Layer Security (TLS) Secret Discovery Service validation context trust.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsvalidationcontexttrust.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                listener_tls_validation_context_trust_property = appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsValidationContextTrustProperty(
                    file=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty(
                        certificate_chain="certificateChain"
                    ),
                    sds=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty(
                        secret_name="secretName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8136c731899ae5471467d6795fcf20ac1bddf72d8a4fa47b6082cd01dafa9de8)
                check_type(argname="argument file", value=file, expected_type=type_hints["file"])
                check_type(argname="argument sds", value=sds, expected_type=type_hints["sds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if file is not None:
                self._values["file"] = file
            if sds is not None:
                self._values["sds"] = sds

        @builtins.property
        def file(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty"]]:
            '''An object that represents a Transport Layer Security (TLS) validation context trust for a local file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsvalidationcontexttrust.html#cfn-appmesh-virtualnode-listenertlsvalidationcontexttrust-file
            '''
            result = self._values.get("file")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty"]], result)

        @builtins.property
        def sds(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty"]]:
            '''A reference to an object that represents a listener's Transport Layer Security (TLS) Secret Discovery Service validation context trust.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsvalidationcontexttrust.html#cfn-appmesh-virtualnode-listenertlsvalidationcontexttrust-sds
            '''
            result = self._values.get("sds")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ListenerTlsValidationContextTrustProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.LoggingFormatProperty",
        jsii_struct_bases=[],
        name_mapping={"json": "json", "text": "text"},
    )
    class LoggingFormatProperty:
        def __init__(
            self,
            *,
            json: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.JsonFormatRefProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            text: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the format for the logs.

            :param json: The logging format for JSON.
            :param text: The logging format for text.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-loggingformat.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                logging_format_property = appmesh_mixins.CfnVirtualNodePropsMixin.LoggingFormatProperty(
                    json=[appmesh_mixins.CfnVirtualNodePropsMixin.JsonFormatRefProperty(
                        key="key",
                        value="value"
                    )],
                    text="text"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cbcbac3b62e7bd0ec19485dfc978b42db0759833ae1e29676a04aeee88f4a833)
                check_type(argname="argument json", value=json, expected_type=type_hints["json"])
                check_type(argname="argument text", value=text, expected_type=type_hints["text"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if json is not None:
                self._values["json"] = json
            if text is not None:
                self._values["text"] = text

        @builtins.property
        def json(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.JsonFormatRefProperty"]]]]:
            '''The logging format for JSON.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-loggingformat.html#cfn-appmesh-virtualnode-loggingformat-json
            '''
            result = self._values.get("json")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.JsonFormatRefProperty"]]]], result)

        @builtins.property
        def text(self) -> typing.Optional[builtins.str]:
            '''The logging format for text.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-loggingformat.html#cfn-appmesh-virtualnode-loggingformat-text
            '''
            result = self._values.get("text")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingFormatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.LoggingProperty",
        jsii_struct_bases=[],
        name_mapping={"access_log": "accessLog"},
    )
    class LoggingProperty:
        def __init__(
            self,
            *,
            access_log: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.AccessLogProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents the logging information for a virtual node.

            :param access_log: The access log configuration for a virtual node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-logging.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                logging_property = appmesh_mixins.CfnVirtualNodePropsMixin.LoggingProperty(
                    access_log=appmesh_mixins.CfnVirtualNodePropsMixin.AccessLogProperty(
                        file=appmesh_mixins.CfnVirtualNodePropsMixin.FileAccessLogProperty(
                            format=appmesh_mixins.CfnVirtualNodePropsMixin.LoggingFormatProperty(
                                json=[appmesh_mixins.CfnVirtualNodePropsMixin.JsonFormatRefProperty(
                                    key="key",
                                    value="value"
                                )],
                                text="text"
                            ),
                            path="path"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__053f6923147b7ac5940ee2002f80da49a54fa727fd3d352180584832a14e9248)
                check_type(argname="argument access_log", value=access_log, expected_type=type_hints["access_log"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_log is not None:
                self._values["access_log"] = access_log

        @builtins.property
        def access_log(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.AccessLogProperty"]]:
            '''The access log configuration for a virtual node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-logging.html#cfn-appmesh-virtualnode-logging-accesslog
            '''
            result = self._values.get("access_log")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.AccessLogProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.OutlierDetectionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "base_ejection_duration": "baseEjectionDuration",
            "interval": "interval",
            "max_ejection_percent": "maxEjectionPercent",
            "max_server_errors": "maxServerErrors",
        },
    )
    class OutlierDetectionProperty:
        def __init__(
            self,
            *,
            base_ejection_duration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.DurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            interval: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.DurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            max_ejection_percent: typing.Optional[jsii.Number] = None,
            max_server_errors: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An object that represents the outlier detection for a virtual node's listener.

            :param base_ejection_duration: The base amount of time for which a host is ejected.
            :param interval: The time interval between ejection sweep analysis.
            :param max_ejection_percent: Maximum percentage of hosts in load balancing pool for upstream service that can be ejected. Will eject at least one host regardless of the value.
            :param max_server_errors: Number of consecutive ``5xx`` errors required for ejection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-outlierdetection.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                outlier_detection_property = appmesh_mixins.CfnVirtualNodePropsMixin.OutlierDetectionProperty(
                    base_ejection_duration=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                        unit="unit",
                        value=123
                    ),
                    interval=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                        unit="unit",
                        value=123
                    ),
                    max_ejection_percent=123,
                    max_server_errors=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__46c9652d6bea9995dc14f8515c74142c745ef7759682a2622767951cd6abe8f9)
                check_type(argname="argument base_ejection_duration", value=base_ejection_duration, expected_type=type_hints["base_ejection_duration"])
                check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
                check_type(argname="argument max_ejection_percent", value=max_ejection_percent, expected_type=type_hints["max_ejection_percent"])
                check_type(argname="argument max_server_errors", value=max_server_errors, expected_type=type_hints["max_server_errors"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if base_ejection_duration is not None:
                self._values["base_ejection_duration"] = base_ejection_duration
            if interval is not None:
                self._values["interval"] = interval
            if max_ejection_percent is not None:
                self._values["max_ejection_percent"] = max_ejection_percent
            if max_server_errors is not None:
                self._values["max_server_errors"] = max_server_errors

        @builtins.property
        def base_ejection_duration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.DurationProperty"]]:
            '''The base amount of time for which a host is ejected.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-outlierdetection.html#cfn-appmesh-virtualnode-outlierdetection-baseejectionduration
            '''
            result = self._values.get("base_ejection_duration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.DurationProperty"]], result)

        @builtins.property
        def interval(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.DurationProperty"]]:
            '''The time interval between ejection sweep analysis.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-outlierdetection.html#cfn-appmesh-virtualnode-outlierdetection-interval
            '''
            result = self._values.get("interval")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.DurationProperty"]], result)

        @builtins.property
        def max_ejection_percent(self) -> typing.Optional[jsii.Number]:
            '''Maximum percentage of hosts in load balancing pool for upstream service that can be ejected.

            Will eject at least one host regardless of the value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-outlierdetection.html#cfn-appmesh-virtualnode-outlierdetection-maxejectionpercent
            '''
            result = self._values.get("max_ejection_percent")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_server_errors(self) -> typing.Optional[jsii.Number]:
            '''Number of consecutive ``5xx`` errors required for ejection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-outlierdetection.html#cfn-appmesh-virtualnode-outlierdetection-maxservererrors
            '''
            result = self._values.get("max_server_errors")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutlierDetectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.PortMappingProperty",
        jsii_struct_bases=[],
        name_mapping={"port": "port", "protocol": "protocol"},
    )
    class PortMappingProperty:
        def __init__(
            self,
            *,
            port: typing.Optional[jsii.Number] = None,
            protocol: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object representing a virtual node or virtual router listener port mapping.

            :param port: The port used for the port mapping.
            :param protocol: The protocol used for the port mapping. Specify ``http`` , ``http2`` , ``grpc`` , or ``tcp`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-portmapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                port_mapping_property = appmesh_mixins.CfnVirtualNodePropsMixin.PortMappingProperty(
                    port=123,
                    protocol="protocol"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6bd254efbcb44e81597b3fed0d0cd27e2b1f6a60d5d82776974e2c32cf62dac5)
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if port is not None:
                self._values["port"] = port
            if protocol is not None:
                self._values["protocol"] = protocol

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port used for the port mapping.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-portmapping.html#cfn-appmesh-virtualnode-portmapping-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The protocol used for the port mapping.

            Specify ``http`` , ``http2`` , ``grpc`` , or ``tcp`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-portmapping.html#cfn-appmesh-virtualnode-portmapping-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.ServiceDiscoveryProperty",
        jsii_struct_bases=[],
        name_mapping={"aws_cloud_map": "awsCloudMap", "dns": "dns"},
    )
    class ServiceDiscoveryProperty:
        def __init__(
            self,
            *,
            aws_cloud_map: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.AwsCloudMapServiceDiscoveryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.DnsServiceDiscoveryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents the service discovery information for a virtual node.

            :param aws_cloud_map: Specifies any AWS Cloud Map information for the virtual node.
            :param dns: Specifies the DNS information for the virtual node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-servicediscovery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                service_discovery_property = appmesh_mixins.CfnVirtualNodePropsMixin.ServiceDiscoveryProperty(
                    aws_cloud_map=appmesh_mixins.CfnVirtualNodePropsMixin.AwsCloudMapServiceDiscoveryProperty(
                        attributes=[appmesh_mixins.CfnVirtualNodePropsMixin.AwsCloudMapInstanceAttributeProperty(
                            key="key",
                            value="value"
                        )],
                        ip_preference="ipPreference",
                        namespace_name="namespaceName",
                        service_name="serviceName"
                    ),
                    dns=appmesh_mixins.CfnVirtualNodePropsMixin.DnsServiceDiscoveryProperty(
                        hostname="hostname",
                        ip_preference="ipPreference",
                        response_type="responseType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__71fcc04dd49f4f562593a47e0f52e28d7e66881b9485c1fb19f7bee674007db4)
                check_type(argname="argument aws_cloud_map", value=aws_cloud_map, expected_type=type_hints["aws_cloud_map"])
                check_type(argname="argument dns", value=dns, expected_type=type_hints["dns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_cloud_map is not None:
                self._values["aws_cloud_map"] = aws_cloud_map
            if dns is not None:
                self._values["dns"] = dns

        @builtins.property
        def aws_cloud_map(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.AwsCloudMapServiceDiscoveryProperty"]]:
            '''Specifies any AWS Cloud Map information for the virtual node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-servicediscovery.html#cfn-appmesh-virtualnode-servicediscovery-awscloudmap
            '''
            result = self._values.get("aws_cloud_map")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.AwsCloudMapServiceDiscoveryProperty"]], result)

        @builtins.property
        def dns(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.DnsServiceDiscoveryProperty"]]:
            '''Specifies the DNS information for the virtual node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-servicediscovery.html#cfn-appmesh-virtualnode-servicediscovery-dns
            '''
            result = self._values.get("dns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.DnsServiceDiscoveryProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceDiscoveryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty",
        jsii_struct_bases=[],
        name_mapping={"exact": "exact"},
    )
    class SubjectAlternativeNameMatchersProperty:
        def __init__(
            self,
            *,
            exact: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''An object that represents the methods by which a subject alternative name on a peer Transport Layer Security (TLS) certificate can be matched.

            :param exact: The values sent must match the specified values exactly.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-subjectalternativenamematchers.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                subject_alternative_name_matchers_property = appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty(
                    exact=["exact"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4cf9b2b5f9ecb63d0a75aa32c4951472166680b967e18959f752df248b86e02a)
                check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exact is not None:
                self._values["exact"] = exact

        @builtins.property
        def exact(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The values sent must match the specified values exactly.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-subjectalternativenamematchers.html#cfn-appmesh-virtualnode-subjectalternativenamematchers-exact
            '''
            result = self._values.get("exact")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubjectAlternativeNameMatchersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty",
        jsii_struct_bases=[],
        name_mapping={"match": "match"},
    )
    class SubjectAlternativeNamesProperty:
        def __init__(
            self,
            *,
            match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents the subject alternative names secured by the certificate.

            :param match: An object that represents the criteria for determining a SANs match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-subjectalternativenames.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                subject_alternative_names_property = appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty(
                    match=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty(
                        exact=["exact"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__da3d4e162c2cc095302e63a084ede8507ee71766b943115b6aed6af7b996befb)
                check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if match is not None:
                self._values["match"] = match

        @builtins.property
        def match(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty"]]:
            '''An object that represents the criteria for determining a SANs match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-subjectalternativenames.html#cfn-appmesh-virtualnode-subjectalternativenames-match
            '''
            result = self._values.get("match")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubjectAlternativeNamesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.TcpTimeoutProperty",
        jsii_struct_bases=[],
        name_mapping={"idle": "idle"},
    )
    class TcpTimeoutProperty:
        def __init__(
            self,
            *,
            idle: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.DurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents types of timeouts.

            :param idle: An object that represents an idle timeout. An idle timeout bounds the amount of time that a connection may be idle. The default value is none.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tcptimeout.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                tcp_timeout_property = appmesh_mixins.CfnVirtualNodePropsMixin.TcpTimeoutProperty(
                    idle=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                        unit="unit",
                        value=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__01b7668a232555df3a102177d7ef4a9cf64642a22785333d0367e6b995254024)
                check_type(argname="argument idle", value=idle, expected_type=type_hints["idle"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if idle is not None:
                self._values["idle"] = idle

        @builtins.property
        def idle(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.DurationProperty"]]:
            '''An object that represents an idle timeout.

            An idle timeout bounds the amount of time that a connection may be idle. The default value is none.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tcptimeout.html#cfn-appmesh-virtualnode-tcptimeout-idle
            '''
            result = self._values.get("idle")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.DurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TcpTimeoutProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.TlsValidationContextAcmTrustProperty",
        jsii_struct_bases=[],
        name_mapping={"certificate_authority_arns": "certificateAuthorityArns"},
    )
    class TlsValidationContextAcmTrustProperty:
        def __init__(
            self,
            *,
            certificate_authority_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''An object that represents a Transport Layer Security (TLS) validation context trust for an Certificate Manager certificate.

            :param certificate_authority_arns: One or more ACM Amazon Resource Name (ARN)s.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontextacmtrust.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                tls_validation_context_acm_trust_property = appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextAcmTrustProperty(
                    certificate_authority_arns=["certificateAuthorityArns"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a87c56e498da1743b8f7411a407f8bfe991a28ba00108cf0ef2f64dc5a573b62)
                check_type(argname="argument certificate_authority_arns", value=certificate_authority_arns, expected_type=type_hints["certificate_authority_arns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_authority_arns is not None:
                self._values["certificate_authority_arns"] = certificate_authority_arns

        @builtins.property
        def certificate_authority_arns(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''One or more ACM Amazon Resource Name (ARN)s.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontextacmtrust.html#cfn-appmesh-virtualnode-tlsvalidationcontextacmtrust-certificateauthorityarns
            '''
            result = self._values.get("certificate_authority_arns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TlsValidationContextAcmTrustProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty",
        jsii_struct_bases=[],
        name_mapping={"certificate_chain": "certificateChain"},
    )
    class TlsValidationContextFileTrustProperty:
        def __init__(
            self,
            *,
            certificate_chain: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents a Transport Layer Security (TLS) validation context trust for a local file.

            :param certificate_chain: The certificate trust chain for a certificate stored on the file system of the virtual node that the proxy is running on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontextfiletrust.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                tls_validation_context_file_trust_property = appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty(
                    certificate_chain="certificateChain"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2cc190d3207e1ddf14cce7d79dee1d5fe0139d04b0e9c1abda90f01205644391)
                check_type(argname="argument certificate_chain", value=certificate_chain, expected_type=type_hints["certificate_chain"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_chain is not None:
                self._values["certificate_chain"] = certificate_chain

        @builtins.property
        def certificate_chain(self) -> typing.Optional[builtins.str]:
            '''The certificate trust chain for a certificate stored on the file system of the virtual node that the proxy is running on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontextfiletrust.html#cfn-appmesh-virtualnode-tlsvalidationcontextfiletrust-certificatechain
            '''
            result = self._values.get("certificate_chain")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TlsValidationContextFileTrustProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.TlsValidationContextProperty",
        jsii_struct_bases=[],
        name_mapping={
            "subject_alternative_names": "subjectAlternativeNames",
            "trust": "trust",
        },
    )
    class TlsValidationContextProperty:
        def __init__(
            self,
            *,
            subject_alternative_names: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            trust: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.TlsValidationContextTrustProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents how the proxy will validate its peer during Transport Layer Security (TLS) negotiation.

            :param subject_alternative_names: A reference to an object that represents the SANs for a Transport Layer Security (TLS) validation context. If you don't specify SANs on the *terminating* mesh endpoint, the Envoy proxy for that node doesn't verify the SAN on a peer client certificate. If you don't specify SANs on the *originating* mesh endpoint, the SAN on the certificate provided by the terminating endpoint must match the mesh endpoint service discovery configuration. Since SPIRE vended certificates have a SPIFFE ID as a name, you must set the SAN since the name doesn't match the service discovery name.
            :param trust: A reference to where to retrieve the trust chain when validating a peer’s Transport Layer Security (TLS) certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontext.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                tls_validation_context_property = appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextProperty(
                    subject_alternative_names=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty(
                        match=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty(
                            exact=["exact"]
                        )
                    ),
                    trust=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextTrustProperty(
                        acm=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextAcmTrustProperty(
                            certificate_authority_arns=["certificateAuthorityArns"]
                        ),
                        file=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty(
                            certificate_chain="certificateChain"
                        ),
                        sds=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty(
                            secret_name="secretName"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6dda146df1f6a674fb88e311139562f73406d157a4be6cda2f61d735a75fe368)
                check_type(argname="argument subject_alternative_names", value=subject_alternative_names, expected_type=type_hints["subject_alternative_names"])
                check_type(argname="argument trust", value=trust, expected_type=type_hints["trust"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if subject_alternative_names is not None:
                self._values["subject_alternative_names"] = subject_alternative_names
            if trust is not None:
                self._values["trust"] = trust

        @builtins.property
        def subject_alternative_names(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty"]]:
            '''A reference to an object that represents the SANs for a Transport Layer Security (TLS) validation context.

            If you don't specify SANs on the *terminating* mesh endpoint, the Envoy proxy for that node doesn't verify the SAN on a peer client certificate. If you don't specify SANs on the *originating* mesh endpoint, the SAN on the certificate provided by the terminating endpoint must match the mesh endpoint service discovery configuration. Since SPIRE vended certificates have a SPIFFE ID as a name, you must set the SAN since the name doesn't match the service discovery name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontext.html#cfn-appmesh-virtualnode-tlsvalidationcontext-subjectalternativenames
            '''
            result = self._values.get("subject_alternative_names")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty"]], result)

        @builtins.property
        def trust(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.TlsValidationContextTrustProperty"]]:
            '''A reference to where to retrieve the trust chain when validating a peer’s Transport Layer Security (TLS) certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontext.html#cfn-appmesh-virtualnode-tlsvalidationcontext-trust
            '''
            result = self._values.get("trust")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.TlsValidationContextTrustProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TlsValidationContextProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty",
        jsii_struct_bases=[],
        name_mapping={"secret_name": "secretName"},
    )
    class TlsValidationContextSdsTrustProperty:
        def __init__(
            self,
            *,
            secret_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents a Transport Layer Security (TLS) Secret Discovery Service validation context trust.

            The proxy must be configured with a local SDS provider via a Unix Domain Socket. See App Mesh `TLS documentation <https://docs.aws.amazon.com/app-mesh/latest/userguide/tls.html>`_ for more info.

            :param secret_name: A reference to an object that represents the name of the secret for a Transport Layer Security (TLS) Secret Discovery Service validation context trust.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontextsdstrust.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                tls_validation_context_sds_trust_property = appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty(
                    secret_name="secretName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b5d7f14b8780365dccb3cdc22f98b01eab453efb85c8c409d535b70946342b47)
                check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if secret_name is not None:
                self._values["secret_name"] = secret_name

        @builtins.property
        def secret_name(self) -> typing.Optional[builtins.str]:
            '''A reference to an object that represents the name of the secret for a Transport Layer Security (TLS) Secret Discovery Service validation context trust.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontextsdstrust.html#cfn-appmesh-virtualnode-tlsvalidationcontextsdstrust-secretname
            '''
            result = self._values.get("secret_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TlsValidationContextSdsTrustProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.TlsValidationContextTrustProperty",
        jsii_struct_bases=[],
        name_mapping={"acm": "acm", "file": "file", "sds": "sds"},
    )
    class TlsValidationContextTrustProperty:
        def __init__(
            self,
            *,
            acm: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.TlsValidationContextAcmTrustProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            file: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sds: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents a Transport Layer Security (TLS) validation context trust.

            :param acm: A reference to an object that represents a Transport Layer Security (TLS) validation context trust for an Certificate Manager certificate.
            :param file: An object that represents a Transport Layer Security (TLS) validation context trust for a local file.
            :param sds: A reference to an object that represents a Transport Layer Security (TLS) Secret Discovery Service validation context trust.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontexttrust.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                tls_validation_context_trust_property = appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextTrustProperty(
                    acm=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextAcmTrustProperty(
                        certificate_authority_arns=["certificateAuthorityArns"]
                    ),
                    file=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty(
                        certificate_chain="certificateChain"
                    ),
                    sds=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty(
                        secret_name="secretName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__07d5078ef0e58fbee3b4f98e3458e38c4e7b48b36c61fb176960d69222969525)
                check_type(argname="argument acm", value=acm, expected_type=type_hints["acm"])
                check_type(argname="argument file", value=file, expected_type=type_hints["file"])
                check_type(argname="argument sds", value=sds, expected_type=type_hints["sds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if acm is not None:
                self._values["acm"] = acm
            if file is not None:
                self._values["file"] = file
            if sds is not None:
                self._values["sds"] = sds

        @builtins.property
        def acm(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.TlsValidationContextAcmTrustProperty"]]:
            '''A reference to an object that represents a Transport Layer Security (TLS) validation context trust for an Certificate Manager certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontexttrust.html#cfn-appmesh-virtualnode-tlsvalidationcontexttrust-acm
            '''
            result = self._values.get("acm")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.TlsValidationContextAcmTrustProperty"]], result)

        @builtins.property
        def file(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty"]]:
            '''An object that represents a Transport Layer Security (TLS) validation context trust for a local file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontexttrust.html#cfn-appmesh-virtualnode-tlsvalidationcontexttrust-file
            '''
            result = self._values.get("file")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty"]], result)

        @builtins.property
        def sds(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty"]]:
            '''A reference to an object that represents a Transport Layer Security (TLS) Secret Discovery Service validation context trust.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontexttrust.html#cfn-appmesh-virtualnode-tlsvalidationcontexttrust-sds
            '''
            result = self._values.get("sds")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TlsValidationContextTrustProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.VirtualNodeConnectionPoolProperty",
        jsii_struct_bases=[],
        name_mapping={"grpc": "grpc", "http": "http", "http2": "http2", "tcp": "tcp"},
    )
    class VirtualNodeConnectionPoolProperty:
        def __init__(
            self,
            *,
            grpc: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.VirtualNodeGrpcConnectionPoolProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            http: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.VirtualNodeHttpConnectionPoolProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            http2: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.VirtualNodeHttp2ConnectionPoolProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            tcp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.VirtualNodeTcpConnectionPoolProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents the type of virtual node connection pool.

            Only one protocol is used at a time and should be the same protocol as the one chosen under port mapping.

            If not present the default value for ``maxPendingRequests`` is ``2147483647`` .

            :param grpc: An object that represents a type of connection pool.
            :param http: An object that represents a type of connection pool.
            :param http2: An object that represents a type of connection pool.
            :param tcp: An object that represents a type of connection pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodeconnectionpool.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_node_connection_pool_property = appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeConnectionPoolProperty(
                    grpc=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeGrpcConnectionPoolProperty(
                        max_requests=123
                    ),
                    http=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeHttpConnectionPoolProperty(
                        max_connections=123,
                        max_pending_requests=123
                    ),
                    http2=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeHttp2ConnectionPoolProperty(
                        max_requests=123
                    ),
                    tcp=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeTcpConnectionPoolProperty(
                        max_connections=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fb24e7db42da6e9724b4238ccb88def1a8dbb32ebc591bf8650d478926a6b322)
                check_type(argname="argument grpc", value=grpc, expected_type=type_hints["grpc"])
                check_type(argname="argument http", value=http, expected_type=type_hints["http"])
                check_type(argname="argument http2", value=http2, expected_type=type_hints["http2"])
                check_type(argname="argument tcp", value=tcp, expected_type=type_hints["tcp"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if grpc is not None:
                self._values["grpc"] = grpc
            if http is not None:
                self._values["http"] = http
            if http2 is not None:
                self._values["http2"] = http2
            if tcp is not None:
                self._values["tcp"] = tcp

        @builtins.property
        def grpc(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.VirtualNodeGrpcConnectionPoolProperty"]]:
            '''An object that represents a type of connection pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodeconnectionpool.html#cfn-appmesh-virtualnode-virtualnodeconnectionpool-grpc
            '''
            result = self._values.get("grpc")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.VirtualNodeGrpcConnectionPoolProperty"]], result)

        @builtins.property
        def http(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.VirtualNodeHttpConnectionPoolProperty"]]:
            '''An object that represents a type of connection pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodeconnectionpool.html#cfn-appmesh-virtualnode-virtualnodeconnectionpool-http
            '''
            result = self._values.get("http")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.VirtualNodeHttpConnectionPoolProperty"]], result)

        @builtins.property
        def http2(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.VirtualNodeHttp2ConnectionPoolProperty"]]:
            '''An object that represents a type of connection pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodeconnectionpool.html#cfn-appmesh-virtualnode-virtualnodeconnectionpool-http2
            '''
            result = self._values.get("http2")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.VirtualNodeHttp2ConnectionPoolProperty"]], result)

        @builtins.property
        def tcp(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.VirtualNodeTcpConnectionPoolProperty"]]:
            '''An object that represents a type of connection pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodeconnectionpool.html#cfn-appmesh-virtualnode-virtualnodeconnectionpool-tcp
            '''
            result = self._values.get("tcp")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.VirtualNodeTcpConnectionPoolProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualNodeConnectionPoolProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.VirtualNodeGrpcConnectionPoolProperty",
        jsii_struct_bases=[],
        name_mapping={"max_requests": "maxRequests"},
    )
    class VirtualNodeGrpcConnectionPoolProperty:
        def __init__(
            self,
            *,
            max_requests: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An object that represents a type of connection pool.

            :param max_requests: Maximum number of inflight requests Envoy can concurrently support across hosts in upstream cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodegrpcconnectionpool.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_node_grpc_connection_pool_property = appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeGrpcConnectionPoolProperty(
                    max_requests=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0265839dc0e096a3378f0a8d9a07c1a8db4e2a05c237558683149b626e0fbaef)
                check_type(argname="argument max_requests", value=max_requests, expected_type=type_hints["max_requests"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_requests is not None:
                self._values["max_requests"] = max_requests

        @builtins.property
        def max_requests(self) -> typing.Optional[jsii.Number]:
            '''Maximum number of inflight requests Envoy can concurrently support across hosts in upstream cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodegrpcconnectionpool.html#cfn-appmesh-virtualnode-virtualnodegrpcconnectionpool-maxrequests
            '''
            result = self._values.get("max_requests")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualNodeGrpcConnectionPoolProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.VirtualNodeHttp2ConnectionPoolProperty",
        jsii_struct_bases=[],
        name_mapping={"max_requests": "maxRequests"},
    )
    class VirtualNodeHttp2ConnectionPoolProperty:
        def __init__(
            self,
            *,
            max_requests: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An object that represents a type of connection pool.

            :param max_requests: Maximum number of inflight requests Envoy can concurrently support across hosts in upstream cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodehttp2connectionpool.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_node_http2_connection_pool_property = appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeHttp2ConnectionPoolProperty(
                    max_requests=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3a7ee245206521f1c337aa2fb4b929bbe2368c619a6d182f19135a14e84aacf0)
                check_type(argname="argument max_requests", value=max_requests, expected_type=type_hints["max_requests"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_requests is not None:
                self._values["max_requests"] = max_requests

        @builtins.property
        def max_requests(self) -> typing.Optional[jsii.Number]:
            '''Maximum number of inflight requests Envoy can concurrently support across hosts in upstream cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodehttp2connectionpool.html#cfn-appmesh-virtualnode-virtualnodehttp2connectionpool-maxrequests
            '''
            result = self._values.get("max_requests")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualNodeHttp2ConnectionPoolProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.VirtualNodeHttpConnectionPoolProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_connections": "maxConnections",
            "max_pending_requests": "maxPendingRequests",
        },
    )
    class VirtualNodeHttpConnectionPoolProperty:
        def __init__(
            self,
            *,
            max_connections: typing.Optional[jsii.Number] = None,
            max_pending_requests: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An object that represents a type of connection pool.

            :param max_connections: Maximum number of outbound TCP connections Envoy can establish concurrently with all hosts in upstream cluster.
            :param max_pending_requests: Number of overflowing requests after ``max_connections`` Envoy will queue to upstream cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodehttpconnectionpool.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_node_http_connection_pool_property = appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeHttpConnectionPoolProperty(
                    max_connections=123,
                    max_pending_requests=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7dfacfdfdc8b4cb46c427e965a4d4fdf9e2da818711acb3d92d39bf17e85b04a)
                check_type(argname="argument max_connections", value=max_connections, expected_type=type_hints["max_connections"])
                check_type(argname="argument max_pending_requests", value=max_pending_requests, expected_type=type_hints["max_pending_requests"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_connections is not None:
                self._values["max_connections"] = max_connections
            if max_pending_requests is not None:
                self._values["max_pending_requests"] = max_pending_requests

        @builtins.property
        def max_connections(self) -> typing.Optional[jsii.Number]:
            '''Maximum number of outbound TCP connections Envoy can establish concurrently with all hosts in upstream cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodehttpconnectionpool.html#cfn-appmesh-virtualnode-virtualnodehttpconnectionpool-maxconnections
            '''
            result = self._values.get("max_connections")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_pending_requests(self) -> typing.Optional[jsii.Number]:
            '''Number of overflowing requests after ``max_connections`` Envoy will queue to upstream cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodehttpconnectionpool.html#cfn-appmesh-virtualnode-virtualnodehttpconnectionpool-maxpendingrequests
            '''
            result = self._values.get("max_pending_requests")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualNodeHttpConnectionPoolProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.VirtualNodeSpecProperty",
        jsii_struct_bases=[],
        name_mapping={
            "backend_defaults": "backendDefaults",
            "backends": "backends",
            "listeners": "listeners",
            "logging": "logging",
            "service_discovery": "serviceDiscovery",
        },
    )
    class VirtualNodeSpecProperty:
        def __init__(
            self,
            *,
            backend_defaults: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.BackendDefaultsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            backends: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.BackendProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            listeners: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.ListenerProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            logging: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.LoggingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            service_discovery: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.ServiceDiscoveryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents the specification of a virtual node.

            :param backend_defaults: A reference to an object that represents the defaults for backends.
            :param backends: The backends that the virtual node is expected to send outbound traffic to. .. epigraph:: App Mesh doesn't validate the existence of those virtual services specified in backends. This is to prevent a cyclic dependency between virtual nodes and virtual services creation. Make sure the virtual service name is correct. The virtual service can be created afterwards if it doesn't already exist.
            :param listeners: The listener that the virtual node is expected to receive inbound traffic from. You can specify one listener.
            :param logging: The inbound and outbound access logging information for the virtual node.
            :param service_discovery: The service discovery information for the virtual node. If your virtual node does not expect ingress traffic, you can omit this parameter. If you specify a ``listener`` , then you must specify service discovery information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodespec.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_node_spec_property = appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeSpecProperty(
                    backend_defaults=appmesh_mixins.CfnVirtualNodePropsMixin.BackendDefaultsProperty(
                        client_policy=appmesh_mixins.CfnVirtualNodePropsMixin.ClientPolicyProperty(
                            tls=appmesh_mixins.CfnVirtualNodePropsMixin.ClientPolicyTlsProperty(
                                certificate=appmesh_mixins.CfnVirtualNodePropsMixin.ClientTlsCertificateProperty(
                                    file=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty(
                                        certificate_chain="certificateChain",
                                        private_key="privateKey"
                                    ),
                                    sds=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty(
                                        secret_name="secretName"
                                    )
                                ),
                                enforce=False,
                                ports=[123],
                                validation=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextProperty(
                                    subject_alternative_names=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty(
                                        match=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty(
                                            exact=["exact"]
                                        )
                                    ),
                                    trust=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextTrustProperty(
                                        acm=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextAcmTrustProperty(
                                            certificate_authority_arns=["certificateAuthorityArns"]
                                        ),
                                        file=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty(
                                            certificate_chain="certificateChain"
                                        ),
                                        sds=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty(
                                            secret_name="secretName"
                                        )
                                    )
                                )
                            )
                        )
                    ),
                    backends=[appmesh_mixins.CfnVirtualNodePropsMixin.BackendProperty(
                        virtual_service=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualServiceBackendProperty(
                            client_policy=appmesh_mixins.CfnVirtualNodePropsMixin.ClientPolicyProperty(
                                tls=appmesh_mixins.CfnVirtualNodePropsMixin.ClientPolicyTlsProperty(
                                    certificate=appmesh_mixins.CfnVirtualNodePropsMixin.ClientTlsCertificateProperty(
                                        file=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty(
                                            certificate_chain="certificateChain",
                                            private_key="privateKey"
                                        ),
                                        sds=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty(
                                            secret_name="secretName"
                                        )
                                    ),
                                    enforce=False,
                                    ports=[123],
                                    validation=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextProperty(
                                        subject_alternative_names=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty(
                                            match=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty(
                                                exact=["exact"]
                                            )
                                        ),
                                        trust=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextTrustProperty(
                                            acm=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextAcmTrustProperty(
                                                certificate_authority_arns=["certificateAuthorityArns"]
                                            ),
                                            file=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty(
                                                certificate_chain="certificateChain"
                                            ),
                                            sds=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty(
                                                secret_name="secretName"
                                            )
                                        )
                                    )
                                )
                            ),
                            virtual_service_name="virtualServiceName"
                        )
                    )],
                    listeners=[appmesh_mixins.CfnVirtualNodePropsMixin.ListenerProperty(
                        connection_pool=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeConnectionPoolProperty(
                            grpc=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeGrpcConnectionPoolProperty(
                                max_requests=123
                            ),
                            http=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeHttpConnectionPoolProperty(
                                max_connections=123,
                                max_pending_requests=123
                            ),
                            http2=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeHttp2ConnectionPoolProperty(
                                max_requests=123
                            ),
                            tcp=appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeTcpConnectionPoolProperty(
                                max_connections=123
                            )
                        ),
                        health_check=appmesh_mixins.CfnVirtualNodePropsMixin.HealthCheckProperty(
                            healthy_threshold=123,
                            interval_millis=123,
                            path="path",
                            port=123,
                            protocol="protocol",
                            timeout_millis=123,
                            unhealthy_threshold=123
                        ),
                        outlier_detection=appmesh_mixins.CfnVirtualNodePropsMixin.OutlierDetectionProperty(
                            base_ejection_duration=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            ),
                            interval=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                unit="unit",
                                value=123
                            ),
                            max_ejection_percent=123,
                            max_server_errors=123
                        ),
                        port_mapping=appmesh_mixins.CfnVirtualNodePropsMixin.PortMappingProperty(
                            port=123,
                            protocol="protocol"
                        ),
                        timeout=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTimeoutProperty(
                            grpc=appmesh_mixins.CfnVirtualNodePropsMixin.GrpcTimeoutProperty(
                                idle=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                    unit="unit",
                                    value=123
                                ),
                                per_request=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                    unit="unit",
                                    value=123
                                )
                            ),
                            http=appmesh_mixins.CfnVirtualNodePropsMixin.HttpTimeoutProperty(
                                idle=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                    unit="unit",
                                    value=123
                                ),
                                per_request=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                    unit="unit",
                                    value=123
                                )
                            ),
                            http2=appmesh_mixins.CfnVirtualNodePropsMixin.HttpTimeoutProperty(
                                idle=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                    unit="unit",
                                    value=123
                                ),
                                per_request=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                    unit="unit",
                                    value=123
                                )
                            ),
                            tcp=appmesh_mixins.CfnVirtualNodePropsMixin.TcpTimeoutProperty(
                                idle=appmesh_mixins.CfnVirtualNodePropsMixin.DurationProperty(
                                    unit="unit",
                                    value=123
                                )
                            )
                        ),
                        tls=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsProperty(
                            certificate=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsCertificateProperty(
                                acm=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsAcmCertificateProperty(
                                    certificate_arn="certificateArn"
                                ),
                                file=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty(
                                    certificate_chain="certificateChain",
                                    private_key="privateKey"
                                ),
                                sds=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty(
                                    secret_name="secretName"
                                )
                            ),
                            mode="mode",
                            validation=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsValidationContextProperty(
                                subject_alternative_names=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty(
                                    match=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty(
                                        exact=["exact"]
                                    )
                                ),
                                trust=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsValidationContextTrustProperty(
                                    file=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty(
                                        certificate_chain="certificateChain"
                                    ),
                                    sds=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty(
                                        secret_name="secretName"
                                    )
                                )
                            )
                        )
                    )],
                    logging=appmesh_mixins.CfnVirtualNodePropsMixin.LoggingProperty(
                        access_log=appmesh_mixins.CfnVirtualNodePropsMixin.AccessLogProperty(
                            file=appmesh_mixins.CfnVirtualNodePropsMixin.FileAccessLogProperty(
                                format=appmesh_mixins.CfnVirtualNodePropsMixin.LoggingFormatProperty(
                                    json=[appmesh_mixins.CfnVirtualNodePropsMixin.JsonFormatRefProperty(
                                        key="key",
                                        value="value"
                                    )],
                                    text="text"
                                ),
                                path="path"
                            )
                        )
                    ),
                    service_discovery=appmesh_mixins.CfnVirtualNodePropsMixin.ServiceDiscoveryProperty(
                        aws_cloud_map=appmesh_mixins.CfnVirtualNodePropsMixin.AwsCloudMapServiceDiscoveryProperty(
                            attributes=[appmesh_mixins.CfnVirtualNodePropsMixin.AwsCloudMapInstanceAttributeProperty(
                                key="key",
                                value="value"
                            )],
                            ip_preference="ipPreference",
                            namespace_name="namespaceName",
                            service_name="serviceName"
                        ),
                        dns=appmesh_mixins.CfnVirtualNodePropsMixin.DnsServiceDiscoveryProperty(
                            hostname="hostname",
                            ip_preference="ipPreference",
                            response_type="responseType"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1863a792e2f983eaec81ade4fb248c4a0ed1c0e58b10777364d9b83debda66e5)
                check_type(argname="argument backend_defaults", value=backend_defaults, expected_type=type_hints["backend_defaults"])
                check_type(argname="argument backends", value=backends, expected_type=type_hints["backends"])
                check_type(argname="argument listeners", value=listeners, expected_type=type_hints["listeners"])
                check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
                check_type(argname="argument service_discovery", value=service_discovery, expected_type=type_hints["service_discovery"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if backend_defaults is not None:
                self._values["backend_defaults"] = backend_defaults
            if backends is not None:
                self._values["backends"] = backends
            if listeners is not None:
                self._values["listeners"] = listeners
            if logging is not None:
                self._values["logging"] = logging
            if service_discovery is not None:
                self._values["service_discovery"] = service_discovery

        @builtins.property
        def backend_defaults(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.BackendDefaultsProperty"]]:
            '''A reference to an object that represents the defaults for backends.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodespec.html#cfn-appmesh-virtualnode-virtualnodespec-backenddefaults
            '''
            result = self._values.get("backend_defaults")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.BackendDefaultsProperty"]], result)

        @builtins.property
        def backends(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.BackendProperty"]]]]:
            '''The backends that the virtual node is expected to send outbound traffic to.

            .. epigraph::

               App Mesh doesn't validate the existence of those virtual services specified in backends. This is to prevent a cyclic dependency between virtual nodes and virtual services creation. Make sure the virtual service name is correct. The virtual service can be created afterwards if it doesn't already exist.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodespec.html#cfn-appmesh-virtualnode-virtualnodespec-backends
            '''
            result = self._values.get("backends")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.BackendProperty"]]]], result)

        @builtins.property
        def listeners(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ListenerProperty"]]]]:
            '''The listener that the virtual node is expected to receive inbound traffic from.

            You can specify one listener.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodespec.html#cfn-appmesh-virtualnode-virtualnodespec-listeners
            '''
            result = self._values.get("listeners")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ListenerProperty"]]]], result)

        @builtins.property
        def logging(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.LoggingProperty"]]:
            '''The inbound and outbound access logging information for the virtual node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodespec.html#cfn-appmesh-virtualnode-virtualnodespec-logging
            '''
            result = self._values.get("logging")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.LoggingProperty"]], result)

        @builtins.property
        def service_discovery(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ServiceDiscoveryProperty"]]:
            '''The service discovery information for the virtual node.

            If your virtual node does not expect ingress traffic, you can omit this parameter. If you specify a ``listener`` , then you must specify service discovery information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodespec.html#cfn-appmesh-virtualnode-virtualnodespec-servicediscovery
            '''
            result = self._values.get("service_discovery")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ServiceDiscoveryProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualNodeSpecProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.VirtualNodeTcpConnectionPoolProperty",
        jsii_struct_bases=[],
        name_mapping={"max_connections": "maxConnections"},
    )
    class VirtualNodeTcpConnectionPoolProperty:
        def __init__(
            self,
            *,
            max_connections: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An object that represents a type of connection pool.

            :param max_connections: Maximum number of outbound TCP connections Envoy can establish concurrently with all hosts in upstream cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodetcpconnectionpool.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_node_tcp_connection_pool_property = appmesh_mixins.CfnVirtualNodePropsMixin.VirtualNodeTcpConnectionPoolProperty(
                    max_connections=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__182338d59e788b351fd353d1dd7c316d217e1c29d8b4e9e88c5d2b689d508866)
                check_type(argname="argument max_connections", value=max_connections, expected_type=type_hints["max_connections"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_connections is not None:
                self._values["max_connections"] = max_connections

        @builtins.property
        def max_connections(self) -> typing.Optional[jsii.Number]:
            '''Maximum number of outbound TCP connections Envoy can establish concurrently with all hosts in upstream cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodetcpconnectionpool.html#cfn-appmesh-virtualnode-virtualnodetcpconnectionpool-maxconnections
            '''
            result = self._values.get("max_connections")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualNodeTcpConnectionPoolProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualNodePropsMixin.VirtualServiceBackendProperty",
        jsii_struct_bases=[],
        name_mapping={
            "client_policy": "clientPolicy",
            "virtual_service_name": "virtualServiceName",
        },
    )
    class VirtualServiceBackendProperty:
        def __init__(
            self,
            *,
            client_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualNodePropsMixin.ClientPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            virtual_service_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents a virtual service backend for a virtual node.

            :param client_policy: A reference to an object that represents the client policy for a backend.
            :param virtual_service_name: The name of the virtual service that is acting as a virtual node backend. .. epigraph:: App Mesh doesn't validate the existence of those virtual services specified in backends. This is to prevent a cyclic dependency between virtual nodes and virtual services creation. Make sure the virtual service name is correct. The virtual service can be created afterwards if it doesn't already exist.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualservicebackend.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_service_backend_property = appmesh_mixins.CfnVirtualNodePropsMixin.VirtualServiceBackendProperty(
                    client_policy=appmesh_mixins.CfnVirtualNodePropsMixin.ClientPolicyProperty(
                        tls=appmesh_mixins.CfnVirtualNodePropsMixin.ClientPolicyTlsProperty(
                            certificate=appmesh_mixins.CfnVirtualNodePropsMixin.ClientTlsCertificateProperty(
                                file=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty(
                                    certificate_chain="certificateChain",
                                    private_key="privateKey"
                                ),
                                sds=appmesh_mixins.CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty(
                                    secret_name="secretName"
                                )
                            ),
                            enforce=False,
                            ports=[123],
                            validation=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextProperty(
                                subject_alternative_names=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty(
                                    match=appmesh_mixins.CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty(
                                        exact=["exact"]
                                    )
                                ),
                                trust=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextTrustProperty(
                                    acm=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextAcmTrustProperty(
                                        certificate_authority_arns=["certificateAuthorityArns"]
                                    ),
                                    file=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty(
                                        certificate_chain="certificateChain"
                                    ),
                                    sds=appmesh_mixins.CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty(
                                        secret_name="secretName"
                                    )
                                )
                            )
                        )
                    ),
                    virtual_service_name="virtualServiceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2c32112b4c8a2ba903dbe27bc9bd1f7d6ea1d6b98fb2655d95577c3b396330b2)
                check_type(argname="argument client_policy", value=client_policy, expected_type=type_hints["client_policy"])
                check_type(argname="argument virtual_service_name", value=virtual_service_name, expected_type=type_hints["virtual_service_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if client_policy is not None:
                self._values["client_policy"] = client_policy
            if virtual_service_name is not None:
                self._values["virtual_service_name"] = virtual_service_name

        @builtins.property
        def client_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ClientPolicyProperty"]]:
            '''A reference to an object that represents the client policy for a backend.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualservicebackend.html#cfn-appmesh-virtualnode-virtualservicebackend-clientpolicy
            '''
            result = self._values.get("client_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualNodePropsMixin.ClientPolicyProperty"]], result)

        @builtins.property
        def virtual_service_name(self) -> typing.Optional[builtins.str]:
            '''The name of the virtual service that is acting as a virtual node backend.

            .. epigraph::

               App Mesh doesn't validate the existence of those virtual services specified in backends. This is to prevent a cyclic dependency between virtual nodes and virtual services creation. Make sure the virtual service name is correct. The virtual service can be created afterwards if it doesn't already exist.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualservicebackend.html#cfn-appmesh-virtualnode-virtualservicebackend-virtualservicename
            '''
            result = self._values.get("virtual_service_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualServiceBackendProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualRouterMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "mesh_name": "meshName",
        "mesh_owner": "meshOwner",
        "spec": "spec",
        "tags": "tags",
        "virtual_router_name": "virtualRouterName",
    },
)
class CfnVirtualRouterMixinProps:
    def __init__(
        self,
        *,
        mesh_name: typing.Optional[builtins.str] = None,
        mesh_owner: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualRouterPropsMixin.VirtualRouterSpecProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        virtual_router_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnVirtualRouterPropsMixin.

        :param mesh_name: The name of the service mesh to create the virtual router in.
        :param mesh_owner: The AWS IAM account ID of the service mesh owner. If the account ID is not your own, then the account that you specify must share the mesh with your account before you can create the resource in the service mesh. For more information about mesh sharing, see `Working with shared meshes <https://docs.aws.amazon.com/app-mesh/latest/userguide/sharing.html>`_ .
        :param spec: The virtual router specification to apply.
        :param tags: Optional metadata that you can apply to the virtual router to assist with categorization and organization. Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.
        :param virtual_router_name: The name to use for the virtual router.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
            
            cfn_virtual_router_mixin_props = appmesh_mixins.CfnVirtualRouterMixinProps(
                mesh_name="meshName",
                mesh_owner="meshOwner",
                spec=appmesh_mixins.CfnVirtualRouterPropsMixin.VirtualRouterSpecProperty(
                    listeners=[appmesh_mixins.CfnVirtualRouterPropsMixin.VirtualRouterListenerProperty(
                        port_mapping=appmesh_mixins.CfnVirtualRouterPropsMixin.PortMappingProperty(
                            port=123,
                            protocol="protocol"
                        )
                    )]
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                virtual_router_name="virtualRouterName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a595b16e7cd8bf8e9436ae3980c9ee141c5aab677603b7d065ff474e25af7c61)
            check_type(argname="argument mesh_name", value=mesh_name, expected_type=type_hints["mesh_name"])
            check_type(argname="argument mesh_owner", value=mesh_owner, expected_type=type_hints["mesh_owner"])
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument virtual_router_name", value=virtual_router_name, expected_type=type_hints["virtual_router_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mesh_name is not None:
            self._values["mesh_name"] = mesh_name
        if mesh_owner is not None:
            self._values["mesh_owner"] = mesh_owner
        if spec is not None:
            self._values["spec"] = spec
        if tags is not None:
            self._values["tags"] = tags
        if virtual_router_name is not None:
            self._values["virtual_router_name"] = virtual_router_name

    @builtins.property
    def mesh_name(self) -> typing.Optional[builtins.str]:
        '''The name of the service mesh to create the virtual router in.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-meshname
        '''
        result = self._values.get("mesh_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mesh_owner(self) -> typing.Optional[builtins.str]:
        '''The AWS IAM account ID of the service mesh owner.

        If the account ID is not your own, then the account that you specify must share the mesh with your account before you can create the resource in the service mesh. For more information about mesh sharing, see `Working with shared meshes <https://docs.aws.amazon.com/app-mesh/latest/userguide/sharing.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-meshowner
        '''
        result = self._values.get("mesh_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spec(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualRouterPropsMixin.VirtualRouterSpecProperty"]]:
        '''The virtual router specification to apply.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-spec
        '''
        result = self._values.get("spec")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualRouterPropsMixin.VirtualRouterSpecProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Optional metadata that you can apply to the virtual router to assist with categorization and organization.

        Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def virtual_router_name(self) -> typing.Optional[builtins.str]:
        '''The name to use for the virtual router.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-virtualroutername
        '''
        result = self._values.get("virtual_router_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVirtualRouterMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVirtualRouterPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualRouterPropsMixin",
):
    '''Creates a virtual router within a service mesh.

    Specify a ``listener`` for any inbound traffic that your virtual router receives. Create a virtual router for each protocol and port that you need to route. Virtual routers handle traffic for one or more virtual services within your mesh. After you create your virtual router, create and associate routes for your virtual router that direct incoming requests to different virtual nodes.

    For more information about virtual routers, see `Virtual routers <https://docs.aws.amazon.com/app-mesh/latest/userguide/virtual_routers.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html
    :cloudformationResource: AWS::AppMesh::VirtualRouter
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
        
        cfn_virtual_router_props_mixin = appmesh_mixins.CfnVirtualRouterPropsMixin(appmesh_mixins.CfnVirtualRouterMixinProps(
            mesh_name="meshName",
            mesh_owner="meshOwner",
            spec=appmesh_mixins.CfnVirtualRouterPropsMixin.VirtualRouterSpecProperty(
                listeners=[appmesh_mixins.CfnVirtualRouterPropsMixin.VirtualRouterListenerProperty(
                    port_mapping=appmesh_mixins.CfnVirtualRouterPropsMixin.PortMappingProperty(
                        port=123,
                        protocol="protocol"
                    )
                )]
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            virtual_router_name="virtualRouterName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVirtualRouterMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppMesh::VirtualRouter``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ab04af38a7f62a19bee44b4930093b581f0e2b3b7401f523843e57b9225957d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca4c93b9912edb5c5158d1f429f2dba997367fb1684cc84ef7f8daccf6e0f5d0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e96a0351035f92ea7fb60f40f166805c883d21093f07d0eb2a5a6ec1f6aae55)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVirtualRouterMixinProps:
        return typing.cast(CfnVirtualRouterMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualRouterPropsMixin.PortMappingProperty",
        jsii_struct_bases=[],
        name_mapping={"port": "port", "protocol": "protocol"},
    )
    class PortMappingProperty:
        def __init__(
            self,
            *,
            port: typing.Optional[jsii.Number] = None,
            protocol: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object representing a virtual router listener port mapping.

            :param port: The port used for the port mapping.
            :param protocol: The protocol used for the port mapping. Specify one protocol.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-portmapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                port_mapping_property = appmesh_mixins.CfnVirtualRouterPropsMixin.PortMappingProperty(
                    port=123,
                    protocol="protocol"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e84e7b62fbf4c03585700db4f1e44ebba7b05b55fd5c222b3913b9168cd21dae)
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if port is not None:
                self._values["port"] = port
            if protocol is not None:
                self._values["protocol"] = protocol

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port used for the port mapping.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-portmapping.html#cfn-appmesh-virtualrouter-portmapping-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The protocol used for the port mapping.

            Specify one protocol.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-portmapping.html#cfn-appmesh-virtualrouter-portmapping-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualRouterPropsMixin.VirtualRouterListenerProperty",
        jsii_struct_bases=[],
        name_mapping={"port_mapping": "portMapping"},
    )
    class VirtualRouterListenerProperty:
        def __init__(
            self,
            *,
            port_mapping: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualRouterPropsMixin.PortMappingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents a virtual router listener.

            :param port_mapping: The port mapping information for the listener.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-virtualrouterlistener.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_router_listener_property = appmesh_mixins.CfnVirtualRouterPropsMixin.VirtualRouterListenerProperty(
                    port_mapping=appmesh_mixins.CfnVirtualRouterPropsMixin.PortMappingProperty(
                        port=123,
                        protocol="protocol"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__812b8813375dd859e8f0f59abd164bedda015ed063a0753c709b9c8a22c75ef2)
                check_type(argname="argument port_mapping", value=port_mapping, expected_type=type_hints["port_mapping"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if port_mapping is not None:
                self._values["port_mapping"] = port_mapping

        @builtins.property
        def port_mapping(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualRouterPropsMixin.PortMappingProperty"]]:
            '''The port mapping information for the listener.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-virtualrouterlistener.html#cfn-appmesh-virtualrouter-virtualrouterlistener-portmapping
            '''
            result = self._values.get("port_mapping")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualRouterPropsMixin.PortMappingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualRouterListenerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualRouterPropsMixin.VirtualRouterSpecProperty",
        jsii_struct_bases=[],
        name_mapping={"listeners": "listeners"},
    )
    class VirtualRouterSpecProperty:
        def __init__(
            self,
            *,
            listeners: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualRouterPropsMixin.VirtualRouterListenerProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''An object that represents the specification of a virtual router.

            :param listeners: The listeners that the virtual router is expected to receive inbound traffic from.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-virtualrouterspec.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_router_spec_property = appmesh_mixins.CfnVirtualRouterPropsMixin.VirtualRouterSpecProperty(
                    listeners=[appmesh_mixins.CfnVirtualRouterPropsMixin.VirtualRouterListenerProperty(
                        port_mapping=appmesh_mixins.CfnVirtualRouterPropsMixin.PortMappingProperty(
                            port=123,
                            protocol="protocol"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3e413f421ca0e50e0216acbe5a0d2ce6f35a8a34dcc4084df9f91f0644db8dc7)
                check_type(argname="argument listeners", value=listeners, expected_type=type_hints["listeners"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if listeners is not None:
                self._values["listeners"] = listeners

        @builtins.property
        def listeners(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualRouterPropsMixin.VirtualRouterListenerProperty"]]]]:
            '''The listeners that the virtual router is expected to receive inbound traffic from.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-virtualrouterspec.html#cfn-appmesh-virtualrouter-virtualrouterspec-listeners
            '''
            result = self._values.get("listeners")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualRouterPropsMixin.VirtualRouterListenerProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualRouterSpecProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualServiceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "mesh_name": "meshName",
        "mesh_owner": "meshOwner",
        "spec": "spec",
        "tags": "tags",
        "virtual_service_name": "virtualServiceName",
    },
)
class CfnVirtualServiceMixinProps:
    def __init__(
        self,
        *,
        mesh_name: typing.Optional[builtins.str] = None,
        mesh_owner: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualServicePropsMixin.VirtualServiceSpecProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        virtual_service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnVirtualServicePropsMixin.

        :param mesh_name: The name of the service mesh to create the virtual service in.
        :param mesh_owner: The AWS IAM account ID of the service mesh owner. If the account ID is not your own, then the account that you specify must share the mesh with your account before you can create the resource in the service mesh. For more information about mesh sharing, see `Working with shared meshes <https://docs.aws.amazon.com/app-mesh/latest/userguide/sharing.html>`_ .
        :param spec: The virtual service specification to apply.
        :param tags: Optional metadata that you can apply to the virtual service to assist with categorization and organization. Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.
        :param virtual_service_name: The name to use for the virtual service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
            
            cfn_virtual_service_mixin_props = appmesh_mixins.CfnVirtualServiceMixinProps(
                mesh_name="meshName",
                mesh_owner="meshOwner",
                spec=appmesh_mixins.CfnVirtualServicePropsMixin.VirtualServiceSpecProperty(
                    provider=appmesh_mixins.CfnVirtualServicePropsMixin.VirtualServiceProviderProperty(
                        virtual_node=appmesh_mixins.CfnVirtualServicePropsMixin.VirtualNodeServiceProviderProperty(
                            virtual_node_name="virtualNodeName"
                        ),
                        virtual_router=appmesh_mixins.CfnVirtualServicePropsMixin.VirtualRouterServiceProviderProperty(
                            virtual_router_name="virtualRouterName"
                        )
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                virtual_service_name="virtualServiceName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb2c9298fd70af0858babd344a2b0c2bec0ae89da72ebe047e4592fbccc4553)
            check_type(argname="argument mesh_name", value=mesh_name, expected_type=type_hints["mesh_name"])
            check_type(argname="argument mesh_owner", value=mesh_owner, expected_type=type_hints["mesh_owner"])
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument virtual_service_name", value=virtual_service_name, expected_type=type_hints["virtual_service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mesh_name is not None:
            self._values["mesh_name"] = mesh_name
        if mesh_owner is not None:
            self._values["mesh_owner"] = mesh_owner
        if spec is not None:
            self._values["spec"] = spec
        if tags is not None:
            self._values["tags"] = tags
        if virtual_service_name is not None:
            self._values["virtual_service_name"] = virtual_service_name

    @builtins.property
    def mesh_name(self) -> typing.Optional[builtins.str]:
        '''The name of the service mesh to create the virtual service in.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-meshname
        '''
        result = self._values.get("mesh_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mesh_owner(self) -> typing.Optional[builtins.str]:
        '''The AWS IAM account ID of the service mesh owner.

        If the account ID is not your own, then the account that you specify must share the mesh with your account before you can create the resource in the service mesh. For more information about mesh sharing, see `Working with shared meshes <https://docs.aws.amazon.com/app-mesh/latest/userguide/sharing.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-meshowner
        '''
        result = self._values.get("mesh_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spec(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualServicePropsMixin.VirtualServiceSpecProperty"]]:
        '''The virtual service specification to apply.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-spec
        '''
        result = self._values.get("spec")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualServicePropsMixin.VirtualServiceSpecProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Optional metadata that you can apply to the virtual service to assist with categorization and organization.

        Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def virtual_service_name(self) -> typing.Optional[builtins.str]:
        '''The name to use for the virtual service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-virtualservicename
        '''
        result = self._values.get("virtual_service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVirtualServiceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVirtualServicePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualServicePropsMixin",
):
    '''Creates a virtual service within a service mesh.

    A virtual service is an abstraction of a real service that is provided by a virtual node directly or indirectly by means of a virtual router. Dependent services call your virtual service by its ``virtualServiceName`` , and those requests are routed to the virtual node or virtual router that is specified as the provider for the virtual service.

    For more information about virtual services, see `Virtual services <https://docs.aws.amazon.com/app-mesh/latest/userguide/virtual_services.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html
    :cloudformationResource: AWS::AppMesh::VirtualService
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
        
        cfn_virtual_service_props_mixin = appmesh_mixins.CfnVirtualServicePropsMixin(appmesh_mixins.CfnVirtualServiceMixinProps(
            mesh_name="meshName",
            mesh_owner="meshOwner",
            spec=appmesh_mixins.CfnVirtualServicePropsMixin.VirtualServiceSpecProperty(
                provider=appmesh_mixins.CfnVirtualServicePropsMixin.VirtualServiceProviderProperty(
                    virtual_node=appmesh_mixins.CfnVirtualServicePropsMixin.VirtualNodeServiceProviderProperty(
                        virtual_node_name="virtualNodeName"
                    ),
                    virtual_router=appmesh_mixins.CfnVirtualServicePropsMixin.VirtualRouterServiceProviderProperty(
                        virtual_router_name="virtualRouterName"
                    )
                )
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            virtual_service_name="virtualServiceName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVirtualServiceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppMesh::VirtualService``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbb4325b60f38642b60a1e817bed8bafda6f50433581ba3a41af3a67c7e64bf1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9123da1f0ab9e6677ef25f534b123a6613d865f73afd2b601ccb7e55c8d1d276)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e905390e403a68f721dc363874e289649da512f8f1e872e2e2dc8fbf19a6f21d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVirtualServiceMixinProps:
        return typing.cast(CfnVirtualServiceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualServicePropsMixin.VirtualNodeServiceProviderProperty",
        jsii_struct_bases=[],
        name_mapping={"virtual_node_name": "virtualNodeName"},
    )
    class VirtualNodeServiceProviderProperty:
        def __init__(
            self,
            *,
            virtual_node_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents a virtual node service provider.

            :param virtual_node_name: The name of the virtual node that is acting as a service provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualnodeserviceprovider.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_node_service_provider_property = appmesh_mixins.CfnVirtualServicePropsMixin.VirtualNodeServiceProviderProperty(
                    virtual_node_name="virtualNodeName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3d99663d983371bad9dcfe52da0008d316513d6fa3729b81a59c7c3791093af8)
                check_type(argname="argument virtual_node_name", value=virtual_node_name, expected_type=type_hints["virtual_node_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if virtual_node_name is not None:
                self._values["virtual_node_name"] = virtual_node_name

        @builtins.property
        def virtual_node_name(self) -> typing.Optional[builtins.str]:
            '''The name of the virtual node that is acting as a service provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualnodeserviceprovider.html#cfn-appmesh-virtualservice-virtualnodeserviceprovider-virtualnodename
            '''
            result = self._values.get("virtual_node_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualNodeServiceProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualServicePropsMixin.VirtualRouterServiceProviderProperty",
        jsii_struct_bases=[],
        name_mapping={"virtual_router_name": "virtualRouterName"},
    )
    class VirtualRouterServiceProviderProperty:
        def __init__(
            self,
            *,
            virtual_router_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents a virtual node service provider.

            :param virtual_router_name: The name of the virtual router that is acting as a service provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualrouterserviceprovider.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_router_service_provider_property = appmesh_mixins.CfnVirtualServicePropsMixin.VirtualRouterServiceProviderProperty(
                    virtual_router_name="virtualRouterName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fe6dd7278b8e2cec7d1efa1a75c8f19d8534178a4e7acea5d64490d127a78631)
                check_type(argname="argument virtual_router_name", value=virtual_router_name, expected_type=type_hints["virtual_router_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if virtual_router_name is not None:
                self._values["virtual_router_name"] = virtual_router_name

        @builtins.property
        def virtual_router_name(self) -> typing.Optional[builtins.str]:
            '''The name of the virtual router that is acting as a service provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualrouterserviceprovider.html#cfn-appmesh-virtualservice-virtualrouterserviceprovider-virtualroutername
            '''
            result = self._values.get("virtual_router_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualRouterServiceProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualServicePropsMixin.VirtualServiceProviderProperty",
        jsii_struct_bases=[],
        name_mapping={
            "virtual_node": "virtualNode",
            "virtual_router": "virtualRouter",
        },
    )
    class VirtualServiceProviderProperty:
        def __init__(
            self,
            *,
            virtual_node: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualServicePropsMixin.VirtualNodeServiceProviderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            virtual_router: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualServicePropsMixin.VirtualRouterServiceProviderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents the provider for a virtual service.

            :param virtual_node: The virtual node associated with a virtual service.
            :param virtual_router: The virtual router associated with a virtual service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualserviceprovider.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_service_provider_property = appmesh_mixins.CfnVirtualServicePropsMixin.VirtualServiceProviderProperty(
                    virtual_node=appmesh_mixins.CfnVirtualServicePropsMixin.VirtualNodeServiceProviderProperty(
                        virtual_node_name="virtualNodeName"
                    ),
                    virtual_router=appmesh_mixins.CfnVirtualServicePropsMixin.VirtualRouterServiceProviderProperty(
                        virtual_router_name="virtualRouterName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__23542b92f04ad7e97ecb6b97a5241087151123d2e644021c0ed249a42fc911b9)
                check_type(argname="argument virtual_node", value=virtual_node, expected_type=type_hints["virtual_node"])
                check_type(argname="argument virtual_router", value=virtual_router, expected_type=type_hints["virtual_router"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if virtual_node is not None:
                self._values["virtual_node"] = virtual_node
            if virtual_router is not None:
                self._values["virtual_router"] = virtual_router

        @builtins.property
        def virtual_node(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualServicePropsMixin.VirtualNodeServiceProviderProperty"]]:
            '''The virtual node associated with a virtual service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualserviceprovider.html#cfn-appmesh-virtualservice-virtualserviceprovider-virtualnode
            '''
            result = self._values.get("virtual_node")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualServicePropsMixin.VirtualNodeServiceProviderProperty"]], result)

        @builtins.property
        def virtual_router(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualServicePropsMixin.VirtualRouterServiceProviderProperty"]]:
            '''The virtual router associated with a virtual service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualserviceprovider.html#cfn-appmesh-virtualservice-virtualserviceprovider-virtualrouter
            '''
            result = self._values.get("virtual_router")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualServicePropsMixin.VirtualRouterServiceProviderProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualServiceProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appmesh.mixins.CfnVirtualServicePropsMixin.VirtualServiceSpecProperty",
        jsii_struct_bases=[],
        name_mapping={"provider": "provider"},
    )
    class VirtualServiceSpecProperty:
        def __init__(
            self,
            *,
            provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVirtualServicePropsMixin.VirtualServiceProviderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents the specification of a virtual service.

            :param provider: The App Mesh object that is acting as the provider for a virtual service. You can specify a single virtual node or virtual router.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualservicespec.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appmesh import mixins as appmesh_mixins
                
                virtual_service_spec_property = appmesh_mixins.CfnVirtualServicePropsMixin.VirtualServiceSpecProperty(
                    provider=appmesh_mixins.CfnVirtualServicePropsMixin.VirtualServiceProviderProperty(
                        virtual_node=appmesh_mixins.CfnVirtualServicePropsMixin.VirtualNodeServiceProviderProperty(
                            virtual_node_name="virtualNodeName"
                        ),
                        virtual_router=appmesh_mixins.CfnVirtualServicePropsMixin.VirtualRouterServiceProviderProperty(
                            virtual_router_name="virtualRouterName"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__76de5b0b7090fde3fb95e5397ced62c0b3c22ed2bf15c4a589dc73c40c228fab)
                check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if provider is not None:
                self._values["provider"] = provider

        @builtins.property
        def provider(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualServicePropsMixin.VirtualServiceProviderProperty"]]:
            '''The App Mesh object that is acting as the provider for a virtual service.

            You can specify a single virtual node or virtual router.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualservicespec.html#cfn-appmesh-virtualservice-virtualservicespec-provider
            '''
            result = self._values.get("provider")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVirtualServicePropsMixin.VirtualServiceProviderProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VirtualServiceSpecProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnGatewayRouteMixinProps",
    "CfnGatewayRoutePropsMixin",
    "CfnMeshMixinProps",
    "CfnMeshPropsMixin",
    "CfnRouteMixinProps",
    "CfnRoutePropsMixin",
    "CfnVirtualGatewayMixinProps",
    "CfnVirtualGatewayPropsMixin",
    "CfnVirtualNodeMixinProps",
    "CfnVirtualNodePropsMixin",
    "CfnVirtualRouterMixinProps",
    "CfnVirtualRouterPropsMixin",
    "CfnVirtualServiceMixinProps",
    "CfnVirtualServicePropsMixin",
]

publication.publish()

def _typecheckingstub__02220d748b1d3ce373730b5de1cc9ff04fc32ef7f876b552de1281509ec60cad(
    *,
    gateway_route_name: typing.Optional[builtins.str] = None,
    mesh_name: typing.Optional[builtins.str] = None,
    mesh_owner: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.GatewayRouteSpecProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    virtual_gateway_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__824815bb481bc192658fa154ae4913585ab614fc94aa6db1672cc5574d4656be(
    props: typing.Union[CfnGatewayRouteMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dd45f06390e9438c7bbd15fcd523edd72623ac2a7618e5e3a0c415a043c9e65(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7e75eed816174686d03f17c653294e26b79bb76f0d3c00b267ea69c65054bf8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75918f333f411933786a1d7aa898cfdb1853ea25c538a5e6e0bac525ed9a15fc(
    *,
    exact: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59db7ca4152bf931bb6755d75236138d746dae95d8bdac9cb2dba0e838c1ee68(
    *,
    default_target_hostname: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c92bca337c042136c5dc91af7a0cc84a37012ed9ebb829dc9b55d12461bc4c28(
    *,
    exact: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    regex: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f4fd3d3ebfdb363d188788bcd6d1800e4a73c8208b64d4869b4d27b09be2d62(
    *,
    end: typing.Optional[jsii.Number] = None,
    start: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42f7865292d581f7869900f67d04fcdf60b372c947488bbd33853c25c4fff9e2(
    *,
    grpc_route: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.GrpcGatewayRouteProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    http2_route: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.HttpGatewayRouteProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    http_route: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.HttpGatewayRouteProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    priority: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d95014113505684b46029e5828143d1d6c91bf915dab819476ac94b9e878f0f3(
    *,
    port: typing.Optional[jsii.Number] = None,
    virtual_service: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.GatewayRouteVirtualServiceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94b71d5d22533990ba0fe2bb2773d917822ca24dff5d5d11fbb36625056d887a(
    *,
    virtual_service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ff18074936ef15630b969bdc52affcb8c82195dcb58f2559782be8b317f7e6f(
    *,
    rewrite: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.GrpcGatewayRouteRewriteProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.GatewayRouteTargetProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f539f6a6f4327f223e298867504bf62411180e5b432a02ccbef6be29b2d901a(
    *,
    hostname: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.GatewayRouteHostnameMatchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.GrpcGatewayRouteMetadataProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    port: typing.Optional[jsii.Number] = None,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da54e85a564a9f4d5877af87fa3fa6a57d44cd2d7581b76a8f7fa69c33a7fa41(
    *,
    invert: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.GatewayRouteMetadataMatchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c698a9386688ea28533b8cab57a73b041eda410a08c67498b30eca63ad829359(
    *,
    action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.GrpcGatewayRouteActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.GrpcGatewayRouteMatchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7399d3106fc9d4da4ebbedbe08e200603fd70d48ef7e175a72d72df0986bf22d(
    *,
    hostname: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf1cc8bca4777e191079c1ee7dfdf05f35856eb4f421c65ba275a15d497ca56f(
    *,
    rewrite: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.HttpGatewayRouteRewriteProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.GatewayRouteTargetProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aae92b2663765c3565ee413d5d8fcedbcc542fa6b5e291d5f454409496410291(
    *,
    exact: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.GatewayRouteRangeMatchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    regex: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c869f289d76ad24fd802ea67417e00b60c18dd28bda825231cb5e7fe0d04cb(
    *,
    invert: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderMatchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e484985e46dfe5059ea5c4169c64547e91e31a8d98a03d967fdb16c07305f055(
    *,
    headers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.HttpGatewayRouteHeaderProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    hostname: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.GatewayRouteHostnameMatchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    method: typing.Optional[builtins.str] = None,
    path: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.HttpPathMatchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    port: typing.Optional[jsii.Number] = None,
    prefix: typing.Optional[builtins.str] = None,
    query_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.QueryParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ee552e5eadbfaa9486e7824612c936f5518f2eb41c2127ab68fae2ac493797(
    *,
    exact: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba5921c074e3cbe5adb35393fb7d26b7bc5a70fef2033904fc4d728c72ffd1df(
    *,
    default_prefix: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__584426435c8e1fe53b80bb6669d777a3775afa420766e2ec6a898388413d135a(
    *,
    action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.HttpGatewayRouteActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.HttpGatewayRouteMatchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f834b65b4d3728bd244d982bdd6f2d4fa7220798dadf80dc9ea11d825961f45(
    *,
    hostname: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.GatewayRouteHostnameRewriteProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    path: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.HttpGatewayRoutePathRewriteProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    prefix: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.HttpGatewayRoutePrefixRewriteProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42cff14877bf3df452c9706e1e7971708b48c22ea01ea901df8161e1a32831a9(
    *,
    exact: typing.Optional[builtins.str] = None,
    regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__971737ac4879c289ff9ed417d1943adf958257f470d189cc43b129f6b9302a26(
    *,
    exact: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc61063112ba05ef4237e6e233f26c76679e4526a3d106dc66ebc2dcdde8cee8(
    *,
    match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayRoutePropsMixin.HttpQueryParameterMatchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ede588460c02f14a65d5a08355c1e35f0b9781189d2daf3545d87b338333faa(
    *,
    mesh_name: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMeshPropsMixin.MeshSpecProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38988e149440e331305117981b0163aac32331899fa0dfecdf03d9b6d7639e04(
    props: typing.Union[CfnMeshMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e24d4fc2d18e51dc70aa7fc6a8c9ff2980fcf5eda014d1400112ba7e0baec65d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dad8738b17f3c4d095489e3a2f86f6ce09b943b371fa39a5d83f8b91f5e8f119(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__247c8d72590c3d60b581a988314731c8c3b736fe1a3b39d0c2fe62f020ecaac9(
    *,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__420e85c30af43109e64606d3de454108e54dad7d2405f4e31607248ef6af0656(
    *,
    ip_preference: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada24799cffe2f70dd3ae1a628145539ec1364546be71000b7e5917e51b2d9ec(
    *,
    egress_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMeshPropsMixin.EgressFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_discovery: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMeshPropsMixin.MeshServiceDiscoveryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__380dc81cd3a8ca265e7db3d5907e58d4e8315f6da184eb4b7bac7da49f0c293f(
    *,
    mesh_name: typing.Optional[builtins.str] = None,
    mesh_owner: typing.Optional[builtins.str] = None,
    route_name: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.RouteSpecProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    virtual_router_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ace25a5fbe16cbb365b0c047337a65dc5675b8962d8c3c20dca0a9c43a9320(
    props: typing.Union[CfnRouteMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9840fac11943daaedeed56900f2fa43b14dd85ccc93a3aead15205ebb6a712b2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d6729a0eeead997d1d959ccece17867809b05e964aef02af2439d289fcb3771(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9739fe72b9053b266b9558682b97664b473da34cac8ef11b9e338484d0ca1d7(
    *,
    unit: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__534f2777100a90426395c1c15b0bb009037fbd3d3da2fb4ee0583a74c6ddedb3(
    *,
    grpc_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
    http_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    per_retry_timeout: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.DurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tcp_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9f1b261c2f7ff65b0d808955cd61314656539cac5423c1ee5f7294a2c6bf36(
    *,
    weighted_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.WeightedTargetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba8a6ff32ecb6a4d80e5c960e535f2cff39e99761891fc0469b8fa21cda9ffa6(
    *,
    metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.GrpcRouteMetadataProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    method_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1d8fa3aa5693a918069a8d878364530f46344f45f9fe7425fcd23ac60e24dc(
    *,
    exact: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.MatchRangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    regex: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__856862a2c802347bc125b1593a042f29e5ee7bca46127ac03464c209e8700f81(
    *,
    invert: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.GrpcRouteMetadataMatchMethodProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd126076857fa450bd1ed943a84eb2e5fdb352a5d26cfd11a516e18b06286b57(
    *,
    action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.GrpcRouteActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.GrpcRouteMatchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    retry_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.GrpcRetryPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.GrpcTimeoutProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdc78059caf2e60ddcd161336c6264cce762998af9c2a973f30f7f5192b954f3(
    *,
    idle: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.DurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    per_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.DurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b443f29d591e03dc7e0be1dfb72bff3d845970069e2738f8e64010ed1d44834(
    *,
    exact: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.MatchRangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    regex: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d6d14bf06eeec0d9a61b2e2283c0f869d5ca67287c0c9156321ac2ed1e749f(
    *,
    exact: typing.Optional[builtins.str] = None,
    regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d052604a1bc5ceef83c2701f45eb7a2be1a2c3088484a88104b99e69cc2630e(
    *,
    exact: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2bc3973892b2942553d996dba395c5f93a7a886aed811ac347853b0d444aed5(
    *,
    http_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    per_retry_timeout: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.DurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tcp_retry_events: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0f54fc69b9ec86220a891f774c462e1e7e0d04594529bbe37616c7d98f07110(
    *,
    weighted_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.WeightedTargetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7c00db7ac1357b00f58860b6e568d5c380a7d1b56525356482fe45b023356ee(
    *,
    invert: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.HeaderMatchMethodProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a80a552d6625a1445dd867a171840b3cb800154e27ce1d80c7fbae3b5f2f949(
    *,
    headers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.HttpRouteHeaderProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    method: typing.Optional[builtins.str] = None,
    path: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.HttpPathMatchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    port: typing.Optional[jsii.Number] = None,
    prefix: typing.Optional[builtins.str] = None,
    query_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.QueryParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    scheme: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dea564eab35874062f3d94e97241597f932e139ec844324c45c6d8543f78711(
    *,
    action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.HttpRouteActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.HttpRouteMatchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    retry_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.HttpRetryPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.HttpTimeoutProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f758495b8a7f27ee7f6ad8563c608931255315b4a0e3fff6127d9aae62e6988(
    *,
    idle: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.DurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    per_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.DurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3261160f35311a128618b6756cafb8819443c5d64a2beb7f4acef40b3c0c0d4b(
    *,
    end: typing.Optional[jsii.Number] = None,
    start: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db84a1b5f6eb35537f3ef5ed0a541f82680ef6cca0c3f9005cea5dad447f7518(
    *,
    match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.HttpQueryParameterMatchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__969748cb4ed84b92b91063106557f7f4e4c41321bdaddef6c656de418c47166d(
    *,
    grpc_route: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.GrpcRouteProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    http2_route: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.HttpRouteProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    http_route: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.HttpRouteProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    priority: typing.Optional[jsii.Number] = None,
    tcp_route: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.TcpRouteProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fecabe504f895a904eb8e9f6e7d1680054868f50bd5b11ea58a3ecd0b79e461b(
    *,
    weighted_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.WeightedTargetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a51fb7fd19811ba2edee4d36a69d6ef46c0cb9ef9efb300735ea489feb15445(
    *,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c00c22a2844428260cd1b1d28fb183ce50334852d452105465cb1cf02bf213b(
    *,
    action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.TcpRouteActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.TcpRouteMatchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.TcpTimeoutProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67f687c66c46623faf9d998aa3ca2d481380a1f7c5169511e2fcdf210a1bc4d6(
    *,
    idle: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.DurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca6cdbb43dc4ee6471ec355d819922265e065bf77a6877952325416d2a4fec95(
    *,
    port: typing.Optional[jsii.Number] = None,
    virtual_node: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c092b126e546ab6267aba59fd5f6ab8c5fbf596612a287ef4c82488349ba2d(
    *,
    mesh_name: typing.Optional[builtins.str] = None,
    mesh_owner: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewaySpecProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    virtual_gateway_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b68f06aa5ab5e21d0272579938d90073efddd2b7d6299e8c3a48ddc0a8dea4(
    props: typing.Union[CfnVirtualGatewayMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb6ae3f8cf3281678918935ba2f2cc4203efe503f5b28d18ab8db0fb39cc4b0c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89dc0b6ffb01d584ed4d965d88a3aa08e4e8fc979881255f872a3fa498d6f041(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9dff69307973e6e0f48bd7408eb775f4812b851b059453d76e2a121d6500967(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5b7e949e24c5c302823facaf85aee2c66b846c6d21e0cfbda87b80521f1c872(
    *,
    json: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.JsonFormatRefProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63488c3c35559d285260ece554d163fc761200e9e79aa5edc3c3604934ad7ed0(
    *,
    exact: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe060ac466f802655e1e286fc6ea6aa24f9330e85528b0f978030c67e5633d56(
    *,
    match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.SubjectAlternativeNameMatchersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96a2d0eb43598f42303a9cee3c32bbab4440c2e45d10d721f0aef912d58d9bc(
    *,
    file: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayFileAccessLogProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b25612fffcbf3a43865f982d8fe8d43d4b8a9dae599b604a77baa8c516ad8a8a(
    *,
    client_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayClientPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a17f061547a4deb7a85c30bfb7fd8734db8378d2cf3a4d4fab3a51b72f3f39ad(
    *,
    tls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayClientPolicyTlsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e02956780ee50b7300761df8505f4cc2619e09f0e7aeae077ceac09e3ee8dee(
    *,
    certificate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayClientTlsCertificateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enforce: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ports: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
    validation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef7f08ea3c70dcbeb5aaa0588db8826193653c4a0a04331f83f5325d5047632(
    *,
    file: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsFileCertificateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sds: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsSdsCertificateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a0963aa8130ae3414efb903786c295f5257dabb8f01ec3dea7831957c5a362(
    *,
    grpc: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayGrpcConnectionPoolProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    http: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayHttpConnectionPoolProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    http2: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayHttp2ConnectionPoolProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e69d128d7886283801eb1b9b867c191d16ae1729510ac08df15ae58383904542(
    *,
    format: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.LoggingFormatProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6fe8c8de12c6bac97d6552635118fe68dc1c4e7b2cfc0c02e7d504f0ac26242(
    *,
    max_requests: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0f44b10c062825f1cf6bf3d828678e8a8954e66d99652a2834bcbc3f174a3de(
    *,
    healthy_threshold: typing.Optional[jsii.Number] = None,
    interval_millis: typing.Optional[jsii.Number] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
    timeout_millis: typing.Optional[jsii.Number] = None,
    unhealthy_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__989c903cc0210c67e0f9b3b072f769b8b948b0b1d6cade5c00c17e817de390a7(
    *,
    max_requests: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbc2869b582807a92e57d445e14735218faaf37d7106c5e5d3476f1967b8d24d(
    *,
    max_connections: typing.Optional[jsii.Number] = None,
    max_pending_requests: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bba8b91f0be203864d48e987c3a3f690db144c10dc76c1910fa2452260bb5dd(
    *,
    connection_pool: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayConnectionPoolProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    health_check: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayHealthCheckPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    port_mapping: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayPortMappingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec50e08fcff89f1426a40ac016e2320babb9d09533d19acf309bbdbb194ed0a0(
    *,
    certificate_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d55e039896ad1c1db7bfbdbda0a74d5c21177cc5de6deaabed33f28b2576ff5c(
    *,
    acm: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsAcmCertificateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    file: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsFileCertificateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sds: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsSdsCertificateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8856d353187133ab04e43cab724b298a4eaf52e5d105f148efaa42bad6e1d1e9(
    *,
    certificate_chain: typing.Optional[builtins.str] = None,
    private_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11b4c004cb2a2117b7432d7888157aedcbce57c8de51ff785e42ad1fe57d44d0(
    *,
    certificate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsCertificateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mode: typing.Optional[builtins.str] = None,
    validation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsValidationContextProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7e424ce7cc3b803db8b2a6fe3f7b3f4cf967740d15158c25c8bcff1e65a3534(
    *,
    secret_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c8666942dc61834d2499847d82d3ec219caacac64afa4cf1975c4caf97bd9e(
    *,
    subject_alternative_names: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.SubjectAlternativeNamesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    trust: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayListenerTlsValidationContextTrustProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ea3d358965268381dc1c68035b2b3870d2b1a1db913e25fa19d1e170f287fdb(
    *,
    file: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sds: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5240ecef3695aeecd28e7d86c2cb9a0a2b5600d1aa50b055d23b7d7015f643a(
    *,
    access_log: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayAccessLogProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c2ea7ab18467fe47760390f35dd8530500f232a3881e2c62b93e2fe91896db(
    *,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d90e7d7f3d066c21a06e0fc8fd14366d9d103281156735e706d0ef451359f01(
    *,
    backend_defaults: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayBackendDefaultsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    listeners: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayListenerProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    logging: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayLoggingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59b8bfc6e58191c4517054cc4c6625bedadfe3390464d3ae6e08d9961fe5ce7a(
    *,
    certificate_authority_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b3a53215488a26ea2218229137343873a082fbf03c0a1a8d9525b1d445ffa2f(
    *,
    certificate_chain: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5448d5705f0e09591386f16b13d2358565b55075f71178e23d04b7e096305d87(
    *,
    subject_alternative_names: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.SubjectAlternativeNamesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    trust: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextTrustProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8c011b92c19f87ffbea532f0e3f3b2baad0b2bbc397daccd95c4e8da3da40fc(
    *,
    secret_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d3d25d307ceb9c1c522f83a3c3e2560fc7de837192f45e5f5df395ece7e999e(
    *,
    acm: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextAcmTrustProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    file: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextFileTrustProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sds: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualGatewayPropsMixin.VirtualGatewayTlsValidationContextSdsTrustProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c250c8231c076d8813fc05af396a6b02bfc5651780ab66e786939020f4b15c8(
    *,
    mesh_name: typing.Optional[builtins.str] = None,
    mesh_owner: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.VirtualNodeSpecProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    virtual_node_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe5580f7aa2a4dc20f82281aa6278fdf9c8554786913aee6b4b8a0bc8f5c767e(
    props: typing.Union[CfnVirtualNodeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb9334bdff07c5981e6161ae821521b7cf8dc820e73d94e324cb8d7ab0f310ab(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb2e407202864b10aa5e0ba461e2cf4d3bcb5cef88ca7097855550deababc2b8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a3888e48ad2be64155a9f6c448a252efbf7c7dc9cfaeea935112216f6bb4ea(
    *,
    file: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.FileAccessLogProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ef3cd9d2db477050cfc8000a7cb178d67cb79bd372a69c333f484565c254683(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f0143c1bab6c6f6274125f8bfbfc76be1091a897b7027550514debc042779a3(
    *,
    attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.AwsCloudMapInstanceAttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ip_preference: typing.Optional[builtins.str] = None,
    namespace_name: typing.Optional[builtins.str] = None,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dd7534d6b589caba59b900a64475b823510735c68b6ad654c3c020f9046303d(
    *,
    client_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.ClientPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__548f88788ddf1750033f10b15a8ef9b56cd9c60200ecc2b54fed2a1ce371a334(
    *,
    virtual_service: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.VirtualServiceBackendProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d8c1c33504fcc327c062cc07213644ae1d90f7ac626d6ebf2362368da2c6568(
    *,
    tls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.ClientPolicyTlsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab8a44a9bef26852f33da3725c56e1327362b4c0aab5561d13ca6cbd7d7e8785(
    *,
    certificate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.ClientTlsCertificateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enforce: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ports: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
    validation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.TlsValidationContextProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5de98cba585287eb3247475dc8b6f1b6c2419a1ee83bafa6c00f42d27d1ff2f1(
    *,
    file: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sds: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a07881c1e18cdd403f5968e06d9cbecd212d6b7c8c6b34766fc8cd148df9a4f(
    *,
    hostname: typing.Optional[builtins.str] = None,
    ip_preference: typing.Optional[builtins.str] = None,
    response_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a50646cb43e85fbf3c0e4792d85e1a439f4c2e9be0b147bd576d728a181c8b(
    *,
    unit: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e159e002948d1bce060e9fd8d1830790747e4ba9a78a1ccd3aa866c6bff2eee(
    *,
    format: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.LoggingFormatProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9edd7a465c0661af9f30f3b658c9a929c9af8649a65d26cca281430e137cb70(
    *,
    idle: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.DurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    per_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.DurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2b7c53f4477c10813973da806c68f381d7faa49b8e8237a98a39f0224d3b3bb(
    *,
    healthy_threshold: typing.Optional[jsii.Number] = None,
    interval_millis: typing.Optional[jsii.Number] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
    timeout_millis: typing.Optional[jsii.Number] = None,
    unhealthy_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a348b72c89b283b5562e2526128023dcdc2005b6c22e414229d4a8400c21d5bb(
    *,
    idle: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.DurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    per_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.DurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e19f4234049604dc90ee0187fd04d5563d9dcf21ef61d2d49efba465332e8f7f(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5eebb7cea0b369f30552306a60d6e93f7e3fb93a6902ea5a36f7cc28634be3f(
    *,
    connection_pool: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.VirtualNodeConnectionPoolProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    health_check: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.HealthCheckProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    outlier_detection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.OutlierDetectionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    port_mapping: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.PortMappingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.ListenerTimeoutProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.ListenerTlsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdd5e829e00c02bb52a3441a2aaa71ab53d0babc4cb7212b0109e9da9b875996(
    *,
    grpc: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.GrpcTimeoutProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    http: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.HttpTimeoutProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    http2: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.HttpTimeoutProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tcp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.TcpTimeoutProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16dedb89d53efb87fb4701ae94bdaf782f719aa6df13ac7e6f261d01004b4c64(
    *,
    certificate_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755b6167a2cb65cc0bd0ce2d0c36cda44ccc9514325b1e960254540f6aaccae4(
    *,
    acm: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.ListenerTlsAcmCertificateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    file: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.ListenerTlsFileCertificateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sds: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.ListenerTlsSdsCertificateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fda26973849660276dc0aadaaaa5982ce92bfce0b61d4e5338d92850d4e09c6(
    *,
    certificate_chain: typing.Optional[builtins.str] = None,
    private_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf3a164dadee2d1eba6ae7831e2dad8048ebea0285735b0cea1859a03c531a53(
    *,
    certificate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.ListenerTlsCertificateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mode: typing.Optional[builtins.str] = None,
    validation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.ListenerTlsValidationContextProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f2cfd36495c99b1fb07b2270c98842140d71294550352e5cc2cbbb37d57e367(
    *,
    secret_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__058125a2840f6d0acf72bea68b127ce7af01e5f856ccdfd0aa9eef0ea9d94f54(
    *,
    subject_alternative_names: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    trust: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.ListenerTlsValidationContextTrustProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8136c731899ae5471467d6795fcf20ac1bddf72d8a4fa47b6082cd01dafa9de8(
    *,
    file: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sds: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbcbac3b62e7bd0ec19485dfc978b42db0759833ae1e29676a04aeee88f4a833(
    *,
    json: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.JsonFormatRefProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__053f6923147b7ac5940ee2002f80da49a54fa727fd3d352180584832a14e9248(
    *,
    access_log: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.AccessLogProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c9652d6bea9995dc14f8515c74142c745ef7759682a2622767951cd6abe8f9(
    *,
    base_ejection_duration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.DurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    interval: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.DurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_ejection_percent: typing.Optional[jsii.Number] = None,
    max_server_errors: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bd254efbcb44e81597b3fed0d0cd27e2b1f6a60d5d82776974e2c32cf62dac5(
    *,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71fcc04dd49f4f562593a47e0f52e28d7e66881b9485c1fb19f7bee674007db4(
    *,
    aws_cloud_map: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.AwsCloudMapServiceDiscoveryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.DnsServiceDiscoveryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf9b2b5f9ecb63d0a75aa32c4951472166680b967e18959f752df248b86e02a(
    *,
    exact: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da3d4e162c2cc095302e63a084ede8507ee71766b943115b6aed6af7b996befb(
    *,
    match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.SubjectAlternativeNameMatchersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01b7668a232555df3a102177d7ef4a9cf64642a22785333d0367e6b995254024(
    *,
    idle: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.DurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a87c56e498da1743b8f7411a407f8bfe991a28ba00108cf0ef2f64dc5a573b62(
    *,
    certificate_authority_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc190d3207e1ddf14cce7d79dee1d5fe0139d04b0e9c1abda90f01205644391(
    *,
    certificate_chain: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dda146df1f6a674fb88e311139562f73406d157a4be6cda2f61d735a75fe368(
    *,
    subject_alternative_names: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.SubjectAlternativeNamesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    trust: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.TlsValidationContextTrustProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5d7f14b8780365dccb3cdc22f98b01eab453efb85c8c409d535b70946342b47(
    *,
    secret_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07d5078ef0e58fbee3b4f98e3458e38c4e7b48b36c61fb176960d69222969525(
    *,
    acm: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.TlsValidationContextAcmTrustProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    file: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.TlsValidationContextFileTrustProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sds: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.TlsValidationContextSdsTrustProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb24e7db42da6e9724b4238ccb88def1a8dbb32ebc591bf8650d478926a6b322(
    *,
    grpc: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.VirtualNodeGrpcConnectionPoolProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    http: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.VirtualNodeHttpConnectionPoolProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    http2: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.VirtualNodeHttp2ConnectionPoolProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tcp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.VirtualNodeTcpConnectionPoolProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0265839dc0e096a3378f0a8d9a07c1a8db4e2a05c237558683149b626e0fbaef(
    *,
    max_requests: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7ee245206521f1c337aa2fb4b929bbe2368c619a6d182f19135a14e84aacf0(
    *,
    max_requests: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dfacfdfdc8b4cb46c427e965a4d4fdf9e2da818711acb3d92d39bf17e85b04a(
    *,
    max_connections: typing.Optional[jsii.Number] = None,
    max_pending_requests: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1863a792e2f983eaec81ade4fb248c4a0ed1c0e58b10777364d9b83debda66e5(
    *,
    backend_defaults: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.BackendDefaultsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    backends: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.BackendProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    listeners: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.ListenerProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    logging: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.LoggingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_discovery: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.ServiceDiscoveryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__182338d59e788b351fd353d1dd7c316d217e1c29d8b4e9e88c5d2b689d508866(
    *,
    max_connections: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c32112b4c8a2ba903dbe27bc9bd1f7d6ea1d6b98fb2655d95577c3b396330b2(
    *,
    client_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualNodePropsMixin.ClientPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    virtual_service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a595b16e7cd8bf8e9436ae3980c9ee141c5aab677603b7d065ff474e25af7c61(
    *,
    mesh_name: typing.Optional[builtins.str] = None,
    mesh_owner: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualRouterPropsMixin.VirtualRouterSpecProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    virtual_router_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab04af38a7f62a19bee44b4930093b581f0e2b3b7401f523843e57b9225957d(
    props: typing.Union[CfnVirtualRouterMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca4c93b9912edb5c5158d1f429f2dba997367fb1684cc84ef7f8daccf6e0f5d0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e96a0351035f92ea7fb60f40f166805c883d21093f07d0eb2a5a6ec1f6aae55(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84e7b62fbf4c03585700db4f1e44ebba7b05b55fd5c222b3913b9168cd21dae(
    *,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__812b8813375dd859e8f0f59abd164bedda015ed063a0753c709b9c8a22c75ef2(
    *,
    port_mapping: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualRouterPropsMixin.PortMappingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e413f421ca0e50e0216acbe5a0d2ce6f35a8a34dcc4084df9f91f0644db8dc7(
    *,
    listeners: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualRouterPropsMixin.VirtualRouterListenerProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb2c9298fd70af0858babd344a2b0c2bec0ae89da72ebe047e4592fbccc4553(
    *,
    mesh_name: typing.Optional[builtins.str] = None,
    mesh_owner: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualServicePropsMixin.VirtualServiceSpecProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    virtual_service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb4325b60f38642b60a1e817bed8bafda6f50433581ba3a41af3a67c7e64bf1(
    props: typing.Union[CfnVirtualServiceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9123da1f0ab9e6677ef25f534b123a6613d865f73afd2b601ccb7e55c8d1d276(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e905390e403a68f721dc363874e289649da512f8f1e872e2e2dc8fbf19a6f21d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d99663d983371bad9dcfe52da0008d316513d6fa3729b81a59c7c3791093af8(
    *,
    virtual_node_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe6dd7278b8e2cec7d1efa1a75c8f19d8534178a4e7acea5d64490d127a78631(
    *,
    virtual_router_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23542b92f04ad7e97ecb6b97a5241087151123d2e644021c0ed249a42fc911b9(
    *,
    virtual_node: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualServicePropsMixin.VirtualNodeServiceProviderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    virtual_router: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualServicePropsMixin.VirtualRouterServiceProviderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76de5b0b7090fde3fb95e5397ced62c0b3c22ed2bf15c4a589dc73c40c228fab(
    *,
    provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVirtualServicePropsMixin.VirtualServiceProviderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
