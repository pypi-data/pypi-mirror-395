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
import aws_cdk.interfaces.aws_kinesisfirehose as _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d
import aws_cdk.interfaces.aws_logs as _aws_cdk_interfaces_aws_logs_ceddda9d
import aws_cdk.interfaces.aws_s3 as _aws_cdk_interfaces_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8
from ...aws_logs import ILogsDelivery as _ILogsDelivery_0d3c9e29
from ...core import IMixin as _IMixin_11e4b965, Mixin as _Mixin_a69446c0
from ...mixins import (
    CfnPropertyMixinOptions as _CfnPropertyMixinOptions_9cbff649,
    PropertyMergeStrategy as _PropertyMergeStrategy_49c157e8,
)


class CfnFirewallAlertLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnFirewallAlertLogs",
):
    '''Builder for CfnFirewallLogsMixin to generate ALERT_LOGS for CfnFirewall.

    :cloudformationResource: AWS::NetworkFirewall::Firewall
    :logType: ALERT_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
        
        cfn_firewall_alert_logs = networkfirewall_mixins.CfnFirewallAlertLogs()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toFirehose")
    def to_firehose(
        self,
        delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
    ) -> "CfnFirewallLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7328590b513805553dee64080b0a79efac3e8f24960e08b3147e3e1c0cd77569)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnFirewallLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnFirewallLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e67a490929fffe050d352d6197630e45bb231048c2061069a1de90a533030013)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnFirewallLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnFirewallLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f141909d9744c277aa229bebcd21ccdf011d035acd18dda3281db79ce95441e)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnFirewallLogsMixin", jsii.invoke(self, "toS3", [bucket]))


class CfnFirewallFlowLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnFirewallFlowLogs",
):
    '''Builder for CfnFirewallLogsMixin to generate FLOW_LOGS for CfnFirewall.

    :cloudformationResource: AWS::NetworkFirewall::Firewall
    :logType: FLOW_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
        
        cfn_firewall_flow_logs = networkfirewall_mixins.CfnFirewallFlowLogs()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toFirehose")
    def to_firehose(
        self,
        delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
    ) -> "CfnFirewallLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d0c1095f2366a9586eb3f395a32504aad3308ecf9172d6fa5ad6412e69e1c70)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnFirewallLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnFirewallLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd71c0b1f1d27a1812b9d05a137e96a538baa825c4553a6e08482e6090df99d3)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnFirewallLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnFirewallLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4a3f58fb66ed021923fb17d2ddd81fb144af311cbc8109de9a34dcc4a9f7445)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnFirewallLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnFirewallLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnFirewallLogsMixin",
):
    '''Use the firewall to provide stateful, managed, network firewall and intrusion detection and prevention filtering for your VPCs in Amazon VPC .

    The firewall defines the configuration settings for an AWS Network Firewall firewall. The settings include the firewall policy, the subnets in your VPC to use for the firewall endpoints, and any tags that are attached to the firewall AWS resource.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html
    :cloudformationResource: AWS::NetworkFirewall::Firewall
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_firewall_logs_mixin = networkfirewall_mixins.CfnFirewallLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::NetworkFirewall::Firewall``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7849a0cb6670c4dec2ef0ae2b87258f087ebacd9f96978d6c1d6aa4fe089ec82)
            check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            check_type(argname="argument log_delivery", value=log_delivery, expected_type=type_hints["log_delivery"])
        jsii.create(self.__class__, self, [log_type, log_delivery])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        resource: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply vended logs configuration to the construct.

        :param resource: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94742363755f8294f26cd606249ac9ba39736c6e737d707ea5c50a34d4ab9a70)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c49fe0c9d241623950091a3176bc672dd3ed72f003894ef6b14ad3a17df03ae5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ALERT_LOGS")
    def ALERT_LOGS(cls) -> CfnFirewallAlertLogs:
        return typing.cast(CfnFirewallAlertLogs, jsii.sget(cls, "ALERT_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="FLOW_LOGS")
    def FLOW_LOGS(cls) -> CfnFirewallFlowLogs:
        return typing.cast(CfnFirewallFlowLogs, jsii.sget(cls, "FLOW_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TLS_LOGS")
    def TLS_LOGS(cls) -> "CfnFirewallTlsLogs":
        return typing.cast("CfnFirewallTlsLogs", jsii.sget(cls, "TLS_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnFirewallMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zone_change_protection": "availabilityZoneChangeProtection",
        "availability_zone_mappings": "availabilityZoneMappings",
        "delete_protection": "deleteProtection",
        "description": "description",
        "enabled_analysis_types": "enabledAnalysisTypes",
        "firewall_name": "firewallName",
        "firewall_policy_arn": "firewallPolicyArn",
        "firewall_policy_change_protection": "firewallPolicyChangeProtection",
        "subnet_change_protection": "subnetChangeProtection",
        "subnet_mappings": "subnetMappings",
        "tags": "tags",
        "transit_gateway_id": "transitGatewayId",
        "vpc_id": "vpcId",
    },
)
class CfnFirewallMixinProps:
    def __init__(
        self,
        *,
        availability_zone_change_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        availability_zone_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFirewallPropsMixin.AvailabilityZoneMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        delete_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled_analysis_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        firewall_name: typing.Optional[builtins.str] = None,
        firewall_policy_arn: typing.Optional[builtins.str] = None,
        firewall_policy_change_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        subnet_change_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        subnet_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFirewallPropsMixin.SubnetMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        transit_gateway_id: typing.Optional[builtins.str] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnFirewallPropsMixin.

        :param availability_zone_change_protection: A setting indicating whether the firewall is protected against changes to its Availability Zone configuration. When set to ``TRUE`` , you must first disable this protection before adding or removing Availability Zones.
        :param availability_zone_mappings: The Availability Zones where the firewall endpoints are created for a transit gateway-attached firewall. Each mapping specifies an Availability Zone where the firewall processes traffic.
        :param delete_protection: A flag indicating whether it is possible to delete the firewall. A setting of ``TRUE`` indicates that the firewall is protected against deletion. Use this setting to protect against accidentally deleting a firewall that is in use. When you create a firewall, the operation initializes this flag to ``TRUE`` .
        :param description: A description of the firewall.
        :param enabled_analysis_types: An optional setting indicating the specific traffic analysis types to enable on the firewall.
        :param firewall_name: The descriptive name of the firewall. You can't change the name of a firewall after you create it.
        :param firewall_policy_arn: The Amazon Resource Name (ARN) of the firewall policy. The relationship of firewall to firewall policy is many to one. Each firewall requires one firewall policy association, and you can use the same firewall policy for multiple firewalls.
        :param firewall_policy_change_protection: A setting indicating whether the firewall is protected against a change to the firewall policy association. Use this setting to protect against accidentally modifying the firewall policy for a firewall that is in use. When you create a firewall, the operation initializes this setting to ``TRUE`` .
        :param subnet_change_protection: A setting indicating whether the firewall is protected against changes to the subnet associations. Use this setting to protect against accidentally modifying the subnet associations for a firewall that is in use. When you create a firewall, the operation initializes this setting to ``TRUE`` .
        :param subnet_mappings: The primary public subnets that Network Firewall is using for the firewall. Network Firewall creates a firewall endpoint in each subnet. Create a subnet mapping for each Availability Zone where you want to use the firewall. These subnets are all defined for a single, primary VPC, and each must belong to a different Availability Zone. Each of these subnets establishes the availability of the firewall in its Availability Zone. In addition to these subnets, you can define other endpoints for the firewall in ``VpcEndpointAssociation`` resources. You can define these additional endpoints for any VPC, and for any of the Availability Zones where the firewall resource already has a subnet mapping. VPC endpoint associations give you the ability to protect multiple VPCs using a single firewall, and to define multiple firewall endpoints for a VPC in a single Availability Zone.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param transit_gateway_id: The unique identifier of the transit gateway associated with this firewall. This field is only present for transit gateway-attached firewalls.
        :param vpc_id: The unique identifier of the VPC where the firewall is in use. You can't change the VPC of a firewall after you create the firewall.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
            
            cfn_firewall_mixin_props = networkfirewall_mixins.CfnFirewallMixinProps(
                availability_zone_change_protection=False,
                availability_zone_mappings=[networkfirewall_mixins.CfnFirewallPropsMixin.AvailabilityZoneMappingProperty(
                    availability_zone="availabilityZone"
                )],
                delete_protection=False,
                description="description",
                enabled_analysis_types=["enabledAnalysisTypes"],
                firewall_name="firewallName",
                firewall_policy_arn="firewallPolicyArn",
                firewall_policy_change_protection=False,
                subnet_change_protection=False,
                subnet_mappings=[networkfirewall_mixins.CfnFirewallPropsMixin.SubnetMappingProperty(
                    ip_address_type="ipAddressType",
                    subnet_id="subnetId"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                transit_gateway_id="transitGatewayId",
                vpc_id="vpcId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d221ece32039d9dc3ade00117446171adc4bdd1faca256da2a943ea6d52e60c)
            check_type(argname="argument availability_zone_change_protection", value=availability_zone_change_protection, expected_type=type_hints["availability_zone_change_protection"])
            check_type(argname="argument availability_zone_mappings", value=availability_zone_mappings, expected_type=type_hints["availability_zone_mappings"])
            check_type(argname="argument delete_protection", value=delete_protection, expected_type=type_hints["delete_protection"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled_analysis_types", value=enabled_analysis_types, expected_type=type_hints["enabled_analysis_types"])
            check_type(argname="argument firewall_name", value=firewall_name, expected_type=type_hints["firewall_name"])
            check_type(argname="argument firewall_policy_arn", value=firewall_policy_arn, expected_type=type_hints["firewall_policy_arn"])
            check_type(argname="argument firewall_policy_change_protection", value=firewall_policy_change_protection, expected_type=type_hints["firewall_policy_change_protection"])
            check_type(argname="argument subnet_change_protection", value=subnet_change_protection, expected_type=type_hints["subnet_change_protection"])
            check_type(argname="argument subnet_mappings", value=subnet_mappings, expected_type=type_hints["subnet_mappings"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument transit_gateway_id", value=transit_gateway_id, expected_type=type_hints["transit_gateway_id"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zone_change_protection is not None:
            self._values["availability_zone_change_protection"] = availability_zone_change_protection
        if availability_zone_mappings is not None:
            self._values["availability_zone_mappings"] = availability_zone_mappings
        if delete_protection is not None:
            self._values["delete_protection"] = delete_protection
        if description is not None:
            self._values["description"] = description
        if enabled_analysis_types is not None:
            self._values["enabled_analysis_types"] = enabled_analysis_types
        if firewall_name is not None:
            self._values["firewall_name"] = firewall_name
        if firewall_policy_arn is not None:
            self._values["firewall_policy_arn"] = firewall_policy_arn
        if firewall_policy_change_protection is not None:
            self._values["firewall_policy_change_protection"] = firewall_policy_change_protection
        if subnet_change_protection is not None:
            self._values["subnet_change_protection"] = subnet_change_protection
        if subnet_mappings is not None:
            self._values["subnet_mappings"] = subnet_mappings
        if tags is not None:
            self._values["tags"] = tags
        if transit_gateway_id is not None:
            self._values["transit_gateway_id"] = transit_gateway_id
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def availability_zone_change_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A setting indicating whether the firewall is protected against changes to its Availability Zone configuration.

        When set to ``TRUE`` , you must first disable this protection before adding or removing Availability Zones.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-availabilityzonechangeprotection
        '''
        result = self._values.get("availability_zone_change_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def availability_zone_mappings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPropsMixin.AvailabilityZoneMappingProperty"]]]]:
        '''The Availability Zones where the firewall endpoints are created for a transit gateway-attached firewall.

        Each mapping specifies an Availability Zone where the firewall processes traffic.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-availabilityzonemappings
        '''
        result = self._values.get("availability_zone_mappings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPropsMixin.AvailabilityZoneMappingProperty"]]]], result)

    @builtins.property
    def delete_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A flag indicating whether it is possible to delete the firewall.

        A setting of ``TRUE`` indicates that the firewall is protected against deletion. Use this setting to protect against accidentally deleting a firewall that is in use. When you create a firewall, the operation initializes this flag to ``TRUE`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-deleteprotection
        '''
        result = self._values.get("delete_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the firewall.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled_analysis_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An optional setting indicating the specific traffic analysis types to enable on the firewall.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-enabledanalysistypes
        '''
        result = self._values.get("enabled_analysis_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def firewall_name(self) -> typing.Optional[builtins.str]:
        '''The descriptive name of the firewall.

        You can't change the name of a firewall after you create it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-firewallname
        '''
        result = self._values.get("firewall_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firewall_policy_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the firewall policy.

        The relationship of firewall to firewall policy is many to one. Each firewall requires one firewall policy association, and you can use the same firewall policy for multiple firewalls.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-firewallpolicyarn
        '''
        result = self._values.get("firewall_policy_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firewall_policy_change_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A setting indicating whether the firewall is protected against a change to the firewall policy association.

        Use this setting to protect against accidentally modifying the firewall policy for a firewall that is in use. When you create a firewall, the operation initializes this setting to ``TRUE`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-firewallpolicychangeprotection
        '''
        result = self._values.get("firewall_policy_change_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def subnet_change_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A setting indicating whether the firewall is protected against changes to the subnet associations.

        Use this setting to protect against accidentally modifying the subnet associations for a firewall that is in use. When you create a firewall, the operation initializes this setting to ``TRUE`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-subnetchangeprotection
        '''
        result = self._values.get("subnet_change_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def subnet_mappings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPropsMixin.SubnetMappingProperty"]]]]:
        '''The primary public subnets that Network Firewall is using for the firewall.

        Network Firewall creates a firewall endpoint in each subnet. Create a subnet mapping for each Availability Zone where you want to use the firewall.

        These subnets are all defined for a single, primary VPC, and each must belong to a different Availability Zone. Each of these subnets establishes the availability of the firewall in its Availability Zone.

        In addition to these subnets, you can define other endpoints for the firewall in ``VpcEndpointAssociation`` resources. You can define these additional endpoints for any VPC, and for any of the Availability Zones where the firewall resource already has a subnet mapping. VPC endpoint associations give you the ability to protect multiple VPCs using a single firewall, and to define multiple firewall endpoints for a VPC in a single Availability Zone.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-subnetmappings
        '''
        result = self._values.get("subnet_mappings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPropsMixin.SubnetMappingProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def transit_gateway_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the transit gateway associated with this firewall.

        This field is only present for transit gateway-attached firewalls.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-transitgatewayid
        '''
        result = self._values.get("transit_gateway_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the VPC where the firewall is in use.

        You can't change the VPC of a firewall after you create the firewall.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-vpcid
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFirewallMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnFirewallPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "firewall_policy": "firewallPolicy",
        "firewall_policy_name": "firewallPolicyName",
        "tags": "tags",
    },
)
class CfnFirewallPolicyMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        firewall_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFirewallPolicyPropsMixin.FirewallPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        firewall_policy_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnFirewallPolicyPropsMixin.

        :param description: A description of the firewall policy.
        :param firewall_policy: The traffic filtering behavior of a firewall policy, defined in a collection of stateless and stateful rule groups and other settings.
        :param firewall_policy_name: The descriptive name of the firewall policy. You can't change the name of a firewall policy after you create it.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
            
            cfn_firewall_policy_mixin_props = networkfirewall_mixins.CfnFirewallPolicyMixinProps(
                description="description",
                firewall_policy=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.FirewallPolicyProperty(
                    enable_tls_session_holding=False,
                    policy_variables=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.PolicyVariablesProperty(
                        rule_variables={
                            "rule_variables_key": {
                                "definition": ["definition"]
                            }
                        }
                    ),
                    stateful_default_actions=["statefulDefaultActions"],
                    stateful_engine_options=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.StatefulEngineOptionsProperty(
                        flow_timeouts=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.FlowTimeoutsProperty(
                            tcp_idle_timeout_seconds=123
                        ),
                        rule_order="ruleOrder",
                        stream_exception_policy="streamExceptionPolicy"
                    ),
                    stateful_rule_group_references=[networkfirewall_mixins.CfnFirewallPolicyPropsMixin.StatefulRuleGroupReferenceProperty(
                        deep_threat_inspection=False,
                        override=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.StatefulRuleGroupOverrideProperty(
                            action="action"
                        ),
                        priority=123,
                        resource_arn="resourceArn"
                    )],
                    stateless_custom_actions=[networkfirewall_mixins.CfnFirewallPolicyPropsMixin.CustomActionProperty(
                        action_definition=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.ActionDefinitionProperty(
                            publish_metric_action=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.PublishMetricActionProperty(
                                dimensions=[networkfirewall_mixins.CfnFirewallPolicyPropsMixin.DimensionProperty(
                                    value="value"
                                )]
                            )
                        ),
                        action_name="actionName"
                    )],
                    stateless_default_actions=["statelessDefaultActions"],
                    stateless_fragment_default_actions=["statelessFragmentDefaultActions"],
                    stateless_rule_group_references=[networkfirewall_mixins.CfnFirewallPolicyPropsMixin.StatelessRuleGroupReferenceProperty(
                        priority=123,
                        resource_arn="resourceArn"
                    )],
                    tls_inspection_configuration_arn="tlsInspectionConfigurationArn"
                ),
                firewall_policy_name="firewallPolicyName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__217c93391153a84db656b13ddf2abd106c7c93dd4065a0e770fb0e5b5923635d)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument firewall_policy", value=firewall_policy, expected_type=type_hints["firewall_policy"])
            check_type(argname="argument firewall_policy_name", value=firewall_policy_name, expected_type=type_hints["firewall_policy_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if firewall_policy is not None:
            self._values["firewall_policy"] = firewall_policy
        if firewall_policy_name is not None:
            self._values["firewall_policy_name"] = firewall_policy_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the firewall policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firewall_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPolicyPropsMixin.FirewallPolicyProperty"]]:
        '''The traffic filtering behavior of a firewall policy, defined in a collection of stateless and stateful rule groups and other settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy
        '''
        result = self._values.get("firewall_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPolicyPropsMixin.FirewallPolicyProperty"]], result)

    @builtins.property
    def firewall_policy_name(self) -> typing.Optional[builtins.str]:
        '''The descriptive name of the firewall policy.

        You can't change the name of a firewall policy after you create it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicyname
        '''
        result = self._values.get("firewall_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFirewallPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFirewallPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnFirewallPolicyPropsMixin",
):
    '''Use the firewall policy to define the stateless and stateful network traffic filtering behavior for your firewall.

    You can use one firewall policy for multiple firewalls.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html
    :cloudformationResource: AWS::NetworkFirewall::FirewallPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
        
        cfn_firewall_policy_props_mixin = networkfirewall_mixins.CfnFirewallPolicyPropsMixin(networkfirewall_mixins.CfnFirewallPolicyMixinProps(
            description="description",
            firewall_policy=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.FirewallPolicyProperty(
                enable_tls_session_holding=False,
                policy_variables=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.PolicyVariablesProperty(
                    rule_variables={
                        "rule_variables_key": {
                            "definition": ["definition"]
                        }
                    }
                ),
                stateful_default_actions=["statefulDefaultActions"],
                stateful_engine_options=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.StatefulEngineOptionsProperty(
                    flow_timeouts=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.FlowTimeoutsProperty(
                        tcp_idle_timeout_seconds=123
                    ),
                    rule_order="ruleOrder",
                    stream_exception_policy="streamExceptionPolicy"
                ),
                stateful_rule_group_references=[networkfirewall_mixins.CfnFirewallPolicyPropsMixin.StatefulRuleGroupReferenceProperty(
                    deep_threat_inspection=False,
                    override=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.StatefulRuleGroupOverrideProperty(
                        action="action"
                    ),
                    priority=123,
                    resource_arn="resourceArn"
                )],
                stateless_custom_actions=[networkfirewall_mixins.CfnFirewallPolicyPropsMixin.CustomActionProperty(
                    action_definition=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.ActionDefinitionProperty(
                        publish_metric_action=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.PublishMetricActionProperty(
                            dimensions=[networkfirewall_mixins.CfnFirewallPolicyPropsMixin.DimensionProperty(
                                value="value"
                            )]
                        )
                    ),
                    action_name="actionName"
                )],
                stateless_default_actions=["statelessDefaultActions"],
                stateless_fragment_default_actions=["statelessFragmentDefaultActions"],
                stateless_rule_group_references=[networkfirewall_mixins.CfnFirewallPolicyPropsMixin.StatelessRuleGroupReferenceProperty(
                    priority=123,
                    resource_arn="resourceArn"
                )],
                tls_inspection_configuration_arn="tlsInspectionConfigurationArn"
            ),
            firewall_policy_name="firewallPolicyName",
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
        props: typing.Union[CfnFirewallPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NetworkFirewall::FirewallPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9f31d99d2404faf116762205aff648f73e80f939ce1f3bdc2b7c8f262c69be3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2a3a996f94b7d7472d8c15da4d3d9654243aa988dc31d82262878a3bc5258cc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3b7e1977444bd0eaf990d45b76f52945de22f938180906e74ff6eb71a855613)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFirewallPolicyMixinProps:
        return typing.cast(CfnFirewallPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnFirewallPolicyPropsMixin.ActionDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"publish_metric_action": "publishMetricAction"},
    )
    class ActionDefinitionProperty:
        def __init__(
            self,
            *,
            publish_metric_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFirewallPolicyPropsMixin.PublishMetricActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A custom action to use in stateless rule actions settings.

            :param publish_metric_action: Stateless inspection criteria that publishes the specified metrics to Amazon CloudWatch for the matching packet. This setting defines a CloudWatch dimension value to be published. You can pair this custom action with any of the standard stateless rule actions. For example, you could pair this in a rule action with the standard action that forwards the packet for stateful inspection. Then, when a packet matches the rule, Network Firewall publishes metrics for the packet and forwards it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-actiondefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                action_definition_property = networkfirewall_mixins.CfnFirewallPolicyPropsMixin.ActionDefinitionProperty(
                    publish_metric_action=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.PublishMetricActionProperty(
                        dimensions=[networkfirewall_mixins.CfnFirewallPolicyPropsMixin.DimensionProperty(
                            value="value"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1e5c0eca83fd919c2802ec0b35e718b5ffec8557e4d92e543942e2a154885d2f)
                check_type(argname="argument publish_metric_action", value=publish_metric_action, expected_type=type_hints["publish_metric_action"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if publish_metric_action is not None:
                self._values["publish_metric_action"] = publish_metric_action

        @builtins.property
        def publish_metric_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPolicyPropsMixin.PublishMetricActionProperty"]]:
            '''Stateless inspection criteria that publishes the specified metrics to Amazon CloudWatch for the matching packet.

            This setting defines a CloudWatch dimension value to be published.

            You can pair this custom action with any of the standard stateless rule actions. For example, you could pair this in a rule action with the standard action that forwards the packet for stateful inspection. Then, when a packet matches the rule, Network Firewall publishes metrics for the packet and forwards it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-actiondefinition.html#cfn-networkfirewall-firewallpolicy-actiondefinition-publishmetricaction
            '''
            result = self._values.get("publish_metric_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPolicyPropsMixin.PublishMetricActionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnFirewallPolicyPropsMixin.CustomActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_definition": "actionDefinition",
            "action_name": "actionName",
        },
    )
    class CustomActionProperty:
        def __init__(
            self,
            *,
            action_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFirewallPolicyPropsMixin.ActionDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            action_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An optional, non-standard action to use for stateless packet handling.

            You can define this in addition to the standard action that you must specify.

            You define and name the custom actions that you want to be able to use, and then you reference them by name in your actions settings.

            You can use custom actions in the following places:

            - In an ``StatelessRulesAndCustomActions`` . The custom actions are available for use by name inside the ``StatelessRulesAndCustomActions`` where you define them. You can use them for your stateless rule actions to specify what to do with a packet that matches the rule's match attributes.
            - In an firewall policy specification, in ``StatelessCustomActions`` . The custom actions are available for use inside the policy where you define them. You can use them for the policy's default stateless actions settings to specify what to do with packets that don't match any of the policy's stateless rules.

            :param action_definition: The custom action associated with the action name.
            :param action_name: The descriptive name of the custom action. You can't change the name of a custom action after you create it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-customaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                custom_action_property = networkfirewall_mixins.CfnFirewallPolicyPropsMixin.CustomActionProperty(
                    action_definition=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.ActionDefinitionProperty(
                        publish_metric_action=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.PublishMetricActionProperty(
                            dimensions=[networkfirewall_mixins.CfnFirewallPolicyPropsMixin.DimensionProperty(
                                value="value"
                            )]
                        )
                    ),
                    action_name="actionName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ee6bdca6fe32f9b7d2aa4e6b899a47df06fdfa30cd21b2067c4b214d48c98ba4)
                check_type(argname="argument action_definition", value=action_definition, expected_type=type_hints["action_definition"])
                check_type(argname="argument action_name", value=action_name, expected_type=type_hints["action_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action_definition is not None:
                self._values["action_definition"] = action_definition
            if action_name is not None:
                self._values["action_name"] = action_name

        @builtins.property
        def action_definition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPolicyPropsMixin.ActionDefinitionProperty"]]:
            '''The custom action associated with the action name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-customaction.html#cfn-networkfirewall-firewallpolicy-customaction-actiondefinition
            '''
            result = self._values.get("action_definition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPolicyPropsMixin.ActionDefinitionProperty"]], result)

        @builtins.property
        def action_name(self) -> typing.Optional[builtins.str]:
            '''The descriptive name of the custom action.

            You can't change the name of a custom action after you create it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-customaction.html#cfn-networkfirewall-firewallpolicy-customaction-actionname
            '''
            result = self._values.get("action_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnFirewallPolicyPropsMixin.DimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value"},
    )
    class DimensionProperty:
        def __init__(self, *, value: typing.Optional[builtins.str] = None) -> None:
            '''The value to use in an Amazon CloudWatch custom metric dimension.

            This is used in the ``PublishMetrics`` custom action. A CloudWatch custom metric dimension is a name/value pair that's part of the identity of a metric.

            AWS Network Firewall sets the dimension name to ``CustomAction`` and you provide the dimension value.

            For more information about CloudWatch custom metric dimensions, see `Publishing Custom Metrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/publishingMetrics.html#usingDimensions>`_ in the `Amazon CloudWatch User Guide <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html>`_ .

            :param value: The value to use in the custom metric dimension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-dimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                dimension_property = networkfirewall_mixins.CfnFirewallPolicyPropsMixin.DimensionProperty(
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e1c4cde82ee095606b04c9109c9d94f07d11cef9699606ae2e02cf341350983d)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value to use in the custom metric dimension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-dimension.html#cfn-networkfirewall-firewallpolicy-dimension-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnFirewallPolicyPropsMixin.FirewallPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enable_tls_session_holding": "enableTlsSessionHolding",
            "policy_variables": "policyVariables",
            "stateful_default_actions": "statefulDefaultActions",
            "stateful_engine_options": "statefulEngineOptions",
            "stateful_rule_group_references": "statefulRuleGroupReferences",
            "stateless_custom_actions": "statelessCustomActions",
            "stateless_default_actions": "statelessDefaultActions",
            "stateless_fragment_default_actions": "statelessFragmentDefaultActions",
            "stateless_rule_group_references": "statelessRuleGroupReferences",
            "tls_inspection_configuration_arn": "tlsInspectionConfigurationArn",
        },
    )
    class FirewallPolicyProperty:
        def __init__(
            self,
            *,
            enable_tls_session_holding: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            policy_variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFirewallPolicyPropsMixin.PolicyVariablesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            stateful_default_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
            stateful_engine_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFirewallPolicyPropsMixin.StatefulEngineOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            stateful_rule_group_references: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFirewallPolicyPropsMixin.StatefulRuleGroupReferenceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            stateless_custom_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFirewallPolicyPropsMixin.CustomActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            stateless_default_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
            stateless_fragment_default_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
            stateless_rule_group_references: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFirewallPolicyPropsMixin.StatelessRuleGroupReferenceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            tls_inspection_configuration_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The traffic filtering behavior of a firewall policy, defined in a collection of stateless and stateful rule groups and other settings.

            :param enable_tls_session_holding: When true, prevents TCP and TLS packets from reaching destination servers until TLS Inspection has evaluated Server Name Indication (SNI) rules. Requires an associated TLS Inspection configuration.
            :param policy_variables: Contains variables that you can use to override default Suricata settings in your firewall policy.
            :param stateful_default_actions: The default actions to take on a packet that doesn't match any stateful rules. The stateful default action is optional, and is only valid when using the strict rule order. Valid values of the stateful default action: - aws:drop_strict - aws:drop_established - aws:alert_strict - aws:alert_established For more information, see `Strict evaluation order <https://docs.aws.amazon.com/network-firewall/latest/developerguide/suricata-rule-evaluation-order.html#suricata-strict-rule-evaluation-order.html>`_ in the *AWS Network Firewall Developer Guide* .
            :param stateful_engine_options: Additional options governing how Network Firewall handles stateful rules. The stateful rule groups that you use in your policy must have stateful rule options settings that are compatible with these settings.
            :param stateful_rule_group_references: References to the stateful rule groups that are used in the policy. These define the inspection criteria in stateful rules.
            :param stateless_custom_actions: The custom action definitions that are available for use in the firewall policy's ``StatelessDefaultActions`` setting. You name each custom action that you define, and then you can use it by name in your default actions specifications.
            :param stateless_default_actions: The actions to take on a packet if it doesn't match any of the stateless rules in the policy. If you want non-matching packets to be forwarded for stateful inspection, specify ``aws:forward_to_sfe`` . You must specify one of the standard actions: ``aws:pass`` , ``aws:drop`` , or ``aws:forward_to_sfe`` . In addition, you can specify custom actions that are compatible with your standard section choice. For example, you could specify ``["aws:pass"]`` or you could specify ``["aws:pass", “customActionName”]`` . For information about compatibility, see the custom action descriptions.
            :param stateless_fragment_default_actions: The actions to take on a fragmented packet if it doesn't match any of the stateless rules in the policy. If you want non-matching fragmented packets to be forwarded for stateful inspection, specify ``aws:forward_to_sfe`` . You must specify one of the standard actions: ``aws:pass`` , ``aws:drop`` , or ``aws:forward_to_sfe`` . In addition, you can specify custom actions that are compatible with your standard section choice. For example, you could specify ``["aws:pass"]`` or you could specify ``["aws:pass", “customActionName”]`` . For information about compatibility, see the custom action descriptions.
            :param stateless_rule_group_references: References to the stateless rule groups that are used in the policy. These define the matching criteria in stateless rules.
            :param tls_inspection_configuration_arn: The Amazon Resource Name (ARN) of the TLS inspection configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                firewall_policy_property = networkfirewall_mixins.CfnFirewallPolicyPropsMixin.FirewallPolicyProperty(
                    enable_tls_session_holding=False,
                    policy_variables=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.PolicyVariablesProperty(
                        rule_variables={
                            "rule_variables_key": {
                                "definition": ["definition"]
                            }
                        }
                    ),
                    stateful_default_actions=["statefulDefaultActions"],
                    stateful_engine_options=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.StatefulEngineOptionsProperty(
                        flow_timeouts=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.FlowTimeoutsProperty(
                            tcp_idle_timeout_seconds=123
                        ),
                        rule_order="ruleOrder",
                        stream_exception_policy="streamExceptionPolicy"
                    ),
                    stateful_rule_group_references=[networkfirewall_mixins.CfnFirewallPolicyPropsMixin.StatefulRuleGroupReferenceProperty(
                        deep_threat_inspection=False,
                        override=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.StatefulRuleGroupOverrideProperty(
                            action="action"
                        ),
                        priority=123,
                        resource_arn="resourceArn"
                    )],
                    stateless_custom_actions=[networkfirewall_mixins.CfnFirewallPolicyPropsMixin.CustomActionProperty(
                        action_definition=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.ActionDefinitionProperty(
                            publish_metric_action=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.PublishMetricActionProperty(
                                dimensions=[networkfirewall_mixins.CfnFirewallPolicyPropsMixin.DimensionProperty(
                                    value="value"
                                )]
                            )
                        ),
                        action_name="actionName"
                    )],
                    stateless_default_actions=["statelessDefaultActions"],
                    stateless_fragment_default_actions=["statelessFragmentDefaultActions"],
                    stateless_rule_group_references=[networkfirewall_mixins.CfnFirewallPolicyPropsMixin.StatelessRuleGroupReferenceProperty(
                        priority=123,
                        resource_arn="resourceArn"
                    )],
                    tls_inspection_configuration_arn="tlsInspectionConfigurationArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__37511d2a2526d0826f880c68538a135daeb08492f7915969354a25445506d91c)
                check_type(argname="argument enable_tls_session_holding", value=enable_tls_session_holding, expected_type=type_hints["enable_tls_session_holding"])
                check_type(argname="argument policy_variables", value=policy_variables, expected_type=type_hints["policy_variables"])
                check_type(argname="argument stateful_default_actions", value=stateful_default_actions, expected_type=type_hints["stateful_default_actions"])
                check_type(argname="argument stateful_engine_options", value=stateful_engine_options, expected_type=type_hints["stateful_engine_options"])
                check_type(argname="argument stateful_rule_group_references", value=stateful_rule_group_references, expected_type=type_hints["stateful_rule_group_references"])
                check_type(argname="argument stateless_custom_actions", value=stateless_custom_actions, expected_type=type_hints["stateless_custom_actions"])
                check_type(argname="argument stateless_default_actions", value=stateless_default_actions, expected_type=type_hints["stateless_default_actions"])
                check_type(argname="argument stateless_fragment_default_actions", value=stateless_fragment_default_actions, expected_type=type_hints["stateless_fragment_default_actions"])
                check_type(argname="argument stateless_rule_group_references", value=stateless_rule_group_references, expected_type=type_hints["stateless_rule_group_references"])
                check_type(argname="argument tls_inspection_configuration_arn", value=tls_inspection_configuration_arn, expected_type=type_hints["tls_inspection_configuration_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable_tls_session_holding is not None:
                self._values["enable_tls_session_holding"] = enable_tls_session_holding
            if policy_variables is not None:
                self._values["policy_variables"] = policy_variables
            if stateful_default_actions is not None:
                self._values["stateful_default_actions"] = stateful_default_actions
            if stateful_engine_options is not None:
                self._values["stateful_engine_options"] = stateful_engine_options
            if stateful_rule_group_references is not None:
                self._values["stateful_rule_group_references"] = stateful_rule_group_references
            if stateless_custom_actions is not None:
                self._values["stateless_custom_actions"] = stateless_custom_actions
            if stateless_default_actions is not None:
                self._values["stateless_default_actions"] = stateless_default_actions
            if stateless_fragment_default_actions is not None:
                self._values["stateless_fragment_default_actions"] = stateless_fragment_default_actions
            if stateless_rule_group_references is not None:
                self._values["stateless_rule_group_references"] = stateless_rule_group_references
            if tls_inspection_configuration_arn is not None:
                self._values["tls_inspection_configuration_arn"] = tls_inspection_configuration_arn

        @builtins.property
        def enable_tls_session_holding(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When true, prevents TCP and TLS packets from reaching destination servers until TLS Inspection has evaluated Server Name Indication (SNI) rules.

            Requires an associated TLS Inspection configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-enabletlssessionholding
            '''
            result = self._values.get("enable_tls_session_holding")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def policy_variables(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPolicyPropsMixin.PolicyVariablesProperty"]]:
            '''Contains variables that you can use to override default Suricata settings in your firewall policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-policyvariables
            '''
            result = self._values.get("policy_variables")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPolicyPropsMixin.PolicyVariablesProperty"]], result)

        @builtins.property
        def stateful_default_actions(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The default actions to take on a packet that doesn't match any stateful rules.

            The stateful default action is optional, and is only valid when using the strict rule order.

            Valid values of the stateful default action:

            - aws:drop_strict
            - aws:drop_established
            - aws:alert_strict
            - aws:alert_established

            For more information, see `Strict evaluation order <https://docs.aws.amazon.com/network-firewall/latest/developerguide/suricata-rule-evaluation-order.html#suricata-strict-rule-evaluation-order.html>`_ in the *AWS Network Firewall Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-statefuldefaultactions
            '''
            result = self._values.get("stateful_default_actions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def stateful_engine_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPolicyPropsMixin.StatefulEngineOptionsProperty"]]:
            '''Additional options governing how Network Firewall handles stateful rules.

            The stateful rule groups that you use in your policy must have stateful rule options settings that are compatible with these settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-statefulengineoptions
            '''
            result = self._values.get("stateful_engine_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPolicyPropsMixin.StatefulEngineOptionsProperty"]], result)

        @builtins.property
        def stateful_rule_group_references(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPolicyPropsMixin.StatefulRuleGroupReferenceProperty"]]]]:
            '''References to the stateful rule groups that are used in the policy.

            These define the inspection criteria in stateful rules.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-statefulrulegroupreferences
            '''
            result = self._values.get("stateful_rule_group_references")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPolicyPropsMixin.StatefulRuleGroupReferenceProperty"]]]], result)

        @builtins.property
        def stateless_custom_actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPolicyPropsMixin.CustomActionProperty"]]]]:
            '''The custom action definitions that are available for use in the firewall policy's ``StatelessDefaultActions`` setting.

            You name each custom action that you define, and then you can use it by name in your default actions specifications.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-statelesscustomactions
            '''
            result = self._values.get("stateless_custom_actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPolicyPropsMixin.CustomActionProperty"]]]], result)

        @builtins.property
        def stateless_default_actions(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The actions to take on a packet if it doesn't match any of the stateless rules in the policy.

            If you want non-matching packets to be forwarded for stateful inspection, specify ``aws:forward_to_sfe`` .

            You must specify one of the standard actions: ``aws:pass`` , ``aws:drop`` , or ``aws:forward_to_sfe`` . In addition, you can specify custom actions that are compatible with your standard section choice.

            For example, you could specify ``["aws:pass"]`` or you could specify ``["aws:pass", “customActionName”]`` . For information about compatibility, see the custom action descriptions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-statelessdefaultactions
            '''
            result = self._values.get("stateless_default_actions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def stateless_fragment_default_actions(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The actions to take on a fragmented packet if it doesn't match any of the stateless rules in the policy.

            If you want non-matching fragmented packets to be forwarded for stateful inspection, specify ``aws:forward_to_sfe`` .

            You must specify one of the standard actions: ``aws:pass`` , ``aws:drop`` , or ``aws:forward_to_sfe`` . In addition, you can specify custom actions that are compatible with your standard section choice.

            For example, you could specify ``["aws:pass"]`` or you could specify ``["aws:pass", “customActionName”]`` . For information about compatibility, see the custom action descriptions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-statelessfragmentdefaultactions
            '''
            result = self._values.get("stateless_fragment_default_actions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def stateless_rule_group_references(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPolicyPropsMixin.StatelessRuleGroupReferenceProperty"]]]]:
            '''References to the stateless rule groups that are used in the policy.

            These define the matching criteria in stateless rules.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-statelessrulegroupreferences
            '''
            result = self._values.get("stateless_rule_group_references")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPolicyPropsMixin.StatelessRuleGroupReferenceProperty"]]]], result)

        @builtins.property
        def tls_inspection_configuration_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the TLS inspection configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-tlsinspectionconfigurationarn
            '''
            result = self._values.get("tls_inspection_configuration_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FirewallPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnFirewallPolicyPropsMixin.FlowTimeoutsProperty",
        jsii_struct_bases=[],
        name_mapping={"tcp_idle_timeout_seconds": "tcpIdleTimeoutSeconds"},
    )
    class FlowTimeoutsProperty:
        def __init__(
            self,
            *,
            tcp_idle_timeout_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes the amount of time that can pass without any traffic sent through the firewall before the firewall determines that the connection is idle and Network Firewall removes the flow entry from its flow table.

            Existing connections and flows are not impacted when you update this value. Only new connections after you update this value are impacted.

            :param tcp_idle_timeout_seconds: The number of seconds that can pass without any TCP traffic sent through the firewall before the firewall determines that the connection is idle. After the idle timeout passes, data packets are dropped, however, the next TCP SYN packet is considered a new flow and is processed by the firewall. Clients or targets can use TCP keepalive packets to reset the idle timeout. You can define the ``TcpIdleTimeoutSeconds`` value to be between 60 and 6000 seconds. If no value is provided, it defaults to 350 seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-flowtimeouts.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                flow_timeouts_property = networkfirewall_mixins.CfnFirewallPolicyPropsMixin.FlowTimeoutsProperty(
                    tcp_idle_timeout_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9e8a137519b9ca17a685dff2ed62a82c4ce0f82324eb98e1a17a4ec80a7094bc)
                check_type(argname="argument tcp_idle_timeout_seconds", value=tcp_idle_timeout_seconds, expected_type=type_hints["tcp_idle_timeout_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if tcp_idle_timeout_seconds is not None:
                self._values["tcp_idle_timeout_seconds"] = tcp_idle_timeout_seconds

        @builtins.property
        def tcp_idle_timeout_seconds(self) -> typing.Optional[jsii.Number]:
            '''The number of seconds that can pass without any TCP traffic sent through the firewall before the firewall determines that the connection is idle.

            After the idle timeout passes, data packets are dropped, however, the next TCP SYN packet is considered a new flow and is processed by the firewall. Clients or targets can use TCP keepalive packets to reset the idle timeout.

            You can define the ``TcpIdleTimeoutSeconds`` value to be between 60 and 6000 seconds. If no value is provided, it defaults to 350 seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-flowtimeouts.html#cfn-networkfirewall-firewallpolicy-flowtimeouts-tcpidletimeoutseconds
            '''
            result = self._values.get("tcp_idle_timeout_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FlowTimeoutsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnFirewallPolicyPropsMixin.IPSetProperty",
        jsii_struct_bases=[],
        name_mapping={"definition": "definition"},
    )
    class IPSetProperty:
        def __init__(
            self,
            *,
            definition: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A list of IP addresses and address ranges, in CIDR notation.

            This is part of a rule variable.

            :param definition: The list of IP addresses and address ranges, in CIDR notation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-ipset.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                i_pSet_property = {
                    "definition": ["definition"]
                }
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cc0c540afeb3a8655ecaadd3587b4f2f48caaeb0c4b2b4ecd3390b871f0e5fc9)
                check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if definition is not None:
                self._values["definition"] = definition

        @builtins.property
        def definition(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of IP addresses and address ranges, in CIDR notation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-ipset.html#cfn-networkfirewall-firewallpolicy-ipset-definition
            '''
            result = self._values.get("definition")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IPSetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnFirewallPolicyPropsMixin.PolicyVariablesProperty",
        jsii_struct_bases=[],
        name_mapping={"rule_variables": "ruleVariables"},
    )
    class PolicyVariablesProperty:
        def __init__(
            self,
            *,
            rule_variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFirewallPolicyPropsMixin.IPSetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Contains variables that you can use to override default Suricata settings in your firewall policy.

            :param rule_variables: The IPv4 or IPv6 addresses in CIDR notation to use for the Suricata ``HOME_NET`` variable. If your firewall uses an inspection VPC, you might want to override the ``HOME_NET`` variable with the CIDRs of your home networks. If you don't override ``HOME_NET`` with your own CIDRs, Network Firewall by default uses the CIDR of your inspection VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-policyvariables.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                policy_variables_property = networkfirewall_mixins.CfnFirewallPolicyPropsMixin.PolicyVariablesProperty(
                    rule_variables={
                        "rule_variables_key": {
                            "definition": ["definition"]
                        }
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__44bb80968f8561390d6243226fcf47b05eccca5cf04bce3dc6e8d9989d69cd01)
                check_type(argname="argument rule_variables", value=rule_variables, expected_type=type_hints["rule_variables"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rule_variables is not None:
                self._values["rule_variables"] = rule_variables

        @builtins.property
        def rule_variables(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPolicyPropsMixin.IPSetProperty"]]]]:
            '''The IPv4 or IPv6 addresses in CIDR notation to use for the Suricata ``HOME_NET`` variable.

            If your firewall uses an inspection VPC, you might want to override the ``HOME_NET`` variable with the CIDRs of your home networks. If you don't override ``HOME_NET`` with your own CIDRs, Network Firewall by default uses the CIDR of your inspection VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-policyvariables.html#cfn-networkfirewall-firewallpolicy-policyvariables-rulevariables
            '''
            result = self._values.get("rule_variables")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPolicyPropsMixin.IPSetProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyVariablesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnFirewallPolicyPropsMixin.PublishMetricActionProperty",
        jsii_struct_bases=[],
        name_mapping={"dimensions": "dimensions"},
    )
    class PublishMetricActionProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFirewallPolicyPropsMixin.DimensionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Stateless inspection criteria that publishes the specified metrics to Amazon CloudWatch for the matching packet.

            This setting defines a CloudWatch dimension value to be published.

            :param dimensions: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-publishmetricaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                publish_metric_action_property = networkfirewall_mixins.CfnFirewallPolicyPropsMixin.PublishMetricActionProperty(
                    dimensions=[networkfirewall_mixins.CfnFirewallPolicyPropsMixin.DimensionProperty(
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3ba578216f83656dc0599ea3c015290a4588b3006fd9a7825c717b6548d2a4ec)
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimensions is not None:
                self._values["dimensions"] = dimensions

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPolicyPropsMixin.DimensionProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-publishmetricaction.html#cfn-networkfirewall-firewallpolicy-publishmetricaction-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPolicyPropsMixin.DimensionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PublishMetricActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnFirewallPolicyPropsMixin.StatefulEngineOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "flow_timeouts": "flowTimeouts",
            "rule_order": "ruleOrder",
            "stream_exception_policy": "streamExceptionPolicy",
        },
    )
    class StatefulEngineOptionsProperty:
        def __init__(
            self,
            *,
            flow_timeouts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFirewallPolicyPropsMixin.FlowTimeoutsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rule_order: typing.Optional[builtins.str] = None,
            stream_exception_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration settings for the handling of the stateful rule groups in a firewall policy.

            :param flow_timeouts: Configures the amount of time that can pass without any traffic sent through the firewall before the firewall determines that the connection is idle.
            :param rule_order: Indicates how to manage the order of stateful rule evaluation for the policy. ``DEFAULT_ACTION_ORDER`` is the default behavior. Stateful rules are provided to the rule engine as Suricata compatible strings, and Suricata evaluates them based on certain settings. For more information, see `Evaluation order for stateful rules <https://docs.aws.amazon.com/network-firewall/latest/developerguide/suricata-rule-evaluation-order.html>`_ in the *AWS Network Firewall Developer Guide* .
            :param stream_exception_policy: Configures how Network Firewall processes traffic when a network connection breaks midstream. Network connections can break due to disruptions in external networks or within the firewall itself. - ``DROP`` - Network Firewall fails closed and drops all subsequent traffic going to the firewall. This is the default behavior. - ``CONTINUE`` - Network Firewall continues to apply rules to the subsequent traffic without context from traffic before the break. This impacts the behavior of rules that depend on this context. For example, if you have a stateful rule to ``drop http`` traffic, Network Firewall won't match the traffic for this rule because the service won't have the context from session initialization defining the application layer protocol as HTTP. However, this behavior is rule dependent—a TCP-layer rule using a ``flow:stateless`` rule would still match, as would the ``aws:drop_strict`` default action. - ``REJECT`` - Network Firewall fails closed and drops all subsequent traffic going to the firewall. Network Firewall also sends a TCP reject packet back to your client so that the client can immediately establish a new session. Network Firewall will have context about the new session and will apply rules to the subsequent traffic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulengineoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                stateful_engine_options_property = networkfirewall_mixins.CfnFirewallPolicyPropsMixin.StatefulEngineOptionsProperty(
                    flow_timeouts=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.FlowTimeoutsProperty(
                        tcp_idle_timeout_seconds=123
                    ),
                    rule_order="ruleOrder",
                    stream_exception_policy="streamExceptionPolicy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__487fd2fb21e4293549dbeb34c36acd758dc2c0d4f1d39f1375a75205f9a468f6)
                check_type(argname="argument flow_timeouts", value=flow_timeouts, expected_type=type_hints["flow_timeouts"])
                check_type(argname="argument rule_order", value=rule_order, expected_type=type_hints["rule_order"])
                check_type(argname="argument stream_exception_policy", value=stream_exception_policy, expected_type=type_hints["stream_exception_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if flow_timeouts is not None:
                self._values["flow_timeouts"] = flow_timeouts
            if rule_order is not None:
                self._values["rule_order"] = rule_order
            if stream_exception_policy is not None:
                self._values["stream_exception_policy"] = stream_exception_policy

        @builtins.property
        def flow_timeouts(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPolicyPropsMixin.FlowTimeoutsProperty"]]:
            '''Configures the amount of time that can pass without any traffic sent through the firewall before the firewall determines that the connection is idle.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulengineoptions.html#cfn-networkfirewall-firewallpolicy-statefulengineoptions-flowtimeouts
            '''
            result = self._values.get("flow_timeouts")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPolicyPropsMixin.FlowTimeoutsProperty"]], result)

        @builtins.property
        def rule_order(self) -> typing.Optional[builtins.str]:
            '''Indicates how to manage the order of stateful rule evaluation for the policy.

            ``DEFAULT_ACTION_ORDER`` is the default behavior. Stateful rules are provided to the rule engine as Suricata compatible strings, and Suricata evaluates them based on certain settings. For more information, see `Evaluation order for stateful rules <https://docs.aws.amazon.com/network-firewall/latest/developerguide/suricata-rule-evaluation-order.html>`_ in the *AWS Network Firewall Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulengineoptions.html#cfn-networkfirewall-firewallpolicy-statefulengineoptions-ruleorder
            '''
            result = self._values.get("rule_order")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stream_exception_policy(self) -> typing.Optional[builtins.str]:
            '''Configures how Network Firewall processes traffic when a network connection breaks midstream.

            Network connections can break due to disruptions in external networks or within the firewall itself.

            - ``DROP`` - Network Firewall fails closed and drops all subsequent traffic going to the firewall. This is the default behavior.
            - ``CONTINUE`` - Network Firewall continues to apply rules to the subsequent traffic without context from traffic before the break. This impacts the behavior of rules that depend on this context. For example, if you have a stateful rule to ``drop http`` traffic, Network Firewall won't match the traffic for this rule because the service won't have the context from session initialization defining the application layer protocol as HTTP. However, this behavior is rule dependent—a TCP-layer rule using a ``flow:stateless`` rule would still match, as would the ``aws:drop_strict`` default action.
            - ``REJECT`` - Network Firewall fails closed and drops all subsequent traffic going to the firewall. Network Firewall also sends a TCP reject packet back to your client so that the client can immediately establish a new session. Network Firewall will have context about the new session and will apply rules to the subsequent traffic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulengineoptions.html#cfn-networkfirewall-firewallpolicy-statefulengineoptions-streamexceptionpolicy
            '''
            result = self._values.get("stream_exception_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatefulEngineOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnFirewallPolicyPropsMixin.StatefulRuleGroupOverrideProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action"},
    )
    class StatefulRuleGroupOverrideProperty:
        def __init__(self, *, action: typing.Optional[builtins.str] = None) -> None:
            '''The setting that allows the policy owner to change the behavior of the rule group within a policy.

            :param action: The action that changes the rule group from ``DROP`` to ``ALERT`` . This only applies to managed rule groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulrulegroupoverride.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                stateful_rule_group_override_property = networkfirewall_mixins.CfnFirewallPolicyPropsMixin.StatefulRuleGroupOverrideProperty(
                    action="action"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e26f17e84a1c51385faf08ac5866559e8b553fedd0371c0df16d81bed04f42f2)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action that changes the rule group from ``DROP`` to ``ALERT`` .

            This only applies to managed rule groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulrulegroupoverride.html#cfn-networkfirewall-firewallpolicy-statefulrulegroupoverride-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatefulRuleGroupOverrideProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnFirewallPolicyPropsMixin.StatefulRuleGroupReferenceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "deep_threat_inspection": "deepThreatInspection",
            "override": "override",
            "priority": "priority",
            "resource_arn": "resourceArn",
        },
    )
    class StatefulRuleGroupReferenceProperty:
        def __init__(
            self,
            *,
            deep_threat_inspection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            override: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFirewallPolicyPropsMixin.StatefulRuleGroupOverrideProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            priority: typing.Optional[jsii.Number] = None,
            resource_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Identifier for a single stateful rule group, used in a firewall policy to refer to a rule group.

            :param deep_threat_inspection: AWS Network Firewall plans to augment the active threat defense managed rule group with an additional deep threat inspection capability. When this capability is released, AWS will analyze service logs of network traffic processed by these rule groups to identify threat indicators across customers. AWS will use these threat indicators to improve the active threat defense managed rule groups and protect the security of AWS customers and services. .. epigraph:: Customers can opt-out of deep threat inspection at any time through the AWS Network Firewall console or API. When customers opt out, AWS Network Firewall will not use the network traffic processed by those customers' active threat defense rule groups for rule group improvement.
            :param override: The action that allows the policy owner to override the behavior of the rule group within a policy.
            :param priority: An integer setting that indicates the order in which to run the stateful rule groups in a single firewall policy. This setting only applies to firewall policies that specify the ``STRICT_ORDER`` rule order in the stateful engine options settings. Network Firewall evalutes each stateful rule group against a packet starting with the group that has the lowest priority setting. You must ensure that the priority settings are unique within each policy. You can change the priority settings of your rule groups at any time. To make it easier to insert rule groups later, number them so there's a wide range in between, for example use 100, 200, and so on.
            :param resource_arn: The Amazon Resource Name (ARN) of the stateful rule group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulrulegroupreference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                stateful_rule_group_reference_property = networkfirewall_mixins.CfnFirewallPolicyPropsMixin.StatefulRuleGroupReferenceProperty(
                    deep_threat_inspection=False,
                    override=networkfirewall_mixins.CfnFirewallPolicyPropsMixin.StatefulRuleGroupOverrideProperty(
                        action="action"
                    ),
                    priority=123,
                    resource_arn="resourceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__111763d75784aba6d58d48d327ac3f16d37b7827c4cafe5d3aafe2a0af09fa67)
                check_type(argname="argument deep_threat_inspection", value=deep_threat_inspection, expected_type=type_hints["deep_threat_inspection"])
                check_type(argname="argument override", value=override, expected_type=type_hints["override"])
                check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if deep_threat_inspection is not None:
                self._values["deep_threat_inspection"] = deep_threat_inspection
            if override is not None:
                self._values["override"] = override
            if priority is not None:
                self._values["priority"] = priority
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn

        @builtins.property
        def deep_threat_inspection(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''AWS Network Firewall plans to augment the active threat defense managed rule group with an additional deep threat inspection capability.

            When this capability is released, AWS will analyze service logs of network traffic processed by these rule groups to identify threat indicators across customers. AWS will use these threat indicators to improve the active threat defense managed rule groups and protect the security of AWS customers and services.
            .. epigraph::

               Customers can opt-out of deep threat inspection at any time through the AWS Network Firewall console or API. When customers opt out, AWS Network Firewall will not use the network traffic processed by those customers' active threat defense rule groups for rule group improvement.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulrulegroupreference.html#cfn-networkfirewall-firewallpolicy-statefulrulegroupreference-deepthreatinspection
            '''
            result = self._values.get("deep_threat_inspection")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def override(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPolicyPropsMixin.StatefulRuleGroupOverrideProperty"]]:
            '''The action that allows the policy owner to override the behavior of the rule group within a policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulrulegroupreference.html#cfn-networkfirewall-firewallpolicy-statefulrulegroupreference-override
            '''
            result = self._values.get("override")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallPolicyPropsMixin.StatefulRuleGroupOverrideProperty"]], result)

        @builtins.property
        def priority(self) -> typing.Optional[jsii.Number]:
            '''An integer setting that indicates the order in which to run the stateful rule groups in a single firewall policy.

            This setting only applies to firewall policies that specify the ``STRICT_ORDER`` rule order in the stateful engine options settings.

            Network Firewall evalutes each stateful rule group against a packet starting with the group that has the lowest priority setting. You must ensure that the priority settings are unique within each policy.

            You can change the priority settings of your rule groups at any time. To make it easier to insert rule groups later, number them so there's a wide range in between, for example use 100, 200, and so on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulrulegroupreference.html#cfn-networkfirewall-firewallpolicy-statefulrulegroupreference-priority
            '''
            result = self._values.get("priority")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the stateful rule group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulrulegroupreference.html#cfn-networkfirewall-firewallpolicy-statefulrulegroupreference-resourcearn
            '''
            result = self._values.get("resource_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatefulRuleGroupReferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnFirewallPolicyPropsMixin.StatelessRuleGroupReferenceProperty",
        jsii_struct_bases=[],
        name_mapping={"priority": "priority", "resource_arn": "resourceArn"},
    )
    class StatelessRuleGroupReferenceProperty:
        def __init__(
            self,
            *,
            priority: typing.Optional[jsii.Number] = None,
            resource_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Identifier for a single stateless rule group, used in a firewall policy to refer to the rule group.

            :param priority: An integer setting that indicates the order in which to run the stateless rule groups in a single firewall policy. Network Firewall applies each stateless rule group to a packet starting with the group that has the lowest priority setting. You must ensure that the priority settings are unique within each policy.
            :param resource_arn: The Amazon Resource Name (ARN) of the stateless rule group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statelessrulegroupreference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                stateless_rule_group_reference_property = networkfirewall_mixins.CfnFirewallPolicyPropsMixin.StatelessRuleGroupReferenceProperty(
                    priority=123,
                    resource_arn="resourceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d28939c78f092b7c561459c078e63018674cf21c9e4df68bba2eb55bceb645c4)
                check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if priority is not None:
                self._values["priority"] = priority
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn

        @builtins.property
        def priority(self) -> typing.Optional[jsii.Number]:
            '''An integer setting that indicates the order in which to run the stateless rule groups in a single firewall policy.

            Network Firewall applies each stateless rule group to a packet starting with the group that has the lowest priority setting. You must ensure that the priority settings are unique within each policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statelessrulegroupreference.html#cfn-networkfirewall-firewallpolicy-statelessrulegroupreference-priority
            '''
            result = self._values.get("priority")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the stateless rule group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statelessrulegroupreference.html#cfn-networkfirewall-firewallpolicy-statelessrulegroupreference-resourcearn
            '''
            result = self._values.get("resource_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatelessRuleGroupReferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IMixin_11e4b965)
class CfnFirewallPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnFirewallPropsMixin",
):
    '''Use the firewall to provide stateful, managed, network firewall and intrusion detection and prevention filtering for your VPCs in Amazon VPC .

    The firewall defines the configuration settings for an AWS Network Firewall firewall. The settings include the firewall policy, the subnets in your VPC to use for the firewall endpoints, and any tags that are attached to the firewall AWS resource.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html
    :cloudformationResource: AWS::NetworkFirewall::Firewall
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
        
        cfn_firewall_props_mixin = networkfirewall_mixins.CfnFirewallPropsMixin(networkfirewall_mixins.CfnFirewallMixinProps(
            availability_zone_change_protection=False,
            availability_zone_mappings=[networkfirewall_mixins.CfnFirewallPropsMixin.AvailabilityZoneMappingProperty(
                availability_zone="availabilityZone"
            )],
            delete_protection=False,
            description="description",
            enabled_analysis_types=["enabledAnalysisTypes"],
            firewall_name="firewallName",
            firewall_policy_arn="firewallPolicyArn",
            firewall_policy_change_protection=False,
            subnet_change_protection=False,
            subnet_mappings=[networkfirewall_mixins.CfnFirewallPropsMixin.SubnetMappingProperty(
                ip_address_type="ipAddressType",
                subnet_id="subnetId"
            )],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            transit_gateway_id="transitGatewayId",
            vpc_id="vpcId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnFirewallMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NetworkFirewall::Firewall``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e0d286e801016f90d4f380f69b736459a371baca385051dd9b25543b38bbfee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__08cb1224629a0e31d94f817940adc4a71ea8038c43fe560cb19af234a92e9fc3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1742574b8cf3e62b7edab37fee5aa43ef28610f4b11504fb16092fd0e9e3456e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFirewallMixinProps:
        return typing.cast(CfnFirewallMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnFirewallPropsMixin.AvailabilityZoneMappingProperty",
        jsii_struct_bases=[],
        name_mapping={"availability_zone": "availabilityZone"},
    )
    class AvailabilityZoneMappingProperty:
        def __init__(
            self,
            *,
            availability_zone: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines the mapping between an Availability Zone and a firewall endpoint for a transit gateway-attached firewall.

            Each mapping represents where the firewall can process traffic. You use these mappings when calling ``CreateFirewall`` , ``AssociateAvailabilityZones`` , and ``DisassociateAvailabilityZones`` .

            To retrieve the current Availability Zone mappings for a firewall, use ``DescribeFirewall`` .

            :param availability_zone: The ID of the Availability Zone where the firewall endpoint is located. For example, ``us-east-2a`` . The Availability Zone must be in the same Region as the transit gateway.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewall-availabilityzonemapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                availability_zone_mapping_property = networkfirewall_mixins.CfnFirewallPropsMixin.AvailabilityZoneMappingProperty(
                    availability_zone="availabilityZone"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0263862ba6a89fc8ab4c89e1666bf8fd0f3baad13e49ff11845177c3dd82c35a)
                check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if availability_zone is not None:
                self._values["availability_zone"] = availability_zone

        @builtins.property
        def availability_zone(self) -> typing.Optional[builtins.str]:
            '''The ID of the Availability Zone where the firewall endpoint is located.

            For example, ``us-east-2a`` . The Availability Zone must be in the same Region as the transit gateway.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewall-availabilityzonemapping.html#cfn-networkfirewall-firewall-availabilityzonemapping-availabilityzone
            '''
            result = self._values.get("availability_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AvailabilityZoneMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnFirewallPropsMixin.SubnetMappingProperty",
        jsii_struct_bases=[],
        name_mapping={"ip_address_type": "ipAddressType", "subnet_id": "subnetId"},
    )
    class SubnetMappingProperty:
        def __init__(
            self,
            *,
            ip_address_type: typing.Optional[builtins.str] = None,
            subnet_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ID for a subnet that you want to associate with the firewall.

            AWS Network Firewall creates an instance of the associated firewall in each subnet that you specify, to filter traffic in the subnet's Availability Zone.

            :param ip_address_type: The subnet's IP address type. You can't change the IP address type after you create the subnet.
            :param subnet_id: The unique identifier for the subnet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewall-subnetmapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                subnet_mapping_property = networkfirewall_mixins.CfnFirewallPropsMixin.SubnetMappingProperty(
                    ip_address_type="ipAddressType",
                    subnet_id="subnetId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9d9ffb21b85677289e60fd5aedae3294c0e6f82cea7b1dd1c94fe94b1cf9329d)
                check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
                check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ip_address_type is not None:
                self._values["ip_address_type"] = ip_address_type
            if subnet_id is not None:
                self._values["subnet_id"] = subnet_id

        @builtins.property
        def ip_address_type(self) -> typing.Optional[builtins.str]:
            '''The subnet's IP address type.

            You can't change the IP address type after you create the subnet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewall-subnetmapping.html#cfn-networkfirewall-firewall-subnetmapping-ipaddresstype
            '''
            result = self._values.get("ip_address_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subnet_id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier for the subnet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewall-subnetmapping.html#cfn-networkfirewall-firewall-subnetmapping-subnetid
            '''
            result = self._values.get("subnet_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubnetMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnFirewallTlsLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnFirewallTlsLogs",
):
    '''Builder for CfnFirewallLogsMixin to generate TLS_LOGS for CfnFirewall.

    :cloudformationResource: AWS::NetworkFirewall::Firewall
    :logType: TLS_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
        
        cfn_firewall_tls_logs = networkfirewall_mixins.CfnFirewallTlsLogs()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toFirehose")
    def to_firehose(
        self,
        delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
    ) -> CfnFirewallLogsMixin:
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a082025e0f2623f1ac880cf67bb1925c5a1542f565f8340d4e62ccebee53575)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast(CfnFirewallLogsMixin, jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> CfnFirewallLogsMixin:
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e217b2015025276aebd37e7b6f40a7f50f1a44304dfbb4b57f8ab0f515a5da20)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast(CfnFirewallLogsMixin, jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> CfnFirewallLogsMixin:
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92e9e0f4001a2d2095af2ca2822a04c06e661dbb403fc7b4b6edb3314f2d735b)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(CfnFirewallLogsMixin, jsii.invoke(self, "toS3", [bucket]))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnLoggingConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "enable_monitoring_dashboard": "enableMonitoringDashboard",
        "firewall_arn": "firewallArn",
        "firewall_name": "firewallName",
        "logging_configuration": "loggingConfiguration",
    },
)
class CfnLoggingConfigurationMixinProps:
    def __init__(
        self,
        *,
        enable_monitoring_dashboard: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        firewall_arn: typing.Optional[builtins.str] = None,
        firewall_name: typing.Optional[builtins.str] = None,
        logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLoggingConfigurationPropsMixin.LoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnLoggingConfigurationPropsMixin.

        :param enable_monitoring_dashboard: 
        :param firewall_arn: The Amazon Resource Name (ARN) of the firewallthat the logging configuration is associated with. You can't change the firewall specification after you create the logging configuration.
        :param firewall_name: The name of the firewall that the logging configuration is associated with. You can't change the firewall specification after you create the logging configuration.
        :param logging_configuration: Defines how AWS Network Firewall performs logging for a firewall.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-loggingconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
            
            cfn_logging_configuration_mixin_props = networkfirewall_mixins.CfnLoggingConfigurationMixinProps(
                enable_monitoring_dashboard=False,
                firewall_arn="firewallArn",
                firewall_name="firewallName",
                logging_configuration=networkfirewall_mixins.CfnLoggingConfigurationPropsMixin.LoggingConfigurationProperty(
                    log_destination_configs=[networkfirewall_mixins.CfnLoggingConfigurationPropsMixin.LogDestinationConfigProperty(
                        log_destination={
                            "log_destination_key": "logDestination"
                        },
                        log_destination_type="logDestinationType",
                        log_type="logType"
                    )]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__245810e535c34d3ddb23058ce4c2402e803560cb49a7c9eb829177f933df2bd6)
            check_type(argname="argument enable_monitoring_dashboard", value=enable_monitoring_dashboard, expected_type=type_hints["enable_monitoring_dashboard"])
            check_type(argname="argument firewall_arn", value=firewall_arn, expected_type=type_hints["firewall_arn"])
            check_type(argname="argument firewall_name", value=firewall_name, expected_type=type_hints["firewall_name"])
            check_type(argname="argument logging_configuration", value=logging_configuration, expected_type=type_hints["logging_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_monitoring_dashboard is not None:
            self._values["enable_monitoring_dashboard"] = enable_monitoring_dashboard
        if firewall_arn is not None:
            self._values["firewall_arn"] = firewall_arn
        if firewall_name is not None:
            self._values["firewall_name"] = firewall_name
        if logging_configuration is not None:
            self._values["logging_configuration"] = logging_configuration

    @builtins.property
    def enable_monitoring_dashboard(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-loggingconfiguration.html#cfn-networkfirewall-loggingconfiguration-enablemonitoringdashboard
        '''
        result = self._values.get("enable_monitoring_dashboard")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def firewall_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the firewallthat the logging configuration is associated with.

        You can't change the firewall specification after you create the logging configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-loggingconfiguration.html#cfn-networkfirewall-loggingconfiguration-firewallarn
        '''
        result = self._values.get("firewall_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firewall_name(self) -> typing.Optional[builtins.str]:
        '''The name of the firewall that the logging configuration is associated with.

        You can't change the firewall specification after you create the logging configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-loggingconfiguration.html#cfn-networkfirewall-loggingconfiguration-firewallname
        '''
        result = self._values.get("firewall_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoggingConfigurationPropsMixin.LoggingConfigurationProperty"]]:
        '''Defines how AWS Network Firewall performs logging for a firewall.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-loggingconfiguration.html#cfn-networkfirewall-loggingconfiguration-loggingconfiguration
        '''
        result = self._values.get("logging_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoggingConfigurationPropsMixin.LoggingConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLoggingConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLoggingConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnLoggingConfigurationPropsMixin",
):
    '''Use the logging configuration to define the destinations and logging options for an firewall.

    You must change the logging configuration by changing one ``LogDestinationConfig`` setting at a time in your ``LogDestinationConfigs`` .

    You can make only one of the following changes to your logging configuration resource:

    - Create a new log destination object by adding a single ``LogDestinationConfig`` array element to ``LogDestinationConfigs`` .
    - Delete a log destination object by removing a single ``LogDestinationConfig`` array element from ``LogDestinationConfigs`` .
    - Change the ``LogDestination`` setting in a single ``LogDestinationConfig`` array element.

    You can't change the ``LogDestinationType`` or ``LogType`` in a ``LogDestinationConfig`` . To change these settings, delete the existing ``LogDestinationConfig`` object and create a new one, in two separate modifications.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-loggingconfiguration.html
    :cloudformationResource: AWS::NetworkFirewall::LoggingConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
        
        cfn_logging_configuration_props_mixin = networkfirewall_mixins.CfnLoggingConfigurationPropsMixin(networkfirewall_mixins.CfnLoggingConfigurationMixinProps(
            enable_monitoring_dashboard=False,
            firewall_arn="firewallArn",
            firewall_name="firewallName",
            logging_configuration=networkfirewall_mixins.CfnLoggingConfigurationPropsMixin.LoggingConfigurationProperty(
                log_destination_configs=[networkfirewall_mixins.CfnLoggingConfigurationPropsMixin.LogDestinationConfigProperty(
                    log_destination={
                        "log_destination_key": "logDestination"
                    },
                    log_destination_type="logDestinationType",
                    log_type="logType"
                )]
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLoggingConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NetworkFirewall::LoggingConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__720c4ff7e3df87f9d00dd4af0e9508926c9ae4c0da2ff90fd94de69bed88e468)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d1be0e48d2f8196be0a0bf3626bb409a5a45db0ba37db5f963ec9f464d7d3d6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6da8d219b8d36b8c7afcccd1dc1f74a75e911993462684e234269b2ee88f4191)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLoggingConfigurationMixinProps:
        return typing.cast(CfnLoggingConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnLoggingConfigurationPropsMixin.LogDestinationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "log_destination": "logDestination",
            "log_destination_type": "logDestinationType",
            "log_type": "logType",
        },
    )
    class LogDestinationConfigProperty:
        def __init__(
            self,
            *,
            log_destination: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            log_destination_type: typing.Optional[builtins.str] = None,
            log_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines where AWS Network Firewall sends logs for the firewall for one log type.

            This is used in logging configuration. You can send each type of log to an Amazon S3 bucket, a CloudWatch log group, or a Kinesis Data Firehose delivery stream.

            Network Firewall generates logs for stateful rule groups. You can save alert and flow log types. The stateful rules engine records flow logs for all network traffic that it receives. It records alert logs for traffic that matches stateful rules that have the rule action set to ``DROP`` or ``ALERT`` .

            :param log_destination: The named location for the logs, provided in a key:value mapping that is specific to the chosen destination type. - For an Amazon S3 bucket, provide the name of the bucket, with key ``bucketName`` , and optionally provide a prefix, with key ``prefix`` . The following example specifies an Amazon S3 bucket named ``DOC-EXAMPLE-BUCKET`` and the prefix ``alerts`` : ``"LogDestination": { "bucketName": "DOC-EXAMPLE-BUCKET", "prefix": "alerts" }`` - For a CloudWatch log group, provide the name of the CloudWatch log group, with key ``logGroup`` . The following example specifies a log group named ``alert-log-group`` : ``"LogDestination": { "logGroup": "alert-log-group" }`` - For a Firehose delivery stream, provide the name of the delivery stream, with key ``deliveryStream`` . The following example specifies a delivery stream named ``alert-delivery-stream`` : ``"LogDestination": { "deliveryStream": "alert-delivery-stream" }``
            :param log_destination_type: The type of storage destination to send these logs to. You can send logs to an Amazon S3 bucket, a CloudWatch log group, or a Firehose delivery stream.
            :param log_type: The type of log to record. You can record the following types of logs from your Network Firewall stateful engine. - ``ALERT`` - Logs for traffic that matches your stateful rules and that have an action that sends an alert. A stateful rule sends alerts for the rule actions DROP, ALERT, and REJECT. For more information, see the ``StatefulRule`` property. - ``FLOW`` - Standard network traffic flow logs. The stateful rules engine records flow logs for all network traffic that it receives. Each flow log record captures the network flow for a specific standard stateless rule group. - ``TLS`` - Logs for events that are related to TLS inspection. For more information, see `Inspecting SSL/TLS traffic with TLS inspection configurations <https://docs.aws.amazon.com/network-firewall/latest/developerguide/tls-inspection-configurations.html>`_ in the *Network Firewall Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-loggingconfiguration-logdestinationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                log_destination_config_property = networkfirewall_mixins.CfnLoggingConfigurationPropsMixin.LogDestinationConfigProperty(
                    log_destination={
                        "log_destination_key": "logDestination"
                    },
                    log_destination_type="logDestinationType",
                    log_type="logType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__abc280b3a170807c53758409e41db26e22f185813326f80f4ed88e06a497f79c)
                check_type(argname="argument log_destination", value=log_destination, expected_type=type_hints["log_destination"])
                check_type(argname="argument log_destination_type", value=log_destination_type, expected_type=type_hints["log_destination_type"])
                check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_destination is not None:
                self._values["log_destination"] = log_destination
            if log_destination_type is not None:
                self._values["log_destination_type"] = log_destination_type
            if log_type is not None:
                self._values["log_type"] = log_type

        @builtins.property
        def log_destination(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The named location for the logs, provided in a key:value mapping that is specific to the chosen destination type.

            - For an Amazon S3 bucket, provide the name of the bucket, with key ``bucketName`` , and optionally provide a prefix, with key ``prefix`` .

            The following example specifies an Amazon S3 bucket named ``DOC-EXAMPLE-BUCKET`` and the prefix ``alerts`` :

            ``"LogDestination": { "bucketName": "DOC-EXAMPLE-BUCKET", "prefix": "alerts" }``

            - For a CloudWatch log group, provide the name of the CloudWatch log group, with key ``logGroup`` . The following example specifies a log group named ``alert-log-group`` :

            ``"LogDestination": { "logGroup": "alert-log-group" }``

            - For a Firehose delivery stream, provide the name of the delivery stream, with key ``deliveryStream`` . The following example specifies a delivery stream named ``alert-delivery-stream`` :

            ``"LogDestination": { "deliveryStream": "alert-delivery-stream" }``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-loggingconfiguration-logdestinationconfig.html#cfn-networkfirewall-loggingconfiguration-logdestinationconfig-logdestination
            '''
            result = self._values.get("log_destination")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def log_destination_type(self) -> typing.Optional[builtins.str]:
            '''The type of storage destination to send these logs to.

            You can send logs to an Amazon S3 bucket, a CloudWatch log group, or a Firehose delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-loggingconfiguration-logdestinationconfig.html#cfn-networkfirewall-loggingconfiguration-logdestinationconfig-logdestinationtype
            '''
            result = self._values.get("log_destination_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_type(self) -> typing.Optional[builtins.str]:
            '''The type of log to record.

            You can record the following types of logs from your Network Firewall stateful engine.

            - ``ALERT`` - Logs for traffic that matches your stateful rules and that have an action that sends an alert. A stateful rule sends alerts for the rule actions DROP, ALERT, and REJECT. For more information, see the ``StatefulRule`` property.
            - ``FLOW`` - Standard network traffic flow logs. The stateful rules engine records flow logs for all network traffic that it receives. Each flow log record captures the network flow for a specific standard stateless rule group.
            - ``TLS`` - Logs for events that are related to TLS inspection. For more information, see `Inspecting SSL/TLS traffic with TLS inspection configurations <https://docs.aws.amazon.com/network-firewall/latest/developerguide/tls-inspection-configurations.html>`_ in the *Network Firewall Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-loggingconfiguration-logdestinationconfig.html#cfn-networkfirewall-loggingconfiguration-logdestinationconfig-logtype
            '''
            result = self._values.get("log_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogDestinationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnLoggingConfigurationPropsMixin.LoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"log_destination_configs": "logDestinationConfigs"},
    )
    class LoggingConfigurationProperty:
        def __init__(
            self,
            *,
            log_destination_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLoggingConfigurationPropsMixin.LogDestinationConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Defines how AWS Network Firewall performs logging for a firewall.

            :param log_destination_configs: Defines the logging destinations for the logs for a firewall. Network Firewall generates logs for stateful rule groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-loggingconfiguration-loggingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                logging_configuration_property = networkfirewall_mixins.CfnLoggingConfigurationPropsMixin.LoggingConfigurationProperty(
                    log_destination_configs=[networkfirewall_mixins.CfnLoggingConfigurationPropsMixin.LogDestinationConfigProperty(
                        log_destination={
                            "log_destination_key": "logDestination"
                        },
                        log_destination_type="logDestinationType",
                        log_type="logType"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4806fee8d71c1c72447f041275263f084e9e571d88df98b3f8f9c1f0ab4453ce)
                check_type(argname="argument log_destination_configs", value=log_destination_configs, expected_type=type_hints["log_destination_configs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_destination_configs is not None:
                self._values["log_destination_configs"] = log_destination_configs

        @builtins.property
        def log_destination_configs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoggingConfigurationPropsMixin.LogDestinationConfigProperty"]]]]:
            '''Defines the logging destinations for the logs for a firewall.

            Network Firewall generates logs for stateful rule groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-loggingconfiguration-loggingconfiguration.html#cfn-networkfirewall-loggingconfiguration-loggingconfiguration-logdestinationconfigs
            '''
            result = self._values.get("log_destination_configs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoggingConfigurationPropsMixin.LogDestinationConfigProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "capacity": "capacity",
        "description": "description",
        "rule_group": "ruleGroup",
        "rule_group_name": "ruleGroupName",
        "summary_configuration": "summaryConfiguration",
        "tags": "tags",
        "type": "type",
    },
)
class CfnRuleGroupMixinProps:
    def __init__(
        self,
        *,
        capacity: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        rule_group: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.RuleGroupProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        rule_group_name: typing.Optional[builtins.str] = None,
        summary_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.SummaryConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnRuleGroupPropsMixin.

        :param capacity: The maximum operating resources that this rule group can use. You can't change a rule group's capacity setting after you create the rule group. When you update a rule group, you are limited to this capacity. When you reference a rule group from a firewall policy, Network Firewall reserves this capacity for the rule group.
        :param description: A description of the rule group.
        :param rule_group: An object that defines the rule group rules.
        :param rule_group_name: The descriptive name of the rule group. You can't change the name of a rule group after you create it.
        :param summary_configuration: A complex type containing the currently selected rule option fields that will be displayed for rule summarization returned by ``DescribeRuleGroupSummary`` . - The ``RuleOptions`` specified in ``SummaryConfiguration`` - Rule metadata organization preferences
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param type: Indicates whether the rule group is stateless or stateful. If the rule group is stateless, it contains stateless rules. If it is stateful, it contains stateful rules.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
            
            cfn_rule_group_mixin_props = networkfirewall_mixins.CfnRuleGroupMixinProps(
                capacity=123,
                description="description",
                rule_group=networkfirewall_mixins.CfnRuleGroupPropsMixin.RuleGroupProperty(
                    reference_sets=networkfirewall_mixins.CfnRuleGroupPropsMixin.ReferenceSetsProperty(
                        ip_set_references={
                            "ip_set_references_key": {
                                "reference_arn": "referenceArn"
                            }
                        }
                    ),
                    rules_source=networkfirewall_mixins.CfnRuleGroupPropsMixin.RulesSourceProperty(
                        rules_source_list=networkfirewall_mixins.CfnRuleGroupPropsMixin.RulesSourceListProperty(
                            generated_rules_type="generatedRulesType",
                            targets=["targets"],
                            target_types=["targetTypes"]
                        ),
                        rules_string="rulesString",
                        stateful_rules=[networkfirewall_mixins.CfnRuleGroupPropsMixin.StatefulRuleProperty(
                            action="action",
                            header=networkfirewall_mixins.CfnRuleGroupPropsMixin.HeaderProperty(
                                destination="destination",
                                destination_port="destinationPort",
                                direction="direction",
                                protocol="protocol",
                                source="source",
                                source_port="sourcePort"
                            ),
                            rule_options=[networkfirewall_mixins.CfnRuleGroupPropsMixin.RuleOptionProperty(
                                keyword="keyword",
                                settings=["settings"]
                            )]
                        )],
                        stateless_rules_and_custom_actions=networkfirewall_mixins.CfnRuleGroupPropsMixin.StatelessRulesAndCustomActionsProperty(
                            custom_actions=[networkfirewall_mixins.CfnRuleGroupPropsMixin.CustomActionProperty(
                                action_definition=networkfirewall_mixins.CfnRuleGroupPropsMixin.ActionDefinitionProperty(
                                    publish_metric_action=networkfirewall_mixins.CfnRuleGroupPropsMixin.PublishMetricActionProperty(
                                        dimensions=[networkfirewall_mixins.CfnRuleGroupPropsMixin.DimensionProperty(
                                            value="value"
                                        )]
                                    )
                                ),
                                action_name="actionName"
                            )],
                            stateless_rules=[networkfirewall_mixins.CfnRuleGroupPropsMixin.StatelessRuleProperty(
                                priority=123,
                                rule_definition=networkfirewall_mixins.CfnRuleGroupPropsMixin.RuleDefinitionProperty(
                                    actions=["actions"],
                                    match_attributes=networkfirewall_mixins.CfnRuleGroupPropsMixin.MatchAttributesProperty(
                                        destination_ports=[networkfirewall_mixins.CfnRuleGroupPropsMixin.PortRangeProperty(
                                            from_port=123,
                                            to_port=123
                                        )],
                                        destinations=[networkfirewall_mixins.CfnRuleGroupPropsMixin.AddressProperty(
                                            address_definition="addressDefinition"
                                        )],
                                        protocols=[123],
                                        source_ports=[networkfirewall_mixins.CfnRuleGroupPropsMixin.PortRangeProperty(
                                            from_port=123,
                                            to_port=123
                                        )],
                                        sources=[networkfirewall_mixins.CfnRuleGroupPropsMixin.AddressProperty(
                                            address_definition="addressDefinition"
                                        )],
                                        tcp_flags=[networkfirewall_mixins.CfnRuleGroupPropsMixin.TCPFlagFieldProperty(
                                            flags=["flags"],
                                            masks=["masks"]
                                        )]
                                    )
                                )
                            )]
                        )
                    ),
                    rule_variables=networkfirewall_mixins.CfnRuleGroupPropsMixin.RuleVariablesProperty(
                        ip_sets={
                            "ip_sets_key": {
                                "definition": ["definition"]
                            }
                        },
                        port_sets={
                            "port_sets_key": networkfirewall_mixins.CfnRuleGroupPropsMixin.PortSetProperty(
                                definition=["definition"]
                            )
                        }
                    ),
                    stateful_rule_options=networkfirewall_mixins.CfnRuleGroupPropsMixin.StatefulRuleOptionsProperty(
                        rule_order="ruleOrder"
                    )
                ),
                rule_group_name="ruleGroupName",
                summary_configuration=networkfirewall_mixins.CfnRuleGroupPropsMixin.SummaryConfigurationProperty(
                    rule_options=["ruleOptions"]
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1077e8425f59a64076268e40e48142443fda82d584f49b6e92c4d9274dbd2d9)
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument rule_group", value=rule_group, expected_type=type_hints["rule_group"])
            check_type(argname="argument rule_group_name", value=rule_group_name, expected_type=type_hints["rule_group_name"])
            check_type(argname="argument summary_configuration", value=summary_configuration, expected_type=type_hints["summary_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if capacity is not None:
            self._values["capacity"] = capacity
        if description is not None:
            self._values["description"] = description
        if rule_group is not None:
            self._values["rule_group"] = rule_group
        if rule_group_name is not None:
            self._values["rule_group_name"] = rule_group_name
        if summary_configuration is not None:
            self._values["summary_configuration"] = summary_configuration
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def capacity(self) -> typing.Optional[jsii.Number]:
        '''The maximum operating resources that this rule group can use.

        You can't change a rule group's capacity setting after you create the rule group. When you update a rule group, you are limited to this capacity. When you reference a rule group from a firewall policy, Network Firewall reserves this capacity for the rule group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-capacity
        '''
        result = self._values.get("capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the rule group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_group(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.RuleGroupProperty"]]:
        '''An object that defines the rule group rules.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroup
        '''
        result = self._values.get("rule_group")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.RuleGroupProperty"]], result)

    @builtins.property
    def rule_group_name(self) -> typing.Optional[builtins.str]:
        '''The descriptive name of the rule group.

        You can't change the name of a rule group after you create it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroupname
        '''
        result = self._values.get("rule_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def summary_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.SummaryConfigurationProperty"]]:
        '''A complex type containing the currently selected rule option fields that will be displayed for rule summarization returned by ``DescribeRuleGroupSummary`` .

        - The ``RuleOptions`` specified in ``SummaryConfiguration``
        - Rule metadata organization preferences

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-summaryconfiguration
        '''
        result = self._values.get("summary_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.SummaryConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Indicates whether the rule group is stateless or stateful.

        If the rule group is stateless, it contains
        stateless rules. If it is stateful, it contains stateful rules.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRuleGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRuleGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin",
):
    '''Use the ` <https://docs.aws.amazon.com/RuleGroup>`_ to define a reusable collection of stateless or stateful network traffic filtering rules. You use rule groups in an firewall policy to specify the filtering behavior of an firewall.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html
    :cloudformationResource: AWS::NetworkFirewall::RuleGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
        
        cfn_rule_group_props_mixin = networkfirewall_mixins.CfnRuleGroupPropsMixin(networkfirewall_mixins.CfnRuleGroupMixinProps(
            capacity=123,
            description="description",
            rule_group=networkfirewall_mixins.CfnRuleGroupPropsMixin.RuleGroupProperty(
                reference_sets=networkfirewall_mixins.CfnRuleGroupPropsMixin.ReferenceSetsProperty(
                    ip_set_references={
                        "ip_set_references_key": {
                            "reference_arn": "referenceArn"
                        }
                    }
                ),
                rules_source=networkfirewall_mixins.CfnRuleGroupPropsMixin.RulesSourceProperty(
                    rules_source_list=networkfirewall_mixins.CfnRuleGroupPropsMixin.RulesSourceListProperty(
                        generated_rules_type="generatedRulesType",
                        targets=["targets"],
                        target_types=["targetTypes"]
                    ),
                    rules_string="rulesString",
                    stateful_rules=[networkfirewall_mixins.CfnRuleGroupPropsMixin.StatefulRuleProperty(
                        action="action",
                        header=networkfirewall_mixins.CfnRuleGroupPropsMixin.HeaderProperty(
                            destination="destination",
                            destination_port="destinationPort",
                            direction="direction",
                            protocol="protocol",
                            source="source",
                            source_port="sourcePort"
                        ),
                        rule_options=[networkfirewall_mixins.CfnRuleGroupPropsMixin.RuleOptionProperty(
                            keyword="keyword",
                            settings=["settings"]
                        )]
                    )],
                    stateless_rules_and_custom_actions=networkfirewall_mixins.CfnRuleGroupPropsMixin.StatelessRulesAndCustomActionsProperty(
                        custom_actions=[networkfirewall_mixins.CfnRuleGroupPropsMixin.CustomActionProperty(
                            action_definition=networkfirewall_mixins.CfnRuleGroupPropsMixin.ActionDefinitionProperty(
                                publish_metric_action=networkfirewall_mixins.CfnRuleGroupPropsMixin.PublishMetricActionProperty(
                                    dimensions=[networkfirewall_mixins.CfnRuleGroupPropsMixin.DimensionProperty(
                                        value="value"
                                    )]
                                )
                            ),
                            action_name="actionName"
                        )],
                        stateless_rules=[networkfirewall_mixins.CfnRuleGroupPropsMixin.StatelessRuleProperty(
                            priority=123,
                            rule_definition=networkfirewall_mixins.CfnRuleGroupPropsMixin.RuleDefinitionProperty(
                                actions=["actions"],
                                match_attributes=networkfirewall_mixins.CfnRuleGroupPropsMixin.MatchAttributesProperty(
                                    destination_ports=[networkfirewall_mixins.CfnRuleGroupPropsMixin.PortRangeProperty(
                                        from_port=123,
                                        to_port=123
                                    )],
                                    destinations=[networkfirewall_mixins.CfnRuleGroupPropsMixin.AddressProperty(
                                        address_definition="addressDefinition"
                                    )],
                                    protocols=[123],
                                    source_ports=[networkfirewall_mixins.CfnRuleGroupPropsMixin.PortRangeProperty(
                                        from_port=123,
                                        to_port=123
                                    )],
                                    sources=[networkfirewall_mixins.CfnRuleGroupPropsMixin.AddressProperty(
                                        address_definition="addressDefinition"
                                    )],
                                    tcp_flags=[networkfirewall_mixins.CfnRuleGroupPropsMixin.TCPFlagFieldProperty(
                                        flags=["flags"],
                                        masks=["masks"]
                                    )]
                                )
                            )
                        )]
                    )
                ),
                rule_variables=networkfirewall_mixins.CfnRuleGroupPropsMixin.RuleVariablesProperty(
                    ip_sets={
                        "ip_sets_key": {
                            "definition": ["definition"]
                        }
                    },
                    port_sets={
                        "port_sets_key": networkfirewall_mixins.CfnRuleGroupPropsMixin.PortSetProperty(
                            definition=["definition"]
                        )
                    }
                ),
                stateful_rule_options=networkfirewall_mixins.CfnRuleGroupPropsMixin.StatefulRuleOptionsProperty(
                    rule_order="ruleOrder"
                )
            ),
            rule_group_name="ruleGroupName",
            summary_configuration=networkfirewall_mixins.CfnRuleGroupPropsMixin.SummaryConfigurationProperty(
                rule_options=["ruleOptions"]
            ),
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
        props: typing.Union[CfnRuleGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NetworkFirewall::RuleGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45de11b74c28461f6ba7aa0925ad0be2f99cc648b5fa480912c48c4ff247547e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9fba49bc98878dc0f9001f1201b9f3fd3e851e23b98d814f9403133af02ae1e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71bfa521110cc24c6d52e398b5f7fd96aa012c33d5aca3a764f9692affe68130)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRuleGroupMixinProps:
        return typing.cast(CfnRuleGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin.ActionDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"publish_metric_action": "publishMetricAction"},
    )
    class ActionDefinitionProperty:
        def __init__(
            self,
            *,
            publish_metric_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.PublishMetricActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A custom action to use in stateless rule actions settings.

            :param publish_metric_action: Stateless inspection criteria that publishes the specified metrics to Amazon CloudWatch for the matching packet. This setting defines a CloudWatch dimension value to be published. You can pair this custom action with any of the standard stateless rule actions. For example, you could pair this in a rule action with the standard action that forwards the packet for stateful inspection. Then, when a packet matches the rule, Network Firewall publishes metrics for the packet and forwards it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-actiondefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                action_definition_property = networkfirewall_mixins.CfnRuleGroupPropsMixin.ActionDefinitionProperty(
                    publish_metric_action=networkfirewall_mixins.CfnRuleGroupPropsMixin.PublishMetricActionProperty(
                        dimensions=[networkfirewall_mixins.CfnRuleGroupPropsMixin.DimensionProperty(
                            value="value"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8d576b5d835828eb320cadf2a154b753b968b0d0fa6e5a653c41aebfe3882352)
                check_type(argname="argument publish_metric_action", value=publish_metric_action, expected_type=type_hints["publish_metric_action"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if publish_metric_action is not None:
                self._values["publish_metric_action"] = publish_metric_action

        @builtins.property
        def publish_metric_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.PublishMetricActionProperty"]]:
            '''Stateless inspection criteria that publishes the specified metrics to Amazon CloudWatch for the matching packet.

            This setting defines a CloudWatch dimension value to be published.

            You can pair this custom action with any of the standard stateless rule actions. For example, you could pair this in a rule action with the standard action that forwards the packet for stateful inspection. Then, when a packet matches the rule, Network Firewall publishes metrics for the packet and forwards it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-actiondefinition.html#cfn-networkfirewall-rulegroup-actiondefinition-publishmetricaction
            '''
            result = self._values.get("publish_metric_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.PublishMetricActionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin.AddressProperty",
        jsii_struct_bases=[],
        name_mapping={"address_definition": "addressDefinition"},
    )
    class AddressProperty:
        def __init__(
            self,
            *,
            address_definition: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A single IP address specification.

            This is used in the match attributes source and destination specifications.

            :param address_definition: Specify an IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation. Network Firewall supports all address ranges for IPv4 and IPv6. Examples: - To configure Network Firewall to inspect for the IP address 192.0.2.44, specify ``192.0.2.44/32`` . - To configure Network Firewall to inspect for IP addresses from 192.0.2.0 to 192.0.2.255, specify ``192.0.2.0/24`` . - To configure Network Firewall to inspect for the IP address 1111:0000:0000:0000:0000:0000:0000:0111, specify ``1111:0000:0000:0000:0000:0000:0000:0111/128`` . - To configure Network Firewall to inspect for IP addresses from 1111:0000:0000:0000:0000:0000:0000:0000 to 1111:0000:0000:0000:ffff:ffff:ffff:ffff, specify ``1111:0000:0000:0000:0000:0000:0000:0000/64`` . For more information about CIDR notation, see the Wikipedia entry `Classless Inter-Domain Routing <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-address.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                address_property = networkfirewall_mixins.CfnRuleGroupPropsMixin.AddressProperty(
                    address_definition="addressDefinition"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__582279fd8b694c9d5bf265a5e68eb304b61bd18f8f95ea0c2b9214ab9b776647)
                check_type(argname="argument address_definition", value=address_definition, expected_type=type_hints["address_definition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address_definition is not None:
                self._values["address_definition"] = address_definition

        @builtins.property
        def address_definition(self) -> typing.Optional[builtins.str]:
            '''Specify an IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation.

            Network Firewall supports all address ranges for IPv4 and IPv6.

            Examples:

            - To configure Network Firewall to inspect for the IP address 192.0.2.44, specify ``192.0.2.44/32`` .
            - To configure Network Firewall to inspect for IP addresses from 192.0.2.0 to 192.0.2.255, specify ``192.0.2.0/24`` .
            - To configure Network Firewall to inspect for the IP address 1111:0000:0000:0000:0000:0000:0000:0111, specify ``1111:0000:0000:0000:0000:0000:0000:0111/128`` .
            - To configure Network Firewall to inspect for IP addresses from 1111:0000:0000:0000:0000:0000:0000:0000 to 1111:0000:0000:0000:ffff:ffff:ffff:ffff, specify ``1111:0000:0000:0000:0000:0000:0000:0000/64`` .

            For more information about CIDR notation, see the Wikipedia entry `Classless Inter-Domain Routing <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-address.html#cfn-networkfirewall-rulegroup-address-addressdefinition
            '''
            result = self._values.get("address_definition")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AddressProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin.CustomActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_definition": "actionDefinition",
            "action_name": "actionName",
        },
    )
    class CustomActionProperty:
        def __init__(
            self,
            *,
            action_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.ActionDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            action_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An optional, non-standard action to use for stateless packet handling.

            You can define this in addition to the standard action that you must specify.

            You define and name the custom actions that you want to be able to use, and then you reference them by name in your actions settings.

            You can use custom actions in the following places:

            - In a ``StatelessRulesAndCustomActions`` . The custom actions are available for use by name inside the ``StatelessRulesAndCustomActions`` where you define them. You can use them for your stateless rule actions to specify what to do with a packet that matches the rule's match attributes.
            - In an firewall policy specification, in ``StatelessCustomActions`` . The custom actions are available for use inside the policy where you define them. You can use them for the policy's default stateless actions settings to specify what to do with packets that don't match any of the policy's stateless rules.

            :param action_definition: The custom action associated with the action name.
            :param action_name: The descriptive name of the custom action. You can't change the name of a custom action after you create it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-customaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                custom_action_property = networkfirewall_mixins.CfnRuleGroupPropsMixin.CustomActionProperty(
                    action_definition=networkfirewall_mixins.CfnRuleGroupPropsMixin.ActionDefinitionProperty(
                        publish_metric_action=networkfirewall_mixins.CfnRuleGroupPropsMixin.PublishMetricActionProperty(
                            dimensions=[networkfirewall_mixins.CfnRuleGroupPropsMixin.DimensionProperty(
                                value="value"
                            )]
                        )
                    ),
                    action_name="actionName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b360dd8a5f7afdbad1a5e5b91c504082d7513580c6d2f9f4431c4de94b914298)
                check_type(argname="argument action_definition", value=action_definition, expected_type=type_hints["action_definition"])
                check_type(argname="argument action_name", value=action_name, expected_type=type_hints["action_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action_definition is not None:
                self._values["action_definition"] = action_definition
            if action_name is not None:
                self._values["action_name"] = action_name

        @builtins.property
        def action_definition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.ActionDefinitionProperty"]]:
            '''The custom action associated with the action name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-customaction.html#cfn-networkfirewall-rulegroup-customaction-actiondefinition
            '''
            result = self._values.get("action_definition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.ActionDefinitionProperty"]], result)

        @builtins.property
        def action_name(self) -> typing.Optional[builtins.str]:
            '''The descriptive name of the custom action.

            You can't change the name of a custom action after you create it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-customaction.html#cfn-networkfirewall-rulegroup-customaction-actionname
            '''
            result = self._values.get("action_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin.DimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value"},
    )
    class DimensionProperty:
        def __init__(self, *, value: typing.Optional[builtins.str] = None) -> None:
            '''The value to use in an Amazon CloudWatch custom metric dimension.

            This is used in the ``PublishMetrics`` custom action. A CloudWatch custom metric dimension is a name/value pair that's part of the identity of a metric.

            AWS Network Firewall sets the dimension name to ``CustomAction`` and you provide the dimension value.

            For more information about CloudWatch custom metric dimensions, see `Publishing Custom Metrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/publishingMetrics.html#usingDimensions>`_ in the `Amazon CloudWatch User Guide <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html>`_ .

            :param value: The value to use in the custom metric dimension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-dimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                dimension_property = networkfirewall_mixins.CfnRuleGroupPropsMixin.DimensionProperty(
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__02f89dba65215935a38132cb025c854127b02d024a915986deae040ee07ab242)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value to use in the custom metric dimension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-dimension.html#cfn-networkfirewall-rulegroup-dimension-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin.HeaderProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination": "destination",
            "destination_port": "destinationPort",
            "direction": "direction",
            "protocol": "protocol",
            "source": "source",
            "source_port": "sourcePort",
        },
    )
    class HeaderProperty:
        def __init__(
            self,
            *,
            destination: typing.Optional[builtins.str] = None,
            destination_port: typing.Optional[builtins.str] = None,
            direction: typing.Optional[builtins.str] = None,
            protocol: typing.Optional[builtins.str] = None,
            source: typing.Optional[builtins.str] = None,
            source_port: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The 5-tuple criteria for AWS Network Firewall to use to inspect packet headers in stateful traffic flow inspection.

            Traffic flows that match the criteria are a match for the corresponding stateful rule.

            :param destination: The destination IP address or address range to inspect for, in CIDR notation. To match with any address, specify ``ANY`` . Specify an IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation. Network Firewall supports all address ranges for IPv4 and IPv6. Examples: - To configure Network Firewall to inspect for the IP address 192.0.2.44, specify ``192.0.2.44/32`` . - To configure Network Firewall to inspect for IP addresses from 192.0.2.0 to 192.0.2.255, specify ``192.0.2.0/24`` . - To configure Network Firewall to inspect for the IP address 1111:0000:0000:0000:0000:0000:0000:0111, specify ``1111:0000:0000:0000:0000:0000:0000:0111/128`` . - To configure Network Firewall to inspect for IP addresses from 1111:0000:0000:0000:0000:0000:0000:0000 to 1111:0000:0000:0000:ffff:ffff:ffff:ffff, specify ``1111:0000:0000:0000:0000:0000:0000:0000/64`` . For more information about CIDR notation, see the Wikipedia entry `Classless Inter-Domain Routing <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`_ .
            :param destination_port: The destination port to inspect for. You can specify an individual port, for example ``1994`` and you can specify a port range, for example ``1990:1994`` . To match with any port, specify ``ANY`` .
            :param direction: The direction of traffic flow to inspect. If set to ``ANY`` , the inspection matches bidirectional traffic, both from the source to the destination and from the destination to the source. If set to ``FORWARD`` , the inspection only matches traffic going from the source to the destination.
            :param protocol: The protocol to inspect for. To specify all, you can use ``IP`` , because all traffic on AWS and on the internet is IP.
            :param source: The source IP address or address range to inspect for, in CIDR notation. To match with any address, specify ``ANY`` . Specify an IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation. Network Firewall supports all address ranges for IPv4 and IPv6. Examples: - To configure Network Firewall to inspect for the IP address 192.0.2.44, specify ``192.0.2.44/32`` . - To configure Network Firewall to inspect for IP addresses from 192.0.2.0 to 192.0.2.255, specify ``192.0.2.0/24`` . - To configure Network Firewall to inspect for the IP address 1111:0000:0000:0000:0000:0000:0000:0111, specify ``1111:0000:0000:0000:0000:0000:0000:0111/128`` . - To configure Network Firewall to inspect for IP addresses from 1111:0000:0000:0000:0000:0000:0000:0000 to 1111:0000:0000:0000:ffff:ffff:ffff:ffff, specify ``1111:0000:0000:0000:0000:0000:0000:0000/64`` . For more information about CIDR notation, see the Wikipedia entry `Classless Inter-Domain Routing <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`_ .
            :param source_port: The source port to inspect for. You can specify an individual port, for example ``1994`` and you can specify a port range, for example ``1990:1994`` . To match with any port, specify ``ANY`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-header.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                header_property = networkfirewall_mixins.CfnRuleGroupPropsMixin.HeaderProperty(
                    destination="destination",
                    destination_port="destinationPort",
                    direction="direction",
                    protocol="protocol",
                    source="source",
                    source_port="sourcePort"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__34df5b26012894fd96e59555a08a0854706d1c1b557b0e5af5e0f2eb5509c7c6)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument destination_port", value=destination_port, expected_type=type_hints["destination_port"])
                check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
                check_type(argname="argument source_port", value=source_port, expected_type=type_hints["source_port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination is not None:
                self._values["destination"] = destination
            if destination_port is not None:
                self._values["destination_port"] = destination_port
            if direction is not None:
                self._values["direction"] = direction
            if protocol is not None:
                self._values["protocol"] = protocol
            if source is not None:
                self._values["source"] = source
            if source_port is not None:
                self._values["source_port"] = source_port

        @builtins.property
        def destination(self) -> typing.Optional[builtins.str]:
            '''The destination IP address or address range to inspect for, in CIDR notation.

            To match with any address, specify ``ANY`` .

            Specify an IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation. Network Firewall supports all address ranges for IPv4 and IPv6.

            Examples:

            - To configure Network Firewall to inspect for the IP address 192.0.2.44, specify ``192.0.2.44/32`` .
            - To configure Network Firewall to inspect for IP addresses from 192.0.2.0 to 192.0.2.255, specify ``192.0.2.0/24`` .
            - To configure Network Firewall to inspect for the IP address 1111:0000:0000:0000:0000:0000:0000:0111, specify ``1111:0000:0000:0000:0000:0000:0000:0111/128`` .
            - To configure Network Firewall to inspect for IP addresses from 1111:0000:0000:0000:0000:0000:0000:0000 to 1111:0000:0000:0000:ffff:ffff:ffff:ffff, specify ``1111:0000:0000:0000:0000:0000:0000:0000/64`` .

            For more information about CIDR notation, see the Wikipedia entry `Classless Inter-Domain Routing <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-header.html#cfn-networkfirewall-rulegroup-header-destination
            '''
            result = self._values.get("destination")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def destination_port(self) -> typing.Optional[builtins.str]:
            '''The destination port to inspect for.

            You can specify an individual port, for example ``1994`` and you can specify a port range, for example ``1990:1994`` . To match with any port, specify ``ANY`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-header.html#cfn-networkfirewall-rulegroup-header-destinationport
            '''
            result = self._values.get("destination_port")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def direction(self) -> typing.Optional[builtins.str]:
            '''The direction of traffic flow to inspect.

            If set to ``ANY`` , the inspection matches bidirectional traffic, both from the source to the destination and from the destination to the source. If set to ``FORWARD`` , the inspection only matches traffic going from the source to the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-header.html#cfn-networkfirewall-rulegroup-header-direction
            '''
            result = self._values.get("direction")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The protocol to inspect for.

            To specify all, you can use ``IP`` , because all traffic on AWS and on the internet is IP.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-header.html#cfn-networkfirewall-rulegroup-header-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''The source IP address or address range to inspect for, in CIDR notation.

            To match with any address, specify ``ANY`` .

            Specify an IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation. Network Firewall supports all address ranges for IPv4 and IPv6.

            Examples:

            - To configure Network Firewall to inspect for the IP address 192.0.2.44, specify ``192.0.2.44/32`` .
            - To configure Network Firewall to inspect for IP addresses from 192.0.2.0 to 192.0.2.255, specify ``192.0.2.0/24`` .
            - To configure Network Firewall to inspect for the IP address 1111:0000:0000:0000:0000:0000:0000:0111, specify ``1111:0000:0000:0000:0000:0000:0000:0111/128`` .
            - To configure Network Firewall to inspect for IP addresses from 1111:0000:0000:0000:0000:0000:0000:0000 to 1111:0000:0000:0000:ffff:ffff:ffff:ffff, specify ``1111:0000:0000:0000:0000:0000:0000:0000/64`` .

            For more information about CIDR notation, see the Wikipedia entry `Classless Inter-Domain Routing <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-header.html#cfn-networkfirewall-rulegroup-header-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_port(self) -> typing.Optional[builtins.str]:
            '''The source port to inspect for.

            You can specify an individual port, for example ``1994`` and you can specify a port range, for example ``1990:1994`` . To match with any port, specify ``ANY`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-header.html#cfn-networkfirewall-rulegroup-header-sourceport
            '''
            result = self._values.get("source_port")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HeaderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin.IPSetProperty",
        jsii_struct_bases=[],
        name_mapping={"definition": "definition"},
    )
    class IPSetProperty:
        def __init__(
            self,
            *,
            definition: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A list of IP addresses and address ranges, in CIDR notation.

            This is part of a ``RuleVariables`` .

            :param definition: The list of IP addresses and address ranges, in CIDR notation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ipset.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                i_pSet_property = {
                    "definition": ["definition"]
                }
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e5114f02ca905bd251454978994b2462b914bff1eae8125317da0b9f7fc19e6c)
                check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if definition is not None:
                self._values["definition"] = definition

        @builtins.property
        def definition(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of IP addresses and address ranges, in CIDR notation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ipset.html#cfn-networkfirewall-rulegroup-ipset-definition
            '''
            result = self._values.get("definition")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IPSetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin.IPSetReferenceProperty",
        jsii_struct_bases=[],
        name_mapping={"reference_arn": "referenceArn"},
    )
    class IPSetReferenceProperty:
        def __init__(
            self,
            *,
            reference_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configures one or more IP set references for a Suricata-compatible rule group.

            An IP set reference is a rule variable that references a resource that you create and manage in another AWS service, such as an Amazon VPC prefix list. Network Firewall IP set references enable you to dynamically update the contents of your rules. When you create, update, or delete the IP set you are referencing in your rule, Network Firewall automatically updates the rule's content with the changes. For more information about IP set references in Network Firewall , see `Using IP set references <https://docs.aws.amazon.com/network-firewall/latest/developerguide/rule-groups-ip-set-references.html>`_ in the *Network Firewall Developer Guide* .

            :param reference_arn: The Amazon Resource Name (ARN) of the resource to include in the IP set reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ipsetreference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                i_pSet_reference_property = {
                    "reference_arn": "referenceArn"
                }
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f87516336eaf6e16b362f9194f8c9719cc80f8431ea244c6a583fee87c4eb37e)
                check_type(argname="argument reference_arn", value=reference_arn, expected_type=type_hints["reference_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if reference_arn is not None:
                self._values["reference_arn"] = reference_arn

        @builtins.property
        def reference_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the resource to include in the IP set reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ipsetreference.html#cfn-networkfirewall-rulegroup-ipsetreference-referencearn
            '''
            result = self._values.get("reference_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IPSetReferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin.MatchAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_ports": "destinationPorts",
            "destinations": "destinations",
            "protocols": "protocols",
            "source_ports": "sourcePorts",
            "sources": "sources",
            "tcp_flags": "tcpFlags",
        },
    )
    class MatchAttributesProperty:
        def __init__(
            self,
            *,
            destination_ports: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.PortRangeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            destinations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.AddressProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            protocols: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
            source_ports: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.PortRangeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.AddressProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            tcp_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.TCPFlagFieldProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Criteria for Network Firewall to use to inspect an individual packet in stateless rule inspection.

            Each match attributes set can include one or more items such as IP address, CIDR range, port number, protocol, and TCP flags.

            :param destination_ports: The destination port to inspect for. You can specify an individual port, for example ``1994`` and you can specify a port range, for example ``1990:1994`` . To match with any port, specify ``ANY`` . This setting is only used for protocols 6 (TCP) and 17 (UDP).
            :param destinations: The destination IP addresses and address ranges to inspect for, in CIDR notation. If not specified, this matches with any destination address.
            :param protocols: The protocols to inspect for, specified using the assigned internet protocol number (IANA) for each protocol. If not specified, this matches with any protocol.
            :param source_ports: The source port to inspect for. You can specify an individual port, for example ``1994`` and you can specify a port range, for example ``1990:1994`` . To match with any port, specify ``ANY`` . If not specified, this matches with any source port. This setting is only used for protocols 6 (TCP) and 17 (UDP).
            :param sources: The source IP addresses and address ranges to inspect for, in CIDR notation. If not specified, this matches with any source address.
            :param tcp_flags: The TCP flags and masks to inspect for. If not specified, this matches with any settings. This setting is only used for protocol 6 (TCP).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                match_attributes_property = networkfirewall_mixins.CfnRuleGroupPropsMixin.MatchAttributesProperty(
                    destination_ports=[networkfirewall_mixins.CfnRuleGroupPropsMixin.PortRangeProperty(
                        from_port=123,
                        to_port=123
                    )],
                    destinations=[networkfirewall_mixins.CfnRuleGroupPropsMixin.AddressProperty(
                        address_definition="addressDefinition"
                    )],
                    protocols=[123],
                    source_ports=[networkfirewall_mixins.CfnRuleGroupPropsMixin.PortRangeProperty(
                        from_port=123,
                        to_port=123
                    )],
                    sources=[networkfirewall_mixins.CfnRuleGroupPropsMixin.AddressProperty(
                        address_definition="addressDefinition"
                    )],
                    tcp_flags=[networkfirewall_mixins.CfnRuleGroupPropsMixin.TCPFlagFieldProperty(
                        flags=["flags"],
                        masks=["masks"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c7b552bdde96d6ca8d76206161f2efabc2624bc4e9932eb4ff51473cc85f6a76)
                check_type(argname="argument destination_ports", value=destination_ports, expected_type=type_hints["destination_ports"])
                check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
                check_type(argname="argument protocols", value=protocols, expected_type=type_hints["protocols"])
                check_type(argname="argument source_ports", value=source_ports, expected_type=type_hints["source_ports"])
                check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
                check_type(argname="argument tcp_flags", value=tcp_flags, expected_type=type_hints["tcp_flags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_ports is not None:
                self._values["destination_ports"] = destination_ports
            if destinations is not None:
                self._values["destinations"] = destinations
            if protocols is not None:
                self._values["protocols"] = protocols
            if source_ports is not None:
                self._values["source_ports"] = source_ports
            if sources is not None:
                self._values["sources"] = sources
            if tcp_flags is not None:
                self._values["tcp_flags"] = tcp_flags

        @builtins.property
        def destination_ports(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.PortRangeProperty"]]]]:
            '''The destination port to inspect for.

            You can specify an individual port, for example ``1994`` and you can specify a port range, for example ``1990:1994`` . To match with any port, specify ``ANY`` .

            This setting is only used for protocols 6 (TCP) and 17 (UDP).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html#cfn-networkfirewall-rulegroup-matchattributes-destinationports
            '''
            result = self._values.get("destination_ports")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.PortRangeProperty"]]]], result)

        @builtins.property
        def destinations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.AddressProperty"]]]]:
            '''The destination IP addresses and address ranges to inspect for, in CIDR notation.

            If not specified, this matches with any destination address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html#cfn-networkfirewall-rulegroup-matchattributes-destinations
            '''
            result = self._values.get("destinations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.AddressProperty"]]]], result)

        @builtins.property
        def protocols(
            self,
        ) -> typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]]:
            '''The protocols to inspect for, specified using the assigned internet protocol number (IANA) for each protocol.

            If not specified, this matches with any protocol.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html#cfn-networkfirewall-rulegroup-matchattributes-protocols
            '''
            result = self._values.get("protocols")
            return typing.cast(typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def source_ports(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.PortRangeProperty"]]]]:
            '''The source port to inspect for.

            You can specify an individual port, for example ``1994`` and you can specify a port range, for example ``1990:1994`` . To match with any port, specify ``ANY`` .

            If not specified, this matches with any source port.

            This setting is only used for protocols 6 (TCP) and 17 (UDP).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html#cfn-networkfirewall-rulegroup-matchattributes-sourceports
            '''
            result = self._values.get("source_ports")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.PortRangeProperty"]]]], result)

        @builtins.property
        def sources(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.AddressProperty"]]]]:
            '''The source IP addresses and address ranges to inspect for, in CIDR notation.

            If not specified, this matches with any source address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html#cfn-networkfirewall-rulegroup-matchattributes-sources
            '''
            result = self._values.get("sources")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.AddressProperty"]]]], result)

        @builtins.property
        def tcp_flags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.TCPFlagFieldProperty"]]]]:
            '''The TCP flags and masks to inspect for.

            If not specified, this matches with any settings. This setting is only used for protocol 6 (TCP).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html#cfn-networkfirewall-rulegroup-matchattributes-tcpflags
            '''
            result = self._values.get("tcp_flags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.TCPFlagFieldProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MatchAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin.PortRangeProperty",
        jsii_struct_bases=[],
        name_mapping={"from_port": "fromPort", "to_port": "toPort"},
    )
    class PortRangeProperty:
        def __init__(
            self,
            *,
            from_port: typing.Optional[jsii.Number] = None,
            to_port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A single port range specification.

            This is used for source and destination port ranges in the stateless match attributes.

            :param from_port: The lower limit of the port range. This must be less than or equal to the ``ToPort`` specification.
            :param to_port: The upper limit of the port range. This must be greater than or equal to the ``FromPort`` specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-portrange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                port_range_property = networkfirewall_mixins.CfnRuleGroupPropsMixin.PortRangeProperty(
                    from_port=123,
                    to_port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__003949cae8b6b57b315534b47fa99c937b85cb7c5b13103618e115117ec6c984)
                check_type(argname="argument from_port", value=from_port, expected_type=type_hints["from_port"])
                check_type(argname="argument to_port", value=to_port, expected_type=type_hints["to_port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if from_port is not None:
                self._values["from_port"] = from_port
            if to_port is not None:
                self._values["to_port"] = to_port

        @builtins.property
        def from_port(self) -> typing.Optional[jsii.Number]:
            '''The lower limit of the port range.

            This must be less than or equal to the ``ToPort`` specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-portrange.html#cfn-networkfirewall-rulegroup-portrange-fromport
            '''
            result = self._values.get("from_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def to_port(self) -> typing.Optional[jsii.Number]:
            '''The upper limit of the port range.

            This must be greater than or equal to the ``FromPort`` specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-portrange.html#cfn-networkfirewall-rulegroup-portrange-toport
            '''
            result = self._values.get("to_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin.PortSetProperty",
        jsii_struct_bases=[],
        name_mapping={"definition": "definition"},
    )
    class PortSetProperty:
        def __init__(
            self,
            *,
            definition: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A set of port ranges for use in the rules in a rule group.

            :param definition: The set of port ranges.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-portset.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                port_set_property = networkfirewall_mixins.CfnRuleGroupPropsMixin.PortSetProperty(
                    definition=["definition"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f816cd4f046d2ee1baaa3c4c18230f1071a7bf4884b956fa6e38a3d054d953ab)
                check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if definition is not None:
                self._values["definition"] = definition

        @builtins.property
        def definition(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The set of port ranges.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-portset.html#cfn-networkfirewall-rulegroup-portset-definition
            '''
            result = self._values.get("definition")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortSetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin.PublishMetricActionProperty",
        jsii_struct_bases=[],
        name_mapping={"dimensions": "dimensions"},
    )
    class PublishMetricActionProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.DimensionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Stateless inspection criteria that publishes the specified metrics to Amazon CloudWatch for the matching packet.

            This setting defines a CloudWatch dimension value to be published.

            :param dimensions: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-publishmetricaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                publish_metric_action_property = networkfirewall_mixins.CfnRuleGroupPropsMixin.PublishMetricActionProperty(
                    dimensions=[networkfirewall_mixins.CfnRuleGroupPropsMixin.DimensionProperty(
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4c181cf3d5f602c6f89bde0fd2868abd4f8b890e12cf9be9e70ee669e1a7c9f8)
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimensions is not None:
                self._values["dimensions"] = dimensions

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.DimensionProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-publishmetricaction.html#cfn-networkfirewall-rulegroup-publishmetricaction-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.DimensionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PublishMetricActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin.ReferenceSetsProperty",
        jsii_struct_bases=[],
        name_mapping={"ip_set_references": "ipSetReferences"},
    )
    class ReferenceSetsProperty:
        def __init__(
            self,
            *,
            ip_set_references: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.IPSetReferenceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Configures the reference sets for a stateful rule group.

            For more information, see the `Using IP set references in Suricata compatible rule groups <https://docs.aws.amazon.com/network-firewall/latest/developerguide/rule-groups-ip-set-references.html>`_ in the *Network Firewall User Guide* .

            :param ip_set_references: The IP set references to use in the stateful rule group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-referencesets.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                reference_sets_property = networkfirewall_mixins.CfnRuleGroupPropsMixin.ReferenceSetsProperty(
                    ip_set_references={
                        "ip_set_references_key": {
                            "reference_arn": "referenceArn"
                        }
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fbb2dbb5aa6d6845495ee9626ff66ce300ec3abdc30ee82b6bc1c42e220d7357)
                check_type(argname="argument ip_set_references", value=ip_set_references, expected_type=type_hints["ip_set_references"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ip_set_references is not None:
                self._values["ip_set_references"] = ip_set_references

        @builtins.property
        def ip_set_references(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.IPSetReferenceProperty"]]]]:
            '''The IP set references to use in the stateful rule group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-referencesets.html#cfn-networkfirewall-rulegroup-referencesets-ipsetreferences
            '''
            result = self._values.get("ip_set_references")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.IPSetReferenceProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReferenceSetsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin.RuleDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"actions": "actions", "match_attributes": "matchAttributes"},
    )
    class RuleDefinitionProperty:
        def __init__(
            self,
            *,
            actions: typing.Optional[typing.Sequence[builtins.str]] = None,
            match_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.MatchAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The inspection criteria and action for a single stateless rule.

            AWS Network Firewall inspects each packet for the specified matching criteria. When a packet matches the criteria, Network Firewall performs the rule's actions on the packet.

            :param actions: The actions to take on a packet that matches one of the stateless rule definition's match attributes. You must specify a standard action and you can add custom actions. .. epigraph:: Network Firewall only forwards a packet for stateful rule inspection if you specify ``aws:forward_to_sfe`` for a rule that the packet matches, or if the packet doesn't match any stateless rule and you specify ``aws:forward_to_sfe`` for the ``StatelessDefaultActions`` setting for the firewall policy. For every rule, you must specify exactly one of the following standard actions. - *aws:pass* - Discontinues all inspection of the packet and permits it to go to its intended destination. - *aws:drop* - Discontinues all inspection of the packet and blocks it from going to its intended destination. - *aws:forward_to_sfe* - Discontinues stateless inspection of the packet and forwards it to the stateful rule engine for inspection. Additionally, you can specify a custom action. To do this, you define a custom action by name and type, then provide the name you've assigned to the action in this ``Actions`` setting. To provide more than one action in this setting, separate the settings with a comma. For example, if you have a publish metrics custom action that you've named ``MyMetricsAction`` , then you could specify the standard action ``aws:pass`` combined with the custom action using ``[“aws:pass”, “MyMetricsAction”]`` .
            :param match_attributes: Criteria for Network Firewall to use to inspect an individual packet in stateless rule inspection. Each match attributes set can include one or more items such as IP address, CIDR range, port number, protocol, and TCP flags.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ruledefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                rule_definition_property = networkfirewall_mixins.CfnRuleGroupPropsMixin.RuleDefinitionProperty(
                    actions=["actions"],
                    match_attributes=networkfirewall_mixins.CfnRuleGroupPropsMixin.MatchAttributesProperty(
                        destination_ports=[networkfirewall_mixins.CfnRuleGroupPropsMixin.PortRangeProperty(
                            from_port=123,
                            to_port=123
                        )],
                        destinations=[networkfirewall_mixins.CfnRuleGroupPropsMixin.AddressProperty(
                            address_definition="addressDefinition"
                        )],
                        protocols=[123],
                        source_ports=[networkfirewall_mixins.CfnRuleGroupPropsMixin.PortRangeProperty(
                            from_port=123,
                            to_port=123
                        )],
                        sources=[networkfirewall_mixins.CfnRuleGroupPropsMixin.AddressProperty(
                            address_definition="addressDefinition"
                        )],
                        tcp_flags=[networkfirewall_mixins.CfnRuleGroupPropsMixin.TCPFlagFieldProperty(
                            flags=["flags"],
                            masks=["masks"]
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e77bd3b2d733609d0c4c825ca23d56491bef394c0ecc54acf00f3e09e642d716)
                check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
                check_type(argname="argument match_attributes", value=match_attributes, expected_type=type_hints["match_attributes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if actions is not None:
                self._values["actions"] = actions
            if match_attributes is not None:
                self._values["match_attributes"] = match_attributes

        @builtins.property
        def actions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The actions to take on a packet that matches one of the stateless rule definition's match attributes.

            You must specify a standard action and you can add custom actions.
            .. epigraph::

               Network Firewall only forwards a packet for stateful rule inspection if you specify ``aws:forward_to_sfe`` for a rule that the packet matches, or if the packet doesn't match any stateless rule and you specify ``aws:forward_to_sfe`` for the ``StatelessDefaultActions`` setting for the firewall policy.

            For every rule, you must specify exactly one of the following standard actions.

            - *aws:pass* - Discontinues all inspection of the packet and permits it to go to its intended destination.
            - *aws:drop* - Discontinues all inspection of the packet and blocks it from going to its intended destination.
            - *aws:forward_to_sfe* - Discontinues stateless inspection of the packet and forwards it to the stateful rule engine for inspection.

            Additionally, you can specify a custom action. To do this, you define a custom action by name and type, then provide the name you've assigned to the action in this ``Actions`` setting.

            To provide more than one action in this setting, separate the settings with a comma. For example, if you have a publish metrics custom action that you've named ``MyMetricsAction`` , then you could specify the standard action ``aws:pass`` combined with the custom action using ``[“aws:pass”, “MyMetricsAction”]`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ruledefinition.html#cfn-networkfirewall-rulegroup-ruledefinition-actions
            '''
            result = self._values.get("actions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def match_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.MatchAttributesProperty"]]:
            '''Criteria for Network Firewall to use to inspect an individual packet in stateless rule inspection.

            Each match attributes set can include one or more items such as IP address, CIDR range, port number, protocol, and TCP flags.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ruledefinition.html#cfn-networkfirewall-rulegroup-ruledefinition-matchattributes
            '''
            result = self._values.get("match_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.MatchAttributesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin.RuleGroupProperty",
        jsii_struct_bases=[],
        name_mapping={
            "reference_sets": "referenceSets",
            "rules_source": "rulesSource",
            "rule_variables": "ruleVariables",
            "stateful_rule_options": "statefulRuleOptions",
        },
    )
    class RuleGroupProperty:
        def __init__(
            self,
            *,
            reference_sets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.ReferenceSetsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rules_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.RulesSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rule_variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.RuleVariablesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            stateful_rule_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.StatefulRuleOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The object that defines the rules in a rule group.

            AWS Network Firewall uses a rule group to inspect and control network traffic. You define stateless rule groups to inspect individual packets and you define stateful rule groups to inspect packets in the context of their traffic flow.

            To use a rule group, you include it by reference in an Network Firewall firewall policy, then you use the policy in a firewall. You can reference a rule group from more than one firewall policy, and you can use a firewall policy in more than one firewall.

            :param reference_sets: The reference sets for the stateful rule group.
            :param rules_source: The stateful rules or stateless rules for the rule group.
            :param rule_variables: Settings that are available for use in the rules in the rule group. You can only use these for stateful rule groups.
            :param stateful_rule_options: Additional options governing how Network Firewall handles stateful rules. The policies where you use your stateful rule group must have stateful rule options settings that are compatible with these settings. Some limitations apply; for more information, see `Strict evaluation order <https://docs.aws.amazon.com/network-firewall/latest/developerguide/suricata-limitations-caveats.html>`_ in the *AWS Network Firewall Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulegroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                rule_group_property = networkfirewall_mixins.CfnRuleGroupPropsMixin.RuleGroupProperty(
                    reference_sets=networkfirewall_mixins.CfnRuleGroupPropsMixin.ReferenceSetsProperty(
                        ip_set_references={
                            "ip_set_references_key": {
                                "reference_arn": "referenceArn"
                            }
                        }
                    ),
                    rules_source=networkfirewall_mixins.CfnRuleGroupPropsMixin.RulesSourceProperty(
                        rules_source_list=networkfirewall_mixins.CfnRuleGroupPropsMixin.RulesSourceListProperty(
                            generated_rules_type="generatedRulesType",
                            targets=["targets"],
                            target_types=["targetTypes"]
                        ),
                        rules_string="rulesString",
                        stateful_rules=[networkfirewall_mixins.CfnRuleGroupPropsMixin.StatefulRuleProperty(
                            action="action",
                            header=networkfirewall_mixins.CfnRuleGroupPropsMixin.HeaderProperty(
                                destination="destination",
                                destination_port="destinationPort",
                                direction="direction",
                                protocol="protocol",
                                source="source",
                                source_port="sourcePort"
                            ),
                            rule_options=[networkfirewall_mixins.CfnRuleGroupPropsMixin.RuleOptionProperty(
                                keyword="keyword",
                                settings=["settings"]
                            )]
                        )],
                        stateless_rules_and_custom_actions=networkfirewall_mixins.CfnRuleGroupPropsMixin.StatelessRulesAndCustomActionsProperty(
                            custom_actions=[networkfirewall_mixins.CfnRuleGroupPropsMixin.CustomActionProperty(
                                action_definition=networkfirewall_mixins.CfnRuleGroupPropsMixin.ActionDefinitionProperty(
                                    publish_metric_action=networkfirewall_mixins.CfnRuleGroupPropsMixin.PublishMetricActionProperty(
                                        dimensions=[networkfirewall_mixins.CfnRuleGroupPropsMixin.DimensionProperty(
                                            value="value"
                                        )]
                                    )
                                ),
                                action_name="actionName"
                            )],
                            stateless_rules=[networkfirewall_mixins.CfnRuleGroupPropsMixin.StatelessRuleProperty(
                                priority=123,
                                rule_definition=networkfirewall_mixins.CfnRuleGroupPropsMixin.RuleDefinitionProperty(
                                    actions=["actions"],
                                    match_attributes=networkfirewall_mixins.CfnRuleGroupPropsMixin.MatchAttributesProperty(
                                        destination_ports=[networkfirewall_mixins.CfnRuleGroupPropsMixin.PortRangeProperty(
                                            from_port=123,
                                            to_port=123
                                        )],
                                        destinations=[networkfirewall_mixins.CfnRuleGroupPropsMixin.AddressProperty(
                                            address_definition="addressDefinition"
                                        )],
                                        protocols=[123],
                                        source_ports=[networkfirewall_mixins.CfnRuleGroupPropsMixin.PortRangeProperty(
                                            from_port=123,
                                            to_port=123
                                        )],
                                        sources=[networkfirewall_mixins.CfnRuleGroupPropsMixin.AddressProperty(
                                            address_definition="addressDefinition"
                                        )],
                                        tcp_flags=[networkfirewall_mixins.CfnRuleGroupPropsMixin.TCPFlagFieldProperty(
                                            flags=["flags"],
                                            masks=["masks"]
                                        )]
                                    )
                                )
                            )]
                        )
                    ),
                    rule_variables=networkfirewall_mixins.CfnRuleGroupPropsMixin.RuleVariablesProperty(
                        ip_sets={
                            "ip_sets_key": {
                                "definition": ["definition"]
                            }
                        },
                        port_sets={
                            "port_sets_key": networkfirewall_mixins.CfnRuleGroupPropsMixin.PortSetProperty(
                                definition=["definition"]
                            )
                        }
                    ),
                    stateful_rule_options=networkfirewall_mixins.CfnRuleGroupPropsMixin.StatefulRuleOptionsProperty(
                        rule_order="ruleOrder"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__22c95b58dd4dac1580aee1746099459d78a14b5ff4a58c2502e64397ed8d13fc)
                check_type(argname="argument reference_sets", value=reference_sets, expected_type=type_hints["reference_sets"])
                check_type(argname="argument rules_source", value=rules_source, expected_type=type_hints["rules_source"])
                check_type(argname="argument rule_variables", value=rule_variables, expected_type=type_hints["rule_variables"])
                check_type(argname="argument stateful_rule_options", value=stateful_rule_options, expected_type=type_hints["stateful_rule_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if reference_sets is not None:
                self._values["reference_sets"] = reference_sets
            if rules_source is not None:
                self._values["rules_source"] = rules_source
            if rule_variables is not None:
                self._values["rule_variables"] = rule_variables
            if stateful_rule_options is not None:
                self._values["stateful_rule_options"] = stateful_rule_options

        @builtins.property
        def reference_sets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.ReferenceSetsProperty"]]:
            '''The reference sets for the stateful rule group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroup-referencesets
            '''
            result = self._values.get("reference_sets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.ReferenceSetsProperty"]], result)

        @builtins.property
        def rules_source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.RulesSourceProperty"]]:
            '''The stateful rules or stateless rules for the rule group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroup-rulessource
            '''
            result = self._values.get("rules_source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.RulesSourceProperty"]], result)

        @builtins.property
        def rule_variables(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.RuleVariablesProperty"]]:
            '''Settings that are available for use in the rules in the rule group.

            You can only use these for stateful rule groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroup-rulevariables
            '''
            result = self._values.get("rule_variables")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.RuleVariablesProperty"]], result)

        @builtins.property
        def stateful_rule_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.StatefulRuleOptionsProperty"]]:
            '''Additional options governing how Network Firewall handles stateful rules.

            The policies where you use your stateful rule group must have stateful rule options settings that are compatible with these settings. Some limitations apply; for more information, see `Strict evaluation order <https://docs.aws.amazon.com/network-firewall/latest/developerguide/suricata-limitations-caveats.html>`_ in the *AWS Network Firewall Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroup-statefulruleoptions
            '''
            result = self._values.get("stateful_rule_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.StatefulRuleOptionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin.RuleOptionProperty",
        jsii_struct_bases=[],
        name_mapping={"keyword": "keyword", "settings": "settings"},
    )
    class RuleOptionProperty:
        def __init__(
            self,
            *,
            keyword: typing.Optional[builtins.str] = None,
            settings: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Additional settings for a stateful rule.

            :param keyword: The Suricata rule option keywords. For Network Firewall , the keyword signature ID (sid) is required in the format ``sid:112233`` . The sid must be unique within the rule group. For information about Suricata rule option keywords, see `Rule options <https://docs.aws.amazon.com/https://suricata.readthedocs.io/en/suricata-6.0.9/rules/intro.html#rule-options>`_ .
            :param settings: The Suricata rule option settings. Settings have zero or more values, and the number of possible settings and required settings depends on the keyword. The format for Settings is ``number`` . For information about Suricata rule option settings, see `Rule options <https://docs.aws.amazon.com/https://suricata.readthedocs.io/en/suricata-6.0.9/rules/intro.html#rule-options>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ruleoption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                rule_option_property = networkfirewall_mixins.CfnRuleGroupPropsMixin.RuleOptionProperty(
                    keyword="keyword",
                    settings=["settings"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__321fc71e2069453f66063c859e60aa00df5279771a5097815a4ee114e9236a0c)
                check_type(argname="argument keyword", value=keyword, expected_type=type_hints["keyword"])
                check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if keyword is not None:
                self._values["keyword"] = keyword
            if settings is not None:
                self._values["settings"] = settings

        @builtins.property
        def keyword(self) -> typing.Optional[builtins.str]:
            '''The Suricata rule option keywords.

            For Network Firewall , the keyword signature ID (sid) is required in the format ``sid:112233`` . The sid must be unique within the rule group. For information about Suricata rule option keywords, see `Rule options <https://docs.aws.amazon.com/https://suricata.readthedocs.io/en/suricata-6.0.9/rules/intro.html#rule-options>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ruleoption.html#cfn-networkfirewall-rulegroup-ruleoption-keyword
            '''
            result = self._values.get("keyword")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def settings(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The Suricata rule option settings.

            Settings have zero or more values, and the number of possible settings and required settings depends on the keyword. The format for Settings is ``number`` . For information about Suricata rule option settings, see `Rule options <https://docs.aws.amazon.com/https://suricata.readthedocs.io/en/suricata-6.0.9/rules/intro.html#rule-options>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ruleoption.html#cfn-networkfirewall-rulegroup-ruleoption-settings
            '''
            result = self._values.get("settings")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin.RuleVariablesProperty",
        jsii_struct_bases=[],
        name_mapping={"ip_sets": "ipSets", "port_sets": "portSets"},
    )
    class RuleVariablesProperty:
        def __init__(
            self,
            *,
            ip_sets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.IPSetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            port_sets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.PortSetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Settings that are available for use in the rules in the rule group where this is defined.

            :param ip_sets: A list of IP addresses and address ranges, in CIDR notation.
            :param port_sets: A list of port ranges.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulevariables.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                rule_variables_property = networkfirewall_mixins.CfnRuleGroupPropsMixin.RuleVariablesProperty(
                    ip_sets={
                        "ip_sets_key": {
                            "definition": ["definition"]
                        }
                    },
                    port_sets={
                        "port_sets_key": networkfirewall_mixins.CfnRuleGroupPropsMixin.PortSetProperty(
                            definition=["definition"]
                        )
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__24dc25df5062a3278fd486bee68b2d86c4b0d8a9e1a0413c85409758c15f04a3)
                check_type(argname="argument ip_sets", value=ip_sets, expected_type=type_hints["ip_sets"])
                check_type(argname="argument port_sets", value=port_sets, expected_type=type_hints["port_sets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ip_sets is not None:
                self._values["ip_sets"] = ip_sets
            if port_sets is not None:
                self._values["port_sets"] = port_sets

        @builtins.property
        def ip_sets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.IPSetProperty"]]]]:
            '''A list of IP addresses and address ranges, in CIDR notation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulevariables.html#cfn-networkfirewall-rulegroup-rulevariables-ipsets
            '''
            result = self._values.get("ip_sets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.IPSetProperty"]]]], result)

        @builtins.property
        def port_sets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.PortSetProperty"]]]]:
            '''A list of port ranges.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulevariables.html#cfn-networkfirewall-rulegroup-rulevariables-portsets
            '''
            result = self._values.get("port_sets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.PortSetProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleVariablesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin.RulesSourceListProperty",
        jsii_struct_bases=[],
        name_mapping={
            "generated_rules_type": "generatedRulesType",
            "targets": "targets",
            "target_types": "targetTypes",
        },
    )
    class RulesSourceListProperty:
        def __init__(
            self,
            *,
            generated_rules_type: typing.Optional[builtins.str] = None,
            targets: typing.Optional[typing.Sequence[builtins.str]] = None,
            target_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Stateful inspection criteria for a domain list rule group.

            For HTTPS traffic, domain filtering is SNI-based. It uses the server name indicator extension of the TLS handshake.

            By default, Network Firewall domain list inspection only includes traffic coming from the VPC where you deploy the firewall. To inspect traffic from IP addresses outside of the deployment VPC, you set the ``HOME_NET`` rule variable to include the CIDR range of the deployment VPC plus the other CIDR ranges. For more information, see ``RuleVariables`` in this guide and `Stateful domain list rule groups in AWS Network Firewall <https://docs.aws.amazon.com/network-firewall/latest/developerguide/stateful-rule-groups-domain-names.html>`_ in the *Network Firewall Developer Guide*

            :param generated_rules_type: Whether you want to apply allow, reject, alert, or drop behavior to the domains in your target list. .. epigraph:: When logging is enabled and you choose Alert, traffic that matches the domain specifications generates an alert in the firewall's logs. Then, traffic either passes, is rejected, or drops based on other rules in the firewall policy.
            :param targets: The domains that you want to inspect for in your traffic flows. Valid domain specifications are the following:. - Explicit names. For example, ``abc.example.com`` matches only the domain ``abc.example.com`` . - Names that use a domain wildcard, which you indicate with an initial ' ``.`` '. For example, ``.example.com`` matches ``example.com`` and matches all subdomains of ``example.com`` , such as ``abc.example.com`` and ``www.example.com`` .
            :param target_types: The types of targets to inspect for. Valid values are ``TLS_SNI`` and ``HTTP_HOST`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessourcelist.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                rules_source_list_property = networkfirewall_mixins.CfnRuleGroupPropsMixin.RulesSourceListProperty(
                    generated_rules_type="generatedRulesType",
                    targets=["targets"],
                    target_types=["targetTypes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d470e6e0cec23d203bb70a7cd31401e80c209421494df6da465a75fa3ecb690a)
                check_type(argname="argument generated_rules_type", value=generated_rules_type, expected_type=type_hints["generated_rules_type"])
                check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
                check_type(argname="argument target_types", value=target_types, expected_type=type_hints["target_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if generated_rules_type is not None:
                self._values["generated_rules_type"] = generated_rules_type
            if targets is not None:
                self._values["targets"] = targets
            if target_types is not None:
                self._values["target_types"] = target_types

        @builtins.property
        def generated_rules_type(self) -> typing.Optional[builtins.str]:
            '''Whether you want to apply allow, reject, alert, or drop behavior to the domains in your target list.

            .. epigraph::

               When logging is enabled and you choose Alert, traffic that matches the domain specifications generates an alert in the firewall's logs. Then, traffic either passes, is rejected, or drops based on other rules in the firewall policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessourcelist.html#cfn-networkfirewall-rulegroup-rulessourcelist-generatedrulestype
            '''
            result = self._values.get("generated_rules_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def targets(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The domains that you want to inspect for in your traffic flows. Valid domain specifications are the following:.

            - Explicit names. For example, ``abc.example.com`` matches only the domain ``abc.example.com`` .
            - Names that use a domain wildcard, which you indicate with an initial ' ``.`` '. For example, ``.example.com`` matches ``example.com`` and matches all subdomains of ``example.com`` , such as ``abc.example.com`` and ``www.example.com`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessourcelist.html#cfn-networkfirewall-rulegroup-rulessourcelist-targets
            '''
            result = self._values.get("targets")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def target_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The types of targets to inspect for.

            Valid values are ``TLS_SNI`` and ``HTTP_HOST`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessourcelist.html#cfn-networkfirewall-rulegroup-rulessourcelist-targettypes
            '''
            result = self._values.get("target_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RulesSourceListProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin.RulesSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "rules_source_list": "rulesSourceList",
            "rules_string": "rulesString",
            "stateful_rules": "statefulRules",
            "stateless_rules_and_custom_actions": "statelessRulesAndCustomActions",
        },
    )
    class RulesSourceProperty:
        def __init__(
            self,
            *,
            rules_source_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.RulesSourceListProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rules_string: typing.Optional[builtins.str] = None,
            stateful_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.StatefulRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            stateless_rules_and_custom_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.StatelessRulesAndCustomActionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The stateless or stateful rules definitions for use in a single rule group.

            Each rule group requires a single ``RulesSource`` . You can use an instance of this for either stateless rules or stateful rules.

            :param rules_source_list: Stateful inspection criteria for a domain list rule group.
            :param rules_string: Stateful inspection criteria, provided in Suricata compatible rules. Suricata is an open-source threat detection framework that includes a standard rule-based language for network traffic inspection. These rules contain the inspection criteria and the action to take for traffic that matches the criteria, so this type of rule group doesn't have a separate action setting. .. epigraph:: You can't use the ``priority`` keyword if the ``RuleOrder`` option in StatefulRuleOptions is set to ``STRICT_ORDER`` .
            :param stateful_rules: An array of individual stateful rules inspection criteria to be used together in a stateful rule group. Use this option to specify simple Suricata rules with protocol, source and destination, ports, direction, and rule options. For information about the Suricata ``Rules`` format, see `Rules Format <https://docs.aws.amazon.com/https://suricata.readthedocs.io/en/suricata-7.0.3/rules/intro.html>`_ .
            :param stateless_rules_and_custom_actions: Stateless inspection criteria to be used in a stateless rule group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                rules_source_property = networkfirewall_mixins.CfnRuleGroupPropsMixin.RulesSourceProperty(
                    rules_source_list=networkfirewall_mixins.CfnRuleGroupPropsMixin.RulesSourceListProperty(
                        generated_rules_type="generatedRulesType",
                        targets=["targets"],
                        target_types=["targetTypes"]
                    ),
                    rules_string="rulesString",
                    stateful_rules=[networkfirewall_mixins.CfnRuleGroupPropsMixin.StatefulRuleProperty(
                        action="action",
                        header=networkfirewall_mixins.CfnRuleGroupPropsMixin.HeaderProperty(
                            destination="destination",
                            destination_port="destinationPort",
                            direction="direction",
                            protocol="protocol",
                            source="source",
                            source_port="sourcePort"
                        ),
                        rule_options=[networkfirewall_mixins.CfnRuleGroupPropsMixin.RuleOptionProperty(
                            keyword="keyword",
                            settings=["settings"]
                        )]
                    )],
                    stateless_rules_and_custom_actions=networkfirewall_mixins.CfnRuleGroupPropsMixin.StatelessRulesAndCustomActionsProperty(
                        custom_actions=[networkfirewall_mixins.CfnRuleGroupPropsMixin.CustomActionProperty(
                            action_definition=networkfirewall_mixins.CfnRuleGroupPropsMixin.ActionDefinitionProperty(
                                publish_metric_action=networkfirewall_mixins.CfnRuleGroupPropsMixin.PublishMetricActionProperty(
                                    dimensions=[networkfirewall_mixins.CfnRuleGroupPropsMixin.DimensionProperty(
                                        value="value"
                                    )]
                                )
                            ),
                            action_name="actionName"
                        )],
                        stateless_rules=[networkfirewall_mixins.CfnRuleGroupPropsMixin.StatelessRuleProperty(
                            priority=123,
                            rule_definition=networkfirewall_mixins.CfnRuleGroupPropsMixin.RuleDefinitionProperty(
                                actions=["actions"],
                                match_attributes=networkfirewall_mixins.CfnRuleGroupPropsMixin.MatchAttributesProperty(
                                    destination_ports=[networkfirewall_mixins.CfnRuleGroupPropsMixin.PortRangeProperty(
                                        from_port=123,
                                        to_port=123
                                    )],
                                    destinations=[networkfirewall_mixins.CfnRuleGroupPropsMixin.AddressProperty(
                                        address_definition="addressDefinition"
                                    )],
                                    protocols=[123],
                                    source_ports=[networkfirewall_mixins.CfnRuleGroupPropsMixin.PortRangeProperty(
                                        from_port=123,
                                        to_port=123
                                    )],
                                    sources=[networkfirewall_mixins.CfnRuleGroupPropsMixin.AddressProperty(
                                        address_definition="addressDefinition"
                                    )],
                                    tcp_flags=[networkfirewall_mixins.CfnRuleGroupPropsMixin.TCPFlagFieldProperty(
                                        flags=["flags"],
                                        masks=["masks"]
                                    )]
                                )
                            )
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aae4a49c455e0531f8b16acaa55d3e9259e1477fccf003668f7015bb822ae8ec)
                check_type(argname="argument rules_source_list", value=rules_source_list, expected_type=type_hints["rules_source_list"])
                check_type(argname="argument rules_string", value=rules_string, expected_type=type_hints["rules_string"])
                check_type(argname="argument stateful_rules", value=stateful_rules, expected_type=type_hints["stateful_rules"])
                check_type(argname="argument stateless_rules_and_custom_actions", value=stateless_rules_and_custom_actions, expected_type=type_hints["stateless_rules_and_custom_actions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rules_source_list is not None:
                self._values["rules_source_list"] = rules_source_list
            if rules_string is not None:
                self._values["rules_string"] = rules_string
            if stateful_rules is not None:
                self._values["stateful_rules"] = stateful_rules
            if stateless_rules_and_custom_actions is not None:
                self._values["stateless_rules_and_custom_actions"] = stateless_rules_and_custom_actions

        @builtins.property
        def rules_source_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.RulesSourceListProperty"]]:
            '''Stateful inspection criteria for a domain list rule group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessource.html#cfn-networkfirewall-rulegroup-rulessource-rulessourcelist
            '''
            result = self._values.get("rules_source_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.RulesSourceListProperty"]], result)

        @builtins.property
        def rules_string(self) -> typing.Optional[builtins.str]:
            '''Stateful inspection criteria, provided in Suricata compatible rules.

            Suricata is an open-source threat detection framework that includes a standard rule-based language for network traffic inspection.

            These rules contain the inspection criteria and the action to take for traffic that matches the criteria, so this type of rule group doesn't have a separate action setting.
            .. epigraph::

               You can't use the ``priority`` keyword if the ``RuleOrder`` option in StatefulRuleOptions is set to ``STRICT_ORDER`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessource.html#cfn-networkfirewall-rulegroup-rulessource-rulesstring
            '''
            result = self._values.get("rules_string")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stateful_rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.StatefulRuleProperty"]]]]:
            '''An array of individual stateful rules inspection criteria to be used together in a stateful rule group.

            Use this option to specify simple Suricata rules with protocol, source and destination, ports, direction, and rule options. For information about the Suricata ``Rules`` format, see `Rules Format <https://docs.aws.amazon.com/https://suricata.readthedocs.io/en/suricata-7.0.3/rules/intro.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessource.html#cfn-networkfirewall-rulegroup-rulessource-statefulrules
            '''
            result = self._values.get("stateful_rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.StatefulRuleProperty"]]]], result)

        @builtins.property
        def stateless_rules_and_custom_actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.StatelessRulesAndCustomActionsProperty"]]:
            '''Stateless inspection criteria to be used in a stateless rule group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessource.html#cfn-networkfirewall-rulegroup-rulessource-statelessrulesandcustomactions
            '''
            result = self._values.get("stateless_rules_and_custom_actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.StatelessRulesAndCustomActionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RulesSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin.StatefulRuleOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"rule_order": "ruleOrder"},
    )
    class StatefulRuleOptionsProperty:
        def __init__(self, *, rule_order: typing.Optional[builtins.str] = None) -> None:
            '''Additional options governing how Network Firewall handles the rule group.

            You can only use these for stateful rule groups.

            :param rule_order: Indicates how to manage the order of the rule evaluation for the rule group. ``DEFAULT_ACTION_ORDER`` is the default behavior. Stateful rules are provided to the rule engine as Suricata compatible strings, and Suricata evaluates them based on certain settings. For more information, see `Evaluation order for stateful rules <https://docs.aws.amazon.com/network-firewall/latest/developerguide/suricata-rule-evaluation-order.html>`_ in the *AWS Network Firewall Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statefulruleoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                stateful_rule_options_property = networkfirewall_mixins.CfnRuleGroupPropsMixin.StatefulRuleOptionsProperty(
                    rule_order="ruleOrder"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__83272891c7571d49700e7b0cd1be91da27283ed251b8fda68cb5847b6b3635bb)
                check_type(argname="argument rule_order", value=rule_order, expected_type=type_hints["rule_order"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rule_order is not None:
                self._values["rule_order"] = rule_order

        @builtins.property
        def rule_order(self) -> typing.Optional[builtins.str]:
            '''Indicates how to manage the order of the rule evaluation for the rule group.

            ``DEFAULT_ACTION_ORDER`` is the default behavior. Stateful rules are provided to the rule engine as Suricata compatible strings, and Suricata evaluates them based on certain settings. For more information, see `Evaluation order for stateful rules <https://docs.aws.amazon.com/network-firewall/latest/developerguide/suricata-rule-evaluation-order.html>`_ in the *AWS Network Firewall Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statefulruleoptions.html#cfn-networkfirewall-rulegroup-statefulruleoptions-ruleorder
            '''
            result = self._values.get("rule_order")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatefulRuleOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin.StatefulRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "header": "header",
            "rule_options": "ruleOptions",
        },
    )
    class StatefulRuleProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            header: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.HeaderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rule_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.RuleOptionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A single Suricata rules specification, for use in a stateful rule group.

            Use this option to specify a simple Suricata rule with protocol, source and destination, ports, direction, and rule options. For information about the Suricata ``Rules`` format, see `Rules Format <https://docs.aws.amazon.com/https://suricata.readthedocs.io/en/suricata-7.0.3/rules/intro.html>`_ .

            :param action: Defines what Network Firewall should do with the packets in a traffic flow when the flow matches the stateful rule criteria. For all actions, Network Firewall performs the specified action and discontinues stateful inspection of the traffic flow. The actions for a stateful rule are defined as follows: - *PASS* - Permits the packets to go to the intended destination. - *DROP* - Blocks the packets from going to the intended destination and sends an alert log message, if alert logging is configured in the firewall logging configuration. - *REJECT* - Drops traffic that matches the conditions of the stateful rule and sends a TCP reset packet back to sender of the packet. A TCP reset packet is a packet with no payload and a ``RST`` bit contained in the TCP header flags. ``REJECT`` is available only for TCP traffic. - *ALERT* - Permits the packets to go to the intended destination and sends an alert log message, if alert logging is configured in the firewall logging configuration. You can use this action to test a rule that you intend to use to drop traffic. You can enable the rule with ``ALERT`` action, verify in the logs that the rule is filtering as you want, then change the action to ``DROP`` . - *REJECT* - Drops TCP traffic that matches the conditions of the stateful rule, and sends a TCP reset packet back to sender of the packet. A TCP reset packet is a packet with no payload and a ``RST`` bit contained in the TCP header flags. Also sends an alert log mesage if alert logging is configured in the firewall logging configuration. ``REJECT`` isn't currently available for use with IMAP and FTP protocols.
            :param header: The stateful inspection criteria for this rule, used to inspect traffic flows.
            :param rule_options: Additional settings for a stateful rule, provided as keywords and settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statefulrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                stateful_rule_property = networkfirewall_mixins.CfnRuleGroupPropsMixin.StatefulRuleProperty(
                    action="action",
                    header=networkfirewall_mixins.CfnRuleGroupPropsMixin.HeaderProperty(
                        destination="destination",
                        destination_port="destinationPort",
                        direction="direction",
                        protocol="protocol",
                        source="source",
                        source_port="sourcePort"
                    ),
                    rule_options=[networkfirewall_mixins.CfnRuleGroupPropsMixin.RuleOptionProperty(
                        keyword="keyword",
                        settings=["settings"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fa2d4ccc582ba35249d17ad56b90bc0b4c49d75cd83aea0a4754bb89ce2d4cec)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument header", value=header, expected_type=type_hints["header"])
                check_type(argname="argument rule_options", value=rule_options, expected_type=type_hints["rule_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if header is not None:
                self._values["header"] = header
            if rule_options is not None:
                self._values["rule_options"] = rule_options

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''Defines what Network Firewall should do with the packets in a traffic flow when the flow matches the stateful rule criteria.

            For all actions, Network Firewall performs the specified action and discontinues stateful inspection of the traffic flow.

            The actions for a stateful rule are defined as follows:

            - *PASS* - Permits the packets to go to the intended destination.
            - *DROP* - Blocks the packets from going to the intended destination and sends an alert log message, if alert logging is configured in the firewall logging configuration.
            - *REJECT* - Drops traffic that matches the conditions of the stateful rule and sends a TCP reset packet back to sender of the packet. A TCP reset packet is a packet with no payload and a ``RST`` bit contained in the TCP header flags. ``REJECT`` is available only for TCP traffic.
            - *ALERT* - Permits the packets to go to the intended destination and sends an alert log message, if alert logging is configured in the firewall logging configuration.

            You can use this action to test a rule that you intend to use to drop traffic. You can enable the rule with ``ALERT`` action, verify in the logs that the rule is filtering as you want, then change the action to ``DROP`` .

            - *REJECT* - Drops TCP traffic that matches the conditions of the stateful rule, and sends a TCP reset packet back to sender of the packet. A TCP reset packet is a packet with no payload and a ``RST`` bit contained in the TCP header flags. Also sends an alert log mesage if alert logging is configured in the firewall logging configuration.

            ``REJECT`` isn't currently available for use with IMAP and FTP protocols.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statefulrule.html#cfn-networkfirewall-rulegroup-statefulrule-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def header(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.HeaderProperty"]]:
            '''The stateful inspection criteria for this rule, used to inspect traffic flows.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statefulrule.html#cfn-networkfirewall-rulegroup-statefulrule-header
            '''
            result = self._values.get("header")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.HeaderProperty"]], result)

        @builtins.property
        def rule_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.RuleOptionProperty"]]]]:
            '''Additional settings for a stateful rule, provided as keywords and settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statefulrule.html#cfn-networkfirewall-rulegroup-statefulrule-ruleoptions
            '''
            result = self._values.get("rule_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.RuleOptionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatefulRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin.StatelessRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"priority": "priority", "rule_definition": "ruleDefinition"},
    )
    class StatelessRuleProperty:
        def __init__(
            self,
            *,
            priority: typing.Optional[jsii.Number] = None,
            rule_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.RuleDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A single stateless rule.

            This is used in ``StatelessRulesAndCustomActions`` .

            :param priority: Indicates the order in which to run this rule relative to all of the rules that are defined for a stateless rule group. Network Firewall evaluates the rules in a rule group starting with the lowest priority setting. You must ensure that the priority settings are unique for the rule group. Each stateless rule group uses exactly one ``StatelessRulesAndCustomActions`` object, and each ``StatelessRulesAndCustomActions`` contains exactly one ``StatelessRules`` object. To ensure unique priority settings for your rule groups, set unique priorities for the stateless rules that you define inside any single ``StatelessRules`` object. You can change the priority settings of your rules at any time. To make it easier to insert rules later, number them so there's a wide range in between, for example use 100, 200, and so on.
            :param rule_definition: Defines the stateless 5-tuple packet inspection criteria and the action to take on a packet that matches the criteria.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statelessrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                stateless_rule_property = networkfirewall_mixins.CfnRuleGroupPropsMixin.StatelessRuleProperty(
                    priority=123,
                    rule_definition=networkfirewall_mixins.CfnRuleGroupPropsMixin.RuleDefinitionProperty(
                        actions=["actions"],
                        match_attributes=networkfirewall_mixins.CfnRuleGroupPropsMixin.MatchAttributesProperty(
                            destination_ports=[networkfirewall_mixins.CfnRuleGroupPropsMixin.PortRangeProperty(
                                from_port=123,
                                to_port=123
                            )],
                            destinations=[networkfirewall_mixins.CfnRuleGroupPropsMixin.AddressProperty(
                                address_definition="addressDefinition"
                            )],
                            protocols=[123],
                            source_ports=[networkfirewall_mixins.CfnRuleGroupPropsMixin.PortRangeProperty(
                                from_port=123,
                                to_port=123
                            )],
                            sources=[networkfirewall_mixins.CfnRuleGroupPropsMixin.AddressProperty(
                                address_definition="addressDefinition"
                            )],
                            tcp_flags=[networkfirewall_mixins.CfnRuleGroupPropsMixin.TCPFlagFieldProperty(
                                flags=["flags"],
                                masks=["masks"]
                            )]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3b1cccfd0cba28e6bdbb65ef005ef4a9d85468a0c608e6821f9ef74ebf44e022)
                check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
                check_type(argname="argument rule_definition", value=rule_definition, expected_type=type_hints["rule_definition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if priority is not None:
                self._values["priority"] = priority
            if rule_definition is not None:
                self._values["rule_definition"] = rule_definition

        @builtins.property
        def priority(self) -> typing.Optional[jsii.Number]:
            '''Indicates the order in which to run this rule relative to all of the rules that are defined for a stateless rule group.

            Network Firewall evaluates the rules in a rule group starting with the lowest priority setting. You must ensure that the priority settings are unique for the rule group.

            Each stateless rule group uses exactly one ``StatelessRulesAndCustomActions`` object, and each ``StatelessRulesAndCustomActions`` contains exactly one ``StatelessRules`` object. To ensure unique priority settings for your rule groups, set unique priorities for the stateless rules that you define inside any single ``StatelessRules`` object.

            You can change the priority settings of your rules at any time. To make it easier to insert rules later, number them so there's a wide range in between, for example use 100, 200, and so on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statelessrule.html#cfn-networkfirewall-rulegroup-statelessrule-priority
            '''
            result = self._values.get("priority")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def rule_definition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.RuleDefinitionProperty"]]:
            '''Defines the stateless 5-tuple packet inspection criteria and the action to take on a packet that matches the criteria.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statelessrule.html#cfn-networkfirewall-rulegroup-statelessrule-ruledefinition
            '''
            result = self._values.get("rule_definition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.RuleDefinitionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatelessRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin.StatelessRulesAndCustomActionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_actions": "customActions",
            "stateless_rules": "statelessRules",
        },
    )
    class StatelessRulesAndCustomActionsProperty:
        def __init__(
            self,
            *,
            custom_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.CustomActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            stateless_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRuleGroupPropsMixin.StatelessRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Stateless inspection criteria.

            Each stateless rule group uses exactly one of these data types to define its stateless rules.

            :param custom_actions: Defines an array of individual custom action definitions that are available for use by the stateless rules in this ``StatelessRulesAndCustomActions`` specification. You name each custom action that you define, and then you can use it by name in your stateless rule definition ``Actions`` specification.
            :param stateless_rules: Defines the set of stateless rules for use in a stateless rule group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statelessrulesandcustomactions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                stateless_rules_and_custom_actions_property = networkfirewall_mixins.CfnRuleGroupPropsMixin.StatelessRulesAndCustomActionsProperty(
                    custom_actions=[networkfirewall_mixins.CfnRuleGroupPropsMixin.CustomActionProperty(
                        action_definition=networkfirewall_mixins.CfnRuleGroupPropsMixin.ActionDefinitionProperty(
                            publish_metric_action=networkfirewall_mixins.CfnRuleGroupPropsMixin.PublishMetricActionProperty(
                                dimensions=[networkfirewall_mixins.CfnRuleGroupPropsMixin.DimensionProperty(
                                    value="value"
                                )]
                            )
                        ),
                        action_name="actionName"
                    )],
                    stateless_rules=[networkfirewall_mixins.CfnRuleGroupPropsMixin.StatelessRuleProperty(
                        priority=123,
                        rule_definition=networkfirewall_mixins.CfnRuleGroupPropsMixin.RuleDefinitionProperty(
                            actions=["actions"],
                            match_attributes=networkfirewall_mixins.CfnRuleGroupPropsMixin.MatchAttributesProperty(
                                destination_ports=[networkfirewall_mixins.CfnRuleGroupPropsMixin.PortRangeProperty(
                                    from_port=123,
                                    to_port=123
                                )],
                                destinations=[networkfirewall_mixins.CfnRuleGroupPropsMixin.AddressProperty(
                                    address_definition="addressDefinition"
                                )],
                                protocols=[123],
                                source_ports=[networkfirewall_mixins.CfnRuleGroupPropsMixin.PortRangeProperty(
                                    from_port=123,
                                    to_port=123
                                )],
                                sources=[networkfirewall_mixins.CfnRuleGroupPropsMixin.AddressProperty(
                                    address_definition="addressDefinition"
                                )],
                                tcp_flags=[networkfirewall_mixins.CfnRuleGroupPropsMixin.TCPFlagFieldProperty(
                                    flags=["flags"],
                                    masks=["masks"]
                                )]
                            )
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ea8e055da435e7152805c51abf3767ef52ef9c9b1c6dc5c8c7d30c25babf4f96)
                check_type(argname="argument custom_actions", value=custom_actions, expected_type=type_hints["custom_actions"])
                check_type(argname="argument stateless_rules", value=stateless_rules, expected_type=type_hints["stateless_rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_actions is not None:
                self._values["custom_actions"] = custom_actions
            if stateless_rules is not None:
                self._values["stateless_rules"] = stateless_rules

        @builtins.property
        def custom_actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.CustomActionProperty"]]]]:
            '''Defines an array of individual custom action definitions that are available for use by the stateless rules in this ``StatelessRulesAndCustomActions`` specification.

            You name each custom action that you define, and then you can use it by name in your stateless rule definition ``Actions`` specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statelessrulesandcustomactions.html#cfn-networkfirewall-rulegroup-statelessrulesandcustomactions-customactions
            '''
            result = self._values.get("custom_actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.CustomActionProperty"]]]], result)

        @builtins.property
        def stateless_rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.StatelessRuleProperty"]]]]:
            '''Defines the set of stateless rules for use in a stateless rule group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statelessrulesandcustomactions.html#cfn-networkfirewall-rulegroup-statelessrulesandcustomactions-statelessrules
            '''
            result = self._values.get("stateless_rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRuleGroupPropsMixin.StatelessRuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatelessRulesAndCustomActionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin.SummaryConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"rule_options": "ruleOptions"},
    )
    class SummaryConfigurationProperty:
        def __init__(
            self,
            *,
            rule_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A complex type that specifies which Suricata rule metadata fields to use when displaying threat information. Contains:.

            - ``RuleOptions`` - The Suricata rule options fields to extract and display

            These settings affect how threat information appears in both the console and API responses. Summaries are available for rule groups you manage and for active threat defense AWS managed rule groups.

            :param rule_options: Specifies the selected rule options returned by ``DescribeRuleGroupSummary`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-summaryconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                summary_configuration_property = networkfirewall_mixins.CfnRuleGroupPropsMixin.SummaryConfigurationProperty(
                    rule_options=["ruleOptions"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ae730268952b3591a348bec3baed6c17c673725465b875f350f1b618951ace13)
                check_type(argname="argument rule_options", value=rule_options, expected_type=type_hints["rule_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rule_options is not None:
                self._values["rule_options"] = rule_options

        @builtins.property
        def rule_options(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the selected rule options returned by ``DescribeRuleGroupSummary`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-summaryconfiguration.html#cfn-networkfirewall-rulegroup-summaryconfiguration-ruleoptions
            '''
            result = self._values.get("rule_options")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SummaryConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnRuleGroupPropsMixin.TCPFlagFieldProperty",
        jsii_struct_bases=[],
        name_mapping={"flags": "flags", "masks": "masks"},
    )
    class TCPFlagFieldProperty:
        def __init__(
            self,
            *,
            flags: typing.Optional[typing.Sequence[builtins.str]] = None,
            masks: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''TCP flags and masks to inspect packets for. This is used in the match attributes specification.

            For example:

            ``"TCPFlags": [ { "Flags": [ "ECE", "SYN" ], "Masks": [ "SYN", "ECE" ] } ]``

            :param flags: Used in conjunction with the ``Masks`` setting to define the flags that must be set and flags that must not be set in order for the packet to match. This setting can only specify values that are also specified in the ``Masks`` setting. For the flags that are specified in the masks setting, the following must be true for the packet to match: - The ones that are set in this flags setting must be set in the packet. - The ones that are not set in this flags setting must also not be set in the packet.
            :param masks: The set of flags to consider in the inspection. To inspect all flags in the valid values list, leave this with no setting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-tcpflagfield.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                t_cPFlag_field_property = networkfirewall_mixins.CfnRuleGroupPropsMixin.TCPFlagFieldProperty(
                    flags=["flags"],
                    masks=["masks"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9014b92cd323283d65c1c96fc693e1fcb76dbaf041e7c7a8cc65c62d1eb7f508)
                check_type(argname="argument flags", value=flags, expected_type=type_hints["flags"])
                check_type(argname="argument masks", value=masks, expected_type=type_hints["masks"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if flags is not None:
                self._values["flags"] = flags
            if masks is not None:
                self._values["masks"] = masks

        @builtins.property
        def flags(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Used in conjunction with the ``Masks`` setting to define the flags that must be set and flags that must not be set in order for the packet to match.

            This setting can only specify values that are also specified in the ``Masks`` setting.

            For the flags that are specified in the masks setting, the following must be true for the packet to match:

            - The ones that are set in this flags setting must be set in the packet.
            - The ones that are not set in this flags setting must also not be set in the packet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-tcpflagfield.html#cfn-networkfirewall-rulegroup-tcpflagfield-flags
            '''
            result = self._values.get("flags")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def masks(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The set of flags to consider in the inspection.

            To inspect all flags in the valid values list, leave this with no setting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-tcpflagfield.html#cfn-networkfirewall-rulegroup-tcpflagfield-masks
            '''
            result = self._values.get("masks")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TCPFlagFieldProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnTLSInspectionConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "tags": "tags",
        "tls_inspection_configuration": "tlsInspectionConfiguration",
        "tls_inspection_configuration_name": "tlsInspectionConfigurationName",
    },
)
class CfnTLSInspectionConfigurationMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        tls_inspection_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTLSInspectionConfigurationPropsMixin.TLSInspectionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tls_inspection_configuration_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTLSInspectionConfigurationPropsMixin.

        :param description: A description of the TLS inspection configuration.
        :param tags: The key:value pairs to associate with the resource.
        :param tls_inspection_configuration: The object that defines a TLS inspection configuration. AWS Network Firewall uses TLS inspection configurations to decrypt your firewall's inbound and outbound SSL/TLS traffic. After decryption, AWS Network Firewall inspects the traffic according to your firewall policy's stateful rules, and then re-encrypts it before sending it to its destination. You can enable inspection of your firewall's inbound traffic, outbound traffic, or both. To use TLS inspection with your firewall, you must first import or provision certificates using Certificate Manager , create a TLS inspection configuration, add that configuration to a new firewall policy, and then associate that policy with your firewall. For more information about using TLS inspection configurations, see `Inspecting SSL/TLS traffic with TLS inspection configurations <https://docs.aws.amazon.com/network-firewall/latest/developerguide/tls-inspection.html>`_ in the *AWS Network Firewall Developer Guide* .
        :param tls_inspection_configuration_name: The descriptive name of the TLS inspection configuration. You can't change the name of a TLS inspection configuration after you create it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-tlsinspectionconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
            
            cfn_tLSInspection_configuration_mixin_props = networkfirewall_mixins.CfnTLSInspectionConfigurationMixinProps(
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                tls_inspection_configuration=networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.TLSInspectionConfigurationProperty(
                    server_certificate_configurations=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.ServerCertificateConfigurationProperty(
                        certificate_authority_arn="certificateAuthorityArn",
                        check_certificate_revocation_status=networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.CheckCertificateRevocationStatusProperty(
                            revoked_status_action="revokedStatusAction",
                            unknown_status_action="unknownStatusAction"
                        ),
                        scopes=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.ServerCertificateScopeProperty(
                            destination_ports=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.PortRangeProperty(
                                from_port=123,
                                to_port=123
                            )],
                            destinations=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.AddressProperty(
                                address_definition="addressDefinition"
                            )],
                            protocols=[123],
                            source_ports=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.PortRangeProperty(
                                from_port=123,
                                to_port=123
                            )],
                            sources=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.AddressProperty(
                                address_definition="addressDefinition"
                            )]
                        )],
                        server_certificates=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.ServerCertificateProperty(
                            resource_arn="resourceArn"
                        )]
                    )]
                ),
                tls_inspection_configuration_name="tlsInspectionConfigurationName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8539d566a73df40a780e01a3f9331c6f673e834d78590860d1f860a2fe578bdf)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tls_inspection_configuration", value=tls_inspection_configuration, expected_type=type_hints["tls_inspection_configuration"])
            check_type(argname="argument tls_inspection_configuration_name", value=tls_inspection_configuration_name, expected_type=type_hints["tls_inspection_configuration_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags
        if tls_inspection_configuration is not None:
            self._values["tls_inspection_configuration"] = tls_inspection_configuration
        if tls_inspection_configuration_name is not None:
            self._values["tls_inspection_configuration_name"] = tls_inspection_configuration_name

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the TLS inspection configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-tlsinspectionconfiguration.html#cfn-networkfirewall-tlsinspectionconfiguration-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The key:value pairs to associate with the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-tlsinspectionconfiguration.html#cfn-networkfirewall-tlsinspectionconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def tls_inspection_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTLSInspectionConfigurationPropsMixin.TLSInspectionConfigurationProperty"]]:
        '''The object that defines a TLS inspection configuration.

        AWS Network Firewall uses TLS inspection configurations to decrypt your firewall's inbound and outbound SSL/TLS traffic. After decryption, AWS Network Firewall inspects the traffic according to your firewall policy's stateful rules, and then re-encrypts it before sending it to its destination. You can enable inspection of your firewall's inbound traffic, outbound traffic, or both. To use TLS inspection with your firewall, you must first import or provision certificates using Certificate Manager , create a TLS inspection configuration, add that configuration to a new firewall policy, and then associate that policy with your firewall. For more information about using TLS inspection configurations, see `Inspecting SSL/TLS traffic with TLS inspection configurations <https://docs.aws.amazon.com/network-firewall/latest/developerguide/tls-inspection.html>`_ in the *AWS Network Firewall Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-tlsinspectionconfiguration.html#cfn-networkfirewall-tlsinspectionconfiguration-tlsinspectionconfiguration
        '''
        result = self._values.get("tls_inspection_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTLSInspectionConfigurationPropsMixin.TLSInspectionConfigurationProperty"]], result)

    @builtins.property
    def tls_inspection_configuration_name(self) -> typing.Optional[builtins.str]:
        '''The descriptive name of the TLS inspection configuration.

        You can't change the name of a TLS inspection configuration after you create it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-tlsinspectionconfiguration.html#cfn-networkfirewall-tlsinspectionconfiguration-tlsinspectionconfigurationname
        '''
        result = self._values.get("tls_inspection_configuration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTLSInspectionConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTLSInspectionConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnTLSInspectionConfigurationPropsMixin",
):
    '''The object that defines a TLS inspection configuration.

    AWS Network Firewall uses a TLS inspection configuration to decrypt traffic. Network Firewall re-encrypts the traffic before sending it to its destination.

    To use a TLS inspection configuration, you add it to a new Network Firewall firewall policy, then you apply the firewall policy to a firewall. Network Firewall acts as a proxy service to decrypt and inspect the traffic traveling through your firewalls. You can reference a TLS inspection configuration from more than one firewall policy, and you can use a firewall policy in more than one firewall. For more information about using TLS inspection configurations, see `Inspecting SSL/TLS traffic with TLS inspection configurations <https://docs.aws.amazon.com/network-firewall/latest/developerguide/tls-inspection.html>`_ in the *AWS Network Firewall Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-tlsinspectionconfiguration.html
    :cloudformationResource: AWS::NetworkFirewall::TLSInspectionConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
        
        cfn_tLSInspection_configuration_props_mixin = networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin(networkfirewall_mixins.CfnTLSInspectionConfigurationMixinProps(
            description="description",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            tls_inspection_configuration=networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.TLSInspectionConfigurationProperty(
                server_certificate_configurations=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.ServerCertificateConfigurationProperty(
                    certificate_authority_arn="certificateAuthorityArn",
                    check_certificate_revocation_status=networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.CheckCertificateRevocationStatusProperty(
                        revoked_status_action="revokedStatusAction",
                        unknown_status_action="unknownStatusAction"
                    ),
                    scopes=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.ServerCertificateScopeProperty(
                        destination_ports=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.PortRangeProperty(
                            from_port=123,
                            to_port=123
                        )],
                        destinations=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.AddressProperty(
                            address_definition="addressDefinition"
                        )],
                        protocols=[123],
                        source_ports=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.PortRangeProperty(
                            from_port=123,
                            to_port=123
                        )],
                        sources=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.AddressProperty(
                            address_definition="addressDefinition"
                        )]
                    )],
                    server_certificates=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.ServerCertificateProperty(
                        resource_arn="resourceArn"
                    )]
                )]
            ),
            tls_inspection_configuration_name="tlsInspectionConfigurationName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTLSInspectionConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NetworkFirewall::TLSInspectionConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71fe682c8679ee9743a68bf04f25c4a67119bf74fc8414b896011e5276e372c3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d89f94eb2fb5af0c8013b249d4ed2157064f07fb297247c3a1b8405a6564c53b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49fe9947d7ea6504fda002120498e41f98a980f278bb79c478abc1bf6d77b4cf)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTLSInspectionConfigurationMixinProps:
        return typing.cast(CfnTLSInspectionConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnTLSInspectionConfigurationPropsMixin.AddressProperty",
        jsii_struct_bases=[],
        name_mapping={"address_definition": "addressDefinition"},
    )
    class AddressProperty:
        def __init__(
            self,
            *,
            address_definition: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A single IP address specification.

            This is used in the `MatchAttributes <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html>`_ source and destination settings.

            :param address_definition: Specify an IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation. Network Firewall supports all address ranges for IPv4 and IPv6. Examples: - To configure Network Firewall to inspect for the IP address 192.0.2.44, specify ``192.0.2.44/32`` . - To configure Network Firewall to inspect for IP addresses from 192.0.2.0 to 192.0.2.255, specify ``192.0.2.0/24`` . - To configure Network Firewall to inspect for the IP address 1111:0000:0000:0000:0000:0000:0000:0111, specify ``1111:0000:0000:0000:0000:0000:0000:0111/128`` . - To configure Network Firewall to inspect for IP addresses from 1111:0000:0000:0000:0000:0000:0000:0000 to 1111:0000:0000:0000:ffff:ffff:ffff:ffff, specify ``1111:0000:0000:0000:0000:0000:0000:0000/64`` . For more information about CIDR notation, see the Wikipedia entry `Classless Inter-Domain Routing <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-tlsinspectionconfiguration-address.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                address_property = networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.AddressProperty(
                    address_definition="addressDefinition"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d6ed246a8e1789f5be43e8601ad0ad1996f2af6a9c5c79d201d79cd4768e629a)
                check_type(argname="argument address_definition", value=address_definition, expected_type=type_hints["address_definition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address_definition is not None:
                self._values["address_definition"] = address_definition

        @builtins.property
        def address_definition(self) -> typing.Optional[builtins.str]:
            '''Specify an IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation.

            Network Firewall supports all address ranges for IPv4 and IPv6.

            Examples:

            - To configure Network Firewall to inspect for the IP address 192.0.2.44, specify ``192.0.2.44/32`` .
            - To configure Network Firewall to inspect for IP addresses from 192.0.2.0 to 192.0.2.255, specify ``192.0.2.0/24`` .
            - To configure Network Firewall to inspect for the IP address 1111:0000:0000:0000:0000:0000:0000:0111, specify ``1111:0000:0000:0000:0000:0000:0000:0111/128`` .
            - To configure Network Firewall to inspect for IP addresses from 1111:0000:0000:0000:0000:0000:0000:0000 to 1111:0000:0000:0000:ffff:ffff:ffff:ffff, specify ``1111:0000:0000:0000:0000:0000:0000:0000/64`` .

            For more information about CIDR notation, see the Wikipedia entry `Classless Inter-Domain Routing <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-tlsinspectionconfiguration-address.html#cfn-networkfirewall-tlsinspectionconfiguration-address-addressdefinition
            '''
            result = self._values.get("address_definition")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AddressProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnTLSInspectionConfigurationPropsMixin.CheckCertificateRevocationStatusProperty",
        jsii_struct_bases=[],
        name_mapping={
            "revoked_status_action": "revokedStatusAction",
            "unknown_status_action": "unknownStatusAction",
        },
    )
    class CheckCertificateRevocationStatusProperty:
        def __init__(
            self,
            *,
            revoked_status_action: typing.Optional[builtins.str] = None,
            unknown_status_action: typing.Optional[builtins.str] = None,
        ) -> None:
            '''When enabled, Network Firewall checks if the server certificate presented by the server in the SSL/TLS connection has a revoked or unkown status.

            If the certificate has an unknown or revoked status, you must specify the actions that Network Firewall takes on outbound traffic. To check the certificate revocation status, you must also specify a ``CertificateAuthorityArn`` in `ServerCertificateConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-networkfirewall-servercertificateconfiguration.html>`_ .

            :param revoked_status_action: Configures how Network Firewall processes traffic when it determines that the certificate presented by the server in the SSL/TLS connection has a revoked status. - *PASS* - Allow the connection to continue, and pass subsequent packets to the stateful engine for inspection. - *DROP* - Network Firewall closes the connection and drops subsequent packets for that connection. - *REJECT* - Network Firewall sends a TCP reject packet back to your client. The service closes the connection and drops subsequent packets for that connection. ``REJECT`` is available only for TCP traffic.
            :param unknown_status_action: Configures how Network Firewall processes traffic when it determines that the certificate presented by the server in the SSL/TLS connection has an unknown status, or a status that cannot be determined for any other reason, including when the service is unable to connect to the OCSP and CRL endpoints for the certificate. - *PASS* - Allow the connection to continue, and pass subsequent packets to the stateful engine for inspection. - *DROP* - Network Firewall closes the connection and drops subsequent packets for that connection. - *REJECT* - Network Firewall sends a TCP reject packet back to your client. The service closes the connection and drops subsequent packets for that connection. ``REJECT`` is available only for TCP traffic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-tlsinspectionconfiguration-checkcertificaterevocationstatus.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                check_certificate_revocation_status_property = networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.CheckCertificateRevocationStatusProperty(
                    revoked_status_action="revokedStatusAction",
                    unknown_status_action="unknownStatusAction"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c6074a3e0e9c555fee51df6f3791a877cd56797bf815cb680ceaee75904fb6b3)
                check_type(argname="argument revoked_status_action", value=revoked_status_action, expected_type=type_hints["revoked_status_action"])
                check_type(argname="argument unknown_status_action", value=unknown_status_action, expected_type=type_hints["unknown_status_action"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if revoked_status_action is not None:
                self._values["revoked_status_action"] = revoked_status_action
            if unknown_status_action is not None:
                self._values["unknown_status_action"] = unknown_status_action

        @builtins.property
        def revoked_status_action(self) -> typing.Optional[builtins.str]:
            '''Configures how Network Firewall processes traffic when it determines that the certificate presented by the server in the SSL/TLS connection has a revoked status.

            - *PASS* - Allow the connection to continue, and pass subsequent packets to the stateful engine for inspection.
            - *DROP* - Network Firewall closes the connection and drops subsequent packets for that connection.
            - *REJECT* - Network Firewall sends a TCP reject packet back to your client. The service closes the connection and drops subsequent packets for that connection. ``REJECT`` is available only for TCP traffic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-tlsinspectionconfiguration-checkcertificaterevocationstatus.html#cfn-networkfirewall-tlsinspectionconfiguration-checkcertificaterevocationstatus-revokedstatusaction
            '''
            result = self._values.get("revoked_status_action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unknown_status_action(self) -> typing.Optional[builtins.str]:
            '''Configures how Network Firewall processes traffic when it determines that the certificate presented by the server in the SSL/TLS connection has an unknown status, or a status that cannot be determined for any other reason, including when the service is unable to connect to the OCSP and CRL endpoints for the certificate.

            - *PASS* - Allow the connection to continue, and pass subsequent packets to the stateful engine for inspection.
            - *DROP* - Network Firewall closes the connection and drops subsequent packets for that connection.
            - *REJECT* - Network Firewall sends a TCP reject packet back to your client. The service closes the connection and drops subsequent packets for that connection. ``REJECT`` is available only for TCP traffic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-tlsinspectionconfiguration-checkcertificaterevocationstatus.html#cfn-networkfirewall-tlsinspectionconfiguration-checkcertificaterevocationstatus-unknownstatusaction
            '''
            result = self._values.get("unknown_status_action")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CheckCertificateRevocationStatusProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnTLSInspectionConfigurationPropsMixin.PortRangeProperty",
        jsii_struct_bases=[],
        name_mapping={"from_port": "fromPort", "to_port": "toPort"},
    )
    class PortRangeProperty:
        def __init__(
            self,
            *,
            from_port: typing.Optional[jsii.Number] = None,
            to_port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A single port range specification.

            This is used for source and destination port ranges in the stateless rule `MatchAttributes <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html>`_ , ``SourcePorts`` , and ``DestinationPorts`` settings.

            :param from_port: The lower limit of the port range. This must be less than or equal to the ``ToPort`` specification.
            :param to_port: The upper limit of the port range. This must be greater than or equal to the ``FromPort`` specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-tlsinspectionconfiguration-portrange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                port_range_property = networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.PortRangeProperty(
                    from_port=123,
                    to_port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3454ffc185333ea95af8150da666cce972edce0ca66ce1eb05cda87a6db88f41)
                check_type(argname="argument from_port", value=from_port, expected_type=type_hints["from_port"])
                check_type(argname="argument to_port", value=to_port, expected_type=type_hints["to_port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if from_port is not None:
                self._values["from_port"] = from_port
            if to_port is not None:
                self._values["to_port"] = to_port

        @builtins.property
        def from_port(self) -> typing.Optional[jsii.Number]:
            '''The lower limit of the port range.

            This must be less than or equal to the ``ToPort`` specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-tlsinspectionconfiguration-portrange.html#cfn-networkfirewall-tlsinspectionconfiguration-portrange-fromport
            '''
            result = self._values.get("from_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def to_port(self) -> typing.Optional[jsii.Number]:
            '''The upper limit of the port range.

            This must be greater than or equal to the ``FromPort`` specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-tlsinspectionconfiguration-portrange.html#cfn-networkfirewall-tlsinspectionconfiguration-portrange-toport
            '''
            result = self._values.get("to_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnTLSInspectionConfigurationPropsMixin.ServerCertificateConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_authority_arn": "certificateAuthorityArn",
            "check_certificate_revocation_status": "checkCertificateRevocationStatus",
            "scopes": "scopes",
            "server_certificates": "serverCertificates",
        },
    )
    class ServerCertificateConfigurationProperty:
        def __init__(
            self,
            *,
            certificate_authority_arn: typing.Optional[builtins.str] = None,
            check_certificate_revocation_status: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTLSInspectionConfigurationPropsMixin.CheckCertificateRevocationStatusProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            scopes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTLSInspectionConfigurationPropsMixin.ServerCertificateScopeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            server_certificates: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTLSInspectionConfigurationPropsMixin.ServerCertificateProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Configures the Certificate Manager certificates and scope that Network Firewall uses to decrypt and re-encrypt traffic using a `TLSInspectionConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-networkfirewall-tlsinspectionconfiguration.html>`_ . You can configure ``ServerCertificates`` for inbound SSL/TLS inspection, a ``CertificateAuthorityArn`` for outbound SSL/TLS inspection, or both. For information about working with certificates for TLS inspection, see `Using SSL/TLS server certficiates with TLS inspection configurations <https://docs.aws.amazon.com/network-firewall/latest/developerguide/tls-inspection-certificate-requirements.html>`_ in the *AWS Network Firewall Developer Guide* .

            .. epigraph::

               If a server certificate that's associated with your `TLSInspectionConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-networkfirewall-tlsinspectionconfiguration.html>`_ is revoked, deleted, or expired it can result in client-side TLS errors.

            :param certificate_authority_arn: The Amazon Resource Name (ARN) of the imported certificate authority (CA) certificate within Certificate Manager (ACM) to use for outbound SSL/TLS inspection. The following limitations apply: - You can use CA certificates that you imported into ACM, but you can't generate CA certificates with ACM. - You can't use certificates issued by Private Certificate Authority . For more information about configuring certificates for outbound inspection, see `Using SSL/TLS certificates with TLS inspection configurations <https://docs.aws.amazon.com/network-firewall/latest/developerguide/tls-inspection-certificate-requirements.html>`_ in the *AWS Network Firewall Developer Guide* . For information about working with certificates in ACM, see `Importing certificates <https://docs.aws.amazon.com/acm/latest/userguide/import-certificate.html>`_ in the *Certificate Manager User Guide* .
            :param check_certificate_revocation_status: When enabled, Network Firewall checks if the server certificate presented by the server in the SSL/TLS connection has a revoked or unkown status. If the certificate has an unknown or revoked status, you must specify the actions that Network Firewall takes on outbound traffic. To check the certificate revocation status, you must also specify a ``CertificateAuthorityArn`` in `ServerCertificateConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-networkfirewall-servercertificateconfiguration.html>`_ .
            :param scopes: A list of scopes.
            :param server_certificates: The list of server certificates to use for inbound SSL/TLS inspection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-tlsinspectionconfiguration-servercertificateconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                server_certificate_configuration_property = networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.ServerCertificateConfigurationProperty(
                    certificate_authority_arn="certificateAuthorityArn",
                    check_certificate_revocation_status=networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.CheckCertificateRevocationStatusProperty(
                        revoked_status_action="revokedStatusAction",
                        unknown_status_action="unknownStatusAction"
                    ),
                    scopes=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.ServerCertificateScopeProperty(
                        destination_ports=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.PortRangeProperty(
                            from_port=123,
                            to_port=123
                        )],
                        destinations=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.AddressProperty(
                            address_definition="addressDefinition"
                        )],
                        protocols=[123],
                        source_ports=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.PortRangeProperty(
                            from_port=123,
                            to_port=123
                        )],
                        sources=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.AddressProperty(
                            address_definition="addressDefinition"
                        )]
                    )],
                    server_certificates=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.ServerCertificateProperty(
                        resource_arn="resourceArn"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d686d935ec1f1cd0fc1e9cf7586e76255bbd4bc35bd497b5da701dcae471a33c)
                check_type(argname="argument certificate_authority_arn", value=certificate_authority_arn, expected_type=type_hints["certificate_authority_arn"])
                check_type(argname="argument check_certificate_revocation_status", value=check_certificate_revocation_status, expected_type=type_hints["check_certificate_revocation_status"])
                check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
                check_type(argname="argument server_certificates", value=server_certificates, expected_type=type_hints["server_certificates"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_authority_arn is not None:
                self._values["certificate_authority_arn"] = certificate_authority_arn
            if check_certificate_revocation_status is not None:
                self._values["check_certificate_revocation_status"] = check_certificate_revocation_status
            if scopes is not None:
                self._values["scopes"] = scopes
            if server_certificates is not None:
                self._values["server_certificates"] = server_certificates

        @builtins.property
        def certificate_authority_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the imported certificate authority (CA) certificate within Certificate Manager (ACM) to use for outbound SSL/TLS inspection.

            The following limitations apply:

            - You can use CA certificates that you imported into ACM, but you can't generate CA certificates with ACM.
            - You can't use certificates issued by Private Certificate Authority .

            For more information about configuring certificates for outbound inspection, see `Using SSL/TLS certificates with TLS inspection configurations <https://docs.aws.amazon.com/network-firewall/latest/developerguide/tls-inspection-certificate-requirements.html>`_ in the *AWS Network Firewall Developer Guide* .

            For information about working with certificates in ACM, see `Importing certificates <https://docs.aws.amazon.com/acm/latest/userguide/import-certificate.html>`_ in the *Certificate Manager User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-tlsinspectionconfiguration-servercertificateconfiguration.html#cfn-networkfirewall-tlsinspectionconfiguration-servercertificateconfiguration-certificateauthorityarn
            '''
            result = self._values.get("certificate_authority_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def check_certificate_revocation_status(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTLSInspectionConfigurationPropsMixin.CheckCertificateRevocationStatusProperty"]]:
            '''When enabled, Network Firewall checks if the server certificate presented by the server in the SSL/TLS connection has a revoked or unkown status.

            If the certificate has an unknown or revoked status, you must specify the actions that Network Firewall takes on outbound traffic. To check the certificate revocation status, you must also specify a ``CertificateAuthorityArn`` in `ServerCertificateConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-networkfirewall-servercertificateconfiguration.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-tlsinspectionconfiguration-servercertificateconfiguration.html#cfn-networkfirewall-tlsinspectionconfiguration-servercertificateconfiguration-checkcertificaterevocationstatus
            '''
            result = self._values.get("check_certificate_revocation_status")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTLSInspectionConfigurationPropsMixin.CheckCertificateRevocationStatusProperty"]], result)

        @builtins.property
        def scopes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTLSInspectionConfigurationPropsMixin.ServerCertificateScopeProperty"]]]]:
            '''A list of scopes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-tlsinspectionconfiguration-servercertificateconfiguration.html#cfn-networkfirewall-tlsinspectionconfiguration-servercertificateconfiguration-scopes
            '''
            result = self._values.get("scopes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTLSInspectionConfigurationPropsMixin.ServerCertificateScopeProperty"]]]], result)

        @builtins.property
        def server_certificates(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTLSInspectionConfigurationPropsMixin.ServerCertificateProperty"]]]]:
            '''The list of server certificates to use for inbound SSL/TLS inspection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-tlsinspectionconfiguration-servercertificateconfiguration.html#cfn-networkfirewall-tlsinspectionconfiguration-servercertificateconfiguration-servercertificates
            '''
            result = self._values.get("server_certificates")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTLSInspectionConfigurationPropsMixin.ServerCertificateProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerCertificateConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnTLSInspectionConfigurationPropsMixin.ServerCertificateProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn"},
    )
    class ServerCertificateProperty:
        def __init__(
            self,
            *,
            resource_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Any Certificate Manager (ACM) Secure Sockets Layer/Transport Layer Security (SSL/TLS) server certificate that's associated with a `ServerCertificateConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-tlsinspectionconfiguration-servercertificateconfiguration.html>`_ . Used in a `TLSInspectionConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-networkfirewall-tlsinspectionconfiguration.html>`_ for inspection of inbound traffic to your firewall. You must request or import a SSL/TLS certificate into ACM for each domain Network Firewall needs to decrypt and inspect. AWS Network Firewall uses the SSL/TLS certificates to decrypt specified inbound SSL/TLS traffic going to your firewall. For information about working with certificates in Certificate Manager , see `Request a public certificate <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-public.html>`_ or `Importing certificates <https://docs.aws.amazon.com/acm/latest/userguide/import-certificate.html>`_ in the *Certificate Manager User Guide* .

            :param resource_arn: The Amazon Resource Name (ARN) of the Certificate Manager SSL/TLS server certificate that's used for inbound SSL/TLS inspection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-tlsinspectionconfiguration-servercertificate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                server_certificate_property = networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.ServerCertificateProperty(
                    resource_arn="resourceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d953b45b3767036981264adc61dc947ff70ac7236b35b3b600122c1b08a18d91)
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Certificate Manager SSL/TLS server certificate that's used for inbound SSL/TLS inspection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-tlsinspectionconfiguration-servercertificate.html#cfn-networkfirewall-tlsinspectionconfiguration-servercertificate-resourcearn
            '''
            result = self._values.get("resource_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerCertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnTLSInspectionConfigurationPropsMixin.ServerCertificateScopeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_ports": "destinationPorts",
            "destinations": "destinations",
            "protocols": "protocols",
            "source_ports": "sourcePorts",
            "sources": "sources",
        },
    )
    class ServerCertificateScopeProperty:
        def __init__(
            self,
            *,
            destination_ports: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTLSInspectionConfigurationPropsMixin.PortRangeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            destinations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTLSInspectionConfigurationPropsMixin.AddressProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            protocols: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
            source_ports: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTLSInspectionConfigurationPropsMixin.PortRangeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTLSInspectionConfigurationPropsMixin.AddressProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Settings that define the Secure Sockets Layer/Transport Layer Security (SSL/TLS) traffic that Network Firewall should decrypt for inspection by the stateful rule engine.

            :param destination_ports: The destination ports to decrypt for inspection, in Transmission Control Protocol (TCP) format. If not specified, this matches with any destination port. You can specify individual ports, for example ``1994`` , and you can specify port ranges, such as ``1990:1994`` .
            :param destinations: The destination IP addresses and address ranges to decrypt for inspection, in CIDR notation. If not specified, this matches with any destination address.
            :param protocols: The protocols to inspect for, specified using the assigned internet protocol number (IANA) for each protocol. If not specified, this matches with any protocol. Network Firewall currently supports only TCP.
            :param source_ports: The source ports to decrypt for inspection, in Transmission Control Protocol (TCP) format. If not specified, this matches with any source port. You can specify individual ports, for example ``1994`` , and you can specify port ranges, such as ``1990:1994`` .
            :param sources: The source IP addresses and address ranges to decrypt for inspection, in CIDR notation. If not specified, this matches with any source address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-tlsinspectionconfiguration-servercertificatescope.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                server_certificate_scope_property = networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.ServerCertificateScopeProperty(
                    destination_ports=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.PortRangeProperty(
                        from_port=123,
                        to_port=123
                    )],
                    destinations=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.AddressProperty(
                        address_definition="addressDefinition"
                    )],
                    protocols=[123],
                    source_ports=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.PortRangeProperty(
                        from_port=123,
                        to_port=123
                    )],
                    sources=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.AddressProperty(
                        address_definition="addressDefinition"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1accef2069e367c209447736ed390ceaf1e64b0b44479537156ee7ef4e099142)
                check_type(argname="argument destination_ports", value=destination_ports, expected_type=type_hints["destination_ports"])
                check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
                check_type(argname="argument protocols", value=protocols, expected_type=type_hints["protocols"])
                check_type(argname="argument source_ports", value=source_ports, expected_type=type_hints["source_ports"])
                check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_ports is not None:
                self._values["destination_ports"] = destination_ports
            if destinations is not None:
                self._values["destinations"] = destinations
            if protocols is not None:
                self._values["protocols"] = protocols
            if source_ports is not None:
                self._values["source_ports"] = source_ports
            if sources is not None:
                self._values["sources"] = sources

        @builtins.property
        def destination_ports(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTLSInspectionConfigurationPropsMixin.PortRangeProperty"]]]]:
            '''The destination ports to decrypt for inspection, in Transmission Control Protocol (TCP) format.

            If not specified, this matches with any destination port.

            You can specify individual ports, for example ``1994`` , and you can specify port ranges, such as ``1990:1994`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-tlsinspectionconfiguration-servercertificatescope.html#cfn-networkfirewall-tlsinspectionconfiguration-servercertificatescope-destinationports
            '''
            result = self._values.get("destination_ports")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTLSInspectionConfigurationPropsMixin.PortRangeProperty"]]]], result)

        @builtins.property
        def destinations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTLSInspectionConfigurationPropsMixin.AddressProperty"]]]]:
            '''The destination IP addresses and address ranges to decrypt for inspection, in CIDR notation.

            If not specified, this
            matches with any destination address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-tlsinspectionconfiguration-servercertificatescope.html#cfn-networkfirewall-tlsinspectionconfiguration-servercertificatescope-destinations
            '''
            result = self._values.get("destinations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTLSInspectionConfigurationPropsMixin.AddressProperty"]]]], result)

        @builtins.property
        def protocols(
            self,
        ) -> typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]]:
            '''The protocols to inspect for, specified using the assigned internet protocol number (IANA) for each protocol.

            If not specified, this matches with any protocol.

            Network Firewall currently supports only TCP.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-tlsinspectionconfiguration-servercertificatescope.html#cfn-networkfirewall-tlsinspectionconfiguration-servercertificatescope-protocols
            '''
            result = self._values.get("protocols")
            return typing.cast(typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def source_ports(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTLSInspectionConfigurationPropsMixin.PortRangeProperty"]]]]:
            '''The source ports to decrypt for inspection, in Transmission Control Protocol (TCP) format.

            If not specified, this matches with any source port.

            You can specify individual ports, for example ``1994`` , and you can specify port ranges, such as ``1990:1994`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-tlsinspectionconfiguration-servercertificatescope.html#cfn-networkfirewall-tlsinspectionconfiguration-servercertificatescope-sourceports
            '''
            result = self._values.get("source_ports")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTLSInspectionConfigurationPropsMixin.PortRangeProperty"]]]], result)

        @builtins.property
        def sources(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTLSInspectionConfigurationPropsMixin.AddressProperty"]]]]:
            '''The source IP addresses and address ranges to decrypt for inspection, in CIDR notation.

            If not specified, this
            matches with any source address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-tlsinspectionconfiguration-servercertificatescope.html#cfn-networkfirewall-tlsinspectionconfiguration-servercertificatescope-sources
            '''
            result = self._values.get("sources")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTLSInspectionConfigurationPropsMixin.AddressProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerCertificateScopeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnTLSInspectionConfigurationPropsMixin.TLSInspectionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "server_certificate_configurations": "serverCertificateConfigurations",
        },
    )
    class TLSInspectionConfigurationProperty:
        def __init__(
            self,
            *,
            server_certificate_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTLSInspectionConfigurationPropsMixin.ServerCertificateConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The object that defines a TLS inspection configuration. This defines the TLS inspection configuration.

            AWS Network Firewall uses a TLS inspection configuration to decrypt traffic. Network Firewall re-encrypts the traffic before sending it to its destination.

            To use a TLS inspection configuration, you add it to a new Network Firewall firewall policy, then you apply the firewall policy to a firewall. Network Firewall acts as a proxy service to decrypt and inspect the traffic traveling through your firewalls. You can reference a TLS inspection configuration from more than one firewall policy, and you can use a firewall policy in more than one firewall. For more information about using TLS inspection configurations, see `Inspecting SSL/TLS traffic with TLS inspection configurations <https://docs.aws.amazon.com/network-firewall/latest/developerguide/tls-inspection.html>`_ in the *AWS Network Firewall Developer Guide* .

            :param server_certificate_configurations: Lists the server certificate configurations that are associated with the TLS configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-tlsinspectionconfiguration-tlsinspectionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                t_lSInspection_configuration_property = networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.TLSInspectionConfigurationProperty(
                    server_certificate_configurations=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.ServerCertificateConfigurationProperty(
                        certificate_authority_arn="certificateAuthorityArn",
                        check_certificate_revocation_status=networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.CheckCertificateRevocationStatusProperty(
                            revoked_status_action="revokedStatusAction",
                            unknown_status_action="unknownStatusAction"
                        ),
                        scopes=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.ServerCertificateScopeProperty(
                            destination_ports=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.PortRangeProperty(
                                from_port=123,
                                to_port=123
                            )],
                            destinations=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.AddressProperty(
                                address_definition="addressDefinition"
                            )],
                            protocols=[123],
                            source_ports=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.PortRangeProperty(
                                from_port=123,
                                to_port=123
                            )],
                            sources=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.AddressProperty(
                                address_definition="addressDefinition"
                            )]
                        )],
                        server_certificates=[networkfirewall_mixins.CfnTLSInspectionConfigurationPropsMixin.ServerCertificateProperty(
                            resource_arn="resourceArn"
                        )]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e6337a0c6c3230af72db2b94235b62587473a967449800eb90885e92676bda32)
                check_type(argname="argument server_certificate_configurations", value=server_certificate_configurations, expected_type=type_hints["server_certificate_configurations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if server_certificate_configurations is not None:
                self._values["server_certificate_configurations"] = server_certificate_configurations

        @builtins.property
        def server_certificate_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTLSInspectionConfigurationPropsMixin.ServerCertificateConfigurationProperty"]]]]:
            '''Lists the server certificate configurations that are associated with the TLS configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-tlsinspectionconfiguration-tlsinspectionconfiguration.html#cfn-networkfirewall-tlsinspectionconfiguration-tlsinspectionconfiguration-servercertificateconfigurations
            '''
            result = self._values.get("server_certificate_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTLSInspectionConfigurationPropsMixin.ServerCertificateConfigurationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TLSInspectionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnVpcEndpointAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "firewall_arn": "firewallArn",
        "subnet_mapping": "subnetMapping",
        "tags": "tags",
        "vpc_id": "vpcId",
    },
)
class CfnVpcEndpointAssociationMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        firewall_arn: typing.Optional[builtins.str] = None,
        subnet_mapping: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVpcEndpointAssociationPropsMixin.SubnetMappingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnVpcEndpointAssociationPropsMixin.

        :param description: A description of the VPC endpoint association.
        :param firewall_arn: The Amazon Resource Name (ARN) of the firewall.
        :param subnet_mapping: The ID for a subnet that's used in an association with a firewall. This is used in ``CreateFirewall`` , ``AssociateSubnets`` , and ``CreateVpcEndpointAssociation`` . AWS Network Firewall creates an instance of the associated firewall in each subnet that you specify, to filter traffic in the subnet's Availability Zone.
        :param tags: The key:value pairs to associate with the resource.
        :param vpc_id: The unique identifier of the VPC for the endpoint association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-vpcendpointassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
            
            cfn_vpc_endpoint_association_mixin_props = networkfirewall_mixins.CfnVpcEndpointAssociationMixinProps(
                description="description",
                firewall_arn="firewallArn",
                subnet_mapping=networkfirewall_mixins.CfnVpcEndpointAssociationPropsMixin.SubnetMappingProperty(
                    ip_address_type="ipAddressType",
                    subnet_id="subnetId"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_id="vpcId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c846310a292184c3a3e2650a5341b65e2f09f296843957de99d4598fb7b14c76)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument firewall_arn", value=firewall_arn, expected_type=type_hints["firewall_arn"])
            check_type(argname="argument subnet_mapping", value=subnet_mapping, expected_type=type_hints["subnet_mapping"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if firewall_arn is not None:
            self._values["firewall_arn"] = firewall_arn
        if subnet_mapping is not None:
            self._values["subnet_mapping"] = subnet_mapping
        if tags is not None:
            self._values["tags"] = tags
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the VPC endpoint association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-vpcendpointassociation.html#cfn-networkfirewall-vpcendpointassociation-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firewall_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the firewall.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-vpcendpointassociation.html#cfn-networkfirewall-vpcendpointassociation-firewallarn
        '''
        result = self._values.get("firewall_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_mapping(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVpcEndpointAssociationPropsMixin.SubnetMappingProperty"]]:
        '''The ID for a subnet that's used in an association with a firewall.

        This is used in ``CreateFirewall`` , ``AssociateSubnets`` , and ``CreateVpcEndpointAssociation`` . AWS Network Firewall creates an instance of the associated firewall in each subnet that you specify, to filter traffic in the subnet's Availability Zone.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-vpcendpointassociation.html#cfn-networkfirewall-vpcendpointassociation-subnetmapping
        '''
        result = self._values.get("subnet_mapping")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVpcEndpointAssociationPropsMixin.SubnetMappingProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The key:value pairs to associate with the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-vpcendpointassociation.html#cfn-networkfirewall-vpcendpointassociation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the VPC for the endpoint association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-vpcendpointassociation.html#cfn-networkfirewall-vpcendpointassociation-vpcid
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVpcEndpointAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVpcEndpointAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnVpcEndpointAssociationPropsMixin",
):
    '''A VPC endpoint association defines a single subnet to use for a firewall endpoint for a ``Firewall`` .

    You can define VPC endpoint associations only in the Availability Zones that already have a subnet mapping defined in the ``Firewall`` resource.
    .. epigraph::

       You can retrieve the list of Availability Zones that are available for use by calling ``DescribeFirewallMetadata`` .

    To manage firewall endpoints, first, in the ``Firewall`` specification, you specify a single VPC and one subnet for each of the Availability Zones where you want to use the firewall. Then you can define additional endpoints as VPC endpoint associations.

    You can use VPC endpoint associations to expand the protections of the firewall as follows:

    - *Protect multiple VPCs with a single firewall* - You can use the firewall to protect other VPCs, either in your account or in accounts where the firewall is shared. You can only specify Availability Zones that already have a firewall endpoint defined in the ``Firewall`` subnet mappings.
    - *Define multiple firewall endpoints for a VPC in an Availability Zone* - You can create additional firewall endpoints for the VPC that you have defined in the firewall, in any Availability Zone that already has an endpoint defined in the ``Firewall`` subnet mappings. You can create multiple VPC endpoint associations for any other VPC where you use the firewall.

    You can use AWS Resource Access Manager to share a ``Firewall`` that you own with other accounts, which gives them the ability to use the firewall to create VPC endpoint associations. For information about sharing a firewall, see ``PutResourcePolicy`` in this guide and see `Sharing Network Firewall resources <https://docs.aws.amazon.com/network-firewall/latest/developerguide/sharing.html>`_ in the *AWS Network Firewall Developer Guide* .

    The status of the VPC endpoint association, which indicates whether it's ready to filter network traffic, is provided in the corresponding VPC endpoint association status. You can retrieve both the association and its status by calling ``DescribeVpcEndpointAssociation`` .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-vpcendpointassociation.html
    :cloudformationResource: AWS::NetworkFirewall::VpcEndpointAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
        
        cfn_vpc_endpoint_association_props_mixin = networkfirewall_mixins.CfnVpcEndpointAssociationPropsMixin(networkfirewall_mixins.CfnVpcEndpointAssociationMixinProps(
            description="description",
            firewall_arn="firewallArn",
            subnet_mapping=networkfirewall_mixins.CfnVpcEndpointAssociationPropsMixin.SubnetMappingProperty(
                ip_address_type="ipAddressType",
                subnet_id="subnetId"
            ),
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
        props: typing.Union[CfnVpcEndpointAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NetworkFirewall::VpcEndpointAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d83cea74bfb86280f5cfacf51916aa258ab0f54acc957bfbf0508304cd15b6d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1706070f173c905e377c42055384af63b30031be4c5d7bd953903670e1eb231d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb07eb608359e702094672f8f1955b211205b89ae2eed3b388b13abc7aef5651)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVpcEndpointAssociationMixinProps:
        return typing.cast(CfnVpcEndpointAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkfirewall.mixins.CfnVpcEndpointAssociationPropsMixin.SubnetMappingProperty",
        jsii_struct_bases=[],
        name_mapping={"ip_address_type": "ipAddressType", "subnet_id": "subnetId"},
    )
    class SubnetMappingProperty:
        def __init__(
            self,
            *,
            ip_address_type: typing.Optional[builtins.str] = None,
            subnet_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ID for a subnet that's used in an association with a firewall.

            This is used in ``CreateFirewall`` , ``AssociateSubnets`` , and ``CreateVpcEndpointAssociation`` . AWS Network Firewall creates an instance of the associated firewall in each subnet that you specify, to filter traffic in the subnet's Availability Zone.

            :param ip_address_type: The subnet's IP address type. You can't change the IP address type after you create the subnet.
            :param subnet_id: The unique identifier for the subnet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-vpcendpointassociation-subnetmapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkfirewall import mixins as networkfirewall_mixins
                
                subnet_mapping_property = networkfirewall_mixins.CfnVpcEndpointAssociationPropsMixin.SubnetMappingProperty(
                    ip_address_type="ipAddressType",
                    subnet_id="subnetId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9c872005968d267fe18b0a4557cc2e93927ab5bd97ad5fc747f0fbf27ef0d464)
                check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
                check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ip_address_type is not None:
                self._values["ip_address_type"] = ip_address_type
            if subnet_id is not None:
                self._values["subnet_id"] = subnet_id

        @builtins.property
        def ip_address_type(self) -> typing.Optional[builtins.str]:
            '''The subnet's IP address type.

            You can't change the IP address type after you create the subnet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-vpcendpointassociation-subnetmapping.html#cfn-networkfirewall-vpcendpointassociation-subnetmapping-ipaddresstype
            '''
            result = self._values.get("ip_address_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subnet_id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier for the subnet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-vpcendpointassociation-subnetmapping.html#cfn-networkfirewall-vpcendpointassociation-subnetmapping-subnetid
            '''
            result = self._values.get("subnet_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubnetMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnFirewallAlertLogs",
    "CfnFirewallFlowLogs",
    "CfnFirewallLogsMixin",
    "CfnFirewallMixinProps",
    "CfnFirewallPolicyMixinProps",
    "CfnFirewallPolicyPropsMixin",
    "CfnFirewallPropsMixin",
    "CfnFirewallTlsLogs",
    "CfnLoggingConfigurationMixinProps",
    "CfnLoggingConfigurationPropsMixin",
    "CfnRuleGroupMixinProps",
    "CfnRuleGroupPropsMixin",
    "CfnTLSInspectionConfigurationMixinProps",
    "CfnTLSInspectionConfigurationPropsMixin",
    "CfnVpcEndpointAssociationMixinProps",
    "CfnVpcEndpointAssociationPropsMixin",
]

publication.publish()

def _typecheckingstub__7328590b513805553dee64080b0a79efac3e8f24960e08b3147e3e1c0cd77569(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67a490929fffe050d352d6197630e45bb231048c2061069a1de90a533030013(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f141909d9744c277aa229bebcd21ccdf011d035acd18dda3281db79ce95441e(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d0c1095f2366a9586eb3f395a32504aad3308ecf9172d6fa5ad6412e69e1c70(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd71c0b1f1d27a1812b9d05a137e96a538baa825c4553a6e08482e6090df99d3(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a3f58fb66ed021923fb17d2ddd81fb144af311cbc8109de9a34dcc4a9f7445(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7849a0cb6670c4dec2ef0ae2b87258f087ebacd9f96978d6c1d6aa4fe089ec82(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94742363755f8294f26cd606249ac9ba39736c6e737d707ea5c50a34d4ab9a70(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c49fe0c9d241623950091a3176bc672dd3ed72f003894ef6b14ad3a17df03ae5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d221ece32039d9dc3ade00117446171adc4bdd1faca256da2a943ea6d52e60c(
    *,
    availability_zone_change_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    availability_zone_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFirewallPropsMixin.AvailabilityZoneMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    delete_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled_analysis_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    firewall_name: typing.Optional[builtins.str] = None,
    firewall_policy_arn: typing.Optional[builtins.str] = None,
    firewall_policy_change_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    subnet_change_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    subnet_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFirewallPropsMixin.SubnetMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    transit_gateway_id: typing.Optional[builtins.str] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__217c93391153a84db656b13ddf2abd106c7c93dd4065a0e770fb0e5b5923635d(
    *,
    description: typing.Optional[builtins.str] = None,
    firewall_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFirewallPolicyPropsMixin.FirewallPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    firewall_policy_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f31d99d2404faf116762205aff648f73e80f939ce1f3bdc2b7c8f262c69be3(
    props: typing.Union[CfnFirewallPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2a3a996f94b7d7472d8c15da4d3d9654243aa988dc31d82262878a3bc5258cc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3b7e1977444bd0eaf990d45b76f52945de22f938180906e74ff6eb71a855613(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e5c0eca83fd919c2802ec0b35e718b5ffec8557e4d92e543942e2a154885d2f(
    *,
    publish_metric_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFirewallPolicyPropsMixin.PublishMetricActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee6bdca6fe32f9b7d2aa4e6b899a47df06fdfa30cd21b2067c4b214d48c98ba4(
    *,
    action_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFirewallPolicyPropsMixin.ActionDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    action_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c4cde82ee095606b04c9109c9d94f07d11cef9699606ae2e02cf341350983d(
    *,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37511d2a2526d0826f880c68538a135daeb08492f7915969354a25445506d91c(
    *,
    enable_tls_session_holding: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    policy_variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFirewallPolicyPropsMixin.PolicyVariablesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stateful_default_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    stateful_engine_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFirewallPolicyPropsMixin.StatefulEngineOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stateful_rule_group_references: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFirewallPolicyPropsMixin.StatefulRuleGroupReferenceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    stateless_custom_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFirewallPolicyPropsMixin.CustomActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    stateless_default_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    stateless_fragment_default_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    stateless_rule_group_references: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFirewallPolicyPropsMixin.StatelessRuleGroupReferenceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tls_inspection_configuration_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e8a137519b9ca17a685dff2ed62a82c4ce0f82324eb98e1a17a4ec80a7094bc(
    *,
    tcp_idle_timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc0c540afeb3a8655ecaadd3587b4f2f48caaeb0c4b2b4ecd3390b871f0e5fc9(
    *,
    definition: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44bb80968f8561390d6243226fcf47b05eccca5cf04bce3dc6e8d9989d69cd01(
    *,
    rule_variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFirewallPolicyPropsMixin.IPSetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ba578216f83656dc0599ea3c015290a4588b3006fd9a7825c717b6548d2a4ec(
    *,
    dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFirewallPolicyPropsMixin.DimensionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487fd2fb21e4293549dbeb34c36acd758dc2c0d4f1d39f1375a75205f9a468f6(
    *,
    flow_timeouts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFirewallPolicyPropsMixin.FlowTimeoutsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rule_order: typing.Optional[builtins.str] = None,
    stream_exception_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e26f17e84a1c51385faf08ac5866559e8b553fedd0371c0df16d81bed04f42f2(
    *,
    action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__111763d75784aba6d58d48d327ac3f16d37b7827c4cafe5d3aafe2a0af09fa67(
    *,
    deep_threat_inspection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    override: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFirewallPolicyPropsMixin.StatefulRuleGroupOverrideProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    priority: typing.Optional[jsii.Number] = None,
    resource_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d28939c78f092b7c561459c078e63018674cf21c9e4df68bba2eb55bceb645c4(
    *,
    priority: typing.Optional[jsii.Number] = None,
    resource_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e0d286e801016f90d4f380f69b736459a371baca385051dd9b25543b38bbfee(
    props: typing.Union[CfnFirewallMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08cb1224629a0e31d94f817940adc4a71ea8038c43fe560cb19af234a92e9fc3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1742574b8cf3e62b7edab37fee5aa43ef28610f4b11504fb16092fd0e9e3456e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0263862ba6a89fc8ab4c89e1666bf8fd0f3baad13e49ff11845177c3dd82c35a(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d9ffb21b85677289e60fd5aedae3294c0e6f82cea7b1dd1c94fe94b1cf9329d(
    *,
    ip_address_type: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a082025e0f2623f1ac880cf67bb1925c5a1542f565f8340d4e62ccebee53575(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e217b2015025276aebd37e7b6f40a7f50f1a44304dfbb4b57f8ab0f515a5da20(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92e9e0f4001a2d2095af2ca2822a04c06e661dbb403fc7b4b6edb3314f2d735b(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__245810e535c34d3ddb23058ce4c2402e803560cb49a7c9eb829177f933df2bd6(
    *,
    enable_monitoring_dashboard: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    firewall_arn: typing.Optional[builtins.str] = None,
    firewall_name: typing.Optional[builtins.str] = None,
    logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLoggingConfigurationPropsMixin.LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__720c4ff7e3df87f9d00dd4af0e9508926c9ae4c0da2ff90fd94de69bed88e468(
    props: typing.Union[CfnLoggingConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d1be0e48d2f8196be0a0bf3626bb409a5a45db0ba37db5f963ec9f464d7d3d6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da8d219b8d36b8c7afcccd1dc1f74a75e911993462684e234269b2ee88f4191(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc280b3a170807c53758409e41db26e22f185813326f80f4ed88e06a497f79c(
    *,
    log_destination: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    log_destination_type: typing.Optional[builtins.str] = None,
    log_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4806fee8d71c1c72447f041275263f084e9e571d88df98b3f8f9c1f0ab4453ce(
    *,
    log_destination_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLoggingConfigurationPropsMixin.LogDestinationConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1077e8425f59a64076268e40e48142443fda82d584f49b6e92c4d9274dbd2d9(
    *,
    capacity: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    rule_group: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.RuleGroupProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rule_group_name: typing.Optional[builtins.str] = None,
    summary_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.SummaryConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45de11b74c28461f6ba7aa0925ad0be2f99cc648b5fa480912c48c4ff247547e(
    props: typing.Union[CfnRuleGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9fba49bc98878dc0f9001f1201b9f3fd3e851e23b98d814f9403133af02ae1e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71bfa521110cc24c6d52e398b5f7fd96aa012c33d5aca3a764f9692affe68130(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d576b5d835828eb320cadf2a154b753b968b0d0fa6e5a653c41aebfe3882352(
    *,
    publish_metric_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.PublishMetricActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__582279fd8b694c9d5bf265a5e68eb304b61bd18f8f95ea0c2b9214ab9b776647(
    *,
    address_definition: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b360dd8a5f7afdbad1a5e5b91c504082d7513580c6d2f9f4431c4de94b914298(
    *,
    action_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.ActionDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    action_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f89dba65215935a38132cb025c854127b02d024a915986deae040ee07ab242(
    *,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34df5b26012894fd96e59555a08a0854706d1c1b557b0e5af5e0f2eb5509c7c6(
    *,
    destination: typing.Optional[builtins.str] = None,
    destination_port: typing.Optional[builtins.str] = None,
    direction: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    source_port: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5114f02ca905bd251454978994b2462b914bff1eae8125317da0b9f7fc19e6c(
    *,
    definition: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f87516336eaf6e16b362f9194f8c9719cc80f8431ea244c6a583fee87c4eb37e(
    *,
    reference_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7b552bdde96d6ca8d76206161f2efabc2624bc4e9932eb4ff51473cc85f6a76(
    *,
    destination_ports: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.PortRangeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    destinations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.AddressProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    protocols: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
    source_ports: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.PortRangeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.AddressProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tcp_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.TCPFlagFieldProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__003949cae8b6b57b315534b47fa99c937b85cb7c5b13103618e115117ec6c984(
    *,
    from_port: typing.Optional[jsii.Number] = None,
    to_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f816cd4f046d2ee1baaa3c4c18230f1071a7bf4884b956fa6e38a3d054d953ab(
    *,
    definition: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c181cf3d5f602c6f89bde0fd2868abd4f8b890e12cf9be9e70ee669e1a7c9f8(
    *,
    dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.DimensionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb2dbb5aa6d6845495ee9626ff66ce300ec3abdc30ee82b6bc1c42e220d7357(
    *,
    ip_set_references: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.IPSetReferenceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e77bd3b2d733609d0c4c825ca23d56491bef394c0ecc54acf00f3e09e642d716(
    *,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    match_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.MatchAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22c95b58dd4dac1580aee1746099459d78a14b5ff4a58c2502e64397ed8d13fc(
    *,
    reference_sets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.ReferenceSetsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rules_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.RulesSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rule_variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.RuleVariablesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stateful_rule_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.StatefulRuleOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__321fc71e2069453f66063c859e60aa00df5279771a5097815a4ee114e9236a0c(
    *,
    keyword: typing.Optional[builtins.str] = None,
    settings: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24dc25df5062a3278fd486bee68b2d86c4b0d8a9e1a0413c85409758c15f04a3(
    *,
    ip_sets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.IPSetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    port_sets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.PortSetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d470e6e0cec23d203bb70a7cd31401e80c209421494df6da465a75fa3ecb690a(
    *,
    generated_rules_type: typing.Optional[builtins.str] = None,
    targets: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aae4a49c455e0531f8b16acaa55d3e9259e1477fccf003668f7015bb822ae8ec(
    *,
    rules_source_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.RulesSourceListProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rules_string: typing.Optional[builtins.str] = None,
    stateful_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.StatefulRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    stateless_rules_and_custom_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.StatelessRulesAndCustomActionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83272891c7571d49700e7b0cd1be91da27283ed251b8fda68cb5847b6b3635bb(
    *,
    rule_order: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa2d4ccc582ba35249d17ad56b90bc0b4c49d75cd83aea0a4754bb89ce2d4cec(
    *,
    action: typing.Optional[builtins.str] = None,
    header: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.HeaderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rule_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.RuleOptionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b1cccfd0cba28e6bdbb65ef005ef4a9d85468a0c608e6821f9ef74ebf44e022(
    *,
    priority: typing.Optional[jsii.Number] = None,
    rule_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.RuleDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea8e055da435e7152805c51abf3767ef52ef9c9b1c6dc5c8c7d30c25babf4f96(
    *,
    custom_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.CustomActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    stateless_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRuleGroupPropsMixin.StatelessRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae730268952b3591a348bec3baed6c17c673725465b875f350f1b618951ace13(
    *,
    rule_options: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9014b92cd323283d65c1c96fc693e1fcb76dbaf041e7c7a8cc65c62d1eb7f508(
    *,
    flags: typing.Optional[typing.Sequence[builtins.str]] = None,
    masks: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8539d566a73df40a780e01a3f9331c6f673e834d78590860d1f860a2fe578bdf(
    *,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    tls_inspection_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTLSInspectionConfigurationPropsMixin.TLSInspectionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tls_inspection_configuration_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71fe682c8679ee9743a68bf04f25c4a67119bf74fc8414b896011e5276e372c3(
    props: typing.Union[CfnTLSInspectionConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d89f94eb2fb5af0c8013b249d4ed2157064f07fb297247c3a1b8405a6564c53b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49fe9947d7ea6504fda002120498e41f98a980f278bb79c478abc1bf6d77b4cf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6ed246a8e1789f5be43e8601ad0ad1996f2af6a9c5c79d201d79cd4768e629a(
    *,
    address_definition: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6074a3e0e9c555fee51df6f3791a877cd56797bf815cb680ceaee75904fb6b3(
    *,
    revoked_status_action: typing.Optional[builtins.str] = None,
    unknown_status_action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3454ffc185333ea95af8150da666cce972edce0ca66ce1eb05cda87a6db88f41(
    *,
    from_port: typing.Optional[jsii.Number] = None,
    to_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d686d935ec1f1cd0fc1e9cf7586e76255bbd4bc35bd497b5da701dcae471a33c(
    *,
    certificate_authority_arn: typing.Optional[builtins.str] = None,
    check_certificate_revocation_status: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTLSInspectionConfigurationPropsMixin.CheckCertificateRevocationStatusProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scopes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTLSInspectionConfigurationPropsMixin.ServerCertificateScopeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    server_certificates: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTLSInspectionConfigurationPropsMixin.ServerCertificateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d953b45b3767036981264adc61dc947ff70ac7236b35b3b600122c1b08a18d91(
    *,
    resource_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1accef2069e367c209447736ed390ceaf1e64b0b44479537156ee7ef4e099142(
    *,
    destination_ports: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTLSInspectionConfigurationPropsMixin.PortRangeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    destinations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTLSInspectionConfigurationPropsMixin.AddressProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    protocols: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
    source_ports: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTLSInspectionConfigurationPropsMixin.PortRangeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTLSInspectionConfigurationPropsMixin.AddressProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6337a0c6c3230af72db2b94235b62587473a967449800eb90885e92676bda32(
    *,
    server_certificate_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTLSInspectionConfigurationPropsMixin.ServerCertificateConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c846310a292184c3a3e2650a5341b65e2f09f296843957de99d4598fb7b14c76(
    *,
    description: typing.Optional[builtins.str] = None,
    firewall_arn: typing.Optional[builtins.str] = None,
    subnet_mapping: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVpcEndpointAssociationPropsMixin.SubnetMappingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83cea74bfb86280f5cfacf51916aa258ab0f54acc957bfbf0508304cd15b6d8(
    props: typing.Union[CfnVpcEndpointAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1706070f173c905e377c42055384af63b30031be4c5d7bd953903670e1eb231d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb07eb608359e702094672f8f1955b211205b89ae2eed3b388b13abc7aef5651(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c872005968d267fe18b0a4557cc2e93927ab5bd97ad5fc747f0fbf27ef0d464(
    *,
    ip_address_type: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
