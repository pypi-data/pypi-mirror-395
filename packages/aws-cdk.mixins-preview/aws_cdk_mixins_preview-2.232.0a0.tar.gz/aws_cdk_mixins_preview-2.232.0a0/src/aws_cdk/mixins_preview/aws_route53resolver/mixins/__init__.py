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
    jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnFirewallDomainListMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain_file_url": "domainFileUrl",
        "domains": "domains",
        "name": "name",
        "tags": "tags",
    },
)
class CfnFirewallDomainListMixinProps:
    def __init__(
        self,
        *,
        domain_file_url: typing.Optional[builtins.str] = None,
        domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnFirewallDomainListPropsMixin.

        :param domain_file_url: The fully qualified URL or URI of the file stored in Amazon Simple Storage Service (Amazon S3) that contains the list of domains to import. The file must be in an S3 bucket that's in the same Region as your DNS Firewall. The file must be a text file and must contain a single domain per line.
        :param domains: A list of the domain lists that you have defined.
        :param name: The name of the domain list.
        :param tags: A list of the tag keys and values that you want to associate with the domain list.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewalldomainlist.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
            
            cfn_firewall_domain_list_mixin_props = route53resolver_mixins.CfnFirewallDomainListMixinProps(
                domain_file_url="domainFileUrl",
                domains=["domains"],
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b088adbd7873e422111b2f2099f497ef81fb60826a6c151a713dbf68665162dd)
            check_type(argname="argument domain_file_url", value=domain_file_url, expected_type=type_hints["domain_file_url"])
            check_type(argname="argument domains", value=domains, expected_type=type_hints["domains"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain_file_url is not None:
            self._values["domain_file_url"] = domain_file_url
        if domains is not None:
            self._values["domains"] = domains
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def domain_file_url(self) -> typing.Optional[builtins.str]:
        '''The fully qualified URL or URI of the file stored in Amazon Simple Storage Service (Amazon S3) that contains the list of domains to import.

        The file must be in an S3 bucket that's in the same Region as your DNS Firewall. The file must be a text file and must contain a single domain per line.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewalldomainlist.html#cfn-route53resolver-firewalldomainlist-domainfileurl
        '''
        result = self._values.get("domain_file_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of the domain lists that you have defined.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewalldomainlist.html#cfn-route53resolver-firewalldomainlist-domains
        '''
        result = self._values.get("domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the domain list.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewalldomainlist.html#cfn-route53resolver-firewalldomainlist-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of the tag keys and values that you want to associate with the domain list.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewalldomainlist.html#cfn-route53resolver-firewalldomainlist-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFirewallDomainListMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFirewallDomainListPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnFirewallDomainListPropsMixin",
):
    '''High-level information about a list of firewall domains for use in a `AWS::Route53Resolver::FirewallRule <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-firewallrulegroup-rule.html>`_ . This is returned by `GetFirewallDomainList <https://docs.aws.amazon.com/Route53/latest/APIReference/API_route53resolver_GetFirewallDomainList.html>`_ .

    To retrieve the domains that are defined for this domain list, call `ListFirewallDomains <https://docs.aws.amazon.com/Route53/latest/APIReference/API_route53resolver_ListFirewallDomains.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewalldomainlist.html
    :cloudformationResource: AWS::Route53Resolver::FirewallDomainList
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
        
        cfn_firewall_domain_list_props_mixin = route53resolver_mixins.CfnFirewallDomainListPropsMixin(route53resolver_mixins.CfnFirewallDomainListMixinProps(
            domain_file_url="domainFileUrl",
            domains=["domains"],
            name="name",
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
        props: typing.Union[CfnFirewallDomainListMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Route53Resolver::FirewallDomainList``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78f815fe419929c4bb953388d40e117f4610e8596b4d6d251957668781246212)
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
            type_hints = typing.get_type_hints(_typecheckingstub__914a7f139dfd119c35d6ad1bc64f2b2df3b2ebc076d5495a7dad2eededa5dbec)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f5b1ce26830c09dcf5eeb57f099c7f7f5a14396d988f16bb2abf0b70bfe405)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFirewallDomainListMixinProps:
        return typing.cast(CfnFirewallDomainListMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnFirewallRuleGroupAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "firewall_rule_group_id": "firewallRuleGroupId",
        "mutation_protection": "mutationProtection",
        "name": "name",
        "priority": "priority",
        "tags": "tags",
        "vpc_id": "vpcId",
    },
)
class CfnFirewallRuleGroupAssociationMixinProps:
    def __init__(
        self,
        *,
        firewall_rule_group_id: typing.Optional[builtins.str] = None,
        mutation_protection: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnFirewallRuleGroupAssociationPropsMixin.

        :param firewall_rule_group_id: The unique identifier of the firewall rule group.
        :param mutation_protection: If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections.
        :param name: The name of the association.
        :param priority: The setting that determines the processing order of the rule group among the rule groups that are associated with a single VPC. DNS Firewall filters VPC traffic starting from rule group with the lowest numeric priority setting. You must specify a unique priority for each rule group that you associate with a single VPC. To make it easier to insert rule groups later, leave space between the numbers, for example, use 101, 200, and so on. You can change the priority setting for a rule group association after you create it. The allowed values for ``Priority`` are between 100 and 9900 (excluding 100 and 9900).
        :param tags: A list of the tag keys and values that you want to associate with the rule group.
        :param vpc_id: The unique identifier of the VPC that is associated with the rule group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
            
            cfn_firewall_rule_group_association_mixin_props = route53resolver_mixins.CfnFirewallRuleGroupAssociationMixinProps(
                firewall_rule_group_id="firewallRuleGroupId",
                mutation_protection="mutationProtection",
                name="name",
                priority=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_id="vpcId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37161a9e8655c2938d4eedf96da023c200a8f35fa6875ecbfdee1af93946b537)
            check_type(argname="argument firewall_rule_group_id", value=firewall_rule_group_id, expected_type=type_hints["firewall_rule_group_id"])
            check_type(argname="argument mutation_protection", value=mutation_protection, expected_type=type_hints["mutation_protection"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if firewall_rule_group_id is not None:
            self._values["firewall_rule_group_id"] = firewall_rule_group_id
        if mutation_protection is not None:
            self._values["mutation_protection"] = mutation_protection
        if name is not None:
            self._values["name"] = name
        if priority is not None:
            self._values["priority"] = priority
        if tags is not None:
            self._values["tags"] = tags
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def firewall_rule_group_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the firewall rule group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html#cfn-route53resolver-firewallrulegroupassociation-firewallrulegroupid
        '''
        result = self._values.get("firewall_rule_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mutation_protection(self) -> typing.Optional[builtins.str]:
        '''If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html#cfn-route53resolver-firewallrulegroupassociation-mutationprotection
        '''
        result = self._values.get("mutation_protection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html#cfn-route53resolver-firewallrulegroupassociation-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''The setting that determines the processing order of the rule group among the rule groups that are associated with a single VPC.

        DNS Firewall filters VPC traffic starting from rule group with the lowest numeric priority setting.

        You must specify a unique priority for each rule group that you associate with a single VPC. To make it easier to insert rule groups later, leave space between the numbers, for example, use 101, 200, and so on. You can change the priority setting for a rule group association after you create it.

        The allowed values for ``Priority`` are between 100 and 9900 (excluding 100 and 9900).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html#cfn-route53resolver-firewallrulegroupassociation-priority
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of the tag keys and values that you want to associate with the rule group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html#cfn-route53resolver-firewallrulegroupassociation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the VPC that is associated with the rule group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html#cfn-route53resolver-firewallrulegroupassociation-vpcid
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFirewallRuleGroupAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFirewallRuleGroupAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnFirewallRuleGroupAssociationPropsMixin",
):
    '''An association between a firewall rule group and a VPC, which enables DNS filtering for the VPC.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html
    :cloudformationResource: AWS::Route53Resolver::FirewallRuleGroupAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
        
        cfn_firewall_rule_group_association_props_mixin = route53resolver_mixins.CfnFirewallRuleGroupAssociationPropsMixin(route53resolver_mixins.CfnFirewallRuleGroupAssociationMixinProps(
            firewall_rule_group_id="firewallRuleGroupId",
            mutation_protection="mutationProtection",
            name="name",
            priority=123,
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
        props: typing.Union[CfnFirewallRuleGroupAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Route53Resolver::FirewallRuleGroupAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb70a7983757949c88fa7c5e6a5eeda2d328cfe7ced42cf570bda2017b9ddc36)
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
            type_hints = typing.get_type_hints(_typecheckingstub__414d73416c95a578d928845c838bd9858a639fd8e0cb01f49929ffeca17aa0ee)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__425cfff78ad7e57a3e3d805aaaaf21e7ccae3896b3a7b264edda994bf8bf3b57)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFirewallRuleGroupAssociationMixinProps:
        return typing.cast(CfnFirewallRuleGroupAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnFirewallRuleGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={"firewall_rules": "firewallRules", "name": "name", "tags": "tags"},
)
class CfnFirewallRuleGroupMixinProps:
    def __init__(
        self,
        *,
        firewall_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFirewallRuleGroupPropsMixin.FirewallRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnFirewallRuleGroupPropsMixin.

        :param firewall_rules: A list of the rules that you have defined.
        :param name: The name of the rule group.
        :param tags: A list of the tag keys and values that you want to associate with the rule group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
            
            cfn_firewall_rule_group_mixin_props = route53resolver_mixins.CfnFirewallRuleGroupMixinProps(
                firewall_rules=[route53resolver_mixins.CfnFirewallRuleGroupPropsMixin.FirewallRuleProperty(
                    action="action",
                    block_override_dns_type="blockOverrideDnsType",
                    block_override_domain="blockOverrideDomain",
                    block_override_ttl=123,
                    block_response="blockResponse",
                    confidence_threshold="confidenceThreshold",
                    dns_threat_protection="dnsThreatProtection",
                    firewall_domain_list_id="firewallDomainListId",
                    firewall_domain_redirection_action="firewallDomainRedirectionAction",
                    firewall_threat_protection_id="firewallThreatProtectionId",
                    priority=123,
                    qtype="qtype"
                )],
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0a979ed1dddf3f3678a80bff4a1f26212bf21b05879b479295bbe3c9bf0d1f8)
            check_type(argname="argument firewall_rules", value=firewall_rules, expected_type=type_hints["firewall_rules"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if firewall_rules is not None:
            self._values["firewall_rules"] = firewall_rules
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def firewall_rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallRuleGroupPropsMixin.FirewallRuleProperty"]]]]:
        '''A list of the rules that you have defined.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroup.html#cfn-route53resolver-firewallrulegroup-firewallrules
        '''
        result = self._values.get("firewall_rules")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFirewallRuleGroupPropsMixin.FirewallRuleProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the rule group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroup.html#cfn-route53resolver-firewallrulegroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of the tag keys and values that you want to associate with the rule group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroup.html#cfn-route53resolver-firewallrulegroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFirewallRuleGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFirewallRuleGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnFirewallRuleGroupPropsMixin",
):
    '''High-level information for a firewall rule group.

    A firewall rule group is a collection of rules that DNS Firewall uses to filter DNS network traffic for a VPC. To retrieve the rules for the rule group, call `ListFirewallRules <https://docs.aws.amazon.com/Route53/latest/APIReference/API_route53resolver_ListFirewallRules.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroup.html
    :cloudformationResource: AWS::Route53Resolver::FirewallRuleGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
        
        cfn_firewall_rule_group_props_mixin = route53resolver_mixins.CfnFirewallRuleGroupPropsMixin(route53resolver_mixins.CfnFirewallRuleGroupMixinProps(
            firewall_rules=[route53resolver_mixins.CfnFirewallRuleGroupPropsMixin.FirewallRuleProperty(
                action="action",
                block_override_dns_type="blockOverrideDnsType",
                block_override_domain="blockOverrideDomain",
                block_override_ttl=123,
                block_response="blockResponse",
                confidence_threshold="confidenceThreshold",
                dns_threat_protection="dnsThreatProtection",
                firewall_domain_list_id="firewallDomainListId",
                firewall_domain_redirection_action="firewallDomainRedirectionAction",
                firewall_threat_protection_id="firewallThreatProtectionId",
                priority=123,
                qtype="qtype"
            )],
            name="name",
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
        props: typing.Union[CfnFirewallRuleGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Route53Resolver::FirewallRuleGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5243d8599026e3b9898491e9c5fa84394c40212a6dcd99545014ed8a1c947b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__625bff58f0e03dc942ba62b2ab0c1f6ddc2f1008bc6fd8d9bf4746589f7dd635)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a40345491d4836232835616c0e244299e0f53bfb87913923bbcd30e3cb0d6e39)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFirewallRuleGroupMixinProps:
        return typing.cast(CfnFirewallRuleGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnFirewallRuleGroupPropsMixin.FirewallRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "block_override_dns_type": "blockOverrideDnsType",
            "block_override_domain": "blockOverrideDomain",
            "block_override_ttl": "blockOverrideTtl",
            "block_response": "blockResponse",
            "confidence_threshold": "confidenceThreshold",
            "dns_threat_protection": "dnsThreatProtection",
            "firewall_domain_list_id": "firewallDomainListId",
            "firewall_domain_redirection_action": "firewallDomainRedirectionAction",
            "firewall_threat_protection_id": "firewallThreatProtectionId",
            "priority": "priority",
            "qtype": "qtype",
        },
    )
    class FirewallRuleProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            block_override_dns_type: typing.Optional[builtins.str] = None,
            block_override_domain: typing.Optional[builtins.str] = None,
            block_override_ttl: typing.Optional[jsii.Number] = None,
            block_response: typing.Optional[builtins.str] = None,
            confidence_threshold: typing.Optional[builtins.str] = None,
            dns_threat_protection: typing.Optional[builtins.str] = None,
            firewall_domain_list_id: typing.Optional[builtins.str] = None,
            firewall_domain_redirection_action: typing.Optional[builtins.str] = None,
            firewall_threat_protection_id: typing.Optional[builtins.str] = None,
            priority: typing.Optional[jsii.Number] = None,
            qtype: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A single firewall rule in a rule group.

            :param action: The action that DNS Firewall should take on a DNS query when it matches one of the domains in the rule's domain list, or a threat in a DNS Firewall Advvanced rule: - ``ALLOW`` - Permit the request to go through. Not available for DNS Firewall Advanced rules. - ``ALERT`` - Permit the request to go through but send an alert to the logs. - ``BLOCK`` - Disallow the request. If this is specified,then ``BlockResponse`` must also be specified. if ``BlockResponse`` is ``OVERRIDE`` , then all of the following ``OVERRIDE`` attributes must be specified: - ``BlockOverrideDnsType`` - ``BlockOverrideDomain`` - ``BlockOverrideTtl``
            :param block_override_dns_type: The DNS record's type. This determines the format of the record value that you provided in ``BlockOverrideDomain`` . Used for the rule action ``BLOCK`` with a ``BlockResponse`` setting of ``OVERRIDE`` .
            :param block_override_domain: The custom DNS record to send back in response to the query. Used for the rule action ``BLOCK`` with a ``BlockResponse`` setting of ``OVERRIDE`` .
            :param block_override_ttl: The recommended amount of time, in seconds, for the DNS resolver or web browser to cache the provided override record. Used for the rule action ``BLOCK`` with a ``BlockResponse`` setting of ``OVERRIDE`` .
            :param block_response: The way that you want DNS Firewall to block the request. Used for the rule action setting ``BLOCK`` . - ``NODATA`` - Respond indicating that the query was successful, but no response is available for it. - ``NXDOMAIN`` - Respond indicating that the domain name that's in the query doesn't exist. - ``OVERRIDE`` - Provide a custom override in the response. This option requires custom handling details in the rule's ``BlockOverride*`` settings.
            :param confidence_threshold: The confidence threshold for DNS Firewall Advanced. You must provide this value when you create a DNS Firewall Advanced rule. The confidence level values mean: - ``LOW`` : Provides the highest detection rate for threats, but also increases false positives. - ``MEDIUM`` : Provides a balance between detecting threats and false positives. - ``HIGH`` : Detects only the most well corroborated threats with a low rate of false positives.
            :param dns_threat_protection: The type of the DNS Firewall Advanced rule. Valid values are:. - ``DGA`` : Domain generation algorithms detection. DGAs are used by attackers to generate a large number of domains to to launch malware attacks. - ``DNS_TUNNELING`` : DNS tunneling detection. DNS tunneling is used by attackers to exfiltrate data from the client by using the DNS tunnel without making a network connection to the client.
            :param firewall_domain_list_id: The ID of the domain list that's used in the rule.
            :param firewall_domain_redirection_action: How you want the the rule to evaluate DNS redirection in the DNS redirection chain, such as CNAME, or DNAME. ``Inspect_Redirection_Domain`` (Default) inspects all domains in the redirection chain. The individual domains in the redirection chain must be added to the domain list. ``Trust_Redirection_Domain`` inspects only the first domain in the redirection chain. You don't need to add the subsequent domains in the domain in the redirection list to the domain list.
            :param firewall_threat_protection_id: ID of the DNS Firewall Advanced rule.
            :param priority: The priority of the rule in the rule group. This value must be unique within the rule group. DNS Firewall processes the rules in a rule group by order of priority, starting from the lowest setting.
            :param qtype: The DNS query type you want the rule to evaluate. Allowed values are; - A: Returns an IPv4 address. - AAAA: Returns an Ipv6 address. - CAA: Restricts CAs that can create SSL/TLS certifications for the domain. - CNAME: Returns another domain name. - DS: Record that identifies the DNSSEC signing key of a delegated zone. - MX: Specifies mail servers. - NAPTR: Regular-expression-based rewriting of domain names. - NS: Authoritative name servers. - PTR: Maps an IP address to a domain name. - SOA: Start of authority record for the zone. - SPF: Lists the servers authorized to send emails from a domain. - SRV: Application specific values that identify servers. - TXT: Verifies email senders and application-specific values. - A query type you define by using the DNS type ID, for example 28 for AAAA. The values must be defined as TYPE NUMBER , where the NUMBER can be 1-65334, for example, TYPE28. For more information, see `List of DNS record types <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/List_of_DNS_record_types>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-firewallrulegroup-firewallrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
                
                firewall_rule_property = route53resolver_mixins.CfnFirewallRuleGroupPropsMixin.FirewallRuleProperty(
                    action="action",
                    block_override_dns_type="blockOverrideDnsType",
                    block_override_domain="blockOverrideDomain",
                    block_override_ttl=123,
                    block_response="blockResponse",
                    confidence_threshold="confidenceThreshold",
                    dns_threat_protection="dnsThreatProtection",
                    firewall_domain_list_id="firewallDomainListId",
                    firewall_domain_redirection_action="firewallDomainRedirectionAction",
                    firewall_threat_protection_id="firewallThreatProtectionId",
                    priority=123,
                    qtype="qtype"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__630bbb3dcd018fe614e1e3da398951fc9bd3773f76f2a638819f6363e757d127)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument block_override_dns_type", value=block_override_dns_type, expected_type=type_hints["block_override_dns_type"])
                check_type(argname="argument block_override_domain", value=block_override_domain, expected_type=type_hints["block_override_domain"])
                check_type(argname="argument block_override_ttl", value=block_override_ttl, expected_type=type_hints["block_override_ttl"])
                check_type(argname="argument block_response", value=block_response, expected_type=type_hints["block_response"])
                check_type(argname="argument confidence_threshold", value=confidence_threshold, expected_type=type_hints["confidence_threshold"])
                check_type(argname="argument dns_threat_protection", value=dns_threat_protection, expected_type=type_hints["dns_threat_protection"])
                check_type(argname="argument firewall_domain_list_id", value=firewall_domain_list_id, expected_type=type_hints["firewall_domain_list_id"])
                check_type(argname="argument firewall_domain_redirection_action", value=firewall_domain_redirection_action, expected_type=type_hints["firewall_domain_redirection_action"])
                check_type(argname="argument firewall_threat_protection_id", value=firewall_threat_protection_id, expected_type=type_hints["firewall_threat_protection_id"])
                check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
                check_type(argname="argument qtype", value=qtype, expected_type=type_hints["qtype"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if block_override_dns_type is not None:
                self._values["block_override_dns_type"] = block_override_dns_type
            if block_override_domain is not None:
                self._values["block_override_domain"] = block_override_domain
            if block_override_ttl is not None:
                self._values["block_override_ttl"] = block_override_ttl
            if block_response is not None:
                self._values["block_response"] = block_response
            if confidence_threshold is not None:
                self._values["confidence_threshold"] = confidence_threshold
            if dns_threat_protection is not None:
                self._values["dns_threat_protection"] = dns_threat_protection
            if firewall_domain_list_id is not None:
                self._values["firewall_domain_list_id"] = firewall_domain_list_id
            if firewall_domain_redirection_action is not None:
                self._values["firewall_domain_redirection_action"] = firewall_domain_redirection_action
            if firewall_threat_protection_id is not None:
                self._values["firewall_threat_protection_id"] = firewall_threat_protection_id
            if priority is not None:
                self._values["priority"] = priority
            if qtype is not None:
                self._values["qtype"] = qtype

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action that DNS Firewall should take on a DNS query when it matches one of the domains in the rule's domain list, or a threat in a DNS Firewall Advvanced rule:  - ``ALLOW`` - Permit the request to go through.

            Not available for DNS Firewall Advanced rules.

            - ``ALERT`` - Permit the request to go through but send an alert to the logs.
            - ``BLOCK`` - Disallow the request. If this is specified,then ``BlockResponse`` must also be specified.

            if ``BlockResponse`` is ``OVERRIDE`` , then all of the following ``OVERRIDE`` attributes must be specified:

            - ``BlockOverrideDnsType``
            - ``BlockOverrideDomain``
            - ``BlockOverrideTtl``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-firewallrulegroup-firewallrule.html#cfn-route53resolver-firewallrulegroup-firewallrule-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def block_override_dns_type(self) -> typing.Optional[builtins.str]:
            '''The DNS record's type.

            This determines the format of the record value that you provided in ``BlockOverrideDomain`` . Used for the rule action ``BLOCK`` with a ``BlockResponse`` setting of ``OVERRIDE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-firewallrulegroup-firewallrule.html#cfn-route53resolver-firewallrulegroup-firewallrule-blockoverridednstype
            '''
            result = self._values.get("block_override_dns_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def block_override_domain(self) -> typing.Optional[builtins.str]:
            '''The custom DNS record to send back in response to the query.

            Used for the rule action ``BLOCK`` with a ``BlockResponse`` setting of ``OVERRIDE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-firewallrulegroup-firewallrule.html#cfn-route53resolver-firewallrulegroup-firewallrule-blockoverridedomain
            '''
            result = self._values.get("block_override_domain")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def block_override_ttl(self) -> typing.Optional[jsii.Number]:
            '''The recommended amount of time, in seconds, for the DNS resolver or web browser to cache the provided override record.

            Used for the rule action ``BLOCK`` with a ``BlockResponse`` setting of ``OVERRIDE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-firewallrulegroup-firewallrule.html#cfn-route53resolver-firewallrulegroup-firewallrule-blockoverridettl
            '''
            result = self._values.get("block_override_ttl")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def block_response(self) -> typing.Optional[builtins.str]:
            '''The way that you want DNS Firewall to block the request. Used for the rule action setting ``BLOCK`` .

            - ``NODATA`` - Respond indicating that the query was successful, but no response is available for it.
            - ``NXDOMAIN`` - Respond indicating that the domain name that's in the query doesn't exist.
            - ``OVERRIDE`` - Provide a custom override in the response. This option requires custom handling details in the rule's ``BlockOverride*`` settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-firewallrulegroup-firewallrule.html#cfn-route53resolver-firewallrulegroup-firewallrule-blockresponse
            '''
            result = self._values.get("block_response")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def confidence_threshold(self) -> typing.Optional[builtins.str]:
            '''The confidence threshold for DNS Firewall Advanced.

            You must provide this value when you create a DNS Firewall Advanced rule. The confidence level values mean:

            - ``LOW`` : Provides the highest detection rate for threats, but also increases false positives.
            - ``MEDIUM`` : Provides a balance between detecting threats and false positives.
            - ``HIGH`` : Detects only the most well corroborated threats with a low rate of false positives.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-firewallrulegroup-firewallrule.html#cfn-route53resolver-firewallrulegroup-firewallrule-confidencethreshold
            '''
            result = self._values.get("confidence_threshold")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dns_threat_protection(self) -> typing.Optional[builtins.str]:
            '''The type of the DNS Firewall Advanced rule. Valid values are:.

            - ``DGA`` : Domain generation algorithms detection. DGAs are used by attackers to generate a large number of domains to to launch malware attacks.
            - ``DNS_TUNNELING`` : DNS tunneling detection. DNS tunneling is used by attackers to exfiltrate data from the client by using the DNS tunnel without making a network connection to the client.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-firewallrulegroup-firewallrule.html#cfn-route53resolver-firewallrulegroup-firewallrule-dnsthreatprotection
            '''
            result = self._values.get("dns_threat_protection")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def firewall_domain_list_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the domain list that's used in the rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-firewallrulegroup-firewallrule.html#cfn-route53resolver-firewallrulegroup-firewallrule-firewalldomainlistid
            '''
            result = self._values.get("firewall_domain_list_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def firewall_domain_redirection_action(self) -> typing.Optional[builtins.str]:
            '''How you want the the rule to evaluate DNS redirection in the DNS redirection chain, such as CNAME, or DNAME.

            ``Inspect_Redirection_Domain`` (Default) inspects all domains in the redirection chain. The individual domains in the redirection chain must be added to the domain list.

            ``Trust_Redirection_Domain`` inspects only the first domain in the redirection chain. You don't need to add the subsequent domains in the domain in the redirection list to the domain list.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-firewallrulegroup-firewallrule.html#cfn-route53resolver-firewallrulegroup-firewallrule-firewalldomainredirectionaction
            '''
            result = self._values.get("firewall_domain_redirection_action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def firewall_threat_protection_id(self) -> typing.Optional[builtins.str]:
            '''ID of the DNS Firewall Advanced rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-firewallrulegroup-firewallrule.html#cfn-route53resolver-firewallrulegroup-firewallrule-firewallthreatprotectionid
            '''
            result = self._values.get("firewall_threat_protection_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def priority(self) -> typing.Optional[jsii.Number]:
            '''The priority of the rule in the rule group.

            This value must be unique within the rule group. DNS Firewall processes the rules in a rule group by order of priority, starting from the lowest setting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-firewallrulegroup-firewallrule.html#cfn-route53resolver-firewallrulegroup-firewallrule-priority
            '''
            result = self._values.get("priority")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def qtype(self) -> typing.Optional[builtins.str]:
            '''The DNS query type you want the rule to evaluate. Allowed values are;

            - A: Returns an IPv4 address.
            - AAAA: Returns an Ipv6 address.
            - CAA: Restricts CAs that can create SSL/TLS certifications for the domain.
            - CNAME: Returns another domain name.
            - DS: Record that identifies the DNSSEC signing key of a delegated zone.
            - MX: Specifies mail servers.
            - NAPTR: Regular-expression-based rewriting of domain names.
            - NS: Authoritative name servers.
            - PTR: Maps an IP address to a domain name.
            - SOA: Start of authority record for the zone.
            - SPF: Lists the servers authorized to send emails from a domain.
            - SRV: Application specific values that identify servers.
            - TXT: Verifies email senders and application-specific values.
            - A query type you define by using the DNS type ID, for example 28 for AAAA. The values must be defined as TYPE NUMBER , where the NUMBER can be 1-65334, for example, TYPE28. For more information, see `List of DNS record types <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/List_of_DNS_record_types>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-firewallrulegroup-firewallrule.html#cfn-route53resolver-firewallrulegroup-firewallrule-qtype
            '''
            result = self._values.get("qtype")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FirewallRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnOutpostResolverMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_count": "instanceCount",
        "name": "name",
        "outpost_arn": "outpostArn",
        "preferred_instance_type": "preferredInstanceType",
        "tags": "tags",
    },
)
class CfnOutpostResolverMixinProps:
    def __init__(
        self,
        *,
        instance_count: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        outpost_arn: typing.Optional[builtins.str] = None,
        preferred_instance_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnOutpostResolverPropsMixin.

        :param instance_count: Amazon EC2 instance count for the Resolver on the Outpost.
        :param name: Name of the Resolver.
        :param outpost_arn: The ARN (Amazon Resource Name) for the Outpost.
        :param preferred_instance_type: The Amazon EC2 instance type. If you specify this, you must also specify a value for the ``OutpostArn`` .
        :param tags: A key value pair that helps you identify a Route 53 Resolver .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-outpostresolver.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
            
            cfn_outpost_resolver_mixin_props = route53resolver_mixins.CfnOutpostResolverMixinProps(
                instance_count=123,
                name="name",
                outpost_arn="outpostArn",
                preferred_instance_type="preferredInstanceType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ce1194929d42c1698259f4362c2aeb0a7d50dcf10994402f5a451292c829a79)
            check_type(argname="argument instance_count", value=instance_count, expected_type=type_hints["instance_count"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument outpost_arn", value=outpost_arn, expected_type=type_hints["outpost_arn"])
            check_type(argname="argument preferred_instance_type", value=preferred_instance_type, expected_type=type_hints["preferred_instance_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_count is not None:
            self._values["instance_count"] = instance_count
        if name is not None:
            self._values["name"] = name
        if outpost_arn is not None:
            self._values["outpost_arn"] = outpost_arn
        if preferred_instance_type is not None:
            self._values["preferred_instance_type"] = preferred_instance_type
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def instance_count(self) -> typing.Optional[jsii.Number]:
        '''Amazon EC2 instance count for the Resolver on the Outpost.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-outpostresolver.html#cfn-route53resolver-outpostresolver-instancecount
        '''
        result = self._values.get("instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the Resolver.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-outpostresolver.html#cfn-route53resolver-outpostresolver-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outpost_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN (Amazon Resource Name) for the Outpost.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-outpostresolver.html#cfn-route53resolver-outpostresolver-outpostarn
        '''
        result = self._values.get("outpost_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_instance_type(self) -> typing.Optional[builtins.str]:
        '''The Amazon EC2 instance type.

        If you specify this, you must also specify a value for the ``OutpostArn`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-outpostresolver.html#cfn-route53resolver-outpostresolver-preferredinstancetype
        '''
        result = self._values.get("preferred_instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A key value pair that helps you identify a Route 53 Resolver .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-outpostresolver.html#cfn-route53resolver-outpostresolver-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOutpostResolverMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnOutpostResolverPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnOutpostResolverPropsMixin",
):
    '''Creates a Amazon Route 53 Resolver on an Outpost.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-outpostresolver.html
    :cloudformationResource: AWS::Route53Resolver::OutpostResolver
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
        
        cfn_outpost_resolver_props_mixin = route53resolver_mixins.CfnOutpostResolverPropsMixin(route53resolver_mixins.CfnOutpostResolverMixinProps(
            instance_count=123,
            name="name",
            outpost_arn="outpostArn",
            preferred_instance_type="preferredInstanceType",
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
        props: typing.Union[CfnOutpostResolverMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Route53Resolver::OutpostResolver``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed3c5325a79ec0de9cbb13c9302ca80054919817a68813690ae7a0590126985d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfb6d36d592bdf6df765582a9365e4dd8f892435a644eb46d75dd30dd5d65737)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b282b10f2490d68c647999e9003ce464c2c249982acf2dd7da738ec0e1bacc5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnOutpostResolverMixinProps:
        return typing.cast(CfnOutpostResolverMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnResolverConfigMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "autodefined_reverse_flag": "autodefinedReverseFlag",
        "resource_id": "resourceId",
    },
)
class CfnResolverConfigMixinProps:
    def __init__(
        self,
        *,
        autodefined_reverse_flag: typing.Optional[builtins.str] = None,
        resource_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnResolverConfigPropsMixin.

        :param autodefined_reverse_flag: Represents the desired status of ``AutodefinedReverse`` . The only supported value on creation is ``DISABLE`` . Deletion of this resource will return ``AutodefinedReverse`` to its default value of ``ENABLED`` .
        :param resource_id: The ID of the Amazon Virtual Private Cloud VPC or a Route 53 Profile that you're configuring Resolver for.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverconfig.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
            
            cfn_resolver_config_mixin_props = route53resolver_mixins.CfnResolverConfigMixinProps(
                autodefined_reverse_flag="autodefinedReverseFlag",
                resource_id="resourceId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d2dfef7e69fa7cdb6e57692229e7c40992de6b3628cd3e8bf706906f18082b6)
            check_type(argname="argument autodefined_reverse_flag", value=autodefined_reverse_flag, expected_type=type_hints["autodefined_reverse_flag"])
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if autodefined_reverse_flag is not None:
            self._values["autodefined_reverse_flag"] = autodefined_reverse_flag
        if resource_id is not None:
            self._values["resource_id"] = resource_id

    @builtins.property
    def autodefined_reverse_flag(self) -> typing.Optional[builtins.str]:
        '''Represents the desired status of ``AutodefinedReverse`` .

        The only supported value on creation is ``DISABLE`` . Deletion of this resource will return ``AutodefinedReverse`` to its default value of ``ENABLED`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverconfig.html#cfn-route53resolver-resolverconfig-autodefinedreverseflag
        '''
        result = self._values.get("autodefined_reverse_flag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Amazon Virtual Private Cloud VPC or a Route 53 Profile that you're configuring Resolver for.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverconfig.html#cfn-route53resolver-resolverconfig-resourceid
        '''
        result = self._values.get("resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResolverConfigMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResolverConfigPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnResolverConfigPropsMixin",
):
    '''A complex type that contains information about a Resolver configuration for a VPC.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverconfig.html
    :cloudformationResource: AWS::Route53Resolver::ResolverConfig
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
        
        cfn_resolver_config_props_mixin = route53resolver_mixins.CfnResolverConfigPropsMixin(route53resolver_mixins.CfnResolverConfigMixinProps(
            autodefined_reverse_flag="autodefinedReverseFlag",
            resource_id="resourceId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResolverConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Route53Resolver::ResolverConfig``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb96d667a52358a183e68c2b55ba84fc57da494b746fc08cf194d4b95da9f8af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__add1b112c13f7955e583cc5f8988134b937f59e94562a59fad8db79d6e50dd11)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eef71a30f54ef9c0078a87c4e0328933394f3ee9e9c981f9a81cfd6b73b3fd57)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResolverConfigMixinProps:
        return typing.cast(CfnResolverConfigMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnResolverDNSSECConfigMixinProps",
    jsii_struct_bases=[],
    name_mapping={"resource_id": "resourceId"},
)
class CfnResolverDNSSECConfigMixinProps:
    def __init__(self, *, resource_id: typing.Optional[builtins.str] = None) -> None:
        '''Properties for CfnResolverDNSSECConfigPropsMixin.

        :param resource_id: The ID of the virtual private cloud (VPC) that you're configuring the DNSSEC validation status for.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverdnssecconfig.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
            
            cfn_resolver_dNSSECConfig_mixin_props = route53resolver_mixins.CfnResolverDNSSECConfigMixinProps(
                resource_id="resourceId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92cf0a768c079ba6244c802a617596f1b76b52f2ea85dc58c176c08ea00ad162)
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_id is not None:
            self._values["resource_id"] = resource_id

    @builtins.property
    def resource_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the virtual private cloud (VPC) that you're configuring the DNSSEC validation status for.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverdnssecconfig.html#cfn-route53resolver-resolverdnssecconfig-resourceid
        '''
        result = self._values.get("resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResolverDNSSECConfigMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResolverDNSSECConfigPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnResolverDNSSECConfigPropsMixin",
):
    '''The ``AWS::Route53Resolver::ResolverDNSSECConfig`` resource is a complex type that contains information about a configuration for DNSSEC validation.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverdnssecconfig.html
    :cloudformationResource: AWS::Route53Resolver::ResolverDNSSECConfig
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
        
        cfn_resolver_dNSSECConfig_props_mixin = route53resolver_mixins.CfnResolverDNSSECConfigPropsMixin(route53resolver_mixins.CfnResolverDNSSECConfigMixinProps(
            resource_id="resourceId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResolverDNSSECConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Route53Resolver::ResolverDNSSECConfig``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a83a39122f0cd0e58f5a8380a679ff69b9343cb778fafcb765d8e977634a9bc9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf73f27fdb84b9a8dc9b1fbc0629aae470700b2bee4845d70ba5af61fc6a8d47)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3481a7b75498c00f30348b56841c9385eb88beadcf14277ec0525f60bad5212)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResolverDNSSECConfigMixinProps:
        return typing.cast(CfnResolverDNSSECConfigMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnResolverEndpointMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "direction": "direction",
        "ip_addresses": "ipAddresses",
        "name": "name",
        "outpost_arn": "outpostArn",
        "preferred_instance_type": "preferredInstanceType",
        "protocols": "protocols",
        "resolver_endpoint_type": "resolverEndpointType",
        "security_group_ids": "securityGroupIds",
        "tags": "tags",
    },
)
class CfnResolverEndpointMixinProps:
    def __init__(
        self,
        *,
        direction: typing.Optional[builtins.str] = None,
        ip_addresses: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResolverEndpointPropsMixin.IpAddressRequestProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        outpost_arn: typing.Optional[builtins.str] = None,
        preferred_instance_type: typing.Optional[builtins.str] = None,
        protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        resolver_endpoint_type: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnResolverEndpointPropsMixin.

        :param direction: Indicates whether the Resolver endpoint allows inbound or outbound DNS queries:. - ``INBOUND`` : allows DNS queries to your VPC from your network - ``OUTBOUND`` : allows DNS queries from your VPC to your network - ``INBOUND_DELEGATION`` : Resolver delegates queries to Route 53 private hosted zones from your network.
        :param ip_addresses: The subnets and IP addresses in your VPC that DNS queries originate from (for outbound endpoints) or that you forward DNS queries to (for inbound endpoints). The subnet ID uniquely identifies a VPC. .. epigraph:: Even though the minimum is 1, Route 53 requires that you create at least two.
        :param name: A friendly name that lets you easily find a configuration in the Resolver dashboard in the Route 53 console.
        :param outpost_arn: The ARN (Amazon Resource Name) for the Outpost.
        :param preferred_instance_type: The Amazon EC2 instance type.
        :param protocols: Protocols used for the endpoint. DoH-FIPS is applicable for a default inbound endpoints only. For an inbound endpoint you can apply the protocols as follows: - Do53 and DoH in combination. - Do53 and DoH-FIPS in combination. - Do53 alone. - DoH alone. - DoH-FIPS alone. - None, which is treated as Do53. For a delegation inbound endpoint you can use Do53 only. For an outbound endpoint you can apply the protocols as follows: - Do53 and DoH in combination. - Do53 alone. - DoH alone. - None, which is treated as Do53.
        :param resolver_endpoint_type: The Resolver endpoint IP address type.
        :param security_group_ids: The ID of one or more security groups that control access to this VPC. The security group must include one or more inbound rules (for inbound endpoints) or outbound rules (for outbound endpoints). Inbound and outbound rules must allow TCP and UDP access. For inbound access, open port 53. For outbound access, open the port that you're using for DNS queries on your network.
        :param tags: Route 53 Resolver doesn't support updating tags through CloudFormation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
            
            cfn_resolver_endpoint_mixin_props = route53resolver_mixins.CfnResolverEndpointMixinProps(
                direction="direction",
                ip_addresses=[route53resolver_mixins.CfnResolverEndpointPropsMixin.IpAddressRequestProperty(
                    ip="ip",
                    ipv6="ipv6",
                    subnet_id="subnetId"
                )],
                name="name",
                outpost_arn="outpostArn",
                preferred_instance_type="preferredInstanceType",
                protocols=["protocols"],
                resolver_endpoint_type="resolverEndpointType",
                security_group_ids=["securityGroupIds"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da3f8cc25fff4e774eaaab5f086afe75a3729f31993e80ce0e5df7e285602bda)
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
            check_type(argname="argument ip_addresses", value=ip_addresses, expected_type=type_hints["ip_addresses"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument outpost_arn", value=outpost_arn, expected_type=type_hints["outpost_arn"])
            check_type(argname="argument preferred_instance_type", value=preferred_instance_type, expected_type=type_hints["preferred_instance_type"])
            check_type(argname="argument protocols", value=protocols, expected_type=type_hints["protocols"])
            check_type(argname="argument resolver_endpoint_type", value=resolver_endpoint_type, expected_type=type_hints["resolver_endpoint_type"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if direction is not None:
            self._values["direction"] = direction
        if ip_addresses is not None:
            self._values["ip_addresses"] = ip_addresses
        if name is not None:
            self._values["name"] = name
        if outpost_arn is not None:
            self._values["outpost_arn"] = outpost_arn
        if preferred_instance_type is not None:
            self._values["preferred_instance_type"] = preferred_instance_type
        if protocols is not None:
            self._values["protocols"] = protocols
        if resolver_endpoint_type is not None:
            self._values["resolver_endpoint_type"] = resolver_endpoint_type
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def direction(self) -> typing.Optional[builtins.str]:
        '''Indicates whether the Resolver endpoint allows inbound or outbound DNS queries:.

        - ``INBOUND`` : allows DNS queries to your VPC from your network
        - ``OUTBOUND`` : allows DNS queries from your VPC to your network
        - ``INBOUND_DELEGATION`` : Resolver delegates queries to Route 53 private hosted zones from your network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-direction
        '''
        result = self._values.get("direction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_addresses(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResolverEndpointPropsMixin.IpAddressRequestProperty"]]]]:
        '''The subnets and IP addresses in your VPC that DNS queries originate from (for outbound endpoints) or that you forward DNS queries to (for inbound endpoints).

        The subnet ID uniquely identifies a VPC.
        .. epigraph::

           Even though the minimum is 1, Route 53 requires that you create at least two.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-ipaddresses
        '''
        result = self._values.get("ip_addresses")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResolverEndpointPropsMixin.IpAddressRequestProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A friendly name that lets you easily find a configuration in the Resolver dashboard in the Route 53 console.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outpost_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN (Amazon Resource Name) for the Outpost.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-outpostarn
        '''
        result = self._values.get("outpost_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_instance_type(self) -> typing.Optional[builtins.str]:
        '''The Amazon EC2 instance type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-preferredinstancetype
        '''
        result = self._values.get("preferred_instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocols(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Protocols used for the endpoint. DoH-FIPS is applicable for a default inbound endpoints only.

        For an inbound endpoint you can apply the protocols as follows:

        - Do53 and DoH in combination.
        - Do53 and DoH-FIPS in combination.
        - Do53 alone.
        - DoH alone.
        - DoH-FIPS alone.
        - None, which is treated as Do53.

        For a delegation inbound endpoint you can use Do53 only.

        For an outbound endpoint you can apply the protocols as follows:

        - Do53 and DoH in combination.
        - Do53 alone.
        - DoH alone.
        - None, which is treated as Do53.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-protocols
        '''
        result = self._values.get("protocols")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resolver_endpoint_type(self) -> typing.Optional[builtins.str]:
        '''The Resolver endpoint IP address type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-resolverendpointtype
        '''
        result = self._values.get("resolver_endpoint_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ID of one or more security groups that control access to this VPC.

        The security group must include one or more inbound rules (for inbound endpoints) or outbound rules (for outbound endpoints). Inbound and outbound rules must allow TCP and UDP access. For inbound access, open port 53. For outbound access, open the port that you're using for DNS queries on your network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Route 53 Resolver doesn't support updating tags through CloudFormation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResolverEndpointMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResolverEndpointPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnResolverEndpointPropsMixin",
):
    '''Creates a Resolver endpoint. There are two types of Resolver endpoints, inbound and outbound:.

    - An *inbound Resolver endpoint* forwards DNS queries to the DNS service for a VPC from your network.
    - An *outbound Resolver endpoint* forwards DNS queries from the DNS service for a VPC to your network.

    .. epigraph::

       - You cannot update ``ResolverEndpointType`` and ``IpAddresses`` in the same request.
       - When you update a dual-stack IP address, you must update both IP addresses. You can’t update only an IPv4 or IPv6 and keep an existing IP address.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html
    :cloudformationResource: AWS::Route53Resolver::ResolverEndpoint
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
        
        cfn_resolver_endpoint_props_mixin = route53resolver_mixins.CfnResolverEndpointPropsMixin(route53resolver_mixins.CfnResolverEndpointMixinProps(
            direction="direction",
            ip_addresses=[route53resolver_mixins.CfnResolverEndpointPropsMixin.IpAddressRequestProperty(
                ip="ip",
                ipv6="ipv6",
                subnet_id="subnetId"
            )],
            name="name",
            outpost_arn="outpostArn",
            preferred_instance_type="preferredInstanceType",
            protocols=["protocols"],
            resolver_endpoint_type="resolverEndpointType",
            security_group_ids=["securityGroupIds"],
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
        props: typing.Union[CfnResolverEndpointMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Route53Resolver::ResolverEndpoint``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd81f65d630427fdc4cdf4be350f91c736c99f4e685f51479e03672db40c8894)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c53d1d4be8453b83ef50b48ac2ffcc77ee6ca1809f4f0fe986560475dda533ca)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d07f43b3b696f5a9b93fe12332f698442e2896b59b008648366dd4e76baff6f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResolverEndpointMixinProps:
        return typing.cast(CfnResolverEndpointMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnResolverEndpointPropsMixin.IpAddressRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"ip": "ip", "ipv6": "ipv6", "subnet_id": "subnetId"},
    )
    class IpAddressRequestProperty:
        def __init__(
            self,
            *,
            ip: typing.Optional[builtins.str] = None,
            ipv6: typing.Optional[builtins.str] = None,
            subnet_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''In a `CreateResolverEndpoint <https://docs.aws.amazon.com/Route53/latest/APIReference/API_route53resolver_CreateResolverEndpoint.html>`_ request, the IP address that DNS queries originate from (for outbound endpoints) or that you forward DNS queries to (for inbound endpoints). ``IpAddressRequest`` also includes the ID of the subnet that contains the IP address.

            :param ip: The IPv4 address that you want to use for DNS queries.
            :param ipv6: The IPv6 address that you want to use for DNS queries.
            :param subnet_id: The ID of the subnet that contains the IP address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-resolverendpoint-ipaddressrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
                
                ip_address_request_property = route53resolver_mixins.CfnResolverEndpointPropsMixin.IpAddressRequestProperty(
                    ip="ip",
                    ipv6="ipv6",
                    subnet_id="subnetId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8922825c01fc124178a66bf6b5d290627141df3c2f7c66f18ed1a0c3e055b9c3)
                check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
                check_type(argname="argument ipv6", value=ipv6, expected_type=type_hints["ipv6"])
                check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ip is not None:
                self._values["ip"] = ip
            if ipv6 is not None:
                self._values["ipv6"] = ipv6
            if subnet_id is not None:
                self._values["subnet_id"] = subnet_id

        @builtins.property
        def ip(self) -> typing.Optional[builtins.str]:
            '''The IPv4 address that you want to use for DNS queries.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-resolverendpoint-ipaddressrequest.html#cfn-route53resolver-resolverendpoint-ipaddressrequest-ip
            '''
            result = self._values.get("ip")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ipv6(self) -> typing.Optional[builtins.str]:
            '''The IPv6 address that you want to use for DNS queries.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-resolverendpoint-ipaddressrequest.html#cfn-route53resolver-resolverendpoint-ipaddressrequest-ipv6
            '''
            result = self._values.get("ipv6")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subnet_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the subnet that contains the IP address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-resolverendpoint-ipaddressrequest.html#cfn-route53resolver-resolverendpoint-ipaddressrequest-subnetid
            '''
            result = self._values.get("subnet_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IpAddressRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnResolverQueryLoggingConfigAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "resolver_query_log_config_id": "resolverQueryLogConfigId",
        "resource_id": "resourceId",
    },
)
class CfnResolverQueryLoggingConfigAssociationMixinProps:
    def __init__(
        self,
        *,
        resolver_query_log_config_id: typing.Optional[builtins.str] = None,
        resource_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnResolverQueryLoggingConfigAssociationPropsMixin.

        :param resolver_query_log_config_id: The ID of the query logging configuration that a VPC is associated with.
        :param resource_id: The ID of the Amazon VPC that is associated with the query logging configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfigassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
            
            cfn_resolver_query_logging_config_association_mixin_props = route53resolver_mixins.CfnResolverQueryLoggingConfigAssociationMixinProps(
                resolver_query_log_config_id="resolverQueryLogConfigId",
                resource_id="resourceId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__177dfe0c9f9fdd28c9b85d5ccbd732411f4f9e1637b3192e5cd2c1d8a8fad67e)
            check_type(argname="argument resolver_query_log_config_id", value=resolver_query_log_config_id, expected_type=type_hints["resolver_query_log_config_id"])
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resolver_query_log_config_id is not None:
            self._values["resolver_query_log_config_id"] = resolver_query_log_config_id
        if resource_id is not None:
            self._values["resource_id"] = resource_id

    @builtins.property
    def resolver_query_log_config_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the query logging configuration that a VPC is associated with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfigassociation.html#cfn-route53resolver-resolverqueryloggingconfigassociation-resolverquerylogconfigid
        '''
        result = self._values.get("resolver_query_log_config_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Amazon VPC that is associated with the query logging configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfigassociation.html#cfn-route53resolver-resolverqueryloggingconfigassociation-resourceid
        '''
        result = self._values.get("resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResolverQueryLoggingConfigAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResolverQueryLoggingConfigAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnResolverQueryLoggingConfigAssociationPropsMixin",
):
    '''The AWS::Route53Resolver::ResolverQueryLoggingConfigAssociation resource is a configuration for DNS query logging.

    After you create a query logging configuration, Amazon Route 53 begins to publish log data to an Amazon CloudWatch Logs log group.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfigassociation.html
    :cloudformationResource: AWS::Route53Resolver::ResolverQueryLoggingConfigAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
        
        cfn_resolver_query_logging_config_association_props_mixin = route53resolver_mixins.CfnResolverQueryLoggingConfigAssociationPropsMixin(route53resolver_mixins.CfnResolverQueryLoggingConfigAssociationMixinProps(
            resolver_query_log_config_id="resolverQueryLogConfigId",
            resource_id="resourceId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResolverQueryLoggingConfigAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Route53Resolver::ResolverQueryLoggingConfigAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4230919aba2dab24a8aa509750954582935429a121ab1ae522a2f5836a9629ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6dbca133ae32fc148ffb195fba5d524af884fb21f4c2f9e104378879b5582bf)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a90108deef81514898048176347effa314b75ff33ea9b40361722e2402869af4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResolverQueryLoggingConfigAssociationMixinProps:
        return typing.cast(CfnResolverQueryLoggingConfigAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnResolverQueryLoggingConfigMixinProps",
    jsii_struct_bases=[],
    name_mapping={"destination_arn": "destinationArn", "name": "name", "tags": "tags"},
)
class CfnResolverQueryLoggingConfigMixinProps:
    def __init__(
        self,
        *,
        destination_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnResolverQueryLoggingConfigPropsMixin.

        :param destination_arn: The ARN of the resource that you want Resolver to send query logs: an Amazon S3 bucket, a CloudWatch Logs log group, or a Kinesis Data Firehose delivery stream.
        :param name: The name of the query logging configuration.
        :param tags: An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfig.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
            
            cfn_resolver_query_logging_config_mixin_props = route53resolver_mixins.CfnResolverQueryLoggingConfigMixinProps(
                destination_arn="destinationArn",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5c27766480cf13b5f836745273e9db6a0f50dc2d8f94d4602aad508e71edb48)
            check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination_arn is not None:
            self._values["destination_arn"] = destination_arn
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def destination_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the resource that you want Resolver to send query logs: an Amazon S3 bucket, a CloudWatch Logs log group, or a Kinesis Data Firehose delivery stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfig.html#cfn-route53resolver-resolverqueryloggingconfig-destinationarn
        '''
        result = self._values.get("destination_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the query logging configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfig.html#cfn-route53resolver-resolverqueryloggingconfig-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfig.html#cfn-route53resolver-resolverqueryloggingconfig-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResolverQueryLoggingConfigMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResolverQueryLoggingConfigPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnResolverQueryLoggingConfigPropsMixin",
):
    '''The AWS::Route53Resolver::ResolverQueryLoggingConfig resource is a complex type that contains settings for one query logging configuration.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfig.html
    :cloudformationResource: AWS::Route53Resolver::ResolverQueryLoggingConfig
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
        
        cfn_resolver_query_logging_config_props_mixin = route53resolver_mixins.CfnResolverQueryLoggingConfigPropsMixin(route53resolver_mixins.CfnResolverQueryLoggingConfigMixinProps(
            destination_arn="destinationArn",
            name="name",
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
        props: typing.Union[CfnResolverQueryLoggingConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Route53Resolver::ResolverQueryLoggingConfig``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6593fe5dfff26853c3ababab25c3a244f8afda86a8f62c14c8315f3307d2dc56)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ea9f5df3849c8714c6a78dce60e3d190bf5577cdb2cfd9c03058f96553413ad)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7b1cbe90a959a4f68716664d298f5c552c9987c30eeb63105fb920e512bb91b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResolverQueryLoggingConfigMixinProps:
        return typing.cast(CfnResolverQueryLoggingConfigMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnResolverRuleAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "resolver_rule_id": "resolverRuleId",
        "vpc_id": "vpcId",
    },
)
class CfnResolverRuleAssociationMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        resolver_rule_id: typing.Optional[builtins.str] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnResolverRuleAssociationPropsMixin.

        :param name: The name of an association between a Resolver rule and a VPC. The name can be up to 64 characters long and can contain letters (a-z, A-Z), numbers (0-9), hyphens (-), underscores (_), and spaces. The name cannot consist of only numbers.
        :param resolver_rule_id: The ID of the Resolver rule that you associated with the VPC that is specified by ``VPCId`` .
        :param vpc_id: The ID of the VPC that you associated the Resolver rule with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverruleassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
            
            cfn_resolver_rule_association_mixin_props = route53resolver_mixins.CfnResolverRuleAssociationMixinProps(
                name="name",
                resolver_rule_id="resolverRuleId",
                vpc_id="vpcId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c02e1281abdbf66c34e327b194bc78aeaf750886f79be7878d9eab72751c5f1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resolver_rule_id", value=resolver_rule_id, expected_type=type_hints["resolver_rule_id"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if resolver_rule_id is not None:
            self._values["resolver_rule_id"] = resolver_rule_id
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of an association between a Resolver rule and a VPC.

        The name can be up to 64 characters long and can contain letters (a-z, A-Z), numbers (0-9), hyphens (-), underscores (_), and spaces. The name cannot consist of only numbers.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverruleassociation.html#cfn-route53resolver-resolverruleassociation-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resolver_rule_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Resolver rule that you associated with the VPC that is specified by ``VPCId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverruleassociation.html#cfn-route53resolver-resolverruleassociation-resolverruleid
        '''
        result = self._values.get("resolver_rule_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the VPC that you associated the Resolver rule with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverruleassociation.html#cfn-route53resolver-resolverruleassociation-vpcid
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResolverRuleAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResolverRuleAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnResolverRuleAssociationPropsMixin",
):
    '''In the response to an `AssociateResolverRule <https://docs.aws.amazon.com/Route53/latest/APIReference/API_route53resolver_AssociateResolverRule.html>`_ , `DisassociateResolverRule <https://docs.aws.amazon.com/Route53/latest/APIReference/API_route53resolver_DisassociateResolverRule.html>`_ , or `ListResolverRuleAssociations <https://docs.aws.amazon.com/Route53/latest/APIReference/API_route53resolver_ListResolverRuleAssociations.html>`_ request, provides information about an association between a resolver rule and a VPC. The association determines which DNS queries that originate in the VPC are forwarded to your network.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverruleassociation.html
    :cloudformationResource: AWS::Route53Resolver::ResolverRuleAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
        
        cfn_resolver_rule_association_props_mixin = route53resolver_mixins.CfnResolverRuleAssociationPropsMixin(route53resolver_mixins.CfnResolverRuleAssociationMixinProps(
            name="name",
            resolver_rule_id="resolverRuleId",
            vpc_id="vpcId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResolverRuleAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Route53Resolver::ResolverRuleAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2165d02a5580b39c78acf5eb69037de21830595a06a6b36f24695279128c8eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__99326f0e6215c779a75af76d68c5845992a727994375268c4a25cc434c26c1c1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a5117739ee78e47187a79e0b6cb6d97b9e12e76c4e64902d0b41cdee6ff6601)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResolverRuleAssociationMixinProps:
        return typing.cast(CfnResolverRuleAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnResolverRuleMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "delegation_record": "delegationRecord",
        "domain_name": "domainName",
        "name": "name",
        "resolver_endpoint_id": "resolverEndpointId",
        "rule_type": "ruleType",
        "tags": "tags",
        "target_ips": "targetIps",
    },
)
class CfnResolverRuleMixinProps:
    def __init__(
        self,
        *,
        delegation_record: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        resolver_endpoint_id: typing.Optional[builtins.str] = None,
        rule_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_ips: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResolverRulePropsMixin.TargetAddressProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnResolverRulePropsMixin.

        :param delegation_record: DNS queries with delegation records that point to this domain name are forwarded to resolvers on your network.
        :param domain_name: DNS queries for this domain name are forwarded to the IP addresses that are specified in ``TargetIps`` . If a query matches multiple Resolver rules (example.com and www.example.com), the query is routed using the Resolver rule that contains the most specific domain name (www.example.com).
        :param name: The name for the Resolver rule, which you specified when you created the Resolver rule. The name can be up to 64 characters long and can contain letters (a-z, A-Z), numbers (0-9), hyphens (-), underscores (_), and spaces. The name cannot consist of only numbers.
        :param resolver_endpoint_id: The ID of the endpoint that the rule is associated with.
        :param rule_type: When you want to forward DNS queries for specified domain name to resolvers on your network, specify ``FORWARD`` or ``DELEGATE`` . If a query matches multiple Resolver rules (example.com and www.example.com), outbound DNS queries are routed using the Resolver rule that contains the most specific domain name (www.example.com). When you have a forwarding rule to forward DNS queries for a domain to your network and you want Resolver to process queries for a subdomain of that domain, specify ``SYSTEM`` . For example, to forward DNS queries for example.com to resolvers on your network, you create a rule and specify ``FORWARD`` for ``RuleType`` . To then have Resolver process queries for apex.example.com, you create a rule and specify ``SYSTEM`` for ``RuleType`` . Currently, only Resolver can create rules that have a value of ``RECURSIVE`` for ``RuleType`` .
        :param tags: Tags help organize and categorize your Resolver rules. Each tag consists of a key and an optional value, both of which you define.
        :param target_ips: An array that contains the IP addresses and ports that an outbound endpoint forwards DNS queries to. Typically, these are the IP addresses of DNS resolvers on your network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
            
            cfn_resolver_rule_mixin_props = route53resolver_mixins.CfnResolverRuleMixinProps(
                delegation_record="delegationRecord",
                domain_name="domainName",
                name="name",
                resolver_endpoint_id="resolverEndpointId",
                rule_type="ruleType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_ips=[route53resolver_mixins.CfnResolverRulePropsMixin.TargetAddressProperty(
                    ip="ip",
                    ipv6="ipv6",
                    port="port",
                    protocol="protocol",
                    server_name_indication="serverNameIndication"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d15c4d3371241b75e42209bfa5f48e90a6b54aef4c547275c441ede2423482d)
            check_type(argname="argument delegation_record", value=delegation_record, expected_type=type_hints["delegation_record"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resolver_endpoint_id", value=resolver_endpoint_id, expected_type=type_hints["resolver_endpoint_id"])
            check_type(argname="argument rule_type", value=rule_type, expected_type=type_hints["rule_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_ips", value=target_ips, expected_type=type_hints["target_ips"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delegation_record is not None:
            self._values["delegation_record"] = delegation_record
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if name is not None:
            self._values["name"] = name
        if resolver_endpoint_id is not None:
            self._values["resolver_endpoint_id"] = resolver_endpoint_id
        if rule_type is not None:
            self._values["rule_type"] = rule_type
        if tags is not None:
            self._values["tags"] = tags
        if target_ips is not None:
            self._values["target_ips"] = target_ips

    @builtins.property
    def delegation_record(self) -> typing.Optional[builtins.str]:
        '''DNS queries with delegation records that point to this domain name are forwarded to resolvers on your network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-delegationrecord
        '''
        result = self._values.get("delegation_record")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''DNS queries for this domain name are forwarded to the IP addresses that are specified in ``TargetIps`` .

        If a query matches multiple Resolver rules (example.com and www.example.com), the query is routed using the Resolver rule that contains the most specific domain name (www.example.com).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name for the Resolver rule, which you specified when you created the Resolver rule.

        The name can be up to 64 characters long and can contain letters (a-z, A-Z), numbers (0-9), hyphens (-), underscores (_), and spaces. The name cannot consist of only numbers.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resolver_endpoint_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the endpoint that the rule is associated with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-resolverendpointid
        '''
        result = self._values.get("resolver_endpoint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_type(self) -> typing.Optional[builtins.str]:
        '''When you want to forward DNS queries for specified domain name to resolvers on your network, specify ``FORWARD`` or ``DELEGATE`` .

        If a query matches multiple Resolver rules (example.com and www.example.com), outbound DNS queries are routed using the Resolver rule that contains the most specific domain name (www.example.com).

        When you have a forwarding rule to forward DNS queries for a domain to your network and you want Resolver to process queries for a subdomain of that domain, specify ``SYSTEM`` .

        For example, to forward DNS queries for example.com to resolvers on your network, you create a rule and specify ``FORWARD`` for ``RuleType`` . To then have Resolver process queries for apex.example.com, you create a rule and specify ``SYSTEM`` for ``RuleType`` .

        Currently, only Resolver can create rules that have a value of ``RECURSIVE`` for ``RuleType`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-ruletype
        '''
        result = self._values.get("rule_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags help organize and categorize your Resolver rules.

        Each tag consists of a key and an optional value, both of which you define.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def target_ips(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResolverRulePropsMixin.TargetAddressProperty"]]]]:
        '''An array that contains the IP addresses and ports that an outbound endpoint forwards DNS queries to.

        Typically, these are the IP addresses of DNS resolvers on your network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-targetips
        '''
        result = self._values.get("target_ips")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResolverRulePropsMixin.TargetAddressProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResolverRuleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResolverRulePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnResolverRulePropsMixin",
):
    '''For DNS queries that originate in your VPCs, specifies which Resolver endpoint the queries pass through, one domain name that you want to forward to your network, and the IP addresses of the DNS resolvers in your network.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html
    :cloudformationResource: AWS::Route53Resolver::ResolverRule
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
        
        cfn_resolver_rule_props_mixin = route53resolver_mixins.CfnResolverRulePropsMixin(route53resolver_mixins.CfnResolverRuleMixinProps(
            delegation_record="delegationRecord",
            domain_name="domainName",
            name="name",
            resolver_endpoint_id="resolverEndpointId",
            rule_type="ruleType",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_ips=[route53resolver_mixins.CfnResolverRulePropsMixin.TargetAddressProperty(
                ip="ip",
                ipv6="ipv6",
                port="port",
                protocol="protocol",
                server_name_indication="serverNameIndication"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResolverRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Route53Resolver::ResolverRule``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2686a9c1252881062341679807e3cf511ce30163823ef6bf779236a2d96577e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__38835a3521aa9e18300294f5d15c05d597530b0a91248df624b66920dc154bff)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72097257e276a5900709cf381227e45b601ad962c48a8d09fc4987e396c6959f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResolverRuleMixinProps:
        return typing.cast(CfnResolverRuleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53resolver.mixins.CfnResolverRulePropsMixin.TargetAddressProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ip": "ip",
            "ipv6": "ipv6",
            "port": "port",
            "protocol": "protocol",
            "server_name_indication": "serverNameIndication",
        },
    )
    class TargetAddressProperty:
        def __init__(
            self,
            *,
            ip: typing.Optional[builtins.str] = None,
            ipv6: typing.Optional[builtins.str] = None,
            port: typing.Optional[builtins.str] = None,
            protocol: typing.Optional[builtins.str] = None,
            server_name_indication: typing.Optional[builtins.str] = None,
        ) -> None:
            '''In a `CreateResolverRule <https://docs.aws.amazon.com/Route53/latest/APIReference/API_route53resolver_CreateResolverRule.html>`_ request, an array of the IPs that you want to forward DNS queries to.

            :param ip: One IPv4 address that you want to forward DNS queries to.
            :param ipv6: One IPv6 address that you want to forward DNS queries to.
            :param port: The port at ``Ip`` that you want to forward DNS queries to.
            :param protocol: The protocols for the target address. The protocol you choose needs to be supported by the outbound endpoint of the Resolver rule.
            :param server_name_indication: The Server Name Indication of the DoH server that you want to forward queries to. This is only used if the Protocol of the ``TargetAddress`` is ``DoH`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-resolverrule-targetaddress.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53resolver import mixins as route53resolver_mixins
                
                target_address_property = route53resolver_mixins.CfnResolverRulePropsMixin.TargetAddressProperty(
                    ip="ip",
                    ipv6="ipv6",
                    port="port",
                    protocol="protocol",
                    server_name_indication="serverNameIndication"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a2720b10eaa5587684ca80e0f75a2e6418495fc3d43b289eca323bdb5dd1b120)
                check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
                check_type(argname="argument ipv6", value=ipv6, expected_type=type_hints["ipv6"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument server_name_indication", value=server_name_indication, expected_type=type_hints["server_name_indication"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ip is not None:
                self._values["ip"] = ip
            if ipv6 is not None:
                self._values["ipv6"] = ipv6
            if port is not None:
                self._values["port"] = port
            if protocol is not None:
                self._values["protocol"] = protocol
            if server_name_indication is not None:
                self._values["server_name_indication"] = server_name_indication

        @builtins.property
        def ip(self) -> typing.Optional[builtins.str]:
            '''One IPv4 address that you want to forward DNS queries to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-resolverrule-targetaddress.html#cfn-route53resolver-resolverrule-targetaddress-ip
            '''
            result = self._values.get("ip")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ipv6(self) -> typing.Optional[builtins.str]:
            '''One IPv6 address that you want to forward DNS queries to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-resolverrule-targetaddress.html#cfn-route53resolver-resolverrule-targetaddress-ipv6
            '''
            result = self._values.get("ipv6")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[builtins.str]:
            '''The port at ``Ip`` that you want to forward DNS queries to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-resolverrule-targetaddress.html#cfn-route53resolver-resolverrule-targetaddress-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The protocols for the target address.

            The protocol you choose needs to be supported by the outbound endpoint of the Resolver rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-resolverrule-targetaddress.html#cfn-route53resolver-resolverrule-targetaddress-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def server_name_indication(self) -> typing.Optional[builtins.str]:
            '''The Server Name Indication of the DoH server that you want to forward queries to.

            This is only used if the Protocol of the ``TargetAddress`` is ``DoH`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-resolverrule-targetaddress.html#cfn-route53resolver-resolverrule-targetaddress-servernameindication
            '''
            result = self._values.get("server_name_indication")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetAddressProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnFirewallDomainListMixinProps",
    "CfnFirewallDomainListPropsMixin",
    "CfnFirewallRuleGroupAssociationMixinProps",
    "CfnFirewallRuleGroupAssociationPropsMixin",
    "CfnFirewallRuleGroupMixinProps",
    "CfnFirewallRuleGroupPropsMixin",
    "CfnOutpostResolverMixinProps",
    "CfnOutpostResolverPropsMixin",
    "CfnResolverConfigMixinProps",
    "CfnResolverConfigPropsMixin",
    "CfnResolverDNSSECConfigMixinProps",
    "CfnResolverDNSSECConfigPropsMixin",
    "CfnResolverEndpointMixinProps",
    "CfnResolverEndpointPropsMixin",
    "CfnResolverQueryLoggingConfigAssociationMixinProps",
    "CfnResolverQueryLoggingConfigAssociationPropsMixin",
    "CfnResolverQueryLoggingConfigMixinProps",
    "CfnResolverQueryLoggingConfigPropsMixin",
    "CfnResolverRuleAssociationMixinProps",
    "CfnResolverRuleAssociationPropsMixin",
    "CfnResolverRuleMixinProps",
    "CfnResolverRulePropsMixin",
]

publication.publish()

def _typecheckingstub__b088adbd7873e422111b2f2099f497ef81fb60826a6c151a713dbf68665162dd(
    *,
    domain_file_url: typing.Optional[builtins.str] = None,
    domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f815fe419929c4bb953388d40e117f4610e8596b4d6d251957668781246212(
    props: typing.Union[CfnFirewallDomainListMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__914a7f139dfd119c35d6ad1bc64f2b2df3b2ebc076d5495a7dad2eededa5dbec(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f5b1ce26830c09dcf5eeb57f099c7f7f5a14396d988f16bb2abf0b70bfe405(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37161a9e8655c2938d4eedf96da023c200a8f35fa6875ecbfdee1af93946b537(
    *,
    firewall_rule_group_id: typing.Optional[builtins.str] = None,
    mutation_protection: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb70a7983757949c88fa7c5e6a5eeda2d328cfe7ced42cf570bda2017b9ddc36(
    props: typing.Union[CfnFirewallRuleGroupAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__414d73416c95a578d928845c838bd9858a639fd8e0cb01f49929ffeca17aa0ee(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__425cfff78ad7e57a3e3d805aaaaf21e7ccae3896b3a7b264edda994bf8bf3b57(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0a979ed1dddf3f3678a80bff4a1f26212bf21b05879b479295bbe3c9bf0d1f8(
    *,
    firewall_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFirewallRuleGroupPropsMixin.FirewallRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5243d8599026e3b9898491e9c5fa84394c40212a6dcd99545014ed8a1c947b7(
    props: typing.Union[CfnFirewallRuleGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__625bff58f0e03dc942ba62b2ab0c1f6ddc2f1008bc6fd8d9bf4746589f7dd635(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a40345491d4836232835616c0e244299e0f53bfb87913923bbcd30e3cb0d6e39(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630bbb3dcd018fe614e1e3da398951fc9bd3773f76f2a638819f6363e757d127(
    *,
    action: typing.Optional[builtins.str] = None,
    block_override_dns_type: typing.Optional[builtins.str] = None,
    block_override_domain: typing.Optional[builtins.str] = None,
    block_override_ttl: typing.Optional[jsii.Number] = None,
    block_response: typing.Optional[builtins.str] = None,
    confidence_threshold: typing.Optional[builtins.str] = None,
    dns_threat_protection: typing.Optional[builtins.str] = None,
    firewall_domain_list_id: typing.Optional[builtins.str] = None,
    firewall_domain_redirection_action: typing.Optional[builtins.str] = None,
    firewall_threat_protection_id: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    qtype: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce1194929d42c1698259f4362c2aeb0a7d50dcf10994402f5a451292c829a79(
    *,
    instance_count: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    outpost_arn: typing.Optional[builtins.str] = None,
    preferred_instance_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed3c5325a79ec0de9cbb13c9302ca80054919817a68813690ae7a0590126985d(
    props: typing.Union[CfnOutpostResolverMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfb6d36d592bdf6df765582a9365e4dd8f892435a644eb46d75dd30dd5d65737(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b282b10f2490d68c647999e9003ce464c2c249982acf2dd7da738ec0e1bacc5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d2dfef7e69fa7cdb6e57692229e7c40992de6b3628cd3e8bf706906f18082b6(
    *,
    autodefined_reverse_flag: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb96d667a52358a183e68c2b55ba84fc57da494b746fc08cf194d4b95da9f8af(
    props: typing.Union[CfnResolverConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__add1b112c13f7955e583cc5f8988134b937f59e94562a59fad8db79d6e50dd11(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eef71a30f54ef9c0078a87c4e0328933394f3ee9e9c981f9a81cfd6b73b3fd57(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92cf0a768c079ba6244c802a617596f1b76b52f2ea85dc58c176c08ea00ad162(
    *,
    resource_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a83a39122f0cd0e58f5a8380a679ff69b9343cb778fafcb765d8e977634a9bc9(
    props: typing.Union[CfnResolverDNSSECConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf73f27fdb84b9a8dc9b1fbc0629aae470700b2bee4845d70ba5af61fc6a8d47(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3481a7b75498c00f30348b56841c9385eb88beadcf14277ec0525f60bad5212(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da3f8cc25fff4e774eaaab5f086afe75a3729f31993e80ce0e5df7e285602bda(
    *,
    direction: typing.Optional[builtins.str] = None,
    ip_addresses: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResolverEndpointPropsMixin.IpAddressRequestProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    outpost_arn: typing.Optional[builtins.str] = None,
    preferred_instance_type: typing.Optional[builtins.str] = None,
    protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
    resolver_endpoint_type: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd81f65d630427fdc4cdf4be350f91c736c99f4e685f51479e03672db40c8894(
    props: typing.Union[CfnResolverEndpointMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c53d1d4be8453b83ef50b48ac2ffcc77ee6ca1809f4f0fe986560475dda533ca(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d07f43b3b696f5a9b93fe12332f698442e2896b59b008648366dd4e76baff6f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8922825c01fc124178a66bf6b5d290627141df3c2f7c66f18ed1a0c3e055b9c3(
    *,
    ip: typing.Optional[builtins.str] = None,
    ipv6: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177dfe0c9f9fdd28c9b85d5ccbd732411f4f9e1637b3192e5cd2c1d8a8fad67e(
    *,
    resolver_query_log_config_id: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4230919aba2dab24a8aa509750954582935429a121ab1ae522a2f5836a9629ed(
    props: typing.Union[CfnResolverQueryLoggingConfigAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6dbca133ae32fc148ffb195fba5d524af884fb21f4c2f9e104378879b5582bf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90108deef81514898048176347effa314b75ff33ea9b40361722e2402869af4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5c27766480cf13b5f836745273e9db6a0f50dc2d8f94d4602aad508e71edb48(
    *,
    destination_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6593fe5dfff26853c3ababab25c3a244f8afda86a8f62c14c8315f3307d2dc56(
    props: typing.Union[CfnResolverQueryLoggingConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ea9f5df3849c8714c6a78dce60e3d190bf5577cdb2cfd9c03058f96553413ad(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b1cbe90a959a4f68716664d298f5c552c9987c30eeb63105fb920e512bb91b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c02e1281abdbf66c34e327b194bc78aeaf750886f79be7878d9eab72751c5f1(
    *,
    name: typing.Optional[builtins.str] = None,
    resolver_rule_id: typing.Optional[builtins.str] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2165d02a5580b39c78acf5eb69037de21830595a06a6b36f24695279128c8eb(
    props: typing.Union[CfnResolverRuleAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99326f0e6215c779a75af76d68c5845992a727994375268c4a25cc434c26c1c1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a5117739ee78e47187a79e0b6cb6d97b9e12e76c4e64902d0b41cdee6ff6601(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d15c4d3371241b75e42209bfa5f48e90a6b54aef4c547275c441ede2423482d(
    *,
    delegation_record: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    resolver_endpoint_id: typing.Optional[builtins.str] = None,
    rule_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_ips: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResolverRulePropsMixin.TargetAddressProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2686a9c1252881062341679807e3cf511ce30163823ef6bf779236a2d96577e7(
    props: typing.Union[CfnResolverRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38835a3521aa9e18300294f5d15c05d597530b0a91248df624b66920dc154bff(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72097257e276a5900709cf381227e45b601ad962c48a8d09fc4987e396c6959f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2720b10eaa5587684ca80e0f75a2e6418495fc3d43b289eca323bdb5dd1b120(
    *,
    ip: typing.Optional[builtins.str] = None,
    ipv6: typing.Optional[builtins.str] = None,
    port: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    server_name_indication: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
