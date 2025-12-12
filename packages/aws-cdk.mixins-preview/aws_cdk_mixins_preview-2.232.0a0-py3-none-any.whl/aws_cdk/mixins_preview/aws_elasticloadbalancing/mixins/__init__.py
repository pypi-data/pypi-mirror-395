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
    jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancing.mixins.CfnLoadBalancerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_logging_policy": "accessLoggingPolicy",
        "app_cookie_stickiness_policy": "appCookieStickinessPolicy",
        "availability_zones": "availabilityZones",
        "connection_draining_policy": "connectionDrainingPolicy",
        "connection_settings": "connectionSettings",
        "cross_zone": "crossZone",
        "health_check": "healthCheck",
        "instances": "instances",
        "lb_cookie_stickiness_policy": "lbCookieStickinessPolicy",
        "listeners": "listeners",
        "load_balancer_name": "loadBalancerName",
        "policies": "policies",
        "scheme": "scheme",
        "security_groups": "securityGroups",
        "subnets": "subnets",
        "tags": "tags",
    },
)
class CfnLoadBalancerMixinProps:
    def __init__(
        self,
        *,
        access_logging_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLoadBalancerPropsMixin.AccessLoggingPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        app_cookie_stickiness_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLoadBalancerPropsMixin.AppCookieStickinessPolicyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection_draining_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLoadBalancerPropsMixin.ConnectionDrainingPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        connection_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLoadBalancerPropsMixin.ConnectionSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        cross_zone: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        health_check: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLoadBalancerPropsMixin.HealthCheckProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        instances: typing.Optional[typing.Sequence[builtins.str]] = None,
        lb_cookie_stickiness_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLoadBalancerPropsMixin.LBCookieStickinessPolicyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        listeners: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLoadBalancerPropsMixin.ListenersProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLoadBalancerPropsMixin.PoliciesProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        scheme: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnLoadBalancerPropsMixin.

        :param access_logging_policy: Information about where and how access logs are stored for the load balancer.
        :param app_cookie_stickiness_policy: Information about a policy for application-controlled session stickiness.
        :param availability_zones: The Availability Zones for a load balancer in a default VPC. For a load balancer in a nondefault VPC, specify ``Subnets`` instead. Update requires replacement if you did not previously specify an Availability Zone or if you are removing all Availability Zones. Otherwise, update requires no interruption.
        :param connection_draining_policy: If enabled, the load balancer allows existing requests to complete before the load balancer shifts traffic away from a deregistered or unhealthy instance. For more information, see `Configure connection draining <https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-conn-drain.html>`_ in the *User Guide for Classic Load Balancers* .
        :param connection_settings: If enabled, the load balancer allows the connections to remain idle (no data is sent over the connection) for the specified duration. By default, Elastic Load Balancing maintains a 60-second idle connection timeout for both front-end and back-end connections of your load balancer. For more information, see `Configure idle connection timeout <https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html>`_ in the *User Guide for Classic Load Balancers* .
        :param cross_zone: If enabled, the load balancer routes the request traffic evenly across all instances regardless of the Availability Zones. For more information, see `Configure cross-zone load balancing <https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/enable-disable-crosszone-lb.html>`_ in the *User Guide for Classic Load Balancers* .
        :param health_check: The health check settings to use when evaluating the health of your EC2 instances. Update requires replacement if you did not previously specify health check settings or if you are removing the health check settings. Otherwise, update requires no interruption.
        :param instances: The IDs of the instances for the load balancer.
        :param lb_cookie_stickiness_policy: Information about a policy for duration-based session stickiness.
        :param listeners: The listeners for the load balancer. You can specify at most one listener per port. If you update the properties for a listener, AWS CloudFormation deletes the existing listener and creates a new one with the specified properties. While the new listener is being created, clients cannot connect to the load balancer.
        :param load_balancer_name: The name of the load balancer. This name must be unique within your set of load balancers for the region. If you don't specify a name, AWS CloudFormation generates a unique physical ID for the load balancer. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . If you specify a name, you cannot perform updates that require replacement of this resource, but you can perform other updates. To replace the resource, specify a new name.
        :param policies: The policies defined for your Classic Load Balancer. Specify only back-end server policies.
        :param scheme: The type of load balancer. Valid only for load balancers in a VPC. If ``Scheme`` is ``internet-facing`` , the load balancer has a public DNS name that resolves to a public IP address. If ``Scheme`` is ``internal`` , the load balancer has a public DNS name that resolves to a private IP address.
        :param security_groups: The security groups for the load balancer. Valid only for load balancers in a VPC.
        :param subnets: The IDs of the subnets for the load balancer. You can specify at most one subnet per Availability Zone. Update requires replacement if you did not previously specify a subnet or if you are removing all subnets. Otherwise, update requires no interruption. To update to a different subnet in the current Availability Zone, you must first update to a subnet in a different Availability Zone, then update to the new subnet in the original Availability Zone.
        :param tags: The tags associated with a load balancer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancing-loadbalancer.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_elasticloadbalancing import mixins as elasticloadbalancing_mixins
            
            # attributes: Any
            
            cfn_load_balancer_mixin_props = elasticloadbalancing_mixins.CfnLoadBalancerMixinProps(
                access_logging_policy=elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin.AccessLoggingPolicyProperty(
                    emit_interval=123,
                    enabled=False,
                    s3_bucket_name="s3BucketName",
                    s3_bucket_prefix="s3BucketPrefix"
                ),
                app_cookie_stickiness_policy=[elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin.AppCookieStickinessPolicyProperty(
                    cookie_name="cookieName",
                    policy_name="policyName"
                )],
                availability_zones=["availabilityZones"],
                connection_draining_policy=elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin.ConnectionDrainingPolicyProperty(
                    enabled=False,
                    timeout=123
                ),
                connection_settings=elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin.ConnectionSettingsProperty(
                    idle_timeout=123
                ),
                cross_zone=False,
                health_check=elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin.HealthCheckProperty(
                    healthy_threshold="healthyThreshold",
                    interval="interval",
                    target="target",
                    timeout="timeout",
                    unhealthy_threshold="unhealthyThreshold"
                ),
                instances=["instances"],
                lb_cookie_stickiness_policy=[elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin.LBCookieStickinessPolicyProperty(
                    cookie_expiration_period="cookieExpirationPeriod",
                    policy_name="policyName"
                )],
                listeners=[elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin.ListenersProperty(
                    instance_port="instancePort",
                    instance_protocol="instanceProtocol",
                    load_balancer_port="loadBalancerPort",
                    policy_names=["policyNames"],
                    protocol="protocol",
                    ssl_certificate_id="sslCertificateId"
                )],
                load_balancer_name="loadBalancerName",
                policies=[elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin.PoliciesProperty(
                    attributes=[attributes],
                    instance_ports=["instancePorts"],
                    load_balancer_ports=["loadBalancerPorts"],
                    policy_name="policyName",
                    policy_type="policyType"
                )],
                scheme="scheme",
                security_groups=["securityGroups"],
                subnets=["subnets"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b5f63383565ee0eeb104fe13eb260c650b0187c2c8132aaaa6151a6c630b35f)
            check_type(argname="argument access_logging_policy", value=access_logging_policy, expected_type=type_hints["access_logging_policy"])
            check_type(argname="argument app_cookie_stickiness_policy", value=app_cookie_stickiness_policy, expected_type=type_hints["app_cookie_stickiness_policy"])
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument connection_draining_policy", value=connection_draining_policy, expected_type=type_hints["connection_draining_policy"])
            check_type(argname="argument connection_settings", value=connection_settings, expected_type=type_hints["connection_settings"])
            check_type(argname="argument cross_zone", value=cross_zone, expected_type=type_hints["cross_zone"])
            check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
            check_type(argname="argument instances", value=instances, expected_type=type_hints["instances"])
            check_type(argname="argument lb_cookie_stickiness_policy", value=lb_cookie_stickiness_policy, expected_type=type_hints["lb_cookie_stickiness_policy"])
            check_type(argname="argument listeners", value=listeners, expected_type=type_hints["listeners"])
            check_type(argname="argument load_balancer_name", value=load_balancer_name, expected_type=type_hints["load_balancer_name"])
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
            check_type(argname="argument scheme", value=scheme, expected_type=type_hints["scheme"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_logging_policy is not None:
            self._values["access_logging_policy"] = access_logging_policy
        if app_cookie_stickiness_policy is not None:
            self._values["app_cookie_stickiness_policy"] = app_cookie_stickiness_policy
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if connection_draining_policy is not None:
            self._values["connection_draining_policy"] = connection_draining_policy
        if connection_settings is not None:
            self._values["connection_settings"] = connection_settings
        if cross_zone is not None:
            self._values["cross_zone"] = cross_zone
        if health_check is not None:
            self._values["health_check"] = health_check
        if instances is not None:
            self._values["instances"] = instances
        if lb_cookie_stickiness_policy is not None:
            self._values["lb_cookie_stickiness_policy"] = lb_cookie_stickiness_policy
        if listeners is not None:
            self._values["listeners"] = listeners
        if load_balancer_name is not None:
            self._values["load_balancer_name"] = load_balancer_name
        if policies is not None:
            self._values["policies"] = policies
        if scheme is not None:
            self._values["scheme"] = scheme
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def access_logging_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoadBalancerPropsMixin.AccessLoggingPolicyProperty"]]:
        '''Information about where and how access logs are stored for the load balancer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancing-loadbalancer.html#cfn-elasticloadbalancing-loadbalancer-accessloggingpolicy
        '''
        result = self._values.get("access_logging_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoadBalancerPropsMixin.AccessLoggingPolicyProperty"]], result)

    @builtins.property
    def app_cookie_stickiness_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoadBalancerPropsMixin.AppCookieStickinessPolicyProperty"]]]]:
        '''Information about a policy for application-controlled session stickiness.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancing-loadbalancer.html#cfn-elasticloadbalancing-loadbalancer-appcookiestickinesspolicy
        '''
        result = self._values.get("app_cookie_stickiness_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoadBalancerPropsMixin.AppCookieStickinessPolicyProperty"]]]], result)

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Availability Zones for a load balancer in a default VPC.

        For a load balancer in a nondefault VPC, specify ``Subnets`` instead.

        Update requires replacement if you did not previously specify an Availability Zone or if you are removing all Availability Zones. Otherwise, update requires no interruption.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancing-loadbalancer.html#cfn-elasticloadbalancing-loadbalancer-availabilityzones
        '''
        result = self._values.get("availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def connection_draining_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoadBalancerPropsMixin.ConnectionDrainingPolicyProperty"]]:
        '''If enabled, the load balancer allows existing requests to complete before the load balancer shifts traffic away from a deregistered or unhealthy instance.

        For more information, see `Configure connection draining <https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-conn-drain.html>`_ in the *User Guide for Classic Load Balancers* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancing-loadbalancer.html#cfn-elasticloadbalancing-loadbalancer-connectiondrainingpolicy
        '''
        result = self._values.get("connection_draining_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoadBalancerPropsMixin.ConnectionDrainingPolicyProperty"]], result)

    @builtins.property
    def connection_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoadBalancerPropsMixin.ConnectionSettingsProperty"]]:
        '''If enabled, the load balancer allows the connections to remain idle (no data is sent over the connection) for the specified duration.

        By default, Elastic Load Balancing maintains a 60-second idle connection timeout for both front-end and back-end connections of your load balancer. For more information, see `Configure idle connection timeout <https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html>`_ in the *User Guide for Classic Load Balancers* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancing-loadbalancer.html#cfn-elasticloadbalancing-loadbalancer-connectionsettings
        '''
        result = self._values.get("connection_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoadBalancerPropsMixin.ConnectionSettingsProperty"]], result)

    @builtins.property
    def cross_zone(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''If enabled, the load balancer routes the request traffic evenly across all instances regardless of the Availability Zones.

        For more information, see `Configure cross-zone load balancing <https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/enable-disable-crosszone-lb.html>`_ in the *User Guide for Classic Load Balancers* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancing-loadbalancer.html#cfn-elasticloadbalancing-loadbalancer-crosszone
        '''
        result = self._values.get("cross_zone")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def health_check(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoadBalancerPropsMixin.HealthCheckProperty"]]:
        '''The health check settings to use when evaluating the health of your EC2 instances.

        Update requires replacement if you did not previously specify health check settings or if you are removing the health check settings. Otherwise, update requires no interruption.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancing-loadbalancer.html#cfn-elasticloadbalancing-loadbalancer-healthcheck
        '''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoadBalancerPropsMixin.HealthCheckProperty"]], result)

    @builtins.property
    def instances(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IDs of the instances for the load balancer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancing-loadbalancer.html#cfn-elasticloadbalancing-loadbalancer-instances
        '''
        result = self._values.get("instances")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def lb_cookie_stickiness_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoadBalancerPropsMixin.LBCookieStickinessPolicyProperty"]]]]:
        '''Information about a policy for duration-based session stickiness.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancing-loadbalancer.html#cfn-elasticloadbalancing-loadbalancer-lbcookiestickinesspolicy
        '''
        result = self._values.get("lb_cookie_stickiness_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoadBalancerPropsMixin.LBCookieStickinessPolicyProperty"]]]], result)

    @builtins.property
    def listeners(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoadBalancerPropsMixin.ListenersProperty"]]]]:
        '''The listeners for the load balancer. You can specify at most one listener per port.

        If you update the properties for a listener, AWS CloudFormation deletes the existing listener and creates a new one with the specified properties. While the new listener is being created, clients cannot connect to the load balancer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancing-loadbalancer.html#cfn-elasticloadbalancing-loadbalancer-listeners
        '''
        result = self._values.get("listeners")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoadBalancerPropsMixin.ListenersProperty"]]]], result)

    @builtins.property
    def load_balancer_name(self) -> typing.Optional[builtins.str]:
        '''The name of the load balancer.

        This name must be unique within your set of load balancers for the region.

        If you don't specify a name, AWS CloudFormation generates a unique physical ID for the load balancer. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . If you specify a name, you cannot perform updates that require replacement of this resource, but you can perform other updates. To replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancing-loadbalancer.html#cfn-elasticloadbalancing-loadbalancer-loadbalancername
        '''
        result = self._values.get("load_balancer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policies(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoadBalancerPropsMixin.PoliciesProperty"]]]]:
        '''The policies defined for your Classic Load Balancer.

        Specify only back-end server policies.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancing-loadbalancer.html#cfn-elasticloadbalancing-loadbalancer-policies
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoadBalancerPropsMixin.PoliciesProperty"]]]], result)

    @builtins.property
    def scheme(self) -> typing.Optional[builtins.str]:
        '''The type of load balancer. Valid only for load balancers in a VPC.

        If ``Scheme`` is ``internet-facing`` , the load balancer has a public DNS name that resolves to a public IP address.

        If ``Scheme`` is ``internal`` , the load balancer has a public DNS name that resolves to a private IP address.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancing-loadbalancer.html#cfn-elasticloadbalancing-loadbalancer-scheme
        '''
        result = self._values.get("scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The security groups for the load balancer.

        Valid only for load balancers in a VPC.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancing-loadbalancer.html#cfn-elasticloadbalancing-loadbalancer-securitygroups
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IDs of the subnets for the load balancer. You can specify at most one subnet per Availability Zone.

        Update requires replacement if you did not previously specify a subnet or if you are removing all subnets. Otherwise, update requires no interruption. To update to a different subnet in the current Availability Zone, you must first update to a subnet in a different Availability Zone, then update to the new subnet in the original Availability Zone.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancing-loadbalancer.html#cfn-elasticloadbalancing-loadbalancer-subnets
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags associated with a load balancer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancing-loadbalancer.html#cfn-elasticloadbalancing-loadbalancer-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLoadBalancerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLoadBalancerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancing.mixins.CfnLoadBalancerPropsMixin",
):
    '''Specifies a Classic Load Balancer.

    If this resource has a public IP address and is also in a VPC that is defined in the same template, you must use the `DependsOn attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ to declare a dependency on the VPC-gateway attachment.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancing-loadbalancer.html
    :cloudformationResource: AWS::ElasticLoadBalancing::LoadBalancer
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_elasticloadbalancing import mixins as elasticloadbalancing_mixins
        
        # attributes: Any
        
        cfn_load_balancer_props_mixin = elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin(elasticloadbalancing_mixins.CfnLoadBalancerMixinProps(
            access_logging_policy=elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin.AccessLoggingPolicyProperty(
                emit_interval=123,
                enabled=False,
                s3_bucket_name="s3BucketName",
                s3_bucket_prefix="s3BucketPrefix"
            ),
            app_cookie_stickiness_policy=[elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin.AppCookieStickinessPolicyProperty(
                cookie_name="cookieName",
                policy_name="policyName"
            )],
            availability_zones=["availabilityZones"],
            connection_draining_policy=elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin.ConnectionDrainingPolicyProperty(
                enabled=False,
                timeout=123
            ),
            connection_settings=elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin.ConnectionSettingsProperty(
                idle_timeout=123
            ),
            cross_zone=False,
            health_check=elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin.HealthCheckProperty(
                healthy_threshold="healthyThreshold",
                interval="interval",
                target="target",
                timeout="timeout",
                unhealthy_threshold="unhealthyThreshold"
            ),
            instances=["instances"],
            lb_cookie_stickiness_policy=[elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin.LBCookieStickinessPolicyProperty(
                cookie_expiration_period="cookieExpirationPeriod",
                policy_name="policyName"
            )],
            listeners=[elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin.ListenersProperty(
                instance_port="instancePort",
                instance_protocol="instanceProtocol",
                load_balancer_port="loadBalancerPort",
                policy_names=["policyNames"],
                protocol="protocol",
                ssl_certificate_id="sslCertificateId"
            )],
            load_balancer_name="loadBalancerName",
            policies=[elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin.PoliciesProperty(
                attributes=[attributes],
                instance_ports=["instancePorts"],
                load_balancer_ports=["loadBalancerPorts"],
                policy_name="policyName",
                policy_type="policyType"
            )],
            scheme="scheme",
            security_groups=["securityGroups"],
            subnets=["subnets"],
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
        props: typing.Union[CfnLoadBalancerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ElasticLoadBalancing::LoadBalancer``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d64726ebad41344728c7f9b210166ff29ad28784d7a56dbe848b66817aefc50)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d602f636ad7fb900f12c71ed14ace402ae6018288723a6d0c82dda9797118530)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25df8f7ef8cb32f6da200b7ea67a7941187398828d8d3376baa0bc9374c791a7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLoadBalancerMixinProps:
        return typing.cast(CfnLoadBalancerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancing.mixins.CfnLoadBalancerPropsMixin.AccessLoggingPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "emit_interval": "emitInterval",
            "enabled": "enabled",
            "s3_bucket_name": "s3BucketName",
            "s3_bucket_prefix": "s3BucketPrefix",
        },
    )
    class AccessLoggingPolicyProperty:
        def __init__(
            self,
            *,
            emit_interval: typing.Optional[jsii.Number] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            s3_bucket_name: typing.Optional[builtins.str] = None,
            s3_bucket_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies where and how access logs are stored for your Classic Load Balancer.

            :param emit_interval: The interval for publishing the access logs. You can specify an interval of either 5 minutes or 60 minutes. Default: 60 minutes
            :param enabled: Specifies whether access logs are enabled for the load balancer.
            :param s3_bucket_name: The name of the Amazon S3 bucket where the access logs are stored.
            :param s3_bucket_prefix: The logical hierarchy you created for your Amazon S3 bucket, for example ``my-bucket-prefix/prod`` . If the prefix is not provided, the log is placed at the root level of the bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-accessloggingpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancing import mixins as elasticloadbalancing_mixins
                
                access_logging_policy_property = elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin.AccessLoggingPolicyProperty(
                    emit_interval=123,
                    enabled=False,
                    s3_bucket_name="s3BucketName",
                    s3_bucket_prefix="s3BucketPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2cc4e1612663c458c557158684a1977edc101cba43002716fdd81010c1014d9b)
                check_type(argname="argument emit_interval", value=emit_interval, expected_type=type_hints["emit_interval"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
                check_type(argname="argument s3_bucket_prefix", value=s3_bucket_prefix, expected_type=type_hints["s3_bucket_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if emit_interval is not None:
                self._values["emit_interval"] = emit_interval
            if enabled is not None:
                self._values["enabled"] = enabled
            if s3_bucket_name is not None:
                self._values["s3_bucket_name"] = s3_bucket_name
            if s3_bucket_prefix is not None:
                self._values["s3_bucket_prefix"] = s3_bucket_prefix

        @builtins.property
        def emit_interval(self) -> typing.Optional[jsii.Number]:
            '''The interval for publishing the access logs. You can specify an interval of either 5 minutes or 60 minutes.

            Default: 60 minutes

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-accessloggingpolicy.html#cfn-elasticloadbalancing-loadbalancer-accessloggingpolicy-emitinterval
            '''
            result = self._values.get("emit_interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether access logs are enabled for the load balancer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-accessloggingpolicy.html#cfn-elasticloadbalancing-loadbalancer-accessloggingpolicy-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def s3_bucket_name(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon S3 bucket where the access logs are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-accessloggingpolicy.html#cfn-elasticloadbalancing-loadbalancer-accessloggingpolicy-s3bucketname
            '''
            result = self._values.get("s3_bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''The logical hierarchy you created for your Amazon S3 bucket, for example ``my-bucket-prefix/prod`` .

            If the prefix is not provided, the log is placed at the root level of the bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-accessloggingpolicy.html#cfn-elasticloadbalancing-loadbalancer-accessloggingpolicy-s3bucketprefix
            '''
            result = self._values.get("s3_bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessLoggingPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancing.mixins.CfnLoadBalancerPropsMixin.AppCookieStickinessPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"cookie_name": "cookieName", "policy_name": "policyName"},
    )
    class AppCookieStickinessPolicyProperty:
        def __init__(
            self,
            *,
            cookie_name: typing.Optional[builtins.str] = None,
            policy_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies a policy for application-controlled session stickiness for your Classic Load Balancer.

            To associate a policy with a listener, use the `PolicyNames <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html#cfn-ec2-elb-listener-policynames>`_ property for the listener.

            :param cookie_name: The name of the application cookie used for stickiness.
            :param policy_name: The mnemonic name for the policy being created. The name must be unique within a set of policies for this load balancer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-appcookiestickinesspolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancing import mixins as elasticloadbalancing_mixins
                
                app_cookie_stickiness_policy_property = elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin.AppCookieStickinessPolicyProperty(
                    cookie_name="cookieName",
                    policy_name="policyName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__316639026a902b69aa74e2ad830e0f065e349ade410d5df6aa6e125f4330330b)
                check_type(argname="argument cookie_name", value=cookie_name, expected_type=type_hints["cookie_name"])
                check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cookie_name is not None:
                self._values["cookie_name"] = cookie_name
            if policy_name is not None:
                self._values["policy_name"] = policy_name

        @builtins.property
        def cookie_name(self) -> typing.Optional[builtins.str]:
            '''The name of the application cookie used for stickiness.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-appcookiestickinesspolicy.html#cfn-elasticloadbalancing-loadbalancer-appcookiestickinesspolicy-cookiename
            '''
            result = self._values.get("cookie_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def policy_name(self) -> typing.Optional[builtins.str]:
            '''The mnemonic name for the policy being created.

            The name must be unique within a set of policies for this load balancer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-appcookiestickinesspolicy.html#cfn-elasticloadbalancing-loadbalancer-appcookiestickinesspolicy-policyname
            '''
            result = self._values.get("policy_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AppCookieStickinessPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancing.mixins.CfnLoadBalancerPropsMixin.ConnectionDrainingPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "timeout": "timeout"},
    )
    class ConnectionDrainingPolicyProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            timeout: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the connection draining settings for your Classic Load Balancer.

            :param enabled: Specifies whether connection draining is enabled for the load balancer.
            :param timeout: The maximum time, in seconds, to keep the existing connections open before deregistering the instances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-connectiondrainingpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancing import mixins as elasticloadbalancing_mixins
                
                connection_draining_policy_property = elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin.ConnectionDrainingPolicyProperty(
                    enabled=False,
                    timeout=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f929135a194cfef7e38532e126641b357c52647595a0b7d85f714482c55f62d1)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if timeout is not None:
                self._values["timeout"] = timeout

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether connection draining is enabled for the load balancer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-connectiondrainingpolicy.html#cfn-elasticloadbalancing-loadbalancer-connectiondrainingpolicy-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def timeout(self) -> typing.Optional[jsii.Number]:
            '''The maximum time, in seconds, to keep the existing connections open before deregistering the instances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-connectiondrainingpolicy.html#cfn-elasticloadbalancing-loadbalancer-connectiondrainingpolicy-timeout
            '''
            result = self._values.get("timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectionDrainingPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancing.mixins.CfnLoadBalancerPropsMixin.ConnectionSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"idle_timeout": "idleTimeout"},
    )
    class ConnectionSettingsProperty:
        def __init__(
            self,
            *,
            idle_timeout: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the idle timeout value for your Classic Load Balancer.

            :param idle_timeout: The time, in seconds, that the connection is allowed to be idle (no data has been sent over the connection) before it is closed by the load balancer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-connectionsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancing import mixins as elasticloadbalancing_mixins
                
                connection_settings_property = elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin.ConnectionSettingsProperty(
                    idle_timeout=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__56084dd29f7e8577442e5a27def43de1fd5270512cb66b7a983b82338fb99bb1)
                check_type(argname="argument idle_timeout", value=idle_timeout, expected_type=type_hints["idle_timeout"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if idle_timeout is not None:
                self._values["idle_timeout"] = idle_timeout

        @builtins.property
        def idle_timeout(self) -> typing.Optional[jsii.Number]:
            '''The time, in seconds, that the connection is allowed to be idle (no data has been sent over the connection) before it is closed by the load balancer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-connectionsettings.html#cfn-elasticloadbalancing-loadbalancer-connectionsettings-idletimeout
            '''
            result = self._values.get("idle_timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectionSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancing.mixins.CfnLoadBalancerPropsMixin.HealthCheckProperty",
        jsii_struct_bases=[],
        name_mapping={
            "healthy_threshold": "healthyThreshold",
            "interval": "interval",
            "target": "target",
            "timeout": "timeout",
            "unhealthy_threshold": "unhealthyThreshold",
        },
    )
    class HealthCheckProperty:
        def __init__(
            self,
            *,
            healthy_threshold: typing.Optional[builtins.str] = None,
            interval: typing.Optional[builtins.str] = None,
            target: typing.Optional[builtins.str] = None,
            timeout: typing.Optional[builtins.str] = None,
            unhealthy_threshold: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies health check settings for your Classic Load Balancer.

            :param healthy_threshold: The number of consecutive health checks successes required before moving the instance to the ``Healthy`` state.
            :param interval: The approximate interval, in seconds, between health checks of an individual instance.
            :param target: The instance being checked. The protocol is either TCP, HTTP, HTTPS, or SSL. The range of valid ports is one (1) through 65535. TCP is the default, specified as a TCP: port pair, for example "TCP:5000". In this case, a health check simply attempts to open a TCP connection to the instance on the specified port. Failure to connect within the configured timeout is considered unhealthy. SSL is also specified as SSL: port pair, for example, SSL:5000. For HTTP/HTTPS, you must include a ping path in the string. HTTP is specified as a HTTP:port;/;PathToPing; grouping, for example "HTTP:80/weather/us/wa/seattle". In this case, a HTTP GET request is issued to the instance on the given port and path. Any answer other than "200 OK" within the timeout period is considered unhealthy. The total length of the HTTP ping target must be 1024 16-bit Unicode characters or less.
            :param timeout: The amount of time, in seconds, during which no response means a failed health check. This value must be less than the ``Interval`` value.
            :param unhealthy_threshold: The number of consecutive health check failures required before moving the instance to the ``Unhealthy`` state.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-healthcheck.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancing import mixins as elasticloadbalancing_mixins
                
                health_check_property = elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin.HealthCheckProperty(
                    healthy_threshold="healthyThreshold",
                    interval="interval",
                    target="target",
                    timeout="timeout",
                    unhealthy_threshold="unhealthyThreshold"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0aaa0f4d1edd67f29ac0b0517a9ce0945ec0764cf09f9b52ab545196ffc7e491)
                check_type(argname="argument healthy_threshold", value=healthy_threshold, expected_type=type_hints["healthy_threshold"])
                check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
                check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
                check_type(argname="argument unhealthy_threshold", value=unhealthy_threshold, expected_type=type_hints["unhealthy_threshold"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if healthy_threshold is not None:
                self._values["healthy_threshold"] = healthy_threshold
            if interval is not None:
                self._values["interval"] = interval
            if target is not None:
                self._values["target"] = target
            if timeout is not None:
                self._values["timeout"] = timeout
            if unhealthy_threshold is not None:
                self._values["unhealthy_threshold"] = unhealthy_threshold

        @builtins.property
        def healthy_threshold(self) -> typing.Optional[builtins.str]:
            '''The number of consecutive health checks successes required before moving the instance to the ``Healthy`` state.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-healthcheck.html#cfn-elasticloadbalancing-loadbalancer-healthcheck-healthythreshold
            '''
            result = self._values.get("healthy_threshold")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def interval(self) -> typing.Optional[builtins.str]:
            '''The approximate interval, in seconds, between health checks of an individual instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-healthcheck.html#cfn-elasticloadbalancing-loadbalancer-healthcheck-interval
            '''
            result = self._values.get("interval")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target(self) -> typing.Optional[builtins.str]:
            '''The instance being checked.

            The protocol is either TCP, HTTP, HTTPS, or SSL. The range of valid ports is one (1) through 65535.

            TCP is the default, specified as a TCP: port pair, for example "TCP:5000". In this case, a health check simply attempts to open a TCP connection to the instance on the specified port. Failure to connect within the configured timeout is considered unhealthy.

            SSL is also specified as SSL: port pair, for example, SSL:5000.

            For HTTP/HTTPS, you must include a ping path in the string. HTTP is specified as a HTTP:port;/;PathToPing; grouping, for example "HTTP:80/weather/us/wa/seattle". In this case, a HTTP GET request is issued to the instance on the given port and path. Any answer other than "200 OK" within the timeout period is considered unhealthy.

            The total length of the HTTP ping target must be 1024 16-bit Unicode characters or less.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-healthcheck.html#cfn-elasticloadbalancing-loadbalancer-healthcheck-target
            '''
            result = self._values.get("target")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timeout(self) -> typing.Optional[builtins.str]:
            '''The amount of time, in seconds, during which no response means a failed health check.

            This value must be less than the ``Interval`` value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-healthcheck.html#cfn-elasticloadbalancing-loadbalancer-healthcheck-timeout
            '''
            result = self._values.get("timeout")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unhealthy_threshold(self) -> typing.Optional[builtins.str]:
            '''The number of consecutive health check failures required before moving the instance to the ``Unhealthy`` state.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-healthcheck.html#cfn-elasticloadbalancing-loadbalancer-healthcheck-unhealthythreshold
            '''
            result = self._values.get("unhealthy_threshold")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HealthCheckProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancing.mixins.CfnLoadBalancerPropsMixin.LBCookieStickinessPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cookie_expiration_period": "cookieExpirationPeriod",
            "policy_name": "policyName",
        },
    )
    class LBCookieStickinessPolicyProperty:
        def __init__(
            self,
            *,
            cookie_expiration_period: typing.Optional[builtins.str] = None,
            policy_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies a policy for duration-based session stickiness for your Classic Load Balancer.

            To associate a policy with a listener, use the `PolicyNames <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html#cfn-ec2-elb-listener-policynames>`_ property for the listener.

            :param cookie_expiration_period: The time period, in seconds, after which the cookie should be considered stale. If this parameter is not specified, the stickiness session lasts for the duration of the browser session.
            :param policy_name: The name of the policy. This name must be unique within the set of policies for this load balancer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-lbcookiestickinesspolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancing import mixins as elasticloadbalancing_mixins
                
                l_bCookie_stickiness_policy_property = elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin.LBCookieStickinessPolicyProperty(
                    cookie_expiration_period="cookieExpirationPeriod",
                    policy_name="policyName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c4835a765d9ab4bc2d8600575ea4a223eb9d8195716517efd42207cba65703d)
                check_type(argname="argument cookie_expiration_period", value=cookie_expiration_period, expected_type=type_hints["cookie_expiration_period"])
                check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cookie_expiration_period is not None:
                self._values["cookie_expiration_period"] = cookie_expiration_period
            if policy_name is not None:
                self._values["policy_name"] = policy_name

        @builtins.property
        def cookie_expiration_period(self) -> typing.Optional[builtins.str]:
            '''The time period, in seconds, after which the cookie should be considered stale.

            If this parameter is not specified, the stickiness session lasts for the duration of the browser session.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-lbcookiestickinesspolicy.html#cfn-elasticloadbalancing-loadbalancer-lbcookiestickinesspolicy-cookieexpirationperiod
            '''
            result = self._values.get("cookie_expiration_period")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def policy_name(self) -> typing.Optional[builtins.str]:
            '''The name of the policy.

            This name must be unique within the set of policies for this load balancer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-lbcookiestickinesspolicy.html#cfn-elasticloadbalancing-loadbalancer-lbcookiestickinesspolicy-policyname
            '''
            result = self._values.get("policy_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LBCookieStickinessPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancing.mixins.CfnLoadBalancerPropsMixin.ListenersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "instance_port": "instancePort",
            "instance_protocol": "instanceProtocol",
            "load_balancer_port": "loadBalancerPort",
            "policy_names": "policyNames",
            "protocol": "protocol",
            "ssl_certificate_id": "sslCertificateId",
        },
    )
    class ListenersProperty:
        def __init__(
            self,
            *,
            instance_port: typing.Optional[builtins.str] = None,
            instance_protocol: typing.Optional[builtins.str] = None,
            load_balancer_port: typing.Optional[builtins.str] = None,
            policy_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            protocol: typing.Optional[builtins.str] = None,
            ssl_certificate_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies a listener for your Classic Load Balancer.

            Modifying any property replaces the listener.

            :param instance_port: The port on which the instance is listening.
            :param instance_protocol: The protocol to use for routing traffic to instances: HTTP, HTTPS, TCP, or SSL. If the front-end protocol is TCP or SSL, the back-end protocol must be TCP or SSL. If the front-end protocol is HTTP or HTTPS, the back-end protocol must be HTTP or HTTPS. If there is another listener with the same ``InstancePort`` whose ``InstanceProtocol`` is secure, (HTTPS or SSL), the listener's ``InstanceProtocol`` must also be secure. If there is another listener with the same ``InstancePort`` whose ``InstanceProtocol`` is HTTP or TCP, the listener's ``InstanceProtocol`` must be HTTP or TCP.
            :param load_balancer_port: The port on which the load balancer is listening. On EC2-VPC, you can specify any port from the range 1-65535. On EC2-Classic, you can specify any port from the following list: 25, 80, 443, 465, 587, 1024-65535.
            :param policy_names: The names of the policies to associate with the listener.
            :param protocol: The load balancer transport protocol to use for routing: HTTP, HTTPS, TCP, or SSL.
            :param ssl_certificate_id: The Amazon Resource Name (ARN) of the server certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-listeners.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancing import mixins as elasticloadbalancing_mixins
                
                listeners_property = elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin.ListenersProperty(
                    instance_port="instancePort",
                    instance_protocol="instanceProtocol",
                    load_balancer_port="loadBalancerPort",
                    policy_names=["policyNames"],
                    protocol="protocol",
                    ssl_certificate_id="sslCertificateId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__367e8283d427486456a48c1992da41ae3ecffc90df1918e18a5c6599a57092a7)
                check_type(argname="argument instance_port", value=instance_port, expected_type=type_hints["instance_port"])
                check_type(argname="argument instance_protocol", value=instance_protocol, expected_type=type_hints["instance_protocol"])
                check_type(argname="argument load_balancer_port", value=load_balancer_port, expected_type=type_hints["load_balancer_port"])
                check_type(argname="argument policy_names", value=policy_names, expected_type=type_hints["policy_names"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument ssl_certificate_id", value=ssl_certificate_id, expected_type=type_hints["ssl_certificate_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instance_port is not None:
                self._values["instance_port"] = instance_port
            if instance_protocol is not None:
                self._values["instance_protocol"] = instance_protocol
            if load_balancer_port is not None:
                self._values["load_balancer_port"] = load_balancer_port
            if policy_names is not None:
                self._values["policy_names"] = policy_names
            if protocol is not None:
                self._values["protocol"] = protocol
            if ssl_certificate_id is not None:
                self._values["ssl_certificate_id"] = ssl_certificate_id

        @builtins.property
        def instance_port(self) -> typing.Optional[builtins.str]:
            '''The port on which the instance is listening.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-listeners.html#cfn-elasticloadbalancing-loadbalancer-listeners-instanceport
            '''
            result = self._values.get("instance_port")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_protocol(self) -> typing.Optional[builtins.str]:
            '''The protocol to use for routing traffic to instances: HTTP, HTTPS, TCP, or SSL.

            If the front-end protocol is TCP or SSL, the back-end protocol must be TCP or SSL. If the front-end protocol is HTTP or HTTPS, the back-end protocol must be HTTP or HTTPS.

            If there is another listener with the same ``InstancePort`` whose ``InstanceProtocol`` is secure, (HTTPS or SSL), the listener's ``InstanceProtocol`` must also be secure.

            If there is another listener with the same ``InstancePort`` whose ``InstanceProtocol`` is HTTP or TCP, the listener's ``InstanceProtocol`` must be HTTP or TCP.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-listeners.html#cfn-elasticloadbalancing-loadbalancer-listeners-instanceprotocol
            '''
            result = self._values.get("instance_protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def load_balancer_port(self) -> typing.Optional[builtins.str]:
            '''The port on which the load balancer is listening.

            On EC2-VPC, you can specify any port from the range 1-65535. On EC2-Classic, you can specify any port from the following list: 25, 80, 443, 465, 587, 1024-65535.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-listeners.html#cfn-elasticloadbalancing-loadbalancer-listeners-loadbalancerport
            '''
            result = self._values.get("load_balancer_port")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def policy_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The names of the policies to associate with the listener.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-listeners.html#cfn-elasticloadbalancing-loadbalancer-listeners-policynames
            '''
            result = self._values.get("policy_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The load balancer transport protocol to use for routing: HTTP, HTTPS, TCP, or SSL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-listeners.html#cfn-elasticloadbalancing-loadbalancer-listeners-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ssl_certificate_id(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the server certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-listeners.html#cfn-elasticloadbalancing-loadbalancer-listeners-sslcertificateid
            '''
            result = self._values.get("ssl_certificate_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ListenersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancing.mixins.CfnLoadBalancerPropsMixin.PoliciesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attributes": "attributes",
            "instance_ports": "instancePorts",
            "load_balancer_ports": "loadBalancerPorts",
            "policy_name": "policyName",
            "policy_type": "policyType",
        },
    )
    class PoliciesProperty:
        def __init__(
            self,
            *,
            attributes: typing.Optional[typing.Union[typing.Sequence[typing.Any], _aws_cdk_ceddda9d.IResolvable]] = None,
            instance_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
            load_balancer_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
            policy_name: typing.Optional[builtins.str] = None,
            policy_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies policies for your Classic Load Balancer.

            To associate policies with a listener, use the `PolicyNames <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html#cfn-ec2-elb-listener-policynames>`_ property for the listener.

            :param attributes: The policy attributes.
            :param instance_ports: The instance ports for the policy. Required only for some policy types.
            :param load_balancer_ports: The load balancer ports for the policy. Required only for some policy types.
            :param policy_name: The name of the policy.
            :param policy_type: The name of the policy type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-policies.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancing import mixins as elasticloadbalancing_mixins
                
                # attributes: Any
                
                policies_property = elasticloadbalancing_mixins.CfnLoadBalancerPropsMixin.PoliciesProperty(
                    attributes=[attributes],
                    instance_ports=["instancePorts"],
                    load_balancer_ports=["loadBalancerPorts"],
                    policy_name="policyName",
                    policy_type="policyType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0c654d0e9db5f26ad2747334e914245d5d17fbed45d78044cab5d673326f4b53)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                check_type(argname="argument instance_ports", value=instance_ports, expected_type=type_hints["instance_ports"])
                check_type(argname="argument load_balancer_ports", value=load_balancer_ports, expected_type=type_hints["load_balancer_ports"])
                check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
                check_type(argname="argument policy_type", value=policy_type, expected_type=type_hints["policy_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if instance_ports is not None:
                self._values["instance_ports"] = instance_ports
            if load_balancer_ports is not None:
                self._values["load_balancer_ports"] = load_balancer_ports
            if policy_name is not None:
                self._values["policy_name"] = policy_name
            if policy_type is not None:
                self._values["policy_type"] = policy_type

        @builtins.property
        def attributes(
            self,
        ) -> typing.Optional[typing.Union[typing.List[typing.Any], _aws_cdk_ceddda9d.IResolvable]]:
            '''The policy attributes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-policies.html#cfn-elasticloadbalancing-loadbalancer-policies-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Optional[typing.Union[typing.List[typing.Any], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def instance_ports(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The instance ports for the policy.

            Required only for some policy types.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-policies.html#cfn-elasticloadbalancing-loadbalancer-policies-instanceports
            '''
            result = self._values.get("instance_ports")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def load_balancer_ports(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The load balancer ports for the policy.

            Required only for some policy types.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-policies.html#cfn-elasticloadbalancing-loadbalancer-policies-loadbalancerports
            '''
            result = self._values.get("load_balancer_ports")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def policy_name(self) -> typing.Optional[builtins.str]:
            '''The name of the policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-policies.html#cfn-elasticloadbalancing-loadbalancer-policies-policyname
            '''
            result = self._values.get("policy_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def policy_type(self) -> typing.Optional[builtins.str]:
            '''The name of the policy type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancing-loadbalancer-policies.html#cfn-elasticloadbalancing-loadbalancer-policies-policytype
            '''
            result = self._values.get("policy_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PoliciesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnLoadBalancerMixinProps",
    "CfnLoadBalancerPropsMixin",
]

publication.publish()

def _typecheckingstub__8b5f63383565ee0eeb104fe13eb260c650b0187c2c8132aaaa6151a6c630b35f(
    *,
    access_logging_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLoadBalancerPropsMixin.AccessLoggingPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    app_cookie_stickiness_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLoadBalancerPropsMixin.AppCookieStickinessPolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection_draining_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLoadBalancerPropsMixin.ConnectionDrainingPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    connection_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLoadBalancerPropsMixin.ConnectionSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cross_zone: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    health_check: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLoadBalancerPropsMixin.HealthCheckProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instances: typing.Optional[typing.Sequence[builtins.str]] = None,
    lb_cookie_stickiness_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLoadBalancerPropsMixin.LBCookieStickinessPolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    listeners: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLoadBalancerPropsMixin.ListenersProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    load_balancer_name: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLoadBalancerPropsMixin.PoliciesProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    scheme: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d64726ebad41344728c7f9b210166ff29ad28784d7a56dbe848b66817aefc50(
    props: typing.Union[CfnLoadBalancerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d602f636ad7fb900f12c71ed14ace402ae6018288723a6d0c82dda9797118530(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25df8f7ef8cb32f6da200b7ea67a7941187398828d8d3376baa0bc9374c791a7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc4e1612663c458c557158684a1977edc101cba43002716fdd81010c1014d9b(
    *,
    emit_interval: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    s3_bucket_name: typing.Optional[builtins.str] = None,
    s3_bucket_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316639026a902b69aa74e2ad830e0f065e349ade410d5df6aa6e125f4330330b(
    *,
    cookie_name: typing.Optional[builtins.str] = None,
    policy_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f929135a194cfef7e38532e126641b357c52647595a0b7d85f714482c55f62d1(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56084dd29f7e8577442e5a27def43de1fd5270512cb66b7a983b82338fb99bb1(
    *,
    idle_timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aaa0f4d1edd67f29ac0b0517a9ce0945ec0764cf09f9b52ab545196ffc7e491(
    *,
    healthy_threshold: typing.Optional[builtins.str] = None,
    interval: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[builtins.str] = None,
    unhealthy_threshold: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c4835a765d9ab4bc2d8600575ea4a223eb9d8195716517efd42207cba65703d(
    *,
    cookie_expiration_period: typing.Optional[builtins.str] = None,
    policy_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__367e8283d427486456a48c1992da41ae3ecffc90df1918e18a5c6599a57092a7(
    *,
    instance_port: typing.Optional[builtins.str] = None,
    instance_protocol: typing.Optional[builtins.str] = None,
    load_balancer_port: typing.Optional[builtins.str] = None,
    policy_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    protocol: typing.Optional[builtins.str] = None,
    ssl_certificate_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c654d0e9db5f26ad2747334e914245d5d17fbed45d78044cab5d673326f4b53(
    *,
    attributes: typing.Optional[typing.Union[typing.Sequence[typing.Any], _aws_cdk_ceddda9d.IResolvable]] = None,
    instance_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    load_balancer_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    policy_name: typing.Optional[builtins.str] = None,
    policy_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
