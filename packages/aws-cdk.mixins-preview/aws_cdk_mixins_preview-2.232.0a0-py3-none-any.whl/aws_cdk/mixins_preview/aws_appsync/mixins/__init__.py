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
    jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnApiCacheMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_caching_behavior": "apiCachingBehavior",
        "api_id": "apiId",
        "at_rest_encryption_enabled": "atRestEncryptionEnabled",
        "health_metrics_config": "healthMetricsConfig",
        "transit_encryption_enabled": "transitEncryptionEnabled",
        "ttl": "ttl",
        "type": "type",
    },
)
class CfnApiCacheMixinProps:
    def __init__(
        self,
        *,
        api_caching_behavior: typing.Optional[builtins.str] = None,
        api_id: typing.Optional[builtins.str] = None,
        at_rest_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        health_metrics_config: typing.Optional[builtins.str] = None,
        transit_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ttl: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnApiCachePropsMixin.

        :param api_caching_behavior: Caching behavior. - *FULL_REQUEST_CACHING* : All requests from the same user are cached. Individual resolvers are automatically cached. All API calls will try to return responses from the cache. - *PER_RESOLVER_CACHING* : Individual resolvers that you specify are cached. - *OPERATION_LEVEL_CACHING* : Full requests are cached together and returned without executing resolvers.
        :param api_id: The GraphQL API ID.
        :param at_rest_encryption_enabled: *This parameter has been deprecated* . At-rest encryption flag for cache. You cannot update this setting after creation.
        :param health_metrics_config: Controls how cache health metrics will be emitted to CloudWatch. Cache health metrics include:. - *NetworkBandwidthOutAllowanceExceeded* : The network packets dropped because the throughput exceeded the aggregated bandwidth limit. This is useful for diagnosing bottlenecks in a cache configuration. - *EngineCPUUtilization* : The CPU utilization (percentage) allocated to the Redis process. This is useful for diagnosing bottlenecks in a cache configuration. Metrics will be recorded by API ID. You can set the value to ``ENABLED`` or ``DISABLED`` .
        :param transit_encryption_enabled: *This parameter has been deprecated* . Transit encryption flag when connecting to cache. You cannot update this setting after creation.
        :param ttl: TTL in seconds for cache entries. Valid values are 1–3,600 seconds.
        :param type: The cache instance type. Valid values are. - ``SMALL`` - ``MEDIUM`` - ``LARGE`` - ``XLARGE`` - ``LARGE_2X`` - ``LARGE_4X`` - ``LARGE_8X`` (not available in all regions) - ``LARGE_12X`` Historically, instance types were identified by an EC2-style value. As of July 2020, this is deprecated, and the generic identifiers above should be used. The following legacy instance types are available, but their use is discouraged: - *T2_SMALL* : A t2.small instance type. - *T2_MEDIUM* : A t2.medium instance type. - *R4_LARGE* : A r4.large instance type. - *R4_XLARGE* : A r4.xlarge instance type. - *R4_2XLARGE* : A r4.2xlarge instance type. - *R4_4XLARGE* : A r4.4xlarge instance type. - *R4_8XLARGE* : A r4.8xlarge instance type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apicache.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
            
            cfn_api_cache_mixin_props = appsync_mixins.CfnApiCacheMixinProps(
                api_caching_behavior="apiCachingBehavior",
                api_id="apiId",
                at_rest_encryption_enabled=False,
                health_metrics_config="healthMetricsConfig",
                transit_encryption_enabled=False,
                ttl=123,
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05c05b00857c4b21388f093f77b097d7ca6f21c88202eb411a79881de6ceec02)
            check_type(argname="argument api_caching_behavior", value=api_caching_behavior, expected_type=type_hints["api_caching_behavior"])
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument at_rest_encryption_enabled", value=at_rest_encryption_enabled, expected_type=type_hints["at_rest_encryption_enabled"])
            check_type(argname="argument health_metrics_config", value=health_metrics_config, expected_type=type_hints["health_metrics_config"])
            check_type(argname="argument transit_encryption_enabled", value=transit_encryption_enabled, expected_type=type_hints["transit_encryption_enabled"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_caching_behavior is not None:
            self._values["api_caching_behavior"] = api_caching_behavior
        if api_id is not None:
            self._values["api_id"] = api_id
        if at_rest_encryption_enabled is not None:
            self._values["at_rest_encryption_enabled"] = at_rest_encryption_enabled
        if health_metrics_config is not None:
            self._values["health_metrics_config"] = health_metrics_config
        if transit_encryption_enabled is not None:
            self._values["transit_encryption_enabled"] = transit_encryption_enabled
        if ttl is not None:
            self._values["ttl"] = ttl
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def api_caching_behavior(self) -> typing.Optional[builtins.str]:
        '''Caching behavior.

        - *FULL_REQUEST_CACHING* : All requests from the same user are cached. Individual resolvers are automatically cached. All API calls will try to return responses from the cache.
        - *PER_RESOLVER_CACHING* : Individual resolvers that you specify are cached.
        - *OPERATION_LEVEL_CACHING* : Full requests are cached together and returned without executing resolvers.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apicache.html#cfn-appsync-apicache-apicachingbehavior
        '''
        result = self._values.get("api_caching_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_id(self) -> typing.Optional[builtins.str]:
        '''The GraphQL API ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apicache.html#cfn-appsync-apicache-apiid
        '''
        result = self._values.get("api_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def at_rest_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''*This parameter has been deprecated* .

        At-rest encryption flag for cache. You cannot update this setting after creation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apicache.html#cfn-appsync-apicache-atrestencryptionenabled
        '''
        result = self._values.get("at_rest_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def health_metrics_config(self) -> typing.Optional[builtins.str]:
        '''Controls how cache health metrics will be emitted to CloudWatch. Cache health metrics include:.

        - *NetworkBandwidthOutAllowanceExceeded* : The network packets dropped because the throughput exceeded the aggregated bandwidth limit. This is useful for diagnosing bottlenecks in a cache configuration.
        - *EngineCPUUtilization* : The CPU utilization (percentage) allocated to the Redis process. This is useful for diagnosing bottlenecks in a cache configuration.

        Metrics will be recorded by API ID. You can set the value to ``ENABLED`` or ``DISABLED`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apicache.html#cfn-appsync-apicache-healthmetricsconfig
        '''
        result = self._values.get("health_metrics_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transit_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''*This parameter has been deprecated* .

        Transit encryption flag when connecting to cache. You cannot update this setting after creation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apicache.html#cfn-appsync-apicache-transitencryptionenabled
        '''
        result = self._values.get("transit_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def ttl(self) -> typing.Optional[jsii.Number]:
        '''TTL in seconds for cache entries.

        Valid values are 1–3,600 seconds.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apicache.html#cfn-appsync-apicache-ttl
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The cache instance type. Valid values are.

        - ``SMALL``
        - ``MEDIUM``
        - ``LARGE``
        - ``XLARGE``
        - ``LARGE_2X``
        - ``LARGE_4X``
        - ``LARGE_8X`` (not available in all regions)
        - ``LARGE_12X``

        Historically, instance types were identified by an EC2-style value. As of July 2020, this is deprecated, and the generic identifiers above should be used.

        The following legacy instance types are available, but their use is discouraged:

        - *T2_SMALL* : A t2.small instance type.
        - *T2_MEDIUM* : A t2.medium instance type.
        - *R4_LARGE* : A r4.large instance type.
        - *R4_XLARGE* : A r4.xlarge instance type.
        - *R4_2XLARGE* : A r4.2xlarge instance type.
        - *R4_4XLARGE* : A r4.4xlarge instance type.
        - *R4_8XLARGE* : A r4.8xlarge instance type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apicache.html#cfn-appsync-apicache-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApiCacheMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnApiCachePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnApiCachePropsMixin",
):
    '''The ``AWS::AppSync::ApiCache`` resource represents the input of a ``CreateApiCache`` operation.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apicache.html
    :cloudformationResource: AWS::AppSync::ApiCache
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
        
        cfn_api_cache_props_mixin = appsync_mixins.CfnApiCachePropsMixin(appsync_mixins.CfnApiCacheMixinProps(
            api_caching_behavior="apiCachingBehavior",
            api_id="apiId",
            at_rest_encryption_enabled=False,
            health_metrics_config="healthMetricsConfig",
            transit_encryption_enabled=False,
            ttl=123,
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnApiCacheMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppSync::ApiCache``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1e91198803cbf7b1d0b86b6bb97df4f192c19dc159ad4691d94b71ab889b64a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e586fb662a5a6b78db9fe649521d84234d9fb961e4a418e140c94f1693b3a55)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1249fbf23cc288a9561bbe3afe259dc369b98d8fe36efde3aa2c7c32f1f26e07)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnApiCacheMixinProps:
        return typing.cast(CfnApiCacheMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnApiKeyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "description": "description",
        "expires": "expires",
    },
)
class CfnApiKeyMixinProps:
    def __init__(
        self,
        *,
        api_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        expires: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for CfnApiKeyPropsMixin.

        :param api_id: Unique AWS AppSync GraphQL API ID for this API key.
        :param description: Unique description of your API key.
        :param expires: The time after which the API key expires. The date is represented as seconds since the epoch, rounded down to the nearest hour.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apikey.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
            
            cfn_api_key_mixin_props = appsync_mixins.CfnApiKeyMixinProps(
                api_id="apiId",
                description="description",
                expires=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0219c7805dbef682f022d17b1eb83874748d94e4869dc6d8d3a29fc2e3eec50d)
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument expires", value=expires, expected_type=type_hints["expires"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_id is not None:
            self._values["api_id"] = api_id
        if description is not None:
            self._values["description"] = description
        if expires is not None:
            self._values["expires"] = expires

    @builtins.property
    def api_id(self) -> typing.Optional[builtins.str]:
        '''Unique AWS AppSync GraphQL API ID for this API key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apikey.html#cfn-appsync-apikey-apiid
        '''
        result = self._values.get("api_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Unique description of your API key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apikey.html#cfn-appsync-apikey-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expires(self) -> typing.Optional[jsii.Number]:
        '''The time after which the API key expires.

        The date is represented as seconds since the epoch, rounded down to the nearest hour.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apikey.html#cfn-appsync-apikey-expires
        '''
        result = self._values.get("expires")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApiKeyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnApiKeyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnApiKeyPropsMixin",
):
    '''The ``AWS::AppSync::ApiKey`` resource creates a unique key that you can distribute to clients who are executing GraphQL operations with AWS AppSync that require an API key.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apikey.html
    :cloudformationResource: AWS::AppSync::ApiKey
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
        
        cfn_api_key_props_mixin = appsync_mixins.CfnApiKeyPropsMixin(appsync_mixins.CfnApiKeyMixinProps(
            api_id="apiId",
            description="description",
            expires=123
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnApiKeyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppSync::ApiKey``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1215d0acb74490c196f558c51c4774b2b5dd82c65a595537c57c2b5f150a6e64)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c36cbec7fe69772ecaa5cdf571ae3b3e48408e73b7321b5ffb1f35af517bea23)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4df8d7eec1dc15424ecca373ccf37dc69b5c6fcecd9db57d824fdb64e4fd1619)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnApiKeyMixinProps:
        return typing.cast(CfnApiKeyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnApiMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "event_config": "eventConfig",
        "name": "name",
        "owner_contact": "ownerContact",
        "tags": "tags",
    },
)
class CfnApiMixinProps:
    def __init__(
        self,
        *,
        event_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApiPropsMixin.EventConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        owner_contact: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnApiPropsMixin.

        :param event_config: Describes the authorization configuration for connections, message publishing, message subscriptions, and logging for an Event API.
        :param name: The name of the ``Api`` .
        :param owner_contact: The owner contact information for an API resource. This field accepts any string input with a length of 0 - 256 characters.
        :param tags: A set of tags (key-value pairs) for this API.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-api.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
            
            cfn_api_mixin_props = appsync_mixins.CfnApiMixinProps(
                event_config=appsync_mixins.CfnApiPropsMixin.EventConfigProperty(
                    auth_providers=[appsync_mixins.CfnApiPropsMixin.AuthProviderProperty(
                        auth_type="authType",
                        cognito_config=appsync_mixins.CfnApiPropsMixin.CognitoConfigProperty(
                            app_id_client_regex="appIdClientRegex",
                            aws_region="awsRegion",
                            user_pool_id="userPoolId"
                        ),
                        lambda_authorizer_config=appsync_mixins.CfnApiPropsMixin.LambdaAuthorizerConfigProperty(
                            authorizer_result_ttl_in_seconds=123,
                            authorizer_uri="authorizerUri",
                            identity_validation_expression="identityValidationExpression"
                        ),
                        open_id_connect_config=appsync_mixins.CfnApiPropsMixin.OpenIDConnectConfigProperty(
                            auth_ttl=123,
                            client_id="clientId",
                            iat_ttl=123,
                            issuer="issuer"
                        )
                    )],
                    connection_auth_modes=[appsync_mixins.CfnApiPropsMixin.AuthModeProperty(
                        auth_type="authType"
                    )],
                    default_publish_auth_modes=[appsync_mixins.CfnApiPropsMixin.AuthModeProperty(
                        auth_type="authType"
                    )],
                    default_subscribe_auth_modes=[appsync_mixins.CfnApiPropsMixin.AuthModeProperty(
                        auth_type="authType"
                    )],
                    log_config=appsync_mixins.CfnApiPropsMixin.EventLogConfigProperty(
                        cloud_watch_logs_role_arn="cloudWatchLogsRoleArn",
                        log_level="logLevel"
                    )
                ),
                name="name",
                owner_contact="ownerContact",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da0e231c7c55caafbb30c69054cc38c88eb0881c96178918d5d7bb2ebe82d66e)
            check_type(argname="argument event_config", value=event_config, expected_type=type_hints["event_config"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument owner_contact", value=owner_contact, expected_type=type_hints["owner_contact"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if event_config is not None:
            self._values["event_config"] = event_config
        if name is not None:
            self._values["name"] = name
        if owner_contact is not None:
            self._values["owner_contact"] = owner_contact
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def event_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.EventConfigProperty"]]:
        '''Describes the authorization configuration for connections, message publishing, message subscriptions, and logging for an Event API.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-api.html#cfn-appsync-api-eventconfig
        '''
        result = self._values.get("event_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.EventConfigProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the ``Api`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-api.html#cfn-appsync-api-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner_contact(self) -> typing.Optional[builtins.str]:
        '''The owner contact information for an API resource.

        This field accepts any string input with a length of 0 - 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-api.html#cfn-appsync-api-ownercontact
        '''
        result = self._values.get("owner_contact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A set of tags (key-value pairs) for this API.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-api.html#cfn-appsync-api-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApiMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnApiPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnApiPropsMixin",
):
    '''The ``AWS::AppSync::Api`` resource creates an AWS AppSync API that you can use for an AWS AppSync API with your preferred configuration, such as an Event API that provides real-time message publishing and message subscriptions over WebSockets.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-api.html
    :cloudformationResource: AWS::AppSync::Api
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
        
        cfn_api_props_mixin = appsync_mixins.CfnApiPropsMixin(appsync_mixins.CfnApiMixinProps(
            event_config=appsync_mixins.CfnApiPropsMixin.EventConfigProperty(
                auth_providers=[appsync_mixins.CfnApiPropsMixin.AuthProviderProperty(
                    auth_type="authType",
                    cognito_config=appsync_mixins.CfnApiPropsMixin.CognitoConfigProperty(
                        app_id_client_regex="appIdClientRegex",
                        aws_region="awsRegion",
                        user_pool_id="userPoolId"
                    ),
                    lambda_authorizer_config=appsync_mixins.CfnApiPropsMixin.LambdaAuthorizerConfigProperty(
                        authorizer_result_ttl_in_seconds=123,
                        authorizer_uri="authorizerUri",
                        identity_validation_expression="identityValidationExpression"
                    ),
                    open_id_connect_config=appsync_mixins.CfnApiPropsMixin.OpenIDConnectConfigProperty(
                        auth_ttl=123,
                        client_id="clientId",
                        iat_ttl=123,
                        issuer="issuer"
                    )
                )],
                connection_auth_modes=[appsync_mixins.CfnApiPropsMixin.AuthModeProperty(
                    auth_type="authType"
                )],
                default_publish_auth_modes=[appsync_mixins.CfnApiPropsMixin.AuthModeProperty(
                    auth_type="authType"
                )],
                default_subscribe_auth_modes=[appsync_mixins.CfnApiPropsMixin.AuthModeProperty(
                    auth_type="authType"
                )],
                log_config=appsync_mixins.CfnApiPropsMixin.EventLogConfigProperty(
                    cloud_watch_logs_role_arn="cloudWatchLogsRoleArn",
                    log_level="logLevel"
                )
            ),
            name="name",
            owner_contact="ownerContact",
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
        props: typing.Union[CfnApiMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppSync::Api``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c700091c61a6d27e42ab3f052878c4b487b9439e8609506d82d36bcf59b5121)
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
            type_hints = typing.get_type_hints(_typecheckingstub__590fa5c36f0a1c635fb29e7fb8d396d9e0dbff1be52ce1d47a9625898f72c675)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd51e64eb8bd6af8b75332e9364c8bea8362001ef97402dc069900f664a6ccbb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnApiMixinProps:
        return typing.cast(CfnApiMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnApiPropsMixin.AuthModeProperty",
        jsii_struct_bases=[],
        name_mapping={"auth_type": "authType"},
    )
    class AuthModeProperty:
        def __init__(self, *, auth_type: typing.Optional[builtins.str] = None) -> None:
            '''Describes an authorization configuration.

            Use ``AuthMode`` to specify the publishing and subscription authorization configuration for an Event API.

            :param auth_type: The authorization type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-authmode.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                auth_mode_property = appsync_mixins.CfnApiPropsMixin.AuthModeProperty(
                    auth_type="authType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c20afe4d1e881e46cc032a41b8025a21a037ec1625eeb277ee4e0f893470b455)
                check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auth_type is not None:
                self._values["auth_type"] = auth_type

        @builtins.property
        def auth_type(self) -> typing.Optional[builtins.str]:
            '''The authorization type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-authmode.html#cfn-appsync-api-authmode-authtype
            '''
            result = self._values.get("auth_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthModeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnApiPropsMixin.AuthProviderProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auth_type": "authType",
            "cognito_config": "cognitoConfig",
            "lambda_authorizer_config": "lambdaAuthorizerConfig",
            "open_id_connect_config": "openIdConnectConfig",
        },
    )
    class AuthProviderProperty:
        def __init__(
            self,
            *,
            auth_type: typing.Optional[builtins.str] = None,
            cognito_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApiPropsMixin.CognitoConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            lambda_authorizer_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApiPropsMixin.LambdaAuthorizerConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            open_id_connect_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApiPropsMixin.OpenIDConnectConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes an authorization provider.

            :param auth_type: The authorization type.
            :param cognito_config: Describes an Amazon Cognito user pool configuration.
            :param lambda_authorizer_config: A ``LambdaAuthorizerConfig`` specifies how to authorize AWS AppSync API access when using the ``AWS_LAMBDA`` authorizer mode. Be aware that an AWS AppSync API can have only one AWS Lambda authorizer configured at a time.
            :param open_id_connect_config: Describes an OpenID Connect (OIDC) configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-authprovider.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                auth_provider_property = appsync_mixins.CfnApiPropsMixin.AuthProviderProperty(
                    auth_type="authType",
                    cognito_config=appsync_mixins.CfnApiPropsMixin.CognitoConfigProperty(
                        app_id_client_regex="appIdClientRegex",
                        aws_region="awsRegion",
                        user_pool_id="userPoolId"
                    ),
                    lambda_authorizer_config=appsync_mixins.CfnApiPropsMixin.LambdaAuthorizerConfigProperty(
                        authorizer_result_ttl_in_seconds=123,
                        authorizer_uri="authorizerUri",
                        identity_validation_expression="identityValidationExpression"
                    ),
                    open_id_connect_config=appsync_mixins.CfnApiPropsMixin.OpenIDConnectConfigProperty(
                        auth_ttl=123,
                        client_id="clientId",
                        iat_ttl=123,
                        issuer="issuer"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__74ffc5fb5a61cd156fe437a4167a2cbabab7b43f99dbd11b5c4c25fe71df20d4)
                check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
                check_type(argname="argument cognito_config", value=cognito_config, expected_type=type_hints["cognito_config"])
                check_type(argname="argument lambda_authorizer_config", value=lambda_authorizer_config, expected_type=type_hints["lambda_authorizer_config"])
                check_type(argname="argument open_id_connect_config", value=open_id_connect_config, expected_type=type_hints["open_id_connect_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auth_type is not None:
                self._values["auth_type"] = auth_type
            if cognito_config is not None:
                self._values["cognito_config"] = cognito_config
            if lambda_authorizer_config is not None:
                self._values["lambda_authorizer_config"] = lambda_authorizer_config
            if open_id_connect_config is not None:
                self._values["open_id_connect_config"] = open_id_connect_config

        @builtins.property
        def auth_type(self) -> typing.Optional[builtins.str]:
            '''The authorization type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-authprovider.html#cfn-appsync-api-authprovider-authtype
            '''
            result = self._values.get("auth_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cognito_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.CognitoConfigProperty"]]:
            '''Describes an Amazon Cognito user pool configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-authprovider.html#cfn-appsync-api-authprovider-cognitoconfig
            '''
            result = self._values.get("cognito_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.CognitoConfigProperty"]], result)

        @builtins.property
        def lambda_authorizer_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.LambdaAuthorizerConfigProperty"]]:
            '''A ``LambdaAuthorizerConfig`` specifies how to authorize AWS AppSync API access when using the ``AWS_LAMBDA`` authorizer mode.

            Be aware that an AWS AppSync API can have only one AWS Lambda authorizer configured at a time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-authprovider.html#cfn-appsync-api-authprovider-lambdaauthorizerconfig
            '''
            result = self._values.get("lambda_authorizer_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.LambdaAuthorizerConfigProperty"]], result)

        @builtins.property
        def open_id_connect_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.OpenIDConnectConfigProperty"]]:
            '''Describes an OpenID Connect (OIDC) configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-authprovider.html#cfn-appsync-api-authprovider-openidconnectconfig
            '''
            result = self._values.get("open_id_connect_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.OpenIDConnectConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnApiPropsMixin.CognitoConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "app_id_client_regex": "appIdClientRegex",
            "aws_region": "awsRegion",
            "user_pool_id": "userPoolId",
        },
    )
    class CognitoConfigProperty:
        def __init__(
            self,
            *,
            app_id_client_regex: typing.Optional[builtins.str] = None,
            aws_region: typing.Optional[builtins.str] = None,
            user_pool_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes an Amazon Cognito configuration.

            :param app_id_client_regex: A regular expression for validating the incoming Amazon Cognito user pool app client ID. If this value isn't set, no filtering is applied.
            :param aws_region: The AWS Region in which the user pool was created.
            :param user_pool_id: The user pool ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-cognitoconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                cognito_config_property = appsync_mixins.CfnApiPropsMixin.CognitoConfigProperty(
                    app_id_client_regex="appIdClientRegex",
                    aws_region="awsRegion",
                    user_pool_id="userPoolId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b9396a768ce9abf7de89418a34f89dd6e0c260cd4b08d3a7f77d4e40772cade0)
                check_type(argname="argument app_id_client_regex", value=app_id_client_regex, expected_type=type_hints["app_id_client_regex"])
                check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if app_id_client_regex is not None:
                self._values["app_id_client_regex"] = app_id_client_regex
            if aws_region is not None:
                self._values["aws_region"] = aws_region
            if user_pool_id is not None:
                self._values["user_pool_id"] = user_pool_id

        @builtins.property
        def app_id_client_regex(self) -> typing.Optional[builtins.str]:
            '''A regular expression for validating the incoming Amazon Cognito user pool app client ID.

            If this value isn't set, no filtering is applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-cognitoconfig.html#cfn-appsync-api-cognitoconfig-appidclientregex
            '''
            result = self._values.get("app_id_client_regex")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def aws_region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region in which the user pool was created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-cognitoconfig.html#cfn-appsync-api-cognitoconfig-awsregion
            '''
            result = self._values.get("aws_region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_pool_id(self) -> typing.Optional[builtins.str]:
            '''The user pool ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-cognitoconfig.html#cfn-appsync-api-cognitoconfig-userpoolid
            '''
            result = self._values.get("user_pool_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CognitoConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnApiPropsMixin.DnsMapProperty",
        jsii_struct_bases=[],
        name_mapping={"http": "http", "realtime": "realtime"},
    )
    class DnsMapProperty:
        def __init__(
            self,
            *,
            http: typing.Optional[builtins.str] = None,
            realtime: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A map of DNS names for the Api.

            :param http: The domain name of the Api's HTTP endpoint.
            :param realtime: The domain name of the Api's real-time endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-dnsmap.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                dns_map_property = appsync_mixins.CfnApiPropsMixin.DnsMapProperty(
                    http="http",
                    realtime="realtime"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e3866e4e00b8a19383ab970813f60f67c6e6c8ce2ce1ee5688df0f7b48cb24b2)
                check_type(argname="argument http", value=http, expected_type=type_hints["http"])
                check_type(argname="argument realtime", value=realtime, expected_type=type_hints["realtime"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if http is not None:
                self._values["http"] = http
            if realtime is not None:
                self._values["realtime"] = realtime

        @builtins.property
        def http(self) -> typing.Optional[builtins.str]:
            '''The domain name of the Api's HTTP endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-dnsmap.html#cfn-appsync-api-dnsmap-http
            '''
            result = self._values.get("http")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def realtime(self) -> typing.Optional[builtins.str]:
            '''The domain name of the Api's real-time endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-dnsmap.html#cfn-appsync-api-dnsmap-realtime
            '''
            result = self._values.get("realtime")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DnsMapProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnApiPropsMixin.EventConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auth_providers": "authProviders",
            "connection_auth_modes": "connectionAuthModes",
            "default_publish_auth_modes": "defaultPublishAuthModes",
            "default_subscribe_auth_modes": "defaultSubscribeAuthModes",
            "log_config": "logConfig",
        },
    )
    class EventConfigProperty:
        def __init__(
            self,
            *,
            auth_providers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApiPropsMixin.AuthProviderProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            connection_auth_modes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApiPropsMixin.AuthModeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            default_publish_auth_modes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApiPropsMixin.AuthModeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            default_subscribe_auth_modes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApiPropsMixin.AuthModeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            log_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApiPropsMixin.EventLogConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes the authorization configuration for connections, message publishing, message subscriptions, and logging for an Event API.

            :param auth_providers: A list of authorization providers.
            :param connection_auth_modes: A list of valid authorization modes for the Event API connections.
            :param default_publish_auth_modes: A list of valid authorization modes for the Event API publishing.
            :param default_subscribe_auth_modes: A list of valid authorization modes for the Event API subscriptions.
            :param log_config: The CloudWatch Logs configuration for the Event API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-eventconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                event_config_property = appsync_mixins.CfnApiPropsMixin.EventConfigProperty(
                    auth_providers=[appsync_mixins.CfnApiPropsMixin.AuthProviderProperty(
                        auth_type="authType",
                        cognito_config=appsync_mixins.CfnApiPropsMixin.CognitoConfigProperty(
                            app_id_client_regex="appIdClientRegex",
                            aws_region="awsRegion",
                            user_pool_id="userPoolId"
                        ),
                        lambda_authorizer_config=appsync_mixins.CfnApiPropsMixin.LambdaAuthorizerConfigProperty(
                            authorizer_result_ttl_in_seconds=123,
                            authorizer_uri="authorizerUri",
                            identity_validation_expression="identityValidationExpression"
                        ),
                        open_id_connect_config=appsync_mixins.CfnApiPropsMixin.OpenIDConnectConfigProperty(
                            auth_ttl=123,
                            client_id="clientId",
                            iat_ttl=123,
                            issuer="issuer"
                        )
                    )],
                    connection_auth_modes=[appsync_mixins.CfnApiPropsMixin.AuthModeProperty(
                        auth_type="authType"
                    )],
                    default_publish_auth_modes=[appsync_mixins.CfnApiPropsMixin.AuthModeProperty(
                        auth_type="authType"
                    )],
                    default_subscribe_auth_modes=[appsync_mixins.CfnApiPropsMixin.AuthModeProperty(
                        auth_type="authType"
                    )],
                    log_config=appsync_mixins.CfnApiPropsMixin.EventLogConfigProperty(
                        cloud_watch_logs_role_arn="cloudWatchLogsRoleArn",
                        log_level="logLevel"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6e2a3afb45c1d4d5da2eafdaf5dea3bd4e5ca2a776d4e25109fde239bdd19def)
                check_type(argname="argument auth_providers", value=auth_providers, expected_type=type_hints["auth_providers"])
                check_type(argname="argument connection_auth_modes", value=connection_auth_modes, expected_type=type_hints["connection_auth_modes"])
                check_type(argname="argument default_publish_auth_modes", value=default_publish_auth_modes, expected_type=type_hints["default_publish_auth_modes"])
                check_type(argname="argument default_subscribe_auth_modes", value=default_subscribe_auth_modes, expected_type=type_hints["default_subscribe_auth_modes"])
                check_type(argname="argument log_config", value=log_config, expected_type=type_hints["log_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auth_providers is not None:
                self._values["auth_providers"] = auth_providers
            if connection_auth_modes is not None:
                self._values["connection_auth_modes"] = connection_auth_modes
            if default_publish_auth_modes is not None:
                self._values["default_publish_auth_modes"] = default_publish_auth_modes
            if default_subscribe_auth_modes is not None:
                self._values["default_subscribe_auth_modes"] = default_subscribe_auth_modes
            if log_config is not None:
                self._values["log_config"] = log_config

        @builtins.property
        def auth_providers(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.AuthProviderProperty"]]]]:
            '''A list of authorization providers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-eventconfig.html#cfn-appsync-api-eventconfig-authproviders
            '''
            result = self._values.get("auth_providers")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.AuthProviderProperty"]]]], result)

        @builtins.property
        def connection_auth_modes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.AuthModeProperty"]]]]:
            '''A list of valid authorization modes for the Event API connections.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-eventconfig.html#cfn-appsync-api-eventconfig-connectionauthmodes
            '''
            result = self._values.get("connection_auth_modes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.AuthModeProperty"]]]], result)

        @builtins.property
        def default_publish_auth_modes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.AuthModeProperty"]]]]:
            '''A list of valid authorization modes for the Event API publishing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-eventconfig.html#cfn-appsync-api-eventconfig-defaultpublishauthmodes
            '''
            result = self._values.get("default_publish_auth_modes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.AuthModeProperty"]]]], result)

        @builtins.property
        def default_subscribe_auth_modes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.AuthModeProperty"]]]]:
            '''A list of valid authorization modes for the Event API subscriptions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-eventconfig.html#cfn-appsync-api-eventconfig-defaultsubscribeauthmodes
            '''
            result = self._values.get("default_subscribe_auth_modes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.AuthModeProperty"]]]], result)

        @builtins.property
        def log_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.EventLogConfigProperty"]]:
            '''The CloudWatch Logs configuration for the Event API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-eventconfig.html#cfn-appsync-api-eventconfig-logconfig
            '''
            result = self._values.get("log_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.EventLogConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnApiPropsMixin.EventLogConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_logs_role_arn": "cloudWatchLogsRoleArn",
            "log_level": "logLevel",
        },
    )
    class EventLogConfigProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs_role_arn: typing.Optional[builtins.str] = None,
            log_level: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the CloudWatch Logs configuration for the Event API.

            :param cloud_watch_logs_role_arn: The IAM service role that AWS AppSync assumes to publish CloudWatch Logs in your account.
            :param log_level: The type of information to log for the Event API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-eventlogconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                event_log_config_property = appsync_mixins.CfnApiPropsMixin.EventLogConfigProperty(
                    cloud_watch_logs_role_arn="cloudWatchLogsRoleArn",
                    log_level="logLevel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a06a75638e023e8a591df69c26ca92e50844d2a2aca6f95b630b2381dbe07cd3)
                check_type(argname="argument cloud_watch_logs_role_arn", value=cloud_watch_logs_role_arn, expected_type=type_hints["cloud_watch_logs_role_arn"])
                check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logs_role_arn is not None:
                self._values["cloud_watch_logs_role_arn"] = cloud_watch_logs_role_arn
            if log_level is not None:
                self._values["log_level"] = log_level

        @builtins.property
        def cloud_watch_logs_role_arn(self) -> typing.Optional[builtins.str]:
            '''The IAM service role that AWS AppSync assumes to publish CloudWatch Logs in your account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-eventlogconfig.html#cfn-appsync-api-eventlogconfig-cloudwatchlogsrolearn
            '''
            result = self._values.get("cloud_watch_logs_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_level(self) -> typing.Optional[builtins.str]:
            '''The type of information to log for the Event API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-eventlogconfig.html#cfn-appsync-api-eventlogconfig-loglevel
            '''
            result = self._values.get("log_level")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventLogConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnApiPropsMixin.LambdaAuthorizerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorizer_result_ttl_in_seconds": "authorizerResultTtlInSeconds",
            "authorizer_uri": "authorizerUri",
            "identity_validation_expression": "identityValidationExpression",
        },
    )
    class LambdaAuthorizerConfigProperty:
        def __init__(
            self,
            *,
            authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number] = None,
            authorizer_uri: typing.Optional[builtins.str] = None,
            identity_validation_expression: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A ``LambdaAuthorizerConfig`` specifies how to authorize AWS AppSync API access when using the ``AWS_LAMBDA`` authorizer mode.

            Be aware that an AWS AppSync API can have only one AWS Lambda authorizer configured at a time.

            :param authorizer_result_ttl_in_seconds: The number of seconds a response should be cached for. The default is 0 seconds, which disables caching. If you don't specify a value for ``authorizerResultTtlInSeconds`` , the default value is used. The maximum value is one hour (3600 seconds). The Lambda function can override this by returning a ``ttlOverride`` key in its response.
            :param authorizer_uri: The Amazon Resource Name (ARN) of the Lambda function to be called for authorization. This can be a standard Lambda ARN, a version ARN ( ``.../v3`` ), or an alias ARN. *Note* : This Lambda function must have the following resource-based policy assigned to it. When configuring Lambda authorizers in the console, this is done for you. To use the AWS Command Line Interface ( AWS CLI ), run the following: ``aws lambda add-permission --function-name "arn:aws:lambda:us-east-2:111122223333:function:my-function" --statement-id "appsync" --principal appsync.amazonaws.com --action lambda:InvokeFunction``
            :param identity_validation_expression: A regular expression for validation of tokens before the Lambda function is called.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-lambdaauthorizerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                lambda_authorizer_config_property = appsync_mixins.CfnApiPropsMixin.LambdaAuthorizerConfigProperty(
                    authorizer_result_ttl_in_seconds=123,
                    authorizer_uri="authorizerUri",
                    identity_validation_expression="identityValidationExpression"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5ccdf6a81bd8a98560c0bd8442a0fca6e0c52e901ca6e2f59044b2d443e09e7f)
                check_type(argname="argument authorizer_result_ttl_in_seconds", value=authorizer_result_ttl_in_seconds, expected_type=type_hints["authorizer_result_ttl_in_seconds"])
                check_type(argname="argument authorizer_uri", value=authorizer_uri, expected_type=type_hints["authorizer_uri"])
                check_type(argname="argument identity_validation_expression", value=identity_validation_expression, expected_type=type_hints["identity_validation_expression"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authorizer_result_ttl_in_seconds is not None:
                self._values["authorizer_result_ttl_in_seconds"] = authorizer_result_ttl_in_seconds
            if authorizer_uri is not None:
                self._values["authorizer_uri"] = authorizer_uri
            if identity_validation_expression is not None:
                self._values["identity_validation_expression"] = identity_validation_expression

        @builtins.property
        def authorizer_result_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The number of seconds a response should be cached for.

            The default is 0 seconds, which disables caching. If you don't specify a value for ``authorizerResultTtlInSeconds`` , the default value is used. The maximum value is one hour (3600 seconds). The Lambda function can override this by returning a ``ttlOverride`` key in its response.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-lambdaauthorizerconfig.html#cfn-appsync-api-lambdaauthorizerconfig-authorizerresultttlinseconds
            '''
            result = self._values.get("authorizer_result_ttl_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def authorizer_uri(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Lambda function to be called for authorization.

            This can be a standard Lambda ARN, a version ARN ( ``.../v3`` ), or an alias ARN.

            *Note* : This Lambda function must have the following resource-based policy assigned to it. When configuring Lambda authorizers in the console, this is done for you. To use the AWS Command Line Interface ( AWS CLI ), run the following:

            ``aws lambda add-permission --function-name "arn:aws:lambda:us-east-2:111122223333:function:my-function" --statement-id "appsync" --principal appsync.amazonaws.com --action lambda:InvokeFunction``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-lambdaauthorizerconfig.html#cfn-appsync-api-lambdaauthorizerconfig-authorizeruri
            '''
            result = self._values.get("authorizer_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def identity_validation_expression(self) -> typing.Optional[builtins.str]:
            '''A regular expression for validation of tokens before the Lambda function is called.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-lambdaauthorizerconfig.html#cfn-appsync-api-lambdaauthorizerconfig-identityvalidationexpression
            '''
            result = self._values.get("identity_validation_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaAuthorizerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnApiPropsMixin.OpenIDConnectConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auth_ttl": "authTtl",
            "client_id": "clientId",
            "iat_ttl": "iatTtl",
            "issuer": "issuer",
        },
    )
    class OpenIDConnectConfigProperty:
        def __init__(
            self,
            *,
            auth_ttl: typing.Optional[jsii.Number] = None,
            client_id: typing.Optional[builtins.str] = None,
            iat_ttl: typing.Optional[jsii.Number] = None,
            issuer: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes an OpenID Connect (OIDC) configuration.

            :param auth_ttl: The number of milliseconds that a token is valid after being authenticated.
            :param client_id: The client identifier of the relying party at the OpenID identity provider. This identifier is typically obtained when the relying party is registered with the OpenID identity provider. You can specify a regular expression so that AWS AppSync can validate against multiple client identifiers at a time.
            :param iat_ttl: The number of milliseconds that a token is valid after it's issued to a user.
            :param issuer: The issuer for the OIDC configuration. The issuer returned by discovery must exactly match the value of ``iss`` in the ID token.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-openidconnectconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                open_iDConnect_config_property = appsync_mixins.CfnApiPropsMixin.OpenIDConnectConfigProperty(
                    auth_ttl=123,
                    client_id="clientId",
                    iat_ttl=123,
                    issuer="issuer"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a4f52bdb79d243a46baeb71994507cdf4eb62e7ddfe5a057f367bd258972322)
                check_type(argname="argument auth_ttl", value=auth_ttl, expected_type=type_hints["auth_ttl"])
                check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
                check_type(argname="argument iat_ttl", value=iat_ttl, expected_type=type_hints["iat_ttl"])
                check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auth_ttl is not None:
                self._values["auth_ttl"] = auth_ttl
            if client_id is not None:
                self._values["client_id"] = client_id
            if iat_ttl is not None:
                self._values["iat_ttl"] = iat_ttl
            if issuer is not None:
                self._values["issuer"] = issuer

        @builtins.property
        def auth_ttl(self) -> typing.Optional[jsii.Number]:
            '''The number of milliseconds that a token is valid after being authenticated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-openidconnectconfig.html#cfn-appsync-api-openidconnectconfig-authttl
            '''
            result = self._values.get("auth_ttl")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def client_id(self) -> typing.Optional[builtins.str]:
            '''The client identifier of the relying party at the OpenID identity provider.

            This identifier is typically obtained when the relying party is registered with the OpenID identity provider. You can specify a regular expression so that AWS AppSync can validate against multiple client identifiers at a time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-openidconnectconfig.html#cfn-appsync-api-openidconnectconfig-clientid
            '''
            result = self._values.get("client_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def iat_ttl(self) -> typing.Optional[jsii.Number]:
            '''The number of milliseconds that a token is valid after it's issued to a user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-openidconnectconfig.html#cfn-appsync-api-openidconnectconfig-iatttl
            '''
            result = self._values.get("iat_ttl")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def issuer(self) -> typing.Optional[builtins.str]:
            '''The issuer for the OIDC configuration.

            The issuer returned by discovery must exactly match the value of ``iss`` in the ID token.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-api-openidconnectconfig.html#cfn-appsync-api-openidconnectconfig-issuer
            '''
            result = self._values.get("issuer")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OpenIDConnectConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnChannelNamespaceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "code_handlers": "codeHandlers",
        "code_s3_location": "codeS3Location",
        "handler_configs": "handlerConfigs",
        "name": "name",
        "publish_auth_modes": "publishAuthModes",
        "subscribe_auth_modes": "subscribeAuthModes",
        "tags": "tags",
    },
)
class CfnChannelNamespaceMixinProps:
    def __init__(
        self,
        *,
        api_id: typing.Optional[builtins.str] = None,
        code_handlers: typing.Optional[builtins.str] = None,
        code_s3_location: typing.Optional[builtins.str] = None,
        handler_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnChannelNamespacePropsMixin.HandlerConfigsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        publish_auth_modes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnChannelNamespacePropsMixin.AuthModeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        subscribe_auth_modes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnChannelNamespacePropsMixin.AuthModeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnChannelNamespacePropsMixin.

        :param api_id: The ``Api`` ID.
        :param code_handlers: The event handler functions that run custom business logic to process published events and subscribe requests.
        :param code_s3_location: The Amazon S3 endpoint where the code is located.
        :param handler_configs: The configuration for the ``OnPublish`` and ``OnSubscribe`` handlers.
        :param name: The name of the channel namespace. This name must be unique within the ``Api`` .
        :param publish_auth_modes: The authorization mode to use for publishing messages on the channel namespace. This configuration overrides the default ``Api`` authorization configuration.
        :param subscribe_auth_modes: The authorization mode to use for subscribing to messages on the channel namespace. This configuration overrides the default ``Api`` authorization configuration.
        :param tags: A set of tags (key-value pairs) for this channel namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-channelnamespace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
            
            cfn_channel_namespace_mixin_props = appsync_mixins.CfnChannelNamespaceMixinProps(
                api_id="apiId",
                code_handlers="codeHandlers",
                code_s3_location="codeS3Location",
                handler_configs=appsync_mixins.CfnChannelNamespacePropsMixin.HandlerConfigsProperty(
                    on_publish=appsync_mixins.CfnChannelNamespacePropsMixin.HandlerConfigProperty(
                        behavior="behavior",
                        integration=appsync_mixins.CfnChannelNamespacePropsMixin.IntegrationProperty(
                            data_source_name="dataSourceName",
                            lambda_config=appsync_mixins.CfnChannelNamespacePropsMixin.LambdaConfigProperty(
                                invoke_type="invokeType"
                            )
                        )
                    ),
                    on_subscribe=appsync_mixins.CfnChannelNamespacePropsMixin.HandlerConfigProperty(
                        behavior="behavior",
                        integration=appsync_mixins.CfnChannelNamespacePropsMixin.IntegrationProperty(
                            data_source_name="dataSourceName",
                            lambda_config=appsync_mixins.CfnChannelNamespacePropsMixin.LambdaConfigProperty(
                                invoke_type="invokeType"
                            )
                        )
                    )
                ),
                name="name",
                publish_auth_modes=[appsync_mixins.CfnChannelNamespacePropsMixin.AuthModeProperty(
                    auth_type="authType"
                )],
                subscribe_auth_modes=[appsync_mixins.CfnChannelNamespacePropsMixin.AuthModeProperty(
                    auth_type="authType"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62d439405ed9d731fe067189dd22a1290af0b0e9c822793785392321b9be2998)
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument code_handlers", value=code_handlers, expected_type=type_hints["code_handlers"])
            check_type(argname="argument code_s3_location", value=code_s3_location, expected_type=type_hints["code_s3_location"])
            check_type(argname="argument handler_configs", value=handler_configs, expected_type=type_hints["handler_configs"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument publish_auth_modes", value=publish_auth_modes, expected_type=type_hints["publish_auth_modes"])
            check_type(argname="argument subscribe_auth_modes", value=subscribe_auth_modes, expected_type=type_hints["subscribe_auth_modes"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_id is not None:
            self._values["api_id"] = api_id
        if code_handlers is not None:
            self._values["code_handlers"] = code_handlers
        if code_s3_location is not None:
            self._values["code_s3_location"] = code_s3_location
        if handler_configs is not None:
            self._values["handler_configs"] = handler_configs
        if name is not None:
            self._values["name"] = name
        if publish_auth_modes is not None:
            self._values["publish_auth_modes"] = publish_auth_modes
        if subscribe_auth_modes is not None:
            self._values["subscribe_auth_modes"] = subscribe_auth_modes
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def api_id(self) -> typing.Optional[builtins.str]:
        '''The ``Api`` ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-channelnamespace.html#cfn-appsync-channelnamespace-apiid
        '''
        result = self._values.get("api_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_handlers(self) -> typing.Optional[builtins.str]:
        '''The event handler functions that run custom business logic to process published events and subscribe requests.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-channelnamespace.html#cfn-appsync-channelnamespace-codehandlers
        '''
        result = self._values.get("code_handlers")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_s3_location(self) -> typing.Optional[builtins.str]:
        '''The Amazon S3 endpoint where the code is located.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-channelnamespace.html#cfn-appsync-channelnamespace-codes3location
        '''
        result = self._values.get("code_s3_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def handler_configs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelNamespacePropsMixin.HandlerConfigsProperty"]]:
        '''The configuration for the ``OnPublish`` and ``OnSubscribe`` handlers.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-channelnamespace.html#cfn-appsync-channelnamespace-handlerconfigs
        '''
        result = self._values.get("handler_configs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelNamespacePropsMixin.HandlerConfigsProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the channel namespace.

        This name must be unique within the ``Api`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-channelnamespace.html#cfn-appsync-channelnamespace-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publish_auth_modes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelNamespacePropsMixin.AuthModeProperty"]]]]:
        '''The authorization mode to use for publishing messages on the channel namespace.

        This configuration overrides the default ``Api`` authorization configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-channelnamespace.html#cfn-appsync-channelnamespace-publishauthmodes
        '''
        result = self._values.get("publish_auth_modes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelNamespacePropsMixin.AuthModeProperty"]]]], result)

    @builtins.property
    def subscribe_auth_modes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelNamespacePropsMixin.AuthModeProperty"]]]]:
        '''The authorization mode to use for subscribing to messages on the channel namespace.

        This configuration overrides the default ``Api`` authorization configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-channelnamespace.html#cfn-appsync-channelnamespace-subscribeauthmodes
        '''
        result = self._values.get("subscribe_auth_modes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelNamespacePropsMixin.AuthModeProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A set of tags (key-value pairs) for this channel namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-channelnamespace.html#cfn-appsync-channelnamespace-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnChannelNamespaceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnChannelNamespacePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnChannelNamespacePropsMixin",
):
    '''The ``AWS::AppSync::ChannelNamespace`` resource creates a channel namespace associated with an ``Api`` .

    The ``ChannelNamespace`` contains the definitions for code handlers for the ``Api`` .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-channelnamespace.html
    :cloudformationResource: AWS::AppSync::ChannelNamespace
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
        
        cfn_channel_namespace_props_mixin = appsync_mixins.CfnChannelNamespacePropsMixin(appsync_mixins.CfnChannelNamespaceMixinProps(
            api_id="apiId",
            code_handlers="codeHandlers",
            code_s3_location="codeS3Location",
            handler_configs=appsync_mixins.CfnChannelNamespacePropsMixin.HandlerConfigsProperty(
                on_publish=appsync_mixins.CfnChannelNamespacePropsMixin.HandlerConfigProperty(
                    behavior="behavior",
                    integration=appsync_mixins.CfnChannelNamespacePropsMixin.IntegrationProperty(
                        data_source_name="dataSourceName",
                        lambda_config=appsync_mixins.CfnChannelNamespacePropsMixin.LambdaConfigProperty(
                            invoke_type="invokeType"
                        )
                    )
                ),
                on_subscribe=appsync_mixins.CfnChannelNamespacePropsMixin.HandlerConfigProperty(
                    behavior="behavior",
                    integration=appsync_mixins.CfnChannelNamespacePropsMixin.IntegrationProperty(
                        data_source_name="dataSourceName",
                        lambda_config=appsync_mixins.CfnChannelNamespacePropsMixin.LambdaConfigProperty(
                            invoke_type="invokeType"
                        )
                    )
                )
            ),
            name="name",
            publish_auth_modes=[appsync_mixins.CfnChannelNamespacePropsMixin.AuthModeProperty(
                auth_type="authType"
            )],
            subscribe_auth_modes=[appsync_mixins.CfnChannelNamespacePropsMixin.AuthModeProperty(
                auth_type="authType"
            )],
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
        props: typing.Union[CfnChannelNamespaceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppSync::ChannelNamespace``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cf8e57cb5ef4cfe94d2bbfd770f3fe85428895af661cda96a2f9892d90dfd53)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c137e0e22031ff19eb0637d05eccb3da1e5d9ae220ac0b3d883f21909f2d106)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e0214bec14d4a7bf806fc23d076a82ab1c932b9af7a078cb7b40f42c8c6e5ae)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnChannelNamespaceMixinProps:
        return typing.cast(CfnChannelNamespaceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnChannelNamespacePropsMixin.AuthModeProperty",
        jsii_struct_bases=[],
        name_mapping={"auth_type": "authType"},
    )
    class AuthModeProperty:
        def __init__(self, *, auth_type: typing.Optional[builtins.str] = None) -> None:
            '''Describes an authorization configuration.

            Use ``AuthMode`` to specify the publishing and subscription authorization configuration for an Event API.

            :param auth_type: The authorization type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-channelnamespace-authmode.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                auth_mode_property = appsync_mixins.CfnChannelNamespacePropsMixin.AuthModeProperty(
                    auth_type="authType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4acc107db66d954a845af466a45072d3c0dfd604646910003c28750e7583b79e)
                check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auth_type is not None:
                self._values["auth_type"] = auth_type

        @builtins.property
        def auth_type(self) -> typing.Optional[builtins.str]:
            '''The authorization type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-channelnamespace-authmode.html#cfn-appsync-channelnamespace-authmode-authtype
            '''
            result = self._values.get("auth_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthModeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnChannelNamespacePropsMixin.HandlerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"behavior": "behavior", "integration": "integration"},
    )
    class HandlerConfigProperty:
        def __init__(
            self,
            *,
            behavior: typing.Optional[builtins.str] = None,
            integration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnChannelNamespacePropsMixin.IntegrationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The ``HandlerConfig`` property type specifies the configuration for the handler.

            :param behavior: The behavior for the handler.
            :param integration: The integration data source configuration for the handler.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-channelnamespace-handlerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                handler_config_property = appsync_mixins.CfnChannelNamespacePropsMixin.HandlerConfigProperty(
                    behavior="behavior",
                    integration=appsync_mixins.CfnChannelNamespacePropsMixin.IntegrationProperty(
                        data_source_name="dataSourceName",
                        lambda_config=appsync_mixins.CfnChannelNamespacePropsMixin.LambdaConfigProperty(
                            invoke_type="invokeType"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__591dc766aef641e8f3c23304c0a401c408641c54d0d9850901e8df04d9b99200)
                check_type(argname="argument behavior", value=behavior, expected_type=type_hints["behavior"])
                check_type(argname="argument integration", value=integration, expected_type=type_hints["integration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if behavior is not None:
                self._values["behavior"] = behavior
            if integration is not None:
                self._values["integration"] = integration

        @builtins.property
        def behavior(self) -> typing.Optional[builtins.str]:
            '''The behavior for the handler.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-channelnamespace-handlerconfig.html#cfn-appsync-channelnamespace-handlerconfig-behavior
            '''
            result = self._values.get("behavior")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def integration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelNamespacePropsMixin.IntegrationProperty"]]:
            '''The integration data source configuration for the handler.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-channelnamespace-handlerconfig.html#cfn-appsync-channelnamespace-handlerconfig-integration
            '''
            result = self._values.get("integration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelNamespacePropsMixin.IntegrationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HandlerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnChannelNamespacePropsMixin.HandlerConfigsProperty",
        jsii_struct_bases=[],
        name_mapping={"on_publish": "onPublish", "on_subscribe": "onSubscribe"},
    )
    class HandlerConfigsProperty:
        def __init__(
            self,
            *,
            on_publish: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnChannelNamespacePropsMixin.HandlerConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            on_subscribe: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnChannelNamespacePropsMixin.HandlerConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The ``HandlerConfigs`` property type specifies the configuration for the ``OnPublish`` and ``OnSubscribe`` handlers.

            :param on_publish: The configuration for the ``OnPublish`` handler.
            :param on_subscribe: The configuration for the ``OnSubscribe`` handler.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-channelnamespace-handlerconfigs.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                handler_configs_property = appsync_mixins.CfnChannelNamespacePropsMixin.HandlerConfigsProperty(
                    on_publish=appsync_mixins.CfnChannelNamespacePropsMixin.HandlerConfigProperty(
                        behavior="behavior",
                        integration=appsync_mixins.CfnChannelNamespacePropsMixin.IntegrationProperty(
                            data_source_name="dataSourceName",
                            lambda_config=appsync_mixins.CfnChannelNamespacePropsMixin.LambdaConfigProperty(
                                invoke_type="invokeType"
                            )
                        )
                    ),
                    on_subscribe=appsync_mixins.CfnChannelNamespacePropsMixin.HandlerConfigProperty(
                        behavior="behavior",
                        integration=appsync_mixins.CfnChannelNamespacePropsMixin.IntegrationProperty(
                            data_source_name="dataSourceName",
                            lambda_config=appsync_mixins.CfnChannelNamespacePropsMixin.LambdaConfigProperty(
                                invoke_type="invokeType"
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d3958e39f93544ad1be5291a97d76058bd81357ba379ea9789b993ee2b58f396)
                check_type(argname="argument on_publish", value=on_publish, expected_type=type_hints["on_publish"])
                check_type(argname="argument on_subscribe", value=on_subscribe, expected_type=type_hints["on_subscribe"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if on_publish is not None:
                self._values["on_publish"] = on_publish
            if on_subscribe is not None:
                self._values["on_subscribe"] = on_subscribe

        @builtins.property
        def on_publish(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelNamespacePropsMixin.HandlerConfigProperty"]]:
            '''The configuration for the ``OnPublish`` handler.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-channelnamespace-handlerconfigs.html#cfn-appsync-channelnamespace-handlerconfigs-onpublish
            '''
            result = self._values.get("on_publish")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelNamespacePropsMixin.HandlerConfigProperty"]], result)

        @builtins.property
        def on_subscribe(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelNamespacePropsMixin.HandlerConfigProperty"]]:
            '''The configuration for the ``OnSubscribe`` handler.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-channelnamespace-handlerconfigs.html#cfn-appsync-channelnamespace-handlerconfigs-onsubscribe
            '''
            result = self._values.get("on_subscribe")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelNamespacePropsMixin.HandlerConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HandlerConfigsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnChannelNamespacePropsMixin.IntegrationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_source_name": "dataSourceName",
            "lambda_config": "lambdaConfig",
        },
    )
    class IntegrationProperty:
        def __init__(
            self,
            *,
            data_source_name: typing.Optional[builtins.str] = None,
            lambda_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnChannelNamespacePropsMixin.LambdaConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The ``Integration`` property type specifies the integration data source configuration for the handler.

            :param data_source_name: The unique name of the data source that has been configured on the API.
            :param lambda_config: The configuration for a Lambda data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-channelnamespace-integration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                integration_property = appsync_mixins.CfnChannelNamespacePropsMixin.IntegrationProperty(
                    data_source_name="dataSourceName",
                    lambda_config=appsync_mixins.CfnChannelNamespacePropsMixin.LambdaConfigProperty(
                        invoke_type="invokeType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1fef0f0c224c287dd8402f373f48a45d49e2c6ff662bba8c77b7b4d0ac2e05ce)
                check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
                check_type(argname="argument lambda_config", value=lambda_config, expected_type=type_hints["lambda_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_source_name is not None:
                self._values["data_source_name"] = data_source_name
            if lambda_config is not None:
                self._values["lambda_config"] = lambda_config

        @builtins.property
        def data_source_name(self) -> typing.Optional[builtins.str]:
            '''The unique name of the data source that has been configured on the API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-channelnamespace-integration.html#cfn-appsync-channelnamespace-integration-datasourcename
            '''
            result = self._values.get("data_source_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def lambda_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelNamespacePropsMixin.LambdaConfigProperty"]]:
            '''The configuration for a Lambda data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-channelnamespace-integration.html#cfn-appsync-channelnamespace-integration-lambdaconfig
            '''
            result = self._values.get("lambda_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelNamespacePropsMixin.LambdaConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntegrationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnChannelNamespacePropsMixin.LambdaConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"invoke_type": "invokeType"},
    )
    class LambdaConfigProperty:
        def __init__(
            self,
            *,
            invoke_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``LambdaConfig`` property type specifies the integration configuration for a Lambda data source.

            :param invoke_type: The invocation type for a Lambda data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-channelnamespace-lambdaconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                lambda_config_property = appsync_mixins.CfnChannelNamespacePropsMixin.LambdaConfigProperty(
                    invoke_type="invokeType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__67de4a54badc543038f1d26a05dc3c0fa5539eae081ffa1805c4d33a5d0ebe18)
                check_type(argname="argument invoke_type", value=invoke_type, expected_type=type_hints["invoke_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if invoke_type is not None:
                self._values["invoke_type"] = invoke_type

        @builtins.property
        def invoke_type(self) -> typing.Optional[builtins.str]:
            '''The invocation type for a Lambda data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-channelnamespace-lambdaconfig.html#cfn-appsync-channelnamespace-lambdaconfig-invoketype
            '''
            result = self._values.get("invoke_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnDataSourceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "description": "description",
        "dynamo_db_config": "dynamoDbConfig",
        "elasticsearch_config": "elasticsearchConfig",
        "event_bridge_config": "eventBridgeConfig",
        "http_config": "httpConfig",
        "lambda_config": "lambdaConfig",
        "metrics_config": "metricsConfig",
        "name": "name",
        "open_search_service_config": "openSearchServiceConfig",
        "relational_database_config": "relationalDatabaseConfig",
        "service_role_arn": "serviceRoleArn",
        "type": "type",
    },
)
class CfnDataSourceMixinProps:
    def __init__(
        self,
        *,
        api_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        dynamo_db_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DynamoDBConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        elasticsearch_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.ElasticsearchConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        event_bridge_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.EventBridgeConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        http_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.HttpConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        lambda_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.LambdaConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        metrics_config: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        open_search_service_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.OpenSearchServiceConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        relational_database_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.RelationalDatabaseConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        service_role_arn: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDataSourcePropsMixin.

        :param api_id: Unique AWS AppSync GraphQL API identifier where this data source will be created.
        :param description: The description of the data source.
        :param dynamo_db_config: AWS Region and TableName for an Amazon DynamoDB table in your account.
        :param elasticsearch_config: 
        :param event_bridge_config: An EventBridge configuration that contains a valid ARN of an event bus.
        :param http_config: Endpoints for an HTTP data source.
        :param lambda_config: An ARN of a Lambda function in valid ARN format. This can be the ARN of a Lambda function that exists in the current account or in another account.
        :param metrics_config: Enables or disables enhanced data source metrics for specified data sources. Note that ``MetricsConfig`` won't be used unless the ``dataSourceLevelMetricsBehavior`` value is set to ``PER_DATA_SOURCE_METRICS`` . If the ``dataSourceLevelMetricsBehavior`` is set to ``FULL_REQUEST_DATA_SOURCE_METRICS`` instead, ``MetricsConfig`` will be ignored. However, you can still set its value. ``MetricsConfig`` can be ``ENABLED`` or ``DISABLED`` .
        :param name: Friendly name for you to identify your AppSync data source after creation.
        :param open_search_service_config: AWS Region and Endpoints for an Amazon OpenSearch Service domain in your account.
        :param relational_database_config: Relational Database configuration of the relational database data source.
        :param service_role_arn: The AWS Identity and Access Management service role ARN for the data source. The system assumes this role when accessing the data source. Required if ``Type`` is specified as ``AWS_LAMBDA`` , ``AMAZON_DYNAMODB`` , ``AMAZON_ELASTICSEARCH`` , ``AMAZON_EVENTBRIDGE`` , ``AMAZON_OPENSEARCH_SERVICE`` , ``RELATIONAL_DATABASE`` , or ``AMAZON_BEDROCK_RUNTIME`` .
        :param type: The type of the data source. - *AWS_LAMBDA* : The data source is an AWS Lambda function. - *AMAZON_DYNAMODB* : The data source is an Amazon DynamoDB table. - *AMAZON_ELASTICSEARCH* : The data source is an Amazon OpenSearch Service domain. - *AMAZON_EVENTBRIDGE* : The data source is an Amazon EventBridge event bus. - *AMAZON_OPENSEARCH_SERVICE* : The data source is an Amazon OpenSearch Service domain. - *AMAZON_BEDROCK_RUNTIME* : The data source is the Amazon Bedrock runtime. - *NONE* : There is no data source. This type is used when you wish to invoke a GraphQL operation without connecting to a data source, such as performing data transformation with resolvers or triggering a subscription to be invoked from a mutation. - *HTTP* : The data source is an HTTP endpoint. - *RELATIONAL_DATABASE* : The data source is a relational database.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
            
            cfn_data_source_mixin_props = appsync_mixins.CfnDataSourceMixinProps(
                api_id="apiId",
                description="description",
                dynamo_db_config=appsync_mixins.CfnDataSourcePropsMixin.DynamoDBConfigProperty(
                    aws_region="awsRegion",
                    delta_sync_config=appsync_mixins.CfnDataSourcePropsMixin.DeltaSyncConfigProperty(
                        base_table_ttl="baseTableTtl",
                        delta_sync_table_name="deltaSyncTableName",
                        delta_sync_table_ttl="deltaSyncTableTtl"
                    ),
                    table_name="tableName",
                    use_caller_credentials=False,
                    versioned=False
                ),
                elasticsearch_config=appsync_mixins.CfnDataSourcePropsMixin.ElasticsearchConfigProperty(
                    aws_region="awsRegion",
                    endpoint="endpoint"
                ),
                event_bridge_config=appsync_mixins.CfnDataSourcePropsMixin.EventBridgeConfigProperty(
                    event_bus_arn="eventBusArn"
                ),
                http_config=appsync_mixins.CfnDataSourcePropsMixin.HttpConfigProperty(
                    authorization_config=appsync_mixins.CfnDataSourcePropsMixin.AuthorizationConfigProperty(
                        authorization_type="authorizationType",
                        aws_iam_config=appsync_mixins.CfnDataSourcePropsMixin.AwsIamConfigProperty(
                            signing_region="signingRegion",
                            signing_service_name="signingServiceName"
                        )
                    ),
                    endpoint="endpoint"
                ),
                lambda_config=appsync_mixins.CfnDataSourcePropsMixin.LambdaConfigProperty(
                    lambda_function_arn="lambdaFunctionArn"
                ),
                metrics_config="metricsConfig",
                name="name",
                open_search_service_config=appsync_mixins.CfnDataSourcePropsMixin.OpenSearchServiceConfigProperty(
                    aws_region="awsRegion",
                    endpoint="endpoint"
                ),
                relational_database_config=appsync_mixins.CfnDataSourcePropsMixin.RelationalDatabaseConfigProperty(
                    rds_http_endpoint_config=appsync_mixins.CfnDataSourcePropsMixin.RdsHttpEndpointConfigProperty(
                        aws_region="awsRegion",
                        aws_secret_store_arn="awsSecretStoreArn",
                        database_name="databaseName",
                        db_cluster_identifier="dbClusterIdentifier",
                        schema="schema"
                    ),
                    relational_database_source_type="relationalDatabaseSourceType"
                ),
                service_role_arn="serviceRoleArn",
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c948aa2178ac1d4bdafd667666eb0b78be94108229aefd20939e6350da4b522c)
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dynamo_db_config", value=dynamo_db_config, expected_type=type_hints["dynamo_db_config"])
            check_type(argname="argument elasticsearch_config", value=elasticsearch_config, expected_type=type_hints["elasticsearch_config"])
            check_type(argname="argument event_bridge_config", value=event_bridge_config, expected_type=type_hints["event_bridge_config"])
            check_type(argname="argument http_config", value=http_config, expected_type=type_hints["http_config"])
            check_type(argname="argument lambda_config", value=lambda_config, expected_type=type_hints["lambda_config"])
            check_type(argname="argument metrics_config", value=metrics_config, expected_type=type_hints["metrics_config"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument open_search_service_config", value=open_search_service_config, expected_type=type_hints["open_search_service_config"])
            check_type(argname="argument relational_database_config", value=relational_database_config, expected_type=type_hints["relational_database_config"])
            check_type(argname="argument service_role_arn", value=service_role_arn, expected_type=type_hints["service_role_arn"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_id is not None:
            self._values["api_id"] = api_id
        if description is not None:
            self._values["description"] = description
        if dynamo_db_config is not None:
            self._values["dynamo_db_config"] = dynamo_db_config
        if elasticsearch_config is not None:
            self._values["elasticsearch_config"] = elasticsearch_config
        if event_bridge_config is not None:
            self._values["event_bridge_config"] = event_bridge_config
        if http_config is not None:
            self._values["http_config"] = http_config
        if lambda_config is not None:
            self._values["lambda_config"] = lambda_config
        if metrics_config is not None:
            self._values["metrics_config"] = metrics_config
        if name is not None:
            self._values["name"] = name
        if open_search_service_config is not None:
            self._values["open_search_service_config"] = open_search_service_config
        if relational_database_config is not None:
            self._values["relational_database_config"] = relational_database_config
        if service_role_arn is not None:
            self._values["service_role_arn"] = service_role_arn
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def api_id(self) -> typing.Optional[builtins.str]:
        '''Unique AWS AppSync GraphQL API identifier where this data source will be created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-apiid
        '''
        result = self._values.get("api_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the data source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dynamo_db_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DynamoDBConfigProperty"]]:
        '''AWS Region and TableName for an Amazon DynamoDB table in your account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-dynamodbconfig
        '''
        result = self._values.get("dynamo_db_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DynamoDBConfigProperty"]], result)

    @builtins.property
    def elasticsearch_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ElasticsearchConfigProperty"]]:
        '''
        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-elasticsearchconfig
        :stability: deprecated
        '''
        result = self._values.get("elasticsearch_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ElasticsearchConfigProperty"]], result)

    @builtins.property
    def event_bridge_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.EventBridgeConfigProperty"]]:
        '''An EventBridge configuration that contains a valid ARN of an event bus.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-eventbridgeconfig
        '''
        result = self._values.get("event_bridge_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.EventBridgeConfigProperty"]], result)

    @builtins.property
    def http_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.HttpConfigProperty"]]:
        '''Endpoints for an HTTP data source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-httpconfig
        '''
        result = self._values.get("http_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.HttpConfigProperty"]], result)

    @builtins.property
    def lambda_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.LambdaConfigProperty"]]:
        '''An ARN of a Lambda function in valid ARN format.

        This can be the ARN of a Lambda function that exists in the current account or in another account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-lambdaconfig
        '''
        result = self._values.get("lambda_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.LambdaConfigProperty"]], result)

    @builtins.property
    def metrics_config(self) -> typing.Optional[builtins.str]:
        '''Enables or disables enhanced data source metrics for specified data sources.

        Note that ``MetricsConfig`` won't be used unless the ``dataSourceLevelMetricsBehavior`` value is set to ``PER_DATA_SOURCE_METRICS`` . If the ``dataSourceLevelMetricsBehavior`` is set to ``FULL_REQUEST_DATA_SOURCE_METRICS`` instead, ``MetricsConfig`` will be ignored. However, you can still set its value.

        ``MetricsConfig`` can be ``ENABLED`` or ``DISABLED`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-metricsconfig
        '''
        result = self._values.get("metrics_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Friendly name for you to identify your AppSync data source after creation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def open_search_service_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.OpenSearchServiceConfigProperty"]]:
        '''AWS Region and Endpoints for an Amazon OpenSearch Service domain in your account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-opensearchserviceconfig
        '''
        result = self._values.get("open_search_service_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.OpenSearchServiceConfigProperty"]], result)

    @builtins.property
    def relational_database_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.RelationalDatabaseConfigProperty"]]:
        '''Relational Database configuration of the relational database data source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-relationaldatabaseconfig
        '''
        result = self._values.get("relational_database_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.RelationalDatabaseConfigProperty"]], result)

    @builtins.property
    def service_role_arn(self) -> typing.Optional[builtins.str]:
        '''The AWS Identity and Access Management service role ARN for the data source.

        The system assumes this role when accessing the data source.

        Required if ``Type`` is specified as ``AWS_LAMBDA`` , ``AMAZON_DYNAMODB`` , ``AMAZON_ELASTICSEARCH`` , ``AMAZON_EVENTBRIDGE`` , ``AMAZON_OPENSEARCH_SERVICE`` , ``RELATIONAL_DATABASE`` , or ``AMAZON_BEDROCK_RUNTIME`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-servicerolearn
        '''
        result = self._values.get("service_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the data source.

        - *AWS_LAMBDA* : The data source is an AWS Lambda function.
        - *AMAZON_DYNAMODB* : The data source is an Amazon DynamoDB table.
        - *AMAZON_ELASTICSEARCH* : The data source is an Amazon OpenSearch Service domain.
        - *AMAZON_EVENTBRIDGE* : The data source is an Amazon EventBridge event bus.
        - *AMAZON_OPENSEARCH_SERVICE* : The data source is an Amazon OpenSearch Service domain.
        - *AMAZON_BEDROCK_RUNTIME* : The data source is the Amazon Bedrock runtime.
        - *NONE* : There is no data source. This type is used when you wish to invoke a GraphQL operation without connecting to a data source, such as performing data transformation with resolvers or triggering a subscription to be invoked from a mutation.
        - *HTTP* : The data source is an HTTP endpoint.
        - *RELATIONAL_DATABASE* : The data source is a relational database.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataSourceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDataSourcePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnDataSourcePropsMixin",
):
    '''The ``AWS::AppSync::DataSource`` resource creates data sources for resolvers in AWS AppSync to connect to, such as Amazon DynamoDB , AWS Lambda , and Amazon OpenSearch Service .

    Resolvers use these data sources to fetch data when clients make GraphQL calls.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html
    :cloudformationResource: AWS::AppSync::DataSource
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
        
        cfn_data_source_props_mixin = appsync_mixins.CfnDataSourcePropsMixin(appsync_mixins.CfnDataSourceMixinProps(
            api_id="apiId",
            description="description",
            dynamo_db_config=appsync_mixins.CfnDataSourcePropsMixin.DynamoDBConfigProperty(
                aws_region="awsRegion",
                delta_sync_config=appsync_mixins.CfnDataSourcePropsMixin.DeltaSyncConfigProperty(
                    base_table_ttl="baseTableTtl",
                    delta_sync_table_name="deltaSyncTableName",
                    delta_sync_table_ttl="deltaSyncTableTtl"
                ),
                table_name="tableName",
                use_caller_credentials=False,
                versioned=False
            ),
            elasticsearch_config=appsync_mixins.CfnDataSourcePropsMixin.ElasticsearchConfigProperty(
                aws_region="awsRegion",
                endpoint="endpoint"
            ),
            event_bridge_config=appsync_mixins.CfnDataSourcePropsMixin.EventBridgeConfigProperty(
                event_bus_arn="eventBusArn"
            ),
            http_config=appsync_mixins.CfnDataSourcePropsMixin.HttpConfigProperty(
                authorization_config=appsync_mixins.CfnDataSourcePropsMixin.AuthorizationConfigProperty(
                    authorization_type="authorizationType",
                    aws_iam_config=appsync_mixins.CfnDataSourcePropsMixin.AwsIamConfigProperty(
                        signing_region="signingRegion",
                        signing_service_name="signingServiceName"
                    )
                ),
                endpoint="endpoint"
            ),
            lambda_config=appsync_mixins.CfnDataSourcePropsMixin.LambdaConfigProperty(
                lambda_function_arn="lambdaFunctionArn"
            ),
            metrics_config="metricsConfig",
            name="name",
            open_search_service_config=appsync_mixins.CfnDataSourcePropsMixin.OpenSearchServiceConfigProperty(
                aws_region="awsRegion",
                endpoint="endpoint"
            ),
            relational_database_config=appsync_mixins.CfnDataSourcePropsMixin.RelationalDatabaseConfigProperty(
                rds_http_endpoint_config=appsync_mixins.CfnDataSourcePropsMixin.RdsHttpEndpointConfigProperty(
                    aws_region="awsRegion",
                    aws_secret_store_arn="awsSecretStoreArn",
                    database_name="databaseName",
                    db_cluster_identifier="dbClusterIdentifier",
                    schema="schema"
                ),
                relational_database_source_type="relationalDatabaseSourceType"
            ),
            service_role_arn="serviceRoleArn",
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDataSourceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppSync::DataSource``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0783acbcb03400459d9c51451d9479fac9894c60899d17fabef7d83a0b855b24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ebe22731bfa41d88112da20a71e01ae6ac53f54056b3a67324b0c6f459dd881)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a6113d7e2949ac56623f686c4c43693b6331f48dc49b2078d9d0d9d35bef6c5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDataSourceMixinProps:
        return typing.cast(CfnDataSourceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnDataSourcePropsMixin.AuthorizationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorization_type": "authorizationType",
            "aws_iam_config": "awsIamConfig",
        },
    )
    class AuthorizationConfigProperty:
        def __init__(
            self,
            *,
            authorization_type: typing.Optional[builtins.str] = None,
            aws_iam_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.AwsIamConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The ``AuthorizationConfig`` property type specifies the authorization type and configuration for an AWS AppSync http data source.

            ``AuthorizationConfig`` is a property of the `AWS AppSync DataSource HttpConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-httpconfig.html>`_ property type.

            :param authorization_type: The authorization type that the HTTP endpoint requires. - *AWS_IAM* : The authorization type is Signature Version 4 (SigV4).
            :param aws_iam_config: The AWS Identity and Access Management settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-authorizationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                authorization_config_property = appsync_mixins.CfnDataSourcePropsMixin.AuthorizationConfigProperty(
                    authorization_type="authorizationType",
                    aws_iam_config=appsync_mixins.CfnDataSourcePropsMixin.AwsIamConfigProperty(
                        signing_region="signingRegion",
                        signing_service_name="signingServiceName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b1bb349b6d7d58ec945cd94cade17eaf94319ed02ea273a1422199a9a25c6c97)
                check_type(argname="argument authorization_type", value=authorization_type, expected_type=type_hints["authorization_type"])
                check_type(argname="argument aws_iam_config", value=aws_iam_config, expected_type=type_hints["aws_iam_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authorization_type is not None:
                self._values["authorization_type"] = authorization_type
            if aws_iam_config is not None:
                self._values["aws_iam_config"] = aws_iam_config

        @builtins.property
        def authorization_type(self) -> typing.Optional[builtins.str]:
            '''The authorization type that the HTTP endpoint requires.

            - *AWS_IAM* : The authorization type is Signature Version 4 (SigV4).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-authorizationconfig.html#cfn-appsync-datasource-authorizationconfig-authorizationtype
            '''
            result = self._values.get("authorization_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def aws_iam_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.AwsIamConfigProperty"]]:
            '''The AWS Identity and Access Management settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-authorizationconfig.html#cfn-appsync-datasource-authorizationconfig-awsiamconfig
            '''
            result = self._values.get("aws_iam_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.AwsIamConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthorizationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnDataSourcePropsMixin.AwsIamConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "signing_region": "signingRegion",
            "signing_service_name": "signingServiceName",
        },
    )
    class AwsIamConfigProperty:
        def __init__(
            self,
            *,
            signing_region: typing.Optional[builtins.str] = None,
            signing_service_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use the ``AwsIamConfig`` property type to specify ``AwsIamConfig`` for a AWS AppSync authorizaton.

            ``AwsIamConfig`` is a property of the `AWS AppSync DataSource AuthorizationConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-httpconfig-authorizationconfig.html>`_ resource.

            :param signing_region: The signing Region for AWS Identity and Access Management authorization.
            :param signing_service_name: The signing service name for AWS Identity and Access Management authorization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-awsiamconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                aws_iam_config_property = appsync_mixins.CfnDataSourcePropsMixin.AwsIamConfigProperty(
                    signing_region="signingRegion",
                    signing_service_name="signingServiceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b02d5f7378e5839c11d435537451fa9085f869c796da32e220142656c7c26e9d)
                check_type(argname="argument signing_region", value=signing_region, expected_type=type_hints["signing_region"])
                check_type(argname="argument signing_service_name", value=signing_service_name, expected_type=type_hints["signing_service_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if signing_region is not None:
                self._values["signing_region"] = signing_region
            if signing_service_name is not None:
                self._values["signing_service_name"] = signing_service_name

        @builtins.property
        def signing_region(self) -> typing.Optional[builtins.str]:
            '''The signing Region for AWS Identity and Access Management authorization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-awsiamconfig.html#cfn-appsync-datasource-awsiamconfig-signingregion
            '''
            result = self._values.get("signing_region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def signing_service_name(self) -> typing.Optional[builtins.str]:
            '''The signing service name for AWS Identity and Access Management authorization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-awsiamconfig.html#cfn-appsync-datasource-awsiamconfig-signingservicename
            '''
            result = self._values.get("signing_service_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AwsIamConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnDataSourcePropsMixin.DeltaSyncConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "base_table_ttl": "baseTableTtl",
            "delta_sync_table_name": "deltaSyncTableName",
            "delta_sync_table_ttl": "deltaSyncTableTtl",
        },
    )
    class DeltaSyncConfigProperty:
        def __init__(
            self,
            *,
            base_table_ttl: typing.Optional[builtins.str] = None,
            delta_sync_table_name: typing.Optional[builtins.str] = None,
            delta_sync_table_ttl: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a Delta Sync configuration.

            :param base_table_ttl: The number of minutes that an Item is stored in the data source.
            :param delta_sync_table_name: The Delta Sync table name.
            :param delta_sync_table_ttl: The number of minutes that a Delta Sync log entry is stored in the Delta Sync table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-deltasyncconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                delta_sync_config_property = appsync_mixins.CfnDataSourcePropsMixin.DeltaSyncConfigProperty(
                    base_table_ttl="baseTableTtl",
                    delta_sync_table_name="deltaSyncTableName",
                    delta_sync_table_ttl="deltaSyncTableTtl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3ff1bb65d343903cc5698fe64df969c585834d254e625f028524032ae3a85d62)
                check_type(argname="argument base_table_ttl", value=base_table_ttl, expected_type=type_hints["base_table_ttl"])
                check_type(argname="argument delta_sync_table_name", value=delta_sync_table_name, expected_type=type_hints["delta_sync_table_name"])
                check_type(argname="argument delta_sync_table_ttl", value=delta_sync_table_ttl, expected_type=type_hints["delta_sync_table_ttl"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if base_table_ttl is not None:
                self._values["base_table_ttl"] = base_table_ttl
            if delta_sync_table_name is not None:
                self._values["delta_sync_table_name"] = delta_sync_table_name
            if delta_sync_table_ttl is not None:
                self._values["delta_sync_table_ttl"] = delta_sync_table_ttl

        @builtins.property
        def base_table_ttl(self) -> typing.Optional[builtins.str]:
            '''The number of minutes that an Item is stored in the data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-deltasyncconfig.html#cfn-appsync-datasource-deltasyncconfig-basetablettl
            '''
            result = self._values.get("base_table_ttl")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def delta_sync_table_name(self) -> typing.Optional[builtins.str]:
            '''The Delta Sync table name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-deltasyncconfig.html#cfn-appsync-datasource-deltasyncconfig-deltasynctablename
            '''
            result = self._values.get("delta_sync_table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def delta_sync_table_ttl(self) -> typing.Optional[builtins.str]:
            '''The number of minutes that a Delta Sync log entry is stored in the Delta Sync table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-deltasyncconfig.html#cfn-appsync-datasource-deltasyncconfig-deltasynctablettl
            '''
            result = self._values.get("delta_sync_table_ttl")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeltaSyncConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnDataSourcePropsMixin.DynamoDBConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aws_region": "awsRegion",
            "delta_sync_config": "deltaSyncConfig",
            "table_name": "tableName",
            "use_caller_credentials": "useCallerCredentials",
            "versioned": "versioned",
        },
    )
    class DynamoDBConfigProperty:
        def __init__(
            self,
            *,
            aws_region: typing.Optional[builtins.str] = None,
            delta_sync_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DeltaSyncConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            table_name: typing.Optional[builtins.str] = None,
            use_caller_credentials: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            versioned: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The ``DynamoDBConfig`` property type specifies the ``AwsRegion`` and ``TableName`` for an Amazon DynamoDB table in your account for an AWS AppSync data source.

            ``DynamoDBConfig`` is a property of the `AWS::AppSync::DataSource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html>`_ property type.

            :param aws_region: The AWS Region.
            :param delta_sync_config: The ``DeltaSyncConfig`` for a versioned datasource.
            :param table_name: The table name.
            :param use_caller_credentials: Set to ``TRUE`` to use AWS Identity and Access Management with this data source.
            :param versioned: Set to TRUE to use Conflict Detection and Resolution with this data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-dynamodbconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                dynamo_dBConfig_property = appsync_mixins.CfnDataSourcePropsMixin.DynamoDBConfigProperty(
                    aws_region="awsRegion",
                    delta_sync_config=appsync_mixins.CfnDataSourcePropsMixin.DeltaSyncConfigProperty(
                        base_table_ttl="baseTableTtl",
                        delta_sync_table_name="deltaSyncTableName",
                        delta_sync_table_ttl="deltaSyncTableTtl"
                    ),
                    table_name="tableName",
                    use_caller_credentials=False,
                    versioned=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e4c543f2b30ad4cd76c1f2bec7b8962b1d36584604c8743f07a84da120f21195)
                check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                check_type(argname="argument delta_sync_config", value=delta_sync_config, expected_type=type_hints["delta_sync_config"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
                check_type(argname="argument use_caller_credentials", value=use_caller_credentials, expected_type=type_hints["use_caller_credentials"])
                check_type(argname="argument versioned", value=versioned, expected_type=type_hints["versioned"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_region is not None:
                self._values["aws_region"] = aws_region
            if delta_sync_config is not None:
                self._values["delta_sync_config"] = delta_sync_config
            if table_name is not None:
                self._values["table_name"] = table_name
            if use_caller_credentials is not None:
                self._values["use_caller_credentials"] = use_caller_credentials
            if versioned is not None:
                self._values["versioned"] = versioned

        @builtins.property
        def aws_region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-dynamodbconfig.html#cfn-appsync-datasource-dynamodbconfig-awsregion
            '''
            result = self._values.get("aws_region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def delta_sync_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DeltaSyncConfigProperty"]]:
            '''The ``DeltaSyncConfig`` for a versioned datasource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-dynamodbconfig.html#cfn-appsync-datasource-dynamodbconfig-deltasyncconfig
            '''
            result = self._values.get("delta_sync_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DeltaSyncConfigProperty"]], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''The table name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-dynamodbconfig.html#cfn-appsync-datasource-dynamodbconfig-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def use_caller_credentials(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set to ``TRUE`` to use AWS Identity and Access Management with this data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-dynamodbconfig.html#cfn-appsync-datasource-dynamodbconfig-usecallercredentials
            '''
            result = self._values.get("use_caller_credentials")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def versioned(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set to TRUE to use Conflict Detection and Resolution with this data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-dynamodbconfig.html#cfn-appsync-datasource-dynamodbconfig-versioned
            '''
            result = self._values.get("versioned")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynamoDBConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnDataSourcePropsMixin.ElasticsearchConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"aws_region": "awsRegion", "endpoint": "endpoint"},
    )
    class ElasticsearchConfigProperty:
        def __init__(
            self,
            *,
            aws_region: typing.Optional[builtins.str] = None,
            endpoint: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param aws_region: The AWS Region.
            :param endpoint: The endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-elasticsearchconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                elasticsearch_config_property = appsync_mixins.CfnDataSourcePropsMixin.ElasticsearchConfigProperty(
                    aws_region="awsRegion",
                    endpoint="endpoint"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c64a149e69e18501a5711766b92d667ad7e38015ca5f9d365d35aed9729e75e2)
                check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_region is not None:
                self._values["aws_region"] = aws_region
            if endpoint is not None:
                self._values["endpoint"] = endpoint

        @builtins.property
        def aws_region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-elasticsearchconfig.html#cfn-appsync-datasource-elasticsearchconfig-awsregion
            '''
            result = self._values.get("aws_region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def endpoint(self) -> typing.Optional[builtins.str]:
            '''The endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-elasticsearchconfig.html#cfn-appsync-datasource-elasticsearchconfig-endpoint
            '''
            result = self._values.get("endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ElasticsearchConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnDataSourcePropsMixin.EventBridgeConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"event_bus_arn": "eventBusArn"},
    )
    class EventBridgeConfigProperty:
        def __init__(
            self,
            *,
            event_bus_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The data source.

            This can be an API destination, resource, or AWS service.

            :param event_bus_arn: The event bus pipeline's ARN. For more information about event buses, see `EventBridge event buses <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-bus.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-eventbridgeconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                event_bridge_config_property = appsync_mixins.CfnDataSourcePropsMixin.EventBridgeConfigProperty(
                    event_bus_arn="eventBusArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ebe4fa646e1ae1036168c8904e4fd83f3050876036d67f0045e8be09f07ed0b9)
                check_type(argname="argument event_bus_arn", value=event_bus_arn, expected_type=type_hints["event_bus_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if event_bus_arn is not None:
                self._values["event_bus_arn"] = event_bus_arn

        @builtins.property
        def event_bus_arn(self) -> typing.Optional[builtins.str]:
            '''The event bus pipeline's ARN.

            For more information about event buses, see `EventBridge event buses <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-bus.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-eventbridgeconfig.html#cfn-appsync-datasource-eventbridgeconfig-eventbusarn
            '''
            result = self._values.get("event_bus_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventBridgeConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnDataSourcePropsMixin.HttpConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorization_config": "authorizationConfig",
            "endpoint": "endpoint",
        },
    )
    class HttpConfigProperty:
        def __init__(
            self,
            *,
            authorization_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.AuthorizationConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            endpoint: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use the ``HttpConfig`` property type to specify ``HttpConfig`` for an AWS AppSync data source.

            ``HttpConfig`` is a property of the `AWS::AppSync::DataSource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html>`_ resource.

            :param authorization_config: The authorization configuration.
            :param endpoint: The endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-httpconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                http_config_property = appsync_mixins.CfnDataSourcePropsMixin.HttpConfigProperty(
                    authorization_config=appsync_mixins.CfnDataSourcePropsMixin.AuthorizationConfigProperty(
                        authorization_type="authorizationType",
                        aws_iam_config=appsync_mixins.CfnDataSourcePropsMixin.AwsIamConfigProperty(
                            signing_region="signingRegion",
                            signing_service_name="signingServiceName"
                        )
                    ),
                    endpoint="endpoint"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9bd88226a6af3b494e0af610fe7e310159fd78fb74a6c0b2e075b110c2eae2e1)
                check_type(argname="argument authorization_config", value=authorization_config, expected_type=type_hints["authorization_config"])
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authorization_config is not None:
                self._values["authorization_config"] = authorization_config
            if endpoint is not None:
                self._values["endpoint"] = endpoint

        @builtins.property
        def authorization_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.AuthorizationConfigProperty"]]:
            '''The authorization configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-httpconfig.html#cfn-appsync-datasource-httpconfig-authorizationconfig
            '''
            result = self._values.get("authorization_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.AuthorizationConfigProperty"]], result)

        @builtins.property
        def endpoint(self) -> typing.Optional[builtins.str]:
            '''The endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-httpconfig.html#cfn-appsync-datasource-httpconfig-endpoint
            '''
            result = self._values.get("endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnDataSourcePropsMixin.LambdaConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"lambda_function_arn": "lambdaFunctionArn"},
    )
    class LambdaConfigProperty:
        def __init__(
            self,
            *,
            lambda_function_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``LambdaConfig`` property type specifies the Lambda function ARN for an AWS AppSync data source.

            ``LambdaConfig`` is a property of the `AWS::AppSync::DataSource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html>`_ property type.

            :param lambda_function_arn: The ARN for the Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-lambdaconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                lambda_config_property = appsync_mixins.CfnDataSourcePropsMixin.LambdaConfigProperty(
                    lambda_function_arn="lambdaFunctionArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3859073b4ec4f2d737991d4863b79356c0b415bc8e723f364ad28df73c5b6e74)
                check_type(argname="argument lambda_function_arn", value=lambda_function_arn, expected_type=type_hints["lambda_function_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_function_arn is not None:
                self._values["lambda_function_arn"] = lambda_function_arn

        @builtins.property
        def lambda_function_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN for the Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-lambdaconfig.html#cfn-appsync-datasource-lambdaconfig-lambdafunctionarn
            '''
            result = self._values.get("lambda_function_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnDataSourcePropsMixin.OpenSearchServiceConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"aws_region": "awsRegion", "endpoint": "endpoint"},
    )
    class OpenSearchServiceConfigProperty:
        def __init__(
            self,
            *,
            aws_region: typing.Optional[builtins.str] = None,
            endpoint: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``OpenSearchServiceConfig`` property type specifies the ``AwsRegion`` and ``Endpoints`` for an Amazon OpenSearch Service domain in your account for an AWS AppSync data source.

            ``OpenSearchServiceConfig`` is a property of the `AWS::AppSync::DataSource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html>`_ property type.

            :param aws_region: The AWS Region.
            :param endpoint: The endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-opensearchserviceconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                open_search_service_config_property = appsync_mixins.CfnDataSourcePropsMixin.OpenSearchServiceConfigProperty(
                    aws_region="awsRegion",
                    endpoint="endpoint"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__df349efa2e246cdc050124451ec187df16392f4a687330decf4acb861a874648)
                check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_region is not None:
                self._values["aws_region"] = aws_region
            if endpoint is not None:
                self._values["endpoint"] = endpoint

        @builtins.property
        def aws_region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-opensearchserviceconfig.html#cfn-appsync-datasource-opensearchserviceconfig-awsregion
            '''
            result = self._values.get("aws_region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def endpoint(self) -> typing.Optional[builtins.str]:
            '''The endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-opensearchserviceconfig.html#cfn-appsync-datasource-opensearchserviceconfig-endpoint
            '''
            result = self._values.get("endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OpenSearchServiceConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnDataSourcePropsMixin.RdsHttpEndpointConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aws_region": "awsRegion",
            "aws_secret_store_arn": "awsSecretStoreArn",
            "database_name": "databaseName",
            "db_cluster_identifier": "dbClusterIdentifier",
            "schema": "schema",
        },
    )
    class RdsHttpEndpointConfigProperty:
        def __init__(
            self,
            *,
            aws_region: typing.Optional[builtins.str] = None,
            aws_secret_store_arn: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            db_cluster_identifier: typing.Optional[builtins.str] = None,
            schema: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use the ``RdsHttpEndpointConfig`` property type to specify the ``RdsHttpEndpoint`` for an AWS AppSync relational database.

            ``RdsHttpEndpointConfig`` is a property of the `AWS AppSync DataSource RelationalDatabaseConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-relationaldatabaseconfig.html>`_ resource.

            :param aws_region: AWS Region for RDS HTTP endpoint.
            :param aws_secret_store_arn: The ARN for database credentials stored in AWS Secrets Manager .
            :param database_name: Logical database name.
            :param db_cluster_identifier: Amazon RDS cluster Amazon Resource Name (ARN).
            :param schema: Logical schema name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-rdshttpendpointconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                rds_http_endpoint_config_property = appsync_mixins.CfnDataSourcePropsMixin.RdsHttpEndpointConfigProperty(
                    aws_region="awsRegion",
                    aws_secret_store_arn="awsSecretStoreArn",
                    database_name="databaseName",
                    db_cluster_identifier="dbClusterIdentifier",
                    schema="schema"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__37349d29bf4d91d7812152e79b6520db3bd5b7ffd81024a37347b00002ea20da)
                check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                check_type(argname="argument aws_secret_store_arn", value=aws_secret_store_arn, expected_type=type_hints["aws_secret_store_arn"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument db_cluster_identifier", value=db_cluster_identifier, expected_type=type_hints["db_cluster_identifier"])
                check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_region is not None:
                self._values["aws_region"] = aws_region
            if aws_secret_store_arn is not None:
                self._values["aws_secret_store_arn"] = aws_secret_store_arn
            if database_name is not None:
                self._values["database_name"] = database_name
            if db_cluster_identifier is not None:
                self._values["db_cluster_identifier"] = db_cluster_identifier
            if schema is not None:
                self._values["schema"] = schema

        @builtins.property
        def aws_region(self) -> typing.Optional[builtins.str]:
            '''AWS Region for RDS HTTP endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-rdshttpendpointconfig.html#cfn-appsync-datasource-rdshttpendpointconfig-awsregion
            '''
            result = self._values.get("aws_region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def aws_secret_store_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN for database credentials stored in AWS Secrets Manager .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-rdshttpendpointconfig.html#cfn-appsync-datasource-rdshttpendpointconfig-awssecretstorearn
            '''
            result = self._values.get("aws_secret_store_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''Logical database name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-rdshttpendpointconfig.html#cfn-appsync-datasource-rdshttpendpointconfig-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def db_cluster_identifier(self) -> typing.Optional[builtins.str]:
            '''Amazon RDS cluster Amazon Resource Name (ARN).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-rdshttpendpointconfig.html#cfn-appsync-datasource-rdshttpendpointconfig-dbclusteridentifier
            '''
            result = self._values.get("db_cluster_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schema(self) -> typing.Optional[builtins.str]:
            '''Logical schema name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-rdshttpendpointconfig.html#cfn-appsync-datasource-rdshttpendpointconfig-schema
            '''
            result = self._values.get("schema")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RdsHttpEndpointConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnDataSourcePropsMixin.RelationalDatabaseConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "rds_http_endpoint_config": "rdsHttpEndpointConfig",
            "relational_database_source_type": "relationalDatabaseSourceType",
        },
    )
    class RelationalDatabaseConfigProperty:
        def __init__(
            self,
            *,
            rds_http_endpoint_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.RdsHttpEndpointConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            relational_database_source_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use the ``RelationalDatabaseConfig`` property type to specify ``RelationalDatabaseConfig`` for an AWS AppSync data source.

            ``RelationalDatabaseConfig`` is a property of the `AWS::AppSync::DataSource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html>`_ property type.

            :param rds_http_endpoint_config: Information about the Amazon RDS resource.
            :param relational_database_source_type: The type of relational data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-relationaldatabaseconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                relational_database_config_property = appsync_mixins.CfnDataSourcePropsMixin.RelationalDatabaseConfigProperty(
                    rds_http_endpoint_config=appsync_mixins.CfnDataSourcePropsMixin.RdsHttpEndpointConfigProperty(
                        aws_region="awsRegion",
                        aws_secret_store_arn="awsSecretStoreArn",
                        database_name="databaseName",
                        db_cluster_identifier="dbClusterIdentifier",
                        schema="schema"
                    ),
                    relational_database_source_type="relationalDatabaseSourceType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__45ae2ec63faef5d15bcedb19e9a3efafaea773970328ee16eed37ddd1ed79ed4)
                check_type(argname="argument rds_http_endpoint_config", value=rds_http_endpoint_config, expected_type=type_hints["rds_http_endpoint_config"])
                check_type(argname="argument relational_database_source_type", value=relational_database_source_type, expected_type=type_hints["relational_database_source_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rds_http_endpoint_config is not None:
                self._values["rds_http_endpoint_config"] = rds_http_endpoint_config
            if relational_database_source_type is not None:
                self._values["relational_database_source_type"] = relational_database_source_type

        @builtins.property
        def rds_http_endpoint_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.RdsHttpEndpointConfigProperty"]]:
            '''Information about the Amazon RDS resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-relationaldatabaseconfig.html#cfn-appsync-datasource-relationaldatabaseconfig-rdshttpendpointconfig
            '''
            result = self._values.get("rds_http_endpoint_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.RdsHttpEndpointConfigProperty"]], result)

        @builtins.property
        def relational_database_source_type(self) -> typing.Optional[builtins.str]:
            '''The type of relational data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-relationaldatabaseconfig.html#cfn-appsync-datasource-relationaldatabaseconfig-relationaldatabasesourcetype
            '''
            result = self._values.get("relational_database_source_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RelationalDatabaseConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnDomainNameApiAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={"api_id": "apiId", "domain_name": "domainName"},
)
class CfnDomainNameApiAssociationMixinProps:
    def __init__(
        self,
        *,
        api_id: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDomainNameApiAssociationPropsMixin.

        :param api_id: The API ID.
        :param domain_name: The domain name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-domainnameapiassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
            
            cfn_domain_name_api_association_mixin_props = appsync_mixins.CfnDomainNameApiAssociationMixinProps(
                api_id="apiId",
                domain_name="domainName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__762b16e5f8cd459d1654832994e398056186a1173cd181c89d0f05decbf2dc17)
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_id is not None:
            self._values["api_id"] = api_id
        if domain_name is not None:
            self._values["domain_name"] = domain_name

    @builtins.property
    def api_id(self) -> typing.Optional[builtins.str]:
        '''The API ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-domainnameapiassociation.html#cfn-appsync-domainnameapiassociation-apiid
        '''
        result = self._values.get("api_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The domain name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-domainnameapiassociation.html#cfn-appsync-domainnameapiassociation-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainNameApiAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDomainNameApiAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnDomainNameApiAssociationPropsMixin",
):
    '''The ``AWS::AppSync::DomainNameApiAssociation`` resource represents the mapping of your custom domain name to the assigned API URL.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-domainnameapiassociation.html
    :cloudformationResource: AWS::AppSync::DomainNameApiAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
        
        cfn_domain_name_api_association_props_mixin = appsync_mixins.CfnDomainNameApiAssociationPropsMixin(appsync_mixins.CfnDomainNameApiAssociationMixinProps(
            api_id="apiId",
            domain_name="domainName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDomainNameApiAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppSync::DomainNameApiAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af18555a02e56bcd6d8b00314f61e3b07843beb4cc058cda5b0358ad03044a3d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__859151fcbb870bf8602f2384bb697d16a1f3170c7f519cc5c05c29cfc16b02b2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__241d9fdfc222b0d749431ea86e3ff181a3c8f7790aff9c348f6822a6a5082a01)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDomainNameApiAssociationMixinProps:
        return typing.cast(CfnDomainNameApiAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnDomainNameMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_arn": "certificateArn",
        "description": "description",
        "domain_name": "domainName",
        "tags": "tags",
    },
)
class CfnDomainNameMixinProps:
    def __init__(
        self,
        *,
        certificate_arn: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDomainNamePropsMixin.

        :param certificate_arn: The Amazon Resource Name (ARN) of the certificate. This will be an Certificate Manager certificate.
        :param description: The decription for your domain name.
        :param domain_name: The domain name.
        :param tags: A set of tags (key-value pairs) for this domain name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-domainname.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
            
            cfn_domain_name_mixin_props = appsync_mixins.CfnDomainNameMixinProps(
                certificate_arn="certificateArn",
                description="description",
                domain_name="domainName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f81d3df5c55f9ab9dacdb80f14ac1827a3034b3b2183d9698419eb6485defb6f)
            check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_arn is not None:
            self._values["certificate_arn"] = certificate_arn
        if description is not None:
            self._values["description"] = description
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def certificate_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the certificate.

        This will be an Certificate Manager certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-domainname.html#cfn-appsync-domainname-certificatearn
        '''
        result = self._values.get("certificate_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The decription for your domain name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-domainname.html#cfn-appsync-domainname-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The domain name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-domainname.html#cfn-appsync-domainname-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A set of tags (key-value pairs) for this domain name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-domainname.html#cfn-appsync-domainname-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainNameMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDomainNamePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnDomainNamePropsMixin",
):
    '''The ``AWS::AppSync::DomainName`` resource creates a ``DomainNameConfig`` object to configure a custom domain.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-domainname.html
    :cloudformationResource: AWS::AppSync::DomainName
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
        
        cfn_domain_name_props_mixin = appsync_mixins.CfnDomainNamePropsMixin(appsync_mixins.CfnDomainNameMixinProps(
            certificate_arn="certificateArn",
            description="description",
            domain_name="domainName",
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
        props: typing.Union[CfnDomainNameMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppSync::DomainName``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e6cd89afad7e3cd9e0294ce8f91e410f5bd47fd7dc327af2fcbccadf9960943)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4559cbed19a5a61c205eeec7baf37fd448000dded937f608829cc72b910b89a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f5893512e1082e24149814b02c2e776f48b15001b5eab1087c2466357157dbf)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDomainNameMixinProps:
        return typing.cast(CfnDomainNameMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnFunctionConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "code": "code",
        "code_s3_location": "codeS3Location",
        "data_source_name": "dataSourceName",
        "description": "description",
        "function_version": "functionVersion",
        "max_batch_size": "maxBatchSize",
        "name": "name",
        "request_mapping_template": "requestMappingTemplate",
        "request_mapping_template_s3_location": "requestMappingTemplateS3Location",
        "response_mapping_template": "responseMappingTemplate",
        "response_mapping_template_s3_location": "responseMappingTemplateS3Location",
        "runtime": "runtime",
        "sync_config": "syncConfig",
    },
)
class CfnFunctionConfigurationMixinProps:
    def __init__(
        self,
        *,
        api_id: typing.Optional[builtins.str] = None,
        code: typing.Optional[builtins.str] = None,
        code_s3_location: typing.Optional[builtins.str] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        function_version: typing.Optional[builtins.str] = None,
        max_batch_size: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        request_mapping_template: typing.Optional[builtins.str] = None,
        request_mapping_template_s3_location: typing.Optional[builtins.str] = None,
        response_mapping_template: typing.Optional[builtins.str] = None,
        response_mapping_template_s3_location: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionConfigurationPropsMixin.AppSyncRuntimeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sync_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionConfigurationPropsMixin.SyncConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnFunctionConfigurationPropsMixin.

        :param api_id: The AWS AppSync GraphQL API that you want to attach using this function.
        :param code: The ``resolver`` code that contains the request and response functions. When code is used, the ``runtime`` is required. The runtime value must be ``APPSYNC_JS`` .
        :param code_s3_location: The Amazon S3 endpoint.
        :param data_source_name: The name of data source this function will attach.
        :param description: The ``Function`` description.
        :param function_version: The version of the request mapping template. Currently, only the 2018-05-29 version of the template is supported.
        :param max_batch_size: The maximum number of resolver request inputs that will be sent to a single AWS Lambda function in a ``BatchInvoke`` operation.
        :param name: The name of the function.
        :param request_mapping_template: The ``Function`` request mapping template. Functions support only the 2018-05-29 version of the request mapping template.
        :param request_mapping_template_s3_location: Describes a Sync configuration for a resolver. Contains information on which Conflict Detection, as well as Resolution strategy, should be performed when the resolver is invoked.
        :param response_mapping_template: The ``Function`` response mapping template.
        :param response_mapping_template_s3_location: The location of a response mapping template in an Amazon S3 bucket. Use this if you want to provision with a template file in Amazon S3 rather than embedding it in your CloudFormation template.
        :param runtime: Describes a runtime used by an AWS AppSync resolver or AWS AppSync function. Specifies the name and version of the runtime to use. Note that if a runtime is specified, code must also be specified.
        :param sync_config: Describes a Sync configuration for a resolver. Specifies which Conflict Detection strategy and Resolution strategy to use when the resolver is invoked.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
            
            cfn_function_configuration_mixin_props = appsync_mixins.CfnFunctionConfigurationMixinProps(
                api_id="apiId",
                code="code",
                code_s3_location="codeS3Location",
                data_source_name="dataSourceName",
                description="description",
                function_version="functionVersion",
                max_batch_size=123,
                name="name",
                request_mapping_template="requestMappingTemplate",
                request_mapping_template_s3_location="requestMappingTemplateS3Location",
                response_mapping_template="responseMappingTemplate",
                response_mapping_template_s3_location="responseMappingTemplateS3Location",
                runtime=appsync_mixins.CfnFunctionConfigurationPropsMixin.AppSyncRuntimeProperty(
                    name="name",
                    runtime_version="runtimeVersion"
                ),
                sync_config=appsync_mixins.CfnFunctionConfigurationPropsMixin.SyncConfigProperty(
                    conflict_detection="conflictDetection",
                    conflict_handler="conflictHandler",
                    lambda_conflict_handler_config=appsync_mixins.CfnFunctionConfigurationPropsMixin.LambdaConflictHandlerConfigProperty(
                        lambda_conflict_handler_arn="lambdaConflictHandlerArn"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7f8679cd8c6a1a9752afe43a5803cce15c38803c22e140b13c75607f9113fce)
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument code_s3_location", value=code_s3_location, expected_type=type_hints["code_s3_location"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument function_version", value=function_version, expected_type=type_hints["function_version"])
            check_type(argname="argument max_batch_size", value=max_batch_size, expected_type=type_hints["max_batch_size"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument request_mapping_template", value=request_mapping_template, expected_type=type_hints["request_mapping_template"])
            check_type(argname="argument request_mapping_template_s3_location", value=request_mapping_template_s3_location, expected_type=type_hints["request_mapping_template_s3_location"])
            check_type(argname="argument response_mapping_template", value=response_mapping_template, expected_type=type_hints["response_mapping_template"])
            check_type(argname="argument response_mapping_template_s3_location", value=response_mapping_template_s3_location, expected_type=type_hints["response_mapping_template_s3_location"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument sync_config", value=sync_config, expected_type=type_hints["sync_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_id is not None:
            self._values["api_id"] = api_id
        if code is not None:
            self._values["code"] = code
        if code_s3_location is not None:
            self._values["code_s3_location"] = code_s3_location
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if description is not None:
            self._values["description"] = description
        if function_version is not None:
            self._values["function_version"] = function_version
        if max_batch_size is not None:
            self._values["max_batch_size"] = max_batch_size
        if name is not None:
            self._values["name"] = name
        if request_mapping_template is not None:
            self._values["request_mapping_template"] = request_mapping_template
        if request_mapping_template_s3_location is not None:
            self._values["request_mapping_template_s3_location"] = request_mapping_template_s3_location
        if response_mapping_template is not None:
            self._values["response_mapping_template"] = response_mapping_template
        if response_mapping_template_s3_location is not None:
            self._values["response_mapping_template_s3_location"] = response_mapping_template_s3_location
        if runtime is not None:
            self._values["runtime"] = runtime
        if sync_config is not None:
            self._values["sync_config"] = sync_config

    @builtins.property
    def api_id(self) -> typing.Optional[builtins.str]:
        '''The AWS AppSync GraphQL API that you want to attach using this function.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-apiid
        '''
        result = self._values.get("api_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code(self) -> typing.Optional[builtins.str]:
        '''The ``resolver`` code that contains the request and response functions.

        When code is used, the ``runtime`` is required. The runtime value must be ``APPSYNC_JS`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-code
        '''
        result = self._values.get("code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_s3_location(self) -> typing.Optional[builtins.str]:
        '''The Amazon S3 endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-codes3location
        '''
        result = self._values.get("code_s3_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''The name of data source this function will attach.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-datasourcename
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The ``Function`` description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def function_version(self) -> typing.Optional[builtins.str]:
        '''The version of the request mapping template.

        Currently, only the 2018-05-29 version of the template is supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-functionversion
        '''
        result = self._values.get("function_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_batch_size(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of resolver request inputs that will be sent to a single AWS Lambda function in a ``BatchInvoke`` operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-maxbatchsize
        '''
        result = self._values.get("max_batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the function.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_mapping_template(self) -> typing.Optional[builtins.str]:
        '''The ``Function`` request mapping template.

        Functions support only the 2018-05-29 version of the request mapping template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-requestmappingtemplate
        '''
        result = self._values.get("request_mapping_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_mapping_template_s3_location(self) -> typing.Optional[builtins.str]:
        '''Describes a Sync configuration for a resolver.

        Contains information on which Conflict Detection, as well as Resolution strategy, should be performed when the resolver is invoked.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-requestmappingtemplates3location
        '''
        result = self._values.get("request_mapping_template_s3_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_mapping_template(self) -> typing.Optional[builtins.str]:
        '''The ``Function`` response mapping template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-responsemappingtemplate
        '''
        result = self._values.get("response_mapping_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_mapping_template_s3_location(self) -> typing.Optional[builtins.str]:
        '''The location of a response mapping template in an Amazon S3 bucket.

        Use this if you want to provision with a template file in Amazon S3 rather than embedding it in your CloudFormation template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-responsemappingtemplates3location
        '''
        result = self._values.get("response_mapping_template_s3_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionConfigurationPropsMixin.AppSyncRuntimeProperty"]]:
        '''Describes a runtime used by an AWS AppSync resolver or AWS AppSync function.

        Specifies the name and version of the runtime to use. Note that if a runtime is specified, code must also be specified.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-runtime
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionConfigurationPropsMixin.AppSyncRuntimeProperty"]], result)

    @builtins.property
    def sync_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionConfigurationPropsMixin.SyncConfigProperty"]]:
        '''Describes a Sync configuration for a resolver.

        Specifies which Conflict Detection strategy and Resolution strategy to use when the resolver is invoked.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-syncconfig
        '''
        result = self._values.get("sync_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionConfigurationPropsMixin.SyncConfigProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFunctionConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFunctionConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnFunctionConfigurationPropsMixin",
):
    '''The ``AWS::AppSync::FunctionConfiguration`` resource defines the functions in GraphQL APIs to perform certain operations.

    You can use pipeline resolvers to attach functions. For more information, see `Pipeline Resolvers <https://docs.aws.amazon.com/appsync/latest/devguide/pipeline-resolvers.html>`_ in the *AWS AppSync Developer Guide* .
    .. epigraph::

       When you submit an update, AWS CloudFormation updates resources based on differences between what you submit and the stack's current template. To cause this resource to be updated you must change a property value for this resource in the CloudFormation template. Changing the Amazon S3 file content without changing a property value will not result in an update operation.

       See `Update Behaviors of Stack Resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html>`_ in the *AWS CloudFormation User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html
    :cloudformationResource: AWS::AppSync::FunctionConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
        
        cfn_function_configuration_props_mixin = appsync_mixins.CfnFunctionConfigurationPropsMixin(appsync_mixins.CfnFunctionConfigurationMixinProps(
            api_id="apiId",
            code="code",
            code_s3_location="codeS3Location",
            data_source_name="dataSourceName",
            description="description",
            function_version="functionVersion",
            max_batch_size=123,
            name="name",
            request_mapping_template="requestMappingTemplate",
            request_mapping_template_s3_location="requestMappingTemplateS3Location",
            response_mapping_template="responseMappingTemplate",
            response_mapping_template_s3_location="responseMappingTemplateS3Location",
            runtime=appsync_mixins.CfnFunctionConfigurationPropsMixin.AppSyncRuntimeProperty(
                name="name",
                runtime_version="runtimeVersion"
            ),
            sync_config=appsync_mixins.CfnFunctionConfigurationPropsMixin.SyncConfigProperty(
                conflict_detection="conflictDetection",
                conflict_handler="conflictHandler",
                lambda_conflict_handler_config=appsync_mixins.CfnFunctionConfigurationPropsMixin.LambdaConflictHandlerConfigProperty(
                    lambda_conflict_handler_arn="lambdaConflictHandlerArn"
                )
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnFunctionConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppSync::FunctionConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64984246fa8df864f7d2ddafc1b80f004c797379d0f603bf0031196827b5efea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91abbfcda09a4ce52677df167fb31b0217d45504a475bf50081ea19a5cb3b82c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb6c5a6de3b5f66ac1d2802034f5077c505945ad97139be6ede240ddc861f427)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFunctionConfigurationMixinProps:
        return typing.cast(CfnFunctionConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnFunctionConfigurationPropsMixin.AppSyncRuntimeProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "runtime_version": "runtimeVersion"},
    )
    class AppSyncRuntimeProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            runtime_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a runtime used by an AWS AppSync resolver or AWS AppSync function.

            Specifies the name and version of the runtime to use. Note that if a runtime is specified, code must also be specified.

            :param name: The ``name`` of the runtime to use. Currently, the only allowed value is ``APPSYNC_JS`` .
            :param runtime_version: The ``version`` of the runtime to use. Currently, the only allowed version is ``1.0.0`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-functionconfiguration-appsyncruntime.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                app_sync_runtime_property = appsync_mixins.CfnFunctionConfigurationPropsMixin.AppSyncRuntimeProperty(
                    name="name",
                    runtime_version="runtimeVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1b314fae8e3a29d1255eb0120dcba3bb7516ef7638938b8ced1423f00eb23397)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument runtime_version", value=runtime_version, expected_type=type_hints["runtime_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if runtime_version is not None:
                self._values["runtime_version"] = runtime_version

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The ``name`` of the runtime to use.

            Currently, the only allowed value is ``APPSYNC_JS`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-functionconfiguration-appsyncruntime.html#cfn-appsync-functionconfiguration-appsyncruntime-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def runtime_version(self) -> typing.Optional[builtins.str]:
            '''The ``version`` of the runtime to use.

            Currently, the only allowed version is ``1.0.0`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-functionconfiguration-appsyncruntime.html#cfn-appsync-functionconfiguration-appsyncruntime-runtimeversion
            '''
            result = self._values.get("runtime_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AppSyncRuntimeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnFunctionConfigurationPropsMixin.LambdaConflictHandlerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"lambda_conflict_handler_arn": "lambdaConflictHandlerArn"},
    )
    class LambdaConflictHandlerConfigProperty:
        def __init__(
            self,
            *,
            lambda_conflict_handler_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``LambdaConflictHandlerConfig`` object when configuring ``LAMBDA`` as the Conflict Handler.

            :param lambda_conflict_handler_arn: The Amazon Resource Name (ARN) for the Lambda function to use as the Conflict Handler.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-functionconfiguration-lambdaconflicthandlerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                lambda_conflict_handler_config_property = appsync_mixins.CfnFunctionConfigurationPropsMixin.LambdaConflictHandlerConfigProperty(
                    lambda_conflict_handler_arn="lambdaConflictHandlerArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__20a24a8643992fddbbe4e2a165a11de5b5c58796f6ecc2f18d0fa506a34e0572)
                check_type(argname="argument lambda_conflict_handler_arn", value=lambda_conflict_handler_arn, expected_type=type_hints["lambda_conflict_handler_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_conflict_handler_arn is not None:
                self._values["lambda_conflict_handler_arn"] = lambda_conflict_handler_arn

        @builtins.property
        def lambda_conflict_handler_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the Lambda function to use as the Conflict Handler.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-functionconfiguration-lambdaconflicthandlerconfig.html#cfn-appsync-functionconfiguration-lambdaconflicthandlerconfig-lambdaconflicthandlerarn
            '''
            result = self._values.get("lambda_conflict_handler_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaConflictHandlerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnFunctionConfigurationPropsMixin.SyncConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "conflict_detection": "conflictDetection",
            "conflict_handler": "conflictHandler",
            "lambda_conflict_handler_config": "lambdaConflictHandlerConfig",
        },
    )
    class SyncConfigProperty:
        def __init__(
            self,
            *,
            conflict_detection: typing.Optional[builtins.str] = None,
            conflict_handler: typing.Optional[builtins.str] = None,
            lambda_conflict_handler_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionConfigurationPropsMixin.LambdaConflictHandlerConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes a Sync configuration for a resolver.

            Specifies which Conflict Detection strategy and Resolution strategy to use when the resolver is invoked.

            :param conflict_detection: The Conflict Detection strategy to use. - *VERSION* : Detect conflicts based on object versions for this resolver. - *NONE* : Do not detect conflicts when invoking this resolver.
            :param conflict_handler: The Conflict Resolution strategy to perform in the event of a conflict. - *OPTIMISTIC_CONCURRENCY* : Resolve conflicts by rejecting mutations when versions don't match the latest version at the server. - *AUTOMERGE* : Resolve conflicts with the Automerge conflict resolution strategy. - *LAMBDA* : Resolve conflicts with an AWS Lambda function supplied in the ``LambdaConflictHandlerConfig`` .
            :param lambda_conflict_handler_config: The ``LambdaConflictHandlerConfig`` when configuring ``LAMBDA`` as the Conflict Handler.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-functionconfiguration-syncconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                sync_config_property = appsync_mixins.CfnFunctionConfigurationPropsMixin.SyncConfigProperty(
                    conflict_detection="conflictDetection",
                    conflict_handler="conflictHandler",
                    lambda_conflict_handler_config=appsync_mixins.CfnFunctionConfigurationPropsMixin.LambdaConflictHandlerConfigProperty(
                        lambda_conflict_handler_arn="lambdaConflictHandlerArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8330060895de021d48b939cefd6dc2cdbef75cfbcd9609229922ff6ac1bd4020)
                check_type(argname="argument conflict_detection", value=conflict_detection, expected_type=type_hints["conflict_detection"])
                check_type(argname="argument conflict_handler", value=conflict_handler, expected_type=type_hints["conflict_handler"])
                check_type(argname="argument lambda_conflict_handler_config", value=lambda_conflict_handler_config, expected_type=type_hints["lambda_conflict_handler_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if conflict_detection is not None:
                self._values["conflict_detection"] = conflict_detection
            if conflict_handler is not None:
                self._values["conflict_handler"] = conflict_handler
            if lambda_conflict_handler_config is not None:
                self._values["lambda_conflict_handler_config"] = lambda_conflict_handler_config

        @builtins.property
        def conflict_detection(self) -> typing.Optional[builtins.str]:
            '''The Conflict Detection strategy to use.

            - *VERSION* : Detect conflicts based on object versions for this resolver.
            - *NONE* : Do not detect conflicts when invoking this resolver.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-functionconfiguration-syncconfig.html#cfn-appsync-functionconfiguration-syncconfig-conflictdetection
            '''
            result = self._values.get("conflict_detection")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def conflict_handler(self) -> typing.Optional[builtins.str]:
            '''The Conflict Resolution strategy to perform in the event of a conflict.

            - *OPTIMISTIC_CONCURRENCY* : Resolve conflicts by rejecting mutations when versions don't match the latest version at the server.
            - *AUTOMERGE* : Resolve conflicts with the Automerge conflict resolution strategy.
            - *LAMBDA* : Resolve conflicts with an AWS Lambda function supplied in the ``LambdaConflictHandlerConfig`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-functionconfiguration-syncconfig.html#cfn-appsync-functionconfiguration-syncconfig-conflicthandler
            '''
            result = self._values.get("conflict_handler")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def lambda_conflict_handler_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionConfigurationPropsMixin.LambdaConflictHandlerConfigProperty"]]:
            '''The ``LambdaConflictHandlerConfig`` when configuring ``LAMBDA`` as the Conflict Handler.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-functionconfiguration-syncconfig.html#cfn-appsync-functionconfiguration-syncconfig-lambdaconflicthandlerconfig
            '''
            result = self._values.get("lambda_conflict_handler_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionConfigurationPropsMixin.LambdaConflictHandlerConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SyncConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnGraphQLApiMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "additional_authentication_providers": "additionalAuthenticationProviders",
        "api_type": "apiType",
        "authentication_type": "authenticationType",
        "enhanced_metrics_config": "enhancedMetricsConfig",
        "environment_variables": "environmentVariables",
        "introspection_config": "introspectionConfig",
        "lambda_authorizer_config": "lambdaAuthorizerConfig",
        "log_config": "logConfig",
        "merged_api_execution_role_arn": "mergedApiExecutionRoleArn",
        "name": "name",
        "open_id_connect_config": "openIdConnectConfig",
        "owner_contact": "ownerContact",
        "query_depth_limit": "queryDepthLimit",
        "resolver_count_limit": "resolverCountLimit",
        "tags": "tags",
        "user_pool_config": "userPoolConfig",
        "visibility": "visibility",
        "xray_enabled": "xrayEnabled",
    },
)
class CfnGraphQLApiMixinProps:
    def __init__(
        self,
        *,
        additional_authentication_providers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGraphQLApiPropsMixin.AdditionalAuthenticationProviderProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        api_type: typing.Optional[builtins.str] = None,
        authentication_type: typing.Optional[builtins.str] = None,
        enhanced_metrics_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGraphQLApiPropsMixin.EnhancedMetricsConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        environment_variables: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        introspection_config: typing.Optional[builtins.str] = None,
        lambda_authorizer_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGraphQLApiPropsMixin.LambdaAuthorizerConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        log_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGraphQLApiPropsMixin.LogConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        merged_api_execution_role_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        open_id_connect_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGraphQLApiPropsMixin.OpenIDConnectConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        owner_contact: typing.Optional[builtins.str] = None,
        query_depth_limit: typing.Optional[jsii.Number] = None,
        resolver_count_limit: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_pool_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGraphQLApiPropsMixin.UserPoolConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        visibility: typing.Optional[builtins.str] = None,
        xray_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ) -> None:
        '''Properties for CfnGraphQLApiPropsMixin.

        :param additional_authentication_providers: A list of additional authentication providers for the ``GraphqlApi`` API.
        :param api_type: The value that indicates whether the GraphQL API is a standard API ( ``GRAPHQL`` ) or merged API ( ``MERGED`` ). *WARNING* : If the ``ApiType`` has not been defined, *explicitly* setting it to ``GRAPHQL`` in a template/stack update will result in an API replacement and new DNS values. The following values are valid: ``GRAPHQL | MERGED``
        :param authentication_type: Security configuration for your GraphQL API. For allowed values (such as ``API_KEY`` , ``AWS_IAM`` , ``AMAZON_COGNITO_USER_POOLS`` , ``OPENID_CONNECT`` , or ``AWS_LAMBDA`` ), see `Security <https://docs.aws.amazon.com/appsync/latest/devguide/security.html>`_ in the *AWS AppSync Developer Guide* .
        :param enhanced_metrics_config: Enables and controls the enhanced metrics feature. Enhanced metrics emit granular data on API usage and performance such as AppSync request and error counts, latency, and cache hits/misses. All enhanced metric data is sent to your CloudWatch account, and you can configure the types of data that will be sent. Enhanced metrics can be configured at the resolver, data source, and operation levels. For more information, see `Monitoring and logging <https://docs.aws.amazon.com//appsync/latest/devguide/monitoring.html#cw-metrics>`_ in the *AWS AppSync User Guide* .
        :param environment_variables: A map containing the list of resources with their properties and environment variables. For more information, see `Environmental variables <https://docs.aws.amazon.com/appsync/latest/devguide/environmental-variables.html>`_ . *Pattern* : ``^[A-Za-z]+\\\\w*$\\\\`` *Minimum* : 2 *Maximum* : 64
        :param introspection_config: Sets the value of the GraphQL API to enable ( ``ENABLED`` ) or disable ( ``DISABLED`` ) introspection. If no value is provided, the introspection configuration will be set to ``ENABLED`` by default. This field will produce an error if the operation attempts to use the introspection feature while this field is disabled. For more information about introspection, see `GraphQL introspection <https://docs.aws.amazon.com/https://graphql.org/learn/introspection/>`_ .
        :param lambda_authorizer_config: A ``LambdaAuthorizerConfig`` holds configuration on how to authorize AWS AppSync API access when using the ``AWS_LAMBDA`` authorizer mode. Be aware that an AWS AppSync API may have only one Lambda authorizer configured at a time.
        :param log_config: The Amazon CloudWatch Logs configuration.
        :param merged_api_execution_role_arn: The AWS Identity and Access Management service role ARN for a merged API. The AppSync service assumes this role on behalf of the Merged API to validate access to source APIs at runtime and to prompt the ``AUTO_MERGE`` to update the merged API endpoint with the source API changes automatically.
        :param name: The API name.
        :param open_id_connect_config: The OpenID Connect configuration.
        :param owner_contact: The owner contact information for an API resource. This field accepts any string input with a length of 0 - 256 characters.
        :param query_depth_limit: The maximum depth a query can have in a single request. Depth refers to the amount of nested levels allowed in the body of query. The default value is ``0`` (or unspecified), which indicates there's no depth limit. If you set a limit, it can be between ``1`` and ``75`` nested levels. This field will produce a limit error if the operation falls out of bounds. Note that fields can still be set to nullable or non-nullable. If a non-nullable field produces an error, the error will be thrown upwards to the first nullable field available.
        :param resolver_count_limit: The maximum number of resolvers that can be invoked in a single request. The default value is ``0`` (or unspecified), which will set the limit to ``10000`` . When specified, the limit value can be between ``1`` and ``10000`` . This field will produce a limit error if the operation falls out of bounds.
        :param tags: An arbitrary set of tags (key-value pairs) for this GraphQL API.
        :param user_pool_config: Optional authorization configuration for using Amazon Cognito user pools with your GraphQL endpoint.
        :param visibility: Sets the scope of the GraphQL API to public ( ``GLOBAL`` ) or private ( ``PRIVATE`` ). By default, the scope is set to ``Global`` if no value is provided. *WARNING* : If ``Visibility`` has not been defined, *explicitly* setting it to ``GLOBAL`` in a template/stack update will result in an API replacement and new DNS values.
        :param xray_enabled: A flag indicating whether to use AWS X-Ray tracing for this ``GraphqlApi`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
            
            cfn_graph_qLApi_mixin_props = appsync_mixins.CfnGraphQLApiMixinProps(
                additional_authentication_providers=[appsync_mixins.CfnGraphQLApiPropsMixin.AdditionalAuthenticationProviderProperty(
                    authentication_type="authenticationType",
                    lambda_authorizer_config=appsync_mixins.CfnGraphQLApiPropsMixin.LambdaAuthorizerConfigProperty(
                        authorizer_result_ttl_in_seconds=123,
                        authorizer_uri="authorizerUri",
                        identity_validation_expression="identityValidationExpression"
                    ),
                    open_id_connect_config=appsync_mixins.CfnGraphQLApiPropsMixin.OpenIDConnectConfigProperty(
                        auth_ttl=123,
                        client_id="clientId",
                        iat_ttl=123,
                        issuer="issuer"
                    ),
                    user_pool_config=appsync_mixins.CfnGraphQLApiPropsMixin.CognitoUserPoolConfigProperty(
                        app_id_client_regex="appIdClientRegex",
                        aws_region="awsRegion",
                        user_pool_id="userPoolId"
                    )
                )],
                api_type="apiType",
                authentication_type="authenticationType",
                enhanced_metrics_config=appsync_mixins.CfnGraphQLApiPropsMixin.EnhancedMetricsConfigProperty(
                    data_source_level_metrics_behavior="dataSourceLevelMetricsBehavior",
                    operation_level_metrics_config="operationLevelMetricsConfig",
                    resolver_level_metrics_behavior="resolverLevelMetricsBehavior"
                ),
                environment_variables={
                    "environment_variables_key": "environmentVariables"
                },
                introspection_config="introspectionConfig",
                lambda_authorizer_config=appsync_mixins.CfnGraphQLApiPropsMixin.LambdaAuthorizerConfigProperty(
                    authorizer_result_ttl_in_seconds=123,
                    authorizer_uri="authorizerUri",
                    identity_validation_expression="identityValidationExpression"
                ),
                log_config=appsync_mixins.CfnGraphQLApiPropsMixin.LogConfigProperty(
                    cloud_watch_logs_role_arn="cloudWatchLogsRoleArn",
                    exclude_verbose_content=False,
                    field_log_level="fieldLogLevel"
                ),
                merged_api_execution_role_arn="mergedApiExecutionRoleArn",
                name="name",
                open_id_connect_config=appsync_mixins.CfnGraphQLApiPropsMixin.OpenIDConnectConfigProperty(
                    auth_ttl=123,
                    client_id="clientId",
                    iat_ttl=123,
                    issuer="issuer"
                ),
                owner_contact="ownerContact",
                query_depth_limit=123,
                resolver_count_limit=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                user_pool_config=appsync_mixins.CfnGraphQLApiPropsMixin.UserPoolConfigProperty(
                    app_id_client_regex="appIdClientRegex",
                    aws_region="awsRegion",
                    default_action="defaultAction",
                    user_pool_id="userPoolId"
                ),
                visibility="visibility",
                xray_enabled=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab0a3a506028393a5970f51b244e086ad074d9c88750e6ee8df9474f3f0b1712)
            check_type(argname="argument additional_authentication_providers", value=additional_authentication_providers, expected_type=type_hints["additional_authentication_providers"])
            check_type(argname="argument api_type", value=api_type, expected_type=type_hints["api_type"])
            check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
            check_type(argname="argument enhanced_metrics_config", value=enhanced_metrics_config, expected_type=type_hints["enhanced_metrics_config"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument introspection_config", value=introspection_config, expected_type=type_hints["introspection_config"])
            check_type(argname="argument lambda_authorizer_config", value=lambda_authorizer_config, expected_type=type_hints["lambda_authorizer_config"])
            check_type(argname="argument log_config", value=log_config, expected_type=type_hints["log_config"])
            check_type(argname="argument merged_api_execution_role_arn", value=merged_api_execution_role_arn, expected_type=type_hints["merged_api_execution_role_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument open_id_connect_config", value=open_id_connect_config, expected_type=type_hints["open_id_connect_config"])
            check_type(argname="argument owner_contact", value=owner_contact, expected_type=type_hints["owner_contact"])
            check_type(argname="argument query_depth_limit", value=query_depth_limit, expected_type=type_hints["query_depth_limit"])
            check_type(argname="argument resolver_count_limit", value=resolver_count_limit, expected_type=type_hints["resolver_count_limit"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_pool_config", value=user_pool_config, expected_type=type_hints["user_pool_config"])
            check_type(argname="argument visibility", value=visibility, expected_type=type_hints["visibility"])
            check_type(argname="argument xray_enabled", value=xray_enabled, expected_type=type_hints["xray_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_authentication_providers is not None:
            self._values["additional_authentication_providers"] = additional_authentication_providers
        if api_type is not None:
            self._values["api_type"] = api_type
        if authentication_type is not None:
            self._values["authentication_type"] = authentication_type
        if enhanced_metrics_config is not None:
            self._values["enhanced_metrics_config"] = enhanced_metrics_config
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if introspection_config is not None:
            self._values["introspection_config"] = introspection_config
        if lambda_authorizer_config is not None:
            self._values["lambda_authorizer_config"] = lambda_authorizer_config
        if log_config is not None:
            self._values["log_config"] = log_config
        if merged_api_execution_role_arn is not None:
            self._values["merged_api_execution_role_arn"] = merged_api_execution_role_arn
        if name is not None:
            self._values["name"] = name
        if open_id_connect_config is not None:
            self._values["open_id_connect_config"] = open_id_connect_config
        if owner_contact is not None:
            self._values["owner_contact"] = owner_contact
        if query_depth_limit is not None:
            self._values["query_depth_limit"] = query_depth_limit
        if resolver_count_limit is not None:
            self._values["resolver_count_limit"] = resolver_count_limit
        if tags is not None:
            self._values["tags"] = tags
        if user_pool_config is not None:
            self._values["user_pool_config"] = user_pool_config
        if visibility is not None:
            self._values["visibility"] = visibility
        if xray_enabled is not None:
            self._values["xray_enabled"] = xray_enabled

    @builtins.property
    def additional_authentication_providers(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGraphQLApiPropsMixin.AdditionalAuthenticationProviderProperty"]]]]:
        '''A list of additional authentication providers for the ``GraphqlApi`` API.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-additionalauthenticationproviders
        '''
        result = self._values.get("additional_authentication_providers")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGraphQLApiPropsMixin.AdditionalAuthenticationProviderProperty"]]]], result)

    @builtins.property
    def api_type(self) -> typing.Optional[builtins.str]:
        '''The value that indicates whether the GraphQL API is a standard API ( ``GRAPHQL`` ) or merged API ( ``MERGED`` ).

        *WARNING* : If the ``ApiType`` has not been defined, *explicitly* setting it to ``GRAPHQL`` in a template/stack update will result in an API replacement and new DNS values.

        The following values are valid:

        ``GRAPHQL | MERGED``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-apitype
        '''
        result = self._values.get("api_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authentication_type(self) -> typing.Optional[builtins.str]:
        '''Security configuration for your GraphQL API.

        For allowed values (such as ``API_KEY`` , ``AWS_IAM`` , ``AMAZON_COGNITO_USER_POOLS`` , ``OPENID_CONNECT`` , or ``AWS_LAMBDA`` ), see `Security <https://docs.aws.amazon.com/appsync/latest/devguide/security.html>`_ in the *AWS AppSync Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-authenticationtype
        '''
        result = self._values.get("authentication_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enhanced_metrics_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGraphQLApiPropsMixin.EnhancedMetricsConfigProperty"]]:
        '''Enables and controls the enhanced metrics feature.

        Enhanced metrics emit granular data on API usage and performance such as AppSync request and error counts, latency, and cache hits/misses. All enhanced metric data is sent to your CloudWatch account, and you can configure the types of data that will be sent.

        Enhanced metrics can be configured at the resolver, data source, and operation levels. For more information, see `Monitoring and logging <https://docs.aws.amazon.com//appsync/latest/devguide/monitoring.html#cw-metrics>`_ in the *AWS AppSync User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-enhancedmetricsconfig
        '''
        result = self._values.get("enhanced_metrics_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGraphQLApiPropsMixin.EnhancedMetricsConfigProperty"]], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''A map containing the list of resources with their properties and environment variables.

        For more information, see `Environmental variables <https://docs.aws.amazon.com/appsync/latest/devguide/environmental-variables.html>`_ .

        *Pattern* : ``^[A-Za-z]+\\\\w*$\\\\``

        *Minimum* : 2

        *Maximum* : 64

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-environmentvariables
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def introspection_config(self) -> typing.Optional[builtins.str]:
        '''Sets the value of the GraphQL API to enable ( ``ENABLED`` ) or disable ( ``DISABLED`` ) introspection.

        If no value is provided, the introspection configuration will be set to ``ENABLED`` by default. This field will produce an error if the operation attempts to use the introspection feature while this field is disabled.

        For more information about introspection, see `GraphQL introspection <https://docs.aws.amazon.com/https://graphql.org/learn/introspection/>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-introspectionconfig
        '''
        result = self._values.get("introspection_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lambda_authorizer_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGraphQLApiPropsMixin.LambdaAuthorizerConfigProperty"]]:
        '''A ``LambdaAuthorizerConfig`` holds configuration on how to authorize AWS AppSync API access when using the ``AWS_LAMBDA`` authorizer mode.

        Be aware that an AWS AppSync API may have only one Lambda authorizer configured at a time.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-lambdaauthorizerconfig
        '''
        result = self._values.get("lambda_authorizer_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGraphQLApiPropsMixin.LambdaAuthorizerConfigProperty"]], result)

    @builtins.property
    def log_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGraphQLApiPropsMixin.LogConfigProperty"]]:
        '''The Amazon CloudWatch Logs configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-logconfig
        '''
        result = self._values.get("log_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGraphQLApiPropsMixin.LogConfigProperty"]], result)

    @builtins.property
    def merged_api_execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''The AWS Identity and Access Management service role ARN for a merged API.

        The AppSync service assumes this role on behalf of the Merged API to validate access to source APIs at runtime and to prompt the ``AUTO_MERGE`` to update the merged API endpoint with the source API changes automatically.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-mergedapiexecutionrolearn
        '''
        result = self._values.get("merged_api_execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The API name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def open_id_connect_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGraphQLApiPropsMixin.OpenIDConnectConfigProperty"]]:
        '''The OpenID Connect configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-openidconnectconfig
        '''
        result = self._values.get("open_id_connect_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGraphQLApiPropsMixin.OpenIDConnectConfigProperty"]], result)

    @builtins.property
    def owner_contact(self) -> typing.Optional[builtins.str]:
        '''The owner contact information for an API resource.

        This field accepts any string input with a length of 0 - 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-ownercontact
        '''
        result = self._values.get("owner_contact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_depth_limit(self) -> typing.Optional[jsii.Number]:
        '''The maximum depth a query can have in a single request.

        Depth refers to the amount of nested levels allowed in the body of query. The default value is ``0`` (or unspecified), which indicates there's no depth limit. If you set a limit, it can be between ``1`` and ``75`` nested levels. This field will produce a limit error if the operation falls out of bounds. Note that fields can still be set to nullable or non-nullable. If a non-nullable field produces an error, the error will be thrown upwards to the first nullable field available.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-querydepthlimit
        '''
        result = self._values.get("query_depth_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resolver_count_limit(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of resolvers that can be invoked in a single request.

        The default value is ``0`` (or unspecified), which will set the limit to ``10000`` . When specified, the limit value can be between ``1`` and ``10000`` . This field will produce a limit error if the operation falls out of bounds.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-resolvercountlimit
        '''
        result = self._values.get("resolver_count_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An arbitrary set of tags (key-value pairs) for this GraphQL API.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def user_pool_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGraphQLApiPropsMixin.UserPoolConfigProperty"]]:
        '''Optional authorization configuration for using Amazon Cognito user pools with your GraphQL endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-userpoolconfig
        '''
        result = self._values.get("user_pool_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGraphQLApiPropsMixin.UserPoolConfigProperty"]], result)

    @builtins.property
    def visibility(self) -> typing.Optional[builtins.str]:
        '''Sets the scope of the GraphQL API to public ( ``GLOBAL`` ) or private ( ``PRIVATE`` ).

        By default, the scope is set to ``Global`` if no value is provided.

        *WARNING* : If ``Visibility`` has not been defined, *explicitly* setting it to ``GLOBAL`` in a template/stack update will result in an API replacement and new DNS values.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-visibility
        '''
        result = self._values.get("visibility")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def xray_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A flag indicating whether to use AWS X-Ray tracing for this ``GraphqlApi`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-xrayenabled
        '''
        result = self._values.get("xray_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGraphQLApiMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGraphQLApiPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnGraphQLApiPropsMixin",
):
    '''The ``AWS::AppSync::GraphQLApi`` resource creates a new AWS AppSync GraphQL API.

    This is the top-level construct for your application. For more information, see `Quick Start <https://docs.aws.amazon.com/appsync/latest/devguide/quickstart.html>`_ in the *AWS AppSync Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html
    :cloudformationResource: AWS::AppSync::GraphQLApi
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
        
        cfn_graph_qLApi_props_mixin = appsync_mixins.CfnGraphQLApiPropsMixin(appsync_mixins.CfnGraphQLApiMixinProps(
            additional_authentication_providers=[appsync_mixins.CfnGraphQLApiPropsMixin.AdditionalAuthenticationProviderProperty(
                authentication_type="authenticationType",
                lambda_authorizer_config=appsync_mixins.CfnGraphQLApiPropsMixin.LambdaAuthorizerConfigProperty(
                    authorizer_result_ttl_in_seconds=123,
                    authorizer_uri="authorizerUri",
                    identity_validation_expression="identityValidationExpression"
                ),
                open_id_connect_config=appsync_mixins.CfnGraphQLApiPropsMixin.OpenIDConnectConfigProperty(
                    auth_ttl=123,
                    client_id="clientId",
                    iat_ttl=123,
                    issuer="issuer"
                ),
                user_pool_config=appsync_mixins.CfnGraphQLApiPropsMixin.CognitoUserPoolConfigProperty(
                    app_id_client_regex="appIdClientRegex",
                    aws_region="awsRegion",
                    user_pool_id="userPoolId"
                )
            )],
            api_type="apiType",
            authentication_type="authenticationType",
            enhanced_metrics_config=appsync_mixins.CfnGraphQLApiPropsMixin.EnhancedMetricsConfigProperty(
                data_source_level_metrics_behavior="dataSourceLevelMetricsBehavior",
                operation_level_metrics_config="operationLevelMetricsConfig",
                resolver_level_metrics_behavior="resolverLevelMetricsBehavior"
            ),
            environment_variables={
                "environment_variables_key": "environmentVariables"
            },
            introspection_config="introspectionConfig",
            lambda_authorizer_config=appsync_mixins.CfnGraphQLApiPropsMixin.LambdaAuthorizerConfigProperty(
                authorizer_result_ttl_in_seconds=123,
                authorizer_uri="authorizerUri",
                identity_validation_expression="identityValidationExpression"
            ),
            log_config=appsync_mixins.CfnGraphQLApiPropsMixin.LogConfigProperty(
                cloud_watch_logs_role_arn="cloudWatchLogsRoleArn",
                exclude_verbose_content=False,
                field_log_level="fieldLogLevel"
            ),
            merged_api_execution_role_arn="mergedApiExecutionRoleArn",
            name="name",
            open_id_connect_config=appsync_mixins.CfnGraphQLApiPropsMixin.OpenIDConnectConfigProperty(
                auth_ttl=123,
                client_id="clientId",
                iat_ttl=123,
                issuer="issuer"
            ),
            owner_contact="ownerContact",
            query_depth_limit=123,
            resolver_count_limit=123,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            user_pool_config=appsync_mixins.CfnGraphQLApiPropsMixin.UserPoolConfigProperty(
                app_id_client_regex="appIdClientRegex",
                aws_region="awsRegion",
                default_action="defaultAction",
                user_pool_id="userPoolId"
            ),
            visibility="visibility",
            xray_enabled=False
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnGraphQLApiMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppSync::GraphQLApi``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fb6d6dec558f2a878ea479d7e4ba94a457fa1f0c353f1ca65f28867e536197c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae55ccf4e97b09379e6ad13639101c645997f25441ea4195d218763f8a2cade6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ac6217d798fce36c378877c7101f89feab8c7a3d18f79ab3cff876caebf2d37)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGraphQLApiMixinProps:
        return typing.cast(CfnGraphQLApiMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnGraphQLApiPropsMixin.AdditionalAuthenticationProviderProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authentication_type": "authenticationType",
            "lambda_authorizer_config": "lambdaAuthorizerConfig",
            "open_id_connect_config": "openIdConnectConfig",
            "user_pool_config": "userPoolConfig",
        },
    )
    class AdditionalAuthenticationProviderProperty:
        def __init__(
            self,
            *,
            authentication_type: typing.Optional[builtins.str] = None,
            lambda_authorizer_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGraphQLApiPropsMixin.LambdaAuthorizerConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            open_id_connect_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGraphQLApiPropsMixin.OpenIDConnectConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            user_pool_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGraphQLApiPropsMixin.CognitoUserPoolConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes an additional authentication provider.

            :param authentication_type: The authentication type for API key, AWS Identity and Access Management , OIDC, Amazon Cognito user pools , or AWS Lambda . Valid Values: ``API_KEY`` | ``AWS_IAM`` | ``OPENID_CONNECT`` | ``AMAZON_COGNITO_USER_POOLS`` | ``AWS_LAMBDA``
            :param lambda_authorizer_config: Configuration for AWS Lambda function authorization.
            :param open_id_connect_config: The OIDC configuration.
            :param user_pool_config: The Amazon Cognito user pool configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-additionalauthenticationprovider.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                additional_authentication_provider_property = appsync_mixins.CfnGraphQLApiPropsMixin.AdditionalAuthenticationProviderProperty(
                    authentication_type="authenticationType",
                    lambda_authorizer_config=appsync_mixins.CfnGraphQLApiPropsMixin.LambdaAuthorizerConfigProperty(
                        authorizer_result_ttl_in_seconds=123,
                        authorizer_uri="authorizerUri",
                        identity_validation_expression="identityValidationExpression"
                    ),
                    open_id_connect_config=appsync_mixins.CfnGraphQLApiPropsMixin.OpenIDConnectConfigProperty(
                        auth_ttl=123,
                        client_id="clientId",
                        iat_ttl=123,
                        issuer="issuer"
                    ),
                    user_pool_config=appsync_mixins.CfnGraphQLApiPropsMixin.CognitoUserPoolConfigProperty(
                        app_id_client_regex="appIdClientRegex",
                        aws_region="awsRegion",
                        user_pool_id="userPoolId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6c544e503256e1b2e51d9ea26c4072b1c99c534407e4e0ef8e9fb1bbe2a91313)
                check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
                check_type(argname="argument lambda_authorizer_config", value=lambda_authorizer_config, expected_type=type_hints["lambda_authorizer_config"])
                check_type(argname="argument open_id_connect_config", value=open_id_connect_config, expected_type=type_hints["open_id_connect_config"])
                check_type(argname="argument user_pool_config", value=user_pool_config, expected_type=type_hints["user_pool_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authentication_type is not None:
                self._values["authentication_type"] = authentication_type
            if lambda_authorizer_config is not None:
                self._values["lambda_authorizer_config"] = lambda_authorizer_config
            if open_id_connect_config is not None:
                self._values["open_id_connect_config"] = open_id_connect_config
            if user_pool_config is not None:
                self._values["user_pool_config"] = user_pool_config

        @builtins.property
        def authentication_type(self) -> typing.Optional[builtins.str]:
            '''The authentication type for API key, AWS Identity and Access Management , OIDC, Amazon Cognito user pools , or AWS Lambda .

            Valid Values: ``API_KEY`` | ``AWS_IAM`` | ``OPENID_CONNECT`` | ``AMAZON_COGNITO_USER_POOLS`` | ``AWS_LAMBDA``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-additionalauthenticationprovider.html#cfn-appsync-graphqlapi-additionalauthenticationprovider-authenticationtype
            '''
            result = self._values.get("authentication_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def lambda_authorizer_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGraphQLApiPropsMixin.LambdaAuthorizerConfigProperty"]]:
            '''Configuration for AWS Lambda function authorization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-additionalauthenticationprovider.html#cfn-appsync-graphqlapi-additionalauthenticationprovider-lambdaauthorizerconfig
            '''
            result = self._values.get("lambda_authorizer_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGraphQLApiPropsMixin.LambdaAuthorizerConfigProperty"]], result)

        @builtins.property
        def open_id_connect_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGraphQLApiPropsMixin.OpenIDConnectConfigProperty"]]:
            '''The OIDC configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-additionalauthenticationprovider.html#cfn-appsync-graphqlapi-additionalauthenticationprovider-openidconnectconfig
            '''
            result = self._values.get("open_id_connect_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGraphQLApiPropsMixin.OpenIDConnectConfigProperty"]], result)

        @builtins.property
        def user_pool_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGraphQLApiPropsMixin.CognitoUserPoolConfigProperty"]]:
            '''The Amazon Cognito user pool configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-additionalauthenticationprovider.html#cfn-appsync-graphqlapi-additionalauthenticationprovider-userpoolconfig
            '''
            result = self._values.get("user_pool_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGraphQLApiPropsMixin.CognitoUserPoolConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdditionalAuthenticationProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnGraphQLApiPropsMixin.CognitoUserPoolConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "app_id_client_regex": "appIdClientRegex",
            "aws_region": "awsRegion",
            "user_pool_id": "userPoolId",
        },
    )
    class CognitoUserPoolConfigProperty:
        def __init__(
            self,
            *,
            app_id_client_regex: typing.Optional[builtins.str] = None,
            aws_region: typing.Optional[builtins.str] = None,
            user_pool_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes an Amazon Cognito user pool configuration.

            :param app_id_client_regex: A regular expression for validating the incoming Amazon Cognito user pool app client ID. If this value isn't set, no filtering is applied.
            :param aws_region: The AWS Region in which the user pool was created.
            :param user_pool_id: The user pool ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-cognitouserpoolconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                cognito_user_pool_config_property = appsync_mixins.CfnGraphQLApiPropsMixin.CognitoUserPoolConfigProperty(
                    app_id_client_regex="appIdClientRegex",
                    aws_region="awsRegion",
                    user_pool_id="userPoolId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e3d96ab603a5b124e7aa3d4626682eb04f9913536fa76af5f2f8bdf670e9aae8)
                check_type(argname="argument app_id_client_regex", value=app_id_client_regex, expected_type=type_hints["app_id_client_regex"])
                check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if app_id_client_regex is not None:
                self._values["app_id_client_regex"] = app_id_client_regex
            if aws_region is not None:
                self._values["aws_region"] = aws_region
            if user_pool_id is not None:
                self._values["user_pool_id"] = user_pool_id

        @builtins.property
        def app_id_client_regex(self) -> typing.Optional[builtins.str]:
            '''A regular expression for validating the incoming Amazon Cognito user pool app client ID.

            If this value isn't set, no filtering is applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-cognitouserpoolconfig.html#cfn-appsync-graphqlapi-cognitouserpoolconfig-appidclientregex
            '''
            result = self._values.get("app_id_client_regex")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def aws_region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region in which the user pool was created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-cognitouserpoolconfig.html#cfn-appsync-graphqlapi-cognitouserpoolconfig-awsregion
            '''
            result = self._values.get("aws_region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_pool_id(self) -> typing.Optional[builtins.str]:
            '''The user pool ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-cognitouserpoolconfig.html#cfn-appsync-graphqlapi-cognitouserpoolconfig-userpoolid
            '''
            result = self._values.get("user_pool_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CognitoUserPoolConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnGraphQLApiPropsMixin.EnhancedMetricsConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_source_level_metrics_behavior": "dataSourceLevelMetricsBehavior",
            "operation_level_metrics_config": "operationLevelMetricsConfig",
            "resolver_level_metrics_behavior": "resolverLevelMetricsBehavior",
        },
    )
    class EnhancedMetricsConfigProperty:
        def __init__(
            self,
            *,
            data_source_level_metrics_behavior: typing.Optional[builtins.str] = None,
            operation_level_metrics_config: typing.Optional[builtins.str] = None,
            resolver_level_metrics_behavior: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes an enhanced metrics configuration.

            :param data_source_level_metrics_behavior: Controls how data source metrics will be emitted to CloudWatch. Data source metrics include:. - *Requests* : The number of invocations that occured during a request. - *Latency* : The time to complete a data source invocation. - *Errors* : The number of errors that occurred during a data source invocation. These metrics can be emitted to CloudWatch per data source or for all data sources in the request. Metrics will be recorded by API ID and data source name. ``dataSourceLevelMetricsBehavior`` accepts one of these values at a time: - ``FULL_REQUEST_DATA_SOURCE_METRICS`` : Records and emits metric data for all data sources in the request. - ``PER_DATA_SOURCE_METRICS`` : Records and emits metric data for data sources that have the ``MetricsConfig`` value set to ``ENABLED`` .
            :param operation_level_metrics_config: Controls how operation metrics will be emitted to CloudWatch. Operation metrics include:. - *Requests* : The number of times a specified GraphQL operation was called. - *GraphQL errors* : The number of GraphQL errors that occurred during a specified GraphQL operation. Metrics will be recorded by API ID and operation name. You can set the value to ``ENABLED`` or ``DISABLED`` .
            :param resolver_level_metrics_behavior: Controls how resolver metrics will be emitted to CloudWatch. Resolver metrics include:. - *GraphQL errors* : The number of GraphQL errors that occurred. - *Requests* : The number of invocations that occurred during a request. - *Latency* : The time to complete a resolver invocation. - *Cache hits* : The number of cache hits during a request. - *Cache misses* : The number of cache misses during a request. These metrics can be emitted to CloudWatch per resolver or for all resolvers in the request. Metrics will be recorded by API ID and resolver name. ``resolverLevelMetricsBehavior`` accepts one of these values at a time: - ``FULL_REQUEST_RESOLVER_METRICS`` : Records and emits metric data for all resolvers in the request. - ``PER_RESOLVER_METRICS`` : Records and emits metric data for resolvers that have the ``MetricsConfig`` value set to ``ENABLED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-enhancedmetricsconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                enhanced_metrics_config_property = appsync_mixins.CfnGraphQLApiPropsMixin.EnhancedMetricsConfigProperty(
                    data_source_level_metrics_behavior="dataSourceLevelMetricsBehavior",
                    operation_level_metrics_config="operationLevelMetricsConfig",
                    resolver_level_metrics_behavior="resolverLevelMetricsBehavior"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__524236f3cab3eab7e5e9a62c2a342cb611b20334a6ad3da177c5cdf3235c281a)
                check_type(argname="argument data_source_level_metrics_behavior", value=data_source_level_metrics_behavior, expected_type=type_hints["data_source_level_metrics_behavior"])
                check_type(argname="argument operation_level_metrics_config", value=operation_level_metrics_config, expected_type=type_hints["operation_level_metrics_config"])
                check_type(argname="argument resolver_level_metrics_behavior", value=resolver_level_metrics_behavior, expected_type=type_hints["resolver_level_metrics_behavior"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_source_level_metrics_behavior is not None:
                self._values["data_source_level_metrics_behavior"] = data_source_level_metrics_behavior
            if operation_level_metrics_config is not None:
                self._values["operation_level_metrics_config"] = operation_level_metrics_config
            if resolver_level_metrics_behavior is not None:
                self._values["resolver_level_metrics_behavior"] = resolver_level_metrics_behavior

        @builtins.property
        def data_source_level_metrics_behavior(self) -> typing.Optional[builtins.str]:
            '''Controls how data source metrics will be emitted to CloudWatch. Data source metrics include:.

            - *Requests* : The number of invocations that occured during a request.
            - *Latency* : The time to complete a data source invocation.
            - *Errors* : The number of errors that occurred during a data source invocation.

            These metrics can be emitted to CloudWatch per data source or for all data sources in the request. Metrics will be recorded by API ID and data source name. ``dataSourceLevelMetricsBehavior`` accepts one of these values at a time:

            - ``FULL_REQUEST_DATA_SOURCE_METRICS`` : Records and emits metric data for all data sources in the request.
            - ``PER_DATA_SOURCE_METRICS`` : Records and emits metric data for data sources that have the ``MetricsConfig`` value set to ``ENABLED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-enhancedmetricsconfig.html#cfn-appsync-graphqlapi-enhancedmetricsconfig-datasourcelevelmetricsbehavior
            '''
            result = self._values.get("data_source_level_metrics_behavior")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operation_level_metrics_config(self) -> typing.Optional[builtins.str]:
            '''Controls how operation metrics will be emitted to CloudWatch. Operation metrics include:.

            - *Requests* : The number of times a specified GraphQL operation was called.
            - *GraphQL errors* : The number of GraphQL errors that occurred during a specified GraphQL operation.

            Metrics will be recorded by API ID and operation name. You can set the value to ``ENABLED`` or ``DISABLED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-enhancedmetricsconfig.html#cfn-appsync-graphqlapi-enhancedmetricsconfig-operationlevelmetricsconfig
            '''
            result = self._values.get("operation_level_metrics_config")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resolver_level_metrics_behavior(self) -> typing.Optional[builtins.str]:
            '''Controls how resolver metrics will be emitted to CloudWatch. Resolver metrics include:.

            - *GraphQL errors* : The number of GraphQL errors that occurred.
            - *Requests* : The number of invocations that occurred during a request.
            - *Latency* : The time to complete a resolver invocation.
            - *Cache hits* : The number of cache hits during a request.
            - *Cache misses* : The number of cache misses during a request.

            These metrics can be emitted to CloudWatch per resolver or for all resolvers in the request. Metrics will be recorded by API ID and resolver name. ``resolverLevelMetricsBehavior`` accepts one of these values at a time:

            - ``FULL_REQUEST_RESOLVER_METRICS`` : Records and emits metric data for all resolvers in the request.
            - ``PER_RESOLVER_METRICS`` : Records and emits metric data for resolvers that have the ``MetricsConfig`` value set to ``ENABLED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-enhancedmetricsconfig.html#cfn-appsync-graphqlapi-enhancedmetricsconfig-resolverlevelmetricsbehavior
            '''
            result = self._values.get("resolver_level_metrics_behavior")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnhancedMetricsConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnGraphQLApiPropsMixin.LambdaAuthorizerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorizer_result_ttl_in_seconds": "authorizerResultTtlInSeconds",
            "authorizer_uri": "authorizerUri",
            "identity_validation_expression": "identityValidationExpression",
        },
    )
    class LambdaAuthorizerConfigProperty:
        def __init__(
            self,
            *,
            authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number] = None,
            authorizer_uri: typing.Optional[builtins.str] = None,
            identity_validation_expression: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration for AWS Lambda function authorization.

            :param authorizer_result_ttl_in_seconds: The number of seconds a response should be cached for. The default is 0 seconds, which disables caching. If you don't specify a value for ``authorizerResultTtlInSeconds`` , the default value is used. The maximum value is one hour (3600 seconds). The Lambda function can override this by returning a ``ttlOverride`` key in its response.
            :param authorizer_uri: The ARN of the Lambda function to be called for authorization. This may be a standard Lambda ARN, a version ARN ( ``.../v3`` ) or alias ARN. *Note* : This Lambda function must have the following resource-based policy assigned to it. When configuring Lambda authorizers in the console, this is done for you. To do so with the AWS CLI , run the following: ``aws lambda add-permission --function-name "arn:aws:lambda:us-east-2:111122223333:function:my-function" --statement-id "appsync" --principal appsync.amazonaws.com --action lambda:InvokeFunction``
            :param identity_validation_expression: A regular expression for validation of tokens before the Lambda function is called.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-lambdaauthorizerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                lambda_authorizer_config_property = appsync_mixins.CfnGraphQLApiPropsMixin.LambdaAuthorizerConfigProperty(
                    authorizer_result_ttl_in_seconds=123,
                    authorizer_uri="authorizerUri",
                    identity_validation_expression="identityValidationExpression"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__613b5142a9a568947bd5b6ca570eb4d5360d45f460d7fa7ada1885b49e67dc5a)
                check_type(argname="argument authorizer_result_ttl_in_seconds", value=authorizer_result_ttl_in_seconds, expected_type=type_hints["authorizer_result_ttl_in_seconds"])
                check_type(argname="argument authorizer_uri", value=authorizer_uri, expected_type=type_hints["authorizer_uri"])
                check_type(argname="argument identity_validation_expression", value=identity_validation_expression, expected_type=type_hints["identity_validation_expression"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authorizer_result_ttl_in_seconds is not None:
                self._values["authorizer_result_ttl_in_seconds"] = authorizer_result_ttl_in_seconds
            if authorizer_uri is not None:
                self._values["authorizer_uri"] = authorizer_uri
            if identity_validation_expression is not None:
                self._values["identity_validation_expression"] = identity_validation_expression

        @builtins.property
        def authorizer_result_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The number of seconds a response should be cached for.

            The default is 0 seconds, which disables caching. If you don't specify a value for ``authorizerResultTtlInSeconds`` , the default value is used. The maximum value is one hour (3600 seconds). The Lambda function can override this by returning a ``ttlOverride`` key in its response.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-lambdaauthorizerconfig.html#cfn-appsync-graphqlapi-lambdaauthorizerconfig-authorizerresultttlinseconds
            '''
            result = self._values.get("authorizer_result_ttl_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def authorizer_uri(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Lambda function to be called for authorization.

            This may be a standard Lambda ARN, a version ARN ( ``.../v3`` ) or alias ARN.

            *Note* : This Lambda function must have the following resource-based policy assigned to it. When configuring Lambda authorizers in the console, this is done for you. To do so with the AWS CLI , run the following:

            ``aws lambda add-permission --function-name "arn:aws:lambda:us-east-2:111122223333:function:my-function" --statement-id "appsync" --principal appsync.amazonaws.com --action lambda:InvokeFunction``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-lambdaauthorizerconfig.html#cfn-appsync-graphqlapi-lambdaauthorizerconfig-authorizeruri
            '''
            result = self._values.get("authorizer_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def identity_validation_expression(self) -> typing.Optional[builtins.str]:
            '''A regular expression for validation of tokens before the Lambda function is called.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-lambdaauthorizerconfig.html#cfn-appsync-graphqlapi-lambdaauthorizerconfig-identityvalidationexpression
            '''
            result = self._values.get("identity_validation_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaAuthorizerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnGraphQLApiPropsMixin.LogConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_logs_role_arn": "cloudWatchLogsRoleArn",
            "exclude_verbose_content": "excludeVerboseContent",
            "field_log_level": "fieldLogLevel",
        },
    )
    class LogConfigProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs_role_arn: typing.Optional[builtins.str] = None,
            exclude_verbose_content: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            field_log_level: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``LogConfig`` property type specifies the logging configuration when writing GraphQL operations and tracing to Amazon CloudWatch for an AWS AppSync GraphQL API.

            ``LogConfig`` is a property of the `AWS::AppSync::GraphQLApi <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html>`_ property type.

            :param cloud_watch_logs_role_arn: The service role that AWS AppSync will assume to publish to Amazon CloudWatch Logs in your account.
            :param exclude_verbose_content: Set to TRUE to exclude sections that contain information such as headers, context, and evaluated mapping templates, regardless of logging level.
            :param field_log_level: The field logging level. Values can be NONE, ERROR, INFO, DEBUG, or ALL. - *NONE* : No field-level logs are captured. - *ERROR* : Logs the following information *only* for the fields that are in the error category: - The error section in the server response. - Field-level errors. - The generated request/response functions that got resolved for error fields. - *INFO* : Logs the following information *only* for the fields that are in the info and error categories: - Info-level messages. - The user messages sent through ``$util.log.info`` and ``console.log`` . - Field-level tracing and mapping logs are not shown. - *DEBUG* : Logs the following information *only* for the fields that are in the debug, info, and error categories: - Debug-level messages. - The user messages sent through ``$util.log.info`` , ``$util.log.debug`` , ``console.log`` , and ``console.debug`` . - Field-level tracing and mapping logs are not shown. - *ALL* : The following information is logged for all fields in the query: - Field-level tracing information. - The generated request/response functions that were resolved for each field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-logconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                log_config_property = appsync_mixins.CfnGraphQLApiPropsMixin.LogConfigProperty(
                    cloud_watch_logs_role_arn="cloudWatchLogsRoleArn",
                    exclude_verbose_content=False,
                    field_log_level="fieldLogLevel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cb13b8bb1367c19757403113fba81ff67a27e867bce1fb7ebf1a5ca84354ba9d)
                check_type(argname="argument cloud_watch_logs_role_arn", value=cloud_watch_logs_role_arn, expected_type=type_hints["cloud_watch_logs_role_arn"])
                check_type(argname="argument exclude_verbose_content", value=exclude_verbose_content, expected_type=type_hints["exclude_verbose_content"])
                check_type(argname="argument field_log_level", value=field_log_level, expected_type=type_hints["field_log_level"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logs_role_arn is not None:
                self._values["cloud_watch_logs_role_arn"] = cloud_watch_logs_role_arn
            if exclude_verbose_content is not None:
                self._values["exclude_verbose_content"] = exclude_verbose_content
            if field_log_level is not None:
                self._values["field_log_level"] = field_log_level

        @builtins.property
        def cloud_watch_logs_role_arn(self) -> typing.Optional[builtins.str]:
            '''The service role that AWS AppSync will assume to publish to Amazon CloudWatch Logs in your account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-logconfig.html#cfn-appsync-graphqlapi-logconfig-cloudwatchlogsrolearn
            '''
            result = self._values.get("cloud_watch_logs_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def exclude_verbose_content(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set to TRUE to exclude sections that contain information such as headers, context, and evaluated mapping templates, regardless of logging level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-logconfig.html#cfn-appsync-graphqlapi-logconfig-excludeverbosecontent
            '''
            result = self._values.get("exclude_verbose_content")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def field_log_level(self) -> typing.Optional[builtins.str]:
            '''The field logging level. Values can be NONE, ERROR, INFO, DEBUG, or ALL.

            - *NONE* : No field-level logs are captured.
            - *ERROR* : Logs the following information *only* for the fields that are in the error category:
            - The error section in the server response.
            - Field-level errors.
            - The generated request/response functions that got resolved for error fields.
            - *INFO* : Logs the following information *only* for the fields that are in the info and error categories:
            - Info-level messages.
            - The user messages sent through ``$util.log.info`` and ``console.log`` .
            - Field-level tracing and mapping logs are not shown.
            - *DEBUG* : Logs the following information *only* for the fields that are in the debug, info, and error categories:
            - Debug-level messages.
            - The user messages sent through ``$util.log.info`` , ``$util.log.debug`` , ``console.log`` , and ``console.debug`` .
            - Field-level tracing and mapping logs are not shown.
            - *ALL* : The following information is logged for all fields in the query:
            - Field-level tracing information.
            - The generated request/response functions that were resolved for each field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-logconfig.html#cfn-appsync-graphqlapi-logconfig-fieldloglevel
            '''
            result = self._values.get("field_log_level")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnGraphQLApiPropsMixin.OpenIDConnectConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auth_ttl": "authTtl",
            "client_id": "clientId",
            "iat_ttl": "iatTtl",
            "issuer": "issuer",
        },
    )
    class OpenIDConnectConfigProperty:
        def __init__(
            self,
            *,
            auth_ttl: typing.Optional[jsii.Number] = None,
            client_id: typing.Optional[builtins.str] = None,
            iat_ttl: typing.Optional[jsii.Number] = None,
            issuer: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``OpenIDConnectConfig`` property type specifies the optional authorization configuration for using an OpenID Connect compliant service with your GraphQL endpoint for an AWS AppSync GraphQL API.

            ``OpenIDConnectConfig`` is a property of the `AWS::AppSync::GraphQLApi <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html>`_ property type.

            :param auth_ttl: The number of milliseconds that a token is valid after being authenticated.
            :param client_id: The client identifier of the Relying party at the OpenID identity provider. This identifier is typically obtained when the Relying party is registered with the OpenID identity provider. You can specify a regular expression so that AWS AppSync can validate against multiple client identifiers at a time.
            :param iat_ttl: The number of milliseconds that a token is valid after it's issued to a user.
            :param issuer: The issuer for the OIDC configuration. The issuer returned by discovery must exactly match the value of ``iss`` in the ID token.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-openidconnectconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                open_iDConnect_config_property = appsync_mixins.CfnGraphQLApiPropsMixin.OpenIDConnectConfigProperty(
                    auth_ttl=123,
                    client_id="clientId",
                    iat_ttl=123,
                    issuer="issuer"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4718eae6502088b81017fdd1131b4f41d6811fb9e6ac0f17d2112f4144c876d0)
                check_type(argname="argument auth_ttl", value=auth_ttl, expected_type=type_hints["auth_ttl"])
                check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
                check_type(argname="argument iat_ttl", value=iat_ttl, expected_type=type_hints["iat_ttl"])
                check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auth_ttl is not None:
                self._values["auth_ttl"] = auth_ttl
            if client_id is not None:
                self._values["client_id"] = client_id
            if iat_ttl is not None:
                self._values["iat_ttl"] = iat_ttl
            if issuer is not None:
                self._values["issuer"] = issuer

        @builtins.property
        def auth_ttl(self) -> typing.Optional[jsii.Number]:
            '''The number of milliseconds that a token is valid after being authenticated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-openidconnectconfig.html#cfn-appsync-graphqlapi-openidconnectconfig-authttl
            '''
            result = self._values.get("auth_ttl")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def client_id(self) -> typing.Optional[builtins.str]:
            '''The client identifier of the Relying party at the OpenID identity provider.

            This identifier is typically obtained when the Relying party is registered with the OpenID identity provider. You can specify a regular expression so that AWS AppSync can validate against multiple client identifiers at a time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-openidconnectconfig.html#cfn-appsync-graphqlapi-openidconnectconfig-clientid
            '''
            result = self._values.get("client_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def iat_ttl(self) -> typing.Optional[jsii.Number]:
            '''The number of milliseconds that a token is valid after it's issued to a user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-openidconnectconfig.html#cfn-appsync-graphqlapi-openidconnectconfig-iatttl
            '''
            result = self._values.get("iat_ttl")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def issuer(self) -> typing.Optional[builtins.str]:
            '''The issuer for the OIDC configuration.

            The issuer returned by discovery must exactly match the value of ``iss`` in the ID token.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-openidconnectconfig.html#cfn-appsync-graphqlapi-openidconnectconfig-issuer
            '''
            result = self._values.get("issuer")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OpenIDConnectConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnGraphQLApiPropsMixin.UserPoolConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "app_id_client_regex": "appIdClientRegex",
            "aws_region": "awsRegion",
            "default_action": "defaultAction",
            "user_pool_id": "userPoolId",
        },
    )
    class UserPoolConfigProperty:
        def __init__(
            self,
            *,
            app_id_client_regex: typing.Optional[builtins.str] = None,
            aws_region: typing.Optional[builtins.str] = None,
            default_action: typing.Optional[builtins.str] = None,
            user_pool_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``UserPoolConfig`` property type specifies the optional authorization configuration for using Amazon Cognito user pools with your GraphQL endpoint for an AWS AppSync GraphQL API.

            :param app_id_client_regex: A regular expression for validating the incoming Amazon Cognito user pool app client ID. If this value isn't set, no filtering is applied.
            :param aws_region: The AWS Region in which the user pool was created.
            :param default_action: The action that you want your GraphQL API to take when a request that uses Amazon Cognito user pool authentication doesn't match the Amazon Cognito user pool configuration. When specifying Amazon Cognito user pools as the default authentication, you must set the value for ``DefaultAction`` to ``ALLOW`` if specifying ``AdditionalAuthenticationProviders`` .
            :param user_pool_id: The user pool ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-userpoolconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                user_pool_config_property = appsync_mixins.CfnGraphQLApiPropsMixin.UserPoolConfigProperty(
                    app_id_client_regex="appIdClientRegex",
                    aws_region="awsRegion",
                    default_action="defaultAction",
                    user_pool_id="userPoolId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4f08c4e593bfaa8394ed8468a44bd9a84ceb022a706708a8599cd4c2aa66b102)
                check_type(argname="argument app_id_client_regex", value=app_id_client_regex, expected_type=type_hints["app_id_client_regex"])
                check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                check_type(argname="argument default_action", value=default_action, expected_type=type_hints["default_action"])
                check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if app_id_client_regex is not None:
                self._values["app_id_client_regex"] = app_id_client_regex
            if aws_region is not None:
                self._values["aws_region"] = aws_region
            if default_action is not None:
                self._values["default_action"] = default_action
            if user_pool_id is not None:
                self._values["user_pool_id"] = user_pool_id

        @builtins.property
        def app_id_client_regex(self) -> typing.Optional[builtins.str]:
            '''A regular expression for validating the incoming Amazon Cognito user pool app client ID.

            If this value isn't set, no filtering is applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-userpoolconfig.html#cfn-appsync-graphqlapi-userpoolconfig-appidclientregex
            '''
            result = self._values.get("app_id_client_regex")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def aws_region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region in which the user pool was created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-userpoolconfig.html#cfn-appsync-graphqlapi-userpoolconfig-awsregion
            '''
            result = self._values.get("aws_region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def default_action(self) -> typing.Optional[builtins.str]:
            '''The action that you want your GraphQL API to take when a request that uses Amazon Cognito user pool authentication doesn't match the Amazon Cognito user pool configuration.

            When specifying Amazon Cognito user pools as the default authentication, you must set the value for ``DefaultAction`` to ``ALLOW`` if specifying ``AdditionalAuthenticationProviders`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-userpoolconfig.html#cfn-appsync-graphqlapi-userpoolconfig-defaultaction
            '''
            result = self._values.get("default_action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_pool_id(self) -> typing.Optional[builtins.str]:
            '''The user pool ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-userpoolconfig.html#cfn-appsync-graphqlapi-userpoolconfig-userpoolid
            '''
            result = self._values.get("user_pool_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserPoolConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnGraphQLSchemaMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "definition": "definition",
        "definition_s3_location": "definitionS3Location",
    },
)
class CfnGraphQLSchemaMixinProps:
    def __init__(
        self,
        *,
        api_id: typing.Optional[builtins.str] = None,
        definition: typing.Optional[builtins.str] = None,
        definition_s3_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnGraphQLSchemaPropsMixin.

        :param api_id: The AWS AppSync GraphQL API identifier to which you want to apply this schema.
        :param definition: The text representation of a GraphQL schema in SDL format. For more information about using the ``Ref`` function, see `Ref <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref>`_ .
        :param definition_s3_location: The location of a GraphQL schema file in an Amazon S3 bucket. Use this if you want to provision with the schema living in Amazon S3 rather than embedding it in your CloudFormation template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlschema.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
            
            cfn_graph_qLSchema_mixin_props = appsync_mixins.CfnGraphQLSchemaMixinProps(
                api_id="apiId",
                definition="definition",
                definition_s3_location="definitionS3Location"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__921887fdef89fe6d44425d1239157b3f69f273125b77a5a99cdd1b99045ba26c)
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument definition_s3_location", value=definition_s3_location, expected_type=type_hints["definition_s3_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_id is not None:
            self._values["api_id"] = api_id
        if definition is not None:
            self._values["definition"] = definition
        if definition_s3_location is not None:
            self._values["definition_s3_location"] = definition_s3_location

    @builtins.property
    def api_id(self) -> typing.Optional[builtins.str]:
        '''The AWS AppSync GraphQL API identifier to which you want to apply this schema.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlschema.html#cfn-appsync-graphqlschema-apiid
        '''
        result = self._values.get("api_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def definition(self) -> typing.Optional[builtins.str]:
        '''The text representation of a GraphQL schema in SDL format.

        For more information about using the ``Ref`` function, see `Ref <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlschema.html#cfn-appsync-graphqlschema-definition
        '''
        result = self._values.get("definition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def definition_s3_location(self) -> typing.Optional[builtins.str]:
        '''The location of a GraphQL schema file in an Amazon S3 bucket.

        Use this if you want to provision with the schema living in Amazon S3 rather than embedding it in your CloudFormation template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlschema.html#cfn-appsync-graphqlschema-definitions3location
        '''
        result = self._values.get("definition_s3_location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGraphQLSchemaMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGraphQLSchemaPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnGraphQLSchemaPropsMixin",
):
    '''The ``AWS::AppSync::GraphQLSchema`` resource is used for your AWS AppSync GraphQL schema that controls the data model for your API.

    Schema files are text written in Schema Definition Language (SDL) format. For more information about schema authoring, see `Designing a GraphQL API <https://docs.aws.amazon.com/appsync/latest/devguide/designing-a-graphql-api.html>`_ in the *AWS AppSync Developer Guide* .
    .. epigraph::

       When you submit an update, AWS CloudFormation updates resources based on differences between what you submit and the stack's current template. To cause this resource to be updated you must change a property value for this resource in the CloudFormation template. Changing the Amazon S3 file content without changing a property value will not result in an update operation.

       See `Update Behaviors of Stack Resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html>`_ in the *AWS CloudFormation User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlschema.html
    :cloudformationResource: AWS::AppSync::GraphQLSchema
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
        
        cfn_graph_qLSchema_props_mixin = appsync_mixins.CfnGraphQLSchemaPropsMixin(appsync_mixins.CfnGraphQLSchemaMixinProps(
            api_id="apiId",
            definition="definition",
            definition_s3_location="definitionS3Location"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnGraphQLSchemaMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppSync::GraphQLSchema``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f89db116e3b849cd21a713d4c25dfde73390325e5de0862e138a4a7000a55552)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c5730822e8789ee2a10e6bc02bcc1dbc2b87b011fe68d218598303836935af0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff8bc5277ee1776212cd3d293d625db8a87b48113355b541504088fd2f4785a6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGraphQLSchemaMixinProps:
        return typing.cast(CfnGraphQLSchemaMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnResolverMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "caching_config": "cachingConfig",
        "code": "code",
        "code_s3_location": "codeS3Location",
        "data_source_name": "dataSourceName",
        "field_name": "fieldName",
        "kind": "kind",
        "max_batch_size": "maxBatchSize",
        "metrics_config": "metricsConfig",
        "pipeline_config": "pipelineConfig",
        "request_mapping_template": "requestMappingTemplate",
        "request_mapping_template_s3_location": "requestMappingTemplateS3Location",
        "response_mapping_template": "responseMappingTemplate",
        "response_mapping_template_s3_location": "responseMappingTemplateS3Location",
        "runtime": "runtime",
        "sync_config": "syncConfig",
        "type_name": "typeName",
    },
)
class CfnResolverMixinProps:
    def __init__(
        self,
        *,
        api_id: typing.Optional[builtins.str] = None,
        caching_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResolverPropsMixin.CachingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        code: typing.Optional[builtins.str] = None,
        code_s3_location: typing.Optional[builtins.str] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        field_name: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
        max_batch_size: typing.Optional[jsii.Number] = None,
        metrics_config: typing.Optional[builtins.str] = None,
        pipeline_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResolverPropsMixin.PipelineConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        request_mapping_template: typing.Optional[builtins.str] = None,
        request_mapping_template_s3_location: typing.Optional[builtins.str] = None,
        response_mapping_template: typing.Optional[builtins.str] = None,
        response_mapping_template_s3_location: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResolverPropsMixin.AppSyncRuntimeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sync_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResolverPropsMixin.SyncConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        type_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnResolverPropsMixin.

        :param api_id: The AWS AppSync GraphQL API to which you want to attach this resolver.
        :param caching_config: The caching configuration for the resolver.
        :param code: The ``resolver`` code that contains the request and response functions. When code is used, the ``runtime`` is required. The runtime value must be ``APPSYNC_JS`` .
        :param code_s3_location: The Amazon S3 endpoint.
        :param data_source_name: The resolver data source name.
        :param field_name: The GraphQL field on a type that invokes the resolver.
        :param kind: The resolver type. - *UNIT* : A UNIT resolver type. A UNIT resolver is the default resolver type. You can use a UNIT resolver to run a GraphQL query against a single data source. - *PIPELINE* : A PIPELINE resolver type. You can use a PIPELINE resolver to invoke a series of ``Function`` objects in a serial manner. You can use a pipeline resolver to run a GraphQL query against multiple data sources.
        :param max_batch_size: The maximum number of resolver request inputs that will be sent to a single AWS Lambda function in a ``BatchInvoke`` operation.
        :param metrics_config: Enables or disables enhanced resolver metrics for specified resolvers. Note that ``MetricsConfig`` won't be used unless the ``resolverLevelMetricsBehavior`` value is set to ``PER_RESOLVER_METRICS`` . If the ``resolverLevelMetricsBehavior`` is set to ``FULL_REQUEST_RESOLVER_METRICS`` instead, ``MetricsConfig`` will be ignored. However, you can still set its value.
        :param pipeline_config: Functions linked with the pipeline resolver.
        :param request_mapping_template: The request mapping template. Request mapping templates are optional when using a Lambda data source. For all other data sources, a request mapping template is required.
        :param request_mapping_template_s3_location: The location of a request mapping template in an Amazon S3 bucket. Use this if you want to provision with a template file in Amazon S3 rather than embedding it in your CloudFormation template.
        :param response_mapping_template: The response mapping template.
        :param response_mapping_template_s3_location: The location of a response mapping template in an Amazon S3 bucket. Use this if you want to provision with a template file in Amazon S3 rather than embedding it in your CloudFormation template.
        :param runtime: Describes a runtime used by an AWS AppSync resolver or AWS AppSync function. Specifies the name and version of the runtime to use. Note that if a runtime is specified, code must also be specified.
        :param sync_config: The ``SyncConfig`` for a resolver attached to a versioned data source.
        :param type_name: The GraphQL type that invokes this resolver.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
            
            cfn_resolver_mixin_props = appsync_mixins.CfnResolverMixinProps(
                api_id="apiId",
                caching_config=appsync_mixins.CfnResolverPropsMixin.CachingConfigProperty(
                    caching_keys=["cachingKeys"],
                    ttl=123
                ),
                code="code",
                code_s3_location="codeS3Location",
                data_source_name="dataSourceName",
                field_name="fieldName",
                kind="kind",
                max_batch_size=123,
                metrics_config="metricsConfig",
                pipeline_config=appsync_mixins.CfnResolverPropsMixin.PipelineConfigProperty(
                    functions=["functions"]
                ),
                request_mapping_template="requestMappingTemplate",
                request_mapping_template_s3_location="requestMappingTemplateS3Location",
                response_mapping_template="responseMappingTemplate",
                response_mapping_template_s3_location="responseMappingTemplateS3Location",
                runtime=appsync_mixins.CfnResolverPropsMixin.AppSyncRuntimeProperty(
                    name="name",
                    runtime_version="runtimeVersion"
                ),
                sync_config=appsync_mixins.CfnResolverPropsMixin.SyncConfigProperty(
                    conflict_detection="conflictDetection",
                    conflict_handler="conflictHandler",
                    lambda_conflict_handler_config=appsync_mixins.CfnResolverPropsMixin.LambdaConflictHandlerConfigProperty(
                        lambda_conflict_handler_arn="lambdaConflictHandlerArn"
                    )
                ),
                type_name="typeName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__777073e0d9ce9df56d1d93c5e72fdd76151ecd0245c6ea5ae8d574845b5a0ece)
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument caching_config", value=caching_config, expected_type=type_hints["caching_config"])
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument code_s3_location", value=code_s3_location, expected_type=type_hints["code_s3_location"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            check_type(argname="argument max_batch_size", value=max_batch_size, expected_type=type_hints["max_batch_size"])
            check_type(argname="argument metrics_config", value=metrics_config, expected_type=type_hints["metrics_config"])
            check_type(argname="argument pipeline_config", value=pipeline_config, expected_type=type_hints["pipeline_config"])
            check_type(argname="argument request_mapping_template", value=request_mapping_template, expected_type=type_hints["request_mapping_template"])
            check_type(argname="argument request_mapping_template_s3_location", value=request_mapping_template_s3_location, expected_type=type_hints["request_mapping_template_s3_location"])
            check_type(argname="argument response_mapping_template", value=response_mapping_template, expected_type=type_hints["response_mapping_template"])
            check_type(argname="argument response_mapping_template_s3_location", value=response_mapping_template_s3_location, expected_type=type_hints["response_mapping_template_s3_location"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument sync_config", value=sync_config, expected_type=type_hints["sync_config"])
            check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_id is not None:
            self._values["api_id"] = api_id
        if caching_config is not None:
            self._values["caching_config"] = caching_config
        if code is not None:
            self._values["code"] = code
        if code_s3_location is not None:
            self._values["code_s3_location"] = code_s3_location
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if field_name is not None:
            self._values["field_name"] = field_name
        if kind is not None:
            self._values["kind"] = kind
        if max_batch_size is not None:
            self._values["max_batch_size"] = max_batch_size
        if metrics_config is not None:
            self._values["metrics_config"] = metrics_config
        if pipeline_config is not None:
            self._values["pipeline_config"] = pipeline_config
        if request_mapping_template is not None:
            self._values["request_mapping_template"] = request_mapping_template
        if request_mapping_template_s3_location is not None:
            self._values["request_mapping_template_s3_location"] = request_mapping_template_s3_location
        if response_mapping_template is not None:
            self._values["response_mapping_template"] = response_mapping_template
        if response_mapping_template_s3_location is not None:
            self._values["response_mapping_template_s3_location"] = response_mapping_template_s3_location
        if runtime is not None:
            self._values["runtime"] = runtime
        if sync_config is not None:
            self._values["sync_config"] = sync_config
        if type_name is not None:
            self._values["type_name"] = type_name

    @builtins.property
    def api_id(self) -> typing.Optional[builtins.str]:
        '''The AWS AppSync GraphQL API to which you want to attach this resolver.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-apiid
        '''
        result = self._values.get("api_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def caching_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResolverPropsMixin.CachingConfigProperty"]]:
        '''The caching configuration for the resolver.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-cachingconfig
        '''
        result = self._values.get("caching_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResolverPropsMixin.CachingConfigProperty"]], result)

    @builtins.property
    def code(self) -> typing.Optional[builtins.str]:
        '''The ``resolver`` code that contains the request and response functions.

        When code is used, the ``runtime`` is required. The runtime value must be ``APPSYNC_JS`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-code
        '''
        result = self._values.get("code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_s3_location(self) -> typing.Optional[builtins.str]:
        '''The Amazon S3 endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-codes3location
        '''
        result = self._values.get("code_s3_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''The resolver data source name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-datasourcename
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def field_name(self) -> typing.Optional[builtins.str]:
        '''The GraphQL field on a type that invokes the resolver.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-fieldname
        '''
        result = self._values.get("field_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kind(self) -> typing.Optional[builtins.str]:
        '''The resolver type.

        - *UNIT* : A UNIT resolver type. A UNIT resolver is the default resolver type. You can use a UNIT resolver to run a GraphQL query against a single data source.
        - *PIPELINE* : A PIPELINE resolver type. You can use a PIPELINE resolver to invoke a series of ``Function`` objects in a serial manner. You can use a pipeline resolver to run a GraphQL query against multiple data sources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-kind
        '''
        result = self._values.get("kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_batch_size(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of resolver request inputs that will be sent to a single AWS Lambda function in a ``BatchInvoke`` operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-maxbatchsize
        '''
        result = self._values.get("max_batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metrics_config(self) -> typing.Optional[builtins.str]:
        '''Enables or disables enhanced resolver metrics for specified resolvers.

        Note that ``MetricsConfig`` won't be used unless the ``resolverLevelMetricsBehavior`` value is set to ``PER_RESOLVER_METRICS`` . If the ``resolverLevelMetricsBehavior`` is set to ``FULL_REQUEST_RESOLVER_METRICS`` instead, ``MetricsConfig`` will be ignored. However, you can still set its value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-metricsconfig
        '''
        result = self._values.get("metrics_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pipeline_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResolverPropsMixin.PipelineConfigProperty"]]:
        '''Functions linked with the pipeline resolver.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-pipelineconfig
        '''
        result = self._values.get("pipeline_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResolverPropsMixin.PipelineConfigProperty"]], result)

    @builtins.property
    def request_mapping_template(self) -> typing.Optional[builtins.str]:
        '''The request mapping template.

        Request mapping templates are optional when using a Lambda data source. For all other data sources, a request mapping template is required.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-requestmappingtemplate
        '''
        result = self._values.get("request_mapping_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_mapping_template_s3_location(self) -> typing.Optional[builtins.str]:
        '''The location of a request mapping template in an Amazon S3 bucket.

        Use this if you want to provision with a template file in Amazon S3 rather than embedding it in your CloudFormation template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-requestmappingtemplates3location
        '''
        result = self._values.get("request_mapping_template_s3_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_mapping_template(self) -> typing.Optional[builtins.str]:
        '''The response mapping template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-responsemappingtemplate
        '''
        result = self._values.get("response_mapping_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_mapping_template_s3_location(self) -> typing.Optional[builtins.str]:
        '''The location of a response mapping template in an Amazon S3 bucket.

        Use this if you want to provision with a template file in Amazon S3 rather than embedding it in your CloudFormation template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-responsemappingtemplates3location
        '''
        result = self._values.get("response_mapping_template_s3_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResolverPropsMixin.AppSyncRuntimeProperty"]]:
        '''Describes a runtime used by an AWS AppSync resolver or AWS AppSync function.

        Specifies the name and version of the runtime to use. Note that if a runtime is specified, code must also be specified.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-runtime
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResolverPropsMixin.AppSyncRuntimeProperty"]], result)

    @builtins.property
    def sync_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResolverPropsMixin.SyncConfigProperty"]]:
        '''The ``SyncConfig`` for a resolver attached to a versioned data source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-syncconfig
        '''
        result = self._values.get("sync_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResolverPropsMixin.SyncConfigProperty"]], result)

    @builtins.property
    def type_name(self) -> typing.Optional[builtins.str]:
        '''The GraphQL type that invokes this resolver.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-typename
        '''
        result = self._values.get("type_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResolverMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResolverPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnResolverPropsMixin",
):
    '''The ``AWS::AppSync::Resolver`` resource defines the logical GraphQL resolver that you attach to fields in a schema.

    Request and response templates for resolvers are written in Apache Velocity Template Language (VTL) format. For more information about resolvers, see `Resolver Mapping Template Reference <https://docs.aws.amazon.com/appsync/latest/devguide/resolver-mapping-template-reference.html>`_ .
    .. epigraph::

       When you submit an update, AWS CloudFormation updates resources based on differences between what you submit and the stack's current template. To cause this resource to be updated you must change a property value for this resource in the CloudFormation template. Changing the Amazon S3 file content without changing a property value will not result in an update operation.

       See `Update Behaviors of Stack Resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html>`_ in the *AWS CloudFormation User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html
    :cloudformationResource: AWS::AppSync::Resolver
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
        
        cfn_resolver_props_mixin = appsync_mixins.CfnResolverPropsMixin(appsync_mixins.CfnResolverMixinProps(
            api_id="apiId",
            caching_config=appsync_mixins.CfnResolverPropsMixin.CachingConfigProperty(
                caching_keys=["cachingKeys"],
                ttl=123
            ),
            code="code",
            code_s3_location="codeS3Location",
            data_source_name="dataSourceName",
            field_name="fieldName",
            kind="kind",
            max_batch_size=123,
            metrics_config="metricsConfig",
            pipeline_config=appsync_mixins.CfnResolverPropsMixin.PipelineConfigProperty(
                functions=["functions"]
            ),
            request_mapping_template="requestMappingTemplate",
            request_mapping_template_s3_location="requestMappingTemplateS3Location",
            response_mapping_template="responseMappingTemplate",
            response_mapping_template_s3_location="responseMappingTemplateS3Location",
            runtime=appsync_mixins.CfnResolverPropsMixin.AppSyncRuntimeProperty(
                name="name",
                runtime_version="runtimeVersion"
            ),
            sync_config=appsync_mixins.CfnResolverPropsMixin.SyncConfigProperty(
                conflict_detection="conflictDetection",
                conflict_handler="conflictHandler",
                lambda_conflict_handler_config=appsync_mixins.CfnResolverPropsMixin.LambdaConflictHandlerConfigProperty(
                    lambda_conflict_handler_arn="lambdaConflictHandlerArn"
                )
            ),
            type_name="typeName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResolverMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppSync::Resolver``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25460e1b0068588a0c38af310d214fefa978d87ccea457395fce22fa7276a289)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1ef66861349dfb40733b9fa3d40db432711955c962027794b6b4de7cfea22a1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07943520e0e55b260594c7f1649a5408409172b0f881411a8c53e0f4a9f1fc42)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResolverMixinProps:
        return typing.cast(CfnResolverMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnResolverPropsMixin.AppSyncRuntimeProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "runtime_version": "runtimeVersion"},
    )
    class AppSyncRuntimeProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            runtime_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a runtime used by an AWS AppSync resolver or AWS AppSync function.

            Specifies the name and version of the runtime to use. Note that if a runtime is specified, code must also be specified.

            :param name: The ``name`` of the runtime to use. Currently, the only allowed value is ``APPSYNC_JS`` .
            :param runtime_version: The ``version`` of the runtime to use. Currently, the only allowed version is ``1.0.0`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-appsyncruntime.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                app_sync_runtime_property = appsync_mixins.CfnResolverPropsMixin.AppSyncRuntimeProperty(
                    name="name",
                    runtime_version="runtimeVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1867033c1c86b3a2b723f7599c5d5679a5c237c7b5b2a33f594ee92156e53784)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument runtime_version", value=runtime_version, expected_type=type_hints["runtime_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if runtime_version is not None:
                self._values["runtime_version"] = runtime_version

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The ``name`` of the runtime to use.

            Currently, the only allowed value is ``APPSYNC_JS`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-appsyncruntime.html#cfn-appsync-resolver-appsyncruntime-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def runtime_version(self) -> typing.Optional[builtins.str]:
            '''The ``version`` of the runtime to use.

            Currently, the only allowed version is ``1.0.0`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-appsyncruntime.html#cfn-appsync-resolver-appsyncruntime-runtimeversion
            '''
            result = self._values.get("runtime_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AppSyncRuntimeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnResolverPropsMixin.CachingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"caching_keys": "cachingKeys", "ttl": "ttl"},
    )
    class CachingConfigProperty:
        def __init__(
            self,
            *,
            caching_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
            ttl: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The caching configuration for a resolver that has caching activated.

            :param caching_keys: The caching keys for a resolver that has caching activated. Valid values are entries from the ``$context.arguments`` , ``$context.source`` , and ``$context.identity`` maps.
            :param ttl: The TTL in seconds for a resolver that has caching activated. Valid values are 1–3,600 seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-cachingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                caching_config_property = appsync_mixins.CfnResolverPropsMixin.CachingConfigProperty(
                    caching_keys=["cachingKeys"],
                    ttl=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__11250d093794e3c12e36ae8ecf9afcda3f570bc81511b75116fa0ffd028ca14e)
                check_type(argname="argument caching_keys", value=caching_keys, expected_type=type_hints["caching_keys"])
                check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if caching_keys is not None:
                self._values["caching_keys"] = caching_keys
            if ttl is not None:
                self._values["ttl"] = ttl

        @builtins.property
        def caching_keys(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The caching keys for a resolver that has caching activated.

            Valid values are entries from the ``$context.arguments`` , ``$context.source`` , and ``$context.identity`` maps.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-cachingconfig.html#cfn-appsync-resolver-cachingconfig-cachingkeys
            '''
            result = self._values.get("caching_keys")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def ttl(self) -> typing.Optional[jsii.Number]:
            '''The TTL in seconds for a resolver that has caching activated.

            Valid values are 1–3,600 seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-cachingconfig.html#cfn-appsync-resolver-cachingconfig-ttl
            '''
            result = self._values.get("ttl")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CachingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnResolverPropsMixin.LambdaConflictHandlerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"lambda_conflict_handler_arn": "lambdaConflictHandlerArn"},
    )
    class LambdaConflictHandlerConfigProperty:
        def __init__(
            self,
            *,
            lambda_conflict_handler_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

            :param lambda_conflict_handler_arn: The Amazon Resource Name (ARN) for the Lambda function to use as the Conflict Handler.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-lambdaconflicthandlerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                lambda_conflict_handler_config_property = appsync_mixins.CfnResolverPropsMixin.LambdaConflictHandlerConfigProperty(
                    lambda_conflict_handler_arn="lambdaConflictHandlerArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a6cd258570c7d245ccff132fd752d1b9289ed281e80be1191096da1a8310743)
                check_type(argname="argument lambda_conflict_handler_arn", value=lambda_conflict_handler_arn, expected_type=type_hints["lambda_conflict_handler_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_conflict_handler_arn is not None:
                self._values["lambda_conflict_handler_arn"] = lambda_conflict_handler_arn

        @builtins.property
        def lambda_conflict_handler_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the Lambda function to use as the Conflict Handler.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-lambdaconflicthandlerconfig.html#cfn-appsync-resolver-lambdaconflicthandlerconfig-lambdaconflicthandlerarn
            '''
            result = self._values.get("lambda_conflict_handler_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaConflictHandlerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnResolverPropsMixin.PipelineConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"functions": "functions"},
    )
    class PipelineConfigProperty:
        def __init__(
            self,
            *,
            functions: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Use the ``PipelineConfig`` property type to specify ``PipelineConfig`` for an AWS AppSync resolver.

            ``PipelineConfig`` is a property of the `AWS::AppSync::Resolver <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html>`_ resource.

            :param functions: A list of ``Function`` objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-pipelineconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                pipeline_config_property = appsync_mixins.CfnResolverPropsMixin.PipelineConfigProperty(
                    functions=["functions"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fdf5bd9bb96b150879bf259ab98b5a11b80f5400c18a4b08bc1cd1f26fe30d7d)
                check_type(argname="argument functions", value=functions, expected_type=type_hints["functions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if functions is not None:
                self._values["functions"] = functions

        @builtins.property
        def functions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of ``Function`` objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-pipelineconfig.html#cfn-appsync-resolver-pipelineconfig-functions
            '''
            result = self._values.get("functions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipelineConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnResolverPropsMixin.SyncConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "conflict_detection": "conflictDetection",
            "conflict_handler": "conflictHandler",
            "lambda_conflict_handler_config": "lambdaConflictHandlerConfig",
        },
    )
    class SyncConfigProperty:
        def __init__(
            self,
            *,
            conflict_detection: typing.Optional[builtins.str] = None,
            conflict_handler: typing.Optional[builtins.str] = None,
            lambda_conflict_handler_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResolverPropsMixin.LambdaConflictHandlerConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes a Sync configuration for a resolver.

            Specifies which Conflict Detection strategy and Resolution strategy to use when the resolver is invoked.

            :param conflict_detection: The Conflict Detection strategy to use. - *VERSION* : Detect conflicts based on object versions for this resolver. - *NONE* : Do not detect conflicts when invoking this resolver.
            :param conflict_handler: The Conflict Resolution strategy to perform in the event of a conflict. - *OPTIMISTIC_CONCURRENCY* : Resolve conflicts by rejecting mutations when versions don't match the latest version at the server. - *AUTOMERGE* : Resolve conflicts with the Automerge conflict resolution strategy. - *LAMBDA* : Resolve conflicts with an AWS Lambda function supplied in the ``LambdaConflictHandlerConfig`` .
            :param lambda_conflict_handler_config: The ``LambdaConflictHandlerConfig`` when configuring ``LAMBDA`` as the Conflict Handler.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-syncconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                sync_config_property = appsync_mixins.CfnResolverPropsMixin.SyncConfigProperty(
                    conflict_detection="conflictDetection",
                    conflict_handler="conflictHandler",
                    lambda_conflict_handler_config=appsync_mixins.CfnResolverPropsMixin.LambdaConflictHandlerConfigProperty(
                        lambda_conflict_handler_arn="lambdaConflictHandlerArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__26c2191a1e4cfcba4e6d9cbb0b805acb2f0aee6c290d234013dbc1e1e7973d00)
                check_type(argname="argument conflict_detection", value=conflict_detection, expected_type=type_hints["conflict_detection"])
                check_type(argname="argument conflict_handler", value=conflict_handler, expected_type=type_hints["conflict_handler"])
                check_type(argname="argument lambda_conflict_handler_config", value=lambda_conflict_handler_config, expected_type=type_hints["lambda_conflict_handler_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if conflict_detection is not None:
                self._values["conflict_detection"] = conflict_detection
            if conflict_handler is not None:
                self._values["conflict_handler"] = conflict_handler
            if lambda_conflict_handler_config is not None:
                self._values["lambda_conflict_handler_config"] = lambda_conflict_handler_config

        @builtins.property
        def conflict_detection(self) -> typing.Optional[builtins.str]:
            '''The Conflict Detection strategy to use.

            - *VERSION* : Detect conflicts based on object versions for this resolver.
            - *NONE* : Do not detect conflicts when invoking this resolver.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-syncconfig.html#cfn-appsync-resolver-syncconfig-conflictdetection
            '''
            result = self._values.get("conflict_detection")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def conflict_handler(self) -> typing.Optional[builtins.str]:
            '''The Conflict Resolution strategy to perform in the event of a conflict.

            - *OPTIMISTIC_CONCURRENCY* : Resolve conflicts by rejecting mutations when versions don't match the latest version at the server.
            - *AUTOMERGE* : Resolve conflicts with the Automerge conflict resolution strategy.
            - *LAMBDA* : Resolve conflicts with an AWS Lambda function supplied in the ``LambdaConflictHandlerConfig`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-syncconfig.html#cfn-appsync-resolver-syncconfig-conflicthandler
            '''
            result = self._values.get("conflict_handler")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def lambda_conflict_handler_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResolverPropsMixin.LambdaConflictHandlerConfigProperty"]]:
            '''The ``LambdaConflictHandlerConfig`` when configuring ``LAMBDA`` as the Conflict Handler.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-syncconfig.html#cfn-appsync-resolver-syncconfig-lambdaconflicthandlerconfig
            '''
            result = self._values.get("lambda_conflict_handler_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResolverPropsMixin.LambdaConflictHandlerConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SyncConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnSourceApiAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "merged_api_identifier": "mergedApiIdentifier",
        "source_api_association_config": "sourceApiAssociationConfig",
        "source_api_identifier": "sourceApiIdentifier",
    },
)
class CfnSourceApiAssociationMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        merged_api_identifier: typing.Optional[builtins.str] = None,
        source_api_association_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSourceApiAssociationPropsMixin.SourceApiAssociationConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        source_api_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSourceApiAssociationPropsMixin.

        :param description: The description field of the association configuration.
        :param merged_api_identifier: The identifier of the AppSync Merged API. This is generated by the AppSync service. In most cases, Merged APIs (especially in your account) only require the API ID value or ARN of the merged API. However, Merged APIs from other accounts (cross-account use cases) strictly require the full resource ARN of the merged API.
        :param source_api_association_config: The ``SourceApiAssociationConfig`` object data.
        :param source_api_identifier: The identifier of the AppSync Source API. This is generated by the AppSync service. In most cases, source APIs (especially in your account) only require the API ID value or ARN of the source API. However, source APIs from other accounts (cross-account use cases) strictly require the full resource ARN of the source API.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-sourceapiassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
            
            cfn_source_api_association_mixin_props = appsync_mixins.CfnSourceApiAssociationMixinProps(
                description="description",
                merged_api_identifier="mergedApiIdentifier",
                source_api_association_config=appsync_mixins.CfnSourceApiAssociationPropsMixin.SourceApiAssociationConfigProperty(
                    merge_type="mergeType"
                ),
                source_api_identifier="sourceApiIdentifier"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53398f12d28f2f39aa36e0e3b1157127c7de1bb61d66e11e3075676533170b3)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument merged_api_identifier", value=merged_api_identifier, expected_type=type_hints["merged_api_identifier"])
            check_type(argname="argument source_api_association_config", value=source_api_association_config, expected_type=type_hints["source_api_association_config"])
            check_type(argname="argument source_api_identifier", value=source_api_identifier, expected_type=type_hints["source_api_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if merged_api_identifier is not None:
            self._values["merged_api_identifier"] = merged_api_identifier
        if source_api_association_config is not None:
            self._values["source_api_association_config"] = source_api_association_config
        if source_api_identifier is not None:
            self._values["source_api_identifier"] = source_api_identifier

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description field of the association configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-sourceapiassociation.html#cfn-appsync-sourceapiassociation-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def merged_api_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the AppSync Merged API.

        This is generated by the AppSync service. In most cases, Merged APIs (especially in your account) only require the API ID value or ARN of the merged API. However, Merged APIs from other accounts (cross-account use cases) strictly require the full resource ARN of the merged API.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-sourceapiassociation.html#cfn-appsync-sourceapiassociation-mergedapiidentifier
        '''
        result = self._values.get("merged_api_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_api_association_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSourceApiAssociationPropsMixin.SourceApiAssociationConfigProperty"]]:
        '''The ``SourceApiAssociationConfig`` object data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-sourceapiassociation.html#cfn-appsync-sourceapiassociation-sourceapiassociationconfig
        '''
        result = self._values.get("source_api_association_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSourceApiAssociationPropsMixin.SourceApiAssociationConfigProperty"]], result)

    @builtins.property
    def source_api_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the AppSync Source API.

        This is generated by the AppSync service. In most cases, source APIs (especially in your account) only require the API ID value or ARN of the source API. However, source APIs from other accounts (cross-account use cases) strictly require the full resource ARN of the source API.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-sourceapiassociation.html#cfn-appsync-sourceapiassociation-sourceapiidentifier
        '''
        result = self._values.get("source_api_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSourceApiAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSourceApiAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnSourceApiAssociationPropsMixin",
):
    '''Describes the configuration of a source API.

    A source API is a GraphQL API that is linked to a merged API. There can be multiple source APIs attached to each merged API. When linked to a merged API, the source API's schema, data sources, and resolvers will be combined with other linked source API data to form a new, singular API. Source APIs can originate from your account or from other accounts via Resource Access Manager.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-sourceapiassociation.html
    :cloudformationResource: AWS::AppSync::SourceApiAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
        
        cfn_source_api_association_props_mixin = appsync_mixins.CfnSourceApiAssociationPropsMixin(appsync_mixins.CfnSourceApiAssociationMixinProps(
            description="description",
            merged_api_identifier="mergedApiIdentifier",
            source_api_association_config=appsync_mixins.CfnSourceApiAssociationPropsMixin.SourceApiAssociationConfigProperty(
                merge_type="mergeType"
            ),
            source_api_identifier="sourceApiIdentifier"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSourceApiAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppSync::SourceApiAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__838f3b30e3d8975b92882a176fea942ade235a7b3ad4ce16f3f3c2e7ea3051b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f59cd50928a6d3fdfcfbc5d4e66281513cad672a4230225d0e4ea8e67423d00c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7a902ec9566b2c79bde87c1fa491c7cf39f79b6b261915fcd2f04fd2ef92f5a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSourceApiAssociationMixinProps:
        return typing.cast(CfnSourceApiAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appsync.mixins.CfnSourceApiAssociationPropsMixin.SourceApiAssociationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"merge_type": "mergeType"},
    )
    class SourceApiAssociationConfigProperty:
        def __init__(self, *, merge_type: typing.Optional[builtins.str] = None) -> None:
            '''Describes properties used to specify configurations related to a source API.

            This is a property of the ``AWS:AppSync:SourceApiAssociation`` type.

            :param merge_type: The property that indicates which merging option is enabled in the source API association. Valid merge types are ``MANUAL_MERGE`` (default) and ``AUTO_MERGE`` . Manual merges are the default behavior and require the user to trigger any changes from the source APIs to the merged API manually. Auto merges subscribe the merged API to the changes performed on the source APIs so that any change in the source APIs are also made to the merged API. Auto merges use ``MergedApiExecutionRoleArn`` to perform merge operations. The following values are valid: ``MANUAL_MERGE | AUTO_MERGE``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-sourceapiassociation-sourceapiassociationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appsync import mixins as appsync_mixins
                
                source_api_association_config_property = appsync_mixins.CfnSourceApiAssociationPropsMixin.SourceApiAssociationConfigProperty(
                    merge_type="mergeType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e32a1029e28179baf8af7c45d1a03c3b03244cce846cbd210eb1ea37b3e34138)
                check_type(argname="argument merge_type", value=merge_type, expected_type=type_hints["merge_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if merge_type is not None:
                self._values["merge_type"] = merge_type

        @builtins.property
        def merge_type(self) -> typing.Optional[builtins.str]:
            '''The property that indicates which merging option is enabled in the source API association.

            Valid merge types are ``MANUAL_MERGE`` (default) and ``AUTO_MERGE`` . Manual merges are the default behavior and require the user to trigger any changes from the source APIs to the merged API manually. Auto merges subscribe the merged API to the changes performed on the source APIs so that any change in the source APIs are also made to the merged API. Auto merges use ``MergedApiExecutionRoleArn`` to perform merge operations.

            The following values are valid:

            ``MANUAL_MERGE | AUTO_MERGE``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-sourceapiassociation-sourceapiassociationconfig.html#cfn-appsync-sourceapiassociation-sourceapiassociationconfig-mergetype
            '''
            result = self._values.get("merge_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceApiAssociationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnApiCacheMixinProps",
    "CfnApiCachePropsMixin",
    "CfnApiKeyMixinProps",
    "CfnApiKeyPropsMixin",
    "CfnApiMixinProps",
    "CfnApiPropsMixin",
    "CfnChannelNamespaceMixinProps",
    "CfnChannelNamespacePropsMixin",
    "CfnDataSourceMixinProps",
    "CfnDataSourcePropsMixin",
    "CfnDomainNameApiAssociationMixinProps",
    "CfnDomainNameApiAssociationPropsMixin",
    "CfnDomainNameMixinProps",
    "CfnDomainNamePropsMixin",
    "CfnFunctionConfigurationMixinProps",
    "CfnFunctionConfigurationPropsMixin",
    "CfnGraphQLApiMixinProps",
    "CfnGraphQLApiPropsMixin",
    "CfnGraphQLSchemaMixinProps",
    "CfnGraphQLSchemaPropsMixin",
    "CfnResolverMixinProps",
    "CfnResolverPropsMixin",
    "CfnSourceApiAssociationMixinProps",
    "CfnSourceApiAssociationPropsMixin",
]

publication.publish()

def _typecheckingstub__05c05b00857c4b21388f093f77b097d7ca6f21c88202eb411a79881de6ceec02(
    *,
    api_caching_behavior: typing.Optional[builtins.str] = None,
    api_id: typing.Optional[builtins.str] = None,
    at_rest_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    health_metrics_config: typing.Optional[builtins.str] = None,
    transit_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ttl: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e91198803cbf7b1d0b86b6bb97df4f192c19dc159ad4691d94b71ab889b64a(
    props: typing.Union[CfnApiCacheMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e586fb662a5a6b78db9fe649521d84234d9fb961e4a418e140c94f1693b3a55(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1249fbf23cc288a9561bbe3afe259dc369b98d8fe36efde3aa2c7c32f1f26e07(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0219c7805dbef682f022d17b1eb83874748d94e4869dc6d8d3a29fc2e3eec50d(
    *,
    api_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    expires: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1215d0acb74490c196f558c51c4774b2b5dd82c65a595537c57c2b5f150a6e64(
    props: typing.Union[CfnApiKeyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c36cbec7fe69772ecaa5cdf571ae3b3e48408e73b7321b5ffb1f35af517bea23(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df8d7eec1dc15424ecca373ccf37dc69b5c6fcecd9db57d824fdb64e4fd1619(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da0e231c7c55caafbb30c69054cc38c88eb0881c96178918d5d7bb2ebe82d66e(
    *,
    event_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApiPropsMixin.EventConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    owner_contact: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c700091c61a6d27e42ab3f052878c4b487b9439e8609506d82d36bcf59b5121(
    props: typing.Union[CfnApiMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__590fa5c36f0a1c635fb29e7fb8d396d9e0dbff1be52ce1d47a9625898f72c675(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd51e64eb8bd6af8b75332e9364c8bea8362001ef97402dc069900f664a6ccbb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c20afe4d1e881e46cc032a41b8025a21a037ec1625eeb277ee4e0f893470b455(
    *,
    auth_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74ffc5fb5a61cd156fe437a4167a2cbabab7b43f99dbd11b5c4c25fe71df20d4(
    *,
    auth_type: typing.Optional[builtins.str] = None,
    cognito_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApiPropsMixin.CognitoConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    lambda_authorizer_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApiPropsMixin.LambdaAuthorizerConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    open_id_connect_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApiPropsMixin.OpenIDConnectConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9396a768ce9abf7de89418a34f89dd6e0c260cd4b08d3a7f77d4e40772cade0(
    *,
    app_id_client_regex: typing.Optional[builtins.str] = None,
    aws_region: typing.Optional[builtins.str] = None,
    user_pool_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3866e4e00b8a19383ab970813f60f67c6e6c8ce2ce1ee5688df0f7b48cb24b2(
    *,
    http: typing.Optional[builtins.str] = None,
    realtime: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e2a3afb45c1d4d5da2eafdaf5dea3bd4e5ca2a776d4e25109fde239bdd19def(
    *,
    auth_providers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApiPropsMixin.AuthProviderProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    connection_auth_modes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApiPropsMixin.AuthModeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    default_publish_auth_modes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApiPropsMixin.AuthModeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    default_subscribe_auth_modes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApiPropsMixin.AuthModeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    log_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApiPropsMixin.EventLogConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a06a75638e023e8a591df69c26ca92e50844d2a2aca6f95b630b2381dbe07cd3(
    *,
    cloud_watch_logs_role_arn: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ccdf6a81bd8a98560c0bd8442a0fca6e0c52e901ca6e2f59044b2d443e09e7f(
    *,
    authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number] = None,
    authorizer_uri: typing.Optional[builtins.str] = None,
    identity_validation_expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4f52bdb79d243a46baeb71994507cdf4eb62e7ddfe5a057f367bd258972322(
    *,
    auth_ttl: typing.Optional[jsii.Number] = None,
    client_id: typing.Optional[builtins.str] = None,
    iat_ttl: typing.Optional[jsii.Number] = None,
    issuer: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62d439405ed9d731fe067189dd22a1290af0b0e9c822793785392321b9be2998(
    *,
    api_id: typing.Optional[builtins.str] = None,
    code_handlers: typing.Optional[builtins.str] = None,
    code_s3_location: typing.Optional[builtins.str] = None,
    handler_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnChannelNamespacePropsMixin.HandlerConfigsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    publish_auth_modes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnChannelNamespacePropsMixin.AuthModeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    subscribe_auth_modes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnChannelNamespacePropsMixin.AuthModeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cf8e57cb5ef4cfe94d2bbfd770f3fe85428895af661cda96a2f9892d90dfd53(
    props: typing.Union[CfnChannelNamespaceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c137e0e22031ff19eb0637d05eccb3da1e5d9ae220ac0b3d883f21909f2d106(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e0214bec14d4a7bf806fc23d076a82ab1c932b9af7a078cb7b40f42c8c6e5ae(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4acc107db66d954a845af466a45072d3c0dfd604646910003c28750e7583b79e(
    *,
    auth_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__591dc766aef641e8f3c23304c0a401c408641c54d0d9850901e8df04d9b99200(
    *,
    behavior: typing.Optional[builtins.str] = None,
    integration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnChannelNamespacePropsMixin.IntegrationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3958e39f93544ad1be5291a97d76058bd81357ba379ea9789b993ee2b58f396(
    *,
    on_publish: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnChannelNamespacePropsMixin.HandlerConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    on_subscribe: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnChannelNamespacePropsMixin.HandlerConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fef0f0c224c287dd8402f373f48a45d49e2c6ff662bba8c77b7b4d0ac2e05ce(
    *,
    data_source_name: typing.Optional[builtins.str] = None,
    lambda_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnChannelNamespacePropsMixin.LambdaConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67de4a54badc543038f1d26a05dc3c0fa5539eae081ffa1805c4d33a5d0ebe18(
    *,
    invoke_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c948aa2178ac1d4bdafd667666eb0b78be94108229aefd20939e6350da4b522c(
    *,
    api_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    dynamo_db_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DynamoDBConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    elasticsearch_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.ElasticsearchConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    event_bridge_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.EventBridgeConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    http_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.HttpConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    lambda_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.LambdaConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    metrics_config: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    open_search_service_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.OpenSearchServiceConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    relational_database_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.RelationalDatabaseConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_role_arn: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0783acbcb03400459d9c51451d9479fac9894c60899d17fabef7d83a0b855b24(
    props: typing.Union[CfnDataSourceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ebe22731bfa41d88112da20a71e01ae6ac53f54056b3a67324b0c6f459dd881(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a6113d7e2949ac56623f686c4c43693b6331f48dc49b2078d9d0d9d35bef6c5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1bb349b6d7d58ec945cd94cade17eaf94319ed02ea273a1422199a9a25c6c97(
    *,
    authorization_type: typing.Optional[builtins.str] = None,
    aws_iam_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.AwsIamConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b02d5f7378e5839c11d435537451fa9085f869c796da32e220142656c7c26e9d(
    *,
    signing_region: typing.Optional[builtins.str] = None,
    signing_service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff1bb65d343903cc5698fe64df969c585834d254e625f028524032ae3a85d62(
    *,
    base_table_ttl: typing.Optional[builtins.str] = None,
    delta_sync_table_name: typing.Optional[builtins.str] = None,
    delta_sync_table_ttl: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4c543f2b30ad4cd76c1f2bec7b8962b1d36584604c8743f07a84da120f21195(
    *,
    aws_region: typing.Optional[builtins.str] = None,
    delta_sync_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DeltaSyncConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_name: typing.Optional[builtins.str] = None,
    use_caller_credentials: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    versioned: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c64a149e69e18501a5711766b92d667ad7e38015ca5f9d365d35aed9729e75e2(
    *,
    aws_region: typing.Optional[builtins.str] = None,
    endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebe4fa646e1ae1036168c8904e4fd83f3050876036d67f0045e8be09f07ed0b9(
    *,
    event_bus_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bd88226a6af3b494e0af610fe7e310159fd78fb74a6c0b2e075b110c2eae2e1(
    *,
    authorization_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.AuthorizationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3859073b4ec4f2d737991d4863b79356c0b415bc8e723f364ad28df73c5b6e74(
    *,
    lambda_function_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df349efa2e246cdc050124451ec187df16392f4a687330decf4acb861a874648(
    *,
    aws_region: typing.Optional[builtins.str] = None,
    endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37349d29bf4d91d7812152e79b6520db3bd5b7ffd81024a37347b00002ea20da(
    *,
    aws_region: typing.Optional[builtins.str] = None,
    aws_secret_store_arn: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    db_cluster_identifier: typing.Optional[builtins.str] = None,
    schema: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ae2ec63faef5d15bcedb19e9a3efafaea773970328ee16eed37ddd1ed79ed4(
    *,
    rds_http_endpoint_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.RdsHttpEndpointConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    relational_database_source_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__762b16e5f8cd459d1654832994e398056186a1173cd181c89d0f05decbf2dc17(
    *,
    api_id: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af18555a02e56bcd6d8b00314f61e3b07843beb4cc058cda5b0358ad03044a3d(
    props: typing.Union[CfnDomainNameApiAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__859151fcbb870bf8602f2384bb697d16a1f3170c7f519cc5c05c29cfc16b02b2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241d9fdfc222b0d749431ea86e3ff181a3c8f7790aff9c348f6822a6a5082a01(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81d3df5c55f9ab9dacdb80f14ac1827a3034b3b2183d9698419eb6485defb6f(
    *,
    certificate_arn: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e6cd89afad7e3cd9e0294ce8f91e410f5bd47fd7dc327af2fcbccadf9960943(
    props: typing.Union[CfnDomainNameMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4559cbed19a5a61c205eeec7baf37fd448000dded937f608829cc72b910b89a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f5893512e1082e24149814b02c2e776f48b15001b5eab1087c2466357157dbf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7f8679cd8c6a1a9752afe43a5803cce15c38803c22e140b13c75607f9113fce(
    *,
    api_id: typing.Optional[builtins.str] = None,
    code: typing.Optional[builtins.str] = None,
    code_s3_location: typing.Optional[builtins.str] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    function_version: typing.Optional[builtins.str] = None,
    max_batch_size: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    request_mapping_template: typing.Optional[builtins.str] = None,
    request_mapping_template_s3_location: typing.Optional[builtins.str] = None,
    response_mapping_template: typing.Optional[builtins.str] = None,
    response_mapping_template_s3_location: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionConfigurationPropsMixin.AppSyncRuntimeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sync_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionConfigurationPropsMixin.SyncConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64984246fa8df864f7d2ddafc1b80f004c797379d0f603bf0031196827b5efea(
    props: typing.Union[CfnFunctionConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91abbfcda09a4ce52677df167fb31b0217d45504a475bf50081ea19a5cb3b82c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb6c5a6de3b5f66ac1d2802034f5077c505945ad97139be6ede240ddc861f427(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b314fae8e3a29d1255eb0120dcba3bb7516ef7638938b8ced1423f00eb23397(
    *,
    name: typing.Optional[builtins.str] = None,
    runtime_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a24a8643992fddbbe4e2a165a11de5b5c58796f6ecc2f18d0fa506a34e0572(
    *,
    lambda_conflict_handler_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8330060895de021d48b939cefd6dc2cdbef75cfbcd9609229922ff6ac1bd4020(
    *,
    conflict_detection: typing.Optional[builtins.str] = None,
    conflict_handler: typing.Optional[builtins.str] = None,
    lambda_conflict_handler_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionConfigurationPropsMixin.LambdaConflictHandlerConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab0a3a506028393a5970f51b244e086ad074d9c88750e6ee8df9474f3f0b1712(
    *,
    additional_authentication_providers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGraphQLApiPropsMixin.AdditionalAuthenticationProviderProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    api_type: typing.Optional[builtins.str] = None,
    authentication_type: typing.Optional[builtins.str] = None,
    enhanced_metrics_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGraphQLApiPropsMixin.EnhancedMetricsConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    environment_variables: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    introspection_config: typing.Optional[builtins.str] = None,
    lambda_authorizer_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGraphQLApiPropsMixin.LambdaAuthorizerConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    log_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGraphQLApiPropsMixin.LogConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    merged_api_execution_role_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    open_id_connect_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGraphQLApiPropsMixin.OpenIDConnectConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    owner_contact: typing.Optional[builtins.str] = None,
    query_depth_limit: typing.Optional[jsii.Number] = None,
    resolver_count_limit: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_pool_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGraphQLApiPropsMixin.UserPoolConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    visibility: typing.Optional[builtins.str] = None,
    xray_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fb6d6dec558f2a878ea479d7e4ba94a457fa1f0c353f1ca65f28867e536197c(
    props: typing.Union[CfnGraphQLApiMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae55ccf4e97b09379e6ad13639101c645997f25441ea4195d218763f8a2cade6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ac6217d798fce36c378877c7101f89feab8c7a3d18f79ab3cff876caebf2d37(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c544e503256e1b2e51d9ea26c4072b1c99c534407e4e0ef8e9fb1bbe2a91313(
    *,
    authentication_type: typing.Optional[builtins.str] = None,
    lambda_authorizer_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGraphQLApiPropsMixin.LambdaAuthorizerConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    open_id_connect_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGraphQLApiPropsMixin.OpenIDConnectConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_pool_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGraphQLApiPropsMixin.CognitoUserPoolConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3d96ab603a5b124e7aa3d4626682eb04f9913536fa76af5f2f8bdf670e9aae8(
    *,
    app_id_client_regex: typing.Optional[builtins.str] = None,
    aws_region: typing.Optional[builtins.str] = None,
    user_pool_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__524236f3cab3eab7e5e9a62c2a342cb611b20334a6ad3da177c5cdf3235c281a(
    *,
    data_source_level_metrics_behavior: typing.Optional[builtins.str] = None,
    operation_level_metrics_config: typing.Optional[builtins.str] = None,
    resolver_level_metrics_behavior: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__613b5142a9a568947bd5b6ca570eb4d5360d45f460d7fa7ada1885b49e67dc5a(
    *,
    authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number] = None,
    authorizer_uri: typing.Optional[builtins.str] = None,
    identity_validation_expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb13b8bb1367c19757403113fba81ff67a27e867bce1fb7ebf1a5ca84354ba9d(
    *,
    cloud_watch_logs_role_arn: typing.Optional[builtins.str] = None,
    exclude_verbose_content: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    field_log_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4718eae6502088b81017fdd1131b4f41d6811fb9e6ac0f17d2112f4144c876d0(
    *,
    auth_ttl: typing.Optional[jsii.Number] = None,
    client_id: typing.Optional[builtins.str] = None,
    iat_ttl: typing.Optional[jsii.Number] = None,
    issuer: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f08c4e593bfaa8394ed8468a44bd9a84ceb022a706708a8599cd4c2aa66b102(
    *,
    app_id_client_regex: typing.Optional[builtins.str] = None,
    aws_region: typing.Optional[builtins.str] = None,
    default_action: typing.Optional[builtins.str] = None,
    user_pool_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__921887fdef89fe6d44425d1239157b3f69f273125b77a5a99cdd1b99045ba26c(
    *,
    api_id: typing.Optional[builtins.str] = None,
    definition: typing.Optional[builtins.str] = None,
    definition_s3_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f89db116e3b849cd21a713d4c25dfde73390325e5de0862e138a4a7000a55552(
    props: typing.Union[CfnGraphQLSchemaMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5730822e8789ee2a10e6bc02bcc1dbc2b87b011fe68d218598303836935af0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff8bc5277ee1776212cd3d293d625db8a87b48113355b541504088fd2f4785a6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__777073e0d9ce9df56d1d93c5e72fdd76151ecd0245c6ea5ae8d574845b5a0ece(
    *,
    api_id: typing.Optional[builtins.str] = None,
    caching_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResolverPropsMixin.CachingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    code: typing.Optional[builtins.str] = None,
    code_s3_location: typing.Optional[builtins.str] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    field_name: typing.Optional[builtins.str] = None,
    kind: typing.Optional[builtins.str] = None,
    max_batch_size: typing.Optional[jsii.Number] = None,
    metrics_config: typing.Optional[builtins.str] = None,
    pipeline_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResolverPropsMixin.PipelineConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    request_mapping_template: typing.Optional[builtins.str] = None,
    request_mapping_template_s3_location: typing.Optional[builtins.str] = None,
    response_mapping_template: typing.Optional[builtins.str] = None,
    response_mapping_template_s3_location: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResolverPropsMixin.AppSyncRuntimeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sync_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResolverPropsMixin.SyncConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25460e1b0068588a0c38af310d214fefa978d87ccea457395fce22fa7276a289(
    props: typing.Union[CfnResolverMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ef66861349dfb40733b9fa3d40db432711955c962027794b6b4de7cfea22a1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07943520e0e55b260594c7f1649a5408409172b0f881411a8c53e0f4a9f1fc42(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1867033c1c86b3a2b723f7599c5d5679a5c237c7b5b2a33f594ee92156e53784(
    *,
    name: typing.Optional[builtins.str] = None,
    runtime_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11250d093794e3c12e36ae8ecf9afcda3f570bc81511b75116fa0ffd028ca14e(
    *,
    caching_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a6cd258570c7d245ccff132fd752d1b9289ed281e80be1191096da1a8310743(
    *,
    lambda_conflict_handler_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf5bd9bb96b150879bf259ab98b5a11b80f5400c18a4b08bc1cd1f26fe30d7d(
    *,
    functions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26c2191a1e4cfcba4e6d9cbb0b805acb2f0aee6c290d234013dbc1e1e7973d00(
    *,
    conflict_detection: typing.Optional[builtins.str] = None,
    conflict_handler: typing.Optional[builtins.str] = None,
    lambda_conflict_handler_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResolverPropsMixin.LambdaConflictHandlerConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53398f12d28f2f39aa36e0e3b1157127c7de1bb61d66e11e3075676533170b3(
    *,
    description: typing.Optional[builtins.str] = None,
    merged_api_identifier: typing.Optional[builtins.str] = None,
    source_api_association_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSourceApiAssociationPropsMixin.SourceApiAssociationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_api_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__838f3b30e3d8975b92882a176fea942ade235a7b3ad4ce16f3f3c2e7ea3051b2(
    props: typing.Union[CfnSourceApiAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f59cd50928a6d3fdfcfbc5d4e66281513cad672a4230225d0e4ea8e67423d00c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7a902ec9566b2c79bde87c1fa491c7cf39f79b6b261915fcd2f04fd2ef92f5a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e32a1029e28179baf8af7c45d1a03c3b03244cce846cbd210eb1ea37b3e34138(
    *,
    merge_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
