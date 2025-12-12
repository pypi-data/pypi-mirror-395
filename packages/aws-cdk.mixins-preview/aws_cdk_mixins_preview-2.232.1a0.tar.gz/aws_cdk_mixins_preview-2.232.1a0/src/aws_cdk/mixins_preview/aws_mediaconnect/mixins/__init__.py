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
    jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnBridgeMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "egress_gateway_bridge": "egressGatewayBridge",
        "ingress_gateway_bridge": "ingressGatewayBridge",
        "name": "name",
        "outputs": "outputs",
        "placement_arn": "placementArn",
        "source_failover_config": "sourceFailoverConfig",
        "sources": "sources",
    },
)
class CfnBridgeMixinProps:
    def __init__(
        self,
        *,
        egress_gateway_bridge: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBridgePropsMixin.EgressGatewayBridgeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ingress_gateway_bridge: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBridgePropsMixin.IngressGatewayBridgeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        outputs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBridgePropsMixin.BridgeOutputProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        placement_arn: typing.Optional[builtins.str] = None,
        source_failover_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBridgePropsMixin.FailoverConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBridgePropsMixin.BridgeSourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnBridgePropsMixin.

        :param egress_gateway_bridge: An egress bridge is a cloud-to-ground bridge. The content comes from an existing MediaConnect flow and is delivered to your premises.
        :param ingress_gateway_bridge: An ingress bridge is a ground-to-cloud bridge. The content originates at your premises and is delivered to the cloud.
        :param name: The name of the bridge. This name can not be modified after the bridge is created.
        :param outputs: The outputs that you want to add to this bridge.
        :param placement_arn: The bridge placement Amazon Resource Number (ARN).
        :param source_failover_config: The settings for source failover.
        :param sources: The sources that you want to add to this bridge.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-bridge.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
            
            cfn_bridge_mixin_props = mediaconnect_mixins.CfnBridgeMixinProps(
                egress_gateway_bridge=mediaconnect_mixins.CfnBridgePropsMixin.EgressGatewayBridgeProperty(
                    max_bitrate=123
                ),
                ingress_gateway_bridge=mediaconnect_mixins.CfnBridgePropsMixin.IngressGatewayBridgeProperty(
                    max_bitrate=123,
                    max_outputs=123
                ),
                name="name",
                outputs=[mediaconnect_mixins.CfnBridgePropsMixin.BridgeOutputProperty(
                    network_output=mediaconnect_mixins.CfnBridgePropsMixin.BridgeNetworkOutputProperty(
                        ip_address="ipAddress",
                        name="name",
                        network_name="networkName",
                        port=123,
                        protocol="protocol",
                        ttl=123
                    )
                )],
                placement_arn="placementArn",
                source_failover_config=mediaconnect_mixins.CfnBridgePropsMixin.FailoverConfigProperty(
                    failover_mode="failoverMode",
                    source_priority=mediaconnect_mixins.CfnBridgePropsMixin.SourcePriorityProperty(
                        primary_source="primarySource"
                    ),
                    state="state"
                ),
                sources=[mediaconnect_mixins.CfnBridgePropsMixin.BridgeSourceProperty(
                    flow_source=mediaconnect_mixins.CfnBridgePropsMixin.BridgeFlowSourceProperty(
                        flow_arn="flowArn",
                        flow_vpc_interface_attachment=mediaconnect_mixins.CfnBridgePropsMixin.VpcInterfaceAttachmentProperty(
                            vpc_interface_name="vpcInterfaceName"
                        ),
                        name="name"
                    ),
                    network_source=mediaconnect_mixins.CfnBridgePropsMixin.BridgeNetworkSourceProperty(
                        multicast_ip="multicastIp",
                        multicast_source_settings=mediaconnect_mixins.CfnBridgePropsMixin.MulticastSourceSettingsProperty(
                            multicast_source_ip="multicastSourceIp"
                        ),
                        name="name",
                        network_name="networkName",
                        port=123,
                        protocol="protocol"
                    )
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16235aad5a3dc715d25f74a9ee546c2cee61d7c148a67bf46577cd68f8d8e2ee)
            check_type(argname="argument egress_gateway_bridge", value=egress_gateway_bridge, expected_type=type_hints["egress_gateway_bridge"])
            check_type(argname="argument ingress_gateway_bridge", value=ingress_gateway_bridge, expected_type=type_hints["ingress_gateway_bridge"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument outputs", value=outputs, expected_type=type_hints["outputs"])
            check_type(argname="argument placement_arn", value=placement_arn, expected_type=type_hints["placement_arn"])
            check_type(argname="argument source_failover_config", value=source_failover_config, expected_type=type_hints["source_failover_config"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if egress_gateway_bridge is not None:
            self._values["egress_gateway_bridge"] = egress_gateway_bridge
        if ingress_gateway_bridge is not None:
            self._values["ingress_gateway_bridge"] = ingress_gateway_bridge
        if name is not None:
            self._values["name"] = name
        if outputs is not None:
            self._values["outputs"] = outputs
        if placement_arn is not None:
            self._values["placement_arn"] = placement_arn
        if source_failover_config is not None:
            self._values["source_failover_config"] = source_failover_config
        if sources is not None:
            self._values["sources"] = sources

    @builtins.property
    def egress_gateway_bridge(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgePropsMixin.EgressGatewayBridgeProperty"]]:
        '''An egress bridge is a cloud-to-ground bridge.

        The content comes from an existing MediaConnect flow and is delivered to your premises.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-bridge.html#cfn-mediaconnect-bridge-egressgatewaybridge
        '''
        result = self._values.get("egress_gateway_bridge")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgePropsMixin.EgressGatewayBridgeProperty"]], result)

    @builtins.property
    def ingress_gateway_bridge(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgePropsMixin.IngressGatewayBridgeProperty"]]:
        '''An ingress bridge is a ground-to-cloud bridge.

        The content originates at your premises and is delivered to the cloud.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-bridge.html#cfn-mediaconnect-bridge-ingressgatewaybridge
        '''
        result = self._values.get("ingress_gateway_bridge")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgePropsMixin.IngressGatewayBridgeProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the bridge.

        This name can not be modified after the bridge is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-bridge.html#cfn-mediaconnect-bridge-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outputs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgePropsMixin.BridgeOutputProperty"]]]]:
        '''The outputs that you want to add to this bridge.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-bridge.html#cfn-mediaconnect-bridge-outputs
        '''
        result = self._values.get("outputs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgePropsMixin.BridgeOutputProperty"]]]], result)

    @builtins.property
    def placement_arn(self) -> typing.Optional[builtins.str]:
        '''The bridge placement Amazon Resource Number (ARN).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-bridge.html#cfn-mediaconnect-bridge-placementarn
        '''
        result = self._values.get("placement_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_failover_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgePropsMixin.FailoverConfigProperty"]]:
        '''The settings for source failover.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-bridge.html#cfn-mediaconnect-bridge-sourcefailoverconfig
        '''
        result = self._values.get("source_failover_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgePropsMixin.FailoverConfigProperty"]], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgePropsMixin.BridgeSourceProperty"]]]]:
        '''The sources that you want to add to this bridge.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-bridge.html#cfn-mediaconnect-bridge-sources
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgePropsMixin.BridgeSourceProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBridgeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnBridgeOutputMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "bridge_arn": "bridgeArn",
        "name": "name",
        "network_output": "networkOutput",
    },
)
class CfnBridgeOutputMixinProps:
    def __init__(
        self,
        *,
        bridge_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        network_output: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBridgeOutputPropsMixin.BridgeNetworkOutputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnBridgeOutputPropsMixin.

        :param bridge_arn: The Amazon Resource Name (ARN) of the bridge that you want to update.
        :param name: The network output name. This name is used to reference the output and must be unique among outputs in this bridge.
        :param network_output: The network output of the bridge. A network output is delivered to your premises.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-bridgeoutput.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
            
            cfn_bridge_output_mixin_props = mediaconnect_mixins.CfnBridgeOutputMixinProps(
                bridge_arn="bridgeArn",
                name="name",
                network_output=mediaconnect_mixins.CfnBridgeOutputPropsMixin.BridgeNetworkOutputProperty(
                    ip_address="ipAddress",
                    network_name="networkName",
                    port=123,
                    protocol="protocol",
                    ttl=123
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1f00e49541be4a9e9c08865479eae478cdeed7722d1effd432d19aab3499dea)
            check_type(argname="argument bridge_arn", value=bridge_arn, expected_type=type_hints["bridge_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_output", value=network_output, expected_type=type_hints["network_output"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bridge_arn is not None:
            self._values["bridge_arn"] = bridge_arn
        if name is not None:
            self._values["name"] = name
        if network_output is not None:
            self._values["network_output"] = network_output

    @builtins.property
    def bridge_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the bridge that you want to update.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-bridgeoutput.html#cfn-mediaconnect-bridgeoutput-bridgearn
        '''
        result = self._values.get("bridge_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The network output name.

        This name is used to reference the output and must be unique among outputs in this bridge.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-bridgeoutput.html#cfn-mediaconnect-bridgeoutput-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_output(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgeOutputPropsMixin.BridgeNetworkOutputProperty"]]:
        '''The network output of the bridge.

        A network output is delivered to your premises.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-bridgeoutput.html#cfn-mediaconnect-bridgeoutput-networkoutput
        '''
        result = self._values.get("network_output")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgeOutputPropsMixin.BridgeNetworkOutputProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBridgeOutputMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnBridgeOutputPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnBridgeOutputPropsMixin",
):
    '''Adds outputs to an existing bridge.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-bridgeoutput.html
    :cloudformationResource: AWS::MediaConnect::BridgeOutput
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
        
        cfn_bridge_output_props_mixin = mediaconnect_mixins.CfnBridgeOutputPropsMixin(mediaconnect_mixins.CfnBridgeOutputMixinProps(
            bridge_arn="bridgeArn",
            name="name",
            network_output=mediaconnect_mixins.CfnBridgeOutputPropsMixin.BridgeNetworkOutputProperty(
                ip_address="ipAddress",
                network_name="networkName",
                port=123,
                protocol="protocol",
                ttl=123
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnBridgeOutputMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaConnect::BridgeOutput``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a721e49cb76d95643d4262194beedf7977b84ebef9887949680c8a634c0a7f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c42c9a1c9d3e449b5489caa559bb67365f7e1d5ff53fd4657d4b2f21c64986e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dd205f5493463b69b5b94023ccf3082048c668f368b60d3212cb0e11b5430ed)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBridgeOutputMixinProps:
        return typing.cast(CfnBridgeOutputMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnBridgeOutputPropsMixin.BridgeNetworkOutputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ip_address": "ipAddress",
            "network_name": "networkName",
            "port": "port",
            "protocol": "protocol",
            "ttl": "ttl",
        },
    )
    class BridgeNetworkOutputProperty:
        def __init__(
            self,
            *,
            ip_address: typing.Optional[builtins.str] = None,
            network_name: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            protocol: typing.Optional[builtins.str] = None,
            ttl: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The output of the bridge.

            A network output is delivered to your premises.

            :param ip_address: The network output IP address.
            :param network_name: The network output's gateway network name.
            :param port: The network output's port.
            :param protocol: The network output protocol. .. epigraph:: AWS Elemental MediaConnect no longer supports the Fujitsu QoS protocol. This reference is maintained for legacy purposes only.
            :param ttl: The network output TTL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridgeoutput-bridgenetworkoutput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                bridge_network_output_property = mediaconnect_mixins.CfnBridgeOutputPropsMixin.BridgeNetworkOutputProperty(
                    ip_address="ipAddress",
                    network_name="networkName",
                    port=123,
                    protocol="protocol",
                    ttl=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aa63255631e965eefa190d5926e7e719349b9960cb4cebb78f62f5c525f94e3b)
                check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
                check_type(argname="argument network_name", value=network_name, expected_type=type_hints["network_name"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ip_address is not None:
                self._values["ip_address"] = ip_address
            if network_name is not None:
                self._values["network_name"] = network_name
            if port is not None:
                self._values["port"] = port
            if protocol is not None:
                self._values["protocol"] = protocol
            if ttl is not None:
                self._values["ttl"] = ttl

        @builtins.property
        def ip_address(self) -> typing.Optional[builtins.str]:
            '''The network output IP address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridgeoutput-bridgenetworkoutput.html#cfn-mediaconnect-bridgeoutput-bridgenetworkoutput-ipaddress
            '''
            result = self._values.get("ip_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def network_name(self) -> typing.Optional[builtins.str]:
            '''The network output's gateway network name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridgeoutput-bridgenetworkoutput.html#cfn-mediaconnect-bridgeoutput-bridgenetworkoutput-networkname
            '''
            result = self._values.get("network_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The network output's port.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridgeoutput-bridgenetworkoutput.html#cfn-mediaconnect-bridgeoutput-bridgenetworkoutput-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The network output protocol.

            .. epigraph::

               AWS Elemental MediaConnect no longer supports the Fujitsu QoS protocol. This reference is maintained for legacy purposes only.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridgeoutput-bridgenetworkoutput.html#cfn-mediaconnect-bridgeoutput-bridgenetworkoutput-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ttl(self) -> typing.Optional[jsii.Number]:
            '''The network output TTL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridgeoutput-bridgenetworkoutput.html#cfn-mediaconnect-bridgeoutput-bridgenetworkoutput-ttl
            '''
            result = self._values.get("ttl")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BridgeNetworkOutputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IMixin_11e4b965)
class CfnBridgePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnBridgePropsMixin",
):
    '''The ``AWS::MediaConnect::Bridge`` resource defines a connection between your data center’s gateway instances and the cloud.

    For each bridge, you specify the type of bridge, transport protocol to use, and details for any outputs and failover.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-bridge.html
    :cloudformationResource: AWS::MediaConnect::Bridge
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
        
        cfn_bridge_props_mixin = mediaconnect_mixins.CfnBridgePropsMixin(mediaconnect_mixins.CfnBridgeMixinProps(
            egress_gateway_bridge=mediaconnect_mixins.CfnBridgePropsMixin.EgressGatewayBridgeProperty(
                max_bitrate=123
            ),
            ingress_gateway_bridge=mediaconnect_mixins.CfnBridgePropsMixin.IngressGatewayBridgeProperty(
                max_bitrate=123,
                max_outputs=123
            ),
            name="name",
            outputs=[mediaconnect_mixins.CfnBridgePropsMixin.BridgeOutputProperty(
                network_output=mediaconnect_mixins.CfnBridgePropsMixin.BridgeNetworkOutputProperty(
                    ip_address="ipAddress",
                    name="name",
                    network_name="networkName",
                    port=123,
                    protocol="protocol",
                    ttl=123
                )
            )],
            placement_arn="placementArn",
            source_failover_config=mediaconnect_mixins.CfnBridgePropsMixin.FailoverConfigProperty(
                failover_mode="failoverMode",
                source_priority=mediaconnect_mixins.CfnBridgePropsMixin.SourcePriorityProperty(
                    primary_source="primarySource"
                ),
                state="state"
            ),
            sources=[mediaconnect_mixins.CfnBridgePropsMixin.BridgeSourceProperty(
                flow_source=mediaconnect_mixins.CfnBridgePropsMixin.BridgeFlowSourceProperty(
                    flow_arn="flowArn",
                    flow_vpc_interface_attachment=mediaconnect_mixins.CfnBridgePropsMixin.VpcInterfaceAttachmentProperty(
                        vpc_interface_name="vpcInterfaceName"
                    ),
                    name="name"
                ),
                network_source=mediaconnect_mixins.CfnBridgePropsMixin.BridgeNetworkSourceProperty(
                    multicast_ip="multicastIp",
                    multicast_source_settings=mediaconnect_mixins.CfnBridgePropsMixin.MulticastSourceSettingsProperty(
                        multicast_source_ip="multicastSourceIp"
                    ),
                    name="name",
                    network_name="networkName",
                    port=123,
                    protocol="protocol"
                )
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnBridgeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaConnect::Bridge``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0591ad5cf313775224ba6ac989be2665af5de2c7c4ca9fb4b862fa6d41c0577)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e63ca835689f352353b110ee9ca4f6f8d2b9864ecfc9c84b806f2dc65f9653e8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52e68203a62a9783236996d3e743e80f3151ebf2e520851b04640e417425f2e3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBridgeMixinProps:
        return typing.cast(CfnBridgeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnBridgePropsMixin.BridgeFlowSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "flow_arn": "flowArn",
            "flow_vpc_interface_attachment": "flowVpcInterfaceAttachment",
            "name": "name",
        },
    )
    class BridgeFlowSourceProperty:
        def __init__(
            self,
            *,
            flow_arn: typing.Optional[builtins.str] = None,
            flow_vpc_interface_attachment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBridgePropsMixin.VpcInterfaceAttachmentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The source of the bridge.

            A flow source originates in MediaConnect as an existing cloud flow.

            :param flow_arn: The ARN of the cloud flow used as a source of this bridge.
            :param flow_vpc_interface_attachment: The name of the VPC interface attachment to use for this source.
            :param name: The name of the flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-bridgeflowsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                bridge_flow_source_property = mediaconnect_mixins.CfnBridgePropsMixin.BridgeFlowSourceProperty(
                    flow_arn="flowArn",
                    flow_vpc_interface_attachment=mediaconnect_mixins.CfnBridgePropsMixin.VpcInterfaceAttachmentProperty(
                        vpc_interface_name="vpcInterfaceName"
                    ),
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4e5bcacdbb43d1a64ec051404e067731d52d2256212de47427277605e34477de)
                check_type(argname="argument flow_arn", value=flow_arn, expected_type=type_hints["flow_arn"])
                check_type(argname="argument flow_vpc_interface_attachment", value=flow_vpc_interface_attachment, expected_type=type_hints["flow_vpc_interface_attachment"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if flow_arn is not None:
                self._values["flow_arn"] = flow_arn
            if flow_vpc_interface_attachment is not None:
                self._values["flow_vpc_interface_attachment"] = flow_vpc_interface_attachment
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def flow_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the cloud flow used as a source of this bridge.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-bridgeflowsource.html#cfn-mediaconnect-bridge-bridgeflowsource-flowarn
            '''
            result = self._values.get("flow_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def flow_vpc_interface_attachment(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgePropsMixin.VpcInterfaceAttachmentProperty"]]:
            '''The name of the VPC interface attachment to use for this source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-bridgeflowsource.html#cfn-mediaconnect-bridge-bridgeflowsource-flowvpcinterfaceattachment
            '''
            result = self._values.get("flow_vpc_interface_attachment")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgePropsMixin.VpcInterfaceAttachmentProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-bridgeflowsource.html#cfn-mediaconnect-bridge-bridgeflowsource-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BridgeFlowSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnBridgePropsMixin.BridgeNetworkOutputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ip_address": "ipAddress",
            "name": "name",
            "network_name": "networkName",
            "port": "port",
            "protocol": "protocol",
            "ttl": "ttl",
        },
    )
    class BridgeNetworkOutputProperty:
        def __init__(
            self,
            *,
            ip_address: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            network_name: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            protocol: typing.Optional[builtins.str] = None,
            ttl: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The output of the bridge.

            A network output is delivered to your premises.

            :param ip_address: The network output IP address.
            :param name: The network output name.
            :param network_name: The network output's gateway network name.
            :param port: The network output's port.
            :param protocol: The network output protocol. .. epigraph:: AWS Elemental MediaConnect no longer supports the Fujitsu QoS protocol. This reference is maintained for legacy purposes only.
            :param ttl: The network output TTL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-bridgenetworkoutput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                bridge_network_output_property = mediaconnect_mixins.CfnBridgePropsMixin.BridgeNetworkOutputProperty(
                    ip_address="ipAddress",
                    name="name",
                    network_name="networkName",
                    port=123,
                    protocol="protocol",
                    ttl=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1f61d2be7a0c0fabe6b1eb55303e8c8172616ecee577982cca652e6b4bd71041)
                check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument network_name", value=network_name, expected_type=type_hints["network_name"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ip_address is not None:
                self._values["ip_address"] = ip_address
            if name is not None:
                self._values["name"] = name
            if network_name is not None:
                self._values["network_name"] = network_name
            if port is not None:
                self._values["port"] = port
            if protocol is not None:
                self._values["protocol"] = protocol
            if ttl is not None:
                self._values["ttl"] = ttl

        @builtins.property
        def ip_address(self) -> typing.Optional[builtins.str]:
            '''The network output IP address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-bridgenetworkoutput.html#cfn-mediaconnect-bridge-bridgenetworkoutput-ipaddress
            '''
            result = self._values.get("ip_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The network output name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-bridgenetworkoutput.html#cfn-mediaconnect-bridge-bridgenetworkoutput-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def network_name(self) -> typing.Optional[builtins.str]:
            '''The network output's gateway network name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-bridgenetworkoutput.html#cfn-mediaconnect-bridge-bridgenetworkoutput-networkname
            '''
            result = self._values.get("network_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The network output's port.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-bridgenetworkoutput.html#cfn-mediaconnect-bridge-bridgenetworkoutput-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The network output protocol.

            .. epigraph::

               AWS Elemental MediaConnect no longer supports the Fujitsu QoS protocol. This reference is maintained for legacy purposes only.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-bridgenetworkoutput.html#cfn-mediaconnect-bridge-bridgenetworkoutput-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ttl(self) -> typing.Optional[jsii.Number]:
            '''The network output TTL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-bridgenetworkoutput.html#cfn-mediaconnect-bridge-bridgenetworkoutput-ttl
            '''
            result = self._values.get("ttl")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BridgeNetworkOutputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnBridgePropsMixin.BridgeNetworkSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "multicast_ip": "multicastIp",
            "multicast_source_settings": "multicastSourceSettings",
            "name": "name",
            "network_name": "networkName",
            "port": "port",
            "protocol": "protocol",
        },
    )
    class BridgeNetworkSourceProperty:
        def __init__(
            self,
            *,
            multicast_ip: typing.Optional[builtins.str] = None,
            multicast_source_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBridgePropsMixin.MulticastSourceSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
            network_name: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            protocol: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The source of the bridge.

            A network source originates at your premises.

            :param multicast_ip: The network source multicast IP.
            :param multicast_source_settings: The settings related to the multicast source.
            :param name: The name of the network source.
            :param network_name: The network source's gateway network name.
            :param port: The network source port.
            :param protocol: The network source protocol. .. epigraph:: AWS Elemental MediaConnect no longer supports the Fujitsu QoS protocol. This reference is maintained for legacy purposes only.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-bridgenetworksource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                bridge_network_source_property = mediaconnect_mixins.CfnBridgePropsMixin.BridgeNetworkSourceProperty(
                    multicast_ip="multicastIp",
                    multicast_source_settings=mediaconnect_mixins.CfnBridgePropsMixin.MulticastSourceSettingsProperty(
                        multicast_source_ip="multicastSourceIp"
                    ),
                    name="name",
                    network_name="networkName",
                    port=123,
                    protocol="protocol"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8eebae8e16046079e65f49519bc3902e42f299510c089e2d8c2238fe732e075d)
                check_type(argname="argument multicast_ip", value=multicast_ip, expected_type=type_hints["multicast_ip"])
                check_type(argname="argument multicast_source_settings", value=multicast_source_settings, expected_type=type_hints["multicast_source_settings"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument network_name", value=network_name, expected_type=type_hints["network_name"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if multicast_ip is not None:
                self._values["multicast_ip"] = multicast_ip
            if multicast_source_settings is not None:
                self._values["multicast_source_settings"] = multicast_source_settings
            if name is not None:
                self._values["name"] = name
            if network_name is not None:
                self._values["network_name"] = network_name
            if port is not None:
                self._values["port"] = port
            if protocol is not None:
                self._values["protocol"] = protocol

        @builtins.property
        def multicast_ip(self) -> typing.Optional[builtins.str]:
            '''The network source multicast IP.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-bridgenetworksource.html#cfn-mediaconnect-bridge-bridgenetworksource-multicastip
            '''
            result = self._values.get("multicast_ip")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def multicast_source_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgePropsMixin.MulticastSourceSettingsProperty"]]:
            '''The settings related to the multicast source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-bridgenetworksource.html#cfn-mediaconnect-bridge-bridgenetworksource-multicastsourcesettings
            '''
            result = self._values.get("multicast_source_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgePropsMixin.MulticastSourceSettingsProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the network source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-bridgenetworksource.html#cfn-mediaconnect-bridge-bridgenetworksource-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def network_name(self) -> typing.Optional[builtins.str]:
            '''The network source's gateway network name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-bridgenetworksource.html#cfn-mediaconnect-bridge-bridgenetworksource-networkname
            '''
            result = self._values.get("network_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The network source port.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-bridgenetworksource.html#cfn-mediaconnect-bridge-bridgenetworksource-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The network source protocol.

            .. epigraph::

               AWS Elemental MediaConnect no longer supports the Fujitsu QoS protocol. This reference is maintained for legacy purposes only.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-bridgenetworksource.html#cfn-mediaconnect-bridge-bridgenetworksource-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BridgeNetworkSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnBridgePropsMixin.BridgeOutputProperty",
        jsii_struct_bases=[],
        name_mapping={"network_output": "networkOutput"},
    )
    class BridgeOutputProperty:
        def __init__(
            self,
            *,
            network_output: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBridgePropsMixin.BridgeNetworkOutputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The output of the bridge.

            :param network_output: The output of the bridge. A network output is delivered to your premises.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-bridgeoutput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                bridge_output_property = mediaconnect_mixins.CfnBridgePropsMixin.BridgeOutputProperty(
                    network_output=mediaconnect_mixins.CfnBridgePropsMixin.BridgeNetworkOutputProperty(
                        ip_address="ipAddress",
                        name="name",
                        network_name="networkName",
                        port=123,
                        protocol="protocol",
                        ttl=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__59edae2f14c29ff9f2455b0897ac22016bebd8d9e0d1c76154d67d9ae9f65ccf)
                check_type(argname="argument network_output", value=network_output, expected_type=type_hints["network_output"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if network_output is not None:
                self._values["network_output"] = network_output

        @builtins.property
        def network_output(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgePropsMixin.BridgeNetworkOutputProperty"]]:
            '''The output of the bridge.

            A network output is delivered to your premises.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-bridgeoutput.html#cfn-mediaconnect-bridge-bridgeoutput-networkoutput
            '''
            result = self._values.get("network_output")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgePropsMixin.BridgeNetworkOutputProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BridgeOutputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnBridgePropsMixin.BridgeSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"flow_source": "flowSource", "network_source": "networkSource"},
    )
    class BridgeSourceProperty:
        def __init__(
            self,
            *,
            flow_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBridgePropsMixin.BridgeFlowSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            network_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBridgePropsMixin.BridgeNetworkSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The bridge's source.

            :param flow_source: The source of the bridge. A flow source originates in MediaConnect as an existing cloud flow.
            :param network_source: The source of the bridge. A network source originates at your premises.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-bridgesource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                bridge_source_property = mediaconnect_mixins.CfnBridgePropsMixin.BridgeSourceProperty(
                    flow_source=mediaconnect_mixins.CfnBridgePropsMixin.BridgeFlowSourceProperty(
                        flow_arn="flowArn",
                        flow_vpc_interface_attachment=mediaconnect_mixins.CfnBridgePropsMixin.VpcInterfaceAttachmentProperty(
                            vpc_interface_name="vpcInterfaceName"
                        ),
                        name="name"
                    ),
                    network_source=mediaconnect_mixins.CfnBridgePropsMixin.BridgeNetworkSourceProperty(
                        multicast_ip="multicastIp",
                        multicast_source_settings=mediaconnect_mixins.CfnBridgePropsMixin.MulticastSourceSettingsProperty(
                            multicast_source_ip="multicastSourceIp"
                        ),
                        name="name",
                        network_name="networkName",
                        port=123,
                        protocol="protocol"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6b5ced5741bc103b9e47e61c69294d6879943edbbeba334f20484be308322790)
                check_type(argname="argument flow_source", value=flow_source, expected_type=type_hints["flow_source"])
                check_type(argname="argument network_source", value=network_source, expected_type=type_hints["network_source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if flow_source is not None:
                self._values["flow_source"] = flow_source
            if network_source is not None:
                self._values["network_source"] = network_source

        @builtins.property
        def flow_source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgePropsMixin.BridgeFlowSourceProperty"]]:
            '''The source of the bridge.

            A flow source originates in MediaConnect as an existing cloud flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-bridgesource.html#cfn-mediaconnect-bridge-bridgesource-flowsource
            '''
            result = self._values.get("flow_source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgePropsMixin.BridgeFlowSourceProperty"]], result)

        @builtins.property
        def network_source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgePropsMixin.BridgeNetworkSourceProperty"]]:
            '''The source of the bridge.

            A network source originates at your premises.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-bridgesource.html#cfn-mediaconnect-bridge-bridgesource-networksource
            '''
            result = self._values.get("network_source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgePropsMixin.BridgeNetworkSourceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BridgeSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnBridgePropsMixin.EgressGatewayBridgeProperty",
        jsii_struct_bases=[],
        name_mapping={"max_bitrate": "maxBitrate"},
    )
    class EgressGatewayBridgeProperty:
        def __init__(self, *, max_bitrate: typing.Optional[jsii.Number] = None) -> None:
            '''Create a bridge with the egress bridge type.

            An egress bridge is a cloud-to-ground bridge. The content comes from an existing MediaConnect flow and is delivered to your premises.

            :param max_bitrate: The maximum expected bitrate (in bps) of the egress bridge.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-egressgatewaybridge.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                egress_gateway_bridge_property = mediaconnect_mixins.CfnBridgePropsMixin.EgressGatewayBridgeProperty(
                    max_bitrate=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c54fd43f8091c501e8cc5d608ae23501bd2c22a86779e3049e984112a5950b8e)
                check_type(argname="argument max_bitrate", value=max_bitrate, expected_type=type_hints["max_bitrate"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_bitrate is not None:
                self._values["max_bitrate"] = max_bitrate

        @builtins.property
        def max_bitrate(self) -> typing.Optional[jsii.Number]:
            '''The maximum expected bitrate (in bps) of the egress bridge.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-egressgatewaybridge.html#cfn-mediaconnect-bridge-egressgatewaybridge-maxbitrate
            '''
            result = self._values.get("max_bitrate")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EgressGatewayBridgeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnBridgePropsMixin.FailoverConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "failover_mode": "failoverMode",
            "source_priority": "sourcePriority",
            "state": "state",
        },
    )
    class FailoverConfigProperty:
        def __init__(
            self,
            *,
            failover_mode: typing.Optional[builtins.str] = None,
            source_priority: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBridgePropsMixin.SourcePriorityProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            state: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The settings for source failover.

            :param failover_mode: The type of failover you choose for this flow. MERGE combines the source streams into a single stream, allowing graceful recovery from any single-source loss. FAILOVER allows switching between different streams.
            :param source_priority: The priority you want to assign to a source. You can have a primary stream and a backup stream or two equally prioritized streams.
            :param state: The state of source failover on the flow. If the state is inactive, the flow can have only one source. If the state is active, the flow can have one or two sources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-failoverconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                failover_config_property = mediaconnect_mixins.CfnBridgePropsMixin.FailoverConfigProperty(
                    failover_mode="failoverMode",
                    source_priority=mediaconnect_mixins.CfnBridgePropsMixin.SourcePriorityProperty(
                        primary_source="primarySource"
                    ),
                    state="state"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__976dcf674111a58e5dd13d27128ee2c38e001a62c9b7ae97cb1ed1d8b3e5a6d4)
                check_type(argname="argument failover_mode", value=failover_mode, expected_type=type_hints["failover_mode"])
                check_type(argname="argument source_priority", value=source_priority, expected_type=type_hints["source_priority"])
                check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if failover_mode is not None:
                self._values["failover_mode"] = failover_mode
            if source_priority is not None:
                self._values["source_priority"] = source_priority
            if state is not None:
                self._values["state"] = state

        @builtins.property
        def failover_mode(self) -> typing.Optional[builtins.str]:
            '''The type of failover you choose for this flow.

            MERGE combines the source streams into a single stream, allowing graceful recovery from any single-source loss. FAILOVER allows switching between different streams.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-failoverconfig.html#cfn-mediaconnect-bridge-failoverconfig-failovermode
            '''
            result = self._values.get("failover_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_priority(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgePropsMixin.SourcePriorityProperty"]]:
            '''The priority you want to assign to a source.

            You can have a primary stream and a backup stream or two equally prioritized streams.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-failoverconfig.html#cfn-mediaconnect-bridge-failoverconfig-sourcepriority
            '''
            result = self._values.get("source_priority")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgePropsMixin.SourcePriorityProperty"]], result)

        @builtins.property
        def state(self) -> typing.Optional[builtins.str]:
            '''The state of source failover on the flow.

            If the state is inactive, the flow can have only one source. If the state is active, the flow can have one or two sources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-failoverconfig.html#cfn-mediaconnect-bridge-failoverconfig-state
            '''
            result = self._values.get("state")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FailoverConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnBridgePropsMixin.IngressGatewayBridgeProperty",
        jsii_struct_bases=[],
        name_mapping={"max_bitrate": "maxBitrate", "max_outputs": "maxOutputs"},
    )
    class IngressGatewayBridgeProperty:
        def __init__(
            self,
            *,
            max_bitrate: typing.Optional[jsii.Number] = None,
            max_outputs: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Create a bridge with the ingress bridge type.

            An ingress bridge is a ground-to-cloud bridge. The content originates at your premises and is delivered to the cloud.

            :param max_bitrate: The maximum expected bitrate (in bps) of the ingress bridge.
            :param max_outputs: The maximum number of outputs on the ingress bridge.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-ingressgatewaybridge.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                ingress_gateway_bridge_property = mediaconnect_mixins.CfnBridgePropsMixin.IngressGatewayBridgeProperty(
                    max_bitrate=123,
                    max_outputs=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2e068d58a11c9658979556b9e658b82e7cc74824fe30ec5369b296a12adc6462)
                check_type(argname="argument max_bitrate", value=max_bitrate, expected_type=type_hints["max_bitrate"])
                check_type(argname="argument max_outputs", value=max_outputs, expected_type=type_hints["max_outputs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_bitrate is not None:
                self._values["max_bitrate"] = max_bitrate
            if max_outputs is not None:
                self._values["max_outputs"] = max_outputs

        @builtins.property
        def max_bitrate(self) -> typing.Optional[jsii.Number]:
            '''The maximum expected bitrate (in bps) of the ingress bridge.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-ingressgatewaybridge.html#cfn-mediaconnect-bridge-ingressgatewaybridge-maxbitrate
            '''
            result = self._values.get("max_bitrate")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_outputs(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of outputs on the ingress bridge.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-ingressgatewaybridge.html#cfn-mediaconnect-bridge-ingressgatewaybridge-maxoutputs
            '''
            result = self._values.get("max_outputs")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IngressGatewayBridgeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnBridgePropsMixin.MulticastSourceSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"multicast_source_ip": "multicastSourceIp"},
    )
    class MulticastSourceSettingsProperty:
        def __init__(
            self,
            *,
            multicast_source_ip: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The settings related to the multicast source.

            :param multicast_source_ip: The IP address of the source for source-specific multicast (SSM).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-multicastsourcesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                multicast_source_settings_property = mediaconnect_mixins.CfnBridgePropsMixin.MulticastSourceSettingsProperty(
                    multicast_source_ip="multicastSourceIp"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dbd3cfab07a938574ffdfe775364b6e74e398109be8acfd8b687e3e016e40e21)
                check_type(argname="argument multicast_source_ip", value=multicast_source_ip, expected_type=type_hints["multicast_source_ip"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if multicast_source_ip is not None:
                self._values["multicast_source_ip"] = multicast_source_ip

        @builtins.property
        def multicast_source_ip(self) -> typing.Optional[builtins.str]:
            '''The IP address of the source for source-specific multicast (SSM).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-multicastsourcesettings.html#cfn-mediaconnect-bridge-multicastsourcesettings-multicastsourceip
            '''
            result = self._values.get("multicast_source_ip")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MulticastSourceSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnBridgePropsMixin.SourcePriorityProperty",
        jsii_struct_bases=[],
        name_mapping={"primary_source": "primarySource"},
    )
    class SourcePriorityProperty:
        def __init__(
            self,
            *,
            primary_source: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The priority you want to assign to a source.

            You can have a primary stream and a backup stream or two equally prioritized streams.

            :param primary_source: The name of the source you choose as the primary source for this flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-sourcepriority.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                source_priority_property = mediaconnect_mixins.CfnBridgePropsMixin.SourcePriorityProperty(
                    primary_source="primarySource"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1219af74cd443a6bc3a03399de38fc30c067588d3281ff408922ddb84be44a13)
                check_type(argname="argument primary_source", value=primary_source, expected_type=type_hints["primary_source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if primary_source is not None:
                self._values["primary_source"] = primary_source

        @builtins.property
        def primary_source(self) -> typing.Optional[builtins.str]:
            '''The name of the source you choose as the primary source for this flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-sourcepriority.html#cfn-mediaconnect-bridge-sourcepriority-primarysource
            '''
            result = self._values.get("primary_source")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourcePriorityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnBridgePropsMixin.VpcInterfaceAttachmentProperty",
        jsii_struct_bases=[],
        name_mapping={"vpc_interface_name": "vpcInterfaceName"},
    )
    class VpcInterfaceAttachmentProperty:
        def __init__(
            self,
            *,
            vpc_interface_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The settings for attaching a VPC interface to an resource.

            :param vpc_interface_name: The name of the VPC interface to use for this resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-vpcinterfaceattachment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                vpc_interface_attachment_property = mediaconnect_mixins.CfnBridgePropsMixin.VpcInterfaceAttachmentProperty(
                    vpc_interface_name="vpcInterfaceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__10c34d4146e372d6cf73547f206350a34331d0a6f187e09f6934b631e6ab906e)
                check_type(argname="argument vpc_interface_name", value=vpc_interface_name, expected_type=type_hints["vpc_interface_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if vpc_interface_name is not None:
                self._values["vpc_interface_name"] = vpc_interface_name

        @builtins.property
        def vpc_interface_name(self) -> typing.Optional[builtins.str]:
            '''The name of the VPC interface to use for this resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridge-vpcinterfaceattachment.html#cfn-mediaconnect-bridge-vpcinterfaceattachment-vpcinterfacename
            '''
            result = self._values.get("vpc_interface_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcInterfaceAttachmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnBridgeSourceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "bridge_arn": "bridgeArn",
        "flow_source": "flowSource",
        "name": "name",
        "network_source": "networkSource",
    },
)
class CfnBridgeSourceMixinProps:
    def __init__(
        self,
        *,
        bridge_arn: typing.Optional[builtins.str] = None,
        flow_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBridgeSourcePropsMixin.BridgeFlowSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        network_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBridgeSourcePropsMixin.BridgeNetworkSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnBridgeSourcePropsMixin.

        :param bridge_arn: The ARN of the bridge feeding this flow.
        :param flow_source: The source of the flow.
        :param name: The name of the flow source. This name is used to reference the source and must be unique among sources in this bridge.
        :param network_source: The source of the network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-bridgesource.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
            
            cfn_bridge_source_mixin_props = mediaconnect_mixins.CfnBridgeSourceMixinProps(
                bridge_arn="bridgeArn",
                flow_source=mediaconnect_mixins.CfnBridgeSourcePropsMixin.BridgeFlowSourceProperty(
                    flow_arn="flowArn",
                    flow_vpc_interface_attachment=mediaconnect_mixins.CfnBridgeSourcePropsMixin.VpcInterfaceAttachmentProperty(
                        vpc_interface_name="vpcInterfaceName"
                    )
                ),
                name="name",
                network_source=mediaconnect_mixins.CfnBridgeSourcePropsMixin.BridgeNetworkSourceProperty(
                    multicast_ip="multicastIp",
                    multicast_source_settings=mediaconnect_mixins.CfnBridgeSourcePropsMixin.MulticastSourceSettingsProperty(
                        multicast_source_ip="multicastSourceIp"
                    ),
                    network_name="networkName",
                    port=123,
                    protocol="protocol"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5150595bc93e12d9ae9d50e101336258223d40e67a00f28fa99393fdeb67b52e)
            check_type(argname="argument bridge_arn", value=bridge_arn, expected_type=type_hints["bridge_arn"])
            check_type(argname="argument flow_source", value=flow_source, expected_type=type_hints["flow_source"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_source", value=network_source, expected_type=type_hints["network_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bridge_arn is not None:
            self._values["bridge_arn"] = bridge_arn
        if flow_source is not None:
            self._values["flow_source"] = flow_source
        if name is not None:
            self._values["name"] = name
        if network_source is not None:
            self._values["network_source"] = network_source

    @builtins.property
    def bridge_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the bridge feeding this flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-bridgesource.html#cfn-mediaconnect-bridgesource-bridgearn
        '''
        result = self._values.get("bridge_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flow_source(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgeSourcePropsMixin.BridgeFlowSourceProperty"]]:
        '''The source of the flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-bridgesource.html#cfn-mediaconnect-bridgesource-flowsource
        '''
        result = self._values.get("flow_source")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgeSourcePropsMixin.BridgeFlowSourceProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the flow source.

        This name is used to reference the source and must be unique among sources in this bridge.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-bridgesource.html#cfn-mediaconnect-bridgesource-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_source(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgeSourcePropsMixin.BridgeNetworkSourceProperty"]]:
        '''The source of the network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-bridgesource.html#cfn-mediaconnect-bridgesource-networksource
        '''
        result = self._values.get("network_source")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgeSourcePropsMixin.BridgeNetworkSourceProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBridgeSourceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnBridgeSourcePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnBridgeSourcePropsMixin",
):
    '''Adds sources to an existing bridge.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-bridgesource.html
    :cloudformationResource: AWS::MediaConnect::BridgeSource
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
        
        cfn_bridge_source_props_mixin = mediaconnect_mixins.CfnBridgeSourcePropsMixin(mediaconnect_mixins.CfnBridgeSourceMixinProps(
            bridge_arn="bridgeArn",
            flow_source=mediaconnect_mixins.CfnBridgeSourcePropsMixin.BridgeFlowSourceProperty(
                flow_arn="flowArn",
                flow_vpc_interface_attachment=mediaconnect_mixins.CfnBridgeSourcePropsMixin.VpcInterfaceAttachmentProperty(
                    vpc_interface_name="vpcInterfaceName"
                )
            ),
            name="name",
            network_source=mediaconnect_mixins.CfnBridgeSourcePropsMixin.BridgeNetworkSourceProperty(
                multicast_ip="multicastIp",
                multicast_source_settings=mediaconnect_mixins.CfnBridgeSourcePropsMixin.MulticastSourceSettingsProperty(
                    multicast_source_ip="multicastSourceIp"
                ),
                network_name="networkName",
                port=123,
                protocol="protocol"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnBridgeSourceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaConnect::BridgeSource``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__747e38a3e74a2af31186e4171e1019c59ba0d4b43c5bfab2b7135d66da5f9380)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ce680e0b4328f8b6ecf1fc7f5189d028b66127a97ed4e8c5a5226298ef4d553)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__957471fbda2e7254407b3b5480fc59442adf89a3855d1d346b6c9e83403b510e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBridgeSourceMixinProps:
        return typing.cast(CfnBridgeSourceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnBridgeSourcePropsMixin.BridgeFlowSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "flow_arn": "flowArn",
            "flow_vpc_interface_attachment": "flowVpcInterfaceAttachment",
        },
    )
    class BridgeFlowSourceProperty:
        def __init__(
            self,
            *,
            flow_arn: typing.Optional[builtins.str] = None,
            flow_vpc_interface_attachment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBridgeSourcePropsMixin.VpcInterfaceAttachmentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The source of the bridge.

            A flow source originates in MediaConnect as an existing cloud flow.

            :param flow_arn: The ARN of the cloud flow used as a source of this bridge.
            :param flow_vpc_interface_attachment: The name of the VPC interface attachment to use for this source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridgesource-bridgeflowsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                bridge_flow_source_property = mediaconnect_mixins.CfnBridgeSourcePropsMixin.BridgeFlowSourceProperty(
                    flow_arn="flowArn",
                    flow_vpc_interface_attachment=mediaconnect_mixins.CfnBridgeSourcePropsMixin.VpcInterfaceAttachmentProperty(
                        vpc_interface_name="vpcInterfaceName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f14d8fe763608e4eacdc26031627394bd4f77ffd7e13c55f34f90b5850e0edd8)
                check_type(argname="argument flow_arn", value=flow_arn, expected_type=type_hints["flow_arn"])
                check_type(argname="argument flow_vpc_interface_attachment", value=flow_vpc_interface_attachment, expected_type=type_hints["flow_vpc_interface_attachment"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if flow_arn is not None:
                self._values["flow_arn"] = flow_arn
            if flow_vpc_interface_attachment is not None:
                self._values["flow_vpc_interface_attachment"] = flow_vpc_interface_attachment

        @builtins.property
        def flow_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the cloud flow used as a source of this bridge.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridgesource-bridgeflowsource.html#cfn-mediaconnect-bridgesource-bridgeflowsource-flowarn
            '''
            result = self._values.get("flow_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def flow_vpc_interface_attachment(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgeSourcePropsMixin.VpcInterfaceAttachmentProperty"]]:
            '''The name of the VPC interface attachment to use for this source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridgesource-bridgeflowsource.html#cfn-mediaconnect-bridgesource-bridgeflowsource-flowvpcinterfaceattachment
            '''
            result = self._values.get("flow_vpc_interface_attachment")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgeSourcePropsMixin.VpcInterfaceAttachmentProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BridgeFlowSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnBridgeSourcePropsMixin.BridgeNetworkSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "multicast_ip": "multicastIp",
            "multicast_source_settings": "multicastSourceSettings",
            "network_name": "networkName",
            "port": "port",
            "protocol": "protocol",
        },
    )
    class BridgeNetworkSourceProperty:
        def __init__(
            self,
            *,
            multicast_ip: typing.Optional[builtins.str] = None,
            multicast_source_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBridgeSourcePropsMixin.MulticastSourceSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            network_name: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            protocol: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The source of the bridge.

            A network source originates at your premises.

            :param multicast_ip: The network source multicast IP.
            :param multicast_source_settings: The settings related to the multicast source.
            :param network_name: The network source's gateway network name.
            :param port: The network source port.
            :param protocol: The network source protocol. .. epigraph:: AWS Elemental MediaConnect no longer supports the Fujitsu QoS protocol. This reference is maintained for legacy purposes only.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridgesource-bridgenetworksource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                bridge_network_source_property = mediaconnect_mixins.CfnBridgeSourcePropsMixin.BridgeNetworkSourceProperty(
                    multicast_ip="multicastIp",
                    multicast_source_settings=mediaconnect_mixins.CfnBridgeSourcePropsMixin.MulticastSourceSettingsProperty(
                        multicast_source_ip="multicastSourceIp"
                    ),
                    network_name="networkName",
                    port=123,
                    protocol="protocol"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8bc8622878bacbfb717b051b040e72f26744b8494520faf8edb1c8c2d7b874b3)
                check_type(argname="argument multicast_ip", value=multicast_ip, expected_type=type_hints["multicast_ip"])
                check_type(argname="argument multicast_source_settings", value=multicast_source_settings, expected_type=type_hints["multicast_source_settings"])
                check_type(argname="argument network_name", value=network_name, expected_type=type_hints["network_name"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if multicast_ip is not None:
                self._values["multicast_ip"] = multicast_ip
            if multicast_source_settings is not None:
                self._values["multicast_source_settings"] = multicast_source_settings
            if network_name is not None:
                self._values["network_name"] = network_name
            if port is not None:
                self._values["port"] = port
            if protocol is not None:
                self._values["protocol"] = protocol

        @builtins.property
        def multicast_ip(self) -> typing.Optional[builtins.str]:
            '''The network source multicast IP.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridgesource-bridgenetworksource.html#cfn-mediaconnect-bridgesource-bridgenetworksource-multicastip
            '''
            result = self._values.get("multicast_ip")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def multicast_source_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgeSourcePropsMixin.MulticastSourceSettingsProperty"]]:
            '''The settings related to the multicast source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridgesource-bridgenetworksource.html#cfn-mediaconnect-bridgesource-bridgenetworksource-multicastsourcesettings
            '''
            result = self._values.get("multicast_source_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBridgeSourcePropsMixin.MulticastSourceSettingsProperty"]], result)

        @builtins.property
        def network_name(self) -> typing.Optional[builtins.str]:
            '''The network source's gateway network name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridgesource-bridgenetworksource.html#cfn-mediaconnect-bridgesource-bridgenetworksource-networkname
            '''
            result = self._values.get("network_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The network source port.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridgesource-bridgenetworksource.html#cfn-mediaconnect-bridgesource-bridgenetworksource-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The network source protocol.

            .. epigraph::

               AWS Elemental MediaConnect no longer supports the Fujitsu QoS protocol. This reference is maintained for legacy purposes only.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridgesource-bridgenetworksource.html#cfn-mediaconnect-bridgesource-bridgenetworksource-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BridgeNetworkSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnBridgeSourcePropsMixin.MulticastSourceSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"multicast_source_ip": "multicastSourceIp"},
    )
    class MulticastSourceSettingsProperty:
        def __init__(
            self,
            *,
            multicast_source_ip: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The settings related to the multicast source.

            :param multicast_source_ip: The IP address of the source for source-specific multicast (SSM).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridgesource-multicastsourcesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                multicast_source_settings_property = mediaconnect_mixins.CfnBridgeSourcePropsMixin.MulticastSourceSettingsProperty(
                    multicast_source_ip="multicastSourceIp"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0b259b2385678edfb6fd47abcd33ce7a59135b8d3277bd96a519d70906451ae4)
                check_type(argname="argument multicast_source_ip", value=multicast_source_ip, expected_type=type_hints["multicast_source_ip"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if multicast_source_ip is not None:
                self._values["multicast_source_ip"] = multicast_source_ip

        @builtins.property
        def multicast_source_ip(self) -> typing.Optional[builtins.str]:
            '''The IP address of the source for source-specific multicast (SSM).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridgesource-multicastsourcesettings.html#cfn-mediaconnect-bridgesource-multicastsourcesettings-multicastsourceip
            '''
            result = self._values.get("multicast_source_ip")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MulticastSourceSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnBridgeSourcePropsMixin.VpcInterfaceAttachmentProperty",
        jsii_struct_bases=[],
        name_mapping={"vpc_interface_name": "vpcInterfaceName"},
    )
    class VpcInterfaceAttachmentProperty:
        def __init__(
            self,
            *,
            vpc_interface_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The settings for attaching a VPC interface to an resource.

            :param vpc_interface_name: The name of the VPC interface to use for this resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridgesource-vpcinterfaceattachment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                vpc_interface_attachment_property = mediaconnect_mixins.CfnBridgeSourcePropsMixin.VpcInterfaceAttachmentProperty(
                    vpc_interface_name="vpcInterfaceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c086e7a01e157d7bff676ad4661d47970aaaaef0fba3f7ee20606c60d243bbe3)
                check_type(argname="argument vpc_interface_name", value=vpc_interface_name, expected_type=type_hints["vpc_interface_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if vpc_interface_name is not None:
                self._values["vpc_interface_name"] = vpc_interface_name

        @builtins.property
        def vpc_interface_name(self) -> typing.Optional[builtins.str]:
            '''The name of the VPC interface to use for this resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-bridgesource-vpcinterfaceattachment.html#cfn-mediaconnect-bridgesource-vpcinterfaceattachment-vpcinterfacename
            '''
            result = self._values.get("vpc_interface_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcInterfaceAttachmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowEntitlementMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_transfer_subscriber_fee_percent": "dataTransferSubscriberFeePercent",
        "description": "description",
        "encryption": "encryption",
        "entitlement_status": "entitlementStatus",
        "flow_arn": "flowArn",
        "name": "name",
        "subscribers": "subscribers",
    },
)
class CfnFlowEntitlementMixinProps:
    def __init__(
        self,
        *,
        data_transfer_subscriber_fee_percent: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowEntitlementPropsMixin.EncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        entitlement_status: typing.Optional[builtins.str] = None,
        flow_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        subscribers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnFlowEntitlementPropsMixin.

        :param data_transfer_subscriber_fee_percent: The percentage of the entitlement data transfer fee that you want the subscriber to be responsible for. Default: - 0
        :param description: A description of the entitlement. This description appears only on the MediaConnect console and is not visible outside of the current AWS account.
        :param encryption: Encryption information.
        :param entitlement_status: An indication of whether the new entitlement should be enabled or disabled as soon as it is created. If you don’t specify the entitlementStatus field in your request, MediaConnect sets it to ENABLED.
        :param flow_arn: The Amazon Resource Name (ARN) of the flow.
        :param name: The name of the entitlement. This value must be unique within the current flow.
        :param subscribers: The AWS account IDs that you want to share your content with. The receiving accounts (subscribers) will be allowed to create their own flows using your content as the source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
            
            cfn_flow_entitlement_mixin_props = mediaconnect_mixins.CfnFlowEntitlementMixinProps(
                data_transfer_subscriber_fee_percent=123,
                description="description",
                encryption=mediaconnect_mixins.CfnFlowEntitlementPropsMixin.EncryptionProperty(
                    algorithm="algorithm",
                    constant_initialization_vector="constantInitializationVector",
                    device_id="deviceId",
                    key_type="keyType",
                    region="region",
                    resource_id="resourceId",
                    role_arn="roleArn",
                    secret_arn="secretArn",
                    url="url"
                ),
                entitlement_status="entitlementStatus",
                flow_arn="flowArn",
                name="name",
                subscribers=["subscribers"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c1d106b9fdf3937af314d7a040d02938af289d92367ccd67f0ef8fd49392287)
            check_type(argname="argument data_transfer_subscriber_fee_percent", value=data_transfer_subscriber_fee_percent, expected_type=type_hints["data_transfer_subscriber_fee_percent"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument entitlement_status", value=entitlement_status, expected_type=type_hints["entitlement_status"])
            check_type(argname="argument flow_arn", value=flow_arn, expected_type=type_hints["flow_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument subscribers", value=subscribers, expected_type=type_hints["subscribers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_transfer_subscriber_fee_percent is not None:
            self._values["data_transfer_subscriber_fee_percent"] = data_transfer_subscriber_fee_percent
        if description is not None:
            self._values["description"] = description
        if encryption is not None:
            self._values["encryption"] = encryption
        if entitlement_status is not None:
            self._values["entitlement_status"] = entitlement_status
        if flow_arn is not None:
            self._values["flow_arn"] = flow_arn
        if name is not None:
            self._values["name"] = name
        if subscribers is not None:
            self._values["subscribers"] = subscribers

    @builtins.property
    def data_transfer_subscriber_fee_percent(self) -> typing.Optional[jsii.Number]:
        '''The percentage of the entitlement data transfer fee that you want the subscriber to be responsible for.

        :default: - 0

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html#cfn-mediaconnect-flowentitlement-datatransfersubscriberfeepercent
        '''
        result = self._values.get("data_transfer_subscriber_fee_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the entitlement.

        This description appears only on the MediaConnect console and is not visible outside of the current AWS account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html#cfn-mediaconnect-flowentitlement-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowEntitlementPropsMixin.EncryptionProperty"]]:
        '''Encryption information.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html#cfn-mediaconnect-flowentitlement-encryption
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowEntitlementPropsMixin.EncryptionProperty"]], result)

    @builtins.property
    def entitlement_status(self) -> typing.Optional[builtins.str]:
        '''An indication of whether the new entitlement should be enabled or disabled as soon as it is created.

        If you don’t specify the entitlementStatus field in your request, MediaConnect sets it to ENABLED.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html#cfn-mediaconnect-flowentitlement-entitlementstatus
        '''
        result = self._values.get("entitlement_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flow_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html#cfn-mediaconnect-flowentitlement-flowarn
        '''
        result = self._values.get("flow_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the entitlement.

        This value must be unique within the current flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html#cfn-mediaconnect-flowentitlement-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subscribers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The AWS account IDs that you want to share your content with.

        The receiving accounts (subscribers) will be allowed to create their own flows using your content as the source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html#cfn-mediaconnect-flowentitlement-subscribers
        '''
        result = self._values.get("subscribers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFlowEntitlementMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFlowEntitlementPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowEntitlementPropsMixin",
):
    '''The ``AWS::MediaConnect::FlowEntitlement`` resource defines the permission that an AWS account grants to another AWS account to allow access to the content in a specific AWS Elemental MediaConnect flow.

    The content originator grants an entitlement to a specific AWS account (the subscriber). When an entitlement is granted, the subscriber can create a flow using the originator's flow as the source. Each flow can have up to 50 entitlements.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html
    :cloudformationResource: AWS::MediaConnect::FlowEntitlement
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
        
        cfn_flow_entitlement_props_mixin = mediaconnect_mixins.CfnFlowEntitlementPropsMixin(mediaconnect_mixins.CfnFlowEntitlementMixinProps(
            data_transfer_subscriber_fee_percent=123,
            description="description",
            encryption=mediaconnect_mixins.CfnFlowEntitlementPropsMixin.EncryptionProperty(
                algorithm="algorithm",
                constant_initialization_vector="constantInitializationVector",
                device_id="deviceId",
                key_type="keyType",
                region="region",
                resource_id="resourceId",
                role_arn="roleArn",
                secret_arn="secretArn",
                url="url"
            ),
            entitlement_status="entitlementStatus",
            flow_arn="flowArn",
            name="name",
            subscribers=["subscribers"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnFlowEntitlementMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaConnect::FlowEntitlement``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e8cf13e37d73b0520b47508cb4cf73a54a4ccffbd22d3cc2d9f8bac2f1215d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d217d988ec7825038c9f98e498f774e33a9a2c4fa05889ad24213906d972687a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac0e3f85f631380cdd4aafffa0932b0e71a0637d29e7facf6d46d98b45faf0d9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFlowEntitlementMixinProps:
        return typing.cast(CfnFlowEntitlementMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowEntitlementPropsMixin.EncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "algorithm": "algorithm",
            "constant_initialization_vector": "constantInitializationVector",
            "device_id": "deviceId",
            "key_type": "keyType",
            "region": "region",
            "resource_id": "resourceId",
            "role_arn": "roleArn",
            "secret_arn": "secretArn",
            "url": "url",
        },
    )
    class EncryptionProperty:
        def __init__(
            self,
            *,
            algorithm: typing.Optional[builtins.str] = None,
            constant_initialization_vector: typing.Optional[builtins.str] = None,
            device_id: typing.Optional[builtins.str] = None,
            key_type: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
            resource_id: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Encryption information.

            :param algorithm: The type of algorithm that is used for static key encryption (such as aes128, aes192, or aes256). If you are using SPEKE or SRT-password encryption, this property must be left blank.
            :param constant_initialization_vector: A 128-bit, 16-byte hex value represented by a 32-character string, to be used with the key for encrypting content. This parameter is not valid for static key encryption.
            :param device_id: The value of one of the devices that you configured with your digital rights management (DRM) platform key provider. This parameter is required for SPEKE encryption and is not valid for static key encryption.
            :param key_type: The type of key that is used for the encryption. If you don't specify a ``keyType`` value, the service uses the default setting ( ``static-key`` ). Valid key types are: ``static-key`` , ``speke`` , and ``srt-password`` . Default: - "static-key"
            :param region: The AWS Region that the API Gateway proxy endpoint was created in. This parameter is required for SPEKE encryption and is not valid for static key encryption.
            :param resource_id: An identifier for the content. The service sends this value to the key server to identify the current endpoint. The resource ID is also known as the content ID. This parameter is required for SPEKE encryption and is not valid for static key encryption.
            :param role_arn: The ARN of the role that you created during setup (when you set up MediaConnect as a trusted entity).
            :param secret_arn: The ARN of the secret that you created in AWS Secrets Manager to store the encryption key. This parameter is required for static key encryption and is not valid for SPEKE encryption.
            :param url: The URL from the API Gateway proxy that you set up to talk to your key server. This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowentitlement-encryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                encryption_property = mediaconnect_mixins.CfnFlowEntitlementPropsMixin.EncryptionProperty(
                    algorithm="algorithm",
                    constant_initialization_vector="constantInitializationVector",
                    device_id="deviceId",
                    key_type="keyType",
                    region="region",
                    resource_id="resourceId",
                    role_arn="roleArn",
                    secret_arn="secretArn",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__af5e8ff3e7351a544d74203bc709bbd87fe458302a6999bd56dc1fbccbb0f152)
                check_type(argname="argument algorithm", value=algorithm, expected_type=type_hints["algorithm"])
                check_type(argname="argument constant_initialization_vector", value=constant_initialization_vector, expected_type=type_hints["constant_initialization_vector"])
                check_type(argname="argument device_id", value=device_id, expected_type=type_hints["device_id"])
                check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
                check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if algorithm is not None:
                self._values["algorithm"] = algorithm
            if constant_initialization_vector is not None:
                self._values["constant_initialization_vector"] = constant_initialization_vector
            if device_id is not None:
                self._values["device_id"] = device_id
            if key_type is not None:
                self._values["key_type"] = key_type
            if region is not None:
                self._values["region"] = region
            if resource_id is not None:
                self._values["resource_id"] = resource_id
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def algorithm(self) -> typing.Optional[builtins.str]:
            '''The type of algorithm that is used for static key encryption (such as aes128, aes192, or aes256).

            If you are using SPEKE or SRT-password encryption, this property must be left blank.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowentitlement-encryption.html#cfn-mediaconnect-flowentitlement-encryption-algorithm
            '''
            result = self._values.get("algorithm")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def constant_initialization_vector(self) -> typing.Optional[builtins.str]:
            '''A 128-bit, 16-byte hex value represented by a 32-character string, to be used with the key for encrypting content.

            This parameter is not valid for static key encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowentitlement-encryption.html#cfn-mediaconnect-flowentitlement-encryption-constantinitializationvector
            '''
            result = self._values.get("constant_initialization_vector")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def device_id(self) -> typing.Optional[builtins.str]:
            '''The value of one of the devices that you configured with your digital rights management (DRM) platform key provider.

            This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowentitlement-encryption.html#cfn-mediaconnect-flowentitlement-encryption-deviceid
            '''
            result = self._values.get("device_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_type(self) -> typing.Optional[builtins.str]:
            '''The type of key that is used for the encryption.

            If you don't specify a ``keyType`` value, the service uses the default setting ( ``static-key`` ). Valid key types are: ``static-key`` , ``speke`` , and ``srt-password`` .

            :default: - "static-key"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowentitlement-encryption.html#cfn-mediaconnect-flowentitlement-encryption-keytype
            '''
            result = self._values.get("key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region that the API Gateway proxy endpoint was created in.

            This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowentitlement-encryption.html#cfn-mediaconnect-flowentitlement-encryption-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_id(self) -> typing.Optional[builtins.str]:
            '''An identifier for the content.

            The service sends this value to the key server to identify the current endpoint. The resource ID is also known as the content ID. This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowentitlement-encryption.html#cfn-mediaconnect-flowentitlement-encryption-resourceid
            '''
            result = self._values.get("resource_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the role that you created during setup (when you set up MediaConnect as a trusted entity).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowentitlement-encryption.html#cfn-mediaconnect-flowentitlement-encryption-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the secret that you created in AWS Secrets Manager to store the encryption key.

            This parameter is required for static key encryption and is not valid for SPEKE encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowentitlement-encryption.html#cfn-mediaconnect-flowentitlement-encryption-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL from the API Gateway proxy that you set up to talk to your key server.

            This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowentitlement-encryption.html#cfn-mediaconnect-flowentitlement-encryption-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zone": "availabilityZone",
        "flow_size": "flowSize",
        "maintenance": "maintenance",
        "media_streams": "mediaStreams",
        "name": "name",
        "ndi_config": "ndiConfig",
        "source": "source",
        "source_failover_config": "sourceFailoverConfig",
        "source_monitoring_config": "sourceMonitoringConfig",
        "vpc_interfaces": "vpcInterfaces",
    },
)
class CfnFlowMixinProps:
    def __init__(
        self,
        *,
        availability_zone: typing.Optional[builtins.str] = None,
        flow_size: typing.Optional[builtins.str] = None,
        maintenance: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.MaintenanceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        media_streams: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.MediaStreamProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        ndi_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.NdiConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.SourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        source_failover_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.FailoverConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        source_monitoring_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.SourceMonitoringConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_interfaces: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.VpcInterfaceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnFlowPropsMixin.

        :param availability_zone: The Availability Zone that you want to create the flow in. These options are limited to the Availability Zones within the current AWS Region.
        :param flow_size: Determines the processing capacity and feature set of the flow. Set this optional parameter to LARGE if you want to enable NDI outputs on the flow.
        :param maintenance: The maintenance settings you want to use for the flow.
        :param media_streams: The media streams that are associated with the flow. After you associate a media stream with a source, you can also associate it with outputs on the flow.
        :param name: The name of the flow.
        :param ndi_config: Specifies the configuration settings for NDI outputs. Required when the flow includes NDI outputs.
        :param source: The settings for the source that you want to use for the new flow.
        :param source_failover_config: The settings for source failover.
        :param source_monitoring_config: The settings for source monitoring.
        :param vpc_interfaces: The VPC Interfaces for this flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flow.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
            
            # automatic: Any
            
            cfn_flow_mixin_props = mediaconnect_mixins.CfnFlowMixinProps(
                availability_zone="availabilityZone",
                flow_size="flowSize",
                maintenance=mediaconnect_mixins.CfnFlowPropsMixin.MaintenanceProperty(
                    maintenance_day="maintenanceDay",
                    maintenance_start_hour="maintenanceStartHour"
                ),
                media_streams=[mediaconnect_mixins.CfnFlowPropsMixin.MediaStreamProperty(
                    attributes=mediaconnect_mixins.CfnFlowPropsMixin.MediaStreamAttributesProperty(
                        fmtp=mediaconnect_mixins.CfnFlowPropsMixin.FmtpProperty(
                            channel_order="channelOrder",
                            colorimetry="colorimetry",
                            exact_framerate="exactFramerate",
                            par="par",
                            range="range",
                            scan_mode="scanMode",
                            tcs="tcs"
                        ),
                        lang="lang"
                    ),
                    clock_rate=123,
                    description="description",
                    fmt=123,
                    media_stream_id=123,
                    media_stream_name="mediaStreamName",
                    media_stream_type="mediaStreamType",
                    video_format="videoFormat"
                )],
                name="name",
                ndi_config=mediaconnect_mixins.CfnFlowPropsMixin.NdiConfigProperty(
                    machine_name="machineName",
                    ndi_discovery_servers=[mediaconnect_mixins.CfnFlowPropsMixin.NdiDiscoveryServerConfigProperty(
                        discovery_server_address="discoveryServerAddress",
                        discovery_server_port=123,
                        vpc_interface_adapter="vpcInterfaceAdapter"
                    )],
                    ndi_state="ndiState"
                ),
                source=mediaconnect_mixins.CfnFlowPropsMixin.SourceProperty(
                    decryption=mediaconnect_mixins.CfnFlowPropsMixin.EncryptionProperty(
                        algorithm="algorithm",
                        constant_initialization_vector="constantInitializationVector",
                        device_id="deviceId",
                        key_type="keyType",
                        region="region",
                        resource_id="resourceId",
                        role_arn="roleArn",
                        secret_arn="secretArn",
                        url="url"
                    ),
                    description="description",
                    entitlement_arn="entitlementArn",
                    gateway_bridge_source=mediaconnect_mixins.CfnFlowPropsMixin.GatewayBridgeSourceProperty(
                        bridge_arn="bridgeArn",
                        vpc_interface_attachment=mediaconnect_mixins.CfnFlowPropsMixin.VpcInterfaceAttachmentProperty(
                            vpc_interface_name="vpcInterfaceName"
                        )
                    ),
                    ingest_ip="ingestIp",
                    ingest_port=123,
                    max_bitrate=123,
                    max_latency=123,
                    max_sync_buffer=123,
                    media_stream_source_configurations=[mediaconnect_mixins.CfnFlowPropsMixin.MediaStreamSourceConfigurationProperty(
                        encoding_name="encodingName",
                        input_configurations=[mediaconnect_mixins.CfnFlowPropsMixin.InputConfigurationProperty(
                            input_port=123,
                            interface=mediaconnect_mixins.CfnFlowPropsMixin.InterfaceProperty(
                                name="name"
                            )
                        )],
                        media_stream_name="mediaStreamName"
                    )],
                    min_latency=123,
                    name="name",
                    protocol="protocol",
                    router_integration_state="routerIntegrationState",
                    router_integration_transit_decryption=mediaconnect_mixins.CfnFlowPropsMixin.FlowTransitEncryptionProperty(
                        encryption_key_configuration=mediaconnect_mixins.CfnFlowPropsMixin.FlowTransitEncryptionKeyConfigurationProperty(
                            automatic=automatic,
                            secrets_manager=mediaconnect_mixins.CfnFlowPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                role_arn="roleArn",
                                secret_arn="secretArn"
                            )
                        ),
                        encryption_key_type="encryptionKeyType"
                    ),
                    sender_control_port=123,
                    sender_ip_address="senderIpAddress",
                    source_arn="sourceArn",
                    source_ingest_port="sourceIngestPort",
                    source_listener_address="sourceListenerAddress",
                    source_listener_port=123,
                    stream_id="streamId",
                    vpc_interface_name="vpcInterfaceName",
                    whitelist_cidr="whitelistCidr"
                ),
                source_failover_config=mediaconnect_mixins.CfnFlowPropsMixin.FailoverConfigProperty(
                    failover_mode="failoverMode",
                    recovery_window=123,
                    source_priority=mediaconnect_mixins.CfnFlowPropsMixin.SourcePriorityProperty(
                        primary_source="primarySource"
                    ),
                    state="state"
                ),
                source_monitoring_config=mediaconnect_mixins.CfnFlowPropsMixin.SourceMonitoringConfigProperty(
                    audio_monitoring_settings=[mediaconnect_mixins.CfnFlowPropsMixin.AudioMonitoringSettingProperty(
                        silent_audio=mediaconnect_mixins.CfnFlowPropsMixin.SilentAudioProperty(
                            state="state",
                            threshold_seconds=123
                        )
                    )],
                    content_quality_analysis_state="contentQualityAnalysisState",
                    thumbnail_state="thumbnailState",
                    video_monitoring_settings=[mediaconnect_mixins.CfnFlowPropsMixin.VideoMonitoringSettingProperty(
                        black_frames=mediaconnect_mixins.CfnFlowPropsMixin.BlackFramesProperty(
                            state="state",
                            threshold_seconds=123
                        ),
                        frozen_frames=mediaconnect_mixins.CfnFlowPropsMixin.FrozenFramesProperty(
                            state="state",
                            threshold_seconds=123
                        )
                    )]
                ),
                vpc_interfaces=[mediaconnect_mixins.CfnFlowPropsMixin.VpcInterfaceProperty(
                    name="name",
                    network_interface_ids=["networkInterfaceIds"],
                    network_interface_type="networkInterfaceType",
                    role_arn="roleArn",
                    security_group_ids=["securityGroupIds"],
                    subnet_id="subnetId"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1ab6f643ff2ee011a1d639636ec8318de1c2af09010d6734a473ae8288bd2db)
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument flow_size", value=flow_size, expected_type=type_hints["flow_size"])
            check_type(argname="argument maintenance", value=maintenance, expected_type=type_hints["maintenance"])
            check_type(argname="argument media_streams", value=media_streams, expected_type=type_hints["media_streams"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ndi_config", value=ndi_config, expected_type=type_hints["ndi_config"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument source_failover_config", value=source_failover_config, expected_type=type_hints["source_failover_config"])
            check_type(argname="argument source_monitoring_config", value=source_monitoring_config, expected_type=type_hints["source_monitoring_config"])
            check_type(argname="argument vpc_interfaces", value=vpc_interfaces, expected_type=type_hints["vpc_interfaces"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if flow_size is not None:
            self._values["flow_size"] = flow_size
        if maintenance is not None:
            self._values["maintenance"] = maintenance
        if media_streams is not None:
            self._values["media_streams"] = media_streams
        if name is not None:
            self._values["name"] = name
        if ndi_config is not None:
            self._values["ndi_config"] = ndi_config
        if source is not None:
            self._values["source"] = source
        if source_failover_config is not None:
            self._values["source_failover_config"] = source_failover_config
        if source_monitoring_config is not None:
            self._values["source_monitoring_config"] = source_monitoring_config
        if vpc_interfaces is not None:
            self._values["vpc_interfaces"] = vpc_interfaces

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''The Availability Zone that you want to create the flow in.

        These options are limited to the Availability Zones within the current AWS Region.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flow.html#cfn-mediaconnect-flow-availabilityzone
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flow_size(self) -> typing.Optional[builtins.str]:
        '''Determines the processing capacity and feature set of the flow.

        Set this optional parameter to LARGE if you want to enable NDI outputs on the flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flow.html#cfn-mediaconnect-flow-flowsize
        '''
        result = self._values.get("flow_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.MaintenanceProperty"]]:
        '''The maintenance settings you want to use for the flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flow.html#cfn-mediaconnect-flow-maintenance
        '''
        result = self._values.get("maintenance")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.MaintenanceProperty"]], result)

    @builtins.property
    def media_streams(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.MediaStreamProperty"]]]]:
        '''The media streams that are associated with the flow.

        After you associate a media stream with a source, you can also associate it with outputs on the flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flow.html#cfn-mediaconnect-flow-mediastreams
        '''
        result = self._values.get("media_streams")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.MediaStreamProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flow.html#cfn-mediaconnect-flow-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ndi_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.NdiConfigProperty"]]:
        '''Specifies the configuration settings for NDI outputs.

        Required when the flow includes NDI outputs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flow.html#cfn-mediaconnect-flow-ndiconfig
        '''
        result = self._values.get("ndi_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.NdiConfigProperty"]], result)

    @builtins.property
    def source(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SourceProperty"]]:
        '''The settings for the source that you want to use for the new flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flow.html#cfn-mediaconnect-flow-source
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SourceProperty"]], result)

    @builtins.property
    def source_failover_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.FailoverConfigProperty"]]:
        '''The settings for source failover.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flow.html#cfn-mediaconnect-flow-sourcefailoverconfig
        '''
        result = self._values.get("source_failover_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.FailoverConfigProperty"]], result)

    @builtins.property
    def source_monitoring_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SourceMonitoringConfigProperty"]]:
        '''The settings for source monitoring.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flow.html#cfn-mediaconnect-flow-sourcemonitoringconfig
        '''
        result = self._values.get("source_monitoring_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SourceMonitoringConfigProperty"]], result)

    @builtins.property
    def vpc_interfaces(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.VpcInterfaceProperty"]]]]:
        '''The VPC Interfaces for this flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flow.html#cfn-mediaconnect-flow-vpcinterfaces
        '''
        result = self._values.get("vpc_interfaces")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.VpcInterfaceProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFlowMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowOutputMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "cidr_allow_list": "cidrAllowList",
        "description": "description",
        "destination": "destination",
        "encryption": "encryption",
        "flow_arn": "flowArn",
        "max_latency": "maxLatency",
        "media_stream_output_configurations": "mediaStreamOutputConfigurations",
        "min_latency": "minLatency",
        "name": "name",
        "ndi_program_name": "ndiProgramName",
        "ndi_speed_hq_quality": "ndiSpeedHqQuality",
        "output_status": "outputStatus",
        "port": "port",
        "protocol": "protocol",
        "remote_id": "remoteId",
        "router_integration_state": "routerIntegrationState",
        "router_integration_transit_encryption": "routerIntegrationTransitEncryption",
        "smoothing_latency": "smoothingLatency",
        "stream_id": "streamId",
        "vpc_interface_attachment": "vpcInterfaceAttachment",
    },
)
class CfnFlowOutputMixinProps:
    def __init__(
        self,
        *,
        cidr_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        destination: typing.Optional[builtins.str] = None,
        encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowOutputPropsMixin.EncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        flow_arn: typing.Optional[builtins.str] = None,
        max_latency: typing.Optional[jsii.Number] = None,
        media_stream_output_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowOutputPropsMixin.MediaStreamOutputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        min_latency: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        ndi_program_name: typing.Optional[builtins.str] = None,
        ndi_speed_hq_quality: typing.Optional[jsii.Number] = None,
        output_status: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[builtins.str] = None,
        remote_id: typing.Optional[builtins.str] = None,
        router_integration_state: typing.Optional[builtins.str] = None,
        router_integration_transit_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowOutputPropsMixin.FlowTransitEncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        smoothing_latency: typing.Optional[jsii.Number] = None,
        stream_id: typing.Optional[builtins.str] = None,
        vpc_interface_attachment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowOutputPropsMixin.VpcInterfaceAttachmentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnFlowOutputPropsMixin.

        :param cidr_allow_list: The range of IP addresses that should be allowed to initiate output requests to this flow. These IP addresses should be in the form of a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16.
        :param description: A description of the output. This description appears only on the MediaConnect console and will not be seen by the end user.
        :param destination: The IP address where you want to send the output.
        :param encryption: The type of key used for the encryption. If no ``keyType`` is provided, the service will use the default setting (static-key). Allowable encryption types: static-key.
        :param flow_arn: The Amazon Resource Name (ARN) of the flow this output is attached to.
        :param max_latency: The maximum latency in milliseconds. This parameter applies only to RIST-based and Zixi-based streams.
        :param media_stream_output_configurations: The media streams that are associated with the output, and the parameters for those associations.
        :param min_latency: The minimum latency in milliseconds for SRT-based streams. In streams that use the SRT protocol, this value that you set on your MediaConnect source or output represents the minimal potential latency of that connection. The latency of the stream is set to the highest number between the sender’s minimum latency and the receiver’s minimum latency.
        :param name: The name of the bridge's output.
        :param ndi_program_name: A suffix for the names of the NDI sources that the flow creates. If a custom name isn't specified, MediaConnect uses the output name.
        :param ndi_speed_hq_quality: A quality setting for the NDI Speed HQ encoder.
        :param output_status: An indication of whether the output should transmit data or not.
        :param port: The port to use when content is distributed to this output.
        :param protocol: The protocol to use for the output. .. epigraph:: AWS Elemental MediaConnect no longer supports the Fujitsu QoS protocol. This reference is maintained for legacy purposes only.
        :param remote_id: The remote ID for the Zixi-pull stream.
        :param router_integration_state: 
        :param router_integration_transit_encryption: Encryption information.
        :param smoothing_latency: The smoothing latency in milliseconds for RIST, RTP, and RTP-FEC streams.
        :param stream_id: The stream ID that you want to use for this transport. This parameter applies only to Zixi and SRT caller-based streams.
        :param vpc_interface_attachment: The name of the VPC interface attachment to use for this output.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
            
            # automatic: Any
            
            cfn_flow_output_mixin_props = mediaconnect_mixins.CfnFlowOutputMixinProps(
                cidr_allow_list=["cidrAllowList"],
                description="description",
                destination="destination",
                encryption=mediaconnect_mixins.CfnFlowOutputPropsMixin.EncryptionProperty(
                    algorithm="algorithm",
                    key_type="keyType",
                    role_arn="roleArn",
                    secret_arn="secretArn"
                ),
                flow_arn="flowArn",
                max_latency=123,
                media_stream_output_configurations=[mediaconnect_mixins.CfnFlowOutputPropsMixin.MediaStreamOutputConfigurationProperty(
                    destination_configurations=[mediaconnect_mixins.CfnFlowOutputPropsMixin.DestinationConfigurationProperty(
                        destination_ip="destinationIp",
                        destination_port=123,
                        interface=mediaconnect_mixins.CfnFlowOutputPropsMixin.InterfaceProperty(
                            name="name"
                        )
                    )],
                    encoding_name="encodingName",
                    encoding_parameters=mediaconnect_mixins.CfnFlowOutputPropsMixin.EncodingParametersProperty(
                        compression_factor=123,
                        encoder_profile="encoderProfile"
                    ),
                    media_stream_name="mediaStreamName"
                )],
                min_latency=123,
                name="name",
                ndi_program_name="ndiProgramName",
                ndi_speed_hq_quality=123,
                output_status="outputStatus",
                port=123,
                protocol="protocol",
                remote_id="remoteId",
                router_integration_state="routerIntegrationState",
                router_integration_transit_encryption=mediaconnect_mixins.CfnFlowOutputPropsMixin.FlowTransitEncryptionProperty(
                    encryption_key_configuration=mediaconnect_mixins.CfnFlowOutputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty(
                        automatic=automatic,
                        secrets_manager=mediaconnect_mixins.CfnFlowOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                            role_arn="roleArn",
                            secret_arn="secretArn"
                        )
                    ),
                    encryption_key_type="encryptionKeyType"
                ),
                smoothing_latency=123,
                stream_id="streamId",
                vpc_interface_attachment=mediaconnect_mixins.CfnFlowOutputPropsMixin.VpcInterfaceAttachmentProperty(
                    vpc_interface_name="vpcInterfaceName"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95adaf5540d02a8cdd782f2326950c0489c4bf372cfc5d2930a1313edf67854b)
            check_type(argname="argument cidr_allow_list", value=cidr_allow_list, expected_type=type_hints["cidr_allow_list"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument flow_arn", value=flow_arn, expected_type=type_hints["flow_arn"])
            check_type(argname="argument max_latency", value=max_latency, expected_type=type_hints["max_latency"])
            check_type(argname="argument media_stream_output_configurations", value=media_stream_output_configurations, expected_type=type_hints["media_stream_output_configurations"])
            check_type(argname="argument min_latency", value=min_latency, expected_type=type_hints["min_latency"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ndi_program_name", value=ndi_program_name, expected_type=type_hints["ndi_program_name"])
            check_type(argname="argument ndi_speed_hq_quality", value=ndi_speed_hq_quality, expected_type=type_hints["ndi_speed_hq_quality"])
            check_type(argname="argument output_status", value=output_status, expected_type=type_hints["output_status"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument remote_id", value=remote_id, expected_type=type_hints["remote_id"])
            check_type(argname="argument router_integration_state", value=router_integration_state, expected_type=type_hints["router_integration_state"])
            check_type(argname="argument router_integration_transit_encryption", value=router_integration_transit_encryption, expected_type=type_hints["router_integration_transit_encryption"])
            check_type(argname="argument smoothing_latency", value=smoothing_latency, expected_type=type_hints["smoothing_latency"])
            check_type(argname="argument stream_id", value=stream_id, expected_type=type_hints["stream_id"])
            check_type(argname="argument vpc_interface_attachment", value=vpc_interface_attachment, expected_type=type_hints["vpc_interface_attachment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cidr_allow_list is not None:
            self._values["cidr_allow_list"] = cidr_allow_list
        if description is not None:
            self._values["description"] = description
        if destination is not None:
            self._values["destination"] = destination
        if encryption is not None:
            self._values["encryption"] = encryption
        if flow_arn is not None:
            self._values["flow_arn"] = flow_arn
        if max_latency is not None:
            self._values["max_latency"] = max_latency
        if media_stream_output_configurations is not None:
            self._values["media_stream_output_configurations"] = media_stream_output_configurations
        if min_latency is not None:
            self._values["min_latency"] = min_latency
        if name is not None:
            self._values["name"] = name
        if ndi_program_name is not None:
            self._values["ndi_program_name"] = ndi_program_name
        if ndi_speed_hq_quality is not None:
            self._values["ndi_speed_hq_quality"] = ndi_speed_hq_quality
        if output_status is not None:
            self._values["output_status"] = output_status
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if remote_id is not None:
            self._values["remote_id"] = remote_id
        if router_integration_state is not None:
            self._values["router_integration_state"] = router_integration_state
        if router_integration_transit_encryption is not None:
            self._values["router_integration_transit_encryption"] = router_integration_transit_encryption
        if smoothing_latency is not None:
            self._values["smoothing_latency"] = smoothing_latency
        if stream_id is not None:
            self._values["stream_id"] = stream_id
        if vpc_interface_attachment is not None:
            self._values["vpc_interface_attachment"] = vpc_interface_attachment

    @builtins.property
    def cidr_allow_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The range of IP addresses that should be allowed to initiate output requests to this flow.

        These IP addresses should be in the form of a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-cidrallowlist
        '''
        result = self._values.get("cidr_allow_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the output.

        This description appears only on the MediaConnect console and will not be seen by the end user.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination(self) -> typing.Optional[builtins.str]:
        '''The IP address where you want to send the output.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-destination
        '''
        result = self._values.get("destination")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowOutputPropsMixin.EncryptionProperty"]]:
        '''The type of key used for the encryption.

        If no ``keyType`` is provided, the service will use the default setting (static-key). Allowable encryption types: static-key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-encryption
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowOutputPropsMixin.EncryptionProperty"]], result)

    @builtins.property
    def flow_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the flow this output is attached to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-flowarn
        '''
        result = self._values.get("flow_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_latency(self) -> typing.Optional[jsii.Number]:
        '''The maximum latency in milliseconds.

        This parameter applies only to RIST-based and Zixi-based streams.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-maxlatency
        '''
        result = self._values.get("max_latency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def media_stream_output_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowOutputPropsMixin.MediaStreamOutputConfigurationProperty"]]]]:
        '''The media streams that are associated with the output, and the parameters for those associations.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-mediastreamoutputconfigurations
        '''
        result = self._values.get("media_stream_output_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowOutputPropsMixin.MediaStreamOutputConfigurationProperty"]]]], result)

    @builtins.property
    def min_latency(self) -> typing.Optional[jsii.Number]:
        '''The minimum latency in milliseconds for SRT-based streams.

        In streams that use the SRT protocol, this value that you set on your MediaConnect source or output represents the minimal potential latency of that connection. The latency of the stream is set to the highest number between the sender’s minimum latency and the receiver’s minimum latency.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-minlatency
        '''
        result = self._values.get("min_latency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the bridge's output.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ndi_program_name(self) -> typing.Optional[builtins.str]:
        '''A suffix for the names of the NDI sources that the flow creates.

        If a custom name isn't specified, MediaConnect uses the output name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-ndiprogramname
        '''
        result = self._values.get("ndi_program_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ndi_speed_hq_quality(self) -> typing.Optional[jsii.Number]:
        '''A quality setting for the NDI Speed HQ encoder.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-ndispeedhqquality
        '''
        result = self._values.get("ndi_speed_hq_quality")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def output_status(self) -> typing.Optional[builtins.str]:
        '''An indication of whether the output should transmit data or not.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-outputstatus
        '''
        result = self._values.get("output_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port to use when content is distributed to this output.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''The protocol to use for the output.

        .. epigraph::

           AWS Elemental MediaConnect no longer supports the Fujitsu QoS protocol. This reference is maintained for legacy purposes only.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-protocol
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_id(self) -> typing.Optional[builtins.str]:
        '''The remote ID for the Zixi-pull stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-remoteid
        '''
        result = self._values.get("remote_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def router_integration_state(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-routerintegrationstate
        '''
        result = self._values.get("router_integration_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def router_integration_transit_encryption(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowOutputPropsMixin.FlowTransitEncryptionProperty"]]:
        '''Encryption information.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-routerintegrationtransitencryption
        '''
        result = self._values.get("router_integration_transit_encryption")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowOutputPropsMixin.FlowTransitEncryptionProperty"]], result)

    @builtins.property
    def smoothing_latency(self) -> typing.Optional[jsii.Number]:
        '''The smoothing latency in milliseconds for RIST, RTP, and RTP-FEC streams.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-smoothinglatency
        '''
        result = self._values.get("smoothing_latency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def stream_id(self) -> typing.Optional[builtins.str]:
        '''The stream ID that you want to use for this transport.

        This parameter applies only to Zixi and SRT caller-based streams.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-streamid
        '''
        result = self._values.get("stream_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_interface_attachment(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowOutputPropsMixin.VpcInterfaceAttachmentProperty"]]:
        '''The name of the VPC interface attachment to use for this output.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-vpcinterfaceattachment
        '''
        result = self._values.get("vpc_interface_attachment")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowOutputPropsMixin.VpcInterfaceAttachmentProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFlowOutputMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFlowOutputPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowOutputPropsMixin",
):
    '''The ``AWS::MediaConnect::FlowOutput`` resource defines the destination address, protocol, and port that AWS Elemental MediaConnect sends the ingested video to.

    Each flow can have up to 50 outputs. An output can have the same protocol or a different protocol from the source. The following protocols are supported: RIST, RTP, RTP-FEC, SRT-listener, SRT-caller, Zixi pull, and Zixi push. CDI and ST 2110 JPEG XS protocols are not currently supported by AWS CloudFormation.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html
    :cloudformationResource: AWS::MediaConnect::FlowOutput
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
        
        # automatic: Any
        
        cfn_flow_output_props_mixin = mediaconnect_mixins.CfnFlowOutputPropsMixin(mediaconnect_mixins.CfnFlowOutputMixinProps(
            cidr_allow_list=["cidrAllowList"],
            description="description",
            destination="destination",
            encryption=mediaconnect_mixins.CfnFlowOutputPropsMixin.EncryptionProperty(
                algorithm="algorithm",
                key_type="keyType",
                role_arn="roleArn",
                secret_arn="secretArn"
            ),
            flow_arn="flowArn",
            max_latency=123,
            media_stream_output_configurations=[mediaconnect_mixins.CfnFlowOutputPropsMixin.MediaStreamOutputConfigurationProperty(
                destination_configurations=[mediaconnect_mixins.CfnFlowOutputPropsMixin.DestinationConfigurationProperty(
                    destination_ip="destinationIp",
                    destination_port=123,
                    interface=mediaconnect_mixins.CfnFlowOutputPropsMixin.InterfaceProperty(
                        name="name"
                    )
                )],
                encoding_name="encodingName",
                encoding_parameters=mediaconnect_mixins.CfnFlowOutputPropsMixin.EncodingParametersProperty(
                    compression_factor=123,
                    encoder_profile="encoderProfile"
                ),
                media_stream_name="mediaStreamName"
            )],
            min_latency=123,
            name="name",
            ndi_program_name="ndiProgramName",
            ndi_speed_hq_quality=123,
            output_status="outputStatus",
            port=123,
            protocol="protocol",
            remote_id="remoteId",
            router_integration_state="routerIntegrationState",
            router_integration_transit_encryption=mediaconnect_mixins.CfnFlowOutputPropsMixin.FlowTransitEncryptionProperty(
                encryption_key_configuration=mediaconnect_mixins.CfnFlowOutputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty(
                    automatic=automatic,
                    secrets_manager=mediaconnect_mixins.CfnFlowOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                        role_arn="roleArn",
                        secret_arn="secretArn"
                    )
                ),
                encryption_key_type="encryptionKeyType"
            ),
            smoothing_latency=123,
            stream_id="streamId",
            vpc_interface_attachment=mediaconnect_mixins.CfnFlowOutputPropsMixin.VpcInterfaceAttachmentProperty(
                vpc_interface_name="vpcInterfaceName"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnFlowOutputMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaConnect::FlowOutput``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0d7ff33cdafdecaa6e84e984fb62b54c127ca01a284adfe2111df877b310b30)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e678320e27a19c95530bf123f5108c71c221f2b2a6b69ca7aa01931e6232327)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcd02657ae75bf8aec8547ed1f57a7d3e6e8a96295422a7d39ca187a4b189805)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFlowOutputMixinProps:
        return typing.cast(CfnFlowOutputMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowOutputPropsMixin.DestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_ip": "destinationIp",
            "destination_port": "destinationPort",
            "interface": "interface",
        },
    )
    class DestinationConfigurationProperty:
        def __init__(
            self,
            *,
            destination_ip: typing.Optional[builtins.str] = None,
            destination_port: typing.Optional[jsii.Number] = None,
            interface: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowOutputPropsMixin.InterfaceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The transport parameters that you want to associate with an outbound media stream.

            :param destination_ip: The IP address where you want MediaConnect to send contents of the media stream.
            :param destination_port: The port that you want MediaConnect to use when it distributes the media stream to the output.
            :param interface: The VPC interface that you want to use for the media stream associated with the output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-destinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                destination_configuration_property = mediaconnect_mixins.CfnFlowOutputPropsMixin.DestinationConfigurationProperty(
                    destination_ip="destinationIp",
                    destination_port=123,
                    interface=mediaconnect_mixins.CfnFlowOutputPropsMixin.InterfaceProperty(
                        name="name"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c5ecfec787514d467ed2f974d0ca3e8bc4f38f5b52afb7110b9f539b97db457)
                check_type(argname="argument destination_ip", value=destination_ip, expected_type=type_hints["destination_ip"])
                check_type(argname="argument destination_port", value=destination_port, expected_type=type_hints["destination_port"])
                check_type(argname="argument interface", value=interface, expected_type=type_hints["interface"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_ip is not None:
                self._values["destination_ip"] = destination_ip
            if destination_port is not None:
                self._values["destination_port"] = destination_port
            if interface is not None:
                self._values["interface"] = interface

        @builtins.property
        def destination_ip(self) -> typing.Optional[builtins.str]:
            '''The IP address where you want MediaConnect to send contents of the media stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-destinationconfiguration.html#cfn-mediaconnect-flowoutput-destinationconfiguration-destinationip
            '''
            result = self._values.get("destination_ip")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def destination_port(self) -> typing.Optional[jsii.Number]:
            '''The port that you want MediaConnect to use when it distributes the media stream to the output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-destinationconfiguration.html#cfn-mediaconnect-flowoutput-destinationconfiguration-destinationport
            '''
            result = self._values.get("destination_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interface(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowOutputPropsMixin.InterfaceProperty"]]:
            '''The VPC interface that you want to use for the media stream associated with the output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-destinationconfiguration.html#cfn-mediaconnect-flowoutput-destinationconfiguration-interface
            '''
            result = self._values.get("interface")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowOutputPropsMixin.InterfaceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowOutputPropsMixin.EncodingParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "compression_factor": "compressionFactor",
            "encoder_profile": "encoderProfile",
        },
    )
    class EncodingParametersProperty:
        def __init__(
            self,
            *,
            compression_factor: typing.Optional[jsii.Number] = None,
            encoder_profile: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A collection of parameters that determine how MediaConnect will convert the content.

            These fields only apply to outputs on flows that have a CDI source.

            :param compression_factor: A value that is used to calculate compression for an output. The bitrate of the output is calculated as follows: Output bitrate = (1 / compressionFactor) * (source bitrate) This property only applies to outputs that use the ST 2110 JPEG XS protocol, with a flow source that uses the CDI protocol. Valid values are floating point numbers in the range of 3.0 to 10.0, inclusive.
            :param encoder_profile: A setting on the encoder that drives compression settings. This property only applies to video media streams associated with outputs that use the ST 2110 JPEG XS protocol, with a flow source that uses the CDI protocol.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-encodingparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                encoding_parameters_property = mediaconnect_mixins.CfnFlowOutputPropsMixin.EncodingParametersProperty(
                    compression_factor=123,
                    encoder_profile="encoderProfile"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f0c4f63e002f285345aa32f3922e4babb2798e0c803ca36db6f84299752088a5)
                check_type(argname="argument compression_factor", value=compression_factor, expected_type=type_hints["compression_factor"])
                check_type(argname="argument encoder_profile", value=encoder_profile, expected_type=type_hints["encoder_profile"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if compression_factor is not None:
                self._values["compression_factor"] = compression_factor
            if encoder_profile is not None:
                self._values["encoder_profile"] = encoder_profile

        @builtins.property
        def compression_factor(self) -> typing.Optional[jsii.Number]:
            '''A value that is used to calculate compression for an output.

            The bitrate of the output is calculated as follows: Output bitrate = (1 / compressionFactor) * (source bitrate) This property only applies to outputs that use the ST 2110 JPEG XS protocol, with a flow source that uses the CDI protocol. Valid values are floating point numbers in the range of 3.0 to 10.0, inclusive.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-encodingparameters.html#cfn-mediaconnect-flowoutput-encodingparameters-compressionfactor
            '''
            result = self._values.get("compression_factor")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def encoder_profile(self) -> typing.Optional[builtins.str]:
            '''A setting on the encoder that drives compression settings.

            This property only applies to video media streams associated with outputs that use the ST 2110 JPEG XS protocol, with a flow source that uses the CDI protocol.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-encodingparameters.html#cfn-mediaconnect-flowoutput-encodingparameters-encoderprofile
            '''
            result = self._values.get("encoder_profile")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncodingParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowOutputPropsMixin.EncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "algorithm": "algorithm",
            "key_type": "keyType",
            "role_arn": "roleArn",
            "secret_arn": "secretArn",
        },
    )
    class EncryptionProperty:
        def __init__(
            self,
            *,
            algorithm: typing.Optional[builtins.str] = None,
            key_type: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Encryption information.

            :param algorithm: The type of algorithm that is used for static key encryption (such as aes128, aes192, or aes256). If you are using SPEKE or SRT-password encryption, this property must be left blank.
            :param key_type: The type of key that is used for the encryption. If you don't specify a ``keyType`` value, the service uses the default setting ( ``static-key`` ). Valid key types are: ``static-key`` , ``speke`` , and ``srt-password`` . Default: - "static-key"
            :param role_arn: The ARN of the role that you created during setup (when you set up MediaConnect as a trusted entity).
            :param secret_arn: The ARN of the secret that you created in AWS Secrets Manager to store the encryption key. This parameter is required for static key encryption and is not valid for SPEKE encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-encryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                encryption_property = mediaconnect_mixins.CfnFlowOutputPropsMixin.EncryptionProperty(
                    algorithm="algorithm",
                    key_type="keyType",
                    role_arn="roleArn",
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a64610f76161f83342d54359dfa50ab33de6cc510f4e32d8a7858faa9b775e00)
                check_type(argname="argument algorithm", value=algorithm, expected_type=type_hints["algorithm"])
                check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if algorithm is not None:
                self._values["algorithm"] = algorithm
            if key_type is not None:
                self._values["key_type"] = key_type
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def algorithm(self) -> typing.Optional[builtins.str]:
            '''The type of algorithm that is used for static key encryption (such as aes128, aes192, or aes256).

            If you are using SPEKE or SRT-password encryption, this property must be left blank.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-encryption.html#cfn-mediaconnect-flowoutput-encryption-algorithm
            '''
            result = self._values.get("algorithm")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_type(self) -> typing.Optional[builtins.str]:
            '''The type of key that is used for the encryption.

            If you don't specify a ``keyType`` value, the service uses the default setting ( ``static-key`` ). Valid key types are: ``static-key`` , ``speke`` , and ``srt-password`` .

            :default: - "static-key"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-encryption.html#cfn-mediaconnect-flowoutput-encryption-keytype
            '''
            result = self._values.get("key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the role that you created during setup (when you set up MediaConnect as a trusted entity).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-encryption.html#cfn-mediaconnect-flowoutput-encryption-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the secret that you created in AWS Secrets Manager to store the encryption key.

            This parameter is required for static key encryption and is not valid for SPEKE encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-encryption.html#cfn-mediaconnect-flowoutput-encryption-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowOutputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"automatic": "automatic", "secrets_manager": "secretsManager"},
    )
    class FlowTransitEncryptionKeyConfigurationProperty:
        def __init__(
            self,
            *,
            automatic: typing.Any = None,
            secrets_manager: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param automatic: Configuration settings for automatic encryption key management, where MediaConnect handles key creation and rotation.
            :param secrets_manager: The configuration settings for transit encryption of a flow output using AWS Secrets Manager, including the secret ARN and role ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-flowtransitencryptionkeyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                # automatic: Any
                
                flow_transit_encryption_key_configuration_property = mediaconnect_mixins.CfnFlowOutputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty(
                    automatic=automatic,
                    secrets_manager=mediaconnect_mixins.CfnFlowOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                        role_arn="roleArn",
                        secret_arn="secretArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__581c68310c5af0bb94de31b54e3b8ebd0e377140830e1378b0b140087aabc5d2)
                check_type(argname="argument automatic", value=automatic, expected_type=type_hints["automatic"])
                check_type(argname="argument secrets_manager", value=secrets_manager, expected_type=type_hints["secrets_manager"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if automatic is not None:
                self._values["automatic"] = automatic
            if secrets_manager is not None:
                self._values["secrets_manager"] = secrets_manager

        @builtins.property
        def automatic(self) -> typing.Any:
            '''Configuration settings for automatic encryption key management, where MediaConnect handles key creation and rotation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-flowtransitencryptionkeyconfiguration.html#cfn-mediaconnect-flowoutput-flowtransitencryptionkeyconfiguration-automatic
            '''
            result = self._values.get("automatic")
            return typing.cast(typing.Any, result)

        @builtins.property
        def secrets_manager(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty"]]:
            '''The configuration settings for transit encryption of a flow output using AWS Secrets Manager, including the secret ARN and role ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-flowtransitencryptionkeyconfiguration.html#cfn-mediaconnect-flowoutput-flowtransitencryptionkeyconfiguration-secretsmanager
            '''
            result = self._values.get("secrets_manager")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FlowTransitEncryptionKeyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowOutputPropsMixin.FlowTransitEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption_key_configuration": "encryptionKeyConfiguration",
            "encryption_key_type": "encryptionKeyType",
        },
    )
    class FlowTransitEncryptionProperty:
        def __init__(
            self,
            *,
            encryption_key_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowOutputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            encryption_key_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration that defines how content is encrypted during transit between the MediaConnect router and a MediaConnect flow.

            :param encryption_key_configuration: Configuration settings for flow transit encryption keys.
            :param encryption_key_type: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-flowtransitencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                # automatic: Any
                
                flow_transit_encryption_property = mediaconnect_mixins.CfnFlowOutputPropsMixin.FlowTransitEncryptionProperty(
                    encryption_key_configuration=mediaconnect_mixins.CfnFlowOutputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty(
                        automatic=automatic,
                        secrets_manager=mediaconnect_mixins.CfnFlowOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                            role_arn="roleArn",
                            secret_arn="secretArn"
                        )
                    ),
                    encryption_key_type="encryptionKeyType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6b0905ce6aede6e9bd0e0ba79675d47f51b4aee97faf7007f7600ee4105555e5)
                check_type(argname="argument encryption_key_configuration", value=encryption_key_configuration, expected_type=type_hints["encryption_key_configuration"])
                check_type(argname="argument encryption_key_type", value=encryption_key_type, expected_type=type_hints["encryption_key_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_key_configuration is not None:
                self._values["encryption_key_configuration"] = encryption_key_configuration
            if encryption_key_type is not None:
                self._values["encryption_key_type"] = encryption_key_type

        @builtins.property
        def encryption_key_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowOutputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty"]]:
            '''Configuration settings for flow transit encryption keys.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-flowtransitencryption.html#cfn-mediaconnect-flowoutput-flowtransitencryption-encryptionkeyconfiguration
            '''
            result = self._values.get("encryption_key_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowOutputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty"]], result)

        @builtins.property
        def encryption_key_type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-flowtransitencryption.html#cfn-mediaconnect-flowoutput-flowtransitencryption-encryptionkeytype
            '''
            result = self._values.get("encryption_key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FlowTransitEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowOutputPropsMixin.InterfaceProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class InterfaceProperty:
        def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
            '''The VPC interface that is used for the media stream associated with the source or output.

            :param name: The name of the VPC interface.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-interface.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                interface_property = mediaconnect_mixins.CfnFlowOutputPropsMixin.InterfaceProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4b15b112f22d97a5cf7066d9024f76b0ec8619e5e297002f09e85214e14f565e)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the VPC interface.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-interface.html#cfn-mediaconnect-flowoutput-interface-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InterfaceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowOutputPropsMixin.MediaStreamOutputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_configurations": "destinationConfigurations",
            "encoding_name": "encodingName",
            "encoding_parameters": "encodingParameters",
            "media_stream_name": "mediaStreamName",
        },
    )
    class MediaStreamOutputConfigurationProperty:
        def __init__(
            self,
            *,
            destination_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowOutputPropsMixin.DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            encoding_name: typing.Optional[builtins.str] = None,
            encoding_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowOutputPropsMixin.EncodingParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            media_stream_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The media stream that is associated with the output, and the parameters for that association.

            :param destination_configurations: The transport parameters that are associated with each outbound media stream.
            :param encoding_name: The format that was used to encode the data. For ancillary data streams, set the encoding name to smpte291. For audio streams, set the encoding name to pcm. For video, 2110 streams, set the encoding name to raw. For video, JPEG XS streams, set the encoding name to jxsv.
            :param encoding_parameters: A collection of parameters that determine how MediaConnect will convert the content. These fields only apply to outputs on flows that have a CDI source.
            :param media_stream_name: The name of the media stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-mediastreamoutputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                media_stream_output_configuration_property = mediaconnect_mixins.CfnFlowOutputPropsMixin.MediaStreamOutputConfigurationProperty(
                    destination_configurations=[mediaconnect_mixins.CfnFlowOutputPropsMixin.DestinationConfigurationProperty(
                        destination_ip="destinationIp",
                        destination_port=123,
                        interface=mediaconnect_mixins.CfnFlowOutputPropsMixin.InterfaceProperty(
                            name="name"
                        )
                    )],
                    encoding_name="encodingName",
                    encoding_parameters=mediaconnect_mixins.CfnFlowOutputPropsMixin.EncodingParametersProperty(
                        compression_factor=123,
                        encoder_profile="encoderProfile"
                    ),
                    media_stream_name="mediaStreamName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9e3941641a31f12837c0098a9543e75085bf8617cd9eb91eff32de22e4c200a3)
                check_type(argname="argument destination_configurations", value=destination_configurations, expected_type=type_hints["destination_configurations"])
                check_type(argname="argument encoding_name", value=encoding_name, expected_type=type_hints["encoding_name"])
                check_type(argname="argument encoding_parameters", value=encoding_parameters, expected_type=type_hints["encoding_parameters"])
                check_type(argname="argument media_stream_name", value=media_stream_name, expected_type=type_hints["media_stream_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_configurations is not None:
                self._values["destination_configurations"] = destination_configurations
            if encoding_name is not None:
                self._values["encoding_name"] = encoding_name
            if encoding_parameters is not None:
                self._values["encoding_parameters"] = encoding_parameters
            if media_stream_name is not None:
                self._values["media_stream_name"] = media_stream_name

        @builtins.property
        def destination_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowOutputPropsMixin.DestinationConfigurationProperty"]]]]:
            '''The transport parameters that are associated with each outbound media stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-mediastreamoutputconfiguration.html#cfn-mediaconnect-flowoutput-mediastreamoutputconfiguration-destinationconfigurations
            '''
            result = self._values.get("destination_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowOutputPropsMixin.DestinationConfigurationProperty"]]]], result)

        @builtins.property
        def encoding_name(self) -> typing.Optional[builtins.str]:
            '''The format that was used to encode the data.

            For ancillary data streams, set the encoding name to smpte291. For audio streams, set the encoding name to pcm. For video, 2110 streams, set the encoding name to raw. For video, JPEG XS streams, set the encoding name to jxsv.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-mediastreamoutputconfiguration.html#cfn-mediaconnect-flowoutput-mediastreamoutputconfiguration-encodingname
            '''
            result = self._values.get("encoding_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encoding_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowOutputPropsMixin.EncodingParametersProperty"]]:
            '''A collection of parameters that determine how MediaConnect will convert the content.

            These fields only apply to outputs on flows that have a CDI source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-mediastreamoutputconfiguration.html#cfn-mediaconnect-flowoutput-mediastreamoutputconfiguration-encodingparameters
            '''
            result = self._values.get("encoding_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowOutputPropsMixin.EncodingParametersProperty"]], result)

        @builtins.property
        def media_stream_name(self) -> typing.Optional[builtins.str]:
            '''The name of the media stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-mediastreamoutputconfiguration.html#cfn-mediaconnect-flowoutput-mediastreamoutputconfiguration-mediastreamname
            '''
            result = self._values.get("media_stream_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MediaStreamOutputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"role_arn": "roleArn", "secret_arn": "secretArn"},
    )
    class SecretsManagerEncryptionKeyConfigurationProperty:
        def __init__(
            self,
            *,
            role_arn: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration settings for transit encryption of a flow output using AWS Secrets Manager, including the secret ARN and role ARN.

            :param role_arn: The ARN of the IAM role used for transit encryption to the router input using AWS Secrets Manager.
            :param secret_arn: The ARN of the AWS Secrets Manager secret used for transit encryption to the router input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-secretsmanagerencryptionkeyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                secrets_manager_encryption_key_configuration_property = mediaconnect_mixins.CfnFlowOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                    role_arn="roleArn",
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d689ea55f6c08a5fe58074200dbe15a9d972434ace7ae4bfe062297afa0ea316)
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM role used for transit encryption to the router input using AWS Secrets Manager.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-secretsmanagerencryptionkeyconfiguration.html#cfn-mediaconnect-flowoutput-secretsmanagerencryptionkeyconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the AWS Secrets Manager secret used for transit encryption to the router input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-secretsmanagerencryptionkeyconfiguration.html#cfn-mediaconnect-flowoutput-secretsmanagerencryptionkeyconfiguration-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecretsManagerEncryptionKeyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowOutputPropsMixin.VpcInterfaceAttachmentProperty",
        jsii_struct_bases=[],
        name_mapping={"vpc_interface_name": "vpcInterfaceName"},
    )
    class VpcInterfaceAttachmentProperty:
        def __init__(
            self,
            *,
            vpc_interface_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The settings for attaching a VPC interface to an resource.

            :param vpc_interface_name: The name of the VPC interface to use for this resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-vpcinterfaceattachment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                vpc_interface_attachment_property = mediaconnect_mixins.CfnFlowOutputPropsMixin.VpcInterfaceAttachmentProperty(
                    vpc_interface_name="vpcInterfaceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4ae9f703db286e45dd3a4a87db017c86e13ebf348a4bcefb57b62226f5638d39)
                check_type(argname="argument vpc_interface_name", value=vpc_interface_name, expected_type=type_hints["vpc_interface_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if vpc_interface_name is not None:
                self._values["vpc_interface_name"] = vpc_interface_name

        @builtins.property
        def vpc_interface_name(self) -> typing.Optional[builtins.str]:
            '''The name of the VPC interface to use for this resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-vpcinterfaceattachment.html#cfn-mediaconnect-flowoutput-vpcinterfaceattachment-vpcinterfacename
            '''
            result = self._values.get("vpc_interface_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcInterfaceAttachmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IMixin_11e4b965)
class CfnFlowPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin",
):
    '''The ``AWS::MediaConnect::Flow`` resource defines a connection between one or more video sources and one or more outputs.

    For each flow, you specify the transport protocol to use, encryption information, and details for any outputs or entitlements that you want. AWS Elemental MediaConnect returns an ingest endpoint where you can send your live video as a single unicast stream. The service replicates and distributes the video to every output that you specify, whether inside or outside the AWS Cloud. You can also set up entitlements on a flow to allow other AWS accounts to access your content.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flow.html
    :cloudformationResource: AWS::MediaConnect::Flow
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
        
        # automatic: Any
        
        cfn_flow_props_mixin = mediaconnect_mixins.CfnFlowPropsMixin(mediaconnect_mixins.CfnFlowMixinProps(
            availability_zone="availabilityZone",
            flow_size="flowSize",
            maintenance=mediaconnect_mixins.CfnFlowPropsMixin.MaintenanceProperty(
                maintenance_day="maintenanceDay",
                maintenance_start_hour="maintenanceStartHour"
            ),
            media_streams=[mediaconnect_mixins.CfnFlowPropsMixin.MediaStreamProperty(
                attributes=mediaconnect_mixins.CfnFlowPropsMixin.MediaStreamAttributesProperty(
                    fmtp=mediaconnect_mixins.CfnFlowPropsMixin.FmtpProperty(
                        channel_order="channelOrder",
                        colorimetry="colorimetry",
                        exact_framerate="exactFramerate",
                        par="par",
                        range="range",
                        scan_mode="scanMode",
                        tcs="tcs"
                    ),
                    lang="lang"
                ),
                clock_rate=123,
                description="description",
                fmt=123,
                media_stream_id=123,
                media_stream_name="mediaStreamName",
                media_stream_type="mediaStreamType",
                video_format="videoFormat"
            )],
            name="name",
            ndi_config=mediaconnect_mixins.CfnFlowPropsMixin.NdiConfigProperty(
                machine_name="machineName",
                ndi_discovery_servers=[mediaconnect_mixins.CfnFlowPropsMixin.NdiDiscoveryServerConfigProperty(
                    discovery_server_address="discoveryServerAddress",
                    discovery_server_port=123,
                    vpc_interface_adapter="vpcInterfaceAdapter"
                )],
                ndi_state="ndiState"
            ),
            source=mediaconnect_mixins.CfnFlowPropsMixin.SourceProperty(
                decryption=mediaconnect_mixins.CfnFlowPropsMixin.EncryptionProperty(
                    algorithm="algorithm",
                    constant_initialization_vector="constantInitializationVector",
                    device_id="deviceId",
                    key_type="keyType",
                    region="region",
                    resource_id="resourceId",
                    role_arn="roleArn",
                    secret_arn="secretArn",
                    url="url"
                ),
                description="description",
                entitlement_arn="entitlementArn",
                gateway_bridge_source=mediaconnect_mixins.CfnFlowPropsMixin.GatewayBridgeSourceProperty(
                    bridge_arn="bridgeArn",
                    vpc_interface_attachment=mediaconnect_mixins.CfnFlowPropsMixin.VpcInterfaceAttachmentProperty(
                        vpc_interface_name="vpcInterfaceName"
                    )
                ),
                ingest_ip="ingestIp",
                ingest_port=123,
                max_bitrate=123,
                max_latency=123,
                max_sync_buffer=123,
                media_stream_source_configurations=[mediaconnect_mixins.CfnFlowPropsMixin.MediaStreamSourceConfigurationProperty(
                    encoding_name="encodingName",
                    input_configurations=[mediaconnect_mixins.CfnFlowPropsMixin.InputConfigurationProperty(
                        input_port=123,
                        interface=mediaconnect_mixins.CfnFlowPropsMixin.InterfaceProperty(
                            name="name"
                        )
                    )],
                    media_stream_name="mediaStreamName"
                )],
                min_latency=123,
                name="name",
                protocol="protocol",
                router_integration_state="routerIntegrationState",
                router_integration_transit_decryption=mediaconnect_mixins.CfnFlowPropsMixin.FlowTransitEncryptionProperty(
                    encryption_key_configuration=mediaconnect_mixins.CfnFlowPropsMixin.FlowTransitEncryptionKeyConfigurationProperty(
                        automatic=automatic,
                        secrets_manager=mediaconnect_mixins.CfnFlowPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                            role_arn="roleArn",
                            secret_arn="secretArn"
                        )
                    ),
                    encryption_key_type="encryptionKeyType"
                ),
                sender_control_port=123,
                sender_ip_address="senderIpAddress",
                source_arn="sourceArn",
                source_ingest_port="sourceIngestPort",
                source_listener_address="sourceListenerAddress",
                source_listener_port=123,
                stream_id="streamId",
                vpc_interface_name="vpcInterfaceName",
                whitelist_cidr="whitelistCidr"
            ),
            source_failover_config=mediaconnect_mixins.CfnFlowPropsMixin.FailoverConfigProperty(
                failover_mode="failoverMode",
                recovery_window=123,
                source_priority=mediaconnect_mixins.CfnFlowPropsMixin.SourcePriorityProperty(
                    primary_source="primarySource"
                ),
                state="state"
            ),
            source_monitoring_config=mediaconnect_mixins.CfnFlowPropsMixin.SourceMonitoringConfigProperty(
                audio_monitoring_settings=[mediaconnect_mixins.CfnFlowPropsMixin.AudioMonitoringSettingProperty(
                    silent_audio=mediaconnect_mixins.CfnFlowPropsMixin.SilentAudioProperty(
                        state="state",
                        threshold_seconds=123
                    )
                )],
                content_quality_analysis_state="contentQualityAnalysisState",
                thumbnail_state="thumbnailState",
                video_monitoring_settings=[mediaconnect_mixins.CfnFlowPropsMixin.VideoMonitoringSettingProperty(
                    black_frames=mediaconnect_mixins.CfnFlowPropsMixin.BlackFramesProperty(
                        state="state",
                        threshold_seconds=123
                    ),
                    frozen_frames=mediaconnect_mixins.CfnFlowPropsMixin.FrozenFramesProperty(
                        state="state",
                        threshold_seconds=123
                    )
                )]
            ),
            vpc_interfaces=[mediaconnect_mixins.CfnFlowPropsMixin.VpcInterfaceProperty(
                name="name",
                network_interface_ids=["networkInterfaceIds"],
                network_interface_type="networkInterfaceType",
                role_arn="roleArn",
                security_group_ids=["securityGroupIds"],
                subnet_id="subnetId"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnFlowMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaConnect::Flow``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d86ff46877b6db246da2216d1359eacd70fe8f4d9e06970e3f857a2a6179819)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3383a8c98d19b0000ceb3d8d0a2d9a110f287f0159e2c660f266166295009b0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6214c9114ab03b1fbd443b1941f12699f56b8d143d8b158cc6121fea9a3b9f6f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFlowMixinProps:
        return typing.cast(CfnFlowMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.AudioMonitoringSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"silent_audio": "silentAudio"},
    )
    class AudioMonitoringSettingProperty:
        def __init__(
            self,
            *,
            silent_audio: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.SilentAudioProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the configuration for audio stream metrics monitoring.

            :param silent_audio: Detects periods of silence.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-audiomonitoringsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                audio_monitoring_setting_property = mediaconnect_mixins.CfnFlowPropsMixin.AudioMonitoringSettingProperty(
                    silent_audio=mediaconnect_mixins.CfnFlowPropsMixin.SilentAudioProperty(
                        state="state",
                        threshold_seconds=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__939912c55cebca624532ef6ae0d56749aff0b4a43f3f20f8b3aecc1c40fa0dff)
                check_type(argname="argument silent_audio", value=silent_audio, expected_type=type_hints["silent_audio"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if silent_audio is not None:
                self._values["silent_audio"] = silent_audio

        @builtins.property
        def silent_audio(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SilentAudioProperty"]]:
            '''Detects periods of silence.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-audiomonitoringsetting.html#cfn-mediaconnect-flow-audiomonitoringsetting-silentaudio
            '''
            result = self._values.get("silent_audio")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SilentAudioProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AudioMonitoringSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.BlackFramesProperty",
        jsii_struct_bases=[],
        name_mapping={"state": "state", "threshold_seconds": "thresholdSeconds"},
    )
    class BlackFramesProperty:
        def __init__(
            self,
            *,
            state: typing.Optional[builtins.str] = None,
            threshold_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Configures settings for the ``BlackFrames`` metric.

            :param state: Indicates whether the ``BlackFrames`` metric is enabled or disabled..
            :param threshold_seconds: Specifies the number of consecutive seconds of black frames that triggers an event or alert.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-blackframes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                black_frames_property = mediaconnect_mixins.CfnFlowPropsMixin.BlackFramesProperty(
                    state="state",
                    threshold_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__97f36aabebb546e089aeec719cd657f819e475f314e74bc1bab2444741cb5fa4)
                check_type(argname="argument state", value=state, expected_type=type_hints["state"])
                check_type(argname="argument threshold_seconds", value=threshold_seconds, expected_type=type_hints["threshold_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if state is not None:
                self._values["state"] = state
            if threshold_seconds is not None:
                self._values["threshold_seconds"] = threshold_seconds

        @builtins.property
        def state(self) -> typing.Optional[builtins.str]:
            '''Indicates whether the ``BlackFrames`` metric is enabled or disabled..

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-blackframes.html#cfn-mediaconnect-flow-blackframes-state
            '''
            result = self._values.get("state")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def threshold_seconds(self) -> typing.Optional[jsii.Number]:
            '''Specifies the number of consecutive seconds of black frames that triggers an event or alert.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-blackframes.html#cfn-mediaconnect-flow-blackframes-thresholdseconds
            '''
            result = self._values.get("threshold_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BlackFramesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.EncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "algorithm": "algorithm",
            "constant_initialization_vector": "constantInitializationVector",
            "device_id": "deviceId",
            "key_type": "keyType",
            "region": "region",
            "resource_id": "resourceId",
            "role_arn": "roleArn",
            "secret_arn": "secretArn",
            "url": "url",
        },
    )
    class EncryptionProperty:
        def __init__(
            self,
            *,
            algorithm: typing.Optional[builtins.str] = None,
            constant_initialization_vector: typing.Optional[builtins.str] = None,
            device_id: typing.Optional[builtins.str] = None,
            key_type: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
            resource_id: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Encryption information.

            :param algorithm: The type of algorithm that is used for static key encryption (such as aes128, aes192, or aes256). If you are using SPEKE or SRT-password encryption, this property must be left blank.
            :param constant_initialization_vector: A 128-bit, 16-byte hex value represented by a 32-character string, to be used with the key for encrypting content. This parameter is not valid for static key encryption.
            :param device_id: The value of one of the devices that you configured with your digital rights management (DRM) platform key provider. This parameter is required for SPEKE encryption and is not valid for static key encryption.
            :param key_type: The type of key that is used for the encryption. If you don't specify a ``keyType`` value, the service uses the default setting ( ``static-key`` ). Valid key types are: ``static-key`` , ``speke`` , and ``srt-password`` . Default: - "static-key"
            :param region: The AWS Region that the API Gateway proxy endpoint was created in. This parameter is required for SPEKE encryption and is not valid for static key encryption.
            :param resource_id: An identifier for the content. The service sends this value to the key server to identify the current endpoint. The resource ID is also known as the content ID. This parameter is required for SPEKE encryption and is not valid for static key encryption.
            :param role_arn: The ARN of the role that you created during setup (when you set up MediaConnect as a trusted entity).
            :param secret_arn: The ARN of the secret that you created in AWS Secrets Manager to store the encryption key. This parameter is required for static key encryption and is not valid for SPEKE encryption.
            :param url: The URL from the API Gateway proxy that you set up to talk to your key server. This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-encryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                encryption_property = mediaconnect_mixins.CfnFlowPropsMixin.EncryptionProperty(
                    algorithm="algorithm",
                    constant_initialization_vector="constantInitializationVector",
                    device_id="deviceId",
                    key_type="keyType",
                    region="region",
                    resource_id="resourceId",
                    role_arn="roleArn",
                    secret_arn="secretArn",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5cdd26afb60ff9ec880e8abfb3f3718b0bcc26b2c4c5c48221f4e2866d1f1e79)
                check_type(argname="argument algorithm", value=algorithm, expected_type=type_hints["algorithm"])
                check_type(argname="argument constant_initialization_vector", value=constant_initialization_vector, expected_type=type_hints["constant_initialization_vector"])
                check_type(argname="argument device_id", value=device_id, expected_type=type_hints["device_id"])
                check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
                check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if algorithm is not None:
                self._values["algorithm"] = algorithm
            if constant_initialization_vector is not None:
                self._values["constant_initialization_vector"] = constant_initialization_vector
            if device_id is not None:
                self._values["device_id"] = device_id
            if key_type is not None:
                self._values["key_type"] = key_type
            if region is not None:
                self._values["region"] = region
            if resource_id is not None:
                self._values["resource_id"] = resource_id
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def algorithm(self) -> typing.Optional[builtins.str]:
            '''The type of algorithm that is used for static key encryption (such as aes128, aes192, or aes256).

            If you are using SPEKE or SRT-password encryption, this property must be left blank.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-encryption.html#cfn-mediaconnect-flow-encryption-algorithm
            '''
            result = self._values.get("algorithm")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def constant_initialization_vector(self) -> typing.Optional[builtins.str]:
            '''A 128-bit, 16-byte hex value represented by a 32-character string, to be used with the key for encrypting content.

            This parameter is not valid for static key encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-encryption.html#cfn-mediaconnect-flow-encryption-constantinitializationvector
            '''
            result = self._values.get("constant_initialization_vector")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def device_id(self) -> typing.Optional[builtins.str]:
            '''The value of one of the devices that you configured with your digital rights management (DRM) platform key provider.

            This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-encryption.html#cfn-mediaconnect-flow-encryption-deviceid
            '''
            result = self._values.get("device_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_type(self) -> typing.Optional[builtins.str]:
            '''The type of key that is used for the encryption.

            If you don't specify a ``keyType`` value, the service uses the default setting ( ``static-key`` ). Valid key types are: ``static-key`` , ``speke`` , and ``srt-password`` .

            :default: - "static-key"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-encryption.html#cfn-mediaconnect-flow-encryption-keytype
            '''
            result = self._values.get("key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region that the API Gateway proxy endpoint was created in.

            This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-encryption.html#cfn-mediaconnect-flow-encryption-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_id(self) -> typing.Optional[builtins.str]:
            '''An identifier for the content.

            The service sends this value to the key server to identify the current endpoint. The resource ID is also known as the content ID. This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-encryption.html#cfn-mediaconnect-flow-encryption-resourceid
            '''
            result = self._values.get("resource_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the role that you created during setup (when you set up MediaConnect as a trusted entity).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-encryption.html#cfn-mediaconnect-flow-encryption-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the secret that you created in AWS Secrets Manager to store the encryption key.

            This parameter is required for static key encryption and is not valid for SPEKE encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-encryption.html#cfn-mediaconnect-flow-encryption-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL from the API Gateway proxy that you set up to talk to your key server.

            This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-encryption.html#cfn-mediaconnect-flow-encryption-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.FailoverConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "failover_mode": "failoverMode",
            "recovery_window": "recoveryWindow",
            "source_priority": "sourcePriority",
            "state": "state",
        },
    )
    class FailoverConfigProperty:
        def __init__(
            self,
            *,
            failover_mode: typing.Optional[builtins.str] = None,
            recovery_window: typing.Optional[jsii.Number] = None,
            source_priority: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.SourcePriorityProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            state: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The settings for source failover.

            :param failover_mode: The type of failover you choose for this flow. MERGE combines the source streams into a single stream, allowing graceful recovery from any single-source loss. FAILOVER allows switching between different streams. The string for this property must be entered as MERGE or FAILOVER. No other string entry is valid.
            :param recovery_window: Search window time to look for dash-7 packets.
            :param source_priority: The priority you want to assign to a source. You can have a primary stream and a backup stream or two equally prioritized streams.
            :param state: The state of source failover on the flow. If the state is inactive, the flow can have only one source. If the state is active, the flow can have one or two sources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-failoverconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                failover_config_property = mediaconnect_mixins.CfnFlowPropsMixin.FailoverConfigProperty(
                    failover_mode="failoverMode",
                    recovery_window=123,
                    source_priority=mediaconnect_mixins.CfnFlowPropsMixin.SourcePriorityProperty(
                        primary_source="primarySource"
                    ),
                    state="state"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ec9df09b6dbb20e5fc98548d6d9d2bd2206079c900fdf7c70979d946f2063f8e)
                check_type(argname="argument failover_mode", value=failover_mode, expected_type=type_hints["failover_mode"])
                check_type(argname="argument recovery_window", value=recovery_window, expected_type=type_hints["recovery_window"])
                check_type(argname="argument source_priority", value=source_priority, expected_type=type_hints["source_priority"])
                check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if failover_mode is not None:
                self._values["failover_mode"] = failover_mode
            if recovery_window is not None:
                self._values["recovery_window"] = recovery_window
            if source_priority is not None:
                self._values["source_priority"] = source_priority
            if state is not None:
                self._values["state"] = state

        @builtins.property
        def failover_mode(self) -> typing.Optional[builtins.str]:
            '''The type of failover you choose for this flow.

            MERGE combines the source streams into a single stream, allowing graceful recovery from any single-source loss. FAILOVER allows switching between different streams. The string for this property must be entered as MERGE or FAILOVER. No other string entry is valid.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-failoverconfig.html#cfn-mediaconnect-flow-failoverconfig-failovermode
            '''
            result = self._values.get("failover_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def recovery_window(self) -> typing.Optional[jsii.Number]:
            '''Search window time to look for dash-7 packets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-failoverconfig.html#cfn-mediaconnect-flow-failoverconfig-recoverywindow
            '''
            result = self._values.get("recovery_window")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def source_priority(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SourcePriorityProperty"]]:
            '''The priority you want to assign to a source.

            You can have a primary stream and a backup stream or two equally prioritized streams.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-failoverconfig.html#cfn-mediaconnect-flow-failoverconfig-sourcepriority
            '''
            result = self._values.get("source_priority")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SourcePriorityProperty"]], result)

        @builtins.property
        def state(self) -> typing.Optional[builtins.str]:
            '''The state of source failover on the flow.

            If the state is inactive, the flow can have only one source. If the state is active, the flow can have one or two sources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-failoverconfig.html#cfn-mediaconnect-flow-failoverconfig-state
            '''
            result = self._values.get("state")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FailoverConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.FlowTransitEncryptionKeyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"automatic": "automatic", "secrets_manager": "secretsManager"},
    )
    class FlowTransitEncryptionKeyConfigurationProperty:
        def __init__(
            self,
            *,
            automatic: typing.Any = None,
            secrets_manager: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param automatic: Configuration settings for automatic encryption key management, where MediaConnect handles key creation and rotation.
            :param secrets_manager: The configuration settings for transit encryption of a flow source using AWS Secrets Manager, including the secret ARN and role ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-flowtransitencryptionkeyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                # automatic: Any
                
                flow_transit_encryption_key_configuration_property = mediaconnect_mixins.CfnFlowPropsMixin.FlowTransitEncryptionKeyConfigurationProperty(
                    automatic=automatic,
                    secrets_manager=mediaconnect_mixins.CfnFlowPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                        role_arn="roleArn",
                        secret_arn="secretArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__327f0e2c2108be403014f890e8f10968b51c174bbb55e8964202669893c5a237)
                check_type(argname="argument automatic", value=automatic, expected_type=type_hints["automatic"])
                check_type(argname="argument secrets_manager", value=secrets_manager, expected_type=type_hints["secrets_manager"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if automatic is not None:
                self._values["automatic"] = automatic
            if secrets_manager is not None:
                self._values["secrets_manager"] = secrets_manager

        @builtins.property
        def automatic(self) -> typing.Any:
            '''Configuration settings for automatic encryption key management, where MediaConnect handles key creation and rotation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-flowtransitencryptionkeyconfiguration.html#cfn-mediaconnect-flow-flowtransitencryptionkeyconfiguration-automatic
            '''
            result = self._values.get("automatic")
            return typing.cast(typing.Any, result)

        @builtins.property
        def secrets_manager(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty"]]:
            '''The configuration settings for transit encryption of a flow source using AWS Secrets Manager, including the secret ARN and role ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-flowtransitencryptionkeyconfiguration.html#cfn-mediaconnect-flow-flowtransitencryptionkeyconfiguration-secretsmanager
            '''
            result = self._values.get("secrets_manager")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FlowTransitEncryptionKeyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.FlowTransitEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption_key_configuration": "encryptionKeyConfiguration",
            "encryption_key_type": "encryptionKeyType",
        },
    )
    class FlowTransitEncryptionProperty:
        def __init__(
            self,
            *,
            encryption_key_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.FlowTransitEncryptionKeyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            encryption_key_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration that defines how content is encrypted during transit between the MediaConnect router and a MediaConnect flow.

            :param encryption_key_configuration: Configuration settings for flow transit encryption keys.
            :param encryption_key_type: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-flowtransitencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                # automatic: Any
                
                flow_transit_encryption_property = mediaconnect_mixins.CfnFlowPropsMixin.FlowTransitEncryptionProperty(
                    encryption_key_configuration=mediaconnect_mixins.CfnFlowPropsMixin.FlowTransitEncryptionKeyConfigurationProperty(
                        automatic=automatic,
                        secrets_manager=mediaconnect_mixins.CfnFlowPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                            role_arn="roleArn",
                            secret_arn="secretArn"
                        )
                    ),
                    encryption_key_type="encryptionKeyType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3830b919b567bff3c746ca727172dd267368d55f55f0c6cac003e727b2a08d3e)
                check_type(argname="argument encryption_key_configuration", value=encryption_key_configuration, expected_type=type_hints["encryption_key_configuration"])
                check_type(argname="argument encryption_key_type", value=encryption_key_type, expected_type=type_hints["encryption_key_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_key_configuration is not None:
                self._values["encryption_key_configuration"] = encryption_key_configuration
            if encryption_key_type is not None:
                self._values["encryption_key_type"] = encryption_key_type

        @builtins.property
        def encryption_key_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.FlowTransitEncryptionKeyConfigurationProperty"]]:
            '''Configuration settings for flow transit encryption keys.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-flowtransitencryption.html#cfn-mediaconnect-flow-flowtransitencryption-encryptionkeyconfiguration
            '''
            result = self._values.get("encryption_key_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.FlowTransitEncryptionKeyConfigurationProperty"]], result)

        @builtins.property
        def encryption_key_type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-flowtransitencryption.html#cfn-mediaconnect-flow-flowtransitencryption-encryptionkeytype
            '''
            result = self._values.get("encryption_key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FlowTransitEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.FmtpProperty",
        jsii_struct_bases=[],
        name_mapping={
            "channel_order": "channelOrder",
            "colorimetry": "colorimetry",
            "exact_framerate": "exactFramerate",
            "par": "par",
            "range": "range",
            "scan_mode": "scanMode",
            "tcs": "tcs",
        },
    )
    class FmtpProperty:
        def __init__(
            self,
            *,
            channel_order: typing.Optional[builtins.str] = None,
            colorimetry: typing.Optional[builtins.str] = None,
            exact_framerate: typing.Optional[builtins.str] = None,
            par: typing.Optional[builtins.str] = None,
            range: typing.Optional[builtins.str] = None,
            scan_mode: typing.Optional[builtins.str] = None,
            tcs: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A set of parameters that define the media stream.

            :param channel_order: The format of the audio channel.
            :param colorimetry: The format used for the representation of color.
            :param exact_framerate: The frame rate for the video stream, in frames/second. For example: 60000/1001.
            :param par: The pixel aspect ratio (PAR) of the video.
            :param range: The encoding range of the video.
            :param scan_mode: The type of compression that was used to smooth the video’s appearance.
            :param tcs: The transfer characteristic system (TCS) that is used in the video.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-fmtp.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                fmtp_property = mediaconnect_mixins.CfnFlowPropsMixin.FmtpProperty(
                    channel_order="channelOrder",
                    colorimetry="colorimetry",
                    exact_framerate="exactFramerate",
                    par="par",
                    range="range",
                    scan_mode="scanMode",
                    tcs="tcs"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4fa8e309b8dc68021f2bc931cecb80d94515ed80e368632d37267b47318dc200)
                check_type(argname="argument channel_order", value=channel_order, expected_type=type_hints["channel_order"])
                check_type(argname="argument colorimetry", value=colorimetry, expected_type=type_hints["colorimetry"])
                check_type(argname="argument exact_framerate", value=exact_framerate, expected_type=type_hints["exact_framerate"])
                check_type(argname="argument par", value=par, expected_type=type_hints["par"])
                check_type(argname="argument range", value=range, expected_type=type_hints["range"])
                check_type(argname="argument scan_mode", value=scan_mode, expected_type=type_hints["scan_mode"])
                check_type(argname="argument tcs", value=tcs, expected_type=type_hints["tcs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if channel_order is not None:
                self._values["channel_order"] = channel_order
            if colorimetry is not None:
                self._values["colorimetry"] = colorimetry
            if exact_framerate is not None:
                self._values["exact_framerate"] = exact_framerate
            if par is not None:
                self._values["par"] = par
            if range is not None:
                self._values["range"] = range
            if scan_mode is not None:
                self._values["scan_mode"] = scan_mode
            if tcs is not None:
                self._values["tcs"] = tcs

        @builtins.property
        def channel_order(self) -> typing.Optional[builtins.str]:
            '''The format of the audio channel.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-fmtp.html#cfn-mediaconnect-flow-fmtp-channelorder
            '''
            result = self._values.get("channel_order")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def colorimetry(self) -> typing.Optional[builtins.str]:
            '''The format used for the representation of color.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-fmtp.html#cfn-mediaconnect-flow-fmtp-colorimetry
            '''
            result = self._values.get("colorimetry")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def exact_framerate(self) -> typing.Optional[builtins.str]:
            '''The frame rate for the video stream, in frames/second.

            For example: 60000/1001.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-fmtp.html#cfn-mediaconnect-flow-fmtp-exactframerate
            '''
            result = self._values.get("exact_framerate")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def par(self) -> typing.Optional[builtins.str]:
            '''The pixel aspect ratio (PAR) of the video.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-fmtp.html#cfn-mediaconnect-flow-fmtp-par
            '''
            result = self._values.get("par")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def range(self) -> typing.Optional[builtins.str]:
            '''The encoding range of the video.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-fmtp.html#cfn-mediaconnect-flow-fmtp-range
            '''
            result = self._values.get("range")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scan_mode(self) -> typing.Optional[builtins.str]:
            '''The type of compression that was used to smooth the video’s appearance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-fmtp.html#cfn-mediaconnect-flow-fmtp-scanmode
            '''
            result = self._values.get("scan_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tcs(self) -> typing.Optional[builtins.str]:
            '''The transfer characteristic system (TCS) that is used in the video.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-fmtp.html#cfn-mediaconnect-flow-fmtp-tcs
            '''
            result = self._values.get("tcs")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FmtpProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.FrozenFramesProperty",
        jsii_struct_bases=[],
        name_mapping={"state": "state", "threshold_seconds": "thresholdSeconds"},
    )
    class FrozenFramesProperty:
        def __init__(
            self,
            *,
            state: typing.Optional[builtins.str] = None,
            threshold_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Configures settings for the ``FrozenFrames`` metric.

            :param state: Indicates whether the ``FrozenFrames`` metric is enabled or disabled.
            :param threshold_seconds: Specifies the number of consecutive seconds of a static image that triggers an event or alert.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-frozenframes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                frozen_frames_property = mediaconnect_mixins.CfnFlowPropsMixin.FrozenFramesProperty(
                    state="state",
                    threshold_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dc3e4579ecbdb1bc7ce4e51b5562496b3a8804e9c8031bf3d70bdf5bb93351d2)
                check_type(argname="argument state", value=state, expected_type=type_hints["state"])
                check_type(argname="argument threshold_seconds", value=threshold_seconds, expected_type=type_hints["threshold_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if state is not None:
                self._values["state"] = state
            if threshold_seconds is not None:
                self._values["threshold_seconds"] = threshold_seconds

        @builtins.property
        def state(self) -> typing.Optional[builtins.str]:
            '''Indicates whether the ``FrozenFrames`` metric is enabled or disabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-frozenframes.html#cfn-mediaconnect-flow-frozenframes-state
            '''
            result = self._values.get("state")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def threshold_seconds(self) -> typing.Optional[jsii.Number]:
            '''Specifies the number of consecutive seconds of a static image that triggers an event or alert.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-frozenframes.html#cfn-mediaconnect-flow-frozenframes-thresholdseconds
            '''
            result = self._values.get("threshold_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FrozenFramesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.GatewayBridgeSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bridge_arn": "bridgeArn",
            "vpc_interface_attachment": "vpcInterfaceAttachment",
        },
    )
    class GatewayBridgeSourceProperty:
        def __init__(
            self,
            *,
            bridge_arn: typing.Optional[builtins.str] = None,
            vpc_interface_attachment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.VpcInterfaceAttachmentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The source configuration for cloud flows receiving a stream from a bridge.

            :param bridge_arn: The ARN of the bridge feeding this flow.
            :param vpc_interface_attachment: The name of the VPC interface attachment to use for this bridge source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-gatewaybridgesource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                gateway_bridge_source_property = mediaconnect_mixins.CfnFlowPropsMixin.GatewayBridgeSourceProperty(
                    bridge_arn="bridgeArn",
                    vpc_interface_attachment=mediaconnect_mixins.CfnFlowPropsMixin.VpcInterfaceAttachmentProperty(
                        vpc_interface_name="vpcInterfaceName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__19263de2735b65eb3cfd8ff49f7595a7c7f2cf8dab4b4ebf506735f045929416)
                check_type(argname="argument bridge_arn", value=bridge_arn, expected_type=type_hints["bridge_arn"])
                check_type(argname="argument vpc_interface_attachment", value=vpc_interface_attachment, expected_type=type_hints["vpc_interface_attachment"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bridge_arn is not None:
                self._values["bridge_arn"] = bridge_arn
            if vpc_interface_attachment is not None:
                self._values["vpc_interface_attachment"] = vpc_interface_attachment

        @builtins.property
        def bridge_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the bridge feeding this flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-gatewaybridgesource.html#cfn-mediaconnect-flow-gatewaybridgesource-bridgearn
            '''
            result = self._values.get("bridge_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_interface_attachment(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.VpcInterfaceAttachmentProperty"]]:
            '''The name of the VPC interface attachment to use for this bridge source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-gatewaybridgesource.html#cfn-mediaconnect-flow-gatewaybridgesource-vpcinterfaceattachment
            '''
            result = self._values.get("vpc_interface_attachment")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.VpcInterfaceAttachmentProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GatewayBridgeSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.InputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"input_port": "inputPort", "interface": "interface"},
    )
    class InputConfigurationProperty:
        def __init__(
            self,
            *,
            input_port: typing.Optional[jsii.Number] = None,
            interface: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.InterfaceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The transport parameters that are associated with an incoming media stream.

            :param input_port: The port that the flow listens on for an incoming media stream.
            :param interface: The VPC interface where the media stream comes in from.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-inputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                input_configuration_property = mediaconnect_mixins.CfnFlowPropsMixin.InputConfigurationProperty(
                    input_port=123,
                    interface=mediaconnect_mixins.CfnFlowPropsMixin.InterfaceProperty(
                        name="name"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a6375d765d95cc088f509403c716e1f361c654ef283ca29e4c3d66e3d34be3d4)
                check_type(argname="argument input_port", value=input_port, expected_type=type_hints["input_port"])
                check_type(argname="argument interface", value=interface, expected_type=type_hints["interface"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if input_port is not None:
                self._values["input_port"] = input_port
            if interface is not None:
                self._values["interface"] = interface

        @builtins.property
        def input_port(self) -> typing.Optional[jsii.Number]:
            '''The port that the flow listens on for an incoming media stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-inputconfiguration.html#cfn-mediaconnect-flow-inputconfiguration-inputport
            '''
            result = self._values.get("input_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interface(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.InterfaceProperty"]]:
            '''The VPC interface where the media stream comes in from.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-inputconfiguration.html#cfn-mediaconnect-flow-inputconfiguration-interface
            '''
            result = self._values.get("interface")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.InterfaceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.InterfaceProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class InterfaceProperty:
        def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
            '''The VPC interface that is used for the media stream associated with the source or output.

            :param name: The name of the VPC interface.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-interface.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                interface_property = mediaconnect_mixins.CfnFlowPropsMixin.InterfaceProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b430b25a0752bcb7b7be7051bd38f34306d67f346f5734e09bccb8a5a7eefbc8)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the VPC interface.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-interface.html#cfn-mediaconnect-flow-interface-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InterfaceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.MaintenanceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "maintenance_day": "maintenanceDay",
            "maintenance_start_hour": "maintenanceStartHour",
        },
    )
    class MaintenanceProperty:
        def __init__(
            self,
            *,
            maintenance_day: typing.Optional[builtins.str] = None,
            maintenance_start_hour: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The maintenance setting of a flow.

            :param maintenance_day: A day of a week when the maintenance will happen. Use Monday/Tuesday/Wednesday/Thursday/Friday/Saturday/Sunday.
            :param maintenance_start_hour: UTC time when the maintenance will happen. Use 24-hour HH:MM format. Minutes must be 00. Example: 13:00. The default value is 02:00.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-maintenance.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                maintenance_property = mediaconnect_mixins.CfnFlowPropsMixin.MaintenanceProperty(
                    maintenance_day="maintenanceDay",
                    maintenance_start_hour="maintenanceStartHour"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__25f2f8d42857124c77915969a551723a3b8afd68be6183d3b1226e767dad3453)
                check_type(argname="argument maintenance_day", value=maintenance_day, expected_type=type_hints["maintenance_day"])
                check_type(argname="argument maintenance_start_hour", value=maintenance_start_hour, expected_type=type_hints["maintenance_start_hour"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if maintenance_day is not None:
                self._values["maintenance_day"] = maintenance_day
            if maintenance_start_hour is not None:
                self._values["maintenance_start_hour"] = maintenance_start_hour

        @builtins.property
        def maintenance_day(self) -> typing.Optional[builtins.str]:
            '''A day of a week when the maintenance will happen.

            Use Monday/Tuesday/Wednesday/Thursday/Friday/Saturday/Sunday.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-maintenance.html#cfn-mediaconnect-flow-maintenance-maintenanceday
            '''
            result = self._values.get("maintenance_day")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def maintenance_start_hour(self) -> typing.Optional[builtins.str]:
            '''UTC time when the maintenance will happen.

            Use 24-hour HH:MM format. Minutes must be 00. Example: 13:00. The default value is 02:00.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-maintenance.html#cfn-mediaconnect-flow-maintenance-maintenancestarthour
            '''
            result = self._values.get("maintenance_start_hour")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaintenanceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.MediaStreamAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={"fmtp": "fmtp", "lang": "lang"},
    )
    class MediaStreamAttributesProperty:
        def __init__(
            self,
            *,
            fmtp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.FmtpProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            lang: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Attributes that are related to the media stream.

            :param fmtp: The settings that you want to use to define the media stream.
            :param lang: The audio language, in a format that is recognized by the receiver.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-mediastreamattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                media_stream_attributes_property = mediaconnect_mixins.CfnFlowPropsMixin.MediaStreamAttributesProperty(
                    fmtp=mediaconnect_mixins.CfnFlowPropsMixin.FmtpProperty(
                        channel_order="channelOrder",
                        colorimetry="colorimetry",
                        exact_framerate="exactFramerate",
                        par="par",
                        range="range",
                        scan_mode="scanMode",
                        tcs="tcs"
                    ),
                    lang="lang"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4f15ae44a94333070725a83ca6b849b3c64b5426edef185adbac285538dd0447)
                check_type(argname="argument fmtp", value=fmtp, expected_type=type_hints["fmtp"])
                check_type(argname="argument lang", value=lang, expected_type=type_hints["lang"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if fmtp is not None:
                self._values["fmtp"] = fmtp
            if lang is not None:
                self._values["lang"] = lang

        @builtins.property
        def fmtp(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.FmtpProperty"]]:
            '''The settings that you want to use to define the media stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-mediastreamattributes.html#cfn-mediaconnect-flow-mediastreamattributes-fmtp
            '''
            result = self._values.get("fmtp")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.FmtpProperty"]], result)

        @builtins.property
        def lang(self) -> typing.Optional[builtins.str]:
            '''The audio language, in a format that is recognized by the receiver.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-mediastreamattributes.html#cfn-mediaconnect-flow-mediastreamattributes-lang
            '''
            result = self._values.get("lang")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MediaStreamAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.MediaStreamProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attributes": "attributes",
            "clock_rate": "clockRate",
            "description": "description",
            "fmt": "fmt",
            "media_stream_id": "mediaStreamId",
            "media_stream_name": "mediaStreamName",
            "media_stream_type": "mediaStreamType",
            "video_format": "videoFormat",
        },
    )
    class MediaStreamProperty:
        def __init__(
            self,
            *,
            attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.MediaStreamAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            clock_rate: typing.Optional[jsii.Number] = None,
            description: typing.Optional[builtins.str] = None,
            fmt: typing.Optional[jsii.Number] = None,
            media_stream_id: typing.Optional[jsii.Number] = None,
            media_stream_name: typing.Optional[builtins.str] = None,
            media_stream_type: typing.Optional[builtins.str] = None,
            video_format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A media stream represents one component of your content, such as video, audio, or ancillary data.

            After you add a media stream to your flow, you can associate it with sources and outputs that use the ST 2110 JPEG XS or CDI protocol.

            :param attributes: Attributes that are related to the media stream.
            :param clock_rate: The sample rate for the stream. This value is measured in Hz.
            :param description: A description that can help you quickly identify what your media stream is used for.
            :param fmt: The format type number (sometimes referred to as RTP payload type) of the media stream. MediaConnect assigns this value to the media stream. For ST 2110 JPEG XS outputs, you need to provide this value to the receiver.
            :param media_stream_id: A unique identifier for the media stream.
            :param media_stream_name: A name that helps you distinguish one media stream from another.
            :param media_stream_type: The type of media stream.
            :param video_format: The resolution of the video.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-mediastream.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                media_stream_property = mediaconnect_mixins.CfnFlowPropsMixin.MediaStreamProperty(
                    attributes=mediaconnect_mixins.CfnFlowPropsMixin.MediaStreamAttributesProperty(
                        fmtp=mediaconnect_mixins.CfnFlowPropsMixin.FmtpProperty(
                            channel_order="channelOrder",
                            colorimetry="colorimetry",
                            exact_framerate="exactFramerate",
                            par="par",
                            range="range",
                            scan_mode="scanMode",
                            tcs="tcs"
                        ),
                        lang="lang"
                    ),
                    clock_rate=123,
                    description="description",
                    fmt=123,
                    media_stream_id=123,
                    media_stream_name="mediaStreamName",
                    media_stream_type="mediaStreamType",
                    video_format="videoFormat"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__76b112275650765553cc150626b5bc455a8e730cd870c2b9eb76251d8fd2db19)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                check_type(argname="argument clock_rate", value=clock_rate, expected_type=type_hints["clock_rate"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument fmt", value=fmt, expected_type=type_hints["fmt"])
                check_type(argname="argument media_stream_id", value=media_stream_id, expected_type=type_hints["media_stream_id"])
                check_type(argname="argument media_stream_name", value=media_stream_name, expected_type=type_hints["media_stream_name"])
                check_type(argname="argument media_stream_type", value=media_stream_type, expected_type=type_hints["media_stream_type"])
                check_type(argname="argument video_format", value=video_format, expected_type=type_hints["video_format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if clock_rate is not None:
                self._values["clock_rate"] = clock_rate
            if description is not None:
                self._values["description"] = description
            if fmt is not None:
                self._values["fmt"] = fmt
            if media_stream_id is not None:
                self._values["media_stream_id"] = media_stream_id
            if media_stream_name is not None:
                self._values["media_stream_name"] = media_stream_name
            if media_stream_type is not None:
                self._values["media_stream_type"] = media_stream_type
            if video_format is not None:
                self._values["video_format"] = video_format

        @builtins.property
        def attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.MediaStreamAttributesProperty"]]:
            '''Attributes that are related to the media stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-mediastream.html#cfn-mediaconnect-flow-mediastream-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.MediaStreamAttributesProperty"]], result)

        @builtins.property
        def clock_rate(self) -> typing.Optional[jsii.Number]:
            '''The sample rate for the stream.

            This value is measured in Hz.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-mediastream.html#cfn-mediaconnect-flow-mediastream-clockrate
            '''
            result = self._values.get("clock_rate")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description that can help you quickly identify what your media stream is used for.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-mediastream.html#cfn-mediaconnect-flow-mediastream-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def fmt(self) -> typing.Optional[jsii.Number]:
            '''The format type number (sometimes referred to as RTP payload type) of the media stream.

            MediaConnect assigns this value to the media stream. For ST 2110 JPEG XS outputs, you need to provide this value to the receiver.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-mediastream.html#cfn-mediaconnect-flow-mediastream-fmt
            '''
            result = self._values.get("fmt")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def media_stream_id(self) -> typing.Optional[jsii.Number]:
            '''A unique identifier for the media stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-mediastream.html#cfn-mediaconnect-flow-mediastream-mediastreamid
            '''
            result = self._values.get("media_stream_id")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def media_stream_name(self) -> typing.Optional[builtins.str]:
            '''A name that helps you distinguish one media stream from another.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-mediastream.html#cfn-mediaconnect-flow-mediastream-mediastreamname
            '''
            result = self._values.get("media_stream_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def media_stream_type(self) -> typing.Optional[builtins.str]:
            '''The type of media stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-mediastream.html#cfn-mediaconnect-flow-mediastream-mediastreamtype
            '''
            result = self._values.get("media_stream_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def video_format(self) -> typing.Optional[builtins.str]:
            '''The resolution of the video.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-mediastream.html#cfn-mediaconnect-flow-mediastream-videoformat
            '''
            result = self._values.get("video_format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MediaStreamProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.MediaStreamSourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encoding_name": "encodingName",
            "input_configurations": "inputConfigurations",
            "media_stream_name": "mediaStreamName",
        },
    )
    class MediaStreamSourceConfigurationProperty:
        def __init__(
            self,
            *,
            encoding_name: typing.Optional[builtins.str] = None,
            input_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.InputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            media_stream_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The media stream that is associated with the source, and the parameters for that association.

            :param encoding_name: The format that was used to encode the data. For ancillary data streams, set the encoding name to smpte291. For audio streams, set the encoding name to pcm. For video, 2110 streams, set the encoding name to raw. For video, JPEG XS streams, set the encoding name to jxsv.
            :param input_configurations: The media streams that you want to associate with the source.
            :param media_stream_name: A name that helps you distinguish one media stream from another.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-mediastreamsourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                media_stream_source_configuration_property = mediaconnect_mixins.CfnFlowPropsMixin.MediaStreamSourceConfigurationProperty(
                    encoding_name="encodingName",
                    input_configurations=[mediaconnect_mixins.CfnFlowPropsMixin.InputConfigurationProperty(
                        input_port=123,
                        interface=mediaconnect_mixins.CfnFlowPropsMixin.InterfaceProperty(
                            name="name"
                        )
                    )],
                    media_stream_name="mediaStreamName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5042eb2dafe9bc994ae8cce17d6e42b8f4f9dd72e7a18d9266b1e7f95a1a26fc)
                check_type(argname="argument encoding_name", value=encoding_name, expected_type=type_hints["encoding_name"])
                check_type(argname="argument input_configurations", value=input_configurations, expected_type=type_hints["input_configurations"])
                check_type(argname="argument media_stream_name", value=media_stream_name, expected_type=type_hints["media_stream_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encoding_name is not None:
                self._values["encoding_name"] = encoding_name
            if input_configurations is not None:
                self._values["input_configurations"] = input_configurations
            if media_stream_name is not None:
                self._values["media_stream_name"] = media_stream_name

        @builtins.property
        def encoding_name(self) -> typing.Optional[builtins.str]:
            '''The format that was used to encode the data.

            For ancillary data streams, set the encoding name to smpte291. For audio streams, set the encoding name to pcm. For video, 2110 streams, set the encoding name to raw. For video, JPEG XS streams, set the encoding name to jxsv.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-mediastreamsourceconfiguration.html#cfn-mediaconnect-flow-mediastreamsourceconfiguration-encodingname
            '''
            result = self._values.get("encoding_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.InputConfigurationProperty"]]]]:
            '''The media streams that you want to associate with the source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-mediastreamsourceconfiguration.html#cfn-mediaconnect-flow-mediastreamsourceconfiguration-inputconfigurations
            '''
            result = self._values.get("input_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.InputConfigurationProperty"]]]], result)

        @builtins.property
        def media_stream_name(self) -> typing.Optional[builtins.str]:
            '''A name that helps you distinguish one media stream from another.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-mediastreamsourceconfiguration.html#cfn-mediaconnect-flow-mediastreamsourceconfiguration-mediastreamname
            '''
            result = self._values.get("media_stream_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MediaStreamSourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.NdiConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "machine_name": "machineName",
            "ndi_discovery_servers": "ndiDiscoveryServers",
            "ndi_state": "ndiState",
        },
    )
    class NdiConfigProperty:
        def __init__(
            self,
            *,
            machine_name: typing.Optional[builtins.str] = None,
            ndi_discovery_servers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.NdiDiscoveryServerConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ndi_state: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration settings for NDI outputs.

            Required when the flow includes NDI outputs.

            :param machine_name: A prefix for the names of the NDI sources that the flow creates. If a custom name isn't specified, MediaConnect generates a unique 12-character ID as the prefix.
            :param ndi_discovery_servers: A list of up to three NDI discovery server configurations. While not required by the API, this configuration is necessary for NDI functionality to work properly.
            :param ndi_state: A setting that controls whether NDI outputs can be used in the flow. Must be ENABLED to add NDI outputs. Default is DISABLED.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-ndiconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                ndi_config_property = mediaconnect_mixins.CfnFlowPropsMixin.NdiConfigProperty(
                    machine_name="machineName",
                    ndi_discovery_servers=[mediaconnect_mixins.CfnFlowPropsMixin.NdiDiscoveryServerConfigProperty(
                        discovery_server_address="discoveryServerAddress",
                        discovery_server_port=123,
                        vpc_interface_adapter="vpcInterfaceAdapter"
                    )],
                    ndi_state="ndiState"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8c75a4577adee00b175f16209d00f094abb6481d1532129d723d8ad643548591)
                check_type(argname="argument machine_name", value=machine_name, expected_type=type_hints["machine_name"])
                check_type(argname="argument ndi_discovery_servers", value=ndi_discovery_servers, expected_type=type_hints["ndi_discovery_servers"])
                check_type(argname="argument ndi_state", value=ndi_state, expected_type=type_hints["ndi_state"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if machine_name is not None:
                self._values["machine_name"] = machine_name
            if ndi_discovery_servers is not None:
                self._values["ndi_discovery_servers"] = ndi_discovery_servers
            if ndi_state is not None:
                self._values["ndi_state"] = ndi_state

        @builtins.property
        def machine_name(self) -> typing.Optional[builtins.str]:
            '''A prefix for the names of the NDI sources that the flow creates.

            If a custom name isn't specified, MediaConnect generates a unique 12-character ID as the prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-ndiconfig.html#cfn-mediaconnect-flow-ndiconfig-machinename
            '''
            result = self._values.get("machine_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ndi_discovery_servers(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.NdiDiscoveryServerConfigProperty"]]]]:
            '''A list of up to three NDI discovery server configurations.

            While not required by the API, this configuration is necessary for NDI functionality to work properly.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-ndiconfig.html#cfn-mediaconnect-flow-ndiconfig-ndidiscoveryservers
            '''
            result = self._values.get("ndi_discovery_servers")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.NdiDiscoveryServerConfigProperty"]]]], result)

        @builtins.property
        def ndi_state(self) -> typing.Optional[builtins.str]:
            '''A setting that controls whether NDI outputs can be used in the flow.

            Must be ENABLED to add NDI outputs. Default is DISABLED.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-ndiconfig.html#cfn-mediaconnect-flow-ndiconfig-ndistate
            '''
            result = self._values.get("ndi_state")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NdiConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.NdiDiscoveryServerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "discovery_server_address": "discoveryServerAddress",
            "discovery_server_port": "discoveryServerPort",
            "vpc_interface_adapter": "vpcInterfaceAdapter",
        },
    )
    class NdiDiscoveryServerConfigProperty:
        def __init__(
            self,
            *,
            discovery_server_address: typing.Optional[builtins.str] = None,
            discovery_server_port: typing.Optional[jsii.Number] = None,
            vpc_interface_adapter: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration settings for individual NDI discovery servers.

            A maximum of 3 servers is allowed.

            :param discovery_server_address: The unique network address of the NDI discovery server.
            :param discovery_server_port: The port for the NDI discovery server. Defaults to 5959 if a custom port isn't specified.
            :param vpc_interface_adapter: The identifier for the Virtual Private Cloud (VPC) network interface used by the flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-ndidiscoveryserverconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                ndi_discovery_server_config_property = mediaconnect_mixins.CfnFlowPropsMixin.NdiDiscoveryServerConfigProperty(
                    discovery_server_address="discoveryServerAddress",
                    discovery_server_port=123,
                    vpc_interface_adapter="vpcInterfaceAdapter"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4e63941cb194cb869b21e62c115e1d82bc66505667f6b015ce7e1bed094e7564)
                check_type(argname="argument discovery_server_address", value=discovery_server_address, expected_type=type_hints["discovery_server_address"])
                check_type(argname="argument discovery_server_port", value=discovery_server_port, expected_type=type_hints["discovery_server_port"])
                check_type(argname="argument vpc_interface_adapter", value=vpc_interface_adapter, expected_type=type_hints["vpc_interface_adapter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if discovery_server_address is not None:
                self._values["discovery_server_address"] = discovery_server_address
            if discovery_server_port is not None:
                self._values["discovery_server_port"] = discovery_server_port
            if vpc_interface_adapter is not None:
                self._values["vpc_interface_adapter"] = vpc_interface_adapter

        @builtins.property
        def discovery_server_address(self) -> typing.Optional[builtins.str]:
            '''The unique network address of the NDI discovery server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-ndidiscoveryserverconfig.html#cfn-mediaconnect-flow-ndidiscoveryserverconfig-discoveryserveraddress
            '''
            result = self._values.get("discovery_server_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def discovery_server_port(self) -> typing.Optional[jsii.Number]:
            '''The port for the NDI discovery server.

            Defaults to 5959 if a custom port isn't specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-ndidiscoveryserverconfig.html#cfn-mediaconnect-flow-ndidiscoveryserverconfig-discoveryserverport
            '''
            result = self._values.get("discovery_server_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def vpc_interface_adapter(self) -> typing.Optional[builtins.str]:
            '''The identifier for the Virtual Private Cloud (VPC) network interface used by the flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-ndidiscoveryserverconfig.html#cfn-mediaconnect-flow-ndidiscoveryserverconfig-vpcinterfaceadapter
            '''
            result = self._values.get("vpc_interface_adapter")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NdiDiscoveryServerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"role_arn": "roleArn", "secret_arn": "secretArn"},
    )
    class SecretsManagerEncryptionKeyConfigurationProperty:
        def __init__(
            self,
            *,
            role_arn: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration settings for transit encryption of a flow source using AWS Secrets Manager, including the secret ARN and role ARN.

            :param role_arn: The ARN of the IAM role used for transit encryption from the router output using AWS Secrets Manager.
            :param secret_arn: The ARN of the AWS Secrets Manager secret used for transit encryption from the router output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-secretsmanagerencryptionkeyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                secrets_manager_encryption_key_configuration_property = mediaconnect_mixins.CfnFlowPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                    role_arn="roleArn",
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__88e36b0007a06aa7eb0df151e49cc225dc0fbe8e6ea03542c857bda214d215e7)
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM role used for transit encryption from the router output using AWS Secrets Manager.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-secretsmanagerencryptionkeyconfiguration.html#cfn-mediaconnect-flow-secretsmanagerencryptionkeyconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the AWS Secrets Manager secret used for transit encryption from the router output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-secretsmanagerencryptionkeyconfiguration.html#cfn-mediaconnect-flow-secretsmanagerencryptionkeyconfiguration-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecretsManagerEncryptionKeyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.SilentAudioProperty",
        jsii_struct_bases=[],
        name_mapping={"state": "state", "threshold_seconds": "thresholdSeconds"},
    )
    class SilentAudioProperty:
        def __init__(
            self,
            *,
            state: typing.Optional[builtins.str] = None,
            threshold_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Configures settings for the ``SilentAudio`` metric.

            :param state: Indicates whether the ``SilentAudio`` metric is enabled or disabled.
            :param threshold_seconds: Specifies the number of consecutive seconds of silence that triggers an event or alert.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-silentaudio.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                silent_audio_property = mediaconnect_mixins.CfnFlowPropsMixin.SilentAudioProperty(
                    state="state",
                    threshold_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__66ccd0359fdc05267a5b960587186c05c5e6bef117b3711a6a0781b155106b27)
                check_type(argname="argument state", value=state, expected_type=type_hints["state"])
                check_type(argname="argument threshold_seconds", value=threshold_seconds, expected_type=type_hints["threshold_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if state is not None:
                self._values["state"] = state
            if threshold_seconds is not None:
                self._values["threshold_seconds"] = threshold_seconds

        @builtins.property
        def state(self) -> typing.Optional[builtins.str]:
            '''Indicates whether the ``SilentAudio`` metric is enabled or disabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-silentaudio.html#cfn-mediaconnect-flow-silentaudio-state
            '''
            result = self._values.get("state")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def threshold_seconds(self) -> typing.Optional[jsii.Number]:
            '''Specifies the number of consecutive seconds of silence that triggers an event or alert.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-silentaudio.html#cfn-mediaconnect-flow-silentaudio-thresholdseconds
            '''
            result = self._values.get("threshold_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SilentAudioProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.SourceMonitoringConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "audio_monitoring_settings": "audioMonitoringSettings",
            "content_quality_analysis_state": "contentQualityAnalysisState",
            "thumbnail_state": "thumbnailState",
            "video_monitoring_settings": "videoMonitoringSettings",
        },
    )
    class SourceMonitoringConfigProperty:
        def __init__(
            self,
            *,
            audio_monitoring_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.AudioMonitoringSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            content_quality_analysis_state: typing.Optional[builtins.str] = None,
            thumbnail_state: typing.Optional[builtins.str] = None,
            video_monitoring_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.VideoMonitoringSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``SourceMonitoringConfig`` property type specifies the source monitoring settings for an ``AWS::MediaConnect::Flow`` .

            :param audio_monitoring_settings: Contains the settings for audio stream metrics monitoring.
            :param content_quality_analysis_state: Indicates whether content quality analysis is enabled or disabled.
            :param thumbnail_state: The current state of the thumbnail monitoring. - If you don't explicitly specify a value when creating a flow, no thumbnail state will be set. - If you update an existing flow and remove a previously set thumbnail state, the value will change to ``DISABLED`` .
            :param video_monitoring_settings: Contains the settings for video stream metrics monitoring.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-sourcemonitoringconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                source_monitoring_config_property = mediaconnect_mixins.CfnFlowPropsMixin.SourceMonitoringConfigProperty(
                    audio_monitoring_settings=[mediaconnect_mixins.CfnFlowPropsMixin.AudioMonitoringSettingProperty(
                        silent_audio=mediaconnect_mixins.CfnFlowPropsMixin.SilentAudioProperty(
                            state="state",
                            threshold_seconds=123
                        )
                    )],
                    content_quality_analysis_state="contentQualityAnalysisState",
                    thumbnail_state="thumbnailState",
                    video_monitoring_settings=[mediaconnect_mixins.CfnFlowPropsMixin.VideoMonitoringSettingProperty(
                        black_frames=mediaconnect_mixins.CfnFlowPropsMixin.BlackFramesProperty(
                            state="state",
                            threshold_seconds=123
                        ),
                        frozen_frames=mediaconnect_mixins.CfnFlowPropsMixin.FrozenFramesProperty(
                            state="state",
                            threshold_seconds=123
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__89a8935dc30e2c4fc5e69fdc55620ba6135fcc03bc03c337c37f0e4a98b90b21)
                check_type(argname="argument audio_monitoring_settings", value=audio_monitoring_settings, expected_type=type_hints["audio_monitoring_settings"])
                check_type(argname="argument content_quality_analysis_state", value=content_quality_analysis_state, expected_type=type_hints["content_quality_analysis_state"])
                check_type(argname="argument thumbnail_state", value=thumbnail_state, expected_type=type_hints["thumbnail_state"])
                check_type(argname="argument video_monitoring_settings", value=video_monitoring_settings, expected_type=type_hints["video_monitoring_settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if audio_monitoring_settings is not None:
                self._values["audio_monitoring_settings"] = audio_monitoring_settings
            if content_quality_analysis_state is not None:
                self._values["content_quality_analysis_state"] = content_quality_analysis_state
            if thumbnail_state is not None:
                self._values["thumbnail_state"] = thumbnail_state
            if video_monitoring_settings is not None:
                self._values["video_monitoring_settings"] = video_monitoring_settings

        @builtins.property
        def audio_monitoring_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.AudioMonitoringSettingProperty"]]]]:
            '''Contains the settings for audio stream metrics monitoring.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-sourcemonitoringconfig.html#cfn-mediaconnect-flow-sourcemonitoringconfig-audiomonitoringsettings
            '''
            result = self._values.get("audio_monitoring_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.AudioMonitoringSettingProperty"]]]], result)

        @builtins.property
        def content_quality_analysis_state(self) -> typing.Optional[builtins.str]:
            '''Indicates whether content quality analysis is enabled or disabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-sourcemonitoringconfig.html#cfn-mediaconnect-flow-sourcemonitoringconfig-contentqualityanalysisstate
            '''
            result = self._values.get("content_quality_analysis_state")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def thumbnail_state(self) -> typing.Optional[builtins.str]:
            '''The current state of the thumbnail monitoring.

            - If you don't explicitly specify a value when creating a flow, no thumbnail state will be set.
            - If you update an existing flow and remove a previously set thumbnail state, the value will change to ``DISABLED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-sourcemonitoringconfig.html#cfn-mediaconnect-flow-sourcemonitoringconfig-thumbnailstate
            '''
            result = self._values.get("thumbnail_state")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def video_monitoring_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.VideoMonitoringSettingProperty"]]]]:
            '''Contains the settings for video stream metrics monitoring.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-sourcemonitoringconfig.html#cfn-mediaconnect-flow-sourcemonitoringconfig-videomonitoringsettings
            '''
            result = self._values.get("video_monitoring_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.VideoMonitoringSettingProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceMonitoringConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.SourcePriorityProperty",
        jsii_struct_bases=[],
        name_mapping={"primary_source": "primarySource"},
    )
    class SourcePriorityProperty:
        def __init__(
            self,
            *,
            primary_source: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The priority you want to assign to a source.

            You can have a primary stream and a backup stream or two equally prioritized streams.

            :param primary_source: The name of the source you choose as the primary source for this flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-sourcepriority.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                source_priority_property = mediaconnect_mixins.CfnFlowPropsMixin.SourcePriorityProperty(
                    primary_source="primarySource"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__88bbf27ba593734e8631a00f0d25fe4ac56ff79dc9467954cecbc3ca54601267)
                check_type(argname="argument primary_source", value=primary_source, expected_type=type_hints["primary_source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if primary_source is not None:
                self._values["primary_source"] = primary_source

        @builtins.property
        def primary_source(self) -> typing.Optional[builtins.str]:
            '''The name of the source you choose as the primary source for this flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-sourcepriority.html#cfn-mediaconnect-flow-sourcepriority-primarysource
            '''
            result = self._values.get("primary_source")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourcePriorityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.SourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "decryption": "decryption",
            "description": "description",
            "entitlement_arn": "entitlementArn",
            "gateway_bridge_source": "gatewayBridgeSource",
            "ingest_ip": "ingestIp",
            "ingest_port": "ingestPort",
            "max_bitrate": "maxBitrate",
            "max_latency": "maxLatency",
            "max_sync_buffer": "maxSyncBuffer",
            "media_stream_source_configurations": "mediaStreamSourceConfigurations",
            "min_latency": "minLatency",
            "name": "name",
            "protocol": "protocol",
            "router_integration_state": "routerIntegrationState",
            "router_integration_transit_decryption": "routerIntegrationTransitDecryption",
            "sender_control_port": "senderControlPort",
            "sender_ip_address": "senderIpAddress",
            "source_arn": "sourceArn",
            "source_ingest_port": "sourceIngestPort",
            "source_listener_address": "sourceListenerAddress",
            "source_listener_port": "sourceListenerPort",
            "stream_id": "streamId",
            "vpc_interface_name": "vpcInterfaceName",
            "whitelist_cidr": "whitelistCidr",
        },
    )
    class SourceProperty:
        def __init__(
            self,
            *,
            decryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.EncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            description: typing.Optional[builtins.str] = None,
            entitlement_arn: typing.Optional[builtins.str] = None,
            gateway_bridge_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.GatewayBridgeSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ingest_ip: typing.Optional[builtins.str] = None,
            ingest_port: typing.Optional[jsii.Number] = None,
            max_bitrate: typing.Optional[jsii.Number] = None,
            max_latency: typing.Optional[jsii.Number] = None,
            max_sync_buffer: typing.Optional[jsii.Number] = None,
            media_stream_source_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.MediaStreamSourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            min_latency: typing.Optional[jsii.Number] = None,
            name: typing.Optional[builtins.str] = None,
            protocol: typing.Optional[builtins.str] = None,
            router_integration_state: typing.Optional[builtins.str] = None,
            router_integration_transit_decryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.FlowTransitEncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sender_control_port: typing.Optional[jsii.Number] = None,
            sender_ip_address: typing.Optional[builtins.str] = None,
            source_arn: typing.Optional[builtins.str] = None,
            source_ingest_port: typing.Optional[builtins.str] = None,
            source_listener_address: typing.Optional[builtins.str] = None,
            source_listener_port: typing.Optional[jsii.Number] = None,
            stream_id: typing.Optional[builtins.str] = None,
            vpc_interface_name: typing.Optional[builtins.str] = None,
            whitelist_cidr: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The details of the sources of the flow.

            If you are creating a flow with a VPC source, you must first create the flow with a temporary standard source by doing the following:

            - Use CloudFormation to create a flow with a standard source that uses the flow’s public IP address.
            - Use CloudFormation to create the VPC interface to add to this flow. This can also be done as part of the previous step.
            - After CloudFormation has created the flow and the VPC interface, update the source to point to the VPC interface that you created.

            :param decryption: The type of encryption that is used on the content ingested from this source.
            :param description: A description for the source. This value is not used or seen outside of the current MediaConnect account.
            :param entitlement_arn: The ARN of the entitlement that allows you to subscribe to content that comes from another AWS account. The entitlement is set by the content originator and the ARN is generated as part of the originator's flow.
            :param gateway_bridge_source: The source configuration for cloud flows receiving a stream from a bridge.
            :param ingest_ip: The IP address that the flow will be listening on for incoming content.
            :param ingest_port: The port that the flow will be listening on for incoming content.
            :param max_bitrate: The maximum bitrate for RIST, RTP, and RTP-FEC streams.
            :param max_latency: The maximum latency in milliseconds for a RIST or Zixi-based source.
            :param max_sync_buffer: The size of the buffer (in milliseconds) to use to sync incoming source data.
            :param media_stream_source_configurations: The media streams that are associated with the source, and the parameters for those associations.
            :param min_latency: The minimum latency in milliseconds for SRT-based streams. In streams that use the SRT protocol, this value that you set on your MediaConnect source or output represents the minimal potential latency of that connection. The latency of the stream is set to the highest number between the sender’s minimum latency and the receiver’s minimum latency.
            :param name: The name of the source.
            :param protocol: The protocol that is used by the source. AWS CloudFormation does not currently support CDI or ST 2110 JPEG XS source protocols. .. epigraph:: AWS Elemental MediaConnect no longer supports the Fujitsu QoS protocol. This reference is maintained for legacy purposes only.
            :param router_integration_state: Indicates if router integration is enabled or disabled on the flow source.
            :param router_integration_transit_decryption: The decryption configuration for the flow source when router integration is enabled.
            :param sender_control_port: The port that the flow uses to send outbound requests to initiate connection with the sender.
            :param sender_ip_address: The IP address that the flow communicates with to initiate connection with the sender.
            :param source_arn: The ARN of the source.
            :param source_ingest_port: The port that the flow listens on for incoming content. If the protocol of the source is Zixi, the port must be set to 2088.
            :param source_listener_address: Source IP or domain name for SRT-caller protocol.
            :param source_listener_port: Source port for SRT-caller protocol.
            :param stream_id: The stream ID that you want to use for the transport. This parameter applies only to Zixi-based streams.
            :param vpc_interface_name: The name of the VPC interface that is used for this source.
            :param whitelist_cidr: The range of IP addresses that should be allowed to contribute content to your source. These IP addresses should be in the form of a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                # automatic: Any
                
                source_property = mediaconnect_mixins.CfnFlowPropsMixin.SourceProperty(
                    decryption=mediaconnect_mixins.CfnFlowPropsMixin.EncryptionProperty(
                        algorithm="algorithm",
                        constant_initialization_vector="constantInitializationVector",
                        device_id="deviceId",
                        key_type="keyType",
                        region="region",
                        resource_id="resourceId",
                        role_arn="roleArn",
                        secret_arn="secretArn",
                        url="url"
                    ),
                    description="description",
                    entitlement_arn="entitlementArn",
                    gateway_bridge_source=mediaconnect_mixins.CfnFlowPropsMixin.GatewayBridgeSourceProperty(
                        bridge_arn="bridgeArn",
                        vpc_interface_attachment=mediaconnect_mixins.CfnFlowPropsMixin.VpcInterfaceAttachmentProperty(
                            vpc_interface_name="vpcInterfaceName"
                        )
                    ),
                    ingest_ip="ingestIp",
                    ingest_port=123,
                    max_bitrate=123,
                    max_latency=123,
                    max_sync_buffer=123,
                    media_stream_source_configurations=[mediaconnect_mixins.CfnFlowPropsMixin.MediaStreamSourceConfigurationProperty(
                        encoding_name="encodingName",
                        input_configurations=[mediaconnect_mixins.CfnFlowPropsMixin.InputConfigurationProperty(
                            input_port=123,
                            interface=mediaconnect_mixins.CfnFlowPropsMixin.InterfaceProperty(
                                name="name"
                            )
                        )],
                        media_stream_name="mediaStreamName"
                    )],
                    min_latency=123,
                    name="name",
                    protocol="protocol",
                    router_integration_state="routerIntegrationState",
                    router_integration_transit_decryption=mediaconnect_mixins.CfnFlowPropsMixin.FlowTransitEncryptionProperty(
                        encryption_key_configuration=mediaconnect_mixins.CfnFlowPropsMixin.FlowTransitEncryptionKeyConfigurationProperty(
                            automatic=automatic,
                            secrets_manager=mediaconnect_mixins.CfnFlowPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                role_arn="roleArn",
                                secret_arn="secretArn"
                            )
                        ),
                        encryption_key_type="encryptionKeyType"
                    ),
                    sender_control_port=123,
                    sender_ip_address="senderIpAddress",
                    source_arn="sourceArn",
                    source_ingest_port="sourceIngestPort",
                    source_listener_address="sourceListenerAddress",
                    source_listener_port=123,
                    stream_id="streamId",
                    vpc_interface_name="vpcInterfaceName",
                    whitelist_cidr="whitelistCidr"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bd16c3f17bc4d41a7c2e2136ce29868227ab500eeb3d6f5a1ee1adfed3966ce7)
                check_type(argname="argument decryption", value=decryption, expected_type=type_hints["decryption"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument entitlement_arn", value=entitlement_arn, expected_type=type_hints["entitlement_arn"])
                check_type(argname="argument gateway_bridge_source", value=gateway_bridge_source, expected_type=type_hints["gateway_bridge_source"])
                check_type(argname="argument ingest_ip", value=ingest_ip, expected_type=type_hints["ingest_ip"])
                check_type(argname="argument ingest_port", value=ingest_port, expected_type=type_hints["ingest_port"])
                check_type(argname="argument max_bitrate", value=max_bitrate, expected_type=type_hints["max_bitrate"])
                check_type(argname="argument max_latency", value=max_latency, expected_type=type_hints["max_latency"])
                check_type(argname="argument max_sync_buffer", value=max_sync_buffer, expected_type=type_hints["max_sync_buffer"])
                check_type(argname="argument media_stream_source_configurations", value=media_stream_source_configurations, expected_type=type_hints["media_stream_source_configurations"])
                check_type(argname="argument min_latency", value=min_latency, expected_type=type_hints["min_latency"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument router_integration_state", value=router_integration_state, expected_type=type_hints["router_integration_state"])
                check_type(argname="argument router_integration_transit_decryption", value=router_integration_transit_decryption, expected_type=type_hints["router_integration_transit_decryption"])
                check_type(argname="argument sender_control_port", value=sender_control_port, expected_type=type_hints["sender_control_port"])
                check_type(argname="argument sender_ip_address", value=sender_ip_address, expected_type=type_hints["sender_ip_address"])
                check_type(argname="argument source_arn", value=source_arn, expected_type=type_hints["source_arn"])
                check_type(argname="argument source_ingest_port", value=source_ingest_port, expected_type=type_hints["source_ingest_port"])
                check_type(argname="argument source_listener_address", value=source_listener_address, expected_type=type_hints["source_listener_address"])
                check_type(argname="argument source_listener_port", value=source_listener_port, expected_type=type_hints["source_listener_port"])
                check_type(argname="argument stream_id", value=stream_id, expected_type=type_hints["stream_id"])
                check_type(argname="argument vpc_interface_name", value=vpc_interface_name, expected_type=type_hints["vpc_interface_name"])
                check_type(argname="argument whitelist_cidr", value=whitelist_cidr, expected_type=type_hints["whitelist_cidr"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if decryption is not None:
                self._values["decryption"] = decryption
            if description is not None:
                self._values["description"] = description
            if entitlement_arn is not None:
                self._values["entitlement_arn"] = entitlement_arn
            if gateway_bridge_source is not None:
                self._values["gateway_bridge_source"] = gateway_bridge_source
            if ingest_ip is not None:
                self._values["ingest_ip"] = ingest_ip
            if ingest_port is not None:
                self._values["ingest_port"] = ingest_port
            if max_bitrate is not None:
                self._values["max_bitrate"] = max_bitrate
            if max_latency is not None:
                self._values["max_latency"] = max_latency
            if max_sync_buffer is not None:
                self._values["max_sync_buffer"] = max_sync_buffer
            if media_stream_source_configurations is not None:
                self._values["media_stream_source_configurations"] = media_stream_source_configurations
            if min_latency is not None:
                self._values["min_latency"] = min_latency
            if name is not None:
                self._values["name"] = name
            if protocol is not None:
                self._values["protocol"] = protocol
            if router_integration_state is not None:
                self._values["router_integration_state"] = router_integration_state
            if router_integration_transit_decryption is not None:
                self._values["router_integration_transit_decryption"] = router_integration_transit_decryption
            if sender_control_port is not None:
                self._values["sender_control_port"] = sender_control_port
            if sender_ip_address is not None:
                self._values["sender_ip_address"] = sender_ip_address
            if source_arn is not None:
                self._values["source_arn"] = source_arn
            if source_ingest_port is not None:
                self._values["source_ingest_port"] = source_ingest_port
            if source_listener_address is not None:
                self._values["source_listener_address"] = source_listener_address
            if source_listener_port is not None:
                self._values["source_listener_port"] = source_listener_port
            if stream_id is not None:
                self._values["stream_id"] = stream_id
            if vpc_interface_name is not None:
                self._values["vpc_interface_name"] = vpc_interface_name
            if whitelist_cidr is not None:
                self._values["whitelist_cidr"] = whitelist_cidr

        @builtins.property
        def decryption(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.EncryptionProperty"]]:
            '''The type of encryption that is used on the content ingested from this source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-decryption
            '''
            result = self._values.get("decryption")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.EncryptionProperty"]], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description for the source.

            This value is not used or seen outside of the current MediaConnect account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def entitlement_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the entitlement that allows you to subscribe to content that comes from another AWS account.

            The entitlement is set by the content originator and the ARN is generated as part of the originator's flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-entitlementarn
            '''
            result = self._values.get("entitlement_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def gateway_bridge_source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.GatewayBridgeSourceProperty"]]:
            '''The source configuration for cloud flows receiving a stream from a bridge.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-gatewaybridgesource
            '''
            result = self._values.get("gateway_bridge_source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.GatewayBridgeSourceProperty"]], result)

        @builtins.property
        def ingest_ip(self) -> typing.Optional[builtins.str]:
            '''The IP address that the flow will be listening on for incoming content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-ingestip
            '''
            result = self._values.get("ingest_ip")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ingest_port(self) -> typing.Optional[jsii.Number]:
            '''The port that the flow will be listening on for incoming content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-ingestport
            '''
            result = self._values.get("ingest_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_bitrate(self) -> typing.Optional[jsii.Number]:
            '''The maximum bitrate for RIST, RTP, and RTP-FEC streams.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-maxbitrate
            '''
            result = self._values.get("max_bitrate")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_latency(self) -> typing.Optional[jsii.Number]:
            '''The maximum latency in milliseconds for a RIST or Zixi-based source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-maxlatency
            '''
            result = self._values.get("max_latency")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_sync_buffer(self) -> typing.Optional[jsii.Number]:
            '''The size of the buffer (in milliseconds) to use to sync incoming source data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-maxsyncbuffer
            '''
            result = self._values.get("max_sync_buffer")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def media_stream_source_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.MediaStreamSourceConfigurationProperty"]]]]:
            '''The media streams that are associated with the source, and the parameters for those associations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-mediastreamsourceconfigurations
            '''
            result = self._values.get("media_stream_source_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.MediaStreamSourceConfigurationProperty"]]]], result)

        @builtins.property
        def min_latency(self) -> typing.Optional[jsii.Number]:
            '''The minimum latency in milliseconds for SRT-based streams.

            In streams that use the SRT protocol, this value that you set on your MediaConnect source or output represents the minimal potential latency of that connection. The latency of the stream is set to the highest number between the sender’s minimum latency and the receiver’s minimum latency.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-minlatency
            '''
            result = self._values.get("min_latency")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The protocol that is used by the source.

            AWS CloudFormation does not currently support CDI or ST 2110 JPEG XS source protocols.
            .. epigraph::

               AWS Elemental MediaConnect no longer supports the Fujitsu QoS protocol. This reference is maintained for legacy purposes only.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def router_integration_state(self) -> typing.Optional[builtins.str]:
            '''Indicates if router integration is enabled or disabled on the flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-routerintegrationstate
            '''
            result = self._values.get("router_integration_state")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def router_integration_transit_decryption(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.FlowTransitEncryptionProperty"]]:
            '''The decryption configuration for the flow source when router integration is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-routerintegrationtransitdecryption
            '''
            result = self._values.get("router_integration_transit_decryption")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.FlowTransitEncryptionProperty"]], result)

        @builtins.property
        def sender_control_port(self) -> typing.Optional[jsii.Number]:
            '''The port that the flow uses to send outbound requests to initiate connection with the sender.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-sendercontrolport
            '''
            result = self._values.get("sender_control_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def sender_ip_address(self) -> typing.Optional[builtins.str]:
            '''The IP address that the flow communicates with to initiate connection with the sender.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-senderipaddress
            '''
            result = self._values.get("sender_ip_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-sourcearn
            '''
            result = self._values.get("source_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_ingest_port(self) -> typing.Optional[builtins.str]:
            '''The port that the flow listens on for incoming content.

            If the protocol of the source is Zixi, the port must be set to 2088.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-sourceingestport
            '''
            result = self._values.get("source_ingest_port")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_listener_address(self) -> typing.Optional[builtins.str]:
            '''Source IP or domain name for SRT-caller protocol.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-sourcelisteneraddress
            '''
            result = self._values.get("source_listener_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_listener_port(self) -> typing.Optional[jsii.Number]:
            '''Source port for SRT-caller protocol.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-sourcelistenerport
            '''
            result = self._values.get("source_listener_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stream_id(self) -> typing.Optional[builtins.str]:
            '''The stream ID that you want to use for the transport.

            This parameter applies only to Zixi-based streams.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-streamid
            '''
            result = self._values.get("stream_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_interface_name(self) -> typing.Optional[builtins.str]:
            '''The name of the VPC interface that is used for this source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-vpcinterfacename
            '''
            result = self._values.get("vpc_interface_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def whitelist_cidr(self) -> typing.Optional[builtins.str]:
            '''The range of IP addresses that should be allowed to contribute content to your source.

            These IP addresses should be in the form of a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-whitelistcidr
            '''
            result = self._values.get("whitelist_cidr")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.VideoMonitoringSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"black_frames": "blackFrames", "frozen_frames": "frozenFrames"},
    )
    class VideoMonitoringSettingProperty:
        def __init__(
            self,
            *,
            black_frames: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.BlackFramesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            frozen_frames: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowPropsMixin.FrozenFramesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the configuration for video stream metrics monitoring.

            :param black_frames: Detects video frames that are black.
            :param frozen_frames: Detects video frames that have not changed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-videomonitoringsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                video_monitoring_setting_property = mediaconnect_mixins.CfnFlowPropsMixin.VideoMonitoringSettingProperty(
                    black_frames=mediaconnect_mixins.CfnFlowPropsMixin.BlackFramesProperty(
                        state="state",
                        threshold_seconds=123
                    ),
                    frozen_frames=mediaconnect_mixins.CfnFlowPropsMixin.FrozenFramesProperty(
                        state="state",
                        threshold_seconds=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3baf104e902e74c7124d7bd34eb814271ebe501b368146cac7983db07a77f943)
                check_type(argname="argument black_frames", value=black_frames, expected_type=type_hints["black_frames"])
                check_type(argname="argument frozen_frames", value=frozen_frames, expected_type=type_hints["frozen_frames"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if black_frames is not None:
                self._values["black_frames"] = black_frames
            if frozen_frames is not None:
                self._values["frozen_frames"] = frozen_frames

        @builtins.property
        def black_frames(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.BlackFramesProperty"]]:
            '''Detects video frames that are black.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-videomonitoringsetting.html#cfn-mediaconnect-flow-videomonitoringsetting-blackframes
            '''
            result = self._values.get("black_frames")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.BlackFramesProperty"]], result)

        @builtins.property
        def frozen_frames(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.FrozenFramesProperty"]]:
            '''Detects video frames that have not changed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-videomonitoringsetting.html#cfn-mediaconnect-flow-videomonitoringsetting-frozenframes
            '''
            result = self._values.get("frozen_frames")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowPropsMixin.FrozenFramesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VideoMonitoringSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.VpcInterfaceAttachmentProperty",
        jsii_struct_bases=[],
        name_mapping={"vpc_interface_name": "vpcInterfaceName"},
    )
    class VpcInterfaceAttachmentProperty:
        def __init__(
            self,
            *,
            vpc_interface_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The settings for attaching a VPC interface to an resource.

            :param vpc_interface_name: The name of the VPC interface to use for this resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-vpcinterfaceattachment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                vpc_interface_attachment_property = mediaconnect_mixins.CfnFlowPropsMixin.VpcInterfaceAttachmentProperty(
                    vpc_interface_name="vpcInterfaceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6ceb24c3a476989afbe314ad466d1b1503fce62659ba5405c4f26cc134c8051c)
                check_type(argname="argument vpc_interface_name", value=vpc_interface_name, expected_type=type_hints["vpc_interface_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if vpc_interface_name is not None:
                self._values["vpc_interface_name"] = vpc_interface_name

        @builtins.property
        def vpc_interface_name(self) -> typing.Optional[builtins.str]:
            '''The name of the VPC interface to use for this resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-vpcinterfaceattachment.html#cfn-mediaconnect-flow-vpcinterfaceattachment-vpcinterfacename
            '''
            result = self._values.get("vpc_interface_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcInterfaceAttachmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowPropsMixin.VpcInterfaceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "network_interface_ids": "networkInterfaceIds",
            "network_interface_type": "networkInterfaceType",
            "role_arn": "roleArn",
            "security_group_ids": "securityGroupIds",
            "subnet_id": "subnetId",
        },
    )
    class VpcInterfaceProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            network_interface_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            network_interface_type: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The details of a VPC interface.

            .. epigraph::

               When configuring VPC interfaces for NDI outputs, keep in mind the following:

               - VPC interfaces must be defined as nested attributes within the ``AWS::MediaConnect::Flow`` resource, and not within the top-level ``AWS::MediaConnect::FlowVpcInterface`` resource.
               - There's a maximum limit of three VPC interfaces for each flow. If you've already reached this limit, you can't update the flow to use a different VPC interface without first removing an existing one.

               To update your VPC interfaces in this scenario, you must first remove the VPC interface that’s not being used. Next, add the new VPC interfaces. Lastly, update the ``VpcInterfaceAdapter`` in the ``NDIConfig`` property. These changes must be performed as separate manual operations and cannot be done through a single template update.

            :param name: Immutable and has to be a unique against other VpcInterfaces in this Flow.
            :param network_interface_ids: IDs of the network interfaces created in customer's account by MediaConnect .
            :param network_interface_type: The type of network interface.
            :param role_arn: A role Arn MediaConnect can assume to create ENIs in your account.
            :param security_group_ids: Security Group IDs to be used on ENI.
            :param subnet_id: Subnet must be in the AZ of the Flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-vpcinterface.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                vpc_interface_property = mediaconnect_mixins.CfnFlowPropsMixin.VpcInterfaceProperty(
                    name="name",
                    network_interface_ids=["networkInterfaceIds"],
                    network_interface_type="networkInterfaceType",
                    role_arn="roleArn",
                    security_group_ids=["securityGroupIds"],
                    subnet_id="subnetId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9eb244b8706c9591d328c0eeb7fbff9a9ec02e83875368672605d8c9f548856c)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument network_interface_ids", value=network_interface_ids, expected_type=type_hints["network_interface_ids"])
                check_type(argname="argument network_interface_type", value=network_interface_type, expected_type=type_hints["network_interface_type"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if network_interface_ids is not None:
                self._values["network_interface_ids"] = network_interface_ids
            if network_interface_type is not None:
                self._values["network_interface_type"] = network_interface_type
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_id is not None:
                self._values["subnet_id"] = subnet_id

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''Immutable and has to be a unique against other VpcInterfaces in this Flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-vpcinterface.html#cfn-mediaconnect-flow-vpcinterface-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def network_interface_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''IDs of the network interfaces created in customer's account by MediaConnect .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-vpcinterface.html#cfn-mediaconnect-flow-vpcinterface-networkinterfaceids
            '''
            result = self._values.get("network_interface_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def network_interface_type(self) -> typing.Optional[builtins.str]:
            '''The type of network interface.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-vpcinterface.html#cfn-mediaconnect-flow-vpcinterface-networkinterfacetype
            '''
            result = self._values.get("network_interface_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''A role Arn MediaConnect can assume to create ENIs in your account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-vpcinterface.html#cfn-mediaconnect-flow-vpcinterface-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Security Group IDs to be used on ENI.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-vpcinterface.html#cfn-mediaconnect-flow-vpcinterface-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_id(self) -> typing.Optional[builtins.str]:
            '''Subnet must be in the AZ of the Flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-vpcinterface.html#cfn-mediaconnect-flow-vpcinterface-subnetid
            '''
            result = self._values.get("subnet_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcInterfaceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowSourceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "decryption": "decryption",
        "description": "description",
        "entitlement_arn": "entitlementArn",
        "flow_arn": "flowArn",
        "gateway_bridge_source": "gatewayBridgeSource",
        "ingest_port": "ingestPort",
        "max_bitrate": "maxBitrate",
        "max_latency": "maxLatency",
        "min_latency": "minLatency",
        "name": "name",
        "protocol": "protocol",
        "sender_control_port": "senderControlPort",
        "sender_ip_address": "senderIpAddress",
        "source_listener_address": "sourceListenerAddress",
        "source_listener_port": "sourceListenerPort",
        "stream_id": "streamId",
        "vpc_interface_name": "vpcInterfaceName",
        "whitelist_cidr": "whitelistCidr",
    },
)
class CfnFlowSourceMixinProps:
    def __init__(
        self,
        *,
        decryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowSourcePropsMixin.EncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        entitlement_arn: typing.Optional[builtins.str] = None,
        flow_arn: typing.Optional[builtins.str] = None,
        gateway_bridge_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowSourcePropsMixin.GatewayBridgeSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ingest_port: typing.Optional[jsii.Number] = None,
        max_bitrate: typing.Optional[jsii.Number] = None,
        max_latency: typing.Optional[jsii.Number] = None,
        min_latency: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        sender_control_port: typing.Optional[jsii.Number] = None,
        sender_ip_address: typing.Optional[builtins.str] = None,
        source_listener_address: typing.Optional[builtins.str] = None,
        source_listener_port: typing.Optional[jsii.Number] = None,
        stream_id: typing.Optional[builtins.str] = None,
        vpc_interface_name: typing.Optional[builtins.str] = None,
        whitelist_cidr: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnFlowSourcePropsMixin.

        :param decryption: The type of encryption that is used on the content ingested from this source. Allowable encryption types: static-key.
        :param description: A description for the source. This value is not used or seen outside of the current MediaConnect account.
        :param entitlement_arn: The ARN of the entitlement that allows you to subscribe to this flow. The entitlement is set by the flow originator, and the ARN is generated as part of the originator's flow.
        :param flow_arn: The Amazon Resource Name (ARN) of the flow this source is connected to. The flow must have Failover enabled to add an additional source.
        :param gateway_bridge_source: The bridge's source.
        :param ingest_port: The port that the flow listens on for incoming content. If the protocol of the source is Zixi, the port must be set to 2088.
        :param max_bitrate: The smoothing max bitrate (in bps) for RIST, RTP, and RTP-FEC streams.
        :param max_latency: The maximum latency in milliseconds. This parameter applies only to RIST-based and Zixi-based streams.
        :param min_latency: The minimum latency in milliseconds for SRT-based streams. In streams that use the SRT protocol, this value that you set on your MediaConnect source or output represents the minimal potential latency of that connection. The latency of the stream is set to the highest number between the sender’s minimum latency and the receiver’s minimum latency.
        :param name: The name of the source.
        :param protocol: The protocol that the source uses to deliver the content to MediaConnect. Adding additional sources to an existing flow requires Failover to be enabled. When you enable Failover, the additional source must use the same protocol as the existing source. Only the following protocols support failover: Zixi-push, RTP-FEC, RTP, RIST and SRT protocols. If you use failover with SRT caller or listener, the ``FailoverMode`` property must be set to ``FAILOVER`` . The ``FailoverMode`` property is found in the ``FailoverConfig`` resource of the same flow ARN you used for the source's ``FlowArn`` property. SRT caller/listener does not support merge mode failover.
        :param sender_control_port: The port that the flow uses to send outbound requests to initiate connection with the sender.
        :param sender_ip_address: The IP address that the flow communicates with to initiate connection with the sender.
        :param source_listener_address: Source IP or domain name for SRT-caller protocol.
        :param source_listener_port: Source port for SRT-caller protocol.
        :param stream_id: The stream ID that you want to use for this transport. This parameter applies only to Zixi and SRT caller-based streams.
        :param vpc_interface_name: The name of the VPC interface to use for this source.
        :param whitelist_cidr: The range of IP addresses that should be allowed to contribute content to your source. These IP addresses should be in the form of a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
            
            cfn_flow_source_mixin_props = mediaconnect_mixins.CfnFlowSourceMixinProps(
                decryption=mediaconnect_mixins.CfnFlowSourcePropsMixin.EncryptionProperty(
                    algorithm="algorithm",
                    constant_initialization_vector="constantInitializationVector",
                    device_id="deviceId",
                    key_type="keyType",
                    region="region",
                    resource_id="resourceId",
                    role_arn="roleArn",
                    secret_arn="secretArn",
                    url="url"
                ),
                description="description",
                entitlement_arn="entitlementArn",
                flow_arn="flowArn",
                gateway_bridge_source=mediaconnect_mixins.CfnFlowSourcePropsMixin.GatewayBridgeSourceProperty(
                    bridge_arn="bridgeArn",
                    vpc_interface_attachment=mediaconnect_mixins.CfnFlowSourcePropsMixin.VpcInterfaceAttachmentProperty(
                        vpc_interface_name="vpcInterfaceName"
                    )
                ),
                ingest_port=123,
                max_bitrate=123,
                max_latency=123,
                min_latency=123,
                name="name",
                protocol="protocol",
                sender_control_port=123,
                sender_ip_address="senderIpAddress",
                source_listener_address="sourceListenerAddress",
                source_listener_port=123,
                stream_id="streamId",
                vpc_interface_name="vpcInterfaceName",
                whitelist_cidr="whitelistCidr"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0aee06c84560ce0699cf9c577beb5764e49775182941faa2b2eaf2c9ba03998)
            check_type(argname="argument decryption", value=decryption, expected_type=type_hints["decryption"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument entitlement_arn", value=entitlement_arn, expected_type=type_hints["entitlement_arn"])
            check_type(argname="argument flow_arn", value=flow_arn, expected_type=type_hints["flow_arn"])
            check_type(argname="argument gateway_bridge_source", value=gateway_bridge_source, expected_type=type_hints["gateway_bridge_source"])
            check_type(argname="argument ingest_port", value=ingest_port, expected_type=type_hints["ingest_port"])
            check_type(argname="argument max_bitrate", value=max_bitrate, expected_type=type_hints["max_bitrate"])
            check_type(argname="argument max_latency", value=max_latency, expected_type=type_hints["max_latency"])
            check_type(argname="argument min_latency", value=min_latency, expected_type=type_hints["min_latency"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument sender_control_port", value=sender_control_port, expected_type=type_hints["sender_control_port"])
            check_type(argname="argument sender_ip_address", value=sender_ip_address, expected_type=type_hints["sender_ip_address"])
            check_type(argname="argument source_listener_address", value=source_listener_address, expected_type=type_hints["source_listener_address"])
            check_type(argname="argument source_listener_port", value=source_listener_port, expected_type=type_hints["source_listener_port"])
            check_type(argname="argument stream_id", value=stream_id, expected_type=type_hints["stream_id"])
            check_type(argname="argument vpc_interface_name", value=vpc_interface_name, expected_type=type_hints["vpc_interface_name"])
            check_type(argname="argument whitelist_cidr", value=whitelist_cidr, expected_type=type_hints["whitelist_cidr"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if decryption is not None:
            self._values["decryption"] = decryption
        if description is not None:
            self._values["description"] = description
        if entitlement_arn is not None:
            self._values["entitlement_arn"] = entitlement_arn
        if flow_arn is not None:
            self._values["flow_arn"] = flow_arn
        if gateway_bridge_source is not None:
            self._values["gateway_bridge_source"] = gateway_bridge_source
        if ingest_port is not None:
            self._values["ingest_port"] = ingest_port
        if max_bitrate is not None:
            self._values["max_bitrate"] = max_bitrate
        if max_latency is not None:
            self._values["max_latency"] = max_latency
        if min_latency is not None:
            self._values["min_latency"] = min_latency
        if name is not None:
            self._values["name"] = name
        if protocol is not None:
            self._values["protocol"] = protocol
        if sender_control_port is not None:
            self._values["sender_control_port"] = sender_control_port
        if sender_ip_address is not None:
            self._values["sender_ip_address"] = sender_ip_address
        if source_listener_address is not None:
            self._values["source_listener_address"] = source_listener_address
        if source_listener_port is not None:
            self._values["source_listener_port"] = source_listener_port
        if stream_id is not None:
            self._values["stream_id"] = stream_id
        if vpc_interface_name is not None:
            self._values["vpc_interface_name"] = vpc_interface_name
        if whitelist_cidr is not None:
            self._values["whitelist_cidr"] = whitelist_cidr

    @builtins.property
    def decryption(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowSourcePropsMixin.EncryptionProperty"]]:
        '''The type of encryption that is used on the content ingested from this source.

        Allowable encryption types: static-key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-decryption
        '''
        result = self._values.get("decryption")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowSourcePropsMixin.EncryptionProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the source.

        This value is not used or seen outside of the current MediaConnect account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entitlement_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the entitlement that allows you to subscribe to this flow.

        The entitlement is set by the flow originator, and the ARN is generated as part of the originator's flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-entitlementarn
        '''
        result = self._values.get("entitlement_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flow_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the flow this source is connected to.

        The flow must have Failover enabled to add an additional source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-flowarn
        '''
        result = self._values.get("flow_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gateway_bridge_source(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowSourcePropsMixin.GatewayBridgeSourceProperty"]]:
        '''The bridge's source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-gatewaybridgesource
        '''
        result = self._values.get("gateway_bridge_source")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowSourcePropsMixin.GatewayBridgeSourceProperty"]], result)

    @builtins.property
    def ingest_port(self) -> typing.Optional[jsii.Number]:
        '''The port that the flow listens on for incoming content.

        If the protocol of the source is Zixi, the port must be set to 2088.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-ingestport
        '''
        result = self._values.get("ingest_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_bitrate(self) -> typing.Optional[jsii.Number]:
        '''The smoothing max bitrate (in bps) for RIST, RTP, and RTP-FEC streams.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-maxbitrate
        '''
        result = self._values.get("max_bitrate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_latency(self) -> typing.Optional[jsii.Number]:
        '''The maximum latency in milliseconds.

        This parameter applies only to RIST-based and Zixi-based streams.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-maxlatency
        '''
        result = self._values.get("max_latency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_latency(self) -> typing.Optional[jsii.Number]:
        '''The minimum latency in milliseconds for SRT-based streams.

        In streams that use the SRT protocol, this value that you set on your MediaConnect source or output represents the minimal potential latency of that connection. The latency of the stream is set to the highest number between the sender’s minimum latency and the receiver’s minimum latency.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-minlatency
        '''
        result = self._values.get("min_latency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''The protocol that the source uses to deliver the content to MediaConnect.

        Adding additional sources to an existing flow requires Failover to be enabled. When you enable Failover, the additional source must use the same protocol as the existing source. Only the following protocols support failover: Zixi-push, RTP-FEC, RTP, RIST and SRT protocols.

        If you use failover with SRT caller or listener, the ``FailoverMode`` property must be set to ``FAILOVER`` . The ``FailoverMode`` property is found in the ``FailoverConfig`` resource of the same flow ARN you used for the source's ``FlowArn`` property. SRT caller/listener does not support merge mode failover.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-protocol
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sender_control_port(self) -> typing.Optional[jsii.Number]:
        '''The port that the flow uses to send outbound requests to initiate connection with the sender.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-sendercontrolport
        '''
        result = self._values.get("sender_control_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sender_ip_address(self) -> typing.Optional[builtins.str]:
        '''The IP address that the flow communicates with to initiate connection with the sender.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-senderipaddress
        '''
        result = self._values.get("sender_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_listener_address(self) -> typing.Optional[builtins.str]:
        '''Source IP or domain name for SRT-caller protocol.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-sourcelisteneraddress
        '''
        result = self._values.get("source_listener_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_listener_port(self) -> typing.Optional[jsii.Number]:
        '''Source port for SRT-caller protocol.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-sourcelistenerport
        '''
        result = self._values.get("source_listener_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def stream_id(self) -> typing.Optional[builtins.str]:
        '''The stream ID that you want to use for this transport.

        This parameter applies only to Zixi and SRT caller-based streams.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-streamid
        '''
        result = self._values.get("stream_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_interface_name(self) -> typing.Optional[builtins.str]:
        '''The name of the VPC interface to use for this source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-vpcinterfacename
        '''
        result = self._values.get("vpc_interface_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def whitelist_cidr(self) -> typing.Optional[builtins.str]:
        '''The range of IP addresses that should be allowed to contribute content to your source.

        These IP addresses should be in the form of a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-whitelistcidr
        '''
        result = self._values.get("whitelist_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFlowSourceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFlowSourcePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowSourcePropsMixin",
):
    '''The ``AWS::MediaConnect::FlowSource`` resource is usedt to add additional sources to an existing flow.

    Adding an additional source requires Failover to be enabled. When you enable Failover, the additional source must use the same protocol as the existing source. A source is the external video content that includes configuration information (encryption and source type) and a network address. Each flow has at least one source. A standard source comes from a source other than another AWS Elemental MediaConnect flow, such as an on-premises encoder.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html
    :cloudformationResource: AWS::MediaConnect::FlowSource
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
        
        cfn_flow_source_props_mixin = mediaconnect_mixins.CfnFlowSourcePropsMixin(mediaconnect_mixins.CfnFlowSourceMixinProps(
            decryption=mediaconnect_mixins.CfnFlowSourcePropsMixin.EncryptionProperty(
                algorithm="algorithm",
                constant_initialization_vector="constantInitializationVector",
                device_id="deviceId",
                key_type="keyType",
                region="region",
                resource_id="resourceId",
                role_arn="roleArn",
                secret_arn="secretArn",
                url="url"
            ),
            description="description",
            entitlement_arn="entitlementArn",
            flow_arn="flowArn",
            gateway_bridge_source=mediaconnect_mixins.CfnFlowSourcePropsMixin.GatewayBridgeSourceProperty(
                bridge_arn="bridgeArn",
                vpc_interface_attachment=mediaconnect_mixins.CfnFlowSourcePropsMixin.VpcInterfaceAttachmentProperty(
                    vpc_interface_name="vpcInterfaceName"
                )
            ),
            ingest_port=123,
            max_bitrate=123,
            max_latency=123,
            min_latency=123,
            name="name",
            protocol="protocol",
            sender_control_port=123,
            sender_ip_address="senderIpAddress",
            source_listener_address="sourceListenerAddress",
            source_listener_port=123,
            stream_id="streamId",
            vpc_interface_name="vpcInterfaceName",
            whitelist_cidr="whitelistCidr"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnFlowSourceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaConnect::FlowSource``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f74844597ad4edf000d0b7bec905f15e58dbe23f867ce5a87df65ebc138a8237)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea07e4e12e7609afc57c1c437ad05e59351b883902074edca0d782caabf2b3a6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30bc093798e3b321491966e1293d81f39ff0a047ef721e996176fa0a421bbcbf)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFlowSourceMixinProps:
        return typing.cast(CfnFlowSourceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowSourcePropsMixin.EncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "algorithm": "algorithm",
            "constant_initialization_vector": "constantInitializationVector",
            "device_id": "deviceId",
            "key_type": "keyType",
            "region": "region",
            "resource_id": "resourceId",
            "role_arn": "roleArn",
            "secret_arn": "secretArn",
            "url": "url",
        },
    )
    class EncryptionProperty:
        def __init__(
            self,
            *,
            algorithm: typing.Optional[builtins.str] = None,
            constant_initialization_vector: typing.Optional[builtins.str] = None,
            device_id: typing.Optional[builtins.str] = None,
            key_type: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
            resource_id: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Encryption information.

            :param algorithm: The type of algorithm that is used for static key encryption (such as aes128, aes192, or aes256). If you are using SPEKE or SRT-password encryption, this property must be left blank.
            :param constant_initialization_vector: A 128-bit, 16-byte hex value represented by a 32-character string, to be used with the key for encrypting content. This parameter is not valid for static key encryption.
            :param device_id: The value of one of the devices that you configured with your digital rights management (DRM) platform key provider. This parameter is required for SPEKE encryption and is not valid for static key encryption.
            :param key_type: The type of key that is used for the encryption. If you don't specify a ``keyType`` value, the service uses the default setting ( ``static-key`` ). Valid key types are: ``static-key`` , ``speke`` , and ``srt-password`` . Default: - "static-key"
            :param region: The AWS Region that the API Gateway proxy endpoint was created in. This parameter is required for SPEKE encryption and is not valid for static key encryption.
            :param resource_id: An identifier for the content. The service sends this value to the key server to identify the current endpoint. The resource ID is also known as the content ID. This parameter is required for SPEKE encryption and is not valid for static key encryption.
            :param role_arn: The ARN of the role that you created during setup (when you set up MediaConnect as a trusted entity).
            :param secret_arn: The ARN of the secret that you created in AWS Secrets Manager to store the encryption key. This parameter is required for static key encryption and is not valid for SPEKE encryption.
            :param url: The URL from the API Gateway proxy that you set up to talk to your key server. This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-encryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                encryption_property = mediaconnect_mixins.CfnFlowSourcePropsMixin.EncryptionProperty(
                    algorithm="algorithm",
                    constant_initialization_vector="constantInitializationVector",
                    device_id="deviceId",
                    key_type="keyType",
                    region="region",
                    resource_id="resourceId",
                    role_arn="roleArn",
                    secret_arn="secretArn",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__26bede2fb08fa2aa992b2d7012185fdc0bf29bcf39d0d385e452ed8545d893a5)
                check_type(argname="argument algorithm", value=algorithm, expected_type=type_hints["algorithm"])
                check_type(argname="argument constant_initialization_vector", value=constant_initialization_vector, expected_type=type_hints["constant_initialization_vector"])
                check_type(argname="argument device_id", value=device_id, expected_type=type_hints["device_id"])
                check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
                check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if algorithm is not None:
                self._values["algorithm"] = algorithm
            if constant_initialization_vector is not None:
                self._values["constant_initialization_vector"] = constant_initialization_vector
            if device_id is not None:
                self._values["device_id"] = device_id
            if key_type is not None:
                self._values["key_type"] = key_type
            if region is not None:
                self._values["region"] = region
            if resource_id is not None:
                self._values["resource_id"] = resource_id
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def algorithm(self) -> typing.Optional[builtins.str]:
            '''The type of algorithm that is used for static key encryption (such as aes128, aes192, or aes256).

            If you are using SPEKE or SRT-password encryption, this property must be left blank.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-encryption.html#cfn-mediaconnect-flowsource-encryption-algorithm
            '''
            result = self._values.get("algorithm")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def constant_initialization_vector(self) -> typing.Optional[builtins.str]:
            '''A 128-bit, 16-byte hex value represented by a 32-character string, to be used with the key for encrypting content.

            This parameter is not valid for static key encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-encryption.html#cfn-mediaconnect-flowsource-encryption-constantinitializationvector
            '''
            result = self._values.get("constant_initialization_vector")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def device_id(self) -> typing.Optional[builtins.str]:
            '''The value of one of the devices that you configured with your digital rights management (DRM) platform key provider.

            This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-encryption.html#cfn-mediaconnect-flowsource-encryption-deviceid
            '''
            result = self._values.get("device_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_type(self) -> typing.Optional[builtins.str]:
            '''The type of key that is used for the encryption.

            If you don't specify a ``keyType`` value, the service uses the default setting ( ``static-key`` ). Valid key types are: ``static-key`` , ``speke`` , and ``srt-password`` .

            :default: - "static-key"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-encryption.html#cfn-mediaconnect-flowsource-encryption-keytype
            '''
            result = self._values.get("key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region that the API Gateway proxy endpoint was created in.

            This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-encryption.html#cfn-mediaconnect-flowsource-encryption-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_id(self) -> typing.Optional[builtins.str]:
            '''An identifier for the content.

            The service sends this value to the key server to identify the current endpoint. The resource ID is also known as the content ID. This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-encryption.html#cfn-mediaconnect-flowsource-encryption-resourceid
            '''
            result = self._values.get("resource_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the role that you created during setup (when you set up MediaConnect as a trusted entity).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-encryption.html#cfn-mediaconnect-flowsource-encryption-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the secret that you created in AWS Secrets Manager to store the encryption key.

            This parameter is required for static key encryption and is not valid for SPEKE encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-encryption.html#cfn-mediaconnect-flowsource-encryption-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL from the API Gateway proxy that you set up to talk to your key server.

            This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-encryption.html#cfn-mediaconnect-flowsource-encryption-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowSourcePropsMixin.GatewayBridgeSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bridge_arn": "bridgeArn",
            "vpc_interface_attachment": "vpcInterfaceAttachment",
        },
    )
    class GatewayBridgeSourceProperty:
        def __init__(
            self,
            *,
            bridge_arn: typing.Optional[builtins.str] = None,
            vpc_interface_attachment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFlowSourcePropsMixin.VpcInterfaceAttachmentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The source configuration for cloud flows receiving a stream from a bridge.

            :param bridge_arn: The ARN of the bridge feeding this flow.
            :param vpc_interface_attachment: The name of the VPC interface attachment to use for this bridge source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-gatewaybridgesource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                gateway_bridge_source_property = mediaconnect_mixins.CfnFlowSourcePropsMixin.GatewayBridgeSourceProperty(
                    bridge_arn="bridgeArn",
                    vpc_interface_attachment=mediaconnect_mixins.CfnFlowSourcePropsMixin.VpcInterfaceAttachmentProperty(
                        vpc_interface_name="vpcInterfaceName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ac25043c3739c104457fd0cae1ea1cb78f7bb412ce3a0b935943b01f7689f267)
                check_type(argname="argument bridge_arn", value=bridge_arn, expected_type=type_hints["bridge_arn"])
                check_type(argname="argument vpc_interface_attachment", value=vpc_interface_attachment, expected_type=type_hints["vpc_interface_attachment"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bridge_arn is not None:
                self._values["bridge_arn"] = bridge_arn
            if vpc_interface_attachment is not None:
                self._values["vpc_interface_attachment"] = vpc_interface_attachment

        @builtins.property
        def bridge_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the bridge feeding this flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-gatewaybridgesource.html#cfn-mediaconnect-flowsource-gatewaybridgesource-bridgearn
            '''
            result = self._values.get("bridge_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_interface_attachment(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowSourcePropsMixin.VpcInterfaceAttachmentProperty"]]:
            '''The name of the VPC interface attachment to use for this bridge source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-gatewaybridgesource.html#cfn-mediaconnect-flowsource-gatewaybridgesource-vpcinterfaceattachment
            '''
            result = self._values.get("vpc_interface_attachment")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFlowSourcePropsMixin.VpcInterfaceAttachmentProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GatewayBridgeSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowSourcePropsMixin.VpcInterfaceAttachmentProperty",
        jsii_struct_bases=[],
        name_mapping={"vpc_interface_name": "vpcInterfaceName"},
    )
    class VpcInterfaceAttachmentProperty:
        def __init__(
            self,
            *,
            vpc_interface_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The settings for attaching a VPC interface to an resource.

            :param vpc_interface_name: The name of the VPC interface to use for this resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-vpcinterfaceattachment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                vpc_interface_attachment_property = mediaconnect_mixins.CfnFlowSourcePropsMixin.VpcInterfaceAttachmentProperty(
                    vpc_interface_name="vpcInterfaceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__87e1d13c319ac98b4579769ca072408a05c20af6df9d3ea92230a73e74cc5798)
                check_type(argname="argument vpc_interface_name", value=vpc_interface_name, expected_type=type_hints["vpc_interface_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if vpc_interface_name is not None:
                self._values["vpc_interface_name"] = vpc_interface_name

        @builtins.property
        def vpc_interface_name(self) -> typing.Optional[builtins.str]:
            '''The name of the VPC interface to use for this resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-vpcinterfaceattachment.html#cfn-mediaconnect-flowsource-vpcinterfaceattachment-vpcinterfacename
            '''
            result = self._values.get("vpc_interface_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcInterfaceAttachmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowVpcInterfaceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "flow_arn": "flowArn",
        "name": "name",
        "role_arn": "roleArn",
        "security_group_ids": "securityGroupIds",
        "subnet_id": "subnetId",
    },
)
class CfnFlowVpcInterfaceMixinProps:
    def __init__(
        self,
        *,
        flow_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnFlowVpcInterfacePropsMixin.

        :param flow_arn: The Amazon Resource Name (ARN) of the flow.
        :param name: The name for the VPC interface. This name must be unique within the flow.
        :param role_arn: The Amazon Resource Name (ARN) of the role that you created when you set up MediaConnect as a trusted service.
        :param security_group_ids: A virtual firewall to control inbound and outbound traffic.
        :param subnet_id: The subnet IDs that you want to use for your VPC interface. A range of IP addresses in your VPC. When you create your VPC, you specify a range of IPv4 addresses for the VPC in the form of a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16. This is the primary CIDR block for your VPC. When you create a subnet for your VPC, you specify the CIDR block for the subnet, which is a subset of the VPC CIDR block. The subnets that you use across all VPC interfaces on the flow must be in the same Availability Zone as the flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowvpcinterface.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
            
            cfn_flow_vpc_interface_mixin_props = mediaconnect_mixins.CfnFlowVpcInterfaceMixinProps(
                flow_arn="flowArn",
                name="name",
                role_arn="roleArn",
                security_group_ids=["securityGroupIds"],
                subnet_id="subnetId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55219b28d1249a53618ab4a108410c2cc2263f30cc1ae25188d45fb387345ed3)
            check_type(argname="argument flow_arn", value=flow_arn, expected_type=type_hints["flow_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if flow_arn is not None:
            self._values["flow_arn"] = flow_arn
        if name is not None:
            self._values["name"] = name
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id

    @builtins.property
    def flow_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowvpcinterface.html#cfn-mediaconnect-flowvpcinterface-flowarn
        '''
        result = self._values.get("flow_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name for the VPC interface.

        This name must be unique within the flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowvpcinterface.html#cfn-mediaconnect-flowvpcinterface-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the role that you created when you set up MediaConnect as a trusted service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowvpcinterface.html#cfn-mediaconnect-flowvpcinterface-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A virtual firewall to control inbound and outbound traffic.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowvpcinterface.html#cfn-mediaconnect-flowvpcinterface-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''The subnet IDs that you want to use for your VPC interface.

        A range of IP addresses in your VPC. When you create your VPC, you specify a range of IPv4 addresses for the VPC in the form of a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16. This is the primary CIDR block for your VPC. When you create a subnet for your VPC, you specify the CIDR block for the subnet, which is a subset of the VPC CIDR block. The subnets that you use across all VPC interfaces on the flow must be in the same Availability Zone as the flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowvpcinterface.html#cfn-mediaconnect-flowvpcinterface-subnetid
        '''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFlowVpcInterfaceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFlowVpcInterfacePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnFlowVpcInterfacePropsMixin",
):
    '''The ``AWS::MediaConnect::FlowVpcInterface`` resource is a connection between your AWS Elemental MediaConnect flow and a virtual private cloud (VPC) that you created using the Amazon Virtual Private Cloud service.

    To avoid streaming your content over the public internet, you can add up to two VPC interfaces to your flow and use those connections to transfer content between your VPC and MediaConnect.

    You can update an existing flow to add a VPC interface. If you haven’t created the flow yet, you must create the flow with a temporary standard source by doing the following:

    - Use CloudFormation to create a flow with a standard source that uses to the flow’s public IP address.
    - Use CloudFormation to create a VPC interface to add to this flow. This can also be done as part of the previous step.
    - After CloudFormation has created the flow and the VPC interface, update the source to point to the VPC interface that you created.

    .. epigraph::

       The previous steps must be undone before the CloudFormation stack can be deleted. Because the source is manually updated in step 3, CloudFormation is not aware of this change. The source must be returned to a standard source before CloudFormation stack deletion. > When configuring NDI outputs for your flow, define the VPC interface as a nested attribute within the ``AWS::MediaConnect::Flow`` resource. Do not use the top-level ``AWS::MediaConnect::FlowVpcInterface`` resource type to specify NDI configurations.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowvpcinterface.html
    :cloudformationResource: AWS::MediaConnect::FlowVpcInterface
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
        
        cfn_flow_vpc_interface_props_mixin = mediaconnect_mixins.CfnFlowVpcInterfacePropsMixin(mediaconnect_mixins.CfnFlowVpcInterfaceMixinProps(
            flow_arn="flowArn",
            name="name",
            role_arn="roleArn",
            security_group_ids=["securityGroupIds"],
            subnet_id="subnetId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnFlowVpcInterfaceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaConnect::FlowVpcInterface``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__409b37f755f20b161a12696d48d5f1578421dc816748fc7cb10300142ce7f6fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1043ec989226d493f90d907c63270433a05807d7ac7d4acb25ffdedd068f0419)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a2c3915c9a4b44d1144db584f1364c54d3fe1cdc51a848ed0c778989ae9d33b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFlowVpcInterfaceMixinProps:
        return typing.cast(CfnFlowVpcInterfaceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnGatewayMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "egress_cidr_blocks": "egressCidrBlocks",
        "name": "name",
        "networks": "networks",
    },
)
class CfnGatewayMixinProps:
    def __init__(
        self,
        *,
        egress_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        networks: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayPropsMixin.GatewayNetworkProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnGatewayPropsMixin.

        :param egress_cidr_blocks: The range of IP addresses that are allowed to contribute content or initiate output requests for flows communicating with this gateway. These IP addresses should be in the form of a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16.
        :param name: The name of the gateway. This name can not be modified after the gateway is created.
        :param networks: The list of networks in the gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-gateway.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
            
            cfn_gateway_mixin_props = mediaconnect_mixins.CfnGatewayMixinProps(
                egress_cidr_blocks=["egressCidrBlocks"],
                name="name",
                networks=[mediaconnect_mixins.CfnGatewayPropsMixin.GatewayNetworkProperty(
                    cidr_block="cidrBlock",
                    name="name"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb91dd33949073677337265b5ab70f66a9d29c7075ee6af603ef327ef004f981)
            check_type(argname="argument egress_cidr_blocks", value=egress_cidr_blocks, expected_type=type_hints["egress_cidr_blocks"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument networks", value=networks, expected_type=type_hints["networks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if egress_cidr_blocks is not None:
            self._values["egress_cidr_blocks"] = egress_cidr_blocks
        if name is not None:
            self._values["name"] = name
        if networks is not None:
            self._values["networks"] = networks

    @builtins.property
    def egress_cidr_blocks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The range of IP addresses that are allowed to contribute content or initiate output requests for flows communicating with this gateway.

        These IP addresses should be in the form of a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-gateway.html#cfn-mediaconnect-gateway-egresscidrblocks
        '''
        result = self._values.get("egress_cidr_blocks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the gateway.

        This name can not be modified after the gateway is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-gateway.html#cfn-mediaconnect-gateway-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def networks(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayPropsMixin.GatewayNetworkProperty"]]]]:
        '''The list of networks in the gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-gateway.html#cfn-mediaconnect-gateway-networks
        '''
        result = self._values.get("networks")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayPropsMixin.GatewayNetworkProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGatewayMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGatewayPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnGatewayPropsMixin",
):
    '''The ``AWS::MediaConnect::Gateway`` resource is used to create a new gateway.

    AWS Elemental MediaConnect Gateway is a feature of MediaConnect that allows the deployment of on-premises resources for transporting live video to and from the AWS Cloud. MediaConnect Gateway allows you to contribute live video to the AWS Cloud from on-premises hardware, as well as distribute live video from the AWS Cloud to your local data center.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-gateway.html
    :cloudformationResource: AWS::MediaConnect::Gateway
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
        
        cfn_gateway_props_mixin = mediaconnect_mixins.CfnGatewayPropsMixin(mediaconnect_mixins.CfnGatewayMixinProps(
            egress_cidr_blocks=["egressCidrBlocks"],
            name="name",
            networks=[mediaconnect_mixins.CfnGatewayPropsMixin.GatewayNetworkProperty(
                cidr_block="cidrBlock",
                name="name"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnGatewayMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaConnect::Gateway``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f029659f640b0b3e554d5df973ba85fc19c9491f265e17c0cc34455e0610a0cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44089f482f0c0aa70664aa603f388a5f52e0554656bd3995ed40eea7c1244a87)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9c9deadee031e2ecee98a95160b14e04de6a047144caa75a36d5831af86ddd8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGatewayMixinProps:
        return typing.cast(CfnGatewayMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnGatewayPropsMixin.GatewayNetworkProperty",
        jsii_struct_bases=[],
        name_mapping={"cidr_block": "cidrBlock", "name": "name"},
    )
    class GatewayNetworkProperty:
        def __init__(
            self,
            *,
            cidr_block: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The network settings for a gateway.

            :param cidr_block: A unique IP address range to use for this network. These IP addresses should be in the form of a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16.
            :param name: The name of the network. This name is used to reference the network and must be unique among networks in this gateway.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-gateway-gatewaynetwork.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                gateway_network_property = mediaconnect_mixins.CfnGatewayPropsMixin.GatewayNetworkProperty(
                    cidr_block="cidrBlock",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__185391e71d9bbd95ffcf303ffad341e61253026a6572c36ede11a2574c6d3e2d)
                check_type(argname="argument cidr_block", value=cidr_block, expected_type=type_hints["cidr_block"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cidr_block is not None:
                self._values["cidr_block"] = cidr_block
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def cidr_block(self) -> typing.Optional[builtins.str]:
            '''A unique IP address range to use for this network.

            These IP addresses should be in the form of a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-gateway-gatewaynetwork.html#cfn-mediaconnect-gateway-gatewaynetwork-cidrblock
            '''
            result = self._values.get("cidr_block")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the network.

            This name is used to reference the network and must be unique among networks in this gateway.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-gateway-gatewaynetwork.html#cfn-mediaconnect-gateway-gatewaynetwork-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GatewayNetworkProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterInputMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zone": "availabilityZone",
        "configuration": "configuration",
        "maintenance_configuration": "maintenanceConfiguration",
        "maximum_bitrate": "maximumBitrate",
        "name": "name",
        "region_name": "regionName",
        "routing_scope": "routingScope",
        "tags": "tags",
        "tier": "tier",
        "transit_encryption": "transitEncryption",
    },
)
class CfnRouterInputMixinProps:
    def __init__(
        self,
        *,
        availability_zone: typing.Optional[builtins.str] = None,
        configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.RouterInputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        maintenance_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.MaintenanceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        maximum_bitrate: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        region_name: typing.Optional[builtins.str] = None,
        routing_scope: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        tier: typing.Optional[builtins.str] = None,
        transit_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.RouterInputTransitEncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnRouterInputPropsMixin.

        :param availability_zone: The Availability Zone of the router input.
        :param configuration: The configuration settings for a router input.
        :param maintenance_configuration: The maintenance configuration settings applied to this router input.
        :param maximum_bitrate: The maximum bitrate for the router input.
        :param name: The name of the router input.
        :param region_name: The AWS Region where the router input is located.
        :param routing_scope: Indicates whether the router input is configured for Regional or global routing.
        :param tags: Key-value pairs that can be used to tag and organize this router input.
        :param tier: The tier level of the router input.
        :param transit_encryption: Encryption information.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routerinput.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
            
            # automatic: Any
            # default_: Any
            
            cfn_router_input_mixin_props = mediaconnect_mixins.CfnRouterInputMixinProps(
                availability_zone="availabilityZone",
                configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.RouterInputConfigurationProperty(
                    failover=mediaconnect_mixins.CfnRouterInputPropsMixin.FailoverRouterInputConfigurationProperty(
                        network_interface_arn="networkInterfaceArn",
                        primary_source_index=123,
                        protocol_configurations=[mediaconnect_mixins.CfnRouterInputPropsMixin.FailoverRouterInputProtocolConfigurationProperty(
                            rist=mediaconnect_mixins.CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty(
                                port=123,
                                recovery_latency_milliseconds=123
                            ),
                            rtp=mediaconnect_mixins.CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty(
                                forward_error_correction="forwardErrorCorrection",
                                port=123
                            ),
                            srt_caller=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtCallerRouterInputConfigurationProperty(
                                decryption_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty(
                                    encryption_key=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                        role_arn="roleArn",
                                        secret_arn="secretArn"
                                    )
                                ),
                                minimum_latency_milliseconds=123,
                                source_address="sourceAddress",
                                source_port=123,
                                stream_id="streamId"
                            ),
                            srt_listener=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtListenerRouterInputConfigurationProperty(
                                decryption_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty(
                                    encryption_key=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                        role_arn="roleArn",
                                        secret_arn="secretArn"
                                    )
                                ),
                                minimum_latency_milliseconds=123,
                                port=123
                            )
                        )],
                        source_priority_mode="sourcePriorityMode"
                    ),
                    media_connect_flow=mediaconnect_mixins.CfnRouterInputPropsMixin.MediaConnectFlowRouterInputConfigurationProperty(
                        flow_arn="flowArn",
                        flow_output_arn="flowOutputArn",
                        source_transit_decryption=mediaconnect_mixins.CfnRouterInputPropsMixin.FlowTransitEncryptionProperty(
                            encryption_key_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty(
                                automatic=automatic,
                                secrets_manager=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                    role_arn="roleArn",
                                    secret_arn="secretArn"
                                )
                            ),
                            encryption_key_type="encryptionKeyType"
                        )
                    ),
                    merge=mediaconnect_mixins.CfnRouterInputPropsMixin.MergeRouterInputConfigurationProperty(
                        merge_recovery_window_milliseconds=123,
                        network_interface_arn="networkInterfaceArn",
                        protocol_configurations=[mediaconnect_mixins.CfnRouterInputPropsMixin.MergeRouterInputProtocolConfigurationProperty(
                            rist=mediaconnect_mixins.CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty(
                                port=123,
                                recovery_latency_milliseconds=123
                            ),
                            rtp=mediaconnect_mixins.CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty(
                                forward_error_correction="forwardErrorCorrection",
                                port=123
                            )
                        )]
                    ),
                    standard=mediaconnect_mixins.CfnRouterInputPropsMixin.StandardRouterInputConfigurationProperty(
                        network_interface_arn="networkInterfaceArn",
                        protocol="protocol",
                        protocol_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.RouterInputProtocolConfigurationProperty(
                            rist=mediaconnect_mixins.CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty(
                                port=123,
                                recovery_latency_milliseconds=123
                            ),
                            rtp=mediaconnect_mixins.CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty(
                                forward_error_correction="forwardErrorCorrection",
                                port=123
                            ),
                            srt_caller=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtCallerRouterInputConfigurationProperty(
                                decryption_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty(
                                    encryption_key=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                        role_arn="roleArn",
                                        secret_arn="secretArn"
                                    )
                                ),
                                minimum_latency_milliseconds=123,
                                source_address="sourceAddress",
                                source_port=123,
                                stream_id="streamId"
                            ),
                            srt_listener=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtListenerRouterInputConfigurationProperty(
                                decryption_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty(
                                    encryption_key=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                        role_arn="roleArn",
                                        secret_arn="secretArn"
                                    )
                                ),
                                minimum_latency_milliseconds=123,
                                port=123
                            )
                        )
                    )
                ),
                maintenance_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.MaintenanceConfigurationProperty(
                    default=default_,
                    preferred_day_time=mediaconnect_mixins.CfnRouterInputPropsMixin.PreferredDayTimeMaintenanceConfigurationProperty(
                        day="day",
                        time="time"
                    )
                ),
                maximum_bitrate=123,
                name="name",
                region_name="regionName",
                routing_scope="routingScope",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                tier="tier",
                transit_encryption=mediaconnect_mixins.CfnRouterInputPropsMixin.RouterInputTransitEncryptionProperty(
                    encryption_key_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.RouterInputTransitEncryptionKeyConfigurationProperty(
                        automatic=automatic,
                        secrets_manager=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                            role_arn="roleArn",
                            secret_arn="secretArn"
                        )
                    ),
                    encryption_key_type="encryptionKeyType"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78503390c836ec6df1491f415cb23595768e315fe7a68372d75299f66f512096)
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument maintenance_configuration", value=maintenance_configuration, expected_type=type_hints["maintenance_configuration"])
            check_type(argname="argument maximum_bitrate", value=maximum_bitrate, expected_type=type_hints["maximum_bitrate"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region_name", value=region_name, expected_type=type_hints["region_name"])
            check_type(argname="argument routing_scope", value=routing_scope, expected_type=type_hints["routing_scope"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument transit_encryption", value=transit_encryption, expected_type=type_hints["transit_encryption"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if configuration is not None:
            self._values["configuration"] = configuration
        if maintenance_configuration is not None:
            self._values["maintenance_configuration"] = maintenance_configuration
        if maximum_bitrate is not None:
            self._values["maximum_bitrate"] = maximum_bitrate
        if name is not None:
            self._values["name"] = name
        if region_name is not None:
            self._values["region_name"] = region_name
        if routing_scope is not None:
            self._values["routing_scope"] = routing_scope
        if tags is not None:
            self._values["tags"] = tags
        if tier is not None:
            self._values["tier"] = tier
        if transit_encryption is not None:
            self._values["transit_encryption"] = transit_encryption

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''The Availability Zone of the router input.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routerinput.html#cfn-mediaconnect-routerinput-availabilityzone
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.RouterInputConfigurationProperty"]]:
        '''The configuration settings for a router input.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routerinput.html#cfn-mediaconnect-routerinput-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.RouterInputConfigurationProperty"]], result)

    @builtins.property
    def maintenance_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.MaintenanceConfigurationProperty"]]:
        '''The maintenance configuration settings applied to this router input.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routerinput.html#cfn-mediaconnect-routerinput-maintenanceconfiguration
        '''
        result = self._values.get("maintenance_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.MaintenanceConfigurationProperty"]], result)

    @builtins.property
    def maximum_bitrate(self) -> typing.Optional[jsii.Number]:
        '''The maximum bitrate for the router input.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routerinput.html#cfn-mediaconnect-routerinput-maximumbitrate
        '''
        result = self._values.get("maximum_bitrate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the router input.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routerinput.html#cfn-mediaconnect-routerinput-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region_name(self) -> typing.Optional[builtins.str]:
        '''The AWS Region where the router input is located.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routerinput.html#cfn-mediaconnect-routerinput-regionname
        '''
        result = self._values.get("region_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_scope(self) -> typing.Optional[builtins.str]:
        '''Indicates whether the router input is configured for Regional or global routing.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routerinput.html#cfn-mediaconnect-routerinput-routingscope
        '''
        result = self._values.get("routing_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Key-value pairs that can be used to tag and organize this router input.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routerinput.html#cfn-mediaconnect-routerinput-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def tier(self) -> typing.Optional[builtins.str]:
        '''The tier level of the router input.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routerinput.html#cfn-mediaconnect-routerinput-tier
        '''
        result = self._values.get("tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transit_encryption(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.RouterInputTransitEncryptionProperty"]]:
        '''Encryption information.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routerinput.html#cfn-mediaconnect-routerinput-transitencryption
        '''
        result = self._values.get("transit_encryption")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.RouterInputTransitEncryptionProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRouterInputMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRouterInputPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterInputPropsMixin",
):
    '''Represents a router input in AWS Elemental MediaConnect that is used to ingest content to be transmitted to router outputs.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routerinput.html
    :cloudformationResource: AWS::MediaConnect::RouterInput
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
        
        # automatic: Any
        # default_: Any
        
        cfn_router_input_props_mixin = mediaconnect_mixins.CfnRouterInputPropsMixin(mediaconnect_mixins.CfnRouterInputMixinProps(
            availability_zone="availabilityZone",
            configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.RouterInputConfigurationProperty(
                failover=mediaconnect_mixins.CfnRouterInputPropsMixin.FailoverRouterInputConfigurationProperty(
                    network_interface_arn="networkInterfaceArn",
                    primary_source_index=123,
                    protocol_configurations=[mediaconnect_mixins.CfnRouterInputPropsMixin.FailoverRouterInputProtocolConfigurationProperty(
                        rist=mediaconnect_mixins.CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty(
                            port=123,
                            recovery_latency_milliseconds=123
                        ),
                        rtp=mediaconnect_mixins.CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty(
                            forward_error_correction="forwardErrorCorrection",
                            port=123
                        ),
                        srt_caller=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtCallerRouterInputConfigurationProperty(
                            decryption_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty(
                                encryption_key=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                    role_arn="roleArn",
                                    secret_arn="secretArn"
                                )
                            ),
                            minimum_latency_milliseconds=123,
                            source_address="sourceAddress",
                            source_port=123,
                            stream_id="streamId"
                        ),
                        srt_listener=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtListenerRouterInputConfigurationProperty(
                            decryption_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty(
                                encryption_key=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                    role_arn="roleArn",
                                    secret_arn="secretArn"
                                )
                            ),
                            minimum_latency_milliseconds=123,
                            port=123
                        )
                    )],
                    source_priority_mode="sourcePriorityMode"
                ),
                media_connect_flow=mediaconnect_mixins.CfnRouterInputPropsMixin.MediaConnectFlowRouterInputConfigurationProperty(
                    flow_arn="flowArn",
                    flow_output_arn="flowOutputArn",
                    source_transit_decryption=mediaconnect_mixins.CfnRouterInputPropsMixin.FlowTransitEncryptionProperty(
                        encryption_key_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty(
                            automatic=automatic,
                            secrets_manager=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                role_arn="roleArn",
                                secret_arn="secretArn"
                            )
                        ),
                        encryption_key_type="encryptionKeyType"
                    )
                ),
                merge=mediaconnect_mixins.CfnRouterInputPropsMixin.MergeRouterInputConfigurationProperty(
                    merge_recovery_window_milliseconds=123,
                    network_interface_arn="networkInterfaceArn",
                    protocol_configurations=[mediaconnect_mixins.CfnRouterInputPropsMixin.MergeRouterInputProtocolConfigurationProperty(
                        rist=mediaconnect_mixins.CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty(
                            port=123,
                            recovery_latency_milliseconds=123
                        ),
                        rtp=mediaconnect_mixins.CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty(
                            forward_error_correction="forwardErrorCorrection",
                            port=123
                        )
                    )]
                ),
                standard=mediaconnect_mixins.CfnRouterInputPropsMixin.StandardRouterInputConfigurationProperty(
                    network_interface_arn="networkInterfaceArn",
                    protocol="protocol",
                    protocol_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.RouterInputProtocolConfigurationProperty(
                        rist=mediaconnect_mixins.CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty(
                            port=123,
                            recovery_latency_milliseconds=123
                        ),
                        rtp=mediaconnect_mixins.CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty(
                            forward_error_correction="forwardErrorCorrection",
                            port=123
                        ),
                        srt_caller=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtCallerRouterInputConfigurationProperty(
                            decryption_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty(
                                encryption_key=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                    role_arn="roleArn",
                                    secret_arn="secretArn"
                                )
                            ),
                            minimum_latency_milliseconds=123,
                            source_address="sourceAddress",
                            source_port=123,
                            stream_id="streamId"
                        ),
                        srt_listener=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtListenerRouterInputConfigurationProperty(
                            decryption_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty(
                                encryption_key=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                    role_arn="roleArn",
                                    secret_arn="secretArn"
                                )
                            ),
                            minimum_latency_milliseconds=123,
                            port=123
                        )
                    )
                )
            ),
            maintenance_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.MaintenanceConfigurationProperty(
                default=default_,
                preferred_day_time=mediaconnect_mixins.CfnRouterInputPropsMixin.PreferredDayTimeMaintenanceConfigurationProperty(
                    day="day",
                    time="time"
                )
            ),
            maximum_bitrate=123,
            name="name",
            region_name="regionName",
            routing_scope="routingScope",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            tier="tier",
            transit_encryption=mediaconnect_mixins.CfnRouterInputPropsMixin.RouterInputTransitEncryptionProperty(
                encryption_key_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.RouterInputTransitEncryptionKeyConfigurationProperty(
                    automatic=automatic,
                    secrets_manager=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                        role_arn="roleArn",
                        secret_arn="secretArn"
                    )
                ),
                encryption_key_type="encryptionKeyType"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRouterInputMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaConnect::RouterInput``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1566708a8326710e9c79c26bfdb4ba1d5c7cb009862f2f0728b02e1bb9fd626f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3caf6656a870ca9630aeb982fe6bd96133d21ef0addfc8570c75ff1d2e7045b0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2656e8aae91aa29a119b1180ecea7f4275a3d0c6de88d7b136f5bbe7095a5969)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRouterInputMixinProps:
        return typing.cast(CfnRouterInputMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterInputPropsMixin.FailoverRouterInputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "network_interface_arn": "networkInterfaceArn",
            "primary_source_index": "primarySourceIndex",
            "protocol_configurations": "protocolConfigurations",
            "source_priority_mode": "sourcePriorityMode",
        },
    )
    class FailoverRouterInputConfigurationProperty:
        def __init__(
            self,
            *,
            network_interface_arn: typing.Optional[builtins.str] = None,
            primary_source_index: typing.Optional[jsii.Number] = None,
            protocol_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.FailoverRouterInputProtocolConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            source_priority_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration settings for a failover router input that allows switching between two input sources.

            :param network_interface_arn: The ARN of the network interface to use for this failover router input.
            :param primary_source_index: The index (0 or 1) that specifies which source in the protocol configurations list is currently active. Used to control which of the two failover sources is currently selected. This field is ignored when sourcePriorityMode is set to NO_PRIORITY
            :param protocol_configurations: A list of exactly two protocol configurations for the failover input sources. Both must use the same protocol type.
            :param source_priority_mode: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-failoverrouterinputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                failover_router_input_configuration_property = mediaconnect_mixins.CfnRouterInputPropsMixin.FailoverRouterInputConfigurationProperty(
                    network_interface_arn="networkInterfaceArn",
                    primary_source_index=123,
                    protocol_configurations=[mediaconnect_mixins.CfnRouterInputPropsMixin.FailoverRouterInputProtocolConfigurationProperty(
                        rist=mediaconnect_mixins.CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty(
                            port=123,
                            recovery_latency_milliseconds=123
                        ),
                        rtp=mediaconnect_mixins.CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty(
                            forward_error_correction="forwardErrorCorrection",
                            port=123
                        ),
                        srt_caller=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtCallerRouterInputConfigurationProperty(
                            decryption_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty(
                                encryption_key=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                    role_arn="roleArn",
                                    secret_arn="secretArn"
                                )
                            ),
                            minimum_latency_milliseconds=123,
                            source_address="sourceAddress",
                            source_port=123,
                            stream_id="streamId"
                        ),
                        srt_listener=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtListenerRouterInputConfigurationProperty(
                            decryption_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty(
                                encryption_key=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                    role_arn="roleArn",
                                    secret_arn="secretArn"
                                )
                            ),
                            minimum_latency_milliseconds=123,
                            port=123
                        )
                    )],
                    source_priority_mode="sourcePriorityMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e17acc119fe7a1c5e4539a54c21b687f0ff075f212b3ad89172d142bda8af344)
                check_type(argname="argument network_interface_arn", value=network_interface_arn, expected_type=type_hints["network_interface_arn"])
                check_type(argname="argument primary_source_index", value=primary_source_index, expected_type=type_hints["primary_source_index"])
                check_type(argname="argument protocol_configurations", value=protocol_configurations, expected_type=type_hints["protocol_configurations"])
                check_type(argname="argument source_priority_mode", value=source_priority_mode, expected_type=type_hints["source_priority_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if network_interface_arn is not None:
                self._values["network_interface_arn"] = network_interface_arn
            if primary_source_index is not None:
                self._values["primary_source_index"] = primary_source_index
            if protocol_configurations is not None:
                self._values["protocol_configurations"] = protocol_configurations
            if source_priority_mode is not None:
                self._values["source_priority_mode"] = source_priority_mode

        @builtins.property
        def network_interface_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the network interface to use for this failover router input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-failoverrouterinputconfiguration.html#cfn-mediaconnect-routerinput-failoverrouterinputconfiguration-networkinterfacearn
            '''
            result = self._values.get("network_interface_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def primary_source_index(self) -> typing.Optional[jsii.Number]:
            '''The index (0 or 1) that specifies which source in the protocol configurations list is currently active.

            Used to control which of the two failover sources is currently selected. This field is ignored when sourcePriorityMode is set to NO_PRIORITY

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-failoverrouterinputconfiguration.html#cfn-mediaconnect-routerinput-failoverrouterinputconfiguration-primarysourceindex
            '''
            result = self._values.get("primary_source_index")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def protocol_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.FailoverRouterInputProtocolConfigurationProperty"]]]]:
            '''A list of exactly two protocol configurations for the failover input sources.

            Both must use the same protocol type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-failoverrouterinputconfiguration.html#cfn-mediaconnect-routerinput-failoverrouterinputconfiguration-protocolconfigurations
            '''
            result = self._values.get("protocol_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.FailoverRouterInputProtocolConfigurationProperty"]]]], result)

        @builtins.property
        def source_priority_mode(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-failoverrouterinputconfiguration.html#cfn-mediaconnect-routerinput-failoverrouterinputconfiguration-sourceprioritymode
            '''
            result = self._values.get("source_priority_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FailoverRouterInputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterInputPropsMixin.FailoverRouterInputProtocolConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "rist": "rist",
            "rtp": "rtp",
            "srt_caller": "srtCaller",
            "srt_listener": "srtListener",
        },
    )
    class FailoverRouterInputProtocolConfigurationProperty:
        def __init__(
            self,
            *,
            rist: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rtp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            srt_caller: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.SrtCallerRouterInputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            srt_listener: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.SrtListenerRouterInputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param rist: The configuration settings for a router input using the RIST (Reliable Internet Stream Transport) protocol, including the port and recovery latency.
            :param rtp: The configuration settings for a Router Input using the RTP (Real-Time Transport Protocol) protocol, including the port and forward error correction state.
            :param srt_caller: The configuration settings for a router input using the SRT (Secure Reliable Transport) protocol in caller mode, including the source address and port, minimum latency, stream ID, and decryption key configuration.
            :param srt_listener: The configuration settings for a router input using the SRT (Secure Reliable Transport) protocol in listener mode, including the port, minimum latency, and decryption key configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-failoverrouterinputprotocolconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                failover_router_input_protocol_configuration_property = mediaconnect_mixins.CfnRouterInputPropsMixin.FailoverRouterInputProtocolConfigurationProperty(
                    rist=mediaconnect_mixins.CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty(
                        port=123,
                        recovery_latency_milliseconds=123
                    ),
                    rtp=mediaconnect_mixins.CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty(
                        forward_error_correction="forwardErrorCorrection",
                        port=123
                    ),
                    srt_caller=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtCallerRouterInputConfigurationProperty(
                        decryption_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty(
                            encryption_key=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                role_arn="roleArn",
                                secret_arn="secretArn"
                            )
                        ),
                        minimum_latency_milliseconds=123,
                        source_address="sourceAddress",
                        source_port=123,
                        stream_id="streamId"
                    ),
                    srt_listener=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtListenerRouterInputConfigurationProperty(
                        decryption_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty(
                            encryption_key=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                role_arn="roleArn",
                                secret_arn="secretArn"
                            )
                        ),
                        minimum_latency_milliseconds=123,
                        port=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__31aaddad9486270d4f23ae001d908ffcce64eb375e254217472daa2f3a449fe5)
                check_type(argname="argument rist", value=rist, expected_type=type_hints["rist"])
                check_type(argname="argument rtp", value=rtp, expected_type=type_hints["rtp"])
                check_type(argname="argument srt_caller", value=srt_caller, expected_type=type_hints["srt_caller"])
                check_type(argname="argument srt_listener", value=srt_listener, expected_type=type_hints["srt_listener"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rist is not None:
                self._values["rist"] = rist
            if rtp is not None:
                self._values["rtp"] = rtp
            if srt_caller is not None:
                self._values["srt_caller"] = srt_caller
            if srt_listener is not None:
                self._values["srt_listener"] = srt_listener

        @builtins.property
        def rist(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty"]]:
            '''The configuration settings for a router input using the RIST (Reliable Internet Stream Transport) protocol, including the port and recovery latency.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-failoverrouterinputprotocolconfiguration.html#cfn-mediaconnect-routerinput-failoverrouterinputprotocolconfiguration-rist
            '''
            result = self._values.get("rist")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty"]], result)

        @builtins.property
        def rtp(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty"]]:
            '''The configuration settings for a Router Input using the RTP (Real-Time Transport Protocol) protocol, including the port and forward error correction state.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-failoverrouterinputprotocolconfiguration.html#cfn-mediaconnect-routerinput-failoverrouterinputprotocolconfiguration-rtp
            '''
            result = self._values.get("rtp")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty"]], result)

        @builtins.property
        def srt_caller(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.SrtCallerRouterInputConfigurationProperty"]]:
            '''The configuration settings for a router input using the SRT (Secure Reliable Transport) protocol in caller mode, including the source address and port, minimum latency, stream ID, and decryption key configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-failoverrouterinputprotocolconfiguration.html#cfn-mediaconnect-routerinput-failoverrouterinputprotocolconfiguration-srtcaller
            '''
            result = self._values.get("srt_caller")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.SrtCallerRouterInputConfigurationProperty"]], result)

        @builtins.property
        def srt_listener(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.SrtListenerRouterInputConfigurationProperty"]]:
            '''The configuration settings for a router input using the SRT (Secure Reliable Transport) protocol in listener mode, including the port, minimum latency, and decryption key configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-failoverrouterinputprotocolconfiguration.html#cfn-mediaconnect-routerinput-failoverrouterinputprotocolconfiguration-srtlistener
            '''
            result = self._values.get("srt_listener")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.SrtListenerRouterInputConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FailoverRouterInputProtocolConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterInputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"automatic": "automatic", "secrets_manager": "secretsManager"},
    )
    class FlowTransitEncryptionKeyConfigurationProperty:
        def __init__(
            self,
            *,
            automatic: typing.Any = None,
            secrets_manager: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param automatic: Configuration settings for automatic encryption key management, where MediaConnect handles key creation and rotation.
            :param secrets_manager: The configuration settings for transit encryption using AWS Secrets Manager, including the secret ARN and role ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-flowtransitencryptionkeyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                # automatic: Any
                
                flow_transit_encryption_key_configuration_property = mediaconnect_mixins.CfnRouterInputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty(
                    automatic=automatic,
                    secrets_manager=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                        role_arn="roleArn",
                        secret_arn="secretArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__edb5cc2830fcef4ea00899d7db45834d795229186d57b0a48b3ff7e3f7105eba)
                check_type(argname="argument automatic", value=automatic, expected_type=type_hints["automatic"])
                check_type(argname="argument secrets_manager", value=secrets_manager, expected_type=type_hints["secrets_manager"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if automatic is not None:
                self._values["automatic"] = automatic
            if secrets_manager is not None:
                self._values["secrets_manager"] = secrets_manager

        @builtins.property
        def automatic(self) -> typing.Any:
            '''Configuration settings for automatic encryption key management, where MediaConnect handles key creation and rotation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-flowtransitencryptionkeyconfiguration.html#cfn-mediaconnect-routerinput-flowtransitencryptionkeyconfiguration-automatic
            '''
            result = self._values.get("automatic")
            return typing.cast(typing.Any, result)

        @builtins.property
        def secrets_manager(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty"]]:
            '''The configuration settings for transit encryption using AWS Secrets Manager, including the secret ARN and role ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-flowtransitencryptionkeyconfiguration.html#cfn-mediaconnect-routerinput-flowtransitencryptionkeyconfiguration-secretsmanager
            '''
            result = self._values.get("secrets_manager")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FlowTransitEncryptionKeyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterInputPropsMixin.FlowTransitEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption_key_configuration": "encryptionKeyConfiguration",
            "encryption_key_type": "encryptionKeyType",
        },
    )
    class FlowTransitEncryptionProperty:
        def __init__(
            self,
            *,
            encryption_key_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            encryption_key_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration that defines how content is encrypted during transit between the MediaConnect router and a MediaConnect flow.

            :param encryption_key_configuration: Configuration settings for flow transit encryption keys.
            :param encryption_key_type: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-flowtransitencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                # automatic: Any
                
                flow_transit_encryption_property = mediaconnect_mixins.CfnRouterInputPropsMixin.FlowTransitEncryptionProperty(
                    encryption_key_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty(
                        automatic=automatic,
                        secrets_manager=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                            role_arn="roleArn",
                            secret_arn="secretArn"
                        )
                    ),
                    encryption_key_type="encryptionKeyType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f25287d521a16647d90722e1a591fcf8774eb8da48b00d612e3014adef96eaa3)
                check_type(argname="argument encryption_key_configuration", value=encryption_key_configuration, expected_type=type_hints["encryption_key_configuration"])
                check_type(argname="argument encryption_key_type", value=encryption_key_type, expected_type=type_hints["encryption_key_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_key_configuration is not None:
                self._values["encryption_key_configuration"] = encryption_key_configuration
            if encryption_key_type is not None:
                self._values["encryption_key_type"] = encryption_key_type

        @builtins.property
        def encryption_key_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty"]]:
            '''Configuration settings for flow transit encryption keys.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-flowtransitencryption.html#cfn-mediaconnect-routerinput-flowtransitencryption-encryptionkeyconfiguration
            '''
            result = self._values.get("encryption_key_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty"]], result)

        @builtins.property
        def encryption_key_type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-flowtransitencryption.html#cfn-mediaconnect-routerinput-flowtransitencryption-encryptionkeytype
            '''
            result = self._values.get("encryption_key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FlowTransitEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterInputPropsMixin.MaintenanceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"default": "default", "preferred_day_time": "preferredDayTime"},
    )
    class MaintenanceConfigurationProperty:
        def __init__(
            self,
            *,
            default: typing.Any = None,
            preferred_day_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.PreferredDayTimeMaintenanceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param default: Configuration settings for default maintenance scheduling.
            :param preferred_day_time: Configuration for preferred day and time maintenance settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-maintenanceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                # default_: Any
                
                maintenance_configuration_property = mediaconnect_mixins.CfnRouterInputPropsMixin.MaintenanceConfigurationProperty(
                    default=default_,
                    preferred_day_time=mediaconnect_mixins.CfnRouterInputPropsMixin.PreferredDayTimeMaintenanceConfigurationProperty(
                        day="day",
                        time="time"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9f9ef96881f91b6f58a223b876257162bfcf70db6f0952fb225065763bbb079e)
                check_type(argname="argument default", value=default, expected_type=type_hints["default"])
                check_type(argname="argument preferred_day_time", value=preferred_day_time, expected_type=type_hints["preferred_day_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default is not None:
                self._values["default"] = default
            if preferred_day_time is not None:
                self._values["preferred_day_time"] = preferred_day_time

        @builtins.property
        def default(self) -> typing.Any:
            '''Configuration settings for default maintenance scheduling.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-maintenanceconfiguration.html#cfn-mediaconnect-routerinput-maintenanceconfiguration-default
            '''
            result = self._values.get("default")
            return typing.cast(typing.Any, result)

        @builtins.property
        def preferred_day_time(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.PreferredDayTimeMaintenanceConfigurationProperty"]]:
            '''Configuration for preferred day and time maintenance settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-maintenanceconfiguration.html#cfn-mediaconnect-routerinput-maintenanceconfiguration-preferreddaytime
            '''
            result = self._values.get("preferred_day_time")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.PreferredDayTimeMaintenanceConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaintenanceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterInputPropsMixin.MediaConnectFlowRouterInputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "flow_arn": "flowArn",
            "flow_output_arn": "flowOutputArn",
            "source_transit_decryption": "sourceTransitDecryption",
        },
    )
    class MediaConnectFlowRouterInputConfigurationProperty:
        def __init__(
            self,
            *,
            flow_arn: typing.Optional[builtins.str] = None,
            flow_output_arn: typing.Optional[builtins.str] = None,
            source_transit_decryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.FlowTransitEncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration settings for connecting a router input to a flow output.

            :param flow_arn: The ARN of the flow to connect to.
            :param flow_output_arn: The ARN of the flow output to connect to this router input.
            :param source_transit_decryption: The configuration that defines how content is encrypted during transit between the MediaConnect router and a MediaConnect flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-mediaconnectflowrouterinputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                # automatic: Any
                
                media_connect_flow_router_input_configuration_property = mediaconnect_mixins.CfnRouterInputPropsMixin.MediaConnectFlowRouterInputConfigurationProperty(
                    flow_arn="flowArn",
                    flow_output_arn="flowOutputArn",
                    source_transit_decryption=mediaconnect_mixins.CfnRouterInputPropsMixin.FlowTransitEncryptionProperty(
                        encryption_key_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty(
                            automatic=automatic,
                            secrets_manager=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                role_arn="roleArn",
                                secret_arn="secretArn"
                            )
                        ),
                        encryption_key_type="encryptionKeyType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8f9036438654c62b0587056b4c3e5b717a9a43e423c3fb72ea02a306503c6cae)
                check_type(argname="argument flow_arn", value=flow_arn, expected_type=type_hints["flow_arn"])
                check_type(argname="argument flow_output_arn", value=flow_output_arn, expected_type=type_hints["flow_output_arn"])
                check_type(argname="argument source_transit_decryption", value=source_transit_decryption, expected_type=type_hints["source_transit_decryption"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if flow_arn is not None:
                self._values["flow_arn"] = flow_arn
            if flow_output_arn is not None:
                self._values["flow_output_arn"] = flow_output_arn
            if source_transit_decryption is not None:
                self._values["source_transit_decryption"] = source_transit_decryption

        @builtins.property
        def flow_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the flow to connect to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-mediaconnectflowrouterinputconfiguration.html#cfn-mediaconnect-routerinput-mediaconnectflowrouterinputconfiguration-flowarn
            '''
            result = self._values.get("flow_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def flow_output_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the flow output to connect to this router input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-mediaconnectflowrouterinputconfiguration.html#cfn-mediaconnect-routerinput-mediaconnectflowrouterinputconfiguration-flowoutputarn
            '''
            result = self._values.get("flow_output_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_transit_decryption(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.FlowTransitEncryptionProperty"]]:
            '''The configuration that defines how content is encrypted during transit between the MediaConnect router and a MediaConnect flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-mediaconnectflowrouterinputconfiguration.html#cfn-mediaconnect-routerinput-mediaconnectflowrouterinputconfiguration-sourcetransitdecryption
            '''
            result = self._values.get("source_transit_decryption")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.FlowTransitEncryptionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MediaConnectFlowRouterInputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterInputPropsMixin.MergeRouterInputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "merge_recovery_window_milliseconds": "mergeRecoveryWindowMilliseconds",
            "network_interface_arn": "networkInterfaceArn",
            "protocol_configurations": "protocolConfigurations",
        },
    )
    class MergeRouterInputConfigurationProperty:
        def __init__(
            self,
            *,
            merge_recovery_window_milliseconds: typing.Optional[jsii.Number] = None,
            network_interface_arn: typing.Optional[builtins.str] = None,
            protocol_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.MergeRouterInputProtocolConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Configuration settings for a merge router input that combines two input sources.

            :param merge_recovery_window_milliseconds: The time window in milliseconds for merging the two input sources.
            :param network_interface_arn: The ARN of the network interface to use for this merge router input.
            :param protocol_configurations: A list of exactly two protocol configurations for the merge input sources. Both must use the same protocol type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-mergerouterinputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                merge_router_input_configuration_property = mediaconnect_mixins.CfnRouterInputPropsMixin.MergeRouterInputConfigurationProperty(
                    merge_recovery_window_milliseconds=123,
                    network_interface_arn="networkInterfaceArn",
                    protocol_configurations=[mediaconnect_mixins.CfnRouterInputPropsMixin.MergeRouterInputProtocolConfigurationProperty(
                        rist=mediaconnect_mixins.CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty(
                            port=123,
                            recovery_latency_milliseconds=123
                        ),
                        rtp=mediaconnect_mixins.CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty(
                            forward_error_correction="forwardErrorCorrection",
                            port=123
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__26deea9c73ecdef770f309152c9b3a9af39ff9add1c9031b73c63c42a59ef6e8)
                check_type(argname="argument merge_recovery_window_milliseconds", value=merge_recovery_window_milliseconds, expected_type=type_hints["merge_recovery_window_milliseconds"])
                check_type(argname="argument network_interface_arn", value=network_interface_arn, expected_type=type_hints["network_interface_arn"])
                check_type(argname="argument protocol_configurations", value=protocol_configurations, expected_type=type_hints["protocol_configurations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if merge_recovery_window_milliseconds is not None:
                self._values["merge_recovery_window_milliseconds"] = merge_recovery_window_milliseconds
            if network_interface_arn is not None:
                self._values["network_interface_arn"] = network_interface_arn
            if protocol_configurations is not None:
                self._values["protocol_configurations"] = protocol_configurations

        @builtins.property
        def merge_recovery_window_milliseconds(self) -> typing.Optional[jsii.Number]:
            '''The time window in milliseconds for merging the two input sources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-mergerouterinputconfiguration.html#cfn-mediaconnect-routerinput-mergerouterinputconfiguration-mergerecoverywindowmilliseconds
            '''
            result = self._values.get("merge_recovery_window_milliseconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def network_interface_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the network interface to use for this merge router input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-mergerouterinputconfiguration.html#cfn-mediaconnect-routerinput-mergerouterinputconfiguration-networkinterfacearn
            '''
            result = self._values.get("network_interface_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.MergeRouterInputProtocolConfigurationProperty"]]]]:
            '''A list of exactly two protocol configurations for the merge input sources.

            Both must use the same protocol type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-mergerouterinputconfiguration.html#cfn-mediaconnect-routerinput-mergerouterinputconfiguration-protocolconfigurations
            '''
            result = self._values.get("protocol_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.MergeRouterInputProtocolConfigurationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MergeRouterInputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterInputPropsMixin.MergeRouterInputProtocolConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"rist": "rist", "rtp": "rtp"},
    )
    class MergeRouterInputProtocolConfigurationProperty:
        def __init__(
            self,
            *,
            rist: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rtp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param rist: The configuration settings for a router input using the RIST (Reliable Internet Stream Transport) protocol, including the port and recovery latency.
            :param rtp: The configuration settings for a Router Input using the RTP (Real-Time Transport Protocol) protocol, including the port and forward error correction state.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-mergerouterinputprotocolconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                merge_router_input_protocol_configuration_property = mediaconnect_mixins.CfnRouterInputPropsMixin.MergeRouterInputProtocolConfigurationProperty(
                    rist=mediaconnect_mixins.CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty(
                        port=123,
                        recovery_latency_milliseconds=123
                    ),
                    rtp=mediaconnect_mixins.CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty(
                        forward_error_correction="forwardErrorCorrection",
                        port=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f05aa15407508d4af14b1440ed6e6dd1b8770a64f2bdda3129f0e2cbeb68df13)
                check_type(argname="argument rist", value=rist, expected_type=type_hints["rist"])
                check_type(argname="argument rtp", value=rtp, expected_type=type_hints["rtp"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rist is not None:
                self._values["rist"] = rist
            if rtp is not None:
                self._values["rtp"] = rtp

        @builtins.property
        def rist(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty"]]:
            '''The configuration settings for a router input using the RIST (Reliable Internet Stream Transport) protocol, including the port and recovery latency.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-mergerouterinputprotocolconfiguration.html#cfn-mediaconnect-routerinput-mergerouterinputprotocolconfiguration-rist
            '''
            result = self._values.get("rist")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty"]], result)

        @builtins.property
        def rtp(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty"]]:
            '''The configuration settings for a Router Input using the RTP (Real-Time Transport Protocol) protocol, including the port and forward error correction state.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-mergerouterinputprotocolconfiguration.html#cfn-mediaconnect-routerinput-mergerouterinputprotocolconfiguration-rtp
            '''
            result = self._values.get("rtp")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MergeRouterInputProtocolConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterInputPropsMixin.PreferredDayTimeMaintenanceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"day": "day", "time": "time"},
    )
    class PreferredDayTimeMaintenanceConfigurationProperty:
        def __init__(
            self,
            *,
            day: typing.Optional[builtins.str] = None,
            time: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration for preferred day and time maintenance settings.

            :param day: 
            :param time: The preferred time for maintenance operations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-preferreddaytimemaintenanceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                preferred_day_time_maintenance_configuration_property = mediaconnect_mixins.CfnRouterInputPropsMixin.PreferredDayTimeMaintenanceConfigurationProperty(
                    day="day",
                    time="time"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c96514398eeaa876a5bfb14ff8ab7ebdc44f9db450125f71684c28e33d28563e)
                check_type(argname="argument day", value=day, expected_type=type_hints["day"])
                check_type(argname="argument time", value=time, expected_type=type_hints["time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if day is not None:
                self._values["day"] = day
            if time is not None:
                self._values["time"] = time

        @builtins.property
        def day(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-preferreddaytimemaintenanceconfiguration.html#cfn-mediaconnect-routerinput-preferreddaytimemaintenanceconfiguration-day
            '''
            result = self._values.get("day")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def time(self) -> typing.Optional[builtins.str]:
            '''The preferred time for maintenance operations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-preferreddaytimemaintenanceconfiguration.html#cfn-mediaconnect-routerinput-preferreddaytimemaintenanceconfiguration-time
            '''
            result = self._values.get("time")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PreferredDayTimeMaintenanceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "port": "port",
            "recovery_latency_milliseconds": "recoveryLatencyMilliseconds",
        },
    )
    class RistRouterInputConfigurationProperty:
        def __init__(
            self,
            *,
            port: typing.Optional[jsii.Number] = None,
            recovery_latency_milliseconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The configuration settings for a router input using the RIST (Reliable Internet Stream Transport) protocol, including the port and recovery latency.

            :param port: The port number used for the RIST protocol in the router input configuration.
            :param recovery_latency_milliseconds: The recovery latency in milliseconds for the RIST protocol in the router input configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-ristrouterinputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                rist_router_input_configuration_property = mediaconnect_mixins.CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty(
                    port=123,
                    recovery_latency_milliseconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6aff331aa43acdb81e5495950dfe72ff5419b926ac3dbeff94558488b19775bc)
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument recovery_latency_milliseconds", value=recovery_latency_milliseconds, expected_type=type_hints["recovery_latency_milliseconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if port is not None:
                self._values["port"] = port
            if recovery_latency_milliseconds is not None:
                self._values["recovery_latency_milliseconds"] = recovery_latency_milliseconds

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port number used for the RIST protocol in the router input configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-ristrouterinputconfiguration.html#cfn-mediaconnect-routerinput-ristrouterinputconfiguration-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def recovery_latency_milliseconds(self) -> typing.Optional[jsii.Number]:
            '''The recovery latency in milliseconds for the RIST protocol in the router input configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-ristrouterinputconfiguration.html#cfn-mediaconnect-routerinput-ristrouterinputconfiguration-recoverylatencymilliseconds
            '''
            result = self._values.get("recovery_latency_milliseconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RistRouterInputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterInputPropsMixin.RouterInputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "failover": "failover",
            "media_connect_flow": "mediaConnectFlow",
            "merge": "merge",
            "standard": "standard",
        },
    )
    class RouterInputConfigurationProperty:
        def __init__(
            self,
            *,
            failover: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.FailoverRouterInputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            media_connect_flow: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.MediaConnectFlowRouterInputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            merge: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.MergeRouterInputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            standard: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.StandardRouterInputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param failover: Configuration settings for a failover router input that allows switching between two input sources.
            :param media_connect_flow: Configuration settings for connecting a router input to a flow output.
            :param merge: Configuration settings for a merge router input that combines two input sources.
            :param standard: The configuration settings for a standard router input, including the protocol, protocol-specific configuration, network interface, and availability zone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-routerinputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                # automatic: Any
                
                router_input_configuration_property = mediaconnect_mixins.CfnRouterInputPropsMixin.RouterInputConfigurationProperty(
                    failover=mediaconnect_mixins.CfnRouterInputPropsMixin.FailoverRouterInputConfigurationProperty(
                        network_interface_arn="networkInterfaceArn",
                        primary_source_index=123,
                        protocol_configurations=[mediaconnect_mixins.CfnRouterInputPropsMixin.FailoverRouterInputProtocolConfigurationProperty(
                            rist=mediaconnect_mixins.CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty(
                                port=123,
                                recovery_latency_milliseconds=123
                            ),
                            rtp=mediaconnect_mixins.CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty(
                                forward_error_correction="forwardErrorCorrection",
                                port=123
                            ),
                            srt_caller=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtCallerRouterInputConfigurationProperty(
                                decryption_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty(
                                    encryption_key=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                        role_arn="roleArn",
                                        secret_arn="secretArn"
                                    )
                                ),
                                minimum_latency_milliseconds=123,
                                source_address="sourceAddress",
                                source_port=123,
                                stream_id="streamId"
                            ),
                            srt_listener=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtListenerRouterInputConfigurationProperty(
                                decryption_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty(
                                    encryption_key=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                        role_arn="roleArn",
                                        secret_arn="secretArn"
                                    )
                                ),
                                minimum_latency_milliseconds=123,
                                port=123
                            )
                        )],
                        source_priority_mode="sourcePriorityMode"
                    ),
                    media_connect_flow=mediaconnect_mixins.CfnRouterInputPropsMixin.MediaConnectFlowRouterInputConfigurationProperty(
                        flow_arn="flowArn",
                        flow_output_arn="flowOutputArn",
                        source_transit_decryption=mediaconnect_mixins.CfnRouterInputPropsMixin.FlowTransitEncryptionProperty(
                            encryption_key_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty(
                                automatic=automatic,
                                secrets_manager=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                    role_arn="roleArn",
                                    secret_arn="secretArn"
                                )
                            ),
                            encryption_key_type="encryptionKeyType"
                        )
                    ),
                    merge=mediaconnect_mixins.CfnRouterInputPropsMixin.MergeRouterInputConfigurationProperty(
                        merge_recovery_window_milliseconds=123,
                        network_interface_arn="networkInterfaceArn",
                        protocol_configurations=[mediaconnect_mixins.CfnRouterInputPropsMixin.MergeRouterInputProtocolConfigurationProperty(
                            rist=mediaconnect_mixins.CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty(
                                port=123,
                                recovery_latency_milliseconds=123
                            ),
                            rtp=mediaconnect_mixins.CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty(
                                forward_error_correction="forwardErrorCorrection",
                                port=123
                            )
                        )]
                    ),
                    standard=mediaconnect_mixins.CfnRouterInputPropsMixin.StandardRouterInputConfigurationProperty(
                        network_interface_arn="networkInterfaceArn",
                        protocol="protocol",
                        protocol_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.RouterInputProtocolConfigurationProperty(
                            rist=mediaconnect_mixins.CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty(
                                port=123,
                                recovery_latency_milliseconds=123
                            ),
                            rtp=mediaconnect_mixins.CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty(
                                forward_error_correction="forwardErrorCorrection",
                                port=123
                            ),
                            srt_caller=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtCallerRouterInputConfigurationProperty(
                                decryption_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty(
                                    encryption_key=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                        role_arn="roleArn",
                                        secret_arn="secretArn"
                                    )
                                ),
                                minimum_latency_milliseconds=123,
                                source_address="sourceAddress",
                                source_port=123,
                                stream_id="streamId"
                            ),
                            srt_listener=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtListenerRouterInputConfigurationProperty(
                                decryption_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty(
                                    encryption_key=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                        role_arn="roleArn",
                                        secret_arn="secretArn"
                                    )
                                ),
                                minimum_latency_milliseconds=123,
                                port=123
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__be1a00d92a09d1f55f93fc6139dc55ed9f3b3ae6f1bc7f1756f389a08221392f)
                check_type(argname="argument failover", value=failover, expected_type=type_hints["failover"])
                check_type(argname="argument media_connect_flow", value=media_connect_flow, expected_type=type_hints["media_connect_flow"])
                check_type(argname="argument merge", value=merge, expected_type=type_hints["merge"])
                check_type(argname="argument standard", value=standard, expected_type=type_hints["standard"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if failover is not None:
                self._values["failover"] = failover
            if media_connect_flow is not None:
                self._values["media_connect_flow"] = media_connect_flow
            if merge is not None:
                self._values["merge"] = merge
            if standard is not None:
                self._values["standard"] = standard

        @builtins.property
        def failover(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.FailoverRouterInputConfigurationProperty"]]:
            '''Configuration settings for a failover router input that allows switching between two input sources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-routerinputconfiguration.html#cfn-mediaconnect-routerinput-routerinputconfiguration-failover
            '''
            result = self._values.get("failover")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.FailoverRouterInputConfigurationProperty"]], result)

        @builtins.property
        def media_connect_flow(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.MediaConnectFlowRouterInputConfigurationProperty"]]:
            '''Configuration settings for connecting a router input to a flow output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-routerinputconfiguration.html#cfn-mediaconnect-routerinput-routerinputconfiguration-mediaconnectflow
            '''
            result = self._values.get("media_connect_flow")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.MediaConnectFlowRouterInputConfigurationProperty"]], result)

        @builtins.property
        def merge(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.MergeRouterInputConfigurationProperty"]]:
            '''Configuration settings for a merge router input that combines two input sources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-routerinputconfiguration.html#cfn-mediaconnect-routerinput-routerinputconfiguration-merge
            '''
            result = self._values.get("merge")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.MergeRouterInputConfigurationProperty"]], result)

        @builtins.property
        def standard(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.StandardRouterInputConfigurationProperty"]]:
            '''The configuration settings for a standard router input, including the protocol, protocol-specific configuration, network interface, and availability zone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-routerinputconfiguration.html#cfn-mediaconnect-routerinput-routerinputconfiguration-standard
            '''
            result = self._values.get("standard")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.StandardRouterInputConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RouterInputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterInputPropsMixin.RouterInputProtocolConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "rist": "rist",
            "rtp": "rtp",
            "srt_caller": "srtCaller",
            "srt_listener": "srtListener",
        },
    )
    class RouterInputProtocolConfigurationProperty:
        def __init__(
            self,
            *,
            rist: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rtp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            srt_caller: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.SrtCallerRouterInputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            srt_listener: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.SrtListenerRouterInputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param rist: The configuration settings for a router input using the RIST (Reliable Internet Stream Transport) protocol, including the port and recovery latency.
            :param rtp: The configuration settings for a Router Input using the RTP (Real-Time Transport Protocol) protocol, including the port and forward error correction state.
            :param srt_caller: The configuration settings for a router input using the SRT (Secure Reliable Transport) protocol in caller mode, including the source address and port, minimum latency, stream ID, and decryption key configuration.
            :param srt_listener: The configuration settings for a router input using the SRT (Secure Reliable Transport) protocol in listener mode, including the port, minimum latency, and decryption key configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-routerinputprotocolconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                router_input_protocol_configuration_property = mediaconnect_mixins.CfnRouterInputPropsMixin.RouterInputProtocolConfigurationProperty(
                    rist=mediaconnect_mixins.CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty(
                        port=123,
                        recovery_latency_milliseconds=123
                    ),
                    rtp=mediaconnect_mixins.CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty(
                        forward_error_correction="forwardErrorCorrection",
                        port=123
                    ),
                    srt_caller=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtCallerRouterInputConfigurationProperty(
                        decryption_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty(
                            encryption_key=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                role_arn="roleArn",
                                secret_arn="secretArn"
                            )
                        ),
                        minimum_latency_milliseconds=123,
                        source_address="sourceAddress",
                        source_port=123,
                        stream_id="streamId"
                    ),
                    srt_listener=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtListenerRouterInputConfigurationProperty(
                        decryption_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty(
                            encryption_key=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                role_arn="roleArn",
                                secret_arn="secretArn"
                            )
                        ),
                        minimum_latency_milliseconds=123,
                        port=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7f49220bee41dd2398c51fdbdae5055c5ccab6ffe8a872da32a2e8bac40eee02)
                check_type(argname="argument rist", value=rist, expected_type=type_hints["rist"])
                check_type(argname="argument rtp", value=rtp, expected_type=type_hints["rtp"])
                check_type(argname="argument srt_caller", value=srt_caller, expected_type=type_hints["srt_caller"])
                check_type(argname="argument srt_listener", value=srt_listener, expected_type=type_hints["srt_listener"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rist is not None:
                self._values["rist"] = rist
            if rtp is not None:
                self._values["rtp"] = rtp
            if srt_caller is not None:
                self._values["srt_caller"] = srt_caller
            if srt_listener is not None:
                self._values["srt_listener"] = srt_listener

        @builtins.property
        def rist(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty"]]:
            '''The configuration settings for a router input using the RIST (Reliable Internet Stream Transport) protocol, including the port and recovery latency.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-routerinputprotocolconfiguration.html#cfn-mediaconnect-routerinput-routerinputprotocolconfiguration-rist
            '''
            result = self._values.get("rist")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty"]], result)

        @builtins.property
        def rtp(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty"]]:
            '''The configuration settings for a Router Input using the RTP (Real-Time Transport Protocol) protocol, including the port and forward error correction state.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-routerinputprotocolconfiguration.html#cfn-mediaconnect-routerinput-routerinputprotocolconfiguration-rtp
            '''
            result = self._values.get("rtp")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty"]], result)

        @builtins.property
        def srt_caller(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.SrtCallerRouterInputConfigurationProperty"]]:
            '''The configuration settings for a router input using the SRT (Secure Reliable Transport) protocol in caller mode, including the source address and port, minimum latency, stream ID, and decryption key configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-routerinputprotocolconfiguration.html#cfn-mediaconnect-routerinput-routerinputprotocolconfiguration-srtcaller
            '''
            result = self._values.get("srt_caller")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.SrtCallerRouterInputConfigurationProperty"]], result)

        @builtins.property
        def srt_listener(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.SrtListenerRouterInputConfigurationProperty"]]:
            '''The configuration settings for a router input using the SRT (Secure Reliable Transport) protocol in listener mode, including the port, minimum latency, and decryption key configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-routerinputprotocolconfiguration.html#cfn-mediaconnect-routerinput-routerinputprotocolconfiguration-srtlistener
            '''
            result = self._values.get("srt_listener")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.SrtListenerRouterInputConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RouterInputProtocolConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterInputPropsMixin.RouterInputTransitEncryptionKeyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"automatic": "automatic", "secrets_manager": "secretsManager"},
    )
    class RouterInputTransitEncryptionKeyConfigurationProperty:
        def __init__(
            self,
            *,
            automatic: typing.Any = None,
            secrets_manager: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param automatic: Configuration settings for automatic encryption key management, where MediaConnect handles key creation and rotation.
            :param secrets_manager: The configuration settings for transit encryption using AWS Secrets Manager, including the secret ARN and role ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-routerinputtransitencryptionkeyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                # automatic: Any
                
                router_input_transit_encryption_key_configuration_property = mediaconnect_mixins.CfnRouterInputPropsMixin.RouterInputTransitEncryptionKeyConfigurationProperty(
                    automatic=automatic,
                    secrets_manager=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                        role_arn="roleArn",
                        secret_arn="secretArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4e71eb1c00f0874b687fd93dfec819c1f80d25fc58c248ceb604b8815a73398e)
                check_type(argname="argument automatic", value=automatic, expected_type=type_hints["automatic"])
                check_type(argname="argument secrets_manager", value=secrets_manager, expected_type=type_hints["secrets_manager"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if automatic is not None:
                self._values["automatic"] = automatic
            if secrets_manager is not None:
                self._values["secrets_manager"] = secrets_manager

        @builtins.property
        def automatic(self) -> typing.Any:
            '''Configuration settings for automatic encryption key management, where MediaConnect handles key creation and rotation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-routerinputtransitencryptionkeyconfiguration.html#cfn-mediaconnect-routerinput-routerinputtransitencryptionkeyconfiguration-automatic
            '''
            result = self._values.get("automatic")
            return typing.cast(typing.Any, result)

        @builtins.property
        def secrets_manager(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty"]]:
            '''The configuration settings for transit encryption using AWS Secrets Manager, including the secret ARN and role ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-routerinputtransitencryptionkeyconfiguration.html#cfn-mediaconnect-routerinput-routerinputtransitencryptionkeyconfiguration-secretsmanager
            '''
            result = self._values.get("secrets_manager")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RouterInputTransitEncryptionKeyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterInputPropsMixin.RouterInputTransitEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption_key_configuration": "encryptionKeyConfiguration",
            "encryption_key_type": "encryptionKeyType",
        },
    )
    class RouterInputTransitEncryptionProperty:
        def __init__(
            self,
            *,
            encryption_key_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.RouterInputTransitEncryptionKeyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            encryption_key_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The transit encryption settings for a router input.

            :param encryption_key_configuration: Defines the configuration settings for transit encryption keys.
            :param encryption_key_type: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-routerinputtransitencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                # automatic: Any
                
                router_input_transit_encryption_property = mediaconnect_mixins.CfnRouterInputPropsMixin.RouterInputTransitEncryptionProperty(
                    encryption_key_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.RouterInputTransitEncryptionKeyConfigurationProperty(
                        automatic=automatic,
                        secrets_manager=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                            role_arn="roleArn",
                            secret_arn="secretArn"
                        )
                    ),
                    encryption_key_type="encryptionKeyType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e2b0130827775a62f47c7a430a30ab5b61efb414fcea9e03d8866ce2c96b739c)
                check_type(argname="argument encryption_key_configuration", value=encryption_key_configuration, expected_type=type_hints["encryption_key_configuration"])
                check_type(argname="argument encryption_key_type", value=encryption_key_type, expected_type=type_hints["encryption_key_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_key_configuration is not None:
                self._values["encryption_key_configuration"] = encryption_key_configuration
            if encryption_key_type is not None:
                self._values["encryption_key_type"] = encryption_key_type

        @builtins.property
        def encryption_key_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.RouterInputTransitEncryptionKeyConfigurationProperty"]]:
            '''Defines the configuration settings for transit encryption keys.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-routerinputtransitencryption.html#cfn-mediaconnect-routerinput-routerinputtransitencryption-encryptionkeyconfiguration
            '''
            result = self._values.get("encryption_key_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.RouterInputTransitEncryptionKeyConfigurationProperty"]], result)

        @builtins.property
        def encryption_key_type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-routerinputtransitencryption.html#cfn-mediaconnect-routerinput-routerinputtransitencryption-encryptionkeytype
            '''
            result = self._values.get("encryption_key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RouterInputTransitEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "forward_error_correction": "forwardErrorCorrection",
            "port": "port",
        },
    )
    class RtpRouterInputConfigurationProperty:
        def __init__(
            self,
            *,
            forward_error_correction: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The configuration settings for a Router Input using the RTP (Real-Time Transport Protocol) protocol, including the port and forward error correction state.

            :param forward_error_correction: 
            :param port: The port number used for the RTP protocol in the router input configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-rtprouterinputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                rtp_router_input_configuration_property = mediaconnect_mixins.CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty(
                    forward_error_correction="forwardErrorCorrection",
                    port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e4bfe3ded3d1a81fddb2aa0a372cbf36aa083a7f32be5f25abf295849fe08388)
                check_type(argname="argument forward_error_correction", value=forward_error_correction, expected_type=type_hints["forward_error_correction"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if forward_error_correction is not None:
                self._values["forward_error_correction"] = forward_error_correction
            if port is not None:
                self._values["port"] = port

        @builtins.property
        def forward_error_correction(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-rtprouterinputconfiguration.html#cfn-mediaconnect-routerinput-rtprouterinputconfiguration-forwarderrorcorrection
            '''
            result = self._values.get("forward_error_correction")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port number used for the RTP protocol in the router input configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-rtprouterinputconfiguration.html#cfn-mediaconnect-routerinput-rtprouterinputconfiguration-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RtpRouterInputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"role_arn": "roleArn", "secret_arn": "secretArn"},
    )
    class SecretsManagerEncryptionKeyConfigurationProperty:
        def __init__(
            self,
            *,
            role_arn: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration settings for transit encryption using AWS Secrets Manager, including the secret ARN and role ARN.

            :param role_arn: The ARN of the IAM role assumed by MediaConnect to access the AWS Secrets Manager secret.
            :param secret_arn: The ARN of the AWS Secrets Manager secret used for transit encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-secretsmanagerencryptionkeyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                secrets_manager_encryption_key_configuration_property = mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                    role_arn="roleArn",
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4ca745017407377c93bf9274b6f6b424c3809b62e0e500705ba1e2beb12ebbaa)
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM role assumed by MediaConnect to access the AWS Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-secretsmanagerencryptionkeyconfiguration.html#cfn-mediaconnect-routerinput-secretsmanagerencryptionkeyconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the AWS Secrets Manager secret used for transit encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-secretsmanagerencryptionkeyconfiguration.html#cfn-mediaconnect-routerinput-secretsmanagerencryptionkeyconfiguration-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecretsManagerEncryptionKeyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterInputPropsMixin.SrtCallerRouterInputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "decryption_configuration": "decryptionConfiguration",
            "minimum_latency_milliseconds": "minimumLatencyMilliseconds",
            "source_address": "sourceAddress",
            "source_port": "sourcePort",
            "stream_id": "streamId",
        },
    )
    class SrtCallerRouterInputConfigurationProperty:
        def __init__(
            self,
            *,
            decryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            minimum_latency_milliseconds: typing.Optional[jsii.Number] = None,
            source_address: typing.Optional[builtins.str] = None,
            source_port: typing.Optional[jsii.Number] = None,
            stream_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration settings for a router input using the SRT (Secure Reliable Transport) protocol in caller mode, including the source address and port, minimum latency, stream ID, and decryption key configuration.

            :param decryption_configuration: Contains the configuration settings for decrypting SRT streams, including the encryption key details and decryption parameters.
            :param minimum_latency_milliseconds: The minimum latency in milliseconds for the SRT protocol in caller mode.
            :param source_address: The source IP address for the SRT protocol in caller mode.
            :param source_port: The source port number for the SRT protocol in caller mode.
            :param stream_id: The stream ID for the SRT protocol in caller mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-srtcallerrouterinputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                srt_caller_router_input_configuration_property = mediaconnect_mixins.CfnRouterInputPropsMixin.SrtCallerRouterInputConfigurationProperty(
                    decryption_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty(
                        encryption_key=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                            role_arn="roleArn",
                            secret_arn="secretArn"
                        )
                    ),
                    minimum_latency_milliseconds=123,
                    source_address="sourceAddress",
                    source_port=123,
                    stream_id="streamId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__044b1425cb641760a419cd9f6282e1e69fb42a9f34f4c3363ee53506c63877b2)
                check_type(argname="argument decryption_configuration", value=decryption_configuration, expected_type=type_hints["decryption_configuration"])
                check_type(argname="argument minimum_latency_milliseconds", value=minimum_latency_milliseconds, expected_type=type_hints["minimum_latency_milliseconds"])
                check_type(argname="argument source_address", value=source_address, expected_type=type_hints["source_address"])
                check_type(argname="argument source_port", value=source_port, expected_type=type_hints["source_port"])
                check_type(argname="argument stream_id", value=stream_id, expected_type=type_hints["stream_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if decryption_configuration is not None:
                self._values["decryption_configuration"] = decryption_configuration
            if minimum_latency_milliseconds is not None:
                self._values["minimum_latency_milliseconds"] = minimum_latency_milliseconds
            if source_address is not None:
                self._values["source_address"] = source_address
            if source_port is not None:
                self._values["source_port"] = source_port
            if stream_id is not None:
                self._values["stream_id"] = stream_id

        @builtins.property
        def decryption_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty"]]:
            '''Contains the configuration settings for decrypting SRT streams, including the encryption key details and decryption parameters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-srtcallerrouterinputconfiguration.html#cfn-mediaconnect-routerinput-srtcallerrouterinputconfiguration-decryptionconfiguration
            '''
            result = self._values.get("decryption_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty"]], result)

        @builtins.property
        def minimum_latency_milliseconds(self) -> typing.Optional[jsii.Number]:
            '''The minimum latency in milliseconds for the SRT protocol in caller mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-srtcallerrouterinputconfiguration.html#cfn-mediaconnect-routerinput-srtcallerrouterinputconfiguration-minimumlatencymilliseconds
            '''
            result = self._values.get("minimum_latency_milliseconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def source_address(self) -> typing.Optional[builtins.str]:
            '''The source IP address for the SRT protocol in caller mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-srtcallerrouterinputconfiguration.html#cfn-mediaconnect-routerinput-srtcallerrouterinputconfiguration-sourceaddress
            '''
            result = self._values.get("source_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_port(self) -> typing.Optional[jsii.Number]:
            '''The source port number for the SRT protocol in caller mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-srtcallerrouterinputconfiguration.html#cfn-mediaconnect-routerinput-srtcallerrouterinputconfiguration-sourceport
            '''
            result = self._values.get("source_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stream_id(self) -> typing.Optional[builtins.str]:
            '''The stream ID for the SRT protocol in caller mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-srtcallerrouterinputconfiguration.html#cfn-mediaconnect-routerinput-srtcallerrouterinputconfiguration-streamid
            '''
            result = self._values.get("stream_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SrtCallerRouterInputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"encryption_key": "encryptionKey"},
    )
    class SrtDecryptionConfigurationProperty:
        def __init__(
            self,
            *,
            encryption_key: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains the configuration settings for decrypting SRT streams, including the encryption key details and decryption parameters.

            :param encryption_key: The configuration settings for transit encryption using AWS Secrets Manager, including the secret ARN and role ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-srtdecryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                srt_decryption_configuration_property = mediaconnect_mixins.CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty(
                    encryption_key=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                        role_arn="roleArn",
                        secret_arn="secretArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__df94785e8cedbffb63bc59b79f0f0d8c9de4a924acad81639abf87ca79996f74)
                check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_key is not None:
                self._values["encryption_key"] = encryption_key

        @builtins.property
        def encryption_key(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty"]]:
            '''The configuration settings for transit encryption using AWS Secrets Manager, including the secret ARN and role ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-srtdecryptionconfiguration.html#cfn-mediaconnect-routerinput-srtdecryptionconfiguration-encryptionkey
            '''
            result = self._values.get("encryption_key")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SrtDecryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterInputPropsMixin.SrtListenerRouterInputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "decryption_configuration": "decryptionConfiguration",
            "minimum_latency_milliseconds": "minimumLatencyMilliseconds",
            "port": "port",
        },
    )
    class SrtListenerRouterInputConfigurationProperty:
        def __init__(
            self,
            *,
            decryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            minimum_latency_milliseconds: typing.Optional[jsii.Number] = None,
            port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The configuration settings for a router input using the SRT (Secure Reliable Transport) protocol in listener mode, including the port, minimum latency, and decryption key configuration.

            :param decryption_configuration: Contains the configuration settings for decrypting SRT streams, including the encryption key details and decryption parameters.
            :param minimum_latency_milliseconds: The minimum latency in milliseconds for the SRT protocol in listener mode.
            :param port: The port number for the SRT protocol in listener mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-srtlistenerrouterinputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                srt_listener_router_input_configuration_property = mediaconnect_mixins.CfnRouterInputPropsMixin.SrtListenerRouterInputConfigurationProperty(
                    decryption_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty(
                        encryption_key=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                            role_arn="roleArn",
                            secret_arn="secretArn"
                        )
                    ),
                    minimum_latency_milliseconds=123,
                    port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6a169e6fa1dc1543f9a15a2ad83039c3ce761a57ecb72e2453d472b4b74082b9)
                check_type(argname="argument decryption_configuration", value=decryption_configuration, expected_type=type_hints["decryption_configuration"])
                check_type(argname="argument minimum_latency_milliseconds", value=minimum_latency_milliseconds, expected_type=type_hints["minimum_latency_milliseconds"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if decryption_configuration is not None:
                self._values["decryption_configuration"] = decryption_configuration
            if minimum_latency_milliseconds is not None:
                self._values["minimum_latency_milliseconds"] = minimum_latency_milliseconds
            if port is not None:
                self._values["port"] = port

        @builtins.property
        def decryption_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty"]]:
            '''Contains the configuration settings for decrypting SRT streams, including the encryption key details and decryption parameters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-srtlistenerrouterinputconfiguration.html#cfn-mediaconnect-routerinput-srtlistenerrouterinputconfiguration-decryptionconfiguration
            '''
            result = self._values.get("decryption_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty"]], result)

        @builtins.property
        def minimum_latency_milliseconds(self) -> typing.Optional[jsii.Number]:
            '''The minimum latency in milliseconds for the SRT protocol in listener mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-srtlistenerrouterinputconfiguration.html#cfn-mediaconnect-routerinput-srtlistenerrouterinputconfiguration-minimumlatencymilliseconds
            '''
            result = self._values.get("minimum_latency_milliseconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port number for the SRT protocol in listener mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-srtlistenerrouterinputconfiguration.html#cfn-mediaconnect-routerinput-srtlistenerrouterinputconfiguration-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SrtListenerRouterInputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterInputPropsMixin.StandardRouterInputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "network_interface_arn": "networkInterfaceArn",
            "protocol": "protocol",
            "protocol_configuration": "protocolConfiguration",
        },
    )
    class StandardRouterInputConfigurationProperty:
        def __init__(
            self,
            *,
            network_interface_arn: typing.Optional[builtins.str] = None,
            protocol: typing.Optional[builtins.str] = None,
            protocol_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterInputPropsMixin.RouterInputProtocolConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration settings for a standard router input, including the protocol, protocol-specific configuration, network interface, and availability zone.

            :param network_interface_arn: The Amazon Resource Name (ARN) of the network interface associated with the standard router input.
            :param protocol: 
            :param protocol_configuration: The protocol configuration settings for a router input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-standardrouterinputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                standard_router_input_configuration_property = mediaconnect_mixins.CfnRouterInputPropsMixin.StandardRouterInputConfigurationProperty(
                    network_interface_arn="networkInterfaceArn",
                    protocol="protocol",
                    protocol_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.RouterInputProtocolConfigurationProperty(
                        rist=mediaconnect_mixins.CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty(
                            port=123,
                            recovery_latency_milliseconds=123
                        ),
                        rtp=mediaconnect_mixins.CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty(
                            forward_error_correction="forwardErrorCorrection",
                            port=123
                        ),
                        srt_caller=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtCallerRouterInputConfigurationProperty(
                            decryption_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty(
                                encryption_key=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                    role_arn="roleArn",
                                    secret_arn="secretArn"
                                )
                            ),
                            minimum_latency_milliseconds=123,
                            source_address="sourceAddress",
                            source_port=123,
                            stream_id="streamId"
                        ),
                        srt_listener=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtListenerRouterInputConfigurationProperty(
                            decryption_configuration=mediaconnect_mixins.CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty(
                                encryption_key=mediaconnect_mixins.CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                    role_arn="roleArn",
                                    secret_arn="secretArn"
                                )
                            ),
                            minimum_latency_milliseconds=123,
                            port=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__13ed1eea02d0ec42039ff033da981dc89577de36d8bd200e6248aadb558d982e)
                check_type(argname="argument network_interface_arn", value=network_interface_arn, expected_type=type_hints["network_interface_arn"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument protocol_configuration", value=protocol_configuration, expected_type=type_hints["protocol_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if network_interface_arn is not None:
                self._values["network_interface_arn"] = network_interface_arn
            if protocol is not None:
                self._values["protocol"] = protocol
            if protocol_configuration is not None:
                self._values["protocol_configuration"] = protocol_configuration

        @builtins.property
        def network_interface_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the network interface associated with the standard router input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-standardrouterinputconfiguration.html#cfn-mediaconnect-routerinput-standardrouterinputconfiguration-networkinterfacearn
            '''
            result = self._values.get("network_interface_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-standardrouterinputconfiguration.html#cfn-mediaconnect-routerinput-standardrouterinputconfiguration-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.RouterInputProtocolConfigurationProperty"]]:
            '''The protocol configuration settings for a router input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routerinput-standardrouterinputconfiguration.html#cfn-mediaconnect-routerinput-standardrouterinputconfiguration-protocolconfiguration
            '''
            result = self._values.get("protocol_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterInputPropsMixin.RouterInputProtocolConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StandardRouterInputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterNetworkInterfaceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration": "configuration",
        "name": "name",
        "region_name": "regionName",
        "tags": "tags",
    },
)
class CfnRouterNetworkInterfaceMixinProps:
    def __init__(
        self,
        *,
        configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterNetworkInterfacePropsMixin.RouterNetworkInterfaceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        region_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnRouterNetworkInterfacePropsMixin.

        :param configuration: The configuration settings for a router network interface.
        :param name: The name of the router network interface.
        :param region_name: The AWS Region where the router network interface is located.
        :param tags: Key-value pairs that can be used to tag and organize this router network interface.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routernetworkinterface.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
            
            cfn_router_network_interface_mixin_props = mediaconnect_mixins.CfnRouterNetworkInterfaceMixinProps(
                configuration=mediaconnect_mixins.CfnRouterNetworkInterfacePropsMixin.RouterNetworkInterfaceConfigurationProperty(
                    public=mediaconnect_mixins.CfnRouterNetworkInterfacePropsMixin.PublicRouterNetworkInterfaceConfigurationProperty(
                        allow_rules=[mediaconnect_mixins.CfnRouterNetworkInterfacePropsMixin.PublicRouterNetworkInterfaceRuleProperty(
                            cidr="cidr"
                        )]
                    ),
                    vpc=mediaconnect_mixins.CfnRouterNetworkInterfacePropsMixin.VpcRouterNetworkInterfaceConfigurationProperty(
                        security_group_ids=["securityGroupIds"],
                        subnet_id="subnetId"
                    )
                ),
                name="name",
                region_name="regionName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2b3484edc492a19afa1c12384baf035cf7060bc471d57073666f23990d627c0)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region_name", value=region_name, expected_type=type_hints["region_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration is not None:
            self._values["configuration"] = configuration
        if name is not None:
            self._values["name"] = name
        if region_name is not None:
            self._values["region_name"] = region_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterNetworkInterfacePropsMixin.RouterNetworkInterfaceConfigurationProperty"]]:
        '''The configuration settings for a router network interface.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routernetworkinterface.html#cfn-mediaconnect-routernetworkinterface-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterNetworkInterfacePropsMixin.RouterNetworkInterfaceConfigurationProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the router network interface.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routernetworkinterface.html#cfn-mediaconnect-routernetworkinterface-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region_name(self) -> typing.Optional[builtins.str]:
        '''The AWS Region where the router network interface is located.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routernetworkinterface.html#cfn-mediaconnect-routernetworkinterface-regionname
        '''
        result = self._values.get("region_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Key-value pairs that can be used to tag and organize this router network interface.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routernetworkinterface.html#cfn-mediaconnect-routernetworkinterface-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRouterNetworkInterfaceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRouterNetworkInterfacePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterNetworkInterfacePropsMixin",
):
    '''Represents a router network interface in AWS Elemental MediaConnect that is used to define a network boundary for router resources.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routernetworkinterface.html
    :cloudformationResource: AWS::MediaConnect::RouterNetworkInterface
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
        
        cfn_router_network_interface_props_mixin = mediaconnect_mixins.CfnRouterNetworkInterfacePropsMixin(mediaconnect_mixins.CfnRouterNetworkInterfaceMixinProps(
            configuration=mediaconnect_mixins.CfnRouterNetworkInterfacePropsMixin.RouterNetworkInterfaceConfigurationProperty(
                public=mediaconnect_mixins.CfnRouterNetworkInterfacePropsMixin.PublicRouterNetworkInterfaceConfigurationProperty(
                    allow_rules=[mediaconnect_mixins.CfnRouterNetworkInterfacePropsMixin.PublicRouterNetworkInterfaceRuleProperty(
                        cidr="cidr"
                    )]
                ),
                vpc=mediaconnect_mixins.CfnRouterNetworkInterfacePropsMixin.VpcRouterNetworkInterfaceConfigurationProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_id="subnetId"
                )
            ),
            name="name",
            region_name="regionName",
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
        props: typing.Union[CfnRouterNetworkInterfaceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaConnect::RouterNetworkInterface``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30887a5eb0c3d9ca7f13caa6a612c5690fc59edfb738f8ab74e2a91fa3063059)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a81bca871ef62b375de8d053657a543ae65b87328946e494ae875cc72dbe7e9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc250bc7033248927edd23cd254457312b25c892725f0ac40f9e968248831192)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRouterNetworkInterfaceMixinProps:
        return typing.cast(CfnRouterNetworkInterfaceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterNetworkInterfacePropsMixin.PublicRouterNetworkInterfaceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"allow_rules": "allowRules"},
    )
    class PublicRouterNetworkInterfaceConfigurationProperty:
        def __init__(
            self,
            *,
            allow_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterNetworkInterfacePropsMixin.PublicRouterNetworkInterfaceRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The configuration settings for a public router network interface, including the list of allowed CIDR blocks.

            :param allow_rules: The list of allowed CIDR blocks for the public router network interface.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routernetworkinterface-publicrouternetworkinterfaceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                public_router_network_interface_configuration_property = mediaconnect_mixins.CfnRouterNetworkInterfacePropsMixin.PublicRouterNetworkInterfaceConfigurationProperty(
                    allow_rules=[mediaconnect_mixins.CfnRouterNetworkInterfacePropsMixin.PublicRouterNetworkInterfaceRuleProperty(
                        cidr="cidr"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__311b3f15b46a0b433fe458c9e7907266474ecebc22bfcf323e5773b0f2f36fa4)
                check_type(argname="argument allow_rules", value=allow_rules, expected_type=type_hints["allow_rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allow_rules is not None:
                self._values["allow_rules"] = allow_rules

        @builtins.property
        def allow_rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterNetworkInterfacePropsMixin.PublicRouterNetworkInterfaceRuleProperty"]]]]:
            '''The list of allowed CIDR blocks for the public router network interface.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routernetworkinterface-publicrouternetworkinterfaceconfiguration.html#cfn-mediaconnect-routernetworkinterface-publicrouternetworkinterfaceconfiguration-allowrules
            '''
            result = self._values.get("allow_rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterNetworkInterfacePropsMixin.PublicRouterNetworkInterfaceRuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PublicRouterNetworkInterfaceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterNetworkInterfacePropsMixin.PublicRouterNetworkInterfaceRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"cidr": "cidr"},
    )
    class PublicRouterNetworkInterfaceRuleProperty:
        def __init__(self, *, cidr: typing.Optional[builtins.str] = None) -> None:
            '''A rule that allows a specific CIDR block to access the public router network interface.

            :param cidr: The CIDR block that is allowed to access the public router network interface.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routernetworkinterface-publicrouternetworkinterfacerule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                public_router_network_interface_rule_property = mediaconnect_mixins.CfnRouterNetworkInterfacePropsMixin.PublicRouterNetworkInterfaceRuleProperty(
                    cidr="cidr"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a613937fcd796f6a32fd46403cbe4fc26ad2b2d78fd337aeeb91c231fe7cc47)
                check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cidr is not None:
                self._values["cidr"] = cidr

        @builtins.property
        def cidr(self) -> typing.Optional[builtins.str]:
            '''The CIDR block that is allowed to access the public router network interface.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routernetworkinterface-publicrouternetworkinterfacerule.html#cfn-mediaconnect-routernetworkinterface-publicrouternetworkinterfacerule-cidr
            '''
            result = self._values.get("cidr")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PublicRouterNetworkInterfaceRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterNetworkInterfacePropsMixin.RouterNetworkInterfaceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"public": "public", "vpc": "vpc"},
    )
    class RouterNetworkInterfaceConfigurationProperty:
        def __init__(
            self,
            *,
            public: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterNetworkInterfacePropsMixin.PublicRouterNetworkInterfaceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            vpc: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterNetworkInterfacePropsMixin.VpcRouterNetworkInterfaceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param public: The configuration settings for a public router network interface, including the list of allowed CIDR blocks.
            :param vpc: The configuration settings for a router network interface within a VPC, including the security group IDs and subnet ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routernetworkinterface-routernetworkinterfaceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                router_network_interface_configuration_property = mediaconnect_mixins.CfnRouterNetworkInterfacePropsMixin.RouterNetworkInterfaceConfigurationProperty(
                    public=mediaconnect_mixins.CfnRouterNetworkInterfacePropsMixin.PublicRouterNetworkInterfaceConfigurationProperty(
                        allow_rules=[mediaconnect_mixins.CfnRouterNetworkInterfacePropsMixin.PublicRouterNetworkInterfaceRuleProperty(
                            cidr="cidr"
                        )]
                    ),
                    vpc=mediaconnect_mixins.CfnRouterNetworkInterfacePropsMixin.VpcRouterNetworkInterfaceConfigurationProperty(
                        security_group_ids=["securityGroupIds"],
                        subnet_id="subnetId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0aced7b56a0b3eff6075026d489b031bd5da947ca3e84eee141aa9f6e09a65d9)
                check_type(argname="argument public", value=public, expected_type=type_hints["public"])
                check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if public is not None:
                self._values["public"] = public
            if vpc is not None:
                self._values["vpc"] = vpc

        @builtins.property
        def public(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterNetworkInterfacePropsMixin.PublicRouterNetworkInterfaceConfigurationProperty"]]:
            '''The configuration settings for a public router network interface, including the list of allowed CIDR blocks.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routernetworkinterface-routernetworkinterfaceconfiguration.html#cfn-mediaconnect-routernetworkinterface-routernetworkinterfaceconfiguration-public
            '''
            result = self._values.get("public")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterNetworkInterfacePropsMixin.PublicRouterNetworkInterfaceConfigurationProperty"]], result)

        @builtins.property
        def vpc(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterNetworkInterfacePropsMixin.VpcRouterNetworkInterfaceConfigurationProperty"]]:
            '''The configuration settings for a router network interface within a VPC, including the security group IDs and subnet ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routernetworkinterface-routernetworkinterfaceconfiguration.html#cfn-mediaconnect-routernetworkinterface-routernetworkinterfaceconfiguration-vpc
            '''
            result = self._values.get("vpc")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterNetworkInterfacePropsMixin.VpcRouterNetworkInterfaceConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RouterNetworkInterfaceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterNetworkInterfacePropsMixin.VpcRouterNetworkInterfaceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_id": "subnetId",
        },
    )
    class VpcRouterNetworkInterfaceConfigurationProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration settings for a router network interface within a VPC, including the security group IDs and subnet ID.

            :param security_group_ids: The IDs of the security groups to associate with the router network interface within the VPC.
            :param subnet_id: The ID of the subnet within the VPC to associate the router network interface with.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routernetworkinterface-vpcrouternetworkinterfaceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                vpc_router_network_interface_configuration_property = mediaconnect_mixins.CfnRouterNetworkInterfacePropsMixin.VpcRouterNetworkInterfaceConfigurationProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_id="subnetId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e3aa4fbd1e12e857144f42cb69810d0cfb60370fced55d27887e2f75511ffbb6)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_id is not None:
                self._values["subnet_id"] = subnet_id

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The IDs of the security groups to associate with the router network interface within the VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routernetworkinterface-vpcrouternetworkinterfaceconfiguration.html#cfn-mediaconnect-routernetworkinterface-vpcrouternetworkinterfaceconfiguration-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the subnet within the VPC to associate the router network interface with.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routernetworkinterface-vpcrouternetworkinterfaceconfiguration.html#cfn-mediaconnect-routernetworkinterface-vpcrouternetworkinterfaceconfiguration-subnetid
            '''
            result = self._values.get("subnet_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcRouterNetworkInterfaceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterOutputMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zone": "availabilityZone",
        "configuration": "configuration",
        "maintenance_configuration": "maintenanceConfiguration",
        "maximum_bitrate": "maximumBitrate",
        "name": "name",
        "region_name": "regionName",
        "routing_scope": "routingScope",
        "tags": "tags",
        "tier": "tier",
    },
)
class CfnRouterOutputMixinProps:
    def __init__(
        self,
        *,
        availability_zone: typing.Optional[builtins.str] = None,
        configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterOutputPropsMixin.RouterOutputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        maintenance_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterOutputPropsMixin.MaintenanceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        maximum_bitrate: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        region_name: typing.Optional[builtins.str] = None,
        routing_scope: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        tier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnRouterOutputPropsMixin.

        :param availability_zone: The Availability Zone of the router output.
        :param configuration: The configuration settings for a router output.
        :param maintenance_configuration: The maintenance configuration settings applied to this router output.
        :param maximum_bitrate: The maximum bitrate for the router output.
        :param name: The name of the router output.
        :param region_name: The AWS Region where the router output is located.
        :param routing_scope: Indicates whether the router output is configured for Regional or global routing.
        :param tags: Key-value pairs that can be used to tag and organize this router output.
        :param tier: The tier level of the router output.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routeroutput.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
            
            # automatic: Any
            # default_: Any
            
            cfn_router_output_mixin_props = mediaconnect_mixins.CfnRouterOutputMixinProps(
                availability_zone="availabilityZone",
                configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.RouterOutputConfigurationProperty(
                    media_connect_flow=mediaconnect_mixins.CfnRouterOutputPropsMixin.MediaConnectFlowRouterOutputConfigurationProperty(
                        destination_transit_encryption=mediaconnect_mixins.CfnRouterOutputPropsMixin.FlowTransitEncryptionProperty(
                            encryption_key_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty(
                                automatic=automatic,
                                secrets_manager=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                    role_arn="roleArn",
                                    secret_arn="secretArn"
                                )
                            ),
                            encryption_key_type="encryptionKeyType"
                        ),
                        flow_arn="flowArn",
                        flow_source_arn="flowSourceArn"
                    ),
                    media_live_input=mediaconnect_mixins.CfnRouterOutputPropsMixin.MediaLiveInputRouterOutputConfigurationProperty(
                        destination_transit_encryption=mediaconnect_mixins.CfnRouterOutputPropsMixin.MediaLiveTransitEncryptionProperty(
                            encryption_key_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.MediaLiveTransitEncryptionKeyConfigurationProperty(
                                automatic=automatic,
                                secrets_manager=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                    role_arn="roleArn",
                                    secret_arn="secretArn"
                                )
                            ),
                            encryption_key_type="encryptionKeyType"
                        ),
                        media_live_input_arn="mediaLiveInputArn",
                        media_live_pipeline_id="mediaLivePipelineId"
                    ),
                    standard=mediaconnect_mixins.CfnRouterOutputPropsMixin.StandardRouterOutputConfigurationProperty(
                        network_interface_arn="networkInterfaceArn",
                        protocol="protocol",
                        protocol_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.RouterOutputProtocolConfigurationProperty(
                            rist=mediaconnect_mixins.CfnRouterOutputPropsMixin.RistRouterOutputConfigurationProperty(
                                destination_address="destinationAddress",
                                destination_port=123
                            ),
                            rtp=mediaconnect_mixins.CfnRouterOutputPropsMixin.RtpRouterOutputConfigurationProperty(
                                destination_address="destinationAddress",
                                destination_port=123,
                                forward_error_correction="forwardErrorCorrection"
                            ),
                            srt_caller=mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtCallerRouterOutputConfigurationProperty(
                                destination_address="destinationAddress",
                                destination_port=123,
                                encryption_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtEncryptionConfigurationProperty(
                                    encryption_key=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                        role_arn="roleArn",
                                        secret_arn="secretArn"
                                    )
                                ),
                                minimum_latency_milliseconds=123,
                                stream_id="streamId"
                            ),
                            srt_listener=mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtListenerRouterOutputConfigurationProperty(
                                encryption_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtEncryptionConfigurationProperty(
                                    encryption_key=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                        role_arn="roleArn",
                                        secret_arn="secretArn"
                                    )
                                ),
                                minimum_latency_milliseconds=123,
                                port=123
                            )
                        )
                    )
                ),
                maintenance_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.MaintenanceConfigurationProperty(
                    default=default_,
                    preferred_day_time=mediaconnect_mixins.CfnRouterOutputPropsMixin.PreferredDayTimeMaintenanceConfigurationProperty(
                        day="day",
                        time="time"
                    )
                ),
                maximum_bitrate=123,
                name="name",
                region_name="regionName",
                routing_scope="routingScope",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                tier="tier"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__183c1f0f197c6e69663b4dbdc2e99d8c1a196b3a9b86c8d8f3a185e97a35bb3f)
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument maintenance_configuration", value=maintenance_configuration, expected_type=type_hints["maintenance_configuration"])
            check_type(argname="argument maximum_bitrate", value=maximum_bitrate, expected_type=type_hints["maximum_bitrate"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region_name", value=region_name, expected_type=type_hints["region_name"])
            check_type(argname="argument routing_scope", value=routing_scope, expected_type=type_hints["routing_scope"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if configuration is not None:
            self._values["configuration"] = configuration
        if maintenance_configuration is not None:
            self._values["maintenance_configuration"] = maintenance_configuration
        if maximum_bitrate is not None:
            self._values["maximum_bitrate"] = maximum_bitrate
        if name is not None:
            self._values["name"] = name
        if region_name is not None:
            self._values["region_name"] = region_name
        if routing_scope is not None:
            self._values["routing_scope"] = routing_scope
        if tags is not None:
            self._values["tags"] = tags
        if tier is not None:
            self._values["tier"] = tier

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''The Availability Zone of the router output.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routeroutput.html#cfn-mediaconnect-routeroutput-availabilityzone
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.RouterOutputConfigurationProperty"]]:
        '''The configuration settings for a router output.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routeroutput.html#cfn-mediaconnect-routeroutput-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.RouterOutputConfigurationProperty"]], result)

    @builtins.property
    def maintenance_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.MaintenanceConfigurationProperty"]]:
        '''The maintenance configuration settings applied to this router output.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routeroutput.html#cfn-mediaconnect-routeroutput-maintenanceconfiguration
        '''
        result = self._values.get("maintenance_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.MaintenanceConfigurationProperty"]], result)

    @builtins.property
    def maximum_bitrate(self) -> typing.Optional[jsii.Number]:
        '''The maximum bitrate for the router output.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routeroutput.html#cfn-mediaconnect-routeroutput-maximumbitrate
        '''
        result = self._values.get("maximum_bitrate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the router output.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routeroutput.html#cfn-mediaconnect-routeroutput-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region_name(self) -> typing.Optional[builtins.str]:
        '''The AWS Region where the router output is located.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routeroutput.html#cfn-mediaconnect-routeroutput-regionname
        '''
        result = self._values.get("region_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_scope(self) -> typing.Optional[builtins.str]:
        '''Indicates whether the router output is configured for Regional or global routing.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routeroutput.html#cfn-mediaconnect-routeroutput-routingscope
        '''
        result = self._values.get("routing_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Key-value pairs that can be used to tag and organize this router output.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routeroutput.html#cfn-mediaconnect-routeroutput-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def tier(self) -> typing.Optional[builtins.str]:
        '''The tier level of the router output.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routeroutput.html#cfn-mediaconnect-routeroutput-tier
        '''
        result = self._values.get("tier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRouterOutputMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRouterOutputPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterOutputPropsMixin",
):
    '''Represents a router input in AWS Elemental MediaConnect that can be used to egress content transmitted from router inputs.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-routeroutput.html
    :cloudformationResource: AWS::MediaConnect::RouterOutput
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
        
        # automatic: Any
        # default_: Any
        
        cfn_router_output_props_mixin = mediaconnect_mixins.CfnRouterOutputPropsMixin(mediaconnect_mixins.CfnRouterOutputMixinProps(
            availability_zone="availabilityZone",
            configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.RouterOutputConfigurationProperty(
                media_connect_flow=mediaconnect_mixins.CfnRouterOutputPropsMixin.MediaConnectFlowRouterOutputConfigurationProperty(
                    destination_transit_encryption=mediaconnect_mixins.CfnRouterOutputPropsMixin.FlowTransitEncryptionProperty(
                        encryption_key_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty(
                            automatic=automatic,
                            secrets_manager=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                role_arn="roleArn",
                                secret_arn="secretArn"
                            )
                        ),
                        encryption_key_type="encryptionKeyType"
                    ),
                    flow_arn="flowArn",
                    flow_source_arn="flowSourceArn"
                ),
                media_live_input=mediaconnect_mixins.CfnRouterOutputPropsMixin.MediaLiveInputRouterOutputConfigurationProperty(
                    destination_transit_encryption=mediaconnect_mixins.CfnRouterOutputPropsMixin.MediaLiveTransitEncryptionProperty(
                        encryption_key_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.MediaLiveTransitEncryptionKeyConfigurationProperty(
                            automatic=automatic,
                            secrets_manager=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                role_arn="roleArn",
                                secret_arn="secretArn"
                            )
                        ),
                        encryption_key_type="encryptionKeyType"
                    ),
                    media_live_input_arn="mediaLiveInputArn",
                    media_live_pipeline_id="mediaLivePipelineId"
                ),
                standard=mediaconnect_mixins.CfnRouterOutputPropsMixin.StandardRouterOutputConfigurationProperty(
                    network_interface_arn="networkInterfaceArn",
                    protocol="protocol",
                    protocol_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.RouterOutputProtocolConfigurationProperty(
                        rist=mediaconnect_mixins.CfnRouterOutputPropsMixin.RistRouterOutputConfigurationProperty(
                            destination_address="destinationAddress",
                            destination_port=123
                        ),
                        rtp=mediaconnect_mixins.CfnRouterOutputPropsMixin.RtpRouterOutputConfigurationProperty(
                            destination_address="destinationAddress",
                            destination_port=123,
                            forward_error_correction="forwardErrorCorrection"
                        ),
                        srt_caller=mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtCallerRouterOutputConfigurationProperty(
                            destination_address="destinationAddress",
                            destination_port=123,
                            encryption_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtEncryptionConfigurationProperty(
                                encryption_key=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                    role_arn="roleArn",
                                    secret_arn="secretArn"
                                )
                            ),
                            minimum_latency_milliseconds=123,
                            stream_id="streamId"
                        ),
                        srt_listener=mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtListenerRouterOutputConfigurationProperty(
                            encryption_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtEncryptionConfigurationProperty(
                                encryption_key=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                    role_arn="roleArn",
                                    secret_arn="secretArn"
                                )
                            ),
                            minimum_latency_milliseconds=123,
                            port=123
                        )
                    )
                )
            ),
            maintenance_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.MaintenanceConfigurationProperty(
                default=default_,
                preferred_day_time=mediaconnect_mixins.CfnRouterOutputPropsMixin.PreferredDayTimeMaintenanceConfigurationProperty(
                    day="day",
                    time="time"
                )
            ),
            maximum_bitrate=123,
            name="name",
            region_name="regionName",
            routing_scope="routingScope",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            tier="tier"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRouterOutputMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaConnect::RouterOutput``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb5be3075dfd57707fb1888d30b9bf64010adc44db27e40e24121cad6fde9454)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d048736b8bc4d4b47a772ee0574ab835ea28d61914d29469863cc7125f13b152)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d3b54b0b2047bd171e89de5e48343f7fa2b9dcbfffc426b1e3d47ccadbb0168)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRouterOutputMixinProps:
        return typing.cast(CfnRouterOutputMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterOutputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"automatic": "automatic", "secrets_manager": "secretsManager"},
    )
    class FlowTransitEncryptionKeyConfigurationProperty:
        def __init__(
            self,
            *,
            automatic: typing.Any = None,
            secrets_manager: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param automatic: Configuration settings for automatic encryption key management, where MediaConnect handles key creation and rotation.
            :param secrets_manager: The configuration settings for transit encryption using AWS Secrets Manager, including the secret ARN and role ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-flowtransitencryptionkeyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                # automatic: Any
                
                flow_transit_encryption_key_configuration_property = mediaconnect_mixins.CfnRouterOutputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty(
                    automatic=automatic,
                    secrets_manager=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                        role_arn="roleArn",
                        secret_arn="secretArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b0bbe24909bd774bf845263d2000da00e7ff2151f710ad1a341c79b03e67bf27)
                check_type(argname="argument automatic", value=automatic, expected_type=type_hints["automatic"])
                check_type(argname="argument secrets_manager", value=secrets_manager, expected_type=type_hints["secrets_manager"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if automatic is not None:
                self._values["automatic"] = automatic
            if secrets_manager is not None:
                self._values["secrets_manager"] = secrets_manager

        @builtins.property
        def automatic(self) -> typing.Any:
            '''Configuration settings for automatic encryption key management, where MediaConnect handles key creation and rotation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-flowtransitencryptionkeyconfiguration.html#cfn-mediaconnect-routeroutput-flowtransitencryptionkeyconfiguration-automatic
            '''
            result = self._values.get("automatic")
            return typing.cast(typing.Any, result)

        @builtins.property
        def secrets_manager(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty"]]:
            '''The configuration settings for transit encryption using AWS Secrets Manager, including the secret ARN and role ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-flowtransitencryptionkeyconfiguration.html#cfn-mediaconnect-routeroutput-flowtransitencryptionkeyconfiguration-secretsmanager
            '''
            result = self._values.get("secrets_manager")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FlowTransitEncryptionKeyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterOutputPropsMixin.FlowTransitEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption_key_configuration": "encryptionKeyConfiguration",
            "encryption_key_type": "encryptionKeyType",
        },
    )
    class FlowTransitEncryptionProperty:
        def __init__(
            self,
            *,
            encryption_key_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterOutputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            encryption_key_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration that defines how content is encrypted during transit between the MediaConnect router and a MediaConnect flow.

            :param encryption_key_configuration: Configuration settings for flow transit encryption keys.
            :param encryption_key_type: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-flowtransitencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                # automatic: Any
                
                flow_transit_encryption_property = mediaconnect_mixins.CfnRouterOutputPropsMixin.FlowTransitEncryptionProperty(
                    encryption_key_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty(
                        automatic=automatic,
                        secrets_manager=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                            role_arn="roleArn",
                            secret_arn="secretArn"
                        )
                    ),
                    encryption_key_type="encryptionKeyType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dba0e156fc31334bad65555e7294b93d94406f43161205183a1faafbc13feab0)
                check_type(argname="argument encryption_key_configuration", value=encryption_key_configuration, expected_type=type_hints["encryption_key_configuration"])
                check_type(argname="argument encryption_key_type", value=encryption_key_type, expected_type=type_hints["encryption_key_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_key_configuration is not None:
                self._values["encryption_key_configuration"] = encryption_key_configuration
            if encryption_key_type is not None:
                self._values["encryption_key_type"] = encryption_key_type

        @builtins.property
        def encryption_key_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty"]]:
            '''Configuration settings for flow transit encryption keys.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-flowtransitencryption.html#cfn-mediaconnect-routeroutput-flowtransitencryption-encryptionkeyconfiguration
            '''
            result = self._values.get("encryption_key_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty"]], result)

        @builtins.property
        def encryption_key_type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-flowtransitencryption.html#cfn-mediaconnect-routeroutput-flowtransitencryption-encryptionkeytype
            '''
            result = self._values.get("encryption_key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FlowTransitEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterOutputPropsMixin.MaintenanceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"default": "default", "preferred_day_time": "preferredDayTime"},
    )
    class MaintenanceConfigurationProperty:
        def __init__(
            self,
            *,
            default: typing.Any = None,
            preferred_day_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterOutputPropsMixin.PreferredDayTimeMaintenanceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param default: Configuration settings for default maintenance scheduling.
            :param preferred_day_time: Configuration for preferred day and time maintenance settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-maintenanceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                # default_: Any
                
                maintenance_configuration_property = mediaconnect_mixins.CfnRouterOutputPropsMixin.MaintenanceConfigurationProperty(
                    default=default_,
                    preferred_day_time=mediaconnect_mixins.CfnRouterOutputPropsMixin.PreferredDayTimeMaintenanceConfigurationProperty(
                        day="day",
                        time="time"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3903eaf25292c4ea3f26c9b7a24f60852dc94688a8ce147aac56d8fc83267589)
                check_type(argname="argument default", value=default, expected_type=type_hints["default"])
                check_type(argname="argument preferred_day_time", value=preferred_day_time, expected_type=type_hints["preferred_day_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default is not None:
                self._values["default"] = default
            if preferred_day_time is not None:
                self._values["preferred_day_time"] = preferred_day_time

        @builtins.property
        def default(self) -> typing.Any:
            '''Configuration settings for default maintenance scheduling.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-maintenanceconfiguration.html#cfn-mediaconnect-routeroutput-maintenanceconfiguration-default
            '''
            result = self._values.get("default")
            return typing.cast(typing.Any, result)

        @builtins.property
        def preferred_day_time(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.PreferredDayTimeMaintenanceConfigurationProperty"]]:
            '''Configuration for preferred day and time maintenance settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-maintenanceconfiguration.html#cfn-mediaconnect-routeroutput-maintenanceconfiguration-preferreddaytime
            '''
            result = self._values.get("preferred_day_time")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.PreferredDayTimeMaintenanceConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaintenanceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterOutputPropsMixin.MediaConnectFlowRouterOutputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_transit_encryption": "destinationTransitEncryption",
            "flow_arn": "flowArn",
            "flow_source_arn": "flowSourceArn",
        },
    )
    class MediaConnectFlowRouterOutputConfigurationProperty:
        def __init__(
            self,
            *,
            destination_transit_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterOutputPropsMixin.FlowTransitEncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            flow_arn: typing.Optional[builtins.str] = None,
            flow_source_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration settings for connecting a router output to a MediaConnect flow source.

            :param destination_transit_encryption: The configuration that defines how content is encrypted during transit between the MediaConnect router and a MediaConnect flow.
            :param flow_arn: The ARN of the flow to connect to this router output.
            :param flow_source_arn: The ARN of the flow source to connect to this router output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-mediaconnectflowrouteroutputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                # automatic: Any
                
                media_connect_flow_router_output_configuration_property = mediaconnect_mixins.CfnRouterOutputPropsMixin.MediaConnectFlowRouterOutputConfigurationProperty(
                    destination_transit_encryption=mediaconnect_mixins.CfnRouterOutputPropsMixin.FlowTransitEncryptionProperty(
                        encryption_key_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty(
                            automatic=automatic,
                            secrets_manager=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                role_arn="roleArn",
                                secret_arn="secretArn"
                            )
                        ),
                        encryption_key_type="encryptionKeyType"
                    ),
                    flow_arn="flowArn",
                    flow_source_arn="flowSourceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7a20225f3dd5556099cc870106523c204943d1e202867339f51d0e2be8f0fe35)
                check_type(argname="argument destination_transit_encryption", value=destination_transit_encryption, expected_type=type_hints["destination_transit_encryption"])
                check_type(argname="argument flow_arn", value=flow_arn, expected_type=type_hints["flow_arn"])
                check_type(argname="argument flow_source_arn", value=flow_source_arn, expected_type=type_hints["flow_source_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_transit_encryption is not None:
                self._values["destination_transit_encryption"] = destination_transit_encryption
            if flow_arn is not None:
                self._values["flow_arn"] = flow_arn
            if flow_source_arn is not None:
                self._values["flow_source_arn"] = flow_source_arn

        @builtins.property
        def destination_transit_encryption(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.FlowTransitEncryptionProperty"]]:
            '''The configuration that defines how content is encrypted during transit between the MediaConnect router and a MediaConnect flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-mediaconnectflowrouteroutputconfiguration.html#cfn-mediaconnect-routeroutput-mediaconnectflowrouteroutputconfiguration-destinationtransitencryption
            '''
            result = self._values.get("destination_transit_encryption")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.FlowTransitEncryptionProperty"]], result)

        @builtins.property
        def flow_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the flow to connect to this router output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-mediaconnectflowrouteroutputconfiguration.html#cfn-mediaconnect-routeroutput-mediaconnectflowrouteroutputconfiguration-flowarn
            '''
            result = self._values.get("flow_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def flow_source_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the flow source to connect to this router output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-mediaconnectflowrouteroutputconfiguration.html#cfn-mediaconnect-routeroutput-mediaconnectflowrouteroutputconfiguration-flowsourcearn
            '''
            result = self._values.get("flow_source_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MediaConnectFlowRouterOutputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterOutputPropsMixin.MediaLiveInputRouterOutputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_transit_encryption": "destinationTransitEncryption",
            "media_live_input_arn": "mediaLiveInputArn",
            "media_live_pipeline_id": "mediaLivePipelineId",
        },
    )
    class MediaLiveInputRouterOutputConfigurationProperty:
        def __init__(
            self,
            *,
            destination_transit_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterOutputPropsMixin.MediaLiveTransitEncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            media_live_input_arn: typing.Optional[builtins.str] = None,
            media_live_pipeline_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration settings for connecting a router output to a MediaLive input.

            :param destination_transit_encryption: The encryption configuration that defines how content is encrypted during transit between MediaConnect Router and MediaLive. This configuration determines whether encryption keys are automatically managed by the service or manually managed through AWS Secrets Manager.
            :param media_live_input_arn: The ARN of the MediaLive input to connect to this router output.
            :param media_live_pipeline_id: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-medialiveinputrouteroutputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                # automatic: Any
                
                media_live_input_router_output_configuration_property = mediaconnect_mixins.CfnRouterOutputPropsMixin.MediaLiveInputRouterOutputConfigurationProperty(
                    destination_transit_encryption=mediaconnect_mixins.CfnRouterOutputPropsMixin.MediaLiveTransitEncryptionProperty(
                        encryption_key_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.MediaLiveTransitEncryptionKeyConfigurationProperty(
                            automatic=automatic,
                            secrets_manager=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                role_arn="roleArn",
                                secret_arn="secretArn"
                            )
                        ),
                        encryption_key_type="encryptionKeyType"
                    ),
                    media_live_input_arn="mediaLiveInputArn",
                    media_live_pipeline_id="mediaLivePipelineId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c7b35fd144b902d14e5f0be8a6c302f9f4817bf2e06cf6332d453137ae692e66)
                check_type(argname="argument destination_transit_encryption", value=destination_transit_encryption, expected_type=type_hints["destination_transit_encryption"])
                check_type(argname="argument media_live_input_arn", value=media_live_input_arn, expected_type=type_hints["media_live_input_arn"])
                check_type(argname="argument media_live_pipeline_id", value=media_live_pipeline_id, expected_type=type_hints["media_live_pipeline_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_transit_encryption is not None:
                self._values["destination_transit_encryption"] = destination_transit_encryption
            if media_live_input_arn is not None:
                self._values["media_live_input_arn"] = media_live_input_arn
            if media_live_pipeline_id is not None:
                self._values["media_live_pipeline_id"] = media_live_pipeline_id

        @builtins.property
        def destination_transit_encryption(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.MediaLiveTransitEncryptionProperty"]]:
            '''The encryption configuration that defines how content is encrypted during transit between MediaConnect Router and MediaLive.

            This configuration determines whether encryption keys are automatically managed by the service or manually managed through AWS Secrets Manager.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-medialiveinputrouteroutputconfiguration.html#cfn-mediaconnect-routeroutput-medialiveinputrouteroutputconfiguration-destinationtransitencryption
            '''
            result = self._values.get("destination_transit_encryption")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.MediaLiveTransitEncryptionProperty"]], result)

        @builtins.property
        def media_live_input_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the MediaLive input to connect to this router output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-medialiveinputrouteroutputconfiguration.html#cfn-mediaconnect-routeroutput-medialiveinputrouteroutputconfiguration-medialiveinputarn
            '''
            result = self._values.get("media_live_input_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def media_live_pipeline_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-medialiveinputrouteroutputconfiguration.html#cfn-mediaconnect-routeroutput-medialiveinputrouteroutputconfiguration-medialivepipelineid
            '''
            result = self._values.get("media_live_pipeline_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MediaLiveInputRouterOutputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterOutputPropsMixin.MediaLiveTransitEncryptionKeyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"automatic": "automatic", "secrets_manager": "secretsManager"},
    )
    class MediaLiveTransitEncryptionKeyConfigurationProperty:
        def __init__(
            self,
            *,
            automatic: typing.Any = None,
            secrets_manager: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param automatic: Configuration settings for automatic encryption key management, where MediaConnect handles key creation and rotation.
            :param secrets_manager: The configuration settings for transit encryption using AWS Secrets Manager, including the secret ARN and role ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-medialivetransitencryptionkeyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                # automatic: Any
                
                media_live_transit_encryption_key_configuration_property = mediaconnect_mixins.CfnRouterOutputPropsMixin.MediaLiveTransitEncryptionKeyConfigurationProperty(
                    automatic=automatic,
                    secrets_manager=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                        role_arn="roleArn",
                        secret_arn="secretArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__420ebff6c7bacd49f62aa10df98f25a2da5e70fdaee99feef606bca38ec1d1cd)
                check_type(argname="argument automatic", value=automatic, expected_type=type_hints["automatic"])
                check_type(argname="argument secrets_manager", value=secrets_manager, expected_type=type_hints["secrets_manager"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if automatic is not None:
                self._values["automatic"] = automatic
            if secrets_manager is not None:
                self._values["secrets_manager"] = secrets_manager

        @builtins.property
        def automatic(self) -> typing.Any:
            '''Configuration settings for automatic encryption key management, where MediaConnect handles key creation and rotation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-medialivetransitencryptionkeyconfiguration.html#cfn-mediaconnect-routeroutput-medialivetransitencryptionkeyconfiguration-automatic
            '''
            result = self._values.get("automatic")
            return typing.cast(typing.Any, result)

        @builtins.property
        def secrets_manager(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty"]]:
            '''The configuration settings for transit encryption using AWS Secrets Manager, including the secret ARN and role ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-medialivetransitencryptionkeyconfiguration.html#cfn-mediaconnect-routeroutput-medialivetransitencryptionkeyconfiguration-secretsmanager
            '''
            result = self._values.get("secrets_manager")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MediaLiveTransitEncryptionKeyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterOutputPropsMixin.MediaLiveTransitEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption_key_configuration": "encryptionKeyConfiguration",
            "encryption_key_type": "encryptionKeyType",
        },
    )
    class MediaLiveTransitEncryptionProperty:
        def __init__(
            self,
            *,
            encryption_key_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterOutputPropsMixin.MediaLiveTransitEncryptionKeyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            encryption_key_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The encryption configuration that defines how content is encrypted during transit between MediaConnect Router and MediaLive.

            This configuration determines whether encryption keys are automatically managed by the service or manually managed through AWS Secrets Manager.

            :param encryption_key_configuration: Configuration settings for the MediaLive transit encryption key.
            :param encryption_key_type: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-medialivetransitencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                # automatic: Any
                
                media_live_transit_encryption_property = mediaconnect_mixins.CfnRouterOutputPropsMixin.MediaLiveTransitEncryptionProperty(
                    encryption_key_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.MediaLiveTransitEncryptionKeyConfigurationProperty(
                        automatic=automatic,
                        secrets_manager=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                            role_arn="roleArn",
                            secret_arn="secretArn"
                        )
                    ),
                    encryption_key_type="encryptionKeyType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cd4edccab5ee92812f9a88720f98bd4fd5d96289659e075330632dd65aee422c)
                check_type(argname="argument encryption_key_configuration", value=encryption_key_configuration, expected_type=type_hints["encryption_key_configuration"])
                check_type(argname="argument encryption_key_type", value=encryption_key_type, expected_type=type_hints["encryption_key_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_key_configuration is not None:
                self._values["encryption_key_configuration"] = encryption_key_configuration
            if encryption_key_type is not None:
                self._values["encryption_key_type"] = encryption_key_type

        @builtins.property
        def encryption_key_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.MediaLiveTransitEncryptionKeyConfigurationProperty"]]:
            '''Configuration settings for the MediaLive transit encryption key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-medialivetransitencryption.html#cfn-mediaconnect-routeroutput-medialivetransitencryption-encryptionkeyconfiguration
            '''
            result = self._values.get("encryption_key_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.MediaLiveTransitEncryptionKeyConfigurationProperty"]], result)

        @builtins.property
        def encryption_key_type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-medialivetransitencryption.html#cfn-mediaconnect-routeroutput-medialivetransitencryption-encryptionkeytype
            '''
            result = self._values.get("encryption_key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MediaLiveTransitEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterOutputPropsMixin.PreferredDayTimeMaintenanceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"day": "day", "time": "time"},
    )
    class PreferredDayTimeMaintenanceConfigurationProperty:
        def __init__(
            self,
            *,
            day: typing.Optional[builtins.str] = None,
            time: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration for preferred day and time maintenance settings.

            :param day: 
            :param time: The preferred time for maintenance operations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-preferreddaytimemaintenanceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                preferred_day_time_maintenance_configuration_property = mediaconnect_mixins.CfnRouterOutputPropsMixin.PreferredDayTimeMaintenanceConfigurationProperty(
                    day="day",
                    time="time"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6cb9901bf03a9ae1eb69f58d17c005b70342f4136e1d6c1d97b742de7b317fad)
                check_type(argname="argument day", value=day, expected_type=type_hints["day"])
                check_type(argname="argument time", value=time, expected_type=type_hints["time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if day is not None:
                self._values["day"] = day
            if time is not None:
                self._values["time"] = time

        @builtins.property
        def day(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-preferreddaytimemaintenanceconfiguration.html#cfn-mediaconnect-routeroutput-preferreddaytimemaintenanceconfiguration-day
            '''
            result = self._values.get("day")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def time(self) -> typing.Optional[builtins.str]:
            '''The preferred time for maintenance operations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-preferreddaytimemaintenanceconfiguration.html#cfn-mediaconnect-routeroutput-preferreddaytimemaintenanceconfiguration-time
            '''
            result = self._values.get("time")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PreferredDayTimeMaintenanceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterOutputPropsMixin.RistRouterOutputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_address": "destinationAddress",
            "destination_port": "destinationPort",
        },
    )
    class RistRouterOutputConfigurationProperty:
        def __init__(
            self,
            *,
            destination_address: typing.Optional[builtins.str] = None,
            destination_port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The configuration settings for a router output using the RIST (Reliable Internet Stream Transport) protocol, including the destination address and port.

            :param destination_address: The destination IP address for the RIST protocol in the router output configuration.
            :param destination_port: The destination port number for the RIST protocol in the router output configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-ristrouteroutputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                rist_router_output_configuration_property = mediaconnect_mixins.CfnRouterOutputPropsMixin.RistRouterOutputConfigurationProperty(
                    destination_address="destinationAddress",
                    destination_port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4591fd3c202a89b95f3c295693ea2f2aa24ea02b10c91f226b91d13e6eb6c779)
                check_type(argname="argument destination_address", value=destination_address, expected_type=type_hints["destination_address"])
                check_type(argname="argument destination_port", value=destination_port, expected_type=type_hints["destination_port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_address is not None:
                self._values["destination_address"] = destination_address
            if destination_port is not None:
                self._values["destination_port"] = destination_port

        @builtins.property
        def destination_address(self) -> typing.Optional[builtins.str]:
            '''The destination IP address for the RIST protocol in the router output configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-ristrouteroutputconfiguration.html#cfn-mediaconnect-routeroutput-ristrouteroutputconfiguration-destinationaddress
            '''
            result = self._values.get("destination_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def destination_port(self) -> typing.Optional[jsii.Number]:
            '''The destination port number for the RIST protocol in the router output configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-ristrouteroutputconfiguration.html#cfn-mediaconnect-routeroutput-ristrouteroutputconfiguration-destinationport
            '''
            result = self._values.get("destination_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RistRouterOutputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterOutputPropsMixin.RouterOutputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "media_connect_flow": "mediaConnectFlow",
            "media_live_input": "mediaLiveInput",
            "standard": "standard",
        },
    )
    class RouterOutputConfigurationProperty:
        def __init__(
            self,
            *,
            media_connect_flow: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterOutputPropsMixin.MediaConnectFlowRouterOutputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            media_live_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterOutputPropsMixin.MediaLiveInputRouterOutputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            standard: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterOutputPropsMixin.StandardRouterOutputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param media_connect_flow: Configuration settings for connecting a router output to a MediaConnect flow source.
            :param media_live_input: Configuration settings for connecting a router output to a MediaLive input.
            :param standard: The configuration settings for a standard router output, including the protocol, protocol-specific configuration, network interface, and availability zone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-routeroutputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                # automatic: Any
                
                router_output_configuration_property = mediaconnect_mixins.CfnRouterOutputPropsMixin.RouterOutputConfigurationProperty(
                    media_connect_flow=mediaconnect_mixins.CfnRouterOutputPropsMixin.MediaConnectFlowRouterOutputConfigurationProperty(
                        destination_transit_encryption=mediaconnect_mixins.CfnRouterOutputPropsMixin.FlowTransitEncryptionProperty(
                            encryption_key_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty(
                                automatic=automatic,
                                secrets_manager=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                    role_arn="roleArn",
                                    secret_arn="secretArn"
                                )
                            ),
                            encryption_key_type="encryptionKeyType"
                        ),
                        flow_arn="flowArn",
                        flow_source_arn="flowSourceArn"
                    ),
                    media_live_input=mediaconnect_mixins.CfnRouterOutputPropsMixin.MediaLiveInputRouterOutputConfigurationProperty(
                        destination_transit_encryption=mediaconnect_mixins.CfnRouterOutputPropsMixin.MediaLiveTransitEncryptionProperty(
                            encryption_key_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.MediaLiveTransitEncryptionKeyConfigurationProperty(
                                automatic=automatic,
                                secrets_manager=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                    role_arn="roleArn",
                                    secret_arn="secretArn"
                                )
                            ),
                            encryption_key_type="encryptionKeyType"
                        ),
                        media_live_input_arn="mediaLiveInputArn",
                        media_live_pipeline_id="mediaLivePipelineId"
                    ),
                    standard=mediaconnect_mixins.CfnRouterOutputPropsMixin.StandardRouterOutputConfigurationProperty(
                        network_interface_arn="networkInterfaceArn",
                        protocol="protocol",
                        protocol_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.RouterOutputProtocolConfigurationProperty(
                            rist=mediaconnect_mixins.CfnRouterOutputPropsMixin.RistRouterOutputConfigurationProperty(
                                destination_address="destinationAddress",
                                destination_port=123
                            ),
                            rtp=mediaconnect_mixins.CfnRouterOutputPropsMixin.RtpRouterOutputConfigurationProperty(
                                destination_address="destinationAddress",
                                destination_port=123,
                                forward_error_correction="forwardErrorCorrection"
                            ),
                            srt_caller=mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtCallerRouterOutputConfigurationProperty(
                                destination_address="destinationAddress",
                                destination_port=123,
                                encryption_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtEncryptionConfigurationProperty(
                                    encryption_key=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                        role_arn="roleArn",
                                        secret_arn="secretArn"
                                    )
                                ),
                                minimum_latency_milliseconds=123,
                                stream_id="streamId"
                            ),
                            srt_listener=mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtListenerRouterOutputConfigurationProperty(
                                encryption_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtEncryptionConfigurationProperty(
                                    encryption_key=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                        role_arn="roleArn",
                                        secret_arn="secretArn"
                                    )
                                ),
                                minimum_latency_milliseconds=123,
                                port=123
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ddbdc4dc1fc39a4fd4c329952ea81941253b92c9d587c84e6ec9d64602ccce1f)
                check_type(argname="argument media_connect_flow", value=media_connect_flow, expected_type=type_hints["media_connect_flow"])
                check_type(argname="argument media_live_input", value=media_live_input, expected_type=type_hints["media_live_input"])
                check_type(argname="argument standard", value=standard, expected_type=type_hints["standard"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if media_connect_flow is not None:
                self._values["media_connect_flow"] = media_connect_flow
            if media_live_input is not None:
                self._values["media_live_input"] = media_live_input
            if standard is not None:
                self._values["standard"] = standard

        @builtins.property
        def media_connect_flow(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.MediaConnectFlowRouterOutputConfigurationProperty"]]:
            '''Configuration settings for connecting a router output to a MediaConnect flow source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-routeroutputconfiguration.html#cfn-mediaconnect-routeroutput-routeroutputconfiguration-mediaconnectflow
            '''
            result = self._values.get("media_connect_flow")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.MediaConnectFlowRouterOutputConfigurationProperty"]], result)

        @builtins.property
        def media_live_input(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.MediaLiveInputRouterOutputConfigurationProperty"]]:
            '''Configuration settings for connecting a router output to a MediaLive input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-routeroutputconfiguration.html#cfn-mediaconnect-routeroutput-routeroutputconfiguration-medialiveinput
            '''
            result = self._values.get("media_live_input")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.MediaLiveInputRouterOutputConfigurationProperty"]], result)

        @builtins.property
        def standard(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.StandardRouterOutputConfigurationProperty"]]:
            '''The configuration settings for a standard router output, including the protocol, protocol-specific configuration, network interface, and availability zone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-routeroutputconfiguration.html#cfn-mediaconnect-routeroutput-routeroutputconfiguration-standard
            '''
            result = self._values.get("standard")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.StandardRouterOutputConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RouterOutputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterOutputPropsMixin.RouterOutputProtocolConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "rist": "rist",
            "rtp": "rtp",
            "srt_caller": "srtCaller",
            "srt_listener": "srtListener",
        },
    )
    class RouterOutputProtocolConfigurationProperty:
        def __init__(
            self,
            *,
            rist: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterOutputPropsMixin.RistRouterOutputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rtp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterOutputPropsMixin.RtpRouterOutputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            srt_caller: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterOutputPropsMixin.SrtCallerRouterOutputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            srt_listener: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterOutputPropsMixin.SrtListenerRouterOutputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param rist: The configuration settings for a router output using the RIST (Reliable Internet Stream Transport) protocol, including the destination address and port.
            :param rtp: The configuration settings for a router output using the RTP (Real-Time Transport Protocol) protocol, including the destination address and port, and forward error correction state.
            :param srt_caller: The configuration settings for a router output using the SRT (Secure Reliable Transport) protocol in caller mode, including the destination address and port, minimum latency, stream ID, and encryption key configuration.
            :param srt_listener: The configuration settings for a router output using the SRT (Secure Reliable Transport) protocol in listener mode, including the port, minimum latency, and encryption key configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-routeroutputprotocolconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                router_output_protocol_configuration_property = mediaconnect_mixins.CfnRouterOutputPropsMixin.RouterOutputProtocolConfigurationProperty(
                    rist=mediaconnect_mixins.CfnRouterOutputPropsMixin.RistRouterOutputConfigurationProperty(
                        destination_address="destinationAddress",
                        destination_port=123
                    ),
                    rtp=mediaconnect_mixins.CfnRouterOutputPropsMixin.RtpRouterOutputConfigurationProperty(
                        destination_address="destinationAddress",
                        destination_port=123,
                        forward_error_correction="forwardErrorCorrection"
                    ),
                    srt_caller=mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtCallerRouterOutputConfigurationProperty(
                        destination_address="destinationAddress",
                        destination_port=123,
                        encryption_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtEncryptionConfigurationProperty(
                            encryption_key=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                role_arn="roleArn",
                                secret_arn="secretArn"
                            )
                        ),
                        minimum_latency_milliseconds=123,
                        stream_id="streamId"
                    ),
                    srt_listener=mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtListenerRouterOutputConfigurationProperty(
                        encryption_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtEncryptionConfigurationProperty(
                            encryption_key=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                role_arn="roleArn",
                                secret_arn="secretArn"
                            )
                        ),
                        minimum_latency_milliseconds=123,
                        port=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3a38a3f2af2dd44571fd5266f82ad0f2c33c4ca5039938727730b541cebdcfd8)
                check_type(argname="argument rist", value=rist, expected_type=type_hints["rist"])
                check_type(argname="argument rtp", value=rtp, expected_type=type_hints["rtp"])
                check_type(argname="argument srt_caller", value=srt_caller, expected_type=type_hints["srt_caller"])
                check_type(argname="argument srt_listener", value=srt_listener, expected_type=type_hints["srt_listener"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rist is not None:
                self._values["rist"] = rist
            if rtp is not None:
                self._values["rtp"] = rtp
            if srt_caller is not None:
                self._values["srt_caller"] = srt_caller
            if srt_listener is not None:
                self._values["srt_listener"] = srt_listener

        @builtins.property
        def rist(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.RistRouterOutputConfigurationProperty"]]:
            '''The configuration settings for a router output using the RIST (Reliable Internet Stream Transport) protocol, including the destination address and port.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-routeroutputprotocolconfiguration.html#cfn-mediaconnect-routeroutput-routeroutputprotocolconfiguration-rist
            '''
            result = self._values.get("rist")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.RistRouterOutputConfigurationProperty"]], result)

        @builtins.property
        def rtp(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.RtpRouterOutputConfigurationProperty"]]:
            '''The configuration settings for a router output using the RTP (Real-Time Transport Protocol) protocol, including the destination address and port, and forward error correction state.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-routeroutputprotocolconfiguration.html#cfn-mediaconnect-routeroutput-routeroutputprotocolconfiguration-rtp
            '''
            result = self._values.get("rtp")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.RtpRouterOutputConfigurationProperty"]], result)

        @builtins.property
        def srt_caller(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.SrtCallerRouterOutputConfigurationProperty"]]:
            '''The configuration settings for a router output using the SRT (Secure Reliable Transport) protocol in caller mode, including the destination address and port, minimum latency, stream ID, and encryption key configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-routeroutputprotocolconfiguration.html#cfn-mediaconnect-routeroutput-routeroutputprotocolconfiguration-srtcaller
            '''
            result = self._values.get("srt_caller")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.SrtCallerRouterOutputConfigurationProperty"]], result)

        @builtins.property
        def srt_listener(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.SrtListenerRouterOutputConfigurationProperty"]]:
            '''The configuration settings for a router output using the SRT (Secure Reliable Transport) protocol in listener mode, including the port, minimum latency, and encryption key configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-routeroutputprotocolconfiguration.html#cfn-mediaconnect-routeroutput-routeroutputprotocolconfiguration-srtlistener
            '''
            result = self._values.get("srt_listener")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.SrtListenerRouterOutputConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RouterOutputProtocolConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterOutputPropsMixin.RtpRouterOutputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_address": "destinationAddress",
            "destination_port": "destinationPort",
            "forward_error_correction": "forwardErrorCorrection",
        },
    )
    class RtpRouterOutputConfigurationProperty:
        def __init__(
            self,
            *,
            destination_address: typing.Optional[builtins.str] = None,
            destination_port: typing.Optional[jsii.Number] = None,
            forward_error_correction: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration settings for a router output using the RTP (Real-Time Transport Protocol) protocol, including the destination address and port, and forward error correction state.

            :param destination_address: The destination IP address for the RTP protocol in the router output configuration.
            :param destination_port: The destination port number for the RTP protocol in the router output configuration.
            :param forward_error_correction: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-rtprouteroutputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                rtp_router_output_configuration_property = mediaconnect_mixins.CfnRouterOutputPropsMixin.RtpRouterOutputConfigurationProperty(
                    destination_address="destinationAddress",
                    destination_port=123,
                    forward_error_correction="forwardErrorCorrection"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c9793208620557eea33c2d2ab727ef80c89a642fcd87f9d31858ee97de10eab3)
                check_type(argname="argument destination_address", value=destination_address, expected_type=type_hints["destination_address"])
                check_type(argname="argument destination_port", value=destination_port, expected_type=type_hints["destination_port"])
                check_type(argname="argument forward_error_correction", value=forward_error_correction, expected_type=type_hints["forward_error_correction"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_address is not None:
                self._values["destination_address"] = destination_address
            if destination_port is not None:
                self._values["destination_port"] = destination_port
            if forward_error_correction is not None:
                self._values["forward_error_correction"] = forward_error_correction

        @builtins.property
        def destination_address(self) -> typing.Optional[builtins.str]:
            '''The destination IP address for the RTP protocol in the router output configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-rtprouteroutputconfiguration.html#cfn-mediaconnect-routeroutput-rtprouteroutputconfiguration-destinationaddress
            '''
            result = self._values.get("destination_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def destination_port(self) -> typing.Optional[jsii.Number]:
            '''The destination port number for the RTP protocol in the router output configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-rtprouteroutputconfiguration.html#cfn-mediaconnect-routeroutput-rtprouteroutputconfiguration-destinationport
            '''
            result = self._values.get("destination_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def forward_error_correction(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-rtprouteroutputconfiguration.html#cfn-mediaconnect-routeroutput-rtprouteroutputconfiguration-forwarderrorcorrection
            '''
            result = self._values.get("forward_error_correction")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RtpRouterOutputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"role_arn": "roleArn", "secret_arn": "secretArn"},
    )
    class SecretsManagerEncryptionKeyConfigurationProperty:
        def __init__(
            self,
            *,
            role_arn: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration settings for transit encryption using AWS Secrets Manager, including the secret ARN and role ARN.

            :param role_arn: The ARN of the IAM role assumed by MediaConnect to access the AWS Secrets Manager secret.
            :param secret_arn: The ARN of the AWS Secrets Manager secret used for transit encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-secretsmanagerencryptionkeyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                secrets_manager_encryption_key_configuration_property = mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                    role_arn="roleArn",
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__453b4d7ebc2e99f313f1ab37fb3b2b9cc117cdad38b7c75b9eeca7039161f34f)
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM role assumed by MediaConnect to access the AWS Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-secretsmanagerencryptionkeyconfiguration.html#cfn-mediaconnect-routeroutput-secretsmanagerencryptionkeyconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the AWS Secrets Manager secret used for transit encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-secretsmanagerencryptionkeyconfiguration.html#cfn-mediaconnect-routeroutput-secretsmanagerencryptionkeyconfiguration-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecretsManagerEncryptionKeyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterOutputPropsMixin.SrtCallerRouterOutputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_address": "destinationAddress",
            "destination_port": "destinationPort",
            "encryption_configuration": "encryptionConfiguration",
            "minimum_latency_milliseconds": "minimumLatencyMilliseconds",
            "stream_id": "streamId",
        },
    )
    class SrtCallerRouterOutputConfigurationProperty:
        def __init__(
            self,
            *,
            destination_address: typing.Optional[builtins.str] = None,
            destination_port: typing.Optional[jsii.Number] = None,
            encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterOutputPropsMixin.SrtEncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            minimum_latency_milliseconds: typing.Optional[jsii.Number] = None,
            stream_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration settings for a router output using the SRT (Secure Reliable Transport) protocol in caller mode, including the destination address and port, minimum latency, stream ID, and encryption key configuration.

            :param destination_address: The destination IP address for the SRT protocol in caller mode.
            :param destination_port: The destination port number for the SRT protocol in caller mode.
            :param encryption_configuration: Contains the configuration settings for encrypting SRT streams, including the encryption key details and encryption parameters.
            :param minimum_latency_milliseconds: The minimum latency in milliseconds for the SRT protocol in caller mode.
            :param stream_id: The stream ID for the SRT protocol in caller mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-srtcallerrouteroutputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                srt_caller_router_output_configuration_property = mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtCallerRouterOutputConfigurationProperty(
                    destination_address="destinationAddress",
                    destination_port=123,
                    encryption_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtEncryptionConfigurationProperty(
                        encryption_key=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                            role_arn="roleArn",
                            secret_arn="secretArn"
                        )
                    ),
                    minimum_latency_milliseconds=123,
                    stream_id="streamId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d6afdedfc466fda44efd2466008654be03d6e6076fc74abaa840bd1ea4413c44)
                check_type(argname="argument destination_address", value=destination_address, expected_type=type_hints["destination_address"])
                check_type(argname="argument destination_port", value=destination_port, expected_type=type_hints["destination_port"])
                check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
                check_type(argname="argument minimum_latency_milliseconds", value=minimum_latency_milliseconds, expected_type=type_hints["minimum_latency_milliseconds"])
                check_type(argname="argument stream_id", value=stream_id, expected_type=type_hints["stream_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_address is not None:
                self._values["destination_address"] = destination_address
            if destination_port is not None:
                self._values["destination_port"] = destination_port
            if encryption_configuration is not None:
                self._values["encryption_configuration"] = encryption_configuration
            if minimum_latency_milliseconds is not None:
                self._values["minimum_latency_milliseconds"] = minimum_latency_milliseconds
            if stream_id is not None:
                self._values["stream_id"] = stream_id

        @builtins.property
        def destination_address(self) -> typing.Optional[builtins.str]:
            '''The destination IP address for the SRT protocol in caller mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-srtcallerrouteroutputconfiguration.html#cfn-mediaconnect-routeroutput-srtcallerrouteroutputconfiguration-destinationaddress
            '''
            result = self._values.get("destination_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def destination_port(self) -> typing.Optional[jsii.Number]:
            '''The destination port number for the SRT protocol in caller mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-srtcallerrouteroutputconfiguration.html#cfn-mediaconnect-routeroutput-srtcallerrouteroutputconfiguration-destinationport
            '''
            result = self._values.get("destination_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.SrtEncryptionConfigurationProperty"]]:
            '''Contains the configuration settings for encrypting SRT streams, including the encryption key details and encryption parameters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-srtcallerrouteroutputconfiguration.html#cfn-mediaconnect-routeroutput-srtcallerrouteroutputconfiguration-encryptionconfiguration
            '''
            result = self._values.get("encryption_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.SrtEncryptionConfigurationProperty"]], result)

        @builtins.property
        def minimum_latency_milliseconds(self) -> typing.Optional[jsii.Number]:
            '''The minimum latency in milliseconds for the SRT protocol in caller mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-srtcallerrouteroutputconfiguration.html#cfn-mediaconnect-routeroutput-srtcallerrouteroutputconfiguration-minimumlatencymilliseconds
            '''
            result = self._values.get("minimum_latency_milliseconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stream_id(self) -> typing.Optional[builtins.str]:
            '''The stream ID for the SRT protocol in caller mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-srtcallerrouteroutputconfiguration.html#cfn-mediaconnect-routeroutput-srtcallerrouteroutputconfiguration-streamid
            '''
            result = self._values.get("stream_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SrtCallerRouterOutputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterOutputPropsMixin.SrtEncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"encryption_key": "encryptionKey"},
    )
    class SrtEncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            encryption_key: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains the configuration settings for encrypting SRT streams, including the encryption key details and encryption parameters.

            :param encryption_key: The configuration settings for transit encryption using AWS Secrets Manager, including the secret ARN and role ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-srtencryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                srt_encryption_configuration_property = mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtEncryptionConfigurationProperty(
                    encryption_key=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                        role_arn="roleArn",
                        secret_arn="secretArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f9a249500d7cc096565af4c7a5a11491ab82a550814d202b21fb85fb5ca6a9d4)
                check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_key is not None:
                self._values["encryption_key"] = encryption_key

        @builtins.property
        def encryption_key(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty"]]:
            '''The configuration settings for transit encryption using AWS Secrets Manager, including the secret ARN and role ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-srtencryptionconfiguration.html#cfn-mediaconnect-routeroutput-srtencryptionconfiguration-encryptionkey
            '''
            result = self._values.get("encryption_key")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SrtEncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterOutputPropsMixin.SrtListenerRouterOutputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption_configuration": "encryptionConfiguration",
            "minimum_latency_milliseconds": "minimumLatencyMilliseconds",
            "port": "port",
        },
    )
    class SrtListenerRouterOutputConfigurationProperty:
        def __init__(
            self,
            *,
            encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterOutputPropsMixin.SrtEncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            minimum_latency_milliseconds: typing.Optional[jsii.Number] = None,
            port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The configuration settings for a router output using the SRT (Secure Reliable Transport) protocol in listener mode, including the port, minimum latency, and encryption key configuration.

            :param encryption_configuration: Contains the configuration settings for encrypting SRT streams, including the encryption key details and encryption parameters.
            :param minimum_latency_milliseconds: The minimum latency in milliseconds for the SRT protocol in listener mode.
            :param port: The port number for the SRT protocol in listener mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-srtlistenerrouteroutputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                srt_listener_router_output_configuration_property = mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtListenerRouterOutputConfigurationProperty(
                    encryption_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtEncryptionConfigurationProperty(
                        encryption_key=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                            role_arn="roleArn",
                            secret_arn="secretArn"
                        )
                    ),
                    minimum_latency_milliseconds=123,
                    port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__df472b706d66cb0aa39b07429a42ef72936a807f1b069b0ffc7e18afbad8759f)
                check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
                check_type(argname="argument minimum_latency_milliseconds", value=minimum_latency_milliseconds, expected_type=type_hints["minimum_latency_milliseconds"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_configuration is not None:
                self._values["encryption_configuration"] = encryption_configuration
            if minimum_latency_milliseconds is not None:
                self._values["minimum_latency_milliseconds"] = minimum_latency_milliseconds
            if port is not None:
                self._values["port"] = port

        @builtins.property
        def encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.SrtEncryptionConfigurationProperty"]]:
            '''Contains the configuration settings for encrypting SRT streams, including the encryption key details and encryption parameters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-srtlistenerrouteroutputconfiguration.html#cfn-mediaconnect-routeroutput-srtlistenerrouteroutputconfiguration-encryptionconfiguration
            '''
            result = self._values.get("encryption_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.SrtEncryptionConfigurationProperty"]], result)

        @builtins.property
        def minimum_latency_milliseconds(self) -> typing.Optional[jsii.Number]:
            '''The minimum latency in milliseconds for the SRT protocol in listener mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-srtlistenerrouteroutputconfiguration.html#cfn-mediaconnect-routeroutput-srtlistenerrouteroutputconfiguration-minimumlatencymilliseconds
            '''
            result = self._values.get("minimum_latency_milliseconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port number for the SRT protocol in listener mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-srtlistenerrouteroutputconfiguration.html#cfn-mediaconnect-routeroutput-srtlistenerrouteroutputconfiguration-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SrtListenerRouterOutputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediaconnect.mixins.CfnRouterOutputPropsMixin.StandardRouterOutputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "network_interface_arn": "networkInterfaceArn",
            "protocol": "protocol",
            "protocol_configuration": "protocolConfiguration",
        },
    )
    class StandardRouterOutputConfigurationProperty:
        def __init__(
            self,
            *,
            network_interface_arn: typing.Optional[builtins.str] = None,
            protocol: typing.Optional[builtins.str] = None,
            protocol_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRouterOutputPropsMixin.RouterOutputProtocolConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration settings for a standard router output, including the protocol, protocol-specific configuration, network interface, and availability zone.

            :param network_interface_arn: The Amazon Resource Name (ARN) of the network interface associated with the standard router output.
            :param protocol: 
            :param protocol_configuration: The protocol configuration settings for a router output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-standardrouteroutputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediaconnect import mixins as mediaconnect_mixins
                
                standard_router_output_configuration_property = mediaconnect_mixins.CfnRouterOutputPropsMixin.StandardRouterOutputConfigurationProperty(
                    network_interface_arn="networkInterfaceArn",
                    protocol="protocol",
                    protocol_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.RouterOutputProtocolConfigurationProperty(
                        rist=mediaconnect_mixins.CfnRouterOutputPropsMixin.RistRouterOutputConfigurationProperty(
                            destination_address="destinationAddress",
                            destination_port=123
                        ),
                        rtp=mediaconnect_mixins.CfnRouterOutputPropsMixin.RtpRouterOutputConfigurationProperty(
                            destination_address="destinationAddress",
                            destination_port=123,
                            forward_error_correction="forwardErrorCorrection"
                        ),
                        srt_caller=mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtCallerRouterOutputConfigurationProperty(
                            destination_address="destinationAddress",
                            destination_port=123,
                            encryption_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtEncryptionConfigurationProperty(
                                encryption_key=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                    role_arn="roleArn",
                                    secret_arn="secretArn"
                                )
                            ),
                            minimum_latency_milliseconds=123,
                            stream_id="streamId"
                        ),
                        srt_listener=mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtListenerRouterOutputConfigurationProperty(
                            encryption_configuration=mediaconnect_mixins.CfnRouterOutputPropsMixin.SrtEncryptionConfigurationProperty(
                                encryption_key=mediaconnect_mixins.CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty(
                                    role_arn="roleArn",
                                    secret_arn="secretArn"
                                )
                            ),
                            minimum_latency_milliseconds=123,
                            port=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a4b8b7e21c5c4f9da800d10ca740c9ab5e9dddfa2a897a0d80ce972f6ca0ce77)
                check_type(argname="argument network_interface_arn", value=network_interface_arn, expected_type=type_hints["network_interface_arn"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument protocol_configuration", value=protocol_configuration, expected_type=type_hints["protocol_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if network_interface_arn is not None:
                self._values["network_interface_arn"] = network_interface_arn
            if protocol is not None:
                self._values["protocol"] = protocol
            if protocol_configuration is not None:
                self._values["protocol_configuration"] = protocol_configuration

        @builtins.property
        def network_interface_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the network interface associated with the standard router output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-standardrouteroutputconfiguration.html#cfn-mediaconnect-routeroutput-standardrouteroutputconfiguration-networkinterfacearn
            '''
            result = self._values.get("network_interface_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-standardrouteroutputconfiguration.html#cfn-mediaconnect-routeroutput-standardrouteroutputconfiguration-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.RouterOutputProtocolConfigurationProperty"]]:
            '''The protocol configuration settings for a router output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-routeroutput-standardrouteroutputconfiguration.html#cfn-mediaconnect-routeroutput-standardrouteroutputconfiguration-protocolconfiguration
            '''
            result = self._values.get("protocol_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRouterOutputPropsMixin.RouterOutputProtocolConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StandardRouterOutputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnBridgeMixinProps",
    "CfnBridgeOutputMixinProps",
    "CfnBridgeOutputPropsMixin",
    "CfnBridgePropsMixin",
    "CfnBridgeSourceMixinProps",
    "CfnBridgeSourcePropsMixin",
    "CfnFlowEntitlementMixinProps",
    "CfnFlowEntitlementPropsMixin",
    "CfnFlowMixinProps",
    "CfnFlowOutputMixinProps",
    "CfnFlowOutputPropsMixin",
    "CfnFlowPropsMixin",
    "CfnFlowSourceMixinProps",
    "CfnFlowSourcePropsMixin",
    "CfnFlowVpcInterfaceMixinProps",
    "CfnFlowVpcInterfacePropsMixin",
    "CfnGatewayMixinProps",
    "CfnGatewayPropsMixin",
    "CfnRouterInputMixinProps",
    "CfnRouterInputPropsMixin",
    "CfnRouterNetworkInterfaceMixinProps",
    "CfnRouterNetworkInterfacePropsMixin",
    "CfnRouterOutputMixinProps",
    "CfnRouterOutputPropsMixin",
]

publication.publish()

def _typecheckingstub__16235aad5a3dc715d25f74a9ee546c2cee61d7c148a67bf46577cd68f8d8e2ee(
    *,
    egress_gateway_bridge: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBridgePropsMixin.EgressGatewayBridgeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ingress_gateway_bridge: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBridgePropsMixin.IngressGatewayBridgeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    outputs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBridgePropsMixin.BridgeOutputProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    placement_arn: typing.Optional[builtins.str] = None,
    source_failover_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBridgePropsMixin.FailoverConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBridgePropsMixin.BridgeSourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1f00e49541be4a9e9c08865479eae478cdeed7722d1effd432d19aab3499dea(
    *,
    bridge_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    network_output: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBridgeOutputPropsMixin.BridgeNetworkOutputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a721e49cb76d95643d4262194beedf7977b84ebef9887949680c8a634c0a7f7(
    props: typing.Union[CfnBridgeOutputMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c42c9a1c9d3e449b5489caa559bb67365f7e1d5ff53fd4657d4b2f21c64986e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd205f5493463b69b5b94023ccf3082048c668f368b60d3212cb0e11b5430ed(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa63255631e965eefa190d5926e7e719349b9960cb4cebb78f62f5c525f94e3b(
    *,
    ip_address: typing.Optional[builtins.str] = None,
    network_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0591ad5cf313775224ba6ac989be2665af5de2c7c4ca9fb4b862fa6d41c0577(
    props: typing.Union[CfnBridgeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63ca835689f352353b110ee9ca4f6f8d2b9864ecfc9c84b806f2dc65f9653e8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52e68203a62a9783236996d3e743e80f3151ebf2e520851b04640e417425f2e3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e5bcacdbb43d1a64ec051404e067731d52d2256212de47427277605e34477de(
    *,
    flow_arn: typing.Optional[builtins.str] = None,
    flow_vpc_interface_attachment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBridgePropsMixin.VpcInterfaceAttachmentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f61d2be7a0c0fabe6b1eb55303e8c8172616ecee577982cca652e6b4bd71041(
    *,
    ip_address: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    network_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eebae8e16046079e65f49519bc3902e42f299510c089e2d8c2238fe732e075d(
    *,
    multicast_ip: typing.Optional[builtins.str] = None,
    multicast_source_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBridgePropsMixin.MulticastSourceSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    network_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59edae2f14c29ff9f2455b0897ac22016bebd8d9e0d1c76154d67d9ae9f65ccf(
    *,
    network_output: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBridgePropsMixin.BridgeNetworkOutputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b5ced5741bc103b9e47e61c69294d6879943edbbeba334f20484be308322790(
    *,
    flow_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBridgePropsMixin.BridgeFlowSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    network_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBridgePropsMixin.BridgeNetworkSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c54fd43f8091c501e8cc5d608ae23501bd2c22a86779e3049e984112a5950b8e(
    *,
    max_bitrate: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__976dcf674111a58e5dd13d27128ee2c38e001a62c9b7ae97cb1ed1d8b3e5a6d4(
    *,
    failover_mode: typing.Optional[builtins.str] = None,
    source_priority: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBridgePropsMixin.SourcePriorityProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e068d58a11c9658979556b9e658b82e7cc74824fe30ec5369b296a12adc6462(
    *,
    max_bitrate: typing.Optional[jsii.Number] = None,
    max_outputs: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbd3cfab07a938574ffdfe775364b6e74e398109be8acfd8b687e3e016e40e21(
    *,
    multicast_source_ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1219af74cd443a6bc3a03399de38fc30c067588d3281ff408922ddb84be44a13(
    *,
    primary_source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10c34d4146e372d6cf73547f206350a34331d0a6f187e09f6934b631e6ab906e(
    *,
    vpc_interface_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5150595bc93e12d9ae9d50e101336258223d40e67a00f28fa99393fdeb67b52e(
    *,
    bridge_arn: typing.Optional[builtins.str] = None,
    flow_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBridgeSourcePropsMixin.BridgeFlowSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    network_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBridgeSourcePropsMixin.BridgeNetworkSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__747e38a3e74a2af31186e4171e1019c59ba0d4b43c5bfab2b7135d66da5f9380(
    props: typing.Union[CfnBridgeSourceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce680e0b4328f8b6ecf1fc7f5189d028b66127a97ed4e8c5a5226298ef4d553(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__957471fbda2e7254407b3b5480fc59442adf89a3855d1d346b6c9e83403b510e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f14d8fe763608e4eacdc26031627394bd4f77ffd7e13c55f34f90b5850e0edd8(
    *,
    flow_arn: typing.Optional[builtins.str] = None,
    flow_vpc_interface_attachment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBridgeSourcePropsMixin.VpcInterfaceAttachmentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc8622878bacbfb717b051b040e72f26744b8494520faf8edb1c8c2d7b874b3(
    *,
    multicast_ip: typing.Optional[builtins.str] = None,
    multicast_source_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBridgeSourcePropsMixin.MulticastSourceSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    network_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b259b2385678edfb6fd47abcd33ce7a59135b8d3277bd96a519d70906451ae4(
    *,
    multicast_source_ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c086e7a01e157d7bff676ad4661d47970aaaaef0fba3f7ee20606c60d243bbe3(
    *,
    vpc_interface_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c1d106b9fdf3937af314d7a040d02938af289d92367ccd67f0ef8fd49392287(
    *,
    data_transfer_subscriber_fee_percent: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowEntitlementPropsMixin.EncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    entitlement_status: typing.Optional[builtins.str] = None,
    flow_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    subscribers: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e8cf13e37d73b0520b47508cb4cf73a54a4ccffbd22d3cc2d9f8bac2f1215d0(
    props: typing.Union[CfnFlowEntitlementMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d217d988ec7825038c9f98e498f774e33a9a2c4fa05889ad24213906d972687a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac0e3f85f631380cdd4aafffa0932b0e71a0637d29e7facf6d46d98b45faf0d9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af5e8ff3e7351a544d74203bc709bbd87fe458302a6999bd56dc1fbccbb0f152(
    *,
    algorithm: typing.Optional[builtins.str] = None,
    constant_initialization_vector: typing.Optional[builtins.str] = None,
    device_id: typing.Optional[builtins.str] = None,
    key_type: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1ab6f643ff2ee011a1d639636ec8318de1c2af09010d6734a473ae8288bd2db(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    flow_size: typing.Optional[builtins.str] = None,
    maintenance: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.MaintenanceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    media_streams: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.MediaStreamProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    ndi_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.NdiConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.SourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_failover_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.FailoverConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_monitoring_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.SourceMonitoringConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_interfaces: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.VpcInterfaceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95adaf5540d02a8cdd782f2326950c0489c4bf372cfc5d2930a1313edf67854b(
    *,
    cidr_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    destination: typing.Optional[builtins.str] = None,
    encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowOutputPropsMixin.EncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    flow_arn: typing.Optional[builtins.str] = None,
    max_latency: typing.Optional[jsii.Number] = None,
    media_stream_output_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowOutputPropsMixin.MediaStreamOutputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    min_latency: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    ndi_program_name: typing.Optional[builtins.str] = None,
    ndi_speed_hq_quality: typing.Optional[jsii.Number] = None,
    output_status: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
    remote_id: typing.Optional[builtins.str] = None,
    router_integration_state: typing.Optional[builtins.str] = None,
    router_integration_transit_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowOutputPropsMixin.FlowTransitEncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    smoothing_latency: typing.Optional[jsii.Number] = None,
    stream_id: typing.Optional[builtins.str] = None,
    vpc_interface_attachment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowOutputPropsMixin.VpcInterfaceAttachmentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0d7ff33cdafdecaa6e84e984fb62b54c127ca01a284adfe2111df877b310b30(
    props: typing.Union[CfnFlowOutputMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e678320e27a19c95530bf123f5108c71c221f2b2a6b69ca7aa01931e6232327(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcd02657ae75bf8aec8547ed1f57a7d3e6e8a96295422a7d39ca187a4b189805(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c5ecfec787514d467ed2f974d0ca3e8bc4f38f5b52afb7110b9f539b97db457(
    *,
    destination_ip: typing.Optional[builtins.str] = None,
    destination_port: typing.Optional[jsii.Number] = None,
    interface: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowOutputPropsMixin.InterfaceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c4f63e002f285345aa32f3922e4babb2798e0c803ca36db6f84299752088a5(
    *,
    compression_factor: typing.Optional[jsii.Number] = None,
    encoder_profile: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a64610f76161f83342d54359dfa50ab33de6cc510f4e32d8a7858faa9b775e00(
    *,
    algorithm: typing.Optional[builtins.str] = None,
    key_type: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__581c68310c5af0bb94de31b54e3b8ebd0e377140830e1378b0b140087aabc5d2(
    *,
    automatic: typing.Any = None,
    secrets_manager: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b0905ce6aede6e9bd0e0ba79675d47f51b4aee97faf7007f7600ee4105555e5(
    *,
    encryption_key_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowOutputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    encryption_key_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b15b112f22d97a5cf7066d9024f76b0ec8619e5e297002f09e85214e14f565e(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e3941641a31f12837c0098a9543e75085bf8617cd9eb91eff32de22e4c200a3(
    *,
    destination_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowOutputPropsMixin.DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    encoding_name: typing.Optional[builtins.str] = None,
    encoding_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowOutputPropsMixin.EncodingParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    media_stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d689ea55f6c08a5fe58074200dbe15a9d972434ace7ae4bfe062297afa0ea316(
    *,
    role_arn: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ae9f703db286e45dd3a4a87db017c86e13ebf348a4bcefb57b62226f5638d39(
    *,
    vpc_interface_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d86ff46877b6db246da2216d1359eacd70fe8f4d9e06970e3f857a2a6179819(
    props: typing.Union[CfnFlowMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3383a8c98d19b0000ceb3d8d0a2d9a110f287f0159e2c660f266166295009b0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6214c9114ab03b1fbd443b1941f12699f56b8d143d8b158cc6121fea9a3b9f6f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__939912c55cebca624532ef6ae0d56749aff0b4a43f3f20f8b3aecc1c40fa0dff(
    *,
    silent_audio: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.SilentAudioProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f36aabebb546e089aeec719cd657f819e475f314e74bc1bab2444741cb5fa4(
    *,
    state: typing.Optional[builtins.str] = None,
    threshold_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cdd26afb60ff9ec880e8abfb3f3718b0bcc26b2c4c5c48221f4e2866d1f1e79(
    *,
    algorithm: typing.Optional[builtins.str] = None,
    constant_initialization_vector: typing.Optional[builtins.str] = None,
    device_id: typing.Optional[builtins.str] = None,
    key_type: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec9df09b6dbb20e5fc98548d6d9d2bd2206079c900fdf7c70979d946f2063f8e(
    *,
    failover_mode: typing.Optional[builtins.str] = None,
    recovery_window: typing.Optional[jsii.Number] = None,
    source_priority: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.SourcePriorityProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__327f0e2c2108be403014f890e8f10968b51c174bbb55e8964202669893c5a237(
    *,
    automatic: typing.Any = None,
    secrets_manager: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3830b919b567bff3c746ca727172dd267368d55f55f0c6cac003e727b2a08d3e(
    *,
    encryption_key_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.FlowTransitEncryptionKeyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    encryption_key_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa8e309b8dc68021f2bc931cecb80d94515ed80e368632d37267b47318dc200(
    *,
    channel_order: typing.Optional[builtins.str] = None,
    colorimetry: typing.Optional[builtins.str] = None,
    exact_framerate: typing.Optional[builtins.str] = None,
    par: typing.Optional[builtins.str] = None,
    range: typing.Optional[builtins.str] = None,
    scan_mode: typing.Optional[builtins.str] = None,
    tcs: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc3e4579ecbdb1bc7ce4e51b5562496b3a8804e9c8031bf3d70bdf5bb93351d2(
    *,
    state: typing.Optional[builtins.str] = None,
    threshold_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19263de2735b65eb3cfd8ff49f7595a7c7f2cf8dab4b4ebf506735f045929416(
    *,
    bridge_arn: typing.Optional[builtins.str] = None,
    vpc_interface_attachment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.VpcInterfaceAttachmentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6375d765d95cc088f509403c716e1f361c654ef283ca29e4c3d66e3d34be3d4(
    *,
    input_port: typing.Optional[jsii.Number] = None,
    interface: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.InterfaceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b430b25a0752bcb7b7be7051bd38f34306d67f346f5734e09bccb8a5a7eefbc8(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25f2f8d42857124c77915969a551723a3b8afd68be6183d3b1226e767dad3453(
    *,
    maintenance_day: typing.Optional[builtins.str] = None,
    maintenance_start_hour: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f15ae44a94333070725a83ca6b849b3c64b5426edef185adbac285538dd0447(
    *,
    fmtp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.FmtpProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    lang: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76b112275650765553cc150626b5bc455a8e730cd870c2b9eb76251d8fd2db19(
    *,
    attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.MediaStreamAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    clock_rate: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    fmt: typing.Optional[jsii.Number] = None,
    media_stream_id: typing.Optional[jsii.Number] = None,
    media_stream_name: typing.Optional[builtins.str] = None,
    media_stream_type: typing.Optional[builtins.str] = None,
    video_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5042eb2dafe9bc994ae8cce17d6e42b8f4f9dd72e7a18d9266b1e7f95a1a26fc(
    *,
    encoding_name: typing.Optional[builtins.str] = None,
    input_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.InputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    media_stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c75a4577adee00b175f16209d00f094abb6481d1532129d723d8ad643548591(
    *,
    machine_name: typing.Optional[builtins.str] = None,
    ndi_discovery_servers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.NdiDiscoveryServerConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ndi_state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e63941cb194cb869b21e62c115e1d82bc66505667f6b015ce7e1bed094e7564(
    *,
    discovery_server_address: typing.Optional[builtins.str] = None,
    discovery_server_port: typing.Optional[jsii.Number] = None,
    vpc_interface_adapter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88e36b0007a06aa7eb0df151e49cc225dc0fbe8e6ea03542c857bda214d215e7(
    *,
    role_arn: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66ccd0359fdc05267a5b960587186c05c5e6bef117b3711a6a0781b155106b27(
    *,
    state: typing.Optional[builtins.str] = None,
    threshold_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a8935dc30e2c4fc5e69fdc55620ba6135fcc03bc03c337c37f0e4a98b90b21(
    *,
    audio_monitoring_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.AudioMonitoringSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    content_quality_analysis_state: typing.Optional[builtins.str] = None,
    thumbnail_state: typing.Optional[builtins.str] = None,
    video_monitoring_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.VideoMonitoringSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88bbf27ba593734e8631a00f0d25fe4ac56ff79dc9467954cecbc3ca54601267(
    *,
    primary_source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd16c3f17bc4d41a7c2e2136ce29868227ab500eeb3d6f5a1ee1adfed3966ce7(
    *,
    decryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.EncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    entitlement_arn: typing.Optional[builtins.str] = None,
    gateway_bridge_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.GatewayBridgeSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ingest_ip: typing.Optional[builtins.str] = None,
    ingest_port: typing.Optional[jsii.Number] = None,
    max_bitrate: typing.Optional[jsii.Number] = None,
    max_latency: typing.Optional[jsii.Number] = None,
    max_sync_buffer: typing.Optional[jsii.Number] = None,
    media_stream_source_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.MediaStreamSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    min_latency: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    router_integration_state: typing.Optional[builtins.str] = None,
    router_integration_transit_decryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.FlowTransitEncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sender_control_port: typing.Optional[jsii.Number] = None,
    sender_ip_address: typing.Optional[builtins.str] = None,
    source_arn: typing.Optional[builtins.str] = None,
    source_ingest_port: typing.Optional[builtins.str] = None,
    source_listener_address: typing.Optional[builtins.str] = None,
    source_listener_port: typing.Optional[jsii.Number] = None,
    stream_id: typing.Optional[builtins.str] = None,
    vpc_interface_name: typing.Optional[builtins.str] = None,
    whitelist_cidr: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3baf104e902e74c7124d7bd34eb814271ebe501b368146cac7983db07a77f943(
    *,
    black_frames: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.BlackFramesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    frozen_frames: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowPropsMixin.FrozenFramesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ceb24c3a476989afbe314ad466d1b1503fce62659ba5405c4f26cc134c8051c(
    *,
    vpc_interface_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb244b8706c9591d328c0eeb7fbff9a9ec02e83875368672605d8c9f548856c(
    *,
    name: typing.Optional[builtins.str] = None,
    network_interface_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_interface_type: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0aee06c84560ce0699cf9c577beb5764e49775182941faa2b2eaf2c9ba03998(
    *,
    decryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowSourcePropsMixin.EncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    entitlement_arn: typing.Optional[builtins.str] = None,
    flow_arn: typing.Optional[builtins.str] = None,
    gateway_bridge_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowSourcePropsMixin.GatewayBridgeSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ingest_port: typing.Optional[jsii.Number] = None,
    max_bitrate: typing.Optional[jsii.Number] = None,
    max_latency: typing.Optional[jsii.Number] = None,
    min_latency: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    sender_control_port: typing.Optional[jsii.Number] = None,
    sender_ip_address: typing.Optional[builtins.str] = None,
    source_listener_address: typing.Optional[builtins.str] = None,
    source_listener_port: typing.Optional[jsii.Number] = None,
    stream_id: typing.Optional[builtins.str] = None,
    vpc_interface_name: typing.Optional[builtins.str] = None,
    whitelist_cidr: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f74844597ad4edf000d0b7bec905f15e58dbe23f867ce5a87df65ebc138a8237(
    props: typing.Union[CfnFlowSourceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea07e4e12e7609afc57c1c437ad05e59351b883902074edca0d782caabf2b3a6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30bc093798e3b321491966e1293d81f39ff0a047ef721e996176fa0a421bbcbf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26bede2fb08fa2aa992b2d7012185fdc0bf29bcf39d0d385e452ed8545d893a5(
    *,
    algorithm: typing.Optional[builtins.str] = None,
    constant_initialization_vector: typing.Optional[builtins.str] = None,
    device_id: typing.Optional[builtins.str] = None,
    key_type: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac25043c3739c104457fd0cae1ea1cb78f7bb412ce3a0b935943b01f7689f267(
    *,
    bridge_arn: typing.Optional[builtins.str] = None,
    vpc_interface_attachment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFlowSourcePropsMixin.VpcInterfaceAttachmentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e1d13c319ac98b4579769ca072408a05c20af6df9d3ea92230a73e74cc5798(
    *,
    vpc_interface_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55219b28d1249a53618ab4a108410c2cc2263f30cc1ae25188d45fb387345ed3(
    *,
    flow_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__409b37f755f20b161a12696d48d5f1578421dc816748fc7cb10300142ce7f6fc(
    props: typing.Union[CfnFlowVpcInterfaceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1043ec989226d493f90d907c63270433a05807d7ac7d4acb25ffdedd068f0419(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a2c3915c9a4b44d1144db584f1364c54d3fe1cdc51a848ed0c778989ae9d33b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb91dd33949073677337265b5ab70f66a9d29c7075ee6af603ef327ef004f981(
    *,
    egress_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    networks: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayPropsMixin.GatewayNetworkProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f029659f640b0b3e554d5df973ba85fc19c9491f265e17c0cc34455e0610a0cd(
    props: typing.Union[CfnGatewayMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44089f482f0c0aa70664aa603f388a5f52e0554656bd3995ed40eea7c1244a87(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9c9deadee031e2ecee98a95160b14e04de6a047144caa75a36d5831af86ddd8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__185391e71d9bbd95ffcf303ffad341e61253026a6572c36ede11a2574c6d3e2d(
    *,
    cidr_block: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78503390c836ec6df1491f415cb23595768e315fe7a68372d75299f66f512096(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.RouterInputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maintenance_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.MaintenanceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maximum_bitrate: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    region_name: typing.Optional[builtins.str] = None,
    routing_scope: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    tier: typing.Optional[builtins.str] = None,
    transit_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.RouterInputTransitEncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1566708a8326710e9c79c26bfdb4ba1d5c7cb009862f2f0728b02e1bb9fd626f(
    props: typing.Union[CfnRouterInputMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3caf6656a870ca9630aeb982fe6bd96133d21ef0addfc8570c75ff1d2e7045b0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2656e8aae91aa29a119b1180ecea7f4275a3d0c6de88d7b136f5bbe7095a5969(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e17acc119fe7a1c5e4539a54c21b687f0ff075f212b3ad89172d142bda8af344(
    *,
    network_interface_arn: typing.Optional[builtins.str] = None,
    primary_source_index: typing.Optional[jsii.Number] = None,
    protocol_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.FailoverRouterInputProtocolConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    source_priority_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31aaddad9486270d4f23ae001d908ffcce64eb375e254217472daa2f3a449fe5(
    *,
    rist: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rtp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    srt_caller: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.SrtCallerRouterInputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    srt_listener: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.SrtListenerRouterInputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb5cc2830fcef4ea00899d7db45834d795229186d57b0a48b3ff7e3f7105eba(
    *,
    automatic: typing.Any = None,
    secrets_manager: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25287d521a16647d90722e1a591fcf8774eb8da48b00d612e3014adef96eaa3(
    *,
    encryption_key_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    encryption_key_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f9ef96881f91b6f58a223b876257162bfcf70db6f0952fb225065763bbb079e(
    *,
    default: typing.Any = None,
    preferred_day_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.PreferredDayTimeMaintenanceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f9036438654c62b0587056b4c3e5b717a9a43e423c3fb72ea02a306503c6cae(
    *,
    flow_arn: typing.Optional[builtins.str] = None,
    flow_output_arn: typing.Optional[builtins.str] = None,
    source_transit_decryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.FlowTransitEncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26deea9c73ecdef770f309152c9b3a9af39ff9add1c9031b73c63c42a59ef6e8(
    *,
    merge_recovery_window_milliseconds: typing.Optional[jsii.Number] = None,
    network_interface_arn: typing.Optional[builtins.str] = None,
    protocol_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.MergeRouterInputProtocolConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f05aa15407508d4af14b1440ed6e6dd1b8770a64f2bdda3129f0e2cbeb68df13(
    *,
    rist: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rtp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96514398eeaa876a5bfb14ff8ab7ebdc44f9db450125f71684c28e33d28563e(
    *,
    day: typing.Optional[builtins.str] = None,
    time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aff331aa43acdb81e5495950dfe72ff5419b926ac3dbeff94558488b19775bc(
    *,
    port: typing.Optional[jsii.Number] = None,
    recovery_latency_milliseconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1a00d92a09d1f55f93fc6139dc55ed9f3b3ae6f1bc7f1756f389a08221392f(
    *,
    failover: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.FailoverRouterInputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    media_connect_flow: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.MediaConnectFlowRouterInputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    merge: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.MergeRouterInputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    standard: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.StandardRouterInputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f49220bee41dd2398c51fdbdae5055c5ccab6ffe8a872da32a2e8bac40eee02(
    *,
    rist: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.RistRouterInputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rtp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.RtpRouterInputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    srt_caller: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.SrtCallerRouterInputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    srt_listener: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.SrtListenerRouterInputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e71eb1c00f0874b687fd93dfec819c1f80d25fc58c248ceb604b8815a73398e(
    *,
    automatic: typing.Any = None,
    secrets_manager: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b0130827775a62f47c7a430a30ab5b61efb414fcea9e03d8866ce2c96b739c(
    *,
    encryption_key_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.RouterInputTransitEncryptionKeyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    encryption_key_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4bfe3ded3d1a81fddb2aa0a372cbf36aa083a7f32be5f25abf295849fe08388(
    *,
    forward_error_correction: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ca745017407377c93bf9274b6f6b424c3809b62e0e500705ba1e2beb12ebbaa(
    *,
    role_arn: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__044b1425cb641760a419cd9f6282e1e69fb42a9f34f4c3363ee53506c63877b2(
    *,
    decryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    minimum_latency_milliseconds: typing.Optional[jsii.Number] = None,
    source_address: typing.Optional[builtins.str] = None,
    source_port: typing.Optional[jsii.Number] = None,
    stream_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df94785e8cedbffb63bc59b79f0f0d8c9de4a924acad81639abf87ca79996f74(
    *,
    encryption_key: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a169e6fa1dc1543f9a15a2ad83039c3ce761a57ecb72e2453d472b4b74082b9(
    *,
    decryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.SrtDecryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    minimum_latency_milliseconds: typing.Optional[jsii.Number] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ed1eea02d0ec42039ff033da981dc89577de36d8bd200e6248aadb558d982e(
    *,
    network_interface_arn: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    protocol_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterInputPropsMixin.RouterInputProtocolConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b3484edc492a19afa1c12384baf035cf7060bc471d57073666f23990d627c0(
    *,
    configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterNetworkInterfacePropsMixin.RouterNetworkInterfaceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    region_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30887a5eb0c3d9ca7f13caa6a612c5690fc59edfb738f8ab74e2a91fa3063059(
    props: typing.Union[CfnRouterNetworkInterfaceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a81bca871ef62b375de8d053657a543ae65b87328946e494ae875cc72dbe7e9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc250bc7033248927edd23cd254457312b25c892725f0ac40f9e968248831192(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__311b3f15b46a0b433fe458c9e7907266474ecebc22bfcf323e5773b0f2f36fa4(
    *,
    allow_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterNetworkInterfacePropsMixin.PublicRouterNetworkInterfaceRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a613937fcd796f6a32fd46403cbe4fc26ad2b2d78fd337aeeb91c231fe7cc47(
    *,
    cidr: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aced7b56a0b3eff6075026d489b031bd5da947ca3e84eee141aa9f6e09a65d9(
    *,
    public: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterNetworkInterfacePropsMixin.PublicRouterNetworkInterfaceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterNetworkInterfacePropsMixin.VpcRouterNetworkInterfaceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3aa4fbd1e12e857144f42cb69810d0cfb60370fced55d27887e2f75511ffbb6(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__183c1f0f197c6e69663b4dbdc2e99d8c1a196b3a9b86c8d8f3a185e97a35bb3f(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterOutputPropsMixin.RouterOutputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maintenance_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterOutputPropsMixin.MaintenanceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maximum_bitrate: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    region_name: typing.Optional[builtins.str] = None,
    routing_scope: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    tier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb5be3075dfd57707fb1888d30b9bf64010adc44db27e40e24121cad6fde9454(
    props: typing.Union[CfnRouterOutputMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d048736b8bc4d4b47a772ee0574ab835ea28d61914d29469863cc7125f13b152(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d3b54b0b2047bd171e89de5e48343f7fa2b9dcbfffc426b1e3d47ccadbb0168(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0bbe24909bd774bf845263d2000da00e7ff2151f710ad1a341c79b03e67bf27(
    *,
    automatic: typing.Any = None,
    secrets_manager: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dba0e156fc31334bad65555e7294b93d94406f43161205183a1faafbc13feab0(
    *,
    encryption_key_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterOutputPropsMixin.FlowTransitEncryptionKeyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    encryption_key_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3903eaf25292c4ea3f26c9b7a24f60852dc94688a8ce147aac56d8fc83267589(
    *,
    default: typing.Any = None,
    preferred_day_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterOutputPropsMixin.PreferredDayTimeMaintenanceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a20225f3dd5556099cc870106523c204943d1e202867339f51d0e2be8f0fe35(
    *,
    destination_transit_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterOutputPropsMixin.FlowTransitEncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    flow_arn: typing.Optional[builtins.str] = None,
    flow_source_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7b35fd144b902d14e5f0be8a6c302f9f4817bf2e06cf6332d453137ae692e66(
    *,
    destination_transit_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterOutputPropsMixin.MediaLiveTransitEncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    media_live_input_arn: typing.Optional[builtins.str] = None,
    media_live_pipeline_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__420ebff6c7bacd49f62aa10df98f25a2da5e70fdaee99feef606bca38ec1d1cd(
    *,
    automatic: typing.Any = None,
    secrets_manager: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd4edccab5ee92812f9a88720f98bd4fd5d96289659e075330632dd65aee422c(
    *,
    encryption_key_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterOutputPropsMixin.MediaLiveTransitEncryptionKeyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    encryption_key_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cb9901bf03a9ae1eb69f58d17c005b70342f4136e1d6c1d97b742de7b317fad(
    *,
    day: typing.Optional[builtins.str] = None,
    time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4591fd3c202a89b95f3c295693ea2f2aa24ea02b10c91f226b91d13e6eb6c779(
    *,
    destination_address: typing.Optional[builtins.str] = None,
    destination_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddbdc4dc1fc39a4fd4c329952ea81941253b92c9d587c84e6ec9d64602ccce1f(
    *,
    media_connect_flow: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterOutputPropsMixin.MediaConnectFlowRouterOutputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    media_live_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterOutputPropsMixin.MediaLiveInputRouterOutputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    standard: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterOutputPropsMixin.StandardRouterOutputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a38a3f2af2dd44571fd5266f82ad0f2c33c4ca5039938727730b541cebdcfd8(
    *,
    rist: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterOutputPropsMixin.RistRouterOutputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rtp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterOutputPropsMixin.RtpRouterOutputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    srt_caller: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterOutputPropsMixin.SrtCallerRouterOutputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    srt_listener: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterOutputPropsMixin.SrtListenerRouterOutputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9793208620557eea33c2d2ab727ef80c89a642fcd87f9d31858ee97de10eab3(
    *,
    destination_address: typing.Optional[builtins.str] = None,
    destination_port: typing.Optional[jsii.Number] = None,
    forward_error_correction: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__453b4d7ebc2e99f313f1ab37fb3b2b9cc117cdad38b7c75b9eeca7039161f34f(
    *,
    role_arn: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6afdedfc466fda44efd2466008654be03d6e6076fc74abaa840bd1ea4413c44(
    *,
    destination_address: typing.Optional[builtins.str] = None,
    destination_port: typing.Optional[jsii.Number] = None,
    encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterOutputPropsMixin.SrtEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    minimum_latency_milliseconds: typing.Optional[jsii.Number] = None,
    stream_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9a249500d7cc096565af4c7a5a11491ab82a550814d202b21fb85fb5ca6a9d4(
    *,
    encryption_key: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterOutputPropsMixin.SecretsManagerEncryptionKeyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df472b706d66cb0aa39b07429a42ef72936a807f1b069b0ffc7e18afbad8759f(
    *,
    encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterOutputPropsMixin.SrtEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    minimum_latency_milliseconds: typing.Optional[jsii.Number] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4b8b7e21c5c4f9da800d10ca740c9ab5e9dddfa2a897a0d80ce972f6ca0ce77(
    *,
    network_interface_arn: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    protocol_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRouterOutputPropsMixin.RouterOutputProtocolConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
