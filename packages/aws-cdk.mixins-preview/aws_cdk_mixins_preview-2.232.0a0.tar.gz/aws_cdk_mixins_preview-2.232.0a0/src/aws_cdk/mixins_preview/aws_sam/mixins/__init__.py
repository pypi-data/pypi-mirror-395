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
    jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnApiMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_log_setting": "accessLogSetting",
        "always_deploy": "alwaysDeploy",
        "auth": "auth",
        "binary_media_types": "binaryMediaTypes",
        "cache_cluster_enabled": "cacheClusterEnabled",
        "cache_cluster_size": "cacheClusterSize",
        "canary_setting": "canarySetting",
        "cors": "cors",
        "definition_body": "definitionBody",
        "definition_uri": "definitionUri",
        "description": "description",
        "disable_execute_api_endpoint": "disableExecuteApiEndpoint",
        "domain": "domain",
        "endpoint_configuration": "endpointConfiguration",
        "gateway_responses": "gatewayResponses",
        "method_settings": "methodSettings",
        "minimum_compression_size": "minimumCompressionSize",
        "models": "models",
        "name": "name",
        "open_api_version": "openApiVersion",
        "stage_name": "stageName",
        "tags": "tags",
        "tracing_enabled": "tracingEnabled",
        "variables": "variables",
    },
)
class CfnApiMixinProps:
    def __init__(
        self,
        *,
        access_log_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApiPropsMixin.AccessLogSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        always_deploy: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        auth: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApiPropsMixin.AuthProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        cache_cluster_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        cache_cluster_size: typing.Optional[builtins.str] = None,
        canary_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApiPropsMixin.CanarySettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        cors: typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApiPropsMixin.CorsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        definition_body: typing.Any = None,
        definition_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApiPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        domain: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApiPropsMixin.DomainConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        endpoint_configuration: typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApiPropsMixin.EndpointConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        gateway_responses: typing.Any = None,
        method_settings: typing.Optional[typing.Union[typing.Sequence[typing.Any], _aws_cdk_ceddda9d.IResolvable]] = None,
        minimum_compression_size: typing.Optional[jsii.Number] = None,
        models: typing.Any = None,
        name: typing.Optional[builtins.str] = None,
        open_api_version: typing.Optional[builtins.str] = None,
        stage_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tracing_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        variables: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    ) -> None:
        '''Properties for CfnApiPropsMixin.

        :param access_log_setting: 
        :param always_deploy: 
        :param auth: 
        :param binary_media_types: 
        :param cache_cluster_enabled: 
        :param cache_cluster_size: 
        :param canary_setting: 
        :param cors: 
        :param definition_body: 
        :param definition_uri: 
        :param description: 
        :param disable_execute_api_endpoint: 
        :param domain: 
        :param endpoint_configuration: 
        :param gateway_responses: 
        :param method_settings: 
        :param minimum_compression_size: 
        :param models: 
        :param name: 
        :param open_api_version: 
        :param stage_name: 
        :param tags: 
        :param tracing_enabled: 
        :param variables: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
            
            # authorizers: Any
            # definition_body: Any
            # gateway_responses: Any
            # method_settings: Any
            # models: Any
            
            cfn_api_mixin_props = sam_mixins.CfnApiMixinProps(
                access_log_setting=sam_mixins.CfnApiPropsMixin.AccessLogSettingProperty(
                    destination_arn="destinationArn",
                    format="format"
                ),
                always_deploy=False,
                auth=sam_mixins.CfnApiPropsMixin.AuthProperty(
                    add_default_authorizer_to_cors_preflight=False,
                    authorizers=authorizers,
                    default_authorizer="defaultAuthorizer"
                ),
                binary_media_types=["binaryMediaTypes"],
                cache_cluster_enabled=False,
                cache_cluster_size="cacheClusterSize",
                canary_setting=sam_mixins.CfnApiPropsMixin.CanarySettingProperty(
                    deployment_id="deploymentId",
                    percent_traffic=123,
                    stage_variable_overrides={
                        "stage_variable_overrides_key": "stageVariableOverrides"
                    },
                    use_stage_cache=False
                ),
                cors="cors",
                definition_body=definition_body,
                definition_uri="definitionUri",
                description="description",
                disable_execute_api_endpoint=False,
                domain=sam_mixins.CfnApiPropsMixin.DomainConfigurationProperty(
                    base_path=["basePath"],
                    certificate_arn="certificateArn",
                    domain_name="domainName",
                    endpoint_configuration="endpointConfiguration",
                    mutual_tls_authentication=sam_mixins.CfnApiPropsMixin.MutualTlsAuthenticationProperty(
                        truststore_uri="truststoreUri",
                        truststore_version="truststoreVersion"
                    ),
                    ownership_verification_certificate_arn="ownershipVerificationCertificateArn",
                    route53=sam_mixins.CfnApiPropsMixin.Route53ConfigurationProperty(
                        distributed_domain_name="distributedDomainName",
                        evaluate_target_health=False,
                        hosted_zone_id="hostedZoneId",
                        hosted_zone_name="hostedZoneName",
                        ip_v6=False
                    ),
                    security_policy="securityPolicy"
                ),
                endpoint_configuration="endpointConfiguration",
                gateway_responses=gateway_responses,
                method_settings=[method_settings],
                minimum_compression_size=123,
                models=models,
                name="name",
                open_api_version="openApiVersion",
                stage_name="stageName",
                tags={
                    "tags_key": "tags"
                },
                tracing_enabled=False,
                variables={
                    "variables_key": "variables"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84f933d0f19c07b09b10d6c9c90a04b351979e75f87a4f6be4d6490c2638f57e)
            check_type(argname="argument access_log_setting", value=access_log_setting, expected_type=type_hints["access_log_setting"])
            check_type(argname="argument always_deploy", value=always_deploy, expected_type=type_hints["always_deploy"])
            check_type(argname="argument auth", value=auth, expected_type=type_hints["auth"])
            check_type(argname="argument binary_media_types", value=binary_media_types, expected_type=type_hints["binary_media_types"])
            check_type(argname="argument cache_cluster_enabled", value=cache_cluster_enabled, expected_type=type_hints["cache_cluster_enabled"])
            check_type(argname="argument cache_cluster_size", value=cache_cluster_size, expected_type=type_hints["cache_cluster_size"])
            check_type(argname="argument canary_setting", value=canary_setting, expected_type=type_hints["canary_setting"])
            check_type(argname="argument cors", value=cors, expected_type=type_hints["cors"])
            check_type(argname="argument definition_body", value=definition_body, expected_type=type_hints["definition_body"])
            check_type(argname="argument definition_uri", value=definition_uri, expected_type=type_hints["definition_uri"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disable_execute_api_endpoint", value=disable_execute_api_endpoint, expected_type=type_hints["disable_execute_api_endpoint"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument endpoint_configuration", value=endpoint_configuration, expected_type=type_hints["endpoint_configuration"])
            check_type(argname="argument gateway_responses", value=gateway_responses, expected_type=type_hints["gateway_responses"])
            check_type(argname="argument method_settings", value=method_settings, expected_type=type_hints["method_settings"])
            check_type(argname="argument minimum_compression_size", value=minimum_compression_size, expected_type=type_hints["minimum_compression_size"])
            check_type(argname="argument models", value=models, expected_type=type_hints["models"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument open_api_version", value=open_api_version, expected_type=type_hints["open_api_version"])
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tracing_enabled", value=tracing_enabled, expected_type=type_hints["tracing_enabled"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_log_setting is not None:
            self._values["access_log_setting"] = access_log_setting
        if always_deploy is not None:
            self._values["always_deploy"] = always_deploy
        if auth is not None:
            self._values["auth"] = auth
        if binary_media_types is not None:
            self._values["binary_media_types"] = binary_media_types
        if cache_cluster_enabled is not None:
            self._values["cache_cluster_enabled"] = cache_cluster_enabled
        if cache_cluster_size is not None:
            self._values["cache_cluster_size"] = cache_cluster_size
        if canary_setting is not None:
            self._values["canary_setting"] = canary_setting
        if cors is not None:
            self._values["cors"] = cors
        if definition_body is not None:
            self._values["definition_body"] = definition_body
        if definition_uri is not None:
            self._values["definition_uri"] = definition_uri
        if description is not None:
            self._values["description"] = description
        if disable_execute_api_endpoint is not None:
            self._values["disable_execute_api_endpoint"] = disable_execute_api_endpoint
        if domain is not None:
            self._values["domain"] = domain
        if endpoint_configuration is not None:
            self._values["endpoint_configuration"] = endpoint_configuration
        if gateway_responses is not None:
            self._values["gateway_responses"] = gateway_responses
        if method_settings is not None:
            self._values["method_settings"] = method_settings
        if minimum_compression_size is not None:
            self._values["minimum_compression_size"] = minimum_compression_size
        if models is not None:
            self._values["models"] = models
        if name is not None:
            self._values["name"] = name
        if open_api_version is not None:
            self._values["open_api_version"] = open_api_version
        if stage_name is not None:
            self._values["stage_name"] = stage_name
        if tags is not None:
            self._values["tags"] = tags
        if tracing_enabled is not None:
            self._values["tracing_enabled"] = tracing_enabled
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def access_log_setting(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.AccessLogSettingProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html#cfn-serverless-api-accesslogsetting
        '''
        result = self._values.get("access_log_setting")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.AccessLogSettingProperty"]], result)

    @builtins.property
    def always_deploy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html#cfn-serverless-api-alwaysdeploy
        '''
        result = self._values.get("always_deploy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def auth(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.AuthProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html#cfn-serverless-api-auth
        '''
        result = self._values.get("auth")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.AuthProperty"]], result)

    @builtins.property
    def binary_media_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html#cfn-serverless-api-binarymediatypes
        '''
        result = self._values.get("binary_media_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cache_cluster_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html#cfn-serverless-api-cacheclusterenabled
        '''
        result = self._values.get("cache_cluster_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def cache_cluster_size(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html#cfn-serverless-api-cacheclustersize
        '''
        result = self._values.get("cache_cluster_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def canary_setting(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.CanarySettingProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html#cfn-serverless-api-canarysetting
        '''
        result = self._values.get("canary_setting")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.CanarySettingProperty"]], result)

    @builtins.property
    def cors(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.CorsConfigurationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html#cfn-serverless-api-cors
        '''
        result = self._values.get("cors")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.CorsConfigurationProperty"]], result)

    @builtins.property
    def definition_body(self) -> typing.Any:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html#cfn-serverless-api-definitionbody
        '''
        result = self._values.get("definition_body")
        return typing.cast(typing.Any, result)

    @builtins.property
    def definition_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.S3LocationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html#cfn-serverless-api-definitionuri
        '''
        result = self._values.get("definition_uri")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.S3LocationProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html#cfn-serverless-api-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_execute_api_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html#cfn-serverless-api-disableexecuteapiendpoint
        '''
        result = self._values.get("disable_execute_api_endpoint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def domain(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.DomainConfigurationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html#cfn-serverless-api-domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.DomainConfigurationProperty"]], result)

    @builtins.property
    def endpoint_configuration(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.EndpointConfigurationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html#cfn-serverless-api-endpointconfiguration
        '''
        result = self._values.get("endpoint_configuration")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.EndpointConfigurationProperty"]], result)

    @builtins.property
    def gateway_responses(self) -> typing.Any:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html#cfn-serverless-api-gatewayresponses
        '''
        result = self._values.get("gateway_responses")
        return typing.cast(typing.Any, result)

    @builtins.property
    def method_settings(
        self,
    ) -> typing.Optional[typing.Union[typing.List[typing.Any], _aws_cdk_ceddda9d.IResolvable]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html#cfn-serverless-api-methodsettings
        '''
        result = self._values.get("method_settings")
        return typing.cast(typing.Optional[typing.Union[typing.List[typing.Any], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def minimum_compression_size(self) -> typing.Optional[jsii.Number]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html#cfn-serverless-api-minimumcompressionsize
        '''
        result = self._values.get("minimum_compression_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def models(self) -> typing.Any:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html#cfn-serverless-api-models
        '''
        result = self._values.get("models")
        return typing.cast(typing.Any, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html#cfn-serverless-api-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def open_api_version(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html#cfn-serverless-api-openapiversion
        '''
        result = self._values.get("open_api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage_name(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html#cfn-serverless-api-stagename
        '''
        result = self._values.get("stage_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html#cfn-serverless-api-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tracing_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html#cfn-serverless-api-tracingenabled
        '''
        result = self._values.get("tracing_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def variables(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html#cfn-serverless-api-variables
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnApiPropsMixin",
):
    '''https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-api.html
    :cloudformationResource: AWS::Serverless::Api
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
        
        # authorizers: Any
        # definition_body: Any
        # gateway_responses: Any
        # method_settings: Any
        # models: Any
        
        cfn_api_props_mixin = sam_mixins.CfnApiPropsMixin(sam_mixins.CfnApiMixinProps(
            access_log_setting=sam_mixins.CfnApiPropsMixin.AccessLogSettingProperty(
                destination_arn="destinationArn",
                format="format"
            ),
            always_deploy=False,
            auth=sam_mixins.CfnApiPropsMixin.AuthProperty(
                add_default_authorizer_to_cors_preflight=False,
                authorizers=authorizers,
                default_authorizer="defaultAuthorizer"
            ),
            binary_media_types=["binaryMediaTypes"],
            cache_cluster_enabled=False,
            cache_cluster_size="cacheClusterSize",
            canary_setting=sam_mixins.CfnApiPropsMixin.CanarySettingProperty(
                deployment_id="deploymentId",
                percent_traffic=123,
                stage_variable_overrides={
                    "stage_variable_overrides_key": "stageVariableOverrides"
                },
                use_stage_cache=False
            ),
            cors="cors",
            definition_body=definition_body,
            definition_uri="definitionUri",
            description="description",
            disable_execute_api_endpoint=False,
            domain=sam_mixins.CfnApiPropsMixin.DomainConfigurationProperty(
                base_path=["basePath"],
                certificate_arn="certificateArn",
                domain_name="domainName",
                endpoint_configuration="endpointConfiguration",
                mutual_tls_authentication=sam_mixins.CfnApiPropsMixin.MutualTlsAuthenticationProperty(
                    truststore_uri="truststoreUri",
                    truststore_version="truststoreVersion"
                ),
                ownership_verification_certificate_arn="ownershipVerificationCertificateArn",
                route53=sam_mixins.CfnApiPropsMixin.Route53ConfigurationProperty(
                    distributed_domain_name="distributedDomainName",
                    evaluate_target_health=False,
                    hosted_zone_id="hostedZoneId",
                    hosted_zone_name="hostedZoneName",
                    ip_v6=False
                ),
                security_policy="securityPolicy"
            ),
            endpoint_configuration="endpointConfiguration",
            gateway_responses=gateway_responses,
            method_settings=[method_settings],
            minimum_compression_size=123,
            models=models,
            name="name",
            open_api_version="openApiVersion",
            stage_name="stageName",
            tags={
                "tags_key": "tags"
            },
            tracing_enabled=False,
            variables={
                "variables_key": "variables"
            }
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
        '''Create a mixin to apply properties to ``AWS::Serverless::Api``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e510da3d6b99a6cfb6181c8cbfbd8d93db66f6244d227dd8899c840765451b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__137949329432f1ea8c946d546b477c4842e952b3c54f50c18597470b9f6f7ff4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed9f188125c2fecb6380952f1b56ba565e3609447cd99841c8db67627bed7daa)
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
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnApiPropsMixin.AccessLogSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"destination_arn": "destinationArn", "format": "format"},
    )
    class AccessLogSettingProperty:
        def __init__(
            self,
            *,
            destination_arn: typing.Optional[builtins.str] = None,
            format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param destination_arn: 
            :param format: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-accesslogsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                access_log_setting_property = sam_mixins.CfnApiPropsMixin.AccessLogSettingProperty(
                    destination_arn="destinationArn",
                    format="format"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e4ef4413f02da8f13dfec2c9ce8599c6b01b649a0691eeb433b80251c7a99e09)
                check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
                check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_arn is not None:
                self._values["destination_arn"] = destination_arn
            if format is not None:
                self._values["format"] = format

        @builtins.property
        def destination_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-accesslogsetting.html#cfn-serverless-api-accesslogsetting-destinationarn
            '''
            result = self._values.get("destination_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def format(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-accesslogsetting.html#cfn-serverless-api-accesslogsetting-format
            '''
            result = self._values.get("format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessLogSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnApiPropsMixin.AuthProperty",
        jsii_struct_bases=[],
        name_mapping={
            "add_default_authorizer_to_cors_preflight": "addDefaultAuthorizerToCorsPreflight",
            "authorizers": "authorizers",
            "default_authorizer": "defaultAuthorizer",
        },
    )
    class AuthProperty:
        def __init__(
            self,
            *,
            add_default_authorizer_to_cors_preflight: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            authorizers: typing.Any = None,
            default_authorizer: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param add_default_authorizer_to_cors_preflight: 
            :param authorizers: 
            :param default_authorizer: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-auth.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                # authorizers: Any
                
                auth_property = sam_mixins.CfnApiPropsMixin.AuthProperty(
                    add_default_authorizer_to_cors_preflight=False,
                    authorizers=authorizers,
                    default_authorizer="defaultAuthorizer"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4d9822383a83801361385ece9af804f620d188cbbaef719efe04548ccc84d68c)
                check_type(argname="argument add_default_authorizer_to_cors_preflight", value=add_default_authorizer_to_cors_preflight, expected_type=type_hints["add_default_authorizer_to_cors_preflight"])
                check_type(argname="argument authorizers", value=authorizers, expected_type=type_hints["authorizers"])
                check_type(argname="argument default_authorizer", value=default_authorizer, expected_type=type_hints["default_authorizer"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if add_default_authorizer_to_cors_preflight is not None:
                self._values["add_default_authorizer_to_cors_preflight"] = add_default_authorizer_to_cors_preflight
            if authorizers is not None:
                self._values["authorizers"] = authorizers
            if default_authorizer is not None:
                self._values["default_authorizer"] = default_authorizer

        @builtins.property
        def add_default_authorizer_to_cors_preflight(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-auth.html#cfn-serverless-api-auth-adddefaultauthorizertocorspreflight
            '''
            result = self._values.get("add_default_authorizer_to_cors_preflight")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def authorizers(self) -> typing.Any:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-auth.html#cfn-serverless-api-auth-authorizers
            '''
            result = self._values.get("authorizers")
            return typing.cast(typing.Any, result)

        @builtins.property
        def default_authorizer(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-auth.html#cfn-serverless-api-auth-defaultauthorizer
            '''
            result = self._values.get("default_authorizer")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnApiPropsMixin.CanarySettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "deployment_id": "deploymentId",
            "percent_traffic": "percentTraffic",
            "stage_variable_overrides": "stageVariableOverrides",
            "use_stage_cache": "useStageCache",
        },
    )
    class CanarySettingProperty:
        def __init__(
            self,
            *,
            deployment_id: typing.Optional[builtins.str] = None,
            percent_traffic: typing.Optional[jsii.Number] = None,
            stage_variable_overrides: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            use_stage_cache: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''
            :param deployment_id: 
            :param percent_traffic: 
            :param stage_variable_overrides: 
            :param use_stage_cache: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-canarysetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                canary_setting_property = sam_mixins.CfnApiPropsMixin.CanarySettingProperty(
                    deployment_id="deploymentId",
                    percent_traffic=123,
                    stage_variable_overrides={
                        "stage_variable_overrides_key": "stageVariableOverrides"
                    },
                    use_stage_cache=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__906348e3f7ff2b29e868eeb3cfb6f2c9bd2e31b0428fc4ad42cab3643efa6b80)
                check_type(argname="argument deployment_id", value=deployment_id, expected_type=type_hints["deployment_id"])
                check_type(argname="argument percent_traffic", value=percent_traffic, expected_type=type_hints["percent_traffic"])
                check_type(argname="argument stage_variable_overrides", value=stage_variable_overrides, expected_type=type_hints["stage_variable_overrides"])
                check_type(argname="argument use_stage_cache", value=use_stage_cache, expected_type=type_hints["use_stage_cache"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if deployment_id is not None:
                self._values["deployment_id"] = deployment_id
            if percent_traffic is not None:
                self._values["percent_traffic"] = percent_traffic
            if stage_variable_overrides is not None:
                self._values["stage_variable_overrides"] = stage_variable_overrides
            if use_stage_cache is not None:
                self._values["use_stage_cache"] = use_stage_cache

        @builtins.property
        def deployment_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-canarysetting.html#cfn-serverless-api-canarysetting-deploymentid
            '''
            result = self._values.get("deployment_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def percent_traffic(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-canarysetting.html#cfn-serverless-api-canarysetting-percenttraffic
            '''
            result = self._values.get("percent_traffic")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stage_variable_overrides(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-canarysetting.html#cfn-serverless-api-canarysetting-stagevariableoverrides
            '''
            result = self._values.get("stage_variable_overrides")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def use_stage_cache(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-canarysetting.html#cfn-serverless-api-canarysetting-usestagecache
            '''
            result = self._values.get("use_stage_cache")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CanarySettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnApiPropsMixin.CorsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_credentials": "allowCredentials",
            "allow_headers": "allowHeaders",
            "allow_methods": "allowMethods",
            "allow_origin": "allowOrigin",
            "max_age": "maxAge",
        },
    )
    class CorsConfigurationProperty:
        def __init__(
            self,
            *,
            allow_credentials: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            allow_headers: typing.Optional[builtins.str] = None,
            allow_methods: typing.Optional[builtins.str] = None,
            allow_origin: typing.Optional[builtins.str] = None,
            max_age: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param allow_credentials: 
            :param allow_headers: 
            :param allow_methods: 
            :param allow_origin: 
            :param max_age: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-corsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                cors_configuration_property = sam_mixins.CfnApiPropsMixin.CorsConfigurationProperty(
                    allow_credentials=False,
                    allow_headers="allowHeaders",
                    allow_methods="allowMethods",
                    allow_origin="allowOrigin",
                    max_age="maxAge"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__19b322e2d0f531d71b2746ebd1563d4d7cfb3a238e82da21b6c539290fefcdc0)
                check_type(argname="argument allow_credentials", value=allow_credentials, expected_type=type_hints["allow_credentials"])
                check_type(argname="argument allow_headers", value=allow_headers, expected_type=type_hints["allow_headers"])
                check_type(argname="argument allow_methods", value=allow_methods, expected_type=type_hints["allow_methods"])
                check_type(argname="argument allow_origin", value=allow_origin, expected_type=type_hints["allow_origin"])
                check_type(argname="argument max_age", value=max_age, expected_type=type_hints["max_age"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allow_credentials is not None:
                self._values["allow_credentials"] = allow_credentials
            if allow_headers is not None:
                self._values["allow_headers"] = allow_headers
            if allow_methods is not None:
                self._values["allow_methods"] = allow_methods
            if allow_origin is not None:
                self._values["allow_origin"] = allow_origin
            if max_age is not None:
                self._values["max_age"] = max_age

        @builtins.property
        def allow_credentials(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-corsconfiguration.html#cfn-serverless-api-corsconfiguration-allowcredentials
            '''
            result = self._values.get("allow_credentials")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def allow_headers(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-corsconfiguration.html#cfn-serverless-api-corsconfiguration-allowheaders
            '''
            result = self._values.get("allow_headers")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def allow_methods(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-corsconfiguration.html#cfn-serverless-api-corsconfiguration-allowmethods
            '''
            result = self._values.get("allow_methods")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def allow_origin(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-corsconfiguration.html#cfn-serverless-api-corsconfiguration-alloworigin
            '''
            result = self._values.get("allow_origin")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_age(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-corsconfiguration.html#cfn-serverless-api-corsconfiguration-maxage
            '''
            result = self._values.get("max_age")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CorsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnApiPropsMixin.DomainConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "base_path": "basePath",
            "certificate_arn": "certificateArn",
            "domain_name": "domainName",
            "endpoint_configuration": "endpointConfiguration",
            "mutual_tls_authentication": "mutualTlsAuthentication",
            "ownership_verification_certificate_arn": "ownershipVerificationCertificateArn",
            "route53": "route53",
            "security_policy": "securityPolicy",
        },
    )
    class DomainConfigurationProperty:
        def __init__(
            self,
            *,
            base_path: typing.Optional[typing.Sequence[builtins.str]] = None,
            certificate_arn: typing.Optional[builtins.str] = None,
            domain_name: typing.Optional[builtins.str] = None,
            endpoint_configuration: typing.Optional[builtins.str] = None,
            mutual_tls_authentication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApiPropsMixin.MutualTlsAuthenticationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ownership_verification_certificate_arn: typing.Optional[builtins.str] = None,
            route53: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApiPropsMixin.Route53ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            security_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param base_path: 
            :param certificate_arn: 
            :param domain_name: 
            :param endpoint_configuration: 
            :param mutual_tls_authentication: 
            :param ownership_verification_certificate_arn: 
            :param route53: 
            :param security_policy: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-domainconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                domain_configuration_property = sam_mixins.CfnApiPropsMixin.DomainConfigurationProperty(
                    base_path=["basePath"],
                    certificate_arn="certificateArn",
                    domain_name="domainName",
                    endpoint_configuration="endpointConfiguration",
                    mutual_tls_authentication=sam_mixins.CfnApiPropsMixin.MutualTlsAuthenticationProperty(
                        truststore_uri="truststoreUri",
                        truststore_version="truststoreVersion"
                    ),
                    ownership_verification_certificate_arn="ownershipVerificationCertificateArn",
                    route53=sam_mixins.CfnApiPropsMixin.Route53ConfigurationProperty(
                        distributed_domain_name="distributedDomainName",
                        evaluate_target_health=False,
                        hosted_zone_id="hostedZoneId",
                        hosted_zone_name="hostedZoneName",
                        ip_v6=False
                    ),
                    security_policy="securityPolicy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f6f4bb51c7fa19c90a855e99103828700bc2dd70063d85c648317c0d4527679f)
                check_type(argname="argument base_path", value=base_path, expected_type=type_hints["base_path"])
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
                check_type(argname="argument endpoint_configuration", value=endpoint_configuration, expected_type=type_hints["endpoint_configuration"])
                check_type(argname="argument mutual_tls_authentication", value=mutual_tls_authentication, expected_type=type_hints["mutual_tls_authentication"])
                check_type(argname="argument ownership_verification_certificate_arn", value=ownership_verification_certificate_arn, expected_type=type_hints["ownership_verification_certificate_arn"])
                check_type(argname="argument route53", value=route53, expected_type=type_hints["route53"])
                check_type(argname="argument security_policy", value=security_policy, expected_type=type_hints["security_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if base_path is not None:
                self._values["base_path"] = base_path
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn
            if domain_name is not None:
                self._values["domain_name"] = domain_name
            if endpoint_configuration is not None:
                self._values["endpoint_configuration"] = endpoint_configuration
            if mutual_tls_authentication is not None:
                self._values["mutual_tls_authentication"] = mutual_tls_authentication
            if ownership_verification_certificate_arn is not None:
                self._values["ownership_verification_certificate_arn"] = ownership_verification_certificate_arn
            if route53 is not None:
                self._values["route53"] = route53
            if security_policy is not None:
                self._values["security_policy"] = security_policy

        @builtins.property
        def base_path(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-domainconfiguration.html#cfn-serverless-api-domainconfiguration-basepath
            '''
            result = self._values.get("base_path")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-domainconfiguration.html#cfn-serverless-api-domainconfiguration-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def domain_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-domainconfiguration.html#cfn-serverless-api-domainconfiguration-domainname
            '''
            result = self._values.get("domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def endpoint_configuration(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-domainconfiguration.html#cfn-serverless-api-domainconfiguration-endpointconfiguration
            '''
            result = self._values.get("endpoint_configuration")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mutual_tls_authentication(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.MutualTlsAuthenticationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-domainconfiguration.html#cfn-serverless-api-domainconfiguration-mutualtlsauthentication
            '''
            result = self._values.get("mutual_tls_authentication")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.MutualTlsAuthenticationProperty"]], result)

        @builtins.property
        def ownership_verification_certificate_arn(
            self,
        ) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-domainconfiguration.html#cfn-serverless-api-domainconfiguration-ownershipverificationcertificatearn
            '''
            result = self._values.get("ownership_verification_certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def route53(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.Route53ConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-domainconfiguration.html#cfn-serverless-api-domainconfiguration-route53
            '''
            result = self._values.get("route53")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiPropsMixin.Route53ConfigurationProperty"]], result)

        @builtins.property
        def security_policy(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-domainconfiguration.html#cfn-serverless-api-domainconfiguration-securitypolicy
            '''
            result = self._values.get("security_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnApiPropsMixin.EndpointConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "vpc_endpoint_ids": "vpcEndpointIds"},
    )
    class EndpointConfigurationProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            vpc_endpoint_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param type: 
            :param vpc_endpoint_ids: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-endpointconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                endpoint_configuration_property = sam_mixins.CfnApiPropsMixin.EndpointConfigurationProperty(
                    type="type",
                    vpc_endpoint_ids=["vpcEndpointIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__79b6f44c8399fdddc016632617b26893bd304aa10377bb52d9ed2c1b572a8e7b)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument vpc_endpoint_ids", value=vpc_endpoint_ids, expected_type=type_hints["vpc_endpoint_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if vpc_endpoint_ids is not None:
                self._values["vpc_endpoint_ids"] = vpc_endpoint_ids

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-endpointconfiguration.html#cfn-serverless-api-endpointconfiguration-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_endpoint_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-endpointconfiguration.html#cfn-serverless-api-endpointconfiguration-vpcendpointids
            '''
            result = self._values.get("vpc_endpoint_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EndpointConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnApiPropsMixin.MutualTlsAuthenticationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "truststore_uri": "truststoreUri",
            "truststore_version": "truststoreVersion",
        },
    )
    class MutualTlsAuthenticationProperty:
        def __init__(
            self,
            *,
            truststore_uri: typing.Optional[builtins.str] = None,
            truststore_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param truststore_uri: 
            :param truststore_version: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-mutualtlsauthentication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                mutual_tls_authentication_property = sam_mixins.CfnApiPropsMixin.MutualTlsAuthenticationProperty(
                    truststore_uri="truststoreUri",
                    truststore_version="truststoreVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ba94ff8650566b2ec6b2b0821dab0782673dd94614d40937a821505134a6bd24)
                check_type(argname="argument truststore_uri", value=truststore_uri, expected_type=type_hints["truststore_uri"])
                check_type(argname="argument truststore_version", value=truststore_version, expected_type=type_hints["truststore_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if truststore_uri is not None:
                self._values["truststore_uri"] = truststore_uri
            if truststore_version is not None:
                self._values["truststore_version"] = truststore_version

        @builtins.property
        def truststore_uri(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-mutualtlsauthentication.html#cfn-serverless-api-mutualtlsauthentication-truststoreuri
            '''
            result = self._values.get("truststore_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def truststore_version(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-mutualtlsauthentication.html#cfn-serverless-api-mutualtlsauthentication-truststoreversion
            '''
            result = self._values.get("truststore_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MutualTlsAuthenticationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnApiPropsMixin.Route53ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "distributed_domain_name": "distributedDomainName",
            "evaluate_target_health": "evaluateTargetHealth",
            "hosted_zone_id": "hostedZoneId",
            "hosted_zone_name": "hostedZoneName",
            "ip_v6": "ipV6",
        },
    )
    class Route53ConfigurationProperty:
        def __init__(
            self,
            *,
            distributed_domain_name: typing.Optional[builtins.str] = None,
            evaluate_target_health: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            hosted_zone_id: typing.Optional[builtins.str] = None,
            hosted_zone_name: typing.Optional[builtins.str] = None,
            ip_v6: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''
            :param distributed_domain_name: 
            :param evaluate_target_health: 
            :param hosted_zone_id: 
            :param hosted_zone_name: 
            :param ip_v6: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-route53configuration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                route53_configuration_property = sam_mixins.CfnApiPropsMixin.Route53ConfigurationProperty(
                    distributed_domain_name="distributedDomainName",
                    evaluate_target_health=False,
                    hosted_zone_id="hostedZoneId",
                    hosted_zone_name="hostedZoneName",
                    ip_v6=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d4e2720040a30d8a749bb767fa54506fa1f118ac3d79610dec298bdbbec5168f)
                check_type(argname="argument distributed_domain_name", value=distributed_domain_name, expected_type=type_hints["distributed_domain_name"])
                check_type(argname="argument evaluate_target_health", value=evaluate_target_health, expected_type=type_hints["evaluate_target_health"])
                check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
                check_type(argname="argument hosted_zone_name", value=hosted_zone_name, expected_type=type_hints["hosted_zone_name"])
                check_type(argname="argument ip_v6", value=ip_v6, expected_type=type_hints["ip_v6"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if distributed_domain_name is not None:
                self._values["distributed_domain_name"] = distributed_domain_name
            if evaluate_target_health is not None:
                self._values["evaluate_target_health"] = evaluate_target_health
            if hosted_zone_id is not None:
                self._values["hosted_zone_id"] = hosted_zone_id
            if hosted_zone_name is not None:
                self._values["hosted_zone_name"] = hosted_zone_name
            if ip_v6 is not None:
                self._values["ip_v6"] = ip_v6

        @builtins.property
        def distributed_domain_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-route53configuration.html#cfn-serverless-api-route53configuration-distributeddomainname
            '''
            result = self._values.get("distributed_domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def evaluate_target_health(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-route53configuration.html#cfn-serverless-api-route53configuration-evaluatetargethealth
            '''
            result = self._values.get("evaluate_target_health")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def hosted_zone_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-route53configuration.html#cfn-serverless-api-route53configuration-hostedzoneid
            '''
            result = self._values.get("hosted_zone_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hosted_zone_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-route53configuration.html#cfn-serverless-api-route53configuration-hostedzonename
            '''
            result = self._values.get("hosted_zone_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ip_v6(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-route53configuration.html#cfn-serverless-api-route53configuration-ipv6
            '''
            result = self._values.get("ip_v6")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "Route53ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnApiPropsMixin.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key", "version": "version"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
            version: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param bucket: 
            :param key: 
            :param version: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                s3_location_property = sam_mixins.CfnApiPropsMixin.S3LocationProperty(
                    bucket="bucket",
                    key="key",
                    version=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7b06b56203b6bc7ebb45e0db6817618fec1b2bf57571e395158ebb4dcdb3c3ff)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if key is not None:
                self._values["key"] = key
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-s3location.html#cfn-serverless-api-s3location-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-s3location.html#cfn-serverless-api-s3location-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-api-s3location.html#cfn-serverless-api-s3location-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnApplicationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "notification_arns": "notificationArns",
        "parameters": "parameters",
        "tags": "tags",
        "timeout_in_minutes": "timeoutInMinutes",
    },
)
class CfnApplicationMixinProps:
    def __init__(
        self,
        *,
        location: typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ApplicationLocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for CfnApplicationPropsMixin.

        :param location: 
        :param notification_arns: 
        :param parameters: 
        :param tags: 
        :param timeout_in_minutes: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
            
            cfn_application_mixin_props = sam_mixins.CfnApplicationMixinProps(
                location="location",
                notification_arns=["notificationArns"],
                parameters={
                    "parameters_key": "parameters"
                },
                tags={
                    "tags_key": "tags"
                },
                timeout_in_minutes=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__031630f98408daca16f032fa6fcd6d4121c52d5018ccff3a62850ca0564369be)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument notification_arns", value=notification_arns, expected_type=type_hints["notification_arns"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeout_in_minutes", value=timeout_in_minutes, expected_type=type_hints["timeout_in_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if location is not None:
            self._values["location"] = location
        if notification_arns is not None:
            self._values["notification_arns"] = notification_arns
        if parameters is not None:
            self._values["parameters"] = parameters
        if tags is not None:
            self._values["tags"] = tags
        if timeout_in_minutes is not None:
            self._values["timeout_in_minutes"] = timeout_in_minutes

    @builtins.property
    def location(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApplicationLocationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-application.html#cfn-serverless-application-location
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApplicationLocationProperty"]], result)

    @builtins.property
    def notification_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-application.html#cfn-serverless-application-notificationarns
        '''
        result = self._values.get("notification_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-application.html#cfn-serverless-application-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-application.html#cfn-serverless-application-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-application.html#cfn-serverless-application-timeoutinminutes
        '''
        result = self._values.get("timeout_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnApplicationPropsMixin",
):
    '''https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-application.html
    :cloudformationResource: AWS::Serverless::Application
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
        
        cfn_application_props_mixin = sam_mixins.CfnApplicationPropsMixin(sam_mixins.CfnApplicationMixinProps(
            location="location",
            notification_arns=["notificationArns"],
            parameters={
                "parameters_key": "parameters"
            },
            tags={
                "tags_key": "tags"
            },
            timeout_in_minutes=123
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
        '''Create a mixin to apply properties to ``AWS::Serverless::Application``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3adbb999472478978c40f0b3e080dd8cdb7268d45178071d99cc42b5ec328f0d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__904b660f14ebb3f08d33f206b5d6dbb81f72186f68ca1051d312f1599fdcd1cb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f47b3f2016f5c0ec0f5b368ff36f3fc1acc9e241b680f21f6942082653e5c3f0)
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
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnApplicationPropsMixin.ApplicationLocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_id": "applicationId",
            "semantic_version": "semanticVersion",
        },
    )
    class ApplicationLocationProperty:
        def __init__(
            self,
            *,
            application_id: typing.Optional[builtins.str] = None,
            semantic_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param application_id: 
            :param semantic_version: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-application-applicationlocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                application_location_property = sam_mixins.CfnApplicationPropsMixin.ApplicationLocationProperty(
                    application_id="applicationId",
                    semantic_version="semanticVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__56bd3042739fbe8579d818a4846d22978f8bfdaa9b6b28ebca93cd63cb021159)
                check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
                check_type(argname="argument semantic_version", value=semantic_version, expected_type=type_hints["semantic_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_id is not None:
                self._values["application_id"] = application_id
            if semantic_version is not None:
                self._values["semantic_version"] = semantic_version

        @builtins.property
        def application_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-application-applicationlocation.html#cfn-serverless-application-applicationlocation-applicationid
            '''
            result = self._values.get("application_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def semantic_version(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-application-applicationlocation.html#cfn-serverless-application-applicationlocation-semanticversion
            '''
            result = self._values.get("semantic_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "architectures": "architectures",
        "assume_role_policy_document": "assumeRolePolicyDocument",
        "auto_publish_alias": "autoPublishAlias",
        "auto_publish_code_sha256": "autoPublishCodeSha256",
        "code_signing_config_arn": "codeSigningConfigArn",
        "code_uri": "codeUri",
        "dead_letter_queue": "deadLetterQueue",
        "deployment_preference": "deploymentPreference",
        "description": "description",
        "environment": "environment",
        "ephemeral_storage": "ephemeralStorage",
        "event_invoke_config": "eventInvokeConfig",
        "events": "events",
        "file_system_configs": "fileSystemConfigs",
        "function_name": "functionName",
        "function_url_config": "functionUrlConfig",
        "handler": "handler",
        "image_config": "imageConfig",
        "image_uri": "imageUri",
        "inline_code": "inlineCode",
        "kms_key_arn": "kmsKeyArn",
        "layers": "layers",
        "memory_size": "memorySize",
        "package_type": "packageType",
        "permissions_boundary": "permissionsBoundary",
        "policies": "policies",
        "provisioned_concurrency_config": "provisionedConcurrencyConfig",
        "reserved_concurrent_executions": "reservedConcurrentExecutions",
        "role": "role",
        "runtime": "runtime",
        "tags": "tags",
        "timeout": "timeout",
        "tracing": "tracing",
        "version_description": "versionDescription",
        "vpc_config": "vpcConfig",
    },
)
class CfnFunctionMixinProps:
    def __init__(
        self,
        *,
        architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
        assume_role_policy_document: typing.Any = None,
        auto_publish_alias: typing.Optional[builtins.str] = None,
        auto_publish_code_sha256: typing.Optional[builtins.str] = None,
        code_signing_config_arn: typing.Optional[builtins.str] = None,
        code_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        dead_letter_queue: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.DeadLetterQueueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        deployment_preference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.DeploymentPreferenceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.FunctionEnvironmentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ephemeral_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.EphemeralStorageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        event_invoke_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.EventInvokeConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.EventSourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        file_system_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.FileSystemConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        function_name: typing.Optional[builtins.str] = None,
        function_url_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.FunctionUrlConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        handler: typing.Optional[builtins.str] = None,
        image_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.ImageConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        image_uri: typing.Optional[builtins.str] = None,
        inline_code: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        layers: typing.Optional[typing.Sequence[builtins.str]] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        package_type: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.IAMPolicyDocumentProperty", typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.IAMPolicyDocumentProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunctionPropsMixin.SAMPolicyTemplateProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        provisioned_concurrency_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.ProvisionedConcurrencyConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        tracing: typing.Optional[builtins.str] = None,
        version_description: typing.Optional[builtins.str] = None,
        vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.VpcConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnFunctionPropsMixin.

        :param architectures: 
        :param assume_role_policy_document: 
        :param auto_publish_alias: 
        :param auto_publish_code_sha256: 
        :param code_signing_config_arn: 
        :param code_uri: 
        :param dead_letter_queue: 
        :param deployment_preference: 
        :param description: 
        :param environment: 
        :param ephemeral_storage: 
        :param event_invoke_config: 
        :param events: 
        :param file_system_configs: 
        :param function_name: 
        :param function_url_config: 
        :param handler: 
        :param image_config: 
        :param image_uri: 
        :param inline_code: 
        :param kms_key_arn: 
        :param layers: 
        :param memory_size: 
        :param package_type: 
        :param permissions_boundary: 
        :param policies: 
        :param provisioned_concurrency_config: 
        :param reserved_concurrent_executions: 
        :param role: 
        :param runtime: 
        :param tags: 
        :param timeout: 
        :param tracing: 
        :param version_description: 
        :param vpc_config: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
            
            # assume_role_policy_document: Any
            
            cfn_function_mixin_props = sam_mixins.CfnFunctionMixinProps(
                architectures=["architectures"],
                assume_role_policy_document=assume_role_policy_document,
                auto_publish_alias="autoPublishAlias",
                auto_publish_code_sha256="autoPublishCodeSha256",
                code_signing_config_arn="codeSigningConfigArn",
                code_uri="codeUri",
                dead_letter_queue=sam_mixins.CfnFunctionPropsMixin.DeadLetterQueueProperty(
                    target_arn="targetArn",
                    type="type"
                ),
                deployment_preference=sam_mixins.CfnFunctionPropsMixin.DeploymentPreferenceProperty(
                    alarms=["alarms"],
                    enabled=False,
                    hooks=sam_mixins.CfnFunctionPropsMixin.HooksProperty(
                        post_traffic="postTraffic",
                        pre_traffic="preTraffic"
                    ),
                    role="role",
                    type="type"
                ),
                description="description",
                environment=sam_mixins.CfnFunctionPropsMixin.FunctionEnvironmentProperty(
                    variables={
                        "variables_key": "variables"
                    }
                ),
                ephemeral_storage=sam_mixins.CfnFunctionPropsMixin.EphemeralStorageProperty(
                    size=123
                ),
                event_invoke_config=sam_mixins.CfnFunctionPropsMixin.EventInvokeConfigProperty(
                    destination_config=sam_mixins.CfnFunctionPropsMixin.EventInvokeDestinationConfigProperty(
                        on_failure=sam_mixins.CfnFunctionPropsMixin.DestinationProperty(
                            destination="destination",
                            type="type"
                        ),
                        on_success=sam_mixins.CfnFunctionPropsMixin.DestinationProperty(
                            destination="destination",
                            type="type"
                        )
                    ),
                    maximum_event_age_in_seconds=123,
                    maximum_retry_attempts=123
                ),
                events={
                    "events_key": sam_mixins.CfnFunctionPropsMixin.EventSourceProperty(
                        properties=sam_mixins.CfnFunctionPropsMixin.AlexaSkillEventProperty(
                            skill_id="skillId"
                        ),
                        type="type"
                    )
                },
                file_system_configs=[sam_mixins.CfnFunctionPropsMixin.FileSystemConfigProperty(
                    arn="arn",
                    local_mount_path="localMountPath"
                )],
                function_name="functionName",
                function_url_config=sam_mixins.CfnFunctionPropsMixin.FunctionUrlConfigProperty(
                    auth_type="authType",
                    cors="cors",
                    invoke_mode="invokeMode"
                ),
                handler="handler",
                image_config=sam_mixins.CfnFunctionPropsMixin.ImageConfigProperty(
                    command=["command"],
                    entry_point=["entryPoint"],
                    working_directory="workingDirectory"
                ),
                image_uri="imageUri",
                inline_code="inlineCode",
                kms_key_arn="kmsKeyArn",
                layers=["layers"],
                memory_size=123,
                package_type="packageType",
                permissions_boundary="permissionsBoundary",
                policies="policies",
                provisioned_concurrency_config=sam_mixins.CfnFunctionPropsMixin.ProvisionedConcurrencyConfigProperty(
                    provisioned_concurrent_executions="provisionedConcurrentExecutions"
                ),
                reserved_concurrent_executions=123,
                role="role",
                runtime="runtime",
                tags={
                    "tags_key": "tags"
                },
                timeout=123,
                tracing="tracing",
                version_description="versionDescription",
                vpc_config=sam_mixins.CfnFunctionPropsMixin.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68c9e2f4743f083f6d616dc861c7a877316d8b6330037fbdd98813faa1b0e60e)
            check_type(argname="argument architectures", value=architectures, expected_type=type_hints["architectures"])
            check_type(argname="argument assume_role_policy_document", value=assume_role_policy_document, expected_type=type_hints["assume_role_policy_document"])
            check_type(argname="argument auto_publish_alias", value=auto_publish_alias, expected_type=type_hints["auto_publish_alias"])
            check_type(argname="argument auto_publish_code_sha256", value=auto_publish_code_sha256, expected_type=type_hints["auto_publish_code_sha256"])
            check_type(argname="argument code_signing_config_arn", value=code_signing_config_arn, expected_type=type_hints["code_signing_config_arn"])
            check_type(argname="argument code_uri", value=code_uri, expected_type=type_hints["code_uri"])
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument deployment_preference", value=deployment_preference, expected_type=type_hints["deployment_preference"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument ephemeral_storage", value=ephemeral_storage, expected_type=type_hints["ephemeral_storage"])
            check_type(argname="argument event_invoke_config", value=event_invoke_config, expected_type=type_hints["event_invoke_config"])
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument file_system_configs", value=file_system_configs, expected_type=type_hints["file_system_configs"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument function_url_config", value=function_url_config, expected_type=type_hints["function_url_config"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument image_config", value=image_config, expected_type=type_hints["image_config"])
            check_type(argname="argument image_uri", value=image_uri, expected_type=type_hints["image_uri"])
            check_type(argname="argument inline_code", value=inline_code, expected_type=type_hints["inline_code"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument layers", value=layers, expected_type=type_hints["layers"])
            check_type(argname="argument memory_size", value=memory_size, expected_type=type_hints["memory_size"])
            check_type(argname="argument package_type", value=package_type, expected_type=type_hints["package_type"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
            check_type(argname="argument provisioned_concurrency_config", value=provisioned_concurrency_config, expected_type=type_hints["provisioned_concurrency_config"])
            check_type(argname="argument reserved_concurrent_executions", value=reserved_concurrent_executions, expected_type=type_hints["reserved_concurrent_executions"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument tracing", value=tracing, expected_type=type_hints["tracing"])
            check_type(argname="argument version_description", value=version_description, expected_type=type_hints["version_description"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if architectures is not None:
            self._values["architectures"] = architectures
        if assume_role_policy_document is not None:
            self._values["assume_role_policy_document"] = assume_role_policy_document
        if auto_publish_alias is not None:
            self._values["auto_publish_alias"] = auto_publish_alias
        if auto_publish_code_sha256 is not None:
            self._values["auto_publish_code_sha256"] = auto_publish_code_sha256
        if code_signing_config_arn is not None:
            self._values["code_signing_config_arn"] = code_signing_config_arn
        if code_uri is not None:
            self._values["code_uri"] = code_uri
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if deployment_preference is not None:
            self._values["deployment_preference"] = deployment_preference
        if description is not None:
            self._values["description"] = description
        if environment is not None:
            self._values["environment"] = environment
        if ephemeral_storage is not None:
            self._values["ephemeral_storage"] = ephemeral_storage
        if event_invoke_config is not None:
            self._values["event_invoke_config"] = event_invoke_config
        if events is not None:
            self._values["events"] = events
        if file_system_configs is not None:
            self._values["file_system_configs"] = file_system_configs
        if function_name is not None:
            self._values["function_name"] = function_name
        if function_url_config is not None:
            self._values["function_url_config"] = function_url_config
        if handler is not None:
            self._values["handler"] = handler
        if image_config is not None:
            self._values["image_config"] = image_config
        if image_uri is not None:
            self._values["image_uri"] = image_uri
        if inline_code is not None:
            self._values["inline_code"] = inline_code
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if layers is not None:
            self._values["layers"] = layers
        if memory_size is not None:
            self._values["memory_size"] = memory_size
        if package_type is not None:
            self._values["package_type"] = package_type
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if policies is not None:
            self._values["policies"] = policies
        if provisioned_concurrency_config is not None:
            self._values["provisioned_concurrency_config"] = provisioned_concurrency_config
        if reserved_concurrent_executions is not None:
            self._values["reserved_concurrent_executions"] = reserved_concurrent_executions
        if role is not None:
            self._values["role"] = role
        if runtime is not None:
            self._values["runtime"] = runtime
        if tags is not None:
            self._values["tags"] = tags
        if timeout is not None:
            self._values["timeout"] = timeout
        if tracing is not None:
            self._values["tracing"] = tracing
        if version_description is not None:
            self._values["version_description"] = version_description
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def architectures(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-architectures
        '''
        result = self._values.get("architectures")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def assume_role_policy_document(self) -> typing.Any:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-assumerolepolicydocument
        '''
        result = self._values.get("assume_role_policy_document")
        return typing.cast(typing.Any, result)

    @builtins.property
    def auto_publish_alias(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-autopublishalias
        '''
        result = self._values.get("auto_publish_alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_publish_code_sha256(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-autopublishcodesha256
        '''
        result = self._values.get("auto_publish_code_sha256")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_signing_config_arn(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-codesigningconfigarn
        '''
        result = self._values.get("code_signing_config_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.S3LocationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-codeuri
        '''
        result = self._values.get("code_uri")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.S3LocationProperty"]], result)

    @builtins.property
    def dead_letter_queue(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.DeadLetterQueueProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-deadletterqueue
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.DeadLetterQueueProperty"]], result)

    @builtins.property
    def deployment_preference(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.DeploymentPreferenceProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-deploymentpreference
        '''
        result = self._values.get("deployment_preference")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.DeploymentPreferenceProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.FunctionEnvironmentProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-environment
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.FunctionEnvironmentProperty"]], result)

    @builtins.property
    def ephemeral_storage(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EphemeralStorageProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-ephemeralstorage
        '''
        result = self._values.get("ephemeral_storage")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EphemeralStorageProperty"]], result)

    @builtins.property
    def event_invoke_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EventInvokeConfigProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-eventinvokeconfig
        '''
        result = self._values.get("event_invoke_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EventInvokeConfigProperty"]], result)

    @builtins.property
    def events(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EventSourceProperty"]]]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-events
        '''
        result = self._values.get("events")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EventSourceProperty"]]]], result)

    @builtins.property
    def file_system_configs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.FileSystemConfigProperty"]]]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-filesystemconfigs
        '''
        result = self._values.get("file_system_configs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.FileSystemConfigProperty"]]]], result)

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-functionname
        '''
        result = self._values.get("function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def function_url_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.FunctionUrlConfigProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-functionurlconfig
        '''
        result = self._values.get("function_url_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.FunctionUrlConfigProperty"]], result)

    @builtins.property
    def handler(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-handler
        '''
        result = self._values.get("handler")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.ImageConfigProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-imageconfig
        '''
        result = self._values.get("image_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.ImageConfigProperty"]], result)

    @builtins.property
    def image_uri(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-imageuri
        '''
        result = self._values.get("image_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inline_code(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-inlinecode
        '''
        result = self._values.get("inline_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-kmskeyarn
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def layers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-layers
        '''
        result = self._values.get("layers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-memorysize
        '''
        result = self._values.get("memory_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def package_type(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-packagetype
        '''
        result = self._values.get("package_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundary(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-permissionsboundary
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policies(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.IAMPolicyDocumentProperty", typing.List[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.IAMPolicyDocumentProperty", "CfnFunctionPropsMixin.SAMPolicyTemplateProperty"]]]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-policies
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.IAMPolicyDocumentProperty", typing.List[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.IAMPolicyDocumentProperty", "CfnFunctionPropsMixin.SAMPolicyTemplateProperty"]]]], result)

    @builtins.property
    def provisioned_concurrency_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.ProvisionedConcurrencyConfigProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-provisionedconcurrencyconfig
        '''
        result = self._values.get("provisioned_concurrency_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.ProvisionedConcurrencyConfigProperty"]], result)

    @builtins.property
    def reserved_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-reservedconcurrentexecutions
        '''
        result = self._values.get("reserved_concurrent_executions")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-role
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-runtime
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-timeout
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tracing(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-tracing
        '''
        result = self._values.get("tracing")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_description(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-versiondescription
        '''
        result = self._values.get("version_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.VpcConfigProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html#cfn-serverless-function-vpcconfig
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.VpcConfigProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFunctionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFunctionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin",
):
    '''https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-function.html
    :cloudformationResource: AWS::Serverless::Function
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
        
        # assume_role_policy_document: Any
        
        cfn_function_props_mixin = sam_mixins.CfnFunctionPropsMixin(sam_mixins.CfnFunctionMixinProps(
            architectures=["architectures"],
            assume_role_policy_document=assume_role_policy_document,
            auto_publish_alias="autoPublishAlias",
            auto_publish_code_sha256="autoPublishCodeSha256",
            code_signing_config_arn="codeSigningConfigArn",
            code_uri="codeUri",
            dead_letter_queue=sam_mixins.CfnFunctionPropsMixin.DeadLetterQueueProperty(
                target_arn="targetArn",
                type="type"
            ),
            deployment_preference=sam_mixins.CfnFunctionPropsMixin.DeploymentPreferenceProperty(
                alarms=["alarms"],
                enabled=False,
                hooks=sam_mixins.CfnFunctionPropsMixin.HooksProperty(
                    post_traffic="postTraffic",
                    pre_traffic="preTraffic"
                ),
                role="role",
                type="type"
            ),
            description="description",
            environment=sam_mixins.CfnFunctionPropsMixin.FunctionEnvironmentProperty(
                variables={
                    "variables_key": "variables"
                }
            ),
            ephemeral_storage=sam_mixins.CfnFunctionPropsMixin.EphemeralStorageProperty(
                size=123
            ),
            event_invoke_config=sam_mixins.CfnFunctionPropsMixin.EventInvokeConfigProperty(
                destination_config=sam_mixins.CfnFunctionPropsMixin.EventInvokeDestinationConfigProperty(
                    on_failure=sam_mixins.CfnFunctionPropsMixin.DestinationProperty(
                        destination="destination",
                        type="type"
                    ),
                    on_success=sam_mixins.CfnFunctionPropsMixin.DestinationProperty(
                        destination="destination",
                        type="type"
                    )
                ),
                maximum_event_age_in_seconds=123,
                maximum_retry_attempts=123
            ),
            events={
                "events_key": sam_mixins.CfnFunctionPropsMixin.EventSourceProperty(
                    properties=sam_mixins.CfnFunctionPropsMixin.AlexaSkillEventProperty(
                        skill_id="skillId"
                    ),
                    type="type"
                )
            },
            file_system_configs=[sam_mixins.CfnFunctionPropsMixin.FileSystemConfigProperty(
                arn="arn",
                local_mount_path="localMountPath"
            )],
            function_name="functionName",
            function_url_config=sam_mixins.CfnFunctionPropsMixin.FunctionUrlConfigProperty(
                auth_type="authType",
                cors="cors",
                invoke_mode="invokeMode"
            ),
            handler="handler",
            image_config=sam_mixins.CfnFunctionPropsMixin.ImageConfigProperty(
                command=["command"],
                entry_point=["entryPoint"],
                working_directory="workingDirectory"
            ),
            image_uri="imageUri",
            inline_code="inlineCode",
            kms_key_arn="kmsKeyArn",
            layers=["layers"],
            memory_size=123,
            package_type="packageType",
            permissions_boundary="permissionsBoundary",
            policies="policies",
            provisioned_concurrency_config=sam_mixins.CfnFunctionPropsMixin.ProvisionedConcurrencyConfigProperty(
                provisioned_concurrent_executions="provisionedConcurrentExecutions"
            ),
            reserved_concurrent_executions=123,
            role="role",
            runtime="runtime",
            tags={
                "tags_key": "tags"
            },
            timeout=123,
            tracing="tracing",
            version_description="versionDescription",
            vpc_config=sam_mixins.CfnFunctionPropsMixin.VpcConfigProperty(
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"]
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnFunctionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Serverless::Function``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8a2393b278c08631e7b20ebc8c4b297b7b63a877d42cf039f2624f084f8c2df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f28a086dcf8465e78313f1de309faf508178e3f57daf9700bfc1fae0844c3134)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f94f1f847971e0cb78d98b6396ee3cd3797c4800e7535db49675a2766689a5c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFunctionMixinProps:
        return typing.cast(CfnFunctionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.AlexaSkillEventProperty",
        jsii_struct_bases=[],
        name_mapping={"skill_id": "skillId"},
    )
    class AlexaSkillEventProperty:
        def __init__(self, *, skill_id: typing.Optional[builtins.str] = None) -> None:
            '''
            :param skill_id: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-alexaskillevent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                alexa_skill_event_property = sam_mixins.CfnFunctionPropsMixin.AlexaSkillEventProperty(
                    skill_id="skillId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9fe595f271c198b097774166355d22fc09bef6e58c69bc4a582bb7d30ceec6d4)
                check_type(argname="argument skill_id", value=skill_id, expected_type=type_hints["skill_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if skill_id is not None:
                self._values["skill_id"] = skill_id

        @builtins.property
        def skill_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-alexaskillevent.html#cfn-serverless-function-alexaskillevent-skillid
            '''
            result = self._values.get("skill_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlexaSkillEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.ApiEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auth": "auth",
            "method": "method",
            "path": "path",
            "request_model": "requestModel",
            "request_parameters": "requestParameters",
            "rest_api_id": "restApiId",
        },
    )
    class ApiEventProperty:
        def __init__(
            self,
            *,
            auth: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.AuthProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            method: typing.Optional[builtins.str] = None,
            path: typing.Optional[builtins.str] = None,
            request_model: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.RequestModelProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            request_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.RequestParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            rest_api_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param auth: 
            :param method: 
            :param path: 
            :param request_model: 
            :param request_parameters: 
            :param rest_api_id: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-apievent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                # custom_statements: Any
                
                api_event_property = sam_mixins.CfnFunctionPropsMixin.ApiEventProperty(
                    auth=sam_mixins.CfnFunctionPropsMixin.AuthProperty(
                        api_key_required=False,
                        authorization_scopes=["authorizationScopes"],
                        authorizer="authorizer",
                        resource_policy=sam_mixins.CfnFunctionPropsMixin.AuthResourcePolicyProperty(
                            aws_account_blacklist=["awsAccountBlacklist"],
                            aws_account_whitelist=["awsAccountWhitelist"],
                            custom_statements=[custom_statements],
                            intrinsic_vpc_blacklist=["intrinsicVpcBlacklist"],
                            intrinsic_vpce_blacklist=["intrinsicVpceBlacklist"],
                            intrinsic_vpce_whitelist=["intrinsicVpceWhitelist"],
                            intrinsic_vpc_whitelist=["intrinsicVpcWhitelist"],
                            ip_range_blacklist=["ipRangeBlacklist"],
                            ip_range_whitelist=["ipRangeWhitelist"],
                            source_vpc_blacklist=["sourceVpcBlacklist"],
                            source_vpc_whitelist=["sourceVpcWhitelist"]
                        )
                    ),
                    method="method",
                    path="path",
                    request_model=sam_mixins.CfnFunctionPropsMixin.RequestModelProperty(
                        model="model",
                        required=False,
                        validate_body=False,
                        validate_parameters=False
                    ),
                    request_parameters=["requestParameters"],
                    rest_api_id="restApiId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__02a7332716c9cd5a819ddbe2c0945eea50ab4afb2a2f914ccbb224e71326cf44)
                check_type(argname="argument auth", value=auth, expected_type=type_hints["auth"])
                check_type(argname="argument method", value=method, expected_type=type_hints["method"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument request_model", value=request_model, expected_type=type_hints["request_model"])
                check_type(argname="argument request_parameters", value=request_parameters, expected_type=type_hints["request_parameters"])
                check_type(argname="argument rest_api_id", value=rest_api_id, expected_type=type_hints["rest_api_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auth is not None:
                self._values["auth"] = auth
            if method is not None:
                self._values["method"] = method
            if path is not None:
                self._values["path"] = path
            if request_model is not None:
                self._values["request_model"] = request_model
            if request_parameters is not None:
                self._values["request_parameters"] = request_parameters
            if rest_api_id is not None:
                self._values["rest_api_id"] = rest_api_id

        @builtins.property
        def auth(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.AuthProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-apievent.html#cfn-serverless-function-apievent-auth
            '''
            result = self._values.get("auth")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.AuthProperty"]], result)

        @builtins.property
        def method(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-apievent.html#cfn-serverless-function-apievent-method
            '''
            result = self._values.get("method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-apievent.html#cfn-serverless-function-apievent-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def request_model(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.RequestModelProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-apievent.html#cfn-serverless-function-apievent-requestmodel
            '''
            result = self._values.get("request_model")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.RequestModelProperty"]], result)

        @builtins.property
        def request_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.RequestParameterProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-apievent.html#cfn-serverless-function-apievent-requestparameters
            '''
            result = self._values.get("request_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.RequestParameterProperty"]]]], result)

        @builtins.property
        def rest_api_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-apievent.html#cfn-serverless-function-apievent-restapiid
            '''
            result = self._values.get("rest_api_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApiEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.AuthProperty",
        jsii_struct_bases=[],
        name_mapping={
            "api_key_required": "apiKeyRequired",
            "authorization_scopes": "authorizationScopes",
            "authorizer": "authorizer",
            "resource_policy": "resourcePolicy",
        },
    )
    class AuthProperty:
        def __init__(
            self,
            *,
            api_key_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
            authorizer: typing.Optional[builtins.str] = None,
            resource_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.AuthResourcePolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param api_key_required: 
            :param authorization_scopes: 
            :param authorizer: 
            :param resource_policy: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-auth.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                # custom_statements: Any
                
                auth_property = sam_mixins.CfnFunctionPropsMixin.AuthProperty(
                    api_key_required=False,
                    authorization_scopes=["authorizationScopes"],
                    authorizer="authorizer",
                    resource_policy=sam_mixins.CfnFunctionPropsMixin.AuthResourcePolicyProperty(
                        aws_account_blacklist=["awsAccountBlacklist"],
                        aws_account_whitelist=["awsAccountWhitelist"],
                        custom_statements=[custom_statements],
                        intrinsic_vpc_blacklist=["intrinsicVpcBlacklist"],
                        intrinsic_vpce_blacklist=["intrinsicVpceBlacklist"],
                        intrinsic_vpce_whitelist=["intrinsicVpceWhitelist"],
                        intrinsic_vpc_whitelist=["intrinsicVpcWhitelist"],
                        ip_range_blacklist=["ipRangeBlacklist"],
                        ip_range_whitelist=["ipRangeWhitelist"],
                        source_vpc_blacklist=["sourceVpcBlacklist"],
                        source_vpc_whitelist=["sourceVpcWhitelist"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b278908bc5ebe1101993002907daba533991858c50a9d07d1b5f25cba0d01443)
                check_type(argname="argument api_key_required", value=api_key_required, expected_type=type_hints["api_key_required"])
                check_type(argname="argument authorization_scopes", value=authorization_scopes, expected_type=type_hints["authorization_scopes"])
                check_type(argname="argument authorizer", value=authorizer, expected_type=type_hints["authorizer"])
                check_type(argname="argument resource_policy", value=resource_policy, expected_type=type_hints["resource_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if api_key_required is not None:
                self._values["api_key_required"] = api_key_required
            if authorization_scopes is not None:
                self._values["authorization_scopes"] = authorization_scopes
            if authorizer is not None:
                self._values["authorizer"] = authorizer
            if resource_policy is not None:
                self._values["resource_policy"] = resource_policy

        @builtins.property
        def api_key_required(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-auth.html#cfn-serverless-function-auth-apikeyrequired
            '''
            result = self._values.get("api_key_required")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def authorization_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-auth.html#cfn-serverless-function-auth-authorizationscopes
            '''
            result = self._values.get("authorization_scopes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def authorizer(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-auth.html#cfn-serverless-function-auth-authorizer
            '''
            result = self._values.get("authorizer")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.AuthResourcePolicyProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-auth.html#cfn-serverless-function-auth-resourcepolicy
            '''
            result = self._values.get("resource_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.AuthResourcePolicyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.AuthResourcePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aws_account_blacklist": "awsAccountBlacklist",
            "aws_account_whitelist": "awsAccountWhitelist",
            "custom_statements": "customStatements",
            "intrinsic_vpc_blacklist": "intrinsicVpcBlacklist",
            "intrinsic_vpce_blacklist": "intrinsicVpceBlacklist",
            "intrinsic_vpce_whitelist": "intrinsicVpceWhitelist",
            "intrinsic_vpc_whitelist": "intrinsicVpcWhitelist",
            "ip_range_blacklist": "ipRangeBlacklist",
            "ip_range_whitelist": "ipRangeWhitelist",
            "source_vpc_blacklist": "sourceVpcBlacklist",
            "source_vpc_whitelist": "sourceVpcWhitelist",
        },
    )
    class AuthResourcePolicyProperty:
        def __init__(
            self,
            *,
            aws_account_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
            aws_account_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
            custom_statements: typing.Optional[typing.Union[typing.Sequence[typing.Any], _aws_cdk_ceddda9d.IResolvable]] = None,
            intrinsic_vpc_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
            intrinsic_vpce_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
            intrinsic_vpce_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
            intrinsic_vpc_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
            ip_range_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
            ip_range_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
            source_vpc_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
            source_vpc_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param aws_account_blacklist: 
            :param aws_account_whitelist: 
            :param custom_statements: 
            :param intrinsic_vpc_blacklist: 
            :param intrinsic_vpce_blacklist: 
            :param intrinsic_vpce_whitelist: 
            :param intrinsic_vpc_whitelist: 
            :param ip_range_blacklist: 
            :param ip_range_whitelist: 
            :param source_vpc_blacklist: 
            :param source_vpc_whitelist: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-authresourcepolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                # custom_statements: Any
                
                auth_resource_policy_property = sam_mixins.CfnFunctionPropsMixin.AuthResourcePolicyProperty(
                    aws_account_blacklist=["awsAccountBlacklist"],
                    aws_account_whitelist=["awsAccountWhitelist"],
                    custom_statements=[custom_statements],
                    intrinsic_vpc_blacklist=["intrinsicVpcBlacklist"],
                    intrinsic_vpce_blacklist=["intrinsicVpceBlacklist"],
                    intrinsic_vpce_whitelist=["intrinsicVpceWhitelist"],
                    intrinsic_vpc_whitelist=["intrinsicVpcWhitelist"],
                    ip_range_blacklist=["ipRangeBlacklist"],
                    ip_range_whitelist=["ipRangeWhitelist"],
                    source_vpc_blacklist=["sourceVpcBlacklist"],
                    source_vpc_whitelist=["sourceVpcWhitelist"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2e32fe8678dbd799c8c772a1ce12dd5fc48b76619af26163aa1f76c1af48f3c7)
                check_type(argname="argument aws_account_blacklist", value=aws_account_blacklist, expected_type=type_hints["aws_account_blacklist"])
                check_type(argname="argument aws_account_whitelist", value=aws_account_whitelist, expected_type=type_hints["aws_account_whitelist"])
                check_type(argname="argument custom_statements", value=custom_statements, expected_type=type_hints["custom_statements"])
                check_type(argname="argument intrinsic_vpc_blacklist", value=intrinsic_vpc_blacklist, expected_type=type_hints["intrinsic_vpc_blacklist"])
                check_type(argname="argument intrinsic_vpce_blacklist", value=intrinsic_vpce_blacklist, expected_type=type_hints["intrinsic_vpce_blacklist"])
                check_type(argname="argument intrinsic_vpce_whitelist", value=intrinsic_vpce_whitelist, expected_type=type_hints["intrinsic_vpce_whitelist"])
                check_type(argname="argument intrinsic_vpc_whitelist", value=intrinsic_vpc_whitelist, expected_type=type_hints["intrinsic_vpc_whitelist"])
                check_type(argname="argument ip_range_blacklist", value=ip_range_blacklist, expected_type=type_hints["ip_range_blacklist"])
                check_type(argname="argument ip_range_whitelist", value=ip_range_whitelist, expected_type=type_hints["ip_range_whitelist"])
                check_type(argname="argument source_vpc_blacklist", value=source_vpc_blacklist, expected_type=type_hints["source_vpc_blacklist"])
                check_type(argname="argument source_vpc_whitelist", value=source_vpc_whitelist, expected_type=type_hints["source_vpc_whitelist"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_account_blacklist is not None:
                self._values["aws_account_blacklist"] = aws_account_blacklist
            if aws_account_whitelist is not None:
                self._values["aws_account_whitelist"] = aws_account_whitelist
            if custom_statements is not None:
                self._values["custom_statements"] = custom_statements
            if intrinsic_vpc_blacklist is not None:
                self._values["intrinsic_vpc_blacklist"] = intrinsic_vpc_blacklist
            if intrinsic_vpce_blacklist is not None:
                self._values["intrinsic_vpce_blacklist"] = intrinsic_vpce_blacklist
            if intrinsic_vpce_whitelist is not None:
                self._values["intrinsic_vpce_whitelist"] = intrinsic_vpce_whitelist
            if intrinsic_vpc_whitelist is not None:
                self._values["intrinsic_vpc_whitelist"] = intrinsic_vpc_whitelist
            if ip_range_blacklist is not None:
                self._values["ip_range_blacklist"] = ip_range_blacklist
            if ip_range_whitelist is not None:
                self._values["ip_range_whitelist"] = ip_range_whitelist
            if source_vpc_blacklist is not None:
                self._values["source_vpc_blacklist"] = source_vpc_blacklist
            if source_vpc_whitelist is not None:
                self._values["source_vpc_whitelist"] = source_vpc_whitelist

        @builtins.property
        def aws_account_blacklist(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-authresourcepolicy.html#cfn-serverless-function-authresourcepolicy-awsaccountblacklist
            '''
            result = self._values.get("aws_account_blacklist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def aws_account_whitelist(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-authresourcepolicy.html#cfn-serverless-function-authresourcepolicy-awsaccountwhitelist
            '''
            result = self._values.get("aws_account_whitelist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def custom_statements(
            self,
        ) -> typing.Optional[typing.Union[typing.List[typing.Any], _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-authresourcepolicy.html#cfn-serverless-function-authresourcepolicy-customstatements
            '''
            result = self._values.get("custom_statements")
            return typing.cast(typing.Optional[typing.Union[typing.List[typing.Any], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def intrinsic_vpc_blacklist(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-authresourcepolicy.html#cfn-serverless-function-authresourcepolicy-intrinsicvpcblacklist
            '''
            result = self._values.get("intrinsic_vpc_blacklist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def intrinsic_vpce_blacklist(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-authresourcepolicy.html#cfn-serverless-function-authresourcepolicy-intrinsicvpceblacklist
            '''
            result = self._values.get("intrinsic_vpce_blacklist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def intrinsic_vpce_whitelist(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-authresourcepolicy.html#cfn-serverless-function-authresourcepolicy-intrinsicvpcewhitelist
            '''
            result = self._values.get("intrinsic_vpce_whitelist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def intrinsic_vpc_whitelist(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-authresourcepolicy.html#cfn-serverless-function-authresourcepolicy-intrinsicvpcwhitelist
            '''
            result = self._values.get("intrinsic_vpc_whitelist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def ip_range_blacklist(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-authresourcepolicy.html#cfn-serverless-function-authresourcepolicy-iprangeblacklist
            '''
            result = self._values.get("ip_range_blacklist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def ip_range_whitelist(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-authresourcepolicy.html#cfn-serverless-function-authresourcepolicy-iprangewhitelist
            '''
            result = self._values.get("ip_range_whitelist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def source_vpc_blacklist(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-authresourcepolicy.html#cfn-serverless-function-authresourcepolicy-sourcevpcblacklist
            '''
            result = self._values.get("source_vpc_blacklist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def source_vpc_whitelist(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-authresourcepolicy.html#cfn-serverless-function-authresourcepolicy-sourcevpcwhitelist
            '''
            result = self._values.get("source_vpc_whitelist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthResourcePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.BucketSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName"},
    )
    class BucketSAMPTProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param bucket_name: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-bucketsampt.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                bucket_sAMPTProperty = sam_mixins.CfnFunctionPropsMixin.BucketSAMPTProperty(
                    bucket_name="bucketName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d740b4a711b2c3eadfc302cb10fd3296bc09e62df5368a27500dcc85ecfc508e)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-bucketsampt.html#cfn-serverless-function-bucketsampt-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BucketSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.CloudWatchEventEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "input": "input",
            "input_path": "inputPath",
            "pattern": "pattern",
        },
    )
    class CloudWatchEventEventProperty:
        def __init__(
            self,
            *,
            input: typing.Optional[builtins.str] = None,
            input_path: typing.Optional[builtins.str] = None,
            pattern: typing.Any = None,
        ) -> None:
            '''
            :param input: 
            :param input_path: 
            :param pattern: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-cloudwatcheventevent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                # pattern: Any
                
                cloud_watch_event_event_property = sam_mixins.CfnFunctionPropsMixin.CloudWatchEventEventProperty(
                    input="input",
                    input_path="inputPath",
                    pattern=pattern
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9f991db682777c05a6de547dfa3019d52863882ae300803303f83dec974d333e)
                check_type(argname="argument input", value=input, expected_type=type_hints["input"])
                check_type(argname="argument input_path", value=input_path, expected_type=type_hints["input_path"])
                check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if input is not None:
                self._values["input"] = input
            if input_path is not None:
                self._values["input_path"] = input_path
            if pattern is not None:
                self._values["pattern"] = pattern

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-cloudwatcheventevent.html#cfn-serverless-function-cloudwatcheventevent-input
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_path(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-cloudwatcheventevent.html#cfn-serverless-function-cloudwatcheventevent-inputpath
            '''
            result = self._values.get("input_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pattern(self) -> typing.Any:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-cloudwatcheventevent.html#cfn-serverless-function-cloudwatcheventevent-pattern
            '''
            result = self._values.get("pattern")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchEventEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.CloudWatchLogsEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "filter_pattern": "filterPattern",
            "log_group_name": "logGroupName",
        },
    )
    class CloudWatchLogsEventProperty:
        def __init__(
            self,
            *,
            filter_pattern: typing.Optional[builtins.str] = None,
            log_group_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param filter_pattern: 
            :param log_group_name: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-cloudwatchlogsevent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                cloud_watch_logs_event_property = sam_mixins.CfnFunctionPropsMixin.CloudWatchLogsEventProperty(
                    filter_pattern="filterPattern",
                    log_group_name="logGroupName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__42ec2414ef539ee0a516f4383e5e08fb066eb33001b380df2c4c42b3a42cb1b3)
                check_type(argname="argument filter_pattern", value=filter_pattern, expected_type=type_hints["filter_pattern"])
                check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if filter_pattern is not None:
                self._values["filter_pattern"] = filter_pattern
            if log_group_name is not None:
                self._values["log_group_name"] = log_group_name

        @builtins.property
        def filter_pattern(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-cloudwatchlogsevent.html#cfn-serverless-function-cloudwatchlogsevent-filterpattern
            '''
            result = self._values.get("filter_pattern")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_group_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-cloudwatchlogsevent.html#cfn-serverless-function-cloudwatchlogsevent-loggroupname
            '''
            result = self._values.get("log_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.CognitoEventProperty",
        jsii_struct_bases=[],
        name_mapping={"trigger": "trigger", "user_pool": "userPool"},
    )
    class CognitoEventProperty:
        def __init__(
            self,
            *,
            trigger: typing.Optional[builtins.str] = None,
            user_pool: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param trigger: 
            :param user_pool: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-cognitoevent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                cognito_event_property = sam_mixins.CfnFunctionPropsMixin.CognitoEventProperty(
                    trigger="trigger",
                    user_pool="userPool"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4cd23864d2ecb83fa496813bb8cf1a848e35a3b1797fe3a63def419dbc7bea6a)
                check_type(argname="argument trigger", value=trigger, expected_type=type_hints["trigger"])
                check_type(argname="argument user_pool", value=user_pool, expected_type=type_hints["user_pool"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if trigger is not None:
                self._values["trigger"] = trigger
            if user_pool is not None:
                self._values["user_pool"] = user_pool

        @builtins.property
        def trigger(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-cognitoevent.html#cfn-serverless-function-cognitoevent-trigger
            '''
            result = self._values.get("trigger")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_pool(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-cognitoevent.html#cfn-serverless-function-cognitoevent-userpool
            '''
            result = self._values.get("user_pool")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CognitoEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.CollectionSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"collection_id": "collectionId"},
    )
    class CollectionSAMPTProperty:
        def __init__(
            self,
            *,
            collection_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param collection_id: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-collectionsampt.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                collection_sAMPTProperty = sam_mixins.CfnFunctionPropsMixin.CollectionSAMPTProperty(
                    collection_id="collectionId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__605d76f64d392af02dc1728613e62574893d8e9113b0216b86f72abc37dda33e)
                check_type(argname="argument collection_id", value=collection_id, expected_type=type_hints["collection_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if collection_id is not None:
                self._values["collection_id"] = collection_id

        @builtins.property
        def collection_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-collectionsampt.html#cfn-serverless-function-collectionsampt-collectionid
            '''
            result = self._values.get("collection_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CollectionSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.CorsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_credentials": "allowCredentials",
            "allow_headers": "allowHeaders",
            "allow_methods": "allowMethods",
            "allow_origin": "allowOrigin",
            "max_age": "maxAge",
        },
    )
    class CorsConfigurationProperty:
        def __init__(
            self,
            *,
            allow_credentials: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            allow_headers: typing.Optional[builtins.str] = None,
            allow_methods: typing.Optional[builtins.str] = None,
            allow_origin: typing.Optional[builtins.str] = None,
            max_age: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param allow_credentials: 
            :param allow_headers: 
            :param allow_methods: 
            :param allow_origin: 
            :param max_age: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-corsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                cors_configuration_property = sam_mixins.CfnFunctionPropsMixin.CorsConfigurationProperty(
                    allow_credentials=False,
                    allow_headers="allowHeaders",
                    allow_methods="allowMethods",
                    allow_origin="allowOrigin",
                    max_age="maxAge"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__24f62268b68a8590c24bc1c41d9c0e43df25c5dd8adb019dd5433eddc27bcd55)
                check_type(argname="argument allow_credentials", value=allow_credentials, expected_type=type_hints["allow_credentials"])
                check_type(argname="argument allow_headers", value=allow_headers, expected_type=type_hints["allow_headers"])
                check_type(argname="argument allow_methods", value=allow_methods, expected_type=type_hints["allow_methods"])
                check_type(argname="argument allow_origin", value=allow_origin, expected_type=type_hints["allow_origin"])
                check_type(argname="argument max_age", value=max_age, expected_type=type_hints["max_age"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allow_credentials is not None:
                self._values["allow_credentials"] = allow_credentials
            if allow_headers is not None:
                self._values["allow_headers"] = allow_headers
            if allow_methods is not None:
                self._values["allow_methods"] = allow_methods
            if allow_origin is not None:
                self._values["allow_origin"] = allow_origin
            if max_age is not None:
                self._values["max_age"] = max_age

        @builtins.property
        def allow_credentials(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-corsconfiguration.html#cfn-serverless-function-corsconfiguration-allowcredentials
            '''
            result = self._values.get("allow_credentials")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def allow_headers(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-corsconfiguration.html#cfn-serverless-function-corsconfiguration-allowheaders
            '''
            result = self._values.get("allow_headers")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def allow_methods(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-corsconfiguration.html#cfn-serverless-function-corsconfiguration-allowmethods
            '''
            result = self._values.get("allow_methods")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def allow_origin(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-corsconfiguration.html#cfn-serverless-function-corsconfiguration-alloworigin
            '''
            result = self._values.get("allow_origin")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_age(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-corsconfiguration.html#cfn-serverless-function-corsconfiguration-maxage
            '''
            result = self._values.get("max_age")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CorsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.DeadLetterQueueProperty",
        jsii_struct_bases=[],
        name_mapping={"target_arn": "targetArn", "type": "type"},
    )
    class DeadLetterQueueProperty:
        def __init__(
            self,
            *,
            target_arn: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param target_arn: 
            :param type: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-deadletterqueue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                dead_letter_queue_property = sam_mixins.CfnFunctionPropsMixin.DeadLetterQueueProperty(
                    target_arn="targetArn",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6370295d3d2bbf2fb560ec1ad24fe3b31c3662551dd92813fbbdfe133e6dd500)
                check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_arn is not None:
                self._values["target_arn"] = target_arn
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def target_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-deadletterqueue.html#cfn-serverless-function-deadletterqueue-targetarn
            '''
            result = self._values.get("target_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-deadletterqueue.html#cfn-serverless-function-deadletterqueue-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeadLetterQueueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.DeploymentPreferenceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alarms": "alarms",
            "enabled": "enabled",
            "hooks": "hooks",
            "role": "role",
            "type": "type",
        },
    )
    class DeploymentPreferenceProperty:
        def __init__(
            self,
            *,
            alarms: typing.Optional[typing.Sequence[builtins.str]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            hooks: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.HooksProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            role: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param alarms: 
            :param enabled: 
            :param hooks: 
            :param role: 
            :param type: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-deploymentpreference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                deployment_preference_property = sam_mixins.CfnFunctionPropsMixin.DeploymentPreferenceProperty(
                    alarms=["alarms"],
                    enabled=False,
                    hooks=sam_mixins.CfnFunctionPropsMixin.HooksProperty(
                        post_traffic="postTraffic",
                        pre_traffic="preTraffic"
                    ),
                    role="role",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a30b4d18679f2ce7e9717501b40f08bbc8d89c6bc19749d5d771ceff8e61ff1b)
                check_type(argname="argument alarms", value=alarms, expected_type=type_hints["alarms"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument hooks", value=hooks, expected_type=type_hints["hooks"])
                check_type(argname="argument role", value=role, expected_type=type_hints["role"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alarms is not None:
                self._values["alarms"] = alarms
            if enabled is not None:
                self._values["enabled"] = enabled
            if hooks is not None:
                self._values["hooks"] = hooks
            if role is not None:
                self._values["role"] = role
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def alarms(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-deploymentpreference.html#cfn-serverless-function-deploymentpreference-alarms
            '''
            result = self._values.get("alarms")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-deploymentpreference.html#cfn-serverless-function-deploymentpreference-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def hooks(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.HooksProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-deploymentpreference.html#cfn-serverless-function-deploymentpreference-hooks
            '''
            result = self._values.get("hooks")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.HooksProperty"]], result)

        @builtins.property
        def role(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-deploymentpreference.html#cfn-serverless-function-deploymentpreference-role
            '''
            result = self._values.get("role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-deploymentpreference.html#cfn-serverless-function-deploymentpreference-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentPreferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.DestinationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"on_failure": "onFailure"},
    )
    class DestinationConfigProperty:
        def __init__(
            self,
            *,
            on_failure: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.DestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param on_failure: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-destinationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                destination_config_property = sam_mixins.CfnFunctionPropsMixin.DestinationConfigProperty(
                    on_failure=sam_mixins.CfnFunctionPropsMixin.DestinationProperty(
                        destination="destination",
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f0cf65bbcdd5b657615335c38d2178f46d4b65d4fd0dc12829c9d44b55414f2f)
                check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if on_failure is not None:
                self._values["on_failure"] = on_failure

        @builtins.property
        def on_failure(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.DestinationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-destinationconfig.html#cfn-serverless-function-destinationconfig-onfailure
            '''
            result = self._values.get("on_failure")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.DestinationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.DestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination", "type": "type"},
    )
    class DestinationProperty:
        def __init__(
            self,
            *,
            destination: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param destination: 
            :param type: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-destination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                destination_property = sam_mixins.CfnFunctionPropsMixin.DestinationProperty(
                    destination="destination",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5d4d23b6809eb544fa53b41f63b0645e6ee842de6f3f2f6f4cb50ff2f632223a)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination is not None:
                self._values["destination"] = destination
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def destination(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-destination.html#cfn-serverless-function-destination-destination
            '''
            result = self._values.get("destination")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-destination.html#cfn-serverless-function-destination-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.DomainSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"domain_name": "domainName"},
    )
    class DomainSAMPTProperty:
        def __init__(
            self,
            *,
            domain_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param domain_name: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-domainsampt.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                domain_sAMPTProperty = sam_mixins.CfnFunctionPropsMixin.DomainSAMPTProperty(
                    domain_name="domainName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__256cc54477e28aea1d909cb738c1488c32b9e4eeebda64bb3f3fb9cb2ce76e41)
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain_name is not None:
                self._values["domain_name"] = domain_name

        @builtins.property
        def domain_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-domainsampt.html#cfn-serverless-function-domainsampt-domainname
            '''
            result = self._values.get("domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.DynamoDBEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "batch_size": "batchSize",
            "bisect_batch_on_function_error": "bisectBatchOnFunctionError",
            "destination_config": "destinationConfig",
            "enabled": "enabled",
            "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
            "maximum_record_age_in_seconds": "maximumRecordAgeInSeconds",
            "maximum_retry_attempts": "maximumRetryAttempts",
            "parallelization_factor": "parallelizationFactor",
            "starting_position": "startingPosition",
            "stream": "stream",
        },
    )
    class DynamoDBEventProperty:
        def __init__(
            self,
            *,
            batch_size: typing.Optional[jsii.Number] = None,
            bisect_batch_on_function_error: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            destination_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.DestinationConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
            maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
            maximum_retry_attempts: typing.Optional[jsii.Number] = None,
            parallelization_factor: typing.Optional[jsii.Number] = None,
            starting_position: typing.Optional[builtins.str] = None,
            stream: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param batch_size: 
            :param bisect_batch_on_function_error: 
            :param destination_config: 
            :param enabled: 
            :param maximum_batching_window_in_seconds: 
            :param maximum_record_age_in_seconds: 
            :param maximum_retry_attempts: 
            :param parallelization_factor: 
            :param starting_position: 
            :param stream: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-dynamodbevent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                dynamo_dBEvent_property = sam_mixins.CfnFunctionPropsMixin.DynamoDBEventProperty(
                    batch_size=123,
                    bisect_batch_on_function_error=False,
                    destination_config=sam_mixins.CfnFunctionPropsMixin.DestinationConfigProperty(
                        on_failure=sam_mixins.CfnFunctionPropsMixin.DestinationProperty(
                            destination="destination",
                            type="type"
                        )
                    ),
                    enabled=False,
                    maximum_batching_window_in_seconds=123,
                    maximum_record_age_in_seconds=123,
                    maximum_retry_attempts=123,
                    parallelization_factor=123,
                    starting_position="startingPosition",
                    stream="stream"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8bc0b3c229bf8d6164cf260c405aef73047bcec889e2562299aca9899a734219)
                check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
                check_type(argname="argument bisect_batch_on_function_error", value=bisect_batch_on_function_error, expected_type=type_hints["bisect_batch_on_function_error"])
                check_type(argname="argument destination_config", value=destination_config, expected_type=type_hints["destination_config"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
                check_type(argname="argument maximum_record_age_in_seconds", value=maximum_record_age_in_seconds, expected_type=type_hints["maximum_record_age_in_seconds"])
                check_type(argname="argument maximum_retry_attempts", value=maximum_retry_attempts, expected_type=type_hints["maximum_retry_attempts"])
                check_type(argname="argument parallelization_factor", value=parallelization_factor, expected_type=type_hints["parallelization_factor"])
                check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
                check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if batch_size is not None:
                self._values["batch_size"] = batch_size
            if bisect_batch_on_function_error is not None:
                self._values["bisect_batch_on_function_error"] = bisect_batch_on_function_error
            if destination_config is not None:
                self._values["destination_config"] = destination_config
            if enabled is not None:
                self._values["enabled"] = enabled
            if maximum_batching_window_in_seconds is not None:
                self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
            if maximum_record_age_in_seconds is not None:
                self._values["maximum_record_age_in_seconds"] = maximum_record_age_in_seconds
            if maximum_retry_attempts is not None:
                self._values["maximum_retry_attempts"] = maximum_retry_attempts
            if parallelization_factor is not None:
                self._values["parallelization_factor"] = parallelization_factor
            if starting_position is not None:
                self._values["starting_position"] = starting_position
            if stream is not None:
                self._values["stream"] = stream

        @builtins.property
        def batch_size(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-dynamodbevent.html#cfn-serverless-function-dynamodbevent-batchsize
            '''
            result = self._values.get("batch_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def bisect_batch_on_function_error(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-dynamodbevent.html#cfn-serverless-function-dynamodbevent-bisectbatchonfunctionerror
            '''
            result = self._values.get("bisect_batch_on_function_error")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def destination_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.DestinationConfigProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-dynamodbevent.html#cfn-serverless-function-dynamodbevent-destinationconfig
            '''
            result = self._values.get("destination_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.DestinationConfigProperty"]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-dynamodbevent.html#cfn-serverless-function-dynamodbevent-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-dynamodbevent.html#cfn-serverless-function-dynamodbevent-maximumbatchingwindowinseconds
            '''
            result = self._values.get("maximum_batching_window_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_record_age_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-dynamodbevent.html#cfn-serverless-function-dynamodbevent-maximumrecordageinseconds
            '''
            result = self._values.get("maximum_record_age_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-dynamodbevent.html#cfn-serverless-function-dynamodbevent-maximumretryattempts
            '''
            result = self._values.get("maximum_retry_attempts")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def parallelization_factor(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-dynamodbevent.html#cfn-serverless-function-dynamodbevent-parallelizationfactor
            '''
            result = self._values.get("parallelization_factor")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def starting_position(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-dynamodbevent.html#cfn-serverless-function-dynamodbevent-startingposition
            '''
            result = self._values.get("starting_position")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stream(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-dynamodbevent.html#cfn-serverless-function-dynamodbevent-stream
            '''
            result = self._values.get("stream")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynamoDBEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.EmptySAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={},
    )
    class EmptySAMPTProperty:
        def __init__(self) -> None:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-emptysampt.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                empty_sAMPTProperty = sam_mixins.CfnFunctionPropsMixin.EmptySAMPTProperty()
            '''
            self._values: typing.Dict[builtins.str, typing.Any] = {}

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EmptySAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.EphemeralStorageProperty",
        jsii_struct_bases=[],
        name_mapping={"size": "size"},
    )
    class EphemeralStorageProperty:
        def __init__(self, *, size: typing.Optional[jsii.Number] = None) -> None:
            '''
            :param size: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-ephemeralstorage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                ephemeral_storage_property = sam_mixins.CfnFunctionPropsMixin.EphemeralStorageProperty(
                    size=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__01548c74543eeb65af42af0f812ec0566bddb43c12678c9dd66cb8fbd36e8b82)
                check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if size is not None:
                self._values["size"] = size

        @builtins.property
        def size(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-ephemeralstorage.html#cfn-serverless-function-ephemeralstorage-size
            '''
            result = self._values.get("size")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EphemeralStorageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.EventBridgeRuleEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "event_bus_name": "eventBusName",
            "input": "input",
            "input_path": "inputPath",
            "pattern": "pattern",
        },
    )
    class EventBridgeRuleEventProperty:
        def __init__(
            self,
            *,
            event_bus_name: typing.Optional[builtins.str] = None,
            input: typing.Optional[builtins.str] = None,
            input_path: typing.Optional[builtins.str] = None,
            pattern: typing.Any = None,
        ) -> None:
            '''
            :param event_bus_name: 
            :param input: 
            :param input_path: 
            :param pattern: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-eventbridgeruleevent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                # pattern: Any
                
                event_bridge_rule_event_property = sam_mixins.CfnFunctionPropsMixin.EventBridgeRuleEventProperty(
                    event_bus_name="eventBusName",
                    input="input",
                    input_path="inputPath",
                    pattern=pattern
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cb1a567ecaec32e8f4b97b7bdfda937fc1c0101a94d2041e237ea1044031a558)
                check_type(argname="argument event_bus_name", value=event_bus_name, expected_type=type_hints["event_bus_name"])
                check_type(argname="argument input", value=input, expected_type=type_hints["input"])
                check_type(argname="argument input_path", value=input_path, expected_type=type_hints["input_path"])
                check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if event_bus_name is not None:
                self._values["event_bus_name"] = event_bus_name
            if input is not None:
                self._values["input"] = input
            if input_path is not None:
                self._values["input_path"] = input_path
            if pattern is not None:
                self._values["pattern"] = pattern

        @builtins.property
        def event_bus_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-eventbridgeruleevent.html#cfn-serverless-function-eventbridgeruleevent-eventbusname
            '''
            result = self._values.get("event_bus_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-eventbridgeruleevent.html#cfn-serverless-function-eventbridgeruleevent-input
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_path(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-eventbridgeruleevent.html#cfn-serverless-function-eventbridgeruleevent-inputpath
            '''
            result = self._values.get("input_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pattern(self) -> typing.Any:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-eventbridgeruleevent.html#cfn-serverless-function-eventbridgeruleevent-pattern
            '''
            result = self._values.get("pattern")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventBridgeRuleEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.EventInvokeConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_config": "destinationConfig",
            "maximum_event_age_in_seconds": "maximumEventAgeInSeconds",
            "maximum_retry_attempts": "maximumRetryAttempts",
        },
    )
    class EventInvokeConfigProperty:
        def __init__(
            self,
            *,
            destination_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.EventInvokeDestinationConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            maximum_event_age_in_seconds: typing.Optional[jsii.Number] = None,
            maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param destination_config: 
            :param maximum_event_age_in_seconds: 
            :param maximum_retry_attempts: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-eventinvokeconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                event_invoke_config_property = sam_mixins.CfnFunctionPropsMixin.EventInvokeConfigProperty(
                    destination_config=sam_mixins.CfnFunctionPropsMixin.EventInvokeDestinationConfigProperty(
                        on_failure=sam_mixins.CfnFunctionPropsMixin.DestinationProperty(
                            destination="destination",
                            type="type"
                        ),
                        on_success=sam_mixins.CfnFunctionPropsMixin.DestinationProperty(
                            destination="destination",
                            type="type"
                        )
                    ),
                    maximum_event_age_in_seconds=123,
                    maximum_retry_attempts=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9fae61446886df13c6f4b145b2e6901101cae06e608965dcc54bc8523d9b97b9)
                check_type(argname="argument destination_config", value=destination_config, expected_type=type_hints["destination_config"])
                check_type(argname="argument maximum_event_age_in_seconds", value=maximum_event_age_in_seconds, expected_type=type_hints["maximum_event_age_in_seconds"])
                check_type(argname="argument maximum_retry_attempts", value=maximum_retry_attempts, expected_type=type_hints["maximum_retry_attempts"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_config is not None:
                self._values["destination_config"] = destination_config
            if maximum_event_age_in_seconds is not None:
                self._values["maximum_event_age_in_seconds"] = maximum_event_age_in_seconds
            if maximum_retry_attempts is not None:
                self._values["maximum_retry_attempts"] = maximum_retry_attempts

        @builtins.property
        def destination_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EventInvokeDestinationConfigProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-eventinvokeconfig.html#cfn-serverless-function-eventinvokeconfig-destinationconfig
            '''
            result = self._values.get("destination_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EventInvokeDestinationConfigProperty"]], result)

        @builtins.property
        def maximum_event_age_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-eventinvokeconfig.html#cfn-serverless-function-eventinvokeconfig-maximumeventageinseconds
            '''
            result = self._values.get("maximum_event_age_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-eventinvokeconfig.html#cfn-serverless-function-eventinvokeconfig-maximumretryattempts
            '''
            result = self._values.get("maximum_retry_attempts")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventInvokeConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.EventInvokeDestinationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"on_failure": "onFailure", "on_success": "onSuccess"},
    )
    class EventInvokeDestinationConfigProperty:
        def __init__(
            self,
            *,
            on_failure: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.DestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            on_success: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.DestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param on_failure: 
            :param on_success: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-eventinvokedestinationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                event_invoke_destination_config_property = sam_mixins.CfnFunctionPropsMixin.EventInvokeDestinationConfigProperty(
                    on_failure=sam_mixins.CfnFunctionPropsMixin.DestinationProperty(
                        destination="destination",
                        type="type"
                    ),
                    on_success=sam_mixins.CfnFunctionPropsMixin.DestinationProperty(
                        destination="destination",
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2bd9f60018412545d590b8c9cd20d100e414c78aa2b855f5acc4944e7c4f45d4)
                check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
                check_type(argname="argument on_success", value=on_success, expected_type=type_hints["on_success"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if on_failure is not None:
                self._values["on_failure"] = on_failure
            if on_success is not None:
                self._values["on_success"] = on_success

        @builtins.property
        def on_failure(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.DestinationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-eventinvokedestinationconfig.html#cfn-serverless-function-eventinvokedestinationconfig-onfailure
            '''
            result = self._values.get("on_failure")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.DestinationProperty"]], result)

        @builtins.property
        def on_success(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.DestinationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-eventinvokedestinationconfig.html#cfn-serverless-function-eventinvokedestinationconfig-onsuccess
            '''
            result = self._values.get("on_success")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.DestinationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventInvokeDestinationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.EventSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"properties": "properties", "type": "type"},
    )
    class EventSourceProperty:
        def __init__(
            self,
            *,
            properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.AlexaSkillEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunctionPropsMixin.ApiEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunctionPropsMixin.CloudWatchEventEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunctionPropsMixin.CloudWatchLogsEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunctionPropsMixin.CognitoEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunctionPropsMixin.DynamoDBEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunctionPropsMixin.EventBridgeRuleEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunctionPropsMixin.HttpApiEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunctionPropsMixin.IoTRuleEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunctionPropsMixin.KinesisEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunctionPropsMixin.S3EventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunctionPropsMixin.ScheduleEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunctionPropsMixin.SNSEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunctionPropsMixin.SQSEventProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param properties: 
            :param type: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-eventsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                event_source_property = sam_mixins.CfnFunctionPropsMixin.EventSourceProperty(
                    properties=sam_mixins.CfnFunctionPropsMixin.AlexaSkillEventProperty(
                        skill_id="skillId"
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__04fc21803b3051be5e22b2f976d4e404963fad6bd860e85090facd4c20ed6ada)
                check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if properties is not None:
                self._values["properties"] = properties
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.AlexaSkillEventProperty", "CfnFunctionPropsMixin.ApiEventProperty", "CfnFunctionPropsMixin.CloudWatchEventEventProperty", "CfnFunctionPropsMixin.CloudWatchLogsEventProperty", "CfnFunctionPropsMixin.CognitoEventProperty", "CfnFunctionPropsMixin.DynamoDBEventProperty", "CfnFunctionPropsMixin.EventBridgeRuleEventProperty", "CfnFunctionPropsMixin.HttpApiEventProperty", "CfnFunctionPropsMixin.IoTRuleEventProperty", "CfnFunctionPropsMixin.KinesisEventProperty", "CfnFunctionPropsMixin.S3EventProperty", "CfnFunctionPropsMixin.ScheduleEventProperty", "CfnFunctionPropsMixin.SNSEventProperty", "CfnFunctionPropsMixin.SQSEventProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-eventsource.html#cfn-serverless-function-eventsource-properties
            '''
            result = self._values.get("properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.AlexaSkillEventProperty", "CfnFunctionPropsMixin.ApiEventProperty", "CfnFunctionPropsMixin.CloudWatchEventEventProperty", "CfnFunctionPropsMixin.CloudWatchLogsEventProperty", "CfnFunctionPropsMixin.CognitoEventProperty", "CfnFunctionPropsMixin.DynamoDBEventProperty", "CfnFunctionPropsMixin.EventBridgeRuleEventProperty", "CfnFunctionPropsMixin.HttpApiEventProperty", "CfnFunctionPropsMixin.IoTRuleEventProperty", "CfnFunctionPropsMixin.KinesisEventProperty", "CfnFunctionPropsMixin.S3EventProperty", "CfnFunctionPropsMixin.ScheduleEventProperty", "CfnFunctionPropsMixin.SNSEventProperty", "CfnFunctionPropsMixin.SQSEventProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-eventsource.html#cfn-serverless-function-eventsource-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.FileSystemConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn", "local_mount_path": "localMountPath"},
    )
    class FileSystemConfigProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            local_mount_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param arn: 
            :param local_mount_path: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-filesystemconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                file_system_config_property = sam_mixins.CfnFunctionPropsMixin.FileSystemConfigProperty(
                    arn="arn",
                    local_mount_path="localMountPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__51a5bf909ea3c7a6cabb446e65d88647b7a6b5884175931d61d22434b231eb96)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument local_mount_path", value=local_mount_path, expected_type=type_hints["local_mount_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if local_mount_path is not None:
                self._values["local_mount_path"] = local_mount_path

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-filesystemconfig.html#cfn-serverless-function-filesystemconfig-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def local_mount_path(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-filesystemconfig.html#cfn-serverless-function-filesystemconfig-localmountpath
            '''
            result = self._values.get("local_mount_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FileSystemConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.FunctionEnvironmentProperty",
        jsii_struct_bases=[],
        name_mapping={"variables": "variables"},
    )
    class FunctionEnvironmentProperty:
        def __init__(
            self,
            *,
            variables: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''
            :param variables: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-functionenvironment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                function_environment_property = sam_mixins.CfnFunctionPropsMixin.FunctionEnvironmentProperty(
                    variables={
                        "variables_key": "variables"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__24041369edee7294e69e16ee14d657873910e47ab7eebeb087be6deb716c2e02)
                check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if variables is not None:
                self._values["variables"] = variables

        @builtins.property
        def variables(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-functionenvironment.html#cfn-serverless-function-functionenvironment-variables
            '''
            result = self._values.get("variables")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionEnvironmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.FunctionSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"function_name": "functionName"},
    )
    class FunctionSAMPTProperty:
        def __init__(
            self,
            *,
            function_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param function_name: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-functionsampt.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                function_sAMPTProperty = sam_mixins.CfnFunctionPropsMixin.FunctionSAMPTProperty(
                    function_name="functionName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__83a41ff962ce8de3a0ae0bf06abaa76e20b965844cc51700865bcaf7c41a5556)
                check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if function_name is not None:
                self._values["function_name"] = function_name

        @builtins.property
        def function_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-functionsampt.html#cfn-serverless-function-functionsampt-functionname
            '''
            result = self._values.get("function_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.FunctionUrlConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auth_type": "authType",
            "cors": "cors",
            "invoke_mode": "invokeMode",
        },
    )
    class FunctionUrlConfigProperty:
        def __init__(
            self,
            *,
            auth_type: typing.Optional[builtins.str] = None,
            cors: typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.CorsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            invoke_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param auth_type: 
            :param cors: 
            :param invoke_mode: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-functionurlconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                function_url_config_property = sam_mixins.CfnFunctionPropsMixin.FunctionUrlConfigProperty(
                    auth_type="authType",
                    cors="cors",
                    invoke_mode="invokeMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__475636cc40022021e567f74ec3011b9feb4e00b4df2dc2a562fbcf243bc479fa)
                check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
                check_type(argname="argument cors", value=cors, expected_type=type_hints["cors"])
                check_type(argname="argument invoke_mode", value=invoke_mode, expected_type=type_hints["invoke_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auth_type is not None:
                self._values["auth_type"] = auth_type
            if cors is not None:
                self._values["cors"] = cors
            if invoke_mode is not None:
                self._values["invoke_mode"] = invoke_mode

        @builtins.property
        def auth_type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-functionurlconfig.html#cfn-serverless-function-functionurlconfig-authtype
            '''
            result = self._values.get("auth_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cors(
            self,
        ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.CorsConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-functionurlconfig.html#cfn-serverless-function-functionurlconfig-cors
            '''
            result = self._values.get("cors")
            return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.CorsConfigurationProperty"]], result)

        @builtins.property
        def invoke_mode(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-functionurlconfig.html#cfn-serverless-function-functionurlconfig-invokemode
            '''
            result = self._values.get("invoke_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionUrlConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.HooksProperty",
        jsii_struct_bases=[],
        name_mapping={"post_traffic": "postTraffic", "pre_traffic": "preTraffic"},
    )
    class HooksProperty:
        def __init__(
            self,
            *,
            post_traffic: typing.Optional[builtins.str] = None,
            pre_traffic: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param post_traffic: 
            :param pre_traffic: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-hooks.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                hooks_property = sam_mixins.CfnFunctionPropsMixin.HooksProperty(
                    post_traffic="postTraffic",
                    pre_traffic="preTraffic"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__17e036b5208d1d39727b50db5eb205ed9df5b0996a4eae30f6a91f18fa7b851f)
                check_type(argname="argument post_traffic", value=post_traffic, expected_type=type_hints["post_traffic"])
                check_type(argname="argument pre_traffic", value=pre_traffic, expected_type=type_hints["pre_traffic"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if post_traffic is not None:
                self._values["post_traffic"] = post_traffic
            if pre_traffic is not None:
                self._values["pre_traffic"] = pre_traffic

        @builtins.property
        def post_traffic(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-hooks.html#cfn-serverless-function-hooks-posttraffic
            '''
            result = self._values.get("post_traffic")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pre_traffic(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-hooks.html#cfn-serverless-function-hooks-pretraffic
            '''
            result = self._values.get("pre_traffic")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HooksProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.HttpApiEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "api_id": "apiId",
            "auth": "auth",
            "method": "method",
            "path": "path",
            "payload_format_version": "payloadFormatVersion",
            "route_settings": "routeSettings",
            "timeout_in_millis": "timeoutInMillis",
        },
    )
    class HttpApiEventProperty:
        def __init__(
            self,
            *,
            api_id: typing.Optional[builtins.str] = None,
            auth: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.HttpApiFunctionAuthProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            method: typing.Optional[builtins.str] = None,
            path: typing.Optional[builtins.str] = None,
            payload_format_version: typing.Optional[builtins.str] = None,
            route_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.RouteSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            timeout_in_millis: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param api_id: 
            :param auth: 
            :param method: 
            :param path: 
            :param payload_format_version: 
            :param route_settings: 
            :param timeout_in_millis: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-httpapievent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                http_api_event_property = sam_mixins.CfnFunctionPropsMixin.HttpApiEventProperty(
                    api_id="apiId",
                    auth=sam_mixins.CfnFunctionPropsMixin.HttpApiFunctionAuthProperty(
                        authorization_scopes=["authorizationScopes"],
                        authorizer="authorizer"
                    ),
                    method="method",
                    path="path",
                    payload_format_version="payloadFormatVersion",
                    route_settings=sam_mixins.CfnFunctionPropsMixin.RouteSettingsProperty(
                        data_trace_enabled=False,
                        detailed_metrics_enabled=False,
                        logging_level="loggingLevel",
                        throttling_burst_limit=123,
                        throttling_rate_limit=123
                    ),
                    timeout_in_millis=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__927e4bcdc0dcd710ec71883f1eb0a92e1d699ed4dfded22aa1b7195f41114881)
                check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
                check_type(argname="argument auth", value=auth, expected_type=type_hints["auth"])
                check_type(argname="argument method", value=method, expected_type=type_hints["method"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument payload_format_version", value=payload_format_version, expected_type=type_hints["payload_format_version"])
                check_type(argname="argument route_settings", value=route_settings, expected_type=type_hints["route_settings"])
                check_type(argname="argument timeout_in_millis", value=timeout_in_millis, expected_type=type_hints["timeout_in_millis"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if api_id is not None:
                self._values["api_id"] = api_id
            if auth is not None:
                self._values["auth"] = auth
            if method is not None:
                self._values["method"] = method
            if path is not None:
                self._values["path"] = path
            if payload_format_version is not None:
                self._values["payload_format_version"] = payload_format_version
            if route_settings is not None:
                self._values["route_settings"] = route_settings
            if timeout_in_millis is not None:
                self._values["timeout_in_millis"] = timeout_in_millis

        @builtins.property
        def api_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-httpapievent.html#cfn-serverless-function-httpapievent-apiid
            '''
            result = self._values.get("api_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def auth(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.HttpApiFunctionAuthProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-httpapievent.html#cfn-serverless-function-httpapievent-auth
            '''
            result = self._values.get("auth")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.HttpApiFunctionAuthProperty"]], result)

        @builtins.property
        def method(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-httpapievent.html#cfn-serverless-function-httpapievent-method
            '''
            result = self._values.get("method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-httpapievent.html#cfn-serverless-function-httpapievent-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def payload_format_version(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-httpapievent.html#cfn-serverless-function-httpapievent-payloadformatversion
            '''
            result = self._values.get("payload_format_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def route_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.RouteSettingsProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-httpapievent.html#cfn-serverless-function-httpapievent-routesettings
            '''
            result = self._values.get("route_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.RouteSettingsProperty"]], result)

        @builtins.property
        def timeout_in_millis(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-httpapievent.html#cfn-serverless-function-httpapievent-timeoutinmillis
            '''
            result = self._values.get("timeout_in_millis")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpApiEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.HttpApiFunctionAuthProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorization_scopes": "authorizationScopes",
            "authorizer": "authorizer",
        },
    )
    class HttpApiFunctionAuthProperty:
        def __init__(
            self,
            *,
            authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
            authorizer: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param authorization_scopes: 
            :param authorizer: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-httpapifunctionauth.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                http_api_function_auth_property = sam_mixins.CfnFunctionPropsMixin.HttpApiFunctionAuthProperty(
                    authorization_scopes=["authorizationScopes"],
                    authorizer="authorizer"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e46877a8368a9ba4f0321c789177eec5593fa9b8393b3185770f51eccd52bca2)
                check_type(argname="argument authorization_scopes", value=authorization_scopes, expected_type=type_hints["authorization_scopes"])
                check_type(argname="argument authorizer", value=authorizer, expected_type=type_hints["authorizer"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authorization_scopes is not None:
                self._values["authorization_scopes"] = authorization_scopes
            if authorizer is not None:
                self._values["authorizer"] = authorizer

        @builtins.property
        def authorization_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-httpapifunctionauth.html#cfn-serverless-function-httpapifunctionauth-authorizationscopes
            '''
            result = self._values.get("authorization_scopes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def authorizer(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-httpapifunctionauth.html#cfn-serverless-function-httpapifunctionauth-authorizer
            '''
            result = self._values.get("authorizer")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpApiFunctionAuthProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.IAMPolicyDocumentProperty",
        jsii_struct_bases=[],
        name_mapping={"statement": "statement", "version": "version"},
    )
    class IAMPolicyDocumentProperty:
        def __init__(
            self,
            *,
            statement: typing.Any = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param statement: 
            :param version: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-iampolicydocument.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                # statement: Any
                
                i_aMPolicy_document_property = {
                    "statement": statement,
                    "version": "version"
                }
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__557b9b8c8599fbe0a2c10a7ff42e22e7e57d945ae15cdf7275654f3835003344)
                check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if statement is not None:
                self._values["statement"] = statement
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def statement(self) -> typing.Any:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-iampolicydocument.html#cfn-serverless-function-iampolicydocument-statement
            '''
            result = self._values.get("statement")
            return typing.cast(typing.Any, result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-iampolicydocument.html#cfn-serverless-function-iampolicydocument-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IAMPolicyDocumentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.IdentitySAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"identity_name": "identityName"},
    )
    class IdentitySAMPTProperty:
        def __init__(
            self,
            *,
            identity_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param identity_name: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-identitysampt.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                identity_sAMPTProperty = sam_mixins.CfnFunctionPropsMixin.IdentitySAMPTProperty(
                    identity_name="identityName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5d6a656d8809f80eea980b34f47426785053497c4be34d5aefb7c93cab7a4b4d)
                check_type(argname="argument identity_name", value=identity_name, expected_type=type_hints["identity_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if identity_name is not None:
                self._values["identity_name"] = identity_name

        @builtins.property
        def identity_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-identitysampt.html#cfn-serverless-function-identitysampt-identityname
            '''
            result = self._values.get("identity_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdentitySAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.ImageConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "command": "command",
            "entry_point": "entryPoint",
            "working_directory": "workingDirectory",
        },
    )
    class ImageConfigProperty:
        def __init__(
            self,
            *,
            command: typing.Optional[typing.Sequence[builtins.str]] = None,
            entry_point: typing.Optional[typing.Sequence[builtins.str]] = None,
            working_directory: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param command: 
            :param entry_point: 
            :param working_directory: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-imageconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                image_config_property = sam_mixins.CfnFunctionPropsMixin.ImageConfigProperty(
                    command=["command"],
                    entry_point=["entryPoint"],
                    working_directory="workingDirectory"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__426cb1b7e56a91bdce02cb6ae25a5defb42bcfc8928ab870415a8eb6e0fdc07b)
                check_type(argname="argument command", value=command, expected_type=type_hints["command"])
                check_type(argname="argument entry_point", value=entry_point, expected_type=type_hints["entry_point"])
                check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if command is not None:
                self._values["command"] = command
            if entry_point is not None:
                self._values["entry_point"] = entry_point
            if working_directory is not None:
                self._values["working_directory"] = working_directory

        @builtins.property
        def command(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-imageconfig.html#cfn-serverless-function-imageconfig-command
            '''
            result = self._values.get("command")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def entry_point(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-imageconfig.html#cfn-serverless-function-imageconfig-entrypoint
            '''
            result = self._values.get("entry_point")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def working_directory(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-imageconfig.html#cfn-serverless-function-imageconfig-workingdirectory
            '''
            result = self._values.get("working_directory")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImageConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.IoTRuleEventProperty",
        jsii_struct_bases=[],
        name_mapping={"aws_iot_sql_version": "awsIotSqlVersion", "sql": "sql"},
    )
    class IoTRuleEventProperty:
        def __init__(
            self,
            *,
            aws_iot_sql_version: typing.Optional[builtins.str] = None,
            sql: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param aws_iot_sql_version: 
            :param sql: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-iotruleevent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                io_tRule_event_property = sam_mixins.CfnFunctionPropsMixin.IoTRuleEventProperty(
                    aws_iot_sql_version="awsIotSqlVersion",
                    sql="sql"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__847b4ec5c5773ffb8571b137351c929c866eefc53b360b34d4f0bc975b2931aa)
                check_type(argname="argument aws_iot_sql_version", value=aws_iot_sql_version, expected_type=type_hints["aws_iot_sql_version"])
                check_type(argname="argument sql", value=sql, expected_type=type_hints["sql"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_iot_sql_version is not None:
                self._values["aws_iot_sql_version"] = aws_iot_sql_version
            if sql is not None:
                self._values["sql"] = sql

        @builtins.property
        def aws_iot_sql_version(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-iotruleevent.html#cfn-serverless-function-iotruleevent-awsiotsqlversion
            '''
            result = self._values.get("aws_iot_sql_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sql(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-iotruleevent.html#cfn-serverless-function-iotruleevent-sql
            '''
            result = self._values.get("sql")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IoTRuleEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.KeySAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"key_id": "keyId"},
    )
    class KeySAMPTProperty:
        def __init__(self, *, key_id: typing.Optional[builtins.str] = None) -> None:
            '''
            :param key_id: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-keysampt.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                key_sAMPTProperty = sam_mixins.CfnFunctionPropsMixin.KeySAMPTProperty(
                    key_id="keyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__03d5d6307de5085ec53c171ae8467c87da921b10d0334378be8654f8313dec48)
                check_type(argname="argument key_id", value=key_id, expected_type=type_hints["key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key_id is not None:
                self._values["key_id"] = key_id

        @builtins.property
        def key_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-keysampt.html#cfn-serverless-function-keysampt-keyid
            '''
            result = self._values.get("key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeySAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.KinesisEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "batch_size": "batchSize",
            "enabled": "enabled",
            "function_response_types": "functionResponseTypes",
            "starting_position": "startingPosition",
            "stream": "stream",
        },
    )
    class KinesisEventProperty:
        def __init__(
            self,
            *,
            batch_size: typing.Optional[jsii.Number] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            function_response_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            starting_position: typing.Optional[builtins.str] = None,
            stream: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param batch_size: 
            :param enabled: 
            :param function_response_types: 
            :param starting_position: 
            :param stream: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-kinesisevent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                kinesis_event_property = sam_mixins.CfnFunctionPropsMixin.KinesisEventProperty(
                    batch_size=123,
                    enabled=False,
                    function_response_types=["functionResponseTypes"],
                    starting_position="startingPosition",
                    stream="stream"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a1ae3fa48f978fbe68e1319545fb177c907c0dc3f514fafa7e6f2460badd2a2d)
                check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument function_response_types", value=function_response_types, expected_type=type_hints["function_response_types"])
                check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
                check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if batch_size is not None:
                self._values["batch_size"] = batch_size
            if enabled is not None:
                self._values["enabled"] = enabled
            if function_response_types is not None:
                self._values["function_response_types"] = function_response_types
            if starting_position is not None:
                self._values["starting_position"] = starting_position
            if stream is not None:
                self._values["stream"] = stream

        @builtins.property
        def batch_size(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-kinesisevent.html#cfn-serverless-function-kinesisevent-batchsize
            '''
            result = self._values.get("batch_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-kinesisevent.html#cfn-serverless-function-kinesisevent-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def function_response_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-kinesisevent.html#cfn-serverless-function-kinesisevent-functionresponsetypes
            '''
            result = self._values.get("function_response_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def starting_position(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-kinesisevent.html#cfn-serverless-function-kinesisevent-startingposition
            '''
            result = self._values.get("starting_position")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stream(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-kinesisevent.html#cfn-serverless-function-kinesisevent-stream
            '''
            result = self._values.get("stream")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.LogGroupSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_name": "logGroupName"},
    )
    class LogGroupSAMPTProperty:
        def __init__(
            self,
            *,
            log_group_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param log_group_name: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-loggroupsampt.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                log_group_sAMPTProperty = sam_mixins.CfnFunctionPropsMixin.LogGroupSAMPTProperty(
                    log_group_name="logGroupName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2b6ee0a5acfc7f7cc3326eaddc6634c8d10759e71f9df57a9bbba855833b6ad5)
                check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_group_name is not None:
                self._values["log_group_name"] = log_group_name

        @builtins.property
        def log_group_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-loggroupsampt.html#cfn-serverless-function-loggroupsampt-loggroupname
            '''
            result = self._values.get("log_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogGroupSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.ParameterNameSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"parameter_name": "parameterName"},
    )
    class ParameterNameSAMPTProperty:
        def __init__(
            self,
            *,
            parameter_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param parameter_name: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-parameternamesampt.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                parameter_name_sAMPTProperty = sam_mixins.CfnFunctionPropsMixin.ParameterNameSAMPTProperty(
                    parameter_name="parameterName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d8cd4ec12e4d927c18ea5694d33402b0dc759654725db994647babd52a95bdb0)
                check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if parameter_name is not None:
                self._values["parameter_name"] = parameter_name

        @builtins.property
        def parameter_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-parameternamesampt.html#cfn-serverless-function-parameternamesampt-parametername
            '''
            result = self._values.get("parameter_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterNameSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.ProvisionedConcurrencyConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "provisioned_concurrent_executions": "provisionedConcurrentExecutions",
        },
    )
    class ProvisionedConcurrencyConfigProperty:
        def __init__(
            self,
            *,
            provisioned_concurrent_executions: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param provisioned_concurrent_executions: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-provisionedconcurrencyconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                provisioned_concurrency_config_property = sam_mixins.CfnFunctionPropsMixin.ProvisionedConcurrencyConfigProperty(
                    provisioned_concurrent_executions="provisionedConcurrentExecutions"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__77d3fa3f6606aa63a236fd393e9ecdc0bfd9a5174f1a63023dfedc1a2eb62b9a)
                check_type(argname="argument provisioned_concurrent_executions", value=provisioned_concurrent_executions, expected_type=type_hints["provisioned_concurrent_executions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if provisioned_concurrent_executions is not None:
                self._values["provisioned_concurrent_executions"] = provisioned_concurrent_executions

        @builtins.property
        def provisioned_concurrent_executions(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-provisionedconcurrencyconfig.html#cfn-serverless-function-provisionedconcurrencyconfig-provisionedconcurrentexecutions
            '''
            result = self._values.get("provisioned_concurrent_executions")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisionedConcurrencyConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.QueueSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"queue_name": "queueName"},
    )
    class QueueSAMPTProperty:
        def __init__(self, *, queue_name: typing.Optional[builtins.str] = None) -> None:
            '''
            :param queue_name: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-queuesampt.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                queue_sAMPTProperty = sam_mixins.CfnFunctionPropsMixin.QueueSAMPTProperty(
                    queue_name="queueName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dcb37d4627dcf475f97b0c424257ca8468c5eba931c4bba4b475fb73d027bded)
                check_type(argname="argument queue_name", value=queue_name, expected_type=type_hints["queue_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if queue_name is not None:
                self._values["queue_name"] = queue_name

        @builtins.property
        def queue_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-queuesampt.html#cfn-serverless-function-queuesampt-queuename
            '''
            result = self._values.get("queue_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueueSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.RequestModelProperty",
        jsii_struct_bases=[],
        name_mapping={
            "model": "model",
            "required": "required",
            "validate_body": "validateBody",
            "validate_parameters": "validateParameters",
        },
    )
    class RequestModelProperty:
        def __init__(
            self,
            *,
            model: typing.Optional[builtins.str] = None,
            required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            validate_body: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            validate_parameters: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''
            :param model: 
            :param required: 
            :param validate_body: 
            :param validate_parameters: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-requestmodel.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                request_model_property = sam_mixins.CfnFunctionPropsMixin.RequestModelProperty(
                    model="model",
                    required=False,
                    validate_body=False,
                    validate_parameters=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c8ae377b329a050cb5873b446146dc8fdb62489d908309cd5fdfadd372b94d2d)
                check_type(argname="argument model", value=model, expected_type=type_hints["model"])
                check_type(argname="argument required", value=required, expected_type=type_hints["required"])
                check_type(argname="argument validate_body", value=validate_body, expected_type=type_hints["validate_body"])
                check_type(argname="argument validate_parameters", value=validate_parameters, expected_type=type_hints["validate_parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if model is not None:
                self._values["model"] = model
            if required is not None:
                self._values["required"] = required
            if validate_body is not None:
                self._values["validate_body"] = validate_body
            if validate_parameters is not None:
                self._values["validate_parameters"] = validate_parameters

        @builtins.property
        def model(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-requestmodel.html#cfn-serverless-function-requestmodel-model
            '''
            result = self._values.get("model")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def required(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-requestmodel.html#cfn-serverless-function-requestmodel-required
            '''
            result = self._values.get("required")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def validate_body(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-requestmodel.html#cfn-serverless-function-requestmodel-validatebody
            '''
            result = self._values.get("validate_body")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def validate_parameters(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-requestmodel.html#cfn-serverless-function-requestmodel-validateparameters
            '''
            result = self._values.get("validate_parameters")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RequestModelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.RequestParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"caching": "caching", "required": "required"},
    )
    class RequestParameterProperty:
        def __init__(
            self,
            *,
            caching: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''
            :param caching: 
            :param required: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-requestparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                request_parameter_property = sam_mixins.CfnFunctionPropsMixin.RequestParameterProperty(
                    caching=False,
                    required=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d31eebfb17b725351f5ef592bf6c4dd567a665ad310b10e88d7e4826a57ba7ba)
                check_type(argname="argument caching", value=caching, expected_type=type_hints["caching"])
                check_type(argname="argument required", value=required, expected_type=type_hints["required"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if caching is not None:
                self._values["caching"] = caching
            if required is not None:
                self._values["required"] = required

        @builtins.property
        def caching(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-requestparameter.html#cfn-serverless-function-requestparameter-caching
            '''
            result = self._values.get("caching")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def required(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-requestparameter.html#cfn-serverless-function-requestparameter-required
            '''
            result = self._values.get("required")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RequestParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.RouteSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_trace_enabled": "dataTraceEnabled",
            "detailed_metrics_enabled": "detailedMetricsEnabled",
            "logging_level": "loggingLevel",
            "throttling_burst_limit": "throttlingBurstLimit",
            "throttling_rate_limit": "throttlingRateLimit",
        },
    )
    class RouteSettingsProperty:
        def __init__(
            self,
            *,
            data_trace_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            detailed_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            logging_level: typing.Optional[builtins.str] = None,
            throttling_burst_limit: typing.Optional[jsii.Number] = None,
            throttling_rate_limit: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param data_trace_enabled: 
            :param detailed_metrics_enabled: 
            :param logging_level: 
            :param throttling_burst_limit: 
            :param throttling_rate_limit: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-routesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                route_settings_property = sam_mixins.CfnFunctionPropsMixin.RouteSettingsProperty(
                    data_trace_enabled=False,
                    detailed_metrics_enabled=False,
                    logging_level="loggingLevel",
                    throttling_burst_limit=123,
                    throttling_rate_limit=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__176e198930e56ca201f000fcf3185baa45fd3394a38a1b66c3f049ef8b5e7b31)
                check_type(argname="argument data_trace_enabled", value=data_trace_enabled, expected_type=type_hints["data_trace_enabled"])
                check_type(argname="argument detailed_metrics_enabled", value=detailed_metrics_enabled, expected_type=type_hints["detailed_metrics_enabled"])
                check_type(argname="argument logging_level", value=logging_level, expected_type=type_hints["logging_level"])
                check_type(argname="argument throttling_burst_limit", value=throttling_burst_limit, expected_type=type_hints["throttling_burst_limit"])
                check_type(argname="argument throttling_rate_limit", value=throttling_rate_limit, expected_type=type_hints["throttling_rate_limit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_trace_enabled is not None:
                self._values["data_trace_enabled"] = data_trace_enabled
            if detailed_metrics_enabled is not None:
                self._values["detailed_metrics_enabled"] = detailed_metrics_enabled
            if logging_level is not None:
                self._values["logging_level"] = logging_level
            if throttling_burst_limit is not None:
                self._values["throttling_burst_limit"] = throttling_burst_limit
            if throttling_rate_limit is not None:
                self._values["throttling_rate_limit"] = throttling_rate_limit

        @builtins.property
        def data_trace_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-routesettings.html#cfn-serverless-function-routesettings-datatraceenabled
            '''
            result = self._values.get("data_trace_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def detailed_metrics_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-routesettings.html#cfn-serverless-function-routesettings-detailedmetricsenabled
            '''
            result = self._values.get("detailed_metrics_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def logging_level(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-routesettings.html#cfn-serverless-function-routesettings-logginglevel
            '''
            result = self._values.get("logging_level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def throttling_burst_limit(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-routesettings.html#cfn-serverless-function-routesettings-throttlingburstlimit
            '''
            result = self._values.get("throttling_burst_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def throttling_rate_limit(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-routesettings.html#cfn-serverless-function-routesettings-throttlingratelimit
            '''
            result = self._values.get("throttling_rate_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RouteSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.S3EventProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "events": "events", "filter": "filter"},
    )
    class S3EventProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            events: typing.Optional[builtins.str] = None,
            filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.S3NotificationFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param bucket: 
            :param events: 
            :param filter: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-s3event.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                s3_event_property = sam_mixins.CfnFunctionPropsMixin.S3EventProperty(
                    bucket="bucket",
                    events="events",
                    filter=sam_mixins.CfnFunctionPropsMixin.S3NotificationFilterProperty(
                        s3_key=sam_mixins.CfnFunctionPropsMixin.S3KeyFilterProperty(
                            rules=[sam_mixins.CfnFunctionPropsMixin.S3KeyFilterRuleProperty(
                                name="name",
                                value="value"
                            )]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__14e620e9c2b678b4d19110760e038c4b2da69a0dfe2cd2bc4e7e35174dfbe7ee)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument events", value=events, expected_type=type_hints["events"])
                check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if events is not None:
                self._values["events"] = events
            if filter is not None:
                self._values["filter"] = filter

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-s3event.html#cfn-serverless-function-s3event-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def events(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-s3event.html#cfn-serverless-function-s3event-events
            '''
            result = self._values.get("events")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.S3NotificationFilterProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-s3event.html#cfn-serverless-function-s3event-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.S3NotificationFilterProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3EventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.S3KeyFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"rules": "rules"},
    )
    class S3KeyFilterProperty:
        def __init__(
            self,
            *,
            rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.S3KeyFilterRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''
            :param rules: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-s3keyfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                s3_key_filter_property = sam_mixins.CfnFunctionPropsMixin.S3KeyFilterProperty(
                    rules=[sam_mixins.CfnFunctionPropsMixin.S3KeyFilterRuleProperty(
                        name="name",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__acd3dd5d8dfcefc55103fcee6c0199d563a6dba78fd3a68597a001335193fb23)
                check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rules is not None:
                self._values["rules"] = rules

        @builtins.property
        def rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.S3KeyFilterRuleProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-s3keyfilter.html#cfn-serverless-function-s3keyfilter-rules
            '''
            result = self._values.get("rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.S3KeyFilterRuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3KeyFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.S3KeyFilterRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class S3KeyFilterRuleProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param name: 
            :param value: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-s3keyfilterrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                s3_key_filter_rule_property = sam_mixins.CfnFunctionPropsMixin.S3KeyFilterRuleProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__853ba889a806b4601df319bf3debca96393794df343721a48b05fef96b06fc1e)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-s3keyfilterrule.html#cfn-serverless-function-s3keyfilterrule-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-s3keyfilterrule.html#cfn-serverless-function-s3keyfilterrule-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3KeyFilterRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key", "version": "version"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
            version: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param bucket: 
            :param key: 
            :param version: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                s3_location_property = sam_mixins.CfnFunctionPropsMixin.S3LocationProperty(
                    bucket="bucket",
                    key="key",
                    version=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b9c387ab066f1790698d8323e6b2acf013a42c625ca0a71cb12f6e263fc4a953)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if key is not None:
                self._values["key"] = key
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-s3location.html#cfn-serverless-function-s3location-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-s3location.html#cfn-serverless-function-s3location-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-s3location.html#cfn-serverless-function-s3location-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.S3NotificationFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_key": "s3Key"},
    )
    class S3NotificationFilterProperty:
        def __init__(
            self,
            *,
            s3_key: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.S3KeyFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param s3_key: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-s3notificationfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                s3_notification_filter_property = sam_mixins.CfnFunctionPropsMixin.S3NotificationFilterProperty(
                    s3_key=sam_mixins.CfnFunctionPropsMixin.S3KeyFilterProperty(
                        rules=[sam_mixins.CfnFunctionPropsMixin.S3KeyFilterRuleProperty(
                            name="name",
                            value="value"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a31f95f8163d83325e5a26337f05fbe9bb7fdeeee262213ab1772ac342afd6a6)
                check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_key is not None:
                self._values["s3_key"] = s3_key

        @builtins.property
        def s3_key(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.S3KeyFilterProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-s3notificationfilter.html#cfn-serverless-function-s3notificationfilter-s3key
            '''
            result = self._values.get("s3_key")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.S3KeyFilterProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3NotificationFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.SAMPolicyTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ami_describe_policy": "amiDescribePolicy",
            "aws_secrets_manager_get_secret_value_policy": "awsSecretsManagerGetSecretValuePolicy",
            "cloud_formation_describe_stacks_policy": "cloudFormationDescribeStacksPolicy",
            "cloud_watch_put_metric_policy": "cloudWatchPutMetricPolicy",
            "dynamo_db_crud_policy": "dynamoDbCrudPolicy",
            "dynamo_db_read_policy": "dynamoDbReadPolicy",
            "dynamo_db_stream_read_policy": "dynamoDbStreamReadPolicy",
            "dynamo_db_write_policy": "dynamoDbWritePolicy",
            "ec2_describe_policy": "ec2DescribePolicy",
            "elasticsearch_http_post_policy": "elasticsearchHttpPostPolicy",
            "filter_log_events_policy": "filterLogEventsPolicy",
            "kinesis_crud_policy": "kinesisCrudPolicy",
            "kinesis_stream_read_policy": "kinesisStreamReadPolicy",
            "kms_decrypt_policy": "kmsDecryptPolicy",
            "lambda_invoke_policy": "lambdaInvokePolicy",
            "rekognition_detect_only_policy": "rekognitionDetectOnlyPolicy",
            "rekognition_labels_policy": "rekognitionLabelsPolicy",
            "rekognition_no_data_access_policy": "rekognitionNoDataAccessPolicy",
            "rekognition_read_policy": "rekognitionReadPolicy",
            "rekognition_write_only_access_policy": "rekognitionWriteOnlyAccessPolicy",
            "s3_crud_policy": "s3CrudPolicy",
            "s3_read_policy": "s3ReadPolicy",
            "s3_write_policy": "s3WritePolicy",
            "ses_bulk_templated_crud_policy": "sesBulkTemplatedCrudPolicy",
            "ses_crud_policy": "sesCrudPolicy",
            "ses_email_template_crud_policy": "sesEmailTemplateCrudPolicy",
            "ses_send_bounce_policy": "sesSendBouncePolicy",
            "sns_crud_policy": "snsCrudPolicy",
            "sns_publish_message_policy": "snsPublishMessagePolicy",
            "sqs_poller_policy": "sqsPollerPolicy",
            "sqs_send_message_policy": "sqsSendMessagePolicy",
            "ssm_parameter_read_policy": "ssmParameterReadPolicy",
            "step_functions_execution_policy": "stepFunctionsExecutionPolicy",
            "vpc_access_policy": "vpcAccessPolicy",
        },
    )
    class SAMPolicyTemplateProperty:
        def __init__(
            self,
            *,
            ami_describe_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.EmptySAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            aws_secrets_manager_get_secret_value_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.SecretArnSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            cloud_formation_describe_stacks_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.EmptySAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            cloud_watch_put_metric_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.EmptySAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dynamo_db_crud_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.TableSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dynamo_db_read_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.TableSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dynamo_db_stream_read_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.TableStreamSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dynamo_db_write_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.TableSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ec2_describe_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.EmptySAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            elasticsearch_http_post_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.DomainSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            filter_log_events_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.LogGroupSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            kinesis_crud_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.StreamSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            kinesis_stream_read_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.StreamSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            kms_decrypt_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.KeySAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            lambda_invoke_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.FunctionSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rekognition_detect_only_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.EmptySAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rekognition_labels_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.EmptySAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rekognition_no_data_access_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.CollectionSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rekognition_read_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.CollectionSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rekognition_write_only_access_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.CollectionSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_crud_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.BucketSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_read_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.BucketSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_write_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.BucketSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ses_bulk_templated_crud_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.IdentitySAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ses_crud_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.IdentitySAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ses_email_template_crud_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.EmptySAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ses_send_bounce_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.IdentitySAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sns_crud_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.TopicSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sns_publish_message_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.TopicSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sqs_poller_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.QueueSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sqs_send_message_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.QueueSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ssm_parameter_read_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.ParameterNameSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            step_functions_execution_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.StateMachineSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            vpc_access_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.EmptySAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param ami_describe_policy: 
            :param aws_secrets_manager_get_secret_value_policy: 
            :param cloud_formation_describe_stacks_policy: 
            :param cloud_watch_put_metric_policy: 
            :param dynamo_db_crud_policy: 
            :param dynamo_db_read_policy: 
            :param dynamo_db_stream_read_policy: 
            :param dynamo_db_write_policy: 
            :param ec2_describe_policy: 
            :param elasticsearch_http_post_policy: 
            :param filter_log_events_policy: 
            :param kinesis_crud_policy: 
            :param kinesis_stream_read_policy: 
            :param kms_decrypt_policy: 
            :param lambda_invoke_policy: 
            :param rekognition_detect_only_policy: 
            :param rekognition_labels_policy: 
            :param rekognition_no_data_access_policy: 
            :param rekognition_read_policy: 
            :param rekognition_write_only_access_policy: 
            :param s3_crud_policy: 
            :param s3_read_policy: 
            :param s3_write_policy: 
            :param ses_bulk_templated_crud_policy: 
            :param ses_crud_policy: 
            :param ses_email_template_crud_policy: 
            :param ses_send_bounce_policy: 
            :param sns_crud_policy: 
            :param sns_publish_message_policy: 
            :param sqs_poller_policy: 
            :param sqs_send_message_policy: 
            :param ssm_parameter_read_policy: 
            :param step_functions_execution_policy: 
            :param vpc_access_policy: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                s_aMPolicy_template_property = sam_mixins.CfnFunctionPropsMixin.SAMPolicyTemplateProperty(
                    ami_describe_policy=sam_mixins.CfnFunctionPropsMixin.EmptySAMPTProperty(),
                    aws_secrets_manager_get_secret_value_policy=sam_mixins.CfnFunctionPropsMixin.SecretArnSAMPTProperty(
                        secret_arn="secretArn"
                    ),
                    cloud_formation_describe_stacks_policy=sam_mixins.CfnFunctionPropsMixin.EmptySAMPTProperty(),
                    cloud_watch_put_metric_policy=sam_mixins.CfnFunctionPropsMixin.EmptySAMPTProperty(),
                    dynamo_db_crud_policy=sam_mixins.CfnFunctionPropsMixin.TableSAMPTProperty(
                        table_name="tableName"
                    ),
                    dynamo_db_read_policy=sam_mixins.CfnFunctionPropsMixin.TableSAMPTProperty(
                        table_name="tableName"
                    ),
                    dynamo_db_stream_read_policy=sam_mixins.CfnFunctionPropsMixin.TableStreamSAMPTProperty(
                        stream_name="streamName",
                        table_name="tableName"
                    ),
                    dynamo_db_write_policy=sam_mixins.CfnFunctionPropsMixin.TableSAMPTProperty(
                        table_name="tableName"
                    ),
                    ec2_describe_policy=sam_mixins.CfnFunctionPropsMixin.EmptySAMPTProperty(),
                    elasticsearch_http_post_policy=sam_mixins.CfnFunctionPropsMixin.DomainSAMPTProperty(
                        domain_name="domainName"
                    ),
                    filter_log_events_policy=sam_mixins.CfnFunctionPropsMixin.LogGroupSAMPTProperty(
                        log_group_name="logGroupName"
                    ),
                    kinesis_crud_policy=sam_mixins.CfnFunctionPropsMixin.StreamSAMPTProperty(
                        stream_name="streamName"
                    ),
                    kinesis_stream_read_policy=sam_mixins.CfnFunctionPropsMixin.StreamSAMPTProperty(
                        stream_name="streamName"
                    ),
                    kms_decrypt_policy=sam_mixins.CfnFunctionPropsMixin.KeySAMPTProperty(
                        key_id="keyId"
                    ),
                    lambda_invoke_policy=sam_mixins.CfnFunctionPropsMixin.FunctionSAMPTProperty(
                        function_name="functionName"
                    ),
                    rekognition_detect_only_policy=sam_mixins.CfnFunctionPropsMixin.EmptySAMPTProperty(),
                    rekognition_labels_policy=sam_mixins.CfnFunctionPropsMixin.EmptySAMPTProperty(),
                    rekognition_no_data_access_policy=sam_mixins.CfnFunctionPropsMixin.CollectionSAMPTProperty(
                        collection_id="collectionId"
                    ),
                    rekognition_read_policy=sam_mixins.CfnFunctionPropsMixin.CollectionSAMPTProperty(
                        collection_id="collectionId"
                    ),
                    rekognition_write_only_access_policy=sam_mixins.CfnFunctionPropsMixin.CollectionSAMPTProperty(
                        collection_id="collectionId"
                    ),
                    s3_crud_policy=sam_mixins.CfnFunctionPropsMixin.BucketSAMPTProperty(
                        bucket_name="bucketName"
                    ),
                    s3_read_policy=sam_mixins.CfnFunctionPropsMixin.BucketSAMPTProperty(
                        bucket_name="bucketName"
                    ),
                    s3_write_policy=sam_mixins.CfnFunctionPropsMixin.BucketSAMPTProperty(
                        bucket_name="bucketName"
                    ),
                    ses_bulk_templated_crud_policy=sam_mixins.CfnFunctionPropsMixin.IdentitySAMPTProperty(
                        identity_name="identityName"
                    ),
                    ses_crud_policy=sam_mixins.CfnFunctionPropsMixin.IdentitySAMPTProperty(
                        identity_name="identityName"
                    ),
                    ses_email_template_crud_policy=sam_mixins.CfnFunctionPropsMixin.EmptySAMPTProperty(),
                    ses_send_bounce_policy=sam_mixins.CfnFunctionPropsMixin.IdentitySAMPTProperty(
                        identity_name="identityName"
                    ),
                    sns_crud_policy=sam_mixins.CfnFunctionPropsMixin.TopicSAMPTProperty(
                        topic_name="topicName"
                    ),
                    sns_publish_message_policy=sam_mixins.CfnFunctionPropsMixin.TopicSAMPTProperty(
                        topic_name="topicName"
                    ),
                    sqs_poller_policy=sam_mixins.CfnFunctionPropsMixin.QueueSAMPTProperty(
                        queue_name="queueName"
                    ),
                    sqs_send_message_policy=sam_mixins.CfnFunctionPropsMixin.QueueSAMPTProperty(
                        queue_name="queueName"
                    ),
                    ssm_parameter_read_policy=sam_mixins.CfnFunctionPropsMixin.ParameterNameSAMPTProperty(
                        parameter_name="parameterName"
                    ),
                    step_functions_execution_policy=sam_mixins.CfnFunctionPropsMixin.StateMachineSAMPTProperty(
                        state_machine_name="stateMachineName"
                    ),
                    vpc_access_policy=sam_mixins.CfnFunctionPropsMixin.EmptySAMPTProperty()
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eef65b7421add41593e34d743ae06d1fcd238f7ad879cebd0e9940a0ea571ea8)
                check_type(argname="argument ami_describe_policy", value=ami_describe_policy, expected_type=type_hints["ami_describe_policy"])
                check_type(argname="argument aws_secrets_manager_get_secret_value_policy", value=aws_secrets_manager_get_secret_value_policy, expected_type=type_hints["aws_secrets_manager_get_secret_value_policy"])
                check_type(argname="argument cloud_formation_describe_stacks_policy", value=cloud_formation_describe_stacks_policy, expected_type=type_hints["cloud_formation_describe_stacks_policy"])
                check_type(argname="argument cloud_watch_put_metric_policy", value=cloud_watch_put_metric_policy, expected_type=type_hints["cloud_watch_put_metric_policy"])
                check_type(argname="argument dynamo_db_crud_policy", value=dynamo_db_crud_policy, expected_type=type_hints["dynamo_db_crud_policy"])
                check_type(argname="argument dynamo_db_read_policy", value=dynamo_db_read_policy, expected_type=type_hints["dynamo_db_read_policy"])
                check_type(argname="argument dynamo_db_stream_read_policy", value=dynamo_db_stream_read_policy, expected_type=type_hints["dynamo_db_stream_read_policy"])
                check_type(argname="argument dynamo_db_write_policy", value=dynamo_db_write_policy, expected_type=type_hints["dynamo_db_write_policy"])
                check_type(argname="argument ec2_describe_policy", value=ec2_describe_policy, expected_type=type_hints["ec2_describe_policy"])
                check_type(argname="argument elasticsearch_http_post_policy", value=elasticsearch_http_post_policy, expected_type=type_hints["elasticsearch_http_post_policy"])
                check_type(argname="argument filter_log_events_policy", value=filter_log_events_policy, expected_type=type_hints["filter_log_events_policy"])
                check_type(argname="argument kinesis_crud_policy", value=kinesis_crud_policy, expected_type=type_hints["kinesis_crud_policy"])
                check_type(argname="argument kinesis_stream_read_policy", value=kinesis_stream_read_policy, expected_type=type_hints["kinesis_stream_read_policy"])
                check_type(argname="argument kms_decrypt_policy", value=kms_decrypt_policy, expected_type=type_hints["kms_decrypt_policy"])
                check_type(argname="argument lambda_invoke_policy", value=lambda_invoke_policy, expected_type=type_hints["lambda_invoke_policy"])
                check_type(argname="argument rekognition_detect_only_policy", value=rekognition_detect_only_policy, expected_type=type_hints["rekognition_detect_only_policy"])
                check_type(argname="argument rekognition_labels_policy", value=rekognition_labels_policy, expected_type=type_hints["rekognition_labels_policy"])
                check_type(argname="argument rekognition_no_data_access_policy", value=rekognition_no_data_access_policy, expected_type=type_hints["rekognition_no_data_access_policy"])
                check_type(argname="argument rekognition_read_policy", value=rekognition_read_policy, expected_type=type_hints["rekognition_read_policy"])
                check_type(argname="argument rekognition_write_only_access_policy", value=rekognition_write_only_access_policy, expected_type=type_hints["rekognition_write_only_access_policy"])
                check_type(argname="argument s3_crud_policy", value=s3_crud_policy, expected_type=type_hints["s3_crud_policy"])
                check_type(argname="argument s3_read_policy", value=s3_read_policy, expected_type=type_hints["s3_read_policy"])
                check_type(argname="argument s3_write_policy", value=s3_write_policy, expected_type=type_hints["s3_write_policy"])
                check_type(argname="argument ses_bulk_templated_crud_policy", value=ses_bulk_templated_crud_policy, expected_type=type_hints["ses_bulk_templated_crud_policy"])
                check_type(argname="argument ses_crud_policy", value=ses_crud_policy, expected_type=type_hints["ses_crud_policy"])
                check_type(argname="argument ses_email_template_crud_policy", value=ses_email_template_crud_policy, expected_type=type_hints["ses_email_template_crud_policy"])
                check_type(argname="argument ses_send_bounce_policy", value=ses_send_bounce_policy, expected_type=type_hints["ses_send_bounce_policy"])
                check_type(argname="argument sns_crud_policy", value=sns_crud_policy, expected_type=type_hints["sns_crud_policy"])
                check_type(argname="argument sns_publish_message_policy", value=sns_publish_message_policy, expected_type=type_hints["sns_publish_message_policy"])
                check_type(argname="argument sqs_poller_policy", value=sqs_poller_policy, expected_type=type_hints["sqs_poller_policy"])
                check_type(argname="argument sqs_send_message_policy", value=sqs_send_message_policy, expected_type=type_hints["sqs_send_message_policy"])
                check_type(argname="argument ssm_parameter_read_policy", value=ssm_parameter_read_policy, expected_type=type_hints["ssm_parameter_read_policy"])
                check_type(argname="argument step_functions_execution_policy", value=step_functions_execution_policy, expected_type=type_hints["step_functions_execution_policy"])
                check_type(argname="argument vpc_access_policy", value=vpc_access_policy, expected_type=type_hints["vpc_access_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ami_describe_policy is not None:
                self._values["ami_describe_policy"] = ami_describe_policy
            if aws_secrets_manager_get_secret_value_policy is not None:
                self._values["aws_secrets_manager_get_secret_value_policy"] = aws_secrets_manager_get_secret_value_policy
            if cloud_formation_describe_stacks_policy is not None:
                self._values["cloud_formation_describe_stacks_policy"] = cloud_formation_describe_stacks_policy
            if cloud_watch_put_metric_policy is not None:
                self._values["cloud_watch_put_metric_policy"] = cloud_watch_put_metric_policy
            if dynamo_db_crud_policy is not None:
                self._values["dynamo_db_crud_policy"] = dynamo_db_crud_policy
            if dynamo_db_read_policy is not None:
                self._values["dynamo_db_read_policy"] = dynamo_db_read_policy
            if dynamo_db_stream_read_policy is not None:
                self._values["dynamo_db_stream_read_policy"] = dynamo_db_stream_read_policy
            if dynamo_db_write_policy is not None:
                self._values["dynamo_db_write_policy"] = dynamo_db_write_policy
            if ec2_describe_policy is not None:
                self._values["ec2_describe_policy"] = ec2_describe_policy
            if elasticsearch_http_post_policy is not None:
                self._values["elasticsearch_http_post_policy"] = elasticsearch_http_post_policy
            if filter_log_events_policy is not None:
                self._values["filter_log_events_policy"] = filter_log_events_policy
            if kinesis_crud_policy is not None:
                self._values["kinesis_crud_policy"] = kinesis_crud_policy
            if kinesis_stream_read_policy is not None:
                self._values["kinesis_stream_read_policy"] = kinesis_stream_read_policy
            if kms_decrypt_policy is not None:
                self._values["kms_decrypt_policy"] = kms_decrypt_policy
            if lambda_invoke_policy is not None:
                self._values["lambda_invoke_policy"] = lambda_invoke_policy
            if rekognition_detect_only_policy is not None:
                self._values["rekognition_detect_only_policy"] = rekognition_detect_only_policy
            if rekognition_labels_policy is not None:
                self._values["rekognition_labels_policy"] = rekognition_labels_policy
            if rekognition_no_data_access_policy is not None:
                self._values["rekognition_no_data_access_policy"] = rekognition_no_data_access_policy
            if rekognition_read_policy is not None:
                self._values["rekognition_read_policy"] = rekognition_read_policy
            if rekognition_write_only_access_policy is not None:
                self._values["rekognition_write_only_access_policy"] = rekognition_write_only_access_policy
            if s3_crud_policy is not None:
                self._values["s3_crud_policy"] = s3_crud_policy
            if s3_read_policy is not None:
                self._values["s3_read_policy"] = s3_read_policy
            if s3_write_policy is not None:
                self._values["s3_write_policy"] = s3_write_policy
            if ses_bulk_templated_crud_policy is not None:
                self._values["ses_bulk_templated_crud_policy"] = ses_bulk_templated_crud_policy
            if ses_crud_policy is not None:
                self._values["ses_crud_policy"] = ses_crud_policy
            if ses_email_template_crud_policy is not None:
                self._values["ses_email_template_crud_policy"] = ses_email_template_crud_policy
            if ses_send_bounce_policy is not None:
                self._values["ses_send_bounce_policy"] = ses_send_bounce_policy
            if sns_crud_policy is not None:
                self._values["sns_crud_policy"] = sns_crud_policy
            if sns_publish_message_policy is not None:
                self._values["sns_publish_message_policy"] = sns_publish_message_policy
            if sqs_poller_policy is not None:
                self._values["sqs_poller_policy"] = sqs_poller_policy
            if sqs_send_message_policy is not None:
                self._values["sqs_send_message_policy"] = sqs_send_message_policy
            if ssm_parameter_read_policy is not None:
                self._values["ssm_parameter_read_policy"] = ssm_parameter_read_policy
            if step_functions_execution_policy is not None:
                self._values["step_functions_execution_policy"] = step_functions_execution_policy
            if vpc_access_policy is not None:
                self._values["vpc_access_policy"] = vpc_access_policy

        @builtins.property
        def ami_describe_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EmptySAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-amidescribepolicy
            '''
            result = self._values.get("ami_describe_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EmptySAMPTProperty"]], result)

        @builtins.property
        def aws_secrets_manager_get_secret_value_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.SecretArnSAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-awssecretsmanagergetsecretvaluepolicy
            '''
            result = self._values.get("aws_secrets_manager_get_secret_value_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.SecretArnSAMPTProperty"]], result)

        @builtins.property
        def cloud_formation_describe_stacks_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EmptySAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-cloudformationdescribestackspolicy
            '''
            result = self._values.get("cloud_formation_describe_stacks_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EmptySAMPTProperty"]], result)

        @builtins.property
        def cloud_watch_put_metric_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EmptySAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-cloudwatchputmetricpolicy
            '''
            result = self._values.get("cloud_watch_put_metric_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EmptySAMPTProperty"]], result)

        @builtins.property
        def dynamo_db_crud_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.TableSAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-dynamodbcrudpolicy
            '''
            result = self._values.get("dynamo_db_crud_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.TableSAMPTProperty"]], result)

        @builtins.property
        def dynamo_db_read_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.TableSAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-dynamodbreadpolicy
            '''
            result = self._values.get("dynamo_db_read_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.TableSAMPTProperty"]], result)

        @builtins.property
        def dynamo_db_stream_read_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.TableStreamSAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-dynamodbstreamreadpolicy
            '''
            result = self._values.get("dynamo_db_stream_read_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.TableStreamSAMPTProperty"]], result)

        @builtins.property
        def dynamo_db_write_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.TableSAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-dynamodbwritepolicy
            '''
            result = self._values.get("dynamo_db_write_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.TableSAMPTProperty"]], result)

        @builtins.property
        def ec2_describe_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EmptySAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-ec2describepolicy
            '''
            result = self._values.get("ec2_describe_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EmptySAMPTProperty"]], result)

        @builtins.property
        def elasticsearch_http_post_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.DomainSAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-elasticsearchhttppostpolicy
            '''
            result = self._values.get("elasticsearch_http_post_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.DomainSAMPTProperty"]], result)

        @builtins.property
        def filter_log_events_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.LogGroupSAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-filterlogeventspolicy
            '''
            result = self._values.get("filter_log_events_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.LogGroupSAMPTProperty"]], result)

        @builtins.property
        def kinesis_crud_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.StreamSAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-kinesiscrudpolicy
            '''
            result = self._values.get("kinesis_crud_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.StreamSAMPTProperty"]], result)

        @builtins.property
        def kinesis_stream_read_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.StreamSAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-kinesisstreamreadpolicy
            '''
            result = self._values.get("kinesis_stream_read_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.StreamSAMPTProperty"]], result)

        @builtins.property
        def kms_decrypt_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.KeySAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-kmsdecryptpolicy
            '''
            result = self._values.get("kms_decrypt_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.KeySAMPTProperty"]], result)

        @builtins.property
        def lambda_invoke_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.FunctionSAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-lambdainvokepolicy
            '''
            result = self._values.get("lambda_invoke_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.FunctionSAMPTProperty"]], result)

        @builtins.property
        def rekognition_detect_only_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EmptySAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-rekognitiondetectonlypolicy
            '''
            result = self._values.get("rekognition_detect_only_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EmptySAMPTProperty"]], result)

        @builtins.property
        def rekognition_labels_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EmptySAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-rekognitionlabelspolicy
            '''
            result = self._values.get("rekognition_labels_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EmptySAMPTProperty"]], result)

        @builtins.property
        def rekognition_no_data_access_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.CollectionSAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-rekognitionnodataaccesspolicy
            '''
            result = self._values.get("rekognition_no_data_access_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.CollectionSAMPTProperty"]], result)

        @builtins.property
        def rekognition_read_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.CollectionSAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-rekognitionreadpolicy
            '''
            result = self._values.get("rekognition_read_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.CollectionSAMPTProperty"]], result)

        @builtins.property
        def rekognition_write_only_access_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.CollectionSAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-rekognitionwriteonlyaccesspolicy
            '''
            result = self._values.get("rekognition_write_only_access_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.CollectionSAMPTProperty"]], result)

        @builtins.property
        def s3_crud_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.BucketSAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-s3crudpolicy
            '''
            result = self._values.get("s3_crud_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.BucketSAMPTProperty"]], result)

        @builtins.property
        def s3_read_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.BucketSAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-s3readpolicy
            '''
            result = self._values.get("s3_read_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.BucketSAMPTProperty"]], result)

        @builtins.property
        def s3_write_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.BucketSAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-s3writepolicy
            '''
            result = self._values.get("s3_write_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.BucketSAMPTProperty"]], result)

        @builtins.property
        def ses_bulk_templated_crud_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.IdentitySAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-sesbulktemplatedcrudpolicy
            '''
            result = self._values.get("ses_bulk_templated_crud_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.IdentitySAMPTProperty"]], result)

        @builtins.property
        def ses_crud_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.IdentitySAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-sescrudpolicy
            '''
            result = self._values.get("ses_crud_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.IdentitySAMPTProperty"]], result)

        @builtins.property
        def ses_email_template_crud_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EmptySAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-sesemailtemplatecrudpolicy
            '''
            result = self._values.get("ses_email_template_crud_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EmptySAMPTProperty"]], result)

        @builtins.property
        def ses_send_bounce_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.IdentitySAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-sessendbouncepolicy
            '''
            result = self._values.get("ses_send_bounce_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.IdentitySAMPTProperty"]], result)

        @builtins.property
        def sns_crud_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.TopicSAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-snscrudpolicy
            '''
            result = self._values.get("sns_crud_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.TopicSAMPTProperty"]], result)

        @builtins.property
        def sns_publish_message_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.TopicSAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-snspublishmessagepolicy
            '''
            result = self._values.get("sns_publish_message_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.TopicSAMPTProperty"]], result)

        @builtins.property
        def sqs_poller_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.QueueSAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-sqspollerpolicy
            '''
            result = self._values.get("sqs_poller_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.QueueSAMPTProperty"]], result)

        @builtins.property
        def sqs_send_message_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.QueueSAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-sqssendmessagepolicy
            '''
            result = self._values.get("sqs_send_message_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.QueueSAMPTProperty"]], result)

        @builtins.property
        def ssm_parameter_read_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.ParameterNameSAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-ssmparameterreadpolicy
            '''
            result = self._values.get("ssm_parameter_read_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.ParameterNameSAMPTProperty"]], result)

        @builtins.property
        def step_functions_execution_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.StateMachineSAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-stepfunctionsexecutionpolicy
            '''
            result = self._values.get("step_functions_execution_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.StateMachineSAMPTProperty"]], result)

        @builtins.property
        def vpc_access_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EmptySAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sampolicytemplate.html#cfn-serverless-function-sampolicytemplate-vpcaccesspolicy
            '''
            result = self._values.get("vpc_access_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EmptySAMPTProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SAMPolicyTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.SNSEventProperty",
        jsii_struct_bases=[],
        name_mapping={"topic": "topic"},
    )
    class SNSEventProperty:
        def __init__(self, *, topic: typing.Optional[builtins.str] = None) -> None:
            '''
            :param topic: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-snsevent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                s_nSEvent_property = sam_mixins.CfnFunctionPropsMixin.SNSEventProperty(
                    topic="topic"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7bba23a0d3b76110d193f1a9ee585e26081cd7bd81dbe4e34b328786ca57c506)
                check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if topic is not None:
                self._values["topic"] = topic

        @builtins.property
        def topic(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-snsevent.html#cfn-serverless-function-snsevent-topic
            '''
            result = self._values.get("topic")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SNSEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.SQSEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "batch_size": "batchSize",
            "enabled": "enabled",
            "queue": "queue",
        },
    )
    class SQSEventProperty:
        def __init__(
            self,
            *,
            batch_size: typing.Optional[jsii.Number] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            queue: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param batch_size: 
            :param enabled: 
            :param queue: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sqsevent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                s_qSEvent_property = sam_mixins.CfnFunctionPropsMixin.SQSEventProperty(
                    batch_size=123,
                    enabled=False,
                    queue="queue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0abba944b461672636b2d68e7b60953184f2a67012f4a9f0b8437f7b6006aac2)
                check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if batch_size is not None:
                self._values["batch_size"] = batch_size
            if enabled is not None:
                self._values["enabled"] = enabled
            if queue is not None:
                self._values["queue"] = queue

        @builtins.property
        def batch_size(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sqsevent.html#cfn-serverless-function-sqsevent-batchsize
            '''
            result = self._values.get("batch_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sqsevent.html#cfn-serverless-function-sqsevent-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def queue(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-sqsevent.html#cfn-serverless-function-sqsevent-queue
            '''
            result = self._values.get("queue")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SQSEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.ScheduleEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "enabled": "enabled",
            "input": "input",
            "name": "name",
            "schedule": "schedule",
        },
    )
    class ScheduleEventProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            input: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            schedule: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param description: 
            :param enabled: 
            :param input: 
            :param name: 
            :param schedule: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-scheduleevent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                schedule_event_property = sam_mixins.CfnFunctionPropsMixin.ScheduleEventProperty(
                    description="description",
                    enabled=False,
                    input="input",
                    name="name",
                    schedule="schedule"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b43e00e4242408b7aa31aa5148d1484d8828cd1e57b081f10eafe8b258d9959b)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument input", value=input, expected_type=type_hints["input"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if enabled is not None:
                self._values["enabled"] = enabled
            if input is not None:
                self._values["input"] = input
            if name is not None:
                self._values["name"] = name
            if schedule is not None:
                self._values["schedule"] = schedule

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-scheduleevent.html#cfn-serverless-function-scheduleevent-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-scheduleevent.html#cfn-serverless-function-scheduleevent-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-scheduleevent.html#cfn-serverless-function-scheduleevent-input
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-scheduleevent.html#cfn-serverless-function-scheduleevent-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schedule(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-scheduleevent.html#cfn-serverless-function-scheduleevent-schedule
            '''
            result = self._values.get("schedule")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.SecretArnSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"secret_arn": "secretArn"},
    )
    class SecretArnSAMPTProperty:
        def __init__(self, *, secret_arn: typing.Optional[builtins.str] = None) -> None:
            '''
            :param secret_arn: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-secretarnsampt.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                secret_arn_sAMPTProperty = sam_mixins.CfnFunctionPropsMixin.SecretArnSAMPTProperty(
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7450b8cae5c1a69e248462035fa55b5c2c8d34c48ae0a7ae6d0f9d8fe19744c5)
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-secretarnsampt.html#cfn-serverless-function-secretarnsampt-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecretArnSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.StateMachineSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"state_machine_name": "stateMachineName"},
    )
    class StateMachineSAMPTProperty:
        def __init__(
            self,
            *,
            state_machine_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param state_machine_name: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-statemachinesampt.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                state_machine_sAMPTProperty = sam_mixins.CfnFunctionPropsMixin.StateMachineSAMPTProperty(
                    state_machine_name="stateMachineName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__703c4cfb2ecdcb596fd8ba749139314dc12eed72ccccebb9c1e7ad68c3088ad7)
                check_type(argname="argument state_machine_name", value=state_machine_name, expected_type=type_hints["state_machine_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if state_machine_name is not None:
                self._values["state_machine_name"] = state_machine_name

        @builtins.property
        def state_machine_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-statemachinesampt.html#cfn-serverless-function-statemachinesampt-statemachinename
            '''
            result = self._values.get("state_machine_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StateMachineSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.StreamSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"stream_name": "streamName"},
    )
    class StreamSAMPTProperty:
        def __init__(
            self,
            *,
            stream_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param stream_name: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-streamsampt.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                stream_sAMPTProperty = sam_mixins.CfnFunctionPropsMixin.StreamSAMPTProperty(
                    stream_name="streamName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9d16ead8efff530b0659dbfc14ce855ddfcbd9c2fddf15b3498baa49ddd699e5)
                check_type(argname="argument stream_name", value=stream_name, expected_type=type_hints["stream_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if stream_name is not None:
                self._values["stream_name"] = stream_name

        @builtins.property
        def stream_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-streamsampt.html#cfn-serverless-function-streamsampt-streamname
            '''
            result = self._values.get("stream_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.TableSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"table_name": "tableName"},
    )
    class TableSAMPTProperty:
        def __init__(self, *, table_name: typing.Optional[builtins.str] = None) -> None:
            '''
            :param table_name: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-tablesampt.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                table_sAMPTProperty = sam_mixins.CfnFunctionPropsMixin.TableSAMPTProperty(
                    table_name="tableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dec4839878a7f641773b46b95bca262a3b0808b76d7c07b21d0a412fda9ad32f)
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if table_name is not None:
                self._values["table_name"] = table_name

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-tablesampt.html#cfn-serverless-function-tablesampt-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TableSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.TableStreamSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"stream_name": "streamName", "table_name": "tableName"},
    )
    class TableStreamSAMPTProperty:
        def __init__(
            self,
            *,
            stream_name: typing.Optional[builtins.str] = None,
            table_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param stream_name: 
            :param table_name: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-tablestreamsampt.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                table_stream_sAMPTProperty = sam_mixins.CfnFunctionPropsMixin.TableStreamSAMPTProperty(
                    stream_name="streamName",
                    table_name="tableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__04e6bb4c45eee1263c78036615fa3cce1b79d6ac2bc58c9b1272baa02882d7cc)
                check_type(argname="argument stream_name", value=stream_name, expected_type=type_hints["stream_name"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if stream_name is not None:
                self._values["stream_name"] = stream_name
            if table_name is not None:
                self._values["table_name"] = table_name

        @builtins.property
        def stream_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-tablestreamsampt.html#cfn-serverless-function-tablestreamsampt-streamname
            '''
            result = self._values.get("stream_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-tablestreamsampt.html#cfn-serverless-function-tablestreamsampt-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TableStreamSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.TopicSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"topic_name": "topicName"},
    )
    class TopicSAMPTProperty:
        def __init__(self, *, topic_name: typing.Optional[builtins.str] = None) -> None:
            '''
            :param topic_name: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-topicsampt.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                topic_sAMPTProperty = sam_mixins.CfnFunctionPropsMixin.TopicSAMPTProperty(
                    topic_name="topicName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__24682dc3027e1c2fca6de8ff4333b7d89e5432e610ca13b336dd7187dccfb012)
                check_type(argname="argument topic_name", value=topic_name, expected_type=type_hints["topic_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if topic_name is not None:
                self._values["topic_name"] = topic_name

        @builtins.property
        def topic_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-topicsampt.html#cfn-serverless-function-topicsampt-topicname
            '''
            result = self._values.get("topic_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TopicSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnFunctionPropsMixin.VpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class VpcConfigProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param security_group_ids: 
            :param subnet_ids: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-vpcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                vpc_config_property = sam_mixins.CfnFunctionPropsMixin.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__97f468271f57ead7995ad7a5b46e55ba72928f7d5eb606cc939b2d01bb97b676)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-vpcconfig.html#cfn-serverless-function-vpcconfig-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-function-vpcconfig.html#cfn-serverless-function-vpcconfig-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnHttpApiMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_log_setting": "accessLogSetting",
        "auth": "auth",
        "cors_configuration": "corsConfiguration",
        "default_route_settings": "defaultRouteSettings",
        "definition_body": "definitionBody",
        "definition_uri": "definitionUri",
        "description": "description",
        "disable_execute_api_endpoint": "disableExecuteApiEndpoint",
        "domain": "domain",
        "fail_on_warnings": "failOnWarnings",
        "route_settings": "routeSettings",
        "stage_name": "stageName",
        "stage_variables": "stageVariables",
        "tags": "tags",
    },
)
class CfnHttpApiMixinProps:
    def __init__(
        self,
        *,
        access_log_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnHttpApiPropsMixin.AccessLogSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        auth: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnHttpApiPropsMixin.HttpApiAuthProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        cors_configuration: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable, typing.Union["CfnHttpApiPropsMixin.CorsConfigurationObjectProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        default_route_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnHttpApiPropsMixin.RouteSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        definition_body: typing.Any = None,
        definition_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union["CfnHttpApiPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        domain: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnHttpApiPropsMixin.HttpApiDomainConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        fail_on_warnings: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        route_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnHttpApiPropsMixin.RouteSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        stage_name: typing.Optional[builtins.str] = None,
        stage_variables: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnHttpApiPropsMixin.

        :param access_log_setting: 
        :param auth: 
        :param cors_configuration: 
        :param default_route_settings: 
        :param definition_body: 
        :param definition_uri: 
        :param description: 
        :param disable_execute_api_endpoint: 
        :param domain: 
        :param fail_on_warnings: 
        :param route_settings: 
        :param stage_name: 
        :param stage_variables: 
        :param tags: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-httpapi.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
            
            # authorizers: Any
            # definition_body: Any
            
            cfn_http_api_mixin_props = sam_mixins.CfnHttpApiMixinProps(
                access_log_setting=sam_mixins.CfnHttpApiPropsMixin.AccessLogSettingProperty(
                    destination_arn="destinationArn",
                    format="format"
                ),
                auth=sam_mixins.CfnHttpApiPropsMixin.HttpApiAuthProperty(
                    authorizers=authorizers,
                    default_authorizer="defaultAuthorizer"
                ),
                cors_configuration=False,
                default_route_settings=sam_mixins.CfnHttpApiPropsMixin.RouteSettingsProperty(
                    data_trace_enabled=False,
                    detailed_metrics_enabled=False,
                    logging_level="loggingLevel",
                    throttling_burst_limit=123,
                    throttling_rate_limit=123
                ),
                definition_body=definition_body,
                definition_uri="definitionUri",
                description="description",
                disable_execute_api_endpoint=False,
                domain=sam_mixins.CfnHttpApiPropsMixin.HttpApiDomainConfigurationProperty(
                    base_path="basePath",
                    certificate_arn="certificateArn",
                    domain_name="domainName",
                    endpoint_configuration="endpointConfiguration",
                    mutual_tls_authentication=sam_mixins.CfnHttpApiPropsMixin.MutualTlsAuthenticationProperty(
                        truststore_uri="truststoreUri",
                        truststore_version=False
                    ),
                    route53=sam_mixins.CfnHttpApiPropsMixin.Route53ConfigurationProperty(
                        distributed_domain_name="distributedDomainName",
                        evaluate_target_health=False,
                        hosted_zone_id="hostedZoneId",
                        hosted_zone_name="hostedZoneName",
                        ip_v6=False
                    ),
                    security_policy="securityPolicy"
                ),
                fail_on_warnings=False,
                route_settings=sam_mixins.CfnHttpApiPropsMixin.RouteSettingsProperty(
                    data_trace_enabled=False,
                    detailed_metrics_enabled=False,
                    logging_level="loggingLevel",
                    throttling_burst_limit=123,
                    throttling_rate_limit=123
                ),
                stage_name="stageName",
                stage_variables={
                    "stage_variables_key": "stageVariables"
                },
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b895fa0e13b2939c6c10c91b22b89be09dfbffe03d799dce049d830def349b3f)
            check_type(argname="argument access_log_setting", value=access_log_setting, expected_type=type_hints["access_log_setting"])
            check_type(argname="argument auth", value=auth, expected_type=type_hints["auth"])
            check_type(argname="argument cors_configuration", value=cors_configuration, expected_type=type_hints["cors_configuration"])
            check_type(argname="argument default_route_settings", value=default_route_settings, expected_type=type_hints["default_route_settings"])
            check_type(argname="argument definition_body", value=definition_body, expected_type=type_hints["definition_body"])
            check_type(argname="argument definition_uri", value=definition_uri, expected_type=type_hints["definition_uri"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disable_execute_api_endpoint", value=disable_execute_api_endpoint, expected_type=type_hints["disable_execute_api_endpoint"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument fail_on_warnings", value=fail_on_warnings, expected_type=type_hints["fail_on_warnings"])
            check_type(argname="argument route_settings", value=route_settings, expected_type=type_hints["route_settings"])
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
            check_type(argname="argument stage_variables", value=stage_variables, expected_type=type_hints["stage_variables"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_log_setting is not None:
            self._values["access_log_setting"] = access_log_setting
        if auth is not None:
            self._values["auth"] = auth
        if cors_configuration is not None:
            self._values["cors_configuration"] = cors_configuration
        if default_route_settings is not None:
            self._values["default_route_settings"] = default_route_settings
        if definition_body is not None:
            self._values["definition_body"] = definition_body
        if definition_uri is not None:
            self._values["definition_uri"] = definition_uri
        if description is not None:
            self._values["description"] = description
        if disable_execute_api_endpoint is not None:
            self._values["disable_execute_api_endpoint"] = disable_execute_api_endpoint
        if domain is not None:
            self._values["domain"] = domain
        if fail_on_warnings is not None:
            self._values["fail_on_warnings"] = fail_on_warnings
        if route_settings is not None:
            self._values["route_settings"] = route_settings
        if stage_name is not None:
            self._values["stage_name"] = stage_name
        if stage_variables is not None:
            self._values["stage_variables"] = stage_variables
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def access_log_setting(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHttpApiPropsMixin.AccessLogSettingProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-httpapi.html#cfn-serverless-httpapi-accesslogsetting
        '''
        result = self._values.get("access_log_setting")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHttpApiPropsMixin.AccessLogSettingProperty"]], result)

    @builtins.property
    def auth(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHttpApiPropsMixin.HttpApiAuthProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-httpapi.html#cfn-serverless-httpapi-auth
        '''
        result = self._values.get("auth")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHttpApiPropsMixin.HttpApiAuthProperty"]], result)

    @builtins.property
    def cors_configuration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable, "CfnHttpApiPropsMixin.CorsConfigurationObjectProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-httpapi.html#cfn-serverless-httpapi-corsconfiguration
        '''
        result = self._values.get("cors_configuration")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable, "CfnHttpApiPropsMixin.CorsConfigurationObjectProperty"]], result)

    @builtins.property
    def default_route_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHttpApiPropsMixin.RouteSettingsProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-httpapi.html#cfn-serverless-httpapi-defaultroutesettings
        '''
        result = self._values.get("default_route_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHttpApiPropsMixin.RouteSettingsProperty"]], result)

    @builtins.property
    def definition_body(self) -> typing.Any:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-httpapi.html#cfn-serverless-httpapi-definitionbody
        '''
        result = self._values.get("definition_body")
        return typing.cast(typing.Any, result)

    @builtins.property
    def definition_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnHttpApiPropsMixin.S3LocationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-httpapi.html#cfn-serverless-httpapi-definitionuri
        '''
        result = self._values.get("definition_uri")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnHttpApiPropsMixin.S3LocationProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-httpapi.html#cfn-serverless-httpapi-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_execute_api_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-httpapi.html#cfn-serverless-httpapi-disableexecuteapiendpoint
        '''
        result = self._values.get("disable_execute_api_endpoint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def domain(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHttpApiPropsMixin.HttpApiDomainConfigurationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-httpapi.html#cfn-serverless-httpapi-domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHttpApiPropsMixin.HttpApiDomainConfigurationProperty"]], result)

    @builtins.property
    def fail_on_warnings(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-httpapi.html#cfn-serverless-httpapi-failonwarnings
        '''
        result = self._values.get("fail_on_warnings")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def route_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHttpApiPropsMixin.RouteSettingsProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-httpapi.html#cfn-serverless-httpapi-routesettings
        '''
        result = self._values.get("route_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHttpApiPropsMixin.RouteSettingsProperty"]], result)

    @builtins.property
    def stage_name(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-httpapi.html#cfn-serverless-httpapi-stagename
        '''
        result = self._values.get("stage_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage_variables(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-httpapi.html#cfn-serverless-httpapi-stagevariables
        '''
        result = self._values.get("stage_variables")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-httpapi.html#cfn-serverless-httpapi-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnHttpApiMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnHttpApiPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnHttpApiPropsMixin",
):
    '''https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-httpapi.html
    :cloudformationResource: AWS::Serverless::HttpApi
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
        
        # authorizers: Any
        # definition_body: Any
        
        cfn_http_api_props_mixin = sam_mixins.CfnHttpApiPropsMixin(sam_mixins.CfnHttpApiMixinProps(
            access_log_setting=sam_mixins.CfnHttpApiPropsMixin.AccessLogSettingProperty(
                destination_arn="destinationArn",
                format="format"
            ),
            auth=sam_mixins.CfnHttpApiPropsMixin.HttpApiAuthProperty(
                authorizers=authorizers,
                default_authorizer="defaultAuthorizer"
            ),
            cors_configuration=False,
            default_route_settings=sam_mixins.CfnHttpApiPropsMixin.RouteSettingsProperty(
                data_trace_enabled=False,
                detailed_metrics_enabled=False,
                logging_level="loggingLevel",
                throttling_burst_limit=123,
                throttling_rate_limit=123
            ),
            definition_body=definition_body,
            definition_uri="definitionUri",
            description="description",
            disable_execute_api_endpoint=False,
            domain=sam_mixins.CfnHttpApiPropsMixin.HttpApiDomainConfigurationProperty(
                base_path="basePath",
                certificate_arn="certificateArn",
                domain_name="domainName",
                endpoint_configuration="endpointConfiguration",
                mutual_tls_authentication=sam_mixins.CfnHttpApiPropsMixin.MutualTlsAuthenticationProperty(
                    truststore_uri="truststoreUri",
                    truststore_version=False
                ),
                route53=sam_mixins.CfnHttpApiPropsMixin.Route53ConfigurationProperty(
                    distributed_domain_name="distributedDomainName",
                    evaluate_target_health=False,
                    hosted_zone_id="hostedZoneId",
                    hosted_zone_name="hostedZoneName",
                    ip_v6=False
                ),
                security_policy="securityPolicy"
            ),
            fail_on_warnings=False,
            route_settings=sam_mixins.CfnHttpApiPropsMixin.RouteSettingsProperty(
                data_trace_enabled=False,
                detailed_metrics_enabled=False,
                logging_level="loggingLevel",
                throttling_burst_limit=123,
                throttling_rate_limit=123
            ),
            stage_name="stageName",
            stage_variables={
                "stage_variables_key": "stageVariables"
            },
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnHttpApiMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Serverless::HttpApi``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94c2f00880f0ddb403b03a96c40b73635c39f512a6dce25c4350b130fafc3186)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbd131721f509fbb05eeee84daf3379bb77247e94a8d4ea25afbac0e39301ca2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da057acbc7e6cb09d9c613ffb594cc8ffdfb086b317c31ab9c7bbd2d9eae5ef5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnHttpApiMixinProps:
        return typing.cast(CfnHttpApiMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnHttpApiPropsMixin.AccessLogSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"destination_arn": "destinationArn", "format": "format"},
    )
    class AccessLogSettingProperty:
        def __init__(
            self,
            *,
            destination_arn: typing.Optional[builtins.str] = None,
            format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param destination_arn: 
            :param format: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-accesslogsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                access_log_setting_property = sam_mixins.CfnHttpApiPropsMixin.AccessLogSettingProperty(
                    destination_arn="destinationArn",
                    format="format"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7a49847edc78aa09cc889a816cfc2969c0f5fdffb8ea48efd25083845b607509)
                check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
                check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_arn is not None:
                self._values["destination_arn"] = destination_arn
            if format is not None:
                self._values["format"] = format

        @builtins.property
        def destination_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-accesslogsetting.html#cfn-serverless-httpapi-accesslogsetting-destinationarn
            '''
            result = self._values.get("destination_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def format(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-accesslogsetting.html#cfn-serverless-httpapi-accesslogsetting-format
            '''
            result = self._values.get("format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessLogSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnHttpApiPropsMixin.CorsConfigurationObjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_credentials": "allowCredentials",
            "allow_headers": "allowHeaders",
            "allow_methods": "allowMethods",
            "allow_origins": "allowOrigins",
            "expose_headers": "exposeHeaders",
            "max_age": "maxAge",
        },
    )
    class CorsConfigurationObjectProperty:
        def __init__(
            self,
            *,
            allow_credentials: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            allow_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
            allow_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
            allow_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
            expose_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
            max_age: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param allow_credentials: 
            :param allow_headers: 
            :param allow_methods: 
            :param allow_origins: 
            :param expose_headers: 
            :param max_age: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-corsconfigurationobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                cors_configuration_object_property = sam_mixins.CfnHttpApiPropsMixin.CorsConfigurationObjectProperty(
                    allow_credentials=False,
                    allow_headers=["allowHeaders"],
                    allow_methods=["allowMethods"],
                    allow_origins=["allowOrigins"],
                    expose_headers=["exposeHeaders"],
                    max_age=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b9ef9b5ed0b9fabba748b3732e2143e7171f57822af49246e691a8e99d5d7874)
                check_type(argname="argument allow_credentials", value=allow_credentials, expected_type=type_hints["allow_credentials"])
                check_type(argname="argument allow_headers", value=allow_headers, expected_type=type_hints["allow_headers"])
                check_type(argname="argument allow_methods", value=allow_methods, expected_type=type_hints["allow_methods"])
                check_type(argname="argument allow_origins", value=allow_origins, expected_type=type_hints["allow_origins"])
                check_type(argname="argument expose_headers", value=expose_headers, expected_type=type_hints["expose_headers"])
                check_type(argname="argument max_age", value=max_age, expected_type=type_hints["max_age"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allow_credentials is not None:
                self._values["allow_credentials"] = allow_credentials
            if allow_headers is not None:
                self._values["allow_headers"] = allow_headers
            if allow_methods is not None:
                self._values["allow_methods"] = allow_methods
            if allow_origins is not None:
                self._values["allow_origins"] = allow_origins
            if expose_headers is not None:
                self._values["expose_headers"] = expose_headers
            if max_age is not None:
                self._values["max_age"] = max_age

        @builtins.property
        def allow_credentials(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-corsconfigurationobject.html#cfn-serverless-httpapi-corsconfigurationobject-allowcredentials
            '''
            result = self._values.get("allow_credentials")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def allow_headers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-corsconfigurationobject.html#cfn-serverless-httpapi-corsconfigurationobject-allowheaders
            '''
            result = self._values.get("allow_headers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allow_methods(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-corsconfigurationobject.html#cfn-serverless-httpapi-corsconfigurationobject-allowmethods
            '''
            result = self._values.get("allow_methods")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allow_origins(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-corsconfigurationobject.html#cfn-serverless-httpapi-corsconfigurationobject-alloworigins
            '''
            result = self._values.get("allow_origins")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def expose_headers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-corsconfigurationobject.html#cfn-serverless-httpapi-corsconfigurationobject-exposeheaders
            '''
            result = self._values.get("expose_headers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def max_age(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-corsconfigurationobject.html#cfn-serverless-httpapi-corsconfigurationobject-maxage
            '''
            result = self._values.get("max_age")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CorsConfigurationObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnHttpApiPropsMixin.HttpApiAuthProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorizers": "authorizers",
            "default_authorizer": "defaultAuthorizer",
        },
    )
    class HttpApiAuthProperty:
        def __init__(
            self,
            *,
            authorizers: typing.Any = None,
            default_authorizer: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param authorizers: 
            :param default_authorizer: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-httpapiauth.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                # authorizers: Any
                
                http_api_auth_property = sam_mixins.CfnHttpApiPropsMixin.HttpApiAuthProperty(
                    authorizers=authorizers,
                    default_authorizer="defaultAuthorizer"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c473c92c3b412bb116159ff4abe6cb8ed0e99e0c6e5e555a0d59ad89bed65261)
                check_type(argname="argument authorizers", value=authorizers, expected_type=type_hints["authorizers"])
                check_type(argname="argument default_authorizer", value=default_authorizer, expected_type=type_hints["default_authorizer"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authorizers is not None:
                self._values["authorizers"] = authorizers
            if default_authorizer is not None:
                self._values["default_authorizer"] = default_authorizer

        @builtins.property
        def authorizers(self) -> typing.Any:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-httpapiauth.html#cfn-serverless-httpapi-httpapiauth-authorizers
            '''
            result = self._values.get("authorizers")
            return typing.cast(typing.Any, result)

        @builtins.property
        def default_authorizer(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-httpapiauth.html#cfn-serverless-httpapi-httpapiauth-defaultauthorizer
            '''
            result = self._values.get("default_authorizer")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpApiAuthProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnHttpApiPropsMixin.HttpApiDomainConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "base_path": "basePath",
            "certificate_arn": "certificateArn",
            "domain_name": "domainName",
            "endpoint_configuration": "endpointConfiguration",
            "mutual_tls_authentication": "mutualTlsAuthentication",
            "route53": "route53",
            "security_policy": "securityPolicy",
        },
    )
    class HttpApiDomainConfigurationProperty:
        def __init__(
            self,
            *,
            base_path: typing.Optional[builtins.str] = None,
            certificate_arn: typing.Optional[builtins.str] = None,
            domain_name: typing.Optional[builtins.str] = None,
            endpoint_configuration: typing.Optional[builtins.str] = None,
            mutual_tls_authentication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnHttpApiPropsMixin.MutualTlsAuthenticationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            route53: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnHttpApiPropsMixin.Route53ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            security_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param base_path: 
            :param certificate_arn: 
            :param domain_name: 
            :param endpoint_configuration: 
            :param mutual_tls_authentication: 
            :param route53: 
            :param security_policy: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-httpapidomainconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                http_api_domain_configuration_property = sam_mixins.CfnHttpApiPropsMixin.HttpApiDomainConfigurationProperty(
                    base_path="basePath",
                    certificate_arn="certificateArn",
                    domain_name="domainName",
                    endpoint_configuration="endpointConfiguration",
                    mutual_tls_authentication=sam_mixins.CfnHttpApiPropsMixin.MutualTlsAuthenticationProperty(
                        truststore_uri="truststoreUri",
                        truststore_version=False
                    ),
                    route53=sam_mixins.CfnHttpApiPropsMixin.Route53ConfigurationProperty(
                        distributed_domain_name="distributedDomainName",
                        evaluate_target_health=False,
                        hosted_zone_id="hostedZoneId",
                        hosted_zone_name="hostedZoneName",
                        ip_v6=False
                    ),
                    security_policy="securityPolicy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__11f062cefa739962ebe6f5912152d4824f7d6bc8c37c51fdacc602a66900c8cf)
                check_type(argname="argument base_path", value=base_path, expected_type=type_hints["base_path"])
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
                check_type(argname="argument endpoint_configuration", value=endpoint_configuration, expected_type=type_hints["endpoint_configuration"])
                check_type(argname="argument mutual_tls_authentication", value=mutual_tls_authentication, expected_type=type_hints["mutual_tls_authentication"])
                check_type(argname="argument route53", value=route53, expected_type=type_hints["route53"])
                check_type(argname="argument security_policy", value=security_policy, expected_type=type_hints["security_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if base_path is not None:
                self._values["base_path"] = base_path
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn
            if domain_name is not None:
                self._values["domain_name"] = domain_name
            if endpoint_configuration is not None:
                self._values["endpoint_configuration"] = endpoint_configuration
            if mutual_tls_authentication is not None:
                self._values["mutual_tls_authentication"] = mutual_tls_authentication
            if route53 is not None:
                self._values["route53"] = route53
            if security_policy is not None:
                self._values["security_policy"] = security_policy

        @builtins.property
        def base_path(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-httpapidomainconfiguration.html#cfn-serverless-httpapi-httpapidomainconfiguration-basepath
            '''
            result = self._values.get("base_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-httpapidomainconfiguration.html#cfn-serverless-httpapi-httpapidomainconfiguration-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def domain_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-httpapidomainconfiguration.html#cfn-serverless-httpapi-httpapidomainconfiguration-domainname
            '''
            result = self._values.get("domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def endpoint_configuration(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-httpapidomainconfiguration.html#cfn-serverless-httpapi-httpapidomainconfiguration-endpointconfiguration
            '''
            result = self._values.get("endpoint_configuration")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mutual_tls_authentication(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHttpApiPropsMixin.MutualTlsAuthenticationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-httpapidomainconfiguration.html#cfn-serverless-httpapi-httpapidomainconfiguration-mutualtlsauthentication
            '''
            result = self._values.get("mutual_tls_authentication")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHttpApiPropsMixin.MutualTlsAuthenticationProperty"]], result)

        @builtins.property
        def route53(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHttpApiPropsMixin.Route53ConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-httpapidomainconfiguration.html#cfn-serverless-httpapi-httpapidomainconfiguration-route53
            '''
            result = self._values.get("route53")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHttpApiPropsMixin.Route53ConfigurationProperty"]], result)

        @builtins.property
        def security_policy(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-httpapidomainconfiguration.html#cfn-serverless-httpapi-httpapidomainconfiguration-securitypolicy
            '''
            result = self._values.get("security_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpApiDomainConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnHttpApiPropsMixin.MutualTlsAuthenticationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "truststore_uri": "truststoreUri",
            "truststore_version": "truststoreVersion",
        },
    )
    class MutualTlsAuthenticationProperty:
        def __init__(
            self,
            *,
            truststore_uri: typing.Optional[builtins.str] = None,
            truststore_version: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''
            :param truststore_uri: 
            :param truststore_version: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-mutualtlsauthentication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                mutual_tls_authentication_property = sam_mixins.CfnHttpApiPropsMixin.MutualTlsAuthenticationProperty(
                    truststore_uri="truststoreUri",
                    truststore_version=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f3445c4e2c24c9eadcfe4520ff2742eaea390263d642159f47e154e36ba2eb1d)
                check_type(argname="argument truststore_uri", value=truststore_uri, expected_type=type_hints["truststore_uri"])
                check_type(argname="argument truststore_version", value=truststore_version, expected_type=type_hints["truststore_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if truststore_uri is not None:
                self._values["truststore_uri"] = truststore_uri
            if truststore_version is not None:
                self._values["truststore_version"] = truststore_version

        @builtins.property
        def truststore_uri(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-mutualtlsauthentication.html#cfn-serverless-httpapi-mutualtlsauthentication-truststoreuri
            '''
            result = self._values.get("truststore_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def truststore_version(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-mutualtlsauthentication.html#cfn-serverless-httpapi-mutualtlsauthentication-truststoreversion
            '''
            result = self._values.get("truststore_version")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MutualTlsAuthenticationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnHttpApiPropsMixin.Route53ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "distributed_domain_name": "distributedDomainName",
            "evaluate_target_health": "evaluateTargetHealth",
            "hosted_zone_id": "hostedZoneId",
            "hosted_zone_name": "hostedZoneName",
            "ip_v6": "ipV6",
        },
    )
    class Route53ConfigurationProperty:
        def __init__(
            self,
            *,
            distributed_domain_name: typing.Optional[builtins.str] = None,
            evaluate_target_health: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            hosted_zone_id: typing.Optional[builtins.str] = None,
            hosted_zone_name: typing.Optional[builtins.str] = None,
            ip_v6: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''
            :param distributed_domain_name: 
            :param evaluate_target_health: 
            :param hosted_zone_id: 
            :param hosted_zone_name: 
            :param ip_v6: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-route53configuration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                route53_configuration_property = sam_mixins.CfnHttpApiPropsMixin.Route53ConfigurationProperty(
                    distributed_domain_name="distributedDomainName",
                    evaluate_target_health=False,
                    hosted_zone_id="hostedZoneId",
                    hosted_zone_name="hostedZoneName",
                    ip_v6=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cfb738f25fe7dc2772b9a2580c60cb09e457f92fdf8990adab10a64899e4b21c)
                check_type(argname="argument distributed_domain_name", value=distributed_domain_name, expected_type=type_hints["distributed_domain_name"])
                check_type(argname="argument evaluate_target_health", value=evaluate_target_health, expected_type=type_hints["evaluate_target_health"])
                check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
                check_type(argname="argument hosted_zone_name", value=hosted_zone_name, expected_type=type_hints["hosted_zone_name"])
                check_type(argname="argument ip_v6", value=ip_v6, expected_type=type_hints["ip_v6"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if distributed_domain_name is not None:
                self._values["distributed_domain_name"] = distributed_domain_name
            if evaluate_target_health is not None:
                self._values["evaluate_target_health"] = evaluate_target_health
            if hosted_zone_id is not None:
                self._values["hosted_zone_id"] = hosted_zone_id
            if hosted_zone_name is not None:
                self._values["hosted_zone_name"] = hosted_zone_name
            if ip_v6 is not None:
                self._values["ip_v6"] = ip_v6

        @builtins.property
        def distributed_domain_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-route53configuration.html#cfn-serverless-httpapi-route53configuration-distributeddomainname
            '''
            result = self._values.get("distributed_domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def evaluate_target_health(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-route53configuration.html#cfn-serverless-httpapi-route53configuration-evaluatetargethealth
            '''
            result = self._values.get("evaluate_target_health")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def hosted_zone_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-route53configuration.html#cfn-serverless-httpapi-route53configuration-hostedzoneid
            '''
            result = self._values.get("hosted_zone_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hosted_zone_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-route53configuration.html#cfn-serverless-httpapi-route53configuration-hostedzonename
            '''
            result = self._values.get("hosted_zone_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ip_v6(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-route53configuration.html#cfn-serverless-httpapi-route53configuration-ipv6
            '''
            result = self._values.get("ip_v6")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "Route53ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnHttpApiPropsMixin.RouteSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_trace_enabled": "dataTraceEnabled",
            "detailed_metrics_enabled": "detailedMetricsEnabled",
            "logging_level": "loggingLevel",
            "throttling_burst_limit": "throttlingBurstLimit",
            "throttling_rate_limit": "throttlingRateLimit",
        },
    )
    class RouteSettingsProperty:
        def __init__(
            self,
            *,
            data_trace_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            detailed_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            logging_level: typing.Optional[builtins.str] = None,
            throttling_burst_limit: typing.Optional[jsii.Number] = None,
            throttling_rate_limit: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param data_trace_enabled: 
            :param detailed_metrics_enabled: 
            :param logging_level: 
            :param throttling_burst_limit: 
            :param throttling_rate_limit: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-routesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                route_settings_property = sam_mixins.CfnHttpApiPropsMixin.RouteSettingsProperty(
                    data_trace_enabled=False,
                    detailed_metrics_enabled=False,
                    logging_level="loggingLevel",
                    throttling_burst_limit=123,
                    throttling_rate_limit=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__313d8924773dc617d153f8a4d78d84ff04ddf2838ba35bb843a2c099978722d5)
                check_type(argname="argument data_trace_enabled", value=data_trace_enabled, expected_type=type_hints["data_trace_enabled"])
                check_type(argname="argument detailed_metrics_enabled", value=detailed_metrics_enabled, expected_type=type_hints["detailed_metrics_enabled"])
                check_type(argname="argument logging_level", value=logging_level, expected_type=type_hints["logging_level"])
                check_type(argname="argument throttling_burst_limit", value=throttling_burst_limit, expected_type=type_hints["throttling_burst_limit"])
                check_type(argname="argument throttling_rate_limit", value=throttling_rate_limit, expected_type=type_hints["throttling_rate_limit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_trace_enabled is not None:
                self._values["data_trace_enabled"] = data_trace_enabled
            if detailed_metrics_enabled is not None:
                self._values["detailed_metrics_enabled"] = detailed_metrics_enabled
            if logging_level is not None:
                self._values["logging_level"] = logging_level
            if throttling_burst_limit is not None:
                self._values["throttling_burst_limit"] = throttling_burst_limit
            if throttling_rate_limit is not None:
                self._values["throttling_rate_limit"] = throttling_rate_limit

        @builtins.property
        def data_trace_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-routesettings.html#cfn-serverless-httpapi-routesettings-datatraceenabled
            '''
            result = self._values.get("data_trace_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def detailed_metrics_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-routesettings.html#cfn-serverless-httpapi-routesettings-detailedmetricsenabled
            '''
            result = self._values.get("detailed_metrics_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def logging_level(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-routesettings.html#cfn-serverless-httpapi-routesettings-logginglevel
            '''
            result = self._values.get("logging_level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def throttling_burst_limit(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-routesettings.html#cfn-serverless-httpapi-routesettings-throttlingburstlimit
            '''
            result = self._values.get("throttling_burst_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def throttling_rate_limit(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-routesettings.html#cfn-serverless-httpapi-routesettings-throttlingratelimit
            '''
            result = self._values.get("throttling_rate_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RouteSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnHttpApiPropsMixin.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key", "version": "version"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
            version: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param bucket: 
            :param key: 
            :param version: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                s3_location_property = sam_mixins.CfnHttpApiPropsMixin.S3LocationProperty(
                    bucket="bucket",
                    key="key",
                    version=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__059c561d8e199d76fa02e36fb00d58ab95d31dd54211b6a0ff80f6326ba3033e)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if key is not None:
                self._values["key"] = key
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-s3location.html#cfn-serverless-httpapi-s3location-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-s3location.html#cfn-serverless-httpapi-s3location-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-httpapi-s3location.html#cfn-serverless-httpapi-s3location-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnLayerVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "compatible_runtimes": "compatibleRuntimes",
        "content_uri": "contentUri",
        "description": "description",
        "layer_name": "layerName",
        "license_info": "licenseInfo",
        "retention_policy": "retentionPolicy",
    },
)
class CfnLayerVersionMixinProps:
    def __init__(
        self,
        *,
        compatible_runtimes: typing.Optional[typing.Sequence[builtins.str]] = None,
        content_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLayerVersionPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        layer_name: typing.Optional[builtins.str] = None,
        license_info: typing.Optional[builtins.str] = None,
        retention_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnLayerVersionPropsMixin.

        :param compatible_runtimes: 
        :param content_uri: 
        :param description: 
        :param layer_name: 
        :param license_info: 
        :param retention_policy: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-layerversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
            
            cfn_layer_version_mixin_props = sam_mixins.CfnLayerVersionMixinProps(
                compatible_runtimes=["compatibleRuntimes"],
                content_uri="contentUri",
                description="description",
                layer_name="layerName",
                license_info="licenseInfo",
                retention_policy="retentionPolicy"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba973e6219551d992f3dd84a92df77b2968a0996d76f43ccf98a2c8313571b83)
            check_type(argname="argument compatible_runtimes", value=compatible_runtimes, expected_type=type_hints["compatible_runtimes"])
            check_type(argname="argument content_uri", value=content_uri, expected_type=type_hints["content_uri"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument layer_name", value=layer_name, expected_type=type_hints["layer_name"])
            check_type(argname="argument license_info", value=license_info, expected_type=type_hints["license_info"])
            check_type(argname="argument retention_policy", value=retention_policy, expected_type=type_hints["retention_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compatible_runtimes is not None:
            self._values["compatible_runtimes"] = compatible_runtimes
        if content_uri is not None:
            self._values["content_uri"] = content_uri
        if description is not None:
            self._values["description"] = description
        if layer_name is not None:
            self._values["layer_name"] = layer_name
        if license_info is not None:
            self._values["license_info"] = license_info
        if retention_policy is not None:
            self._values["retention_policy"] = retention_policy

    @builtins.property
    def compatible_runtimes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-layerversion.html#cfn-serverless-layerversion-compatibleruntimes
        '''
        result = self._values.get("compatible_runtimes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def content_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnLayerVersionPropsMixin.S3LocationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-layerversion.html#cfn-serverless-layerversion-contenturi
        '''
        result = self._values.get("content_uri")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnLayerVersionPropsMixin.S3LocationProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-layerversion.html#cfn-serverless-layerversion-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def layer_name(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-layerversion.html#cfn-serverless-layerversion-layername
        '''
        result = self._values.get("layer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license_info(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-layerversion.html#cfn-serverless-layerversion-licenseinfo
        '''
        result = self._values.get("license_info")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_policy(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-layerversion.html#cfn-serverless-layerversion-retentionpolicy
        '''
        result = self._values.get("retention_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLayerVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLayerVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnLayerVersionPropsMixin",
):
    '''https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-layerversion.html
    :cloudformationResource: AWS::Serverless::LayerVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
        
        cfn_layer_version_props_mixin = sam_mixins.CfnLayerVersionPropsMixin(sam_mixins.CfnLayerVersionMixinProps(
            compatible_runtimes=["compatibleRuntimes"],
            content_uri="contentUri",
            description="description",
            layer_name="layerName",
            license_info="licenseInfo",
            retention_policy="retentionPolicy"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLayerVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Serverless::LayerVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfaa70e25631878c163308fdf24852bb09d97e131854c3f9abebcaaba159f2fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40ce50742d3803970d714e8c9643db626044d01a93da3d06df4dd32d99526109)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b69fc1f0d83008bcdcbdc4c579f9ba820b59dc847cb3392360643669606e78a3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLayerVersionMixinProps:
        return typing.cast(CfnLayerVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnLayerVersionPropsMixin.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key", "version": "version"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
            version: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param bucket: 
            :param key: 
            :param version: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-layerversion-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                s3_location_property = sam_mixins.CfnLayerVersionPropsMixin.S3LocationProperty(
                    bucket="bucket",
                    key="key",
                    version=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d9036f09f6f6b55116f974ad9307b2e1d52bcecb3b35f7e0fec54a932a668f33)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if key is not None:
                self._values["key"] = key
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-layerversion-s3location.html#cfn-serverless-layerversion-s3location-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-layerversion-s3location.html#cfn-serverless-layerversion-s3location-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-layerversion-s3location.html#cfn-serverless-layerversion-s3location-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnSimpleTableMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "primary_key": "primaryKey",
        "provisioned_throughput": "provisionedThroughput",
        "sse_specification": "sseSpecification",
        "table_name": "tableName",
        "tags": "tags",
    },
)
class CfnSimpleTableMixinProps:
    def __init__(
        self,
        *,
        primary_key: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSimpleTablePropsMixin.PrimaryKeyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        provisioned_throughput: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSimpleTablePropsMixin.ProvisionedThroughputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sse_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSimpleTablePropsMixin.SSESpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        table_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnSimpleTablePropsMixin.

        :param primary_key: 
        :param provisioned_throughput: 
        :param sse_specification: 
        :param table_name: 
        :param tags: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-simpletable.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
            
            cfn_simple_table_mixin_props = sam_mixins.CfnSimpleTableMixinProps(
                primary_key=sam_mixins.CfnSimpleTablePropsMixin.PrimaryKeyProperty(
                    name="name",
                    type="type"
                ),
                provisioned_throughput=sam_mixins.CfnSimpleTablePropsMixin.ProvisionedThroughputProperty(
                    read_capacity_units=123,
                    write_capacity_units=123
                ),
                sse_specification=sam_mixins.CfnSimpleTablePropsMixin.SSESpecificationProperty(
                    sse_enabled=False
                ),
                table_name="tableName",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ff61d9ef23e27ae2ae0252ae24afc45c34d13038326b95cd7b40940d42efd2a)
            check_type(argname="argument primary_key", value=primary_key, expected_type=type_hints["primary_key"])
            check_type(argname="argument provisioned_throughput", value=provisioned_throughput, expected_type=type_hints["provisioned_throughput"])
            check_type(argname="argument sse_specification", value=sse_specification, expected_type=type_hints["sse_specification"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if primary_key is not None:
            self._values["primary_key"] = primary_key
        if provisioned_throughput is not None:
            self._values["provisioned_throughput"] = provisioned_throughput
        if sse_specification is not None:
            self._values["sse_specification"] = sse_specification
        if table_name is not None:
            self._values["table_name"] = table_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def primary_key(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSimpleTablePropsMixin.PrimaryKeyProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-simpletable.html#cfn-serverless-simpletable-primarykey
        '''
        result = self._values.get("primary_key")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSimpleTablePropsMixin.PrimaryKeyProperty"]], result)

    @builtins.property
    def provisioned_throughput(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSimpleTablePropsMixin.ProvisionedThroughputProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-simpletable.html#cfn-serverless-simpletable-provisionedthroughput
        '''
        result = self._values.get("provisioned_throughput")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSimpleTablePropsMixin.ProvisionedThroughputProperty"]], result)

    @builtins.property
    def sse_specification(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSimpleTablePropsMixin.SSESpecificationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-simpletable.html#cfn-serverless-simpletable-ssespecification
        '''
        result = self._values.get("sse_specification")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSimpleTablePropsMixin.SSESpecificationProperty"]], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-simpletable.html#cfn-serverless-simpletable-tablename
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-simpletable.html#cfn-serverless-simpletable-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSimpleTableMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSimpleTablePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnSimpleTablePropsMixin",
):
    '''https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-simpletable.html
    :cloudformationResource: AWS::Serverless::SimpleTable
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
        
        cfn_simple_table_props_mixin = sam_mixins.CfnSimpleTablePropsMixin(sam_mixins.CfnSimpleTableMixinProps(
            primary_key=sam_mixins.CfnSimpleTablePropsMixin.PrimaryKeyProperty(
                name="name",
                type="type"
            ),
            provisioned_throughput=sam_mixins.CfnSimpleTablePropsMixin.ProvisionedThroughputProperty(
                read_capacity_units=123,
                write_capacity_units=123
            ),
            sse_specification=sam_mixins.CfnSimpleTablePropsMixin.SSESpecificationProperty(
                sse_enabled=False
            ),
            table_name="tableName",
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSimpleTableMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Serverless::SimpleTable``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a7237cd946619faf8839de5c367d0b2ede1d4a4dc6449e12cf25c6502b3ed1d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca514830aa0768b9a447000967dfa5078eb64c423a72adb0ec2cf3376f8ac261)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3f2e6290f8a84f7fa328ed291fc3ad1985a120c163a3f02560edfc645e7ed7b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSimpleTableMixinProps:
        return typing.cast(CfnSimpleTableMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnSimpleTablePropsMixin.PrimaryKeyProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "type": "type"},
    )
    class PrimaryKeyProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param name: 
            :param type: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-simpletable-primarykey.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                primary_key_property = sam_mixins.CfnSimpleTablePropsMixin.PrimaryKeyProperty(
                    name="name",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__89cd509acfaf49a3a870db2f1613e85290db15391015e4b3317f193b7b0967e4)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-simpletable-primarykey.html#cfn-serverless-simpletable-primarykey-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-simpletable-primarykey.html#cfn-serverless-simpletable-primarykey-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrimaryKeyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnSimpleTablePropsMixin.ProvisionedThroughputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "read_capacity_units": "readCapacityUnits",
            "write_capacity_units": "writeCapacityUnits",
        },
    )
    class ProvisionedThroughputProperty:
        def __init__(
            self,
            *,
            read_capacity_units: typing.Optional[jsii.Number] = None,
            write_capacity_units: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param read_capacity_units: 
            :param write_capacity_units: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-simpletable-provisionedthroughput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                provisioned_throughput_property = sam_mixins.CfnSimpleTablePropsMixin.ProvisionedThroughputProperty(
                    read_capacity_units=123,
                    write_capacity_units=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__670a56bc982e5588a27b3957efdbed409202d1c312919240918a508852cf73f0)
                check_type(argname="argument read_capacity_units", value=read_capacity_units, expected_type=type_hints["read_capacity_units"])
                check_type(argname="argument write_capacity_units", value=write_capacity_units, expected_type=type_hints["write_capacity_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if read_capacity_units is not None:
                self._values["read_capacity_units"] = read_capacity_units
            if write_capacity_units is not None:
                self._values["write_capacity_units"] = write_capacity_units

        @builtins.property
        def read_capacity_units(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-simpletable-provisionedthroughput.html#cfn-serverless-simpletable-provisionedthroughput-readcapacityunits
            '''
            result = self._values.get("read_capacity_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def write_capacity_units(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-simpletable-provisionedthroughput.html#cfn-serverless-simpletable-provisionedthroughput-writecapacityunits
            '''
            result = self._values.get("write_capacity_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisionedThroughputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnSimpleTablePropsMixin.SSESpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"sse_enabled": "sseEnabled"},
    )
    class SSESpecificationProperty:
        def __init__(
            self,
            *,
            sse_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''
            :param sse_enabled: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-simpletable-ssespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                s_sESpecification_property = sam_mixins.CfnSimpleTablePropsMixin.SSESpecificationProperty(
                    sse_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b94eb66cf4d08ef47213890ac26f0ca226cbb2058ae4d389b129b792eb05436b)
                check_type(argname="argument sse_enabled", value=sse_enabled, expected_type=type_hints["sse_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if sse_enabled is not None:
                self._values["sse_enabled"] = sse_enabled

        @builtins.property
        def sse_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-simpletable-ssespecification.html#cfn-serverless-simpletable-ssespecification-sseenabled
            '''
            result = self._values.get("sse_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SSESpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnStateMachineMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "definition": "definition",
        "definition_substitutions": "definitionSubstitutions",
        "definition_uri": "definitionUri",
        "events": "events",
        "logging": "logging",
        "name": "name",
        "permissions_boundaries": "permissionsBoundaries",
        "policies": "policies",
        "role": "role",
        "tags": "tags",
        "tracing": "tracing",
        "type": "type",
    },
)
class CfnStateMachineMixinProps:
    def __init__(
        self,
        *,
        definition: typing.Any = None,
        definition_substitutions: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        definition_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStateMachinePropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStateMachinePropsMixin.EventSourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        logging: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStateMachinePropsMixin.LoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        permissions_boundaries: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStateMachinePropsMixin.IAMPolicyDocumentProperty", typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStateMachinePropsMixin.IAMPolicyDocumentProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnStateMachinePropsMixin.SAMPolicyTemplateProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        role: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tracing: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStateMachinePropsMixin.TracingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnStateMachinePropsMixin.

        :param definition: 
        :param definition_substitutions: 
        :param definition_uri: 
        :param events: 
        :param logging: 
        :param name: 
        :param permissions_boundaries: 
        :param policies: 
        :param role: 
        :param tags: 
        :param tracing: 
        :param type: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-statemachine.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
            
            # definition: Any
            
            cfn_state_machine_mixin_props = sam_mixins.CfnStateMachineMixinProps(
                definition=definition,
                definition_substitutions={
                    "definition_substitutions_key": "definitionSubstitutions"
                },
                definition_uri="definitionUri",
                events={
                    "events_key": sam_mixins.CfnStateMachinePropsMixin.EventSourceProperty(
                        properties=sam_mixins.CfnStateMachinePropsMixin.ApiEventProperty(
                            method="method",
                            path="path",
                            rest_api_id="restApiId"
                        ),
                        type="type"
                    )
                },
                logging=sam_mixins.CfnStateMachinePropsMixin.LoggingConfigurationProperty(
                    destinations=[sam_mixins.CfnStateMachinePropsMixin.LogDestinationProperty(
                        cloud_watch_logs_log_group=sam_mixins.CfnStateMachinePropsMixin.CloudWatchLogsLogGroupProperty(
                            log_group_arn="logGroupArn"
                        )
                    )],
                    include_execution_data=False,
                    level="level"
                ),
                name="name",
                permissions_boundaries="permissionsBoundaries",
                policies="policies",
                role="role",
                tags={
                    "tags_key": "tags"
                },
                tracing=sam_mixins.CfnStateMachinePropsMixin.TracingConfigurationProperty(
                    enabled=False
                ),
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__965771fdbc93800b169b26300483c8afb72640cb45f4bd92f21d88e961bca5b4)
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument definition_substitutions", value=definition_substitutions, expected_type=type_hints["definition_substitutions"])
            check_type(argname="argument definition_uri", value=definition_uri, expected_type=type_hints["definition_uri"])
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument permissions_boundaries", value=permissions_boundaries, expected_type=type_hints["permissions_boundaries"])
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tracing", value=tracing, expected_type=type_hints["tracing"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if definition is not None:
            self._values["definition"] = definition
        if definition_substitutions is not None:
            self._values["definition_substitutions"] = definition_substitutions
        if definition_uri is not None:
            self._values["definition_uri"] = definition_uri
        if events is not None:
            self._values["events"] = events
        if logging is not None:
            self._values["logging"] = logging
        if name is not None:
            self._values["name"] = name
        if permissions_boundaries is not None:
            self._values["permissions_boundaries"] = permissions_boundaries
        if policies is not None:
            self._values["policies"] = policies
        if role is not None:
            self._values["role"] = role
        if tags is not None:
            self._values["tags"] = tags
        if tracing is not None:
            self._values["tracing"] = tracing
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def definition(self) -> typing.Any:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-statemachine.html#cfn-serverless-statemachine-definition
        '''
        result = self._values.get("definition")
        return typing.cast(typing.Any, result)

    @builtins.property
    def definition_substitutions(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-statemachine.html#cfn-serverless-statemachine-definitionsubstitutions
        '''
        result = self._values.get("definition_substitutions")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def definition_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.S3LocationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-statemachine.html#cfn-serverless-statemachine-definitionuri
        '''
        result = self._values.get("definition_uri")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.S3LocationProperty"]], result)

    @builtins.property
    def events(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.EventSourceProperty"]]]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-statemachine.html#cfn-serverless-statemachine-events
        '''
        result = self._values.get("events")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.EventSourceProperty"]]]], result)

    @builtins.property
    def logging(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.LoggingConfigurationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-statemachine.html#cfn-serverless-statemachine-logging
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.LoggingConfigurationProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-statemachine.html#cfn-serverless-statemachine-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundaries(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-statemachine.html#cfn-serverless-statemachine-permissionsboundaries
        '''
        result = self._values.get("permissions_boundaries")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policies(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.IAMPolicyDocumentProperty", typing.List[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.IAMPolicyDocumentProperty", "CfnStateMachinePropsMixin.SAMPolicyTemplateProperty"]]]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-statemachine.html#cfn-serverless-statemachine-policies
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.IAMPolicyDocumentProperty", typing.List[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.IAMPolicyDocumentProperty", "CfnStateMachinePropsMixin.SAMPolicyTemplateProperty"]]]], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-statemachine.html#cfn-serverless-statemachine-role
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-statemachine.html#cfn-serverless-statemachine-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tracing(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.TracingConfigurationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-statemachine.html#cfn-serverless-statemachine-tracing
        '''
        result = self._values.get("tracing")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.TracingConfigurationProperty"]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-statemachine.html#cfn-serverless-statemachine-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStateMachineMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStateMachinePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnStateMachinePropsMixin",
):
    '''https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-serverless-statemachine.html
    :cloudformationResource: AWS::Serverless::StateMachine
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
        
        # definition: Any
        
        cfn_state_machine_props_mixin = sam_mixins.CfnStateMachinePropsMixin(sam_mixins.CfnStateMachineMixinProps(
            definition=definition,
            definition_substitutions={
                "definition_substitutions_key": "definitionSubstitutions"
            },
            definition_uri="definitionUri",
            events={
                "events_key": sam_mixins.CfnStateMachinePropsMixin.EventSourceProperty(
                    properties=sam_mixins.CfnStateMachinePropsMixin.ApiEventProperty(
                        method="method",
                        path="path",
                        rest_api_id="restApiId"
                    ),
                    type="type"
                )
            },
            logging=sam_mixins.CfnStateMachinePropsMixin.LoggingConfigurationProperty(
                destinations=[sam_mixins.CfnStateMachinePropsMixin.LogDestinationProperty(
                    cloud_watch_logs_log_group=sam_mixins.CfnStateMachinePropsMixin.CloudWatchLogsLogGroupProperty(
                        log_group_arn="logGroupArn"
                    )
                )],
                include_execution_data=False,
                level="level"
            ),
            name="name",
            permissions_boundaries="permissionsBoundaries",
            policies="policies",
            role="role",
            tags={
                "tags_key": "tags"
            },
            tracing=sam_mixins.CfnStateMachinePropsMixin.TracingConfigurationProperty(
                enabled=False
            ),
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnStateMachineMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Serverless::StateMachine``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02dcdb9426cb06aa4818b8a9481eea276c00fa9972940ac2f54c6f1f50eaa0df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d58d4876081e1ab1586ee575db22236de78b9d1838c5b5c95354cc00a8da290b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3440f0d321c1c701661e75d4d11c01dcddd668b01fadbb6b6ceef556ab8176f5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStateMachineMixinProps:
        return typing.cast(CfnStateMachineMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnStateMachinePropsMixin.ApiEventProperty",
        jsii_struct_bases=[],
        name_mapping={"method": "method", "path": "path", "rest_api_id": "restApiId"},
    )
    class ApiEventProperty:
        def __init__(
            self,
            *,
            method: typing.Optional[builtins.str] = None,
            path: typing.Optional[builtins.str] = None,
            rest_api_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param method: 
            :param path: 
            :param rest_api_id: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-apievent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                api_event_property = sam_mixins.CfnStateMachinePropsMixin.ApiEventProperty(
                    method="method",
                    path="path",
                    rest_api_id="restApiId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aba857f7500737bf6664ac056b3fb7c14e86c71b9e879fddf3929543fd5081e6)
                check_type(argname="argument method", value=method, expected_type=type_hints["method"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument rest_api_id", value=rest_api_id, expected_type=type_hints["rest_api_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if method is not None:
                self._values["method"] = method
            if path is not None:
                self._values["path"] = path
            if rest_api_id is not None:
                self._values["rest_api_id"] = rest_api_id

        @builtins.property
        def method(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-apievent.html#cfn-serverless-statemachine-apievent-method
            '''
            result = self._values.get("method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-apievent.html#cfn-serverless-statemachine-apievent-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rest_api_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-apievent.html#cfn-serverless-statemachine-apievent-restapiid
            '''
            result = self._values.get("rest_api_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApiEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnStateMachinePropsMixin.CloudWatchEventEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "event_bus_name": "eventBusName",
            "input": "input",
            "input_path": "inputPath",
            "pattern": "pattern",
        },
    )
    class CloudWatchEventEventProperty:
        def __init__(
            self,
            *,
            event_bus_name: typing.Optional[builtins.str] = None,
            input: typing.Optional[builtins.str] = None,
            input_path: typing.Optional[builtins.str] = None,
            pattern: typing.Any = None,
        ) -> None:
            '''
            :param event_bus_name: 
            :param input: 
            :param input_path: 
            :param pattern: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-cloudwatcheventevent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                # pattern: Any
                
                cloud_watch_event_event_property = sam_mixins.CfnStateMachinePropsMixin.CloudWatchEventEventProperty(
                    event_bus_name="eventBusName",
                    input="input",
                    input_path="inputPath",
                    pattern=pattern
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__69f2edb6d3b97c877d28a34f21d706ae7a0bd27d4367444e8eddda00cfcc6c14)
                check_type(argname="argument event_bus_name", value=event_bus_name, expected_type=type_hints["event_bus_name"])
                check_type(argname="argument input", value=input, expected_type=type_hints["input"])
                check_type(argname="argument input_path", value=input_path, expected_type=type_hints["input_path"])
                check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if event_bus_name is not None:
                self._values["event_bus_name"] = event_bus_name
            if input is not None:
                self._values["input"] = input
            if input_path is not None:
                self._values["input_path"] = input_path
            if pattern is not None:
                self._values["pattern"] = pattern

        @builtins.property
        def event_bus_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-cloudwatcheventevent.html#cfn-serverless-statemachine-cloudwatcheventevent-eventbusname
            '''
            result = self._values.get("event_bus_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-cloudwatcheventevent.html#cfn-serverless-statemachine-cloudwatcheventevent-input
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_path(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-cloudwatcheventevent.html#cfn-serverless-statemachine-cloudwatcheventevent-inputpath
            '''
            result = self._values.get("input_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pattern(self) -> typing.Any:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-cloudwatcheventevent.html#cfn-serverless-statemachine-cloudwatcheventevent-pattern
            '''
            result = self._values.get("pattern")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchEventEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnStateMachinePropsMixin.CloudWatchLogsLogGroupProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_arn": "logGroupArn"},
    )
    class CloudWatchLogsLogGroupProperty:
        def __init__(
            self,
            *,
            log_group_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param log_group_arn: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-cloudwatchlogsloggroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                cloud_watch_logs_log_group_property = sam_mixins.CfnStateMachinePropsMixin.CloudWatchLogsLogGroupProperty(
                    log_group_arn="logGroupArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cd67aaa92240897cf5a584fadac0c09604db806141d2c7ff4c6352aec5cb9898)
                check_type(argname="argument log_group_arn", value=log_group_arn, expected_type=type_hints["log_group_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_group_arn is not None:
                self._values["log_group_arn"] = log_group_arn

        @builtins.property
        def log_group_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-cloudwatchlogsloggroup.html#cfn-serverless-statemachine-cloudwatchlogsloggroup-loggrouparn
            '''
            result = self._values.get("log_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsLogGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnStateMachinePropsMixin.EventBridgeRuleEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "event_bus_name": "eventBusName",
            "input": "input",
            "input_path": "inputPath",
            "pattern": "pattern",
        },
    )
    class EventBridgeRuleEventProperty:
        def __init__(
            self,
            *,
            event_bus_name: typing.Optional[builtins.str] = None,
            input: typing.Optional[builtins.str] = None,
            input_path: typing.Optional[builtins.str] = None,
            pattern: typing.Any = None,
        ) -> None:
            '''
            :param event_bus_name: 
            :param input: 
            :param input_path: 
            :param pattern: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-eventbridgeruleevent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                # pattern: Any
                
                event_bridge_rule_event_property = sam_mixins.CfnStateMachinePropsMixin.EventBridgeRuleEventProperty(
                    event_bus_name="eventBusName",
                    input="input",
                    input_path="inputPath",
                    pattern=pattern
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__936e47e3eb31f16954cd2e162d5e303cb451fffe3265a3f1345ebc16f61098ea)
                check_type(argname="argument event_bus_name", value=event_bus_name, expected_type=type_hints["event_bus_name"])
                check_type(argname="argument input", value=input, expected_type=type_hints["input"])
                check_type(argname="argument input_path", value=input_path, expected_type=type_hints["input_path"])
                check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if event_bus_name is not None:
                self._values["event_bus_name"] = event_bus_name
            if input is not None:
                self._values["input"] = input
            if input_path is not None:
                self._values["input_path"] = input_path
            if pattern is not None:
                self._values["pattern"] = pattern

        @builtins.property
        def event_bus_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-eventbridgeruleevent.html#cfn-serverless-statemachine-eventbridgeruleevent-eventbusname
            '''
            result = self._values.get("event_bus_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-eventbridgeruleevent.html#cfn-serverless-statemachine-eventbridgeruleevent-input
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_path(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-eventbridgeruleevent.html#cfn-serverless-statemachine-eventbridgeruleevent-inputpath
            '''
            result = self._values.get("input_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pattern(self) -> typing.Any:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-eventbridgeruleevent.html#cfn-serverless-statemachine-eventbridgeruleevent-pattern
            '''
            result = self._values.get("pattern")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventBridgeRuleEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnStateMachinePropsMixin.EventSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"properties": "properties", "type": "type"},
    )
    class EventSourceProperty:
        def __init__(
            self,
            *,
            properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStateMachinePropsMixin.ApiEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnStateMachinePropsMixin.CloudWatchEventEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnStateMachinePropsMixin.EventBridgeRuleEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnStateMachinePropsMixin.ScheduleEventProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param properties: 
            :param type: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-eventsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                event_source_property = sam_mixins.CfnStateMachinePropsMixin.EventSourceProperty(
                    properties=sam_mixins.CfnStateMachinePropsMixin.ApiEventProperty(
                        method="method",
                        path="path",
                        rest_api_id="restApiId"
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d28471eedd233e5502f7a302d794e175998c99d6712c58481c5112e7405c9ef2)
                check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if properties is not None:
                self._values["properties"] = properties
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.ApiEventProperty", "CfnStateMachinePropsMixin.CloudWatchEventEventProperty", "CfnStateMachinePropsMixin.EventBridgeRuleEventProperty", "CfnStateMachinePropsMixin.ScheduleEventProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-eventsource.html#cfn-serverless-statemachine-eventsource-properties
            '''
            result = self._values.get("properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.ApiEventProperty", "CfnStateMachinePropsMixin.CloudWatchEventEventProperty", "CfnStateMachinePropsMixin.EventBridgeRuleEventProperty", "CfnStateMachinePropsMixin.ScheduleEventProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-eventsource.html#cfn-serverless-statemachine-eventsource-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnStateMachinePropsMixin.FunctionSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"function_name": "functionName"},
    )
    class FunctionSAMPTProperty:
        def __init__(
            self,
            *,
            function_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param function_name: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-functionsampt.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                function_sAMPTProperty = sam_mixins.CfnStateMachinePropsMixin.FunctionSAMPTProperty(
                    function_name="functionName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5d38cfd265aedde526d3218c530332e7347f40df7f60d2cc8bf5f3a933f4fdfc)
                check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if function_name is not None:
                self._values["function_name"] = function_name

        @builtins.property
        def function_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-functionsampt.html#cfn-serverless-statemachine-functionsampt-functionname
            '''
            result = self._values.get("function_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnStateMachinePropsMixin.IAMPolicyDocumentProperty",
        jsii_struct_bases=[],
        name_mapping={"statement": "statement", "version": "version"},
    )
    class IAMPolicyDocumentProperty:
        def __init__(
            self,
            *,
            statement: typing.Any = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param statement: 
            :param version: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-iampolicydocument.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                # statement: Any
                
                i_aMPolicy_document_property = {
                    "statement": statement,
                    "version": "version"
                }
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ede2c3a1430c3a6300f2e3a3223ad00800f52319c5174755302cab68bb8148e4)
                check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if statement is not None:
                self._values["statement"] = statement
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def statement(self) -> typing.Any:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-iampolicydocument.html#cfn-serverless-statemachine-iampolicydocument-statement
            '''
            result = self._values.get("statement")
            return typing.cast(typing.Any, result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-iampolicydocument.html#cfn-serverless-statemachine-iampolicydocument-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IAMPolicyDocumentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnStateMachinePropsMixin.LogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"cloud_watch_logs_log_group": "cloudWatchLogsLogGroup"},
    )
    class LogDestinationProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs_log_group: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStateMachinePropsMixin.CloudWatchLogsLogGroupProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param cloud_watch_logs_log_group: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-logdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                log_destination_property = sam_mixins.CfnStateMachinePropsMixin.LogDestinationProperty(
                    cloud_watch_logs_log_group=sam_mixins.CfnStateMachinePropsMixin.CloudWatchLogsLogGroupProperty(
                        log_group_arn="logGroupArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__27de390ed682480c2c31ca55ca97bd355a96150607b14bd93ecfb85cbcb1c436)
                check_type(argname="argument cloud_watch_logs_log_group", value=cloud_watch_logs_log_group, expected_type=type_hints["cloud_watch_logs_log_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logs_log_group is not None:
                self._values["cloud_watch_logs_log_group"] = cloud_watch_logs_log_group

        @builtins.property
        def cloud_watch_logs_log_group(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.CloudWatchLogsLogGroupProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-logdestination.html#cfn-serverless-statemachine-logdestination-cloudwatchlogsloggroup
            '''
            result = self._values.get("cloud_watch_logs_log_group")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.CloudWatchLogsLogGroupProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnStateMachinePropsMixin.LoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destinations": "destinations",
            "include_execution_data": "includeExecutionData",
            "level": "level",
        },
    )
    class LoggingConfigurationProperty:
        def __init__(
            self,
            *,
            destinations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStateMachinePropsMixin.LogDestinationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            include_execution_data: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            level: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param destinations: 
            :param include_execution_data: 
            :param level: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-loggingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                logging_configuration_property = sam_mixins.CfnStateMachinePropsMixin.LoggingConfigurationProperty(
                    destinations=[sam_mixins.CfnStateMachinePropsMixin.LogDestinationProperty(
                        cloud_watch_logs_log_group=sam_mixins.CfnStateMachinePropsMixin.CloudWatchLogsLogGroupProperty(
                            log_group_arn="logGroupArn"
                        )
                    )],
                    include_execution_data=False,
                    level="level"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__537694399fa6617cf5fef10c58dd8a7617a6c8933f481f008711045164b4a4a7)
                check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
                check_type(argname="argument include_execution_data", value=include_execution_data, expected_type=type_hints["include_execution_data"])
                check_type(argname="argument level", value=level, expected_type=type_hints["level"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destinations is not None:
                self._values["destinations"] = destinations
            if include_execution_data is not None:
                self._values["include_execution_data"] = include_execution_data
            if level is not None:
                self._values["level"] = level

        @builtins.property
        def destinations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.LogDestinationProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-loggingconfiguration.html#cfn-serverless-statemachine-loggingconfiguration-destinations
            '''
            result = self._values.get("destinations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.LogDestinationProperty"]]]], result)

        @builtins.property
        def include_execution_data(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-loggingconfiguration.html#cfn-serverless-statemachine-loggingconfiguration-includeexecutiondata
            '''
            result = self._values.get("include_execution_data")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def level(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-loggingconfiguration.html#cfn-serverless-statemachine-loggingconfiguration-level
            '''
            result = self._values.get("level")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnStateMachinePropsMixin.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key", "version": "version"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
            version: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param bucket: 
            :param key: 
            :param version: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                s3_location_property = sam_mixins.CfnStateMachinePropsMixin.S3LocationProperty(
                    bucket="bucket",
                    key="key",
                    version=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4531427cb0517284f3e494f21db9d370bdef95d86f20b8f71aef4051eb7a4fa5)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if key is not None:
                self._values["key"] = key
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-s3location.html#cfn-serverless-statemachine-s3location-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-s3location.html#cfn-serverless-statemachine-s3location-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-s3location.html#cfn-serverless-statemachine-s3location-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnStateMachinePropsMixin.SAMPolicyTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lambda_invoke_policy": "lambdaInvokePolicy",
            "step_functions_execution_policy": "stepFunctionsExecutionPolicy",
        },
    )
    class SAMPolicyTemplateProperty:
        def __init__(
            self,
            *,
            lambda_invoke_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStateMachinePropsMixin.FunctionSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            step_functions_execution_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStateMachinePropsMixin.StateMachineSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param lambda_invoke_policy: 
            :param step_functions_execution_policy: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-sampolicytemplate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                s_aMPolicy_template_property = sam_mixins.CfnStateMachinePropsMixin.SAMPolicyTemplateProperty(
                    lambda_invoke_policy=sam_mixins.CfnStateMachinePropsMixin.FunctionSAMPTProperty(
                        function_name="functionName"
                    ),
                    step_functions_execution_policy=sam_mixins.CfnStateMachinePropsMixin.StateMachineSAMPTProperty(
                        state_machine_name="stateMachineName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bc8f5136e8d5ecac60b049f80fb32eed1ab74fadf7fe4d3befaf9cd39eb585b8)
                check_type(argname="argument lambda_invoke_policy", value=lambda_invoke_policy, expected_type=type_hints["lambda_invoke_policy"])
                check_type(argname="argument step_functions_execution_policy", value=step_functions_execution_policy, expected_type=type_hints["step_functions_execution_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_invoke_policy is not None:
                self._values["lambda_invoke_policy"] = lambda_invoke_policy
            if step_functions_execution_policy is not None:
                self._values["step_functions_execution_policy"] = step_functions_execution_policy

        @builtins.property
        def lambda_invoke_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.FunctionSAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-sampolicytemplate.html#cfn-serverless-statemachine-sampolicytemplate-lambdainvokepolicy
            '''
            result = self._values.get("lambda_invoke_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.FunctionSAMPTProperty"]], result)

        @builtins.property
        def step_functions_execution_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.StateMachineSAMPTProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-sampolicytemplate.html#cfn-serverless-statemachine-sampolicytemplate-stepfunctionsexecutionpolicy
            '''
            result = self._values.get("step_functions_execution_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStateMachinePropsMixin.StateMachineSAMPTProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SAMPolicyTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnStateMachinePropsMixin.ScheduleEventProperty",
        jsii_struct_bases=[],
        name_mapping={"input": "input", "schedule": "schedule"},
    )
    class ScheduleEventProperty:
        def __init__(
            self,
            *,
            input: typing.Optional[builtins.str] = None,
            schedule: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param input: 
            :param schedule: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-scheduleevent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                schedule_event_property = sam_mixins.CfnStateMachinePropsMixin.ScheduleEventProperty(
                    input="input",
                    schedule="schedule"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__56625d0715f0c91fbda1a8db6b30f169b9958924f21644133db0c4a8cce63a10)
                check_type(argname="argument input", value=input, expected_type=type_hints["input"])
                check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if input is not None:
                self._values["input"] = input
            if schedule is not None:
                self._values["schedule"] = schedule

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-scheduleevent.html#cfn-serverless-statemachine-scheduleevent-input
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schedule(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-scheduleevent.html#cfn-serverless-statemachine-scheduleevent-schedule
            '''
            result = self._values.get("schedule")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnStateMachinePropsMixin.StateMachineSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"state_machine_name": "stateMachineName"},
    )
    class StateMachineSAMPTProperty:
        def __init__(
            self,
            *,
            state_machine_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param state_machine_name: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-statemachinesampt.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                state_machine_sAMPTProperty = sam_mixins.CfnStateMachinePropsMixin.StateMachineSAMPTProperty(
                    state_machine_name="stateMachineName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__641429a1d1e390a01cb74900f536da2444b1ee1068bb3ca90cc31a929aecd31f)
                check_type(argname="argument state_machine_name", value=state_machine_name, expected_type=type_hints["state_machine_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if state_machine_name is not None:
                self._values["state_machine_name"] = state_machine_name

        @builtins.property
        def state_machine_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-statemachinesampt.html#cfn-serverless-statemachine-statemachinesampt-statemachinename
            '''
            result = self._values.get("state_machine_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StateMachineSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sam.mixins.CfnStateMachinePropsMixin.TracingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class TracingConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''
            :param enabled: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-tracingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sam import mixins as sam_mixins
                
                tracing_configuration_property = sam_mixins.CfnStateMachinePropsMixin.TracingConfigurationProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b46bf197049ea24cd22b8eaf9a390ce407e8f8ecb5852e726387bfacc33608b9)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-serverless-statemachine-tracingconfiguration.html#cfn-serverless-statemachine-tracingconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TracingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnApiMixinProps",
    "CfnApiPropsMixin",
    "CfnApplicationMixinProps",
    "CfnApplicationPropsMixin",
    "CfnFunctionMixinProps",
    "CfnFunctionPropsMixin",
    "CfnHttpApiMixinProps",
    "CfnHttpApiPropsMixin",
    "CfnLayerVersionMixinProps",
    "CfnLayerVersionPropsMixin",
    "CfnSimpleTableMixinProps",
    "CfnSimpleTablePropsMixin",
    "CfnStateMachineMixinProps",
    "CfnStateMachinePropsMixin",
]

publication.publish()

def _typecheckingstub__84f933d0f19c07b09b10d6c9c90a04b351979e75f87a4f6be4d6490c2638f57e(
    *,
    access_log_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApiPropsMixin.AccessLogSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    always_deploy: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    auth: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApiPropsMixin.AuthProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    cache_cluster_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    cache_cluster_size: typing.Optional[builtins.str] = None,
    canary_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApiPropsMixin.CanarySettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cors: typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApiPropsMixin.CorsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    definition_body: typing.Any = None,
    definition_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApiPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    domain: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApiPropsMixin.DomainConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    endpoint_configuration: typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApiPropsMixin.EndpointConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    gateway_responses: typing.Any = None,
    method_settings: typing.Optional[typing.Union[typing.Sequence[typing.Any], _aws_cdk_ceddda9d.IResolvable]] = None,
    minimum_compression_size: typing.Optional[jsii.Number] = None,
    models: typing.Any = None,
    name: typing.Optional[builtins.str] = None,
    open_api_version: typing.Optional[builtins.str] = None,
    stage_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tracing_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    variables: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e510da3d6b99a6cfb6181c8cbfbd8d93db66f6244d227dd8899c840765451b7(
    props: typing.Union[CfnApiMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__137949329432f1ea8c946d546b477c4842e952b3c54f50c18597470b9f6f7ff4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed9f188125c2fecb6380952f1b56ba565e3609447cd99841c8db67627bed7daa(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4ef4413f02da8f13dfec2c9ce8599c6b01b649a0691eeb433b80251c7a99e09(
    *,
    destination_arn: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d9822383a83801361385ece9af804f620d188cbbaef719efe04548ccc84d68c(
    *,
    add_default_authorizer_to_cors_preflight: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    authorizers: typing.Any = None,
    default_authorizer: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906348e3f7ff2b29e868eeb3cfb6f2c9bd2e31b0428fc4ad42cab3643efa6b80(
    *,
    deployment_id: typing.Optional[builtins.str] = None,
    percent_traffic: typing.Optional[jsii.Number] = None,
    stage_variable_overrides: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    use_stage_cache: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19b322e2d0f531d71b2746ebd1563d4d7cfb3a238e82da21b6c539290fefcdc0(
    *,
    allow_credentials: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    allow_headers: typing.Optional[builtins.str] = None,
    allow_methods: typing.Optional[builtins.str] = None,
    allow_origin: typing.Optional[builtins.str] = None,
    max_age: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f4bb51c7fa19c90a855e99103828700bc2dd70063d85c648317c0d4527679f(
    *,
    base_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    certificate_arn: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    endpoint_configuration: typing.Optional[builtins.str] = None,
    mutual_tls_authentication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApiPropsMixin.MutualTlsAuthenticationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ownership_verification_certificate_arn: typing.Optional[builtins.str] = None,
    route53: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApiPropsMixin.Route53ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    security_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79b6f44c8399fdddc016632617b26893bd304aa10377bb52d9ed2c1b572a8e7b(
    *,
    type: typing.Optional[builtins.str] = None,
    vpc_endpoint_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba94ff8650566b2ec6b2b0821dab0782673dd94614d40937a821505134a6bd24(
    *,
    truststore_uri: typing.Optional[builtins.str] = None,
    truststore_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4e2720040a30d8a749bb767fa54506fa1f118ac3d79610dec298bdbbec5168f(
    *,
    distributed_domain_name: typing.Optional[builtins.str] = None,
    evaluate_target_health: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    hosted_zone_id: typing.Optional[builtins.str] = None,
    hosted_zone_name: typing.Optional[builtins.str] = None,
    ip_v6: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b06b56203b6bc7ebb45e0db6817618fec1b2bf57571e395158ebb4dcdb3c3ff(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__031630f98408daca16f032fa6fcd6d4121c52d5018ccff3a62850ca0564369be(
    *,
    location: typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ApplicationLocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeout_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3adbb999472478978c40f0b3e080dd8cdb7268d45178071d99cc42b5ec328f0d(
    props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__904b660f14ebb3f08d33f206b5d6dbb81f72186f68ca1051d312f1599fdcd1cb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f47b3f2016f5c0ec0f5b368ff36f3fc1acc9e241b680f21f6942082653e5c3f0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56bd3042739fbe8579d818a4846d22978f8bfdaa9b6b28ebca93cd63cb021159(
    *,
    application_id: typing.Optional[builtins.str] = None,
    semantic_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c9e2f4743f083f6d616dc861c7a877316d8b6330037fbdd98813faa1b0e60e(
    *,
    architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
    assume_role_policy_document: typing.Any = None,
    auto_publish_alias: typing.Optional[builtins.str] = None,
    auto_publish_code_sha256: typing.Optional[builtins.str] = None,
    code_signing_config_arn: typing.Optional[builtins.str] = None,
    code_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dead_letter_queue: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.DeadLetterQueueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    deployment_preference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.DeploymentPreferenceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.FunctionEnvironmentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ephemeral_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.EphemeralStorageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    event_invoke_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.EventInvokeConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.EventSourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    file_system_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.FileSystemConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    function_name: typing.Optional[builtins.str] = None,
    function_url_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.FunctionUrlConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    handler: typing.Optional[builtins.str] = None,
    image_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.ImageConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_uri: typing.Optional[builtins.str] = None,
    inline_code: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    layers: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    package_type: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunctionPropsMixin.SAMPolicyTemplateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    provisioned_concurrency_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.ProvisionedConcurrencyConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
    role: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    tracing: typing.Optional[builtins.str] = None,
    version_description: typing.Optional[builtins.str] = None,
    vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8a2393b278c08631e7b20ebc8c4b297b7b63a877d42cf039f2624f084f8c2df(
    props: typing.Union[CfnFunctionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f28a086dcf8465e78313f1de309faf508178e3f57daf9700bfc1fae0844c3134(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f94f1f847971e0cb78d98b6396ee3cd3797c4800e7535db49675a2766689a5c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fe595f271c198b097774166355d22fc09bef6e58c69bc4a582bb7d30ceec6d4(
    *,
    skill_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02a7332716c9cd5a819ddbe2c0945eea50ab4afb2a2f914ccbb224e71326cf44(
    *,
    auth: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.AuthProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    method: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    request_model: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.RequestModelProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    request_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.RequestParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    rest_api_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b278908bc5ebe1101993002907daba533991858c50a9d07d1b5f25cba0d01443(
    *,
    api_key_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    authorizer: typing.Optional[builtins.str] = None,
    resource_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.AuthResourcePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e32fe8678dbd799c8c772a1ce12dd5fc48b76619af26163aa1f76c1af48f3c7(
    *,
    aws_account_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
    aws_account_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    custom_statements: typing.Optional[typing.Union[typing.Sequence[typing.Any], _aws_cdk_ceddda9d.IResolvable]] = None,
    intrinsic_vpc_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
    intrinsic_vpce_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
    intrinsic_vpce_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    intrinsic_vpc_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_range_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_range_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_vpc_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_vpc_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d740b4a711b2c3eadfc302cb10fd3296bc09e62df5368a27500dcc85ecfc508e(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f991db682777c05a6de547dfa3019d52863882ae300803303f83dec974d333e(
    *,
    input: typing.Optional[builtins.str] = None,
    input_path: typing.Optional[builtins.str] = None,
    pattern: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ec2414ef539ee0a516f4383e5e08fb066eb33001b380df2c4c42b3a42cb1b3(
    *,
    filter_pattern: typing.Optional[builtins.str] = None,
    log_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cd23864d2ecb83fa496813bb8cf1a848e35a3b1797fe3a63def419dbc7bea6a(
    *,
    trigger: typing.Optional[builtins.str] = None,
    user_pool: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__605d76f64d392af02dc1728613e62574893d8e9113b0216b86f72abc37dda33e(
    *,
    collection_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24f62268b68a8590c24bc1c41d9c0e43df25c5dd8adb019dd5433eddc27bcd55(
    *,
    allow_credentials: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    allow_headers: typing.Optional[builtins.str] = None,
    allow_methods: typing.Optional[builtins.str] = None,
    allow_origin: typing.Optional[builtins.str] = None,
    max_age: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6370295d3d2bbf2fb560ec1ad24fe3b31c3662551dd92813fbbdfe133e6dd500(
    *,
    target_arn: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a30b4d18679f2ce7e9717501b40f08bbc8d89c6bc19749d5d771ceff8e61ff1b(
    *,
    alarms: typing.Optional[typing.Sequence[builtins.str]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    hooks: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.HooksProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0cf65bbcdd5b657615335c38d2178f46d4b65d4fd0dc12829c9d44b55414f2f(
    *,
    on_failure: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.DestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d4d23b6809eb544fa53b41f63b0645e6ee842de6f3f2f6f4cb50ff2f632223a(
    *,
    destination: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__256cc54477e28aea1d909cb738c1488c32b9e4eeebda64bb3f3fb9cb2ce76e41(
    *,
    domain_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc0b3c229bf8d6164cf260c405aef73047bcec889e2562299aca9899a734219(
    *,
    batch_size: typing.Optional[jsii.Number] = None,
    bisect_batch_on_function_error: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    destination_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.DestinationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
    starting_position: typing.Optional[builtins.str] = None,
    stream: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01548c74543eeb65af42af0f812ec0566bddb43c12678c9dd66cb8fbd36e8b82(
    *,
    size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb1a567ecaec32e8f4b97b7bdfda937fc1c0101a94d2041e237ea1044031a558(
    *,
    event_bus_name: typing.Optional[builtins.str] = None,
    input: typing.Optional[builtins.str] = None,
    input_path: typing.Optional[builtins.str] = None,
    pattern: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fae61446886df13c6f4b145b2e6901101cae06e608965dcc54bc8523d9b97b9(
    *,
    destination_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.EventInvokeDestinationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maximum_event_age_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bd9f60018412545d590b8c9cd20d100e414c78aa2b855f5acc4944e7c4f45d4(
    *,
    on_failure: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.DestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    on_success: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.DestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04fc21803b3051be5e22b2f976d4e404963fad6bd860e85090facd4c20ed6ada(
    *,
    properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.AlexaSkillEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunctionPropsMixin.ApiEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunctionPropsMixin.CloudWatchEventEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunctionPropsMixin.CloudWatchLogsEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunctionPropsMixin.CognitoEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunctionPropsMixin.DynamoDBEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunctionPropsMixin.EventBridgeRuleEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunctionPropsMixin.HttpApiEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunctionPropsMixin.IoTRuleEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunctionPropsMixin.KinesisEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunctionPropsMixin.S3EventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunctionPropsMixin.ScheduleEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunctionPropsMixin.SNSEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunctionPropsMixin.SQSEventProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51a5bf909ea3c7a6cabb446e65d88647b7a6b5884175931d61d22434b231eb96(
    *,
    arn: typing.Optional[builtins.str] = None,
    local_mount_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24041369edee7294e69e16ee14d657873910e47ab7eebeb087be6deb716c2e02(
    *,
    variables: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a41ff962ce8de3a0ae0bf06abaa76e20b965844cc51700865bcaf7c41a5556(
    *,
    function_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__475636cc40022021e567f74ec3011b9feb4e00b4df2dc2a562fbcf243bc479fa(
    *,
    auth_type: typing.Optional[builtins.str] = None,
    cors: typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.CorsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    invoke_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17e036b5208d1d39727b50db5eb205ed9df5b0996a4eae30f6a91f18fa7b851f(
    *,
    post_traffic: typing.Optional[builtins.str] = None,
    pre_traffic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__927e4bcdc0dcd710ec71883f1eb0a92e1d699ed4dfded22aa1b7195f41114881(
    *,
    api_id: typing.Optional[builtins.str] = None,
    auth: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.HttpApiFunctionAuthProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    method: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    payload_format_version: typing.Optional[builtins.str] = None,
    route_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.RouteSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout_in_millis: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e46877a8368a9ba4f0321c789177eec5593fa9b8393b3185770f51eccd52bca2(
    *,
    authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    authorizer: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__557b9b8c8599fbe0a2c10a7ff42e22e7e57d945ae15cdf7275654f3835003344(
    *,
    statement: typing.Any = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d6a656d8809f80eea980b34f47426785053497c4be34d5aefb7c93cab7a4b4d(
    *,
    identity_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__426cb1b7e56a91bdce02cb6ae25a5defb42bcfc8928ab870415a8eb6e0fdc07b(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    entry_point: typing.Optional[typing.Sequence[builtins.str]] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__847b4ec5c5773ffb8571b137351c929c866eefc53b360b34d4f0bc975b2931aa(
    *,
    aws_iot_sql_version: typing.Optional[builtins.str] = None,
    sql: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03d5d6307de5085ec53c171ae8467c87da921b10d0334378be8654f8313dec48(
    *,
    key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ae3fa48f978fbe68e1319545fb177c907c0dc3f514fafa7e6f2460badd2a2d(
    *,
    batch_size: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    function_response_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    starting_position: typing.Optional[builtins.str] = None,
    stream: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b6ee0a5acfc7f7cc3326eaddc6634c8d10759e71f9df57a9bbba855833b6ad5(
    *,
    log_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8cd4ec12e4d927c18ea5694d33402b0dc759654725db994647babd52a95bdb0(
    *,
    parameter_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d3fa3f6606aa63a236fd393e9ecdc0bfd9a5174f1a63023dfedc1a2eb62b9a(
    *,
    provisioned_concurrent_executions: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcb37d4627dcf475f97b0c424257ca8468c5eba931c4bba4b475fb73d027bded(
    *,
    queue_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8ae377b329a050cb5873b446146dc8fdb62489d908309cd5fdfadd372b94d2d(
    *,
    model: typing.Optional[builtins.str] = None,
    required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    validate_body: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    validate_parameters: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d31eebfb17b725351f5ef592bf6c4dd567a665ad310b10e88d7e4826a57ba7ba(
    *,
    caching: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__176e198930e56ca201f000fcf3185baa45fd3394a38a1b66c3f049ef8b5e7b31(
    *,
    data_trace_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    detailed_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    logging_level: typing.Optional[builtins.str] = None,
    throttling_burst_limit: typing.Optional[jsii.Number] = None,
    throttling_rate_limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14e620e9c2b678b4d19110760e038c4b2da69a0dfe2cd2bc4e7e35174dfbe7ee(
    *,
    bucket: typing.Optional[builtins.str] = None,
    events: typing.Optional[builtins.str] = None,
    filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.S3NotificationFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acd3dd5d8dfcefc55103fcee6c0199d563a6dba78fd3a68597a001335193fb23(
    *,
    rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.S3KeyFilterRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__853ba889a806b4601df319bf3debca96393794df343721a48b05fef96b06fc1e(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c387ab066f1790698d8323e6b2acf013a42c625ca0a71cb12f6e263fc4a953(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31f95f8163d83325e5a26337f05fbe9bb7fdeeee262213ab1772ac342afd6a6(
    *,
    s3_key: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.S3KeyFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eef65b7421add41593e34d743ae06d1fcd238f7ad879cebd0e9940a0ea571ea8(
    *,
    ami_describe_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.EmptySAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    aws_secrets_manager_get_secret_value_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.SecretArnSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cloud_formation_describe_stacks_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.EmptySAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cloud_watch_put_metric_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.EmptySAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dynamo_db_crud_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.TableSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dynamo_db_read_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.TableSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dynamo_db_stream_read_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.TableStreamSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dynamo_db_write_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.TableSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ec2_describe_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.EmptySAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    elasticsearch_http_post_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.DomainSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    filter_log_events_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.LogGroupSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kinesis_crud_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.StreamSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kinesis_stream_read_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.StreamSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kms_decrypt_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.KeySAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    lambda_invoke_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.FunctionSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rekognition_detect_only_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.EmptySAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rekognition_labels_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.EmptySAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rekognition_no_data_access_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.CollectionSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rekognition_read_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.CollectionSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rekognition_write_only_access_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.CollectionSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_crud_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.BucketSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_read_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.BucketSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_write_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.BucketSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ses_bulk_templated_crud_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.IdentitySAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ses_crud_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.IdentitySAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ses_email_template_crud_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.EmptySAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ses_send_bounce_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.IdentitySAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sns_crud_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.TopicSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sns_publish_message_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.TopicSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sqs_poller_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.QueueSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sqs_send_message_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.QueueSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ssm_parameter_read_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.ParameterNameSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    step_functions_execution_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.StateMachineSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_access_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.EmptySAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bba23a0d3b76110d193f1a9ee585e26081cd7bd81dbe4e34b328786ca57c506(
    *,
    topic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0abba944b461672636b2d68e7b60953184f2a67012f4a9f0b8437f7b6006aac2(
    *,
    batch_size: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    queue: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43e00e4242408b7aa31aa5148d1484d8828cd1e57b081f10eafe8b258d9959b(
    *,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    input: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7450b8cae5c1a69e248462035fa55b5c2c8d34c48ae0a7ae6d0f9d8fe19744c5(
    *,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__703c4cfb2ecdcb596fd8ba749139314dc12eed72ccccebb9c1e7ad68c3088ad7(
    *,
    state_machine_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d16ead8efff530b0659dbfc14ce855ddfcbd9c2fddf15b3498baa49ddd699e5(
    *,
    stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec4839878a7f641773b46b95bca262a3b0808b76d7c07b21d0a412fda9ad32f(
    *,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e6bb4c45eee1263c78036615fa3cce1b79d6ac2bc58c9b1272baa02882d7cc(
    *,
    stream_name: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24682dc3027e1c2fca6de8ff4333b7d89e5432e610ca13b336dd7187dccfb012(
    *,
    topic_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f468271f57ead7995ad7a5b46e55ba72928f7d5eb606cc939b2d01bb97b676(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b895fa0e13b2939c6c10c91b22b89be09dfbffe03d799dce049d830def349b3f(
    *,
    access_log_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnHttpApiPropsMixin.AccessLogSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    auth: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnHttpApiPropsMixin.HttpApiAuthProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cors_configuration: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable, typing.Union[CfnHttpApiPropsMixin.CorsConfigurationObjectProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_route_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnHttpApiPropsMixin.RouteSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    definition_body: typing.Any = None,
    definition_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union[CfnHttpApiPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    domain: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnHttpApiPropsMixin.HttpApiDomainConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    fail_on_warnings: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    route_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnHttpApiPropsMixin.RouteSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stage_name: typing.Optional[builtins.str] = None,
    stage_variables: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94c2f00880f0ddb403b03a96c40b73635c39f512a6dce25c4350b130fafc3186(
    props: typing.Union[CfnHttpApiMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbd131721f509fbb05eeee84daf3379bb77247e94a8d4ea25afbac0e39301ca2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da057acbc7e6cb09d9c613ffb594cc8ffdfb086b317c31ab9c7bbd2d9eae5ef5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a49847edc78aa09cc889a816cfc2969c0f5fdffb8ea48efd25083845b607509(
    *,
    destination_arn: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ef9b5ed0b9fabba748b3732e2143e7171f57822af49246e691a8e99d5d7874(
    *,
    allow_credentials: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    allow_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    allow_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    allow_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
    expose_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_age: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c473c92c3b412bb116159ff4abe6cb8ed0e99e0c6e5e555a0d59ad89bed65261(
    *,
    authorizers: typing.Any = None,
    default_authorizer: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f062cefa739962ebe6f5912152d4824f7d6bc8c37c51fdacc602a66900c8cf(
    *,
    base_path: typing.Optional[builtins.str] = None,
    certificate_arn: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    endpoint_configuration: typing.Optional[builtins.str] = None,
    mutual_tls_authentication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnHttpApiPropsMixin.MutualTlsAuthenticationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    route53: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnHttpApiPropsMixin.Route53ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    security_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3445c4e2c24c9eadcfe4520ff2742eaea390263d642159f47e154e36ba2eb1d(
    *,
    truststore_uri: typing.Optional[builtins.str] = None,
    truststore_version: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfb738f25fe7dc2772b9a2580c60cb09e457f92fdf8990adab10a64899e4b21c(
    *,
    distributed_domain_name: typing.Optional[builtins.str] = None,
    evaluate_target_health: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    hosted_zone_id: typing.Optional[builtins.str] = None,
    hosted_zone_name: typing.Optional[builtins.str] = None,
    ip_v6: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__313d8924773dc617d153f8a4d78d84ff04ddf2838ba35bb843a2c099978722d5(
    *,
    data_trace_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    detailed_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    logging_level: typing.Optional[builtins.str] = None,
    throttling_burst_limit: typing.Optional[jsii.Number] = None,
    throttling_rate_limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__059c561d8e199d76fa02e36fb00d58ab95d31dd54211b6a0ff80f6326ba3033e(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba973e6219551d992f3dd84a92df77b2968a0996d76f43ccf98a2c8313571b83(
    *,
    compatible_runtimes: typing.Optional[typing.Sequence[builtins.str]] = None,
    content_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLayerVersionPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    layer_name: typing.Optional[builtins.str] = None,
    license_info: typing.Optional[builtins.str] = None,
    retention_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfaa70e25631878c163308fdf24852bb09d97e131854c3f9abebcaaba159f2fb(
    props: typing.Union[CfnLayerVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40ce50742d3803970d714e8c9643db626044d01a93da3d06df4dd32d99526109(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69fc1f0d83008bcdcbdc4c579f9ba820b59dc847cb3392360643669606e78a3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9036f09f6f6b55116f974ad9307b2e1d52bcecb3b35f7e0fec54a932a668f33(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ff61d9ef23e27ae2ae0252ae24afc45c34d13038326b95cd7b40940d42efd2a(
    *,
    primary_key: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSimpleTablePropsMixin.PrimaryKeyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    provisioned_throughput: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSimpleTablePropsMixin.ProvisionedThroughputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sse_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSimpleTablePropsMixin.SSESpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7237cd946619faf8839de5c367d0b2ede1d4a4dc6449e12cf25c6502b3ed1d(
    props: typing.Union[CfnSimpleTableMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca514830aa0768b9a447000967dfa5078eb64c423a72adb0ec2cf3376f8ac261(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3f2e6290f8a84f7fa328ed291fc3ad1985a120c163a3f02560edfc645e7ed7b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89cd509acfaf49a3a870db2f1613e85290db15391015e4b3317f193b7b0967e4(
    *,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__670a56bc982e5588a27b3957efdbed409202d1c312919240918a508852cf73f0(
    *,
    read_capacity_units: typing.Optional[jsii.Number] = None,
    write_capacity_units: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b94eb66cf4d08ef47213890ac26f0ca226cbb2058ae4d389b129b792eb05436b(
    *,
    sse_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__965771fdbc93800b169b26300483c8afb72640cb45f4bd92f21d88e961bca5b4(
    *,
    definition: typing.Any = None,
    definition_substitutions: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    definition_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStateMachinePropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStateMachinePropsMixin.EventSourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    logging: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStateMachinePropsMixin.LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    permissions_boundaries: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStateMachinePropsMixin.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, _aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStateMachinePropsMixin.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnStateMachinePropsMixin.SAMPolicyTemplateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    role: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tracing: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStateMachinePropsMixin.TracingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02dcdb9426cb06aa4818b8a9481eea276c00fa9972940ac2f54c6f1f50eaa0df(
    props: typing.Union[CfnStateMachineMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58d4876081e1ab1586ee575db22236de78b9d1838c5b5c95354cc00a8da290b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3440f0d321c1c701661e75d4d11c01dcddd668b01fadbb6b6ceef556ab8176f5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba857f7500737bf6664ac056b3fb7c14e86c71b9e879fddf3929543fd5081e6(
    *,
    method: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    rest_api_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f2edb6d3b97c877d28a34f21d706ae7a0bd27d4367444e8eddda00cfcc6c14(
    *,
    event_bus_name: typing.Optional[builtins.str] = None,
    input: typing.Optional[builtins.str] = None,
    input_path: typing.Optional[builtins.str] = None,
    pattern: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd67aaa92240897cf5a584fadac0c09604db806141d2c7ff4c6352aec5cb9898(
    *,
    log_group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__936e47e3eb31f16954cd2e162d5e303cb451fffe3265a3f1345ebc16f61098ea(
    *,
    event_bus_name: typing.Optional[builtins.str] = None,
    input: typing.Optional[builtins.str] = None,
    input_path: typing.Optional[builtins.str] = None,
    pattern: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d28471eedd233e5502f7a302d794e175998c99d6712c58481c5112e7405c9ef2(
    *,
    properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStateMachinePropsMixin.ApiEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnStateMachinePropsMixin.CloudWatchEventEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnStateMachinePropsMixin.EventBridgeRuleEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnStateMachinePropsMixin.ScheduleEventProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d38cfd265aedde526d3218c530332e7347f40df7f60d2cc8bf5f3a933f4fdfc(
    *,
    function_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ede2c3a1430c3a6300f2e3a3223ad00800f52319c5174755302cab68bb8148e4(
    *,
    statement: typing.Any = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27de390ed682480c2c31ca55ca97bd355a96150607b14bd93ecfb85cbcb1c436(
    *,
    cloud_watch_logs_log_group: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStateMachinePropsMixin.CloudWatchLogsLogGroupProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__537694399fa6617cf5fef10c58dd8a7617a6c8933f481f008711045164b4a4a7(
    *,
    destinations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStateMachinePropsMixin.LogDestinationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    include_execution_data: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4531427cb0517284f3e494f21db9d370bdef95d86f20b8f71aef4051eb7a4fa5(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc8f5136e8d5ecac60b049f80fb32eed1ab74fadf7fe4d3befaf9cd39eb585b8(
    *,
    lambda_invoke_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStateMachinePropsMixin.FunctionSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    step_functions_execution_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStateMachinePropsMixin.StateMachineSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56625d0715f0c91fbda1a8db6b30f169b9958924f21644133db0c4a8cce63a10(
    *,
    input: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__641429a1d1e390a01cb74900f536da2444b1ee1068bb3ca90cc31a929aecd31f(
    *,
    state_machine_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b46bf197049ea24cd22b8eaf9a390ce407e8f8ecb5852e726387bfacc33608b9(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
