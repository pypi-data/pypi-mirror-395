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
    jsii_type="@aws-cdk/mixins-preview.aws_refactorspaces.mixins.CfnApplicationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_gateway_proxy": "apiGatewayProxy",
        "environment_identifier": "environmentIdentifier",
        "name": "name",
        "proxy_type": "proxyType",
        "tags": "tags",
        "vpc_id": "vpcId",
    },
)
class CfnApplicationMixinProps:
    def __init__(
        self,
        *,
        api_gateway_proxy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ApiGatewayProxyInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        environment_identifier: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        proxy_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnApplicationPropsMixin.

        :param api_gateway_proxy: The endpoint URL of the Amazon API Gateway proxy.
        :param environment_identifier: The unique identifier of the environment.
        :param name: The name of the application.
        :param proxy_type: The proxy type of the proxy created within the application.
        :param tags: The tags assigned to the application.
        :param vpc_id: The ID of the virtual private cloud (VPC).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_refactorspaces import mixins as refactorspaces_mixins
            
            cfn_application_mixin_props = refactorspaces_mixins.CfnApplicationMixinProps(
                api_gateway_proxy=refactorspaces_mixins.CfnApplicationPropsMixin.ApiGatewayProxyInputProperty(
                    endpoint_type="endpointType",
                    stage_name="stageName"
                ),
                environment_identifier="environmentIdentifier",
                name="name",
                proxy_type="proxyType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_id="vpcId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca698f3824463234452e90c49556308de726dbe3151eea0e29ca88aaa145c635)
            check_type(argname="argument api_gateway_proxy", value=api_gateway_proxy, expected_type=type_hints["api_gateway_proxy"])
            check_type(argname="argument environment_identifier", value=environment_identifier, expected_type=type_hints["environment_identifier"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument proxy_type", value=proxy_type, expected_type=type_hints["proxy_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_gateway_proxy is not None:
            self._values["api_gateway_proxy"] = api_gateway_proxy
        if environment_identifier is not None:
            self._values["environment_identifier"] = environment_identifier
        if name is not None:
            self._values["name"] = name
        if proxy_type is not None:
            self._values["proxy_type"] = proxy_type
        if tags is not None:
            self._values["tags"] = tags
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def api_gateway_proxy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApiGatewayProxyInputProperty"]]:
        '''The endpoint URL of the Amazon API Gateway proxy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-apigatewayproxy
        '''
        result = self._values.get("api_gateway_proxy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApiGatewayProxyInputProperty"]], result)

    @builtins.property
    def environment_identifier(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-environmentidentifier
        '''
        result = self._values.get("environment_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_type(self) -> typing.Optional[builtins.str]:
        '''The proxy type of the proxy created within the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-proxytype
        '''
        result = self._values.get("proxy_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags assigned to the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the virtual private cloud (VPC).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-vpcid
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_refactorspaces.mixins.CfnApplicationPropsMixin",
):
    '''.. epigraph::

   AWS Migration Hub is no longer open to new customers as of November 7, 2025.

    For capabilities similar to AWS Migration Hub , explore `AWS Migration Hub <https://docs.aws.amazon.com/https://aws.amazon.com/transform>`_ .

    Creates an AWS Migration Hub Refactor Spaces application. The account that owns the environment also owns the applications created inside the environment, regardless of the account that creates the application. Refactor Spaces provisions an Amazon API Gateway, API Gateway VPC link, and Network Load Balancer for the application proxy inside your account.

    In environments created with a `CreateEnvironment:NetworkFabricType <https://docs.aws.amazon.com/migrationhub-refactor-spaces/latest/APIReference/API_CreateEnvironment.html#migrationhubrefactorspaces-CreateEnvironment-request-NetworkFabricType>`_ of ``NONE`` you need to configure `VPC to VPC connectivity <https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/amazon-vpc-to-amazon-vpc-connectivity-options.html>`_ between your service VPC and the application proxy VPC to route traffic through the application proxy to a service with a private URL endpoint. For more information, see `Create an application <https://docs.aws.amazon.com/migrationhub-refactor-spaces/latest/userguide/getting-started-create-application.html>`_ in the *Refactor Spaces User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html
    :cloudformationResource: AWS::RefactorSpaces::Application
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_refactorspaces import mixins as refactorspaces_mixins
        
        cfn_application_props_mixin = refactorspaces_mixins.CfnApplicationPropsMixin(refactorspaces_mixins.CfnApplicationMixinProps(
            api_gateway_proxy=refactorspaces_mixins.CfnApplicationPropsMixin.ApiGatewayProxyInputProperty(
                endpoint_type="endpointType",
                stage_name="stageName"
            ),
            environment_identifier="environmentIdentifier",
            name="name",
            proxy_type="proxyType",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_id="vpcId"
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
        '''Create a mixin to apply properties to ``AWS::RefactorSpaces::Application``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d2b1e5e0c23bd2a16bb27c02080552710bf102efdce77588a84b37d3ebfcb8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca9c065a673d37daea04c97f86c8b28cc04264d76dcd62497201bd7b0af3b69b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b7c000b1593e859f681df2d410c1a1310f59bb472f741659f6efa91ed7bc537)
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
        jsii_type="@aws-cdk/mixins-preview.aws_refactorspaces.mixins.CfnApplicationPropsMixin.ApiGatewayProxyInputProperty",
        jsii_struct_bases=[],
        name_mapping={"endpoint_type": "endpointType", "stage_name": "stageName"},
    )
    class ApiGatewayProxyInputProperty:
        def __init__(
            self,
            *,
            endpoint_type: typing.Optional[builtins.str] = None,
            stage_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A wrapper object holding the Amazon API Gateway endpoint input.

            :param endpoint_type: The type of endpoint to use for the API Gateway proxy. If no value is specified in the request, the value is set to ``REGIONAL`` by default. If the value is set to ``PRIVATE`` in the request, this creates a private API endpoint that is isolated from the public internet. The private endpoint can only be accessed by using Amazon Virtual Private Cloud (Amazon VPC) interface endpoints for the Amazon API Gateway that has been granted access. For more information about creating a private connection with Refactor Spaces and interface endpoint ( AWS PrivateLink ) availability, see `Access Refactor Spaces using an interface endpoint ( AWS PrivateLink ) <https://docs.aws.amazon.com/migrationhub-refactor-spaces/latest/userguide/vpc-interface-endpoints.html>`_ .
            :param stage_name: The name of the API Gateway stage. The name defaults to ``prod`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-application-apigatewayproxyinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_refactorspaces import mixins as refactorspaces_mixins
                
                api_gateway_proxy_input_property = refactorspaces_mixins.CfnApplicationPropsMixin.ApiGatewayProxyInputProperty(
                    endpoint_type="endpointType",
                    stage_name="stageName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2ae354ff68eba0398cf39d38cc2ea4e41fbe9c17cfc9d74331da550fec92412e)
                check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
                check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if endpoint_type is not None:
                self._values["endpoint_type"] = endpoint_type
            if stage_name is not None:
                self._values["stage_name"] = stage_name

        @builtins.property
        def endpoint_type(self) -> typing.Optional[builtins.str]:
            '''The type of endpoint to use for the API Gateway proxy.

            If no value is specified in the request, the value is set to ``REGIONAL`` by default.

            If the value is set to ``PRIVATE`` in the request, this creates a private API endpoint that is isolated from the public internet. The private endpoint can only be accessed by using Amazon Virtual Private Cloud (Amazon VPC) interface endpoints for the Amazon API Gateway that has been granted access. For more information about creating a private connection with Refactor Spaces and interface endpoint ( AWS PrivateLink ) availability, see `Access Refactor Spaces using an interface endpoint ( AWS PrivateLink ) <https://docs.aws.amazon.com/migrationhub-refactor-spaces/latest/userguide/vpc-interface-endpoints.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-application-apigatewayproxyinput.html#cfn-refactorspaces-application-apigatewayproxyinput-endpointtype
            '''
            result = self._values.get("endpoint_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stage_name(self) -> typing.Optional[builtins.str]:
            '''The name of the API Gateway stage.

            The name defaults to ``prod`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-application-apigatewayproxyinput.html#cfn-refactorspaces-application-apigatewayproxyinput-stagename
            '''
            result = self._values.get("stage_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApiGatewayProxyInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_refactorspaces.mixins.CfnEnvironmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "network_fabric_type": "networkFabricType",
        "tags": "tags",
    },
)
class CfnEnvironmentMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        network_fabric_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnEnvironmentPropsMixin.

        :param description: A description of the environment.
        :param name: The name of the environment.
        :param network_fabric_type: The network fabric type of the environment.
        :param tags: The tags assigned to the environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_refactorspaces import mixins as refactorspaces_mixins
            
            cfn_environment_mixin_props = refactorspaces_mixins.CfnEnvironmentMixinProps(
                description="description",
                name="name",
                network_fabric_type="networkFabricType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a54b6e9a3052f94febdfb3bc575742ecaf318607570fcf6835312f3ec4a75bab)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_fabric_type", value=network_fabric_type, expected_type=type_hints["network_fabric_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if network_fabric_type is not None:
            self._values["network_fabric_type"] = network_fabric_type
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html#cfn-refactorspaces-environment-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html#cfn-refactorspaces-environment-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_fabric_type(self) -> typing.Optional[builtins.str]:
        '''The network fabric type of the environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html#cfn-refactorspaces-environment-networkfabrictype
        '''
        result = self._values.get("network_fabric_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags assigned to the environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html#cfn-refactorspaces-environment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnvironmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEnvironmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_refactorspaces.mixins.CfnEnvironmentPropsMixin",
):
    '''.. epigraph::

   AWS Migration Hub is no longer open to new customers as of November 7, 2025.

    For capabilities similar to AWS Migration Hub , explore `AWS Migration Hub <https://docs.aws.amazon.com/https://aws.amazon.com/transform>`_ .

    Creates an AWS Migration Hub Refactor Spaces environment. The caller owns the environment resource, and all Refactor Spaces applications, services, and routes created within the environment. They are referred to as the *environment owner* . The environment owner has cross-account visibility and control of Refactor Spaces resources that are added to the environment by other accounts that the environment is shared with.

    When creating an environment with a `CreateEnvironment:NetworkFabricType <https://docs.aws.amazon.com/migrationhub-refactor-spaces/latest/APIReference/API_CreateEnvironment.html#migrationhubrefactorspaces-CreateEnvironment-request-NetworkFabricType>`_ of ``TRANSIT_GATEWAY`` , Refactor Spaces provisions a transit gateway to enable services in VPCs to communicate directly across accounts. If `CreateEnvironment:NetworkFabricType <https://docs.aws.amazon.com/migrationhub-refactor-spaces/latest/APIReference/API_CreateEnvironment.html#migrationhubrefactorspaces-CreateEnvironment-request-NetworkFabricType>`_ is ``NONE`` , Refactor Spaces does not create a transit gateway and you must use your network infrastructure to route traffic to services with private URL endpoints.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html
    :cloudformationResource: AWS::RefactorSpaces::Environment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_refactorspaces import mixins as refactorspaces_mixins
        
        cfn_environment_props_mixin = refactorspaces_mixins.CfnEnvironmentPropsMixin(refactorspaces_mixins.CfnEnvironmentMixinProps(
            description="description",
            name="name",
            network_fabric_type="networkFabricType",
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
        props: typing.Union[CfnEnvironmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RefactorSpaces::Environment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01e87d1877d27e444a3b51ff976de9c963e4c47d009ace6698dc5a65f11c0b9f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__75e579d4004783413400e5d76e005d21d09df4854050f6d032b1f5ca1baf1b7f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b5435737e658d1c009e0ca54aff4d0ddc920a2ac1cd10dc9145b41efbf327a7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEnvironmentMixinProps:
        return typing.cast(CfnEnvironmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_refactorspaces.mixins.CfnRouteMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_identifier": "applicationIdentifier",
        "default_route": "defaultRoute",
        "environment_identifier": "environmentIdentifier",
        "route_type": "routeType",
        "service_identifier": "serviceIdentifier",
        "tags": "tags",
        "uri_path_route": "uriPathRoute",
    },
)
class CfnRouteMixinProps:
    def __init__(
        self,
        *,
        application_identifier: typing.Optional[builtins.str] = None,
        default_route: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.DefaultRouteInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        environment_identifier: typing.Optional[builtins.str] = None,
        route_type: typing.Optional[builtins.str] = None,
        service_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        uri_path_route: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutePropsMixin.UriPathRouteInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnRoutePropsMixin.

        :param application_identifier: The unique identifier of the application.
        :param default_route: Configuration for the default route type.
        :param environment_identifier: The unique identifier of the environment.
        :param route_type: The route type of the route.
        :param service_identifier: The unique identifier of the service.
        :param tags: The tags assigned to the route.
        :param uri_path_route: The configuration for the URI path route type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_refactorspaces import mixins as refactorspaces_mixins
            
            cfn_route_mixin_props = refactorspaces_mixins.CfnRouteMixinProps(
                application_identifier="applicationIdentifier",
                default_route=refactorspaces_mixins.CfnRoutePropsMixin.DefaultRouteInputProperty(
                    activation_state="activationState"
                ),
                environment_identifier="environmentIdentifier",
                route_type="routeType",
                service_identifier="serviceIdentifier",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                uri_path_route=refactorspaces_mixins.CfnRoutePropsMixin.UriPathRouteInputProperty(
                    activation_state="activationState",
                    append_source_path=False,
                    include_child_paths=False,
                    methods=["methods"],
                    source_path="sourcePath"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00896d4603a1518abbe80cd940c296a7cd661d76cbcf155b7eec10973deb9e98)
            check_type(argname="argument application_identifier", value=application_identifier, expected_type=type_hints["application_identifier"])
            check_type(argname="argument default_route", value=default_route, expected_type=type_hints["default_route"])
            check_type(argname="argument environment_identifier", value=environment_identifier, expected_type=type_hints["environment_identifier"])
            check_type(argname="argument route_type", value=route_type, expected_type=type_hints["route_type"])
            check_type(argname="argument service_identifier", value=service_identifier, expected_type=type_hints["service_identifier"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument uri_path_route", value=uri_path_route, expected_type=type_hints["uri_path_route"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_identifier is not None:
            self._values["application_identifier"] = application_identifier
        if default_route is not None:
            self._values["default_route"] = default_route
        if environment_identifier is not None:
            self._values["environment_identifier"] = environment_identifier
        if route_type is not None:
            self._values["route_type"] = route_type
        if service_identifier is not None:
            self._values["service_identifier"] = service_identifier
        if tags is not None:
            self._values["tags"] = tags
        if uri_path_route is not None:
            self._values["uri_path_route"] = uri_path_route

    @builtins.property
    def application_identifier(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-applicationidentifier
        '''
        result = self._values.get("application_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_route(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.DefaultRouteInputProperty"]]:
        '''Configuration for the default route type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-defaultroute
        '''
        result = self._values.get("default_route")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.DefaultRouteInputProperty"]], result)

    @builtins.property
    def environment_identifier(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-environmentidentifier
        '''
        result = self._values.get("environment_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route_type(self) -> typing.Optional[builtins.str]:
        '''The route type of the route.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-routetype
        '''
        result = self._values.get("route_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_identifier(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-serviceidentifier
        '''
        result = self._values.get("service_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags assigned to the route.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def uri_path_route(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.UriPathRouteInputProperty"]]:
        '''The configuration for the URI path route type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-uripathroute
        '''
        result = self._values.get("uri_path_route")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutePropsMixin.UriPathRouteInputProperty"]], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_refactorspaces.mixins.CfnRoutePropsMixin",
):
    '''Creates an AWS Migration Hub Refactor Spaces route.

    The account owner of the service resource is always the environment owner, regardless of which account creates the route. Routes target a service in the application. If an application does not have any routes, then the first route must be created as a ``DEFAULT`` ``RouteType`` .

    When created, the default route defaults to an active state so state is not a required input. However, like all other state values the state of the default route can be updated after creation, but only when all other routes are also inactive. Conversely, no route can be active without the default route also being active.
    .. epigraph::

       In the ``AWS::RefactorSpaces::Route`` resource, you can only update the ``ActivationState`` property, which resides under the ``UriPathRoute`` and ``DefaultRoute`` properties. All other properties associated with the ``AWS::RefactorSpaces::Route`` cannot be updated, even though the property description might indicate otherwise. Updating all other properties will result in the replacement of Route.

    When you create a route, Refactor Spaces configures the ABPlong to send traffic to the target service as follows:

    - *URL Endpoints*

    If the service has a URL endpoint, and the endpoint resolves to a private IP address, Refactor Spaces routes traffic using the ABP VPC link. If a service endpoint resolves to a public IP address, Refactor Spaces routes traffic over the public internet. Services can have HTTP or HTTPS URL endpoints. For HTTPS URLs, publicly-signed certificates are supported. Private Certificate Authorities (CAs) are permitted only if the CA's domain is also publicly resolvable.

    Refactor Spaces automatically resolves the public Domain Name System (DNS) names that are set in ``CreateService:UrlEndpoint`` when you create a service. The DNS names resolve when the DNS time-to-live (TTL) expires, or every 60 seconds for TTLs less than 60 seconds. This periodic DNS resolution ensures that the route configuration remains up-to-date.

    *One-time health check*

    A one-time health check is performed on the service when either the route is updated from inactive to active, or when it is created with an active state. If the health check fails, the route transitions the route state to ``FAILED`` , an error code of ``SERVICE_ENDPOINT_HEALTH_CHECK_FAILURE`` is provided, and no traffic is sent to the service.

    For private URLs, a target group is created on the Network Load Balancer and the load balancer target group runs default target health checks. By default, the health check is run against the service endpoint URL. Optionally, the health check can be performed against a different protocol, port, and/or path using the `CreateService:UrlEndpoint <https://docs.aws.amazon.com/migrationhub-refactor-spaces/latest/APIReference/API_CreateService.html#migrationhubrefactorspaces-CreateService-request-UrlEndpoint>`_ parameter. All other health check settings for the load balancer use the default values described in the `Health checks for your target groups <https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html>`_ in the *ELB guide* . The health check is considered successful if at least one target within the target group transitions to a healthy state.

    - *AWS Lambda function endpoints*

    If the service has an AWS Lambda function endpoint, then Refactor Spaces configures the Lambda function's resource policy to allow the application's ABP to invoke the function.

    The Lambda function state is checked. If the function is not active, the function configuration is updated so that Lambda resources are provisioned. If the Lambda state is ``Failed`` , then the route creation fails. For more information, see the `GetFunctionConfiguration's State response parameter <https://docs.aws.amazon.com/lambda/latest/dg/API_GetFunctionConfiguration.html#SSS-GetFunctionConfiguration-response-State>`_ in the *AWS Lambda Developer Guide* .

    A check is performed to determine that a Lambda function with the specified ARN exists. If it does not exist, the health check fails. For public URLs, a connection is opened to the public endpoint. If the URL is not reachable, the health check fails.

    *Environments without a network bridge*

    When you create environments without a network bridge ( `CreateEnvironment:NetworkFabricType <https://docs.aws.amazon.com/migrationhub-refactor-spaces/latest/APIReference/API_CreateEnvironment.html#migrationhubrefactorspaces-CreateEnvironment-request-NetworkFabricType>`_ is ``NONE)`` and you use your own networking infrastructure, you need to configure `VPC to VPC connectivity <https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/amazon-vpc-to-amazon-vpc-connectivity-options.html>`_ between your network and the application proxy VPC. Route creation from the application proxy to service endpoints will fail if your network is not configured to connect to the application proxy VPC. For more information, see `Create a route <https://docs.aws.amazon.com/migrationhub-refactor-spaces/latest/userguide/getting-started-create-role.html>`_ in the *Refactor Spaces User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html
    :cloudformationResource: AWS::RefactorSpaces::Route
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_refactorspaces import mixins as refactorspaces_mixins
        
        cfn_route_props_mixin = refactorspaces_mixins.CfnRoutePropsMixin(refactorspaces_mixins.CfnRouteMixinProps(
            application_identifier="applicationIdentifier",
            default_route=refactorspaces_mixins.CfnRoutePropsMixin.DefaultRouteInputProperty(
                activation_state="activationState"
            ),
            environment_identifier="environmentIdentifier",
            route_type="routeType",
            service_identifier="serviceIdentifier",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            uri_path_route=refactorspaces_mixins.CfnRoutePropsMixin.UriPathRouteInputProperty(
                activation_state="activationState",
                append_source_path=False,
                include_child_paths=False,
                methods=["methods"],
                source_path="sourcePath"
            )
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
        '''Create a mixin to apply properties to ``AWS::RefactorSpaces::Route``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1326061d5d1ef25f87757b65fe8a8c1f7cfe4e0832d27daa1e771e2ced046c91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55435390f1f0ba3639ff252d2589d1b92d5c93343b33cdb1cfb809e6645a90e3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deb8900b0c714d0881be8130ea1bd0fb327191a59070df81d117e70742f17088)
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
        jsii_type="@aws-cdk/mixins-preview.aws_refactorspaces.mixins.CfnRoutePropsMixin.DefaultRouteInputProperty",
        jsii_struct_bases=[],
        name_mapping={"activation_state": "activationState"},
    )
    class DefaultRouteInputProperty:
        def __init__(
            self,
            *,
            activation_state: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for the default route type.

            :param activation_state: If set to ``ACTIVE`` , traffic is forwarded to this route’s service after the route is created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-route-defaultrouteinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_refactorspaces import mixins as refactorspaces_mixins
                
                default_route_input_property = refactorspaces_mixins.CfnRoutePropsMixin.DefaultRouteInputProperty(
                    activation_state="activationState"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f8e1d2621eb3450a3ba1d1b90a2234003317a345101490973f43649bb48713dd)
                check_type(argname="argument activation_state", value=activation_state, expected_type=type_hints["activation_state"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if activation_state is not None:
                self._values["activation_state"] = activation_state

        @builtins.property
        def activation_state(self) -> typing.Optional[builtins.str]:
            '''If set to ``ACTIVE`` , traffic is forwarded to this route’s service after the route is created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-route-defaultrouteinput.html#cfn-refactorspaces-route-defaultrouteinput-activationstate
            '''
            result = self._values.get("activation_state")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultRouteInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_refactorspaces.mixins.CfnRoutePropsMixin.UriPathRouteInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "activation_state": "activationState",
            "append_source_path": "appendSourcePath",
            "include_child_paths": "includeChildPaths",
            "methods": "methods",
            "source_path": "sourcePath",
        },
    )
    class UriPathRouteInputProperty:
        def __init__(
            self,
            *,
            activation_state: typing.Optional[builtins.str] = None,
            append_source_path: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_child_paths: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            methods: typing.Optional[typing.Sequence[builtins.str]] = None,
            source_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for the URI path route type.

            :param activation_state: If set to ``ACTIVE`` , traffic is forwarded to this route’s service after the route is created.
            :param append_source_path: If set to ``true`` , this option appends the source path to the service URL endpoint.
            :param include_child_paths: Indicates whether to match all subpaths of the given source path. If this value is ``false`` , requests must match the source path exactly before they are forwarded to this route's service.
            :param methods: A list of HTTP methods to match. An empty list matches all values. If a method is present, only HTTP requests using that method are forwarded to this route’s service.
            :param source_path: This is the path that Refactor Spaces uses to match traffic. Paths must start with ``/`` and are relative to the base of the application. To use path parameters in the source path, add a variable in curly braces. For example, the resource path {user} represents a path parameter called 'user'.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-route-uripathrouteinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_refactorspaces import mixins as refactorspaces_mixins
                
                uri_path_route_input_property = refactorspaces_mixins.CfnRoutePropsMixin.UriPathRouteInputProperty(
                    activation_state="activationState",
                    append_source_path=False,
                    include_child_paths=False,
                    methods=["methods"],
                    source_path="sourcePath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__82145f22e05c81b9c15c298471eb3118697a6e56cd9ef3615e068f6e5b5372f7)
                check_type(argname="argument activation_state", value=activation_state, expected_type=type_hints["activation_state"])
                check_type(argname="argument append_source_path", value=append_source_path, expected_type=type_hints["append_source_path"])
                check_type(argname="argument include_child_paths", value=include_child_paths, expected_type=type_hints["include_child_paths"])
                check_type(argname="argument methods", value=methods, expected_type=type_hints["methods"])
                check_type(argname="argument source_path", value=source_path, expected_type=type_hints["source_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if activation_state is not None:
                self._values["activation_state"] = activation_state
            if append_source_path is not None:
                self._values["append_source_path"] = append_source_path
            if include_child_paths is not None:
                self._values["include_child_paths"] = include_child_paths
            if methods is not None:
                self._values["methods"] = methods
            if source_path is not None:
                self._values["source_path"] = source_path

        @builtins.property
        def activation_state(self) -> typing.Optional[builtins.str]:
            '''If set to ``ACTIVE`` , traffic is forwarded to this route’s service after the route is created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-route-uripathrouteinput.html#cfn-refactorspaces-route-uripathrouteinput-activationstate
            '''
            result = self._values.get("activation_state")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def append_source_path(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If set to ``true`` , this option appends the source path to the service URL endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-route-uripathrouteinput.html#cfn-refactorspaces-route-uripathrouteinput-appendsourcepath
            '''
            result = self._values.get("append_source_path")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_child_paths(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether to match all subpaths of the given source path.

            If this value is ``false`` , requests must match the source path exactly before they are forwarded to this route's service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-route-uripathrouteinput.html#cfn-refactorspaces-route-uripathrouteinput-includechildpaths
            '''
            result = self._values.get("include_child_paths")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def methods(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of HTTP methods to match.

            An empty list matches all values. If a method is present, only HTTP requests using that method are forwarded to this route’s service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-route-uripathrouteinput.html#cfn-refactorspaces-route-uripathrouteinput-methods
            '''
            result = self._values.get("methods")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def source_path(self) -> typing.Optional[builtins.str]:
            '''This is the path that Refactor Spaces uses to match traffic.

            Paths must start with ``/`` and are relative to the base of the application. To use path parameters in the source path, add a variable in curly braces. For example, the resource path {user} represents a path parameter called 'user'.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-route-uripathrouteinput.html#cfn-refactorspaces-route-uripathrouteinput-sourcepath
            '''
            result = self._values.get("source_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UriPathRouteInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_refactorspaces.mixins.CfnServiceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_identifier": "applicationIdentifier",
        "description": "description",
        "endpoint_type": "endpointType",
        "environment_identifier": "environmentIdentifier",
        "lambda_endpoint": "lambdaEndpoint",
        "name": "name",
        "tags": "tags",
        "url_endpoint": "urlEndpoint",
        "vpc_id": "vpcId",
    },
)
class CfnServiceMixinProps:
    def __init__(
        self,
        *,
        application_identifier: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        endpoint_type: typing.Optional[builtins.str] = None,
        environment_identifier: typing.Optional[builtins.str] = None,
        lambda_endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.LambdaEndpointInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        url_endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.UrlEndpointInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnServicePropsMixin.

        :param application_identifier: The unique identifier of the application.
        :param description: A description of the service.
        :param endpoint_type: The endpoint type of the service.
        :param environment_identifier: The unique identifier of the environment.
        :param lambda_endpoint: A summary of the configuration for the AWS Lambda endpoint type.
        :param name: The name of the service.
        :param tags: The tags assigned to the service.
        :param url_endpoint: The summary of the configuration for the URL endpoint type.
        :param vpc_id: The ID of the virtual private cloud (VPC).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_refactorspaces import mixins as refactorspaces_mixins
            
            cfn_service_mixin_props = refactorspaces_mixins.CfnServiceMixinProps(
                application_identifier="applicationIdentifier",
                description="description",
                endpoint_type="endpointType",
                environment_identifier="environmentIdentifier",
                lambda_endpoint=refactorspaces_mixins.CfnServicePropsMixin.LambdaEndpointInputProperty(
                    arn="arn"
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                url_endpoint=refactorspaces_mixins.CfnServicePropsMixin.UrlEndpointInputProperty(
                    health_url="healthUrl",
                    url="url"
                ),
                vpc_id="vpcId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__922a97ef04b3346fd165d59712a6bf425c4ce2f95ffbecc8eed2f2d5aaecfaae)
            check_type(argname="argument application_identifier", value=application_identifier, expected_type=type_hints["application_identifier"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
            check_type(argname="argument environment_identifier", value=environment_identifier, expected_type=type_hints["environment_identifier"])
            check_type(argname="argument lambda_endpoint", value=lambda_endpoint, expected_type=type_hints["lambda_endpoint"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument url_endpoint", value=url_endpoint, expected_type=type_hints["url_endpoint"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_identifier is not None:
            self._values["application_identifier"] = application_identifier
        if description is not None:
            self._values["description"] = description
        if endpoint_type is not None:
            self._values["endpoint_type"] = endpoint_type
        if environment_identifier is not None:
            self._values["environment_identifier"] = environment_identifier
        if lambda_endpoint is not None:
            self._values["lambda_endpoint"] = lambda_endpoint
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if url_endpoint is not None:
            self._values["url_endpoint"] = url_endpoint
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def application_identifier(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-applicationidentifier
        '''
        result = self._values.get("application_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_type(self) -> typing.Optional[builtins.str]:
        '''The endpoint type of the service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-endpointtype
        '''
        result = self._values.get("endpoint_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_identifier(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-environmentidentifier
        '''
        result = self._values.get("environment_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lambda_endpoint(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.LambdaEndpointInputProperty"]]:
        '''A summary of the configuration for the AWS Lambda endpoint type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-lambdaendpoint
        '''
        result = self._values.get("lambda_endpoint")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.LambdaEndpointInputProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags assigned to the service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def url_endpoint(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.UrlEndpointInputProperty"]]:
        '''The summary of the configuration for the URL endpoint type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-urlendpoint
        '''
        result = self._values.get("url_endpoint")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.UrlEndpointInputProperty"]], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the virtual private cloud (VPC).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-vpcid
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnServicePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_refactorspaces.mixins.CfnServicePropsMixin",
):
    '''.. epigraph::

   AWS Migration Hub is no longer open to new customers as of November 7, 2025.

    For capabilities similar to AWS Migration Hub , explore `AWS Migration Hub <https://docs.aws.amazon.com/https://aws.amazon.com/transform>`_ .

    Creates an AWS Migration Hub Refactor Spaces service. The account owner of the service is always the environment owner, regardless of which account in the environment creates the service. Services have either a URL endpoint in a virtual private cloud (VPC), or a Lambda function endpoint.
    .. epigraph::

       If an AWS resource is launched in a service VPC, and you want it to be accessible to all of an environment’s services with VPCs and routes, apply the ``RefactorSpacesSecurityGroup`` to the resource. Alternatively, to add more cross-account constraints, apply your own security group.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html
    :cloudformationResource: AWS::RefactorSpaces::Service
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_refactorspaces import mixins as refactorspaces_mixins
        
        cfn_service_props_mixin = refactorspaces_mixins.CfnServicePropsMixin(refactorspaces_mixins.CfnServiceMixinProps(
            application_identifier="applicationIdentifier",
            description="description",
            endpoint_type="endpointType",
            environment_identifier="environmentIdentifier",
            lambda_endpoint=refactorspaces_mixins.CfnServicePropsMixin.LambdaEndpointInputProperty(
                arn="arn"
            ),
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            url_endpoint=refactorspaces_mixins.CfnServicePropsMixin.UrlEndpointInputProperty(
                health_url="healthUrl",
                url="url"
            ),
            vpc_id="vpcId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnServiceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RefactorSpaces::Service``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__185ca92dbc70fa6c8117982f863c98be20b2a0217178c81113c2dd1ccf59d7b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c86af025e5286795d1f25e4d6f930c677a78ce0ba3e54e39711348c48b44f9bd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__321a7611a080383b99ab8c598908130b1307e9bbcf8d244a4648784659fd7f64)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnServiceMixinProps:
        return typing.cast(CfnServiceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_refactorspaces.mixins.CfnServicePropsMixin.LambdaEndpointInputProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class LambdaEndpointInputProperty:
        def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
            '''The input for the AWS Lambda endpoint type.

            :param arn: The Amazon Resource Name (ARN) of the Lambda function or alias.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-service-lambdaendpointinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_refactorspaces import mixins as refactorspaces_mixins
                
                lambda_endpoint_input_property = refactorspaces_mixins.CfnServicePropsMixin.LambdaEndpointInputProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__571a2b8ae9113c393910d8ee1e8b25db5d8490b78ef21eda8fc2a0a40233886e)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Lambda function or alias.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-service-lambdaendpointinput.html#cfn-refactorspaces-service-lambdaendpointinput-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaEndpointInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_refactorspaces.mixins.CfnServicePropsMixin.UrlEndpointInputProperty",
        jsii_struct_bases=[],
        name_mapping={"health_url": "healthUrl", "url": "url"},
    )
    class UrlEndpointInputProperty:
        def __init__(
            self,
            *,
            health_url: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for the URL endpoint type.

            :param health_url: The health check URL of the URL endpoint type. If the URL is a public endpoint, the ``HealthUrl`` must also be a public endpoint. If the URL is a private endpoint inside a virtual private cloud (VPC), the health URL must also be a private endpoint, and the host must be the same as the URL.
            :param url: The URL to route traffic to. The URL must be an `rfc3986-formatted URL <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc3986>`_ . If the host is a domain name, the name must be resolvable over the public internet. If the scheme is ``https`` , the top level domain of the host must be listed in the `IANA root zone database <https://docs.aws.amazon.com/https://www.iana.org/domains/root/db>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-service-urlendpointinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_refactorspaces import mixins as refactorspaces_mixins
                
                url_endpoint_input_property = refactorspaces_mixins.CfnServicePropsMixin.UrlEndpointInputProperty(
                    health_url="healthUrl",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__816621a92358e17c503e06ec561d87d49b1149f2e0cd2521a0693e6e7e52211b)
                check_type(argname="argument health_url", value=health_url, expected_type=type_hints["health_url"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if health_url is not None:
                self._values["health_url"] = health_url
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def health_url(self) -> typing.Optional[builtins.str]:
            '''The health check URL of the URL endpoint type.

            If the URL is a public endpoint, the ``HealthUrl`` must also be a public endpoint. If the URL is a private endpoint inside a virtual private cloud (VPC), the health URL must also be a private endpoint, and the host must be the same as the URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-service-urlendpointinput.html#cfn-refactorspaces-service-urlendpointinput-healthurl
            '''
            result = self._values.get("health_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL to route traffic to.

            The URL must be an `rfc3986-formatted URL <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc3986>`_ . If the host is a domain name, the name must be resolvable over the public internet. If the scheme is ``https`` , the top level domain of the host must be listed in the `IANA root zone database <https://docs.aws.amazon.com/https://www.iana.org/domains/root/db>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-service-urlendpointinput.html#cfn-refactorspaces-service-urlendpointinput-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UrlEndpointInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnApplicationMixinProps",
    "CfnApplicationPropsMixin",
    "CfnEnvironmentMixinProps",
    "CfnEnvironmentPropsMixin",
    "CfnRouteMixinProps",
    "CfnRoutePropsMixin",
    "CfnServiceMixinProps",
    "CfnServicePropsMixin",
]

publication.publish()

def _typecheckingstub__ca698f3824463234452e90c49556308de726dbe3151eea0e29ca88aaa145c635(
    *,
    api_gateway_proxy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ApiGatewayProxyInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    environment_identifier: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    proxy_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d2b1e5e0c23bd2a16bb27c02080552710bf102efdce77588a84b37d3ebfcb8f(
    props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca9c065a673d37daea04c97f86c8b28cc04264d76dcd62497201bd7b0af3b69b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7c000b1593e859f681df2d410c1a1310f59bb472f741659f6efa91ed7bc537(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae354ff68eba0398cf39d38cc2ea4e41fbe9c17cfc9d74331da550fec92412e(
    *,
    endpoint_type: typing.Optional[builtins.str] = None,
    stage_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a54b6e9a3052f94febdfb3bc575742ecaf318607570fcf6835312f3ec4a75bab(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    network_fabric_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01e87d1877d27e444a3b51ff976de9c963e4c47d009ace6698dc5a65f11c0b9f(
    props: typing.Union[CfnEnvironmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e579d4004783413400e5d76e005d21d09df4854050f6d032b1f5ca1baf1b7f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5435737e658d1c009e0ca54aff4d0ddc920a2ac1cd10dc9145b41efbf327a7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00896d4603a1518abbe80cd940c296a7cd661d76cbcf155b7eec10973deb9e98(
    *,
    application_identifier: typing.Optional[builtins.str] = None,
    default_route: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.DefaultRouteInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    environment_identifier: typing.Optional[builtins.str] = None,
    route_type: typing.Optional[builtins.str] = None,
    service_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    uri_path_route: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutePropsMixin.UriPathRouteInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1326061d5d1ef25f87757b65fe8a8c1f7cfe4e0832d27daa1e771e2ced046c91(
    props: typing.Union[CfnRouteMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55435390f1f0ba3639ff252d2589d1b92d5c93343b33cdb1cfb809e6645a90e3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb8900b0c714d0881be8130ea1bd0fb327191a59070df81d117e70742f17088(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8e1d2621eb3450a3ba1d1b90a2234003317a345101490973f43649bb48713dd(
    *,
    activation_state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82145f22e05c81b9c15c298471eb3118697a6e56cd9ef3615e068f6e5b5372f7(
    *,
    activation_state: typing.Optional[builtins.str] = None,
    append_source_path: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_child_paths: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__922a97ef04b3346fd165d59712a6bf425c4ce2f95ffbecc8eed2f2d5aaecfaae(
    *,
    application_identifier: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    endpoint_type: typing.Optional[builtins.str] = None,
    environment_identifier: typing.Optional[builtins.str] = None,
    lambda_endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.LambdaEndpointInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    url_endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.UrlEndpointInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__185ca92dbc70fa6c8117982f863c98be20b2a0217178c81113c2dd1ccf59d7b9(
    props: typing.Union[CfnServiceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c86af025e5286795d1f25e4d6f930c677a78ce0ba3e54e39711348c48b44f9bd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__321a7611a080383b99ab8c598908130b1307e9bbcf8d244a4648784659fd7f64(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__571a2b8ae9113c393910d8ee1e8b25db5d8490b78ef21eda8fc2a0a40233886e(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__816621a92358e17c503e06ec561d87d49b1149f2e0cd2521a0693e6e7e52211b(
    *,
    health_url: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
