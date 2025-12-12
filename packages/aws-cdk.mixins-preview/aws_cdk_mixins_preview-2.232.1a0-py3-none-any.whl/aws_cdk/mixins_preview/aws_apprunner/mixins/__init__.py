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
    jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnAutoScalingConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_scaling_configuration_name": "autoScalingConfigurationName",
        "max_concurrency": "maxConcurrency",
        "max_size": "maxSize",
        "min_size": "minSize",
        "tags": "tags",
    },
)
class CfnAutoScalingConfigurationMixinProps:
    def __init__(
        self,
        *,
        auto_scaling_configuration_name: typing.Optional[builtins.str] = None,
        max_concurrency: typing.Optional[jsii.Number] = None,
        max_size: typing.Optional[jsii.Number] = None,
        min_size: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAutoScalingConfigurationPropsMixin.

        :param auto_scaling_configuration_name: The customer-provided auto scaling configuration name. It can be used in multiple revisions of a configuration.
        :param max_concurrency: The maximum number of concurrent requests that an instance processes. If the number of concurrent requests exceeds this limit, App Runner scales the service up.
        :param max_size: The maximum number of instances that a service scales up to. At most ``MaxSize`` instances actively serve traffic for your service.
        :param min_size: The minimum number of instances that App Runner provisions for a service. The service always has at least ``MinSize`` provisioned instances. Some of them actively serve traffic. The rest of them (provisioned and inactive instances) are a cost-effective compute capacity reserve and are ready to be quickly activated. You pay for memory usage of all the provisioned instances. You pay for CPU usage of only the active subset. App Runner temporarily doubles the number of provisioned instances during deployments, to maintain the same capacity for both old and new code.
        :param tags: A list of metadata items that you can associate with your auto scaling configuration resource. A tag is a key-value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-autoscalingconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
            
            cfn_auto_scaling_configuration_mixin_props = apprunner_mixins.CfnAutoScalingConfigurationMixinProps(
                auto_scaling_configuration_name="autoScalingConfigurationName",
                max_concurrency=123,
                max_size=123,
                min_size=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48e07c8405ffedf48c4594ddd306b17ea5c7a43eec50a5e71c24cb14b7ba9af0)
            check_type(argname="argument auto_scaling_configuration_name", value=auto_scaling_configuration_name, expected_type=type_hints["auto_scaling_configuration_name"])
            check_type(argname="argument max_concurrency", value=max_concurrency, expected_type=type_hints["max_concurrency"])
            check_type(argname="argument max_size", value=max_size, expected_type=type_hints["max_size"])
            check_type(argname="argument min_size", value=min_size, expected_type=type_hints["min_size"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_scaling_configuration_name is not None:
            self._values["auto_scaling_configuration_name"] = auto_scaling_configuration_name
        if max_concurrency is not None:
            self._values["max_concurrency"] = max_concurrency
        if max_size is not None:
            self._values["max_size"] = max_size
        if min_size is not None:
            self._values["min_size"] = min_size
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def auto_scaling_configuration_name(self) -> typing.Optional[builtins.str]:
        '''The customer-provided auto scaling configuration name.

        It can be used in multiple revisions of a configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-autoscalingconfiguration.html#cfn-apprunner-autoscalingconfiguration-autoscalingconfigurationname
        '''
        result = self._values.get("auto_scaling_configuration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_concurrency(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of concurrent requests that an instance processes.

        If the number of concurrent requests exceeds this limit, App Runner scales the service up.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-autoscalingconfiguration.html#cfn-apprunner-autoscalingconfiguration-maxconcurrency
        '''
        result = self._values.get("max_concurrency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_size(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of instances that a service scales up to.

        At most ``MaxSize`` instances actively serve traffic for your service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-autoscalingconfiguration.html#cfn-apprunner-autoscalingconfiguration-maxsize
        '''
        result = self._values.get("max_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_size(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of instances that App Runner provisions for a service.

        The service always has at least ``MinSize`` provisioned instances. Some of them actively serve traffic. The rest of them (provisioned and inactive instances) are a cost-effective compute capacity reserve and are ready to be quickly activated. You pay for memory usage of all the provisioned instances. You pay for CPU usage of only the active subset.

        App Runner temporarily doubles the number of provisioned instances during deployments, to maintain the same capacity for both old and new code.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-autoscalingconfiguration.html#cfn-apprunner-autoscalingconfiguration-minsize
        '''
        result = self._values.get("min_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of metadata items that you can associate with your auto scaling configuration resource.

        A tag is a key-value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-autoscalingconfiguration.html#cfn-apprunner-autoscalingconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAutoScalingConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAutoScalingConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnAutoScalingConfigurationPropsMixin",
):
    '''Specify an AWS App Runner Automatic Scaling configuration by using the ``AWS::AppRunner::AutoScalingConfiguration`` resource in an AWS CloudFormation template.

    The ``AWS::AppRunner::AutoScalingConfiguration`` resource is an AWS App Runner resource type that specifies an App Runner automatic scaling configuration.

    App Runner requires this resource to set non-default auto scaling settings for instances used to process the web requests. You can share an auto scaling configuration across multiple services.

    Create multiple revisions of a configuration by calling this action multiple times using the same ``AutoScalingConfigurationName`` . The call returns incremental ``AutoScalingConfigurationRevision`` values. When you create a service and configure an auto scaling configuration resource, the service uses the latest active revision of the auto scaling configuration by default. You can optionally configure the service to use a specific revision.

    Configure a higher ``MinSize`` to increase the spread of your App Runner service over more Availability Zones in the AWS Region . The tradeoff is a higher minimal cost.

    Configure a lower ``MaxSize`` to control your cost. The tradeoff is lower responsiveness during peak demand.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-autoscalingconfiguration.html
    :cloudformationResource: AWS::AppRunner::AutoScalingConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
        
        cfn_auto_scaling_configuration_props_mixin = apprunner_mixins.CfnAutoScalingConfigurationPropsMixin(apprunner_mixins.CfnAutoScalingConfigurationMixinProps(
            auto_scaling_configuration_name="autoScalingConfigurationName",
            max_concurrency=123,
            max_size=123,
            min_size=123,
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
        props: typing.Union[CfnAutoScalingConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppRunner::AutoScalingConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__561bf753599b72bf50e1657bbc287cbc42e66db2414666e878ec37b9ddda6550)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0b58cfe5e8551b1f1ae67028d34d790733714156e27023bff9aefc57a9429fe)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc1a14d20c338b3ba9a02c4d3b26e9edad62b9e96708f3c02d44fb27b20d43f0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAutoScalingConfigurationMixinProps:
        return typing.cast(CfnAutoScalingConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnObservabilityConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "observability_configuration_name": "observabilityConfigurationName",
        "tags": "tags",
        "trace_configuration": "traceConfiguration",
    },
)
class CfnObservabilityConfigurationMixinProps:
    def __init__(
        self,
        *,
        observability_configuration_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        trace_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnObservabilityConfigurationPropsMixin.TraceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnObservabilityConfigurationPropsMixin.

        :param observability_configuration_name: A name for the observability configuration. When you use it for the first time in an AWS Region , App Runner creates revision number ``1`` of this name. When you use the same name in subsequent calls, App Runner creates incremental revisions of the configuration. .. epigraph:: The name ``DefaultConfiguration`` is reserved. You can't use it to create a new observability configuration, and you can't create a revision of it. When you want to use your own observability configuration for your App Runner service, *create a configuration with a different name* , and then provide it when you create or update your service. If you don't specify a name, CloudFormation generates a name for your observability configuration.
        :param tags: A list of metadata items that you can associate with your observability configuration resource. A tag is a key-value pair.
        :param trace_configuration: The configuration of the tracing feature within this observability configuration. If you don't specify it, App Runner doesn't enable tracing.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-observabilityconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
            
            cfn_observability_configuration_mixin_props = apprunner_mixins.CfnObservabilityConfigurationMixinProps(
                observability_configuration_name="observabilityConfigurationName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                trace_configuration=apprunner_mixins.CfnObservabilityConfigurationPropsMixin.TraceConfigurationProperty(
                    vendor="vendor"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08dd308a9678c7b688bbf346800cde12da3d61fe405478b9c9852d75388c3264)
            check_type(argname="argument observability_configuration_name", value=observability_configuration_name, expected_type=type_hints["observability_configuration_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument trace_configuration", value=trace_configuration, expected_type=type_hints["trace_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if observability_configuration_name is not None:
            self._values["observability_configuration_name"] = observability_configuration_name
        if tags is not None:
            self._values["tags"] = tags
        if trace_configuration is not None:
            self._values["trace_configuration"] = trace_configuration

    @builtins.property
    def observability_configuration_name(self) -> typing.Optional[builtins.str]:
        '''A name for the observability configuration.

        When you use it for the first time in an AWS Region , App Runner creates revision number ``1`` of this name. When you use the same name in subsequent calls, App Runner creates incremental revisions of the configuration.
        .. epigraph::

           The name ``DefaultConfiguration`` is reserved. You can't use it to create a new observability configuration, and you can't create a revision of it.

           When you want to use your own observability configuration for your App Runner service, *create a configuration with a different name* , and then provide it when you create or update your service.

        If you don't specify a name, CloudFormation generates a name for your observability configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-observabilityconfiguration.html#cfn-apprunner-observabilityconfiguration-observabilityconfigurationname
        '''
        result = self._values.get("observability_configuration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of metadata items that you can associate with your observability configuration resource.

        A tag is a key-value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-observabilityconfiguration.html#cfn-apprunner-observabilityconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def trace_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnObservabilityConfigurationPropsMixin.TraceConfigurationProperty"]]:
        '''The configuration of the tracing feature within this observability configuration.

        If you don't specify it, App Runner doesn't enable tracing.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-observabilityconfiguration.html#cfn-apprunner-observabilityconfiguration-traceconfiguration
        '''
        result = self._values.get("trace_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnObservabilityConfigurationPropsMixin.TraceConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnObservabilityConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnObservabilityConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnObservabilityConfigurationPropsMixin",
):
    '''Specify an AWS App Runner observability configuration by using the ``AWS::AppRunner::ObservabilityConfiguration`` resource in an AWS CloudFormation template.

    The ``AWS::AppRunner::ObservabilityConfiguration`` resource is an AWS App Runner resource type that specifies an App Runner observability configuration.

    App Runner requires this resource when you specify App Runner services and you want to enable non-default observability features. You can share an observability configuration across multiple services.

    Create multiple revisions of a configuration by specifying this resource multiple times using the same ``ObservabilityConfigurationName`` . App Runner creates multiple resources with incremental ``ObservabilityConfigurationRevision`` values. When you specify a service and configure an observability configuration resource, the service uses the latest active revision of the observability configuration by default. You can optionally configure the service to use a specific revision.

    The observability configuration resource is designed to configure multiple features (currently one feature, tracing). This resource takes optional parameters that describe the configuration of these features (currently one parameter, ``TraceConfiguration`` ). If you don't specify a feature parameter, App Runner doesn't enable the feature.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-observabilityconfiguration.html
    :cloudformationResource: AWS::AppRunner::ObservabilityConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
        
        cfn_observability_configuration_props_mixin = apprunner_mixins.CfnObservabilityConfigurationPropsMixin(apprunner_mixins.CfnObservabilityConfigurationMixinProps(
            observability_configuration_name="observabilityConfigurationName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            trace_configuration=apprunner_mixins.CfnObservabilityConfigurationPropsMixin.TraceConfigurationProperty(
                vendor="vendor"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnObservabilityConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppRunner::ObservabilityConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b564d02c1e0c6de0690420e0d3324e51bc887ebdfe6e9b423c545dd5492e197)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4aac092815cfeed29313598b83e606bd0e7dd62a6014ebe5e83822685a9d2836)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdcd4e4e0da6c4b8f2a0b1def2d2146363ddaa71a4b5a4dff74fecee8e990494)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnObservabilityConfigurationMixinProps:
        return typing.cast(CfnObservabilityConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnObservabilityConfigurationPropsMixin.TraceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"vendor": "vendor"},
    )
    class TraceConfigurationProperty:
        def __init__(self, *, vendor: typing.Optional[builtins.str] = None) -> None:
            '''Describes the configuration of the tracing feature within an AWS App Runner observability configuration.

            :param vendor: The implementation provider chosen for tracing App Runner services.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-observabilityconfiguration-traceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
                
                trace_configuration_property = apprunner_mixins.CfnObservabilityConfigurationPropsMixin.TraceConfigurationProperty(
                    vendor="vendor"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__63209d7f9534369862aed6a0082ff40f7b198bf02f72ff0174b5b6c1c70e1d9d)
                check_type(argname="argument vendor", value=vendor, expected_type=type_hints["vendor"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if vendor is not None:
                self._values["vendor"] = vendor

        @builtins.property
        def vendor(self) -> typing.Optional[builtins.str]:
            '''The implementation provider chosen for tracing App Runner services.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-observabilityconfiguration-traceconfiguration.html#cfn-apprunner-observabilityconfiguration-traceconfiguration-vendor
            '''
            result = self._values.get("vendor")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TraceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnServiceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_scaling_configuration_arn": "autoScalingConfigurationArn",
        "encryption_configuration": "encryptionConfiguration",
        "health_check_configuration": "healthCheckConfiguration",
        "instance_configuration": "instanceConfiguration",
        "network_configuration": "networkConfiguration",
        "observability_configuration": "observabilityConfiguration",
        "service_name": "serviceName",
        "source_configuration": "sourceConfiguration",
        "tags": "tags",
    },
)
class CfnServiceMixinProps:
    def __init__(
        self,
        *,
        auto_scaling_configuration_arn: typing.Optional[builtins.str] = None,
        encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.EncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        health_check_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.HealthCheckConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.InstanceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.NetworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        observability_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.ServiceObservabilityConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        service_name: typing.Optional[builtins.str] = None,
        source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.SourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnServicePropsMixin.

        :param auto_scaling_configuration_arn: The Amazon Resource Name (ARN) of an App Runner automatic scaling configuration resource that you want to associate with your service. If not provided, App Runner associates the latest revision of a default auto scaling configuration. Specify an ARN with a name and a revision number to associate that revision. For example: ``arn:aws:apprunner:us-east-1:123456789012:autoscalingconfiguration/high-availability/3`` Specify just the name to associate the latest revision. For example: ``arn:aws:apprunner:us-east-1:123456789012:autoscalingconfiguration/high-availability``
        :param encryption_configuration: An optional custom encryption key that App Runner uses to encrypt the copy of your source repository that it maintains and your service logs. By default, App Runner uses an AWS managed key .
        :param health_check_configuration: The settings for the health check that AWS App Runner performs to monitor the health of the App Runner service.
        :param instance_configuration: The runtime configuration of instances (scaling units) of your service.
        :param network_configuration: Configuration settings related to network traffic of the web application that the App Runner service runs.
        :param observability_configuration: The observability configuration of your service.
        :param service_name: A name for the App Runner service. It must be unique across all the running App Runner services in your AWS account in the AWS Region . If you don't specify a name, CloudFormation generates a name for your service.
        :param source_configuration: The source to deploy to the App Runner service. It can be a code or an image repository.
        :param tags: An optional list of metadata items that you can associate with the App Runner service resource. A tag is a key-value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
            
            cfn_service_mixin_props = apprunner_mixins.CfnServiceMixinProps(
                auto_scaling_configuration_arn="autoScalingConfigurationArn",
                encryption_configuration=apprunner_mixins.CfnServicePropsMixin.EncryptionConfigurationProperty(
                    kms_key="kmsKey"
                ),
                health_check_configuration=apprunner_mixins.CfnServicePropsMixin.HealthCheckConfigurationProperty(
                    healthy_threshold=123,
                    interval=123,
                    path="path",
                    protocol="protocol",
                    timeout=123,
                    unhealthy_threshold=123
                ),
                instance_configuration=apprunner_mixins.CfnServicePropsMixin.InstanceConfigurationProperty(
                    cpu="cpu",
                    instance_role_arn="instanceRoleArn",
                    memory="memory"
                ),
                network_configuration=apprunner_mixins.CfnServicePropsMixin.NetworkConfigurationProperty(
                    egress_configuration=apprunner_mixins.CfnServicePropsMixin.EgressConfigurationProperty(
                        egress_type="egressType",
                        vpc_connector_arn="vpcConnectorArn"
                    ),
                    ingress_configuration=apprunner_mixins.CfnServicePropsMixin.IngressConfigurationProperty(
                        is_publicly_accessible=False
                    ),
                    ip_address_type="ipAddressType"
                ),
                observability_configuration=apprunner_mixins.CfnServicePropsMixin.ServiceObservabilityConfigurationProperty(
                    observability_configuration_arn="observabilityConfigurationArn",
                    observability_enabled=False
                ),
                service_name="serviceName",
                source_configuration=apprunner_mixins.CfnServicePropsMixin.SourceConfigurationProperty(
                    authentication_configuration=apprunner_mixins.CfnServicePropsMixin.AuthenticationConfigurationProperty(
                        access_role_arn="accessRoleArn",
                        connection_arn="connectionArn"
                    ),
                    auto_deployments_enabled=False,
                    code_repository=apprunner_mixins.CfnServicePropsMixin.CodeRepositoryProperty(
                        code_configuration=apprunner_mixins.CfnServicePropsMixin.CodeConfigurationProperty(
                            code_configuration_values=apprunner_mixins.CfnServicePropsMixin.CodeConfigurationValuesProperty(
                                build_command="buildCommand",
                                port="port",
                                runtime="runtime",
                                runtime_environment_secrets=[apprunner_mixins.CfnServicePropsMixin.KeyValuePairProperty(
                                    name="name",
                                    value="value"
                                )],
                                runtime_environment_variables=[apprunner_mixins.CfnServicePropsMixin.KeyValuePairProperty(
                                    name="name",
                                    value="value"
                                )],
                                start_command="startCommand"
                            ),
                            configuration_source="configurationSource"
                        ),
                        repository_url="repositoryUrl",
                        source_code_version=apprunner_mixins.CfnServicePropsMixin.SourceCodeVersionProperty(
                            type="type",
                            value="value"
                        ),
                        source_directory="sourceDirectory"
                    ),
                    image_repository=apprunner_mixins.CfnServicePropsMixin.ImageRepositoryProperty(
                        image_configuration=apprunner_mixins.CfnServicePropsMixin.ImageConfigurationProperty(
                            port="port",
                            runtime_environment_secrets=[apprunner_mixins.CfnServicePropsMixin.KeyValuePairProperty(
                                name="name",
                                value="value"
                            )],
                            runtime_environment_variables=[apprunner_mixins.CfnServicePropsMixin.KeyValuePairProperty(
                                name="name",
                                value="value"
                            )],
                            start_command="startCommand"
                        ),
                        image_identifier="imageIdentifier",
                        image_repository_type="imageRepositoryType"
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a8931a11ba339adc4dcd3353638da53bcebb3b420eb391d893f61506e211fdd)
            check_type(argname="argument auto_scaling_configuration_arn", value=auto_scaling_configuration_arn, expected_type=type_hints["auto_scaling_configuration_arn"])
            check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
            check_type(argname="argument health_check_configuration", value=health_check_configuration, expected_type=type_hints["health_check_configuration"])
            check_type(argname="argument instance_configuration", value=instance_configuration, expected_type=type_hints["instance_configuration"])
            check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
            check_type(argname="argument observability_configuration", value=observability_configuration, expected_type=type_hints["observability_configuration"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument source_configuration", value=source_configuration, expected_type=type_hints["source_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_scaling_configuration_arn is not None:
            self._values["auto_scaling_configuration_arn"] = auto_scaling_configuration_arn
        if encryption_configuration is not None:
            self._values["encryption_configuration"] = encryption_configuration
        if health_check_configuration is not None:
            self._values["health_check_configuration"] = health_check_configuration
        if instance_configuration is not None:
            self._values["instance_configuration"] = instance_configuration
        if network_configuration is not None:
            self._values["network_configuration"] = network_configuration
        if observability_configuration is not None:
            self._values["observability_configuration"] = observability_configuration
        if service_name is not None:
            self._values["service_name"] = service_name
        if source_configuration is not None:
            self._values["source_configuration"] = source_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def auto_scaling_configuration_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of an App Runner automatic scaling configuration resource that you want to associate with your service.

        If not provided, App Runner associates the latest revision of a default auto scaling configuration.

        Specify an ARN with a name and a revision number to associate that revision. For example: ``arn:aws:apprunner:us-east-1:123456789012:autoscalingconfiguration/high-availability/3``

        Specify just the name to associate the latest revision. For example: ``arn:aws:apprunner:us-east-1:123456789012:autoscalingconfiguration/high-availability``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-autoscalingconfigurationarn
        '''
        result = self._values.get("auto_scaling_configuration_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.EncryptionConfigurationProperty"]]:
        '''An optional custom encryption key that App Runner uses to encrypt the copy of your source repository that it maintains and your service logs.

        By default, App Runner uses an AWS managed key .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-encryptionconfiguration
        '''
        result = self._values.get("encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.EncryptionConfigurationProperty"]], result)

    @builtins.property
    def health_check_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.HealthCheckConfigurationProperty"]]:
        '''The settings for the health check that AWS App Runner performs to monitor the health of the App Runner service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-healthcheckconfiguration
        '''
        result = self._values.get("health_check_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.HealthCheckConfigurationProperty"]], result)

    @builtins.property
    def instance_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.InstanceConfigurationProperty"]]:
        '''The runtime configuration of instances (scaling units) of your service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-instanceconfiguration
        '''
        result = self._values.get("instance_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.InstanceConfigurationProperty"]], result)

    @builtins.property
    def network_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.NetworkConfigurationProperty"]]:
        '''Configuration settings related to network traffic of the web application that the App Runner service runs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-networkconfiguration
        '''
        result = self._values.get("network_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.NetworkConfigurationProperty"]], result)

    @builtins.property
    def observability_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.ServiceObservabilityConfigurationProperty"]]:
        '''The observability configuration of your service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-observabilityconfiguration
        '''
        result = self._values.get("observability_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.ServiceObservabilityConfigurationProperty"]], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''A name for the App Runner service.

        It must be unique across all the running App Runner services in your AWS account in the AWS Region .

        If you don't specify a name, CloudFormation generates a name for your service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-servicename
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.SourceConfigurationProperty"]]:
        '''The source to deploy to the App Runner service.

        It can be a code or an image repository.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-sourceconfiguration
        '''
        result = self._values.get("source_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.SourceConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An optional list of metadata items that you can associate with the App Runner service resource.

        A tag is a key-value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html#cfn-apprunner-service-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnServicePropsMixin",
):
    '''Specify an AWS App Runner service by using the ``AWS::AppRunner::Service`` resource in an AWS CloudFormation template.

    The ``AWS::AppRunner::Service`` resource is an AWS App Runner resource type that specifies an App Runner service.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-service.html
    :cloudformationResource: AWS::AppRunner::Service
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
        
        cfn_service_props_mixin = apprunner_mixins.CfnServicePropsMixin(apprunner_mixins.CfnServiceMixinProps(
            auto_scaling_configuration_arn="autoScalingConfigurationArn",
            encryption_configuration=apprunner_mixins.CfnServicePropsMixin.EncryptionConfigurationProperty(
                kms_key="kmsKey"
            ),
            health_check_configuration=apprunner_mixins.CfnServicePropsMixin.HealthCheckConfigurationProperty(
                healthy_threshold=123,
                interval=123,
                path="path",
                protocol="protocol",
                timeout=123,
                unhealthy_threshold=123
            ),
            instance_configuration=apprunner_mixins.CfnServicePropsMixin.InstanceConfigurationProperty(
                cpu="cpu",
                instance_role_arn="instanceRoleArn",
                memory="memory"
            ),
            network_configuration=apprunner_mixins.CfnServicePropsMixin.NetworkConfigurationProperty(
                egress_configuration=apprunner_mixins.CfnServicePropsMixin.EgressConfigurationProperty(
                    egress_type="egressType",
                    vpc_connector_arn="vpcConnectorArn"
                ),
                ingress_configuration=apprunner_mixins.CfnServicePropsMixin.IngressConfigurationProperty(
                    is_publicly_accessible=False
                ),
                ip_address_type="ipAddressType"
            ),
            observability_configuration=apprunner_mixins.CfnServicePropsMixin.ServiceObservabilityConfigurationProperty(
                observability_configuration_arn="observabilityConfigurationArn",
                observability_enabled=False
            ),
            service_name="serviceName",
            source_configuration=apprunner_mixins.CfnServicePropsMixin.SourceConfigurationProperty(
                authentication_configuration=apprunner_mixins.CfnServicePropsMixin.AuthenticationConfigurationProperty(
                    access_role_arn="accessRoleArn",
                    connection_arn="connectionArn"
                ),
                auto_deployments_enabled=False,
                code_repository=apprunner_mixins.CfnServicePropsMixin.CodeRepositoryProperty(
                    code_configuration=apprunner_mixins.CfnServicePropsMixin.CodeConfigurationProperty(
                        code_configuration_values=apprunner_mixins.CfnServicePropsMixin.CodeConfigurationValuesProperty(
                            build_command="buildCommand",
                            port="port",
                            runtime="runtime",
                            runtime_environment_secrets=[apprunner_mixins.CfnServicePropsMixin.KeyValuePairProperty(
                                name="name",
                                value="value"
                            )],
                            runtime_environment_variables=[apprunner_mixins.CfnServicePropsMixin.KeyValuePairProperty(
                                name="name",
                                value="value"
                            )],
                            start_command="startCommand"
                        ),
                        configuration_source="configurationSource"
                    ),
                    repository_url="repositoryUrl",
                    source_code_version=apprunner_mixins.CfnServicePropsMixin.SourceCodeVersionProperty(
                        type="type",
                        value="value"
                    ),
                    source_directory="sourceDirectory"
                ),
                image_repository=apprunner_mixins.CfnServicePropsMixin.ImageRepositoryProperty(
                    image_configuration=apprunner_mixins.CfnServicePropsMixin.ImageConfigurationProperty(
                        port="port",
                        runtime_environment_secrets=[apprunner_mixins.CfnServicePropsMixin.KeyValuePairProperty(
                            name="name",
                            value="value"
                        )],
                        runtime_environment_variables=[apprunner_mixins.CfnServicePropsMixin.KeyValuePairProperty(
                            name="name",
                            value="value"
                        )],
                        start_command="startCommand"
                    ),
                    image_identifier="imageIdentifier",
                    image_repository_type="imageRepositoryType"
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
        props: typing.Union[CfnServiceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppRunner::Service``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99c6ff9ebb49a48c30cbbdda447fc221a61a952cff5b27ce6ea5966792a8423d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__469faf4819785e75048c51bc42a4f758b13e1a6c89d4c14b6ae959be509cfb4a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4c5c6c97f68d369818a8f927b0bc3d1eb260f01e259fc1cf79d775b70b6f43d)
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
        jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnServicePropsMixin.AuthenticationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_role_arn": "accessRoleArn",
            "connection_arn": "connectionArn",
        },
    )
    class AuthenticationConfigurationProperty:
        def __init__(
            self,
            *,
            access_role_arn: typing.Optional[builtins.str] = None,
            connection_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes resources needed to authenticate access to some source repositories.

            The specific resource depends on the repository provider.

            :param access_role_arn: The Amazon Resource Name (ARN) of the IAM role that grants the App Runner service access to a source repository. It's required for ECR image repositories (but not for ECR Public repositories).
            :param connection_arn: The Amazon Resource Name (ARN) of the App Runner connection that enables the App Runner service to connect to a source repository. It's required for GitHub code repositories.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-authenticationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
                
                authentication_configuration_property = apprunner_mixins.CfnServicePropsMixin.AuthenticationConfigurationProperty(
                    access_role_arn="accessRoleArn",
                    connection_arn="connectionArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ed6a7f1f2a0d6145638c6f37eb0ee04d0901a9a524c760181397a15a804fee09)
                check_type(argname="argument access_role_arn", value=access_role_arn, expected_type=type_hints["access_role_arn"])
                check_type(argname="argument connection_arn", value=connection_arn, expected_type=type_hints["connection_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_role_arn is not None:
                self._values["access_role_arn"] = access_role_arn
            if connection_arn is not None:
                self._values["connection_arn"] = connection_arn

        @builtins.property
        def access_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM role that grants the App Runner service access to a source repository.

            It's required for ECR image repositories (but not for ECR Public repositories).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-authenticationconfiguration.html#cfn-apprunner-service-authenticationconfiguration-accessrolearn
            '''
            result = self._values.get("access_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connection_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the App Runner connection that enables the App Runner service to connect to a source repository.

            It's required for GitHub code repositories.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-authenticationconfiguration.html#cfn-apprunner-service-authenticationconfiguration-connectionarn
            '''
            result = self._values.get("connection_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthenticationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnServicePropsMixin.CodeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "code_configuration_values": "codeConfigurationValues",
            "configuration_source": "configurationSource",
        },
    )
    class CodeConfigurationProperty:
        def __init__(
            self,
            *,
            code_configuration_values: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.CodeConfigurationValuesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            configuration_source: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the configuration that AWS App Runner uses to build and run an App Runner service from a source code repository.

            :param code_configuration_values: The basic configuration for building and running the App Runner service. Use it to quickly launch an App Runner service without providing a ``apprunner.yaml`` file in the source code repository (or ignoring the file if it exists).
            :param configuration_source: The source of the App Runner configuration. Values are interpreted as follows:. - ``REPOSITORY`` – App Runner reads configuration values from the ``apprunner.yaml`` file in the source code repository and ignores ``CodeConfigurationValues`` . - ``API`` – App Runner uses configuration values provided in ``CodeConfigurationValues`` and ignores the ``apprunner.yaml`` file in the source code repository.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-codeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
                
                code_configuration_property = apprunner_mixins.CfnServicePropsMixin.CodeConfigurationProperty(
                    code_configuration_values=apprunner_mixins.CfnServicePropsMixin.CodeConfigurationValuesProperty(
                        build_command="buildCommand",
                        port="port",
                        runtime="runtime",
                        runtime_environment_secrets=[apprunner_mixins.CfnServicePropsMixin.KeyValuePairProperty(
                            name="name",
                            value="value"
                        )],
                        runtime_environment_variables=[apprunner_mixins.CfnServicePropsMixin.KeyValuePairProperty(
                            name="name",
                            value="value"
                        )],
                        start_command="startCommand"
                    ),
                    configuration_source="configurationSource"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ebebda430b1ae185975f392390e190254540932c79f9cbef4500d090c29011dc)
                check_type(argname="argument code_configuration_values", value=code_configuration_values, expected_type=type_hints["code_configuration_values"])
                check_type(argname="argument configuration_source", value=configuration_source, expected_type=type_hints["configuration_source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code_configuration_values is not None:
                self._values["code_configuration_values"] = code_configuration_values
            if configuration_source is not None:
                self._values["configuration_source"] = configuration_source

        @builtins.property
        def code_configuration_values(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.CodeConfigurationValuesProperty"]]:
            '''The basic configuration for building and running the App Runner service.

            Use it to quickly launch an App Runner service without providing a ``apprunner.yaml`` file in the source code repository (or ignoring the file if it exists).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-codeconfiguration.html#cfn-apprunner-service-codeconfiguration-codeconfigurationvalues
            '''
            result = self._values.get("code_configuration_values")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.CodeConfigurationValuesProperty"]], result)

        @builtins.property
        def configuration_source(self) -> typing.Optional[builtins.str]:
            '''The source of the App Runner configuration. Values are interpreted as follows:.

            - ``REPOSITORY`` – App Runner reads configuration values from the ``apprunner.yaml`` file in the source code repository and ignores ``CodeConfigurationValues`` .
            - ``API`` – App Runner uses configuration values provided in ``CodeConfigurationValues`` and ignores the ``apprunner.yaml`` file in the source code repository.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-codeconfiguration.html#cfn-apprunner-service-codeconfiguration-configurationsource
            '''
            result = self._values.get("configuration_source")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnServicePropsMixin.CodeConfigurationValuesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "build_command": "buildCommand",
            "port": "port",
            "runtime": "runtime",
            "runtime_environment_secrets": "runtimeEnvironmentSecrets",
            "runtime_environment_variables": "runtimeEnvironmentVariables",
            "start_command": "startCommand",
        },
    )
    class CodeConfigurationValuesProperty:
        def __init__(
            self,
            *,
            build_command: typing.Optional[builtins.str] = None,
            port: typing.Optional[builtins.str] = None,
            runtime: typing.Optional[builtins.str] = None,
            runtime_environment_secrets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.KeyValuePairProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            runtime_environment_variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.KeyValuePairProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            start_command: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the basic configuration needed for building and running an AWS App Runner service.

            This type doesn't support the full set of possible configuration options. Fur full configuration capabilities, use a ``apprunner.yaml`` file in the source code repository.

            :param build_command: The command App Runner runs to build your application.
            :param port: The port that your application listens to in the container. Default: ``8080``
            :param runtime: A runtime environment type for building and running an App Runner service. It represents a programming language runtime.
            :param runtime_environment_secrets: An array of key-value pairs representing the secrets and parameters that get referenced to your service as an environment variable. The supported values are either the full Amazon Resource Name (ARN) of the AWS Secrets Manager secret or the full ARN of the parameter in the AWS Systems Manager Parameter Store. .. epigraph:: - If the AWS Systems Manager Parameter Store parameter exists in the same AWS Region as the service that you're launching, you can use either the full ARN or name of the secret. If the parameter exists in a different Region, then the full ARN must be specified. - Currently, cross account referencing of AWS Systems Manager Parameter Store parameter is not supported.
            :param runtime_environment_variables: The environment variables that are available to your running AWS App Runner service. An array of key-value pairs.
            :param start_command: The command App Runner runs to start your application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-codeconfigurationvalues.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
                
                code_configuration_values_property = apprunner_mixins.CfnServicePropsMixin.CodeConfigurationValuesProperty(
                    build_command="buildCommand",
                    port="port",
                    runtime="runtime",
                    runtime_environment_secrets=[apprunner_mixins.CfnServicePropsMixin.KeyValuePairProperty(
                        name="name",
                        value="value"
                    )],
                    runtime_environment_variables=[apprunner_mixins.CfnServicePropsMixin.KeyValuePairProperty(
                        name="name",
                        value="value"
                    )],
                    start_command="startCommand"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__79eb9d1f64d3c6959a4371962274f4f7f663b5907af6fe3f96b001875d55f46f)
                check_type(argname="argument build_command", value=build_command, expected_type=type_hints["build_command"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
                check_type(argname="argument runtime_environment_secrets", value=runtime_environment_secrets, expected_type=type_hints["runtime_environment_secrets"])
                check_type(argname="argument runtime_environment_variables", value=runtime_environment_variables, expected_type=type_hints["runtime_environment_variables"])
                check_type(argname="argument start_command", value=start_command, expected_type=type_hints["start_command"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if build_command is not None:
                self._values["build_command"] = build_command
            if port is not None:
                self._values["port"] = port
            if runtime is not None:
                self._values["runtime"] = runtime
            if runtime_environment_secrets is not None:
                self._values["runtime_environment_secrets"] = runtime_environment_secrets
            if runtime_environment_variables is not None:
                self._values["runtime_environment_variables"] = runtime_environment_variables
            if start_command is not None:
                self._values["start_command"] = start_command

        @builtins.property
        def build_command(self) -> typing.Optional[builtins.str]:
            '''The command App Runner runs to build your application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-codeconfigurationvalues.html#cfn-apprunner-service-codeconfigurationvalues-buildcommand
            '''
            result = self._values.get("build_command")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[builtins.str]:
            '''The port that your application listens to in the container.

            Default: ``8080``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-codeconfigurationvalues.html#cfn-apprunner-service-codeconfigurationvalues-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def runtime(self) -> typing.Optional[builtins.str]:
            '''A runtime environment type for building and running an App Runner service.

            It represents a programming language runtime.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-codeconfigurationvalues.html#cfn-apprunner-service-codeconfigurationvalues-runtime
            '''
            result = self._values.get("runtime")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def runtime_environment_secrets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.KeyValuePairProperty"]]]]:
            '''An array of key-value pairs representing the secrets and parameters that get referenced to your service as an environment variable.

            The supported values are either the full Amazon Resource Name (ARN) of the AWS Secrets Manager secret or the full ARN of the parameter in the AWS Systems Manager Parameter Store.
            .. epigraph::

               - If the AWS Systems Manager Parameter Store parameter exists in the same AWS Region as the service that you're launching, you can use either the full ARN or name of the secret. If the parameter exists in a different Region, then the full ARN must be specified.
               - Currently, cross account referencing of AWS Systems Manager Parameter Store parameter is not supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-codeconfigurationvalues.html#cfn-apprunner-service-codeconfigurationvalues-runtimeenvironmentsecrets
            '''
            result = self._values.get("runtime_environment_secrets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.KeyValuePairProperty"]]]], result)

        @builtins.property
        def runtime_environment_variables(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.KeyValuePairProperty"]]]]:
            '''The environment variables that are available to your running AWS App Runner service.

            An array of key-value pairs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-codeconfigurationvalues.html#cfn-apprunner-service-codeconfigurationvalues-runtimeenvironmentvariables
            '''
            result = self._values.get("runtime_environment_variables")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.KeyValuePairProperty"]]]], result)

        @builtins.property
        def start_command(self) -> typing.Optional[builtins.str]:
            '''The command App Runner runs to start your application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-codeconfigurationvalues.html#cfn-apprunner-service-codeconfigurationvalues-startcommand
            '''
            result = self._values.get("start_command")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeConfigurationValuesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnServicePropsMixin.CodeRepositoryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "code_configuration": "codeConfiguration",
            "repository_url": "repositoryUrl",
            "source_code_version": "sourceCodeVersion",
            "source_directory": "sourceDirectory",
        },
    )
    class CodeRepositoryProperty:
        def __init__(
            self,
            *,
            code_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.CodeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            repository_url: typing.Optional[builtins.str] = None,
            source_code_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.SourceCodeVersionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            source_directory: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a source code repository.

            :param code_configuration: Configuration for building and running the service from a source code repository. .. epigraph:: ``CodeConfiguration`` is required only for ``CreateService`` request.
            :param repository_url: The location of the repository that contains the source code.
            :param source_code_version: The version that should be used within the source code repository.
            :param source_directory: The path of the directory that stores source code and configuration files. The build and start commands also execute from here. The path is absolute from root and, if not specified, defaults to the repository root.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-coderepository.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
                
                code_repository_property = apprunner_mixins.CfnServicePropsMixin.CodeRepositoryProperty(
                    code_configuration=apprunner_mixins.CfnServicePropsMixin.CodeConfigurationProperty(
                        code_configuration_values=apprunner_mixins.CfnServicePropsMixin.CodeConfigurationValuesProperty(
                            build_command="buildCommand",
                            port="port",
                            runtime="runtime",
                            runtime_environment_secrets=[apprunner_mixins.CfnServicePropsMixin.KeyValuePairProperty(
                                name="name",
                                value="value"
                            )],
                            runtime_environment_variables=[apprunner_mixins.CfnServicePropsMixin.KeyValuePairProperty(
                                name="name",
                                value="value"
                            )],
                            start_command="startCommand"
                        ),
                        configuration_source="configurationSource"
                    ),
                    repository_url="repositoryUrl",
                    source_code_version=apprunner_mixins.CfnServicePropsMixin.SourceCodeVersionProperty(
                        type="type",
                        value="value"
                    ),
                    source_directory="sourceDirectory"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__912c48654e20ac3981d2d68010fa9aa433a1bade03f4f20516bde4410048c1da)
                check_type(argname="argument code_configuration", value=code_configuration, expected_type=type_hints["code_configuration"])
                check_type(argname="argument repository_url", value=repository_url, expected_type=type_hints["repository_url"])
                check_type(argname="argument source_code_version", value=source_code_version, expected_type=type_hints["source_code_version"])
                check_type(argname="argument source_directory", value=source_directory, expected_type=type_hints["source_directory"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code_configuration is not None:
                self._values["code_configuration"] = code_configuration
            if repository_url is not None:
                self._values["repository_url"] = repository_url
            if source_code_version is not None:
                self._values["source_code_version"] = source_code_version
            if source_directory is not None:
                self._values["source_directory"] = source_directory

        @builtins.property
        def code_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.CodeConfigurationProperty"]]:
            '''Configuration for building and running the service from a source code repository.

            .. epigraph::

               ``CodeConfiguration`` is required only for ``CreateService`` request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-coderepository.html#cfn-apprunner-service-coderepository-codeconfiguration
            '''
            result = self._values.get("code_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.CodeConfigurationProperty"]], result)

        @builtins.property
        def repository_url(self) -> typing.Optional[builtins.str]:
            '''The location of the repository that contains the source code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-coderepository.html#cfn-apprunner-service-coderepository-repositoryurl
            '''
            result = self._values.get("repository_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_code_version(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.SourceCodeVersionProperty"]]:
            '''The version that should be used within the source code repository.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-coderepository.html#cfn-apprunner-service-coderepository-sourcecodeversion
            '''
            result = self._values.get("source_code_version")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.SourceCodeVersionProperty"]], result)

        @builtins.property
        def source_directory(self) -> typing.Optional[builtins.str]:
            '''The path of the directory that stores source code and configuration files.

            The build and start commands also execute from here. The path is absolute from root and, if not specified, defaults to the repository root.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-coderepository.html#cfn-apprunner-service-coderepository-sourcedirectory
            '''
            result = self._values.get("source_directory")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeRepositoryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnServicePropsMixin.EgressConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "egress_type": "egressType",
            "vpc_connector_arn": "vpcConnectorArn",
        },
    )
    class EgressConfigurationProperty:
        def __init__(
            self,
            *,
            egress_type: typing.Optional[builtins.str] = None,
            vpc_connector_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes configuration settings related to outbound network traffic of an AWS App Runner service.

            :param egress_type: The type of egress configuration. Set to ``DEFAULT`` for access to resources hosted on public networks. Set to ``VPC`` to associate your service to a custom VPC specified by ``VpcConnectorArn`` .
            :param vpc_connector_arn: The Amazon Resource Name (ARN) of the App Runner VPC connector that you want to associate with your App Runner service. Only valid when ``EgressType = VPC`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-egressconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
                
                egress_configuration_property = apprunner_mixins.CfnServicePropsMixin.EgressConfigurationProperty(
                    egress_type="egressType",
                    vpc_connector_arn="vpcConnectorArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e06cc3e3ceb9ae41f44a90a595bcce4841878da178cbdbf8e2c66e9a205f63b6)
                check_type(argname="argument egress_type", value=egress_type, expected_type=type_hints["egress_type"])
                check_type(argname="argument vpc_connector_arn", value=vpc_connector_arn, expected_type=type_hints["vpc_connector_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if egress_type is not None:
                self._values["egress_type"] = egress_type
            if vpc_connector_arn is not None:
                self._values["vpc_connector_arn"] = vpc_connector_arn

        @builtins.property
        def egress_type(self) -> typing.Optional[builtins.str]:
            '''The type of egress configuration.

            Set to ``DEFAULT`` for access to resources hosted on public networks.

            Set to ``VPC`` to associate your service to a custom VPC specified by ``VpcConnectorArn`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-egressconfiguration.html#cfn-apprunner-service-egressconfiguration-egresstype
            '''
            result = self._values.get("egress_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_connector_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the App Runner VPC connector that you want to associate with your App Runner service.

            Only valid when ``EgressType = VPC`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-egressconfiguration.html#cfn-apprunner-service-egressconfiguration-vpcconnectorarn
            '''
            result = self._values.get("vpc_connector_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EgressConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnServicePropsMixin.EncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key": "kmsKey"},
    )
    class EncryptionConfigurationProperty:
        def __init__(self, *, kms_key: typing.Optional[builtins.str] = None) -> None:
            '''Describes a custom encryption key that AWS App Runner uses to encrypt copies of the source repository and service logs.

            :param kms_key: The ARN of the KMS key that's used for encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-encryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
                
                encryption_configuration_property = apprunner_mixins.CfnServicePropsMixin.EncryptionConfigurationProperty(
                    kms_key="kmsKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__69a4004ba95cacd6e742254170c9f93b897f2982a9110a89276d82e78f6ec33c)
                check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key is not None:
                self._values["kms_key"] = kms_key

        @builtins.property
        def kms_key(self) -> typing.Optional[builtins.str]:
            '''The ARN of the KMS key that's used for encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-encryptionconfiguration.html#cfn-apprunner-service-encryptionconfiguration-kmskey
            '''
            result = self._values.get("kms_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnServicePropsMixin.HealthCheckConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "healthy_threshold": "healthyThreshold",
            "interval": "interval",
            "path": "path",
            "protocol": "protocol",
            "timeout": "timeout",
            "unhealthy_threshold": "unhealthyThreshold",
        },
    )
    class HealthCheckConfigurationProperty:
        def __init__(
            self,
            *,
            healthy_threshold: typing.Optional[jsii.Number] = None,
            interval: typing.Optional[jsii.Number] = None,
            path: typing.Optional[builtins.str] = None,
            protocol: typing.Optional[builtins.str] = None,
            timeout: typing.Optional[jsii.Number] = None,
            unhealthy_threshold: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes the settings for the health check that AWS App Runner performs to monitor the health of a service.

            :param healthy_threshold: The number of consecutive checks that must succeed before App Runner decides that the service is healthy. Default: ``1``
            :param interval: The time interval, in seconds, between health checks. Default: ``5``
            :param path: The URL that health check requests are sent to. ``Path`` is only applicable when you set ``Protocol`` to ``HTTP`` . Default: ``"/"``
            :param protocol: The IP protocol that App Runner uses to perform health checks for your service. If you set ``Protocol`` to ``HTTP`` , App Runner sends health check requests to the HTTP path specified by ``Path`` . Default: ``TCP``
            :param timeout: The time, in seconds, to wait for a health check response before deciding it failed. Default: ``2``
            :param unhealthy_threshold: The number of consecutive checks that must fail before App Runner decides that the service is unhealthy. Default: ``5``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-healthcheckconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
                
                health_check_configuration_property = apprunner_mixins.CfnServicePropsMixin.HealthCheckConfigurationProperty(
                    healthy_threshold=123,
                    interval=123,
                    path="path",
                    protocol="protocol",
                    timeout=123,
                    unhealthy_threshold=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b5ac846cb6c632d402fa67dbc8f9b36d972561c52f94375562b4a8183ca580f6)
                check_type(argname="argument healthy_threshold", value=healthy_threshold, expected_type=type_hints["healthy_threshold"])
                check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
                check_type(argname="argument unhealthy_threshold", value=unhealthy_threshold, expected_type=type_hints["unhealthy_threshold"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if healthy_threshold is not None:
                self._values["healthy_threshold"] = healthy_threshold
            if interval is not None:
                self._values["interval"] = interval
            if path is not None:
                self._values["path"] = path
            if protocol is not None:
                self._values["protocol"] = protocol
            if timeout is not None:
                self._values["timeout"] = timeout
            if unhealthy_threshold is not None:
                self._values["unhealthy_threshold"] = unhealthy_threshold

        @builtins.property
        def healthy_threshold(self) -> typing.Optional[jsii.Number]:
            '''The number of consecutive checks that must succeed before App Runner decides that the service is healthy.

            Default: ``1``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-healthcheckconfiguration.html#cfn-apprunner-service-healthcheckconfiguration-healthythreshold
            '''
            result = self._values.get("healthy_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval(self) -> typing.Optional[jsii.Number]:
            '''The time interval, in seconds, between health checks.

            Default: ``5``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-healthcheckconfiguration.html#cfn-apprunner-service-healthcheckconfiguration-interval
            '''
            result = self._values.get("interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The URL that health check requests are sent to.

            ``Path`` is only applicable when you set ``Protocol`` to ``HTTP`` .

            Default: ``"/"``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-healthcheckconfiguration.html#cfn-apprunner-service-healthcheckconfiguration-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The IP protocol that App Runner uses to perform health checks for your service.

            If you set ``Protocol`` to ``HTTP`` , App Runner sends health check requests to the HTTP path specified by ``Path`` .

            Default: ``TCP``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-healthcheckconfiguration.html#cfn-apprunner-service-healthcheckconfiguration-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timeout(self) -> typing.Optional[jsii.Number]:
            '''The time, in seconds, to wait for a health check response before deciding it failed.

            Default: ``2``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-healthcheckconfiguration.html#cfn-apprunner-service-healthcheckconfiguration-timeout
            '''
            result = self._values.get("timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unhealthy_threshold(self) -> typing.Optional[jsii.Number]:
            '''The number of consecutive checks that must fail before App Runner decides that the service is unhealthy.

            Default: ``5``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-healthcheckconfiguration.html#cfn-apprunner-service-healthcheckconfiguration-unhealthythreshold
            '''
            result = self._values.get("unhealthy_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HealthCheckConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnServicePropsMixin.ImageConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "port": "port",
            "runtime_environment_secrets": "runtimeEnvironmentSecrets",
            "runtime_environment_variables": "runtimeEnvironmentVariables",
            "start_command": "startCommand",
        },
    )
    class ImageConfigurationProperty:
        def __init__(
            self,
            *,
            port: typing.Optional[builtins.str] = None,
            runtime_environment_secrets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.KeyValuePairProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            runtime_environment_variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.KeyValuePairProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            start_command: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the configuration that AWS App Runner uses to run an App Runner service using an image pulled from a source image repository.

            :param port: The port that your application listens to in the container. Default: ``8080``
            :param runtime_environment_secrets: An array of key-value pairs representing the secrets and parameters that get referenced to your service as an environment variable. The supported values are either the full Amazon Resource Name (ARN) of the AWS Secrets Manager secret or the full ARN of the parameter in the AWS Systems Manager Parameter Store. .. epigraph:: - If the AWS Systems Manager Parameter Store parameter exists in the same AWS Region as the service that you're launching, you can use either the full ARN or name of the secret. If the parameter exists in a different Region, then the full ARN must be specified. - Currently, cross account referencing of AWS Systems Manager Parameter Store parameter is not supported.
            :param runtime_environment_variables: Environment variables that are available to your running App Runner service. An array of key-value pairs.
            :param start_command: An optional command that App Runner runs to start the application in the source image. If specified, this command overrides the Docker image’s default start command.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imageconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
                
                image_configuration_property = apprunner_mixins.CfnServicePropsMixin.ImageConfigurationProperty(
                    port="port",
                    runtime_environment_secrets=[apprunner_mixins.CfnServicePropsMixin.KeyValuePairProperty(
                        name="name",
                        value="value"
                    )],
                    runtime_environment_variables=[apprunner_mixins.CfnServicePropsMixin.KeyValuePairProperty(
                        name="name",
                        value="value"
                    )],
                    start_command="startCommand"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f4f91a11860a0a1141b3a4187c4957e7b7f48b67c20734f682dbdaa93d976be2)
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument runtime_environment_secrets", value=runtime_environment_secrets, expected_type=type_hints["runtime_environment_secrets"])
                check_type(argname="argument runtime_environment_variables", value=runtime_environment_variables, expected_type=type_hints["runtime_environment_variables"])
                check_type(argname="argument start_command", value=start_command, expected_type=type_hints["start_command"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if port is not None:
                self._values["port"] = port
            if runtime_environment_secrets is not None:
                self._values["runtime_environment_secrets"] = runtime_environment_secrets
            if runtime_environment_variables is not None:
                self._values["runtime_environment_variables"] = runtime_environment_variables
            if start_command is not None:
                self._values["start_command"] = start_command

        @builtins.property
        def port(self) -> typing.Optional[builtins.str]:
            '''The port that your application listens to in the container.

            Default: ``8080``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imageconfiguration.html#cfn-apprunner-service-imageconfiguration-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def runtime_environment_secrets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.KeyValuePairProperty"]]]]:
            '''An array of key-value pairs representing the secrets and parameters that get referenced to your service as an environment variable.

            The supported values are either the full Amazon Resource Name (ARN) of the AWS Secrets Manager secret or the full ARN of the parameter in the AWS Systems Manager Parameter Store.
            .. epigraph::

               - If the AWS Systems Manager Parameter Store parameter exists in the same AWS Region as the service that you're launching, you can use either the full ARN or name of the secret. If the parameter exists in a different Region, then the full ARN must be specified.
               - Currently, cross account referencing of AWS Systems Manager Parameter Store parameter is not supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imageconfiguration.html#cfn-apprunner-service-imageconfiguration-runtimeenvironmentsecrets
            '''
            result = self._values.get("runtime_environment_secrets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.KeyValuePairProperty"]]]], result)

        @builtins.property
        def runtime_environment_variables(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.KeyValuePairProperty"]]]]:
            '''Environment variables that are available to your running App Runner service.

            An array of key-value pairs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imageconfiguration.html#cfn-apprunner-service-imageconfiguration-runtimeenvironmentvariables
            '''
            result = self._values.get("runtime_environment_variables")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.KeyValuePairProperty"]]]], result)

        @builtins.property
        def start_command(self) -> typing.Optional[builtins.str]:
            '''An optional command that App Runner runs to start the application in the source image.

            If specified, this command overrides the Docker image’s default start command.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imageconfiguration.html#cfn-apprunner-service-imageconfiguration-startcommand
            '''
            result = self._values.get("start_command")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImageConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnServicePropsMixin.ImageRepositoryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "image_configuration": "imageConfiguration",
            "image_identifier": "imageIdentifier",
            "image_repository_type": "imageRepositoryType",
        },
    )
    class ImageRepositoryProperty:
        def __init__(
            self,
            *,
            image_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.ImageConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            image_identifier: typing.Optional[builtins.str] = None,
            image_repository_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a source image repository.

            :param image_configuration: Configuration for running the identified image.
            :param image_identifier: The identifier of an image. For an image in Amazon Elastic Container Registry (Amazon ECR), this is an image name. For the image name format, see `Pulling an image <https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-pull-ecr-image.html>`_ in the *Amazon ECR User Guide* .
            :param image_repository_type: The type of the image repository. This reflects the repository provider and whether the repository is private or public.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imagerepository.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
                
                image_repository_property = apprunner_mixins.CfnServicePropsMixin.ImageRepositoryProperty(
                    image_configuration=apprunner_mixins.CfnServicePropsMixin.ImageConfigurationProperty(
                        port="port",
                        runtime_environment_secrets=[apprunner_mixins.CfnServicePropsMixin.KeyValuePairProperty(
                            name="name",
                            value="value"
                        )],
                        runtime_environment_variables=[apprunner_mixins.CfnServicePropsMixin.KeyValuePairProperty(
                            name="name",
                            value="value"
                        )],
                        start_command="startCommand"
                    ),
                    image_identifier="imageIdentifier",
                    image_repository_type="imageRepositoryType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3132da677953716462efa5ea4086194588461688472c0d51d204874e6b0ca523)
                check_type(argname="argument image_configuration", value=image_configuration, expected_type=type_hints["image_configuration"])
                check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
                check_type(argname="argument image_repository_type", value=image_repository_type, expected_type=type_hints["image_repository_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if image_configuration is not None:
                self._values["image_configuration"] = image_configuration
            if image_identifier is not None:
                self._values["image_identifier"] = image_identifier
            if image_repository_type is not None:
                self._values["image_repository_type"] = image_repository_type

        @builtins.property
        def image_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.ImageConfigurationProperty"]]:
            '''Configuration for running the identified image.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imagerepository.html#cfn-apprunner-service-imagerepository-imageconfiguration
            '''
            result = self._values.get("image_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.ImageConfigurationProperty"]], result)

        @builtins.property
        def image_identifier(self) -> typing.Optional[builtins.str]:
            '''The identifier of an image.

            For an image in Amazon Elastic Container Registry (Amazon ECR), this is an image name. For the image name format, see `Pulling an image <https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-pull-ecr-image.html>`_ in the *Amazon ECR User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imagerepository.html#cfn-apprunner-service-imagerepository-imageidentifier
            '''
            result = self._values.get("image_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_repository_type(self) -> typing.Optional[builtins.str]:
            '''The type of the image repository.

            This reflects the repository provider and whether the repository is private or public.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imagerepository.html#cfn-apprunner-service-imagerepository-imagerepositorytype
            '''
            result = self._values.get("image_repository_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImageRepositoryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnServicePropsMixin.IngressConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"is_publicly_accessible": "isPubliclyAccessible"},
    )
    class IngressConfigurationProperty:
        def __init__(
            self,
            *,
            is_publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Network configuration settings for inbound network traffic.

            :param is_publicly_accessible: Specifies whether your App Runner service is publicly accessible. To make the service publicly accessible set it to ``True`` . To make the service privately accessible, from only within an Amazon VPC set it to ``False`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-ingressconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
                
                ingress_configuration_property = apprunner_mixins.CfnServicePropsMixin.IngressConfigurationProperty(
                    is_publicly_accessible=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ac78ce0c5331c904e31e9bd25b139bdb8023dac6e2f9c2f6426c7452b576f903)
                check_type(argname="argument is_publicly_accessible", value=is_publicly_accessible, expected_type=type_hints["is_publicly_accessible"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_publicly_accessible is not None:
                self._values["is_publicly_accessible"] = is_publicly_accessible

        @builtins.property
        def is_publicly_accessible(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether your App Runner service is publicly accessible.

            To make the service publicly accessible set it to ``True`` . To make the service privately accessible, from only within an Amazon VPC set it to ``False`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-ingressconfiguration.html#cfn-apprunner-service-ingressconfiguration-ispubliclyaccessible
            '''
            result = self._values.get("is_publicly_accessible")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IngressConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnServicePropsMixin.InstanceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cpu": "cpu",
            "instance_role_arn": "instanceRoleArn",
            "memory": "memory",
        },
    )
    class InstanceConfigurationProperty:
        def __init__(
            self,
            *,
            cpu: typing.Optional[builtins.str] = None,
            instance_role_arn: typing.Optional[builtins.str] = None,
            memory: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the runtime configuration of an AWS App Runner service instance (scaling unit).

            :param cpu: The number of CPU units reserved for each instance of your App Runner service. Default: ``1 vCPU``
            :param instance_role_arn: The Amazon Resource Name (ARN) of an IAM role that provides permissions to your App Runner service. These are permissions that your code needs when it calls any AWS APIs.
            :param memory: The amount of memory, in MB or GB, reserved for each instance of your App Runner service. Default: ``2 GB``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-instanceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
                
                instance_configuration_property = apprunner_mixins.CfnServicePropsMixin.InstanceConfigurationProperty(
                    cpu="cpu",
                    instance_role_arn="instanceRoleArn",
                    memory="memory"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ddaa2d4eda805ddd79035e3ed547ca629c20d9b64f0aeb03372f4ba5c8ac42cc)
                check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
                check_type(argname="argument instance_role_arn", value=instance_role_arn, expected_type=type_hints["instance_role_arn"])
                check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cpu is not None:
                self._values["cpu"] = cpu
            if instance_role_arn is not None:
                self._values["instance_role_arn"] = instance_role_arn
            if memory is not None:
                self._values["memory"] = memory

        @builtins.property
        def cpu(self) -> typing.Optional[builtins.str]:
            '''The number of CPU units reserved for each instance of your App Runner service.

            Default: ``1 vCPU``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-instanceconfiguration.html#cfn-apprunner-service-instanceconfiguration-cpu
            '''
            result = self._values.get("cpu")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an IAM role that provides permissions to your App Runner service.

            These are permissions that your code needs when it calls any AWS APIs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-instanceconfiguration.html#cfn-apprunner-service-instanceconfiguration-instancerolearn
            '''
            result = self._values.get("instance_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def memory(self) -> typing.Optional[builtins.str]:
            '''The amount of memory, in MB or GB, reserved for each instance of your App Runner service.

            Default: ``2 GB``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-instanceconfiguration.html#cfn-apprunner-service-instanceconfiguration-memory
            '''
            result = self._values.get("memory")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnServicePropsMixin.KeyValuePairProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class KeyValuePairProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a key-value pair, which is a string-to-string mapping.

            :param name: The key name string to map to a value.
            :param value: The value string to which the key name is mapped.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-keyvaluepair.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
                
                key_value_pair_property = apprunner_mixins.CfnServicePropsMixin.KeyValuePairProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4850d588987bf79aa5a6a1fed4a79eb6438ce49992667d418cf68c2730f02620)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The key name string to map to a value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-keyvaluepair.html#cfn-apprunner-service-keyvaluepair-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value string to which the key name is mapped.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-keyvaluepair.html#cfn-apprunner-service-keyvaluepair-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeyValuePairProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnServicePropsMixin.NetworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "egress_configuration": "egressConfiguration",
            "ingress_configuration": "ingressConfiguration",
            "ip_address_type": "ipAddressType",
        },
    )
    class NetworkConfigurationProperty:
        def __init__(
            self,
            *,
            egress_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.EgressConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ingress_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.IngressConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ip_address_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes configuration settings related to network traffic of an AWS App Runner service.

            Consists of embedded objects for each configurable network feature.

            :param egress_configuration: Network configuration settings for outbound message traffic.
            :param ingress_configuration: Network configuration settings for inbound message traffic.
            :param ip_address_type: App Runner provides you with the option to choose between *IPv4* and *dual stack* (IPv4 and IPv6) for your incoming public network configuration. This is an optional parameter. If you do not specify an ``IpAddressType`` , it defaults to select IPv4.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-networkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
                
                network_configuration_property = apprunner_mixins.CfnServicePropsMixin.NetworkConfigurationProperty(
                    egress_configuration=apprunner_mixins.CfnServicePropsMixin.EgressConfigurationProperty(
                        egress_type="egressType",
                        vpc_connector_arn="vpcConnectorArn"
                    ),
                    ingress_configuration=apprunner_mixins.CfnServicePropsMixin.IngressConfigurationProperty(
                        is_publicly_accessible=False
                    ),
                    ip_address_type="ipAddressType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__972870568f0dff8d6ab3dd19a595486885fde6772cfce412ea97686b302cf530)
                check_type(argname="argument egress_configuration", value=egress_configuration, expected_type=type_hints["egress_configuration"])
                check_type(argname="argument ingress_configuration", value=ingress_configuration, expected_type=type_hints["ingress_configuration"])
                check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if egress_configuration is not None:
                self._values["egress_configuration"] = egress_configuration
            if ingress_configuration is not None:
                self._values["ingress_configuration"] = ingress_configuration
            if ip_address_type is not None:
                self._values["ip_address_type"] = ip_address_type

        @builtins.property
        def egress_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.EgressConfigurationProperty"]]:
            '''Network configuration settings for outbound message traffic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-networkconfiguration.html#cfn-apprunner-service-networkconfiguration-egressconfiguration
            '''
            result = self._values.get("egress_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.EgressConfigurationProperty"]], result)

        @builtins.property
        def ingress_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.IngressConfigurationProperty"]]:
            '''Network configuration settings for inbound message traffic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-networkconfiguration.html#cfn-apprunner-service-networkconfiguration-ingressconfiguration
            '''
            result = self._values.get("ingress_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.IngressConfigurationProperty"]], result)

        @builtins.property
        def ip_address_type(self) -> typing.Optional[builtins.str]:
            '''App Runner provides you with the option to choose between *IPv4* and *dual stack* (IPv4 and IPv6) for your incoming public network configuration.

            This is an optional parameter. If you do not specify an ``IpAddressType`` , it defaults to select IPv4.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-networkconfiguration.html#cfn-apprunner-service-networkconfiguration-ipaddresstype
            '''
            result = self._values.get("ip_address_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnServicePropsMixin.ServiceObservabilityConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "observability_configuration_arn": "observabilityConfigurationArn",
            "observability_enabled": "observabilityEnabled",
        },
    )
    class ServiceObservabilityConfigurationProperty:
        def __init__(
            self,
            *,
            observability_configuration_arn: typing.Optional[builtins.str] = None,
            observability_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Describes the observability configuration of an AWS App Runner service.

            These are additional observability features, like tracing, that you choose to enable. They're configured in a separate resource that you associate with your service.

            :param observability_configuration_arn: The Amazon Resource Name (ARN) of the observability configuration that is associated with the service. Specified only when ``ObservabilityEnabled`` is ``true`` . Specify an ARN with a name and a revision number to associate that revision. For example: ``arn:aws:apprunner:us-east-1:123456789012:observabilityconfiguration/xray-tracing/3`` Specify just the name to associate the latest revision. For example: ``arn:aws:apprunner:us-east-1:123456789012:observabilityconfiguration/xray-tracing``
            :param observability_enabled: When ``true`` , an observability configuration resource is associated with the service, and an ``ObservabilityConfigurationArn`` is specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-serviceobservabilityconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
                
                service_observability_configuration_property = apprunner_mixins.CfnServicePropsMixin.ServiceObservabilityConfigurationProperty(
                    observability_configuration_arn="observabilityConfigurationArn",
                    observability_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__db12ffad662b13386be04be266c41e2b670c94e7b33c050b322067a425d354dc)
                check_type(argname="argument observability_configuration_arn", value=observability_configuration_arn, expected_type=type_hints["observability_configuration_arn"])
                check_type(argname="argument observability_enabled", value=observability_enabled, expected_type=type_hints["observability_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if observability_configuration_arn is not None:
                self._values["observability_configuration_arn"] = observability_configuration_arn
            if observability_enabled is not None:
                self._values["observability_enabled"] = observability_enabled

        @builtins.property
        def observability_configuration_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the observability configuration that is associated with the service.

            Specified only when ``ObservabilityEnabled`` is ``true`` .

            Specify an ARN with a name and a revision number to associate that revision. For example: ``arn:aws:apprunner:us-east-1:123456789012:observabilityconfiguration/xray-tracing/3``

            Specify just the name to associate the latest revision. For example: ``arn:aws:apprunner:us-east-1:123456789012:observabilityconfiguration/xray-tracing``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-serviceobservabilityconfiguration.html#cfn-apprunner-service-serviceobservabilityconfiguration-observabilityconfigurationarn
            '''
            result = self._values.get("observability_configuration_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def observability_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When ``true`` , an observability configuration resource is associated with the service, and an ``ObservabilityConfigurationArn`` is specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-serviceobservabilityconfiguration.html#cfn-apprunner-service-serviceobservabilityconfiguration-observabilityenabled
            '''
            result = self._values.get("observability_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceObservabilityConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnServicePropsMixin.SourceCodeVersionProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class SourceCodeVersionProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Identifies a version of code that AWS App Runner refers to within a source code repository.

            :param type: The type of version identifier. For a git-based repository, branches represent versions.
            :param value: A source code version. For a git-based repository, a branch name maps to a specific version. App Runner uses the most recent commit to the branch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-sourcecodeversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
                
                source_code_version_property = apprunner_mixins.CfnServicePropsMixin.SourceCodeVersionProperty(
                    type="type",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1db357892e99e6d7532c28e7da40689d2643d65393abe6de4dd4616c0a94d888)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of version identifier.

            For a git-based repository, branches represent versions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-sourcecodeversion.html#cfn-apprunner-service-sourcecodeversion-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''A source code version.

            For a git-based repository, a branch name maps to a specific version. App Runner uses the most recent commit to the branch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-sourcecodeversion.html#cfn-apprunner-service-sourcecodeversion-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceCodeVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnServicePropsMixin.SourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authentication_configuration": "authenticationConfiguration",
            "auto_deployments_enabled": "autoDeploymentsEnabled",
            "code_repository": "codeRepository",
            "image_repository": "imageRepository",
        },
    )
    class SourceConfigurationProperty:
        def __init__(
            self,
            *,
            authentication_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.AuthenticationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            auto_deployments_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            code_repository: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.CodeRepositoryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            image_repository: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.ImageRepositoryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes the source deployed to an AWS App Runner service.

            It can be a code or an image repository.

            :param authentication_configuration: Describes the resources that are needed to authenticate access to some source repositories.
            :param auto_deployments_enabled: If ``true`` , continuous integration from the source repository is enabled for the App Runner service. Each repository change (including any source code commit or new image version) starts a deployment. Default: App Runner sets to ``false`` for a source image that uses an ECR Public repository or an ECR repository that's in an AWS account other than the one that the service is in. App Runner sets to ``true`` in all other cases (which currently include a source code repository or a source image using a same-account ECR repository).
            :param code_repository: The description of a source code repository. You must provide either this member or ``ImageRepository`` (but not both).
            :param image_repository: The description of a source image repository. You must provide either this member or ``CodeRepository`` (but not both).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-sourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
                
                source_configuration_property = apprunner_mixins.CfnServicePropsMixin.SourceConfigurationProperty(
                    authentication_configuration=apprunner_mixins.CfnServicePropsMixin.AuthenticationConfigurationProperty(
                        access_role_arn="accessRoleArn",
                        connection_arn="connectionArn"
                    ),
                    auto_deployments_enabled=False,
                    code_repository=apprunner_mixins.CfnServicePropsMixin.CodeRepositoryProperty(
                        code_configuration=apprunner_mixins.CfnServicePropsMixin.CodeConfigurationProperty(
                            code_configuration_values=apprunner_mixins.CfnServicePropsMixin.CodeConfigurationValuesProperty(
                                build_command="buildCommand",
                                port="port",
                                runtime="runtime",
                                runtime_environment_secrets=[apprunner_mixins.CfnServicePropsMixin.KeyValuePairProperty(
                                    name="name",
                                    value="value"
                                )],
                                runtime_environment_variables=[apprunner_mixins.CfnServicePropsMixin.KeyValuePairProperty(
                                    name="name",
                                    value="value"
                                )],
                                start_command="startCommand"
                            ),
                            configuration_source="configurationSource"
                        ),
                        repository_url="repositoryUrl",
                        source_code_version=apprunner_mixins.CfnServicePropsMixin.SourceCodeVersionProperty(
                            type="type",
                            value="value"
                        ),
                        source_directory="sourceDirectory"
                    ),
                    image_repository=apprunner_mixins.CfnServicePropsMixin.ImageRepositoryProperty(
                        image_configuration=apprunner_mixins.CfnServicePropsMixin.ImageConfigurationProperty(
                            port="port",
                            runtime_environment_secrets=[apprunner_mixins.CfnServicePropsMixin.KeyValuePairProperty(
                                name="name",
                                value="value"
                            )],
                            runtime_environment_variables=[apprunner_mixins.CfnServicePropsMixin.KeyValuePairProperty(
                                name="name",
                                value="value"
                            )],
                            start_command="startCommand"
                        ),
                        image_identifier="imageIdentifier",
                        image_repository_type="imageRepositoryType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ee781e495e904d4e7232383e6bd241ca1136d743908196db9ae3ef70f0851fe1)
                check_type(argname="argument authentication_configuration", value=authentication_configuration, expected_type=type_hints["authentication_configuration"])
                check_type(argname="argument auto_deployments_enabled", value=auto_deployments_enabled, expected_type=type_hints["auto_deployments_enabled"])
                check_type(argname="argument code_repository", value=code_repository, expected_type=type_hints["code_repository"])
                check_type(argname="argument image_repository", value=image_repository, expected_type=type_hints["image_repository"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authentication_configuration is not None:
                self._values["authentication_configuration"] = authentication_configuration
            if auto_deployments_enabled is not None:
                self._values["auto_deployments_enabled"] = auto_deployments_enabled
            if code_repository is not None:
                self._values["code_repository"] = code_repository
            if image_repository is not None:
                self._values["image_repository"] = image_repository

        @builtins.property
        def authentication_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.AuthenticationConfigurationProperty"]]:
            '''Describes the resources that are needed to authenticate access to some source repositories.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-sourceconfiguration.html#cfn-apprunner-service-sourceconfiguration-authenticationconfiguration
            '''
            result = self._values.get("authentication_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.AuthenticationConfigurationProperty"]], result)

        @builtins.property
        def auto_deployments_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If ``true`` , continuous integration from the source repository is enabled for the App Runner service.

            Each repository change (including any source code commit or new image version) starts a deployment.

            Default: App Runner sets to ``false`` for a source image that uses an ECR Public repository or an ECR repository that's in an AWS account other than the one that the service is in. App Runner sets to ``true`` in all other cases (which currently include a source code repository or a source image using a same-account ECR repository).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-sourceconfiguration.html#cfn-apprunner-service-sourceconfiguration-autodeploymentsenabled
            '''
            result = self._values.get("auto_deployments_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def code_repository(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.CodeRepositoryProperty"]]:
            '''The description of a source code repository.

            You must provide either this member or ``ImageRepository`` (but not both).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-sourceconfiguration.html#cfn-apprunner-service-sourceconfiguration-coderepository
            '''
            result = self._values.get("code_repository")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.CodeRepositoryProperty"]], result)

        @builtins.property
        def image_repository(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.ImageRepositoryProperty"]]:
            '''The description of a source image repository.

            You must provide either this member or ``CodeRepository`` (but not both).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-sourceconfiguration.html#cfn-apprunner-service-sourceconfiguration-imagerepository
            '''
            result = self._values.get("image_repository")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.ImageRepositoryProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnVpcConnectorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "security_groups": "securityGroups",
        "subnets": "subnets",
        "tags": "tags",
        "vpc_connector_name": "vpcConnectorName",
    },
)
class CfnVpcConnectorMixinProps:
    def __init__(
        self,
        *,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_connector_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnVpcConnectorPropsMixin.

        :param security_groups: A list of IDs of security groups that App Runner should use for access to AWS resources under the specified subnets. If not specified, App Runner uses the default security group of the Amazon VPC. The default security group allows all outbound traffic.
        :param subnets: A list of IDs of subnets that App Runner should use when it associates your service with a custom Amazon VPC. Specify IDs of subnets of a single Amazon VPC. App Runner determines the Amazon VPC from the subnets you specify. .. epigraph:: App Runner only supports subnets of IP address type *IPv4* and *dual stack* (IPv4 and IPv6).
        :param tags: A list of metadata items that you can associate with your VPC connector resource. A tag is a key-value pair. .. epigraph:: A ``VpcConnector`` is immutable, so you cannot update its tags. To change the tags, replace the resource. To replace a ``VpcConnector`` , you must provide a new combination of security groups.
        :param vpc_connector_name: A name for the VPC connector. If you don't specify a name, CloudFormation generates a name for your VPC connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcconnector.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
            
            cfn_vpc_connector_mixin_props = apprunner_mixins.CfnVpcConnectorMixinProps(
                security_groups=["securityGroups"],
                subnets=["subnets"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_connector_name="vpcConnectorName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__062e73549a92dee3671f2f141354cfc52954fe456f73181d85fdeac6b039a2fb)
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_connector_name", value=vpc_connector_name, expected_type=type_hints["vpc_connector_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets
        if tags is not None:
            self._values["tags"] = tags
        if vpc_connector_name is not None:
            self._values["vpc_connector_name"] = vpc_connector_name

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IDs of security groups that App Runner should use for access to AWS resources under the specified subnets.

        If not specified, App Runner uses the default security group of the Amazon VPC. The default security group allows all outbound traffic.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcconnector.html#cfn-apprunner-vpcconnector-securitygroups
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IDs of subnets that App Runner should use when it associates your service with a custom Amazon VPC.

        Specify IDs of subnets of a single Amazon VPC. App Runner determines the Amazon VPC from the subnets you specify.
        .. epigraph::

           App Runner only supports subnets of IP address type *IPv4* and *dual stack* (IPv4 and IPv6).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcconnector.html#cfn-apprunner-vpcconnector-subnets
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of metadata items that you can associate with your VPC connector resource.

        A tag is a key-value pair.
        .. epigraph::

           A ``VpcConnector`` is immutable, so you cannot update its tags. To change the tags, replace the resource. To replace a ``VpcConnector`` , you must provide a new combination of security groups.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcconnector.html#cfn-apprunner-vpcconnector-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_connector_name(self) -> typing.Optional[builtins.str]:
        '''A name for the VPC connector.

        If you don't specify a name, CloudFormation generates a name for your VPC connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcconnector.html#cfn-apprunner-vpcconnector-vpcconnectorname
        '''
        result = self._values.get("vpc_connector_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVpcConnectorMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVpcConnectorPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnVpcConnectorPropsMixin",
):
    '''Specify an AWS App Runner VPC connector by using the ``AWS::AppRunner::VpcConnector`` resource in an AWS CloudFormation template.

    The ``AWS::AppRunner::VpcConnector`` resource is an AWS App Runner resource type that specifies an App Runner VPC connector.

    App Runner requires this resource when you want to associate your App Runner service to a custom Amazon Virtual Private Cloud ( Amazon VPC ).

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcconnector.html
    :cloudformationResource: AWS::AppRunner::VpcConnector
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
        
        cfn_vpc_connector_props_mixin = apprunner_mixins.CfnVpcConnectorPropsMixin(apprunner_mixins.CfnVpcConnectorMixinProps(
            security_groups=["securityGroups"],
            subnets=["subnets"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_connector_name="vpcConnectorName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVpcConnectorMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppRunner::VpcConnector``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3868786a6f0de764a74134ec2d385460bed56b6e17be70e9053980aca3267854)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a508e849d472cebce4954ea6693d9d7305ec68cc5ac934f660dcfab1da96499)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e840d00b23c3f79d7d2146efc38cb54e376528184821ee762b46c316f5b4cab)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVpcConnectorMixinProps:
        return typing.cast(CfnVpcConnectorMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnVpcIngressConnectionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "ingress_vpc_configuration": "ingressVpcConfiguration",
        "service_arn": "serviceArn",
        "tags": "tags",
        "vpc_ingress_connection_name": "vpcIngressConnectionName",
    },
)
class CfnVpcIngressConnectionMixinProps:
    def __init__(
        self,
        *,
        ingress_vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVpcIngressConnectionPropsMixin.IngressVpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        service_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_ingress_connection_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnVpcIngressConnectionPropsMixin.

        :param ingress_vpc_configuration: Specifications for the customer’s Amazon VPC and the related AWS PrivateLink VPC endpoint that are used to create the VPC Ingress Connection resource.
        :param service_arn: The Amazon Resource Name (ARN) for this App Runner service that is used to create the VPC Ingress Connection resource.
        :param tags: An optional list of metadata items that you can associate with the VPC Ingress Connection resource. A tag is a key-value pair.
        :param vpc_ingress_connection_name: The customer-provided VPC Ingress Connection name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcingressconnection.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
            
            cfn_vpc_ingress_connection_mixin_props = apprunner_mixins.CfnVpcIngressConnectionMixinProps(
                ingress_vpc_configuration=apprunner_mixins.CfnVpcIngressConnectionPropsMixin.IngressVpcConfigurationProperty(
                    vpc_endpoint_id="vpcEndpointId",
                    vpc_id="vpcId"
                ),
                service_arn="serviceArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_ingress_connection_name="vpcIngressConnectionName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b95c5b616cdf995906ecea0634ae125d841e532f40dae2e4fc33ffcd0bd73f0f)
            check_type(argname="argument ingress_vpc_configuration", value=ingress_vpc_configuration, expected_type=type_hints["ingress_vpc_configuration"])
            check_type(argname="argument service_arn", value=service_arn, expected_type=type_hints["service_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_ingress_connection_name", value=vpc_ingress_connection_name, expected_type=type_hints["vpc_ingress_connection_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ingress_vpc_configuration is not None:
            self._values["ingress_vpc_configuration"] = ingress_vpc_configuration
        if service_arn is not None:
            self._values["service_arn"] = service_arn
        if tags is not None:
            self._values["tags"] = tags
        if vpc_ingress_connection_name is not None:
            self._values["vpc_ingress_connection_name"] = vpc_ingress_connection_name

    @builtins.property
    def ingress_vpc_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVpcIngressConnectionPropsMixin.IngressVpcConfigurationProperty"]]:
        '''Specifications for the customer’s Amazon VPC and the related AWS PrivateLink VPC endpoint that are used to create the VPC Ingress Connection resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcingressconnection.html#cfn-apprunner-vpcingressconnection-ingressvpcconfiguration
        '''
        result = self._values.get("ingress_vpc_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVpcIngressConnectionPropsMixin.IngressVpcConfigurationProperty"]], result)

    @builtins.property
    def service_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) for this App Runner service that is used to create the VPC Ingress Connection resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcingressconnection.html#cfn-apprunner-vpcingressconnection-servicearn
        '''
        result = self._values.get("service_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An optional list of metadata items that you can associate with the VPC Ingress Connection resource.

        A tag is a key-value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcingressconnection.html#cfn-apprunner-vpcingressconnection-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_ingress_connection_name(self) -> typing.Optional[builtins.str]:
        '''The customer-provided VPC Ingress Connection name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcingressconnection.html#cfn-apprunner-vpcingressconnection-vpcingressconnectionname
        '''
        result = self._values.get("vpc_ingress_connection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVpcIngressConnectionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVpcIngressConnectionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnVpcIngressConnectionPropsMixin",
):
    '''Specify an AWS App Runner VPC Ingress Connection by using the ``AWS::AppRunner::VpcIngressConnection`` resource in an AWS CloudFormation template.

    The ``AWS::AppRunner::VpcIngressConnection`` resource is an AWS App Runner resource type that specifies an App Runner VPC Ingress Connection.

    App Runner requires this resource when you want to associate your App Runner service to an Amazon VPC endpoint.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcingressconnection.html
    :cloudformationResource: AWS::AppRunner::VpcIngressConnection
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
        
        cfn_vpc_ingress_connection_props_mixin = apprunner_mixins.CfnVpcIngressConnectionPropsMixin(apprunner_mixins.CfnVpcIngressConnectionMixinProps(
            ingress_vpc_configuration=apprunner_mixins.CfnVpcIngressConnectionPropsMixin.IngressVpcConfigurationProperty(
                vpc_endpoint_id="vpcEndpointId",
                vpc_id="vpcId"
            ),
            service_arn="serviceArn",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_ingress_connection_name="vpcIngressConnectionName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVpcIngressConnectionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppRunner::VpcIngressConnection``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a217e4f552c853fbf12059f15d2a7aca320ddcaea9cf45501490c6a4fee29bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1afe5afba7b332df7b73fbddec7e52dacff5ec470196e13ba268977dbc1884a9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4241953f64e6a9e120aee1f41600353a7d99a41d88bbe59911b8cb151edef1ec)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVpcIngressConnectionMixinProps:
        return typing.cast(CfnVpcIngressConnectionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apprunner.mixins.CfnVpcIngressConnectionPropsMixin.IngressVpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"vpc_endpoint_id": "vpcEndpointId", "vpc_id": "vpcId"},
    )
    class IngressVpcConfigurationProperty:
        def __init__(
            self,
            *,
            vpc_endpoint_id: typing.Optional[builtins.str] = None,
            vpc_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifications for the customer’s VPC and related PrivateLink VPC endpoint that are used to associate with the VPC Ingress Connection resource.

            :param vpc_endpoint_id: The ID of the VPC endpoint that your App Runner service connects to.
            :param vpc_id: The ID of the VPC that is used for the VPC endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-vpcingressconnection-ingressvpcconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apprunner import mixins as apprunner_mixins
                
                ingress_vpc_configuration_property = apprunner_mixins.CfnVpcIngressConnectionPropsMixin.IngressVpcConfigurationProperty(
                    vpc_endpoint_id="vpcEndpointId",
                    vpc_id="vpcId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6800a4fe2782277716ceec8adaef7e68a5e454bc2288602f8867e64023e715ff)
                check_type(argname="argument vpc_endpoint_id", value=vpc_endpoint_id, expected_type=type_hints["vpc_endpoint_id"])
                check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if vpc_endpoint_id is not None:
                self._values["vpc_endpoint_id"] = vpc_endpoint_id
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id

        @builtins.property
        def vpc_endpoint_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the VPC endpoint that your App Runner service connects to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-vpcingressconnection-ingressvpcconfiguration.html#cfn-apprunner-vpcingressconnection-ingressvpcconfiguration-vpcendpointid
            '''
            result = self._values.get("vpc_endpoint_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the VPC that is used for the VPC endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-vpcingressconnection-ingressvpcconfiguration.html#cfn-apprunner-vpcingressconnection-ingressvpcconfiguration-vpcid
            '''
            result = self._values.get("vpc_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IngressVpcConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAutoScalingConfigurationMixinProps",
    "CfnAutoScalingConfigurationPropsMixin",
    "CfnObservabilityConfigurationMixinProps",
    "CfnObservabilityConfigurationPropsMixin",
    "CfnServiceMixinProps",
    "CfnServicePropsMixin",
    "CfnVpcConnectorMixinProps",
    "CfnVpcConnectorPropsMixin",
    "CfnVpcIngressConnectionMixinProps",
    "CfnVpcIngressConnectionPropsMixin",
]

publication.publish()

def _typecheckingstub__48e07c8405ffedf48c4594ddd306b17ea5c7a43eec50a5e71c24cb14b7ba9af0(
    *,
    auto_scaling_configuration_name: typing.Optional[builtins.str] = None,
    max_concurrency: typing.Optional[jsii.Number] = None,
    max_size: typing.Optional[jsii.Number] = None,
    min_size: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__561bf753599b72bf50e1657bbc287cbc42e66db2414666e878ec37b9ddda6550(
    props: typing.Union[CfnAutoScalingConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0b58cfe5e8551b1f1ae67028d34d790733714156e27023bff9aefc57a9429fe(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc1a14d20c338b3ba9a02c4d3b26e9edad62b9e96708f3c02d44fb27b20d43f0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08dd308a9678c7b688bbf346800cde12da3d61fe405478b9c9852d75388c3264(
    *,
    observability_configuration_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    trace_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnObservabilityConfigurationPropsMixin.TraceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b564d02c1e0c6de0690420e0d3324e51bc887ebdfe6e9b423c545dd5492e197(
    props: typing.Union[CfnObservabilityConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aac092815cfeed29313598b83e606bd0e7dd62a6014ebe5e83822685a9d2836(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdcd4e4e0da6c4b8f2a0b1def2d2146363ddaa71a4b5a4dff74fecee8e990494(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63209d7f9534369862aed6a0082ff40f7b198bf02f72ff0174b5b6c1c70e1d9d(
    *,
    vendor: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a8931a11ba339adc4dcd3353638da53bcebb3b420eb391d893f61506e211fdd(
    *,
    auto_scaling_configuration_arn: typing.Optional[builtins.str] = None,
    encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.EncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    health_check_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.HealthCheckConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.InstanceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    observability_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.ServiceObservabilityConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_name: typing.Optional[builtins.str] = None,
    source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.SourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99c6ff9ebb49a48c30cbbdda447fc221a61a952cff5b27ce6ea5966792a8423d(
    props: typing.Union[CfnServiceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__469faf4819785e75048c51bc42a4f758b13e1a6c89d4c14b6ae959be509cfb4a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4c5c6c97f68d369818a8f927b0bc3d1eb260f01e259fc1cf79d775b70b6f43d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed6a7f1f2a0d6145638c6f37eb0ee04d0901a9a524c760181397a15a804fee09(
    *,
    access_role_arn: typing.Optional[builtins.str] = None,
    connection_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebebda430b1ae185975f392390e190254540932c79f9cbef4500d090c29011dc(
    *,
    code_configuration_values: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.CodeConfigurationValuesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    configuration_source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79eb9d1f64d3c6959a4371962274f4f7f663b5907af6fe3f96b001875d55f46f(
    *,
    build_command: typing.Optional[builtins.str] = None,
    port: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[builtins.str] = None,
    runtime_environment_secrets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.KeyValuePairProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    runtime_environment_variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.KeyValuePairProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    start_command: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__912c48654e20ac3981d2d68010fa9aa433a1bade03f4f20516bde4410048c1da(
    *,
    code_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.CodeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    repository_url: typing.Optional[builtins.str] = None,
    source_code_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.SourceCodeVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e06cc3e3ceb9ae41f44a90a595bcce4841878da178cbdbf8e2c66e9a205f63b6(
    *,
    egress_type: typing.Optional[builtins.str] = None,
    vpc_connector_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69a4004ba95cacd6e742254170c9f93b897f2982a9110a89276d82e78f6ec33c(
    *,
    kms_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5ac846cb6c632d402fa67dbc8f9b36d972561c52f94375562b4a8183ca580f6(
    *,
    healthy_threshold: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[jsii.Number] = None,
    path: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[jsii.Number] = None,
    unhealthy_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4f91a11860a0a1141b3a4187c4957e7b7f48b67c20734f682dbdaa93d976be2(
    *,
    port: typing.Optional[builtins.str] = None,
    runtime_environment_secrets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.KeyValuePairProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    runtime_environment_variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.KeyValuePairProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    start_command: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3132da677953716462efa5ea4086194588461688472c0d51d204874e6b0ca523(
    *,
    image_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.ImageConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_identifier: typing.Optional[builtins.str] = None,
    image_repository_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac78ce0c5331c904e31e9bd25b139bdb8023dac6e2f9c2f6426c7452b576f903(
    *,
    is_publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddaa2d4eda805ddd79035e3ed547ca629c20d9b64f0aeb03372f4ba5c8ac42cc(
    *,
    cpu: typing.Optional[builtins.str] = None,
    instance_role_arn: typing.Optional[builtins.str] = None,
    memory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4850d588987bf79aa5a6a1fed4a79eb6438ce49992667d418cf68c2730f02620(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__972870568f0dff8d6ab3dd19a595486885fde6772cfce412ea97686b302cf530(
    *,
    egress_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.EgressConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ingress_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.IngressConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ip_address_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db12ffad662b13386be04be266c41e2b670c94e7b33c050b322067a425d354dc(
    *,
    observability_configuration_arn: typing.Optional[builtins.str] = None,
    observability_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db357892e99e6d7532c28e7da40689d2643d65393abe6de4dd4616c0a94d888(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee781e495e904d4e7232383e6bd241ca1136d743908196db9ae3ef70f0851fe1(
    *,
    authentication_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.AuthenticationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    auto_deployments_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    code_repository: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.CodeRepositoryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_repository: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.ImageRepositoryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__062e73549a92dee3671f2f141354cfc52954fe456f73181d85fdeac6b039a2fb(
    *,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_connector_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3868786a6f0de764a74134ec2d385460bed56b6e17be70e9053980aca3267854(
    props: typing.Union[CfnVpcConnectorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a508e849d472cebce4954ea6693d9d7305ec68cc5ac934f660dcfab1da96499(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e840d00b23c3f79d7d2146efc38cb54e376528184821ee762b46c316f5b4cab(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b95c5b616cdf995906ecea0634ae125d841e532f40dae2e4fc33ffcd0bd73f0f(
    *,
    ingress_vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVpcIngressConnectionPropsMixin.IngressVpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_ingress_connection_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a217e4f552c853fbf12059f15d2a7aca320ddcaea9cf45501490c6a4fee29bb(
    props: typing.Union[CfnVpcIngressConnectionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1afe5afba7b332df7b73fbddec7e52dacff5ec470196e13ba268977dbc1884a9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4241953f64e6a9e120aee1f41600353a7d99a41d88bbe59911b8cb151edef1ec(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6800a4fe2782277716ceec8adaef7e68a5e454bc2288602f8867e64023e715ff(
    *,
    vpc_endpoint_id: typing.Optional[builtins.str] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
