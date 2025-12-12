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
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.interfaces.aws_route53resolver as _aws_cdk_interfaces_aws_route53resolver_ceddda9d


class FirewallDomainListEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.events.FirewallDomainListEvents",
):
    '''(experimental) EventBridge event patterns for FirewallDomainList.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_route53resolver import events as route53resolver_events
        from aws_cdk.interfaces import aws_route53resolver as interfaces_route53resolver
        
        # firewall_domain_list_ref: interfaces_route53resolver.IFirewallDomainListRef
        
        firewall_domain_list_events = route53resolver_events.FirewallDomainListEvents.from_firewall_domain_list(firewall_domain_list_ref)
    '''

    @jsii.member(jsii_name="fromFirewallDomainList")
    @builtins.classmethod
    def from_firewall_domain_list(
        cls,
        firewall_domain_list_ref: _aws_cdk_interfaces_aws_route53resolver_ceddda9d.IFirewallDomainListRef,
    ) -> "FirewallDomainListEvents":
        '''(experimental) Create FirewallDomainListEvents from a FirewallDomainList reference.

        :param firewall_domain_list_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8f9333cd1abe443af66f332fb80ff4c96606a874572ac7aa4bd4d41552113fa)
            check_type(argname="argument firewall_domain_list_ref", value=firewall_domain_list_ref, expected_type=type_hints["firewall_domain_list_ref"])
        return typing.cast("FirewallDomainListEvents", jsii.sinvoke(cls, "fromFirewallDomainList", [firewall_domain_list_ref]))

    @jsii.member(jsii_name="dNSFirewallAlertPattern")
    def d_ns_firewall_alert_pattern(
        self,
        *,
        account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        firewall_domain_list_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        firewall_rule_action: typing.Optional[typing.Sequence[builtins.str]] = None,
        firewall_rule_group_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        last_observed_at: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_class: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        resources: typing.Optional[typing.Sequence[typing.Union["FirewallDomainListEvents.DNSFirewallAlert.DnsFirewallAlertItem", typing.Dict[builtins.str, typing.Any]]]] = None,
        src_addr: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_port: typing.Optional[typing.Sequence[builtins.str]] = None,
        transport: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for FirewallDomainList DNS Firewall Alert.

        :param account_id: (experimental) account-id property. Specify an array of string values to match this event if the actual value of account-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param firewall_domain_list_id: (experimental) firewall-domain-list-id property. Specify an array of string values to match this event if the actual value of firewall-domain-list-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the FirewallDomainList reference
        :param firewall_rule_action: (experimental) firewall-rule-action property. Specify an array of string values to match this event if the actual value of firewall-rule-action is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param firewall_rule_group_id: (experimental) firewall-rule-group-id property. Specify an array of string values to match this event if the actual value of firewall-rule-group-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param last_observed_at: (experimental) last-observed-at property. Specify an array of string values to match this event if the actual value of last-observed-at is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param query_class: (experimental) query-class property. Specify an array of string values to match this event if the actual value of query-class is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param query_name: (experimental) query-name property. Specify an array of string values to match this event if the actual value of query-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param query_type: (experimental) query-type property. Specify an array of string values to match this event if the actual value of query-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param resources: (experimental) resources property. Specify an array of string values to match this event if the actual value of resources is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param src_addr: (experimental) src-addr property. Specify an array of string values to match this event if the actual value of src-addr is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param src_port: (experimental) src-port property. Specify an array of string values to match this event if the actual value of src-port is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param transport: (experimental) transport property. Specify an array of string values to match this event if the actual value of transport is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param vpc_id: (experimental) vpc-id property. Specify an array of string values to match this event if the actual value of vpc-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = FirewallDomainListEvents.DNSFirewallAlert.DNSFirewallAlertProps(
            account_id=account_id,
            event_metadata=event_metadata,
            firewall_domain_list_id=firewall_domain_list_id,
            firewall_rule_action=firewall_rule_action,
            firewall_rule_group_id=firewall_rule_group_id,
            last_observed_at=last_observed_at,
            query_class=query_class,
            query_name=query_name,
            query_type=query_type,
            resources=resources,
            src_addr=src_addr,
            src_port=src_port,
            transport=transport,
            vpc_id=vpc_id,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "dNSFirewallAlertPattern", [options]))

    @jsii.member(jsii_name="dNSFirewallBlockPattern")
    def d_ns_firewall_block_pattern(
        self,
        *,
        account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        firewall_domain_list_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        firewall_rule_action: typing.Optional[typing.Sequence[builtins.str]] = None,
        firewall_rule_group_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        last_observed_at: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_class: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        resources: typing.Optional[typing.Sequence[typing.Union["FirewallDomainListEvents.DNSFirewallBlock.DnsFirewallBlockItem", typing.Dict[builtins.str, typing.Any]]]] = None,
        src_addr: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_port: typing.Optional[typing.Sequence[builtins.str]] = None,
        transport: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for FirewallDomainList DNS Firewall Block.

        :param account_id: (experimental) account-id property. Specify an array of string values to match this event if the actual value of account-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param firewall_domain_list_id: (experimental) firewall-domain-list-id property. Specify an array of string values to match this event if the actual value of firewall-domain-list-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the FirewallDomainList reference
        :param firewall_rule_action: (experimental) firewall-rule-action property. Specify an array of string values to match this event if the actual value of firewall-rule-action is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param firewall_rule_group_id: (experimental) firewall-rule-group-id property. Specify an array of string values to match this event if the actual value of firewall-rule-group-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param last_observed_at: (experimental) last-observed-at property. Specify an array of string values to match this event if the actual value of last-observed-at is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param query_class: (experimental) query-class property. Specify an array of string values to match this event if the actual value of query-class is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param query_name: (experimental) query-name property. Specify an array of string values to match this event if the actual value of query-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param query_type: (experimental) query-type property. Specify an array of string values to match this event if the actual value of query-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param resources: (experimental) resources property. Specify an array of string values to match this event if the actual value of resources is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param src_addr: (experimental) src-addr property. Specify an array of string values to match this event if the actual value of src-addr is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param src_port: (experimental) src-port property. Specify an array of string values to match this event if the actual value of src-port is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param transport: (experimental) transport property. Specify an array of string values to match this event if the actual value of transport is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param vpc_id: (experimental) vpc-id property. Specify an array of string values to match this event if the actual value of vpc-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = FirewallDomainListEvents.DNSFirewallBlock.DNSFirewallBlockProps(
            account_id=account_id,
            event_metadata=event_metadata,
            firewall_domain_list_id=firewall_domain_list_id,
            firewall_rule_action=firewall_rule_action,
            firewall_rule_group_id=firewall_rule_group_id,
            last_observed_at=last_observed_at,
            query_class=query_class,
            query_name=query_name,
            query_type=query_type,
            resources=resources,
            src_addr=src_addr,
            src_port=src_port,
            transport=transport,
            vpc_id=vpc_id,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "dNSFirewallBlockPattern", [options]))

    class DNSFirewallAlert(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.events.FirewallDomainListEvents.DNSFirewallAlert",
    ):
        '''(experimental) aws.route53resolver@DNSFirewallAlert event types for FirewallDomainList.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53resolver import events as route53resolver_events
            
            d_nSFirewall_alert = route53resolver_events.FirewallDomainListEvents.DNSFirewallAlert()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.events.FirewallDomainListEvents.DNSFirewallAlert.DNSFirewallAlertProps",
            jsii_struct_bases=[],
            name_mapping={
                "account_id": "accountId",
                "event_metadata": "eventMetadata",
                "firewall_domain_list_id": "firewallDomainListId",
                "firewall_rule_action": "firewallRuleAction",
                "firewall_rule_group_id": "firewallRuleGroupId",
                "last_observed_at": "lastObservedAt",
                "query_class": "queryClass",
                "query_name": "queryName",
                "query_type": "queryType",
                "resources": "resources",
                "src_addr": "srcAddr",
                "src_port": "srcPort",
                "transport": "transport",
                "vpc_id": "vpcId",
            },
        )
        class DNSFirewallAlertProps:
            def __init__(
                self,
                *,
                account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                firewall_domain_list_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                firewall_rule_action: typing.Optional[typing.Sequence[builtins.str]] = None,
                firewall_rule_group_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                last_observed_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                query_class: typing.Optional[typing.Sequence[builtins.str]] = None,
                query_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                query_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                resources: typing.Optional[typing.Sequence[typing.Union["FirewallDomainListEvents.DNSFirewallAlert.DnsFirewallAlertItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                src_addr: typing.Optional[typing.Sequence[builtins.str]] = None,
                src_port: typing.Optional[typing.Sequence[builtins.str]] = None,
                transport: typing.Optional[typing.Sequence[builtins.str]] = None,
                vpc_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for FirewallDomainList aws.route53resolver@DNSFirewallAlert event.

                :param account_id: (experimental) account-id property. Specify an array of string values to match this event if the actual value of account-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param firewall_domain_list_id: (experimental) firewall-domain-list-id property. Specify an array of string values to match this event if the actual value of firewall-domain-list-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the FirewallDomainList reference
                :param firewall_rule_action: (experimental) firewall-rule-action property. Specify an array of string values to match this event if the actual value of firewall-rule-action is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param firewall_rule_group_id: (experimental) firewall-rule-group-id property. Specify an array of string values to match this event if the actual value of firewall-rule-group-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param last_observed_at: (experimental) last-observed-at property. Specify an array of string values to match this event if the actual value of last-observed-at is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param query_class: (experimental) query-class property. Specify an array of string values to match this event if the actual value of query-class is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param query_name: (experimental) query-name property. Specify an array of string values to match this event if the actual value of query-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param query_type: (experimental) query-type property. Specify an array of string values to match this event if the actual value of query-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param resources: (experimental) resources property. Specify an array of string values to match this event if the actual value of resources is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param src_addr: (experimental) src-addr property. Specify an array of string values to match this event if the actual value of src-addr is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param src_port: (experimental) src-port property. Specify an array of string values to match this event if the actual value of src-port is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param transport: (experimental) transport property. Specify an array of string values to match this event if the actual value of transport is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param vpc_id: (experimental) vpc-id property. Specify an array of string values to match this event if the actual value of vpc-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_route53resolver import events as route53resolver_events
                    
                    d_nSFirewall_alert_props = route53resolver_events.FirewallDomainListEvents.DNSFirewallAlert.DNSFirewallAlertProps(
                        account_id=["accountId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        firewall_domain_list_id=["firewallDomainListId"],
                        firewall_rule_action=["firewallRuleAction"],
                        firewall_rule_group_id=["firewallRuleGroupId"],
                        last_observed_at=["lastObservedAt"],
                        query_class=["queryClass"],
                        query_name=["queryName"],
                        query_type=["queryType"],
                        resources=[route53resolver_events.FirewallDomainListEvents.DNSFirewallAlert.DnsFirewallAlertItem(
                            resolver_endpoint_details=route53resolver_events.FirewallDomainListEvents.DNSFirewallAlert.ResolverEndpointDetails(
                                id=["id"]
                            ),
                            resolver_network_interface_details=route53resolver_events.FirewallDomainListEvents.DNSFirewallAlert.ResolverNetworkInterfaceDetails(
                                id=["id"]
                            ),
                            resource_type=["resourceType"]
                        )],
                        src_addr=["srcAddr"],
                        src_port=["srcPort"],
                        transport=["transport"],
                        vpc_id=["vpcId"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__3887570322b9e0da6dff0cccfda9f46463eddbddd9136a3b8eef7da5dbeab70a)
                    check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument firewall_domain_list_id", value=firewall_domain_list_id, expected_type=type_hints["firewall_domain_list_id"])
                    check_type(argname="argument firewall_rule_action", value=firewall_rule_action, expected_type=type_hints["firewall_rule_action"])
                    check_type(argname="argument firewall_rule_group_id", value=firewall_rule_group_id, expected_type=type_hints["firewall_rule_group_id"])
                    check_type(argname="argument last_observed_at", value=last_observed_at, expected_type=type_hints["last_observed_at"])
                    check_type(argname="argument query_class", value=query_class, expected_type=type_hints["query_class"])
                    check_type(argname="argument query_name", value=query_name, expected_type=type_hints["query_name"])
                    check_type(argname="argument query_type", value=query_type, expected_type=type_hints["query_type"])
                    check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
                    check_type(argname="argument src_addr", value=src_addr, expected_type=type_hints["src_addr"])
                    check_type(argname="argument src_port", value=src_port, expected_type=type_hints["src_port"])
                    check_type(argname="argument transport", value=transport, expected_type=type_hints["transport"])
                    check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if account_id is not None:
                    self._values["account_id"] = account_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if firewall_domain_list_id is not None:
                    self._values["firewall_domain_list_id"] = firewall_domain_list_id
                if firewall_rule_action is not None:
                    self._values["firewall_rule_action"] = firewall_rule_action
                if firewall_rule_group_id is not None:
                    self._values["firewall_rule_group_id"] = firewall_rule_group_id
                if last_observed_at is not None:
                    self._values["last_observed_at"] = last_observed_at
                if query_class is not None:
                    self._values["query_class"] = query_class
                if query_name is not None:
                    self._values["query_name"] = query_name
                if query_type is not None:
                    self._values["query_type"] = query_type
                if resources is not None:
                    self._values["resources"] = resources
                if src_addr is not None:
                    self._values["src_addr"] = src_addr
                if src_port is not None:
                    self._values["src_port"] = src_port
                if transport is not None:
                    self._values["transport"] = transport
                if vpc_id is not None:
                    self._values["vpc_id"] = vpc_id

            @builtins.property
            def account_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) account-id property.

                Specify an array of string values to match this event if the actual value of account-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("account_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_metadata(
                self,
            ) -> typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps]:
                '''(experimental) EventBridge event metadata.

                :default:

                -
                -

                :stability: experimental
                '''
                result = self._values.get("event_metadata")
                return typing.cast(typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps], result)

            @builtins.property
            def firewall_domain_list_id(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) firewall-domain-list-id property.

                Specify an array of string values to match this event if the actual value of firewall-domain-list-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the FirewallDomainList reference

                :stability: experimental
                '''
                result = self._values.get("firewall_domain_list_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def firewall_rule_action(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) firewall-rule-action property.

                Specify an array of string values to match this event if the actual value of firewall-rule-action is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("firewall_rule_action")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def firewall_rule_group_id(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) firewall-rule-group-id property.

                Specify an array of string values to match this event if the actual value of firewall-rule-group-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("firewall_rule_group_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def last_observed_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) last-observed-at property.

                Specify an array of string values to match this event if the actual value of last-observed-at is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("last_observed_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def query_class(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) query-class property.

                Specify an array of string values to match this event if the actual value of query-class is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("query_class")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def query_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) query-name property.

                Specify an array of string values to match this event if the actual value of query-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("query_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def query_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) query-type property.

                Specify an array of string values to match this event if the actual value of query-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("query_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def resources(
                self,
            ) -> typing.Optional[typing.List["FirewallDomainListEvents.DNSFirewallAlert.DnsFirewallAlertItem"]]:
                '''(experimental) resources property.

                Specify an array of string values to match this event if the actual value of resources is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("resources")
                return typing.cast(typing.Optional[typing.List["FirewallDomainListEvents.DNSFirewallAlert.DnsFirewallAlertItem"]], result)

            @builtins.property
            def src_addr(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) src-addr property.

                Specify an array of string values to match this event if the actual value of src-addr is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("src_addr")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def src_port(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) src-port property.

                Specify an array of string values to match this event if the actual value of src-port is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("src_port")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def transport(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) transport property.

                Specify an array of string values to match this event if the actual value of transport is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("transport")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def vpc_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) vpc-id property.

                Specify an array of string values to match this event if the actual value of vpc-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("vpc_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "DNSFirewallAlertProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.events.FirewallDomainListEvents.DNSFirewallAlert.DnsFirewallAlertItem",
            jsii_struct_bases=[],
            name_mapping={
                "resolver_endpoint_details": "resolverEndpointDetails",
                "resolver_network_interface_details": "resolverNetworkInterfaceDetails",
                "resource_type": "resourceType",
            },
        )
        class DnsFirewallAlertItem:
            def __init__(
                self,
                *,
                resolver_endpoint_details: typing.Optional[typing.Union["FirewallDomainListEvents.DNSFirewallAlert.ResolverEndpointDetails", typing.Dict[builtins.str, typing.Any]]] = None,
                resolver_network_interface_details: typing.Optional[typing.Union["FirewallDomainListEvents.DNSFirewallAlert.ResolverNetworkInterfaceDetails", typing.Dict[builtins.str, typing.Any]]] = None,
                resource_type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for DNSFirewallAlertItem.

                :param resolver_endpoint_details: (experimental) resolver-endpoint-details property. Specify an array of string values to match this event if the actual value of resolver-endpoint-details is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param resolver_network_interface_details: (experimental) resolver-network-interface-details property. Specify an array of string values to match this event if the actual value of resolver-network-interface-details is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param resource_type: (experimental) resource-type property. Specify an array of string values to match this event if the actual value of resource-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_route53resolver import events as route53resolver_events
                    
                    dns_firewall_alert_item = route53resolver_events.FirewallDomainListEvents.DNSFirewallAlert.DnsFirewallAlertItem(
                        resolver_endpoint_details=route53resolver_events.FirewallDomainListEvents.DNSFirewallAlert.ResolverEndpointDetails(
                            id=["id"]
                        ),
                        resolver_network_interface_details=route53resolver_events.FirewallDomainListEvents.DNSFirewallAlert.ResolverNetworkInterfaceDetails(
                            id=["id"]
                        ),
                        resource_type=["resourceType"]
                    )
                '''
                if isinstance(resolver_endpoint_details, dict):
                    resolver_endpoint_details = FirewallDomainListEvents.DNSFirewallAlert.ResolverEndpointDetails(**resolver_endpoint_details)
                if isinstance(resolver_network_interface_details, dict):
                    resolver_network_interface_details = FirewallDomainListEvents.DNSFirewallAlert.ResolverNetworkInterfaceDetails(**resolver_network_interface_details)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__1f864db1c3f1c22dae0cda7830b25db530111d7841235f2ed55a0e95e8fd8bee)
                    check_type(argname="argument resolver_endpoint_details", value=resolver_endpoint_details, expected_type=type_hints["resolver_endpoint_details"])
                    check_type(argname="argument resolver_network_interface_details", value=resolver_network_interface_details, expected_type=type_hints["resolver_network_interface_details"])
                    check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if resolver_endpoint_details is not None:
                    self._values["resolver_endpoint_details"] = resolver_endpoint_details
                if resolver_network_interface_details is not None:
                    self._values["resolver_network_interface_details"] = resolver_network_interface_details
                if resource_type is not None:
                    self._values["resource_type"] = resource_type

            @builtins.property
            def resolver_endpoint_details(
                self,
            ) -> typing.Optional["FirewallDomainListEvents.DNSFirewallAlert.ResolverEndpointDetails"]:
                '''(experimental) resolver-endpoint-details property.

                Specify an array of string values to match this event if the actual value of resolver-endpoint-details is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("resolver_endpoint_details")
                return typing.cast(typing.Optional["FirewallDomainListEvents.DNSFirewallAlert.ResolverEndpointDetails"], result)

            @builtins.property
            def resolver_network_interface_details(
                self,
            ) -> typing.Optional["FirewallDomainListEvents.DNSFirewallAlert.ResolverNetworkInterfaceDetails"]:
                '''(experimental) resolver-network-interface-details property.

                Specify an array of string values to match this event if the actual value of resolver-network-interface-details is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("resolver_network_interface_details")
                return typing.cast(typing.Optional["FirewallDomainListEvents.DNSFirewallAlert.ResolverNetworkInterfaceDetails"], result)

            @builtins.property
            def resource_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) resource-type property.

                Specify an array of string values to match this event if the actual value of resource-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("resource_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "DnsFirewallAlertItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.events.FirewallDomainListEvents.DNSFirewallAlert.ResolverEndpointDetails",
            jsii_struct_bases=[],
            name_mapping={"id": "id"},
        )
        class ResolverEndpointDetails:
            def __init__(
                self,
                *,
                id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Resolver-endpoint-details.

                :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_route53resolver import events as route53resolver_events
                    
                    resolver_endpoint_details = route53resolver_events.FirewallDomainListEvents.DNSFirewallAlert.ResolverEndpointDetails(
                        id=["id"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__cabccc009fcc3e72e93b577665ea810fb1ba8d867b669c7d99c8e20877128a96)
                    check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if id is not None:
                    self._values["id"] = id

            @builtins.property
            def id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) id property.

                Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ResolverEndpointDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.events.FirewallDomainListEvents.DNSFirewallAlert.ResolverNetworkInterfaceDetails",
            jsii_struct_bases=[],
            name_mapping={"id": "id"},
        )
        class ResolverNetworkInterfaceDetails:
            def __init__(
                self,
                *,
                id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Resolver-network-interface-details.

                :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_route53resolver import events as route53resolver_events
                    
                    resolver_network_interface_details = route53resolver_events.FirewallDomainListEvents.DNSFirewallAlert.ResolverNetworkInterfaceDetails(
                        id=["id"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__90b40aa77f3ab22e8a9cbdb9f9c66b46a9927ff7d563081462d176990cf4301e)
                    check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if id is not None:
                    self._values["id"] = id

            @builtins.property
            def id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) id property.

                Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ResolverNetworkInterfaceDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class DNSFirewallBlock(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.events.FirewallDomainListEvents.DNSFirewallBlock",
    ):
        '''(experimental) aws.route53resolver@DNSFirewallBlock event types for FirewallDomainList.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53resolver import events as route53resolver_events
            
            d_nSFirewall_block = route53resolver_events.FirewallDomainListEvents.DNSFirewallBlock()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.events.FirewallDomainListEvents.DNSFirewallBlock.DNSFirewallBlockProps",
            jsii_struct_bases=[],
            name_mapping={
                "account_id": "accountId",
                "event_metadata": "eventMetadata",
                "firewall_domain_list_id": "firewallDomainListId",
                "firewall_rule_action": "firewallRuleAction",
                "firewall_rule_group_id": "firewallRuleGroupId",
                "last_observed_at": "lastObservedAt",
                "query_class": "queryClass",
                "query_name": "queryName",
                "query_type": "queryType",
                "resources": "resources",
                "src_addr": "srcAddr",
                "src_port": "srcPort",
                "transport": "transport",
                "vpc_id": "vpcId",
            },
        )
        class DNSFirewallBlockProps:
            def __init__(
                self,
                *,
                account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                firewall_domain_list_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                firewall_rule_action: typing.Optional[typing.Sequence[builtins.str]] = None,
                firewall_rule_group_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                last_observed_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                query_class: typing.Optional[typing.Sequence[builtins.str]] = None,
                query_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                query_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                resources: typing.Optional[typing.Sequence[typing.Union["FirewallDomainListEvents.DNSFirewallBlock.DnsFirewallBlockItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                src_addr: typing.Optional[typing.Sequence[builtins.str]] = None,
                src_port: typing.Optional[typing.Sequence[builtins.str]] = None,
                transport: typing.Optional[typing.Sequence[builtins.str]] = None,
                vpc_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for FirewallDomainList aws.route53resolver@DNSFirewallBlock event.

                :param account_id: (experimental) account-id property. Specify an array of string values to match this event if the actual value of account-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param firewall_domain_list_id: (experimental) firewall-domain-list-id property. Specify an array of string values to match this event if the actual value of firewall-domain-list-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the FirewallDomainList reference
                :param firewall_rule_action: (experimental) firewall-rule-action property. Specify an array of string values to match this event if the actual value of firewall-rule-action is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param firewall_rule_group_id: (experimental) firewall-rule-group-id property. Specify an array of string values to match this event if the actual value of firewall-rule-group-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param last_observed_at: (experimental) last-observed-at property. Specify an array of string values to match this event if the actual value of last-observed-at is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param query_class: (experimental) query-class property. Specify an array of string values to match this event if the actual value of query-class is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param query_name: (experimental) query-name property. Specify an array of string values to match this event if the actual value of query-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param query_type: (experimental) query-type property. Specify an array of string values to match this event if the actual value of query-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param resources: (experimental) resources property. Specify an array of string values to match this event if the actual value of resources is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param src_addr: (experimental) src-addr property. Specify an array of string values to match this event if the actual value of src-addr is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param src_port: (experimental) src-port property. Specify an array of string values to match this event if the actual value of src-port is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param transport: (experimental) transport property. Specify an array of string values to match this event if the actual value of transport is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param vpc_id: (experimental) vpc-id property. Specify an array of string values to match this event if the actual value of vpc-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_route53resolver import events as route53resolver_events
                    
                    d_nSFirewall_block_props = route53resolver_events.FirewallDomainListEvents.DNSFirewallBlock.DNSFirewallBlockProps(
                        account_id=["accountId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        firewall_domain_list_id=["firewallDomainListId"],
                        firewall_rule_action=["firewallRuleAction"],
                        firewall_rule_group_id=["firewallRuleGroupId"],
                        last_observed_at=["lastObservedAt"],
                        query_class=["queryClass"],
                        query_name=["queryName"],
                        query_type=["queryType"],
                        resources=[route53resolver_events.FirewallDomainListEvents.DNSFirewallBlock.DnsFirewallBlockItem(
                            resolver_endpoint_details=route53resolver_events.FirewallDomainListEvents.DNSFirewallBlock.ResolverEndpointDetails(
                                id=["id"]
                            ),
                            resolver_network_interface_details=route53resolver_events.FirewallDomainListEvents.DNSFirewallBlock.ResolverNetworkInterfaceDetails(
                                id=["id"]
                            ),
                            resource_type=["resourceType"]
                        )],
                        src_addr=["srcAddr"],
                        src_port=["srcPort"],
                        transport=["transport"],
                        vpc_id=["vpcId"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__c969118b5830d6e7c8117988101deeabd95d5e6e276f22cfe0d59feb98caa321)
                    check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument firewall_domain_list_id", value=firewall_domain_list_id, expected_type=type_hints["firewall_domain_list_id"])
                    check_type(argname="argument firewall_rule_action", value=firewall_rule_action, expected_type=type_hints["firewall_rule_action"])
                    check_type(argname="argument firewall_rule_group_id", value=firewall_rule_group_id, expected_type=type_hints["firewall_rule_group_id"])
                    check_type(argname="argument last_observed_at", value=last_observed_at, expected_type=type_hints["last_observed_at"])
                    check_type(argname="argument query_class", value=query_class, expected_type=type_hints["query_class"])
                    check_type(argname="argument query_name", value=query_name, expected_type=type_hints["query_name"])
                    check_type(argname="argument query_type", value=query_type, expected_type=type_hints["query_type"])
                    check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
                    check_type(argname="argument src_addr", value=src_addr, expected_type=type_hints["src_addr"])
                    check_type(argname="argument src_port", value=src_port, expected_type=type_hints["src_port"])
                    check_type(argname="argument transport", value=transport, expected_type=type_hints["transport"])
                    check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if account_id is not None:
                    self._values["account_id"] = account_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if firewall_domain_list_id is not None:
                    self._values["firewall_domain_list_id"] = firewall_domain_list_id
                if firewall_rule_action is not None:
                    self._values["firewall_rule_action"] = firewall_rule_action
                if firewall_rule_group_id is not None:
                    self._values["firewall_rule_group_id"] = firewall_rule_group_id
                if last_observed_at is not None:
                    self._values["last_observed_at"] = last_observed_at
                if query_class is not None:
                    self._values["query_class"] = query_class
                if query_name is not None:
                    self._values["query_name"] = query_name
                if query_type is not None:
                    self._values["query_type"] = query_type
                if resources is not None:
                    self._values["resources"] = resources
                if src_addr is not None:
                    self._values["src_addr"] = src_addr
                if src_port is not None:
                    self._values["src_port"] = src_port
                if transport is not None:
                    self._values["transport"] = transport
                if vpc_id is not None:
                    self._values["vpc_id"] = vpc_id

            @builtins.property
            def account_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) account-id property.

                Specify an array of string values to match this event if the actual value of account-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("account_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_metadata(
                self,
            ) -> typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps]:
                '''(experimental) EventBridge event metadata.

                :default:

                -
                -

                :stability: experimental
                '''
                result = self._values.get("event_metadata")
                return typing.cast(typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps], result)

            @builtins.property
            def firewall_domain_list_id(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) firewall-domain-list-id property.

                Specify an array of string values to match this event if the actual value of firewall-domain-list-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the FirewallDomainList reference

                :stability: experimental
                '''
                result = self._values.get("firewall_domain_list_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def firewall_rule_action(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) firewall-rule-action property.

                Specify an array of string values to match this event if the actual value of firewall-rule-action is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("firewall_rule_action")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def firewall_rule_group_id(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) firewall-rule-group-id property.

                Specify an array of string values to match this event if the actual value of firewall-rule-group-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("firewall_rule_group_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def last_observed_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) last-observed-at property.

                Specify an array of string values to match this event if the actual value of last-observed-at is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("last_observed_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def query_class(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) query-class property.

                Specify an array of string values to match this event if the actual value of query-class is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("query_class")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def query_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) query-name property.

                Specify an array of string values to match this event if the actual value of query-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("query_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def query_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) query-type property.

                Specify an array of string values to match this event if the actual value of query-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("query_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def resources(
                self,
            ) -> typing.Optional[typing.List["FirewallDomainListEvents.DNSFirewallBlock.DnsFirewallBlockItem"]]:
                '''(experimental) resources property.

                Specify an array of string values to match this event if the actual value of resources is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("resources")
                return typing.cast(typing.Optional[typing.List["FirewallDomainListEvents.DNSFirewallBlock.DnsFirewallBlockItem"]], result)

            @builtins.property
            def src_addr(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) src-addr property.

                Specify an array of string values to match this event if the actual value of src-addr is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("src_addr")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def src_port(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) src-port property.

                Specify an array of string values to match this event if the actual value of src-port is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("src_port")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def transport(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) transport property.

                Specify an array of string values to match this event if the actual value of transport is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("transport")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def vpc_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) vpc-id property.

                Specify an array of string values to match this event if the actual value of vpc-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("vpc_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "DNSFirewallBlockProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.events.FirewallDomainListEvents.DNSFirewallBlock.DnsFirewallBlockItem",
            jsii_struct_bases=[],
            name_mapping={
                "resolver_endpoint_details": "resolverEndpointDetails",
                "resolver_network_interface_details": "resolverNetworkInterfaceDetails",
                "resource_type": "resourceType",
            },
        )
        class DnsFirewallBlockItem:
            def __init__(
                self,
                *,
                resolver_endpoint_details: typing.Optional[typing.Union["FirewallDomainListEvents.DNSFirewallBlock.ResolverEndpointDetails", typing.Dict[builtins.str, typing.Any]]] = None,
                resolver_network_interface_details: typing.Optional[typing.Union["FirewallDomainListEvents.DNSFirewallBlock.ResolverNetworkInterfaceDetails", typing.Dict[builtins.str, typing.Any]]] = None,
                resource_type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for DNSFirewallBlockItem.

                :param resolver_endpoint_details: (experimental) resolver-endpoint-details property. Specify an array of string values to match this event if the actual value of resolver-endpoint-details is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param resolver_network_interface_details: (experimental) resolver-network-interface-details property. Specify an array of string values to match this event if the actual value of resolver-network-interface-details is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param resource_type: (experimental) resource-type property. Specify an array of string values to match this event if the actual value of resource-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_route53resolver import events as route53resolver_events
                    
                    dns_firewall_block_item = route53resolver_events.FirewallDomainListEvents.DNSFirewallBlock.DnsFirewallBlockItem(
                        resolver_endpoint_details=route53resolver_events.FirewallDomainListEvents.DNSFirewallBlock.ResolverEndpointDetails(
                            id=["id"]
                        ),
                        resolver_network_interface_details=route53resolver_events.FirewallDomainListEvents.DNSFirewallBlock.ResolverNetworkInterfaceDetails(
                            id=["id"]
                        ),
                        resource_type=["resourceType"]
                    )
                '''
                if isinstance(resolver_endpoint_details, dict):
                    resolver_endpoint_details = FirewallDomainListEvents.DNSFirewallBlock.ResolverEndpointDetails(**resolver_endpoint_details)
                if isinstance(resolver_network_interface_details, dict):
                    resolver_network_interface_details = FirewallDomainListEvents.DNSFirewallBlock.ResolverNetworkInterfaceDetails(**resolver_network_interface_details)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__e4249d4dc322d6beb6b19bb0f3f847eeaa4edb7aae72e8d45604577a75188d25)
                    check_type(argname="argument resolver_endpoint_details", value=resolver_endpoint_details, expected_type=type_hints["resolver_endpoint_details"])
                    check_type(argname="argument resolver_network_interface_details", value=resolver_network_interface_details, expected_type=type_hints["resolver_network_interface_details"])
                    check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if resolver_endpoint_details is not None:
                    self._values["resolver_endpoint_details"] = resolver_endpoint_details
                if resolver_network_interface_details is not None:
                    self._values["resolver_network_interface_details"] = resolver_network_interface_details
                if resource_type is not None:
                    self._values["resource_type"] = resource_type

            @builtins.property
            def resolver_endpoint_details(
                self,
            ) -> typing.Optional["FirewallDomainListEvents.DNSFirewallBlock.ResolverEndpointDetails"]:
                '''(experimental) resolver-endpoint-details property.

                Specify an array of string values to match this event if the actual value of resolver-endpoint-details is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("resolver_endpoint_details")
                return typing.cast(typing.Optional["FirewallDomainListEvents.DNSFirewallBlock.ResolverEndpointDetails"], result)

            @builtins.property
            def resolver_network_interface_details(
                self,
            ) -> typing.Optional["FirewallDomainListEvents.DNSFirewallBlock.ResolverNetworkInterfaceDetails"]:
                '''(experimental) resolver-network-interface-details property.

                Specify an array of string values to match this event if the actual value of resolver-network-interface-details is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("resolver_network_interface_details")
                return typing.cast(typing.Optional["FirewallDomainListEvents.DNSFirewallBlock.ResolverNetworkInterfaceDetails"], result)

            @builtins.property
            def resource_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) resource-type property.

                Specify an array of string values to match this event if the actual value of resource-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("resource_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "DnsFirewallBlockItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.events.FirewallDomainListEvents.DNSFirewallBlock.ResolverEndpointDetails",
            jsii_struct_bases=[],
            name_mapping={"id": "id"},
        )
        class ResolverEndpointDetails:
            def __init__(
                self,
                *,
                id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Resolver-endpoint-details.

                :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_route53resolver import events as route53resolver_events
                    
                    resolver_endpoint_details = route53resolver_events.FirewallDomainListEvents.DNSFirewallBlock.ResolverEndpointDetails(
                        id=["id"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__a72e486ef0f62a94f37f7dfb3558a060a50f872d559a1ebb103dd7566a9052c2)
                    check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if id is not None:
                    self._values["id"] = id

            @builtins.property
            def id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) id property.

                Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ResolverEndpointDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.events.FirewallDomainListEvents.DNSFirewallBlock.ResolverNetworkInterfaceDetails",
            jsii_struct_bases=[],
            name_mapping={"id": "id"},
        )
        class ResolverNetworkInterfaceDetails:
            def __init__(
                self,
                *,
                id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Resolver-network-interface-details.

                :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_route53resolver import events as route53resolver_events
                    
                    resolver_network_interface_details = route53resolver_events.FirewallDomainListEvents.DNSFirewallBlock.ResolverNetworkInterfaceDetails(
                        id=["id"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__4f81aa50179f1cf9dc22619d0fb3c6156da0210113cf59bfa1b649e085604ff8)
                    check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if id is not None:
                    self._values["id"] = id

            @builtins.property
            def id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) id property.

                Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ResolverNetworkInterfaceDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


__all__ = [
    "FirewallDomainListEvents",
]

publication.publish()

def _typecheckingstub__d8f9333cd1abe443af66f332fb80ff4c96606a874572ac7aa4bd4d41552113fa(
    firewall_domain_list_ref: _aws_cdk_interfaces_aws_route53resolver_ceddda9d.IFirewallDomainListRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3887570322b9e0da6dff0cccfda9f46463eddbddd9136a3b8eef7da5dbeab70a(
    *,
    account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    firewall_domain_list_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    firewall_rule_action: typing.Optional[typing.Sequence[builtins.str]] = None,
    firewall_rule_group_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    last_observed_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_class: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    resources: typing.Optional[typing.Sequence[typing.Union[FirewallDomainListEvents.DNSFirewallAlert.DnsFirewallAlertItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    src_addr: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_port: typing.Optional[typing.Sequence[builtins.str]] = None,
    transport: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f864db1c3f1c22dae0cda7830b25db530111d7841235f2ed55a0e95e8fd8bee(
    *,
    resolver_endpoint_details: typing.Optional[typing.Union[FirewallDomainListEvents.DNSFirewallAlert.ResolverEndpointDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    resolver_network_interface_details: typing.Optional[typing.Union[FirewallDomainListEvents.DNSFirewallAlert.ResolverNetworkInterfaceDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cabccc009fcc3e72e93b577665ea810fb1ba8d867b669c7d99c8e20877128a96(
    *,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90b40aa77f3ab22e8a9cbdb9f9c66b46a9927ff7d563081462d176990cf4301e(
    *,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c969118b5830d6e7c8117988101deeabd95d5e6e276f22cfe0d59feb98caa321(
    *,
    account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    firewall_domain_list_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    firewall_rule_action: typing.Optional[typing.Sequence[builtins.str]] = None,
    firewall_rule_group_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    last_observed_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_class: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    resources: typing.Optional[typing.Sequence[typing.Union[FirewallDomainListEvents.DNSFirewallBlock.DnsFirewallBlockItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    src_addr: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_port: typing.Optional[typing.Sequence[builtins.str]] = None,
    transport: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4249d4dc322d6beb6b19bb0f3f847eeaa4edb7aae72e8d45604577a75188d25(
    *,
    resolver_endpoint_details: typing.Optional[typing.Union[FirewallDomainListEvents.DNSFirewallBlock.ResolverEndpointDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    resolver_network_interface_details: typing.Optional[typing.Union[FirewallDomainListEvents.DNSFirewallBlock.ResolverNetworkInterfaceDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a72e486ef0f62a94f37f7dfb3558a060a50f872d559a1ebb103dd7566a9052c2(
    *,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f81aa50179f1cf9dc22619d0fb3c6156da0210113cf59bfa1b649e085604ff8(
    *,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
