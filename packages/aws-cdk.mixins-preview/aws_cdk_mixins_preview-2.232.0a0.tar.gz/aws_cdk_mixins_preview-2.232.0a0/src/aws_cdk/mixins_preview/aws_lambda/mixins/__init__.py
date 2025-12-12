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
    jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnAliasMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "function_name": "functionName",
        "function_version": "functionVersion",
        "name": "name",
        "provisioned_concurrency_config": "provisionedConcurrencyConfig",
        "routing_config": "routingConfig",
    },
)
class CfnAliasMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        function_name: typing.Optional[builtins.str] = None,
        function_version: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        provisioned_concurrency_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAliasPropsMixin.ProvisionedConcurrencyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        routing_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAliasPropsMixin.AliasRoutingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAliasPropsMixin.

        :param description: A description of the alias.
        :param function_name: The name or ARN of the Lambda function. **Name formats** - *Function name* - ``MyFunction`` . - *Function ARN* - ``arn:aws:lambda:us-west-2:123456789012:function:MyFunction`` . - *Partial ARN* - ``123456789012:function:MyFunction`` . The length constraint applies only to the full ARN. If you specify only the function name, it is limited to 64 characters in length.
        :param function_version: The function version that the alias invokes.
        :param name: The name of the alias.
        :param provisioned_concurrency_config: Specifies a `provisioned concurrency <https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html>`_ configuration for a function's alias.
        :param routing_config: The `routing configuration <https://docs.aws.amazon.com/lambda/latest/dg/lambda-traffic-shifting-using-aliases.html>`_ of the alias.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-alias.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
            
            cfn_alias_mixin_props = lambda_mixins.CfnAliasMixinProps(
                description="description",
                function_name="functionName",
                function_version="functionVersion",
                name="name",
                provisioned_concurrency_config=lambda_mixins.CfnAliasPropsMixin.ProvisionedConcurrencyConfigurationProperty(
                    provisioned_concurrent_executions=123
                ),
                routing_config=lambda_mixins.CfnAliasPropsMixin.AliasRoutingConfigurationProperty(
                    additional_version_weights=[lambda_mixins.CfnAliasPropsMixin.VersionWeightProperty(
                        function_version="functionVersion",
                        function_weight=123
                    )]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08289c831cc94cd4f9e909f776b089700d48d82c01234ad5eba7e0ca7dd7f19c)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument function_version", value=function_version, expected_type=type_hints["function_version"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument provisioned_concurrency_config", value=provisioned_concurrency_config, expected_type=type_hints["provisioned_concurrency_config"])
            check_type(argname="argument routing_config", value=routing_config, expected_type=type_hints["routing_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if function_name is not None:
            self._values["function_name"] = function_name
        if function_version is not None:
            self._values["function_version"] = function_version
        if name is not None:
            self._values["name"] = name
        if provisioned_concurrency_config is not None:
            self._values["provisioned_concurrency_config"] = provisioned_concurrency_config
        if routing_config is not None:
            self._values["routing_config"] = routing_config

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the alias.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-alias.html#cfn-lambda-alias-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        '''The name or ARN of the Lambda function.

        **Name formats** - *Function name* - ``MyFunction`` .

        - *Function ARN* - ``arn:aws:lambda:us-west-2:123456789012:function:MyFunction`` .
        - *Partial ARN* - ``123456789012:function:MyFunction`` .

        The length constraint applies only to the full ARN. If you specify only the function name, it is limited to 64 characters in length.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-alias.html#cfn-lambda-alias-functionname
        '''
        result = self._values.get("function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def function_version(self) -> typing.Optional[builtins.str]:
        '''The function version that the alias invokes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-alias.html#cfn-lambda-alias-functionversion
        '''
        result = self._values.get("function_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the alias.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-alias.html#cfn-lambda-alias-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioned_concurrency_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAliasPropsMixin.ProvisionedConcurrencyConfigurationProperty"]]:
        '''Specifies a `provisioned concurrency <https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html>`_ configuration for a function's alias.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-alias.html#cfn-lambda-alias-provisionedconcurrencyconfig
        '''
        result = self._values.get("provisioned_concurrency_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAliasPropsMixin.ProvisionedConcurrencyConfigurationProperty"]], result)

    @builtins.property
    def routing_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAliasPropsMixin.AliasRoutingConfigurationProperty"]]:
        '''The `routing configuration <https://docs.aws.amazon.com/lambda/latest/dg/lambda-traffic-shifting-using-aliases.html>`_ of the alias.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-alias.html#cfn-lambda-alias-routingconfig
        '''
        result = self._values.get("routing_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAliasPropsMixin.AliasRoutingConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAliasMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAliasPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnAliasPropsMixin",
):
    '''The ``AWS::Lambda::Alias`` resource creates an `alias <https://docs.aws.amazon.com/lambda/latest/dg/configuration-aliases.html>`_ for a Lambda function version. Use aliases to provide clients with a function identifier that you can update to invoke a different version.

    You can also map an alias to split invocation requests between two versions. Use the ``RoutingConfig`` parameter to specify a second version and the percentage of invocation requests that it receives.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-alias.html
    :cloudformationResource: AWS::Lambda::Alias
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
        
        cfn_alias_props_mixin = lambda_mixins.CfnAliasPropsMixin(lambda_mixins.CfnAliasMixinProps(
            description="description",
            function_name="functionName",
            function_version="functionVersion",
            name="name",
            provisioned_concurrency_config=lambda_mixins.CfnAliasPropsMixin.ProvisionedConcurrencyConfigurationProperty(
                provisioned_concurrent_executions=123
            ),
            routing_config=lambda_mixins.CfnAliasPropsMixin.AliasRoutingConfigurationProperty(
                additional_version_weights=[lambda_mixins.CfnAliasPropsMixin.VersionWeightProperty(
                    function_version="functionVersion",
                    function_weight=123
                )]
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAliasMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lambda::Alias``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a54440f0c53832f71757a618d3f999a2968f01e81980177b7656dead70cc806b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6ff16e7cf48fa81820d553cd5441c88d951bab6839f51cdb9e8967cf034f603)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22de2b5069bd82b895be1d5b4dfc5523054f644c6834b49148758bc3a90e1970)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAliasMixinProps:
        return typing.cast(CfnAliasMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnAliasPropsMixin.AliasRoutingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"additional_version_weights": "additionalVersionWeights"},
    )
    class AliasRoutingConfigurationProperty:
        def __init__(
            self,
            *,
            additional_version_weights: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAliasPropsMixin.VersionWeightProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The `traffic-shifting <https://docs.aws.amazon.com/lambda/latest/dg/lambda-traffic-shifting-using-aliases.html>`_ configuration of a Lambda function alias.

            :param additional_version_weights: The second version, and the percentage of traffic that's routed to it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-alias-aliasroutingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                alias_routing_configuration_property = lambda_mixins.CfnAliasPropsMixin.AliasRoutingConfigurationProperty(
                    additional_version_weights=[lambda_mixins.CfnAliasPropsMixin.VersionWeightProperty(
                        function_version="functionVersion",
                        function_weight=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__466208344a63929a00d35184b5f541d8b6e8e90f0f680a30489d46657fa62d84)
                check_type(argname="argument additional_version_weights", value=additional_version_weights, expected_type=type_hints["additional_version_weights"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if additional_version_weights is not None:
                self._values["additional_version_weights"] = additional_version_weights

        @builtins.property
        def additional_version_weights(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAliasPropsMixin.VersionWeightProperty"]]]]:
            '''The second version, and the percentage of traffic that's routed to it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-alias-aliasroutingconfiguration.html#cfn-lambda-alias-aliasroutingconfiguration-additionalversionweights
            '''
            result = self._values.get("additional_version_weights")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAliasPropsMixin.VersionWeightProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AliasRoutingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnAliasPropsMixin.ProvisionedConcurrencyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "provisioned_concurrent_executions": "provisionedConcurrentExecutions",
        },
    )
    class ProvisionedConcurrencyConfigurationProperty:
        def __init__(
            self,
            *,
            provisioned_concurrent_executions: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A provisioned concurrency configuration for a function's alias.

            :param provisioned_concurrent_executions: The amount of provisioned concurrency to allocate for the alias.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-alias-provisionedconcurrencyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                provisioned_concurrency_configuration_property = lambda_mixins.CfnAliasPropsMixin.ProvisionedConcurrencyConfigurationProperty(
                    provisioned_concurrent_executions=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b0397bb9428f7d2d85a6d20c0f2e2df1db82a7ea675e6514fed4019b4cd5443a)
                check_type(argname="argument provisioned_concurrent_executions", value=provisioned_concurrent_executions, expected_type=type_hints["provisioned_concurrent_executions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if provisioned_concurrent_executions is not None:
                self._values["provisioned_concurrent_executions"] = provisioned_concurrent_executions

        @builtins.property
        def provisioned_concurrent_executions(self) -> typing.Optional[jsii.Number]:
            '''The amount of provisioned concurrency to allocate for the alias.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-alias-provisionedconcurrencyconfiguration.html#cfn-lambda-alias-provisionedconcurrencyconfiguration-provisionedconcurrentexecutions
            '''
            result = self._values.get("provisioned_concurrent_executions")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisionedConcurrencyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnAliasPropsMixin.VersionWeightProperty",
        jsii_struct_bases=[],
        name_mapping={
            "function_version": "functionVersion",
            "function_weight": "functionWeight",
        },
    )
    class VersionWeightProperty:
        def __init__(
            self,
            *,
            function_version: typing.Optional[builtins.str] = None,
            function_weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The `traffic-shifting <https://docs.aws.amazon.com/lambda/latest/dg/lambda-traffic-shifting-using-aliases.html>`_ configuration of a Lambda function alias.

            :param function_version: The qualifier of the second version.
            :param function_weight: The percentage of traffic that the alias routes to the second version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-alias-versionweight.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                version_weight_property = lambda_mixins.CfnAliasPropsMixin.VersionWeightProperty(
                    function_version="functionVersion",
                    function_weight=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5417cb45df34acafd624da5caa5c4620a0cbb1a3eeac749353a8d4b6a66ffda1)
                check_type(argname="argument function_version", value=function_version, expected_type=type_hints["function_version"])
                check_type(argname="argument function_weight", value=function_weight, expected_type=type_hints["function_weight"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if function_version is not None:
                self._values["function_version"] = function_version
            if function_weight is not None:
                self._values["function_weight"] = function_weight

        @builtins.property
        def function_version(self) -> typing.Optional[builtins.str]:
            '''The qualifier of the second version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-alias-versionweight.html#cfn-lambda-alias-versionweight-functionversion
            '''
            result = self._values.get("function_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def function_weight(self) -> typing.Optional[jsii.Number]:
            '''The percentage of traffic that the alias routes to the second version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-alias-versionweight.html#cfn-lambda-alias-versionweight-functionweight
            '''
            result = self._values.get("function_weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VersionWeightProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnCapacityProviderMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "capacity_provider_name": "capacityProviderName",
        "capacity_provider_scaling_config": "capacityProviderScalingConfig",
        "instance_requirements": "instanceRequirements",
        "kms_key_arn": "kmsKeyArn",
        "permissions_config": "permissionsConfig",
        "tags": "tags",
        "vpc_config": "vpcConfig",
    },
)
class CfnCapacityProviderMixinProps:
    def __init__(
        self,
        *,
        capacity_provider_name: typing.Optional[builtins.str] = None,
        capacity_provider_scaling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCapacityProviderPropsMixin.CapacityProviderScalingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_requirements: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCapacityProviderPropsMixin.InstanceRequirementsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        permissions_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCapacityProviderPropsMixin.CapacityProviderPermissionsConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCapacityProviderPropsMixin.CapacityProviderVpcConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnCapacityProviderPropsMixin.

        :param capacity_provider_name: The name of the capacity provider. The name must be unique within your AWS account and region. If you don't specify a name, CloudFormation generates one.
        :param capacity_provider_scaling_config: The scaling configuration for the capacity provider.
        :param instance_requirements: Specifications for the types of EC2 instances that the capacity provider can use.
        :param kms_key_arn: The ARN of the AWS Key Management Service (KMS) key used by the capacity provider.
        :param permissions_config: IAM permissions configuration for the capacity provider.
        :param tags: A list of tags to apply to the capacity provider.
        :param vpc_config: VPC configuration for the capacity provider.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-capacityprovider.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
            
            cfn_capacity_provider_mixin_props = lambda_mixins.CfnCapacityProviderMixinProps(
                capacity_provider_name="capacityProviderName",
                capacity_provider_scaling_config=lambda_mixins.CfnCapacityProviderPropsMixin.CapacityProviderScalingConfigProperty(
                    max_vCpu_count=123,
                    scaling_mode="scalingMode",
                    scaling_policies=[lambda_mixins.CfnCapacityProviderPropsMixin.TargetTrackingScalingPolicyProperty(
                        predefined_metric_type="predefinedMetricType",
                        target_value=123
                    )]
                ),
                instance_requirements=lambda_mixins.CfnCapacityProviderPropsMixin.InstanceRequirementsProperty(
                    allowed_instance_types=["allowedInstanceTypes"],
                    architectures=["architectures"],
                    excluded_instance_types=["excludedInstanceTypes"]
                ),
                kms_key_arn="kmsKeyArn",
                permissions_config=lambda_mixins.CfnCapacityProviderPropsMixin.CapacityProviderPermissionsConfigProperty(
                    capacity_provider_operator_role_arn="capacityProviderOperatorRoleArn"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_config=lambda_mixins.CfnCapacityProviderPropsMixin.CapacityProviderVpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0cf4c5f1b15ef6daf34810cec04480713c883ab720107d6e2d4fb674f5f4cb9)
            check_type(argname="argument capacity_provider_name", value=capacity_provider_name, expected_type=type_hints["capacity_provider_name"])
            check_type(argname="argument capacity_provider_scaling_config", value=capacity_provider_scaling_config, expected_type=type_hints["capacity_provider_scaling_config"])
            check_type(argname="argument instance_requirements", value=instance_requirements, expected_type=type_hints["instance_requirements"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument permissions_config", value=permissions_config, expected_type=type_hints["permissions_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if capacity_provider_name is not None:
            self._values["capacity_provider_name"] = capacity_provider_name
        if capacity_provider_scaling_config is not None:
            self._values["capacity_provider_scaling_config"] = capacity_provider_scaling_config
        if instance_requirements is not None:
            self._values["instance_requirements"] = instance_requirements
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if permissions_config is not None:
            self._values["permissions_config"] = permissions_config
        if tags is not None:
            self._values["tags"] = tags
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def capacity_provider_name(self) -> typing.Optional[builtins.str]:
        '''The name of the capacity provider.

        The name must be unique within your AWS account and region. If you don't specify a name, CloudFormation generates one.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-capacityprovider.html#cfn-lambda-capacityprovider-capacityprovidername
        '''
        result = self._values.get("capacity_provider_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def capacity_provider_scaling_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapacityProviderPropsMixin.CapacityProviderScalingConfigProperty"]]:
        '''The scaling configuration for the capacity provider.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-capacityprovider.html#cfn-lambda-capacityprovider-capacityproviderscalingconfig
        '''
        result = self._values.get("capacity_provider_scaling_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapacityProviderPropsMixin.CapacityProviderScalingConfigProperty"]], result)

    @builtins.property
    def instance_requirements(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapacityProviderPropsMixin.InstanceRequirementsProperty"]]:
        '''Specifications for the types of EC2 instances that the capacity provider can use.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-capacityprovider.html#cfn-lambda-capacityprovider-instancerequirements
        '''
        result = self._values.get("instance_requirements")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapacityProviderPropsMixin.InstanceRequirementsProperty"]], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the AWS Key Management Service (KMS) key used by the capacity provider.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-capacityprovider.html#cfn-lambda-capacityprovider-kmskeyarn
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapacityProviderPropsMixin.CapacityProviderPermissionsConfigProperty"]]:
        '''IAM permissions configuration for the capacity provider.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-capacityprovider.html#cfn-lambda-capacityprovider-permissionsconfig
        '''
        result = self._values.get("permissions_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapacityProviderPropsMixin.CapacityProviderPermissionsConfigProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags to apply to the capacity provider.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-capacityprovider.html#cfn-lambda-capacityprovider-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapacityProviderPropsMixin.CapacityProviderVpcConfigProperty"]]:
        '''VPC configuration for the capacity provider.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-capacityprovider.html#cfn-lambda-capacityprovider-vpcconfig
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapacityProviderPropsMixin.CapacityProviderVpcConfigProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCapacityProviderMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCapacityProviderPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnCapacityProviderPropsMixin",
):
    '''Resource Type definition for AWS::Lambda::CapacityProvider.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-capacityprovider.html
    :cloudformationResource: AWS::Lambda::CapacityProvider
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
        
        cfn_capacity_provider_props_mixin = lambda_mixins.CfnCapacityProviderPropsMixin(lambda_mixins.CfnCapacityProviderMixinProps(
            capacity_provider_name="capacityProviderName",
            capacity_provider_scaling_config=lambda_mixins.CfnCapacityProviderPropsMixin.CapacityProviderScalingConfigProperty(
                max_vCpu_count=123,
                scaling_mode="scalingMode",
                scaling_policies=[lambda_mixins.CfnCapacityProviderPropsMixin.TargetTrackingScalingPolicyProperty(
                    predefined_metric_type="predefinedMetricType",
                    target_value=123
                )]
            ),
            instance_requirements=lambda_mixins.CfnCapacityProviderPropsMixin.InstanceRequirementsProperty(
                allowed_instance_types=["allowedInstanceTypes"],
                architectures=["architectures"],
                excluded_instance_types=["excludedInstanceTypes"]
            ),
            kms_key_arn="kmsKeyArn",
            permissions_config=lambda_mixins.CfnCapacityProviderPropsMixin.CapacityProviderPermissionsConfigProperty(
                capacity_provider_operator_role_arn="capacityProviderOperatorRoleArn"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_config=lambda_mixins.CfnCapacityProviderPropsMixin.CapacityProviderVpcConfigProperty(
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"]
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCapacityProviderMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lambda::CapacityProvider``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b57773093eaa04517d6be2d86a204e798caea634d9dbafccaf95755bf0e696f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ddaccfb7ac1a6259a7f9d804fe6be20d7303c79b730e8432160925832c892ba)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0eb2d39813c111bb24aa9fcca013f7643aabdc94516c7463102cfaeb28045c2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCapacityProviderMixinProps:
        return typing.cast(CfnCapacityProviderMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnCapacityProviderPropsMixin.CapacityProviderPermissionsConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "capacity_provider_operator_role_arn": "capacityProviderOperatorRoleArn",
        },
    )
    class CapacityProviderPermissionsConfigProperty:
        def __init__(
            self,
            *,
            capacity_provider_operator_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''IAM permissions configuration for the capacity provider.

            :param capacity_provider_operator_role_arn: The ARN of the IAM role that Lambda assumes to manage the capacity provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-capacityprovider-capacityproviderpermissionsconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                capacity_provider_permissions_config_property = lambda_mixins.CfnCapacityProviderPropsMixin.CapacityProviderPermissionsConfigProperty(
                    capacity_provider_operator_role_arn="capacityProviderOperatorRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0f3c23fb87e4860897397259e7b88b4775d25aa18ee00b83b7b37f4d257d6879)
                check_type(argname="argument capacity_provider_operator_role_arn", value=capacity_provider_operator_role_arn, expected_type=type_hints["capacity_provider_operator_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if capacity_provider_operator_role_arn is not None:
                self._values["capacity_provider_operator_role_arn"] = capacity_provider_operator_role_arn

        @builtins.property
        def capacity_provider_operator_role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM role that Lambda assumes to manage the capacity provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-capacityprovider-capacityproviderpermissionsconfig.html#cfn-lambda-capacityprovider-capacityproviderpermissionsconfig-capacityprovideroperatorrolearn
            '''
            result = self._values.get("capacity_provider_operator_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityProviderPermissionsConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnCapacityProviderPropsMixin.CapacityProviderScalingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_v_cpu_count": "maxVCpuCount",
            "scaling_mode": "scalingMode",
            "scaling_policies": "scalingPolicies",
        },
    )
    class CapacityProviderScalingConfigProperty:
        def __init__(
            self,
            *,
            max_v_cpu_count: typing.Optional[jsii.Number] = None,
            scaling_mode: typing.Optional[builtins.str] = None,
            scaling_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCapacityProviderPropsMixin.TargetTrackingScalingPolicyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The scaling configuration for the capacity provider.

            :param max_v_cpu_count: The maximum number of EC2 instances that the capacity provider can scale up to.
            :param scaling_mode: The scaling mode for the capacity provider.
            :param scaling_policies: A list of target tracking scaling policies for the capacity provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-capacityprovider-capacityproviderscalingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                capacity_provider_scaling_config_property = lambda_mixins.CfnCapacityProviderPropsMixin.CapacityProviderScalingConfigProperty(
                    max_vCpu_count=123,
                    scaling_mode="scalingMode",
                    scaling_policies=[lambda_mixins.CfnCapacityProviderPropsMixin.TargetTrackingScalingPolicyProperty(
                        predefined_metric_type="predefinedMetricType",
                        target_value=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0b7f8a39b8a929aa1aa46f573d2c04d459dda523ee478d2fe9906965f5dea13f)
                check_type(argname="argument max_v_cpu_count", value=max_v_cpu_count, expected_type=type_hints["max_v_cpu_count"])
                check_type(argname="argument scaling_mode", value=scaling_mode, expected_type=type_hints["scaling_mode"])
                check_type(argname="argument scaling_policies", value=scaling_policies, expected_type=type_hints["scaling_policies"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_v_cpu_count is not None:
                self._values["max_v_cpu_count"] = max_v_cpu_count
            if scaling_mode is not None:
                self._values["scaling_mode"] = scaling_mode
            if scaling_policies is not None:
                self._values["scaling_policies"] = scaling_policies

        @builtins.property
        def max_v_cpu_count(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of EC2 instances that the capacity provider can scale up to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-capacityprovider-capacityproviderscalingconfig.html#cfn-lambda-capacityprovider-capacityproviderscalingconfig-maxvcpucount
            '''
            result = self._values.get("max_v_cpu_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def scaling_mode(self) -> typing.Optional[builtins.str]:
            '''The scaling mode for the capacity provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-capacityprovider-capacityproviderscalingconfig.html#cfn-lambda-capacityprovider-capacityproviderscalingconfig-scalingmode
            '''
            result = self._values.get("scaling_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scaling_policies(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapacityProviderPropsMixin.TargetTrackingScalingPolicyProperty"]]]]:
            '''A list of target tracking scaling policies for the capacity provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-capacityprovider-capacityproviderscalingconfig.html#cfn-lambda-capacityprovider-capacityproviderscalingconfig-scalingpolicies
            '''
            result = self._values.get("scaling_policies")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapacityProviderPropsMixin.TargetTrackingScalingPolicyProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityProviderScalingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnCapacityProviderPropsMixin.CapacityProviderVpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class CapacityProviderVpcConfigProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''VPC configuration for the capacity provider.

            :param security_group_ids: A list of security group IDs to associate with EC2 instances.
            :param subnet_ids: A list of subnet IDs where the capacity provider can launch EC2 instances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-capacityprovider-capacityprovidervpcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                capacity_provider_vpc_config_property = lambda_mixins.CfnCapacityProviderPropsMixin.CapacityProviderVpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__73476f5f83d5da533b4a96ceba7bf5a04d68cbefe28af58a70208012c459e437)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of security group IDs to associate with EC2 instances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-capacityprovider-capacityprovidervpcconfig.html#cfn-lambda-capacityprovider-capacityprovidervpcconfig-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of subnet IDs where the capacity provider can launch EC2 instances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-capacityprovider-capacityprovidervpcconfig.html#cfn-lambda-capacityprovider-capacityprovidervpcconfig-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityProviderVpcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnCapacityProviderPropsMixin.InstanceRequirementsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_instance_types": "allowedInstanceTypes",
            "architectures": "architectures",
            "excluded_instance_types": "excludedInstanceTypes",
        },
    )
    class InstanceRequirementsProperty:
        def __init__(
            self,
            *,
            allowed_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
            excluded_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifications for the types of EC2 instances that the capacity provider can use.

            :param allowed_instance_types: A list of instance types that the capacity provider can use. Supports wildcards (for example, m5.*).
            :param architectures: The instruction set architecture for EC2 instances. Specify either x86_64 or arm64.
            :param excluded_instance_types: A list of instance types that the capacity provider should not use. Takes precedence over AllowedInstanceTypes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-capacityprovider-instancerequirements.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                instance_requirements_property = lambda_mixins.CfnCapacityProviderPropsMixin.InstanceRequirementsProperty(
                    allowed_instance_types=["allowedInstanceTypes"],
                    architectures=["architectures"],
                    excluded_instance_types=["excludedInstanceTypes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b557b06e502b8b177d44b05c8ed91db2bb7cdbfe55c8d2757831f96e62685cd4)
                check_type(argname="argument allowed_instance_types", value=allowed_instance_types, expected_type=type_hints["allowed_instance_types"])
                check_type(argname="argument architectures", value=architectures, expected_type=type_hints["architectures"])
                check_type(argname="argument excluded_instance_types", value=excluded_instance_types, expected_type=type_hints["excluded_instance_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_instance_types is not None:
                self._values["allowed_instance_types"] = allowed_instance_types
            if architectures is not None:
                self._values["architectures"] = architectures
            if excluded_instance_types is not None:
                self._values["excluded_instance_types"] = excluded_instance_types

        @builtins.property
        def allowed_instance_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of instance types that the capacity provider can use.

            Supports wildcards (for example, m5.*).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-capacityprovider-instancerequirements.html#cfn-lambda-capacityprovider-instancerequirements-allowedinstancetypes
            '''
            result = self._values.get("allowed_instance_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def architectures(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The instruction set architecture for EC2 instances.

            Specify either x86_64 or arm64.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-capacityprovider-instancerequirements.html#cfn-lambda-capacityprovider-instancerequirements-architectures
            '''
            result = self._values.get("architectures")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def excluded_instance_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of instance types that the capacity provider should not use.

            Takes precedence over AllowedInstanceTypes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-capacityprovider-instancerequirements.html#cfn-lambda-capacityprovider-instancerequirements-excludedinstancetypes
            '''
            result = self._values.get("excluded_instance_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceRequirementsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnCapacityProviderPropsMixin.TargetTrackingScalingPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "predefined_metric_type": "predefinedMetricType",
            "target_value": "targetValue",
        },
    )
    class TargetTrackingScalingPolicyProperty:
        def __init__(
            self,
            *,
            predefined_metric_type: typing.Optional[builtins.str] = None,
            target_value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A target tracking scaling policy for the capacity provider.

            :param predefined_metric_type: The predefined metric for target tracking.
            :param target_value: The target value for the metric as a percentage (for example, 70.0 for 70%).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-capacityprovider-targettrackingscalingpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                target_tracking_scaling_policy_property = lambda_mixins.CfnCapacityProviderPropsMixin.TargetTrackingScalingPolicyProperty(
                    predefined_metric_type="predefinedMetricType",
                    target_value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c043bf47a78dc48e0769be8d6e8be42ef0d39e34475e34a902d0ab3142ada2be)
                check_type(argname="argument predefined_metric_type", value=predefined_metric_type, expected_type=type_hints["predefined_metric_type"])
                check_type(argname="argument target_value", value=target_value, expected_type=type_hints["target_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if predefined_metric_type is not None:
                self._values["predefined_metric_type"] = predefined_metric_type
            if target_value is not None:
                self._values["target_value"] = target_value

        @builtins.property
        def predefined_metric_type(self) -> typing.Optional[builtins.str]:
            '''The predefined metric for target tracking.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-capacityprovider-targettrackingscalingpolicy.html#cfn-lambda-capacityprovider-targettrackingscalingpolicy-predefinedmetrictype
            '''
            result = self._values.get("predefined_metric_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_value(self) -> typing.Optional[jsii.Number]:
            '''The target value for the metric as a percentage (for example, 70.0 for 70%).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-capacityprovider-targettrackingscalingpolicy.html#cfn-lambda-capacityprovider-targettrackingscalingpolicy-targetvalue
            '''
            result = self._values.get("target_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetTrackingScalingPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnCodeSigningConfigMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_publishers": "allowedPublishers",
        "code_signing_policies": "codeSigningPolicies",
        "description": "description",
        "tags": "tags",
    },
)
class CfnCodeSigningConfigMixinProps:
    def __init__(
        self,
        *,
        allowed_publishers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCodeSigningConfigPropsMixin.AllowedPublishersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        code_signing_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCodeSigningConfigPropsMixin.CodeSigningPoliciesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnCodeSigningConfigPropsMixin.

        :param allowed_publishers: List of allowed publishers.
        :param code_signing_policies: The code signing policy controls the validation failure action for signature mismatch or expiry.
        :param description: Code signing configuration description.
        :param tags: A list of tags to add to the code signing configuration. .. epigraph:: You must have the ``lambda:TagResource`` , ``lambda:UntagResource`` , and ``lambda:ListTags`` permissions for your `IAM principal <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html>`_ to manage the CloudFormation stack. If you don't have these permissions, there might be unexpected behavior with stack-level tags propagating to the resource during resource creation and update.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-codesigningconfig.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
            
            cfn_code_signing_config_mixin_props = lambda_mixins.CfnCodeSigningConfigMixinProps(
                allowed_publishers=lambda_mixins.CfnCodeSigningConfigPropsMixin.AllowedPublishersProperty(
                    signing_profile_version_arns=["signingProfileVersionArns"]
                ),
                code_signing_policies=lambda_mixins.CfnCodeSigningConfigPropsMixin.CodeSigningPoliciesProperty(
                    untrusted_artifact_on_deployment="untrustedArtifactOnDeployment"
                ),
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ebb82706cbc7d48ddb8df5ae08f3c1600288f23efea22ed2abe3d7d7b104485)
            check_type(argname="argument allowed_publishers", value=allowed_publishers, expected_type=type_hints["allowed_publishers"])
            check_type(argname="argument code_signing_policies", value=code_signing_policies, expected_type=type_hints["code_signing_policies"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_publishers is not None:
            self._values["allowed_publishers"] = allowed_publishers
        if code_signing_policies is not None:
            self._values["code_signing_policies"] = code_signing_policies
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def allowed_publishers(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeSigningConfigPropsMixin.AllowedPublishersProperty"]]:
        '''List of allowed publishers.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-codesigningconfig.html#cfn-lambda-codesigningconfig-allowedpublishers
        '''
        result = self._values.get("allowed_publishers")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeSigningConfigPropsMixin.AllowedPublishersProperty"]], result)

    @builtins.property
    def code_signing_policies(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeSigningConfigPropsMixin.CodeSigningPoliciesProperty"]]:
        '''The code signing policy controls the validation failure action for signature mismatch or expiry.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-codesigningconfig.html#cfn-lambda-codesigningconfig-codesigningpolicies
        '''
        result = self._values.get("code_signing_policies")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeSigningConfigPropsMixin.CodeSigningPoliciesProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Code signing configuration description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-codesigningconfig.html#cfn-lambda-codesigningconfig-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags to add to the code signing configuration.

        .. epigraph::

           You must have the ``lambda:TagResource`` , ``lambda:UntagResource`` , and ``lambda:ListTags`` permissions for your `IAM principal <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html>`_ to manage the CloudFormation stack. If you don't have these permissions, there might be unexpected behavior with stack-level tags propagating to the resource during resource creation and update.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-codesigningconfig.html#cfn-lambda-codesigningconfig-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCodeSigningConfigMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCodeSigningConfigPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnCodeSigningConfigPropsMixin",
):
    '''Details about a `Code signing configuration <https://docs.aws.amazon.com/lambda/latest/dg/configuration-codesigning.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-codesigningconfig.html
    :cloudformationResource: AWS::Lambda::CodeSigningConfig
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
        
        cfn_code_signing_config_props_mixin = lambda_mixins.CfnCodeSigningConfigPropsMixin(lambda_mixins.CfnCodeSigningConfigMixinProps(
            allowed_publishers=lambda_mixins.CfnCodeSigningConfigPropsMixin.AllowedPublishersProperty(
                signing_profile_version_arns=["signingProfileVersionArns"]
            ),
            code_signing_policies=lambda_mixins.CfnCodeSigningConfigPropsMixin.CodeSigningPoliciesProperty(
                untrusted_artifact_on_deployment="untrustedArtifactOnDeployment"
            ),
            description="description",
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
        props: typing.Union[CfnCodeSigningConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lambda::CodeSigningConfig``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99d8028b502c61f06980e8317e4860fc415411379a58d6477ad25752871d2526)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbdcf3f8ebeeced197040326770db2e4ef041701421eb78101e254e2b5d99a7d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ca778445bfc62a0f0a74c04d9d5d502cba921fdc25d4a08dfc48a2c4362c6b1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCodeSigningConfigMixinProps:
        return typing.cast(CfnCodeSigningConfigMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnCodeSigningConfigPropsMixin.AllowedPublishersProperty",
        jsii_struct_bases=[],
        name_mapping={"signing_profile_version_arns": "signingProfileVersionArns"},
    )
    class AllowedPublishersProperty:
        def __init__(
            self,
            *,
            signing_profile_version_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''List of signing profiles that can sign a code package.

            :param signing_profile_version_arns: The Amazon Resource Name (ARN) for each of the signing profiles. A signing profile defines a trusted user who can sign a code package.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-codesigningconfig-allowedpublishers.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                allowed_publishers_property = lambda_mixins.CfnCodeSigningConfigPropsMixin.AllowedPublishersProperty(
                    signing_profile_version_arns=["signingProfileVersionArns"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f16c6a033619b2b180de74937420bdb1c2ae6be04d056972dc2f657c82786785)
                check_type(argname="argument signing_profile_version_arns", value=signing_profile_version_arns, expected_type=type_hints["signing_profile_version_arns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if signing_profile_version_arns is not None:
                self._values["signing_profile_version_arns"] = signing_profile_version_arns

        @builtins.property
        def signing_profile_version_arns(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The Amazon Resource Name (ARN) for each of the signing profiles.

            A signing profile defines a trusted user who can sign a code package.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-codesigningconfig-allowedpublishers.html#cfn-lambda-codesigningconfig-allowedpublishers-signingprofileversionarns
            '''
            result = self._values.get("signing_profile_version_arns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AllowedPublishersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnCodeSigningConfigPropsMixin.CodeSigningPoliciesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "untrusted_artifact_on_deployment": "untrustedArtifactOnDeployment",
        },
    )
    class CodeSigningPoliciesProperty:
        def __init__(
            self,
            *,
            untrusted_artifact_on_deployment: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Code signing configuration `policies <https://docs.aws.amazon.com/lambda/latest/dg/configuration-codesigning.html#config-codesigning-policies>`_ specify the validation failure action for signature mismatch or expiry.

            :param untrusted_artifact_on_deployment: Code signing configuration policy for deployment validation failure. If you set the policy to ``Enforce`` , Lambda blocks the deployment request if signature validation checks fail. If you set the policy to ``Warn`` , Lambda allows the deployment and issues a new Amazon CloudWatch metric ( ``SignatureValidationErrors`` ) and also stores the warning in the CloudTrail log. Default value: ``Warn`` Default: - "Warn"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-codesigningconfig-codesigningpolicies.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                code_signing_policies_property = lambda_mixins.CfnCodeSigningConfigPropsMixin.CodeSigningPoliciesProperty(
                    untrusted_artifact_on_deployment="untrustedArtifactOnDeployment"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cbb72c2dd898878bdf2ed22238154b8bf1619aaf205c4330a54f7dff11ebe37a)
                check_type(argname="argument untrusted_artifact_on_deployment", value=untrusted_artifact_on_deployment, expected_type=type_hints["untrusted_artifact_on_deployment"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if untrusted_artifact_on_deployment is not None:
                self._values["untrusted_artifact_on_deployment"] = untrusted_artifact_on_deployment

        @builtins.property
        def untrusted_artifact_on_deployment(self) -> typing.Optional[builtins.str]:
            '''Code signing configuration policy for deployment validation failure.

            If you set the policy to ``Enforce`` , Lambda blocks the deployment request if signature validation checks fail. If you set the policy to ``Warn`` , Lambda allows the deployment and issues a new Amazon CloudWatch metric ( ``SignatureValidationErrors`` ) and also stores the warning in the CloudTrail log.

            Default value: ``Warn``

            :default: - "Warn"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-codesigningconfig-codesigningpolicies.html#cfn-lambda-codesigningconfig-codesigningpolicies-untrustedartifactondeployment
            '''
            result = self._values.get("untrusted_artifact_on_deployment")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeSigningPoliciesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnEventInvokeConfigMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination_config": "destinationConfig",
        "function_name": "functionName",
        "maximum_event_age_in_seconds": "maximumEventAgeInSeconds",
        "maximum_retry_attempts": "maximumRetryAttempts",
        "qualifier": "qualifier",
    },
)
class CfnEventInvokeConfigMixinProps:
    def __init__(
        self,
        *,
        destination_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventInvokeConfigPropsMixin.DestinationConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        function_name: typing.Optional[builtins.str] = None,
        maximum_event_age_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        qualifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnEventInvokeConfigPropsMixin.

        :param destination_config: A destination for events after they have been sent to a function for processing. **Destinations** - *Function* - The Amazon Resource Name (ARN) of a Lambda function. - *Queue* - The ARN of a standard SQS queue. - *Bucket* - The ARN of an Amazon S3 bucket. - *Topic* - The ARN of a standard SNS topic. - *Event Bus* - The ARN of an Amazon EventBridge event bus. .. epigraph:: S3 buckets are supported only for on-failure destinations. To retain records of successful invocations, use another destination type.
        :param function_name: The name of the Lambda function. *Minimum* : ``1`` *Maximum* : ``64`` *Pattern* : ``([a-zA-Z0-9-_]+)``
        :param maximum_event_age_in_seconds: The maximum age of a request that Lambda sends to a function for processing.
        :param maximum_retry_attempts: The maximum number of times to retry when the function returns an error.
        :param qualifier: The identifier of a version or alias. - *Version* - A version number. - *Alias* - An alias name. - *Latest* - To specify the unpublished version, use ``$LATEST`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventinvokeconfig.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
            
            cfn_event_invoke_config_mixin_props = lambda_mixins.CfnEventInvokeConfigMixinProps(
                destination_config=lambda_mixins.CfnEventInvokeConfigPropsMixin.DestinationConfigProperty(
                    on_failure=lambda_mixins.CfnEventInvokeConfigPropsMixin.OnFailureProperty(
                        destination="destination"
                    ),
                    on_success=lambda_mixins.CfnEventInvokeConfigPropsMixin.OnSuccessProperty(
                        destination="destination"
                    )
                ),
                function_name="functionName",
                maximum_event_age_in_seconds=123,
                maximum_retry_attempts=123,
                qualifier="qualifier"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4a4676ea89f7d1115c3b9d96b9c9a1ba1879bc9128bfbcaff30200be66f3cff)
            check_type(argname="argument destination_config", value=destination_config, expected_type=type_hints["destination_config"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument maximum_event_age_in_seconds", value=maximum_event_age_in_seconds, expected_type=type_hints["maximum_event_age_in_seconds"])
            check_type(argname="argument maximum_retry_attempts", value=maximum_retry_attempts, expected_type=type_hints["maximum_retry_attempts"])
            check_type(argname="argument qualifier", value=qualifier, expected_type=type_hints["qualifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination_config is not None:
            self._values["destination_config"] = destination_config
        if function_name is not None:
            self._values["function_name"] = function_name
        if maximum_event_age_in_seconds is not None:
            self._values["maximum_event_age_in_seconds"] = maximum_event_age_in_seconds
        if maximum_retry_attempts is not None:
            self._values["maximum_retry_attempts"] = maximum_retry_attempts
        if qualifier is not None:
            self._values["qualifier"] = qualifier

    @builtins.property
    def destination_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventInvokeConfigPropsMixin.DestinationConfigProperty"]]:
        '''A destination for events after they have been sent to a function for processing.

        **Destinations** - *Function* - The Amazon Resource Name (ARN) of a Lambda function.

        - *Queue* - The ARN of a standard SQS queue.
        - *Bucket* - The ARN of an Amazon S3 bucket.
        - *Topic* - The ARN of a standard SNS topic.
        - *Event Bus* - The ARN of an Amazon EventBridge event bus.

        .. epigraph::

           S3 buckets are supported only for on-failure destinations. To retain records of successful invocations, use another destination type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventinvokeconfig.html#cfn-lambda-eventinvokeconfig-destinationconfig
        '''
        result = self._values.get("destination_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventInvokeConfigPropsMixin.DestinationConfigProperty"]], result)

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Lambda function.

        *Minimum* : ``1``

        *Maximum* : ``64``

        *Pattern* : ``([a-zA-Z0-9-_]+)``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventinvokeconfig.html#cfn-lambda-eventinvokeconfig-functionname
        '''
        result = self._values.get("function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maximum_event_age_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''The maximum age of a request that Lambda sends to a function for processing.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventinvokeconfig.html#cfn-lambda-eventinvokeconfig-maximumeventageinseconds
        '''
        result = self._values.get("maximum_event_age_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of times to retry when the function returns an error.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventinvokeconfig.html#cfn-lambda-eventinvokeconfig-maximumretryattempts
        '''
        result = self._values.get("maximum_retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def qualifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of a version or alias.

        - *Version* - A version number.
        - *Alias* - An alias name.
        - *Latest* - To specify the unpublished version, use ``$LATEST`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventinvokeconfig.html#cfn-lambda-eventinvokeconfig-qualifier
        '''
        result = self._values.get("qualifier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEventInvokeConfigMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEventInvokeConfigPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnEventInvokeConfigPropsMixin",
):
    '''The ``AWS::Lambda::EventInvokeConfig`` resource configures options for `asynchronous invocation <https://docs.aws.amazon.com/lambda/latest/dg/invocation-async.html>`_ on a version or an alias.

    By default, Lambda retries an asynchronous invocation twice if the function returns an error. It retains events in a queue for up to six hours. When an event fails all processing attempts or stays in the asynchronous invocation queue for too long, Lambda discards it.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventinvokeconfig.html
    :cloudformationResource: AWS::Lambda::EventInvokeConfig
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
        
        cfn_event_invoke_config_props_mixin = lambda_mixins.CfnEventInvokeConfigPropsMixin(lambda_mixins.CfnEventInvokeConfigMixinProps(
            destination_config=lambda_mixins.CfnEventInvokeConfigPropsMixin.DestinationConfigProperty(
                on_failure=lambda_mixins.CfnEventInvokeConfigPropsMixin.OnFailureProperty(
                    destination="destination"
                ),
                on_success=lambda_mixins.CfnEventInvokeConfigPropsMixin.OnSuccessProperty(
                    destination="destination"
                )
            ),
            function_name="functionName",
            maximum_event_age_in_seconds=123,
            maximum_retry_attempts=123,
            qualifier="qualifier"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEventInvokeConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lambda::EventInvokeConfig``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a318025e7c3b15462fa20792985d52c705641c1f96b84105de95a42264227f02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__124874c0567e8f5c47530a30115017f9f55391edcda17cbde357fec6116058e0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd74f9bd377d333d24804e5c60c431a91c387211a3051496b3afb0a1353b515e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEventInvokeConfigMixinProps:
        return typing.cast(CfnEventInvokeConfigMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnEventInvokeConfigPropsMixin.DestinationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"on_failure": "onFailure", "on_success": "onSuccess"},
    )
    class DestinationConfigProperty:
        def __init__(
            self,
            *,
            on_failure: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventInvokeConfigPropsMixin.OnFailureProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            on_success: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventInvokeConfigPropsMixin.OnSuccessProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A configuration object that specifies the destination of an event after Lambda processes it.

            For more information, see `Adding a destination <https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-retain-records.html#invocation-async-destinations>`_ .

            :param on_failure: The destination configuration for failed invocations. .. epigraph:: When using an Amazon SQS queue as a destination, FIFO queues cannot be used.
            :param on_success: The destination configuration for successful invocations. .. epigraph:: When using an Amazon SQS queue as a destination, FIFO queues cannot be used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventinvokeconfig-destinationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                destination_config_property = lambda_mixins.CfnEventInvokeConfigPropsMixin.DestinationConfigProperty(
                    on_failure=lambda_mixins.CfnEventInvokeConfigPropsMixin.OnFailureProperty(
                        destination="destination"
                    ),
                    on_success=lambda_mixins.CfnEventInvokeConfigPropsMixin.OnSuccessProperty(
                        destination="destination"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0c2772492abadfb939ed6612df29bdf04b0592598d1fa88896b61e87b5a7fca1)
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
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventInvokeConfigPropsMixin.OnFailureProperty"]]:
            '''The destination configuration for failed invocations.

            .. epigraph::

               When using an Amazon SQS queue as a destination, FIFO queues cannot be used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventinvokeconfig-destinationconfig.html#cfn-lambda-eventinvokeconfig-destinationconfig-onfailure
            '''
            result = self._values.get("on_failure")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventInvokeConfigPropsMixin.OnFailureProperty"]], result)

        @builtins.property
        def on_success(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventInvokeConfigPropsMixin.OnSuccessProperty"]]:
            '''The destination configuration for successful invocations.

            .. epigraph::

               When using an Amazon SQS queue as a destination, FIFO queues cannot be used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventinvokeconfig-destinationconfig.html#cfn-lambda-eventinvokeconfig-destinationconfig-onsuccess
            '''
            result = self._values.get("on_success")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventInvokeConfigPropsMixin.OnSuccessProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnEventInvokeConfigPropsMixin.OnFailureProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination"},
    )
    class OnFailureProperty:
        def __init__(
            self,
            *,
            destination: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A destination for events that failed processing.

            For more information, see `Adding a destination <https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-retain-records.html#invocation-async-destinations>`_ .

            :param destination: The Amazon Resource Name (ARN) of the destination resource. To retain records of failed invocations from `Kinesis <https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html>`_ , `DynamoDB <https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html>`_ , `self-managed Apache Kafka <https://docs.aws.amazon.com/lambda/latest/dg/kafka-on-failure.html>`_ , or `Amazon MSK <https://docs.aws.amazon.com/lambda/latest/dg/kafka-on-failure.html>`_ , you can configure an Amazon SNS topic, Amazon SQS queue, Amazon S3 bucket, or Kafka topic as the destination. .. epigraph:: Amazon SNS destinations have a message size limit of 256 KB. If the combined size of the function request and response payload exceeds the limit, Lambda will drop the payload when sending ``OnFailure`` event to the destination. For details on this behavior, refer to `Retaining records of asynchronous invocations <https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-retain-records.html>`_ . To retain records of failed invocations from `Kinesis <https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html>`_ , `DynamoDB <https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html>`_ , `self-managed Kafka <https://docs.aws.amazon.com/lambda/latest/dg/with-kafka.html#services-smaa-onfailure-destination>`_ or `Amazon MSK <https://docs.aws.amazon.com/lambda/latest/dg/with-msk.html#services-msk-onfailure-destination>`_ , you can configure an Amazon SNS topic, Amazon SQS queue, or Amazon S3 bucket as the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventinvokeconfig-onfailure.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                on_failure_property = lambda_mixins.CfnEventInvokeConfigPropsMixin.OnFailureProperty(
                    destination="destination"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2cd418fa3a6731285f539fbf0f7da211347b466350b4f228bec33ccf5a8021a4)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination is not None:
                self._values["destination"] = destination

        @builtins.property
        def destination(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the destination resource.

            To retain records of failed invocations from `Kinesis <https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html>`_ , `DynamoDB <https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html>`_ , `self-managed Apache Kafka <https://docs.aws.amazon.com/lambda/latest/dg/kafka-on-failure.html>`_ , or `Amazon MSK <https://docs.aws.amazon.com/lambda/latest/dg/kafka-on-failure.html>`_ , you can configure an Amazon SNS topic, Amazon SQS queue, Amazon S3 bucket, or Kafka topic as the destination.
            .. epigraph::

               Amazon SNS destinations have a message size limit of 256 KB. If the combined size of the function request and response payload exceeds the limit, Lambda will drop the payload when sending ``OnFailure`` event to the destination. For details on this behavior, refer to `Retaining records of asynchronous invocations <https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-retain-records.html>`_ .

            To retain records of failed invocations from `Kinesis <https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html>`_ , `DynamoDB <https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html>`_ , `self-managed Kafka <https://docs.aws.amazon.com/lambda/latest/dg/with-kafka.html#services-smaa-onfailure-destination>`_ or `Amazon MSK <https://docs.aws.amazon.com/lambda/latest/dg/with-msk.html#services-msk-onfailure-destination>`_ , you can configure an Amazon SNS topic, Amazon SQS queue, or Amazon S3 bucket as the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventinvokeconfig-onfailure.html#cfn-lambda-eventinvokeconfig-onfailure-destination
            '''
            result = self._values.get("destination")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnFailureProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnEventInvokeConfigPropsMixin.OnSuccessProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination"},
    )
    class OnSuccessProperty:
        def __init__(
            self,
            *,
            destination: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A destination for events that were processed successfully.

            To retain records of successful `asynchronous invocations <https://docs.aws.amazon.com/lambda/latest/dg/invocation-async.html#invocation-async-destinations>`_ , you can configure an Amazon SNS topic, Amazon SQS queue, Lambda function, or Amazon EventBridge event bus as the destination.
            .. epigraph::

               ``OnSuccess`` is not supported in ``CreateEventSourceMapping`` or ``UpdateEventSourceMapping`` requests.

            :param destination: The Amazon Resource Name (ARN) of the destination resource. .. epigraph:: Amazon SNS destinations have a message size limit of 256 KB. If the combined size of the function request and response payload exceeds the limit, Lambda will drop the payload when sending ``OnFailure`` event to the destination. For details on this behavior, refer to `Retaining records of asynchronous invocations <https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-retain-records.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventinvokeconfig-onsuccess.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                on_success_property = lambda_mixins.CfnEventInvokeConfigPropsMixin.OnSuccessProperty(
                    destination="destination"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1b0c0a79ed3d5e4b1e08c2daac73a36d8be9be4a8ff0cd5d2febbc5eacfd7b6e)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination is not None:
                self._values["destination"] = destination

        @builtins.property
        def destination(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the destination resource.

            .. epigraph::

               Amazon SNS destinations have a message size limit of 256 KB. If the combined size of the function request and response payload exceeds the limit, Lambda will drop the payload when sending ``OnFailure`` event to the destination. For details on this behavior, refer to `Retaining records of asynchronous invocations <https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-retain-records.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventinvokeconfig-onsuccess.html#cfn-lambda-eventinvokeconfig-onsuccess-destination
            '''
            result = self._values.get("destination")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnSuccessProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnEventSourceMappingMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "amazon_managed_kafka_event_source_config": "amazonManagedKafkaEventSourceConfig",
        "batch_size": "batchSize",
        "bisect_batch_on_function_error": "bisectBatchOnFunctionError",
        "destination_config": "destinationConfig",
        "document_db_event_source_config": "documentDbEventSourceConfig",
        "enabled": "enabled",
        "event_source_arn": "eventSourceArn",
        "filter_criteria": "filterCriteria",
        "function_name": "functionName",
        "function_response_types": "functionResponseTypes",
        "kms_key_arn": "kmsKeyArn",
        "logging_config": "loggingConfig",
        "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
        "maximum_record_age_in_seconds": "maximumRecordAgeInSeconds",
        "maximum_retry_attempts": "maximumRetryAttempts",
        "metrics_config": "metricsConfig",
        "parallelization_factor": "parallelizationFactor",
        "provisioned_poller_config": "provisionedPollerConfig",
        "queues": "queues",
        "scaling_config": "scalingConfig",
        "self_managed_event_source": "selfManagedEventSource",
        "self_managed_kafka_event_source_config": "selfManagedKafkaEventSourceConfig",
        "source_access_configurations": "sourceAccessConfigurations",
        "starting_position": "startingPosition",
        "starting_position_timestamp": "startingPositionTimestamp",
        "tags": "tags",
        "topics": "topics",
        "tumbling_window_in_seconds": "tumblingWindowInSeconds",
    },
)
class CfnEventSourceMappingMixinProps:
    def __init__(
        self,
        *,
        amazon_managed_kafka_event_source_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventSourceMappingPropsMixin.AmazonManagedKafkaEventSourceConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_function_error: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        destination_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventSourceMappingPropsMixin.DestinationConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        document_db_event_source_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventSourceMappingPropsMixin.DocumentDBEventSourceConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        event_source_arn: typing.Optional[builtins.str] = None,
        filter_criteria: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventSourceMappingPropsMixin.FilterCriteriaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        function_name: typing.Optional[builtins.str] = None,
        function_response_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventSourceMappingPropsMixin.LoggingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
        maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        metrics_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventSourceMappingPropsMixin.MetricsConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        provisioned_poller_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventSourceMappingPropsMixin.ProvisionedPollerConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        queues: typing.Optional[typing.Sequence[builtins.str]] = None,
        scaling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventSourceMappingPropsMixin.ScalingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        self_managed_event_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventSourceMappingPropsMixin.SelfManagedEventSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        self_managed_kafka_event_source_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventSourceMappingPropsMixin.SelfManagedKafkaEventSourceConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        source_access_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventSourceMappingPropsMixin.SourceAccessConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        starting_position: typing.Optional[builtins.str] = None,
        starting_position_timestamp: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        topics: typing.Optional[typing.Sequence[builtins.str]] = None,
        tumbling_window_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for CfnEventSourceMappingPropsMixin.

        :param amazon_managed_kafka_event_source_config: Specific configuration settings for an Amazon Managed Streaming for Apache Kafka (Amazon MSK) event source.
        :param batch_size: The maximum number of records in each batch that Lambda pulls from your stream or queue and sends to your function. Lambda passes all of the records in the batch to the function in a single call, up to the payload limit for synchronous invocation (6 MB). - *Amazon Kinesis* – Default 100. Max 10,000. - *Amazon DynamoDB Streams* – Default 100. Max 10,000. - *Amazon Simple Queue Service* – Default 10. For standard queues the max is 10,000. For FIFO queues the max is 10. - *Amazon Managed Streaming for Apache Kafka* – Default 100. Max 10,000. - *Self-managed Apache Kafka* – Default 100. Max 10,000. - *Amazon MQ (ActiveMQ and RabbitMQ)* – Default 100. Max 10,000. - *DocumentDB* – Default 100. Max 10,000.
        :param bisect_batch_on_function_error: (Kinesis and DynamoDB Streams only) If the function returns an error, split the batch in two and retry. The default value is false. .. epigraph:: When using ``BisectBatchOnFunctionError`` , check the ``BatchSize`` parameter in the ``OnFailure`` destination message's metadata. The ``BatchSize`` could be greater than 1 since Lambda consolidates failed messages metadata when writing to the ``OnFailure`` destination.
        :param destination_config: (Kinesis, DynamoDB Streams, Amazon MSK, and self-managed Apache Kafka) A configuration object that specifies the destination of an event after Lambda processes it.
        :param document_db_event_source_config: Specific configuration settings for a DocumentDB event source.
        :param enabled: When true, the event source mapping is active. When false, Lambda pauses polling and invocation. Default: True
        :param event_source_arn: The Amazon Resource Name (ARN) of the event source. - *Amazon Kinesis* – The ARN of the data stream or a stream consumer. - *Amazon DynamoDB Streams* – The ARN of the stream. - *Amazon Simple Queue Service* – The ARN of the queue. - *Amazon Managed Streaming for Apache Kafka* – The ARN of the cluster or the ARN of the VPC connection (for `cross-account event source mappings <https://docs.aws.amazon.com/lambda/latest/dg/with-msk.html#msk-multi-vpc>`_ ). - *Amazon MQ* – The ARN of the broker. - *Amazon DocumentDB* – The ARN of the DocumentDB change stream.
        :param filter_criteria: An object that defines the filter criteria that determine whether Lambda should process an event. For more information, see `Lambda event filtering <https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventfiltering.html>`_ .
        :param function_name: The name or ARN of the Lambda function. **Name formats** - *Function name* – ``MyFunction`` . - *Function ARN* – ``arn:aws:lambda:us-west-2:123456789012:function:MyFunction`` . - *Version or Alias ARN* – ``arn:aws:lambda:us-west-2:123456789012:function:MyFunction:PROD`` . - *Partial ARN* – ``123456789012:function:MyFunction`` . The length constraint applies only to the full ARN. If you specify only the function name, it's limited to 64 characters in length.
        :param function_response_types: (Kinesis, DynamoDB Streams, and SQS) A list of current response type enums applied to the event source mapping. Valid Values: ``ReportBatchItemFailures``
        :param kms_key_arn: The ARN of the AWS Key Management Service ( AWS ) customer managed key that Lambda uses to encrypt your function's `filter criteria <https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventfiltering.html#filtering-basics>`_ .
        :param logging_config: The function's Amazon CloudWatch Logs configuration settings.
        :param maximum_batching_window_in_seconds: The maximum amount of time, in seconds, that Lambda spends gathering records before invoking the function. *Default ( Kinesis , DynamoDB , Amazon SQS event sources)* : 0 *Default ( Amazon MSK , Kafka, Amazon MQ , Amazon DocumentDB event sources)* : 500 ms *Related setting:* For Amazon SQS event sources, when you set ``BatchSize`` to a value greater than 10, you must set ``MaximumBatchingWindowInSeconds`` to at least 1.
        :param maximum_record_age_in_seconds: (Kinesis, DynamoDB Streams, Amazon MSK, and self-managed Apache Kafka) Discard records older than the specified age. The default value is -1, which sets the maximum age to infinite. When the value is set to infinite, Lambda never discards old records. .. epigraph:: The minimum valid value for maximum record age is 60s. Although values less than 60 and greater than -1 fall within the parameter's absolute range, they are not allowed
        :param maximum_retry_attempts: (Kinesis, DynamoDB Streams, Amazon MSK, and self-managed Apache Kafka) Discard records after the specified number of retries. The default value is -1, which sets the maximum number of retries to infinite. When MaximumRetryAttempts is infinite, Lambda retries failed records until the record expires in the event source.
        :param metrics_config: The metrics configuration for your event source. For more information, see `Event source mapping metrics <https://docs.aws.amazon.com/lambda/latest/dg/monitoring-metrics-types.html#event-source-mapping-metrics>`_ .
        :param parallelization_factor: (Kinesis and DynamoDB Streams only) The number of batches to process concurrently from each shard. The default value is 1.
        :param provisioned_poller_config: (Amazon SQS, Amazon MSK, and self-managed Apache Kafka only) The provisioned mode configuration for the event source. For more information, see `provisioned mode <https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html#invocation-eventsourcemapping-provisioned-mode>`_ .
        :param queues: (Amazon MQ) The name of the Amazon MQ broker destination queue to consume.
        :param scaling_config: This property is for Amazon SQS event sources only. You cannot use ``ProvisionedPollerConfig`` while using ``ScalingConfig`` . These options are mutually exclusive. To remove the scaling configuration, pass an empty value.
        :param self_managed_event_source: The self-managed Apache Kafka cluster for your event source.
        :param self_managed_kafka_event_source_config: Specific configuration settings for a self-managed Apache Kafka event source.
        :param source_access_configurations: An array of the authentication protocol, VPC components, or virtual host to secure and define your event source.
        :param starting_position: The position in a stream from which to start reading. Required for Amazon Kinesis and Amazon DynamoDB. - *LATEST* - Read only new records. - *TRIM_HORIZON* - Process all available records. - *AT_TIMESTAMP* - Specify a time from which to start reading records.
        :param starting_position_timestamp: With ``StartingPosition`` set to ``AT_TIMESTAMP`` , the time from which to start reading, in Unix time seconds. ``StartingPositionTimestamp`` cannot be in the future.
        :param tags: A list of tags to add to the event source mapping. .. epigraph:: You must have the ``lambda:TagResource`` , ``lambda:UntagResource`` , and ``lambda:ListTags`` permissions for your `IAM principal <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html>`_ to manage the CloudFormation stack. If you don't have these permissions, there might be unexpected behavior with stack-level tags propagating to the resource during resource creation and update.
        :param topics: The name of the Kafka topic.
        :param tumbling_window_in_seconds: (Kinesis and DynamoDB Streams only) The duration in seconds of a processing window for DynamoDB and Kinesis Streams event sources. A value of 0 seconds indicates no tumbling window.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
            
            cfn_event_source_mapping_mixin_props = lambda_mixins.CfnEventSourceMappingMixinProps(
                amazon_managed_kafka_event_source_config=lambda_mixins.CfnEventSourceMappingPropsMixin.AmazonManagedKafkaEventSourceConfigProperty(
                    consumer_group_id="consumerGroupId",
                    schema_registry_config=lambda_mixins.CfnEventSourceMappingPropsMixin.SchemaRegistryConfigProperty(
                        access_configs=[lambda_mixins.CfnEventSourceMappingPropsMixin.SchemaRegistryAccessConfigProperty(
                            type="type",
                            uri="uri"
                        )],
                        event_record_format="eventRecordFormat",
                        schema_registry_uri="schemaRegistryUri",
                        schema_validation_configs=[lambda_mixins.CfnEventSourceMappingPropsMixin.SchemaValidationConfigProperty(
                            attribute="attribute"
                        )]
                    )
                ),
                batch_size=123,
                bisect_batch_on_function_error=False,
                destination_config=lambda_mixins.CfnEventSourceMappingPropsMixin.DestinationConfigProperty(
                    on_failure=lambda_mixins.CfnEventSourceMappingPropsMixin.OnFailureProperty(
                        destination="destination"
                    )
                ),
                document_db_event_source_config=lambda_mixins.CfnEventSourceMappingPropsMixin.DocumentDBEventSourceConfigProperty(
                    collection_name="collectionName",
                    database_name="databaseName",
                    full_document="fullDocument"
                ),
                enabled=False,
                event_source_arn="eventSourceArn",
                filter_criteria=lambda_mixins.CfnEventSourceMappingPropsMixin.FilterCriteriaProperty(
                    filters=[lambda_mixins.CfnEventSourceMappingPropsMixin.FilterProperty(
                        pattern="pattern"
                    )]
                ),
                function_name="functionName",
                function_response_types=["functionResponseTypes"],
                kms_key_arn="kmsKeyArn",
                logging_config=lambda_mixins.CfnEventSourceMappingPropsMixin.LoggingConfigProperty(
                    system_log_level="systemLogLevel"
                ),
                maximum_batching_window_in_seconds=123,
                maximum_record_age_in_seconds=123,
                maximum_retry_attempts=123,
                metrics_config=lambda_mixins.CfnEventSourceMappingPropsMixin.MetricsConfigProperty(
                    metrics=["metrics"]
                ),
                parallelization_factor=123,
                provisioned_poller_config=lambda_mixins.CfnEventSourceMappingPropsMixin.ProvisionedPollerConfigProperty(
                    maximum_pollers=123,
                    minimum_pollers=123,
                    poller_group_name="pollerGroupName"
                ),
                queues=["queues"],
                scaling_config=lambda_mixins.CfnEventSourceMappingPropsMixin.ScalingConfigProperty(
                    maximum_concurrency=123
                ),
                self_managed_event_source=lambda_mixins.CfnEventSourceMappingPropsMixin.SelfManagedEventSourceProperty(
                    endpoints=lambda_mixins.CfnEventSourceMappingPropsMixin.EndpointsProperty(
                        kafka_bootstrap_servers=["kafkaBootstrapServers"]
                    )
                ),
                self_managed_kafka_event_source_config=lambda_mixins.CfnEventSourceMappingPropsMixin.SelfManagedKafkaEventSourceConfigProperty(
                    consumer_group_id="consumerGroupId",
                    schema_registry_config=lambda_mixins.CfnEventSourceMappingPropsMixin.SchemaRegistryConfigProperty(
                        access_configs=[lambda_mixins.CfnEventSourceMappingPropsMixin.SchemaRegistryAccessConfigProperty(
                            type="type",
                            uri="uri"
                        )],
                        event_record_format="eventRecordFormat",
                        schema_registry_uri="schemaRegistryUri",
                        schema_validation_configs=[lambda_mixins.CfnEventSourceMappingPropsMixin.SchemaValidationConfigProperty(
                            attribute="attribute"
                        )]
                    )
                ),
                source_access_configurations=[lambda_mixins.CfnEventSourceMappingPropsMixin.SourceAccessConfigurationProperty(
                    type="type",
                    uri="uri"
                )],
                starting_position="startingPosition",
                starting_position_timestamp=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                topics=["topics"],
                tumbling_window_in_seconds=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3651a8aaa3f9ebdaa199a9708d570432aa9e54d5f39512bce458df8a84b76999)
            check_type(argname="argument amazon_managed_kafka_event_source_config", value=amazon_managed_kafka_event_source_config, expected_type=type_hints["amazon_managed_kafka_event_source_config"])
            check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
            check_type(argname="argument bisect_batch_on_function_error", value=bisect_batch_on_function_error, expected_type=type_hints["bisect_batch_on_function_error"])
            check_type(argname="argument destination_config", value=destination_config, expected_type=type_hints["destination_config"])
            check_type(argname="argument document_db_event_source_config", value=document_db_event_source_config, expected_type=type_hints["document_db_event_source_config"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument event_source_arn", value=event_source_arn, expected_type=type_hints["event_source_arn"])
            check_type(argname="argument filter_criteria", value=filter_criteria, expected_type=type_hints["filter_criteria"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument function_response_types", value=function_response_types, expected_type=type_hints["function_response_types"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
            check_type(argname="argument maximum_record_age_in_seconds", value=maximum_record_age_in_seconds, expected_type=type_hints["maximum_record_age_in_seconds"])
            check_type(argname="argument maximum_retry_attempts", value=maximum_retry_attempts, expected_type=type_hints["maximum_retry_attempts"])
            check_type(argname="argument metrics_config", value=metrics_config, expected_type=type_hints["metrics_config"])
            check_type(argname="argument parallelization_factor", value=parallelization_factor, expected_type=type_hints["parallelization_factor"])
            check_type(argname="argument provisioned_poller_config", value=provisioned_poller_config, expected_type=type_hints["provisioned_poller_config"])
            check_type(argname="argument queues", value=queues, expected_type=type_hints["queues"])
            check_type(argname="argument scaling_config", value=scaling_config, expected_type=type_hints["scaling_config"])
            check_type(argname="argument self_managed_event_source", value=self_managed_event_source, expected_type=type_hints["self_managed_event_source"])
            check_type(argname="argument self_managed_kafka_event_source_config", value=self_managed_kafka_event_source_config, expected_type=type_hints["self_managed_kafka_event_source_config"])
            check_type(argname="argument source_access_configurations", value=source_access_configurations, expected_type=type_hints["source_access_configurations"])
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
            check_type(argname="argument starting_position_timestamp", value=starting_position_timestamp, expected_type=type_hints["starting_position_timestamp"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument topics", value=topics, expected_type=type_hints["topics"])
            check_type(argname="argument tumbling_window_in_seconds", value=tumbling_window_in_seconds, expected_type=type_hints["tumbling_window_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if amazon_managed_kafka_event_source_config is not None:
            self._values["amazon_managed_kafka_event_source_config"] = amazon_managed_kafka_event_source_config
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if bisect_batch_on_function_error is not None:
            self._values["bisect_batch_on_function_error"] = bisect_batch_on_function_error
        if destination_config is not None:
            self._values["destination_config"] = destination_config
        if document_db_event_source_config is not None:
            self._values["document_db_event_source_config"] = document_db_event_source_config
        if enabled is not None:
            self._values["enabled"] = enabled
        if event_source_arn is not None:
            self._values["event_source_arn"] = event_source_arn
        if filter_criteria is not None:
            self._values["filter_criteria"] = filter_criteria
        if function_name is not None:
            self._values["function_name"] = function_name
        if function_response_types is not None:
            self._values["function_response_types"] = function_response_types
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if maximum_batching_window_in_seconds is not None:
            self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
        if maximum_record_age_in_seconds is not None:
            self._values["maximum_record_age_in_seconds"] = maximum_record_age_in_seconds
        if maximum_retry_attempts is not None:
            self._values["maximum_retry_attempts"] = maximum_retry_attempts
        if metrics_config is not None:
            self._values["metrics_config"] = metrics_config
        if parallelization_factor is not None:
            self._values["parallelization_factor"] = parallelization_factor
        if provisioned_poller_config is not None:
            self._values["provisioned_poller_config"] = provisioned_poller_config
        if queues is not None:
            self._values["queues"] = queues
        if scaling_config is not None:
            self._values["scaling_config"] = scaling_config
        if self_managed_event_source is not None:
            self._values["self_managed_event_source"] = self_managed_event_source
        if self_managed_kafka_event_source_config is not None:
            self._values["self_managed_kafka_event_source_config"] = self_managed_kafka_event_source_config
        if source_access_configurations is not None:
            self._values["source_access_configurations"] = source_access_configurations
        if starting_position is not None:
            self._values["starting_position"] = starting_position
        if starting_position_timestamp is not None:
            self._values["starting_position_timestamp"] = starting_position_timestamp
        if tags is not None:
            self._values["tags"] = tags
        if topics is not None:
            self._values["topics"] = topics
        if tumbling_window_in_seconds is not None:
            self._values["tumbling_window_in_seconds"] = tumbling_window_in_seconds

    @builtins.property
    def amazon_managed_kafka_event_source_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.AmazonManagedKafkaEventSourceConfigProperty"]]:
        '''Specific configuration settings for an Amazon Managed Streaming for Apache Kafka (Amazon MSK) event source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-amazonmanagedkafkaeventsourceconfig
        '''
        result = self._values.get("amazon_managed_kafka_event_source_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.AmazonManagedKafkaEventSourceConfigProperty"]], result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of records in each batch that Lambda pulls from your stream or queue and sends to your function.

        Lambda passes all of the records in the batch to the function in a single call, up to the payload limit for synchronous invocation (6 MB).

        - *Amazon Kinesis* – Default 100. Max 10,000.
        - *Amazon DynamoDB Streams* – Default 100. Max 10,000.
        - *Amazon Simple Queue Service* – Default 10. For standard queues the max is 10,000. For FIFO queues the max is 10.
        - *Amazon Managed Streaming for Apache Kafka* – Default 100. Max 10,000.
        - *Self-managed Apache Kafka* – Default 100. Max 10,000.
        - *Amazon MQ (ActiveMQ and RabbitMQ)* – Default 100. Max 10,000.
        - *DocumentDB* – Default 100. Max 10,000.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-batchsize
        '''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bisect_batch_on_function_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''(Kinesis and DynamoDB Streams only) If the function returns an error, split the batch in two and retry.

        The default value is false.
        .. epigraph::

           When using ``BisectBatchOnFunctionError`` , check the ``BatchSize`` parameter in the ``OnFailure`` destination message's metadata. The ``BatchSize`` could be greater than 1 since Lambda consolidates failed messages metadata when writing to the ``OnFailure`` destination.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-bisectbatchonfunctionerror
        '''
        result = self._values.get("bisect_batch_on_function_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def destination_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.DestinationConfigProperty"]]:
        '''(Kinesis, DynamoDB Streams, Amazon MSK, and self-managed Apache Kafka) A configuration object that specifies the destination of an event after Lambda processes it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-destinationconfig
        '''
        result = self._values.get("destination_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.DestinationConfigProperty"]], result)

    @builtins.property
    def document_db_event_source_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.DocumentDBEventSourceConfigProperty"]]:
        '''Specific configuration settings for a DocumentDB event source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-documentdbeventsourceconfig
        '''
        result = self._values.get("document_db_event_source_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.DocumentDBEventSourceConfigProperty"]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''When true, the event source mapping is active. When false, Lambda pauses polling and invocation.

        Default: True

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def event_source_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the event source.

        - *Amazon Kinesis* – The ARN of the data stream or a stream consumer.
        - *Amazon DynamoDB Streams* – The ARN of the stream.
        - *Amazon Simple Queue Service* – The ARN of the queue.
        - *Amazon Managed Streaming for Apache Kafka* – The ARN of the cluster or the ARN of the VPC connection (for `cross-account event source mappings <https://docs.aws.amazon.com/lambda/latest/dg/with-msk.html#msk-multi-vpc>`_ ).
        - *Amazon MQ* – The ARN of the broker.
        - *Amazon DocumentDB* – The ARN of the DocumentDB change stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-eventsourcearn
        '''
        result = self._values.get("event_source_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_criteria(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.FilterCriteriaProperty"]]:
        '''An object that defines the filter criteria that determine whether Lambda should process an event.

        For more information, see `Lambda event filtering <https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventfiltering.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-filtercriteria
        '''
        result = self._values.get("filter_criteria")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.FilterCriteriaProperty"]], result)

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        '''The name or ARN of the Lambda function.

        **Name formats** - *Function name* – ``MyFunction`` .

        - *Function ARN* – ``arn:aws:lambda:us-west-2:123456789012:function:MyFunction`` .
        - *Version or Alias ARN* – ``arn:aws:lambda:us-west-2:123456789012:function:MyFunction:PROD`` .
        - *Partial ARN* – ``123456789012:function:MyFunction`` .

        The length constraint applies only to the full ARN. If you specify only the function name, it's limited to 64 characters in length.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-functionname
        '''
        result = self._values.get("function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def function_response_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(Kinesis, DynamoDB Streams, and SQS) A list of current response type enums applied to the event source mapping.

        Valid Values: ``ReportBatchItemFailures``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-functionresponsetypes
        '''
        result = self._values.get("function_response_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the AWS Key Management Service ( AWS  ) customer managed key that Lambda uses to encrypt your function's `filter criteria <https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventfiltering.html#filtering-basics>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-kmskeyarn
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.LoggingConfigProperty"]]:
        '''The function's Amazon CloudWatch Logs configuration settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-loggingconfig
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.LoggingConfigProperty"]], result)

    @builtins.property
    def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''The maximum amount of time, in seconds, that Lambda spends gathering records before invoking the function.

        *Default ( Kinesis , DynamoDB , Amazon SQS event sources)* : 0

        *Default ( Amazon MSK , Kafka, Amazon MQ , Amazon DocumentDB event sources)* : 500 ms

        *Related setting:* For Amazon SQS event sources, when you set ``BatchSize`` to a value greater than 10, you must set ``MaximumBatchingWindowInSeconds`` to at least 1.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-maximumbatchingwindowinseconds
        '''
        result = self._values.get("maximum_batching_window_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_record_age_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''(Kinesis, DynamoDB Streams, Amazon MSK, and self-managed Apache Kafka) Discard records older than the specified age.

        The default value is -1,
        which sets the maximum age to infinite. When the value is set to infinite, Lambda never discards old records.
        .. epigraph::

           The minimum valid value for maximum record age is 60s. Although values less than 60 and greater than -1 fall within the parameter's absolute range, they are not allowed

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-maximumrecordageinseconds
        '''
        result = self._values.get("maximum_record_age_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(Kinesis, DynamoDB Streams, Amazon MSK, and self-managed Apache Kafka) Discard records after the specified number of retries.

        The default value is -1,
        which sets the maximum number of retries to infinite. When MaximumRetryAttempts is infinite, Lambda retries failed records until the record expires in the event source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-maximumretryattempts
        '''
        result = self._values.get("maximum_retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metrics_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.MetricsConfigProperty"]]:
        '''The metrics configuration for your event source.

        For more information, see `Event source mapping metrics <https://docs.aws.amazon.com/lambda/latest/dg/monitoring-metrics-types.html#event-source-mapping-metrics>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-metricsconfig
        '''
        result = self._values.get("metrics_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.MetricsConfigProperty"]], result)

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        '''(Kinesis and DynamoDB Streams only) The number of batches to process concurrently from each shard.

        The default value is 1.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-parallelizationfactor
        '''
        result = self._values.get("parallelization_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def provisioned_poller_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.ProvisionedPollerConfigProperty"]]:
        '''(Amazon SQS, Amazon MSK, and self-managed Apache Kafka only) The provisioned mode configuration for the event source.

        For more information, see `provisioned mode <https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html#invocation-eventsourcemapping-provisioned-mode>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-provisionedpollerconfig
        '''
        result = self._values.get("provisioned_poller_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.ProvisionedPollerConfigProperty"]], result)

    @builtins.property
    def queues(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(Amazon MQ) The name of the Amazon MQ broker destination queue to consume.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-queues
        '''
        result = self._values.get("queues")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def scaling_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.ScalingConfigProperty"]]:
        '''This property is for Amazon SQS event sources only.

        You cannot use ``ProvisionedPollerConfig`` while using ``ScalingConfig`` . These options are mutually exclusive. To remove the scaling configuration, pass an empty value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-scalingconfig
        '''
        result = self._values.get("scaling_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.ScalingConfigProperty"]], result)

    @builtins.property
    def self_managed_event_source(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.SelfManagedEventSourceProperty"]]:
        '''The self-managed Apache Kafka cluster for your event source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-selfmanagedeventsource
        '''
        result = self._values.get("self_managed_event_source")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.SelfManagedEventSourceProperty"]], result)

    @builtins.property
    def self_managed_kafka_event_source_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.SelfManagedKafkaEventSourceConfigProperty"]]:
        '''Specific configuration settings for a self-managed Apache Kafka event source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-selfmanagedkafkaeventsourceconfig
        '''
        result = self._values.get("self_managed_kafka_event_source_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.SelfManagedKafkaEventSourceConfigProperty"]], result)

    @builtins.property
    def source_access_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.SourceAccessConfigurationProperty"]]]]:
        '''An array of the authentication protocol, VPC components, or virtual host to secure and define your event source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-sourceaccessconfigurations
        '''
        result = self._values.get("source_access_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.SourceAccessConfigurationProperty"]]]], result)

    @builtins.property
    def starting_position(self) -> typing.Optional[builtins.str]:
        '''The position in a stream from which to start reading. Required for Amazon Kinesis and Amazon DynamoDB.

        - *LATEST* - Read only new records.
        - *TRIM_HORIZON* - Process all available records.
        - *AT_TIMESTAMP* - Specify a time from which to start reading records.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-startingposition
        '''
        result = self._values.get("starting_position")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def starting_position_timestamp(self) -> typing.Optional[jsii.Number]:
        '''With ``StartingPosition`` set to ``AT_TIMESTAMP`` , the time from which to start reading, in Unix time seconds.

        ``StartingPositionTimestamp`` cannot be in the future.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-startingpositiontimestamp
        '''
        result = self._values.get("starting_position_timestamp")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags to add to the event source mapping.

        .. epigraph::

           You must have the ``lambda:TagResource`` , ``lambda:UntagResource`` , and ``lambda:ListTags`` permissions for your `IAM principal <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html>`_ to manage the CloudFormation stack. If you don't have these permissions, there might be unexpected behavior with stack-level tags propagating to the resource during resource creation and update.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def topics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of the Kafka topic.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-topics
        '''
        result = self._values.get("topics")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tumbling_window_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''(Kinesis and DynamoDB Streams only) The duration in seconds of a processing window for DynamoDB and Kinesis Streams event sources.

        A value of 0 seconds indicates no tumbling window.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-tumblingwindowinseconds
        '''
        result = self._values.get("tumbling_window_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEventSourceMappingMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEventSourceMappingPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnEventSourceMappingPropsMixin",
):
    '''The ``AWS::Lambda::EventSourceMapping`` resource creates a mapping between an event source and an AWS Lambda function.

    Lambda reads items from the event source and triggers the function.

    For details about each event source type, see the following topics. In particular, each of the topics describes the required and optional parameters for the specific event source.

    - `Configuring a Dynamo DB stream as an event source <https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html#services-dynamodb-eventsourcemapping>`_
    - `Configuring a Kinesis stream as an event source <https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html#services-kinesis-eventsourcemapping>`_
    - `Configuring an SQS queue as an event source <https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html#events-sqs-eventsource>`_
    - `Configuring an MQ broker as an event source <https://docs.aws.amazon.com/lambda/latest/dg/with-mq.html#services-mq-eventsourcemapping>`_
    - `Configuring MSK as an event source <https://docs.aws.amazon.com/lambda/latest/dg/with-msk.html>`_
    - `Configuring Self-Managed Apache Kafka as an event source <https://docs.aws.amazon.com/lambda/latest/dg/kafka-smaa.html>`_
    - `Configuring Amazon DocumentDB as an event source <https://docs.aws.amazon.com/lambda/latest/dg/with-documentdb.html>`_

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html
    :cloudformationResource: AWS::Lambda::EventSourceMapping
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
        
        cfn_event_source_mapping_props_mixin = lambda_mixins.CfnEventSourceMappingPropsMixin(lambda_mixins.CfnEventSourceMappingMixinProps(
            amazon_managed_kafka_event_source_config=lambda_mixins.CfnEventSourceMappingPropsMixin.AmazonManagedKafkaEventSourceConfigProperty(
                consumer_group_id="consumerGroupId",
                schema_registry_config=lambda_mixins.CfnEventSourceMappingPropsMixin.SchemaRegistryConfigProperty(
                    access_configs=[lambda_mixins.CfnEventSourceMappingPropsMixin.SchemaRegistryAccessConfigProperty(
                        type="type",
                        uri="uri"
                    )],
                    event_record_format="eventRecordFormat",
                    schema_registry_uri="schemaRegistryUri",
                    schema_validation_configs=[lambda_mixins.CfnEventSourceMappingPropsMixin.SchemaValidationConfigProperty(
                        attribute="attribute"
                    )]
                )
            ),
            batch_size=123,
            bisect_batch_on_function_error=False,
            destination_config=lambda_mixins.CfnEventSourceMappingPropsMixin.DestinationConfigProperty(
                on_failure=lambda_mixins.CfnEventSourceMappingPropsMixin.OnFailureProperty(
                    destination="destination"
                )
            ),
            document_db_event_source_config=lambda_mixins.CfnEventSourceMappingPropsMixin.DocumentDBEventSourceConfigProperty(
                collection_name="collectionName",
                database_name="databaseName",
                full_document="fullDocument"
            ),
            enabled=False,
            event_source_arn="eventSourceArn",
            filter_criteria=lambda_mixins.CfnEventSourceMappingPropsMixin.FilterCriteriaProperty(
                filters=[lambda_mixins.CfnEventSourceMappingPropsMixin.FilterProperty(
                    pattern="pattern"
                )]
            ),
            function_name="functionName",
            function_response_types=["functionResponseTypes"],
            kms_key_arn="kmsKeyArn",
            logging_config=lambda_mixins.CfnEventSourceMappingPropsMixin.LoggingConfigProperty(
                system_log_level="systemLogLevel"
            ),
            maximum_batching_window_in_seconds=123,
            maximum_record_age_in_seconds=123,
            maximum_retry_attempts=123,
            metrics_config=lambda_mixins.CfnEventSourceMappingPropsMixin.MetricsConfigProperty(
                metrics=["metrics"]
            ),
            parallelization_factor=123,
            provisioned_poller_config=lambda_mixins.CfnEventSourceMappingPropsMixin.ProvisionedPollerConfigProperty(
                maximum_pollers=123,
                minimum_pollers=123,
                poller_group_name="pollerGroupName"
            ),
            queues=["queues"],
            scaling_config=lambda_mixins.CfnEventSourceMappingPropsMixin.ScalingConfigProperty(
                maximum_concurrency=123
            ),
            self_managed_event_source=lambda_mixins.CfnEventSourceMappingPropsMixin.SelfManagedEventSourceProperty(
                endpoints=lambda_mixins.CfnEventSourceMappingPropsMixin.EndpointsProperty(
                    kafka_bootstrap_servers=["kafkaBootstrapServers"]
                )
            ),
            self_managed_kafka_event_source_config=lambda_mixins.CfnEventSourceMappingPropsMixin.SelfManagedKafkaEventSourceConfigProperty(
                consumer_group_id="consumerGroupId",
                schema_registry_config=lambda_mixins.CfnEventSourceMappingPropsMixin.SchemaRegistryConfigProperty(
                    access_configs=[lambda_mixins.CfnEventSourceMappingPropsMixin.SchemaRegistryAccessConfigProperty(
                        type="type",
                        uri="uri"
                    )],
                    event_record_format="eventRecordFormat",
                    schema_registry_uri="schemaRegistryUri",
                    schema_validation_configs=[lambda_mixins.CfnEventSourceMappingPropsMixin.SchemaValidationConfigProperty(
                        attribute="attribute"
                    )]
                )
            ),
            source_access_configurations=[lambda_mixins.CfnEventSourceMappingPropsMixin.SourceAccessConfigurationProperty(
                type="type",
                uri="uri"
            )],
            starting_position="startingPosition",
            starting_position_timestamp=123,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            topics=["topics"],
            tumbling_window_in_seconds=123
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEventSourceMappingMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lambda::EventSourceMapping``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f76000eee7701dbf527e107c9a8a89c610a77fd9068ea05bff861cf867110099)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16c031629768dda22e010d1942ce617c71aa22463d0bbb1a461672f188abe799)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b60fefa766362cc0c416fa583cc7fde8d8f07826ebe0a0d228493f6bf78ca9a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEventSourceMappingMixinProps:
        return typing.cast(CfnEventSourceMappingMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnEventSourceMappingPropsMixin.AmazonManagedKafkaEventSourceConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "consumer_group_id": "consumerGroupId",
            "schema_registry_config": "schemaRegistryConfig",
        },
    )
    class AmazonManagedKafkaEventSourceConfigProperty:
        def __init__(
            self,
            *,
            consumer_group_id: typing.Optional[builtins.str] = None,
            schema_registry_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventSourceMappingPropsMixin.SchemaRegistryConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specific configuration settings for an Amazon Managed Streaming for Apache Kafka (Amazon MSK) event source.

            :param consumer_group_id: The identifier for the Kafka consumer group to join. The consumer group ID must be unique among all your Kafka event sources. After creating a Kafka event source mapping with the consumer group ID specified, you cannot update this value. For more information, see `Customizable consumer group ID <https://docs.aws.amazon.com/lambda/latest/dg/with-msk.html#services-msk-consumer-group-id>`_ .
            :param schema_registry_config: Specific configuration settings for a Kafka schema registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-amazonmanagedkafkaeventsourceconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                amazon_managed_kafka_event_source_config_property = lambda_mixins.CfnEventSourceMappingPropsMixin.AmazonManagedKafkaEventSourceConfigProperty(
                    consumer_group_id="consumerGroupId",
                    schema_registry_config=lambda_mixins.CfnEventSourceMappingPropsMixin.SchemaRegistryConfigProperty(
                        access_configs=[lambda_mixins.CfnEventSourceMappingPropsMixin.SchemaRegistryAccessConfigProperty(
                            type="type",
                            uri="uri"
                        )],
                        event_record_format="eventRecordFormat",
                        schema_registry_uri="schemaRegistryUri",
                        schema_validation_configs=[lambda_mixins.CfnEventSourceMappingPropsMixin.SchemaValidationConfigProperty(
                            attribute="attribute"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1faa149851617d2bd03a7c53588fb19bab764e6bf71bb18f52582666755c8c21)
                check_type(argname="argument consumer_group_id", value=consumer_group_id, expected_type=type_hints["consumer_group_id"])
                check_type(argname="argument schema_registry_config", value=schema_registry_config, expected_type=type_hints["schema_registry_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if consumer_group_id is not None:
                self._values["consumer_group_id"] = consumer_group_id
            if schema_registry_config is not None:
                self._values["schema_registry_config"] = schema_registry_config

        @builtins.property
        def consumer_group_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the Kafka consumer group to join.

            The consumer group ID must be unique among all your Kafka event sources. After creating a Kafka event source mapping with the consumer group ID specified, you cannot update this value. For more information, see `Customizable consumer group ID <https://docs.aws.amazon.com/lambda/latest/dg/with-msk.html#services-msk-consumer-group-id>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-amazonmanagedkafkaeventsourceconfig.html#cfn-lambda-eventsourcemapping-amazonmanagedkafkaeventsourceconfig-consumergroupid
            '''
            result = self._values.get("consumer_group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schema_registry_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.SchemaRegistryConfigProperty"]]:
            '''Specific configuration settings for a Kafka schema registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-amazonmanagedkafkaeventsourceconfig.html#cfn-lambda-eventsourcemapping-amazonmanagedkafkaeventsourceconfig-schemaregistryconfig
            '''
            result = self._values.get("schema_registry_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.SchemaRegistryConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AmazonManagedKafkaEventSourceConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnEventSourceMappingPropsMixin.DestinationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"on_failure": "onFailure"},
    )
    class DestinationConfigProperty:
        def __init__(
            self,
            *,
            on_failure: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventSourceMappingPropsMixin.OnFailureProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A configuration object that specifies the destination of an event after Lambda processes it.

            For more information, see `Adding a destination <https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-retain-records.html#invocation-async-destinations>`_ .

            :param on_failure: The destination configuration for failed invocations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-destinationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                destination_config_property = lambda_mixins.CfnEventSourceMappingPropsMixin.DestinationConfigProperty(
                    on_failure=lambda_mixins.CfnEventSourceMappingPropsMixin.OnFailureProperty(
                        destination="destination"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__81baf50d08b1aeaf1d4541bb5a849005cc0bdbb6a8fdc2b9c969f0ba86f13c05)
                check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if on_failure is not None:
                self._values["on_failure"] = on_failure

        @builtins.property
        def on_failure(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.OnFailureProperty"]]:
            '''The destination configuration for failed invocations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-destinationconfig.html#cfn-lambda-eventsourcemapping-destinationconfig-onfailure
            '''
            result = self._values.get("on_failure")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.OnFailureProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnEventSourceMappingPropsMixin.DocumentDBEventSourceConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "collection_name": "collectionName",
            "database_name": "databaseName",
            "full_document": "fullDocument",
        },
    )
    class DocumentDBEventSourceConfigProperty:
        def __init__(
            self,
            *,
            collection_name: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            full_document: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specific configuration settings for a DocumentDB event source.

            :param collection_name: The name of the collection to consume within the database. If you do not specify a collection, Lambda consumes all collections.
            :param database_name: The name of the database to consume within the DocumentDB cluster.
            :param full_document: Determines what DocumentDB sends to your event stream during document update operations. If set to UpdateLookup, DocumentDB sends a delta describing the changes, along with a copy of the entire document. Otherwise, DocumentDB sends only a partial document that contains the changes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-documentdbeventsourceconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                document_dBEvent_source_config_property = lambda_mixins.CfnEventSourceMappingPropsMixin.DocumentDBEventSourceConfigProperty(
                    collection_name="collectionName",
                    database_name="databaseName",
                    full_document="fullDocument"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a17b7a278cfae90a30dd3f76995be1c2a036bf5c0d25ca0e4c3e44e1c4496bc3)
                check_type(argname="argument collection_name", value=collection_name, expected_type=type_hints["collection_name"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument full_document", value=full_document, expected_type=type_hints["full_document"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if collection_name is not None:
                self._values["collection_name"] = collection_name
            if database_name is not None:
                self._values["database_name"] = database_name
            if full_document is not None:
                self._values["full_document"] = full_document

        @builtins.property
        def collection_name(self) -> typing.Optional[builtins.str]:
            '''The name of the collection to consume within the database.

            If you do not specify a collection, Lambda consumes all collections.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-documentdbeventsourceconfig.html#cfn-lambda-eventsourcemapping-documentdbeventsourceconfig-collectionname
            '''
            result = self._values.get("collection_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The name of the database to consume within the DocumentDB cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-documentdbeventsourceconfig.html#cfn-lambda-eventsourcemapping-documentdbeventsourceconfig-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def full_document(self) -> typing.Optional[builtins.str]:
            '''Determines what DocumentDB sends to your event stream during document update operations.

            If set to UpdateLookup, DocumentDB sends a delta describing the changes, along with a copy of the entire document. Otherwise, DocumentDB sends only a partial document that contains the changes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-documentdbeventsourceconfig.html#cfn-lambda-eventsourcemapping-documentdbeventsourceconfig-fulldocument
            '''
            result = self._values.get("full_document")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentDBEventSourceConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnEventSourceMappingPropsMixin.EndpointsProperty",
        jsii_struct_bases=[],
        name_mapping={"kafka_bootstrap_servers": "kafkaBootstrapServers"},
    )
    class EndpointsProperty:
        def __init__(
            self,
            *,
            kafka_bootstrap_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The list of bootstrap servers for your Kafka brokers in the following format: ``"KafkaBootstrapServers": ["abc.xyz.com:xxxx","abc2.xyz.com:xxxx"]`` .

            :param kafka_bootstrap_servers: The list of bootstrap servers for your Kafka brokers in the following format: ``"KafkaBootstrapServers": ["abc.xyz.com:xxxx","abc2.xyz.com:xxxx"]`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-endpoints.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                endpoints_property = lambda_mixins.CfnEventSourceMappingPropsMixin.EndpointsProperty(
                    kafka_bootstrap_servers=["kafkaBootstrapServers"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dec58e8e328a41c4cbd74d1fb218abda9e5a389291e2342418e75ba9dee04c3e)
                check_type(argname="argument kafka_bootstrap_servers", value=kafka_bootstrap_servers, expected_type=type_hints["kafka_bootstrap_servers"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kafka_bootstrap_servers is not None:
                self._values["kafka_bootstrap_servers"] = kafka_bootstrap_servers

        @builtins.property
        def kafka_bootstrap_servers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of bootstrap servers for your Kafka brokers in the following format: ``"KafkaBootstrapServers": ["abc.xyz.com:xxxx","abc2.xyz.com:xxxx"]`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-endpoints.html#cfn-lambda-eventsourcemapping-endpoints-kafkabootstrapservers
            '''
            result = self._values.get("kafka_bootstrap_servers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EndpointsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnEventSourceMappingPropsMixin.FilterCriteriaProperty",
        jsii_struct_bases=[],
        name_mapping={"filters": "filters"},
    )
    class FilterCriteriaProperty:
        def __init__(
            self,
            *,
            filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventSourceMappingPropsMixin.FilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''An object that contains the filters for an event source.

            :param filters: A list of filters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-filtercriteria.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                filter_criteria_property = lambda_mixins.CfnEventSourceMappingPropsMixin.FilterCriteriaProperty(
                    filters=[lambda_mixins.CfnEventSourceMappingPropsMixin.FilterProperty(
                        pattern="pattern"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7e41ea139482d0935756439fa42d7b5dcd3a1a08153521f55003e8f0e8fce283)
                check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if filters is not None:
                self._values["filters"] = filters

        @builtins.property
        def filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.FilterProperty"]]]]:
            '''A list of filters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-filtercriteria.html#cfn-lambda-eventsourcemapping-filtercriteria-filters
            '''
            result = self._values.get("filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.FilterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterCriteriaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnEventSourceMappingPropsMixin.FilterProperty",
        jsii_struct_bases=[],
        name_mapping={"pattern": "pattern"},
    )
    class FilterProperty:
        def __init__(self, *, pattern: typing.Optional[builtins.str] = None) -> None:
            '''A structure within a ``FilterCriteria`` object that defines an event filtering pattern.

            :param pattern: A filter pattern. For more information on the syntax of a filter pattern, see `Filter rule syntax <https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventfiltering.html#filtering-syntax>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-filter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                filter_property = lambda_mixins.CfnEventSourceMappingPropsMixin.FilterProperty(
                    pattern="pattern"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aa21c548bffd47cd2d2d016d3e511d6af3bd1d0d85f034dbb0a49e8a2080c758)
                check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if pattern is not None:
                self._values["pattern"] = pattern

        @builtins.property
        def pattern(self) -> typing.Optional[builtins.str]:
            '''A filter pattern.

            For more information on the syntax of a filter pattern, see `Filter rule syntax <https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventfiltering.html#filtering-syntax>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-filter.html#cfn-lambda-eventsourcemapping-filter-pattern
            '''
            result = self._values.get("pattern")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnEventSourceMappingPropsMixin.LoggingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"system_log_level": "systemLogLevel"},
    )
    class LoggingConfigProperty:
        def __init__(
            self,
            *,
            system_log_level: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The function's Amazon CloudWatch Logs configuration settings.

            :param system_log_level: Set this property to filter the system logs for your function that Lambda sends to CloudWatch. Lambda only sends system logs at the selected level of detail and lower, where ``DEBUG`` is the highest level and ``WARN`` is the lowest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-loggingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                logging_config_property = lambda_mixins.CfnEventSourceMappingPropsMixin.LoggingConfigProperty(
                    system_log_level="systemLogLevel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__404cef2da0edb20fb1e474e8716f13ee7da6e9c367b987a59ceef1aa3022ea0c)
                check_type(argname="argument system_log_level", value=system_log_level, expected_type=type_hints["system_log_level"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if system_log_level is not None:
                self._values["system_log_level"] = system_log_level

        @builtins.property
        def system_log_level(self) -> typing.Optional[builtins.str]:
            '''Set this property to filter the system logs for your function that Lambda sends to CloudWatch.

            Lambda only sends system logs at the selected level of detail and lower, where ``DEBUG`` is the highest level and ``WARN`` is the lowest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-loggingconfig.html#cfn-lambda-eventsourcemapping-loggingconfig-systemloglevel
            '''
            result = self._values.get("system_log_level")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnEventSourceMappingPropsMixin.MetricsConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"metrics": "metrics"},
    )
    class MetricsConfigProperty:
        def __init__(
            self,
            *,
            metrics: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The metrics configuration for your event source.

            Use this configuration object to define which metrics you want your event source mapping to produce.

            :param metrics: The metrics you want your event source mapping to produce. Include ``EventCount`` to receive event source mapping metrics related to the number of events processed by your event source mapping. For more information about these metrics, see `Event source mapping metrics <https://docs.aws.amazon.com/lambda/latest/dg/monitoring-metrics-types.html#event-source-mapping-metrics>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-metricsconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                metrics_config_property = lambda_mixins.CfnEventSourceMappingPropsMixin.MetricsConfigProperty(
                    metrics=["metrics"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__807b050bd95bb8a3d2051cfd59e3856e0099c147c0f81cc419be5d432f6c66f8)
                check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metrics is not None:
                self._values["metrics"] = metrics

        @builtins.property
        def metrics(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The metrics you want your event source mapping to produce.

            Include ``EventCount`` to receive event source mapping metrics related to the number of events processed by your event source mapping. For more information about these metrics, see `Event source mapping metrics <https://docs.aws.amazon.com/lambda/latest/dg/monitoring-metrics-types.html#event-source-mapping-metrics>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-metricsconfig.html#cfn-lambda-eventsourcemapping-metricsconfig-metrics
            '''
            result = self._values.get("metrics")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricsConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnEventSourceMappingPropsMixin.OnFailureProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination"},
    )
    class OnFailureProperty:
        def __init__(
            self,
            *,
            destination: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A destination for events that failed processing.

            For more information, see `Adding a destination <https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-retain-records.html#invocation-async-destinations>`_ .

            :param destination: The Amazon Resource Name (ARN) of the destination resource. To retain records of failed invocations from `Kinesis <https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html>`_ , `DynamoDB <https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html>`_ , `self-managed Apache Kafka <https://docs.aws.amazon.com/lambda/latest/dg/kafka-on-failure.html>`_ , or `Amazon MSK <https://docs.aws.amazon.com/lambda/latest/dg/kafka-on-failure.html>`_ , you can configure an Amazon SNS topic, Amazon SQS queue, Amazon S3 bucket, or Kafka topic as the destination. .. epigraph:: Amazon SNS destinations have a message size limit of 256 KB. If the combined size of the function request and response payload exceeds the limit, Lambda will drop the payload when sending ``OnFailure`` event to the destination. For details on this behavior, refer to `Retaining records of asynchronous invocations <https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-retain-records.html>`_ . To retain records of failed invocations from `Kinesis <https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html>`_ , `DynamoDB <https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html>`_ , `self-managed Kafka <https://docs.aws.amazon.com/lambda/latest/dg/with-kafka.html#services-smaa-onfailure-destination>`_ or `Amazon MSK <https://docs.aws.amazon.com/lambda/latest/dg/with-msk.html#services-msk-onfailure-destination>`_ , you can configure an Amazon SNS topic, Amazon SQS queue, or Amazon S3 bucket as the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-onfailure.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                on_failure_property = lambda_mixins.CfnEventSourceMappingPropsMixin.OnFailureProperty(
                    destination="destination"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a5ad5e62166acc899251c077195157e0445e8a9e95185476c1b2559086560c27)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination is not None:
                self._values["destination"] = destination

        @builtins.property
        def destination(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the destination resource.

            To retain records of failed invocations from `Kinesis <https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html>`_ , `DynamoDB <https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html>`_ , `self-managed Apache Kafka <https://docs.aws.amazon.com/lambda/latest/dg/kafka-on-failure.html>`_ , or `Amazon MSK <https://docs.aws.amazon.com/lambda/latest/dg/kafka-on-failure.html>`_ , you can configure an Amazon SNS topic, Amazon SQS queue, Amazon S3 bucket, or Kafka topic as the destination.
            .. epigraph::

               Amazon SNS destinations have a message size limit of 256 KB. If the combined size of the function request and response payload exceeds the limit, Lambda will drop the payload when sending ``OnFailure`` event to the destination. For details on this behavior, refer to `Retaining records of asynchronous invocations <https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-retain-records.html>`_ .

            To retain records of failed invocations from `Kinesis <https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html>`_ , `DynamoDB <https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html>`_ , `self-managed Kafka <https://docs.aws.amazon.com/lambda/latest/dg/with-kafka.html#services-smaa-onfailure-destination>`_ or `Amazon MSK <https://docs.aws.amazon.com/lambda/latest/dg/with-msk.html#services-msk-onfailure-destination>`_ , you can configure an Amazon SNS topic, Amazon SQS queue, or Amazon S3 bucket as the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-onfailure.html#cfn-lambda-eventsourcemapping-onfailure-destination
            '''
            result = self._values.get("destination")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnFailureProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnEventSourceMappingPropsMixin.ProvisionedPollerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "maximum_pollers": "maximumPollers",
            "minimum_pollers": "minimumPollers",
            "poller_group_name": "pollerGroupName",
        },
    )
    class ProvisionedPollerConfigProperty:
        def __init__(
            self,
            *,
            maximum_pollers: typing.Optional[jsii.Number] = None,
            minimum_pollers: typing.Optional[jsii.Number] = None,
            poller_group_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The `provisioned mode <https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html#invocation-eventsourcemapping-provisioned-mode>`_ configuration for the event source. Use Provisioned Mode to customize the minimum and maximum number of event pollers for your event source.

            :param maximum_pollers: The maximum number of event pollers this event source can scale up to. For Amazon SQS events source mappings, default is 200, and minimum value allowed is 2. For Amazon MSK and self-managed Apache Kafka event source mappings, default is 200, and minimum value allowed is 1.
            :param minimum_pollers: The minimum number of event pollers this event source can scale down to. For Amazon SQS events source mappings, default is 2, and minimum 2 required. For Amazon MSK and self-managed Apache Kafka event source mappings, default is 1.
            :param poller_group_name: (Amazon MSK and self-managed Apache Kafka) The name of the provisioned poller group. Use this option to group multiple ESMs within the event source's VPC to share Event Poller Unit (EPU) capacity. You can use this option to optimize Provisioned mode costs for your ESMs. You can group up to 100 ESMs per poller group and aggregate maximum pollers across all ESMs in a group cannot exceed 2000.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-provisionedpollerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                provisioned_poller_config_property = lambda_mixins.CfnEventSourceMappingPropsMixin.ProvisionedPollerConfigProperty(
                    maximum_pollers=123,
                    minimum_pollers=123,
                    poller_group_name="pollerGroupName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9e58a6cb75cbb156572c5e657332157f2b1465f0fd252ec59b8d9d8e48aebbd9)
                check_type(argname="argument maximum_pollers", value=maximum_pollers, expected_type=type_hints["maximum_pollers"])
                check_type(argname="argument minimum_pollers", value=minimum_pollers, expected_type=type_hints["minimum_pollers"])
                check_type(argname="argument poller_group_name", value=poller_group_name, expected_type=type_hints["poller_group_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if maximum_pollers is not None:
                self._values["maximum_pollers"] = maximum_pollers
            if minimum_pollers is not None:
                self._values["minimum_pollers"] = minimum_pollers
            if poller_group_name is not None:
                self._values["poller_group_name"] = poller_group_name

        @builtins.property
        def maximum_pollers(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of event pollers this event source can scale up to.

            For Amazon SQS events source mappings, default is 200, and minimum value allowed is 2. For Amazon MSK and self-managed Apache Kafka event source mappings, default is 200, and minimum value allowed is 1.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-provisionedpollerconfig.html#cfn-lambda-eventsourcemapping-provisionedpollerconfig-maximumpollers
            '''
            result = self._values.get("maximum_pollers")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def minimum_pollers(self) -> typing.Optional[jsii.Number]:
            '''The minimum number of event pollers this event source can scale down to.

            For Amazon SQS events source mappings, default is 2, and minimum 2 required. For Amazon MSK and self-managed Apache Kafka event source mappings, default is 1.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-provisionedpollerconfig.html#cfn-lambda-eventsourcemapping-provisionedpollerconfig-minimumpollers
            '''
            result = self._values.get("minimum_pollers")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def poller_group_name(self) -> typing.Optional[builtins.str]:
            '''(Amazon MSK and self-managed Apache Kafka) The name of the provisioned poller group.

            Use this option to group multiple ESMs within the event source's VPC to share Event Poller Unit (EPU) capacity. You can use this option to optimize Provisioned mode costs for your ESMs. You can group up to 100 ESMs per poller group and aggregate maximum pollers across all ESMs in a group cannot exceed 2000.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-provisionedpollerconfig.html#cfn-lambda-eventsourcemapping-provisionedpollerconfig-pollergroupname
            '''
            result = self._values.get("poller_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisionedPollerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnEventSourceMappingPropsMixin.ScalingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"maximum_concurrency": "maximumConcurrency"},
    )
    class ScalingConfigProperty:
        def __init__(
            self,
            *,
            maximum_concurrency: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''(Amazon SQS only) The scaling configuration for the event source.

            To remove the configuration, pass an empty value.

            :param maximum_concurrency: Limits the number of concurrent instances that the Amazon SQS event source can invoke.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-scalingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                scaling_config_property = lambda_mixins.CfnEventSourceMappingPropsMixin.ScalingConfigProperty(
                    maximum_concurrency=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ac85acb2e5b3a166ce34a555ed989e69abe4b882f9111b9394d2b1864f1a4c1b)
                check_type(argname="argument maximum_concurrency", value=maximum_concurrency, expected_type=type_hints["maximum_concurrency"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if maximum_concurrency is not None:
                self._values["maximum_concurrency"] = maximum_concurrency

        @builtins.property
        def maximum_concurrency(self) -> typing.Optional[jsii.Number]:
            '''Limits the number of concurrent instances that the Amazon SQS event source can invoke.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-scalingconfig.html#cfn-lambda-eventsourcemapping-scalingconfig-maximumconcurrency
            '''
            result = self._values.get("maximum_concurrency")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScalingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnEventSourceMappingPropsMixin.SchemaRegistryAccessConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "uri": "uri"},
    )
    class SchemaRegistryAccessConfigProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specific access configuration settings that tell Lambda how to authenticate with your schema registry.

            If you're working with an AWS Glue schema registry, don't provide authentication details in this object. Instead, ensure that your execution role has the required permissions for Lambda to access your cluster.

            If you're working with a Confluent schema registry, choose the authentication method in the ``Type`` field, and provide the AWS Secrets Manager secret ARN in the ``URI`` field.

            :param type: The type of authentication Lambda uses to access your schema registry.
            :param uri: The URI of the secret (Secrets Manager secret ARN) to authenticate with your schema registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-schemaregistryaccessconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                schema_registry_access_config_property = lambda_mixins.CfnEventSourceMappingPropsMixin.SchemaRegistryAccessConfigProperty(
                    type="type",
                    uri="uri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5ebcaec7601a7cb431284ce359eb8b28468c8d977bf335c622b8c013700040fd)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if uri is not None:
                self._values["uri"] = uri

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of authentication Lambda uses to access your schema registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-schemaregistryaccessconfig.html#cfn-lambda-eventsourcemapping-schemaregistryaccessconfig-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def uri(self) -> typing.Optional[builtins.str]:
            '''The URI of the secret (Secrets Manager secret ARN) to authenticate with your schema registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-schemaregistryaccessconfig.html#cfn-lambda-eventsourcemapping-schemaregistryaccessconfig-uri
            '''
            result = self._values.get("uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchemaRegistryAccessConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnEventSourceMappingPropsMixin.SchemaRegistryConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_configs": "accessConfigs",
            "event_record_format": "eventRecordFormat",
            "schema_registry_uri": "schemaRegistryUri",
            "schema_validation_configs": "schemaValidationConfigs",
        },
    )
    class SchemaRegistryConfigProperty:
        def __init__(
            self,
            *,
            access_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventSourceMappingPropsMixin.SchemaRegistryAccessConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            event_record_format: typing.Optional[builtins.str] = None,
            schema_registry_uri: typing.Optional[builtins.str] = None,
            schema_validation_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventSourceMappingPropsMixin.SchemaValidationConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specific configuration settings for a Kafka schema registry.

            :param access_configs: An array of access configuration objects that tell Lambda how to authenticate with your schema registry.
            :param event_record_format: The record format that Lambda delivers to your function after schema validation. - Choose ``JSON`` to have Lambda deliver the record to your function as a standard JSON object. - Choose ``SOURCE`` to have Lambda deliver the record to your function in its original source format. Lambda removes all schema metadata, such as the schema ID, before sending the record to your function.
            :param schema_registry_uri: The URI for your schema registry. The correct URI format depends on the type of schema registry you're using. - For AWS Glue schema registries, use the ARN of the registry. - For Confluent schema registries, use the URL of the registry.
            :param schema_validation_configs: An array of schema validation configuration objects, which tell Lambda the message attributes you want to validate and filter using your schema registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-schemaregistryconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                schema_registry_config_property = lambda_mixins.CfnEventSourceMappingPropsMixin.SchemaRegistryConfigProperty(
                    access_configs=[lambda_mixins.CfnEventSourceMappingPropsMixin.SchemaRegistryAccessConfigProperty(
                        type="type",
                        uri="uri"
                    )],
                    event_record_format="eventRecordFormat",
                    schema_registry_uri="schemaRegistryUri",
                    schema_validation_configs=[lambda_mixins.CfnEventSourceMappingPropsMixin.SchemaValidationConfigProperty(
                        attribute="attribute"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cb021f6f174dd6341a0a3a5acdbe47f57d0eee38f4990ad4c661e78547d3a613)
                check_type(argname="argument access_configs", value=access_configs, expected_type=type_hints["access_configs"])
                check_type(argname="argument event_record_format", value=event_record_format, expected_type=type_hints["event_record_format"])
                check_type(argname="argument schema_registry_uri", value=schema_registry_uri, expected_type=type_hints["schema_registry_uri"])
                check_type(argname="argument schema_validation_configs", value=schema_validation_configs, expected_type=type_hints["schema_validation_configs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_configs is not None:
                self._values["access_configs"] = access_configs
            if event_record_format is not None:
                self._values["event_record_format"] = event_record_format
            if schema_registry_uri is not None:
                self._values["schema_registry_uri"] = schema_registry_uri
            if schema_validation_configs is not None:
                self._values["schema_validation_configs"] = schema_validation_configs

        @builtins.property
        def access_configs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.SchemaRegistryAccessConfigProperty"]]]]:
            '''An array of access configuration objects that tell Lambda how to authenticate with your schema registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-schemaregistryconfig.html#cfn-lambda-eventsourcemapping-schemaregistryconfig-accessconfigs
            '''
            result = self._values.get("access_configs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.SchemaRegistryAccessConfigProperty"]]]], result)

        @builtins.property
        def event_record_format(self) -> typing.Optional[builtins.str]:
            '''The record format that Lambda delivers to your function after schema validation.

            - Choose ``JSON`` to have Lambda deliver the record to your function as a standard JSON object.
            - Choose ``SOURCE`` to have Lambda deliver the record to your function in its original source format. Lambda removes all schema metadata, such as the schema ID, before sending the record to your function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-schemaregistryconfig.html#cfn-lambda-eventsourcemapping-schemaregistryconfig-eventrecordformat
            '''
            result = self._values.get("event_record_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schema_registry_uri(self) -> typing.Optional[builtins.str]:
            '''The URI for your schema registry. The correct URI format depends on the type of schema registry you're using.

            - For AWS Glue schema registries, use the ARN of the registry.
            - For Confluent schema registries, use the URL of the registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-schemaregistryconfig.html#cfn-lambda-eventsourcemapping-schemaregistryconfig-schemaregistryuri
            '''
            result = self._values.get("schema_registry_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schema_validation_configs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.SchemaValidationConfigProperty"]]]]:
            '''An array of schema validation configuration objects, which tell Lambda the message attributes you want to validate and filter using your schema registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-schemaregistryconfig.html#cfn-lambda-eventsourcemapping-schemaregistryconfig-schemavalidationconfigs
            '''
            result = self._values.get("schema_validation_configs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.SchemaValidationConfigProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchemaRegistryConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnEventSourceMappingPropsMixin.SchemaValidationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"attribute": "attribute"},
    )
    class SchemaValidationConfigProperty:
        def __init__(self, *, attribute: typing.Optional[builtins.str] = None) -> None:
            '''Specific schema validation configuration settings that tell Lambda the message attributes you want to validate and filter using your schema registry.

            :param attribute: The attributes you want your schema registry to validate and filter for. If you selected ``JSON`` as the ``EventRecordFormat`` , Lambda also deserializes the selected message attributes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-schemavalidationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                schema_validation_config_property = lambda_mixins.CfnEventSourceMappingPropsMixin.SchemaValidationConfigProperty(
                    attribute="attribute"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a634722c1fdd087ea9f0825307404d17d3da0592da5c1aa187b000f6a7a77d28)
                check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute is not None:
                self._values["attribute"] = attribute

        @builtins.property
        def attribute(self) -> typing.Optional[builtins.str]:
            '''The attributes you want your schema registry to validate and filter for.

            If you selected ``JSON`` as the ``EventRecordFormat`` , Lambda also deserializes the selected message attributes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-schemavalidationconfig.html#cfn-lambda-eventsourcemapping-schemavalidationconfig-attribute
            '''
            result = self._values.get("attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchemaValidationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnEventSourceMappingPropsMixin.SelfManagedEventSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"endpoints": "endpoints"},
    )
    class SelfManagedEventSourceProperty:
        def __init__(
            self,
            *,
            endpoints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventSourceMappingPropsMixin.EndpointsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The self-managed Apache Kafka cluster for your event source.

            :param endpoints: The list of bootstrap servers for your Kafka brokers in the following format: ``"KafkaBootstrapServers": ["abc.xyz.com:xxxx","abc2.xyz.com:xxxx"]`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-selfmanagedeventsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                self_managed_event_source_property = lambda_mixins.CfnEventSourceMappingPropsMixin.SelfManagedEventSourceProperty(
                    endpoints=lambda_mixins.CfnEventSourceMappingPropsMixin.EndpointsProperty(
                        kafka_bootstrap_servers=["kafkaBootstrapServers"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f68ed610d8058095e7ee62c779e12192c33287d1ceeb6dad9c48ff84a170635b)
                check_type(argname="argument endpoints", value=endpoints, expected_type=type_hints["endpoints"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if endpoints is not None:
                self._values["endpoints"] = endpoints

        @builtins.property
        def endpoints(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.EndpointsProperty"]]:
            '''The list of bootstrap servers for your Kafka brokers in the following format: ``"KafkaBootstrapServers": ["abc.xyz.com:xxxx","abc2.xyz.com:xxxx"]`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-selfmanagedeventsource.html#cfn-lambda-eventsourcemapping-selfmanagedeventsource-endpoints
            '''
            result = self._values.get("endpoints")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.EndpointsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SelfManagedEventSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnEventSourceMappingPropsMixin.SelfManagedKafkaEventSourceConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "consumer_group_id": "consumerGroupId",
            "schema_registry_config": "schemaRegistryConfig",
        },
    )
    class SelfManagedKafkaEventSourceConfigProperty:
        def __init__(
            self,
            *,
            consumer_group_id: typing.Optional[builtins.str] = None,
            schema_registry_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventSourceMappingPropsMixin.SchemaRegistryConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specific configuration settings for a self-managed Apache Kafka event source.

            :param consumer_group_id: The identifier for the Kafka consumer group to join. The consumer group ID must be unique among all your Kafka event sources. After creating a Kafka event source mapping with the consumer group ID specified, you cannot update this value. For more information, see `Customizable consumer group ID <https://docs.aws.amazon.com/lambda/latest/dg/with-kafka-process.html#services-smaa-topic-add>`_ .
            :param schema_registry_config: Specific configuration settings for a Kafka schema registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-selfmanagedkafkaeventsourceconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                self_managed_kafka_event_source_config_property = lambda_mixins.CfnEventSourceMappingPropsMixin.SelfManagedKafkaEventSourceConfigProperty(
                    consumer_group_id="consumerGroupId",
                    schema_registry_config=lambda_mixins.CfnEventSourceMappingPropsMixin.SchemaRegistryConfigProperty(
                        access_configs=[lambda_mixins.CfnEventSourceMappingPropsMixin.SchemaRegistryAccessConfigProperty(
                            type="type",
                            uri="uri"
                        )],
                        event_record_format="eventRecordFormat",
                        schema_registry_uri="schemaRegistryUri",
                        schema_validation_configs=[lambda_mixins.CfnEventSourceMappingPropsMixin.SchemaValidationConfigProperty(
                            attribute="attribute"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7924f708028888eca5e1d5bc625bebc6ae6e7f3b0e8b491acbc4db9e77cc8800)
                check_type(argname="argument consumer_group_id", value=consumer_group_id, expected_type=type_hints["consumer_group_id"])
                check_type(argname="argument schema_registry_config", value=schema_registry_config, expected_type=type_hints["schema_registry_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if consumer_group_id is not None:
                self._values["consumer_group_id"] = consumer_group_id
            if schema_registry_config is not None:
                self._values["schema_registry_config"] = schema_registry_config

        @builtins.property
        def consumer_group_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the Kafka consumer group to join.

            The consumer group ID must be unique among all your Kafka event sources. After creating a Kafka event source mapping with the consumer group ID specified, you cannot update this value. For more information, see `Customizable consumer group ID <https://docs.aws.amazon.com/lambda/latest/dg/with-kafka-process.html#services-smaa-topic-add>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-selfmanagedkafkaeventsourceconfig.html#cfn-lambda-eventsourcemapping-selfmanagedkafkaeventsourceconfig-consumergroupid
            '''
            result = self._values.get("consumer_group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schema_registry_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.SchemaRegistryConfigProperty"]]:
            '''Specific configuration settings for a Kafka schema registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-selfmanagedkafkaeventsourceconfig.html#cfn-lambda-eventsourcemapping-selfmanagedkafkaeventsourceconfig-schemaregistryconfig
            '''
            result = self._values.get("schema_registry_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventSourceMappingPropsMixin.SchemaRegistryConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SelfManagedKafkaEventSourceConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnEventSourceMappingPropsMixin.SourceAccessConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "uri": "uri"},
    )
    class SourceAccessConfigurationProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An array of the authentication protocol, VPC components, or virtual host to secure and define your event source.

            :param type: The type of authentication protocol, VPC components, or virtual host for your event source. For example: ``"Type":"SASL_SCRAM_512_AUTH"`` . - ``BASIC_AUTH`` – (Amazon MQ) The AWS Secrets Manager secret that stores your broker credentials. - ``BASIC_AUTH`` – (Self-managed Apache Kafka) The Secrets Manager ARN of your secret key used for SASL/PLAIN authentication of your Apache Kafka brokers. - ``VPC_SUBNET`` – (Self-managed Apache Kafka) The subnets associated with your VPC. Lambda connects to these subnets to fetch data from your self-managed Apache Kafka cluster. - ``VPC_SECURITY_GROUP`` – (Self-managed Apache Kafka) The VPC security group used to manage access to your self-managed Apache Kafka brokers. - ``SASL_SCRAM_256_AUTH`` – (Self-managed Apache Kafka) The Secrets Manager ARN of your secret key used for SASL SCRAM-256 authentication of your self-managed Apache Kafka brokers. - ``SASL_SCRAM_512_AUTH`` – (Amazon MSK, Self-managed Apache Kafka) The Secrets Manager ARN of your secret key used for SASL SCRAM-512 authentication of your self-managed Apache Kafka brokers. - ``VIRTUAL_HOST`` –- (RabbitMQ) The name of the virtual host in your RabbitMQ broker. Lambda uses this RabbitMQ host as the event source. This property cannot be specified in an UpdateEventSourceMapping API call. - ``CLIENT_CERTIFICATE_TLS_AUTH`` – (Amazon MSK, self-managed Apache Kafka) The Secrets Manager ARN of your secret key containing the certificate chain (X.509 PEM), private key (PKCS#8 PEM), and private key password (optional) used for mutual TLS authentication of your MSK/Apache Kafka brokers. - ``SERVER_ROOT_CA_CERTIFICATE`` – (Self-managed Apache Kafka) The Secrets Manager ARN of your secret key containing the root CA certificate (X.509 PEM) used for TLS encryption of your Apache Kafka brokers.
            :param uri: The value for your chosen configuration in ``Type`` . For example: ``"URI": "arn:aws:secretsmanager:us-east-1:01234567890:secret:MyBrokerSecretName"`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-sourceaccessconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                source_access_configuration_property = lambda_mixins.CfnEventSourceMappingPropsMixin.SourceAccessConfigurationProperty(
                    type="type",
                    uri="uri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8a43dde8d7736ff862142afb31a03bcb960256fc5ac1dc29552eabf9ab79cd1c)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if uri is not None:
                self._values["uri"] = uri

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of authentication protocol, VPC components, or virtual host for your event source. For example: ``"Type":"SASL_SCRAM_512_AUTH"`` .

            - ``BASIC_AUTH`` – (Amazon MQ) The AWS Secrets Manager secret that stores your broker credentials.
            - ``BASIC_AUTH`` – (Self-managed Apache Kafka) The Secrets Manager ARN of your secret key used for SASL/PLAIN authentication of your Apache Kafka brokers.
            - ``VPC_SUBNET`` – (Self-managed Apache Kafka) The subnets associated with your VPC. Lambda connects to these subnets to fetch data from your self-managed Apache Kafka cluster.
            - ``VPC_SECURITY_GROUP`` – (Self-managed Apache Kafka) The VPC security group used to manage access to your self-managed Apache Kafka brokers.
            - ``SASL_SCRAM_256_AUTH`` – (Self-managed Apache Kafka) The Secrets Manager ARN of your secret key used for SASL SCRAM-256 authentication of your self-managed Apache Kafka brokers.
            - ``SASL_SCRAM_512_AUTH`` – (Amazon MSK, Self-managed Apache Kafka) The Secrets Manager ARN of your secret key used for SASL SCRAM-512 authentication of your self-managed Apache Kafka brokers.
            - ``VIRTUAL_HOST`` –- (RabbitMQ) The name of the virtual host in your RabbitMQ broker. Lambda uses this RabbitMQ host as the event source. This property cannot be specified in an UpdateEventSourceMapping API call.
            - ``CLIENT_CERTIFICATE_TLS_AUTH`` – (Amazon MSK, self-managed Apache Kafka) The Secrets Manager ARN of your secret key containing the certificate chain (X.509 PEM), private key (PKCS#8 PEM), and private key password (optional) used for mutual TLS authentication of your MSK/Apache Kafka brokers.
            - ``SERVER_ROOT_CA_CERTIFICATE`` – (Self-managed Apache Kafka) The Secrets Manager ARN of your secret key containing the root CA certificate (X.509 PEM) used for TLS encryption of your Apache Kafka brokers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-sourceaccessconfiguration.html#cfn-lambda-eventsourcemapping-sourceaccessconfiguration-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def uri(self) -> typing.Optional[builtins.str]:
            '''The value for your chosen configuration in ``Type`` .

            For example: ``"URI": "arn:aws:secretsmanager:us-east-1:01234567890:secret:MyBrokerSecretName"`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-sourceaccessconfiguration.html#cfn-lambda-eventsourcemapping-sourceaccessconfiguration-uri
            '''
            result = self._values.get("uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceAccessConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnFunctionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "architectures": "architectures",
        "capacity_provider_config": "capacityProviderConfig",
        "code": "code",
        "code_signing_config_arn": "codeSigningConfigArn",
        "dead_letter_config": "deadLetterConfig",
        "description": "description",
        "durable_config": "durableConfig",
        "environment": "environment",
        "ephemeral_storage": "ephemeralStorage",
        "file_system_configs": "fileSystemConfigs",
        "function_name": "functionName",
        "function_scaling_config": "functionScalingConfig",
        "handler": "handler",
        "image_config": "imageConfig",
        "kms_key_arn": "kmsKeyArn",
        "layers": "layers",
        "logging_config": "loggingConfig",
        "memory_size": "memorySize",
        "package_type": "packageType",
        "publish_to_latest_published": "publishToLatestPublished",
        "recursive_loop": "recursiveLoop",
        "reserved_concurrent_executions": "reservedConcurrentExecutions",
        "role": "role",
        "runtime": "runtime",
        "runtime_management_config": "runtimeManagementConfig",
        "snap_start": "snapStart",
        "tags": "tags",
        "tenancy_config": "tenancyConfig",
        "timeout": "timeout",
        "tracing_config": "tracingConfig",
        "vpc_config": "vpcConfig",
    },
)
class CfnFunctionMixinProps:
    def __init__(
        self,
        *,
        architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
        capacity_provider_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.CapacityProviderConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        code: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.CodeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        code_signing_config_arn: typing.Optional[builtins.str] = None,
        dead_letter_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.DeadLetterConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        durable_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.DurableConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        environment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.EnvironmentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ephemeral_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.EphemeralStorageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        file_system_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.FileSystemConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        function_name: typing.Optional[builtins.str] = None,
        function_scaling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.FunctionScalingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        handler: typing.Optional[builtins.str] = None,
        image_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.ImageConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        layers: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.LoggingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        package_type: typing.Optional[builtins.str] = None,
        publish_to_latest_published: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        recursive_loop: typing.Optional[builtins.str] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[builtins.str] = None,
        runtime_management_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.RuntimeManagementConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        snap_start: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.SnapStartProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        tenancy_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.TenancyConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        tracing_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.TracingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.VpcConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnFunctionPropsMixin.

        :param architectures: The instruction set architecture that the function supports. Enter a string array with one of the valid values (arm64 or x86_64). The default value is ``x86_64`` .
        :param capacity_provider_config: 
        :param code: The code for the function. You can define your function code in multiple ways:. - For .zip deployment packages, you can specify the Amazon S3 location of the .zip file in the ``S3Bucket`` , ``S3Key`` , and ``S3ObjectVersion`` properties. - For .zip deployment packages, you can alternatively define the function code inline in the ``ZipFile`` property. This method works only for Node.js and Python functions. - For container images, specify the URI of your container image in the Amazon ECR registry in the ``ImageUri`` property.
        :param code_signing_config_arn: To enable code signing for this function, specify the ARN of a code-signing configuration. A code-signing configuration includes a set of signing profiles, which define the trusted publishers for this function.
        :param dead_letter_config: A dead-letter queue configuration that specifies the queue or topic where Lambda sends asynchronous events when they fail processing. For more information, see `Dead-letter queues <https://docs.aws.amazon.com/lambda/latest/dg/invocation-async.html#invocation-dlq>`_ .
        :param description: A description of the function.
        :param durable_config: 
        :param environment: Environment variables that are accessible from function code during execution.
        :param ephemeral_storage: The size of the function's ``/tmp`` directory in MB. The default value is 512, but it can be any whole number between 512 and 10,240 MB.
        :param file_system_configs: Connection settings for an Amazon EFS file system. To connect a function to a file system, a mount target must be available in every Availability Zone that your function connects to. If your template contains an `AWS::EFS::MountTarget <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html>`_ resource, you must also specify a ``DependsOn`` attribute to ensure that the mount target is created or updated before the function. For more information about using the ``DependsOn`` attribute, see `DependsOn Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ .
        :param function_name: The name of the Lambda function, up to 64 characters in length. If you don't specify a name, CloudFormation generates one. If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param function_scaling_config: 
        :param handler: The name of the method within your code that Lambda calls to run your function. Handler is required if the deployment package is a .zip file archive. The format includes the file name. It can also include namespaces and other qualifiers, depending on the runtime. For more information, see `Lambda programming model <https://docs.aws.amazon.com/lambda/latest/dg/foundation-progmodel.html>`_ .
        :param image_config: Configuration values that override the container image Dockerfile settings. For more information, see `Container image settings <https://docs.aws.amazon.com/lambda/latest/dg/images-create.html#images-parms>`_ .
        :param kms_key_arn: The ARN of the AWS Key Management Service ( AWS ) customer managed key that's used to encrypt the following resources:. - The function's `environment variables <https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html#configuration-envvars-encryption>`_ . - The function's `Lambda SnapStart <https://docs.aws.amazon.com/lambda/latest/dg/snapstart-security.html>`_ snapshots. - When used with ``SourceKMSKeyArn`` , the unzipped version of the .zip deployment package that's used for function invocations. For more information, see `Specifying a customer managed key for Lambda <https://docs.aws.amazon.com/lambda/latest/dg/encrypt-zip-package.html#enable-zip-custom-encryption>`_ . - The optimized version of the container image that's used for function invocations. Note that this is not the same key that's used to protect your container image in the Amazon Elastic Container Registry (Amazon ECR). For more information, see `Function lifecycle <https://docs.aws.amazon.com/lambda/latest/dg/images-create.html#images-lifecycle>`_ . If you don't provide a customer managed key, Lambda uses an `AWS owned key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-owned-cmk>`_ or an `AWS managed key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-managed-cmk>`_ .
        :param layers: A list of `function layers <https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html>`_ to add to the function's execution environment. Specify each layer by its ARN, including the version.
        :param logging_config: The function's Amazon CloudWatch Logs configuration settings.
        :param memory_size: The amount of `memory available to the function <https://docs.aws.amazon.com/lambda/latest/dg/configuration-function-common.html#configuration-memory-console>`_ at runtime. Increasing the function memory also increases its CPU allocation. The default value is 128 MB. The value can be any multiple of 1 MB. Note that new AWS accounts have reduced concurrency and memory quotas. AWS raises these quotas automatically based on your usage. You can also request a quota increase.
        :param package_type: The type of deployment package. Set to ``Image`` for container image and set ``Zip`` for .zip file archive.
        :param publish_to_latest_published: 
        :param recursive_loop: The status of your function's recursive loop detection configuration. When this value is set to ``Allow`` and Lambda detects your function being invoked as part of a recursive loop, it doesn't take any action. When this value is set to ``Terminate`` and Lambda detects your function being invoked as part of a recursive loop, it stops your function being invoked and notifies you.
        :param reserved_concurrent_executions: The number of simultaneous executions to reserve for the function.
        :param role: The Amazon Resource Name (ARN) of the function's execution role.
        :param runtime: The identifier of the function's `runtime <https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html>`_ . Runtime is required if the deployment package is a .zip file archive. Specifying a runtime results in an error if you're deploying a function using a container image. The following list includes deprecated runtimes. Lambda blocks creating new functions and updating existing functions shortly after each runtime is deprecated. For more information, see `Runtime use after deprecation <https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html#runtime-deprecation-levels>`_ . For a list of all currently supported runtimes, see `Supported runtimes <https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html#runtimes-supported>`_ .
        :param runtime_management_config: Sets the runtime management configuration for a function's version. For more information, see `Runtime updates <https://docs.aws.amazon.com/lambda/latest/dg/runtimes-update.html>`_ .
        :param snap_start: The function's `AWS Lambda SnapStart <https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html>`_ setting.
        :param tags: A list of `tags <https://docs.aws.amazon.com/lambda/latest/dg/tagging.html>`_ to apply to the function. .. epigraph:: You must have the ``lambda:TagResource`` , ``lambda:UntagResource`` , and ``lambda:ListTags`` permissions for your `IAM principal <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html>`_ to manage the CloudFormation stack. If you don't have these permissions, there might be unexpected behavior with stack-level tags propagating to the resource during resource creation and update.
        :param tenancy_config: The function's tenant isolation configuration settings. Determines whether the Lambda function runs on a shared or dedicated infrastructure per unique tenant.
        :param timeout: The amount of time (in seconds) that Lambda allows a function to run before stopping it. The default is 3 seconds. The maximum allowed value is 900 seconds. For more information, see `Lambda execution environment <https://docs.aws.amazon.com/lambda/latest/dg/runtimes-context.html>`_ .
        :param tracing_config: Set ``Mode`` to ``Active`` to sample and trace a subset of incoming requests with `X-Ray <https://docs.aws.amazon.com/lambda/latest/dg/services-xray.html>`_ .
        :param vpc_config: For network connectivity to AWS resources in a VPC, specify a list of security groups and subnets in the VPC. When you connect a function to a VPC, it can access resources and the internet only through that VPC. For more information, see `Configuring a Lambda function to access resources in a VPC <https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
            
            cfn_function_mixin_props = lambda_mixins.CfnFunctionMixinProps(
                architectures=["architectures"],
                capacity_provider_config=lambda_mixins.CfnFunctionPropsMixin.CapacityProviderConfigProperty(
                    lambda_managed_instances_capacity_provider_config=lambda_mixins.CfnFunctionPropsMixin.LambdaManagedInstancesCapacityProviderConfigProperty(
                        capacity_provider_arn="capacityProviderArn",
                        execution_environment_memory_gi_bPer_vCpu=123,
                        per_execution_environment_max_concurrency=123
                    )
                ),
                code=lambda_mixins.CfnFunctionPropsMixin.CodeProperty(
                    image_uri="imageUri",
                    s3_bucket="s3Bucket",
                    s3_key="s3Key",
                    s3_object_version="s3ObjectVersion",
                    source_kms_key_arn="sourceKmsKeyArn",
                    zip_file="zipFile"
                ),
                code_signing_config_arn="codeSigningConfigArn",
                dead_letter_config=lambda_mixins.CfnFunctionPropsMixin.DeadLetterConfigProperty(
                    target_arn="targetArn"
                ),
                description="description",
                durable_config=lambda_mixins.CfnFunctionPropsMixin.DurableConfigProperty(
                    execution_timeout=123,
                    retention_period_in_days=123
                ),
                environment=lambda_mixins.CfnFunctionPropsMixin.EnvironmentProperty(
                    variables={
                        "variables_key": "variables"
                    }
                ),
                ephemeral_storage=lambda_mixins.CfnFunctionPropsMixin.EphemeralStorageProperty(
                    size=123
                ),
                file_system_configs=[lambda_mixins.CfnFunctionPropsMixin.FileSystemConfigProperty(
                    arn="arn",
                    local_mount_path="localMountPath"
                )],
                function_name="functionName",
                function_scaling_config=lambda_mixins.CfnFunctionPropsMixin.FunctionScalingConfigProperty(
                    max_execution_environments=123,
                    min_execution_environments=123
                ),
                handler="handler",
                image_config=lambda_mixins.CfnFunctionPropsMixin.ImageConfigProperty(
                    command=["command"],
                    entry_point=["entryPoint"],
                    working_directory="workingDirectory"
                ),
                kms_key_arn="kmsKeyArn",
                layers=["layers"],
                logging_config=lambda_mixins.CfnFunctionPropsMixin.LoggingConfigProperty(
                    application_log_level="applicationLogLevel",
                    log_format="logFormat",
                    log_group="logGroup",
                    system_log_level="systemLogLevel"
                ),
                memory_size=123,
                package_type="packageType",
                publish_to_latest_published=False,
                recursive_loop="recursiveLoop",
                reserved_concurrent_executions=123,
                role="role",
                runtime="runtime",
                runtime_management_config=lambda_mixins.CfnFunctionPropsMixin.RuntimeManagementConfigProperty(
                    runtime_version_arn="runtimeVersionArn",
                    update_runtime_on="updateRuntimeOn"
                ),
                snap_start=lambda_mixins.CfnFunctionPropsMixin.SnapStartProperty(
                    apply_on="applyOn"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                tenancy_config=lambda_mixins.CfnFunctionPropsMixin.TenancyConfigProperty(
                    tenant_isolation_mode="tenantIsolationMode"
                ),
                timeout=123,
                tracing_config=lambda_mixins.CfnFunctionPropsMixin.TracingConfigProperty(
                    mode="mode"
                ),
                vpc_config=lambda_mixins.CfnFunctionPropsMixin.VpcConfigProperty(
                    ipv6_allowed_for_dual_stack=False,
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0081ae7cb2352db284c15bdfee27f535eb56cc8272589b1aa67dce99dce5fe4)
            check_type(argname="argument architectures", value=architectures, expected_type=type_hints["architectures"])
            check_type(argname="argument capacity_provider_config", value=capacity_provider_config, expected_type=type_hints["capacity_provider_config"])
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument code_signing_config_arn", value=code_signing_config_arn, expected_type=type_hints["code_signing_config_arn"])
            check_type(argname="argument dead_letter_config", value=dead_letter_config, expected_type=type_hints["dead_letter_config"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument durable_config", value=durable_config, expected_type=type_hints["durable_config"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument ephemeral_storage", value=ephemeral_storage, expected_type=type_hints["ephemeral_storage"])
            check_type(argname="argument file_system_configs", value=file_system_configs, expected_type=type_hints["file_system_configs"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument function_scaling_config", value=function_scaling_config, expected_type=type_hints["function_scaling_config"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument image_config", value=image_config, expected_type=type_hints["image_config"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument layers", value=layers, expected_type=type_hints["layers"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument memory_size", value=memory_size, expected_type=type_hints["memory_size"])
            check_type(argname="argument package_type", value=package_type, expected_type=type_hints["package_type"])
            check_type(argname="argument publish_to_latest_published", value=publish_to_latest_published, expected_type=type_hints["publish_to_latest_published"])
            check_type(argname="argument recursive_loop", value=recursive_loop, expected_type=type_hints["recursive_loop"])
            check_type(argname="argument reserved_concurrent_executions", value=reserved_concurrent_executions, expected_type=type_hints["reserved_concurrent_executions"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument runtime_management_config", value=runtime_management_config, expected_type=type_hints["runtime_management_config"])
            check_type(argname="argument snap_start", value=snap_start, expected_type=type_hints["snap_start"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tenancy_config", value=tenancy_config, expected_type=type_hints["tenancy_config"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument tracing_config", value=tracing_config, expected_type=type_hints["tracing_config"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if architectures is not None:
            self._values["architectures"] = architectures
        if capacity_provider_config is not None:
            self._values["capacity_provider_config"] = capacity_provider_config
        if code is not None:
            self._values["code"] = code
        if code_signing_config_arn is not None:
            self._values["code_signing_config_arn"] = code_signing_config_arn
        if dead_letter_config is not None:
            self._values["dead_letter_config"] = dead_letter_config
        if description is not None:
            self._values["description"] = description
        if durable_config is not None:
            self._values["durable_config"] = durable_config
        if environment is not None:
            self._values["environment"] = environment
        if ephemeral_storage is not None:
            self._values["ephemeral_storage"] = ephemeral_storage
        if file_system_configs is not None:
            self._values["file_system_configs"] = file_system_configs
        if function_name is not None:
            self._values["function_name"] = function_name
        if function_scaling_config is not None:
            self._values["function_scaling_config"] = function_scaling_config
        if handler is not None:
            self._values["handler"] = handler
        if image_config is not None:
            self._values["image_config"] = image_config
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if layers is not None:
            self._values["layers"] = layers
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if memory_size is not None:
            self._values["memory_size"] = memory_size
        if package_type is not None:
            self._values["package_type"] = package_type
        if publish_to_latest_published is not None:
            self._values["publish_to_latest_published"] = publish_to_latest_published
        if recursive_loop is not None:
            self._values["recursive_loop"] = recursive_loop
        if reserved_concurrent_executions is not None:
            self._values["reserved_concurrent_executions"] = reserved_concurrent_executions
        if role is not None:
            self._values["role"] = role
        if runtime is not None:
            self._values["runtime"] = runtime
        if runtime_management_config is not None:
            self._values["runtime_management_config"] = runtime_management_config
        if snap_start is not None:
            self._values["snap_start"] = snap_start
        if tags is not None:
            self._values["tags"] = tags
        if tenancy_config is not None:
            self._values["tenancy_config"] = tenancy_config
        if timeout is not None:
            self._values["timeout"] = timeout
        if tracing_config is not None:
            self._values["tracing_config"] = tracing_config
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def architectures(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The instruction set architecture that the function supports.

        Enter a string array with one of the valid values (arm64 or x86_64). The default value is ``x86_64`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-architectures
        '''
        result = self._values.get("architectures")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def capacity_provider_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.CapacityProviderConfigProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-capacityproviderconfig
        '''
        result = self._values.get("capacity_provider_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.CapacityProviderConfigProperty"]], result)

    @builtins.property
    def code(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.CodeProperty"]]:
        '''The code for the function. You can define your function code in multiple ways:.

        - For .zip deployment packages, you can specify the Amazon S3 location of the .zip file in the ``S3Bucket`` , ``S3Key`` , and ``S3ObjectVersion`` properties.
        - For .zip deployment packages, you can alternatively define the function code inline in the ``ZipFile`` property. This method works only for Node.js and Python functions.
        - For container images, specify the URI of your container image in the Amazon ECR registry in the ``ImageUri`` property.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-code
        '''
        result = self._values.get("code")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.CodeProperty"]], result)

    @builtins.property
    def code_signing_config_arn(self) -> typing.Optional[builtins.str]:
        '''To enable code signing for this function, specify the ARN of a code-signing configuration.

        A code-signing configuration
        includes a set of signing profiles, which define the trusted publishers for this function.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-codesigningconfigarn
        '''
        result = self._values.get("code_signing_config_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dead_letter_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.DeadLetterConfigProperty"]]:
        '''A dead-letter queue configuration that specifies the queue or topic where Lambda sends asynchronous events when they fail processing.

        For more information, see `Dead-letter queues <https://docs.aws.amazon.com/lambda/latest/dg/invocation-async.html#invocation-dlq>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-deadletterconfig
        '''
        result = self._values.get("dead_letter_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.DeadLetterConfigProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the function.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def durable_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.DurableConfigProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-durableconfig
        '''
        result = self._values.get("durable_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.DurableConfigProperty"]], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EnvironmentProperty"]]:
        '''Environment variables that are accessible from function code during execution.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-environment
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EnvironmentProperty"]], result)

    @builtins.property
    def ephemeral_storage(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EphemeralStorageProperty"]]:
        '''The size of the function's ``/tmp`` directory in MB.

        The default value is 512, but it can be any whole number between 512 and 10,240 MB.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-ephemeralstorage
        '''
        result = self._values.get("ephemeral_storage")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.EphemeralStorageProperty"]], result)

    @builtins.property
    def file_system_configs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.FileSystemConfigProperty"]]]]:
        '''Connection settings for an Amazon EFS file system.

        To connect a function to a file system, a mount target must be available in every Availability Zone that your function connects to. If your template contains an `AWS::EFS::MountTarget <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html>`_ resource, you must also specify a ``DependsOn`` attribute to ensure that the mount target is created or updated before the function.

        For more information about using the ``DependsOn`` attribute, see `DependsOn Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-filesystemconfigs
        '''
        result = self._values.get("file_system_configs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.FileSystemConfigProperty"]]]], result)

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Lambda function, up to 64 characters in length.

        If you don't specify a name, CloudFormation generates one.

        If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-functionname
        '''
        result = self._values.get("function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def function_scaling_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.FunctionScalingConfigProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-functionscalingconfig
        '''
        result = self._values.get("function_scaling_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.FunctionScalingConfigProperty"]], result)

    @builtins.property
    def handler(self) -> typing.Optional[builtins.str]:
        '''The name of the method within your code that Lambda calls to run your function.

        Handler is required if the deployment package is a .zip file archive. The format includes the file name. It can also include namespaces and other qualifiers, depending on the runtime. For more information, see `Lambda programming model <https://docs.aws.amazon.com/lambda/latest/dg/foundation-progmodel.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-handler
        '''
        result = self._values.get("handler")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.ImageConfigProperty"]]:
        '''Configuration values that override the container image Dockerfile settings.

        For more information, see `Container image settings <https://docs.aws.amazon.com/lambda/latest/dg/images-create.html#images-parms>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-imageconfig
        '''
        result = self._values.get("image_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.ImageConfigProperty"]], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the AWS Key Management Service ( AWS  ) customer managed key that's used to encrypt the following resources:.

        - The function's `environment variables <https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html#configuration-envvars-encryption>`_ .
        - The function's `Lambda SnapStart <https://docs.aws.amazon.com/lambda/latest/dg/snapstart-security.html>`_ snapshots.
        - When used with ``SourceKMSKeyArn`` , the unzipped version of the .zip deployment package that's used for function invocations. For more information, see `Specifying a customer managed key for Lambda <https://docs.aws.amazon.com/lambda/latest/dg/encrypt-zip-package.html#enable-zip-custom-encryption>`_ .
        - The optimized version of the container image that's used for function invocations. Note that this is not the same key that's used to protect your container image in the Amazon Elastic Container Registry (Amazon ECR). For more information, see `Function lifecycle <https://docs.aws.amazon.com/lambda/latest/dg/images-create.html#images-lifecycle>`_ .

        If you don't provide a customer managed key, Lambda uses an `AWS owned key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-owned-cmk>`_ or an `AWS managed key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-managed-cmk>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-kmskeyarn
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def layers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of `function layers <https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html>`_ to add to the function's execution environment. Specify each layer by its ARN, including the version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-layers
        '''
        result = self._values.get("layers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.LoggingConfigProperty"]]:
        '''The function's Amazon CloudWatch Logs configuration settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-loggingconfig
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.LoggingConfigProperty"]], result)

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        '''The amount of `memory available to the function <https://docs.aws.amazon.com/lambda/latest/dg/configuration-function-common.html#configuration-memory-console>`_ at runtime. Increasing the function memory also increases its CPU allocation. The default value is 128 MB. The value can be any multiple of 1 MB. Note that new AWS accounts have reduced concurrency and memory quotas. AWS raises these quotas automatically based on your usage. You can also request a quota increase.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-memorysize
        '''
        result = self._values.get("memory_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def package_type(self) -> typing.Optional[builtins.str]:
        '''The type of deployment package.

        Set to ``Image`` for container image and set ``Zip`` for .zip file archive.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-packagetype
        '''
        result = self._values.get("package_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publish_to_latest_published(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-publishtolatestpublished
        '''
        result = self._values.get("publish_to_latest_published")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def recursive_loop(self) -> typing.Optional[builtins.str]:
        '''The status of your function's recursive loop detection configuration.

        When this value is set to ``Allow`` and Lambda detects your function being invoked as part of a recursive loop, it doesn't take any action.

        When this value is set to ``Terminate`` and Lambda detects your function being invoked as part of a recursive loop, it stops your function being invoked and notifies you.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-recursiveloop
        '''
        result = self._values.get("recursive_loop")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reserved_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        '''The number of simultaneous executions to reserve for the function.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-reservedconcurrentexecutions
        '''
        result = self._values.get("reserved_concurrent_executions")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the function's execution role.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-role
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime(self) -> typing.Optional[builtins.str]:
        '''The identifier of the function's `runtime <https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html>`_ . Runtime is required if the deployment package is a .zip file archive. Specifying a runtime results in an error if you're deploying a function using a container image.

        The following list includes deprecated runtimes. Lambda blocks creating new functions and updating existing functions shortly after each runtime is deprecated. For more information, see `Runtime use after deprecation <https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html#runtime-deprecation-levels>`_ .

        For a list of all currently supported runtimes, see `Supported runtimes <https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html#runtimes-supported>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-runtime
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_management_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.RuntimeManagementConfigProperty"]]:
        '''Sets the runtime management configuration for a function's version.

        For more information, see `Runtime updates <https://docs.aws.amazon.com/lambda/latest/dg/runtimes-update.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-runtimemanagementconfig
        '''
        result = self._values.get("runtime_management_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.RuntimeManagementConfigProperty"]], result)

    @builtins.property
    def snap_start(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.SnapStartProperty"]]:
        '''The function's `AWS Lambda SnapStart <https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html>`_ setting.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-snapstart
        '''
        result = self._values.get("snap_start")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.SnapStartProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of `tags <https://docs.aws.amazon.com/lambda/latest/dg/tagging.html>`_ to apply to the function.

        .. epigraph::

           You must have the ``lambda:TagResource`` , ``lambda:UntagResource`` , and ``lambda:ListTags`` permissions for your `IAM principal <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html>`_ to manage the CloudFormation stack. If you don't have these permissions, there might be unexpected behavior with stack-level tags propagating to the resource during resource creation and update.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def tenancy_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.TenancyConfigProperty"]]:
        '''The function's tenant isolation configuration settings.

        Determines whether the Lambda function runs on a shared or dedicated infrastructure per unique tenant.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-tenancyconfig
        '''
        result = self._values.get("tenancy_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.TenancyConfigProperty"]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''The amount of time (in seconds) that Lambda allows a function to run before stopping it.

        The default is 3 seconds. The maximum allowed value is 900 seconds. For more information, see `Lambda execution environment <https://docs.aws.amazon.com/lambda/latest/dg/runtimes-context.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-timeout
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tracing_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.TracingConfigProperty"]]:
        '''Set ``Mode`` to ``Active`` to sample and trace a subset of incoming requests with `X-Ray <https://docs.aws.amazon.com/lambda/latest/dg/services-xray.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-tracingconfig
        '''
        result = self._values.get("tracing_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.TracingConfigProperty"]], result)

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.VpcConfigProperty"]]:
        '''For network connectivity to AWS resources in a VPC, specify a list of security groups and subnets in the VPC.

        When you connect a function to a VPC, it can access resources and the internet only through that VPC. For more information, see `Configuring a Lambda function to access resources in a VPC <https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-vpcconfig
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
    jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnFunctionPropsMixin",
):
    '''The ``AWS::Lambda::Function`` resource creates a Lambda function.

    To create a function, you need a `deployment package <https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-package.html>`_ and an `execution role <https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html>`_ . The deployment package is a .zip file archive or container image that contains your function code. The execution role grants the function permission to use AWS services, such as Amazon CloudWatch Logs for log streaming and AWS X-Ray for request tracing.

    You set the package type to ``Image`` if the deployment package is a `container image <https://docs.aws.amazon.com/lambda/latest/dg/lambda-images.html>`_ . For these functions, include the URI of the container image in the Amazon ECR registry in the ```ImageUri`` property of the ``Code`` property <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html#cfn-lambda-function-code-imageuri>`_ . You do not need to specify the handler and runtime properties.

    You set the package type to ``Zip`` if the deployment package is a `.zip file archive <https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-package.html#gettingstarted-package-zip>`_ . For these functions, specify the Amazon S3 location of your .zip file in the ``Code`` property. Alternatively, for Node.js and Python functions, you can define your function inline in the ```ZipFile`` property of the ``Code`` property <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html#cfn-lambda-function-code-zipfile>`_ . In both cases, you must also specify the handler and runtime properties.

    You can use `code signing <https://docs.aws.amazon.com/lambda/latest/dg/configuration-codesigning.html>`_ if your deployment package is a .zip file archive. To enable code signing for this function, specify the ARN of a code-signing configuration. When a user attempts to deploy a code package with ``UpdateFunctionCode`` , Lambda checks that the code package has a valid signature from a trusted publisher. The code-signing configuration includes a set of signing profiles, which define the trusted publishers for this function.

    When you update a ``AWS::Lambda::Function`` resource, CloudFormation calls the `UpdateFunctionConfiguration <https://docs.aws.amazon.com/lambda/latest/api/API_UpdateFunctionConfiguration.html>`_ and `UpdateFunctionCode <https://docs.aws.amazon.com/lambda/latest/api/API_UpdateFunctionCode.html>`_ Lambda APIs under the hood. Because these calls happen sequentially, and invocations can happen between these calls, your function may encounter errors in the time between the calls. For example, if you remove an environment variable, and the code that references that environment variable in the same CloudFormation update, you may see invocation errors related to a missing environment variable. To work around this, you can invoke your function against a version or alias by default, rather than the ``$LATEST`` version.

    Note that you configure `provisioned concurrency <https://docs.aws.amazon.com/lambda/latest/dg/provisioned-concurrency.html>`_ on a ``AWS::Lambda::Version`` or a ``AWS::Lambda::Alias`` .

    For a complete introduction to Lambda functions, see `What is Lambda? <https://docs.aws.amazon.com/lambda/latest/dg/lambda-welcome.html>`_ in the *Lambda developer guide.*

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html
    :cloudformationResource: AWS::Lambda::Function
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
        
        cfn_function_props_mixin = lambda_mixins.CfnFunctionPropsMixin(lambda_mixins.CfnFunctionMixinProps(
            architectures=["architectures"],
            capacity_provider_config=lambda_mixins.CfnFunctionPropsMixin.CapacityProviderConfigProperty(
                lambda_managed_instances_capacity_provider_config=lambda_mixins.CfnFunctionPropsMixin.LambdaManagedInstancesCapacityProviderConfigProperty(
                    capacity_provider_arn="capacityProviderArn",
                    execution_environment_memory_gi_bPer_vCpu=123,
                    per_execution_environment_max_concurrency=123
                )
            ),
            code=lambda_mixins.CfnFunctionPropsMixin.CodeProperty(
                image_uri="imageUri",
                s3_bucket="s3Bucket",
                s3_key="s3Key",
                s3_object_version="s3ObjectVersion",
                source_kms_key_arn="sourceKmsKeyArn",
                zip_file="zipFile"
            ),
            code_signing_config_arn="codeSigningConfigArn",
            dead_letter_config=lambda_mixins.CfnFunctionPropsMixin.DeadLetterConfigProperty(
                target_arn="targetArn"
            ),
            description="description",
            durable_config=lambda_mixins.CfnFunctionPropsMixin.DurableConfigProperty(
                execution_timeout=123,
                retention_period_in_days=123
            ),
            environment=lambda_mixins.CfnFunctionPropsMixin.EnvironmentProperty(
                variables={
                    "variables_key": "variables"
                }
            ),
            ephemeral_storage=lambda_mixins.CfnFunctionPropsMixin.EphemeralStorageProperty(
                size=123
            ),
            file_system_configs=[lambda_mixins.CfnFunctionPropsMixin.FileSystemConfigProperty(
                arn="arn",
                local_mount_path="localMountPath"
            )],
            function_name="functionName",
            function_scaling_config=lambda_mixins.CfnFunctionPropsMixin.FunctionScalingConfigProperty(
                max_execution_environments=123,
                min_execution_environments=123
            ),
            handler="handler",
            image_config=lambda_mixins.CfnFunctionPropsMixin.ImageConfigProperty(
                command=["command"],
                entry_point=["entryPoint"],
                working_directory="workingDirectory"
            ),
            kms_key_arn="kmsKeyArn",
            layers=["layers"],
            logging_config=lambda_mixins.CfnFunctionPropsMixin.LoggingConfigProperty(
                application_log_level="applicationLogLevel",
                log_format="logFormat",
                log_group="logGroup",
                system_log_level="systemLogLevel"
            ),
            memory_size=123,
            package_type="packageType",
            publish_to_latest_published=False,
            recursive_loop="recursiveLoop",
            reserved_concurrent_executions=123,
            role="role",
            runtime="runtime",
            runtime_management_config=lambda_mixins.CfnFunctionPropsMixin.RuntimeManagementConfigProperty(
                runtime_version_arn="runtimeVersionArn",
                update_runtime_on="updateRuntimeOn"
            ),
            snap_start=lambda_mixins.CfnFunctionPropsMixin.SnapStartProperty(
                apply_on="applyOn"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            tenancy_config=lambda_mixins.CfnFunctionPropsMixin.TenancyConfigProperty(
                tenant_isolation_mode="tenantIsolationMode"
            ),
            timeout=123,
            tracing_config=lambda_mixins.CfnFunctionPropsMixin.TracingConfigProperty(
                mode="mode"
            ),
            vpc_config=lambda_mixins.CfnFunctionPropsMixin.VpcConfigProperty(
                ipv6_allowed_for_dual_stack=False,
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
        '''Create a mixin to apply properties to ``AWS::Lambda::Function``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f16a781f0389d172f38be2ba1f79a13a4aae3fddf099e1b4c369431f865cf152)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2223309c221f3e73c5050476cc9697ba54dd4772d30d58489a2f93a5159eaea)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3d5617135fad9f8621f8a11b053501adafc4990c56284291e3bc1818bc94041)
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
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnFunctionPropsMixin.CapacityProviderConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lambda_managed_instances_capacity_provider_config": "lambdaManagedInstancesCapacityProviderConfig",
        },
    )
    class CapacityProviderConfigProperty:
        def __init__(
            self,
            *,
            lambda_managed_instances_capacity_provider_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFunctionPropsMixin.LambdaManagedInstancesCapacityProviderConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param lambda_managed_instances_capacity_provider_config: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-capacityproviderconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                capacity_provider_config_property = lambda_mixins.CfnFunctionPropsMixin.CapacityProviderConfigProperty(
                    lambda_managed_instances_capacity_provider_config=lambda_mixins.CfnFunctionPropsMixin.LambdaManagedInstancesCapacityProviderConfigProperty(
                        capacity_provider_arn="capacityProviderArn",
                        execution_environment_memory_gi_bPer_vCpu=123,
                        per_execution_environment_max_concurrency=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6a6eacf2d56ef3626f1f8caa4b8a9f0f18f6a5161965eb253081e36ffb312305)
                check_type(argname="argument lambda_managed_instances_capacity_provider_config", value=lambda_managed_instances_capacity_provider_config, expected_type=type_hints["lambda_managed_instances_capacity_provider_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_managed_instances_capacity_provider_config is not None:
                self._values["lambda_managed_instances_capacity_provider_config"] = lambda_managed_instances_capacity_provider_config

        @builtins.property
        def lambda_managed_instances_capacity_provider_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.LambdaManagedInstancesCapacityProviderConfigProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-capacityproviderconfig.html#cfn-lambda-function-capacityproviderconfig-lambdamanagedinstancescapacityproviderconfig
            '''
            result = self._values.get("lambda_managed_instances_capacity_provider_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFunctionPropsMixin.LambdaManagedInstancesCapacityProviderConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityProviderConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnFunctionPropsMixin.CodeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "image_uri": "imageUri",
            "s3_bucket": "s3Bucket",
            "s3_key": "s3Key",
            "s3_object_version": "s3ObjectVersion",
            "source_kms_key_arn": "sourceKmsKeyArn",
            "zip_file": "zipFile",
        },
    )
    class CodeProperty:
        def __init__(
            self,
            *,
            image_uri: typing.Optional[builtins.str] = None,
            s3_bucket: typing.Optional[builtins.str] = None,
            s3_key: typing.Optional[builtins.str] = None,
            s3_object_version: typing.Optional[builtins.str] = None,
            source_kms_key_arn: typing.Optional[builtins.str] = None,
            zip_file: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The `deployment package <https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-package.html>`_ for a Lambda function. To deploy a function defined as a container image, you specify the location of a container image in the Amazon ECR registry. For a .zip file deployment package, you can specify the location of an object in Amazon S3. For Node.js and Python functions, you can specify the function code inline in the template.

            .. epigraph::

               When you specify source code inline for a Node.js function, the ``index`` file that CloudFormation creates uses the extension ``.js`` . This means that Node.js treats the file as a CommonJS module.

            Changes to a deployment package in Amazon S3 or a container image in ECR are not detected automatically during stack updates. To update the function code, change the object key or version in the template.

            :param image_uri: URI of a `container image <https://docs.aws.amazon.com/lambda/latest/dg/lambda-images.html>`_ in the Amazon ECR registry.
            :param s3_bucket: An Amazon S3 bucket in the same AWS Region as your function. The bucket can be in a different AWS account .
            :param s3_key: The Amazon S3 key of the deployment package.
            :param s3_object_version: For versioned objects, the version of the deployment package object to use.
            :param source_kms_key_arn: The ARN of the AWS Key Management Service ( AWS ) customer managed key that's used to encrypt your function's .zip deployment package. If you don't provide a customer managed key, Lambda uses an `AWS owned key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-owned-cmk>`_ .
            :param zip_file: (Node.js and Python) The source code of your Lambda function. If you include your function source inline with this parameter, CloudFormation places it in a file named ``index`` and zips it to create a `deployment package <https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-package.html>`_ . This zip file cannot exceed 4MB. For the ``Handler`` property, the first part of the handler identifier must be ``index`` . For example, ``index.handler`` . .. epigraph:: When you specify source code inline for a Node.js function, the ``index`` file that CloudFormation creates uses the extension ``.js`` . This means that Node.js treats the file as a CommonJS module. When using Node.js 24 or later, Node.js can automatically detect if a ``.js`` file should be treated as CommonJS or as an ES module. To enable auto-detection, add the ``--experimental-detect-module`` flag to the ``NODE_OPTIONS`` environment variable. For more information, see `Experimental Node.js features <https://docs.aws.amazon.com//lambda/latest/dg/lambda-nodejs.html#nodejs-experimental-features>`_ . For JSON, you must escape quotes and special characters such as newline ( ``\\n`` ) with a backslash. If you specify a function that interacts with an AWS CloudFormation custom resource, you don't have to write your own functions to send responses to the custom resource that invoked the function. AWS CloudFormation provides a response module ( `cfn-response <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-lambda-function-code-cfnresponsemodule.html>`_ ) that simplifies sending responses. See `Using AWS Lambda with AWS CloudFormation <https://docs.aws.amazon.com/lambda/latest/dg/services-cloudformation.html>`_ for details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                code_property = lambda_mixins.CfnFunctionPropsMixin.CodeProperty(
                    image_uri="imageUri",
                    s3_bucket="s3Bucket",
                    s3_key="s3Key",
                    s3_object_version="s3ObjectVersion",
                    source_kms_key_arn="sourceKmsKeyArn",
                    zip_file="zipFile"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cdc26a099931c9b92ca429e69136417b8c54924bcc48e1b290df5a98fefa17a5)
                check_type(argname="argument image_uri", value=image_uri, expected_type=type_hints["image_uri"])
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
                check_type(argname="argument s3_object_version", value=s3_object_version, expected_type=type_hints["s3_object_version"])
                check_type(argname="argument source_kms_key_arn", value=source_kms_key_arn, expected_type=type_hints["source_kms_key_arn"])
                check_type(argname="argument zip_file", value=zip_file, expected_type=type_hints["zip_file"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if image_uri is not None:
                self._values["image_uri"] = image_uri
            if s3_bucket is not None:
                self._values["s3_bucket"] = s3_bucket
            if s3_key is not None:
                self._values["s3_key"] = s3_key
            if s3_object_version is not None:
                self._values["s3_object_version"] = s3_object_version
            if source_kms_key_arn is not None:
                self._values["source_kms_key_arn"] = source_kms_key_arn
            if zip_file is not None:
                self._values["zip_file"] = zip_file

        @builtins.property
        def image_uri(self) -> typing.Optional[builtins.str]:
            '''URI of a `container image <https://docs.aws.amazon.com/lambda/latest/dg/lambda-images.html>`_ in the Amazon ECR registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html#cfn-lambda-function-code-imageuri
            '''
            result = self._values.get("image_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_bucket(self) -> typing.Optional[builtins.str]:
            '''An Amazon S3 bucket in the same AWS Region as your function.

            The bucket can be in a different AWS account .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html#cfn-lambda-function-code-s3bucket
            '''
            result = self._values.get("s3_bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_key(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 key of the deployment package.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html#cfn-lambda-function-code-s3key
            '''
            result = self._values.get("s3_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_object_version(self) -> typing.Optional[builtins.str]:
            '''For versioned objects, the version of the deployment package object to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html#cfn-lambda-function-code-s3objectversion
            '''
            result = self._values.get("s3_object_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the AWS Key Management Service ( AWS  ) customer managed key that's used to encrypt your function's .zip deployment package. If you don't provide a customer managed key, Lambda uses an `AWS owned key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-owned-cmk>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html#cfn-lambda-function-code-sourcekmskeyarn
            '''
            result = self._values.get("source_kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def zip_file(self) -> typing.Optional[builtins.str]:
            '''(Node.js and Python) The source code of your Lambda function. If you include your function source inline with this parameter, CloudFormation places it in a file named ``index`` and zips it to create a `deployment package <https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-package.html>`_ . This zip file cannot exceed 4MB. For the ``Handler`` property, the first part of the handler identifier must be ``index`` . For example, ``index.handler`` .

            .. epigraph::

               When you specify source code inline for a Node.js function, the ``index`` file that CloudFormation creates uses the extension ``.js`` . This means that Node.js treats the file as a CommonJS module.

               When using Node.js 24 or later, Node.js can automatically detect if a ``.js`` file should be treated as CommonJS or as an ES module. To enable auto-detection, add the ``--experimental-detect-module`` flag to the ``NODE_OPTIONS`` environment variable. For more information, see `Experimental Node.js features <https://docs.aws.amazon.com//lambda/latest/dg/lambda-nodejs.html#nodejs-experimental-features>`_ .

            For JSON, you must escape quotes and special characters such as newline ( ``\\n`` ) with a backslash.

            If you specify a function that interacts with an AWS CloudFormation custom resource, you don't have to write your own functions to send responses to the custom resource that invoked the function. AWS CloudFormation provides a response module ( `cfn-response <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-lambda-function-code-cfnresponsemodule.html>`_ ) that simplifies sending responses. See `Using AWS Lambda with AWS CloudFormation <https://docs.aws.amazon.com/lambda/latest/dg/services-cloudformation.html>`_ for details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html#cfn-lambda-function-code-zipfile
            '''
            result = self._values.get("zip_file")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnFunctionPropsMixin.DeadLetterConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"target_arn": "targetArn"},
    )
    class DeadLetterConfigProperty:
        def __init__(self, *, target_arn: typing.Optional[builtins.str] = None) -> None:
            '''The `dead-letter queue <https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-retain-records.html#invocation-dlq>`_ for failed asynchronous invocations.

            :param target_arn: The Amazon Resource Name (ARN) of an Amazon SQS queue or Amazon SNS topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-deadletterconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                dead_letter_config_property = lambda_mixins.CfnFunctionPropsMixin.DeadLetterConfigProperty(
                    target_arn="targetArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4965ae8ef5b972ae7d008c2c09ba37e18857b9a4831cd3d0a7ab4fa8f10a5a2c)
                check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_arn is not None:
                self._values["target_arn"] = target_arn

        @builtins.property
        def target_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an Amazon SQS queue or Amazon SNS topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-deadletterconfig.html#cfn-lambda-function-deadletterconfig-targetarn
            '''
            result = self._values.get("target_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeadLetterConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnFunctionPropsMixin.DurableConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "execution_timeout": "executionTimeout",
            "retention_period_in_days": "retentionPeriodInDays",
        },
    )
    class DurableConfigProperty:
        def __init__(
            self,
            *,
            execution_timeout: typing.Optional[jsii.Number] = None,
            retention_period_in_days: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param execution_timeout: The amount of time (in seconds) that Lambda allows a durable function to run before stopping it. The maximum is one 366-day year or 31,622,400 seconds.
            :param retention_period_in_days: The number of days after a durable execution is closed that Lambda retains its history, from one to 90 days. The default is 14 days. Default: - 14

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-durableconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                durable_config_property = lambda_mixins.CfnFunctionPropsMixin.DurableConfigProperty(
                    execution_timeout=123,
                    retention_period_in_days=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f642c60c21e0eb6f37d03586065f526e5933a062c04f4b2f0c1ee270dccb6637)
                check_type(argname="argument execution_timeout", value=execution_timeout, expected_type=type_hints["execution_timeout"])
                check_type(argname="argument retention_period_in_days", value=retention_period_in_days, expected_type=type_hints["retention_period_in_days"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if execution_timeout is not None:
                self._values["execution_timeout"] = execution_timeout
            if retention_period_in_days is not None:
                self._values["retention_period_in_days"] = retention_period_in_days

        @builtins.property
        def execution_timeout(self) -> typing.Optional[jsii.Number]:
            '''The amount of time (in seconds) that Lambda allows a durable function to run before stopping it.

            The maximum is one 366-day year or 31,622,400 seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-durableconfig.html#cfn-lambda-function-durableconfig-executiontimeout
            '''
            result = self._values.get("execution_timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def retention_period_in_days(self) -> typing.Optional[jsii.Number]:
            '''The number of days after a durable execution is closed that Lambda retains its history, from one to 90 days.

            The default is 14 days.

            :default: - 14

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-durableconfig.html#cfn-lambda-function-durableconfig-retentionperiodindays
            '''
            result = self._values.get("retention_period_in_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DurableConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnFunctionPropsMixin.EnvironmentProperty",
        jsii_struct_bases=[],
        name_mapping={"variables": "variables"},
    )
    class EnvironmentProperty:
        def __init__(
            self,
            *,
            variables: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''A function's environment variable settings.

            You can use environment variables to adjust your function's behavior without updating code. An environment variable is a pair of strings that are stored in a function's version-specific configuration.

            :param variables: Environment variable key-value pairs. For more information, see `Using Lambda environment variables <https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html>`_ . If the value of the environment variable is a time or a duration, enclose the value in quotes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-environment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                environment_property = lambda_mixins.CfnFunctionPropsMixin.EnvironmentProperty(
                    variables={
                        "variables_key": "variables"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__45ce2cd543064df87d811c57c4905266d4811fd5acfa6fc6fed7395f675076ef)
                check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if variables is not None:
                self._values["variables"] = variables

        @builtins.property
        def variables(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Environment variable key-value pairs. For more information, see `Using Lambda environment variables <https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html>`_ .

            If the value of the environment variable is a time or a duration, enclose the value in quotes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-environment.html#cfn-lambda-function-environment-variables
            '''
            result = self._values.get("variables")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnFunctionPropsMixin.EphemeralStorageProperty",
        jsii_struct_bases=[],
        name_mapping={"size": "size"},
    )
    class EphemeralStorageProperty:
        def __init__(self, *, size: typing.Optional[jsii.Number] = None) -> None:
            '''The size of the function's ``/tmp`` directory in MB.

            The default value is 512, but it can be any whole number between 512 and 10,240 MB.

            :param size: The size of the function's ``/tmp`` directory.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-ephemeralstorage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                ephemeral_storage_property = lambda_mixins.CfnFunctionPropsMixin.EphemeralStorageProperty(
                    size=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__26de07fd8ef9c744dfacfb3637e5534dcbe8bc6bdf2258e9e1f5c9615c945c34)
                check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if size is not None:
                self._values["size"] = size

        @builtins.property
        def size(self) -> typing.Optional[jsii.Number]:
            '''The size of the function's ``/tmp`` directory.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-ephemeralstorage.html#cfn-lambda-function-ephemeralstorage-size
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
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnFunctionPropsMixin.FileSystemConfigProperty",
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
            '''Details about the connection between a Lambda function and an `Amazon EFS file system <https://docs.aws.amazon.com/lambda/latest/dg/configuration-filesystem.html>`_ .

            :param arn: The Amazon Resource Name (ARN) of the Amazon EFS access point that provides access to the file system.
            :param local_mount_path: The path where the function can access the file system, starting with ``/mnt/`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-filesystemconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                file_system_config_property = lambda_mixins.CfnFunctionPropsMixin.FileSystemConfigProperty(
                    arn="arn",
                    local_mount_path="localMountPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__86a7d67389b5759657747d4b3ca5565d7f0cf0a384026ce7980cc55c8b706caf)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument local_mount_path", value=local_mount_path, expected_type=type_hints["local_mount_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if local_mount_path is not None:
                self._values["local_mount_path"] = local_mount_path

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon EFS access point that provides access to the file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-filesystemconfig.html#cfn-lambda-function-filesystemconfig-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def local_mount_path(self) -> typing.Optional[builtins.str]:
            '''The path where the function can access the file system, starting with ``/mnt/`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-filesystemconfig.html#cfn-lambda-function-filesystemconfig-localmountpath
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
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnFunctionPropsMixin.FunctionScalingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_execution_environments": "maxExecutionEnvironments",
            "min_execution_environments": "minExecutionEnvironments",
        },
    )
    class FunctionScalingConfigProperty:
        def __init__(
            self,
            *,
            max_execution_environments: typing.Optional[jsii.Number] = None,
            min_execution_environments: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param max_execution_environments: The maximum number of execution environments that can be provisioned for the function.
            :param min_execution_environments: The minimum number of execution environments to maintain for the function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-functionscalingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                function_scaling_config_property = lambda_mixins.CfnFunctionPropsMixin.FunctionScalingConfigProperty(
                    max_execution_environments=123,
                    min_execution_environments=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e68d67260a81b197e198d213f4392df03cb856a3a6fb0303a73a52c7c71d711e)
                check_type(argname="argument max_execution_environments", value=max_execution_environments, expected_type=type_hints["max_execution_environments"])
                check_type(argname="argument min_execution_environments", value=min_execution_environments, expected_type=type_hints["min_execution_environments"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_execution_environments is not None:
                self._values["max_execution_environments"] = max_execution_environments
            if min_execution_environments is not None:
                self._values["min_execution_environments"] = min_execution_environments

        @builtins.property
        def max_execution_environments(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of execution environments that can be provisioned for the function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-functionscalingconfig.html#cfn-lambda-function-functionscalingconfig-maxexecutionenvironments
            '''
            result = self._values.get("max_execution_environments")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_execution_environments(self) -> typing.Optional[jsii.Number]:
            '''The minimum number of execution environments to maintain for the function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-functionscalingconfig.html#cfn-lambda-function-functionscalingconfig-minexecutionenvironments
            '''
            result = self._values.get("min_execution_environments")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionScalingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnFunctionPropsMixin.ImageConfigProperty",
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
            '''Configuration values that override the container image Dockerfile settings.

            For more information, see `Container image settings <https://docs.aws.amazon.com/lambda/latest/dg/images-create.html#images-parms>`_ .

            :param command: Specifies parameters that you want to pass in with ENTRYPOINT. You can specify a maximum of 1,500 parameters in the list.
            :param entry_point: Specifies the entry point to their application, which is typically the location of the runtime executable. You can specify a maximum of 1,500 string entries in the list.
            :param working_directory: Specifies the working directory. The length of the directory string cannot exceed 1,000 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-imageconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                image_config_property = lambda_mixins.CfnFunctionPropsMixin.ImageConfigProperty(
                    command=["command"],
                    entry_point=["entryPoint"],
                    working_directory="workingDirectory"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b3f0925b5831d50be91a3a0f00e107544d8d60c7c8b6f6fe35413640d9790ac6)
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
            '''Specifies parameters that you want to pass in with ENTRYPOINT.

            You can specify a maximum of 1,500 parameters in the list.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-imageconfig.html#cfn-lambda-function-imageconfig-command
            '''
            result = self._values.get("command")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def entry_point(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the entry point to their application, which is typically the location of the runtime executable.

            You can specify a maximum of 1,500 string entries in the list.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-imageconfig.html#cfn-lambda-function-imageconfig-entrypoint
            '''
            result = self._values.get("entry_point")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def working_directory(self) -> typing.Optional[builtins.str]:
            '''Specifies the working directory.

            The length of the directory string cannot exceed 1,000 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-imageconfig.html#cfn-lambda-function-imageconfig-workingdirectory
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
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnFunctionPropsMixin.LambdaManagedInstancesCapacityProviderConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "capacity_provider_arn": "capacityProviderArn",
            "execution_environment_memory_gib_per_v_cpu": "executionEnvironmentMemoryGiBPerVCpu",
            "per_execution_environment_max_concurrency": "perExecutionEnvironmentMaxConcurrency",
        },
    )
    class LambdaManagedInstancesCapacityProviderConfigProperty:
        def __init__(
            self,
            *,
            capacity_provider_arn: typing.Optional[builtins.str] = None,
            execution_environment_memory_gib_per_v_cpu: typing.Optional[jsii.Number] = None,
            per_execution_environment_max_concurrency: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param capacity_provider_arn: The Amazon Resource Name (ARN) of the capacity provider.
            :param execution_environment_memory_gib_per_v_cpu: The amount of memory in GiB allocated per vCPU for execution environments.
            :param per_execution_environment_max_concurrency: The maximum number of concurrent execution environments that can run on each compute instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-lambdamanagedinstancescapacityproviderconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                lambda_managed_instances_capacity_provider_config_property = lambda_mixins.CfnFunctionPropsMixin.LambdaManagedInstancesCapacityProviderConfigProperty(
                    capacity_provider_arn="capacityProviderArn",
                    execution_environment_memory_gi_bPer_vCpu=123,
                    per_execution_environment_max_concurrency=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__62816e128f322d9bfa7db0e2bf8f05107fe4e524978125be6403879489f23403)
                check_type(argname="argument capacity_provider_arn", value=capacity_provider_arn, expected_type=type_hints["capacity_provider_arn"])
                check_type(argname="argument execution_environment_memory_gib_per_v_cpu", value=execution_environment_memory_gib_per_v_cpu, expected_type=type_hints["execution_environment_memory_gib_per_v_cpu"])
                check_type(argname="argument per_execution_environment_max_concurrency", value=per_execution_environment_max_concurrency, expected_type=type_hints["per_execution_environment_max_concurrency"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if capacity_provider_arn is not None:
                self._values["capacity_provider_arn"] = capacity_provider_arn
            if execution_environment_memory_gib_per_v_cpu is not None:
                self._values["execution_environment_memory_gib_per_v_cpu"] = execution_environment_memory_gib_per_v_cpu
            if per_execution_environment_max_concurrency is not None:
                self._values["per_execution_environment_max_concurrency"] = per_execution_environment_max_concurrency

        @builtins.property
        def capacity_provider_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the capacity provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-lambdamanagedinstancescapacityproviderconfig.html#cfn-lambda-function-lambdamanagedinstancescapacityproviderconfig-capacityproviderarn
            '''
            result = self._values.get("capacity_provider_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def execution_environment_memory_gib_per_v_cpu(
            self,
        ) -> typing.Optional[jsii.Number]:
            '''The amount of memory in GiB allocated per vCPU for execution environments.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-lambdamanagedinstancescapacityproviderconfig.html#cfn-lambda-function-lambdamanagedinstancescapacityproviderconfig-executionenvironmentmemorygibpervcpu
            '''
            result = self._values.get("execution_environment_memory_gib_per_v_cpu")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def per_execution_environment_max_concurrency(
            self,
        ) -> typing.Optional[jsii.Number]:
            '''The maximum number of concurrent execution environments that can run on each compute instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-lambdamanagedinstancescapacityproviderconfig.html#cfn-lambda-function-lambdamanagedinstancescapacityproviderconfig-perexecutionenvironmentmaxconcurrency
            '''
            result = self._values.get("per_execution_environment_max_concurrency")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaManagedInstancesCapacityProviderConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnFunctionPropsMixin.LoggingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_log_level": "applicationLogLevel",
            "log_format": "logFormat",
            "log_group": "logGroup",
            "system_log_level": "systemLogLevel",
        },
    )
    class LoggingConfigProperty:
        def __init__(
            self,
            *,
            application_log_level: typing.Optional[builtins.str] = None,
            log_format: typing.Optional[builtins.str] = None,
            log_group: typing.Optional[builtins.str] = None,
            system_log_level: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The function's Amazon CloudWatch Logs configuration settings.

            :param application_log_level: Set this property to filter the application logs for your function that Lambda sends to CloudWatch. Lambda only sends application logs at the selected level of detail and lower, where ``TRACE`` is the highest level and ``FATAL`` is the lowest.
            :param log_format: The format in which Lambda sends your function's application and system logs to CloudWatch. Select between plain text and structured JSON.
            :param log_group: The name of the Amazon CloudWatch log group the function sends logs to. By default, Lambda functions send logs to a default log group named ``/aws/lambda/<function name>`` . To use a different log group, enter an existing log group or enter a new log group name.
            :param system_log_level: Set this property to filter the system logs for your function that Lambda sends to CloudWatch. Lambda only sends system logs at the selected level of detail and lower, where ``DEBUG`` is the highest level and ``WARN`` is the lowest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-loggingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                logging_config_property = lambda_mixins.CfnFunctionPropsMixin.LoggingConfigProperty(
                    application_log_level="applicationLogLevel",
                    log_format="logFormat",
                    log_group="logGroup",
                    system_log_level="systemLogLevel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6adbe4bc817f0dad8a9718ec9b8f86eb625c8a25998463ef750b2e800c254903)
                check_type(argname="argument application_log_level", value=application_log_level, expected_type=type_hints["application_log_level"])
                check_type(argname="argument log_format", value=log_format, expected_type=type_hints["log_format"])
                check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
                check_type(argname="argument system_log_level", value=system_log_level, expected_type=type_hints["system_log_level"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_log_level is not None:
                self._values["application_log_level"] = application_log_level
            if log_format is not None:
                self._values["log_format"] = log_format
            if log_group is not None:
                self._values["log_group"] = log_group
            if system_log_level is not None:
                self._values["system_log_level"] = system_log_level

        @builtins.property
        def application_log_level(self) -> typing.Optional[builtins.str]:
            '''Set this property to filter the application logs for your function that Lambda sends to CloudWatch.

            Lambda only sends application logs at the selected level of detail and lower, where ``TRACE`` is the highest level and ``FATAL`` is the lowest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-loggingconfig.html#cfn-lambda-function-loggingconfig-applicationloglevel
            '''
            result = self._values.get("application_log_level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_format(self) -> typing.Optional[builtins.str]:
            '''The format in which Lambda sends your function's application and system logs to CloudWatch.

            Select between plain text and structured JSON.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-loggingconfig.html#cfn-lambda-function-loggingconfig-logformat
            '''
            result = self._values.get("log_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_group(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon CloudWatch log group the function sends logs to.

            By default, Lambda functions send logs to a default log group named ``/aws/lambda/<function name>`` . To use a different log group, enter an existing log group or enter a new log group name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-loggingconfig.html#cfn-lambda-function-loggingconfig-loggroup
            '''
            result = self._values.get("log_group")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def system_log_level(self) -> typing.Optional[builtins.str]:
            '''Set this property to filter the system logs for your function that Lambda sends to CloudWatch.

            Lambda only sends system logs at the selected level of detail and lower, where ``DEBUG`` is the highest level and ``WARN`` is the lowest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-loggingconfig.html#cfn-lambda-function-loggingconfig-systemloglevel
            '''
            result = self._values.get("system_log_level")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnFunctionPropsMixin.RuntimeManagementConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "runtime_version_arn": "runtimeVersionArn",
            "update_runtime_on": "updateRuntimeOn",
        },
    )
    class RuntimeManagementConfigProperty:
        def __init__(
            self,
            *,
            runtime_version_arn: typing.Optional[builtins.str] = None,
            update_runtime_on: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Sets the runtime management configuration for a function's version.

            For more information, see `Runtime updates <https://docs.aws.amazon.com/lambda/latest/dg/runtimes-update.html>`_ .

            :param runtime_version_arn: The ARN of the runtime version you want the function to use. .. epigraph:: This is only required if you're using the *Manual* runtime update mode.
            :param update_runtime_on: Specify the runtime update mode. - *Auto (default)* - Automatically update to the most recent and secure runtime version using a `Two-phase runtime version rollout <https://docs.aws.amazon.com/lambda/latest/dg/runtimes-update.html#runtime-management-two-phase>`_ . This is the best choice for most customers to ensure they always benefit from runtime updates. - *FunctionUpdate* - Lambda updates the runtime of you function to the most recent and secure runtime version when you update your function. This approach synchronizes runtime updates with function deployments, giving you control over when runtime updates are applied and allowing you to detect and mitigate rare runtime update incompatibilities early. When using this setting, you need to regularly update your functions to keep their runtime up-to-date. - *Manual* - You specify a runtime version in your function configuration. The function will use this runtime version indefinitely. In the rare case where a new runtime version is incompatible with an existing function, this allows you to roll back your function to an earlier runtime version. For more information, see `Roll back a runtime version <https://docs.aws.amazon.com/lambda/latest/dg/runtimes-update.html#runtime-management-rollback>`_ . *Valid Values* : ``Auto`` | ``FunctionUpdate`` | ``Manual``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-runtimemanagementconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                runtime_management_config_property = lambda_mixins.CfnFunctionPropsMixin.RuntimeManagementConfigProperty(
                    runtime_version_arn="runtimeVersionArn",
                    update_runtime_on="updateRuntimeOn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__93982a67fb081c808c8dd573b7cbbc814133cb00bdb677d3b0d66835be2fb5d8)
                check_type(argname="argument runtime_version_arn", value=runtime_version_arn, expected_type=type_hints["runtime_version_arn"])
                check_type(argname="argument update_runtime_on", value=update_runtime_on, expected_type=type_hints["update_runtime_on"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if runtime_version_arn is not None:
                self._values["runtime_version_arn"] = runtime_version_arn
            if update_runtime_on is not None:
                self._values["update_runtime_on"] = update_runtime_on

        @builtins.property
        def runtime_version_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the runtime version you want the function to use.

            .. epigraph::

               This is only required if you're using the *Manual* runtime update mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-runtimemanagementconfig.html#cfn-lambda-function-runtimemanagementconfig-runtimeversionarn
            '''
            result = self._values.get("runtime_version_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def update_runtime_on(self) -> typing.Optional[builtins.str]:
            '''Specify the runtime update mode.

            - *Auto (default)* - Automatically update to the most recent and secure runtime version using a `Two-phase runtime version rollout <https://docs.aws.amazon.com/lambda/latest/dg/runtimes-update.html#runtime-management-two-phase>`_ . This is the best choice for most customers to ensure they always benefit from runtime updates.
            - *FunctionUpdate* - Lambda updates the runtime of you function to the most recent and secure runtime version when you update your function. This approach synchronizes runtime updates with function deployments, giving you control over when runtime updates are applied and allowing you to detect and mitigate rare runtime update incompatibilities early. When using this setting, you need to regularly update your functions to keep their runtime up-to-date.
            - *Manual* - You specify a runtime version in your function configuration. The function will use this runtime version indefinitely. In the rare case where a new runtime version is incompatible with an existing function, this allows you to roll back your function to an earlier runtime version. For more information, see `Roll back a runtime version <https://docs.aws.amazon.com/lambda/latest/dg/runtimes-update.html#runtime-management-rollback>`_ .

            *Valid Values* : ``Auto`` | ``FunctionUpdate`` | ``Manual``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-runtimemanagementconfig.html#cfn-lambda-function-runtimemanagementconfig-updateruntimeon
            '''
            result = self._values.get("update_runtime_on")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuntimeManagementConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnFunctionPropsMixin.SnapStartProperty",
        jsii_struct_bases=[],
        name_mapping={"apply_on": "applyOn"},
    )
    class SnapStartProperty:
        def __init__(self, *, apply_on: typing.Optional[builtins.str] = None) -> None:
            '''The function's `AWS Lambda SnapStart <https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html>`_ setting.

            :param apply_on: Set ``ApplyOn`` to ``PublishedVersions`` to create a snapshot of the initialized execution environment when you publish a function version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-snapstart.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                snap_start_property = lambda_mixins.CfnFunctionPropsMixin.SnapStartProperty(
                    apply_on="applyOn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__44d514fa59f4a6406084ba589f5d0521a7b4370ac0d6819a604040a8b0dc0eb0)
                check_type(argname="argument apply_on", value=apply_on, expected_type=type_hints["apply_on"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if apply_on is not None:
                self._values["apply_on"] = apply_on

        @builtins.property
        def apply_on(self) -> typing.Optional[builtins.str]:
            '''Set ``ApplyOn`` to ``PublishedVersions`` to create a snapshot of the initialized execution environment when you publish a function version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-snapstart.html#cfn-lambda-function-snapstart-applyon
            '''
            result = self._values.get("apply_on")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnapStartProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnFunctionPropsMixin.SnapStartResponseProperty",
        jsii_struct_bases=[],
        name_mapping={
            "apply_on": "applyOn",
            "optimization_status": "optimizationStatus",
        },
    )
    class SnapStartResponseProperty:
        def __init__(
            self,
            *,
            apply_on: typing.Optional[builtins.str] = None,
            optimization_status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The function's `SnapStart <https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html>`_ setting.

            :param apply_on: When set to ``PublishedVersions`` , Lambda creates a snapshot of the execution environment when you publish a function version.
            :param optimization_status: When you provide a `qualified Amazon Resource Name (ARN) <https://docs.aws.amazon.com/lambda/latest/dg/configuration-versions.html#versioning-versions-using>`_ , this response element indicates whether SnapStart is activated for the specified function version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-snapstartresponse.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                snap_start_response_property = lambda_mixins.CfnFunctionPropsMixin.SnapStartResponseProperty(
                    apply_on="applyOn",
                    optimization_status="optimizationStatus"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__73878e81d01e28f332ec74e63f7faafae3cf551362e9e3ce10eb842aa715b081)
                check_type(argname="argument apply_on", value=apply_on, expected_type=type_hints["apply_on"])
                check_type(argname="argument optimization_status", value=optimization_status, expected_type=type_hints["optimization_status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if apply_on is not None:
                self._values["apply_on"] = apply_on
            if optimization_status is not None:
                self._values["optimization_status"] = optimization_status

        @builtins.property
        def apply_on(self) -> typing.Optional[builtins.str]:
            '''When set to ``PublishedVersions`` , Lambda creates a snapshot of the execution environment when you publish a function version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-snapstartresponse.html#cfn-lambda-function-snapstartresponse-applyon
            '''
            result = self._values.get("apply_on")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def optimization_status(self) -> typing.Optional[builtins.str]:
            '''When you provide a `qualified Amazon Resource Name (ARN) <https://docs.aws.amazon.com/lambda/latest/dg/configuration-versions.html#versioning-versions-using>`_ , this response element indicates whether SnapStart is activated for the specified function version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-snapstartresponse.html#cfn-lambda-function-snapstartresponse-optimizationstatus
            '''
            result = self._values.get("optimization_status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnapStartResponseProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnFunctionPropsMixin.TenancyConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"tenant_isolation_mode": "tenantIsolationMode"},
    )
    class TenancyConfigProperty:
        def __init__(
            self,
            *,
            tenant_isolation_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the tenant isolation mode configuration for a Lambda function.

            This allows you to configure specific tenant isolation strategies for your function invocations. Tenant isolation configuration cannot be modified after function creation.

            :param tenant_isolation_mode: Tenant isolation mode allows for invocation to be sent to a corresponding execution environment dedicated to a specific tenant ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-tenancyconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                tenancy_config_property = lambda_mixins.CfnFunctionPropsMixin.TenancyConfigProperty(
                    tenant_isolation_mode="tenantIsolationMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__795a4838660d1fcb938a62756dc56f81aef5bc484d83e4d648da265648220307)
                check_type(argname="argument tenant_isolation_mode", value=tenant_isolation_mode, expected_type=type_hints["tenant_isolation_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if tenant_isolation_mode is not None:
                self._values["tenant_isolation_mode"] = tenant_isolation_mode

        @builtins.property
        def tenant_isolation_mode(self) -> typing.Optional[builtins.str]:
            '''Tenant isolation mode allows for invocation to be sent to a corresponding execution environment dedicated to a specific tenant ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-tenancyconfig.html#cfn-lambda-function-tenancyconfig-tenantisolationmode
            '''
            result = self._values.get("tenant_isolation_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TenancyConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnFunctionPropsMixin.TracingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"mode": "mode"},
    )
    class TracingConfigProperty:
        def __init__(self, *, mode: typing.Optional[builtins.str] = None) -> None:
            '''The function's `AWS X-Ray <https://docs.aws.amazon.com/lambda/latest/dg/services-xray.html>`_ tracing configuration. To sample and record incoming requests, set ``Mode`` to ``Active`` .

            :param mode: The tracing mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-tracingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                tracing_config_property = lambda_mixins.CfnFunctionPropsMixin.TracingConfigProperty(
                    mode="mode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dc3f72be563484986171e5649dce4e8ea5f8af3920c8b4af0798e37dce7f6f12)
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mode is not None:
                self._values["mode"] = mode

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''The tracing mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-tracingconfig.html#cfn-lambda-function-tracingconfig-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TracingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnFunctionPropsMixin.VpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ipv6_allowed_for_dual_stack": "ipv6AllowedForDualStack",
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class VpcConfigProperty:
        def __init__(
            self,
            *,
            ipv6_allowed_for_dual_stack: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The VPC security groups and subnets that are attached to a Lambda function.

            When you connect a function to a VPC, Lambda creates an elastic network interface for each combination of security group and subnet in the function's VPC configuration. The function can only access resources and the internet through that VPC. For more information, see `VPC Settings <https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html>`_ .
            .. epigraph::

               When you delete a function, CloudFormation monitors the state of its network interfaces and waits for Lambda to delete them before proceeding. If the VPC is defined in the same stack, the network interfaces need to be deleted by Lambda before CloudFormation can delete the VPC's resources.

               To monitor network interfaces, CloudFormation needs the ``ec2:DescribeNetworkInterfaces`` permission. It obtains this from the user or role that modifies the stack. If you don't provide this permission, CloudFormation does not wait for network interfaces to be deleted.

            :param ipv6_allowed_for_dual_stack: Allows outbound IPv6 traffic on VPC functions that are connected to dual-stack subnets.
            :param security_group_ids: A list of VPC security group IDs.
            :param subnet_ids: A list of VPC subnet IDs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-vpcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                vpc_config_property = lambda_mixins.CfnFunctionPropsMixin.VpcConfigProperty(
                    ipv6_allowed_for_dual_stack=False,
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__59106bddbe5a22aa6e0d19e653a6e4920d37c34898af8e443d7c80941f40a3ed)
                check_type(argname="argument ipv6_allowed_for_dual_stack", value=ipv6_allowed_for_dual_stack, expected_type=type_hints["ipv6_allowed_for_dual_stack"])
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ipv6_allowed_for_dual_stack is not None:
                self._values["ipv6_allowed_for_dual_stack"] = ipv6_allowed_for_dual_stack
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def ipv6_allowed_for_dual_stack(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Allows outbound IPv6 traffic on VPC functions that are connected to dual-stack subnets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-vpcconfig.html#cfn-lambda-function-vpcconfig-ipv6allowedfordualstack
            '''
            result = self._values.get("ipv6_allowed_for_dual_stack")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of VPC security group IDs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-vpcconfig.html#cfn-lambda-function-vpcconfig-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of VPC subnet IDs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-vpcconfig.html#cfn-lambda-function-vpcconfig-subnetids
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
    jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnLayerVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "compatible_architectures": "compatibleArchitectures",
        "compatible_runtimes": "compatibleRuntimes",
        "content": "content",
        "description": "description",
        "layer_name": "layerName",
        "license_info": "licenseInfo",
    },
)
class CfnLayerVersionMixinProps:
    def __init__(
        self,
        *,
        compatible_architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
        compatible_runtimes: typing.Optional[typing.Sequence[builtins.str]] = None,
        content: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLayerVersionPropsMixin.ContentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        layer_name: typing.Optional[builtins.str] = None,
        license_info: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnLayerVersionPropsMixin.

        :param compatible_architectures: A list of compatible `instruction set architectures <https://docs.aws.amazon.com/lambda/latest/dg/foundation-arch.html>`_ .
        :param compatible_runtimes: A list of compatible `function runtimes <https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html>`_ . Used for filtering with `ListLayers <https://docs.aws.amazon.com/lambda/latest/dg/API_ListLayers.html>`_ and `ListLayerVersions <https://docs.aws.amazon.com/lambda/latest/dg/API_ListLayerVersions.html>`_ .
        :param content: The function layer archive.
        :param description: The description of the version.
        :param layer_name: The name or Amazon Resource Name (ARN) of the layer.
        :param license_info: The layer's software license. It can be any of the following:. - An `SPDX license identifier <https://docs.aws.amazon.com/https://spdx.org/licenses/>`_ . For example, ``MIT`` . - The URL of a license hosted on the internet. For example, ``https://opensource.org/licenses/MIT`` . - The full text of the license.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
            
            cfn_layer_version_mixin_props = lambda_mixins.CfnLayerVersionMixinProps(
                compatible_architectures=["compatibleArchitectures"],
                compatible_runtimes=["compatibleRuntimes"],
                content=lambda_mixins.CfnLayerVersionPropsMixin.ContentProperty(
                    s3_bucket="s3Bucket",
                    s3_key="s3Key",
                    s3_object_version="s3ObjectVersion"
                ),
                description="description",
                layer_name="layerName",
                license_info="licenseInfo"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a86a417b02bbd1c5d8f1b46653a01c49cccf0d55e84331b296fc9800f25b36ff)
            check_type(argname="argument compatible_architectures", value=compatible_architectures, expected_type=type_hints["compatible_architectures"])
            check_type(argname="argument compatible_runtimes", value=compatible_runtimes, expected_type=type_hints["compatible_runtimes"])
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument layer_name", value=layer_name, expected_type=type_hints["layer_name"])
            check_type(argname="argument license_info", value=license_info, expected_type=type_hints["license_info"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compatible_architectures is not None:
            self._values["compatible_architectures"] = compatible_architectures
        if compatible_runtimes is not None:
            self._values["compatible_runtimes"] = compatible_runtimes
        if content is not None:
            self._values["content"] = content
        if description is not None:
            self._values["description"] = description
        if layer_name is not None:
            self._values["layer_name"] = layer_name
        if license_info is not None:
            self._values["license_info"] = license_info

    @builtins.property
    def compatible_architectures(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of compatible `instruction set architectures <https://docs.aws.amazon.com/lambda/latest/dg/foundation-arch.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversion.html#cfn-lambda-layerversion-compatiblearchitectures
        '''
        result = self._values.get("compatible_architectures")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def compatible_runtimes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of compatible `function runtimes <https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html>`_ . Used for filtering with `ListLayers <https://docs.aws.amazon.com/lambda/latest/dg/API_ListLayers.html>`_ and `ListLayerVersions <https://docs.aws.amazon.com/lambda/latest/dg/API_ListLayerVersions.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversion.html#cfn-lambda-layerversion-compatibleruntimes
        '''
        result = self._values.get("compatible_runtimes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def content(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLayerVersionPropsMixin.ContentProperty"]]:
        '''The function layer archive.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversion.html#cfn-lambda-layerversion-content
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLayerVersionPropsMixin.ContentProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversion.html#cfn-lambda-layerversion-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def layer_name(self) -> typing.Optional[builtins.str]:
        '''The name or Amazon Resource Name (ARN) of the layer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversion.html#cfn-lambda-layerversion-layername
        '''
        result = self._values.get("layer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license_info(self) -> typing.Optional[builtins.str]:
        '''The layer's software license. It can be any of the following:.

        - An `SPDX license identifier <https://docs.aws.amazon.com/https://spdx.org/licenses/>`_ . For example, ``MIT`` .
        - The URL of a license hosted on the internet. For example, ``https://opensource.org/licenses/MIT`` .
        - The full text of the license.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversion.html#cfn-lambda-layerversion-licenseinfo
        '''
        result = self._values.get("license_info")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLayerVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnLayerVersionPermissionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "layer_version_arn": "layerVersionArn",
        "organization_id": "organizationId",
        "principal": "principal",
    },
)
class CfnLayerVersionPermissionMixinProps:
    def __init__(
        self,
        *,
        action: typing.Optional[builtins.str] = None,
        layer_version_arn: typing.Optional[builtins.str] = None,
        organization_id: typing.Optional[builtins.str] = None,
        principal: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnLayerVersionPermissionPropsMixin.

        :param action: The API action that grants access to the layer. For example, ``lambda:GetLayerVersion`` .
        :param layer_version_arn: The name or Amazon Resource Name (ARN) of the layer.
        :param organization_id: With the principal set to ``*`` , grant permission to all accounts in the specified organization.
        :param principal: An account ID, or ``*`` to grant layer usage permission to all accounts in an organization, or all AWS accounts (if ``organizationId`` is not specified). For the last case, make sure that you really do want all AWS accounts to have usage permission to this layer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversionpermission.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
            
            cfn_layer_version_permission_mixin_props = lambda_mixins.CfnLayerVersionPermissionMixinProps(
                action="action",
                layer_version_arn="layerVersionArn",
                organization_id="organizationId",
                principal="principal"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1670500895f6c87af20ad2a0bbfdb73a184167597e4b2e6ae90c584726e0ab2)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument layer_version_arn", value=layer_version_arn, expected_type=type_hints["layer_version_arn"])
            check_type(argname="argument organization_id", value=organization_id, expected_type=type_hints["organization_id"])
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if layer_version_arn is not None:
            self._values["layer_version_arn"] = layer_version_arn
        if organization_id is not None:
            self._values["organization_id"] = organization_id
        if principal is not None:
            self._values["principal"] = principal

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''The API action that grants access to the layer.

        For example, ``lambda:GetLayerVersion`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversionpermission.html#cfn-lambda-layerversionpermission-action
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def layer_version_arn(self) -> typing.Optional[builtins.str]:
        '''The name or Amazon Resource Name (ARN) of the layer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversionpermission.html#cfn-lambda-layerversionpermission-layerversionarn
        '''
        result = self._values.get("layer_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization_id(self) -> typing.Optional[builtins.str]:
        '''With the principal set to ``*`` , grant permission to all accounts in the specified organization.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversionpermission.html#cfn-lambda-layerversionpermission-organizationid
        '''
        result = self._values.get("organization_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def principal(self) -> typing.Optional[builtins.str]:
        '''An account ID, or ``*`` to grant layer usage permission to all accounts in an organization, or all AWS accounts (if ``organizationId`` is not specified).

        For the last case, make sure that you really do want all AWS accounts to have usage permission to this layer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversionpermission.html#cfn-lambda-layerversionpermission-principal
        '''
        result = self._values.get("principal")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLayerVersionPermissionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLayerVersionPermissionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnLayerVersionPermissionPropsMixin",
):
    '''The ``AWS::Lambda::LayerVersionPermission`` resource adds permissions to the resource-based policy of a version of an `Lambda layer <https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html>`_ . Use this action to grant layer usage permission to other accounts. You can grant permission to a single account, all AWS accounts, or all accounts in an organization.

    .. epigraph::

       Since the release of the `UpdateReplacePolicy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatereplacepolicy.html>`_ both ``UpdateReplacePolicy`` and ``DeletionPolicy`` are required to protect your Resources/LayerPermissions from deletion.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversionpermission.html
    :cloudformationResource: AWS::Lambda::LayerVersionPermission
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
        
        cfn_layer_version_permission_props_mixin = lambda_mixins.CfnLayerVersionPermissionPropsMixin(lambda_mixins.CfnLayerVersionPermissionMixinProps(
            action="action",
            layer_version_arn="layerVersionArn",
            organization_id="organizationId",
            principal="principal"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLayerVersionPermissionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lambda::LayerVersionPermission``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__592633b235d749284213e4af07bc4eafeee0086617c257d6c160d63038bb3af8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__608976824d323a0c8d4f6e995c877ecf2f995b7405f10398cf048f050b8a9e17)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e763dbfcb57c6ae0a3b1312ff4c0639da9d98c4271c98a5b7d76b9abcfeb2568)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLayerVersionPermissionMixinProps:
        return typing.cast(CfnLayerVersionPermissionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.implements(_IMixin_11e4b965)
class CfnLayerVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnLayerVersionPropsMixin",
):
    '''The ``AWS::Lambda::LayerVersion`` resource creates a `Lambda layer <https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html>`_ from a ZIP archive.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversion.html
    :cloudformationResource: AWS::Lambda::LayerVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
        
        cfn_layer_version_props_mixin = lambda_mixins.CfnLayerVersionPropsMixin(lambda_mixins.CfnLayerVersionMixinProps(
            compatible_architectures=["compatibleArchitectures"],
            compatible_runtimes=["compatibleRuntimes"],
            content=lambda_mixins.CfnLayerVersionPropsMixin.ContentProperty(
                s3_bucket="s3Bucket",
                s3_key="s3Key",
                s3_object_version="s3ObjectVersion"
            ),
            description="description",
            layer_name="layerName",
            license_info="licenseInfo"
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
        '''Create a mixin to apply properties to ``AWS::Lambda::LayerVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb6094413ad011e73710d7253c65215768548db6cf0489159b0819606f9c8453)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b74fbc777a8c483f9bca7c0202131d70ace01b66134e24c0850609c221520024)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91ae234beb02fe4cb8ffc94380a617605a5f7dd0770ac58030fcd41e51675436)
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
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnLayerVersionPropsMixin.ContentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "s3_bucket": "s3Bucket",
            "s3_key": "s3Key",
            "s3_object_version": "s3ObjectVersion",
        },
    )
    class ContentProperty:
        def __init__(
            self,
            *,
            s3_bucket: typing.Optional[builtins.str] = None,
            s3_key: typing.Optional[builtins.str] = None,
            s3_object_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A ZIP archive that contains the contents of an `Lambda layer <https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html>`_ .

            :param s3_bucket: The Amazon S3 bucket of the layer archive.
            :param s3_key: The Amazon S3 key of the layer archive.
            :param s3_object_version: For versioned objects, the version of the layer archive object to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-layerversion-content.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                content_property = lambda_mixins.CfnLayerVersionPropsMixin.ContentProperty(
                    s3_bucket="s3Bucket",
                    s3_key="s3Key",
                    s3_object_version="s3ObjectVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a7e41391063a3577270c20c4758a2cb7567c19f32cf2c3ad3ac7b3eef1ce3769)
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
                check_type(argname="argument s3_object_version", value=s3_object_version, expected_type=type_hints["s3_object_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_bucket is not None:
                self._values["s3_bucket"] = s3_bucket
            if s3_key is not None:
                self._values["s3_key"] = s3_key
            if s3_object_version is not None:
                self._values["s3_object_version"] = s3_object_version

        @builtins.property
        def s3_bucket(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 bucket of the layer archive.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-layerversion-content.html#cfn-lambda-layerversion-content-s3bucket
            '''
            result = self._values.get("s3_bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_key(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 key of the layer archive.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-layerversion-content.html#cfn-lambda-layerversion-content-s3key
            '''
            result = self._values.get("s3_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_object_version(self) -> typing.Optional[builtins.str]:
            '''For versioned objects, the version of the layer archive object to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-layerversion-content.html#cfn-lambda-layerversion-content-s3objectversion
            '''
            result = self._values.get("s3_object_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnPermissionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "event_source_token": "eventSourceToken",
        "function_name": "functionName",
        "function_url_auth_type": "functionUrlAuthType",
        "invoked_via_function_url": "invokedViaFunctionUrl",
        "principal": "principal",
        "principal_org_id": "principalOrgId",
        "source_account": "sourceAccount",
        "source_arn": "sourceArn",
    },
)
class CfnPermissionMixinProps:
    def __init__(
        self,
        *,
        action: typing.Optional[builtins.str] = None,
        event_source_token: typing.Optional[builtins.str] = None,
        function_name: typing.Optional[builtins.str] = None,
        function_url_auth_type: typing.Optional[builtins.str] = None,
        invoked_via_function_url: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        principal: typing.Optional[builtins.str] = None,
        principal_org_id: typing.Optional[builtins.str] = None,
        source_account: typing.Optional[builtins.str] = None,
        source_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPermissionPropsMixin.

        :param action: The action that the principal can use on the function. For example, ``lambda:InvokeFunction`` or ``lambda:GetFunction`` .
        :param event_source_token: For Alexa Smart Home functions, a token that the invoker must supply.
        :param function_name: The name or ARN of the Lambda function, version, or alias. **Name formats** - *Function name* – ``my-function`` (name-only), ``my-function:v1`` (with alias). - *Function ARN* – ``arn:aws:lambda:us-west-2:123456789012:function:my-function`` . - *Partial ARN* – ``123456789012:function:my-function`` . You can append a version number or alias to any of the formats. The length constraint applies only to the full ARN. If you specify only the function name, it is limited to 64 characters in length.
        :param function_url_auth_type: The type of authentication that your function URL uses. Set to ``AWS_IAM`` if you want to restrict access to authenticated users only. Set to ``NONE`` if you want to bypass IAM authentication to create a public endpoint. For more information, see `Control access to Lambda function URLs <https://docs.aws.amazon.com/lambda/latest/dg/urls-auth.html>`_ .
        :param invoked_via_function_url: Restricts the ``lambda:InvokeFunction`` action to function URL calls. When specified, this option prevents the principal from invoking the function by any means other than the function URL. For more information, see `Control access to Lambda function URLs <https://docs.aws.amazon.com/lambda/latest/dg/urls-auth.html>`_ .
        :param principal: The AWS service , AWS account , IAM user, or IAM role that invokes the function. If you specify a service, use ``SourceArn`` or ``SourceAccount`` to limit who can invoke the function through that service.
        :param principal_org_id: The identifier for your organization in AWS Organizations . Use this to grant permissions to all the AWS accounts under this organization.
        :param source_account: For AWS service , the ID of the AWS account that owns the resource. Use this together with ``SourceArn`` to ensure that the specified account owns the resource. It is possible for an Amazon S3 bucket to be deleted by its owner and recreated by another account.
        :param source_arn: For AWS services , the ARN of the AWS resource that invokes the function. For example, an Amazon S3 bucket or Amazon SNS topic. Note that Lambda configures the comparison using the ``StringLike`` operator.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
            
            cfn_permission_mixin_props = lambda_mixins.CfnPermissionMixinProps(
                action="action",
                event_source_token="eventSourceToken",
                function_name="functionName",
                function_url_auth_type="functionUrlAuthType",
                invoked_via_function_url=False,
                principal="principal",
                principal_org_id="principalOrgId",
                source_account="sourceAccount",
                source_arn="sourceArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89586071974279e49a61674d471bfc7e62cfabfd32da17a273c10cfccd1de42f)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument event_source_token", value=event_source_token, expected_type=type_hints["event_source_token"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument function_url_auth_type", value=function_url_auth_type, expected_type=type_hints["function_url_auth_type"])
            check_type(argname="argument invoked_via_function_url", value=invoked_via_function_url, expected_type=type_hints["invoked_via_function_url"])
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
            check_type(argname="argument principal_org_id", value=principal_org_id, expected_type=type_hints["principal_org_id"])
            check_type(argname="argument source_account", value=source_account, expected_type=type_hints["source_account"])
            check_type(argname="argument source_arn", value=source_arn, expected_type=type_hints["source_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if event_source_token is not None:
            self._values["event_source_token"] = event_source_token
        if function_name is not None:
            self._values["function_name"] = function_name
        if function_url_auth_type is not None:
            self._values["function_url_auth_type"] = function_url_auth_type
        if invoked_via_function_url is not None:
            self._values["invoked_via_function_url"] = invoked_via_function_url
        if principal is not None:
            self._values["principal"] = principal
        if principal_org_id is not None:
            self._values["principal_org_id"] = principal_org_id
        if source_account is not None:
            self._values["source_account"] = source_account
        if source_arn is not None:
            self._values["source_arn"] = source_arn

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''The action that the principal can use on the function.

        For example, ``lambda:InvokeFunction`` or ``lambda:GetFunction`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html#cfn-lambda-permission-action
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_source_token(self) -> typing.Optional[builtins.str]:
        '''For Alexa Smart Home functions, a token that the invoker must supply.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html#cfn-lambda-permission-eventsourcetoken
        '''
        result = self._values.get("event_source_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        '''The name or ARN of the Lambda function, version, or alias.

        **Name formats** - *Function name* – ``my-function`` (name-only), ``my-function:v1`` (with alias).

        - *Function ARN* – ``arn:aws:lambda:us-west-2:123456789012:function:my-function`` .
        - *Partial ARN* – ``123456789012:function:my-function`` .

        You can append a version number or alias to any of the formats. The length constraint applies only to the full ARN. If you specify only the function name, it is limited to 64 characters in length.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html#cfn-lambda-permission-functionname
        '''
        result = self._values.get("function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def function_url_auth_type(self) -> typing.Optional[builtins.str]:
        '''The type of authentication that your function URL uses.

        Set to ``AWS_IAM`` if you want to restrict access to authenticated users only. Set to ``NONE`` if you want to bypass IAM authentication to create a public endpoint. For more information, see `Control access to Lambda function URLs <https://docs.aws.amazon.com/lambda/latest/dg/urls-auth.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html#cfn-lambda-permission-functionurlauthtype
        '''
        result = self._values.get("function_url_auth_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invoked_via_function_url(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Restricts the ``lambda:InvokeFunction`` action to function URL calls.

        When specified, this option prevents the principal from invoking the function by any means other than the function URL. For more information, see `Control access to Lambda function URLs <https://docs.aws.amazon.com/lambda/latest/dg/urls-auth.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html#cfn-lambda-permission-invokedviafunctionurl
        '''
        result = self._values.get("invoked_via_function_url")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def principal(self) -> typing.Optional[builtins.str]:
        '''The AWS service , AWS account , IAM user, or IAM role that invokes the function.

        If you specify a service, use ``SourceArn`` or ``SourceAccount`` to limit who can invoke the function through that service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html#cfn-lambda-permission-principal
        '''
        result = self._values.get("principal")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def principal_org_id(self) -> typing.Optional[builtins.str]:
        '''The identifier for your organization in AWS Organizations .

        Use this to grant permissions to all the AWS accounts under this organization.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html#cfn-lambda-permission-principalorgid
        '''
        result = self._values.get("principal_org_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_account(self) -> typing.Optional[builtins.str]:
        '''For AWS service , the ID of the AWS account that owns the resource.

        Use this together with ``SourceArn`` to ensure that the specified account owns the resource. It is possible for an Amazon S3 bucket to be deleted by its owner and recreated by another account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html#cfn-lambda-permission-sourceaccount
        '''
        result = self._values.get("source_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_arn(self) -> typing.Optional[builtins.str]:
        '''For AWS services , the ARN of the AWS resource that invokes the function.

        For example, an Amazon S3 bucket or Amazon SNS topic.

        Note that Lambda configures the comparison using the ``StringLike`` operator.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html#cfn-lambda-permission-sourcearn
        '''
        result = self._values.get("source_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPermissionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPermissionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnPermissionPropsMixin",
):
    '''The ``AWS::Lambda::Permission`` resource grants an AWS service or another account permission to use a function.

    You can apply the policy at the function level, or specify a qualifier to restrict access to a single version or alias. If you use a qualifier, the invoker must use the full Amazon Resource Name (ARN) of that version or alias to invoke the function.

    To grant permission to another account, specify the account ID as the ``Principal`` . To grant permission to an organization defined in AWS Organizations , specify the organization ID as the ``PrincipalOrgID`` . For AWS services, the principal is a domain-style identifier defined by the service, like ``s3.amazonaws.com`` or ``sns.amazonaws.com`` . For AWS services, you can also specify the ARN of the associated resource as the ``SourceArn`` . If you grant permission to a service principal without specifying the source, other accounts could potentially configure resources in their account to invoke your Lambda function.

    If your function has a function URL, you can specify the ``FunctionUrlAuthType`` parameter. This adds a condition to your permission that only applies when your function URL's ``AuthType`` matches the specified ``FunctionUrlAuthType`` . For more information about the ``AuthType`` parameter, see `Control access to Lambda function URLs <https://docs.aws.amazon.com/lambda/latest/dg/urls-auth.html>`_ .

    This resource adds a statement to a resource-based permission policy for the function. For more information about function policies, see `Lambda Function Policies <https://docs.aws.amazon.com/lambda/latest/dg/access-control-resource-based.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html
    :cloudformationResource: AWS::Lambda::Permission
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
        
        cfn_permission_props_mixin = lambda_mixins.CfnPermissionPropsMixin(lambda_mixins.CfnPermissionMixinProps(
            action="action",
            event_source_token="eventSourceToken",
            function_name="functionName",
            function_url_auth_type="functionUrlAuthType",
            invoked_via_function_url=False,
            principal="principal",
            principal_org_id="principalOrgId",
            source_account="sourceAccount",
            source_arn="sourceArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPermissionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lambda::Permission``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73f41790fa2854b31d2caf82ce3872b1d494c832e2b0fc884f1843393aca8e71)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ba6c06e09def4a873df560c1dd5e96e37b4227d46d650e5c30f50ea3c7917bb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60335c93909da5a31777e91f31f92443d0ed53fed4b3d708c4fe753bf416c207)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPermissionMixinProps:
        return typing.cast(CfnPermissionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnUrlMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "auth_type": "authType",
        "cors": "cors",
        "invoke_mode": "invokeMode",
        "qualifier": "qualifier",
        "target_function_arn": "targetFunctionArn",
    },
)
class CfnUrlMixinProps:
    def __init__(
        self,
        *,
        auth_type: typing.Optional[builtins.str] = None,
        cors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUrlPropsMixin.CorsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        invoke_mode: typing.Optional[builtins.str] = None,
        qualifier: typing.Optional[builtins.str] = None,
        target_function_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnUrlPropsMixin.

        :param auth_type: The type of authentication that your function URL uses. Set to ``AWS_IAM`` if you want to restrict access to authenticated users only. Set to ``NONE`` if you want to bypass IAM authentication to create a public endpoint. For more information, see `Security and auth model for Lambda function URLs <https://docs.aws.amazon.com/lambda/latest/dg/urls-auth.html>`_ .
        :param cors: The `Cross-Origin Resource Sharing (CORS) <https://docs.aws.amazon.com/https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS>`_ settings for your function URL.
        :param invoke_mode: Use one of the following options:. - ``BUFFERED`` – This is the default option. Lambda invokes your function using the ``Invoke`` API operation. Invocation results are available when the payload is complete. The maximum payload size is 6 MB. - ``RESPONSE_STREAM`` – Your function streams payload results as they become available. Lambda invokes your function using the ``InvokeWithResponseStream`` API operation. The maximum response payload size is 200 MB.
        :param qualifier: The alias name.
        :param target_function_arn: The name of the Lambda function. **Name formats** - *Function name* - ``my-function`` . - *Function ARN* - ``lambda: : :function:my-function`` . - *Partial ARN* - ``:function:my-function`` . The length constraint applies only to the full ARN. If you specify only the function name, it is limited to 64 characters in length.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-url.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
            
            cfn_url_mixin_props = lambda_mixins.CfnUrlMixinProps(
                auth_type="authType",
                cors=lambda_mixins.CfnUrlPropsMixin.CorsProperty(
                    allow_credentials=False,
                    allow_headers=["allowHeaders"],
                    allow_methods=["allowMethods"],
                    allow_origins=["allowOrigins"],
                    expose_headers=["exposeHeaders"],
                    max_age=123
                ),
                invoke_mode="invokeMode",
                qualifier="qualifier",
                target_function_arn="targetFunctionArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4bfe5dc4bea6253fab30277a2ac0ea387cb89a2fd7f7639b40867d336d662c8)
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument cors", value=cors, expected_type=type_hints["cors"])
            check_type(argname="argument invoke_mode", value=invoke_mode, expected_type=type_hints["invoke_mode"])
            check_type(argname="argument qualifier", value=qualifier, expected_type=type_hints["qualifier"])
            check_type(argname="argument target_function_arn", value=target_function_arn, expected_type=type_hints["target_function_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_type is not None:
            self._values["auth_type"] = auth_type
        if cors is not None:
            self._values["cors"] = cors
        if invoke_mode is not None:
            self._values["invoke_mode"] = invoke_mode
        if qualifier is not None:
            self._values["qualifier"] = qualifier
        if target_function_arn is not None:
            self._values["target_function_arn"] = target_function_arn

    @builtins.property
    def auth_type(self) -> typing.Optional[builtins.str]:
        '''The type of authentication that your function URL uses.

        Set to ``AWS_IAM`` if you want to restrict access to authenticated users only. Set to ``NONE`` if you want to bypass IAM authentication to create a public endpoint. For more information, see `Security and auth model for Lambda function URLs <https://docs.aws.amazon.com/lambda/latest/dg/urls-auth.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-url.html#cfn-lambda-url-authtype
        '''
        result = self._values.get("auth_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cors(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUrlPropsMixin.CorsProperty"]]:
        '''The `Cross-Origin Resource Sharing (CORS) <https://docs.aws.amazon.com/https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS>`_ settings for your function URL.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-url.html#cfn-lambda-url-cors
        '''
        result = self._values.get("cors")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUrlPropsMixin.CorsProperty"]], result)

    @builtins.property
    def invoke_mode(self) -> typing.Optional[builtins.str]:
        '''Use one of the following options:.

        - ``BUFFERED`` – This is the default option. Lambda invokes your function using the ``Invoke`` API operation. Invocation results are available when the payload is complete. The maximum payload size is 6 MB.
        - ``RESPONSE_STREAM`` – Your function streams payload results as they become available. Lambda invokes your function using the ``InvokeWithResponseStream`` API operation. The maximum response payload size is 200 MB.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-url.html#cfn-lambda-url-invokemode
        '''
        result = self._values.get("invoke_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def qualifier(self) -> typing.Optional[builtins.str]:
        '''The alias name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-url.html#cfn-lambda-url-qualifier
        '''
        result = self._values.get("qualifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_function_arn(self) -> typing.Optional[builtins.str]:
        '''The name of the Lambda function.

        **Name formats** - *Function name* - ``my-function`` .

        - *Function ARN* - ``lambda:  :  :function:my-function`` .
        - *Partial ARN* - ``:function:my-function`` .

        The length constraint applies only to the full ARN. If you specify only the function name, it is limited to 64 characters in length.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-url.html#cfn-lambda-url-targetfunctionarn
        '''
        result = self._values.get("target_function_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUrlMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUrlPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnUrlPropsMixin",
):
    '''The ``AWS::Lambda::Url`` resource creates a function URL with the specified configuration parameters.

    A `function URL <https://docs.aws.amazon.com/lambda/latest/dg/lambda-urls.html>`_ is a dedicated HTTP(S) endpoint that you can use to invoke your function.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-url.html
    :cloudformationResource: AWS::Lambda::Url
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
        
        cfn_url_props_mixin = lambda_mixins.CfnUrlPropsMixin(lambda_mixins.CfnUrlMixinProps(
            auth_type="authType",
            cors=lambda_mixins.CfnUrlPropsMixin.CorsProperty(
                allow_credentials=False,
                allow_headers=["allowHeaders"],
                allow_methods=["allowMethods"],
                allow_origins=["allowOrigins"],
                expose_headers=["exposeHeaders"],
                max_age=123
            ),
            invoke_mode="invokeMode",
            qualifier="qualifier",
            target_function_arn="targetFunctionArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnUrlMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lambda::Url``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dca29365ffadb207aa16d462a498148bc0e370e3b6e264251acaf3ddc39bc28)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8105d8cf410f42bc65a4be9fa20a33ab799e0b1c5ae4b5082e26e33a8117d23)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4897c85d2cfaebd029b3467431d69f2579aee3015c6dea2b90213299358edc42)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUrlMixinProps:
        return typing.cast(CfnUrlMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnUrlPropsMixin.CorsProperty",
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
    class CorsProperty:
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
            '''The `Cross-Origin Resource Sharing (CORS) <https://docs.aws.amazon.com/https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS>`_ settings for your function URL. Use CORS to grant access to your function URL from any origin. You can also use CORS to control access for specific HTTP headers and methods in requests to your function URL.

            :param allow_credentials: Whether you want to allow cookies or other credentials in requests to your function URL. The default is ``false`` .
            :param allow_headers: The HTTP headers that origins can include in requests to your function URL. For example: ``Date`` , ``Keep-Alive`` , ``X-Custom-Header`` .
            :param allow_methods: The HTTP methods that are allowed when calling your function URL. For example: ``GET`` , ``POST`` , ``DELETE`` , or the wildcard character ( ``*`` ).
            :param allow_origins: The origins that can access your function URL. You can list any number of specific origins, separated by a comma. For example: ``https://www.example.com`` , ``http://localhost:60905`` . Alternatively, you can grant access to all origins with the wildcard character ( ``*`` ).
            :param expose_headers: The HTTP headers in your function response that you want to expose to origins that call your function URL. For example: ``Date`` , ``Keep-Alive`` , ``X-Custom-Header`` .
            :param max_age: The maximum amount of time, in seconds, that browsers can cache results of a preflight request. By default, this is set to ``0`` , which means the browser will not cache results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-url-cors.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                cors_property = lambda_mixins.CfnUrlPropsMixin.CorsProperty(
                    allow_credentials=False,
                    allow_headers=["allowHeaders"],
                    allow_methods=["allowMethods"],
                    allow_origins=["allowOrigins"],
                    expose_headers=["exposeHeaders"],
                    max_age=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1c136eff3446d9856516dba04451bc1f5d976d9b812902431486215d125102e7)
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
            '''Whether you want to allow cookies or other credentials in requests to your function URL.

            The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-url-cors.html#cfn-lambda-url-cors-allowcredentials
            '''
            result = self._values.get("allow_credentials")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def allow_headers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The HTTP headers that origins can include in requests to your function URL.

            For example: ``Date`` , ``Keep-Alive`` , ``X-Custom-Header`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-url-cors.html#cfn-lambda-url-cors-allowheaders
            '''
            result = self._values.get("allow_headers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allow_methods(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The HTTP methods that are allowed when calling your function URL.

            For example: ``GET`` , ``POST`` , ``DELETE`` , or the wildcard character ( ``*`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-url-cors.html#cfn-lambda-url-cors-allowmethods
            '''
            result = self._values.get("allow_methods")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allow_origins(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The origins that can access your function URL.

            You can list any number of specific origins, separated by a comma. For example: ``https://www.example.com`` , ``http://localhost:60905`` .

            Alternatively, you can grant access to all origins with the wildcard character ( ``*`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-url-cors.html#cfn-lambda-url-cors-alloworigins
            '''
            result = self._values.get("allow_origins")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def expose_headers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The HTTP headers in your function response that you want to expose to origins that call your function URL.

            For example: ``Date`` , ``Keep-Alive`` , ``X-Custom-Header`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-url-cors.html#cfn-lambda-url-cors-exposeheaders
            '''
            result = self._values.get("expose_headers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def max_age(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of time, in seconds, that browsers can cache results of a preflight request.

            By default, this is set to ``0`` , which means the browser will not cache results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-url-cors.html#cfn-lambda-url-cors-maxage
            '''
            result = self._values.get("max_age")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CorsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "code_sha256": "codeSha256",
        "description": "description",
        "function_name": "functionName",
        "function_scaling_config": "functionScalingConfig",
        "provisioned_concurrency_config": "provisionedConcurrencyConfig",
        "runtime_policy": "runtimePolicy",
    },
)
class CfnVersionMixinProps:
    def __init__(
        self,
        *,
        code_sha256: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        function_name: typing.Optional[builtins.str] = None,
        function_scaling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVersionPropsMixin.FunctionScalingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        provisioned_concurrency_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVersionPropsMixin.ProvisionedConcurrencyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        runtime_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVersionPropsMixin.RuntimePolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnVersionPropsMixin.

        :param code_sha256: Only publish a version if the hash value matches the value that's specified. Use this option to avoid publishing a version if the function code has changed since you last updated it. Updates are not supported for this property.
        :param description: A description for the version to override the description in the function configuration. Updates are not supported for this property.
        :param function_name: The name or ARN of the Lambda function. **Name formats** - *Function name* - ``MyFunction`` . - *Function ARN* - ``arn:aws:lambda:us-west-2:123456789012:function:MyFunction`` . - *Partial ARN* - ``123456789012:function:MyFunction`` . The length constraint applies only to the full ARN. If you specify only the function name, it is limited to 64 characters in length.
        :param function_scaling_config: Configuration that defines the scaling behavior for a Lambda Managed Instances function, including the minimum and maximum number of execution environments that can be provisioned.
        :param provisioned_concurrency_config: Specifies a provisioned concurrency configuration for a function's version. Updates are not supported for this property.
        :param runtime_policy: Runtime Management Config of a function.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-version.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
            
            cfn_version_mixin_props = lambda_mixins.CfnVersionMixinProps(
                code_sha256="codeSha256",
                description="description",
                function_name="functionName",
                function_scaling_config=lambda_mixins.CfnVersionPropsMixin.FunctionScalingConfigProperty(
                    max_execution_environments=123,
                    min_execution_environments=123
                ),
                provisioned_concurrency_config=lambda_mixins.CfnVersionPropsMixin.ProvisionedConcurrencyConfigurationProperty(
                    provisioned_concurrent_executions=123
                ),
                runtime_policy=lambda_mixins.CfnVersionPropsMixin.RuntimePolicyProperty(
                    runtime_version_arn="runtimeVersionArn",
                    update_runtime_on="updateRuntimeOn"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67f8b3d64961eb47d653e961b17a16fc83e12dbf06d684a6e01e014838622265)
            check_type(argname="argument code_sha256", value=code_sha256, expected_type=type_hints["code_sha256"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument function_scaling_config", value=function_scaling_config, expected_type=type_hints["function_scaling_config"])
            check_type(argname="argument provisioned_concurrency_config", value=provisioned_concurrency_config, expected_type=type_hints["provisioned_concurrency_config"])
            check_type(argname="argument runtime_policy", value=runtime_policy, expected_type=type_hints["runtime_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if code_sha256 is not None:
            self._values["code_sha256"] = code_sha256
        if description is not None:
            self._values["description"] = description
        if function_name is not None:
            self._values["function_name"] = function_name
        if function_scaling_config is not None:
            self._values["function_scaling_config"] = function_scaling_config
        if provisioned_concurrency_config is not None:
            self._values["provisioned_concurrency_config"] = provisioned_concurrency_config
        if runtime_policy is not None:
            self._values["runtime_policy"] = runtime_policy

    @builtins.property
    def code_sha256(self) -> typing.Optional[builtins.str]:
        '''Only publish a version if the hash value matches the value that's specified.

        Use this option to avoid publishing a version if the function code has changed since you last updated it. Updates are not supported for this property.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-version.html#cfn-lambda-version-codesha256
        '''
        result = self._values.get("code_sha256")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the version to override the description in the function configuration.

        Updates are not supported for this property.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-version.html#cfn-lambda-version-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        '''The name or ARN of the Lambda function.

        **Name formats** - *Function name* - ``MyFunction`` .

        - *Function ARN* - ``arn:aws:lambda:us-west-2:123456789012:function:MyFunction`` .
        - *Partial ARN* - ``123456789012:function:MyFunction`` .

        The length constraint applies only to the full ARN. If you specify only the function name, it is limited to 64 characters in length.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-version.html#cfn-lambda-version-functionname
        '''
        result = self._values.get("function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def function_scaling_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVersionPropsMixin.FunctionScalingConfigProperty"]]:
        '''Configuration that defines the scaling behavior for a Lambda Managed Instances function, including the minimum and maximum number of execution environments that can be provisioned.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-version.html#cfn-lambda-version-functionscalingconfig
        '''
        result = self._values.get("function_scaling_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVersionPropsMixin.FunctionScalingConfigProperty"]], result)

    @builtins.property
    def provisioned_concurrency_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVersionPropsMixin.ProvisionedConcurrencyConfigurationProperty"]]:
        '''Specifies a provisioned concurrency configuration for a function's version.

        Updates are not supported for this property.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-version.html#cfn-lambda-version-provisionedconcurrencyconfig
        '''
        result = self._values.get("provisioned_concurrency_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVersionPropsMixin.ProvisionedConcurrencyConfigurationProperty"]], result)

    @builtins.property
    def runtime_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVersionPropsMixin.RuntimePolicyProperty"]]:
        '''Runtime Management Config of a function.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-version.html#cfn-lambda-version-runtimepolicy
        '''
        result = self._values.get("runtime_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVersionPropsMixin.RuntimePolicyProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnVersionPropsMixin",
):
    '''The ``AWS::Lambda::Version`` resource creates a `version <https://docs.aws.amazon.com/lambda/latest/dg/versioning-aliases.html>`_ from the current code and configuration of a function. Use versions to create a snapshot of your function code and configuration that doesn't change.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-version.html
    :cloudformationResource: AWS::Lambda::Version
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
        
        cfn_version_props_mixin = lambda_mixins.CfnVersionPropsMixin(lambda_mixins.CfnVersionMixinProps(
            code_sha256="codeSha256",
            description="description",
            function_name="functionName",
            function_scaling_config=lambda_mixins.CfnVersionPropsMixin.FunctionScalingConfigProperty(
                max_execution_environments=123,
                min_execution_environments=123
            ),
            provisioned_concurrency_config=lambda_mixins.CfnVersionPropsMixin.ProvisionedConcurrencyConfigurationProperty(
                provisioned_concurrent_executions=123
            ),
            runtime_policy=lambda_mixins.CfnVersionPropsMixin.RuntimePolicyProperty(
                runtime_version_arn="runtimeVersionArn",
                update_runtime_on="updateRuntimeOn"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lambda::Version``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dafc13931cfa8fcfc348a826aa5e32faee7c58cad164b67e37ddf4398b718acb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d27293759bb3491290fb03d2c8c50c5fa558e4dd32d314a032310ca56c4498d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c3a3309f63b7831ff4cf183854a9958f26818044d0fc1ba088b9eac9046f598)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVersionMixinProps:
        return typing.cast(CfnVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnVersionPropsMixin.FunctionScalingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_execution_environments": "maxExecutionEnvironments",
            "min_execution_environments": "minExecutionEnvironments",
        },
    )
    class FunctionScalingConfigProperty:
        def __init__(
            self,
            *,
            max_execution_environments: typing.Optional[jsii.Number] = None,
            min_execution_environments: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Configuration that defines the scaling behavior for a Lambda Managed Instances function, including the minimum and maximum number of execution environments that can be provisioned.

            :param max_execution_environments: The maximum number of execution environments that can be provisioned for the function.
            :param min_execution_environments: The minimum number of execution environments to maintain for the function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-version-functionscalingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                function_scaling_config_property = lambda_mixins.CfnVersionPropsMixin.FunctionScalingConfigProperty(
                    max_execution_environments=123,
                    min_execution_environments=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c958b30b7e0cfe3de83723817a2d13b6482dae4fb3e5b4f7a862a3c60f8d1e77)
                check_type(argname="argument max_execution_environments", value=max_execution_environments, expected_type=type_hints["max_execution_environments"])
                check_type(argname="argument min_execution_environments", value=min_execution_environments, expected_type=type_hints["min_execution_environments"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_execution_environments is not None:
                self._values["max_execution_environments"] = max_execution_environments
            if min_execution_environments is not None:
                self._values["min_execution_environments"] = min_execution_environments

        @builtins.property
        def max_execution_environments(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of execution environments that can be provisioned for the function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-version-functionscalingconfig.html#cfn-lambda-version-functionscalingconfig-maxexecutionenvironments
            '''
            result = self._values.get("max_execution_environments")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_execution_environments(self) -> typing.Optional[jsii.Number]:
            '''The minimum number of execution environments to maintain for the function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-version-functionscalingconfig.html#cfn-lambda-version-functionscalingconfig-minexecutionenvironments
            '''
            result = self._values.get("min_execution_environments")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionScalingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnVersionPropsMixin.ProvisionedConcurrencyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "provisioned_concurrent_executions": "provisionedConcurrentExecutions",
        },
    )
    class ProvisionedConcurrencyConfigurationProperty:
        def __init__(
            self,
            *,
            provisioned_concurrent_executions: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A `provisioned concurrency <https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html>`_ configuration for a function's version.

            :param provisioned_concurrent_executions: The amount of provisioned concurrency to allocate for the version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-version-provisionedconcurrencyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                provisioned_concurrency_configuration_property = lambda_mixins.CfnVersionPropsMixin.ProvisionedConcurrencyConfigurationProperty(
                    provisioned_concurrent_executions=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6dd02a8163bd152b19e1f8abf1c41f1e6b83b6220e63f05ecb6cdb842ec58c5e)
                check_type(argname="argument provisioned_concurrent_executions", value=provisioned_concurrent_executions, expected_type=type_hints["provisioned_concurrent_executions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if provisioned_concurrent_executions is not None:
                self._values["provisioned_concurrent_executions"] = provisioned_concurrent_executions

        @builtins.property
        def provisioned_concurrent_executions(self) -> typing.Optional[jsii.Number]:
            '''The amount of provisioned concurrency to allocate for the version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-version-provisionedconcurrencyconfiguration.html#cfn-lambda-version-provisionedconcurrencyconfiguration-provisionedconcurrentexecutions
            '''
            result = self._values.get("provisioned_concurrent_executions")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisionedConcurrencyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lambda.mixins.CfnVersionPropsMixin.RuntimePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "runtime_version_arn": "runtimeVersionArn",
            "update_runtime_on": "updateRuntimeOn",
        },
    )
    class RuntimePolicyProperty:
        def __init__(
            self,
            *,
            runtime_version_arn: typing.Optional[builtins.str] = None,
            update_runtime_on: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Sets the runtime management configuration for a function's version.

            For more information, see `Runtime updates <https://docs.aws.amazon.com/lambda/latest/dg/runtimes-update.html>`_ .

            :param runtime_version_arn: The ARN of the runtime version you want the function to use. .. epigraph:: This is only required if you're using the *Manual* runtime update mode.
            :param update_runtime_on: Specify the runtime update mode. - *Auto (default)* - Automatically update to the most recent and secure runtime version using a `Two-phase runtime version rollout <https://docs.aws.amazon.com/lambda/latest/dg/runtimes-update.html#runtime-management-two-phase>`_ . This is the best choice for most customers to ensure they always benefit from runtime updates. - *FunctionUpdate* - Lambda updates the runtime of you function to the most recent and secure runtime version when you update your function. This approach synchronizes runtime updates with function deployments, giving you control over when runtime updates are applied and allowing you to detect and mitigate rare runtime update incompatibilities early. When using this setting, you need to regularly update your functions to keep their runtime up-to-date. - *Manual* - You specify a runtime version in your function configuration. The function will use this runtime version indefinitely. In the rare case where a new runtime version is incompatible with an existing function, this allows you to roll back your function to an earlier runtime version. For more information, see `Roll back a runtime version <https://docs.aws.amazon.com/lambda/latest/dg/runtimes-update.html#runtime-management-rollback>`_ . *Valid Values* : ``Auto`` | ``FunctionUpdate`` | ``Manual``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-version-runtimepolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lambda import mixins as lambda_mixins
                
                runtime_policy_property = lambda_mixins.CfnVersionPropsMixin.RuntimePolicyProperty(
                    runtime_version_arn="runtimeVersionArn",
                    update_runtime_on="updateRuntimeOn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f3b6c60e371e400cd9ce4f25ee89dd6d66fc4a74c4ffb0ed8d67ad3518393fa1)
                check_type(argname="argument runtime_version_arn", value=runtime_version_arn, expected_type=type_hints["runtime_version_arn"])
                check_type(argname="argument update_runtime_on", value=update_runtime_on, expected_type=type_hints["update_runtime_on"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if runtime_version_arn is not None:
                self._values["runtime_version_arn"] = runtime_version_arn
            if update_runtime_on is not None:
                self._values["update_runtime_on"] = update_runtime_on

        @builtins.property
        def runtime_version_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the runtime version you want the function to use.

            .. epigraph::

               This is only required if you're using the *Manual* runtime update mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-version-runtimepolicy.html#cfn-lambda-version-runtimepolicy-runtimeversionarn
            '''
            result = self._values.get("runtime_version_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def update_runtime_on(self) -> typing.Optional[builtins.str]:
            '''Specify the runtime update mode.

            - *Auto (default)* - Automatically update to the most recent and secure runtime version using a `Two-phase runtime version rollout <https://docs.aws.amazon.com/lambda/latest/dg/runtimes-update.html#runtime-management-two-phase>`_ . This is the best choice for most customers to ensure they always benefit from runtime updates.
            - *FunctionUpdate* - Lambda updates the runtime of you function to the most recent and secure runtime version when you update your function. This approach synchronizes runtime updates with function deployments, giving you control over when runtime updates are applied and allowing you to detect and mitigate rare runtime update incompatibilities early. When using this setting, you need to regularly update your functions to keep their runtime up-to-date.
            - *Manual* - You specify a runtime version in your function configuration. The function will use this runtime version indefinitely. In the rare case where a new runtime version is incompatible with an existing function, this allows you to roll back your function to an earlier runtime version. For more information, see `Roll back a runtime version <https://docs.aws.amazon.com/lambda/latest/dg/runtimes-update.html#runtime-management-rollback>`_ .

            *Valid Values* : ``Auto`` | ``FunctionUpdate`` | ``Manual``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-version-runtimepolicy.html#cfn-lambda-version-runtimepolicy-updateruntimeon
            '''
            result = self._values.get("update_runtime_on")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuntimePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAliasMixinProps",
    "CfnAliasPropsMixin",
    "CfnCapacityProviderMixinProps",
    "CfnCapacityProviderPropsMixin",
    "CfnCodeSigningConfigMixinProps",
    "CfnCodeSigningConfigPropsMixin",
    "CfnEventInvokeConfigMixinProps",
    "CfnEventInvokeConfigPropsMixin",
    "CfnEventSourceMappingMixinProps",
    "CfnEventSourceMappingPropsMixin",
    "CfnFunctionMixinProps",
    "CfnFunctionPropsMixin",
    "CfnLayerVersionMixinProps",
    "CfnLayerVersionPermissionMixinProps",
    "CfnLayerVersionPermissionPropsMixin",
    "CfnLayerVersionPropsMixin",
    "CfnPermissionMixinProps",
    "CfnPermissionPropsMixin",
    "CfnUrlMixinProps",
    "CfnUrlPropsMixin",
    "CfnVersionMixinProps",
    "CfnVersionPropsMixin",
]

publication.publish()

def _typecheckingstub__08289c831cc94cd4f9e909f776b089700d48d82c01234ad5eba7e0ca7dd7f19c(
    *,
    description: typing.Optional[builtins.str] = None,
    function_name: typing.Optional[builtins.str] = None,
    function_version: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    provisioned_concurrency_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAliasPropsMixin.ProvisionedConcurrencyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    routing_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAliasPropsMixin.AliasRoutingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a54440f0c53832f71757a618d3f999a2968f01e81980177b7656dead70cc806b(
    props: typing.Union[CfnAliasMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6ff16e7cf48fa81820d553cd5441c88d951bab6839f51cdb9e8967cf034f603(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22de2b5069bd82b895be1d5b4dfc5523054f644c6834b49148758bc3a90e1970(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466208344a63929a00d35184b5f541d8b6e8e90f0f680a30489d46657fa62d84(
    *,
    additional_version_weights: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAliasPropsMixin.VersionWeightProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0397bb9428f7d2d85a6d20c0f2e2df1db82a7ea675e6514fed4019b4cd5443a(
    *,
    provisioned_concurrent_executions: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5417cb45df34acafd624da5caa5c4620a0cbb1a3eeac749353a8d4b6a66ffda1(
    *,
    function_version: typing.Optional[builtins.str] = None,
    function_weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0cf4c5f1b15ef6daf34810cec04480713c883ab720107d6e2d4fb674f5f4cb9(
    *,
    capacity_provider_name: typing.Optional[builtins.str] = None,
    capacity_provider_scaling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCapacityProviderPropsMixin.CapacityProviderScalingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_requirements: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCapacityProviderPropsMixin.InstanceRequirementsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    permissions_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCapacityProviderPropsMixin.CapacityProviderPermissionsConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCapacityProviderPropsMixin.CapacityProviderVpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b57773093eaa04517d6be2d86a204e798caea634d9dbafccaf95755bf0e696f(
    props: typing.Union[CfnCapacityProviderMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ddaccfb7ac1a6259a7f9d804fe6be20d7303c79b730e8432160925832c892ba(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0eb2d39813c111bb24aa9fcca013f7643aabdc94516c7463102cfaeb28045c2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3c23fb87e4860897397259e7b88b4775d25aa18ee00b83b7b37f4d257d6879(
    *,
    capacity_provider_operator_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b7f8a39b8a929aa1aa46f573d2c04d459dda523ee478d2fe9906965f5dea13f(
    *,
    max_v_cpu_count: typing.Optional[jsii.Number] = None,
    scaling_mode: typing.Optional[builtins.str] = None,
    scaling_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCapacityProviderPropsMixin.TargetTrackingScalingPolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73476f5f83d5da533b4a96ceba7bf5a04d68cbefe28af58a70208012c459e437(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b557b06e502b8b177d44b05c8ed91db2bb7cdbfe55c8d2757831f96e62685cd4(
    *,
    allowed_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
    excluded_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c043bf47a78dc48e0769be8d6e8be42ef0d39e34475e34a902d0ab3142ada2be(
    *,
    predefined_metric_type: typing.Optional[builtins.str] = None,
    target_value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ebb82706cbc7d48ddb8df5ae08f3c1600288f23efea22ed2abe3d7d7b104485(
    *,
    allowed_publishers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCodeSigningConfigPropsMixin.AllowedPublishersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    code_signing_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCodeSigningConfigPropsMixin.CodeSigningPoliciesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d8028b502c61f06980e8317e4860fc415411379a58d6477ad25752871d2526(
    props: typing.Union[CfnCodeSigningConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbdcf3f8ebeeced197040326770db2e4ef041701421eb78101e254e2b5d99a7d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ca778445bfc62a0f0a74c04d9d5d502cba921fdc25d4a08dfc48a2c4362c6b1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f16c6a033619b2b180de74937420bdb1c2ae6be04d056972dc2f657c82786785(
    *,
    signing_profile_version_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbb72c2dd898878bdf2ed22238154b8bf1619aaf205c4330a54f7dff11ebe37a(
    *,
    untrusted_artifact_on_deployment: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a4676ea89f7d1115c3b9d96b9c9a1ba1879bc9128bfbcaff30200be66f3cff(
    *,
    destination_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventInvokeConfigPropsMixin.DestinationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    function_name: typing.Optional[builtins.str] = None,
    maximum_event_age_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
    qualifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a318025e7c3b15462fa20792985d52c705641c1f96b84105de95a42264227f02(
    props: typing.Union[CfnEventInvokeConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__124874c0567e8f5c47530a30115017f9f55391edcda17cbde357fec6116058e0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd74f9bd377d333d24804e5c60c431a91c387211a3051496b3afb0a1353b515e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c2772492abadfb939ed6612df29bdf04b0592598d1fa88896b61e87b5a7fca1(
    *,
    on_failure: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventInvokeConfigPropsMixin.OnFailureProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    on_success: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventInvokeConfigPropsMixin.OnSuccessProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd418fa3a6731285f539fbf0f7da211347b466350b4f228bec33ccf5a8021a4(
    *,
    destination: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b0c0a79ed3d5e4b1e08c2daac73a36d8be9be4a8ff0cd5d2febbc5eacfd7b6e(
    *,
    destination: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3651a8aaa3f9ebdaa199a9708d570432aa9e54d5f39512bce458df8a84b76999(
    *,
    amazon_managed_kafka_event_source_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventSourceMappingPropsMixin.AmazonManagedKafkaEventSourceConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    batch_size: typing.Optional[jsii.Number] = None,
    bisect_batch_on_function_error: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    destination_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventSourceMappingPropsMixin.DestinationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    document_db_event_source_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventSourceMappingPropsMixin.DocumentDBEventSourceConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    event_source_arn: typing.Optional[builtins.str] = None,
    filter_criteria: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventSourceMappingPropsMixin.FilterCriteriaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    function_name: typing.Optional[builtins.str] = None,
    function_response_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    logging_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventSourceMappingPropsMixin.LoggingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
    metrics_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventSourceMappingPropsMixin.MetricsConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
    provisioned_poller_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventSourceMappingPropsMixin.ProvisionedPollerConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    queues: typing.Optional[typing.Sequence[builtins.str]] = None,
    scaling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventSourceMappingPropsMixin.ScalingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    self_managed_event_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventSourceMappingPropsMixin.SelfManagedEventSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    self_managed_kafka_event_source_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventSourceMappingPropsMixin.SelfManagedKafkaEventSourceConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_access_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventSourceMappingPropsMixin.SourceAccessConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    starting_position: typing.Optional[builtins.str] = None,
    starting_position_timestamp: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    topics: typing.Optional[typing.Sequence[builtins.str]] = None,
    tumbling_window_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f76000eee7701dbf527e107c9a8a89c610a77fd9068ea05bff861cf867110099(
    props: typing.Union[CfnEventSourceMappingMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c031629768dda22e010d1942ce617c71aa22463d0bbb1a461672f188abe799(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b60fefa766362cc0c416fa583cc7fde8d8f07826ebe0a0d228493f6bf78ca9a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1faa149851617d2bd03a7c53588fb19bab764e6bf71bb18f52582666755c8c21(
    *,
    consumer_group_id: typing.Optional[builtins.str] = None,
    schema_registry_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventSourceMappingPropsMixin.SchemaRegistryConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81baf50d08b1aeaf1d4541bb5a849005cc0bdbb6a8fdc2b9c969f0ba86f13c05(
    *,
    on_failure: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventSourceMappingPropsMixin.OnFailureProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a17b7a278cfae90a30dd3f76995be1c2a036bf5c0d25ca0e4c3e44e1c4496bc3(
    *,
    collection_name: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    full_document: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec58e8e328a41c4cbd74d1fb218abda9e5a389291e2342418e75ba9dee04c3e(
    *,
    kafka_bootstrap_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e41ea139482d0935756439fa42d7b5dcd3a1a08153521f55003e8f0e8fce283(
    *,
    filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventSourceMappingPropsMixin.FilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa21c548bffd47cd2d2d016d3e511d6af3bd1d0d85f034dbb0a49e8a2080c758(
    *,
    pattern: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__404cef2da0edb20fb1e474e8716f13ee7da6e9c367b987a59ceef1aa3022ea0c(
    *,
    system_log_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__807b050bd95bb8a3d2051cfd59e3856e0099c147c0f81cc419be5d432f6c66f8(
    *,
    metrics: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ad5e62166acc899251c077195157e0445e8a9e95185476c1b2559086560c27(
    *,
    destination: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e58a6cb75cbb156572c5e657332157f2b1465f0fd252ec59b8d9d8e48aebbd9(
    *,
    maximum_pollers: typing.Optional[jsii.Number] = None,
    minimum_pollers: typing.Optional[jsii.Number] = None,
    poller_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac85acb2e5b3a166ce34a555ed989e69abe4b882f9111b9394d2b1864f1a4c1b(
    *,
    maximum_concurrency: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ebcaec7601a7cb431284ce359eb8b28468c8d977bf335c622b8c013700040fd(
    *,
    type: typing.Optional[builtins.str] = None,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb021f6f174dd6341a0a3a5acdbe47f57d0eee38f4990ad4c661e78547d3a613(
    *,
    access_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventSourceMappingPropsMixin.SchemaRegistryAccessConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    event_record_format: typing.Optional[builtins.str] = None,
    schema_registry_uri: typing.Optional[builtins.str] = None,
    schema_validation_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventSourceMappingPropsMixin.SchemaValidationConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a634722c1fdd087ea9f0825307404d17d3da0592da5c1aa187b000f6a7a77d28(
    *,
    attribute: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f68ed610d8058095e7ee62c779e12192c33287d1ceeb6dad9c48ff84a170635b(
    *,
    endpoints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventSourceMappingPropsMixin.EndpointsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7924f708028888eca5e1d5bc625bebc6ae6e7f3b0e8b491acbc4db9e77cc8800(
    *,
    consumer_group_id: typing.Optional[builtins.str] = None,
    schema_registry_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventSourceMappingPropsMixin.SchemaRegistryConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a43dde8d7736ff862142afb31a03bcb960256fc5ac1dc29552eabf9ab79cd1c(
    *,
    type: typing.Optional[builtins.str] = None,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0081ae7cb2352db284c15bdfee27f535eb56cc8272589b1aa67dce99dce5fe4(
    *,
    architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
    capacity_provider_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.CapacityProviderConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    code: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.CodeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    code_signing_config_arn: typing.Optional[builtins.str] = None,
    dead_letter_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.DeadLetterConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    durable_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.DurableConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    environment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.EnvironmentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ephemeral_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.EphemeralStorageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    file_system_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.FileSystemConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    function_name: typing.Optional[builtins.str] = None,
    function_scaling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.FunctionScalingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    handler: typing.Optional[builtins.str] = None,
    image_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.ImageConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    layers: typing.Optional[typing.Sequence[builtins.str]] = None,
    logging_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.LoggingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    package_type: typing.Optional[builtins.str] = None,
    publish_to_latest_published: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    recursive_loop: typing.Optional[builtins.str] = None,
    reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
    role: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[builtins.str] = None,
    runtime_management_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.RuntimeManagementConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    snap_start: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.SnapStartProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    tenancy_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.TenancyConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    tracing_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.TracingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f16a781f0389d172f38be2ba1f79a13a4aae3fddf099e1b4c369431f865cf152(
    props: typing.Union[CfnFunctionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2223309c221f3e73c5050476cc9697ba54dd4772d30d58489a2f93a5159eaea(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d5617135fad9f8621f8a11b053501adafc4990c56284291e3bc1818bc94041(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a6eacf2d56ef3626f1f8caa4b8a9f0f18f6a5161965eb253081e36ffb312305(
    *,
    lambda_managed_instances_capacity_provider_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFunctionPropsMixin.LambdaManagedInstancesCapacityProviderConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc26a099931c9b92ca429e69136417b8c54924bcc48e1b290df5a98fefa17a5(
    *,
    image_uri: typing.Optional[builtins.str] = None,
    s3_bucket: typing.Optional[builtins.str] = None,
    s3_key: typing.Optional[builtins.str] = None,
    s3_object_version: typing.Optional[builtins.str] = None,
    source_kms_key_arn: typing.Optional[builtins.str] = None,
    zip_file: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4965ae8ef5b972ae7d008c2c09ba37e18857b9a4831cd3d0a7ab4fa8f10a5a2c(
    *,
    target_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f642c60c21e0eb6f37d03586065f526e5933a062c04f4b2f0c1ee270dccb6637(
    *,
    execution_timeout: typing.Optional[jsii.Number] = None,
    retention_period_in_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ce2cd543064df87d811c57c4905266d4811fd5acfa6fc6fed7395f675076ef(
    *,
    variables: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26de07fd8ef9c744dfacfb3637e5534dcbe8bc6bdf2258e9e1f5c9615c945c34(
    *,
    size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86a7d67389b5759657747d4b3ca5565d7f0cf0a384026ce7980cc55c8b706caf(
    *,
    arn: typing.Optional[builtins.str] = None,
    local_mount_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e68d67260a81b197e198d213f4392df03cb856a3a6fb0303a73a52c7c71d711e(
    *,
    max_execution_environments: typing.Optional[jsii.Number] = None,
    min_execution_environments: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f0925b5831d50be91a3a0f00e107544d8d60c7c8b6f6fe35413640d9790ac6(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    entry_point: typing.Optional[typing.Sequence[builtins.str]] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62816e128f322d9bfa7db0e2bf8f05107fe4e524978125be6403879489f23403(
    *,
    capacity_provider_arn: typing.Optional[builtins.str] = None,
    execution_environment_memory_gib_per_v_cpu: typing.Optional[jsii.Number] = None,
    per_execution_environment_max_concurrency: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6adbe4bc817f0dad8a9718ec9b8f86eb625c8a25998463ef750b2e800c254903(
    *,
    application_log_level: typing.Optional[builtins.str] = None,
    log_format: typing.Optional[builtins.str] = None,
    log_group: typing.Optional[builtins.str] = None,
    system_log_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93982a67fb081c808c8dd573b7cbbc814133cb00bdb677d3b0d66835be2fb5d8(
    *,
    runtime_version_arn: typing.Optional[builtins.str] = None,
    update_runtime_on: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44d514fa59f4a6406084ba589f5d0521a7b4370ac0d6819a604040a8b0dc0eb0(
    *,
    apply_on: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73878e81d01e28f332ec74e63f7faafae3cf551362e9e3ce10eb842aa715b081(
    *,
    apply_on: typing.Optional[builtins.str] = None,
    optimization_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__795a4838660d1fcb938a62756dc56f81aef5bc484d83e4d648da265648220307(
    *,
    tenant_isolation_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc3f72be563484986171e5649dce4e8ea5f8af3920c8b4af0798e37dce7f6f12(
    *,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59106bddbe5a22aa6e0d19e653a6e4920d37c34898af8e443d7c80941f40a3ed(
    *,
    ipv6_allowed_for_dual_stack: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a86a417b02bbd1c5d8f1b46653a01c49cccf0d55e84331b296fc9800f25b36ff(
    *,
    compatible_architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
    compatible_runtimes: typing.Optional[typing.Sequence[builtins.str]] = None,
    content: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLayerVersionPropsMixin.ContentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    layer_name: typing.Optional[builtins.str] = None,
    license_info: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1670500895f6c87af20ad2a0bbfdb73a184167597e4b2e6ae90c584726e0ab2(
    *,
    action: typing.Optional[builtins.str] = None,
    layer_version_arn: typing.Optional[builtins.str] = None,
    organization_id: typing.Optional[builtins.str] = None,
    principal: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__592633b235d749284213e4af07bc4eafeee0086617c257d6c160d63038bb3af8(
    props: typing.Union[CfnLayerVersionPermissionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__608976824d323a0c8d4f6e995c877ecf2f995b7405f10398cf048f050b8a9e17(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e763dbfcb57c6ae0a3b1312ff4c0639da9d98c4271c98a5b7d76b9abcfeb2568(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb6094413ad011e73710d7253c65215768548db6cf0489159b0819606f9c8453(
    props: typing.Union[CfnLayerVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b74fbc777a8c483f9bca7c0202131d70ace01b66134e24c0850609c221520024(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ae234beb02fe4cb8ffc94380a617605a5f7dd0770ac58030fcd41e51675436(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e41391063a3577270c20c4758a2cb7567c19f32cf2c3ad3ac7b3eef1ce3769(
    *,
    s3_bucket: typing.Optional[builtins.str] = None,
    s3_key: typing.Optional[builtins.str] = None,
    s3_object_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89586071974279e49a61674d471bfc7e62cfabfd32da17a273c10cfccd1de42f(
    *,
    action: typing.Optional[builtins.str] = None,
    event_source_token: typing.Optional[builtins.str] = None,
    function_name: typing.Optional[builtins.str] = None,
    function_url_auth_type: typing.Optional[builtins.str] = None,
    invoked_via_function_url: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    principal: typing.Optional[builtins.str] = None,
    principal_org_id: typing.Optional[builtins.str] = None,
    source_account: typing.Optional[builtins.str] = None,
    source_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f41790fa2854b31d2caf82ce3872b1d494c832e2b0fc884f1843393aca8e71(
    props: typing.Union[CfnPermissionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ba6c06e09def4a873df560c1dd5e96e37b4227d46d650e5c30f50ea3c7917bb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60335c93909da5a31777e91f31f92443d0ed53fed4b3d708c4fe753bf416c207(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4bfe5dc4bea6253fab30277a2ac0ea387cb89a2fd7f7639b40867d336d662c8(
    *,
    auth_type: typing.Optional[builtins.str] = None,
    cors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUrlPropsMixin.CorsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    invoke_mode: typing.Optional[builtins.str] = None,
    qualifier: typing.Optional[builtins.str] = None,
    target_function_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dca29365ffadb207aa16d462a498148bc0e370e3b6e264251acaf3ddc39bc28(
    props: typing.Union[CfnUrlMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8105d8cf410f42bc65a4be9fa20a33ab799e0b1c5ae4b5082e26e33a8117d23(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4897c85d2cfaebd029b3467431d69f2579aee3015c6dea2b90213299358edc42(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c136eff3446d9856516dba04451bc1f5d976d9b812902431486215d125102e7(
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

def _typecheckingstub__67f8b3d64961eb47d653e961b17a16fc83e12dbf06d684a6e01e014838622265(
    *,
    code_sha256: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    function_name: typing.Optional[builtins.str] = None,
    function_scaling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVersionPropsMixin.FunctionScalingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    provisioned_concurrency_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVersionPropsMixin.ProvisionedConcurrencyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    runtime_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVersionPropsMixin.RuntimePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dafc13931cfa8fcfc348a826aa5e32faee7c58cad164b67e37ddf4398b718acb(
    props: typing.Union[CfnVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d27293759bb3491290fb03d2c8c50c5fa558e4dd32d314a032310ca56c4498d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c3a3309f63b7831ff4cf183854a9958f26818044d0fc1ba088b9eac9046f598(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c958b30b7e0cfe3de83723817a2d13b6482dae4fb3e5b4f7a862a3c60f8d1e77(
    *,
    max_execution_environments: typing.Optional[jsii.Number] = None,
    min_execution_environments: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd02a8163bd152b19e1f8abf1c41f1e6b83b6220e63f05ecb6cdb842ec58c5e(
    *,
    provisioned_concurrent_executions: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3b6c60e371e400cd9ce4f25ee89dd6d66fc4a74c4ffb0ed8d67ad3518393fa1(
    *,
    runtime_version_arn: typing.Optional[builtins.str] = None,
    update_runtime_on: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
