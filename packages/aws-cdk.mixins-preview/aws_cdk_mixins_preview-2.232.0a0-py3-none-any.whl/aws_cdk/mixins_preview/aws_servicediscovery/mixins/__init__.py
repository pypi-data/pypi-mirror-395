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
    jsii_type="@aws-cdk/mixins-preview.aws_servicediscovery.mixins.CfnHttpNamespaceMixinProps",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "name": "name", "tags": "tags"},
)
class CfnHttpNamespaceMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnHttpNamespacePropsMixin.

        :param description: A description for the namespace.
        :param name: The name that you want to assign to this namespace.
        :param tags: The tags for the namespace. Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-httpnamespace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicediscovery import mixins as servicediscovery_mixins
            
            cfn_http_namespace_mixin_props = servicediscovery_mixins.CfnHttpNamespaceMixinProps(
                description="description",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fc2cb20960b706f0d6d1ee3ee1afef094f530acf4e3717bf096adec9d576f46)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-httpnamespace.html#cfn-servicediscovery-httpnamespace-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name that you want to assign to this namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-httpnamespace.html#cfn-servicediscovery-httpnamespace-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags for the namespace.

        Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-httpnamespace.html#cfn-servicediscovery-httpnamespace-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnHttpNamespaceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnHttpNamespacePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_servicediscovery.mixins.CfnHttpNamespacePropsMixin",
):
    '''Creates an HTTP namespace.

    Service instances registered using an HTTP namespace can be discovered using a ``DiscoverInstances`` request but can't be discovered using DNS.

    For the current quota on the number of namespaces that you can create using the same AWS account , see `AWS Cloud Map quotas <https://docs.aws.amazon.com/cloud-map/latest/dg/cloud-map-limits.html>`_ in the *AWS Cloud Map Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-httpnamespace.html
    :cloudformationResource: AWS::ServiceDiscovery::HttpNamespace
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicediscovery import mixins as servicediscovery_mixins
        
        cfn_http_namespace_props_mixin = servicediscovery_mixins.CfnHttpNamespacePropsMixin(servicediscovery_mixins.CfnHttpNamespaceMixinProps(
            description="description",
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
        props: typing.Union[CfnHttpNamespaceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceDiscovery::HttpNamespace``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8910cc6b27ae792fd9546fe1be096f12d2ff6e2c3660f5f259f4573fce038b07)
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
            type_hints = typing.get_type_hints(_typecheckingstub__973503c159abac8fabafbed73bf6e768a57f375fcbd8cc65cdbc3cdd6a8775d8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4320488579fc0931d52ec7fa0621f48c23e19ba1ebfd4d6a5c480981fddf7945)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnHttpNamespaceMixinProps:
        return typing.cast(CfnHttpNamespaceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_servicediscovery.mixins.CfnInstanceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_attributes": "instanceAttributes",
        "instance_id": "instanceId",
        "service_id": "serviceId",
    },
)
class CfnInstanceMixinProps:
    def __init__(
        self,
        *,
        instance_attributes: typing.Any = None,
        instance_id: typing.Optional[builtins.str] = None,
        service_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnInstancePropsMixin.

        :param instance_attributes: A string map that contains the following information for the service that you specify in ``ServiceId`` :. - The attributes that apply to the records that are defined in the service. - For each attribute, the applicable value. Supported attribute keys include the following: - **AWS_ALIAS_DNS_NAME** - If you want AWS Cloud Map to create a Route 53 alias record that routes traffic to an Elastic Load Balancing load balancer, specify the DNS name that is associated with the load balancer. For information about how to get the DNS name, see `AliasTarget->DNSName <https://docs.aws.amazon.com/Route53/latest/APIReference/API_AliasTarget.html#Route53-Type-AliasTarget-DNSName>`_ in the *Route 53 API Reference* . Note the following: - The configuration for the service that is specified by ``ServiceId`` must include settings for an ``A`` record, an ``AAAA`` record, or both. - In the service that is specified by ``ServiceId`` , the value of ``RoutingPolicy`` must be ``WEIGHTED`` . - If the service that is specified by ``ServiceId`` includes ``HealthCheckConfig`` settings, AWS Cloud Map will create the health check, but it won't associate the health check with the alias record. - Auto naming currently doesn't support creating alias records that route traffic to AWS resources other than ELB load balancers. - If you specify a value for ``AWS_ALIAS_DNS_NAME`` , don't specify values for any of the ``AWS_INSTANCE`` attributes. - **AWS_EC2_INSTANCE_ID** - *HTTP namespaces only.* The Amazon EC2 instance ID for the instance. The ``AWS_INSTANCE_IPV4`` attribute contains the primary private IPv4 address. When creating resources with a type of `AWS::ServiceDiscovery::Instance <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html>`_ , if the ``AWS_EC2_INSTANCE_ID`` attribute is specified, the only other attribute that can be specified is ``AWS_INIT_HEALTH_STATUS`` . After the resource has been created, the ``AWS_INSTANCE_IPV4`` attribute contains the primary private IPv4 address. - **AWS_INIT_HEALTH_STATUS** - If the service configuration includes ``HealthCheckCustomConfig`` , when creating resources with a type of `AWS::ServiceDiscovery::Instance <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html>`_ you can optionally use ``AWS_INIT_HEALTH_STATUS`` to specify the initial status of the custom health check, ``HEALTHY`` or ``UNHEALTHY`` . If you don't specify a value for ``AWS_INIT_HEALTH_STATUS`` , the initial status is ``HEALTHY`` . This attribute can only be used when creating resources and will not be seen on existing resources. - **AWS_INSTANCE_CNAME** - If the service configuration includes a ``CNAME`` record, the domain name that you want Route 53 to return in response to DNS queries, for example, ``example.com`` . This value is required if the service specified by ``ServiceId`` includes settings for an ``CNAME`` record. - **AWS_INSTANCE_IPV4** - If the service configuration includes an ``A`` record, the IPv4 address that you want Route 53 to return in response to DNS queries, for example, ``192.0.2.44`` . This value is required if the service specified by ``ServiceId`` includes settings for an ``A`` record. If the service includes settings for an ``SRV`` record, you must specify a value for ``AWS_INSTANCE_IPV4`` , ``AWS_INSTANCE_IPV6`` , or both. - **AWS_INSTANCE_IPV6** - If the service configuration includes an ``AAAA`` record, the IPv6 address that you want Route 53 to return in response to DNS queries, for example, ``2001:0db8:85a3:0000:0000:abcd:0001:2345`` . This value is required if the service specified by ``ServiceId`` includes settings for an ``AAAA`` record. If the service includes settings for an ``SRV`` record, you must specify a value for ``AWS_INSTANCE_IPV4`` , ``AWS_INSTANCE_IPV6`` , or both. - **AWS_INSTANCE_PORT** - If the service includes an ``SRV`` record, the value that you want Route 53 to return for the port. If the service includes ``HealthCheckConfig`` , the port on the endpoint that you want Route 53 to send requests to. This value is required if you specified settings for an ``SRV`` record or a Route 53 health check when you created the service.
        :param instance_id: An identifier that you want to associate with the instance. Note the following:. - If the service that's specified by ``ServiceId`` includes settings for an ``SRV`` record, the value of ``InstanceId`` is automatically included as part of the value for the ``SRV`` record. For more information, see `DnsRecord > Type <https://docs.aws.amazon.com/cloud-map/latest/api/API_DnsRecord.html#cloudmap-Type-DnsRecord-Type>`_ . - You can use this value to update an existing instance. - To register a new instance, you must specify a value that's unique among instances that you register by using the same service. - If you specify an existing ``InstanceId`` and ``ServiceId`` , AWS Cloud Map updates the existing DNS records, if any. If there's also an existing health check, AWS Cloud Map deletes the old health check and creates a new one. .. epigraph:: The health check isn't deleted immediately, so it will still appear for a while if you submit a ``ListHealthChecks`` request, for example. .. epigraph:: Do not include sensitive information in ``InstanceId`` if the namespace is discoverable by public DNS queries and any ``Type`` member of ``DnsRecord`` for the service contains ``SRV`` because the ``InstanceId`` is discoverable by public DNS queries.
        :param service_id: The ID or Amazon Resource Name (ARN) of the service that you want to use for settings for the instance. For services created in a shared namespace, specify the service ARN. For more information about shared namespaces, see `Cross-account AWS Cloud Map namespace sharing <https://docs.aws.amazon.com/cloud-map/latest/dg/sharing-namespaces.html>`_ in the *AWS Cloud Map Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicediscovery import mixins as servicediscovery_mixins
            
            # instance_attributes: Any
            
            cfn_instance_mixin_props = servicediscovery_mixins.CfnInstanceMixinProps(
                instance_attributes=instance_attributes,
                instance_id="instanceId",
                service_id="serviceId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09fca416f756247df39b50a9f14ab40afeab65ff49bf1b107fe260d92415a151)
            check_type(argname="argument instance_attributes", value=instance_attributes, expected_type=type_hints["instance_attributes"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument service_id", value=service_id, expected_type=type_hints["service_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_attributes is not None:
            self._values["instance_attributes"] = instance_attributes
        if instance_id is not None:
            self._values["instance_id"] = instance_id
        if service_id is not None:
            self._values["service_id"] = service_id

    @builtins.property
    def instance_attributes(self) -> typing.Any:
        '''A string map that contains the following information for the service that you specify in ``ServiceId`` :.

        - The attributes that apply to the records that are defined in the service.
        - For each attribute, the applicable value.

        Supported attribute keys include the following:

        - **AWS_ALIAS_DNS_NAME** - If you want AWS Cloud Map to create a Route 53 alias record that routes traffic to an Elastic Load Balancing load balancer, specify the DNS name that is associated with the load balancer. For information about how to get the DNS name, see `AliasTarget->DNSName <https://docs.aws.amazon.com/Route53/latest/APIReference/API_AliasTarget.html#Route53-Type-AliasTarget-DNSName>`_ in the *Route 53 API Reference* .

        Note the following:

        - The configuration for the service that is specified by ``ServiceId`` must include settings for an ``A`` record, an ``AAAA`` record, or both.
        - In the service that is specified by ``ServiceId`` , the value of ``RoutingPolicy`` must be ``WEIGHTED`` .
        - If the service that is specified by ``ServiceId`` includes ``HealthCheckConfig`` settings, AWS Cloud Map will create the health check, but it won't associate the health check with the alias record.
        - Auto naming currently doesn't support creating alias records that route traffic to AWS resources other than ELB load balancers.
        - If you specify a value for ``AWS_ALIAS_DNS_NAME`` , don't specify values for any of the ``AWS_INSTANCE`` attributes.
        - **AWS_EC2_INSTANCE_ID** - *HTTP namespaces only.* The Amazon EC2 instance ID for the instance. The ``AWS_INSTANCE_IPV4`` attribute contains the primary private IPv4 address. When creating resources with a type of `AWS::ServiceDiscovery::Instance <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html>`_ , if the ``AWS_EC2_INSTANCE_ID`` attribute is specified, the only other attribute that can be specified is ``AWS_INIT_HEALTH_STATUS`` . After the resource has been created, the ``AWS_INSTANCE_IPV4`` attribute contains the primary private IPv4 address.
        - **AWS_INIT_HEALTH_STATUS** - If the service configuration includes ``HealthCheckCustomConfig`` , when creating resources with a type of `AWS::ServiceDiscovery::Instance <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html>`_ you can optionally use ``AWS_INIT_HEALTH_STATUS`` to specify the initial status of the custom health check, ``HEALTHY`` or ``UNHEALTHY`` . If you don't specify a value for ``AWS_INIT_HEALTH_STATUS`` , the initial status is ``HEALTHY`` . This attribute can only be used when creating resources and will not be seen on existing resources.
        - **AWS_INSTANCE_CNAME** - If the service configuration includes a ``CNAME`` record, the domain name that you want Route 53 to return in response to DNS queries, for example, ``example.com`` .

        This value is required if the service specified by ``ServiceId`` includes settings for an ``CNAME`` record.

        - **AWS_INSTANCE_IPV4** - If the service configuration includes an ``A`` record, the IPv4 address that you want Route 53 to return in response to DNS queries, for example, ``192.0.2.44`` .

        This value is required if the service specified by ``ServiceId`` includes settings for an ``A`` record. If the service includes settings for an ``SRV`` record, you must specify a value for ``AWS_INSTANCE_IPV4`` , ``AWS_INSTANCE_IPV6`` , or both.

        - **AWS_INSTANCE_IPV6** - If the service configuration includes an ``AAAA`` record, the IPv6 address that you want Route 53 to return in response to DNS queries, for example, ``2001:0db8:85a3:0000:0000:abcd:0001:2345`` .

        This value is required if the service specified by ``ServiceId`` includes settings for an ``AAAA`` record. If the service includes settings for an ``SRV`` record, you must specify a value for ``AWS_INSTANCE_IPV4`` , ``AWS_INSTANCE_IPV6`` , or both.

        - **AWS_INSTANCE_PORT** - If the service includes an ``SRV`` record, the value that you want Route 53 to return for the port.

        If the service includes ``HealthCheckConfig`` , the port on the endpoint that you want Route 53 to send requests to.

        This value is required if you specified settings for an ``SRV`` record or a Route 53 health check when you created the service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html#cfn-servicediscovery-instance-instanceattributes
        '''
        result = self._values.get("instance_attributes")
        return typing.cast(typing.Any, result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''An identifier that you want to associate with the instance. Note the following:.

        - If the service that's specified by ``ServiceId`` includes settings for an ``SRV`` record, the value of ``InstanceId`` is automatically included as part of the value for the ``SRV`` record. For more information, see `DnsRecord > Type <https://docs.aws.amazon.com/cloud-map/latest/api/API_DnsRecord.html#cloudmap-Type-DnsRecord-Type>`_ .
        - You can use this value to update an existing instance.
        - To register a new instance, you must specify a value that's unique among instances that you register by using the same service.
        - If you specify an existing ``InstanceId`` and ``ServiceId`` , AWS Cloud Map updates the existing DNS records, if any. If there's also an existing health check, AWS Cloud Map deletes the old health check and creates a new one.

        .. epigraph::

           The health check isn't deleted immediately, so it will still appear for a while if you submit a ``ListHealthChecks`` request, for example.
        .. epigraph::

           Do not include sensitive information in ``InstanceId`` if the namespace is discoverable by public DNS queries and any ``Type`` member of ``DnsRecord`` for the service contains ``SRV`` because the ``InstanceId`` is discoverable by public DNS queries.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html#cfn-servicediscovery-instance-instanceid
        '''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_id(self) -> typing.Optional[builtins.str]:
        '''The ID or Amazon Resource Name (ARN) of the service that you want to use for settings for the instance.

        For services created in a shared namespace, specify the service ARN. For more information about shared namespaces, see `Cross-account AWS Cloud Map namespace sharing <https://docs.aws.amazon.com/cloud-map/latest/dg/sharing-namespaces.html>`_ in the *AWS Cloud Map Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html#cfn-servicediscovery-instance-serviceid
        '''
        result = self._values.get("service_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInstanceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnInstancePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_servicediscovery.mixins.CfnInstancePropsMixin",
):
    '''A complex type that contains information about an instance that AWS Cloud Map creates when you submit a ``RegisterInstance`` request.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html
    :cloudformationResource: AWS::ServiceDiscovery::Instance
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicediscovery import mixins as servicediscovery_mixins
        
        # instance_attributes: Any
        
        cfn_instance_props_mixin = servicediscovery_mixins.CfnInstancePropsMixin(servicediscovery_mixins.CfnInstanceMixinProps(
            instance_attributes=instance_attributes,
            instance_id="instanceId",
            service_id="serviceId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnInstanceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceDiscovery::Instance``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9514f54d0f998dcb0b8394d502ebbe3a6fd3d32c88dfa7c326f13633fe571b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7367c4d65d7d87500d9cd4aebf07078ee4237f658bf974edf0a5c2b050d7184d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa788b8f1ae0cf2bfeb4ef95bac7491af5a00e3c6465f978ecdd60b37eea259)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnInstanceMixinProps:
        return typing.cast(CfnInstanceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_servicediscovery.mixins.CfnPrivateDnsNamespaceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "properties": "properties",
        "tags": "tags",
        "vpc": "vpc",
    },
)
class CfnPrivateDnsNamespaceMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPrivateDnsNamespacePropsMixin.PropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPrivateDnsNamespacePropsMixin.

        :param description: A description for the namespace.
        :param name: The name that you want to assign to this namespace. When you create a private DNS namespace, AWS Cloud Map automatically creates an Amazon Route 53 private hosted zone that has the same name as the namespace.
        :param properties: Properties for the private DNS namespace.
        :param tags: The tags for the namespace. Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.
        :param vpc: The ID of the Amazon VPC that you want to associate the namespace with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicediscovery import mixins as servicediscovery_mixins
            
            cfn_private_dns_namespace_mixin_props = servicediscovery_mixins.CfnPrivateDnsNamespaceMixinProps(
                description="description",
                name="name",
                properties=servicediscovery_mixins.CfnPrivateDnsNamespacePropsMixin.PropertiesProperty(
                    dns_properties=servicediscovery_mixins.CfnPrivateDnsNamespacePropsMixin.PrivateDnsPropertiesMutableProperty(
                        soa=servicediscovery_mixins.CfnPrivateDnsNamespacePropsMixin.SOAProperty(
                            ttl=123
                        )
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc="vpc"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__339a9530458dce0a711303fdfef99e5e8ac6e4ac04939101e73becd726ad90ea)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if properties is not None:
            self._values["properties"] = properties
        if tags is not None:
            self._values["tags"] = tags
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html#cfn-servicediscovery-privatednsnamespace-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name that you want to assign to this namespace.

        When you create a private DNS namespace, AWS Cloud Map automatically creates an Amazon Route 53 private hosted zone that has the same name as the namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html#cfn-servicediscovery-privatednsnamespace-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrivateDnsNamespacePropsMixin.PropertiesProperty"]]:
        '''Properties for the private DNS namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html#cfn-servicediscovery-privatednsnamespace-properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrivateDnsNamespacePropsMixin.PropertiesProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags for the namespace.

        Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html#cfn-servicediscovery-privatednsnamespace-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc(self) -> typing.Optional[builtins.str]:
        '''The ID of the Amazon VPC that you want to associate the namespace with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html#cfn-servicediscovery-privatednsnamespace-vpc
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPrivateDnsNamespaceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPrivateDnsNamespacePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_servicediscovery.mixins.CfnPrivateDnsNamespacePropsMixin",
):
    '''Creates a private namespace based on DNS, which is visible only inside a specified Amazon VPC.

    The namespace defines your service naming scheme. For example, if you name your namespace ``example.com`` and name your service ``backend`` , the resulting DNS name for the service is ``backend.example.com`` . Service instances that are registered using a private DNS namespace can be discovered using either a ``DiscoverInstances`` request or using DNS. For the current quota on the number of namespaces that you can create using the same AWS account , see `AWS Cloud Map quotas <https://docs.aws.amazon.com/cloud-map/latest/dg/cloud-map-limits.html>`_ in the *AWS Cloud Map Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html
    :cloudformationResource: AWS::ServiceDiscovery::PrivateDnsNamespace
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicediscovery import mixins as servicediscovery_mixins
        
        cfn_private_dns_namespace_props_mixin = servicediscovery_mixins.CfnPrivateDnsNamespacePropsMixin(servicediscovery_mixins.CfnPrivateDnsNamespaceMixinProps(
            description="description",
            name="name",
            properties=servicediscovery_mixins.CfnPrivateDnsNamespacePropsMixin.PropertiesProperty(
                dns_properties=servicediscovery_mixins.CfnPrivateDnsNamespacePropsMixin.PrivateDnsPropertiesMutableProperty(
                    soa=servicediscovery_mixins.CfnPrivateDnsNamespacePropsMixin.SOAProperty(
                        ttl=123
                    )
                )
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc="vpc"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPrivateDnsNamespaceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceDiscovery::PrivateDnsNamespace``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69e0f70049a344c12d55f06765cd1b9e7863c29f1bed074ff4b524de87b0f5b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2f035a2d55512053a8ec3ac82df99328265a767b4c8069e4f3ef1785eed5f12)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b9ec13f5aa0cba05e49305fd8e7b172845a8125a3a235130882b5982248fab3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPrivateDnsNamespaceMixinProps:
        return typing.cast(CfnPrivateDnsNamespaceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_servicediscovery.mixins.CfnPrivateDnsNamespacePropsMixin.PrivateDnsPropertiesMutableProperty",
        jsii_struct_bases=[],
        name_mapping={"soa": "soa"},
    )
    class PrivateDnsPropertiesMutableProperty:
        def __init__(
            self,
            *,
            soa: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPrivateDnsNamespacePropsMixin.SOAProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''DNS properties for the private DNS namespace.

            :param soa: Fields for the Start of Authority (SOA) record for the hosted zone for the private DNS namespace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-privatednsnamespace-privatednspropertiesmutable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_servicediscovery import mixins as servicediscovery_mixins
                
                private_dns_properties_mutable_property = servicediscovery_mixins.CfnPrivateDnsNamespacePropsMixin.PrivateDnsPropertiesMutableProperty(
                    soa=servicediscovery_mixins.CfnPrivateDnsNamespacePropsMixin.SOAProperty(
                        ttl=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__902cc0865505445b946d094ebc746941f05916af1b11e84ac05e1d91e13b152b)
                check_type(argname="argument soa", value=soa, expected_type=type_hints["soa"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if soa is not None:
                self._values["soa"] = soa

        @builtins.property
        def soa(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrivateDnsNamespacePropsMixin.SOAProperty"]]:
            '''Fields for the Start of Authority (SOA) record for the hosted zone for the private DNS namespace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-privatednsnamespace-privatednspropertiesmutable.html#cfn-servicediscovery-privatednsnamespace-privatednspropertiesmutable-soa
            '''
            result = self._values.get("soa")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrivateDnsNamespacePropsMixin.SOAProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrivateDnsPropertiesMutableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_servicediscovery.mixins.CfnPrivateDnsNamespacePropsMixin.PropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"dns_properties": "dnsProperties"},
    )
    class PropertiesProperty:
        def __init__(
            self,
            *,
            dns_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPrivateDnsNamespacePropsMixin.PrivateDnsPropertiesMutableProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Properties for the private DNS namespace.

            :param dns_properties: DNS properties for the private DNS namespace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-privatednsnamespace-properties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_servicediscovery import mixins as servicediscovery_mixins
                
                properties_property = servicediscovery_mixins.CfnPrivateDnsNamespacePropsMixin.PropertiesProperty(
                    dns_properties=servicediscovery_mixins.CfnPrivateDnsNamespacePropsMixin.PrivateDnsPropertiesMutableProperty(
                        soa=servicediscovery_mixins.CfnPrivateDnsNamespacePropsMixin.SOAProperty(
                            ttl=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d69f3a5bfa8690e7c9f12e6a0046e95127fe5e81a059eed0528d3e6b717b2e2d)
                check_type(argname="argument dns_properties", value=dns_properties, expected_type=type_hints["dns_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dns_properties is not None:
                self._values["dns_properties"] = dns_properties

        @builtins.property
        def dns_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrivateDnsNamespacePropsMixin.PrivateDnsPropertiesMutableProperty"]]:
            '''DNS properties for the private DNS namespace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-privatednsnamespace-properties.html#cfn-servicediscovery-privatednsnamespace-properties-dnsproperties
            '''
            result = self._values.get("dns_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrivateDnsNamespacePropsMixin.PrivateDnsPropertiesMutableProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_servicediscovery.mixins.CfnPrivateDnsNamespacePropsMixin.SOAProperty",
        jsii_struct_bases=[],
        name_mapping={"ttl": "ttl"},
    )
    class SOAProperty:
        def __init__(self, *, ttl: typing.Optional[jsii.Number] = None) -> None:
            '''Start of Authority (SOA) properties for a public or private DNS namespace.

            :param ttl: The time to live (TTL) for purposes of negative caching.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-privatednsnamespace-soa.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_servicediscovery import mixins as servicediscovery_mixins
                
                s_oAProperty = servicediscovery_mixins.CfnPrivateDnsNamespacePropsMixin.SOAProperty(
                    ttl=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__082c054e29ff846ff5f74d95caf0240ac852c00e5433b7e03b75c06067e287c8)
                check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ttl is not None:
                self._values["ttl"] = ttl

        @builtins.property
        def ttl(self) -> typing.Optional[jsii.Number]:
            '''The time to live (TTL) for purposes of negative caching.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-privatednsnamespace-soa.html#cfn-servicediscovery-privatednsnamespace-soa-ttl
            '''
            result = self._values.get("ttl")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SOAProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_servicediscovery.mixins.CfnPublicDnsNamespaceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "properties": "properties",
        "tags": "tags",
    },
)
class CfnPublicDnsNamespaceMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPublicDnsNamespacePropsMixin.PropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPublicDnsNamespacePropsMixin.

        :param description: A description for the namespace.
        :param name: The name that you want to assign to this namespace. .. epigraph:: Do not include sensitive information in the name. The name is publicly available using DNS queries.
        :param properties: Properties for the public DNS namespace.
        :param tags: The tags for the namespace. Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-publicdnsnamespace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicediscovery import mixins as servicediscovery_mixins
            
            cfn_public_dns_namespace_mixin_props = servicediscovery_mixins.CfnPublicDnsNamespaceMixinProps(
                description="description",
                name="name",
                properties=servicediscovery_mixins.CfnPublicDnsNamespacePropsMixin.PropertiesProperty(
                    dns_properties=servicediscovery_mixins.CfnPublicDnsNamespacePropsMixin.PublicDnsPropertiesMutableProperty(
                        soa=servicediscovery_mixins.CfnPublicDnsNamespacePropsMixin.SOAProperty(
                            ttl=123
                        )
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1519247186593c0cc185c533473ce5ee00c0337e30b6a429bd9ff49553a0f4f3)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if properties is not None:
            self._values["properties"] = properties
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-publicdnsnamespace.html#cfn-servicediscovery-publicdnsnamespace-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name that you want to assign to this namespace.

        .. epigraph::

           Do not include sensitive information in the name. The name is publicly available using DNS queries.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-publicdnsnamespace.html#cfn-servicediscovery-publicdnsnamespace-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPublicDnsNamespacePropsMixin.PropertiesProperty"]]:
        '''Properties for the public DNS namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-publicdnsnamespace.html#cfn-servicediscovery-publicdnsnamespace-properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPublicDnsNamespacePropsMixin.PropertiesProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags for the namespace.

        Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-publicdnsnamespace.html#cfn-servicediscovery-publicdnsnamespace-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPublicDnsNamespaceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPublicDnsNamespacePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_servicediscovery.mixins.CfnPublicDnsNamespacePropsMixin",
):
    '''Creates a public namespace based on DNS, which is visible on the internet.

    The namespace defines your service naming scheme. For example, if you name your namespace ``example.com`` and name your service ``backend`` , the resulting DNS name for the service is ``backend.example.com`` . You can discover instances that were registered with a public DNS namespace by using either a ``DiscoverInstances`` request or using DNS. For the current quota on the number of namespaces that you can create using the same AWS account , see `AWS Cloud Map quotas <https://docs.aws.amazon.com/cloud-map/latest/dg/cloud-map-limits.html>`_ in the *AWS Cloud Map Developer Guide* .
    .. epigraph::

       The ``CreatePublicDnsNamespace`` API operation is not supported in the AWS GovCloud (US) Regions.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-publicdnsnamespace.html
    :cloudformationResource: AWS::ServiceDiscovery::PublicDnsNamespace
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicediscovery import mixins as servicediscovery_mixins
        
        cfn_public_dns_namespace_props_mixin = servicediscovery_mixins.CfnPublicDnsNamespacePropsMixin(servicediscovery_mixins.CfnPublicDnsNamespaceMixinProps(
            description="description",
            name="name",
            properties=servicediscovery_mixins.CfnPublicDnsNamespacePropsMixin.PropertiesProperty(
                dns_properties=servicediscovery_mixins.CfnPublicDnsNamespacePropsMixin.PublicDnsPropertiesMutableProperty(
                    soa=servicediscovery_mixins.CfnPublicDnsNamespacePropsMixin.SOAProperty(
                        ttl=123
                    )
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
        props: typing.Union[CfnPublicDnsNamespaceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceDiscovery::PublicDnsNamespace``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11006825bdeae959af5ec7c1b04a73109b0fa8a41ea4978f97805319a3c7645b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__08468200bc446e43fa4062beba524ebfb6fd06720065efa601230d42b2c5a956)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a95b17c32b5102533763e720454116710a7723b7ff2c165703b32549a3b68a1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPublicDnsNamespaceMixinProps:
        return typing.cast(CfnPublicDnsNamespaceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_servicediscovery.mixins.CfnPublicDnsNamespacePropsMixin.PropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"dns_properties": "dnsProperties"},
    )
    class PropertiesProperty:
        def __init__(
            self,
            *,
            dns_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPublicDnsNamespacePropsMixin.PublicDnsPropertiesMutableProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Properties for the public DNS namespace.

            :param dns_properties: DNS properties for the public DNS namespace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-publicdnsnamespace-properties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_servicediscovery import mixins as servicediscovery_mixins
                
                properties_property = servicediscovery_mixins.CfnPublicDnsNamespacePropsMixin.PropertiesProperty(
                    dns_properties=servicediscovery_mixins.CfnPublicDnsNamespacePropsMixin.PublicDnsPropertiesMutableProperty(
                        soa=servicediscovery_mixins.CfnPublicDnsNamespacePropsMixin.SOAProperty(
                            ttl=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3cb55fe509b0338a767d7289ed6eff76dadb91db1b394c4d840bf938e873ff6a)
                check_type(argname="argument dns_properties", value=dns_properties, expected_type=type_hints["dns_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dns_properties is not None:
                self._values["dns_properties"] = dns_properties

        @builtins.property
        def dns_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPublicDnsNamespacePropsMixin.PublicDnsPropertiesMutableProperty"]]:
            '''DNS properties for the public DNS namespace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-publicdnsnamespace-properties.html#cfn-servicediscovery-publicdnsnamespace-properties-dnsproperties
            '''
            result = self._values.get("dns_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPublicDnsNamespacePropsMixin.PublicDnsPropertiesMutableProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_servicediscovery.mixins.CfnPublicDnsNamespacePropsMixin.PublicDnsPropertiesMutableProperty",
        jsii_struct_bases=[],
        name_mapping={"soa": "soa"},
    )
    class PublicDnsPropertiesMutableProperty:
        def __init__(
            self,
            *,
            soa: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPublicDnsNamespacePropsMixin.SOAProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''DNS properties for the public DNS namespace.

            :param soa: Start of Authority (SOA) record for the hosted zone for the public DNS namespace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-publicdnsnamespace-publicdnspropertiesmutable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_servicediscovery import mixins as servicediscovery_mixins
                
                public_dns_properties_mutable_property = servicediscovery_mixins.CfnPublicDnsNamespacePropsMixin.PublicDnsPropertiesMutableProperty(
                    soa=servicediscovery_mixins.CfnPublicDnsNamespacePropsMixin.SOAProperty(
                        ttl=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5b90416f4b3b0207bc78749cb4e2e45fe8d0dc4dd7fb4885809135d51a71131c)
                check_type(argname="argument soa", value=soa, expected_type=type_hints["soa"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if soa is not None:
                self._values["soa"] = soa

        @builtins.property
        def soa(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPublicDnsNamespacePropsMixin.SOAProperty"]]:
            '''Start of Authority (SOA) record for the hosted zone for the public DNS namespace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-publicdnsnamespace-publicdnspropertiesmutable.html#cfn-servicediscovery-publicdnsnamespace-publicdnspropertiesmutable-soa
            '''
            result = self._values.get("soa")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPublicDnsNamespacePropsMixin.SOAProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PublicDnsPropertiesMutableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_servicediscovery.mixins.CfnPublicDnsNamespacePropsMixin.SOAProperty",
        jsii_struct_bases=[],
        name_mapping={"ttl": "ttl"},
    )
    class SOAProperty:
        def __init__(self, *, ttl: typing.Optional[jsii.Number] = None) -> None:
            '''Start of Authority (SOA) properties for a public or private DNS namespace.

            :param ttl: The time to live (TTL) for purposes of negative caching.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-publicdnsnamespace-soa.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_servicediscovery import mixins as servicediscovery_mixins
                
                s_oAProperty = servicediscovery_mixins.CfnPublicDnsNamespacePropsMixin.SOAProperty(
                    ttl=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7833058a8c651a3fdb00fc8861c039f4af36231afe97a3ed388861f0526b5888)
                check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ttl is not None:
                self._values["ttl"] = ttl

        @builtins.property
        def ttl(self) -> typing.Optional[jsii.Number]:
            '''The time to live (TTL) for purposes of negative caching.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-publicdnsnamespace-soa.html#cfn-servicediscovery-publicdnsnamespace-soa-ttl
            '''
            result = self._values.get("ttl")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SOAProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_servicediscovery.mixins.CfnServiceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "dns_config": "dnsConfig",
        "health_check_config": "healthCheckConfig",
        "health_check_custom_config": "healthCheckCustomConfig",
        "name": "name",
        "namespace_id": "namespaceId",
        "service_attributes": "serviceAttributes",
        "tags": "tags",
        "type": "type",
    },
)
class CfnServiceMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        dns_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.DnsConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        health_check_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.HealthCheckConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        health_check_custom_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.HealthCheckCustomConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        namespace_id: typing.Optional[builtins.str] = None,
        service_attributes: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnServicePropsMixin.

        :param description: The description of the service.
        :param dns_config: A complex type that contains information about the Route 53 DNS records that you want AWS Cloud Map to create when you register an instance. .. epigraph:: The record types of a service can only be changed by deleting the service and recreating it with a new ``Dnsconfig`` .
        :param health_check_config: *Public DNS and HTTP namespaces only.* A complex type that contains settings for an optional health check. If you specify settings for a health check, AWS Cloud Map associates the health check with the records that you specify in ``DnsConfig`` . For information about the charges for health checks, see `Amazon Route 53 Pricing <https://docs.aws.amazon.com/route53/pricing/>`_ .
        :param health_check_custom_config: A complex type that contains information about an optional custom health check. .. epigraph:: If you specify a health check configuration, you can specify either ``HealthCheckCustomConfig`` or ``HealthCheckConfig`` but not both.
        :param name: The name of the service.
        :param namespace_id: The ID or Amazon Resource Name (ARN) of the namespace that you want to use to create the service. For namespaces shared with your AWS account, specify the namespace ARN. For more information about shared namespaces, see `Cross-account AWS Cloud Map namespace sharing <https://docs.aws.amazon.com/cloud-map/latest/dg/sharing-namespaces.html>`_ in the *AWS Cloud Map Developer Guide* .
        :param service_attributes: A complex type that contains information about attributes associated with a specific service.
        :param tags: The tags for the service. Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.
        :param type: If present, specifies that the service instances are only discoverable using the ``DiscoverInstances`` API operation. No DNS records is registered for the service instances. The only valid value is ``HTTP`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicediscovery import mixins as servicediscovery_mixins
            
            # service_attributes: Any
            
            cfn_service_mixin_props = servicediscovery_mixins.CfnServiceMixinProps(
                description="description",
                dns_config=servicediscovery_mixins.CfnServicePropsMixin.DnsConfigProperty(
                    dns_records=[servicediscovery_mixins.CfnServicePropsMixin.DnsRecordProperty(
                        ttl=123,
                        type="type"
                    )],
                    namespace_id="namespaceId",
                    routing_policy="routingPolicy"
                ),
                health_check_config=servicediscovery_mixins.CfnServicePropsMixin.HealthCheckConfigProperty(
                    failure_threshold=123,
                    resource_path="resourcePath",
                    type="type"
                ),
                health_check_custom_config=servicediscovery_mixins.CfnServicePropsMixin.HealthCheckCustomConfigProperty(
                    failure_threshold=123
                ),
                name="name",
                namespace_id="namespaceId",
                service_attributes=service_attributes,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__722cb81ff0c57becf9e2596c6faa8e9f8ea79a1b2463ea7117710dbc721f1c4e)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dns_config", value=dns_config, expected_type=type_hints["dns_config"])
            check_type(argname="argument health_check_config", value=health_check_config, expected_type=type_hints["health_check_config"])
            check_type(argname="argument health_check_custom_config", value=health_check_custom_config, expected_type=type_hints["health_check_custom_config"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace_id", value=namespace_id, expected_type=type_hints["namespace_id"])
            check_type(argname="argument service_attributes", value=service_attributes, expected_type=type_hints["service_attributes"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if dns_config is not None:
            self._values["dns_config"] = dns_config
        if health_check_config is not None:
            self._values["health_check_config"] = health_check_config
        if health_check_custom_config is not None:
            self._values["health_check_custom_config"] = health_check_custom_config
        if name is not None:
            self._values["name"] = name
        if namespace_id is not None:
            self._values["namespace_id"] = namespace_id
        if service_attributes is not None:
            self._values["service_attributes"] = service_attributes
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.DnsConfigProperty"]]:
        '''A complex type that contains information about the Route 53 DNS records that you want AWS Cloud Map to create when you register an instance.

        .. epigraph::

           The record types of a service can only be changed by deleting the service and recreating it with a new ``Dnsconfig`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-dnsconfig
        '''
        result = self._values.get("dns_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.DnsConfigProperty"]], result)

    @builtins.property
    def health_check_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.HealthCheckConfigProperty"]]:
        '''*Public DNS and HTTP namespaces only.* A complex type that contains settings for an optional health check. If you specify settings for a health check, AWS Cloud Map associates the health check with the records that you specify in ``DnsConfig`` .

        For information about the charges for health checks, see `Amazon Route 53 Pricing <https://docs.aws.amazon.com/route53/pricing/>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-healthcheckconfig
        '''
        result = self._values.get("health_check_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.HealthCheckConfigProperty"]], result)

    @builtins.property
    def health_check_custom_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.HealthCheckCustomConfigProperty"]]:
        '''A complex type that contains information about an optional custom health check.

        .. epigraph::

           If you specify a health check configuration, you can specify either ``HealthCheckCustomConfig`` or ``HealthCheckConfig`` but not both.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-healthcheckcustomconfig
        '''
        result = self._values.get("health_check_custom_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.HealthCheckCustomConfigProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace_id(self) -> typing.Optional[builtins.str]:
        '''The ID or Amazon Resource Name (ARN) of the namespace that you want to use to create the service.

        For namespaces shared with your AWS account, specify the namespace ARN. For more information about shared namespaces, see `Cross-account AWS Cloud Map namespace sharing <https://docs.aws.amazon.com/cloud-map/latest/dg/sharing-namespaces.html>`_ in the *AWS Cloud Map Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-namespaceid
        '''
        result = self._values.get("namespace_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_attributes(self) -> typing.Any:
        '''A complex type that contains information about attributes associated with a specific service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-serviceattributes
        '''
        result = self._values.get("service_attributes")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags for the service.

        Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''If present, specifies that the service instances are only discoverable using the ``DiscoverInstances`` API operation.

        No DNS records is registered for the service instances. The only valid value is ``HTTP`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-type
        '''
        result = self._values.get("type")
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
    jsii_type="@aws-cdk/mixins-preview.aws_servicediscovery.mixins.CfnServicePropsMixin",
):
    '''A complex type that contains information about the specified service.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html
    :cloudformationResource: AWS::ServiceDiscovery::Service
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicediscovery import mixins as servicediscovery_mixins
        
        # service_attributes: Any
        
        cfn_service_props_mixin = servicediscovery_mixins.CfnServicePropsMixin(servicediscovery_mixins.CfnServiceMixinProps(
            description="description",
            dns_config=servicediscovery_mixins.CfnServicePropsMixin.DnsConfigProperty(
                dns_records=[servicediscovery_mixins.CfnServicePropsMixin.DnsRecordProperty(
                    ttl=123,
                    type="type"
                )],
                namespace_id="namespaceId",
                routing_policy="routingPolicy"
            ),
            health_check_config=servicediscovery_mixins.CfnServicePropsMixin.HealthCheckConfigProperty(
                failure_threshold=123,
                resource_path="resourcePath",
                type="type"
            ),
            health_check_custom_config=servicediscovery_mixins.CfnServicePropsMixin.HealthCheckCustomConfigProperty(
                failure_threshold=123
            ),
            name="name",
            namespace_id="namespaceId",
            service_attributes=service_attributes,
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
        props: typing.Union[CfnServiceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceDiscovery::Service``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4927b4aa43a759806586d2ddd6e0715a7cad9a6bdc5e4ded89ed0ff57c0e45f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa0cd7c03dc56bdb45ad31443ae0071e8e8e766fe93a65076ff835845d31d487)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39400e62220db13f41f4940b1d9035df741442f0bd6af532f76b00ec4981a5f1)
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
        jsii_type="@aws-cdk/mixins-preview.aws_servicediscovery.mixins.CfnServicePropsMixin.DnsConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dns_records": "dnsRecords",
            "namespace_id": "namespaceId",
            "routing_policy": "routingPolicy",
        },
    )
    class DnsConfigProperty:
        def __init__(
            self,
            *,
            dns_records: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.DnsRecordProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            namespace_id: typing.Optional[builtins.str] = None,
            routing_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A complex type that contains information about the Amazon Route 53 DNS records that you want AWS Cloud Map to create when you register an instance.

            :param dns_records: An array that contains one ``DnsRecord`` object for each Route 53 DNS record that you want AWS Cloud Map to create when you register an instance. .. epigraph:: The record type of a service can't be updated directly and can only be changed by deleting the service and recreating it with a new ``DnsConfig`` .
            :param namespace_id: *Use NamespaceId in `Service <https://docs.aws.amazon.com/cloud-map/latest/api/API_Service.html>`_ instead.*. The ID of the namespace to use for DNS configuration.
            :param routing_policy: The routing policy that you want to apply to all Route 53 DNS records that AWS Cloud Map creates when you register an instance and specify this service. .. epigraph:: If you want to use this service to register instances that create alias records, specify ``WEIGHTED`` for the routing policy. You can specify the following values: - **MULTIVALUE** - If you define a health check for the service and the health check is healthy, Route 53 returns the applicable value for up to eight instances. For example, suppose that the service includes configurations for one ``A`` record and a health check. You use the service to register 10 instances. Route 53 responds to DNS queries with IP addresses for up to eight healthy instances. If fewer than eight instances are healthy, Route 53 responds to every DNS query with the IP addresses for all of the healthy instances. If you don't define a health check for the service, Route 53 assumes that all instances are healthy and returns the values for up to eight instances. For more information about the multivalue routing policy, see `Multivalue Answer Routing <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html#routing-policy-multivalue>`_ in the *Route 53 Developer Guide* . - **WEIGHTED** - Route 53 returns the applicable value from one randomly selected instance from among the instances that you registered using the same service. Currently, all records have the same weight, so you can't route more or less traffic to any instances. For example, suppose that the service includes configurations for one ``A`` record and a health check. You use the service to register 10 instances. Route 53 responds to DNS queries with the IP address for one randomly selected instance from among the healthy instances. If no instances are healthy, Route 53 responds to DNS queries as if all of the instances were healthy. If you don't define a health check for the service, Route 53 assumes that all instances are healthy and returns the applicable value for one randomly selected instance. For more information about the weighted routing policy, see `Weighted Routing <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html#routing-policy-weighted>`_ in the *Route 53 Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_servicediscovery import mixins as servicediscovery_mixins
                
                dns_config_property = servicediscovery_mixins.CfnServicePropsMixin.DnsConfigProperty(
                    dns_records=[servicediscovery_mixins.CfnServicePropsMixin.DnsRecordProperty(
                        ttl=123,
                        type="type"
                    )],
                    namespace_id="namespaceId",
                    routing_policy="routingPolicy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6db1a42d1e569900c7ab3a28b1fd907f5e236a440425aa1d26248c44b8b7aa69)
                check_type(argname="argument dns_records", value=dns_records, expected_type=type_hints["dns_records"])
                check_type(argname="argument namespace_id", value=namespace_id, expected_type=type_hints["namespace_id"])
                check_type(argname="argument routing_policy", value=routing_policy, expected_type=type_hints["routing_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dns_records is not None:
                self._values["dns_records"] = dns_records
            if namespace_id is not None:
                self._values["namespace_id"] = namespace_id
            if routing_policy is not None:
                self._values["routing_policy"] = routing_policy

        @builtins.property
        def dns_records(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.DnsRecordProperty"]]]]:
            '''An array that contains one ``DnsRecord`` object for each Route 53 DNS record that you want AWS Cloud Map to create when you register an instance.

            .. epigraph::

               The record type of a service can't be updated directly and can only be changed by deleting the service and recreating it with a new ``DnsConfig`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsconfig.html#cfn-servicediscovery-service-dnsconfig-dnsrecords
            '''
            result = self._values.get("dns_records")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.DnsRecordProperty"]]]], result)

        @builtins.property
        def namespace_id(self) -> typing.Optional[builtins.str]:
            '''*Use NamespaceId in `Service <https://docs.aws.amazon.com/cloud-map/latest/api/API_Service.html>`_ instead.*.

            The ID of the namespace to use for DNS configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsconfig.html#cfn-servicediscovery-service-dnsconfig-namespaceid
            '''
            result = self._values.get("namespace_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def routing_policy(self) -> typing.Optional[builtins.str]:
            '''The routing policy that you want to apply to all Route 53 DNS records that AWS Cloud Map creates when you register an instance and specify this service.

            .. epigraph::

               If you want to use this service to register instances that create alias records, specify ``WEIGHTED`` for the routing policy.

            You can specify the following values:

            - **MULTIVALUE** - If you define a health check for the service and the health check is healthy, Route 53 returns the applicable value for up to eight instances.

            For example, suppose that the service includes configurations for one ``A`` record and a health check. You use the service to register 10 instances. Route 53 responds to DNS queries with IP addresses for up to eight healthy instances. If fewer than eight instances are healthy, Route 53 responds to every DNS query with the IP addresses for all of the healthy instances.

            If you don't define a health check for the service, Route 53 assumes that all instances are healthy and returns the values for up to eight instances.

            For more information about the multivalue routing policy, see `Multivalue Answer Routing <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html#routing-policy-multivalue>`_ in the *Route 53 Developer Guide* .

            - **WEIGHTED** - Route 53 returns the applicable value from one randomly selected instance from among the instances that you registered using the same service. Currently, all records have the same weight, so you can't route more or less traffic to any instances.

            For example, suppose that the service includes configurations for one ``A`` record and a health check. You use the service to register 10 instances. Route 53 responds to DNS queries with the IP address for one randomly selected instance from among the healthy instances. If no instances are healthy, Route 53 responds to DNS queries as if all of the instances were healthy.

            If you don't define a health check for the service, Route 53 assumes that all instances are healthy and returns the applicable value for one randomly selected instance.

            For more information about the weighted routing policy, see `Weighted Routing <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html#routing-policy-weighted>`_ in the *Route 53 Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsconfig.html#cfn-servicediscovery-service-dnsconfig-routingpolicy
            '''
            result = self._values.get("routing_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DnsConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_servicediscovery.mixins.CfnServicePropsMixin.DnsRecordProperty",
        jsii_struct_bases=[],
        name_mapping={"ttl": "ttl", "type": "type"},
    )
    class DnsRecordProperty:
        def __init__(
            self,
            *,
            ttl: typing.Optional[jsii.Number] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A complex type that contains information about the Route 53 DNS records that you want AWS Cloud Map to create when you register an instance.

            :param ttl: The amount of time, in seconds, that you want DNS resolvers to cache the settings for this record. .. epigraph:: Alias records don't include a TTL because Route 53 uses the TTL for the AWS resource that an alias record routes traffic to. If you include the ``AWS_ALIAS_DNS_NAME`` attribute when you submit a `RegisterInstance <https://docs.aws.amazon.com/cloud-map/latest/api/API_RegisterInstance.html>`_ request, the ``TTL`` value is ignored. Always specify a TTL for the service; you can use a service to register instances that create either alias or non-alias records.
            :param type: The type of the resource, which indicates the type of value that Route 53 returns in response to DNS queries. You can specify values for ``Type`` in the following combinations: - ``A`` - ``AAAA`` - ``A`` and ``AAAA`` - ``SRV`` - ``CNAME`` If you want AWS Cloud Map to create a Route 53 alias record when you register an instance, specify ``A`` or ``AAAA`` for ``Type`` . You specify other settings, such as the IP address for ``A`` and ``AAAA`` records, when you register an instance. For more information, see `RegisterInstance <https://docs.aws.amazon.com/cloud-map/latest/api/API_RegisterInstance.html>`_ . The following values are supported: - **A** - Route 53 returns the IP address of the resource in IPv4 format, such as 192.0.2.44. - **AAAA** - Route 53 returns the IP address of the resource in IPv6 format, such as 2001:0db8:85a3:0000:0000:abcd:0001:2345. - **CNAME** - Route 53 returns the domain name of the resource, such as www.example.com. Note the following: - You specify the domain name that you want to route traffic to when you register an instance. For more information, see `Attributes <https://docs.aws.amazon.com/cloud-map/latest/api/API_RegisterInstance.html#cloudmap-RegisterInstance-request-Attributes>`_ in the topic `RegisterInstance <https://docs.aws.amazon.com/cloud-map/latest/api/API_RegisterInstance.html>`_ . - You must specify ``WEIGHTED`` for the value of ``RoutingPolicy`` . - You can't specify both ``CNAME`` for ``Type`` and settings for ``HealthCheckConfig`` . If you do, the request will fail with an ``InvalidInput`` error. - **SRV** - Route 53 returns the value for an ``SRV`` record. The value for an ``SRV`` record uses the following values: ``priority weight port service-hostname`` Note the following about the values: - The values of ``priority`` and ``weight`` are both set to ``1`` and can't be changed. - The value of ``port`` comes from the value that you specify for the ``AWS_INSTANCE_PORT`` attribute when you submit a `RegisterInstance <https://docs.aws.amazon.com/cloud-map/latest/api/API_RegisterInstance.html>`_ request. - The value of ``service-hostname`` is a concatenation of the following values: - The value that you specify for ``InstanceId`` when you register an instance. - The name of the service. - The name of the namespace. For example, if the value of ``InstanceId`` is ``test`` , the name of the service is ``backend`` , and the name of the namespace is ``example.com`` , the value of ``service-hostname`` is: ``test.backend.example.com`` If you specify settings for an ``SRV`` record and if you specify values for ``AWS_INSTANCE_IPV4`` , ``AWS_INSTANCE_IPV6`` , or both in the ``RegisterInstance`` request, AWS Cloud Map automatically creates ``A`` and/or ``AAAA`` records that have the same name as the value of ``service-hostname`` in the ``SRV`` record. You can ignore these records.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsrecord.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_servicediscovery import mixins as servicediscovery_mixins
                
                dns_record_property = servicediscovery_mixins.CfnServicePropsMixin.DnsRecordProperty(
                    ttl=123,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2fee6c05978ddd187fc5e56cd71fc2a3f3714f6324f62a3cccc7a8b115780831)
                check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ttl is not None:
                self._values["ttl"] = ttl
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def ttl(self) -> typing.Optional[jsii.Number]:
            '''The amount of time, in seconds, that you want DNS resolvers to cache the settings for this record.

            .. epigraph::

               Alias records don't include a TTL because Route 53 uses the TTL for the AWS resource that an alias record routes traffic to. If you include the ``AWS_ALIAS_DNS_NAME`` attribute when you submit a `RegisterInstance <https://docs.aws.amazon.com/cloud-map/latest/api/API_RegisterInstance.html>`_ request, the ``TTL`` value is ignored. Always specify a TTL for the service; you can use a service to register instances that create either alias or non-alias records.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsrecord.html#cfn-servicediscovery-service-dnsrecord-ttl
            '''
            result = self._values.get("ttl")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of the resource, which indicates the type of value that Route 53 returns in response to DNS queries.

            You can specify values for ``Type`` in the following combinations:

            - ``A``
            - ``AAAA``
            - ``A`` and ``AAAA``
            - ``SRV``
            - ``CNAME``

            If you want AWS Cloud Map to create a Route 53 alias record when you register an instance, specify ``A`` or ``AAAA`` for ``Type`` .

            You specify other settings, such as the IP address for ``A`` and ``AAAA`` records, when you register an instance. For more information, see `RegisterInstance <https://docs.aws.amazon.com/cloud-map/latest/api/API_RegisterInstance.html>`_ .

            The following values are supported:

            - **A** - Route 53 returns the IP address of the resource in IPv4 format, such as 192.0.2.44.
            - **AAAA** - Route 53 returns the IP address of the resource in IPv6 format, such as 2001:0db8:85a3:0000:0000:abcd:0001:2345.
            - **CNAME** - Route 53 returns the domain name of the resource, such as www.example.com. Note the following:
            - You specify the domain name that you want to route traffic to when you register an instance. For more information, see `Attributes <https://docs.aws.amazon.com/cloud-map/latest/api/API_RegisterInstance.html#cloudmap-RegisterInstance-request-Attributes>`_ in the topic `RegisterInstance <https://docs.aws.amazon.com/cloud-map/latest/api/API_RegisterInstance.html>`_ .
            - You must specify ``WEIGHTED`` for the value of ``RoutingPolicy`` .
            - You can't specify both ``CNAME`` for ``Type`` and settings for ``HealthCheckConfig`` . If you do, the request will fail with an ``InvalidInput`` error.
            - **SRV** - Route 53 returns the value for an ``SRV`` record. The value for an ``SRV`` record uses the following values:

            ``priority weight port service-hostname``

            Note the following about the values:

            - The values of ``priority`` and ``weight`` are both set to ``1`` and can't be changed.
            - The value of ``port`` comes from the value that you specify for the ``AWS_INSTANCE_PORT`` attribute when you submit a `RegisterInstance <https://docs.aws.amazon.com/cloud-map/latest/api/API_RegisterInstance.html>`_ request.
            - The value of ``service-hostname`` is a concatenation of the following values:
            - The value that you specify for ``InstanceId`` when you register an instance.
            - The name of the service.
            - The name of the namespace.

            For example, if the value of ``InstanceId`` is ``test`` , the name of the service is ``backend`` , and the name of the namespace is ``example.com`` , the value of ``service-hostname`` is:

            ``test.backend.example.com``

            If you specify settings for an ``SRV`` record and if you specify values for ``AWS_INSTANCE_IPV4`` , ``AWS_INSTANCE_IPV6`` , or both in the ``RegisterInstance`` request, AWS Cloud Map automatically creates ``A`` and/or ``AAAA`` records that have the same name as the value of ``service-hostname`` in the ``SRV`` record. You can ignore these records.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsrecord.html#cfn-servicediscovery-service-dnsrecord-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DnsRecordProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_servicediscovery.mixins.CfnServicePropsMixin.HealthCheckConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "failure_threshold": "failureThreshold",
            "resource_path": "resourcePath",
            "type": "type",
        },
    )
    class HealthCheckConfigProperty:
        def __init__(
            self,
            *,
            failure_threshold: typing.Optional[jsii.Number] = None,
            resource_path: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''*Public DNS and HTTP namespaces only.* A complex type that contains settings for an optional health check. If you specify settings for a health check, AWS Cloud Map associates the health check with the records that you specify in ``DnsConfig`` .

            .. epigraph::

               If you specify a health check configuration, you can specify either ``HealthCheckCustomConfig`` or ``HealthCheckConfig`` but not both.

            Health checks are basic Route 53 health checks that monitor an AWS endpoint. For information about pricing for health checks, see `Amazon Route 53 Pricing <https://docs.aws.amazon.com/route53/pricing/>`_ .

            Note the following about configuring health checks.

            - **A and AAAA records** - If ``DnsConfig`` includes configurations for both ``A`` and ``AAAA`` records, AWS Cloud Map creates a health check that uses the IPv4 address to check the health of the resource. If the endpoint tthat's specified by the IPv4 address is unhealthy, Route 53 considers both the ``A`` and ``AAAA`` records to be unhealthy.
            - **CNAME records** - You can't specify settings for ``HealthCheckConfig`` when the ``DNSConfig`` includes ``CNAME`` for the value of ``Type`` . If you do, the ``CreateService`` request will fail with an ``InvalidInput`` error.
            - **Request interval** - A Route 53 health checker in each health-checking AWS Region sends a health check request to an endpoint every 30 seconds. On average, your endpoint receives a health check request about every two seconds. However, health checkers don't coordinate with one another. Therefore, you might sometimes see several requests in one second that's followed by a few seconds with no health checks at all.
            - **Health checking regions** - Health checkers perform checks from all Route 53 health-checking Regions. For a list of the current Regions, see `Regions <https://docs.aws.amazon.com/Route53/latest/APIReference/API_HealthCheckConfig.html#Route53-Type-HealthCheckConfig-Regions>`_ .
            - **Alias records** - When you register an instance, if you include the ``AWS_ALIAS_DNS_NAME`` attribute, AWS Cloud Map creates a Route 53 alias record. Note the following:
            - Route 53 automatically sets ``EvaluateTargetHealth`` to true for alias records. When ``EvaluateTargetHealth`` is true, the alias record inherits the health of the referenced AWS resource. such as an ELB load balancer. For more information, see `EvaluateTargetHealth <https://docs.aws.amazon.com/Route53/latest/APIReference/API_AliasTarget.html#Route53-Type-AliasTarget-EvaluateTargetHealth>`_ .
            - If you include ``HealthCheckConfig`` and then use the service to register an instance that creates an alias record, Route 53 doesn't create the health check.
            - **Charges for health checks** - Health checks are basic Route 53 health checks that monitor an AWS endpoint. For information about pricing for health checks, see `Amazon Route 53 Pricing <https://docs.aws.amazon.com/route53/pricing/>`_ .

            :param failure_threshold: The number of consecutive health checks that an endpoint must pass or fail for Route 53 to change the current status of the endpoint from unhealthy to healthy or the other way around. For more information, see `How Route 53 Determines Whether an Endpoint Is Healthy <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-determining-health-of-endpoints.html>`_ in the *Route 53 Developer Guide* .
            :param resource_path: The path that you want Route 53 to request when performing health checks. The path can be any value that your endpoint returns an HTTP status code of a 2xx or 3xx format for when the endpoint is healthy. An example file is ``/docs/route53-health-check.html`` . Route 53 automatically adds the DNS name for the service. If you don't specify a value for ``ResourcePath`` , the default value is ``/`` . If you specify ``TCP`` for ``Type`` , you must *not* specify a value for ``ResourcePath`` .
            :param type: The type of health check that you want to create, which indicates how Route 53 determines whether an endpoint is healthy. .. epigraph:: You can't change the value of ``Type`` after you create a health check. You can create the following types of health checks: - *HTTP* : Route 53 tries to establish a TCP connection. If successful, Route 53 submits an HTTP request and waits for an HTTP status code of 200 or greater and less than 400. - *HTTPS* : Route 53 tries to establish a TCP connection. If successful, Route 53 submits an HTTPS request and waits for an HTTP status code of 200 or greater and less than 400. .. epigraph:: If you specify HTTPS for the value of ``Type`` , the endpoint must support TLS v1.0 or later. - *TCP* : Route 53 tries to establish a TCP connection. If you specify ``TCP`` for ``Type`` , don't specify a value for ``ResourcePath`` . For more information, see `How Route 53 Determines Whether an Endpoint Is Healthy <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-determining-health-of-endpoints.html>`_ in the *Route 53 Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-healthcheckconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_servicediscovery import mixins as servicediscovery_mixins
                
                health_check_config_property = servicediscovery_mixins.CfnServicePropsMixin.HealthCheckConfigProperty(
                    failure_threshold=123,
                    resource_path="resourcePath",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__585665193fa65d9bd0f4087829ced3562c96375e57c9fe9f01776a0e6ccefef3)
                check_type(argname="argument failure_threshold", value=failure_threshold, expected_type=type_hints["failure_threshold"])
                check_type(argname="argument resource_path", value=resource_path, expected_type=type_hints["resource_path"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if failure_threshold is not None:
                self._values["failure_threshold"] = failure_threshold
            if resource_path is not None:
                self._values["resource_path"] = resource_path
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def failure_threshold(self) -> typing.Optional[jsii.Number]:
            '''The number of consecutive health checks that an endpoint must pass or fail for Route 53 to change the current status of the endpoint from unhealthy to healthy or the other way around.

            For more information, see `How Route 53 Determines Whether an Endpoint Is Healthy <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-determining-health-of-endpoints.html>`_ in the *Route 53 Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-healthcheckconfig.html#cfn-servicediscovery-service-healthcheckconfig-failurethreshold
            '''
            result = self._values.get("failure_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def resource_path(self) -> typing.Optional[builtins.str]:
            '''The path that you want Route 53 to request when performing health checks.

            The path can be any value that your endpoint returns an HTTP status code of a 2xx or 3xx format for when the endpoint is healthy. An example file is ``/docs/route53-health-check.html`` . Route 53 automatically adds the DNS name for the service. If you don't specify a value for ``ResourcePath`` , the default value is ``/`` .

            If you specify ``TCP`` for ``Type`` , you must *not* specify a value for ``ResourcePath`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-healthcheckconfig.html#cfn-servicediscovery-service-healthcheckconfig-resourcepath
            '''
            result = self._values.get("resource_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of health check that you want to create, which indicates how Route 53 determines whether an endpoint is healthy.

            .. epigraph::

               You can't change the value of ``Type`` after you create a health check.

            You can create the following types of health checks:

            - *HTTP* : Route 53 tries to establish a TCP connection. If successful, Route 53 submits an HTTP request and waits for an HTTP status code of 200 or greater and less than 400.
            - *HTTPS* : Route 53 tries to establish a TCP connection. If successful, Route 53 submits an HTTPS request and waits for an HTTP status code of 200 or greater and less than 400.

            .. epigraph::

               If you specify HTTPS for the value of ``Type`` , the endpoint must support TLS v1.0 or later.

            - *TCP* : Route 53 tries to establish a TCP connection.

            If you specify ``TCP`` for ``Type`` , don't specify a value for ``ResourcePath`` .

            For more information, see `How Route 53 Determines Whether an Endpoint Is Healthy <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-determining-health-of-endpoints.html>`_ in the *Route 53 Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-healthcheckconfig.html#cfn-servicediscovery-service-healthcheckconfig-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HealthCheckConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_servicediscovery.mixins.CfnServicePropsMixin.HealthCheckCustomConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"failure_threshold": "failureThreshold"},
    )
    class HealthCheckCustomConfigProperty:
        def __init__(
            self,
            *,
            failure_threshold: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A complex type that contains information about an optional custom health check.

            A custom health check, which requires that you use a third-party health checker to evaluate the health of your resources, is useful in the following circumstances:

            - You can't use a health check that's defined by ``HealthCheckConfig`` because the resource isn't available over the internet. For example, you can use a custom health check when the instance is in an Amazon VPC. (To check the health of resources in a VPC, the health checker must also be in the VPC.)
            - You want to use a third-party health checker regardless of where your resources are located.

            .. epigraph::

               If you specify a health check configuration, you can specify either ``HealthCheckCustomConfig`` or ``HealthCheckConfig`` but not both.

            To change the status of a custom health check, submit an ``UpdateInstanceCustomHealthStatus`` request. AWS Cloud Map doesn't monitor the status of the resource, it just keeps a record of the status specified in the most recent ``UpdateInstanceCustomHealthStatus`` request.

            Here's how custom health checks work:

            - You create a service.
            - You register an instance.
            - You configure a third-party health checker to monitor the resource that's associated with the new instance.

            .. epigraph::

               AWS Cloud Map doesn't check the health of the resource directly.

            - The third-party health-checker determines that the resource is unhealthy and notifies your application.
            - Your application submits an ``UpdateInstanceCustomHealthStatus`` request.
            - AWS Cloud Map waits for 30 seconds.
            - If another ``UpdateInstanceCustomHealthStatus`` request doesn't arrive during that time to change the status back to healthy, AWS Cloud Map stops routing traffic to the resource.

            :param failure_threshold: .. epigraph:: This parameter is no longer supported and is always set to 1. AWS Cloud Map waits for approximately 30 seconds after receiving an ``UpdateInstanceCustomHealthStatus`` request before changing the status of the service instance. The number of 30-second intervals that you want AWS Cloud Map to wait after receiving an ``UpdateInstanceCustomHealthStatus`` request before it changes the health status of a service instance. Sending a second or subsequent ``UpdateInstanceCustomHealthStatus`` request with the same value before 30 seconds has passed doesn't accelerate the change. AWS Cloud Map still waits ``30`` seconds after the first request to make the change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-healthcheckcustomconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_servicediscovery import mixins as servicediscovery_mixins
                
                health_check_custom_config_property = servicediscovery_mixins.CfnServicePropsMixin.HealthCheckCustomConfigProperty(
                    failure_threshold=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f8bd78c728d35effc33cbf0b143c2a83659951c53dc0bfad50ab08193144f795)
                check_type(argname="argument failure_threshold", value=failure_threshold, expected_type=type_hints["failure_threshold"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if failure_threshold is not None:
                self._values["failure_threshold"] = failure_threshold

        @builtins.property
        def failure_threshold(self) -> typing.Optional[jsii.Number]:
            '''.. epigraph::

   This parameter is no longer supported and is always set to 1.

            AWS Cloud Map waits for approximately 30 seconds after receiving an ``UpdateInstanceCustomHealthStatus`` request before changing the status of the service instance.

            The number of 30-second intervals that you want AWS Cloud Map to wait after receiving an ``UpdateInstanceCustomHealthStatus`` request before it changes the health status of a service instance.

            Sending a second or subsequent ``UpdateInstanceCustomHealthStatus`` request with the same value before 30 seconds has passed doesn't accelerate the change. AWS Cloud Map still waits ``30`` seconds after the first request to make the change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-healthcheckcustomconfig.html#cfn-servicediscovery-service-healthcheckcustomconfig-failurethreshold
            '''
            result = self._values.get("failure_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HealthCheckCustomConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnHttpNamespaceMixinProps",
    "CfnHttpNamespacePropsMixin",
    "CfnInstanceMixinProps",
    "CfnInstancePropsMixin",
    "CfnPrivateDnsNamespaceMixinProps",
    "CfnPrivateDnsNamespacePropsMixin",
    "CfnPublicDnsNamespaceMixinProps",
    "CfnPublicDnsNamespacePropsMixin",
    "CfnServiceMixinProps",
    "CfnServicePropsMixin",
]

publication.publish()

def _typecheckingstub__9fc2cb20960b706f0d6d1ee3ee1afef094f530acf4e3717bf096adec9d576f46(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8910cc6b27ae792fd9546fe1be096f12d2ff6e2c3660f5f259f4573fce038b07(
    props: typing.Union[CfnHttpNamespaceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__973503c159abac8fabafbed73bf6e768a57f375fcbd8cc65cdbc3cdd6a8775d8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4320488579fc0931d52ec7fa0621f48c23e19ba1ebfd4d6a5c480981fddf7945(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09fca416f756247df39b50a9f14ab40afeab65ff49bf1b107fe260d92415a151(
    *,
    instance_attributes: typing.Any = None,
    instance_id: typing.Optional[builtins.str] = None,
    service_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9514f54d0f998dcb0b8394d502ebbe3a6fd3d32c88dfa7c326f13633fe571b3(
    props: typing.Union[CfnInstanceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7367c4d65d7d87500d9cd4aebf07078ee4237f658bf974edf0a5c2b050d7184d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa788b8f1ae0cf2bfeb4ef95bac7491af5a00e3c6465f978ecdd60b37eea259(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__339a9530458dce0a711303fdfef99e5e8ac6e4ac04939101e73becd726ad90ea(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPrivateDnsNamespacePropsMixin.PropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69e0f70049a344c12d55f06765cd1b9e7863c29f1bed074ff4b524de87b0f5b5(
    props: typing.Union[CfnPrivateDnsNamespaceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f035a2d55512053a8ec3ac82df99328265a767b4c8069e4f3ef1785eed5f12(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b9ec13f5aa0cba05e49305fd8e7b172845a8125a3a235130882b5982248fab3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__902cc0865505445b946d094ebc746941f05916af1b11e84ac05e1d91e13b152b(
    *,
    soa: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPrivateDnsNamespacePropsMixin.SOAProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d69f3a5bfa8690e7c9f12e6a0046e95127fe5e81a059eed0528d3e6b717b2e2d(
    *,
    dns_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPrivateDnsNamespacePropsMixin.PrivateDnsPropertiesMutableProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__082c054e29ff846ff5f74d95caf0240ac852c00e5433b7e03b75c06067e287c8(
    *,
    ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1519247186593c0cc185c533473ce5ee00c0337e30b6a429bd9ff49553a0f4f3(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPublicDnsNamespacePropsMixin.PropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11006825bdeae959af5ec7c1b04a73109b0fa8a41ea4978f97805319a3c7645b(
    props: typing.Union[CfnPublicDnsNamespaceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08468200bc446e43fa4062beba524ebfb6fd06720065efa601230d42b2c5a956(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a95b17c32b5102533763e720454116710a7723b7ff2c165703b32549a3b68a1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb55fe509b0338a767d7289ed6eff76dadb91db1b394c4d840bf938e873ff6a(
    *,
    dns_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPublicDnsNamespacePropsMixin.PublicDnsPropertiesMutableProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b90416f4b3b0207bc78749cb4e2e45fe8d0dc4dd7fb4885809135d51a71131c(
    *,
    soa: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPublicDnsNamespacePropsMixin.SOAProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7833058a8c651a3fdb00fc8861c039f4af36231afe97a3ed388861f0526b5888(
    *,
    ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__722cb81ff0c57becf9e2596c6faa8e9f8ea79a1b2463ea7117710dbc721f1c4e(
    *,
    description: typing.Optional[builtins.str] = None,
    dns_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.DnsConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    health_check_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.HealthCheckConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    health_check_custom_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.HealthCheckCustomConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    namespace_id: typing.Optional[builtins.str] = None,
    service_attributes: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4927b4aa43a759806586d2ddd6e0715a7cad9a6bdc5e4ded89ed0ff57c0e45f1(
    props: typing.Union[CfnServiceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0cd7c03dc56bdb45ad31443ae0071e8e8e766fe93a65076ff835845d31d487(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39400e62220db13f41f4940b1d9035df741442f0bd6af532f76b00ec4981a5f1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6db1a42d1e569900c7ab3a28b1fd907f5e236a440425aa1d26248c44b8b7aa69(
    *,
    dns_records: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.DnsRecordProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    namespace_id: typing.Optional[builtins.str] = None,
    routing_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fee6c05978ddd187fc5e56cd71fc2a3f3714f6324f62a3cccc7a8b115780831(
    *,
    ttl: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__585665193fa65d9bd0f4087829ced3562c96375e57c9fe9f01776a0e6ccefef3(
    *,
    failure_threshold: typing.Optional[jsii.Number] = None,
    resource_path: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8bd78c728d35effc33cbf0b143c2a83659951c53dc0bfad50ab08193144f795(
    *,
    failure_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
