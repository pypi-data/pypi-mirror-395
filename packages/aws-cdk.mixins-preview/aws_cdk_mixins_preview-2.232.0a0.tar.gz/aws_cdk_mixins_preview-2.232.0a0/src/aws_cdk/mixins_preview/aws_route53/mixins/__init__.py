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
    jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnCidrCollectionMixinProps",
    jsii_struct_bases=[],
    name_mapping={"locations": "locations", "name": "name"},
)
class CfnCidrCollectionMixinProps:
    def __init__(
        self,
        *,
        locations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCidrCollectionPropsMixin.LocationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnCidrCollectionPropsMixin.

        :param locations: A complex type that contains information about the list of CIDR locations.
        :param name: The name of a CIDR collection.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-cidrcollection.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
            
            cfn_cidr_collection_mixin_props = route53_mixins.CfnCidrCollectionMixinProps(
                locations=[route53_mixins.CfnCidrCollectionPropsMixin.LocationProperty(
                    cidr_list=["cidrList"],
                    location_name="locationName"
                )],
                name="name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4381a08c0c2cbcf2d6263120d563a88f6ce9eeb05465b276c02bcda50fa99bc7)
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if locations is not None:
            self._values["locations"] = locations
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def locations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCidrCollectionPropsMixin.LocationProperty"]]]]:
        '''A complex type that contains information about the list of CIDR locations.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-cidrcollection.html#cfn-route53-cidrcollection-locations
        '''
        result = self._values.get("locations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCidrCollectionPropsMixin.LocationProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of a CIDR collection.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-cidrcollection.html#cfn-route53-cidrcollection-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCidrCollectionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCidrCollectionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnCidrCollectionPropsMixin",
):
    '''Creates a CIDR collection in the current AWS account.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-cidrcollection.html
    :cloudformationResource: AWS::Route53::CidrCollection
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
        
        cfn_cidr_collection_props_mixin = route53_mixins.CfnCidrCollectionPropsMixin(route53_mixins.CfnCidrCollectionMixinProps(
            locations=[route53_mixins.CfnCidrCollectionPropsMixin.LocationProperty(
                cidr_list=["cidrList"],
                location_name="locationName"
            )],
            name="name"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCidrCollectionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Route53::CidrCollection``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d7ef7c0909f7a76baf4c350b5b540dbf73e24cb11112c1e927a04aada3e9aa2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf7873af7155301f3d321737d2a088c564272d26b5faaeb8bc197345e2edd004)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0763d2a9c52643604649b2b94695e77c2b05345468a1d229adafe8aee9a9f27)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCidrCollectionMixinProps:
        return typing.cast(CfnCidrCollectionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnCidrCollectionPropsMixin.LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"cidr_list": "cidrList", "location_name": "locationName"},
    )
    class LocationProperty:
        def __init__(
            self,
            *,
            cidr_list: typing.Optional[typing.Sequence[builtins.str]] = None,
            location_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the list of CIDR blocks for a CIDR location.

            :param cidr_list: List of CIDR blocks.
            :param location_name: The CIDR collection location name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-cidrcollection-location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
                
                location_property = route53_mixins.CfnCidrCollectionPropsMixin.LocationProperty(
                    cidr_list=["cidrList"],
                    location_name="locationName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dbda44f4fbecd910d8ec14c6deafee7c1321aebc7765f32ff8052fb7a37cdd71)
                check_type(argname="argument cidr_list", value=cidr_list, expected_type=type_hints["cidr_list"])
                check_type(argname="argument location_name", value=location_name, expected_type=type_hints["location_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cidr_list is not None:
                self._values["cidr_list"] = cidr_list
            if location_name is not None:
                self._values["location_name"] = location_name

        @builtins.property
        def cidr_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of CIDR blocks.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-cidrcollection-location.html#cfn-route53-cidrcollection-location-cidrlist
            '''
            result = self._values.get("cidr_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def location_name(self) -> typing.Optional[builtins.str]:
            '''The CIDR collection location name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-cidrcollection-location.html#cfn-route53-cidrcollection-location-locationname
            '''
            result = self._values.get("location_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnDNSSECMixinProps",
    jsii_struct_bases=[],
    name_mapping={"hosted_zone_id": "hostedZoneId"},
)
class CfnDNSSECMixinProps:
    def __init__(self, *, hosted_zone_id: typing.Optional[builtins.str] = None) -> None:
        '''Properties for CfnDNSSECPropsMixin.

        :param hosted_zone_id: A unique string (ID) that is used to identify a hosted zone. For example: ``Z00001111A1ABCaaABC11`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-dnssec.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
            
            cfn_dNSSECMixin_props = route53_mixins.CfnDNSSECMixinProps(
                hosted_zone_id="hostedZoneId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__425176cad6f995ab72de3220473fa5db98ee4af2f06a9f0a06364abd18502a03)
            check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hosted_zone_id is not None:
            self._values["hosted_zone_id"] = hosted_zone_id

    @builtins.property
    def hosted_zone_id(self) -> typing.Optional[builtins.str]:
        '''A unique string (ID) that is used to identify a hosted zone.

        For example: ``Z00001111A1ABCaaABC11`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-dnssec.html#cfn-route53-dnssec-hostedzoneid
        '''
        result = self._values.get("hosted_zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDNSSECMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDNSSECPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnDNSSECPropsMixin",
):
    '''The ``AWS::Route53::DNSSEC`` resource is used to enable DNSSEC signing in a hosted zone.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-dnssec.html
    :cloudformationResource: AWS::Route53::DNSSEC
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
        
        cfn_dNSSECProps_mixin = route53_mixins.CfnDNSSECPropsMixin(route53_mixins.CfnDNSSECMixinProps(
            hosted_zone_id="hostedZoneId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDNSSECMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Route53::DNSSEC``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60394d48758e93bf095d8ae77ced2e2a573548a57c4a390cd4dd0d399257b72f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4843dc2928483315a98ee581e6b5feb6fdd522f5e165973aa8bfbb95c144a77c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0db8405b923289eb195755211ee77609074348efcf8419ee085e51fc74f182a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDNSSECMixinProps:
        return typing.cast(CfnDNSSECMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnHealthCheckMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "health_check_config": "healthCheckConfig",
        "health_check_tags": "healthCheckTags",
    },
)
class CfnHealthCheckMixinProps:
    def __init__(
        self,
        *,
        health_check_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnHealthCheckPropsMixin.HealthCheckConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        health_check_tags: typing.Optional[typing.Sequence[typing.Union["CfnHealthCheckPropsMixin.HealthCheckTagProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnHealthCheckPropsMixin.

        :param health_check_config: A complex type that contains detailed information about one health check. For the values to enter for ``HealthCheckConfig`` , see `HealthCheckConfig <https://docs.aws.amazon.com/Route53/latest/APIReference/API_HealthCheckConfig.html>`_
        :param health_check_tags: The ``HealthCheckTags`` property describes key-value pairs that are associated with an ``AWS::Route53::HealthCheck`` resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-healthcheck.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
            
            cfn_health_check_mixin_props = route53_mixins.CfnHealthCheckMixinProps(
                health_check_config=route53_mixins.CfnHealthCheckPropsMixin.HealthCheckConfigProperty(
                    alarm_identifier=route53_mixins.CfnHealthCheckPropsMixin.AlarmIdentifierProperty(
                        name="name",
                        region="region"
                    ),
                    child_health_checks=["childHealthChecks"],
                    enable_sni=False,
                    failure_threshold=123,
                    fully_qualified_domain_name="fullyQualifiedDomainName",
                    health_threshold=123,
                    insufficient_data_health_status="insufficientDataHealthStatus",
                    inverted=False,
                    ip_address="ipAddress",
                    measure_latency=False,
                    port=123,
                    regions=["regions"],
                    request_interval=123,
                    resource_path="resourcePath",
                    routing_control_arn="routingControlArn",
                    search_string="searchString",
                    type="type"
                ),
                health_check_tags=[route53_mixins.CfnHealthCheckPropsMixin.HealthCheckTagProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4a98dbd034c669f1992f4f7f6d8770eb3bd4b215690d597b21cd8b06adc5182)
            check_type(argname="argument health_check_config", value=health_check_config, expected_type=type_hints["health_check_config"])
            check_type(argname="argument health_check_tags", value=health_check_tags, expected_type=type_hints["health_check_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if health_check_config is not None:
            self._values["health_check_config"] = health_check_config
        if health_check_tags is not None:
            self._values["health_check_tags"] = health_check_tags

    @builtins.property
    def health_check_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHealthCheckPropsMixin.HealthCheckConfigProperty"]]:
        '''A complex type that contains detailed information about one health check.

        For the values to enter for ``HealthCheckConfig`` , see `HealthCheckConfig <https://docs.aws.amazon.com/Route53/latest/APIReference/API_HealthCheckConfig.html>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-healthcheck.html#cfn-route53-healthcheck-healthcheckconfig
        '''
        result = self._values.get("health_check_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHealthCheckPropsMixin.HealthCheckConfigProperty"]], result)

    @builtins.property
    def health_check_tags(
        self,
    ) -> typing.Optional[typing.List["CfnHealthCheckPropsMixin.HealthCheckTagProperty"]]:
        '''The ``HealthCheckTags`` property describes key-value pairs that are associated with an ``AWS::Route53::HealthCheck`` resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-healthcheck.html#cfn-route53-healthcheck-healthchecktags
        '''
        result = self._values.get("health_check_tags")
        return typing.cast(typing.Optional[typing.List["CfnHealthCheckPropsMixin.HealthCheckTagProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnHealthCheckMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnHealthCheckPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnHealthCheckPropsMixin",
):
    '''The ``AWS::Route53::HealthCheck`` resource is a Route 53 resource type that contains settings for a Route 53 health check.

    For information about associating health checks with records, see `HealthCheckId <https://docs.aws.amazon.com/Route53/latest/APIReference/API_ResourceRecordSet.html#Route53-Type-ResourceRecordSet-HealthCheckId>`_ in `ChangeResourceRecordSets <https://docs.aws.amazon.com/Route53/latest/APIReference/API_ChangeResourceRecordSets.html>`_ .
    .. epigraph::

       You can't create a health check with simple routing.

    *ELB Load Balancers*

    If you're registering EC2 instances with an Elastic Load Balancing (ELB) load balancer, do not create Amazon Route 53 health checks for the EC2 instances. When you register an EC2 instance with a load balancer, you configure settings for an ELB health check, which performs a similar function to a Route 53 health check.

    *Private Hosted Zones*

    You can associate health checks with failover records in a private hosted zone. Note the following:

    - Route 53 health checkers are outside the VPC. To check the health of an endpoint within a VPC by IP address, you must assign a public IP address to the instance in the VPC.
    - You can configure a health checker to check the health of an external resource that the instance relies on, such as a database server.
    - You can create a CloudWatch metric, associate an alarm with the metric, and then create a health check that is based on the state of the alarm. For example, you might create a CloudWatch metric that checks the status of the Amazon EC2 ``StatusCheckFailed`` metric, add an alarm to the metric, and then create a health check that is based on the state of the alarm. For information about creating CloudWatch metrics and alarms by using the CloudWatch console, see the `Amazon CloudWatch User Guide <https://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/WhatIsCloudWatch.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-healthcheck.html
    :cloudformationResource: AWS::Route53::HealthCheck
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
        
        cfn_health_check_props_mixin = route53_mixins.CfnHealthCheckPropsMixin(route53_mixins.CfnHealthCheckMixinProps(
            health_check_config=route53_mixins.CfnHealthCheckPropsMixin.HealthCheckConfigProperty(
                alarm_identifier=route53_mixins.CfnHealthCheckPropsMixin.AlarmIdentifierProperty(
                    name="name",
                    region="region"
                ),
                child_health_checks=["childHealthChecks"],
                enable_sni=False,
                failure_threshold=123,
                fully_qualified_domain_name="fullyQualifiedDomainName",
                health_threshold=123,
                insufficient_data_health_status="insufficientDataHealthStatus",
                inverted=False,
                ip_address="ipAddress",
                measure_latency=False,
                port=123,
                regions=["regions"],
                request_interval=123,
                resource_path="resourcePath",
                routing_control_arn="routingControlArn",
                search_string="searchString",
                type="type"
            ),
            health_check_tags=[route53_mixins.CfnHealthCheckPropsMixin.HealthCheckTagProperty(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnHealthCheckMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Route53::HealthCheck``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__555b39fe277f35258bdc5b71bde824ab20b4a3ab03e585a51b8b9990e008c2b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a839970c929f598c3d0ee493261db550d21a6e3b9d0f9253d76905ac989a5bc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbb3ef4da4583208de571c70ced69e3dac3bb45248c94e9f67588bd1be8a1760)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnHealthCheckMixinProps:
        return typing.cast(CfnHealthCheckMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnHealthCheckPropsMixin.AlarmIdentifierProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "region": "region"},
    )
    class AlarmIdentifierProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A complex type that identifies the CloudWatch alarm that you want Amazon Route 53 health checkers to use to determine whether the specified health check is healthy.

            :param name: The name of the CloudWatch alarm that you want Amazon Route 53 health checkers to use to determine whether this health check is healthy. .. epigraph:: Route 53 supports CloudWatch alarms with the following features: - Standard-resolution metrics. High-resolution metrics aren't supported. For more information, see `High-Resolution Metrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/publishingMetrics.html#high-resolution-metrics>`_ in the *Amazon CloudWatch User Guide* . - Statistics: Average, Minimum, Maximum, Sum, and SampleCount. Extended statistics aren't supported.
            :param region: For the CloudWatch alarm that you want Route 53 health checkers to use to determine whether this health check is healthy, the region that the alarm was created in. For the current list of CloudWatch regions, see `Amazon CloudWatch endpoints and quotas <https://docs.aws.amazon.com/general/latest/gr/cw_region.html>`_ in the *Amazon Web Services General Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-alarmidentifier.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
                
                alarm_identifier_property = route53_mixins.CfnHealthCheckPropsMixin.AlarmIdentifierProperty(
                    name="name",
                    region="region"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6ccc0f3d626755705c5850858a7a5284c21dce6763947a8840b704a126d1e52f)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if region is not None:
                self._values["region"] = region

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the CloudWatch alarm that you want Amazon Route 53 health checkers to use to determine whether this health check is healthy.

            .. epigraph::

               Route 53 supports CloudWatch alarms with the following features:

               - Standard-resolution metrics. High-resolution metrics aren't supported. For more information, see `High-Resolution Metrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/publishingMetrics.html#high-resolution-metrics>`_ in the *Amazon CloudWatch User Guide* .
               - Statistics: Average, Minimum, Maximum, Sum, and SampleCount. Extended statistics aren't supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-alarmidentifier.html#cfn-route53-healthcheck-alarmidentifier-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''For the CloudWatch alarm that you want Route 53 health checkers to use to determine whether this health check is healthy, the region that the alarm was created in.

            For the current list of CloudWatch regions, see `Amazon CloudWatch endpoints and quotas <https://docs.aws.amazon.com/general/latest/gr/cw_region.html>`_ in the *Amazon Web Services General Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-alarmidentifier.html#cfn-route53-healthcheck-alarmidentifier-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmIdentifierProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnHealthCheckPropsMixin.HealthCheckConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alarm_identifier": "alarmIdentifier",
            "child_health_checks": "childHealthChecks",
            "enable_sni": "enableSni",
            "failure_threshold": "failureThreshold",
            "fully_qualified_domain_name": "fullyQualifiedDomainName",
            "health_threshold": "healthThreshold",
            "insufficient_data_health_status": "insufficientDataHealthStatus",
            "inverted": "inverted",
            "ip_address": "ipAddress",
            "measure_latency": "measureLatency",
            "port": "port",
            "regions": "regions",
            "request_interval": "requestInterval",
            "resource_path": "resourcePath",
            "routing_control_arn": "routingControlArn",
            "search_string": "searchString",
            "type": "type",
        },
    )
    class HealthCheckConfigProperty:
        def __init__(
            self,
            *,
            alarm_identifier: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnHealthCheckPropsMixin.AlarmIdentifierProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            child_health_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
            enable_sni: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            failure_threshold: typing.Optional[jsii.Number] = None,
            fully_qualified_domain_name: typing.Optional[builtins.str] = None,
            health_threshold: typing.Optional[jsii.Number] = None,
            insufficient_data_health_status: typing.Optional[builtins.str] = None,
            inverted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            ip_address: typing.Optional[builtins.str] = None,
            measure_latency: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            port: typing.Optional[jsii.Number] = None,
            regions: typing.Optional[typing.Sequence[builtins.str]] = None,
            request_interval: typing.Optional[jsii.Number] = None,
            resource_path: typing.Optional[builtins.str] = None,
            routing_control_arn: typing.Optional[builtins.str] = None,
            search_string: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A complex type that contains information about the health check.

            :param alarm_identifier: A complex type that identifies the CloudWatch alarm that you want Amazon Route 53 health checkers to use to determine whether the specified health check is healthy.
            :param child_health_checks: (CALCULATED Health Checks Only) A complex type that contains one ``ChildHealthCheck`` element for each health check that you want to associate with a ``CALCULATED`` health check.
            :param enable_sni: Specify whether you want Amazon Route 53 to send the value of ``FullyQualifiedDomainName`` to the endpoint in the ``client_hello`` message during TLS negotiation. This allows the endpoint to respond to ``HTTPS`` health check requests with the applicable SSL/TLS certificate. Some endpoints require that ``HTTPS`` requests include the host name in the ``client_hello`` message. If you don't enable SNI, the status of the health check will be ``SSL alert handshake_failure`` . A health check can also have that status for other reasons. If SNI is enabled and you're still getting the error, check the SSL/TLS configuration on your endpoint and confirm that your certificate is valid. The SSL/TLS certificate on your endpoint includes a domain name in the ``Common Name`` field and possibly several more in the ``Subject Alternative Names`` field. One of the domain names in the certificate should match the value that you specify for ``FullyQualifiedDomainName`` . If the endpoint responds to the ``client_hello`` message with a certificate that does not include the domain name that you specified in ``FullyQualifiedDomainName`` , a health checker will retry the handshake. In the second attempt, the health checker will omit ``FullyQualifiedDomainName`` from the ``client_hello`` message.
            :param failure_threshold: The number of consecutive health checks that an endpoint must pass or fail for Amazon Route 53 to change the current status of the endpoint from unhealthy to healthy or vice versa. For more information, see `How Amazon Route 53 Determines Whether an Endpoint Is Healthy <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-determining-health-of-endpoints.html>`_ in the *Amazon Route 53 Developer Guide* . ``FailureThreshold`` is not supported when you specify a value for ``Type`` of ``RECOVERY_CONTROL`` . Otherwise, if you don't specify a value for ``FailureThreshold`` , the default value is three health checks.
            :param fully_qualified_domain_name: Amazon Route 53 behavior depends on whether you specify a value for ``IPAddress`` . *If you specify a value for* ``IPAddress`` : Amazon Route 53 sends health check requests to the specified IPv4 or IPv6 address and passes the value of ``FullyQualifiedDomainName`` in the ``Host`` header for all health checks except TCP health checks. This is typically the fully qualified DNS name of the endpoint on which you want Route 53 to perform health checks. When Route 53 checks the health of an endpoint, here is how it constructs the ``Host`` header: - If you specify a value of ``80`` for ``Port`` and ``HTTP`` or ``HTTP_STR_MATCH`` for ``Type`` , Route 53 passes the value of ``FullyQualifiedDomainName`` to the endpoint in the Host header. - If you specify a value of ``443`` for ``Port`` and ``HTTPS`` or ``HTTPS_STR_MATCH`` for ``Type`` , Route 53 passes the value of ``FullyQualifiedDomainName`` to the endpoint in the ``Host`` header. - If you specify another value for ``Port`` and any value except ``TCP`` for ``Type`` , Route 53 passes ``FullyQualifiedDomainName:Port`` to the endpoint in the ``Host`` header. If you don't specify a value for ``FullyQualifiedDomainName`` , Route 53 substitutes the value of ``IPAddress`` in the ``Host`` header in each of the preceding cases. *If you don't specify a value for ``IPAddress``* : Route 53 sends a DNS request to the domain that you specify for ``FullyQualifiedDomainName`` at the interval that you specify for ``RequestInterval`` . Using an IPv4 address that DNS returns, Route 53 then checks the health of the endpoint. .. epigraph:: If you don't specify a value for ``IPAddress`` , Route 53 uses only IPv4 to send health checks to the endpoint. If there's no record with a type of A for the name that you specify for ``FullyQualifiedDomainName`` , the health check fails with a "DNS resolution failed" error. If you want to check the health of multiple records that have the same name and type, such as multiple weighted records, and if you choose to specify the endpoint only by ``FullyQualifiedDomainName`` , we recommend that you create a separate health check for each endpoint. For example, create a health check for each HTTP server that is serving content for www.example.com. For the value of ``FullyQualifiedDomainName`` , specify the domain name of the server (such as us-east-2-www.example.com), not the name of the records (www.example.com). .. epigraph:: In this configuration, if you create a health check for which the value of ``FullyQualifiedDomainName`` matches the name of the records and you then associate the health check with those records, health check results will be unpredictable. In addition, if the value that you specify for ``Type`` is ``HTTP`` , ``HTTPS`` , ``HTTP_STR_MATCH`` , or ``HTTPS_STR_MATCH`` , Route 53 passes the value of ``FullyQualifiedDomainName`` in the ``Host`` header, as it does when you specify a value for ``IPAddress`` . If the value of ``Type`` is ``TCP`` , Route 53 doesn't pass a ``Host`` header.
            :param health_threshold: The number of child health checks that are associated with a ``CALCULATED`` health check that Amazon Route 53 must consider healthy for the ``CALCULATED`` health check to be considered healthy. To specify the child health checks that you want to associate with a ``CALCULATED`` health check, use the `ChildHealthChecks <https://docs.aws.amazon.com/Route53/latest/APIReference/API_UpdateHealthCheck.html#Route53-UpdateHealthCheck-request-ChildHealthChecks>`_ element. Note the following: - If you specify a number greater than the number of child health checks, Route 53 always considers this health check to be unhealthy. - If you specify ``0`` , Route 53 always considers this health check to be healthy.
            :param insufficient_data_health_status: When CloudWatch has insufficient data about the metric to determine the alarm state, the status that you want Amazon Route 53 to assign to the health check: - ``Healthy`` : Route 53 considers the health check to be healthy. - ``Unhealthy`` : Route 53 considers the health check to be unhealthy. - ``LastKnownStatus`` : Route 53 uses the status of the health check from the last time that CloudWatch had sufficient data to determine the alarm state. For new health checks that have no last known status, the default status for the health check is healthy.
            :param inverted: Specify whether you want Amazon Route 53 to invert the status of a health check, for example, to consider a health check unhealthy when it otherwise would be considered healthy.
            :param ip_address: The IPv4 or IPv6 IP address of the endpoint that you want Amazon Route 53 to perform health checks on. If you don't specify a value for ``IPAddress`` , Route 53 sends a DNS request to resolve the domain name that you specify in ``FullyQualifiedDomainName`` at the interval that you specify in ``RequestInterval`` . Using an IP address returned by DNS, Route 53 then checks the health of the endpoint. Use one of the following formats for the value of ``IPAddress`` : - *IPv4 address* : four values between 0 and 255, separated by periods (.), for example, ``192.0.2.44`` . - *IPv6 address* : eight groups of four hexadecimal values, separated by colons (:), for example, ``2001:0db8:85a3:0000:0000:abcd:0001:2345`` . You can also shorten IPv6 addresses as described in RFC 5952, for example, ``2001:db8:85a3::abcd:1:2345`` . If the endpoint is an EC2 instance, we recommend that you create an Elastic IP address, associate it with your EC2 instance, and specify the Elastic IP address for ``IPAddress`` . This ensures that the IP address of your instance will never change. For more information, see `FullyQualifiedDomainName <https://docs.aws.amazon.com/Route53/latest/APIReference/API_UpdateHealthCheck.html#Route53-UpdateHealthCheck-request-FullyQualifiedDomainName>`_ . Constraints: Route 53 can't check the health of endpoints for which the IP address is in local, private, non-routable, or multicast ranges. For more information about IP addresses for which you can't create health checks, see the following documents: - `RFC 5735, Special Use IPv4 Addresses <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc5735>`_ - `RFC 6598, IANA-Reserved IPv4 Prefix for Shared Address Space <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc6598>`_ - `RFC 5156, Special-Use IPv6 Addresses <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc5156>`_ When the value of ``Type`` is ``CALCULATED`` or ``CLOUDWATCH_METRIC`` , omit ``IPAddress`` .
            :param measure_latency: Specify whether you want Amazon Route 53 to measure the latency between health checkers in multiple AWS regions and your endpoint, and to display CloudWatch latency graphs on the *Health Checks* page in the Route 53 console. ``MeasureLatency`` is not supported when you specify a value for ``Type`` of ``RECOVERY_CONTROL`` . .. epigraph:: You can't change the value of ``MeasureLatency`` after you create a health check.
            :param port: The port on the endpoint that you want Amazon Route 53 to perform health checks on. .. epigraph:: Don't specify a value for ``Port`` when you specify a value for `Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-type>`_ of ``CLOUDWATCH_METRIC`` or ``CALCULATED`` .
            :param regions: A complex type that contains one ``Region`` element for each region from which you want Amazon Route 53 health checkers to check the specified endpoint. If you don't specify any regions, Route 53 health checkers automatically performs checks from all of the regions that are listed under *Valid Values* . If you update a health check to remove a region that has been performing health checks, Route 53 will briefly continue to perform checks from that region to ensure that some health checkers are always checking the endpoint (for example, if you replace three regions with four different regions).
            :param request_interval: The number of seconds between the time that Amazon Route 53 gets a response from your endpoint and the time that it sends the next health check request. Each Route 53 health checker makes requests at this interval. ``RequestInterval`` is not supported when you specify a value for ``Type`` of ``RECOVERY_CONTROL`` . .. epigraph:: You can't change the value of ``RequestInterval`` after you create a health check. If you don't specify a value for ``RequestInterval`` , the default value is ``30`` seconds.
            :param resource_path: The path, if any, that you want Amazon Route 53 to request when performing health checks. The path can be any value for which your endpoint will return an HTTP status code of 2xx or 3xx when the endpoint is healthy, for example, the file /docs/route53-health-check.html. You can also include query string parameters, for example, ``/welcome.html?language=jp&login=y`` .
            :param routing_control_arn: The Amazon Resource Name (ARN) for the Route 53 Application Recovery Controller routing control. For more information about Route 53 Application Recovery Controller, see `Route 53 Application Recovery Controller Developer Guide. <https://docs.aws.amazon.com/r53recovery/latest/dg/what-is-route-53-recovery.html>`_ .
            :param search_string: If the value of Type is ``HTTP_STR_MATCH`` or ``HTTPS_STR_MATCH`` , the string that you want Amazon Route 53 to search for in the response body from the specified resource. If the string appears in the response body, Route 53 considers the resource healthy. Route 53 considers case when searching for ``SearchString`` in the response body.
            :param type: The type of health check that you want to create, which indicates how Amazon Route 53 determines whether an endpoint is healthy. .. epigraph:: You can't change the value of ``Type`` after you create a health check. You can create the following types of health checks: - *HTTP* : Route 53 tries to establish a TCP connection. If successful, Route 53 submits an HTTP request and waits for an HTTP status code of 200 or greater and less than 400. - *HTTPS* : Route 53 tries to establish a TCP connection. If successful, Route 53 submits an HTTPS request and waits for an HTTP status code of 200 or greater and less than 400. .. epigraph:: If you specify ``HTTPS`` for the value of ``Type`` , the endpoint must support TLS v1.0 or later. - *HTTP_STR_MATCH* : Route 53 tries to establish a TCP connection. If successful, Route 53 submits an HTTP request and searches the first 5,120 bytes of the response body for the string that you specify in ``SearchString`` . - *HTTPS_STR_MATCH* : Route 53 tries to establish a TCP connection. If successful, Route 53 submits an ``HTTPS`` request and searches the first 5,120 bytes of the response body for the string that you specify in ``SearchString`` . - *TCP* : Route 53 tries to establish a TCP connection. - *CLOUDWATCH_METRIC* : The health check is associated with a CloudWatch alarm. If the state of the alarm is ``OK`` , the health check is considered healthy. If the state is ``ALARM`` , the health check is considered unhealthy. If CloudWatch doesn't have sufficient data to determine whether the state is ``OK`` or ``ALARM`` , the health check status depends on the setting for ``InsufficientDataHealthStatus`` : ``Healthy`` , ``Unhealthy`` , or ``LastKnownStatus`` . .. epigraph:: Route 53 supports CloudWatch alarms with the following features: - Standard-resolution metrics. High-resolution metrics aren't supported. For more information, see `High-Resolution Metrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/publishingMetrics.html#high-resolution-metrics>`_ in the *Amazon CloudWatch User Guide* . - Statistics: Average, Minimum, Maximum, Sum, and SampleCount. Extended statistics aren't supported. - *CALCULATED* : For health checks that monitor the status of other health checks, Route 53 adds up the number of health checks that Route 53 health checkers consider to be healthy and compares that number with the value of ``HealthThreshold`` . - *RECOVERY_CONTROL* : The health check is assocated with a Route53 Application Recovery Controller routing control. If the routing control state is ``ON`` , the health check is considered healthy. If the state is ``OFF`` , the health check is considered unhealthy. For more information, see `How Route 53 Determines Whether an Endpoint Is Healthy <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-determining-health-of-endpoints.html>`_ in the *Amazon Route 53 Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
                
                health_check_config_property = route53_mixins.CfnHealthCheckPropsMixin.HealthCheckConfigProperty(
                    alarm_identifier=route53_mixins.CfnHealthCheckPropsMixin.AlarmIdentifierProperty(
                        name="name",
                        region="region"
                    ),
                    child_health_checks=["childHealthChecks"],
                    enable_sni=False,
                    failure_threshold=123,
                    fully_qualified_domain_name="fullyQualifiedDomainName",
                    health_threshold=123,
                    insufficient_data_health_status="insufficientDataHealthStatus",
                    inverted=False,
                    ip_address="ipAddress",
                    measure_latency=False,
                    port=123,
                    regions=["regions"],
                    request_interval=123,
                    resource_path="resourcePath",
                    routing_control_arn="routingControlArn",
                    search_string="searchString",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e6f910ae03cedb36dad31b9de48f3366d4769842f256dfc22b311465116d076d)
                check_type(argname="argument alarm_identifier", value=alarm_identifier, expected_type=type_hints["alarm_identifier"])
                check_type(argname="argument child_health_checks", value=child_health_checks, expected_type=type_hints["child_health_checks"])
                check_type(argname="argument enable_sni", value=enable_sni, expected_type=type_hints["enable_sni"])
                check_type(argname="argument failure_threshold", value=failure_threshold, expected_type=type_hints["failure_threshold"])
                check_type(argname="argument fully_qualified_domain_name", value=fully_qualified_domain_name, expected_type=type_hints["fully_qualified_domain_name"])
                check_type(argname="argument health_threshold", value=health_threshold, expected_type=type_hints["health_threshold"])
                check_type(argname="argument insufficient_data_health_status", value=insufficient_data_health_status, expected_type=type_hints["insufficient_data_health_status"])
                check_type(argname="argument inverted", value=inverted, expected_type=type_hints["inverted"])
                check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
                check_type(argname="argument measure_latency", value=measure_latency, expected_type=type_hints["measure_latency"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
                check_type(argname="argument request_interval", value=request_interval, expected_type=type_hints["request_interval"])
                check_type(argname="argument resource_path", value=resource_path, expected_type=type_hints["resource_path"])
                check_type(argname="argument routing_control_arn", value=routing_control_arn, expected_type=type_hints["routing_control_arn"])
                check_type(argname="argument search_string", value=search_string, expected_type=type_hints["search_string"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alarm_identifier is not None:
                self._values["alarm_identifier"] = alarm_identifier
            if child_health_checks is not None:
                self._values["child_health_checks"] = child_health_checks
            if enable_sni is not None:
                self._values["enable_sni"] = enable_sni
            if failure_threshold is not None:
                self._values["failure_threshold"] = failure_threshold
            if fully_qualified_domain_name is not None:
                self._values["fully_qualified_domain_name"] = fully_qualified_domain_name
            if health_threshold is not None:
                self._values["health_threshold"] = health_threshold
            if insufficient_data_health_status is not None:
                self._values["insufficient_data_health_status"] = insufficient_data_health_status
            if inverted is not None:
                self._values["inverted"] = inverted
            if ip_address is not None:
                self._values["ip_address"] = ip_address
            if measure_latency is not None:
                self._values["measure_latency"] = measure_latency
            if port is not None:
                self._values["port"] = port
            if regions is not None:
                self._values["regions"] = regions
            if request_interval is not None:
                self._values["request_interval"] = request_interval
            if resource_path is not None:
                self._values["resource_path"] = resource_path
            if routing_control_arn is not None:
                self._values["routing_control_arn"] = routing_control_arn
            if search_string is not None:
                self._values["search_string"] = search_string
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def alarm_identifier(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHealthCheckPropsMixin.AlarmIdentifierProperty"]]:
            '''A complex type that identifies the CloudWatch alarm that you want Amazon Route 53 health checkers to use to determine whether the specified health check is healthy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-alarmidentifier
            '''
            result = self._values.get("alarm_identifier")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHealthCheckPropsMixin.AlarmIdentifierProperty"]], result)

        @builtins.property
        def child_health_checks(self) -> typing.Optional[typing.List[builtins.str]]:
            '''(CALCULATED Health Checks Only) A complex type that contains one ``ChildHealthCheck`` element for each health check that you want to associate with a ``CALCULATED`` health check.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-childhealthchecks
            '''
            result = self._values.get("child_health_checks")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def enable_sni(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specify whether you want Amazon Route 53 to send the value of ``FullyQualifiedDomainName`` to the endpoint in the ``client_hello`` message during TLS negotiation.

            This allows the endpoint to respond to ``HTTPS`` health check requests with the applicable SSL/TLS certificate.

            Some endpoints require that ``HTTPS`` requests include the host name in the ``client_hello`` message. If you don't enable SNI, the status of the health check will be ``SSL alert handshake_failure`` . A health check can also have that status for other reasons. If SNI is enabled and you're still getting the error, check the SSL/TLS configuration on your endpoint and confirm that your certificate is valid.

            The SSL/TLS certificate on your endpoint includes a domain name in the ``Common Name`` field and possibly several more in the ``Subject Alternative Names`` field. One of the domain names in the certificate should match the value that you specify for ``FullyQualifiedDomainName`` . If the endpoint responds to the ``client_hello`` message with a certificate that does not include the domain name that you specified in ``FullyQualifiedDomainName`` , a health checker will retry the handshake. In the second attempt, the health checker will omit ``FullyQualifiedDomainName`` from the ``client_hello`` message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-enablesni
            '''
            result = self._values.get("enable_sni")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def failure_threshold(self) -> typing.Optional[jsii.Number]:
            '''The number of consecutive health checks that an endpoint must pass or fail for Amazon Route 53 to change the current status of the endpoint from unhealthy to healthy or vice versa.

            For more information, see `How Amazon Route 53 Determines Whether an Endpoint Is Healthy <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-determining-health-of-endpoints.html>`_ in the *Amazon Route 53 Developer Guide* .

            ``FailureThreshold`` is not supported when you specify a value for ``Type`` of ``RECOVERY_CONTROL`` .

            Otherwise, if you don't specify a value for ``FailureThreshold`` , the default value is three health checks.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-failurethreshold
            '''
            result = self._values.get("failure_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def fully_qualified_domain_name(self) -> typing.Optional[builtins.str]:
            '''Amazon Route 53 behavior depends on whether you specify a value for ``IPAddress`` .

            *If you specify a value for* ``IPAddress`` :

            Amazon Route 53 sends health check requests to the specified IPv4 or IPv6 address and passes the value of ``FullyQualifiedDomainName`` in the ``Host`` header for all health checks except TCP health checks. This is typically the fully qualified DNS name of the endpoint on which you want Route 53 to perform health checks.

            When Route 53 checks the health of an endpoint, here is how it constructs the ``Host`` header:

            - If you specify a value of ``80`` for ``Port`` and ``HTTP`` or ``HTTP_STR_MATCH`` for ``Type`` , Route 53 passes the value of ``FullyQualifiedDomainName`` to the endpoint in the Host header.
            - If you specify a value of ``443`` for ``Port`` and ``HTTPS`` or ``HTTPS_STR_MATCH`` for ``Type`` , Route 53 passes the value of ``FullyQualifiedDomainName`` to the endpoint in the ``Host`` header.
            - If you specify another value for ``Port`` and any value except ``TCP`` for ``Type`` , Route 53 passes ``FullyQualifiedDomainName:Port`` to the endpoint in the ``Host`` header.

            If you don't specify a value for ``FullyQualifiedDomainName`` , Route 53 substitutes the value of ``IPAddress`` in the ``Host`` header in each of the preceding cases.

            *If you don't specify a value for ``IPAddress``* :

            Route 53 sends a DNS request to the domain that you specify for ``FullyQualifiedDomainName`` at the interval that you specify for ``RequestInterval`` . Using an IPv4 address that DNS returns, Route 53 then checks the health of the endpoint.
            .. epigraph::

               If you don't specify a value for ``IPAddress`` , Route 53 uses only IPv4 to send health checks to the endpoint. If there's no record with a type of A for the name that you specify for ``FullyQualifiedDomainName`` , the health check fails with a "DNS resolution failed" error.

            If you want to check the health of multiple records that have the same name and type, such as multiple weighted records, and if you choose to specify the endpoint only by ``FullyQualifiedDomainName`` , we recommend that you create a separate health check for each endpoint. For example, create a health check for each HTTP server that is serving content for www.example.com. For the value of ``FullyQualifiedDomainName`` , specify the domain name of the server (such as us-east-2-www.example.com), not the name of the records (www.example.com).
            .. epigraph::

               In this configuration, if you create a health check for which the value of ``FullyQualifiedDomainName`` matches the name of the records and you then associate the health check with those records, health check results will be unpredictable.

            In addition, if the value that you specify for ``Type`` is ``HTTP`` , ``HTTPS`` , ``HTTP_STR_MATCH`` , or ``HTTPS_STR_MATCH`` , Route 53 passes the value of ``FullyQualifiedDomainName`` in the ``Host`` header, as it does when you specify a value for ``IPAddress`` . If the value of ``Type`` is ``TCP`` , Route 53 doesn't pass a ``Host`` header.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-fullyqualifieddomainname
            '''
            result = self._values.get("fully_qualified_domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def health_threshold(self) -> typing.Optional[jsii.Number]:
            '''The number of child health checks that are associated with a ``CALCULATED`` health check that Amazon Route 53 must consider healthy for the ``CALCULATED`` health check to be considered healthy.

            To specify the child health checks that you want to associate with a ``CALCULATED`` health check, use the `ChildHealthChecks <https://docs.aws.amazon.com/Route53/latest/APIReference/API_UpdateHealthCheck.html#Route53-UpdateHealthCheck-request-ChildHealthChecks>`_ element.

            Note the following:

            - If you specify a number greater than the number of child health checks, Route 53 always considers this health check to be unhealthy.
            - If you specify ``0`` , Route 53 always considers this health check to be healthy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-healththreshold
            '''
            result = self._values.get("health_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def insufficient_data_health_status(self) -> typing.Optional[builtins.str]:
            '''When CloudWatch has insufficient data about the metric to determine the alarm state, the status that you want Amazon Route 53 to assign to the health check:  - ``Healthy`` : Route 53 considers the health check to be healthy.

            - ``Unhealthy`` : Route 53 considers the health check to be unhealthy.
            - ``LastKnownStatus`` : Route 53 uses the status of the health check from the last time that CloudWatch had sufficient data to determine the alarm state. For new health checks that have no last known status, the default status for the health check is healthy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-insufficientdatahealthstatus
            '''
            result = self._values.get("insufficient_data_health_status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def inverted(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specify whether you want Amazon Route 53 to invert the status of a health check, for example, to consider a health check unhealthy when it otherwise would be considered healthy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-inverted
            '''
            result = self._values.get("inverted")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def ip_address(self) -> typing.Optional[builtins.str]:
            '''The IPv4 or IPv6 IP address of the endpoint that you want Amazon Route 53 to perform health checks on.

            If you don't specify a value for ``IPAddress`` , Route 53 sends a DNS request to resolve the domain name that you specify in ``FullyQualifiedDomainName`` at the interval that you specify in ``RequestInterval`` . Using an IP address returned by DNS, Route 53 then checks the health of the endpoint.

            Use one of the following formats for the value of ``IPAddress`` :

            - *IPv4 address* : four values between 0 and 255, separated by periods (.), for example, ``192.0.2.44`` .
            - *IPv6 address* : eight groups of four hexadecimal values, separated by colons (:), for example, ``2001:0db8:85a3:0000:0000:abcd:0001:2345`` . You can also shorten IPv6 addresses as described in RFC 5952, for example, ``2001:db8:85a3::abcd:1:2345`` .

            If the endpoint is an EC2 instance, we recommend that you create an Elastic IP address, associate it with your EC2 instance, and specify the Elastic IP address for ``IPAddress`` . This ensures that the IP address of your instance will never change.

            For more information, see `FullyQualifiedDomainName <https://docs.aws.amazon.com/Route53/latest/APIReference/API_UpdateHealthCheck.html#Route53-UpdateHealthCheck-request-FullyQualifiedDomainName>`_ .

            Constraints: Route 53 can't check the health of endpoints for which the IP address is in local, private, non-routable, or multicast ranges. For more information about IP addresses for which you can't create health checks, see the following documents:

            - `RFC 5735, Special Use IPv4 Addresses <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc5735>`_
            - `RFC 6598, IANA-Reserved IPv4 Prefix for Shared Address Space <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc6598>`_
            - `RFC 5156, Special-Use IPv6 Addresses <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc5156>`_

            When the value of ``Type`` is ``CALCULATED`` or ``CLOUDWATCH_METRIC`` , omit ``IPAddress`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-ipaddress
            '''
            result = self._values.get("ip_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def measure_latency(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specify whether you want Amazon Route 53 to measure the latency between health checkers in multiple AWS regions and your endpoint, and to display CloudWatch latency graphs on the *Health Checks* page in the Route 53 console.

            ``MeasureLatency`` is not supported when you specify a value for ``Type`` of ``RECOVERY_CONTROL`` .
            .. epigraph::

               You can't change the value of ``MeasureLatency`` after you create a health check.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-measurelatency
            '''
            result = self._values.get("measure_latency")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port on the endpoint that you want Amazon Route 53 to perform health checks on.

            .. epigraph::

               Don't specify a value for ``Port`` when you specify a value for `Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-type>`_ of ``CLOUDWATCH_METRIC`` or ``CALCULATED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def regions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A complex type that contains one ``Region`` element for each region from which you want Amazon Route 53 health checkers to check the specified endpoint.

            If you don't specify any regions, Route 53 health checkers automatically performs checks from all of the regions that are listed under *Valid Values* .

            If you update a health check to remove a region that has been performing health checks, Route 53 will briefly continue to perform checks from that region to ensure that some health checkers are always checking the endpoint (for example, if you replace three regions with four different regions).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-regions
            '''
            result = self._values.get("regions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def request_interval(self) -> typing.Optional[jsii.Number]:
            '''The number of seconds between the time that Amazon Route 53 gets a response from your endpoint and the time that it sends the next health check request.

            Each Route 53 health checker makes requests at this interval.

            ``RequestInterval`` is not supported when you specify a value for ``Type`` of ``RECOVERY_CONTROL`` .
            .. epigraph::

               You can't change the value of ``RequestInterval`` after you create a health check.

            If you don't specify a value for ``RequestInterval`` , the default value is ``30`` seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-requestinterval
            '''
            result = self._values.get("request_interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def resource_path(self) -> typing.Optional[builtins.str]:
            '''The path, if any, that you want Amazon Route 53 to request when performing health checks.

            The path can be any value for which your endpoint will return an HTTP status code of 2xx or 3xx when the endpoint is healthy, for example, the file /docs/route53-health-check.html. You can also include query string parameters, for example, ``/welcome.html?language=jp&login=y`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-resourcepath
            '''
            result = self._values.get("resource_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def routing_control_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the Route 53 Application Recovery Controller routing control.

            For more information about Route 53 Application Recovery Controller, see `Route 53 Application Recovery Controller Developer Guide. <https://docs.aws.amazon.com/r53recovery/latest/dg/what-is-route-53-recovery.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-routingcontrolarn
            '''
            result = self._values.get("routing_control_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def search_string(self) -> typing.Optional[builtins.str]:
            '''If the value of Type is ``HTTP_STR_MATCH`` or ``HTTPS_STR_MATCH`` , the string that you want Amazon Route 53 to search for in the response body from the specified resource.

            If the string appears in the response body, Route 53 considers the resource healthy.

            Route 53 considers case when searching for ``SearchString`` in the response body.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-searchstring
            '''
            result = self._values.get("search_string")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of health check that you want to create, which indicates how Amazon Route 53 determines whether an endpoint is healthy.

            .. epigraph::

               You can't change the value of ``Type`` after you create a health check.

            You can create the following types of health checks:

            - *HTTP* : Route 53 tries to establish a TCP connection. If successful, Route 53 submits an HTTP request and waits for an HTTP status code of 200 or greater and less than 400.
            - *HTTPS* : Route 53 tries to establish a TCP connection. If successful, Route 53 submits an HTTPS request and waits for an HTTP status code of 200 or greater and less than 400.

            .. epigraph::

               If you specify ``HTTPS`` for the value of ``Type`` , the endpoint must support TLS v1.0 or later.

            - *HTTP_STR_MATCH* : Route 53 tries to establish a TCP connection. If successful, Route 53 submits an HTTP request and searches the first 5,120 bytes of the response body for the string that you specify in ``SearchString`` .
            - *HTTPS_STR_MATCH* : Route 53 tries to establish a TCP connection. If successful, Route 53 submits an ``HTTPS`` request and searches the first 5,120 bytes of the response body for the string that you specify in ``SearchString`` .
            - *TCP* : Route 53 tries to establish a TCP connection.
            - *CLOUDWATCH_METRIC* : The health check is associated with a CloudWatch alarm. If the state of the alarm is ``OK`` , the health check is considered healthy. If the state is ``ALARM`` , the health check is considered unhealthy. If CloudWatch doesn't have sufficient data to determine whether the state is ``OK`` or ``ALARM`` , the health check status depends on the setting for ``InsufficientDataHealthStatus`` : ``Healthy`` , ``Unhealthy`` , or ``LastKnownStatus`` .

            .. epigraph::

               Route 53 supports CloudWatch alarms with the following features:

               - Standard-resolution metrics. High-resolution metrics aren't supported. For more information, see `High-Resolution Metrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/publishingMetrics.html#high-resolution-metrics>`_ in the *Amazon CloudWatch User Guide* .
               - Statistics: Average, Minimum, Maximum, Sum, and SampleCount. Extended statistics aren't supported.

            - *CALCULATED* : For health checks that monitor the status of other health checks, Route 53 adds up the number of health checks that Route 53 health checkers consider to be healthy and compares that number with the value of ``HealthThreshold`` .
            - *RECOVERY_CONTROL* : The health check is assocated with a Route53 Application Recovery Controller routing control. If the routing control state is ``ON`` , the health check is considered healthy. If the state is ``OFF`` , the health check is considered unhealthy.

            For more information, see `How Route 53 Determines Whether an Endpoint Is Healthy <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-determining-health-of-endpoints.html>`_ in the *Amazon Route 53 Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-type
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
        jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnHealthCheckPropsMixin.HealthCheckTagProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class HealthCheckTagProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``HealthCheckTag`` property describes one key-value pair that is associated with an ``AWS::Route53::HealthCheck`` resource.

            :param key: The value of ``Key`` depends on the operation that you want to perform:. - *Add a tag to a health check or hosted zone* : ``Key`` is the name that you want to give the new tag. - *Edit a tag* : ``Key`` is the name of the tag that you want to change the ``Value`` for. - *Delete a key* : ``Key`` is the name of the tag you want to remove. - *Give a name to a health check* : Edit the default ``Name`` tag. In the Amazon Route 53 console, the list of your health checks includes a *Name* column that lets you see the name that you've given to each health check.
            :param value: The value of ``Value`` depends on the operation that you want to perform:. - *Add a tag to a health check or hosted zone* : ``Value`` is the value that you want to give the new tag. - *Edit a tag* : ``Value`` is the new value that you want to assign the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthchecktag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
                
                health_check_tag_property = route53_mixins.CfnHealthCheckPropsMixin.HealthCheckTagProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__515d044b538e4e93885694d595a95bc9de92eb535fdd0d613727cfe7b1a427eb)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The value of ``Key`` depends on the operation that you want to perform:.

            - *Add a tag to a health check or hosted zone* : ``Key`` is the name that you want to give the new tag.
            - *Edit a tag* : ``Key`` is the name of the tag that you want to change the ``Value`` for.
            - *Delete a key* : ``Key`` is the name of the tag you want to remove.
            - *Give a name to a health check* : Edit the default ``Name`` tag. In the Amazon Route 53 console, the list of your health checks includes a *Name* column that lets you see the name that you've given to each health check.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthchecktag.html#cfn-route53-healthcheck-healthchecktag-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of ``Value`` depends on the operation that you want to perform:.

            - *Add a tag to a health check or hosted zone* : ``Value`` is the value that you want to give the new tag.
            - *Edit a tag* : ``Value`` is the new value that you want to assign the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthchecktag.html#cfn-route53-healthcheck-healthchecktag-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HealthCheckTagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnHostedZoneMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "hosted_zone_config": "hostedZoneConfig",
        "hosted_zone_tags": "hostedZoneTags",
        "name": "name",
        "query_logging_config": "queryLoggingConfig",
        "vpcs": "vpcs",
    },
)
class CfnHostedZoneMixinProps:
    def __init__(
        self,
        *,
        hosted_zone_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnHostedZonePropsMixin.HostedZoneConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        hosted_zone_tags: typing.Optional[typing.Sequence[typing.Union["CfnHostedZonePropsMixin.HostedZoneTagProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        query_logging_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnHostedZonePropsMixin.QueryLoggingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        vpcs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnHostedZonePropsMixin.VPCProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnHostedZonePropsMixin.

        :param hosted_zone_config: A complex type that contains an optional comment. If you don't want to specify a comment, omit the ``HostedZoneConfig`` and ``Comment`` elements.
        :param hosted_zone_tags: Adds, edits, or deletes tags for a health check or a hosted zone. For information about using tags for cost allocation, see `Using Cost Allocation Tags <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html>`_ in the *Billing and Cost Management User Guide* .
        :param name: The name of the domain. Specify a fully qualified domain name, for example, *www.example.com* . The trailing dot is optional; Amazon Route 53 assumes that the domain name is fully qualified. This means that Route 53 treats *www.example.com* (without a trailing dot) and *www.example.com.* (with a trailing dot) as identical. If you're creating a public hosted zone, this is the name you have registered with your DNS registrar. If your domain name is registered with a registrar other than Route 53, change the name servers for your domain to the set of ``NameServers`` that are returned by the ``Fn::GetAtt`` intrinsic function.
        :param query_logging_config: Creates a configuration for DNS query logging. After you create a query logging configuration, Amazon Route 53 begins to publish log data to an Amazon CloudWatch Logs log group. DNS query logs contain information about the queries that Route 53 receives for a specified public hosted zone, such as the following: - Route 53 edge location that responded to the DNS query - Domain or subdomain that was requested - DNS record type, such as A or AAAA - DNS response code, such as ``NoError`` or ``ServFail`` - **Log Group and Resource Policy** - Before you create a query logging configuration, perform the following operations. .. epigraph:: If you create a query logging configuration using the Route 53 console, Route 53 performs these operations automatically. - Create a CloudWatch Logs log group, and make note of the ARN, which you specify when you create a query logging configuration. Note the following: - You must create the log group in the us-east-1 region. - You must use the same AWS account to create the log group and the hosted zone that you want to configure query logging for. - When you create log groups for query logging, we recommend that you use a consistent prefix, for example: ``/aws/route53/ *hosted zone name*`` In the next step, you'll create a resource policy, which controls access to one or more log groups and the associated AWS resources, such as Route 53 hosted zones. There's a limit on the number of resource policies that you can create, so we recommend that you use a consistent prefix so you can use the same resource policy for all the log groups that you create for query logging. - Create a CloudWatch Logs resource policy, and give it the permissions that Route 53 needs to create log streams and to send query logs to log streams. You must create the CloudWatch Logs resource policy in the us-east-1 region. For the value of ``Resource`` , specify the ARN for the log group that you created in the previous step. To use the same resource policy for all the CloudWatch Logs log groups that you created for query logging configurations, replace the hosted zone name with ``*`` , for example: ``arn:aws:logs:us-east-1:123412341234:log-group:/aws/route53/*`` To avoid the confused deputy problem, a security issue where an entity without a permission for an action can coerce a more-privileged entity to perform it, you can optionally limit the permissions that a service has to a resource in a resource-based policy by supplying the following values: - For ``aws:SourceArn`` , supply the hosted zone ARN used in creating the query logging configuration. For example, ``aws:SourceArn: arn:aws:route53:::hostedzone/hosted zone ID`` . - For ``aws:SourceAccount`` , supply the account ID for the account that creates the query logging configuration. For example, ``aws:SourceAccount:111111111111`` . For more information, see `The confused deputy problem <https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html>`_ in the *AWS IAM User Guide* . .. epigraph:: You can't use the CloudWatch console to create or edit a resource policy. You must use the CloudWatch API, one of the AWS SDKs, or the AWS CLI . - **Log Streams and Edge Locations** - When Route 53 finishes creating the configuration for DNS query logging, it does the following: - Creates a log stream for an edge location the first time that the edge location responds to DNS queries for the specified hosted zone. That log stream is used to log all queries that Route 53 responds to for that edge location. - Begins to send query logs to the applicable log stream. The name of each log stream is in the following format: ``*hosted zone ID* / *edge location code*`` The edge location code is a three-letter code and an arbitrarily assigned number, for example, DFW3. The three-letter code typically corresponds with the International Air Transport Association airport code for an airport near the edge location. (These abbreviations might change in the future.) For a list of edge locations, see "The Route 53 Global Network" on the `Route 53 Product Details <https://docs.aws.amazon.com/route53/details/>`_ page. - **Queries That Are Logged** - Query logs contain only the queries that DNS resolvers forward to Route 53. If a DNS resolver has already cached the response to a query (such as the IP address for a load balancer for example.com), the resolver will continue to return the cached response. It doesn't forward another query to Route 53 until the TTL for the corresponding resource record set expires. Depending on how many DNS queries are submitted for a resource record set, and depending on the TTL for that resource record set, query logs might contain information about only one query out of every several thousand queries that are submitted to DNS. For more information about how DNS works, see `Routing Internet Traffic to Your Website or Web Application <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/welcome-dns-service.html>`_ in the *Amazon Route 53 Developer Guide* . - **Log File Format** - For a list of the values in each query log and the format of each value, see `Logging DNS Queries <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/query-logs.html>`_ in the *Amazon Route 53 Developer Guide* . - **Pricing** - For information about charges for query logs, see `Amazon CloudWatch Pricing <https://docs.aws.amazon.com/cloudwatch/pricing/>`_ . - **How to Stop Logging** - If you want Route 53 to stop sending query logs to CloudWatch Logs, delete the query logging configuration. For more information, see `DeleteQueryLoggingConfig <https://docs.aws.amazon.com/Route53/latest/APIReference/API_DeleteQueryLoggingConfig.html>`_ .
        :param vpcs: *Private hosted zones:* A complex type that contains information about the VPCs that are associated with the specified hosted zone. .. epigraph:: For public hosted zones, omit ``VPCs`` , ``VPCId`` , and ``VPCRegion`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
            
            cfn_hosted_zone_mixin_props = route53_mixins.CfnHostedZoneMixinProps(
                hosted_zone_config=route53_mixins.CfnHostedZonePropsMixin.HostedZoneConfigProperty(
                    comment="comment"
                ),
                hosted_zone_tags=[route53_mixins.CfnHostedZonePropsMixin.HostedZoneTagProperty(
                    key="key",
                    value="value"
                )],
                name="name",
                query_logging_config=route53_mixins.CfnHostedZonePropsMixin.QueryLoggingConfigProperty(
                    cloud_watch_logs_log_group_arn="cloudWatchLogsLogGroupArn"
                ),
                vpcs=[route53_mixins.CfnHostedZonePropsMixin.VPCProperty(
                    vpc_id="vpcId",
                    vpc_region="vpcRegion"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1274c4e119a5111943c7c474fe81217deb26720caef2693a3eaf4bb3f961cdba)
            check_type(argname="argument hosted_zone_config", value=hosted_zone_config, expected_type=type_hints["hosted_zone_config"])
            check_type(argname="argument hosted_zone_tags", value=hosted_zone_tags, expected_type=type_hints["hosted_zone_tags"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument query_logging_config", value=query_logging_config, expected_type=type_hints["query_logging_config"])
            check_type(argname="argument vpcs", value=vpcs, expected_type=type_hints["vpcs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hosted_zone_config is not None:
            self._values["hosted_zone_config"] = hosted_zone_config
        if hosted_zone_tags is not None:
            self._values["hosted_zone_tags"] = hosted_zone_tags
        if name is not None:
            self._values["name"] = name
        if query_logging_config is not None:
            self._values["query_logging_config"] = query_logging_config
        if vpcs is not None:
            self._values["vpcs"] = vpcs

    @builtins.property
    def hosted_zone_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHostedZonePropsMixin.HostedZoneConfigProperty"]]:
        '''A complex type that contains an optional comment.

        If you don't want to specify a comment, omit the ``HostedZoneConfig`` and ``Comment`` elements.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html#cfn-route53-hostedzone-hostedzoneconfig
        '''
        result = self._values.get("hosted_zone_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHostedZonePropsMixin.HostedZoneConfigProperty"]], result)

    @builtins.property
    def hosted_zone_tags(
        self,
    ) -> typing.Optional[typing.List["CfnHostedZonePropsMixin.HostedZoneTagProperty"]]:
        '''Adds, edits, or deletes tags for a health check or a hosted zone.

        For information about using tags for cost allocation, see `Using Cost Allocation Tags <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html>`_ in the *Billing and Cost Management User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html#cfn-route53-hostedzone-hostedzonetags
        '''
        result = self._values.get("hosted_zone_tags")
        return typing.cast(typing.Optional[typing.List["CfnHostedZonePropsMixin.HostedZoneTagProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the domain.

        Specify a fully qualified domain name, for example, *www.example.com* . The trailing dot is optional; Amazon Route 53 assumes that the domain name is fully qualified. This means that Route 53 treats *www.example.com* (without a trailing dot) and *www.example.com.* (with a trailing dot) as identical.

        If you're creating a public hosted zone, this is the name you have registered with your DNS registrar. If your domain name is registered with a registrar other than Route 53, change the name servers for your domain to the set of ``NameServers`` that are returned by the ``Fn::GetAtt`` intrinsic function.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html#cfn-route53-hostedzone-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_logging_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHostedZonePropsMixin.QueryLoggingConfigProperty"]]:
        '''Creates a configuration for DNS query logging.

        After you create a query logging configuration, Amazon Route 53 begins to publish log data to an Amazon CloudWatch Logs log group.

        DNS query logs contain information about the queries that Route 53 receives for a specified public hosted zone, such as the following:

        - Route 53 edge location that responded to the DNS query
        - Domain or subdomain that was requested
        - DNS record type, such as A or AAAA
        - DNS response code, such as ``NoError`` or ``ServFail``
        - **Log Group and Resource Policy** - Before you create a query logging configuration, perform the following operations.

        .. epigraph::

           If you create a query logging configuration using the Route 53 console, Route 53 performs these operations automatically.

        - Create a CloudWatch Logs log group, and make note of the ARN, which you specify when you create a query logging configuration. Note the following:
        - You must create the log group in the us-east-1 region.
        - You must use the same AWS account to create the log group and the hosted zone that you want to configure query logging for.
        - When you create log groups for query logging, we recommend that you use a consistent prefix, for example:

        ``/aws/route53/ *hosted zone name*``

        In the next step, you'll create a resource policy, which controls access to one or more log groups and the associated AWS resources, such as Route 53 hosted zones. There's a limit on the number of resource policies that you can create, so we recommend that you use a consistent prefix so you can use the same resource policy for all the log groups that you create for query logging.

        - Create a CloudWatch Logs resource policy, and give it the permissions that Route 53 needs to create log streams and to send query logs to log streams. You must create the CloudWatch Logs resource policy in the us-east-1 region. For the value of ``Resource`` , specify the ARN for the log group that you created in the previous step. To use the same resource policy for all the CloudWatch Logs log groups that you created for query logging configurations, replace the hosted zone name with ``*`` , for example:

        ``arn:aws:logs:us-east-1:123412341234:log-group:/aws/route53/*``

        To avoid the confused deputy problem, a security issue where an entity without a permission for an action can coerce a more-privileged entity to perform it, you can optionally limit the permissions that a service has to a resource in a resource-based policy by supplying the following values:

        - For ``aws:SourceArn`` , supply the hosted zone ARN used in creating the query logging configuration. For example, ``aws:SourceArn: arn:aws:route53:::hostedzone/hosted zone ID`` .
        - For ``aws:SourceAccount`` , supply the account ID for the account that creates the query logging configuration. For example, ``aws:SourceAccount:111111111111`` .

        For more information, see `The confused deputy problem <https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html>`_ in the *AWS IAM User Guide* .
        .. epigraph::

           You can't use the CloudWatch console to create or edit a resource policy. You must use the CloudWatch API, one of the AWS SDKs, or the AWS CLI .

        - **Log Streams and Edge Locations** - When Route 53 finishes creating the configuration for DNS query logging, it does the following:
        - Creates a log stream for an edge location the first time that the edge location responds to DNS queries for the specified hosted zone. That log stream is used to log all queries that Route 53 responds to for that edge location.
        - Begins to send query logs to the applicable log stream.

        The name of each log stream is in the following format:

        ``*hosted zone ID* / *edge location code*``

        The edge location code is a three-letter code and an arbitrarily assigned number, for example, DFW3. The three-letter code typically corresponds with the International Air Transport Association airport code for an airport near the edge location. (These abbreviations might change in the future.) For a list of edge locations, see "The Route 53 Global Network" on the `Route 53 Product Details <https://docs.aws.amazon.com/route53/details/>`_ page.

        - **Queries That Are Logged** - Query logs contain only the queries that DNS resolvers forward to Route 53. If a DNS resolver has already cached the response to a query (such as the IP address for a load balancer for example.com), the resolver will continue to return the cached response. It doesn't forward another query to Route 53 until the TTL for the corresponding resource record set expires. Depending on how many DNS queries are submitted for a resource record set, and depending on the TTL for that resource record set, query logs might contain information about only one query out of every several thousand queries that are submitted to DNS. For more information about how DNS works, see `Routing Internet Traffic to Your Website or Web Application <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/welcome-dns-service.html>`_ in the *Amazon Route 53 Developer Guide* .
        - **Log File Format** - For a list of the values in each query log and the format of each value, see `Logging DNS Queries <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/query-logs.html>`_ in the *Amazon Route 53 Developer Guide* .
        - **Pricing** - For information about charges for query logs, see `Amazon CloudWatch Pricing <https://docs.aws.amazon.com/cloudwatch/pricing/>`_ .
        - **How to Stop Logging** - If you want Route 53 to stop sending query logs to CloudWatch Logs, delete the query logging configuration. For more information, see `DeleteQueryLoggingConfig <https://docs.aws.amazon.com/Route53/latest/APIReference/API_DeleteQueryLoggingConfig.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html#cfn-route53-hostedzone-queryloggingconfig
        '''
        result = self._values.get("query_logging_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHostedZonePropsMixin.QueryLoggingConfigProperty"]], result)

    @builtins.property
    def vpcs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHostedZonePropsMixin.VPCProperty"]]]]:
        '''*Private hosted zones:* A complex type that contains information about the VPCs that are associated with the specified hosted zone.

        .. epigraph::

           For public hosted zones, omit ``VPCs`` , ``VPCId`` , and ``VPCRegion`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html#cfn-route53-hostedzone-vpcs
        '''
        result = self._values.get("vpcs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHostedZonePropsMixin.VPCProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnHostedZoneMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnHostedZonePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnHostedZonePropsMixin",
):
    '''Creates a new public or private hosted zone.

    You create records in a public hosted zone to define how you want to route traffic on the internet for a domain, such as example.com, and its subdomains (apex.example.com, acme.example.com). You create records in a private hosted zone to define how you want to route traffic for a domain and its subdomains within one or more Amazon Virtual Private Clouds (Amazon VPCs).
    .. epigraph::

       You can't convert a public hosted zone to a private hosted zone or vice versa. Instead, you must create a new hosted zone with the same name and create new resource record sets.

    For more information about charges for hosted zones, see `Amazon Route 53 Pricing <https://docs.aws.amazon.com/route53/pricing/>`_ .

    Note the following:

    - You can't create a hosted zone for a top-level domain (TLD) such as .com.
    - If your domain is registered with a registrar other than Route 53, you must update the name servers with your registrar to make Route 53 the DNS service for the domain. For more information, see `Migrating DNS Service for an Existing Domain to Amazon Route 53 <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/MigratingDNS.html>`_ in the *Amazon Route 53 Developer Guide* .

    When you submit a ``CreateHostedZone`` request, the initial status of the hosted zone is ``PENDING`` . For public hosted zones, this means that the NS and SOA records are not yet available on all Route 53 DNS servers. When the NS and SOA records are available, the status of the zone changes to ``INSYNC`` .

    The ``CreateHostedZone`` request requires the caller to have an ``ec2:DescribeVpcs`` permission.
    .. epigraph::

       When creating private hosted zones, the Amazon VPC must belong to the same partition where the hosted zone is created. A partition is a group of AWS Regions . Each AWS account is scoped to one partition.

       The following are the supported partitions:

       - ``aws`` - AWS Regions
       - ``aws-cn`` - China Regions
       - ``aws-us-gov`` - AWS GovCloud (US) Region

       For more information, see `Access Management <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html
    :cloudformationResource: AWS::Route53::HostedZone
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
        
        cfn_hosted_zone_props_mixin = route53_mixins.CfnHostedZonePropsMixin(route53_mixins.CfnHostedZoneMixinProps(
            hosted_zone_config=route53_mixins.CfnHostedZonePropsMixin.HostedZoneConfigProperty(
                comment="comment"
            ),
            hosted_zone_tags=[route53_mixins.CfnHostedZonePropsMixin.HostedZoneTagProperty(
                key="key",
                value="value"
            )],
            name="name",
            query_logging_config=route53_mixins.CfnHostedZonePropsMixin.QueryLoggingConfigProperty(
                cloud_watch_logs_log_group_arn="cloudWatchLogsLogGroupArn"
            ),
            vpcs=[route53_mixins.CfnHostedZonePropsMixin.VPCProperty(
                vpc_id="vpcId",
                vpc_region="vpcRegion"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnHostedZoneMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Route53::HostedZone``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f395ee3d3ef050ddb5b40cc33a31525a836336b7600fc1ed3d2b71c99b346eb4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a68b33204dc935eb4dc97d23a230fd7700280b4cbb7bb9e5d53d2ebb8dc788d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3623c06ec6ed06be317c76e4d696ea87ffecc68093214c461c1e0aa9c43446e6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnHostedZoneMixinProps:
        return typing.cast(CfnHostedZoneMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnHostedZonePropsMixin.HostedZoneConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"comment": "comment"},
    )
    class HostedZoneConfigProperty:
        def __init__(self, *, comment: typing.Optional[builtins.str] = None) -> None:
            '''A complex type that contains an optional comment about your hosted zone.

            If you don't want to specify a comment, omit both the ``HostedZoneConfig`` and ``Comment`` elements.

            :param comment: Any comments that you want to include about the hosted zone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-hostedzone-hostedzoneconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
                
                hosted_zone_config_property = route53_mixins.CfnHostedZonePropsMixin.HostedZoneConfigProperty(
                    comment="comment"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dde17c1b770163098a7a8db50de473c5255fd88887341a9b0cb6407b7d66c91b)
                check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comment is not None:
                self._values["comment"] = comment

        @builtins.property
        def comment(self) -> typing.Optional[builtins.str]:
            '''Any comments that you want to include about the hosted zone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-hostedzone-hostedzoneconfig.html#cfn-route53-hostedzone-hostedzoneconfig-comment
            '''
            result = self._values.get("comment")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HostedZoneConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnHostedZonePropsMixin.HostedZoneTagProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class HostedZoneTagProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A complex type that contains information about a tag that you want to add or edit for the specified health check or hosted zone.

            :param key: The value of ``Key`` depends on the operation that you want to perform:. - *Add a tag to a health check or hosted zone* : ``Key`` is the name that you want to give the new tag. - *Edit a tag* : ``Key`` is the name of the tag that you want to change the ``Value`` for. - *Delete a key* : ``Key`` is the name of the tag you want to remove. - *Give a name to a health check* : Edit the default ``Name`` tag. In the Amazon Route 53 console, the list of your health checks includes a *Name* column that lets you see the name that you've given to each health check.
            :param value: The value of ``Value`` depends on the operation that you want to perform:. - *Add a tag to a health check or hosted zone* : ``Value`` is the value that you want to give the new tag. - *Edit a tag* : ``Value`` is the new value that you want to assign the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-hostedzone-hostedzonetag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
                
                hosted_zone_tag_property = route53_mixins.CfnHostedZonePropsMixin.HostedZoneTagProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3e3e058306abe7688662e01ece00f23f68c10a344ca435942920282a09e9a829)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The value of ``Key`` depends on the operation that you want to perform:.

            - *Add a tag to a health check or hosted zone* : ``Key`` is the name that you want to give the new tag.
            - *Edit a tag* : ``Key`` is the name of the tag that you want to change the ``Value`` for.
            - *Delete a key* : ``Key`` is the name of the tag you want to remove.
            - *Give a name to a health check* : Edit the default ``Name`` tag. In the Amazon Route 53 console, the list of your health checks includes a *Name* column that lets you see the name that you've given to each health check.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-hostedzone-hostedzonetag.html#cfn-route53-hostedzone-hostedzonetag-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of ``Value`` depends on the operation that you want to perform:.

            - *Add a tag to a health check or hosted zone* : ``Value`` is the value that you want to give the new tag.
            - *Edit a tag* : ``Value`` is the new value that you want to assign the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-hostedzone-hostedzonetag.html#cfn-route53-hostedzone-hostedzonetag-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HostedZoneTagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnHostedZonePropsMixin.QueryLoggingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"cloud_watch_logs_log_group_arn": "cloudWatchLogsLogGroupArn"},
    )
    class QueryLoggingConfigProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs_log_group_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A complex type that contains information about a configuration for DNS query logging.

            :param cloud_watch_logs_log_group_arn: The Amazon Resource Name (ARN) of the CloudWatch Logs log group that Amazon Route 53 is publishing logs to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-hostedzone-queryloggingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
                
                query_logging_config_property = route53_mixins.CfnHostedZonePropsMixin.QueryLoggingConfigProperty(
                    cloud_watch_logs_log_group_arn="cloudWatchLogsLogGroupArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8cf5ee86e3529c37e33dc4f1bf06f11cba80de2cbdb3342f874f8f95cf32385d)
                check_type(argname="argument cloud_watch_logs_log_group_arn", value=cloud_watch_logs_log_group_arn, expected_type=type_hints["cloud_watch_logs_log_group_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logs_log_group_arn is not None:
                self._values["cloud_watch_logs_log_group_arn"] = cloud_watch_logs_log_group_arn

        @builtins.property
        def cloud_watch_logs_log_group_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the CloudWatch Logs log group that Amazon Route 53 is publishing logs to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-hostedzone-queryloggingconfig.html#cfn-route53-hostedzone-queryloggingconfig-cloudwatchlogsloggrouparn
            '''
            result = self._values.get("cloud_watch_logs_log_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueryLoggingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnHostedZonePropsMixin.VPCProperty",
        jsii_struct_bases=[],
        name_mapping={"vpc_id": "vpcId", "vpc_region": "vpcRegion"},
    )
    class VPCProperty:
        def __init__(
            self,
            *,
            vpc_id: typing.Optional[builtins.str] = None,
            vpc_region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''*Private hosted zones only:* A complex type that contains information about an Amazon VPC.

            Route 53 Resolver uses the records in the private hosted zone to route traffic in that VPC.
            .. epigraph::

               For public hosted zones, omit ``VPCs`` , ``VPCId`` , and ``VPCRegion`` .

            :param vpc_id: *Private hosted zones only:* The ID of an Amazon VPC. .. epigraph:: For public hosted zones, omit ``VPCs`` , ``VPCId`` , and ``VPCRegion`` .
            :param vpc_region: *Private hosted zones only:* The region that an Amazon VPC was created in. .. epigraph:: For public hosted zones, omit ``VPCs`` , ``VPCId`` , and ``VPCRegion`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-hostedzone-vpc.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
                
                v_pCProperty = route53_mixins.CfnHostedZonePropsMixin.VPCProperty(
                    vpc_id="vpcId",
                    vpc_region="vpcRegion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b334713b8c988282a62557ff55a15cac60698518f93510170d32527c89b16a4b)
                check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
                check_type(argname="argument vpc_region", value=vpc_region, expected_type=type_hints["vpc_region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id
            if vpc_region is not None:
                self._values["vpc_region"] = vpc_region

        @builtins.property
        def vpc_id(self) -> typing.Optional[builtins.str]:
            '''*Private hosted zones only:* The ID of an Amazon VPC.

            .. epigraph::

               For public hosted zones, omit ``VPCs`` , ``VPCId`` , and ``VPCRegion`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-hostedzone-vpc.html#cfn-route53-hostedzone-vpc-vpcid
            '''
            result = self._values.get("vpc_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_region(self) -> typing.Optional[builtins.str]:
            '''*Private hosted zones only:* The region that an Amazon VPC was created in.

            .. epigraph::

               For public hosted zones, omit ``VPCs`` , ``VPCId`` , and ``VPCRegion`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-hostedzone-vpc.html#cfn-route53-hostedzone-vpc-vpcregion
            '''
            result = self._values.get("vpc_region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VPCProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnKeySigningKeyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "hosted_zone_id": "hostedZoneId",
        "key_management_service_arn": "keyManagementServiceArn",
        "name": "name",
        "status": "status",
    },
)
class CfnKeySigningKeyMixinProps:
    def __init__(
        self,
        *,
        hosted_zone_id: typing.Optional[builtins.str] = None,
        key_management_service_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnKeySigningKeyPropsMixin.

        :param hosted_zone_id: The unique string (ID) that is used to identify a hosted zone. For example: ``Z00001111A1ABCaaABC11`` .
        :param key_management_service_arn: The Amazon resource name (ARN) for a customer managed customer master key (CMK) in AWS Key Management Service ( AWS ). The ``KeyManagementServiceArn`` must be unique for each key-signing key (KSK) in a single hosted zone. For example: ``arn:aws:kms:us-east-1:111122223333:key/111a2222-a11b-1ab1-2ab2-1ab21a2b3a111`` .
        :param name: A string used to identify a key-signing key (KSK). ``Name`` can include numbers, letters, and underscores (_). ``Name`` must be unique for each key-signing key in the same hosted zone.
        :param status: A string that represents the current key-signing key (KSK) status. Status can have one of the following values: - **ACTIVE** - The KSK is being used for signing. - **INACTIVE** - The KSK is not being used for signing. - **DELETING** - The KSK is in the process of being deleted. - **ACTION_NEEDED** - There is a problem with the KSK that requires you to take action to resolve. For example, the customer managed key might have been deleted, or the permissions for the customer managed key might have been changed. - **INTERNAL_FAILURE** - There was an error during a request. Before you can continue to work with DNSSEC signing, including actions that involve this KSK, you must correct the problem. For example, you may need to activate or deactivate the KSK.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-keysigningkey.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
            
            cfn_key_signing_key_mixin_props = route53_mixins.CfnKeySigningKeyMixinProps(
                hosted_zone_id="hostedZoneId",
                key_management_service_arn="keyManagementServiceArn",
                name="name",
                status="status"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d605361f5974f0bac030fcb009ad12e47bdcece8f7f79d12bdfdb7607d585c2f)
            check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
            check_type(argname="argument key_management_service_arn", value=key_management_service_arn, expected_type=type_hints["key_management_service_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hosted_zone_id is not None:
            self._values["hosted_zone_id"] = hosted_zone_id
        if key_management_service_arn is not None:
            self._values["key_management_service_arn"] = key_management_service_arn
        if name is not None:
            self._values["name"] = name
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def hosted_zone_id(self) -> typing.Optional[builtins.str]:
        '''The unique string (ID) that is used to identify a hosted zone.

        For example: ``Z00001111A1ABCaaABC11`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-keysigningkey.html#cfn-route53-keysigningkey-hostedzoneid
        '''
        result = self._values.get("hosted_zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_management_service_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon resource name (ARN) for a customer managed customer master key (CMK) in AWS Key Management Service ( AWS  ).

        The ``KeyManagementServiceArn`` must be unique for each key-signing key (KSK) in a single hosted zone. For example: ``arn:aws:kms:us-east-1:111122223333:key/111a2222-a11b-1ab1-2ab2-1ab21a2b3a111`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-keysigningkey.html#cfn-route53-keysigningkey-keymanagementservicearn
        '''
        result = self._values.get("key_management_service_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A string used to identify a key-signing key (KSK).

        ``Name`` can include numbers, letters, and underscores (_). ``Name`` must be unique for each key-signing key in the same hosted zone.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-keysigningkey.html#cfn-route53-keysigningkey-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''A string that represents the current key-signing key (KSK) status.

        Status can have one of the following values:

        - **ACTIVE** - The KSK is being used for signing.
        - **INACTIVE** - The KSK is not being used for signing.
        - **DELETING** - The KSK is in the process of being deleted.
        - **ACTION_NEEDED** - There is a problem with the KSK that requires you to take action to resolve. For example, the customer managed key might have been deleted, or the permissions for the customer managed key might have been changed.
        - **INTERNAL_FAILURE** - There was an error during a request. Before you can continue to work with DNSSEC signing, including actions that involve this KSK, you must correct the problem. For example, you may need to activate or deactivate the KSK.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-keysigningkey.html#cfn-route53-keysigningkey-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnKeySigningKeyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnKeySigningKeyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnKeySigningKeyPropsMixin",
):
    '''The ``AWS::Route53::KeySigningKey`` resource creates a new key-signing key (KSK) in a hosted zone.

    The hosted zone ID is passed as a parameter in the KSK properties. You can specify the properties of this KSK using the ``Name`` , ``Status`` , and ``KeyManagementServiceArn`` properties of the resource.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-keysigningkey.html
    :cloudformationResource: AWS::Route53::KeySigningKey
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
        
        cfn_key_signing_key_props_mixin = route53_mixins.CfnKeySigningKeyPropsMixin(route53_mixins.CfnKeySigningKeyMixinProps(
            hosted_zone_id="hostedZoneId",
            key_management_service_arn="keyManagementServiceArn",
            name="name",
            status="status"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnKeySigningKeyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Route53::KeySigningKey``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64f1a1d8a26eccbd5cef66b58d91a46c6895b4623981a0495ea25ffd8206800e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3094d1ac04a6143ea3a7278ac2e485baab5c2be123cad1395e1a91b0a32d8dbb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53e1bcd860885a2c1bf08b4c244a908cf23093a627713adbbae0c2860ee215c5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnKeySigningKeyMixinProps:
        return typing.cast(CfnKeySigningKeyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnRecordSetGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "comment": "comment",
        "hosted_zone_id": "hostedZoneId",
        "hosted_zone_name": "hostedZoneName",
        "record_sets": "recordSets",
    },
)
class CfnRecordSetGroupMixinProps:
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        hosted_zone_id: typing.Optional[builtins.str] = None,
        hosted_zone_name: typing.Optional[builtins.str] = None,
        record_sets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRecordSetGroupPropsMixin.RecordSetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnRecordSetGroupPropsMixin.

        :param comment: *Optional:* Any comments you want to include about a change batch request.
        :param hosted_zone_id: The ID of the hosted zone that you want to create records in. Specify either ``HostedZoneName`` or ``HostedZoneId`` , but not both. If you have multiple hosted zones with the same domain name, you must specify the hosted zone using ``HostedZoneId`` .
        :param hosted_zone_name: The name of the hosted zone that you want to create records in. You must include a trailing dot (for example, ``www.example.com.`` ) as part of the ``HostedZoneName`` . When you create a stack using an ``AWS::Route53::RecordSet`` that specifies ``HostedZoneName`` , AWS CloudFormation attempts to find a hosted zone whose name matches the ``HostedZoneName`` . If AWS CloudFormation can't find a hosted zone with a matching domain name, or if there is more than one hosted zone with the specified domain name, AWS CloudFormation will not create the stack. Specify either ``HostedZoneName`` or ``HostedZoneId`` , but not both. If you have multiple hosted zones with the same domain name, you must specify the hosted zone using ``HostedZoneId`` .
        :param record_sets: A complex type that contains one ``RecordSet`` element for each record that you want to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordsetgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
            
            cfn_record_set_group_mixin_props = route53_mixins.CfnRecordSetGroupMixinProps(
                comment="comment",
                hosted_zone_id="hostedZoneId",
                hosted_zone_name="hostedZoneName",
                record_sets=[route53_mixins.CfnRecordSetGroupPropsMixin.RecordSetProperty(
                    alias_target=route53_mixins.CfnRecordSetGroupPropsMixin.AliasTargetProperty(
                        dns_name="dnsName",
                        evaluate_target_health=False,
                        hosted_zone_id="hostedZoneId"
                    ),
                    cidr_routing_config=route53_mixins.CfnRecordSetGroupPropsMixin.CidrRoutingConfigProperty(
                        collection_id="collectionId",
                        location_name="locationName"
                    ),
                    failover="failover",
                    geo_location=route53_mixins.CfnRecordSetGroupPropsMixin.GeoLocationProperty(
                        continent_code="continentCode",
                        country_code="countryCode",
                        subdivision_code="subdivisionCode"
                    ),
                    geo_proximity_location=route53_mixins.CfnRecordSetGroupPropsMixin.GeoProximityLocationProperty(
                        aws_region="awsRegion",
                        bias=123,
                        coordinates=route53_mixins.CfnRecordSetGroupPropsMixin.CoordinatesProperty(
                            latitude="latitude",
                            longitude="longitude"
                        ),
                        local_zone_group="localZoneGroup"
                    ),
                    health_check_id="healthCheckId",
                    hosted_zone_id="hostedZoneId",
                    hosted_zone_name="hostedZoneName",
                    multi_value_answer=False,
                    name="name",
                    region="region",
                    resource_records=["resourceRecords"],
                    set_identifier="setIdentifier",
                    ttl="ttl",
                    type="type",
                    weight=123
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__003537c327ec31bc54cc31a2c09bd817db5ac8f8d8f366eeb469d79b59d7ca9c)
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
            check_type(argname="argument hosted_zone_name", value=hosted_zone_name, expected_type=type_hints["hosted_zone_name"])
            check_type(argname="argument record_sets", value=record_sets, expected_type=type_hints["record_sets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if comment is not None:
            self._values["comment"] = comment
        if hosted_zone_id is not None:
            self._values["hosted_zone_id"] = hosted_zone_id
        if hosted_zone_name is not None:
            self._values["hosted_zone_name"] = hosted_zone_name
        if record_sets is not None:
            self._values["record_sets"] = record_sets

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''*Optional:* Any comments you want to include about a change batch request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordsetgroup.html#cfn-route53-recordsetgroup-comment
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hosted_zone_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the hosted zone that you want to create records in.

        Specify either ``HostedZoneName`` or ``HostedZoneId`` , but not both. If you have multiple hosted zones with the same domain name, you must specify the hosted zone using ``HostedZoneId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordsetgroup.html#cfn-route53-recordsetgroup-hostedzoneid
        '''
        result = self._values.get("hosted_zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hosted_zone_name(self) -> typing.Optional[builtins.str]:
        '''The name of the hosted zone that you want to create records in.

        You must include a trailing dot (for example, ``www.example.com.`` ) as part of the ``HostedZoneName`` .

        When you create a stack using an ``AWS::Route53::RecordSet`` that specifies ``HostedZoneName`` , AWS CloudFormation attempts to find a hosted zone whose name matches the ``HostedZoneName`` . If AWS CloudFormation can't find a hosted zone with a matching domain name, or if there is more than one hosted zone with the specified domain name, AWS CloudFormation will not create the stack.

        Specify either ``HostedZoneName`` or ``HostedZoneId`` , but not both. If you have multiple hosted zones with the same domain name, you must specify the hosted zone using ``HostedZoneId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordsetgroup.html#cfn-route53-recordsetgroup-hostedzonename
        '''
        result = self._values.get("hosted_zone_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def record_sets(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordSetGroupPropsMixin.RecordSetProperty"]]]]:
        '''A complex type that contains one ``RecordSet`` element for each record that you want to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordsetgroup.html#cfn-route53-recordsetgroup-recordsets
        '''
        result = self._values.get("record_sets")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordSetGroupPropsMixin.RecordSetProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRecordSetGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRecordSetGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnRecordSetGroupPropsMixin",
):
    '''A complex type that contains an optional comment, the name and ID of the hosted zone that you want to make changes in, and values for the records that you want to create.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordsetgroup.html
    :cloudformationResource: AWS::Route53::RecordSetGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
        
        cfn_record_set_group_props_mixin = route53_mixins.CfnRecordSetGroupPropsMixin(route53_mixins.CfnRecordSetGroupMixinProps(
            comment="comment",
            hosted_zone_id="hostedZoneId",
            hosted_zone_name="hostedZoneName",
            record_sets=[route53_mixins.CfnRecordSetGroupPropsMixin.RecordSetProperty(
                alias_target=route53_mixins.CfnRecordSetGroupPropsMixin.AliasTargetProperty(
                    dns_name="dnsName",
                    evaluate_target_health=False,
                    hosted_zone_id="hostedZoneId"
                ),
                cidr_routing_config=route53_mixins.CfnRecordSetGroupPropsMixin.CidrRoutingConfigProperty(
                    collection_id="collectionId",
                    location_name="locationName"
                ),
                failover="failover",
                geo_location=route53_mixins.CfnRecordSetGroupPropsMixin.GeoLocationProperty(
                    continent_code="continentCode",
                    country_code="countryCode",
                    subdivision_code="subdivisionCode"
                ),
                geo_proximity_location=route53_mixins.CfnRecordSetGroupPropsMixin.GeoProximityLocationProperty(
                    aws_region="awsRegion",
                    bias=123,
                    coordinates=route53_mixins.CfnRecordSetGroupPropsMixin.CoordinatesProperty(
                        latitude="latitude",
                        longitude="longitude"
                    ),
                    local_zone_group="localZoneGroup"
                ),
                health_check_id="healthCheckId",
                hosted_zone_id="hostedZoneId",
                hosted_zone_name="hostedZoneName",
                multi_value_answer=False,
                name="name",
                region="region",
                resource_records=["resourceRecords"],
                set_identifier="setIdentifier",
                ttl="ttl",
                type="type",
                weight=123
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRecordSetGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Route53::RecordSetGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b8269b04831cadefdb41fc68ad44fa9b722a8aa74e3658656e9ccbd58300557)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57643a76be8544a244adf0fecbd03d20e6f3f19c5cf6772d8e0cf22388b89538)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdf61fa0795117b90a8d671e2f9aed13f2152f16bb281539ee69f4dcc7c15f5d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRecordSetGroupMixinProps:
        return typing.cast(CfnRecordSetGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnRecordSetGroupPropsMixin.AliasTargetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dns_name": "dnsName",
            "evaluate_target_health": "evaluateTargetHealth",
            "hosted_zone_id": "hostedZoneId",
        },
    )
    class AliasTargetProperty:
        def __init__(
            self,
            *,
            dns_name: typing.Optional[builtins.str] = None,
            evaluate_target_health: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            hosted_zone_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''*Alias records only:* Information about the AWS resource, such as a CloudFront distribution or an Amazon S3 bucket, that you want to route traffic to.

            When creating records for a private hosted zone, note the following:

            - Creating geolocation alias and latency alias records in a private hosted zone is allowed but not supported.
            - For information about creating failover records in a private hosted zone, see `Configuring Failover in a Private Hosted Zone <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-private-hosted-zones.html>`_ .

            :param dns_name: *Alias records only:* The value that you specify depends on where you want to route queries:. - **Amazon API Gateway custom regional APIs and edge-optimized APIs** - Specify the applicable domain name for your API. You can get the applicable value using the AWS CLI command `get-domain-names <https://docs.aws.amazon.com/cli/latest/reference/apigateway/get-domain-names.html>`_ : - For regional APIs, specify the value of ``regionalDomainName`` . - For edge-optimized APIs, specify the value of ``distributionDomainName`` . This is the name of the associated CloudFront distribution, such as ``da1b2c3d4e5.cloudfront.net`` . .. epigraph:: The name of the record that you're creating must match a custom domain name for your API, such as ``api.example.com`` . - **Amazon Virtual Private Cloud interface VPC endpoint** - Enter the API endpoint for the interface endpoint, such as ``vpce-123456789abcdef01-example-us-east-1a.elasticloadbalancing.us-east-1.vpce.amazonaws.com`` . For edge-optimized APIs, this is the domain name for the corresponding CloudFront distribution. You can get the value of ``DnsName`` using the AWS CLI command `describe-vpc-endpoints <https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-vpc-endpoints.html>`_ . - **CloudFront distribution** - Specify the domain name that CloudFront assigned when you created your distribution. Your CloudFront distribution must include an alternate domain name that matches the name of the record. For example, if the name of the record is *acme.example.com* , your CloudFront distribution must include *acme.example.com* as one of the alternate domain names. For more information, see `Using Alternate Domain Names (CNAMEs) <https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/CNAMEs.html>`_ in the *Amazon CloudFront Developer Guide* . You can't create a record in a private hosted zone to route traffic to a CloudFront distribution. .. epigraph:: For failover alias records, you can't specify a CloudFront distribution for both the primary and secondary records. A distribution must include an alternate domain name that matches the name of the record. However, the primary and secondary records have the same name, and you can't include the same alternate domain name in more than one distribution. - **Elastic Beanstalk environment** - If the domain name for your Elastic Beanstalk environment includes the region that you deployed the environment in, you can create an alias record that routes traffic to the environment. For example, the domain name ``my-environment. *us-west-2* .elasticbeanstalk.com`` is a regionalized domain name. .. epigraph:: For environments that were created before early 2016, the domain name doesn't include the region. To route traffic to these environments, you must create a CNAME record instead of an alias record. Note that you can't create a CNAME record for the root domain name. For example, if your domain name is example.com, you can create a record that routes traffic for acme.example.com to your Elastic Beanstalk environment, but you can't create a record that routes traffic for example.com to your Elastic Beanstalk environment. For Elastic Beanstalk environments that have regionalized subdomains, specify the ``CNAME`` attribute for the environment. You can use the following methods to get the value of the CNAME attribute: - *AWS Management Console* : For information about how to get the value by using the console, see `Using Custom Domains with AWS Elastic Beanstalk <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/customdomains.html>`_ in the *AWS Elastic Beanstalk Developer Guide* . - *Elastic Beanstalk API* : Use the ``DescribeEnvironments`` action to get the value of the ``CNAME`` attribute. For more information, see `DescribeEnvironments <https://docs.aws.amazon.com/elasticbeanstalk/latest/api/API_DescribeEnvironments.html>`_ in the *AWS Elastic Beanstalk API Reference* . - *AWS CLI* : Use the ``describe-environments`` command to get the value of the ``CNAME`` attribute. For more information, see `describe-environments <https://docs.aws.amazon.com/cli/latest/reference/elasticbeanstalk/describe-environments.html>`_ in the *AWS CLI* . - **ELB load balancer** - Specify the DNS name that is associated with the load balancer. Get the DNS name by using the AWS Management Console , the ELB API, or the AWS CLI . - *AWS Management Console* : Go to the EC2 page, choose *Load Balancers* in the navigation pane, choose the load balancer, choose the *Description* tab, and get the value of the *DNS name* field. If you're routing traffic to a Classic Load Balancer, get the value that begins with *dualstack* . If you're routing traffic to another type of load balancer, get the value that applies to the record type, A or AAAA. - *Elastic Load Balancing API* : Use ``DescribeLoadBalancers`` to get the value of ``DNSName`` . For more information, see the applicable guide: - Classic Load Balancers: `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/2012-06-01/APIReference/API_DescribeLoadBalancers.html>`_ - Application and Network Load Balancers: `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeLoadBalancers.html>`_ - *CloudFormation Fn::GetAtt intrinsic function* : Use the `Fn::GetAtt <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html>`_ intrinsic function to get the value of ``DNSName`` : - `Classic Load Balancers <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#aws-properties-ec2-elb-return-values>`_ . - `Application and Network Load Balancers <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#aws-resource-elasticloadbalancingv2-loadbalancer-return-values>`_ . - *AWS CLI* : Use ``describe-load-balancers`` to get the value of ``DNSName`` . For more information, see the applicable guide: - Classic Load Balancers: `describe-load-balancers <https://docs.aws.amazon.com/cli/latest/reference/elb/describe-load-balancers.html>`_ - Application and Network Load Balancers: `describe-load-balancers <https://docs.aws.amazon.com/cli/latest/reference/elbv2/describe-load-balancers.html>`_ - **Global Accelerator accelerator** - Specify the DNS name for your accelerator: - *Global Accelerator API* : To get the DNS name, use `DescribeAccelerator <https://docs.aws.amazon.com/global-accelerator/latest/api/API_DescribeAccelerator.html>`_ . - *AWS CLI* : To get the DNS name, use `describe-accelerator <https://docs.aws.amazon.com/cli/latest/reference/globalaccelerator/describe-accelerator.html>`_ . - **Amazon S3 bucket that is configured as a static website** - Specify the domain name of the Amazon S3 website endpoint that you created the bucket in, for example, ``s3-website.us-east-2.amazonaws.com`` . For more information about valid values, see the table `Amazon S3 Website Endpoints <https://docs.aws.amazon.com/general/latest/gr/s3.html#s3_website_region_endpoints>`_ in the *Amazon Web Services General Reference* . For more information about using S3 buckets for websites, see `Getting Started with Amazon Route 53 <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/getting-started.html>`_ in the *Amazon Route 53 Developer Guide.* - **Another Route 53 record** - Specify the value of the ``Name`` element for a record in the current hosted zone. .. epigraph:: If you're creating an alias record that has the same name as the hosted zone (known as the zone apex), you can't specify the domain name for a record for which the value of ``Type`` is ``CNAME`` . This is because the alias record must have the same type as the record that you're routing traffic to, and creating a CNAME record for the zone apex isn't supported even for an alias record.
            :param evaluate_target_health: *Applies only to alias records with any routing policy:* When ``EvaluateTargetHealth`` is ``true`` , an alias record inherits the health of the referenced AWS resource, such as an ELB load balancer or another record in the hosted zone. Note the following: - **CloudFront distributions** - You can't set ``EvaluateTargetHealth`` to ``true`` when the alias target is a CloudFront distribution. - **Elastic Beanstalk environments that have regionalized subdomains** - If you specify an Elastic Beanstalk environment in ``DNSName`` and the environment contains an ELB load balancer, Elastic Load Balancing routes queries only to the healthy Amazon EC2 instances that are registered with the load balancer. (An environment automatically contains an ELB load balancer if it includes more than one Amazon EC2 instance.) If you set ``EvaluateTargetHealth`` to ``true`` and either no Amazon EC2 instances are healthy or the load balancer itself is unhealthy, Route 53 routes queries to other available resources that are healthy, if any. If the environment contains a single Amazon EC2 instance, there are no special requirements. - **ELB load balancers** - Health checking behavior depends on the type of load balancer: - *Classic Load Balancers* : If you specify an ELB Classic Load Balancer in ``DNSName`` , Elastic Load Balancing routes queries only to the healthy Amazon EC2 instances that are registered with the load balancer. If you set ``EvaluateTargetHealth`` to ``true`` and either no EC2 instances are healthy or the load balancer itself is unhealthy, Route 53 routes queries to other resources. - *Application and Network Load Balancers* : If you specify an ELB Application or Network Load Balancer and you set ``EvaluateTargetHealth`` to ``true`` , Route 53 routes queries to the load balancer based on the health of the target groups that are associated with the load balancer: - For an Application or Network Load Balancer to be considered healthy, every target group that contains targets must contain at least one healthy target. If any target group contains only unhealthy targets, the load balancer is considered unhealthy, and Route 53 routes queries to other resources. - A target group that has no registered targets is considered unhealthy. .. epigraph:: When you create a load balancer, you configure settings for Elastic Load Balancing health checks; they're not Route 53 health checks, but they perform a similar function. Do not create Route 53 health checks for the EC2 instances that you register with an ELB load balancer. - **S3 buckets** - There are no special requirements for setting ``EvaluateTargetHealth`` to ``true`` when the alias target is an S3 bucket. - **Other records in the same hosted zone** - If the AWS resource that you specify in ``DNSName`` is a record or a group of records (for example, a group of weighted records) but is not another alias record, we recommend that you associate a health check with all of the records in the alias target. For more information, see `What Happens When You Omit Health Checks? <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-complex-configs.html#dns-failover-complex-configs-hc-omitting>`_ in the *Amazon Route 53 Developer Guide* . For more information and examples, see `Amazon Route 53 Health Checks and DNS Failover <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html>`_ in the *Amazon Route 53 Developer Guide* .
            :param hosted_zone_id: *Alias resource records sets only* : The value used depends on where you want to route traffic:. - **Amazon API Gateway custom regional APIs and edge-optimized APIs** - Specify the hosted zone ID for your API. You can get the applicable value using the AWS CLI command `get-domain-names <https://docs.aws.amazon.com/cli/latest/reference/apigateway/get-domain-names.html>`_ : - For regional APIs, specify the value of ``regionalHostedZoneId`` . - For edge-optimized APIs, specify the value of ``distributionHostedZoneId`` . - **Amazon Virtual Private Cloud interface VPC endpoint** - Specify the hosted zone ID for your interface endpoint. You can get the value of ``HostedZoneId`` using the AWS CLI command `describe-vpc-endpoints <https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-vpc-endpoints.html>`_ . - **CloudFront distribution** - Specify ``Z2FDTNDATAQYW2`` . This is always the hosted zone ID when you create an alias record that routes traffic to a CloudFront distribution. .. epigraph:: Alias records for CloudFront can't be created in a private zone. - **Elastic Beanstalk environment** - Specify the hosted zone ID for the region that you created the environment in. The environment must have a regionalized subdomain. For a list of regions and the corresponding hosted zone IDs, see `AWS Elastic Beanstalk endpoints and quotas <https://docs.aws.amazon.com/general/latest/gr/elasticbeanstalk.html>`_ in the *Amazon Web Services General Reference* . - **ELB load balancer** - Specify the value of the hosted zone ID for the load balancer. Use the following methods to get the hosted zone ID: - `Service Endpoints <https://docs.aws.amazon.com/general/latest/gr/elb.html>`_ table in the "Elastic Load Balancing endpoints and quotas" topic in the *Amazon Web Services General Reference* : Use the value that corresponds with the region that you created your load balancer in. Note that there are separate columns for Application and Classic Load Balancers and for Network Load Balancers. - *AWS Management Console* : Go to the Amazon EC2 page, choose *Load Balancers* in the navigation pane, select the load balancer, and get the value of the *Hosted zone* field on the *Description* tab. - *Elastic Load Balancing API* : Use ``DescribeLoadBalancers`` to get the applicable value. For more information, see the applicable guide: - Classic Load Balancers: Use `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/2012-06-01/APIReference/API_DescribeLoadBalancers.html>`_ to get the value of ``CanonicalHostedZoneNameID`` . - Application and Network Load Balancers: Use `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeLoadBalancers.html>`_ to get the value of ``CanonicalHostedZoneID`` . - *CloudFormation Fn::GetAtt intrinsic function* : Use the `Fn::GetAtt <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html>`_ intrinsic function to get the applicable value: - Classic Load Balancers: Get `CanonicalHostedZoneNameID <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#aws-properties-ec2-elb-return-values>`_ . - Application and Network Load Balancers: Get `CanonicalHostedZoneID <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#aws-resource-elasticloadbalancingv2-loadbalancer-return-values>`_ . - *AWS CLI* : Use ``describe-load-balancers`` to get the applicable value. For more information, see the applicable guide: - Classic Load Balancers: Use `describe-load-balancers <https://docs.aws.amazon.com/cli/latest/reference/elb/describe-load-balancers.html>`_ to get the value of ``CanonicalHostedZoneNameID`` . - Application and Network Load Balancers: Use `describe-load-balancers <https://docs.aws.amazon.com/cli/latest/reference/elbv2/describe-load-balancers.html>`_ to get the value of ``CanonicalHostedZoneID`` . - **Global Accelerator accelerator** - Specify ``Z2BJ6XQ5FK7U4H`` . - **An Amazon S3 bucket configured as a static website** - Specify the hosted zone ID for the region that you created the bucket in. For more information about valid values, see the table `Amazon S3 Website Endpoints <https://docs.aws.amazon.com/general/latest/gr/s3.html#s3_website_region_endpoints>`_ in the *Amazon Web Services General Reference* . - **Another Route 53 record in your hosted zone** - Specify the hosted zone ID of your hosted zone. (An alias record can't reference a record in a different hosted zone.)

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-aliastarget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
                
                alias_target_property = route53_mixins.CfnRecordSetGroupPropsMixin.AliasTargetProperty(
                    dns_name="dnsName",
                    evaluate_target_health=False,
                    hosted_zone_id="hostedZoneId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6b666b53f4ee3d71b5d7b2ef2d60ba8663d347f3dadcc062e0bdaba41c6d1b49)
                check_type(argname="argument dns_name", value=dns_name, expected_type=type_hints["dns_name"])
                check_type(argname="argument evaluate_target_health", value=evaluate_target_health, expected_type=type_hints["evaluate_target_health"])
                check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dns_name is not None:
                self._values["dns_name"] = dns_name
            if evaluate_target_health is not None:
                self._values["evaluate_target_health"] = evaluate_target_health
            if hosted_zone_id is not None:
                self._values["hosted_zone_id"] = hosted_zone_id

        @builtins.property
        def dns_name(self) -> typing.Optional[builtins.str]:
            '''*Alias records only:* The value that you specify depends on where you want to route queries:.

            - **Amazon API Gateway custom regional APIs and edge-optimized APIs** - Specify the applicable domain name for your API. You can get the applicable value using the AWS CLI command `get-domain-names <https://docs.aws.amazon.com/cli/latest/reference/apigateway/get-domain-names.html>`_ :
            - For regional APIs, specify the value of ``regionalDomainName`` .
            - For edge-optimized APIs, specify the value of ``distributionDomainName`` . This is the name of the associated CloudFront distribution, such as ``da1b2c3d4e5.cloudfront.net`` .

            .. epigraph::

               The name of the record that you're creating must match a custom domain name for your API, such as ``api.example.com`` .

            - **Amazon Virtual Private Cloud interface VPC endpoint** - Enter the API endpoint for the interface endpoint, such as ``vpce-123456789abcdef01-example-us-east-1a.elasticloadbalancing.us-east-1.vpce.amazonaws.com`` . For edge-optimized APIs, this is the domain name for the corresponding CloudFront distribution. You can get the value of ``DnsName`` using the AWS CLI command `describe-vpc-endpoints <https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-vpc-endpoints.html>`_ .
            - **CloudFront distribution** - Specify the domain name that CloudFront assigned when you created your distribution.

            Your CloudFront distribution must include an alternate domain name that matches the name of the record. For example, if the name of the record is *acme.example.com* , your CloudFront distribution must include *acme.example.com* as one of the alternate domain names. For more information, see `Using Alternate Domain Names (CNAMEs) <https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/CNAMEs.html>`_ in the *Amazon CloudFront Developer Guide* .

            You can't create a record in a private hosted zone to route traffic to a CloudFront distribution.
            .. epigraph::

               For failover alias records, you can't specify a CloudFront distribution for both the primary and secondary records. A distribution must include an alternate domain name that matches the name of the record. However, the primary and secondary records have the same name, and you can't include the same alternate domain name in more than one distribution.

            - **Elastic Beanstalk environment** - If the domain name for your Elastic Beanstalk environment includes the region that you deployed the environment in, you can create an alias record that routes traffic to the environment. For example, the domain name ``my-environment. *us-west-2* .elasticbeanstalk.com`` is a regionalized domain name.

            .. epigraph::

               For environments that were created before early 2016, the domain name doesn't include the region. To route traffic to these environments, you must create a CNAME record instead of an alias record. Note that you can't create a CNAME record for the root domain name. For example, if your domain name is example.com, you can create a record that routes traffic for acme.example.com to your Elastic Beanstalk environment, but you can't create a record that routes traffic for example.com to your Elastic Beanstalk environment.

            For Elastic Beanstalk environments that have regionalized subdomains, specify the ``CNAME`` attribute for the environment. You can use the following methods to get the value of the CNAME attribute:

            - *AWS Management Console* : For information about how to get the value by using the console, see `Using Custom Domains with AWS Elastic Beanstalk <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/customdomains.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .
            - *Elastic Beanstalk API* : Use the ``DescribeEnvironments`` action to get the value of the ``CNAME`` attribute. For more information, see `DescribeEnvironments <https://docs.aws.amazon.com/elasticbeanstalk/latest/api/API_DescribeEnvironments.html>`_ in the *AWS Elastic Beanstalk API Reference* .
            - *AWS CLI* : Use the ``describe-environments`` command to get the value of the ``CNAME`` attribute. For more information, see `describe-environments <https://docs.aws.amazon.com/cli/latest/reference/elasticbeanstalk/describe-environments.html>`_ in the *AWS CLI* .
            - **ELB load balancer** - Specify the DNS name that is associated with the load balancer. Get the DNS name by using the AWS Management Console , the ELB API, or the AWS CLI .
            - *AWS Management Console* : Go to the EC2 page, choose *Load Balancers* in the navigation pane, choose the load balancer, choose the *Description* tab, and get the value of the *DNS name* field.

            If you're routing traffic to a Classic Load Balancer, get the value that begins with *dualstack* . If you're routing traffic to another type of load balancer, get the value that applies to the record type, A or AAAA.

            - *Elastic Load Balancing API* : Use ``DescribeLoadBalancers`` to get the value of ``DNSName`` . For more information, see the applicable guide:
            - Classic Load Balancers: `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/2012-06-01/APIReference/API_DescribeLoadBalancers.html>`_
            - Application and Network Load Balancers: `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeLoadBalancers.html>`_
            - *CloudFormation Fn::GetAtt intrinsic function* : Use the `Fn::GetAtt <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html>`_ intrinsic function to get the value of ``DNSName`` :
            - `Classic Load Balancers <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#aws-properties-ec2-elb-return-values>`_ .
            - `Application and Network Load Balancers <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#aws-resource-elasticloadbalancingv2-loadbalancer-return-values>`_ .
            - *AWS CLI* : Use ``describe-load-balancers`` to get the value of ``DNSName`` . For more information, see the applicable guide:
            - Classic Load Balancers: `describe-load-balancers <https://docs.aws.amazon.com/cli/latest/reference/elb/describe-load-balancers.html>`_
            - Application and Network Load Balancers: `describe-load-balancers <https://docs.aws.amazon.com/cli/latest/reference/elbv2/describe-load-balancers.html>`_
            - **Global Accelerator accelerator** - Specify the DNS name for your accelerator:
            - *Global Accelerator API* : To get the DNS name, use `DescribeAccelerator <https://docs.aws.amazon.com/global-accelerator/latest/api/API_DescribeAccelerator.html>`_ .
            - *AWS CLI* : To get the DNS name, use `describe-accelerator <https://docs.aws.amazon.com/cli/latest/reference/globalaccelerator/describe-accelerator.html>`_ .
            - **Amazon S3 bucket that is configured as a static website** - Specify the domain name of the Amazon S3 website endpoint that you created the bucket in, for example, ``s3-website.us-east-2.amazonaws.com`` . For more information about valid values, see the table `Amazon S3 Website Endpoints <https://docs.aws.amazon.com/general/latest/gr/s3.html#s3_website_region_endpoints>`_ in the *Amazon Web Services General Reference* . For more information about using S3 buckets for websites, see `Getting Started with Amazon Route 53 <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/getting-started.html>`_ in the *Amazon Route 53 Developer Guide.*
            - **Another Route 53 record** - Specify the value of the ``Name`` element for a record in the current hosted zone.

            .. epigraph::

               If you're creating an alias record that has the same name as the hosted zone (known as the zone apex), you can't specify the domain name for a record for which the value of ``Type`` is ``CNAME`` . This is because the alias record must have the same type as the record that you're routing traffic to, and creating a CNAME record for the zone apex isn't supported even for an alias record.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-aliastarget.html#cfn-route53-recordsetgroup-aliastarget-dnsname
            '''
            result = self._values.get("dns_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def evaluate_target_health(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''*Applies only to alias records with any routing policy:* When ``EvaluateTargetHealth`` is ``true`` , an alias record inherits the health of the referenced AWS resource, such as an ELB load balancer or another record in the hosted zone.

            Note the following:

            - **CloudFront distributions** - You can't set ``EvaluateTargetHealth`` to ``true`` when the alias target is a CloudFront distribution.
            - **Elastic Beanstalk environments that have regionalized subdomains** - If you specify an Elastic Beanstalk environment in ``DNSName`` and the environment contains an ELB load balancer, Elastic Load Balancing routes queries only to the healthy Amazon EC2 instances that are registered with the load balancer. (An environment automatically contains an ELB load balancer if it includes more than one Amazon EC2 instance.) If you set ``EvaluateTargetHealth`` to ``true`` and either no Amazon EC2 instances are healthy or the load balancer itself is unhealthy, Route 53 routes queries to other available resources that are healthy, if any.

            If the environment contains a single Amazon EC2 instance, there are no special requirements.

            - **ELB load balancers** - Health checking behavior depends on the type of load balancer:
            - *Classic Load Balancers* : If you specify an ELB Classic Load Balancer in ``DNSName`` , Elastic Load Balancing routes queries only to the healthy Amazon EC2 instances that are registered with the load balancer. If you set ``EvaluateTargetHealth`` to ``true`` and either no EC2 instances are healthy or the load balancer itself is unhealthy, Route 53 routes queries to other resources.
            - *Application and Network Load Balancers* : If you specify an ELB Application or Network Load Balancer and you set ``EvaluateTargetHealth`` to ``true`` , Route 53 routes queries to the load balancer based on the health of the target groups that are associated with the load balancer:
            - For an Application or Network Load Balancer to be considered healthy, every target group that contains targets must contain at least one healthy target. If any target group contains only unhealthy targets, the load balancer is considered unhealthy, and Route 53 routes queries to other resources.
            - A target group that has no registered targets is considered unhealthy.

            .. epigraph::

               When you create a load balancer, you configure settings for Elastic Load Balancing health checks; they're not Route 53 health checks, but they perform a similar function. Do not create Route 53 health checks for the EC2 instances that you register with an ELB load balancer.

            - **S3 buckets** - There are no special requirements for setting ``EvaluateTargetHealth`` to ``true`` when the alias target is an S3 bucket.
            - **Other records in the same hosted zone** - If the AWS resource that you specify in ``DNSName`` is a record or a group of records (for example, a group of weighted records) but is not another alias record, we recommend that you associate a health check with all of the records in the alias target. For more information, see `What Happens When You Omit Health Checks? <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-complex-configs.html#dns-failover-complex-configs-hc-omitting>`_ in the *Amazon Route 53 Developer Guide* .

            For more information and examples, see `Amazon Route 53 Health Checks and DNS Failover <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html>`_ in the *Amazon Route 53 Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-aliastarget.html#cfn-route53-recordsetgroup-aliastarget-evaluatetargethealth
            '''
            result = self._values.get("evaluate_target_health")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def hosted_zone_id(self) -> typing.Optional[builtins.str]:
            '''*Alias resource records sets only* : The value used depends on where you want to route traffic:.

            - **Amazon API Gateway custom regional APIs and edge-optimized APIs** - Specify the hosted zone ID for your API. You can get the applicable value using the AWS CLI command `get-domain-names <https://docs.aws.amazon.com/cli/latest/reference/apigateway/get-domain-names.html>`_ :
            - For regional APIs, specify the value of ``regionalHostedZoneId`` .
            - For edge-optimized APIs, specify the value of ``distributionHostedZoneId`` .
            - **Amazon Virtual Private Cloud interface VPC endpoint** - Specify the hosted zone ID for your interface endpoint. You can get the value of ``HostedZoneId`` using the AWS CLI command `describe-vpc-endpoints <https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-vpc-endpoints.html>`_ .
            - **CloudFront distribution** - Specify ``Z2FDTNDATAQYW2`` . This is always the hosted zone ID when you create an alias record that routes traffic to a CloudFront distribution.

            .. epigraph::

               Alias records for CloudFront can't be created in a private zone.

            - **Elastic Beanstalk environment** - Specify the hosted zone ID for the region that you created the environment in. The environment must have a regionalized subdomain. For a list of regions and the corresponding hosted zone IDs, see `AWS Elastic Beanstalk endpoints and quotas <https://docs.aws.amazon.com/general/latest/gr/elasticbeanstalk.html>`_ in the *Amazon Web Services General Reference* .
            - **ELB load balancer** - Specify the value of the hosted zone ID for the load balancer. Use the following methods to get the hosted zone ID:
            - `Service Endpoints <https://docs.aws.amazon.com/general/latest/gr/elb.html>`_ table in the "Elastic Load Balancing endpoints and quotas" topic in the *Amazon Web Services General Reference* : Use the value that corresponds with the region that you created your load balancer in. Note that there are separate columns for Application and Classic Load Balancers and for Network Load Balancers.
            - *AWS Management Console* : Go to the Amazon EC2 page, choose *Load Balancers* in the navigation pane, select the load balancer, and get the value of the *Hosted zone* field on the *Description* tab.
            - *Elastic Load Balancing API* : Use ``DescribeLoadBalancers`` to get the applicable value. For more information, see the applicable guide:
            - Classic Load Balancers: Use `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/2012-06-01/APIReference/API_DescribeLoadBalancers.html>`_ to get the value of ``CanonicalHostedZoneNameID`` .
            - Application and Network Load Balancers: Use `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeLoadBalancers.html>`_ to get the value of ``CanonicalHostedZoneID`` .
            - *CloudFormation Fn::GetAtt intrinsic function* : Use the `Fn::GetAtt <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html>`_ intrinsic function to get the applicable value:
            - Classic Load Balancers: Get `CanonicalHostedZoneNameID <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#aws-properties-ec2-elb-return-values>`_ .
            - Application and Network Load Balancers: Get `CanonicalHostedZoneID <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#aws-resource-elasticloadbalancingv2-loadbalancer-return-values>`_ .
            - *AWS CLI* : Use ``describe-load-balancers`` to get the applicable value. For more information, see the applicable guide:
            - Classic Load Balancers: Use `describe-load-balancers <https://docs.aws.amazon.com/cli/latest/reference/elb/describe-load-balancers.html>`_ to get the value of ``CanonicalHostedZoneNameID`` .
            - Application and Network Load Balancers: Use `describe-load-balancers <https://docs.aws.amazon.com/cli/latest/reference/elbv2/describe-load-balancers.html>`_ to get the value of ``CanonicalHostedZoneID`` .
            - **Global Accelerator accelerator** - Specify ``Z2BJ6XQ5FK7U4H`` .
            - **An Amazon S3 bucket configured as a static website** - Specify the hosted zone ID for the region that you created the bucket in. For more information about valid values, see the table `Amazon S3 Website Endpoints <https://docs.aws.amazon.com/general/latest/gr/s3.html#s3_website_region_endpoints>`_ in the *Amazon Web Services General Reference* .
            - **Another Route 53 record in your hosted zone** - Specify the hosted zone ID of your hosted zone. (An alias record can't reference a record in a different hosted zone.)

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-aliastarget.html#cfn-route53-recordsetgroup-aliastarget-hostedzoneid
            '''
            result = self._values.get("hosted_zone_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AliasTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnRecordSetGroupPropsMixin.CidrRoutingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "collection_id": "collectionId",
            "location_name": "locationName",
        },
    )
    class CidrRoutingConfigProperty:
        def __init__(
            self,
            *,
            collection_id: typing.Optional[builtins.str] = None,
            location_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The object that is specified in resource record set object when you are linking a resource record set to a CIDR location.

            A ``LocationName`` with an asterisk “*” can be used to create a default CIDR record. ``CollectionId`` is still required for default record.

            :param collection_id: The CIDR collection ID.
            :param location_name: The CIDR collection location name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-cidrroutingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
                
                cidr_routing_config_property = route53_mixins.CfnRecordSetGroupPropsMixin.CidrRoutingConfigProperty(
                    collection_id="collectionId",
                    location_name="locationName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b8d55f5393bb8740143b8affc7451395b4fd9275860b0b7ef1fab1778d5fa83e)
                check_type(argname="argument collection_id", value=collection_id, expected_type=type_hints["collection_id"])
                check_type(argname="argument location_name", value=location_name, expected_type=type_hints["location_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if collection_id is not None:
                self._values["collection_id"] = collection_id
            if location_name is not None:
                self._values["location_name"] = location_name

        @builtins.property
        def collection_id(self) -> typing.Optional[builtins.str]:
            '''The CIDR collection ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-cidrroutingconfig.html#cfn-route53-recordsetgroup-cidrroutingconfig-collectionid
            '''
            result = self._values.get("collection_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def location_name(self) -> typing.Optional[builtins.str]:
            '''The CIDR collection location name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-cidrroutingconfig.html#cfn-route53-recordsetgroup-cidrroutingconfig-locationname
            '''
            result = self._values.get("location_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CidrRoutingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnRecordSetGroupPropsMixin.CoordinatesProperty",
        jsii_struct_bases=[],
        name_mapping={"latitude": "latitude", "longitude": "longitude"},
    )
    class CoordinatesProperty:
        def __init__(
            self,
            *,
            latitude: typing.Optional[builtins.str] = None,
            longitude: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A complex type that lists the coordinates for a geoproximity resource record.

            :param latitude: Specifies a coordinate of the north–south position of a geographic point on the surface of the Earth (-90 - 90).
            :param longitude: Specifies a coordinate of the east–west position of a geographic point on the surface of the Earth (-180 - 180).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-coordinates.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
                
                coordinates_property = route53_mixins.CfnRecordSetGroupPropsMixin.CoordinatesProperty(
                    latitude="latitude",
                    longitude="longitude"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__92185053b1268da08c5a6393edccc81ec25f4a74cf82fcb3a97c5e6b6e180383)
                check_type(argname="argument latitude", value=latitude, expected_type=type_hints["latitude"])
                check_type(argname="argument longitude", value=longitude, expected_type=type_hints["longitude"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if latitude is not None:
                self._values["latitude"] = latitude
            if longitude is not None:
                self._values["longitude"] = longitude

        @builtins.property
        def latitude(self) -> typing.Optional[builtins.str]:
            '''Specifies a coordinate of the north–south position of a geographic point on the surface of the Earth (-90 - 90).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-coordinates.html#cfn-route53-recordsetgroup-coordinates-latitude
            '''
            result = self._values.get("latitude")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def longitude(self) -> typing.Optional[builtins.str]:
            '''Specifies a coordinate of the east–west position of a geographic point on the surface of the Earth (-180 - 180).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-coordinates.html#cfn-route53-recordsetgroup-coordinates-longitude
            '''
            result = self._values.get("longitude")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CoordinatesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnRecordSetGroupPropsMixin.GeoLocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "continent_code": "continentCode",
            "country_code": "countryCode",
            "subdivision_code": "subdivisionCode",
        },
    )
    class GeoLocationProperty:
        def __init__(
            self,
            *,
            continent_code: typing.Optional[builtins.str] = None,
            country_code: typing.Optional[builtins.str] = None,
            subdivision_code: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A complex type that contains information about a geographic location.

            :param continent_code: For geolocation resource record sets, a two-letter abbreviation that identifies a continent. Route 53 supports the following continent codes:. - *AF* : Africa - *AN* : Antarctica - *AS* : Asia - *EU* : Europe - *OC* : Oceania - *NA* : North America - *SA* : South America Constraint: Specifying ``ContinentCode`` with either ``CountryCode`` or ``SubdivisionCode`` returns an ``InvalidInput`` error.
            :param country_code: For geolocation resource record sets, the two-letter code for a country. Route 53 uses the two-letter country codes that are specified in `ISO standard 3166-1 alpha-2 <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2>`_ .
            :param subdivision_code: For geolocation resource record sets, the two-letter code for a state of the United States. Route 53 doesn't support any other values for ``SubdivisionCode`` . For a list of state abbreviations, see `Appendix B: Two–Letter State and Possession Abbreviations <https://docs.aws.amazon.com/https://pe.usps.com/text/pub28/28apb.htm>`_ on the United States Postal Service website. If you specify ``subdivisioncode`` , you must also specify ``US`` for ``CountryCode`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-geolocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
                
                geo_location_property = route53_mixins.CfnRecordSetGroupPropsMixin.GeoLocationProperty(
                    continent_code="continentCode",
                    country_code="countryCode",
                    subdivision_code="subdivisionCode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c94b9c8e6e08f441b76733e56a9ec475af4c8de0ed82e95f0f62dc091e67269f)
                check_type(argname="argument continent_code", value=continent_code, expected_type=type_hints["continent_code"])
                check_type(argname="argument country_code", value=country_code, expected_type=type_hints["country_code"])
                check_type(argname="argument subdivision_code", value=subdivision_code, expected_type=type_hints["subdivision_code"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if continent_code is not None:
                self._values["continent_code"] = continent_code
            if country_code is not None:
                self._values["country_code"] = country_code
            if subdivision_code is not None:
                self._values["subdivision_code"] = subdivision_code

        @builtins.property
        def continent_code(self) -> typing.Optional[builtins.str]:
            '''For geolocation resource record sets, a two-letter abbreviation that identifies a continent. Route 53 supports the following continent codes:.

            - *AF* : Africa
            - *AN* : Antarctica
            - *AS* : Asia
            - *EU* : Europe
            - *OC* : Oceania
            - *NA* : North America
            - *SA* : South America

            Constraint: Specifying ``ContinentCode`` with either ``CountryCode`` or ``SubdivisionCode`` returns an ``InvalidInput`` error.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-geolocation.html#cfn-route53-recordsetgroup-geolocation-continentcode
            '''
            result = self._values.get("continent_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def country_code(self) -> typing.Optional[builtins.str]:
            '''For geolocation resource record sets, the two-letter code for a country.

            Route 53 uses the two-letter country codes that are specified in `ISO standard 3166-1 alpha-2 <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-geolocation.html#cfn-route53-recordsetgroup-geolocation-countrycode
            '''
            result = self._values.get("country_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subdivision_code(self) -> typing.Optional[builtins.str]:
            '''For geolocation resource record sets, the two-letter code for a state of the United States.

            Route 53 doesn't support any other values for ``SubdivisionCode`` . For a list of state abbreviations, see `Appendix B: Two–Letter State and Possession Abbreviations <https://docs.aws.amazon.com/https://pe.usps.com/text/pub28/28apb.htm>`_ on the United States Postal Service website.

            If you specify ``subdivisioncode`` , you must also specify ``US`` for ``CountryCode`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-geolocation.html#cfn-route53-recordsetgroup-geolocation-subdivisioncode
            '''
            result = self._values.get("subdivision_code")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GeoLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnRecordSetGroupPropsMixin.GeoProximityLocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aws_region": "awsRegion",
            "bias": "bias",
            "coordinates": "coordinates",
            "local_zone_group": "localZoneGroup",
        },
    )
    class GeoProximityLocationProperty:
        def __init__(
            self,
            *,
            aws_region: typing.Optional[builtins.str] = None,
            bias: typing.Optional[jsii.Number] = None,
            coordinates: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRecordSetGroupPropsMixin.CoordinatesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            local_zone_group: typing.Optional[builtins.str] = None,
        ) -> None:
            '''(Resource record sets only): A complex type that lets you specify where your resources are located.

            Only one of ``LocalZoneGroup`` , ``Coordinates`` , or ``AWS Region`` is allowed per request at a time.

            For more information about geoproximity routing, see `Geoproximity routing <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy-geoproximity.html>`_ in the *Amazon Route 53 Developer Guide* .

            :param aws_region: The AWS Region the resource you are directing DNS traffic to, is in.
            :param bias: The bias increases or decreases the size of the geographic region from which Route 53 routes traffic to a resource. To use ``Bias`` to change the size of the geographic region, specify the applicable value for the bias: - To expand the size of the geographic region from which Route 53 routes traffic to a resource, specify a positive integer from 1 to 99 for the bias. Route 53 shrinks the size of adjacent regions. - To shrink the size of the geographic region from which Route 53 routes traffic to a resource, specify a negative bias of -1 to -99. Route 53 expands the size of adjacent regions.
            :param coordinates: Contains the longitude and latitude for a geographic region.
            :param local_zone_group: Specifies an AWS Local Zone Group. A local Zone Group is usually the Local Zone code without the ending character. For example, if the Local Zone is ``us-east-1-bue-1a`` the Local Zone Group is ``us-east-1-bue-1`` . You can identify the Local Zones Group for a specific Local Zone by using the `describe-availability-zones <https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-availability-zones.html>`_ CLI command: This command returns: ``"GroupName": "us-west-2-den-1"`` , specifying that the Local Zone ``us-west-2-den-1a`` belongs to the Local Zone Group ``us-west-2-den-1`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-geoproximitylocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
                
                geo_proximity_location_property = route53_mixins.CfnRecordSetGroupPropsMixin.GeoProximityLocationProperty(
                    aws_region="awsRegion",
                    bias=123,
                    coordinates=route53_mixins.CfnRecordSetGroupPropsMixin.CoordinatesProperty(
                        latitude="latitude",
                        longitude="longitude"
                    ),
                    local_zone_group="localZoneGroup"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d708f0317446e31a991928807b92fded7aa2b497c5d5f4dbcfef64ae0d2783ae)
                check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                check_type(argname="argument bias", value=bias, expected_type=type_hints["bias"])
                check_type(argname="argument coordinates", value=coordinates, expected_type=type_hints["coordinates"])
                check_type(argname="argument local_zone_group", value=local_zone_group, expected_type=type_hints["local_zone_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_region is not None:
                self._values["aws_region"] = aws_region
            if bias is not None:
                self._values["bias"] = bias
            if coordinates is not None:
                self._values["coordinates"] = coordinates
            if local_zone_group is not None:
                self._values["local_zone_group"] = local_zone_group

        @builtins.property
        def aws_region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region the resource you are directing DNS traffic to, is in.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-geoproximitylocation.html#cfn-route53-recordsetgroup-geoproximitylocation-awsregion
            '''
            result = self._values.get("aws_region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bias(self) -> typing.Optional[jsii.Number]:
            '''The bias increases or decreases the size of the geographic region from which Route 53 routes traffic to a resource.

            To use ``Bias`` to change the size of the geographic region, specify the applicable value for the bias:

            - To expand the size of the geographic region from which Route 53 routes traffic to a resource, specify a positive integer from 1 to 99 for the bias. Route 53 shrinks the size of adjacent regions.
            - To shrink the size of the geographic region from which Route 53 routes traffic to a resource, specify a negative bias of -1 to -99. Route 53 expands the size of adjacent regions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-geoproximitylocation.html#cfn-route53-recordsetgroup-geoproximitylocation-bias
            '''
            result = self._values.get("bias")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def coordinates(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordSetGroupPropsMixin.CoordinatesProperty"]]:
            '''Contains the longitude and latitude for a geographic region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-geoproximitylocation.html#cfn-route53-recordsetgroup-geoproximitylocation-coordinates
            '''
            result = self._values.get("coordinates")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordSetGroupPropsMixin.CoordinatesProperty"]], result)

        @builtins.property
        def local_zone_group(self) -> typing.Optional[builtins.str]:
            '''Specifies an AWS Local Zone Group.

            A local Zone Group is usually the Local Zone code without the ending character. For example, if the Local Zone is ``us-east-1-bue-1a`` the Local Zone Group is ``us-east-1-bue-1`` .

            You can identify the Local Zones Group for a specific Local Zone by using the `describe-availability-zones <https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-availability-zones.html>`_ CLI command:

            This command returns: ``"GroupName": "us-west-2-den-1"`` , specifying that the Local Zone ``us-west-2-den-1a`` belongs to the Local Zone Group ``us-west-2-den-1`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-geoproximitylocation.html#cfn-route53-recordsetgroup-geoproximitylocation-localzonegroup
            '''
            result = self._values.get("local_zone_group")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GeoProximityLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnRecordSetGroupPropsMixin.RecordSetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alias_target": "aliasTarget",
            "cidr_routing_config": "cidrRoutingConfig",
            "failover": "failover",
            "geo_location": "geoLocation",
            "geo_proximity_location": "geoProximityLocation",
            "health_check_id": "healthCheckId",
            "hosted_zone_id": "hostedZoneId",
            "hosted_zone_name": "hostedZoneName",
            "multi_value_answer": "multiValueAnswer",
            "name": "name",
            "region": "region",
            "resource_records": "resourceRecords",
            "set_identifier": "setIdentifier",
            "ttl": "ttl",
            "type": "type",
            "weight": "weight",
        },
    )
    class RecordSetProperty:
        def __init__(
            self,
            *,
            alias_target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRecordSetGroupPropsMixin.AliasTargetProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            cidr_routing_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRecordSetGroupPropsMixin.CidrRoutingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            failover: typing.Optional[builtins.str] = None,
            geo_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRecordSetGroupPropsMixin.GeoLocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            geo_proximity_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRecordSetGroupPropsMixin.GeoProximityLocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            health_check_id: typing.Optional[builtins.str] = None,
            hosted_zone_id: typing.Optional[builtins.str] = None,
            hosted_zone_name: typing.Optional[builtins.str] = None,
            multi_value_answer: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            name: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
            resource_records: typing.Optional[typing.Sequence[builtins.str]] = None,
            set_identifier: typing.Optional[builtins.str] = None,
            ttl: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information about one record that you want to create.

            :param alias_target: *Alias resource record sets only:* Information about the AWS resource, such as a CloudFront distribution or an Amazon S3 bucket, that you want to route traffic to. If you're creating resource records sets for a private hosted zone, note the following: - You can't create an alias resource record set in a private hosted zone to route traffic to a CloudFront distribution. - For information about creating failover resource record sets in a private hosted zone, see `Configuring Failover in a Private Hosted Zone <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-private-hosted-zones.html>`_ in the *Amazon Route 53 Developer Guide* .
            :param cidr_routing_config: 
            :param failover: *Failover resource record sets only:* To configure failover, you add the ``Failover`` element to two resource record sets. For one resource record set, you specify ``PRIMARY`` as the value for ``Failover`` ; for the other resource record set, you specify ``SECONDARY`` . In addition, you include the ``HealthCheckId`` element and specify the health check that you want Amazon Route 53 to perform for each resource record set. Except where noted, the following failover behaviors assume that you have included the ``HealthCheckId`` element in both resource record sets: - When the primary resource record set is healthy, Route 53 responds to DNS queries with the applicable value from the primary resource record set regardless of the health of the secondary resource record set. - When the primary resource record set is unhealthy and the secondary resource record set is healthy, Route 53 responds to DNS queries with the applicable value from the secondary resource record set. - When the secondary resource record set is unhealthy, Route 53 responds to DNS queries with the applicable value from the primary resource record set regardless of the health of the primary resource record set. - If you omit the ``HealthCheckId`` element for the secondary resource record set, and if the primary resource record set is unhealthy, Route 53 always responds to DNS queries with the applicable value from the secondary resource record set. This is true regardless of the health of the associated endpoint. You can't create non-failover resource record sets that have the same values for the ``Name`` and ``Type`` elements as failover resource record sets. For failover alias resource record sets, you must also include the ``EvaluateTargetHealth`` element and set the value to true. For more information about configuring failover for Route 53, see the following topics in the *Amazon Route 53 Developer Guide* : - `Route 53 Health Checks and DNS Failover <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html>`_ - `Configuring Failover in a Private Hosted Zone <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-private-hosted-zones.html>`_
            :param geo_location: *Geolocation resource record sets only:* A complex type that lets you control how Amazon Route 53 responds to DNS queries based on the geographic origin of the query. For example, if you want all queries from Africa to be routed to a web server with an IP address of ``192.0.2.111`` , create a resource record set with a ``Type`` of ``A`` and a ``ContinentCode`` of ``AF`` . If you create separate resource record sets for overlapping geographic regions (for example, one resource record set for a continent and one for a country on the same continent), priority goes to the smallest geographic region. This allows you to route most queries for a continent to one resource and to route queries for a country on that continent to a different resource. You can't create two geolocation resource record sets that specify the same geographic location. The value ``*`` in the ``CountryCode`` element matches all geographic locations that aren't specified in other geolocation resource record sets that have the same values for the ``Name`` and ``Type`` elements. .. epigraph:: Geolocation works by mapping IP addresses to locations. However, some IP addresses aren't mapped to geographic locations, so even if you create geolocation resource record sets that cover all seven continents, Route 53 will receive some DNS queries from locations that it can't identify. We recommend that you create a resource record set for which the value of ``CountryCode`` is ``*`` . Two groups of queries are routed to the resource that you specify in this record: queries that come from locations for which you haven't created geolocation resource record sets and queries from IP addresses that aren't mapped to a location. If you don't create a ``*`` resource record set, Route 53 returns a "no answer" response for queries from those locations. You can't create non-geolocation resource record sets that have the same values for the ``Name`` and ``Type`` elements as geolocation resource record sets.
            :param geo_proximity_location: A complex type that contains information about a geographic location.
            :param health_check_id: If you want Amazon Route 53 to return this resource record set in response to a DNS query only when the status of a health check is healthy, include the ``HealthCheckId`` element and specify the ID of the applicable health check. Route 53 determines whether a resource record set is healthy based on one of the following: - By periodically sending a request to the endpoint that is specified in the health check - By aggregating the status of a specified group of health checks (calculated health checks) - By determining the current state of a CloudWatch alarm (CloudWatch metric health checks) .. epigraph:: Route 53 doesn't check the health of the endpoint that is specified in the resource record set, for example, the endpoint specified by the IP address in the ``Value`` element. When you add a ``HealthCheckId`` element to a resource record set, Route 53 checks the health of the endpoint that you specified in the health check. For more information, see the following topics in the *Amazon Route 53 Developer Guide* : - `How Amazon Route 53 Determines Whether an Endpoint Is Healthy <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-determining-health-of-endpoints.html>`_ - `Route 53 Health Checks and DNS Failover <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html>`_ - `Configuring Failover in a Private Hosted Zone <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-private-hosted-zones.html>`_ *When to Specify HealthCheckId* Specifying a value for ``HealthCheckId`` is useful only when Route 53 is choosing between two or more resource record sets to respond to a DNS query, and you want Route 53 to base the choice in part on the status of a health check. Configuring health checks makes sense only in the following configurations: - *Non-alias resource record sets* : You're checking the health of a group of non-alias resource record sets that have the same routing policy, name, and type (such as multiple weighted records named www.example.com with a type of A) and you specify health check IDs for all the resource record sets. If the health check status for a resource record set is healthy, Route 53 includes the record among the records that it responds to DNS queries with. If the health check status for a resource record set is unhealthy, Route 53 stops responding to DNS queries using the value for that resource record set. If the health check status for all resource record sets in the group is unhealthy, Route 53 considers all resource record sets in the group healthy and responds to DNS queries accordingly. - *Alias resource record sets* : You specify the following settings: - You set ``EvaluateTargetHealth`` to true for an alias resource record set in a group of resource record sets that have the same routing policy, name, and type (such as multiple weighted records named www.example.com with a type of A). - You configure the alias resource record set to route traffic to a non-alias resource record set in the same hosted zone. - You specify a health check ID for the non-alias resource record set. If the health check status is healthy, Route 53 considers the alias resource record set to be healthy and includes the alias record among the records that it responds to DNS queries with. If the health check status is unhealthy, Route 53 stops responding to DNS queries using the alias resource record set. .. epigraph:: The alias resource record set can also route traffic to a *group* of non-alias resource record sets that have the same routing policy, name, and type. In that configuration, associate health checks with all of the resource record sets in the group of non-alias resource record sets. *Geolocation Routing* For geolocation resource record sets, if an endpoint is unhealthy, Route 53 looks for a resource record set for the larger, associated geographic region. For example, suppose you have resource record sets for a state in the United States, for the entire United States, for North America, and a resource record set that has ``*`` for ``CountryCode`` is ``*`` , which applies to all locations. If the endpoint for the state resource record set is unhealthy, Route 53 checks for healthy resource record sets in the following order until it finds a resource record set for which the endpoint is healthy: - The United States - North America - The default resource record set *Specifying the Health Check Endpoint by Domain Name* If your health checks specify the endpoint only by domain name, we recommend that you create a separate health check for each endpoint. For example, create a health check for each ``HTTP`` server that is serving content for ``www.example.com`` . For the value of ``FullyQualifiedDomainName`` , specify the domain name of the server (such as ``us-east-2-www.example.com`` ), not the name of the resource record sets ( ``www.example.com`` ). .. epigraph:: Health check results will be unpredictable if you do the following: - Create a health check that has the same value for ``FullyQualifiedDomainName`` as the name of a resource record set. - Associate that health check with the resource record set.
            :param hosted_zone_id: The ID of the hosted zone that you want to create records in. Specify either ``HostedZoneName`` or ``HostedZoneId`` , but not both. If you have multiple hosted zones with the same domain name, you must specify the hosted zone using ``HostedZoneId`` . Do not provide the ``HostedZoneId`` if it is already defined in ``AWS::Route53::RecordSetGroup`` . The creation fails if ``HostedZoneId`` is defined in both.
            :param hosted_zone_name: The name of the hosted zone that you want to create records in. You must include a trailing dot (for example, ``www.example.com.`` ) as part of the ``HostedZoneName`` . When you create a stack using an ``AWS::Route53::RecordSet`` that specifies ``HostedZoneName`` , AWS CloudFormation attempts to find a hosted zone whose name matches the ``HostedZoneName`` . If AWS CloudFormation can't find a hosted zone with a matching domain name, or if there is more than one hosted zone with the specified domain name, AWS CloudFormation will not create the stack. Specify either ``HostedZoneName`` or ``HostedZoneId`` , but not both. If you have multiple hosted zones with the same domain name, you must specify the hosted zone using ``HostedZoneId`` .
            :param multi_value_answer: *Multivalue answer resource record sets only* : To route traffic approximately randomly to multiple resources, such as web servers, create one multivalue answer record for each resource and specify ``true`` for ``MultiValueAnswer`` . Note the following: - If you associate a health check with a multivalue answer resource record set, Amazon Route 53 responds to DNS queries with the corresponding IP address only when the health check is healthy. - If you don't associate a health check with a multivalue answer record, Route 53 always considers the record to be healthy. - Route 53 responds to DNS queries with up to eight healthy records; if you have eight or fewer healthy records, Route 53 responds to all DNS queries with all the healthy records. - If you have more than eight healthy records, Route 53 responds to different DNS resolvers with different combinations of healthy records. - When all records are unhealthy, Route 53 responds to DNS queries with up to eight unhealthy records. - If a resource becomes unavailable after a resolver caches a response, client software typically tries another of the IP addresses in the response. You can't create multivalue answer alias records.
            :param name: The name of the record that you want to create, update, or delete. Enter a fully qualified domain name, for example, ``www.example.com`` . You can optionally include a trailing dot. If you omit the trailing dot, Amazon Route 53 assumes that the domain name that you specify is fully qualified. This means that Route 53 treats ``www.example.com`` (without a trailing dot) and ``www.example.com.`` (with a trailing dot) as identical. For information about how to specify characters other than ``a-z`` , ``0-9`` , and ``-`` (hyphen) and how to specify internationalized domain names, see `DNS Domain Name Format <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/DomainNameFormat.html>`_ in the *Amazon Route 53 Developer Guide* . You can use the asterisk (*) wildcard to replace the leftmost label in a domain name, for example, ``*.example.com`` . Note the following: - The * must replace the entire label. For example, you can't specify ``*prod.example.com`` or ``prod*.example.com`` . - The * can't replace any of the middle labels, for example, marketing.*.example.com. - If you include * in any position other than the leftmost label in a domain name, DNS treats it as an * character (ASCII 42), not as a wildcard. .. epigraph:: You can't use the * wildcard for resource records sets that have a type of NS.
            :param region: *Latency-based resource record sets only:* The Amazon EC2 Region where you created the resource that this resource record set refers to. The resource typically is an AWS resource, such as an EC2 instance or an ELB load balancer, and is referred to by an IP address or a DNS domain name, depending on the record type. When Amazon Route 53 receives a DNS query for a domain name and type for which you have created latency resource record sets, Route 53 selects the latency resource record set that has the lowest latency between the end user and the associated Amazon EC2 Region. Route 53 then returns the value that is associated with the selected resource record set. Note the following: - You can only specify one ``ResourceRecord`` per latency resource record set. - You can only create one latency resource record set for each Amazon EC2 Region. - You aren't required to create latency resource record sets for all Amazon EC2 Regions. Route 53 will choose the region with the best latency from among the regions that you create latency resource record sets for. - You can't create non-latency resource record sets that have the same values for the ``Name`` and ``Type`` elements as latency resource record sets.
            :param resource_records: Information about the records that you want to create. Each record should be in the format appropriate for the record type specified by the ``Type`` property. For information about different record types and their record formats, see `Values That You Specify When You Create or Edit Amazon Route 53 Records <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-values.html>`_ in the *Amazon Route 53 Developer Guide* .
            :param set_identifier: *Resource record sets that have a routing policy other than simple:* An identifier that differentiates among multiple resource record sets that have the same combination of name and type, such as multiple weighted resource record sets named acme.example.com that have a type of A. In a group of resource record sets that have the same name and type, the value of ``SetIdentifier`` must be unique for each resource record set. For information about routing policies, see `Choosing a Routing Policy <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html>`_ in the *Amazon Route 53 Developer Guide* .
            :param ttl: The resource record cache time to live (TTL), in seconds. Note the following:. - If you're creating or updating an alias resource record set, omit ``TTL`` . Amazon Route 53 uses the value of ``TTL`` for the alias target. - If you're associating this resource record set with a health check (if you're adding a ``HealthCheckId`` element), we recommend that you specify a ``TTL`` of 60 seconds or less so clients respond quickly to changes in health status. - All of the resource record sets in a group of weighted resource record sets must have the same value for ``TTL`` . - If a group of weighted resource record sets includes one or more weighted alias resource record sets for which the alias target is an ELB load balancer, we recommend that you specify a ``TTL`` of 60 seconds for all of the non-alias weighted resource record sets that have the same name and type. Values other than 60 seconds (the TTL for load balancers) will change the effect of the values that you specify for ``Weight`` .
            :param type: The DNS record type. For information about different record types and how data is encoded for them, see `Supported DNS Resource Record Types <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/ResourceRecordTypes.html>`_ in the *Amazon Route 53 Developer Guide* . Valid values for basic resource record sets: ``A`` | ``AAAA`` | ``CAA`` | ``CNAME`` | ``DS`` | ``MX`` | ``NAPTR`` | ``NS`` | ``PTR`` | ``SOA`` | ``SPF`` | ``SRV`` | ``TXT`` | ``TLSA`` | ``SSHFP`` | ``SVCB`` | ``HTTPS`` Values for weighted, latency, geolocation, and failover resource record sets: ``A`` | ``AAAA`` | ``CAA`` | ``CNAME`` | ``MX`` | ``NAPTR`` | ``PTR`` | ``SPF`` | ``SRV`` | ``TXT`` | ``TLSA`` | ``SSHFP`` | ``SVCB`` | ``HTTPS`` . When creating a group of weighted, latency, geolocation, or failover resource record sets, specify the same value for all of the resource record sets in the group. Valid values for multivalue answer resource record sets: ``A`` | ``AAAA`` | ``MX`` | ``NAPTR`` | ``PTR`` | ``SPF`` | ``SRV`` | ``TXT`` | ``CAA`` | ``TLSA`` | ``SSHFP`` | ``SVCB`` | ``HTTPS`` .. epigraph:: SPF records were formerly used to verify the identity of the sender of email messages. However, we no longer recommend that you create resource record sets for which the value of ``Type`` is ``SPF`` . RFC 7208, *Sender Policy Framework (SPF) for Authorizing Use of Domains in Email, Version 1* , has been updated to say, "...[I]ts existence and mechanism defined in [RFC4408] have led to some interoperability issues. Accordingly, its use is no longer appropriate for SPF version 1; implementations are not to use it." In RFC 7208, see section 14.1, `The SPF DNS Record Type <https://docs.aws.amazon.com/http://tools.ietf.org/html/rfc7208#section-14.1>`_ . Values for alias resource record sets: - *Amazon API Gateway custom regional APIs and edge-optimized APIs:* ``A`` - *CloudFront distributions:* ``A`` If IPv6 is enabled for the distribution, create two resource record sets to route traffic to your distribution, one with a value of ``A`` and one with a value of ``AAAA`` . - *Amazon API Gateway environment that has a regionalized subdomain* : ``A`` - *ELB load balancers:* ``A`` | ``AAAA`` - *Amazon S3 buckets:* ``A`` - *Amazon Virtual Private Cloud interface VPC endpoints* ``A`` - *Another resource record set in this hosted zone:* Specify the type of the resource record set that you're creating the alias for. All values are supported except ``NS`` and ``SOA`` . .. epigraph:: If you're creating an alias record that has the same name as the hosted zone (known as the zone apex), you can't route traffic to a record for which the value of ``Type`` is ``CNAME`` . This is because the alias record must have the same type as the record you're routing traffic to, and creating a CNAME record for the zone apex isn't supported even for an alias record.
            :param weight: *Weighted resource record sets only:* Among resource record sets that have the same combination of DNS name and type, a value that determines the proportion of DNS queries that Amazon Route 53 responds to using the current resource record set. Route 53 calculates the sum of the weights for the resource record sets that have the same combination of DNS name and type. Route 53 then responds to queries based on the ratio of a resource's weight to the total. Note the following: - You must specify a value for the ``Weight`` element for every weighted resource record set. - You can only specify one ``ResourceRecord`` per weighted resource record set. - You can't create latency, failover, or geolocation resource record sets that have the same values for the ``Name`` and ``Type`` elements as weighted resource record sets. - You can create a maximum of 100 weighted resource record sets that have the same values for the ``Name`` and ``Type`` elements. - For weighted (but not weighted alias) resource record sets, if you set ``Weight`` to ``0`` for a resource record set, Route 53 never responds to queries with the applicable value for that resource record set. However, if you set ``Weight`` to ``0`` for all resource record sets that have the same combination of DNS name and type, traffic is routed to all resources with equal probability. The effect of setting ``Weight`` to ``0`` is different when you associate health checks with weighted resource record sets. For more information, see `Options for Configuring Route 53 Active-Active and Active-Passive Failover <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-configuring-options.html>`_ in the *Amazon Route 53 Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-recordset.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
                
                record_set_property = route53_mixins.CfnRecordSetGroupPropsMixin.RecordSetProperty(
                    alias_target=route53_mixins.CfnRecordSetGroupPropsMixin.AliasTargetProperty(
                        dns_name="dnsName",
                        evaluate_target_health=False,
                        hosted_zone_id="hostedZoneId"
                    ),
                    cidr_routing_config=route53_mixins.CfnRecordSetGroupPropsMixin.CidrRoutingConfigProperty(
                        collection_id="collectionId",
                        location_name="locationName"
                    ),
                    failover="failover",
                    geo_location=route53_mixins.CfnRecordSetGroupPropsMixin.GeoLocationProperty(
                        continent_code="continentCode",
                        country_code="countryCode",
                        subdivision_code="subdivisionCode"
                    ),
                    geo_proximity_location=route53_mixins.CfnRecordSetGroupPropsMixin.GeoProximityLocationProperty(
                        aws_region="awsRegion",
                        bias=123,
                        coordinates=route53_mixins.CfnRecordSetGroupPropsMixin.CoordinatesProperty(
                            latitude="latitude",
                            longitude="longitude"
                        ),
                        local_zone_group="localZoneGroup"
                    ),
                    health_check_id="healthCheckId",
                    hosted_zone_id="hostedZoneId",
                    hosted_zone_name="hostedZoneName",
                    multi_value_answer=False,
                    name="name",
                    region="region",
                    resource_records=["resourceRecords"],
                    set_identifier="setIdentifier",
                    ttl="ttl",
                    type="type",
                    weight=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a8fa61ff0e1455726abcfff5dc086fd1a85b191b23d6736579fb241a9efebfca)
                check_type(argname="argument alias_target", value=alias_target, expected_type=type_hints["alias_target"])
                check_type(argname="argument cidr_routing_config", value=cidr_routing_config, expected_type=type_hints["cidr_routing_config"])
                check_type(argname="argument failover", value=failover, expected_type=type_hints["failover"])
                check_type(argname="argument geo_location", value=geo_location, expected_type=type_hints["geo_location"])
                check_type(argname="argument geo_proximity_location", value=geo_proximity_location, expected_type=type_hints["geo_proximity_location"])
                check_type(argname="argument health_check_id", value=health_check_id, expected_type=type_hints["health_check_id"])
                check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
                check_type(argname="argument hosted_zone_name", value=hosted_zone_name, expected_type=type_hints["hosted_zone_name"])
                check_type(argname="argument multi_value_answer", value=multi_value_answer, expected_type=type_hints["multi_value_answer"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
                check_type(argname="argument resource_records", value=resource_records, expected_type=type_hints["resource_records"])
                check_type(argname="argument set_identifier", value=set_identifier, expected_type=type_hints["set_identifier"])
                check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alias_target is not None:
                self._values["alias_target"] = alias_target
            if cidr_routing_config is not None:
                self._values["cidr_routing_config"] = cidr_routing_config
            if failover is not None:
                self._values["failover"] = failover
            if geo_location is not None:
                self._values["geo_location"] = geo_location
            if geo_proximity_location is not None:
                self._values["geo_proximity_location"] = geo_proximity_location
            if health_check_id is not None:
                self._values["health_check_id"] = health_check_id
            if hosted_zone_id is not None:
                self._values["hosted_zone_id"] = hosted_zone_id
            if hosted_zone_name is not None:
                self._values["hosted_zone_name"] = hosted_zone_name
            if multi_value_answer is not None:
                self._values["multi_value_answer"] = multi_value_answer
            if name is not None:
                self._values["name"] = name
            if region is not None:
                self._values["region"] = region
            if resource_records is not None:
                self._values["resource_records"] = resource_records
            if set_identifier is not None:
                self._values["set_identifier"] = set_identifier
            if ttl is not None:
                self._values["ttl"] = ttl
            if type is not None:
                self._values["type"] = type
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def alias_target(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordSetGroupPropsMixin.AliasTargetProperty"]]:
            '''*Alias resource record sets only:* Information about the AWS resource, such as a CloudFront distribution or an Amazon S3 bucket, that you want to route traffic to.

            If you're creating resource records sets for a private hosted zone, note the following:

            - You can't create an alias resource record set in a private hosted zone to route traffic to a CloudFront distribution.
            - For information about creating failover resource record sets in a private hosted zone, see `Configuring Failover in a Private Hosted Zone <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-private-hosted-zones.html>`_ in the *Amazon Route 53 Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-recordset.html#cfn-route53-recordsetgroup-recordset-aliastarget
            '''
            result = self._values.get("alias_target")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordSetGroupPropsMixin.AliasTargetProperty"]], result)

        @builtins.property
        def cidr_routing_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordSetGroupPropsMixin.CidrRoutingConfigProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-recordset.html#cfn-route53-recordsetgroup-recordset-cidrroutingconfig
            '''
            result = self._values.get("cidr_routing_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordSetGroupPropsMixin.CidrRoutingConfigProperty"]], result)

        @builtins.property
        def failover(self) -> typing.Optional[builtins.str]:
            '''*Failover resource record sets only:* To configure failover, you add the ``Failover`` element to two resource record sets.

            For one resource record set, you specify ``PRIMARY`` as the value for ``Failover`` ; for the other resource record set, you specify ``SECONDARY`` . In addition, you include the ``HealthCheckId`` element and specify the health check that you want Amazon Route 53 to perform for each resource record set.

            Except where noted, the following failover behaviors assume that you have included the ``HealthCheckId`` element in both resource record sets:

            - When the primary resource record set is healthy, Route 53 responds to DNS queries with the applicable value from the primary resource record set regardless of the health of the secondary resource record set.
            - When the primary resource record set is unhealthy and the secondary resource record set is healthy, Route 53 responds to DNS queries with the applicable value from the secondary resource record set.
            - When the secondary resource record set is unhealthy, Route 53 responds to DNS queries with the applicable value from the primary resource record set regardless of the health of the primary resource record set.
            - If you omit the ``HealthCheckId`` element for the secondary resource record set, and if the primary resource record set is unhealthy, Route 53 always responds to DNS queries with the applicable value from the secondary resource record set. This is true regardless of the health of the associated endpoint.

            You can't create non-failover resource record sets that have the same values for the ``Name`` and ``Type`` elements as failover resource record sets.

            For failover alias resource record sets, you must also include the ``EvaluateTargetHealth`` element and set the value to true.

            For more information about configuring failover for Route 53, see the following topics in the *Amazon Route 53 Developer Guide* :

            - `Route 53 Health Checks and DNS Failover <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html>`_
            - `Configuring Failover in a Private Hosted Zone <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-private-hosted-zones.html>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-recordset.html#cfn-route53-recordsetgroup-recordset-failover
            '''
            result = self._values.get("failover")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def geo_location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordSetGroupPropsMixin.GeoLocationProperty"]]:
            '''*Geolocation resource record sets only:* A complex type that lets you control how Amazon Route 53 responds to DNS queries based on the geographic origin of the query.

            For example, if you want all queries from Africa to be routed to a web server with an IP address of ``192.0.2.111`` , create a resource record set with a ``Type`` of ``A`` and a ``ContinentCode`` of ``AF`` .

            If you create separate resource record sets for overlapping geographic regions (for example, one resource record set for a continent and one for a country on the same continent), priority goes to the smallest geographic region. This allows you to route most queries for a continent to one resource and to route queries for a country on that continent to a different resource.

            You can't create two geolocation resource record sets that specify the same geographic location.

            The value ``*`` in the ``CountryCode`` element matches all geographic locations that aren't specified in other geolocation resource record sets that have the same values for the ``Name`` and ``Type`` elements.
            .. epigraph::

               Geolocation works by mapping IP addresses to locations. However, some IP addresses aren't mapped to geographic locations, so even if you create geolocation resource record sets that cover all seven continents, Route 53 will receive some DNS queries from locations that it can't identify. We recommend that you create a resource record set for which the value of ``CountryCode`` is ``*`` . Two groups of queries are routed to the resource that you specify in this record: queries that come from locations for which you haven't created geolocation resource record sets and queries from IP addresses that aren't mapped to a location. If you don't create a ``*`` resource record set, Route 53 returns a "no answer" response for queries from those locations.

            You can't create non-geolocation resource record sets that have the same values for the ``Name`` and ``Type`` elements as geolocation resource record sets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-recordset.html#cfn-route53-recordsetgroup-recordset-geolocation
            '''
            result = self._values.get("geo_location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordSetGroupPropsMixin.GeoLocationProperty"]], result)

        @builtins.property
        def geo_proximity_location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordSetGroupPropsMixin.GeoProximityLocationProperty"]]:
            '''A complex type that contains information about a geographic location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-recordset.html#cfn-route53-recordsetgroup-recordset-geoproximitylocation
            '''
            result = self._values.get("geo_proximity_location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordSetGroupPropsMixin.GeoProximityLocationProperty"]], result)

        @builtins.property
        def health_check_id(self) -> typing.Optional[builtins.str]:
            '''If you want Amazon Route 53 to return this resource record set in response to a DNS query only when the status of a health check is healthy, include the ``HealthCheckId`` element and specify the ID of the applicable health check.

            Route 53 determines whether a resource record set is healthy based on one of the following:

            - By periodically sending a request to the endpoint that is specified in the health check
            - By aggregating the status of a specified group of health checks (calculated health checks)
            - By determining the current state of a CloudWatch alarm (CloudWatch metric health checks)

            .. epigraph::

               Route 53 doesn't check the health of the endpoint that is specified in the resource record set, for example, the endpoint specified by the IP address in the ``Value`` element. When you add a ``HealthCheckId`` element to a resource record set, Route 53 checks the health of the endpoint that you specified in the health check.

            For more information, see the following topics in the *Amazon Route 53 Developer Guide* :

            - `How Amazon Route 53 Determines Whether an Endpoint Is Healthy <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-determining-health-of-endpoints.html>`_
            - `Route 53 Health Checks and DNS Failover <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html>`_
            - `Configuring Failover in a Private Hosted Zone <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-private-hosted-zones.html>`_

            *When to Specify HealthCheckId*

            Specifying a value for ``HealthCheckId`` is useful only when Route 53 is choosing between two or more resource record sets to respond to a DNS query, and you want Route 53 to base the choice in part on the status of a health check. Configuring health checks makes sense only in the following configurations:

            - *Non-alias resource record sets* : You're checking the health of a group of non-alias resource record sets that have the same routing policy, name, and type (such as multiple weighted records named www.example.com with a type of A) and you specify health check IDs for all the resource record sets.

            If the health check status for a resource record set is healthy, Route 53 includes the record among the records that it responds to DNS queries with.

            If the health check status for a resource record set is unhealthy, Route 53 stops responding to DNS queries using the value for that resource record set.

            If the health check status for all resource record sets in the group is unhealthy, Route 53 considers all resource record sets in the group healthy and responds to DNS queries accordingly.

            - *Alias resource record sets* : You specify the following settings:
            - You set ``EvaluateTargetHealth`` to true for an alias resource record set in a group of resource record sets that have the same routing policy, name, and type (such as multiple weighted records named www.example.com with a type of A).
            - You configure the alias resource record set to route traffic to a non-alias resource record set in the same hosted zone.
            - You specify a health check ID for the non-alias resource record set.

            If the health check status is healthy, Route 53 considers the alias resource record set to be healthy and includes the alias record among the records that it responds to DNS queries with.

            If the health check status is unhealthy, Route 53 stops responding to DNS queries using the alias resource record set.
            .. epigraph::

               The alias resource record set can also route traffic to a *group* of non-alias resource record sets that have the same routing policy, name, and type. In that configuration, associate health checks with all of the resource record sets in the group of non-alias resource record sets.

            *Geolocation Routing*

            For geolocation resource record sets, if an endpoint is unhealthy, Route 53 looks for a resource record set for the larger, associated geographic region. For example, suppose you have resource record sets for a state in the United States, for the entire United States, for North America, and a resource record set that has ``*`` for ``CountryCode`` is ``*`` , which applies to all locations. If the endpoint for the state resource record set is unhealthy, Route 53 checks for healthy resource record sets in the following order until it finds a resource record set for which the endpoint is healthy:

            - The United States
            - North America
            - The default resource record set

            *Specifying the Health Check Endpoint by Domain Name*

            If your health checks specify the endpoint only by domain name, we recommend that you create a separate health check for each endpoint. For example, create a health check for each ``HTTP`` server that is serving content for ``www.example.com`` . For the value of ``FullyQualifiedDomainName`` , specify the domain name of the server (such as ``us-east-2-www.example.com`` ), not the name of the resource record sets ( ``www.example.com`` ).
            .. epigraph::

               Health check results will be unpredictable if you do the following:

               - Create a health check that has the same value for ``FullyQualifiedDomainName`` as the name of a resource record set.
               - Associate that health check with the resource record set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-recordset.html#cfn-route53-recordsetgroup-recordset-healthcheckid
            '''
            result = self._values.get("health_check_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hosted_zone_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the hosted zone that you want to create records in.

            Specify either ``HostedZoneName`` or ``HostedZoneId`` , but not both. If you have multiple hosted zones with the same domain name, you must specify the hosted zone using ``HostedZoneId`` .

            Do not provide the ``HostedZoneId`` if it is already defined in ``AWS::Route53::RecordSetGroup`` . The creation fails if ``HostedZoneId`` is defined in both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-recordset.html#cfn-route53-recordsetgroup-recordset-hostedzoneid
            '''
            result = self._values.get("hosted_zone_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hosted_zone_name(self) -> typing.Optional[builtins.str]:
            '''The name of the hosted zone that you want to create records in.

            You must include a trailing dot (for example, ``www.example.com.`` ) as part of the ``HostedZoneName`` .

            When you create a stack using an ``AWS::Route53::RecordSet`` that specifies ``HostedZoneName`` , AWS CloudFormation attempts to find a hosted zone whose name matches the ``HostedZoneName`` . If AWS CloudFormation can't find a hosted zone with a matching domain name, or if there is more than one hosted zone with the specified domain name, AWS CloudFormation will not create the stack.

            Specify either ``HostedZoneName`` or ``HostedZoneId`` , but not both. If you have multiple hosted zones with the same domain name, you must specify the hosted zone using ``HostedZoneId`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-recordset.html#cfn-route53-recordsetgroup-recordset-hostedzonename
            '''
            result = self._values.get("hosted_zone_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def multi_value_answer(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''*Multivalue answer resource record sets only* : To route traffic approximately randomly to multiple resources, such as web servers, create one multivalue answer record for each resource and specify ``true`` for ``MultiValueAnswer`` .

            Note the following:

            - If you associate a health check with a multivalue answer resource record set, Amazon Route 53 responds to DNS queries with the corresponding IP address only when the health check is healthy.
            - If you don't associate a health check with a multivalue answer record, Route 53 always considers the record to be healthy.
            - Route 53 responds to DNS queries with up to eight healthy records; if you have eight or fewer healthy records, Route 53 responds to all DNS queries with all the healthy records.
            - If you have more than eight healthy records, Route 53 responds to different DNS resolvers with different combinations of healthy records.
            - When all records are unhealthy, Route 53 responds to DNS queries with up to eight unhealthy records.
            - If a resource becomes unavailable after a resolver caches a response, client software typically tries another of the IP addresses in the response.

            You can't create multivalue answer alias records.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-recordset.html#cfn-route53-recordsetgroup-recordset-multivalueanswer
            '''
            result = self._values.get("multi_value_answer")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the record that you want to create, update, or delete.

            Enter a fully qualified domain name, for example, ``www.example.com`` . You can optionally include a trailing dot. If you omit the trailing dot, Amazon Route 53 assumes that the domain name that you specify is fully qualified. This means that Route 53 treats ``www.example.com`` (without a trailing dot) and ``www.example.com.`` (with a trailing dot) as identical.

            For information about how to specify characters other than ``a-z`` , ``0-9`` , and ``-`` (hyphen) and how to specify internationalized domain names, see `DNS Domain Name Format <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/DomainNameFormat.html>`_ in the *Amazon Route 53 Developer Guide* .

            You can use the asterisk (*) wildcard to replace the leftmost label in a domain name, for example, ``*.example.com`` . Note the following:

            - The * must replace the entire label. For example, you can't specify ``*prod.example.com`` or ``prod*.example.com`` .
            - The * can't replace any of the middle labels, for example, marketing.*.example.com.
            - If you include * in any position other than the leftmost label in a domain name, DNS treats it as an * character (ASCII 42), not as a wildcard.

            .. epigraph::

               You can't use the * wildcard for resource records sets that have a type of NS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-recordset.html#cfn-route53-recordsetgroup-recordset-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''*Latency-based resource record sets only:* The Amazon EC2 Region where you created the resource that this resource record set refers to.

            The resource typically is an AWS resource, such as an EC2 instance or an ELB load balancer, and is referred to by an IP address or a DNS domain name, depending on the record type.

            When Amazon Route 53 receives a DNS query for a domain name and type for which you have created latency resource record sets, Route 53 selects the latency resource record set that has the lowest latency between the end user and the associated Amazon EC2 Region. Route 53 then returns the value that is associated with the selected resource record set.

            Note the following:

            - You can only specify one ``ResourceRecord`` per latency resource record set.
            - You can only create one latency resource record set for each Amazon EC2 Region.
            - You aren't required to create latency resource record sets for all Amazon EC2 Regions. Route 53 will choose the region with the best latency from among the regions that you create latency resource record sets for.
            - You can't create non-latency resource record sets that have the same values for the ``Name`` and ``Type`` elements as latency resource record sets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-recordset.html#cfn-route53-recordsetgroup-recordset-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_records(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Information about the records that you want to create.

            Each record should be in the format appropriate for the record type specified by the ``Type`` property. For information about different record types and their record formats, see `Values That You Specify When You Create or Edit Amazon Route 53 Records <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-values.html>`_ in the *Amazon Route 53 Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-recordset.html#cfn-route53-recordsetgroup-recordset-resourcerecords
            '''
            result = self._values.get("resource_records")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def set_identifier(self) -> typing.Optional[builtins.str]:
            '''*Resource record sets that have a routing policy other than simple:* An identifier that differentiates among multiple resource record sets that have the same combination of name and type, such as multiple weighted resource record sets named acme.example.com that have a type of A. In a group of resource record sets that have the same name and type, the value of ``SetIdentifier`` must be unique for each resource record set.

            For information about routing policies, see `Choosing a Routing Policy <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html>`_ in the *Amazon Route 53 Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-recordset.html#cfn-route53-recordsetgroup-recordset-setidentifier
            '''
            result = self._values.get("set_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ttl(self) -> typing.Optional[builtins.str]:
            '''The resource record cache time to live (TTL), in seconds. Note the following:.

            - If you're creating or updating an alias resource record set, omit ``TTL`` . Amazon Route 53 uses the value of ``TTL`` for the alias target.
            - If you're associating this resource record set with a health check (if you're adding a ``HealthCheckId`` element), we recommend that you specify a ``TTL`` of 60 seconds or less so clients respond quickly to changes in health status.
            - All of the resource record sets in a group of weighted resource record sets must have the same value for ``TTL`` .
            - If a group of weighted resource record sets includes one or more weighted alias resource record sets for which the alias target is an ELB load balancer, we recommend that you specify a ``TTL`` of 60 seconds for all of the non-alias weighted resource record sets that have the same name and type. Values other than 60 seconds (the TTL for load balancers) will change the effect of the values that you specify for ``Weight`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-recordset.html#cfn-route53-recordsetgroup-recordset-ttl
            '''
            result = self._values.get("ttl")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The DNS record type.

            For information about different record types and how data is encoded for them, see `Supported DNS Resource Record Types <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/ResourceRecordTypes.html>`_ in the *Amazon Route 53 Developer Guide* .

            Valid values for basic resource record sets: ``A`` | ``AAAA`` | ``CAA`` | ``CNAME`` | ``DS`` | ``MX`` | ``NAPTR`` | ``NS`` | ``PTR`` | ``SOA`` | ``SPF`` | ``SRV`` | ``TXT`` | ``TLSA`` | ``SSHFP`` | ``SVCB`` | ``HTTPS``

            Values for weighted, latency, geolocation, and failover resource record sets: ``A`` | ``AAAA`` | ``CAA`` | ``CNAME`` | ``MX`` | ``NAPTR`` | ``PTR`` | ``SPF`` | ``SRV`` | ``TXT`` | ``TLSA`` | ``SSHFP`` | ``SVCB`` | ``HTTPS`` . When creating a group of weighted, latency, geolocation, or failover resource record sets, specify the same value for all of the resource record sets in the group.

            Valid values for multivalue answer resource record sets: ``A`` | ``AAAA`` | ``MX`` | ``NAPTR`` | ``PTR`` | ``SPF`` | ``SRV`` | ``TXT`` | ``CAA`` | ``TLSA`` | ``SSHFP`` | ``SVCB`` | ``HTTPS``
            .. epigraph::

               SPF records were formerly used to verify the identity of the sender of email messages. However, we no longer recommend that you create resource record sets for which the value of ``Type`` is ``SPF`` . RFC 7208, *Sender Policy Framework (SPF) for Authorizing Use of Domains in Email, Version 1* , has been updated to say, "...[I]ts existence and mechanism defined in [RFC4408] have led to some interoperability issues. Accordingly, its use is no longer appropriate for SPF version 1; implementations are not to use it." In RFC 7208, see section 14.1, `The SPF DNS Record Type <https://docs.aws.amazon.com/http://tools.ietf.org/html/rfc7208#section-14.1>`_ .

            Values for alias resource record sets:

            - *Amazon API Gateway custom regional APIs and edge-optimized APIs:* ``A``
            - *CloudFront distributions:* ``A``

            If IPv6 is enabled for the distribution, create two resource record sets to route traffic to your distribution, one with a value of ``A`` and one with a value of ``AAAA`` .

            - *Amazon API Gateway environment that has a regionalized subdomain* : ``A``
            - *ELB load balancers:* ``A`` | ``AAAA``
            - *Amazon S3 buckets:* ``A``
            - *Amazon Virtual Private Cloud interface VPC endpoints* ``A``
            - *Another resource record set in this hosted zone:* Specify the type of the resource record set that you're creating the alias for. All values are supported except ``NS`` and ``SOA`` .

            .. epigraph::

               If you're creating an alias record that has the same name as the hosted zone (known as the zone apex), you can't route traffic to a record for which the value of ``Type`` is ``CNAME`` . This is because the alias record must have the same type as the record you're routing traffic to, and creating a CNAME record for the zone apex isn't supported even for an alias record.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-recordset.html#cfn-route53-recordsetgroup-recordset-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            '''*Weighted resource record sets only:* Among resource record sets that have the same combination of DNS name and type, a value that determines the proportion of DNS queries that Amazon Route 53 responds to using the current resource record set.

            Route 53 calculates the sum of the weights for the resource record sets that have the same combination of DNS name and type. Route 53 then responds to queries based on the ratio of a resource's weight to the total. Note the following:

            - You must specify a value for the ``Weight`` element for every weighted resource record set.
            - You can only specify one ``ResourceRecord`` per weighted resource record set.
            - You can't create latency, failover, or geolocation resource record sets that have the same values for the ``Name`` and ``Type`` elements as weighted resource record sets.
            - You can create a maximum of 100 weighted resource record sets that have the same values for the ``Name`` and ``Type`` elements.
            - For weighted (but not weighted alias) resource record sets, if you set ``Weight`` to ``0`` for a resource record set, Route 53 never responds to queries with the applicable value for that resource record set. However, if you set ``Weight`` to ``0`` for all resource record sets that have the same combination of DNS name and type, traffic is routed to all resources with equal probability.

            The effect of setting ``Weight`` to ``0`` is different when you associate health checks with weighted resource record sets. For more information, see `Options for Configuring Route 53 Active-Active and Active-Passive Failover <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-configuring-options.html>`_ in the *Amazon Route 53 Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordsetgroup-recordset.html#cfn-route53-recordsetgroup-recordset-weight
            '''
            result = self._values.get("weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecordSetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnRecordSetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "alias_target": "aliasTarget",
        "cidr_routing_config": "cidrRoutingConfig",
        "comment": "comment",
        "failover": "failover",
        "geo_location": "geoLocation",
        "geo_proximity_location": "geoProximityLocation",
        "health_check_id": "healthCheckId",
        "hosted_zone_id": "hostedZoneId",
        "hosted_zone_name": "hostedZoneName",
        "multi_value_answer": "multiValueAnswer",
        "name": "name",
        "region": "region",
        "resource_records": "resourceRecords",
        "set_identifier": "setIdentifier",
        "ttl": "ttl",
        "type": "type",
        "weight": "weight",
    },
)
class CfnRecordSetMixinProps:
    def __init__(
        self,
        *,
        alias_target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRecordSetPropsMixin.AliasTargetProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        cidr_routing_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRecordSetPropsMixin.CidrRoutingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        comment: typing.Optional[builtins.str] = None,
        failover: typing.Optional[builtins.str] = None,
        geo_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRecordSetPropsMixin.GeoLocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        geo_proximity_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRecordSetPropsMixin.GeoProximityLocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        health_check_id: typing.Optional[builtins.str] = None,
        hosted_zone_id: typing.Optional[builtins.str] = None,
        hosted_zone_name: typing.Optional[builtins.str] = None,
        multi_value_answer: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        resource_records: typing.Optional[typing.Sequence[builtins.str]] = None,
        set_identifier: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for CfnRecordSetPropsMixin.

        :param alias_target: *Alias resource record sets only:* Information about the AWS resource, such as a CloudFront distribution or an Amazon S3 bucket, that you want to route traffic to. If you're creating resource records sets for a private hosted zone, note the following: - You can't create an alias resource record set in a private hosted zone to route traffic to a CloudFront distribution. - For information about creating failover resource record sets in a private hosted zone, see `Configuring Failover in a Private Hosted Zone <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-private-hosted-zones.html>`_ in the *Amazon Route 53 Developer Guide* .
        :param cidr_routing_config: The object that is specified in resource record set object when you are linking a resource record set to a CIDR location. A ``LocationName`` with an asterisk “*” can be used to create a default CIDR record. ``CollectionId`` is still required for default record.
        :param comment: *Optional:* Any comments you want to include about a change batch request.
        :param failover: *Failover resource record sets only:* To configure failover, you add the ``Failover`` element to two resource record sets. For one resource record set, you specify ``PRIMARY`` as the value for ``Failover`` ; for the other resource record set, you specify ``SECONDARY`` . In addition, you include the ``HealthCheckId`` element and specify the health check that you want Amazon Route 53 to perform for each resource record set. Except where noted, the following failover behaviors assume that you have included the ``HealthCheckId`` element in both resource record sets: - When the primary resource record set is healthy, Route 53 responds to DNS queries with the applicable value from the primary resource record set regardless of the health of the secondary resource record set. - When the primary resource record set is unhealthy and the secondary resource record set is healthy, Route 53 responds to DNS queries with the applicable value from the secondary resource record set. - When the secondary resource record set is unhealthy, Route 53 responds to DNS queries with the applicable value from the primary resource record set regardless of the health of the primary resource record set. - If you omit the ``HealthCheckId`` element for the secondary resource record set, and if the primary resource record set is unhealthy, Route 53 always responds to DNS queries with the applicable value from the secondary resource record set. This is true regardless of the health of the associated endpoint. You can't create non-failover resource record sets that have the same values for the ``Name`` and ``Type`` elements as failover resource record sets. For failover alias resource record sets, you must also include the ``EvaluateTargetHealth`` element and set the value to true. For more information about configuring failover for Route 53, see the following topics in the *Amazon Route 53 Developer Guide* : - `Route 53 Health Checks and DNS Failover <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html>`_ - `Configuring Failover in a Private Hosted Zone <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-private-hosted-zones.html>`_
        :param geo_location: *Geolocation resource record sets only:* A complex type that lets you control how Amazon Route 53 responds to DNS queries based on the geographic origin of the query. For example, if you want all queries from Africa to be routed to a web server with an IP address of ``192.0.2.111`` , create a resource record set with a ``Type`` of ``A`` and a ``ContinentCode`` of ``AF`` . If you create separate resource record sets for overlapping geographic regions (for example, one resource record set for a continent and one for a country on the same continent), priority goes to the smallest geographic region. This allows you to route most queries for a continent to one resource and to route queries for a country on that continent to a different resource. You can't create two geolocation resource record sets that specify the same geographic location. The value ``*`` in the ``CountryCode`` element matches all geographic locations that aren't specified in other geolocation resource record sets that have the same values for the ``Name`` and ``Type`` elements. .. epigraph:: Geolocation works by mapping IP addresses to locations. However, some IP addresses aren't mapped to geographic locations, so even if you create geolocation resource record sets that cover all seven continents, Route 53 will receive some DNS queries from locations that it can't identify. We recommend that you create a resource record set for which the value of ``CountryCode`` is ``*`` . Two groups of queries are routed to the resource that you specify in this record: queries that come from locations for which you haven't created geolocation resource record sets and queries from IP addresses that aren't mapped to a location. If you don't create a ``*`` resource record set, Route 53 returns a "no answer" response for queries from those locations. You can't create non-geolocation resource record sets that have the same values for the ``Name`` and ``Type`` elements as geolocation resource record sets.
        :param geo_proximity_location: *GeoproximityLocation resource record sets only:* A complex type that lets you control how Route 53 responds to DNS queries based on the geographic origin of the query and your resources.
        :param health_check_id: If you want Amazon Route 53 to return this resource record set in response to a DNS query only when the status of a health check is healthy, include the ``HealthCheckId`` element and specify the ID of the applicable health check. Route 53 determines whether a resource record set is healthy based on one of the following: - By periodically sending a request to the endpoint that is specified in the health check - By aggregating the status of a specified group of health checks (calculated health checks) - By determining the current state of a CloudWatch alarm (CloudWatch metric health checks) .. epigraph:: Route 53 doesn't check the health of the endpoint that is specified in the resource record set, for example, the endpoint specified by the IP address in the ``Value`` element. When you add a ``HealthCheckId`` element to a resource record set, Route 53 checks the health of the endpoint that you specified in the health check. For more information, see the following topics in the *Amazon Route 53 Developer Guide* : - `How Amazon Route 53 Determines Whether an Endpoint Is Healthy <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-determining-health-of-endpoints.html>`_ - `Route 53 Health Checks and DNS Failover <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html>`_ - `Configuring Failover in a Private Hosted Zone <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-private-hosted-zones.html>`_ *When to Specify HealthCheckId* Specifying a value for ``HealthCheckId`` is useful only when Route 53 is choosing between two or more resource record sets to respond to a DNS query, and you want Route 53 to base the choice in part on the status of a health check. Configuring health checks makes sense only in the following configurations: - *Non-alias resource record sets* : You're checking the health of a group of non-alias resource record sets that have the same routing policy, name, and type (such as multiple weighted records named www.example.com with a type of A) and you specify health check IDs for all the resource record sets. If the health check status for a resource record set is healthy, Route 53 includes the record among the records that it responds to DNS queries with. If the health check status for a resource record set is unhealthy, Route 53 stops responding to DNS queries using the value for that resource record set. If the health check status for all resource record sets in the group is unhealthy, Route 53 considers all resource record sets in the group healthy and responds to DNS queries accordingly. - *Alias resource record sets* : You specify the following settings: - You set ``EvaluateTargetHealth`` to true for an alias resource record set in a group of resource record sets that have the same routing policy, name, and type (such as multiple weighted records named www.example.com with a type of A). - You configure the alias resource record set to route traffic to a non-alias resource record set in the same hosted zone. - You specify a health check ID for the non-alias resource record set. If the health check status is healthy, Route 53 considers the alias resource record set to be healthy and includes the alias record among the records that it responds to DNS queries with. If the health check status is unhealthy, Route 53 stops responding to DNS queries using the alias resource record set. .. epigraph:: The alias resource record set can also route traffic to a *group* of non-alias resource record sets that have the same routing policy, name, and type. In that configuration, associate health checks with all of the resource record sets in the group of non-alias resource record sets. *Geolocation Routing* For geolocation resource record sets, if an endpoint is unhealthy, Route 53 looks for a resource record set for the larger, associated geographic region. For example, suppose you have resource record sets for a state in the United States, for the entire United States, for North America, and a resource record set that has ``*`` for ``CountryCode`` is ``*`` , which applies to all locations. If the endpoint for the state resource record set is unhealthy, Route 53 checks for healthy resource record sets in the following order until it finds a resource record set for which the endpoint is healthy: - The United States - North America - The default resource record set *Specifying the Health Check Endpoint by Domain Name* If your health checks specify the endpoint only by domain name, we recommend that you create a separate health check for each endpoint. For example, create a health check for each ``HTTP`` server that is serving content for ``www.example.com`` . For the value of ``FullyQualifiedDomainName`` , specify the domain name of the server (such as ``us-east-2-www.example.com`` ), not the name of the resource record sets ( ``www.example.com`` ). .. epigraph:: Health check results will be unpredictable if you do the following: - Create a health check that has the same value for ``FullyQualifiedDomainName`` as the name of a resource record set. - Associate that health check with the resource record set.
        :param hosted_zone_id: The ID of the hosted zone that you want to create records in. Specify either ``HostedZoneName`` or ``HostedZoneId`` , but not both. If you have multiple hosted zones with the same domain name, you must specify the hosted zone using ``HostedZoneId`` .
        :param hosted_zone_name: The name of the hosted zone that you want to create records in. You must include a trailing dot (for example, ``www.example.com.`` ) as part of the ``HostedZoneName`` . When you create a stack using an AWS::Route53::RecordSet that specifies ``HostedZoneName`` , AWS CloudFormation attempts to find a hosted zone whose name matches the HostedZoneName. If AWS CloudFormation cannot find a hosted zone with a matching domain name, or if there is more than one hosted zone with the specified domain name, AWS CloudFormation will not create the stack. Specify either ``HostedZoneName`` or ``HostedZoneId`` , but not both. If you have multiple hosted zones with the same domain name, you must specify the hosted zone using ``HostedZoneId`` .
        :param multi_value_answer: *Multivalue answer resource record sets only* : To route traffic approximately randomly to multiple resources, such as web servers, create one multivalue answer record for each resource and specify ``true`` for ``MultiValueAnswer`` . Note the following: - If you associate a health check with a multivalue answer resource record set, Amazon Route 53 responds to DNS queries with the corresponding IP address only when the health check is healthy. - If you don't associate a health check with a multivalue answer record, Route 53 always considers the record to be healthy. - Route 53 responds to DNS queries with up to eight healthy records; if you have eight or fewer healthy records, Route 53 responds to all DNS queries with all the healthy records. - If you have more than eight healthy records, Route 53 responds to different DNS resolvers with different combinations of healthy records. - When all records are unhealthy, Route 53 responds to DNS queries with up to eight unhealthy records. - If a resource becomes unavailable after a resolver caches a response, client software typically tries another of the IP addresses in the response. You can't create multivalue answer alias records.
        :param name: The name of the record that you want to create, update, or delete. Enter a fully qualified domain name, for example, ``www.example.com`` . You can optionally include a trailing dot. If you omit the trailing dot, Amazon Route 53 assumes that the domain name that you specify is fully qualified. This means that Route 53 treats ``www.example.com`` (without a trailing dot) and ``www.example.com.`` (with a trailing dot) as identical. For information about how to specify characters other than ``a-z`` , ``0-9`` , and ``-`` (hyphen) and how to specify internationalized domain names, see `DNS Domain Name Format <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/DomainNameFormat.html>`_ in the *Amazon Route 53 Developer Guide* . You can use the asterisk (*) wildcard to replace the leftmost label in a domain name, for example, ``*.example.com`` . Note the following: - The * must replace the entire label. For example, you can't specify ``*prod.example.com`` or ``prod*.example.com`` . - The * can't replace any of the middle labels, for example, marketing.*.example.com. - If you include * in any position other than the leftmost label in a domain name, DNS treats it as an * character (ASCII 42), not as a wildcard. .. epigraph:: You can't use the * wildcard for resource records sets that have a type of NS.
        :param region: *Latency-based resource record sets only:* The Amazon EC2 Region where you created the resource that this resource record set refers to. The resource typically is an AWS resource, such as an EC2 instance or an ELB load balancer, and is referred to by an IP address or a DNS domain name, depending on the record type. When Amazon Route 53 receives a DNS query for a domain name and type for which you have created latency resource record sets, Route 53 selects the latency resource record set that has the lowest latency between the end user and the associated Amazon EC2 Region. Route 53 then returns the value that is associated with the selected resource record set. Note the following: - You can only specify one ``ResourceRecord`` per latency resource record set. - You can only create one latency resource record set for each Amazon EC2 Region. - You aren't required to create latency resource record sets for all Amazon EC2 Regions. Route 53 will choose the region with the best latency from among the regions that you create latency resource record sets for. - You can't create non-latency resource record sets that have the same values for the ``Name`` and ``Type`` elements as latency resource record sets.
        :param resource_records: One or more values that correspond with the value that you specified for the ``Type`` property. For example, if you specified ``A`` for ``Type`` , you specify one or more IP addresses in IPv4 format for ``ResourceRecords`` . For information about the format of values for each record type, see `Supported DNS Resource Record Types <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/ResourceRecordTypes.html>`_ in the *Amazon Route 53 Developer Guide* . Note the following: - You can specify more than one value for all record types except CNAME and SOA. - The maximum length of a value is 4000 characters. - If you're creating an alias record, omit ``ResourceRecords`` .
        :param set_identifier: *Resource record sets that have a routing policy other than simple:* An identifier that differentiates among multiple resource record sets that have the same combination of name and type, such as multiple weighted resource record sets named acme.example.com that have a type of A. In a group of resource record sets that have the same name and type, the value of ``SetIdentifier`` must be unique for each resource record set. For information about routing policies, see `Choosing a Routing Policy <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html>`_ in the *Amazon Route 53 Developer Guide* .
        :param ttl: The resource record cache time to live (TTL), in seconds. Note the following:. - If you're creating or updating an alias resource record set, omit ``TTL`` . Amazon Route 53 uses the value of ``TTL`` for the alias target. - If you're associating this resource record set with a health check (if you're adding a ``HealthCheckId`` element), we recommend that you specify a ``TTL`` of 60 seconds or less so clients respond quickly to changes in health status. - All of the resource record sets in a group of weighted resource record sets must have the same value for ``TTL`` . - If a group of weighted resource record sets includes one or more weighted alias resource record sets for which the alias target is an ELB load balancer, we recommend that you specify a ``TTL`` of 60 seconds for all of the non-alias weighted resource record sets that have the same name and type. Values other than 60 seconds (the TTL for load balancers) will change the effect of the values that you specify for ``Weight`` .
        :param type: The DNS record type. For information about different record types and how data is encoded for them, see `Supported DNS Resource Record Types <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/ResourceRecordTypes.html>`_ in the *Amazon Route 53 Developer Guide* . Valid values for basic resource record sets: ``A`` | ``AAAA`` | ``CAA`` | ``CNAME`` | ``DS`` | ``MX`` | ``NAPTR`` | ``NS`` | ``PTR`` | ``SOA`` | ``SPF`` | ``SRV`` | ``TXT`` | ``TLSA`` | ``SSHFP`` | ``SVCB`` | ``HTTPS`` Values for weighted, latency, geolocation, and failover resource record sets: ``A`` | ``AAAA`` | ``CAA`` | ``CNAME`` | ``MX`` | ``NAPTR`` | ``PTR`` | ``SPF`` | ``SRV`` | ``TXT`` | ``TLSA`` | ``SSHFP`` | ``SVCB`` | ``HTTPS`` . When creating a group of weighted, latency, geolocation, or failover resource record sets, specify the same value for all of the resource record sets in the group. Valid values for multivalue answer resource record sets: ``A`` | ``AAAA`` | ``MX`` | ``NAPTR`` | ``PTR`` | ``SPF`` | ``SRV`` | ``TXT`` | ``CAA`` | ``TLSA`` | ``SSHFP`` | ``SVCB`` | ``HTTPS`` .. epigraph:: SPF records were formerly used to verify the identity of the sender of email messages. However, we no longer recommend that you create resource record sets for which the value of ``Type`` is ``SPF`` . RFC 7208, *Sender Policy Framework (SPF) for Authorizing Use of Domains in Email, Version 1* , has been updated to say, "...[I]ts existence and mechanism defined in [RFC4408] have led to some interoperability issues. Accordingly, its use is no longer appropriate for SPF version 1; implementations are not to use it." In RFC 7208, see section 14.1, `The SPF DNS Record Type <https://docs.aws.amazon.com/http://tools.ietf.org/html/rfc7208#section-14.1>`_ . Values for alias resource record sets: - *Amazon API Gateway custom regional APIs and edge-optimized APIs:* ``A`` - *CloudFront distributions:* ``A`` If IPv6 is enabled for the distribution, create two resource record sets to route traffic to your distribution, one with a value of ``A`` and one with a value of ``AAAA`` . - *Amazon API Gateway environment that has a regionalized subdomain* : ``A`` - *ELB load balancers:* ``A`` | ``AAAA`` - *Amazon S3 buckets:* ``A`` - *Amazon Virtual Private Cloud interface VPC endpoints* ``A`` - *Another resource record set in this hosted zone:* Specify the type of the resource record set that you're creating the alias for. All values are supported except ``NS`` and ``SOA`` . .. epigraph:: If you're creating an alias record that has the same name as the hosted zone (known as the zone apex), you can't route traffic to a record for which the value of ``Type`` is ``CNAME`` . This is because the alias record must have the same type as the record you're routing traffic to, and creating a CNAME record for the zone apex isn't supported even for an alias record.
        :param weight: *Weighted resource record sets only:* Among resource record sets that have the same combination of DNS name and type, a value that determines the proportion of DNS queries that Amazon Route 53 responds to using the current resource record set. Route 53 calculates the sum of the weights for the resource record sets that have the same combination of DNS name and type. Route 53 then responds to queries based on the ratio of a resource's weight to the total. Note the following: - You must specify a value for the ``Weight`` element for every weighted resource record set. - You can only specify one ``ResourceRecord`` per weighted resource record set. - You can't create latency, failover, or geolocation resource record sets that have the same values for the ``Name`` and ``Type`` elements as weighted resource record sets. - You can create a maximum of 100 weighted resource record sets that have the same values for the ``Name`` and ``Type`` elements. - For weighted (but not weighted alias) resource record sets, if you set ``Weight`` to ``0`` for a resource record set, Route 53 never responds to queries with the applicable value for that resource record set. However, if you set ``Weight`` to ``0`` for all resource record sets that have the same combination of DNS name and type, traffic is routed to all resources with equal probability. The effect of setting ``Weight`` to ``0`` is different when you associate health checks with weighted resource record sets. For more information, see `Options for Configuring Route 53 Active-Active and Active-Passive Failover <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-configuring-options.html>`_ in the *Amazon Route 53 Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
            
            cfn_record_set_mixin_props = route53_mixins.CfnRecordSetMixinProps(
                alias_target=route53_mixins.CfnRecordSetPropsMixin.AliasTargetProperty(
                    dns_name="dnsName",
                    evaluate_target_health=False,
                    hosted_zone_id="hostedZoneId"
                ),
                cidr_routing_config=route53_mixins.CfnRecordSetPropsMixin.CidrRoutingConfigProperty(
                    collection_id="collectionId",
                    location_name="locationName"
                ),
                comment="comment",
                failover="failover",
                geo_location=route53_mixins.CfnRecordSetPropsMixin.GeoLocationProperty(
                    continent_code="continentCode",
                    country_code="countryCode",
                    subdivision_code="subdivisionCode"
                ),
                geo_proximity_location=route53_mixins.CfnRecordSetPropsMixin.GeoProximityLocationProperty(
                    aws_region="awsRegion",
                    bias=123,
                    coordinates=route53_mixins.CfnRecordSetPropsMixin.CoordinatesProperty(
                        latitude="latitude",
                        longitude="longitude"
                    ),
                    local_zone_group="localZoneGroup"
                ),
                health_check_id="healthCheckId",
                hosted_zone_id="hostedZoneId",
                hosted_zone_name="hostedZoneName",
                multi_value_answer=False,
                name="name",
                region="region",
                resource_records=["resourceRecords"],
                set_identifier="setIdentifier",
                ttl="ttl",
                type="type",
                weight=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__237deea5889fe21fbc58a2f5eaad425c47f7a4b413b44bec068d8c608d289d2e)
            check_type(argname="argument alias_target", value=alias_target, expected_type=type_hints["alias_target"])
            check_type(argname="argument cidr_routing_config", value=cidr_routing_config, expected_type=type_hints["cidr_routing_config"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument failover", value=failover, expected_type=type_hints["failover"])
            check_type(argname="argument geo_location", value=geo_location, expected_type=type_hints["geo_location"])
            check_type(argname="argument geo_proximity_location", value=geo_proximity_location, expected_type=type_hints["geo_proximity_location"])
            check_type(argname="argument health_check_id", value=health_check_id, expected_type=type_hints["health_check_id"])
            check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
            check_type(argname="argument hosted_zone_name", value=hosted_zone_name, expected_type=type_hints["hosted_zone_name"])
            check_type(argname="argument multi_value_answer", value=multi_value_answer, expected_type=type_hints["multi_value_answer"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument resource_records", value=resource_records, expected_type=type_hints["resource_records"])
            check_type(argname="argument set_identifier", value=set_identifier, expected_type=type_hints["set_identifier"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias_target is not None:
            self._values["alias_target"] = alias_target
        if cidr_routing_config is not None:
            self._values["cidr_routing_config"] = cidr_routing_config
        if comment is not None:
            self._values["comment"] = comment
        if failover is not None:
            self._values["failover"] = failover
        if geo_location is not None:
            self._values["geo_location"] = geo_location
        if geo_proximity_location is not None:
            self._values["geo_proximity_location"] = geo_proximity_location
        if health_check_id is not None:
            self._values["health_check_id"] = health_check_id
        if hosted_zone_id is not None:
            self._values["hosted_zone_id"] = hosted_zone_id
        if hosted_zone_name is not None:
            self._values["hosted_zone_name"] = hosted_zone_name
        if multi_value_answer is not None:
            self._values["multi_value_answer"] = multi_value_answer
        if name is not None:
            self._values["name"] = name
        if region is not None:
            self._values["region"] = region
        if resource_records is not None:
            self._values["resource_records"] = resource_records
        if set_identifier is not None:
            self._values["set_identifier"] = set_identifier
        if ttl is not None:
            self._values["ttl"] = ttl
        if type is not None:
            self._values["type"] = type
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def alias_target(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordSetPropsMixin.AliasTargetProperty"]]:
        '''*Alias resource record sets only:* Information about the AWS resource, such as a CloudFront distribution or an Amazon S3 bucket, that you want to route traffic to.

        If you're creating resource records sets for a private hosted zone, note the following:

        - You can't create an alias resource record set in a private hosted zone to route traffic to a CloudFront distribution.
        - For information about creating failover resource record sets in a private hosted zone, see `Configuring Failover in a Private Hosted Zone <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-private-hosted-zones.html>`_ in the *Amazon Route 53 Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordset.html#cfn-route53-recordset-aliastarget
        '''
        result = self._values.get("alias_target")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordSetPropsMixin.AliasTargetProperty"]], result)

    @builtins.property
    def cidr_routing_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordSetPropsMixin.CidrRoutingConfigProperty"]]:
        '''The object that is specified in resource record set object when you are linking a resource record set to a CIDR location.

        A ``LocationName`` with an asterisk “*” can be used to create a default CIDR record. ``CollectionId`` is still required for default record.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordset.html#cfn-route53-recordset-cidrroutingconfig
        '''
        result = self._values.get("cidr_routing_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordSetPropsMixin.CidrRoutingConfigProperty"]], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''*Optional:* Any comments you want to include about a change batch request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordset.html#cfn-route53-recordset-comment
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failover(self) -> typing.Optional[builtins.str]:
        '''*Failover resource record sets only:* To configure failover, you add the ``Failover`` element to two resource record sets.

        For one resource record set, you specify ``PRIMARY`` as the value for ``Failover`` ; for the other resource record set, you specify ``SECONDARY`` . In addition, you include the ``HealthCheckId`` element and specify the health check that you want Amazon Route 53 to perform for each resource record set.

        Except where noted, the following failover behaviors assume that you have included the ``HealthCheckId`` element in both resource record sets:

        - When the primary resource record set is healthy, Route 53 responds to DNS queries with the applicable value from the primary resource record set regardless of the health of the secondary resource record set.
        - When the primary resource record set is unhealthy and the secondary resource record set is healthy, Route 53 responds to DNS queries with the applicable value from the secondary resource record set.
        - When the secondary resource record set is unhealthy, Route 53 responds to DNS queries with the applicable value from the primary resource record set regardless of the health of the primary resource record set.
        - If you omit the ``HealthCheckId`` element for the secondary resource record set, and if the primary resource record set is unhealthy, Route 53 always responds to DNS queries with the applicable value from the secondary resource record set. This is true regardless of the health of the associated endpoint.

        You can't create non-failover resource record sets that have the same values for the ``Name`` and ``Type`` elements as failover resource record sets.

        For failover alias resource record sets, you must also include the ``EvaluateTargetHealth`` element and set the value to true.

        For more information about configuring failover for Route 53, see the following topics in the *Amazon Route 53 Developer Guide* :

        - `Route 53 Health Checks and DNS Failover <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html>`_
        - `Configuring Failover in a Private Hosted Zone <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-private-hosted-zones.html>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordset.html#cfn-route53-recordset-failover
        '''
        result = self._values.get("failover")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def geo_location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordSetPropsMixin.GeoLocationProperty"]]:
        '''*Geolocation resource record sets only:* A complex type that lets you control how Amazon Route 53 responds to DNS queries based on the geographic origin of the query.

        For example, if you want all queries from Africa to be routed to a web server with an IP address of ``192.0.2.111`` , create a resource record set with a ``Type`` of ``A`` and a ``ContinentCode`` of ``AF`` .

        If you create separate resource record sets for overlapping geographic regions (for example, one resource record set for a continent and one for a country on the same continent), priority goes to the smallest geographic region. This allows you to route most queries for a continent to one resource and to route queries for a country on that continent to a different resource.

        You can't create two geolocation resource record sets that specify the same geographic location.

        The value ``*`` in the ``CountryCode`` element matches all geographic locations that aren't specified in other geolocation resource record sets that have the same values for the ``Name`` and ``Type`` elements.
        .. epigraph::

           Geolocation works by mapping IP addresses to locations. However, some IP addresses aren't mapped to geographic locations, so even if you create geolocation resource record sets that cover all seven continents, Route 53 will receive some DNS queries from locations that it can't identify. We recommend that you create a resource record set for which the value of ``CountryCode`` is ``*`` . Two groups of queries are routed to the resource that you specify in this record: queries that come from locations for which you haven't created geolocation resource record sets and queries from IP addresses that aren't mapped to a location. If you don't create a ``*`` resource record set, Route 53 returns a "no answer" response for queries from those locations.

        You can't create non-geolocation resource record sets that have the same values for the ``Name`` and ``Type`` elements as geolocation resource record sets.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordset.html#cfn-route53-recordset-geolocation
        '''
        result = self._values.get("geo_location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordSetPropsMixin.GeoLocationProperty"]], result)

    @builtins.property
    def geo_proximity_location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordSetPropsMixin.GeoProximityLocationProperty"]]:
        '''*GeoproximityLocation resource record sets only:* A complex type that lets you control how Route 53 responds to DNS queries based on the geographic origin of the query and your resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordset.html#cfn-route53-recordset-geoproximitylocation
        '''
        result = self._values.get("geo_proximity_location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordSetPropsMixin.GeoProximityLocationProperty"]], result)

    @builtins.property
    def health_check_id(self) -> typing.Optional[builtins.str]:
        '''If you want Amazon Route 53 to return this resource record set in response to a DNS query only when the status of a health check is healthy, include the ``HealthCheckId`` element and specify the ID of the applicable health check.

        Route 53 determines whether a resource record set is healthy based on one of the following:

        - By periodically sending a request to the endpoint that is specified in the health check
        - By aggregating the status of a specified group of health checks (calculated health checks)
        - By determining the current state of a CloudWatch alarm (CloudWatch metric health checks)

        .. epigraph::

           Route 53 doesn't check the health of the endpoint that is specified in the resource record set, for example, the endpoint specified by the IP address in the ``Value`` element. When you add a ``HealthCheckId`` element to a resource record set, Route 53 checks the health of the endpoint that you specified in the health check.

        For more information, see the following topics in the *Amazon Route 53 Developer Guide* :

        - `How Amazon Route 53 Determines Whether an Endpoint Is Healthy <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-determining-health-of-endpoints.html>`_
        - `Route 53 Health Checks and DNS Failover <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html>`_
        - `Configuring Failover in a Private Hosted Zone <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-private-hosted-zones.html>`_

        *When to Specify HealthCheckId*

        Specifying a value for ``HealthCheckId`` is useful only when Route 53 is choosing between two or more resource record sets to respond to a DNS query, and you want Route 53 to base the choice in part on the status of a health check. Configuring health checks makes sense only in the following configurations:

        - *Non-alias resource record sets* : You're checking the health of a group of non-alias resource record sets that have the same routing policy, name, and type (such as multiple weighted records named www.example.com with a type of A) and you specify health check IDs for all the resource record sets.

        If the health check status for a resource record set is healthy, Route 53 includes the record among the records that it responds to DNS queries with.

        If the health check status for a resource record set is unhealthy, Route 53 stops responding to DNS queries using the value for that resource record set.

        If the health check status for all resource record sets in the group is unhealthy, Route 53 considers all resource record sets in the group healthy and responds to DNS queries accordingly.

        - *Alias resource record sets* : You specify the following settings:
        - You set ``EvaluateTargetHealth`` to true for an alias resource record set in a group of resource record sets that have the same routing policy, name, and type (such as multiple weighted records named www.example.com with a type of A).
        - You configure the alias resource record set to route traffic to a non-alias resource record set in the same hosted zone.
        - You specify a health check ID for the non-alias resource record set.

        If the health check status is healthy, Route 53 considers the alias resource record set to be healthy and includes the alias record among the records that it responds to DNS queries with.

        If the health check status is unhealthy, Route 53 stops responding to DNS queries using the alias resource record set.
        .. epigraph::

           The alias resource record set can also route traffic to a *group* of non-alias resource record sets that have the same routing policy, name, and type. In that configuration, associate health checks with all of the resource record sets in the group of non-alias resource record sets.

        *Geolocation Routing*

        For geolocation resource record sets, if an endpoint is unhealthy, Route 53 looks for a resource record set for the larger, associated geographic region. For example, suppose you have resource record sets for a state in the United States, for the entire United States, for North America, and a resource record set that has ``*`` for ``CountryCode`` is ``*`` , which applies to all locations. If the endpoint for the state resource record set is unhealthy, Route 53 checks for healthy resource record sets in the following order until it finds a resource record set for which the endpoint is healthy:

        - The United States
        - North America
        - The default resource record set

        *Specifying the Health Check Endpoint by Domain Name*

        If your health checks specify the endpoint only by domain name, we recommend that you create a separate health check for each endpoint. For example, create a health check for each ``HTTP`` server that is serving content for ``www.example.com`` . For the value of ``FullyQualifiedDomainName`` , specify the domain name of the server (such as ``us-east-2-www.example.com`` ), not the name of the resource record sets ( ``www.example.com`` ).
        .. epigraph::

           Health check results will be unpredictable if you do the following:

           - Create a health check that has the same value for ``FullyQualifiedDomainName`` as the name of a resource record set.
           - Associate that health check with the resource record set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordset.html#cfn-route53-recordset-healthcheckid
        '''
        result = self._values.get("health_check_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hosted_zone_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the hosted zone that you want to create records in.

        Specify either ``HostedZoneName`` or ``HostedZoneId`` , but not both. If you have multiple hosted zones with the same domain name, you must specify the hosted zone using ``HostedZoneId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordset.html#cfn-route53-recordset-hostedzoneid
        '''
        result = self._values.get("hosted_zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hosted_zone_name(self) -> typing.Optional[builtins.str]:
        '''The name of the hosted zone that you want to create records in.

        You must include a trailing dot (for example, ``www.example.com.`` ) as part of the ``HostedZoneName`` .

        When you create a stack using an AWS::Route53::RecordSet that specifies ``HostedZoneName`` , AWS CloudFormation attempts to find a hosted zone whose name matches the HostedZoneName. If AWS CloudFormation cannot find a hosted zone with a matching domain name, or if there is more than one hosted zone with the specified domain name, AWS CloudFormation will not create the stack.

        Specify either ``HostedZoneName`` or ``HostedZoneId`` , but not both. If you have multiple hosted zones with the same domain name, you must specify the hosted zone using ``HostedZoneId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordset.html#cfn-route53-recordset-hostedzonename
        '''
        result = self._values.get("hosted_zone_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multi_value_answer(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''*Multivalue answer resource record sets only* : To route traffic approximately randomly to multiple resources, such as web servers, create one multivalue answer record for each resource and specify ``true`` for ``MultiValueAnswer`` .

        Note the following:

        - If you associate a health check with a multivalue answer resource record set, Amazon Route 53 responds to DNS queries with the corresponding IP address only when the health check is healthy.
        - If you don't associate a health check with a multivalue answer record, Route 53 always considers the record to be healthy.
        - Route 53 responds to DNS queries with up to eight healthy records; if you have eight or fewer healthy records, Route 53 responds to all DNS queries with all the healthy records.
        - If you have more than eight healthy records, Route 53 responds to different DNS resolvers with different combinations of healthy records.
        - When all records are unhealthy, Route 53 responds to DNS queries with up to eight unhealthy records.
        - If a resource becomes unavailable after a resolver caches a response, client software typically tries another of the IP addresses in the response.

        You can't create multivalue answer alias records.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordset.html#cfn-route53-recordset-multivalueanswer
        '''
        result = self._values.get("multi_value_answer")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the record that you want to create, update, or delete.

        Enter a fully qualified domain name, for example, ``www.example.com`` . You can optionally include a trailing dot. If you omit the trailing dot, Amazon Route 53 assumes that the domain name that you specify is fully qualified. This means that Route 53 treats ``www.example.com`` (without a trailing dot) and ``www.example.com.`` (with a trailing dot) as identical.

        For information about how to specify characters other than ``a-z`` , ``0-9`` , and ``-`` (hyphen) and how to specify internationalized domain names, see `DNS Domain Name Format <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/DomainNameFormat.html>`_ in the *Amazon Route 53 Developer Guide* .

        You can use the asterisk (*) wildcard to replace the leftmost label in a domain name, for example, ``*.example.com`` . Note the following:

        - The * must replace the entire label. For example, you can't specify ``*prod.example.com`` or ``prod*.example.com`` .
        - The * can't replace any of the middle labels, for example, marketing.*.example.com.
        - If you include * in any position other than the leftmost label in a domain name, DNS treats it as an * character (ASCII 42), not as a wildcard.

        .. epigraph::

           You can't use the * wildcard for resource records sets that have a type of NS.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordset.html#cfn-route53-recordset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''*Latency-based resource record sets only:* The Amazon EC2 Region where you created the resource that this resource record set refers to.

        The resource typically is an AWS resource, such as an EC2 instance or an ELB load balancer, and is referred to by an IP address or a DNS domain name, depending on the record type.

        When Amazon Route 53 receives a DNS query for a domain name and type for which you have created latency resource record sets, Route 53 selects the latency resource record set that has the lowest latency between the end user and the associated Amazon EC2 Region. Route 53 then returns the value that is associated with the selected resource record set.

        Note the following:

        - You can only specify one ``ResourceRecord`` per latency resource record set.
        - You can only create one latency resource record set for each Amazon EC2 Region.
        - You aren't required to create latency resource record sets for all Amazon EC2 Regions. Route 53 will choose the region with the best latency from among the regions that you create latency resource record sets for.
        - You can't create non-latency resource record sets that have the same values for the ``Name`` and ``Type`` elements as latency resource record sets.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordset.html#cfn-route53-recordset-region
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_records(self) -> typing.Optional[typing.List[builtins.str]]:
        '''One or more values that correspond with the value that you specified for the ``Type`` property.

        For example, if you specified ``A`` for ``Type`` , you specify one or more IP addresses in IPv4 format for ``ResourceRecords`` . For information about the format of values for each record type, see `Supported DNS Resource Record Types <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/ResourceRecordTypes.html>`_ in the *Amazon Route 53 Developer Guide* .

        Note the following:

        - You can specify more than one value for all record types except CNAME and SOA.
        - The maximum length of a value is 4000 characters.
        - If you're creating an alias record, omit ``ResourceRecords`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordset.html#cfn-route53-recordset-resourcerecords
        '''
        result = self._values.get("resource_records")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def set_identifier(self) -> typing.Optional[builtins.str]:
        '''*Resource record sets that have a routing policy other than simple:* An identifier that differentiates among multiple resource record sets that have the same combination of name and type, such as multiple weighted resource record sets named acme.example.com that have a type of A. In a group of resource record sets that have the same name and type, the value of ``SetIdentifier`` must be unique for each resource record set.

        For information about routing policies, see `Choosing a Routing Policy <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html>`_ in the *Amazon Route 53 Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordset.html#cfn-route53-recordset-setidentifier
        '''
        result = self._values.get("set_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ttl(self) -> typing.Optional[builtins.str]:
        '''The resource record cache time to live (TTL), in seconds. Note the following:.

        - If you're creating or updating an alias resource record set, omit ``TTL`` . Amazon Route 53 uses the value of ``TTL`` for the alias target.
        - If you're associating this resource record set with a health check (if you're adding a ``HealthCheckId`` element), we recommend that you specify a ``TTL`` of 60 seconds or less so clients respond quickly to changes in health status.
        - All of the resource record sets in a group of weighted resource record sets must have the same value for ``TTL`` .
        - If a group of weighted resource record sets includes one or more weighted alias resource record sets for which the alias target is an ELB load balancer, we recommend that you specify a ``TTL`` of 60 seconds for all of the non-alias weighted resource record sets that have the same name and type. Values other than 60 seconds (the TTL for load balancers) will change the effect of the values that you specify for ``Weight`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordset.html#cfn-route53-recordset-ttl
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The DNS record type.

        For information about different record types and how data is encoded for them, see `Supported DNS Resource Record Types <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/ResourceRecordTypes.html>`_ in the *Amazon Route 53 Developer Guide* .

        Valid values for basic resource record sets: ``A`` | ``AAAA`` | ``CAA`` | ``CNAME`` | ``DS`` | ``MX`` | ``NAPTR`` | ``NS`` | ``PTR`` | ``SOA`` | ``SPF`` | ``SRV`` | ``TXT`` | ``TLSA`` | ``SSHFP`` | ``SVCB`` | ``HTTPS``

        Values for weighted, latency, geolocation, and failover resource record sets: ``A`` | ``AAAA`` | ``CAA`` | ``CNAME`` | ``MX`` | ``NAPTR`` | ``PTR`` | ``SPF`` | ``SRV`` | ``TXT`` | ``TLSA`` | ``SSHFP`` | ``SVCB`` | ``HTTPS`` . When creating a group of weighted, latency, geolocation, or failover resource record sets, specify the same value for all of the resource record sets in the group.

        Valid values for multivalue answer resource record sets: ``A`` | ``AAAA`` | ``MX`` | ``NAPTR`` | ``PTR`` | ``SPF`` | ``SRV`` | ``TXT`` | ``CAA`` | ``TLSA`` | ``SSHFP`` | ``SVCB`` | ``HTTPS``
        .. epigraph::

           SPF records were formerly used to verify the identity of the sender of email messages. However, we no longer recommend that you create resource record sets for which the value of ``Type`` is ``SPF`` . RFC 7208, *Sender Policy Framework (SPF) for Authorizing Use of Domains in Email, Version 1* , has been updated to say, "...[I]ts existence and mechanism defined in [RFC4408] have led to some interoperability issues. Accordingly, its use is no longer appropriate for SPF version 1; implementations are not to use it." In RFC 7208, see section 14.1, `The SPF DNS Record Type <https://docs.aws.amazon.com/http://tools.ietf.org/html/rfc7208#section-14.1>`_ .

        Values for alias resource record sets:

        - *Amazon API Gateway custom regional APIs and edge-optimized APIs:* ``A``
        - *CloudFront distributions:* ``A``

        If IPv6 is enabled for the distribution, create two resource record sets to route traffic to your distribution, one with a value of ``A`` and one with a value of ``AAAA`` .

        - *Amazon API Gateway environment that has a regionalized subdomain* : ``A``
        - *ELB load balancers:* ``A`` | ``AAAA``
        - *Amazon S3 buckets:* ``A``
        - *Amazon Virtual Private Cloud interface VPC endpoints* ``A``
        - *Another resource record set in this hosted zone:* Specify the type of the resource record set that you're creating the alias for. All values are supported except ``NS`` and ``SOA`` .

        .. epigraph::

           If you're creating an alias record that has the same name as the hosted zone (known as the zone apex), you can't route traffic to a record for which the value of ``Type`` is ``CNAME`` . This is because the alias record must have the same type as the record you're routing traffic to, and creating a CNAME record for the zone apex isn't supported even for an alias record.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordset.html#cfn-route53-recordset-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''*Weighted resource record sets only:* Among resource record sets that have the same combination of DNS name and type, a value that determines the proportion of DNS queries that Amazon Route 53 responds to using the current resource record set.

        Route 53 calculates the sum of the weights for the resource record sets that have the same combination of DNS name and type. Route 53 then responds to queries based on the ratio of a resource's weight to the total. Note the following:

        - You must specify a value for the ``Weight`` element for every weighted resource record set.
        - You can only specify one ``ResourceRecord`` per weighted resource record set.
        - You can't create latency, failover, or geolocation resource record sets that have the same values for the ``Name`` and ``Type`` elements as weighted resource record sets.
        - You can create a maximum of 100 weighted resource record sets that have the same values for the ``Name`` and ``Type`` elements.
        - For weighted (but not weighted alias) resource record sets, if you set ``Weight`` to ``0`` for a resource record set, Route 53 never responds to queries with the applicable value for that resource record set. However, if you set ``Weight`` to ``0`` for all resource record sets that have the same combination of DNS name and type, traffic is routed to all resources with equal probability.

        The effect of setting ``Weight`` to ``0`` is different when you associate health checks with weighted resource record sets. For more information, see `Options for Configuring Route 53 Active-Active and Active-Passive Failover <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-configuring-options.html>`_ in the *Amazon Route 53 Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordset.html#cfn-route53-recordset-weight
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRecordSetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRecordSetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnRecordSetPropsMixin",
):
    '''Information about the record that you want to create.

    The ``AWS::Route53::RecordSet`` type can be used as a standalone resource or as an embedded property in the ``AWS::Route53::RecordSetGroup`` type. Note that some ``AWS::Route53::RecordSet`` properties are valid only when used within ``AWS::Route53::RecordSetGroup`` .

    For more information, see `ChangeResourceRecordSets <https://docs.aws.amazon.com/Route53/latest/APIReference/API_ChangeResourceRecordSets.html>`_ in the *Amazon Route 53 API Reference* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordset.html
    :cloudformationResource: AWS::Route53::RecordSet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
        
        cfn_record_set_props_mixin = route53_mixins.CfnRecordSetPropsMixin(route53_mixins.CfnRecordSetMixinProps(
            alias_target=route53_mixins.CfnRecordSetPropsMixin.AliasTargetProperty(
                dns_name="dnsName",
                evaluate_target_health=False,
                hosted_zone_id="hostedZoneId"
            ),
            cidr_routing_config=route53_mixins.CfnRecordSetPropsMixin.CidrRoutingConfigProperty(
                collection_id="collectionId",
                location_name="locationName"
            ),
            comment="comment",
            failover="failover",
            geo_location=route53_mixins.CfnRecordSetPropsMixin.GeoLocationProperty(
                continent_code="continentCode",
                country_code="countryCode",
                subdivision_code="subdivisionCode"
            ),
            geo_proximity_location=route53_mixins.CfnRecordSetPropsMixin.GeoProximityLocationProperty(
                aws_region="awsRegion",
                bias=123,
                coordinates=route53_mixins.CfnRecordSetPropsMixin.CoordinatesProperty(
                    latitude="latitude",
                    longitude="longitude"
                ),
                local_zone_group="localZoneGroup"
            ),
            health_check_id="healthCheckId",
            hosted_zone_id="hostedZoneId",
            hosted_zone_name="hostedZoneName",
            multi_value_answer=False,
            name="name",
            region="region",
            resource_records=["resourceRecords"],
            set_identifier="setIdentifier",
            ttl="ttl",
            type="type",
            weight=123
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRecordSetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Route53::RecordSet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6513fe0a8bb865cb2fb56a732a4d1b9e1bc15b70bb43aa44afb7df46cfba49e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4590cc76a1b74eb6ecd905b7261cfba632d24b3a7d26552038ff1431a280a498)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__133723f7705380b1d981d4d909d9fd5744b5513e97a5e1c11b69fb8c05b0e7e0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRecordSetMixinProps:
        return typing.cast(CfnRecordSetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnRecordSetPropsMixin.AliasTargetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dns_name": "dnsName",
            "evaluate_target_health": "evaluateTargetHealth",
            "hosted_zone_id": "hostedZoneId",
        },
    )
    class AliasTargetProperty:
        def __init__(
            self,
            *,
            dns_name: typing.Optional[builtins.str] = None,
            evaluate_target_health: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            hosted_zone_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''*Alias records only:* Information about the AWS resource, such as a CloudFront distribution or an Amazon S3 bucket, that you want to route traffic to.

            When creating records for a private hosted zone, note the following:

            - Creating geolocation alias and latency alias records in a private hosted zone is allowed but not supported.
            - For information about creating failover records in a private hosted zone, see `Configuring Failover in a Private Hosted Zone <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-private-hosted-zones.html>`_ .

            :param dns_name: *Alias records only:* The value that you specify depends on where you want to route queries:. - **Amazon API Gateway custom regional APIs and edge-optimized APIs** - Specify the applicable domain name for your API. You can get the applicable value using the AWS CLI command `get-domain-names <https://docs.aws.amazon.com/cli/latest/reference/apigateway/get-domain-names.html>`_ : - For regional APIs, specify the value of ``regionalDomainName`` . - For edge-optimized APIs, specify the value of ``distributionDomainName`` . This is the name of the associated CloudFront distribution, such as ``da1b2c3d4e5.cloudfront.net`` . .. epigraph:: The name of the record that you're creating must match a custom domain name for your API, such as ``api.example.com`` . - **Amazon Virtual Private Cloud interface VPC endpoint** - Enter the API endpoint for the interface endpoint, such as ``vpce-123456789abcdef01-example-us-east-1a.elasticloadbalancing.us-east-1.vpce.amazonaws.com`` . For edge-optimized APIs, this is the domain name for the corresponding CloudFront distribution. You can get the value of ``DnsName`` using the AWS CLI command `describe-vpc-endpoints <https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-vpc-endpoints.html>`_ . - **CloudFront distribution** - Specify the domain name that CloudFront assigned when you created your distribution. Your CloudFront distribution must include an alternate domain name that matches the name of the record. For example, if the name of the record is *acme.example.com* , your CloudFront distribution must include *acme.example.com* as one of the alternate domain names. For more information, see `Using Alternate Domain Names (CNAMEs) <https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/CNAMEs.html>`_ in the *Amazon CloudFront Developer Guide* . You can't create a record in a private hosted zone to route traffic to a CloudFront distribution. .. epigraph:: For failover alias records, you can't specify a CloudFront distribution for both the primary and secondary records. A distribution must include an alternate domain name that matches the name of the record. However, the primary and secondary records have the same name, and you can't include the same alternate domain name in more than one distribution. - **Elastic Beanstalk environment** - If the domain name for your Elastic Beanstalk environment includes the region that you deployed the environment in, you can create an alias record that routes traffic to the environment. For example, the domain name ``my-environment. *us-west-2* .elasticbeanstalk.com`` is a regionalized domain name. .. epigraph:: For environments that were created before early 2016, the domain name doesn't include the region. To route traffic to these environments, you must create a CNAME record instead of an alias record. Note that you can't create a CNAME record for the root domain name. For example, if your domain name is example.com, you can create a record that routes traffic for acme.example.com to your Elastic Beanstalk environment, but you can't create a record that routes traffic for example.com to your Elastic Beanstalk environment. For Elastic Beanstalk environments that have regionalized subdomains, specify the ``CNAME`` attribute for the environment. You can use the following methods to get the value of the CNAME attribute: - *AWS Management Console* : For information about how to get the value by using the console, see `Using Custom Domains with AWS Elastic Beanstalk <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/customdomains.html>`_ in the *AWS Elastic Beanstalk Developer Guide* . - *Elastic Beanstalk API* : Use the ``DescribeEnvironments`` action to get the value of the ``CNAME`` attribute. For more information, see `DescribeEnvironments <https://docs.aws.amazon.com/elasticbeanstalk/latest/api/API_DescribeEnvironments.html>`_ in the *AWS Elastic Beanstalk API Reference* . - *AWS CLI* : Use the ``describe-environments`` command to get the value of the ``CNAME`` attribute. For more information, see `describe-environments <https://docs.aws.amazon.com/cli/latest/reference/elasticbeanstalk/describe-environments.html>`_ in the *AWS CLI* . - **ELB load balancer** - Specify the DNS name that is associated with the load balancer. Get the DNS name by using the AWS Management Console , the ELB API, or the AWS CLI . - *AWS Management Console* : Go to the EC2 page, choose *Load Balancers* in the navigation pane, choose the load balancer, choose the *Description* tab, and get the value of the *DNS name* field. If you're routing traffic to a Classic Load Balancer, get the value that begins with *dualstack* . If you're routing traffic to another type of load balancer, get the value that applies to the record type, A or AAAA. - *Elastic Load Balancing API* : Use ``DescribeLoadBalancers`` to get the value of ``DNSName`` . For more information, see the applicable guide: - Classic Load Balancers: `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/2012-06-01/APIReference/API_DescribeLoadBalancers.html>`_ - Application and Network Load Balancers: `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeLoadBalancers.html>`_ - *CloudFormation Fn::GetAtt intrinsic function* : Use the `Fn::GetAtt <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html>`_ intrinsic function to get the value of ``DNSName`` : - `Classic Load Balancers <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#aws-properties-ec2-elb-return-values>`_ . - `Application and Network Load Balancers <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#aws-resource-elasticloadbalancingv2-loadbalancer-return-values>`_ . - *AWS CLI* : Use ``describe-load-balancers`` to get the value of ``DNSName`` . For more information, see the applicable guide: - Classic Load Balancers: `describe-load-balancers <https://docs.aws.amazon.com/cli/latest/reference/elb/describe-load-balancers.html>`_ - Application and Network Load Balancers: `describe-load-balancers <https://docs.aws.amazon.com/cli/latest/reference/elbv2/describe-load-balancers.html>`_ - **Global Accelerator accelerator** - Specify the DNS name for your accelerator: - *Global Accelerator API* : To get the DNS name, use `DescribeAccelerator <https://docs.aws.amazon.com/global-accelerator/latest/api/API_DescribeAccelerator.html>`_ . - *AWS CLI* : To get the DNS name, use `describe-accelerator <https://docs.aws.amazon.com/cli/latest/reference/globalaccelerator/describe-accelerator.html>`_ . - **Amazon S3 bucket that is configured as a static website** - Specify the domain name of the Amazon S3 website endpoint that you created the bucket in, for example, ``s3-website.us-east-2.amazonaws.com`` . For more information about valid values, see the table `Amazon S3 Website Endpoints <https://docs.aws.amazon.com/general/latest/gr/s3.html#s3_website_region_endpoints>`_ in the *Amazon Web Services General Reference* . For more information about using S3 buckets for websites, see `Getting Started with Amazon Route 53 <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/getting-started.html>`_ in the *Amazon Route 53 Developer Guide.* - **Another Route 53 record** - Specify the value of the ``Name`` element for a record in the current hosted zone. .. epigraph:: If you're creating an alias record that has the same name as the hosted zone (known as the zone apex), you can't specify the domain name for a record for which the value of ``Type`` is ``CNAME`` . This is because the alias record must have the same type as the record that you're routing traffic to, and creating a CNAME record for the zone apex isn't supported even for an alias record.
            :param evaluate_target_health: *Applies only to alias, failover alias, geolocation alias, latency alias, and weighted alias resource record sets:* When ``EvaluateTargetHealth`` is ``true`` , an alias resource record set inherits the health of the referenced AWS resource, such as an ELB load balancer or another resource record set in the hosted zone. Note the following: - **CloudFront distributions** - You can't set ``EvaluateTargetHealth`` to ``true`` when the alias target is a CloudFront distribution. - **Elastic Beanstalk environments that have regionalized subdomains** - If you specify an Elastic Beanstalk environment in ``DNSName`` and the environment contains an ELB load balancer, Elastic Load Balancing routes queries only to the healthy Amazon EC2 instances that are registered with the load balancer. (An environment automatically contains an ELB load balancer if it includes more than one Amazon EC2 instance.) If you set ``EvaluateTargetHealth`` to ``true`` and either no Amazon EC2 instances are healthy or the load balancer itself is unhealthy, Route 53 routes queries to other available resources that are healthy, if any. If the environment contains a single Amazon EC2 instance, there are no special requirements. - **ELB load balancers** - Health checking behavior depends on the type of load balancer: - *Classic Load Balancers* : If you specify an ELB Classic Load Balancer in ``DNSName`` , Elastic Load Balancing routes queries only to the healthy Amazon EC2 instances that are registered with the load balancer. If you set ``EvaluateTargetHealth`` to ``true`` and either no EC2 instances are healthy or the load balancer itself is unhealthy, Route 53 routes queries to other resources. - *Application and Network Load Balancers* : If you specify an ELB Application or Network Load Balancer and you set ``EvaluateTargetHealth`` to ``true`` , Route 53 routes queries to the load balancer based on the health of the target groups that are associated with the load balancer: - For an Application or Network Load Balancer to be considered healthy, every target group that contains targets must contain at least one healthy target. If any target group contains only unhealthy targets, the load balancer is considered unhealthy, and Route 53 routes queries to other resources. - A target group that has no registered targets is considered unhealthy. .. epigraph:: When you create a load balancer, you configure settings for Elastic Load Balancing health checks; they're not Route 53 health checks, but they perform a similar function. Do not create Route 53 health checks for the EC2 instances that you register with an ELB load balancer. - **API Gateway APIs** - There are no special requirements for setting ``EvaluateTargetHealth`` to ``true`` when the alias target is an API Gateway API. However, because API Gateway is highly available by design, ``EvaluateTargetHealth`` provides no operational benefit and `Route 53 health checks <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html>`_ are recommended instead for failover scenarios. - **S3 buckets** - There are no special requirements for setting ``EvaluateTargetHealth`` to ``true`` when the alias target is an S3 bucket. However, because S3 buckets are highly available by design, ``EvaluateTargetHealth`` provides no operational benefit and `Route 53 health checks <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html>`_ are recommended instead for failover scenarios. - **VPC interface endpoints** - There are no special requirements for setting ``EvaluateTargetHealth`` to ``true`` when the alias target is a VPC interface endpoint. However, because VPC interface endpoints are highly available by design, ``EvaluateTargetHealth`` provides no operational benefit and `Route 53 health checks <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html>`_ are recommended instead for failover scenarios. - **Other records in the same hosted zone** - If the AWS resource that you specify in ``DNSName`` is a record or a group of records (for example, a group of weighted records) but is not another alias record, we recommend that you associate a health check with all of the records in the alias target. For more information, see `What Happens When You Omit Health Checks? <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-complex-configs.html#dns-failover-complex-configs-hc-omitting>`_ in the *Amazon Route 53 Developer Guide* . .. epigraph:: While ``EvaluateTargetHealth`` can be set to ``true`` for highly available AWS services (such as S3 buckets, VPC interface endpoints, and API Gateway), these services are designed for high availability and rarely experience outages that would be detected by this feature. For failover scenarios with these services, consider using `Route 53 health checks <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html>`_ that monitor your application's ability to access the service instead. For more information and examples, see `Amazon Route 53 Health Checks and DNS Failover <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html>`_ in the *Amazon Route 53 Developer Guide* .
            :param hosted_zone_id: *Alias resource records sets only* : The value used depends on where you want to route traffic:. - **Amazon API Gateway custom regional APIs and edge-optimized APIs** - Specify the hosted zone ID for your API. You can get the applicable value using the AWS CLI command `get-domain-names <https://docs.aws.amazon.com/cli/latest/reference/apigateway/get-domain-names.html>`_ : - For regional APIs, specify the value of ``regionalHostedZoneId`` . - For edge-optimized APIs, specify the value of ``distributionHostedZoneId`` . - **Amazon Virtual Private Cloud interface VPC endpoint** - Specify the hosted zone ID for your interface endpoint. You can get the value of ``HostedZoneId`` using the AWS CLI command `describe-vpc-endpoints <https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-vpc-endpoints.html>`_ . - **CloudFront distribution** - Specify ``Z2FDTNDATAQYW2`` . This is always the hosted zone ID when you create an alias record that routes traffic to a CloudFront distribution. .. epigraph:: Alias records for CloudFront can't be created in a private zone. - **Elastic Beanstalk environment** - Specify the hosted zone ID for the region that you created the environment in. The environment must have a regionalized subdomain. For a list of regions and the corresponding hosted zone IDs, see `AWS Elastic Beanstalk endpoints and quotas <https://docs.aws.amazon.com/general/latest/gr/elasticbeanstalk.html>`_ in the *Amazon Web Services General Reference* . - **ELB load balancer** - Specify the value of the hosted zone ID for the load balancer. Use the following methods to get the hosted zone ID: - `Service Endpoints <https://docs.aws.amazon.com/general/latest/gr/elb.html>`_ table in the "Elastic Load Balancing Endpoints and Quotas" topic in the *Amazon Web Services General Reference* : Use the value that corresponds with the region that you created your load balancer in. Note that there are separate columns for Application and Classic Load Balancers and for Network Load Balancers. - *AWS Management Console* : Go to the Amazon EC2 page, choose *Load Balancers* in the navigation pane, select the load balancer, and get the value of the *Hosted zone* field on the *Description* tab. - *Elastic Load Balancing API* : Use ``DescribeLoadBalancers`` to get the applicable value. For more information, see the applicable guide: - Classic Load Balancers: Use `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/2012-06-01/APIReference/API_DescribeLoadBalancers.html>`_ to get the value of ``CanonicalHostedZoneNameID`` . - Application and Network Load Balancers: Use `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeLoadBalancers.html>`_ to get the value of ``CanonicalHostedZoneID`` . - *CloudFormation Fn::GetAtt intrinsic function* : Use the `Fn::GetAtt <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html>`_ intrinsic function to get the applicable value: - Classic Load Balancers: Get `CanonicalHostedZoneNameID <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#aws-properties-ec2-elb-return-values>`_ . - Application and Network Load Balancers: Get `CanonicalHostedZoneID <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#aws-resource-elasticloadbalancingv2-loadbalancer-return-values>`_ . - *AWS CLI* : Use ``describe-load-balancers`` to get the applicable value. For more information, see the applicable guide: - Classic Load Balancers: Use `describe-load-balancers <https://docs.aws.amazon.com/cli/latest/reference/elb/describe-load-balancers.html>`_ to get the value of ``CanonicalHostedZoneNameID`` . - Application and Network Load Balancers: Use `describe-load-balancers <https://docs.aws.amazon.com/cli/latest/reference/elbv2/describe-load-balancers.html>`_ to get the value of ``CanonicalHostedZoneID`` . - **Global Accelerator accelerator** - Specify ``Z2BJ6XQ5FK7U4H`` . - **An Amazon S3 bucket configured as a static website** - Specify the hosted zone ID for the region that you created the bucket in. For more information about valid values, see the table `Amazon S3 Website Endpoints <https://docs.aws.amazon.com/general/latest/gr/s3.html#s3_website_region_endpoints>`_ in the *Amazon Web Services General Reference* . - **Another Route 53 record in your hosted zone** - Specify the hosted zone ID of your hosted zone. (An alias record can't reference a record in a different hosted zone.)

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-aliastarget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
                
                alias_target_property = route53_mixins.CfnRecordSetPropsMixin.AliasTargetProperty(
                    dns_name="dnsName",
                    evaluate_target_health=False,
                    hosted_zone_id="hostedZoneId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__377e6b495784f342eb105a0b5165623b6b9189f04e7deb0e00b69e6f113946f2)
                check_type(argname="argument dns_name", value=dns_name, expected_type=type_hints["dns_name"])
                check_type(argname="argument evaluate_target_health", value=evaluate_target_health, expected_type=type_hints["evaluate_target_health"])
                check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dns_name is not None:
                self._values["dns_name"] = dns_name
            if evaluate_target_health is not None:
                self._values["evaluate_target_health"] = evaluate_target_health
            if hosted_zone_id is not None:
                self._values["hosted_zone_id"] = hosted_zone_id

        @builtins.property
        def dns_name(self) -> typing.Optional[builtins.str]:
            '''*Alias records only:* The value that you specify depends on where you want to route queries:.

            - **Amazon API Gateway custom regional APIs and edge-optimized APIs** - Specify the applicable domain name for your API. You can get the applicable value using the AWS CLI command `get-domain-names <https://docs.aws.amazon.com/cli/latest/reference/apigateway/get-domain-names.html>`_ :
            - For regional APIs, specify the value of ``regionalDomainName`` .
            - For edge-optimized APIs, specify the value of ``distributionDomainName`` . This is the name of the associated CloudFront distribution, such as ``da1b2c3d4e5.cloudfront.net`` .

            .. epigraph::

               The name of the record that you're creating must match a custom domain name for your API, such as ``api.example.com`` .

            - **Amazon Virtual Private Cloud interface VPC endpoint** - Enter the API endpoint for the interface endpoint, such as ``vpce-123456789abcdef01-example-us-east-1a.elasticloadbalancing.us-east-1.vpce.amazonaws.com`` . For edge-optimized APIs, this is the domain name for the corresponding CloudFront distribution. You can get the value of ``DnsName`` using the AWS CLI command `describe-vpc-endpoints <https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-vpc-endpoints.html>`_ .
            - **CloudFront distribution** - Specify the domain name that CloudFront assigned when you created your distribution.

            Your CloudFront distribution must include an alternate domain name that matches the name of the record. For example, if the name of the record is *acme.example.com* , your CloudFront distribution must include *acme.example.com* as one of the alternate domain names. For more information, see `Using Alternate Domain Names (CNAMEs) <https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/CNAMEs.html>`_ in the *Amazon CloudFront Developer Guide* .

            You can't create a record in a private hosted zone to route traffic to a CloudFront distribution.
            .. epigraph::

               For failover alias records, you can't specify a CloudFront distribution for both the primary and secondary records. A distribution must include an alternate domain name that matches the name of the record. However, the primary and secondary records have the same name, and you can't include the same alternate domain name in more than one distribution.

            - **Elastic Beanstalk environment** - If the domain name for your Elastic Beanstalk environment includes the region that you deployed the environment in, you can create an alias record that routes traffic to the environment. For example, the domain name ``my-environment. *us-west-2* .elasticbeanstalk.com`` is a regionalized domain name.

            .. epigraph::

               For environments that were created before early 2016, the domain name doesn't include the region. To route traffic to these environments, you must create a CNAME record instead of an alias record. Note that you can't create a CNAME record for the root domain name. For example, if your domain name is example.com, you can create a record that routes traffic for acme.example.com to your Elastic Beanstalk environment, but you can't create a record that routes traffic for example.com to your Elastic Beanstalk environment.

            For Elastic Beanstalk environments that have regionalized subdomains, specify the ``CNAME`` attribute for the environment. You can use the following methods to get the value of the CNAME attribute:

            - *AWS Management Console* : For information about how to get the value by using the console, see `Using Custom Domains with AWS Elastic Beanstalk <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/customdomains.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .
            - *Elastic Beanstalk API* : Use the ``DescribeEnvironments`` action to get the value of the ``CNAME`` attribute. For more information, see `DescribeEnvironments <https://docs.aws.amazon.com/elasticbeanstalk/latest/api/API_DescribeEnvironments.html>`_ in the *AWS Elastic Beanstalk API Reference* .
            - *AWS CLI* : Use the ``describe-environments`` command to get the value of the ``CNAME`` attribute. For more information, see `describe-environments <https://docs.aws.amazon.com/cli/latest/reference/elasticbeanstalk/describe-environments.html>`_ in the *AWS CLI* .
            - **ELB load balancer** - Specify the DNS name that is associated with the load balancer. Get the DNS name by using the AWS Management Console , the ELB API, or the AWS CLI .
            - *AWS Management Console* : Go to the EC2 page, choose *Load Balancers* in the navigation pane, choose the load balancer, choose the *Description* tab, and get the value of the *DNS name* field.

            If you're routing traffic to a Classic Load Balancer, get the value that begins with *dualstack* . If you're routing traffic to another type of load balancer, get the value that applies to the record type, A or AAAA.

            - *Elastic Load Balancing API* : Use ``DescribeLoadBalancers`` to get the value of ``DNSName`` . For more information, see the applicable guide:
            - Classic Load Balancers: `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/2012-06-01/APIReference/API_DescribeLoadBalancers.html>`_
            - Application and Network Load Balancers: `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeLoadBalancers.html>`_
            - *CloudFormation Fn::GetAtt intrinsic function* : Use the `Fn::GetAtt <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html>`_ intrinsic function to get the value of ``DNSName`` :
            - `Classic Load Balancers <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#aws-properties-ec2-elb-return-values>`_ .
            - `Application and Network Load Balancers <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#aws-resource-elasticloadbalancingv2-loadbalancer-return-values>`_ .
            - *AWS CLI* : Use ``describe-load-balancers`` to get the value of ``DNSName`` . For more information, see the applicable guide:
            - Classic Load Balancers: `describe-load-balancers <https://docs.aws.amazon.com/cli/latest/reference/elb/describe-load-balancers.html>`_
            - Application and Network Load Balancers: `describe-load-balancers <https://docs.aws.amazon.com/cli/latest/reference/elbv2/describe-load-balancers.html>`_
            - **Global Accelerator accelerator** - Specify the DNS name for your accelerator:
            - *Global Accelerator API* : To get the DNS name, use `DescribeAccelerator <https://docs.aws.amazon.com/global-accelerator/latest/api/API_DescribeAccelerator.html>`_ .
            - *AWS CLI* : To get the DNS name, use `describe-accelerator <https://docs.aws.amazon.com/cli/latest/reference/globalaccelerator/describe-accelerator.html>`_ .
            - **Amazon S3 bucket that is configured as a static website** - Specify the domain name of the Amazon S3 website endpoint that you created the bucket in, for example, ``s3-website.us-east-2.amazonaws.com`` . For more information about valid values, see the table `Amazon S3 Website Endpoints <https://docs.aws.amazon.com/general/latest/gr/s3.html#s3_website_region_endpoints>`_ in the *Amazon Web Services General Reference* . For more information about using S3 buckets for websites, see `Getting Started with Amazon Route 53 <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/getting-started.html>`_ in the *Amazon Route 53 Developer Guide.*
            - **Another Route 53 record** - Specify the value of the ``Name`` element for a record in the current hosted zone.

            .. epigraph::

               If you're creating an alias record that has the same name as the hosted zone (known as the zone apex), you can't specify the domain name for a record for which the value of ``Type`` is ``CNAME`` . This is because the alias record must have the same type as the record that you're routing traffic to, and creating a CNAME record for the zone apex isn't supported even for an alias record.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-aliastarget.html#cfn-route53-recordset-aliastarget-dnsname
            '''
            result = self._values.get("dns_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def evaluate_target_health(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''*Applies only to alias, failover alias, geolocation alias, latency alias, and weighted alias resource record sets:* When ``EvaluateTargetHealth`` is ``true`` , an alias resource record set inherits the health of the referenced AWS resource, such as an ELB load balancer or another resource record set in the hosted zone.

            Note the following:

            - **CloudFront distributions** - You can't set ``EvaluateTargetHealth`` to ``true`` when the alias target is a CloudFront distribution.
            - **Elastic Beanstalk environments that have regionalized subdomains** - If you specify an Elastic Beanstalk environment in ``DNSName`` and the environment contains an ELB load balancer, Elastic Load Balancing routes queries only to the healthy Amazon EC2 instances that are registered with the load balancer. (An environment automatically contains an ELB load balancer if it includes more than one Amazon EC2 instance.) If you set ``EvaluateTargetHealth`` to ``true`` and either no Amazon EC2 instances are healthy or the load balancer itself is unhealthy, Route 53 routes queries to other available resources that are healthy, if any.

            If the environment contains a single Amazon EC2 instance, there are no special requirements.

            - **ELB load balancers** - Health checking behavior depends on the type of load balancer:
            - *Classic Load Balancers* : If you specify an ELB Classic Load Balancer in ``DNSName`` , Elastic Load Balancing routes queries only to the healthy Amazon EC2 instances that are registered with the load balancer. If you set ``EvaluateTargetHealth`` to ``true`` and either no EC2 instances are healthy or the load balancer itself is unhealthy, Route 53 routes queries to other resources.
            - *Application and Network Load Balancers* : If you specify an ELB Application or Network Load Balancer and you set ``EvaluateTargetHealth`` to ``true`` , Route 53 routes queries to the load balancer based on the health of the target groups that are associated with the load balancer:
            - For an Application or Network Load Balancer to be considered healthy, every target group that contains targets must contain at least one healthy target. If any target group contains only unhealthy targets, the load balancer is considered unhealthy, and Route 53 routes queries to other resources.
            - A target group that has no registered targets is considered unhealthy.

            .. epigraph::

               When you create a load balancer, you configure settings for Elastic Load Balancing health checks; they're not Route 53 health checks, but they perform a similar function. Do not create Route 53 health checks for the EC2 instances that you register with an ELB load balancer.

            - **API Gateway APIs** - There are no special requirements for setting ``EvaluateTargetHealth`` to ``true`` when the alias target is an API Gateway API. However, because API Gateway is highly available by design, ``EvaluateTargetHealth`` provides no operational benefit and `Route 53 health checks <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html>`_ are recommended instead for failover scenarios.
            - **S3 buckets** - There are no special requirements for setting ``EvaluateTargetHealth`` to ``true`` when the alias target is an S3 bucket. However, because S3 buckets are highly available by design, ``EvaluateTargetHealth`` provides no operational benefit and `Route 53 health checks <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html>`_ are recommended instead for failover scenarios.
            - **VPC interface endpoints** - There are no special requirements for setting ``EvaluateTargetHealth`` to ``true`` when the alias target is a VPC interface endpoint. However, because VPC interface endpoints are highly available by design, ``EvaluateTargetHealth`` provides no operational benefit and `Route 53 health checks <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html>`_ are recommended instead for failover scenarios.
            - **Other records in the same hosted zone** - If the AWS resource that you specify in ``DNSName`` is a record or a group of records (for example, a group of weighted records) but is not another alias record, we recommend that you associate a health check with all of the records in the alias target. For more information, see `What Happens When You Omit Health Checks? <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-complex-configs.html#dns-failover-complex-configs-hc-omitting>`_ in the *Amazon Route 53 Developer Guide* .

            .. epigraph::

               While ``EvaluateTargetHealth`` can be set to ``true`` for highly available AWS services (such as S3 buckets, VPC interface endpoints, and API Gateway), these services are designed for high availability and rarely experience outages that would be detected by this feature. For failover scenarios with these services, consider using `Route 53 health checks <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html>`_ that monitor your application's ability to access the service instead.

            For more information and examples, see `Amazon Route 53 Health Checks and DNS Failover <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html>`_ in the *Amazon Route 53 Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-aliastarget.html#cfn-route53-recordset-aliastarget-evaluatetargethealth
            '''
            result = self._values.get("evaluate_target_health")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def hosted_zone_id(self) -> typing.Optional[builtins.str]:
            '''*Alias resource records sets only* : The value used depends on where you want to route traffic:.

            - **Amazon API Gateway custom regional APIs and edge-optimized APIs** - Specify the hosted zone ID for your API. You can get the applicable value using the AWS CLI command `get-domain-names <https://docs.aws.amazon.com/cli/latest/reference/apigateway/get-domain-names.html>`_ :
            - For regional APIs, specify the value of ``regionalHostedZoneId`` .
            - For edge-optimized APIs, specify the value of ``distributionHostedZoneId`` .
            - **Amazon Virtual Private Cloud interface VPC endpoint** - Specify the hosted zone ID for your interface endpoint. You can get the value of ``HostedZoneId`` using the AWS CLI command `describe-vpc-endpoints <https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-vpc-endpoints.html>`_ .
            - **CloudFront distribution** - Specify ``Z2FDTNDATAQYW2`` . This is always the hosted zone ID when you create an alias record that routes traffic to a CloudFront distribution.

            .. epigraph::

               Alias records for CloudFront can't be created in a private zone.

            - **Elastic Beanstalk environment** - Specify the hosted zone ID for the region that you created the environment in. The environment must have a regionalized subdomain. For a list of regions and the corresponding hosted zone IDs, see `AWS Elastic Beanstalk endpoints and quotas <https://docs.aws.amazon.com/general/latest/gr/elasticbeanstalk.html>`_ in the *Amazon Web Services General Reference* .
            - **ELB load balancer** - Specify the value of the hosted zone ID for the load balancer. Use the following methods to get the hosted zone ID:
            - `Service Endpoints <https://docs.aws.amazon.com/general/latest/gr/elb.html>`_ table in the "Elastic Load Balancing Endpoints and Quotas" topic in the *Amazon Web Services General Reference* : Use the value that corresponds with the region that you created your load balancer in. Note that there are separate columns for Application and Classic Load Balancers and for Network Load Balancers.
            - *AWS Management Console* : Go to the Amazon EC2 page, choose *Load Balancers* in the navigation pane, select the load balancer, and get the value of the *Hosted zone* field on the *Description* tab.
            - *Elastic Load Balancing API* : Use ``DescribeLoadBalancers`` to get the applicable value. For more information, see the applicable guide:
            - Classic Load Balancers: Use `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/2012-06-01/APIReference/API_DescribeLoadBalancers.html>`_ to get the value of ``CanonicalHostedZoneNameID`` .
            - Application and Network Load Balancers: Use `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeLoadBalancers.html>`_ to get the value of ``CanonicalHostedZoneID`` .
            - *CloudFormation Fn::GetAtt intrinsic function* : Use the `Fn::GetAtt <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html>`_ intrinsic function to get the applicable value:
            - Classic Load Balancers: Get `CanonicalHostedZoneNameID <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#aws-properties-ec2-elb-return-values>`_ .
            - Application and Network Load Balancers: Get `CanonicalHostedZoneID <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#aws-resource-elasticloadbalancingv2-loadbalancer-return-values>`_ .
            - *AWS CLI* : Use ``describe-load-balancers`` to get the applicable value. For more information, see the applicable guide:
            - Classic Load Balancers: Use `describe-load-balancers <https://docs.aws.amazon.com/cli/latest/reference/elb/describe-load-balancers.html>`_ to get the value of ``CanonicalHostedZoneNameID`` .
            - Application and Network Load Balancers: Use `describe-load-balancers <https://docs.aws.amazon.com/cli/latest/reference/elbv2/describe-load-balancers.html>`_ to get the value of ``CanonicalHostedZoneID`` .
            - **Global Accelerator accelerator** - Specify ``Z2BJ6XQ5FK7U4H`` .
            - **An Amazon S3 bucket configured as a static website** - Specify the hosted zone ID for the region that you created the bucket in. For more information about valid values, see the table `Amazon S3 Website Endpoints <https://docs.aws.amazon.com/general/latest/gr/s3.html#s3_website_region_endpoints>`_ in the *Amazon Web Services General Reference* .
            - **Another Route 53 record in your hosted zone** - Specify the hosted zone ID of your hosted zone. (An alias record can't reference a record in a different hosted zone.)

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-aliastarget.html#cfn-route53-recordset-aliastarget-hostedzoneid
            '''
            result = self._values.get("hosted_zone_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AliasTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnRecordSetPropsMixin.CidrRoutingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "collection_id": "collectionId",
            "location_name": "locationName",
        },
    )
    class CidrRoutingConfigProperty:
        def __init__(
            self,
            *,
            collection_id: typing.Optional[builtins.str] = None,
            location_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The object that is specified in resource record set object when you are linking a resource record set to a CIDR location.

            A ``LocationName`` with an asterisk “*” can be used to create a default CIDR record. ``CollectionId`` is still required for default record.

            :param collection_id: The CIDR collection ID.
            :param location_name: The CIDR collection location name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-cidrroutingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
                
                cidr_routing_config_property = route53_mixins.CfnRecordSetPropsMixin.CidrRoutingConfigProperty(
                    collection_id="collectionId",
                    location_name="locationName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c600739fc3b2839dd5fcf05e7034dfcac040f6f01006611750392bcec9b69eba)
                check_type(argname="argument collection_id", value=collection_id, expected_type=type_hints["collection_id"])
                check_type(argname="argument location_name", value=location_name, expected_type=type_hints["location_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if collection_id is not None:
                self._values["collection_id"] = collection_id
            if location_name is not None:
                self._values["location_name"] = location_name

        @builtins.property
        def collection_id(self) -> typing.Optional[builtins.str]:
            '''The CIDR collection ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-cidrroutingconfig.html#cfn-route53-recordset-cidrroutingconfig-collectionid
            '''
            result = self._values.get("collection_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def location_name(self) -> typing.Optional[builtins.str]:
            '''The CIDR collection location name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-cidrroutingconfig.html#cfn-route53-recordset-cidrroutingconfig-locationname
            '''
            result = self._values.get("location_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CidrRoutingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnRecordSetPropsMixin.CoordinatesProperty",
        jsii_struct_bases=[],
        name_mapping={"latitude": "latitude", "longitude": "longitude"},
    )
    class CoordinatesProperty:
        def __init__(
            self,
            *,
            latitude: typing.Optional[builtins.str] = None,
            longitude: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A complex type that lists the coordinates for a geoproximity resource record.

            :param latitude: Specifies a coordinate of the north–south position of a geographic point on the surface of the Earth (-90 - 90).
            :param longitude: Specifies a coordinate of the east–west position of a geographic point on the surface of the Earth (-180 - 180).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-coordinates.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
                
                coordinates_property = route53_mixins.CfnRecordSetPropsMixin.CoordinatesProperty(
                    latitude="latitude",
                    longitude="longitude"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6ae82ca3ed14b83f754ffd1bd4ed55bf576d9c914985864944ee9d880a872abf)
                check_type(argname="argument latitude", value=latitude, expected_type=type_hints["latitude"])
                check_type(argname="argument longitude", value=longitude, expected_type=type_hints["longitude"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if latitude is not None:
                self._values["latitude"] = latitude
            if longitude is not None:
                self._values["longitude"] = longitude

        @builtins.property
        def latitude(self) -> typing.Optional[builtins.str]:
            '''Specifies a coordinate of the north–south position of a geographic point on the surface of the Earth (-90 - 90).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-coordinates.html#cfn-route53-recordset-coordinates-latitude
            '''
            result = self._values.get("latitude")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def longitude(self) -> typing.Optional[builtins.str]:
            '''Specifies a coordinate of the east–west position of a geographic point on the surface of the Earth (-180 - 180).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-coordinates.html#cfn-route53-recordset-coordinates-longitude
            '''
            result = self._values.get("longitude")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CoordinatesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnRecordSetPropsMixin.GeoLocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "continent_code": "continentCode",
            "country_code": "countryCode",
            "subdivision_code": "subdivisionCode",
        },
    )
    class GeoLocationProperty:
        def __init__(
            self,
            *,
            continent_code: typing.Optional[builtins.str] = None,
            country_code: typing.Optional[builtins.str] = None,
            subdivision_code: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A complex type that contains information about a geographic location.

            :param continent_code: For geolocation resource record sets, a two-letter abbreviation that identifies a continent. Route 53 supports the following continent codes:. - *AF* : Africa - *AN* : Antarctica - *AS* : Asia - *EU* : Europe - *OC* : Oceania - *NA* : North America - *SA* : South America Constraint: Specifying ``ContinentCode`` with either ``CountryCode`` or ``SubdivisionCode`` returns an ``InvalidInput`` error.
            :param country_code: For geolocation resource record sets, the two-letter code for a country. Route 53 uses the two-letter country codes that are specified in `ISO standard 3166-1 alpha-2 <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2>`_ .
            :param subdivision_code: For geolocation resource record sets, the two-letter code for a state of the United States. Route 53 doesn't support any other values for ``SubdivisionCode`` . For a list of state abbreviations, see `Appendix B: Two–Letter State and Possession Abbreviations <https://docs.aws.amazon.com/https://pe.usps.com/text/pub28/28apb.htm>`_ on the United States Postal Service website. If you specify ``subdivisioncode`` , you must also specify ``US`` for ``CountryCode`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geolocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
                
                geo_location_property = route53_mixins.CfnRecordSetPropsMixin.GeoLocationProperty(
                    continent_code="continentCode",
                    country_code="countryCode",
                    subdivision_code="subdivisionCode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1bca0d2f9fbda44862ef5ae71229b1647f191c573456e5ca52a3cad46fe1f28c)
                check_type(argname="argument continent_code", value=continent_code, expected_type=type_hints["continent_code"])
                check_type(argname="argument country_code", value=country_code, expected_type=type_hints["country_code"])
                check_type(argname="argument subdivision_code", value=subdivision_code, expected_type=type_hints["subdivision_code"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if continent_code is not None:
                self._values["continent_code"] = continent_code
            if country_code is not None:
                self._values["country_code"] = country_code
            if subdivision_code is not None:
                self._values["subdivision_code"] = subdivision_code

        @builtins.property
        def continent_code(self) -> typing.Optional[builtins.str]:
            '''For geolocation resource record sets, a two-letter abbreviation that identifies a continent. Route 53 supports the following continent codes:.

            - *AF* : Africa
            - *AN* : Antarctica
            - *AS* : Asia
            - *EU* : Europe
            - *OC* : Oceania
            - *NA* : North America
            - *SA* : South America

            Constraint: Specifying ``ContinentCode`` with either ``CountryCode`` or ``SubdivisionCode`` returns an ``InvalidInput`` error.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geolocation.html#cfn-route53-recordset-geolocation-continentcode
            '''
            result = self._values.get("continent_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def country_code(self) -> typing.Optional[builtins.str]:
            '''For geolocation resource record sets, the two-letter code for a country.

            Route 53 uses the two-letter country codes that are specified in `ISO standard 3166-1 alpha-2 <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geolocation.html#cfn-route53-recordset-geolocation-countrycode
            '''
            result = self._values.get("country_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subdivision_code(self) -> typing.Optional[builtins.str]:
            '''For geolocation resource record sets, the two-letter code for a state of the United States.

            Route 53 doesn't support any other values for ``SubdivisionCode`` . For a list of state abbreviations, see `Appendix B: Two–Letter State and Possession Abbreviations <https://docs.aws.amazon.com/https://pe.usps.com/text/pub28/28apb.htm>`_ on the United States Postal Service website.

            If you specify ``subdivisioncode`` , you must also specify ``US`` for ``CountryCode`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geolocation.html#cfn-route53-recordset-geolocation-subdivisioncode
            '''
            result = self._values.get("subdivision_code")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GeoLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53.mixins.CfnRecordSetPropsMixin.GeoProximityLocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aws_region": "awsRegion",
            "bias": "bias",
            "coordinates": "coordinates",
            "local_zone_group": "localZoneGroup",
        },
    )
    class GeoProximityLocationProperty:
        def __init__(
            self,
            *,
            aws_region: typing.Optional[builtins.str] = None,
            bias: typing.Optional[jsii.Number] = None,
            coordinates: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRecordSetPropsMixin.CoordinatesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            local_zone_group: typing.Optional[builtins.str] = None,
        ) -> None:
            '''(Resource record sets only): A complex type that lets you specify where your resources are located.

            Only one of ``LocalZoneGroup`` , ``Coordinates`` , or ``AWS Region`` is allowed per request at a time.

            For more information about geoproximity routing, see `Geoproximity routing <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy-geoproximity.html>`_ in the *Amazon Route 53 Developer Guide* .

            :param aws_region: The AWS Region the resource you are directing DNS traffic to, is in.
            :param bias: The bias increases or decreases the size of the geographic region from which Route 53 routes traffic to a resource. To use ``Bias`` to change the size of the geographic region, specify the applicable value for the bias: - To expand the size of the geographic region from which Route 53 routes traffic to a resource, specify a positive integer from 1 to 99 for the bias. Route 53 shrinks the size of adjacent regions. - To shrink the size of the geographic region from which Route 53 routes traffic to a resource, specify a negative bias of -1 to -99. Route 53 expands the size of adjacent regions.
            :param coordinates: Contains the longitude and latitude for a geographic region.
            :param local_zone_group: Specifies an AWS Local Zone Group. A local Zone Group is usually the Local Zone code without the ending character. For example, if the Local Zone is ``us-east-1-bue-1a`` the Local Zone Group is ``us-east-1-bue-1`` . You can identify the Local Zones Group for a specific Local Zone by using the `describe-availability-zones <https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-availability-zones.html>`_ CLI command: This command returns: ``"GroupName": "us-west-2-den-1"`` , specifying that the Local Zone ``us-west-2-den-1a`` belongs to the Local Zone Group ``us-west-2-den-1`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geoproximitylocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53 import mixins as route53_mixins
                
                geo_proximity_location_property = route53_mixins.CfnRecordSetPropsMixin.GeoProximityLocationProperty(
                    aws_region="awsRegion",
                    bias=123,
                    coordinates=route53_mixins.CfnRecordSetPropsMixin.CoordinatesProperty(
                        latitude="latitude",
                        longitude="longitude"
                    ),
                    local_zone_group="localZoneGroup"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__430a922679a9793ddb47ae25a44e2c81a604399b3f38b23b437849be099c678b)
                check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                check_type(argname="argument bias", value=bias, expected_type=type_hints["bias"])
                check_type(argname="argument coordinates", value=coordinates, expected_type=type_hints["coordinates"])
                check_type(argname="argument local_zone_group", value=local_zone_group, expected_type=type_hints["local_zone_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_region is not None:
                self._values["aws_region"] = aws_region
            if bias is not None:
                self._values["bias"] = bias
            if coordinates is not None:
                self._values["coordinates"] = coordinates
            if local_zone_group is not None:
                self._values["local_zone_group"] = local_zone_group

        @builtins.property
        def aws_region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region the resource you are directing DNS traffic to, is in.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geoproximitylocation.html#cfn-route53-recordset-geoproximitylocation-awsregion
            '''
            result = self._values.get("aws_region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bias(self) -> typing.Optional[jsii.Number]:
            '''The bias increases or decreases the size of the geographic region from which Route 53 routes traffic to a resource.

            To use ``Bias`` to change the size of the geographic region, specify the applicable value for the bias:

            - To expand the size of the geographic region from which Route 53 routes traffic to a resource, specify a positive integer from 1 to 99 for the bias. Route 53 shrinks the size of adjacent regions.
            - To shrink the size of the geographic region from which Route 53 routes traffic to a resource, specify a negative bias of -1 to -99. Route 53 expands the size of adjacent regions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geoproximitylocation.html#cfn-route53-recordset-geoproximitylocation-bias
            '''
            result = self._values.get("bias")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def coordinates(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordSetPropsMixin.CoordinatesProperty"]]:
            '''Contains the longitude and latitude for a geographic region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geoproximitylocation.html#cfn-route53-recordset-geoproximitylocation-coordinates
            '''
            result = self._values.get("coordinates")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecordSetPropsMixin.CoordinatesProperty"]], result)

        @builtins.property
        def local_zone_group(self) -> typing.Optional[builtins.str]:
            '''Specifies an AWS Local Zone Group.

            A local Zone Group is usually the Local Zone code without the ending character. For example, if the Local Zone is ``us-east-1-bue-1a`` the Local Zone Group is ``us-east-1-bue-1`` .

            You can identify the Local Zones Group for a specific Local Zone by using the `describe-availability-zones <https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-availability-zones.html>`_ CLI command:

            This command returns: ``"GroupName": "us-west-2-den-1"`` , specifying that the Local Zone ``us-west-2-den-1a`` belongs to the Local Zone Group ``us-west-2-den-1`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geoproximitylocation.html#cfn-route53-recordset-geoproximitylocation-localzonegroup
            '''
            result = self._values.get("local_zone_group")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GeoProximityLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnCidrCollectionMixinProps",
    "CfnCidrCollectionPropsMixin",
    "CfnDNSSECMixinProps",
    "CfnDNSSECPropsMixin",
    "CfnHealthCheckMixinProps",
    "CfnHealthCheckPropsMixin",
    "CfnHostedZoneMixinProps",
    "CfnHostedZonePropsMixin",
    "CfnKeySigningKeyMixinProps",
    "CfnKeySigningKeyPropsMixin",
    "CfnRecordSetGroupMixinProps",
    "CfnRecordSetGroupPropsMixin",
    "CfnRecordSetMixinProps",
    "CfnRecordSetPropsMixin",
]

publication.publish()

def _typecheckingstub__4381a08c0c2cbcf2d6263120d563a88f6ce9eeb05465b276c02bcda50fa99bc7(
    *,
    locations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCidrCollectionPropsMixin.LocationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d7ef7c0909f7a76baf4c350b5b540dbf73e24cb11112c1e927a04aada3e9aa2(
    props: typing.Union[CfnCidrCollectionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf7873af7155301f3d321737d2a088c564272d26b5faaeb8bc197345e2edd004(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0763d2a9c52643604649b2b94695e77c2b05345468a1d229adafe8aee9a9f27(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbda44f4fbecd910d8ec14c6deafee7c1321aebc7765f32ff8052fb7a37cdd71(
    *,
    cidr_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    location_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__425176cad6f995ab72de3220473fa5db98ee4af2f06a9f0a06364abd18502a03(
    *,
    hosted_zone_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60394d48758e93bf095d8ae77ced2e2a573548a57c4a390cd4dd0d399257b72f(
    props: typing.Union[CfnDNSSECMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4843dc2928483315a98ee581e6b5feb6fdd522f5e165973aa8bfbb95c144a77c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0db8405b923289eb195755211ee77609074348efcf8419ee085e51fc74f182a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a98dbd034c669f1992f4f7f6d8770eb3bd4b215690d597b21cd8b06adc5182(
    *,
    health_check_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnHealthCheckPropsMixin.HealthCheckConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    health_check_tags: typing.Optional[typing.Sequence[typing.Union[CfnHealthCheckPropsMixin.HealthCheckTagProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__555b39fe277f35258bdc5b71bde824ab20b4a3ab03e585a51b8b9990e008c2b6(
    props: typing.Union[CfnHealthCheckMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a839970c929f598c3d0ee493261db550d21a6e3b9d0f9253d76905ac989a5bc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbb3ef4da4583208de571c70ced69e3dac3bb45248c94e9f67588bd1be8a1760(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ccc0f3d626755705c5850858a7a5284c21dce6763947a8840b704a126d1e52f(
    *,
    name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6f910ae03cedb36dad31b9de48f3366d4769842f256dfc22b311465116d076d(
    *,
    alarm_identifier: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnHealthCheckPropsMixin.AlarmIdentifierProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    child_health_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_sni: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    failure_threshold: typing.Optional[jsii.Number] = None,
    fully_qualified_domain_name: typing.Optional[builtins.str] = None,
    health_threshold: typing.Optional[jsii.Number] = None,
    insufficient_data_health_status: typing.Optional[builtins.str] = None,
    inverted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ip_address: typing.Optional[builtins.str] = None,
    measure_latency: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    port: typing.Optional[jsii.Number] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_interval: typing.Optional[jsii.Number] = None,
    resource_path: typing.Optional[builtins.str] = None,
    routing_control_arn: typing.Optional[builtins.str] = None,
    search_string: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515d044b538e4e93885694d595a95bc9de92eb535fdd0d613727cfe7b1a427eb(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1274c4e119a5111943c7c474fe81217deb26720caef2693a3eaf4bb3f961cdba(
    *,
    hosted_zone_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnHostedZonePropsMixin.HostedZoneConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    hosted_zone_tags: typing.Optional[typing.Sequence[typing.Union[CfnHostedZonePropsMixin.HostedZoneTagProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    query_logging_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnHostedZonePropsMixin.QueryLoggingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpcs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnHostedZonePropsMixin.VPCProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f395ee3d3ef050ddb5b40cc33a31525a836336b7600fc1ed3d2b71c99b346eb4(
    props: typing.Union[CfnHostedZoneMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a68b33204dc935eb4dc97d23a230fd7700280b4cbb7bb9e5d53d2ebb8dc788d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3623c06ec6ed06be317c76e4d696ea87ffecc68093214c461c1e0aa9c43446e6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dde17c1b770163098a7a8db50de473c5255fd88887341a9b0cb6407b7d66c91b(
    *,
    comment: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e3e058306abe7688662e01ece00f23f68c10a344ca435942920282a09e9a829(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cf5ee86e3529c37e33dc4f1bf06f11cba80de2cbdb3342f874f8f95cf32385d(
    *,
    cloud_watch_logs_log_group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b334713b8c988282a62557ff55a15cac60698518f93510170d32527c89b16a4b(
    *,
    vpc_id: typing.Optional[builtins.str] = None,
    vpc_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d605361f5974f0bac030fcb009ad12e47bdcece8f7f79d12bdfdb7607d585c2f(
    *,
    hosted_zone_id: typing.Optional[builtins.str] = None,
    key_management_service_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64f1a1d8a26eccbd5cef66b58d91a46c6895b4623981a0495ea25ffd8206800e(
    props: typing.Union[CfnKeySigningKeyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3094d1ac04a6143ea3a7278ac2e485baab5c2be123cad1395e1a91b0a32d8dbb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53e1bcd860885a2c1bf08b4c244a908cf23093a627713adbbae0c2860ee215c5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__003537c327ec31bc54cc31a2c09bd817db5ac8f8d8f366eeb469d79b59d7ca9c(
    *,
    comment: typing.Optional[builtins.str] = None,
    hosted_zone_id: typing.Optional[builtins.str] = None,
    hosted_zone_name: typing.Optional[builtins.str] = None,
    record_sets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRecordSetGroupPropsMixin.RecordSetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8269b04831cadefdb41fc68ad44fa9b722a8aa74e3658656e9ccbd58300557(
    props: typing.Union[CfnRecordSetGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57643a76be8544a244adf0fecbd03d20e6f3f19c5cf6772d8e0cf22388b89538(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdf61fa0795117b90a8d671e2f9aed13f2152f16bb281539ee69f4dcc7c15f5d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b666b53f4ee3d71b5d7b2ef2d60ba8663d347f3dadcc062e0bdaba41c6d1b49(
    *,
    dns_name: typing.Optional[builtins.str] = None,
    evaluate_target_health: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    hosted_zone_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8d55f5393bb8740143b8affc7451395b4fd9275860b0b7ef1fab1778d5fa83e(
    *,
    collection_id: typing.Optional[builtins.str] = None,
    location_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92185053b1268da08c5a6393edccc81ec25f4a74cf82fcb3a97c5e6b6e180383(
    *,
    latitude: typing.Optional[builtins.str] = None,
    longitude: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c94b9c8e6e08f441b76733e56a9ec475af4c8de0ed82e95f0f62dc091e67269f(
    *,
    continent_code: typing.Optional[builtins.str] = None,
    country_code: typing.Optional[builtins.str] = None,
    subdivision_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d708f0317446e31a991928807b92fded7aa2b497c5d5f4dbcfef64ae0d2783ae(
    *,
    aws_region: typing.Optional[builtins.str] = None,
    bias: typing.Optional[jsii.Number] = None,
    coordinates: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRecordSetGroupPropsMixin.CoordinatesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    local_zone_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8fa61ff0e1455726abcfff5dc086fd1a85b191b23d6736579fb241a9efebfca(
    *,
    alias_target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRecordSetGroupPropsMixin.AliasTargetProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cidr_routing_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRecordSetGroupPropsMixin.CidrRoutingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    failover: typing.Optional[builtins.str] = None,
    geo_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRecordSetGroupPropsMixin.GeoLocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    geo_proximity_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRecordSetGroupPropsMixin.GeoProximityLocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    health_check_id: typing.Optional[builtins.str] = None,
    hosted_zone_id: typing.Optional[builtins.str] = None,
    hosted_zone_name: typing.Optional[builtins.str] = None,
    multi_value_answer: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    resource_records: typing.Optional[typing.Sequence[builtins.str]] = None,
    set_identifier: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__237deea5889fe21fbc58a2f5eaad425c47f7a4b413b44bec068d8c608d289d2e(
    *,
    alias_target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRecordSetPropsMixin.AliasTargetProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cidr_routing_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRecordSetPropsMixin.CidrRoutingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    comment: typing.Optional[builtins.str] = None,
    failover: typing.Optional[builtins.str] = None,
    geo_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRecordSetPropsMixin.GeoLocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    geo_proximity_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRecordSetPropsMixin.GeoProximityLocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    health_check_id: typing.Optional[builtins.str] = None,
    hosted_zone_id: typing.Optional[builtins.str] = None,
    hosted_zone_name: typing.Optional[builtins.str] = None,
    multi_value_answer: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    resource_records: typing.Optional[typing.Sequence[builtins.str]] = None,
    set_identifier: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6513fe0a8bb865cb2fb56a732a4d1b9e1bc15b70bb43aa44afb7df46cfba49e5(
    props: typing.Union[CfnRecordSetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4590cc76a1b74eb6ecd905b7261cfba632d24b3a7d26552038ff1431a280a498(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__133723f7705380b1d981d4d909d9fd5744b5513e97a5e1c11b69fb8c05b0e7e0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__377e6b495784f342eb105a0b5165623b6b9189f04e7deb0e00b69e6f113946f2(
    *,
    dns_name: typing.Optional[builtins.str] = None,
    evaluate_target_health: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    hosted_zone_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c600739fc3b2839dd5fcf05e7034dfcac040f6f01006611750392bcec9b69eba(
    *,
    collection_id: typing.Optional[builtins.str] = None,
    location_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ae82ca3ed14b83f754ffd1bd4ed55bf576d9c914985864944ee9d880a872abf(
    *,
    latitude: typing.Optional[builtins.str] = None,
    longitude: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bca0d2f9fbda44862ef5ae71229b1647f191c573456e5ca52a3cad46fe1f28c(
    *,
    continent_code: typing.Optional[builtins.str] = None,
    country_code: typing.Optional[builtins.str] = None,
    subdivision_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__430a922679a9793ddb47ae25a44e2c81a604399b3f38b23b437849be099c678b(
    *,
    aws_region: typing.Optional[builtins.str] = None,
    bias: typing.Optional[jsii.Number] = None,
    coordinates: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRecordSetPropsMixin.CoordinatesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    local_zone_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
