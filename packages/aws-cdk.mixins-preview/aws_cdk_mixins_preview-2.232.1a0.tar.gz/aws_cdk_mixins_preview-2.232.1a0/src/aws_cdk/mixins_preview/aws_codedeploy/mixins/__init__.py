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
    jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnApplicationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "compute_platform": "computePlatform",
        "tags": "tags",
    },
)
class CfnApplicationMixinProps:
    def __init__(
        self,
        *,
        application_name: typing.Optional[builtins.str] = None,
        compute_platform: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnApplicationPropsMixin.

        :param application_name: A name for the application. If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the application name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: Updates to ``ApplicationName`` are not supported.
        :param compute_platform: The compute platform that CodeDeploy deploys the application to.
        :param tags: The metadata that you apply to CodeDeploy applications to help you organize and categorize them. Each tag consists of a key and an optional value, both of which you define.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
            
            cfn_application_mixin_props = codedeploy_mixins.CfnApplicationMixinProps(
                application_name="applicationName",
                compute_platform="computePlatform",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9922994ee16b14d481ca65862354242a86ceb7596b105d24c5d3f3c72d888ad)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
            check_type(argname="argument compute_platform", value=compute_platform, expected_type=type_hints["compute_platform"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_name is not None:
            self._values["application_name"] = application_name
        if compute_platform is not None:
            self._values["compute_platform"] = compute_platform
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''A name for the application.

        If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the application name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           Updates to ``ApplicationName`` are not supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html#cfn-codedeploy-application-applicationname
        '''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compute_platform(self) -> typing.Optional[builtins.str]:
        '''The compute platform that CodeDeploy deploys the application to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html#cfn-codedeploy-application-computeplatform
        '''
        result = self._values.get("compute_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The metadata that you apply to CodeDeploy applications to help you organize and categorize them.

        Each tag consists of a key and an optional value, both of which you define.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html#cfn-codedeploy-application-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnApplicationPropsMixin",
):
    '''The ``AWS::CodeDeploy::Application`` resource creates an AWS CodeDeploy application.

    In CodeDeploy , an application is a name that functions as a container to ensure that the correct combination of revision, deployment configuration, and deployment group are referenced during a deployment. You can use the ``AWS::CodeDeploy::DeploymentGroup`` resource to associate the application with a CodeDeploy deployment group. For more information, see `CodeDeploy Deployments <https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-steps.html>`_ in the *AWS CodeDeploy User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html
    :cloudformationResource: AWS::CodeDeploy::Application
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
        
        cfn_application_props_mixin = codedeploy_mixins.CfnApplicationPropsMixin(codedeploy_mixins.CfnApplicationMixinProps(
            application_name="applicationName",
            compute_platform="computePlatform",
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
        props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CodeDeploy::Application``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40927613ae7f44db9986a939a06abf06f85734fe34ea2cdd80b696907b392305)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aaa42e09551a360f1655ff1bf5ba3112f516b28b5eac228964cf3e67715fb7e6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__897abd8cda7a779d2b19ac6c8ec327b503858f02e06a9602234435e3125a31e0)
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
    jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentConfigMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "compute_platform": "computePlatform",
        "deployment_config_name": "deploymentConfigName",
        "minimum_healthy_hosts": "minimumHealthyHosts",
        "traffic_routing_config": "trafficRoutingConfig",
        "zonal_config": "zonalConfig",
    },
)
class CfnDeploymentConfigMixinProps:
    def __init__(
        self,
        *,
        compute_platform: typing.Optional[builtins.str] = None,
        deployment_config_name: typing.Optional[builtins.str] = None,
        minimum_healthy_hosts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentConfigPropsMixin.MinimumHealthyHostsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        traffic_routing_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentConfigPropsMixin.TrafficRoutingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        zonal_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentConfigPropsMixin.ZonalConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDeploymentConfigPropsMixin.

        :param compute_platform: The destination platform type for the deployment ( ``Lambda`` , ``Server`` , or ``ECS`` ).
        :param deployment_config_name: A name for the deployment configuration. If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the deployment configuration name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param minimum_healthy_hosts: The minimum number of healthy instances that should be available at any time during the deployment. There are two parameters expected in the input: type and value. The type parameter takes either of the following values: - HOST_COUNT: The value parameter represents the minimum number of healthy instances as an absolute value. - FLEET_PERCENT: The value parameter represents the minimum number of healthy instances as a percentage of the total number of instances in the deployment. If you specify FLEET_PERCENT, at the start of the deployment, AWS CodeDeploy converts the percentage to the equivalent number of instance and rounds up fractional instances. The value parameter takes an integer. For example, to set a minimum of 95% healthy instance, specify a type of FLEET_PERCENT and a value of 95. For more information about instance health, see `CodeDeploy Instance Health <https://docs.aws.amazon.com/codedeploy/latest/userguide/instances-health.html>`_ in the AWS CodeDeploy User Guide.
        :param traffic_routing_config: The configuration that specifies how the deployment traffic is routed.
        :param zonal_config: Configure the ``ZonalConfig`` object if you want AWS CodeDeploy to deploy your application to one `Availability Zone <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-availability-zones>`_ at a time, within an AWS Region. For more information about the zonal configuration feature, see `zonal configuration <https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations-create.html#zonal-config>`_ in the *CodeDeploy User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
            
            cfn_deployment_config_mixin_props = codedeploy_mixins.CfnDeploymentConfigMixinProps(
                compute_platform="computePlatform",
                deployment_config_name="deploymentConfigName",
                minimum_healthy_hosts=codedeploy_mixins.CfnDeploymentConfigPropsMixin.MinimumHealthyHostsProperty(
                    type="type",
                    value=123
                ),
                traffic_routing_config=codedeploy_mixins.CfnDeploymentConfigPropsMixin.TrafficRoutingConfigProperty(
                    time_based_canary=codedeploy_mixins.CfnDeploymentConfigPropsMixin.TimeBasedCanaryProperty(
                        canary_interval=123,
                        canary_percentage=123
                    ),
                    time_based_linear=codedeploy_mixins.CfnDeploymentConfigPropsMixin.TimeBasedLinearProperty(
                        linear_interval=123,
                        linear_percentage=123
                    ),
                    type="type"
                ),
                zonal_config=codedeploy_mixins.CfnDeploymentConfigPropsMixin.ZonalConfigProperty(
                    first_zone_monitor_duration_in_seconds=123,
                    minimum_healthy_hosts_per_zone=codedeploy_mixins.CfnDeploymentConfigPropsMixin.MinimumHealthyHostsPerZoneProperty(
                        type="type",
                        value=123
                    ),
                    monitor_duration_in_seconds=123
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8058eeae33fe8c9638aac58461c0d0f60dff85246919dfc1556172660aacc2b4)
            check_type(argname="argument compute_platform", value=compute_platform, expected_type=type_hints["compute_platform"])
            check_type(argname="argument deployment_config_name", value=deployment_config_name, expected_type=type_hints["deployment_config_name"])
            check_type(argname="argument minimum_healthy_hosts", value=minimum_healthy_hosts, expected_type=type_hints["minimum_healthy_hosts"])
            check_type(argname="argument traffic_routing_config", value=traffic_routing_config, expected_type=type_hints["traffic_routing_config"])
            check_type(argname="argument zonal_config", value=zonal_config, expected_type=type_hints["zonal_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compute_platform is not None:
            self._values["compute_platform"] = compute_platform
        if deployment_config_name is not None:
            self._values["deployment_config_name"] = deployment_config_name
        if minimum_healthy_hosts is not None:
            self._values["minimum_healthy_hosts"] = minimum_healthy_hosts
        if traffic_routing_config is not None:
            self._values["traffic_routing_config"] = traffic_routing_config
        if zonal_config is not None:
            self._values["zonal_config"] = zonal_config

    @builtins.property
    def compute_platform(self) -> typing.Optional[builtins.str]:
        '''The destination platform type for the deployment ( ``Lambda`` , ``Server`` , or ``ECS`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-computeplatform
        '''
        result = self._values.get("compute_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_config_name(self) -> typing.Optional[builtins.str]:
        '''A name for the deployment configuration.

        If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the deployment configuration name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-deploymentconfigname
        '''
        result = self._values.get("deployment_config_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimum_healthy_hosts(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentConfigPropsMixin.MinimumHealthyHostsProperty"]]:
        '''The minimum number of healthy instances that should be available at any time during the deployment.

        There are two parameters expected in the input: type and value.

        The type parameter takes either of the following values:

        - HOST_COUNT: The value parameter represents the minimum number of healthy instances as an absolute value.
        - FLEET_PERCENT: The value parameter represents the minimum number of healthy instances as a percentage of the total number of instances in the deployment. If you specify FLEET_PERCENT, at the start of the deployment, AWS CodeDeploy converts the percentage to the equivalent number of instance and rounds up fractional instances.

        The value parameter takes an integer.

        For example, to set a minimum of 95% healthy instance, specify a type of FLEET_PERCENT and a value of 95.

        For more information about instance health, see `CodeDeploy Instance Health <https://docs.aws.amazon.com/codedeploy/latest/userguide/instances-health.html>`_ in the AWS CodeDeploy User Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-minimumhealthyhosts
        '''
        result = self._values.get("minimum_healthy_hosts")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentConfigPropsMixin.MinimumHealthyHostsProperty"]], result)

    @builtins.property
    def traffic_routing_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentConfigPropsMixin.TrafficRoutingConfigProperty"]]:
        '''The configuration that specifies how the deployment traffic is routed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-trafficroutingconfig
        '''
        result = self._values.get("traffic_routing_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentConfigPropsMixin.TrafficRoutingConfigProperty"]], result)

    @builtins.property
    def zonal_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentConfigPropsMixin.ZonalConfigProperty"]]:
        '''Configure the ``ZonalConfig`` object if you want AWS CodeDeploy to deploy your application to one `Availability Zone <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-availability-zones>`_ at a time, within an AWS Region.

        For more information about the zonal configuration feature, see `zonal configuration <https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations-create.html#zonal-config>`_ in the *CodeDeploy User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-zonalconfig
        '''
        result = self._values.get("zonal_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentConfigPropsMixin.ZonalConfigProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentConfigMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDeploymentConfigPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentConfigPropsMixin",
):
    '''The ``AWS::CodeDeploy::DeploymentConfig`` resource creates a set of deployment rules, deployment success conditions, and deployment failure conditions that AWS CodeDeploy uses during a deployment.

    The deployment configuration specifies the number or percentage of instances that must remain available at any time during a deployment.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html
    :cloudformationResource: AWS::CodeDeploy::DeploymentConfig
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
        
        cfn_deployment_config_props_mixin = codedeploy_mixins.CfnDeploymentConfigPropsMixin(codedeploy_mixins.CfnDeploymentConfigMixinProps(
            compute_platform="computePlatform",
            deployment_config_name="deploymentConfigName",
            minimum_healthy_hosts=codedeploy_mixins.CfnDeploymentConfigPropsMixin.MinimumHealthyHostsProperty(
                type="type",
                value=123
            ),
            traffic_routing_config=codedeploy_mixins.CfnDeploymentConfigPropsMixin.TrafficRoutingConfigProperty(
                time_based_canary=codedeploy_mixins.CfnDeploymentConfigPropsMixin.TimeBasedCanaryProperty(
                    canary_interval=123,
                    canary_percentage=123
                ),
                time_based_linear=codedeploy_mixins.CfnDeploymentConfigPropsMixin.TimeBasedLinearProperty(
                    linear_interval=123,
                    linear_percentage=123
                ),
                type="type"
            ),
            zonal_config=codedeploy_mixins.CfnDeploymentConfigPropsMixin.ZonalConfigProperty(
                first_zone_monitor_duration_in_seconds=123,
                minimum_healthy_hosts_per_zone=codedeploy_mixins.CfnDeploymentConfigPropsMixin.MinimumHealthyHostsPerZoneProperty(
                    type="type",
                    value=123
                ),
                monitor_duration_in_seconds=123
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDeploymentConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CodeDeploy::DeploymentConfig``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2599c5863f2d0fdf46cc07e1cf6c374fea09df43a4ed825ffab7797936466400)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2ba75513d03506052a9f7ad261f311bf709327ce1b3e8a53410f267b4e02545)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9268e9c0ccde6c53c0e3a604fe618d600777f5a8b504651b35e4111c03190868)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDeploymentConfigMixinProps:
        return typing.cast(CfnDeploymentConfigMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentConfigPropsMixin.MinimumHealthyHostsPerZoneProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class MinimumHealthyHostsPerZoneProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information about the minimum number of healthy instances per Availability Zone.

            :param type: The ``type`` associated with the ``MinimumHealthyHostsPerZone`` option.
            :param value: The ``value`` associated with the ``MinimumHealthyHostsPerZone`` option.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-minimumhealthyhostsperzone.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                minimum_healthy_hosts_per_zone_property = codedeploy_mixins.CfnDeploymentConfigPropsMixin.MinimumHealthyHostsPerZoneProperty(
                    type="type",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1c6a41708b4039e371d33a39453b6ccc9299625df70d7c2bdacd441c2a6be7f6)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The ``type`` associated with the ``MinimumHealthyHostsPerZone`` option.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-minimumhealthyhostsperzone.html#cfn-codedeploy-deploymentconfig-minimumhealthyhostsperzone-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''The ``value`` associated with the ``MinimumHealthyHostsPerZone`` option.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-minimumhealthyhostsperzone.html#cfn-codedeploy-deploymentconfig-minimumhealthyhostsperzone-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MinimumHealthyHostsPerZoneProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentConfigPropsMixin.MinimumHealthyHostsProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class MinimumHealthyHostsProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``MinimumHealthyHosts`` is a property of the `DeploymentConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html>`_ resource that defines how many instances must remain healthy during an AWS CodeDeploy deployment.

            :param type: The minimum healthy instance type:. - HOST_COUNT: The minimum number of healthy instance as an absolute value. - FLEET_PERCENT: The minimum number of healthy instance as a percentage of the total number of instance in the deployment. In an example of nine instance, if a HOST_COUNT of six is specified, deploy to up to three instances at a time. The deployment is successful if six or more instances are deployed to successfully. Otherwise, the deployment fails. If a FLEET_PERCENT of 40 is specified, deploy to up to five instance at a time. The deployment is successful if four or more instance are deployed to successfully. Otherwise, the deployment fails. .. epigraph:: In a call to ``GetDeploymentConfig`` , CodeDeployDefault.OneAtATime returns a minimum healthy instance type of MOST_CONCURRENCY and a value of 1. This means a deployment to only one instance at a time. (You cannot set the type to MOST_CONCURRENCY, only to HOST_COUNT or FLEET_PERCENT.) In addition, with CodeDeployDefault.OneAtATime, AWS CodeDeploy attempts to ensure that all instances but one are kept in a healthy state during the deployment. Although this allows one instance at a time to be taken offline for a new deployment, it also means that if the deployment to the last instance fails, the overall deployment is still successful. For more information, see `AWS CodeDeploy Instance Health <https://docs.aws.amazon.com//codedeploy/latest/userguide/instances-health.html>`_ in the *AWS CodeDeploy User Guide* .
            :param value: The minimum healthy instance value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-minimumhealthyhosts.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                minimum_healthy_hosts_property = codedeploy_mixins.CfnDeploymentConfigPropsMixin.MinimumHealthyHostsProperty(
                    type="type",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eabdf224ebb36fa5643804d9788ab45d27108f6d5117d1d52b4f59bd15f43610)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The minimum healthy instance type:.

            - HOST_COUNT: The minimum number of healthy instance as an absolute value.
            - FLEET_PERCENT: The minimum number of healthy instance as a percentage of the total number of instance in the deployment.

            In an example of nine instance, if a HOST_COUNT of six is specified, deploy to up to three instances at a time. The deployment is successful if six or more instances are deployed to successfully. Otherwise, the deployment fails. If a FLEET_PERCENT of 40 is specified, deploy to up to five instance at a time. The deployment is successful if four or more instance are deployed to successfully. Otherwise, the deployment fails.
            .. epigraph::

               In a call to ``GetDeploymentConfig`` , CodeDeployDefault.OneAtATime returns a minimum healthy instance type of MOST_CONCURRENCY and a value of 1. This means a deployment to only one instance at a time. (You cannot set the type to MOST_CONCURRENCY, only to HOST_COUNT or FLEET_PERCENT.) In addition, with CodeDeployDefault.OneAtATime, AWS CodeDeploy attempts to ensure that all instances but one are kept in a healthy state during the deployment. Although this allows one instance at a time to be taken offline for a new deployment, it also means that if the deployment to the last instance fails, the overall deployment is still successful.

            For more information, see `AWS CodeDeploy Instance Health <https://docs.aws.amazon.com//codedeploy/latest/userguide/instances-health.html>`_ in the *AWS CodeDeploy User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-minimumhealthyhosts.html#cfn-codedeploy-deploymentconfig-minimumhealthyhosts-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''The minimum healthy instance value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-minimumhealthyhosts.html#cfn-codedeploy-deploymentconfig-minimumhealthyhosts-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MinimumHealthyHostsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentConfigPropsMixin.TimeBasedCanaryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "canary_interval": "canaryInterval",
            "canary_percentage": "canaryPercentage",
        },
    )
    class TimeBasedCanaryProperty:
        def __init__(
            self,
            *,
            canary_interval: typing.Optional[jsii.Number] = None,
            canary_percentage: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A configuration that shifts traffic from one version of a Lambda function or Amazon ECS task set to another in two increments.

            The original and target Lambda function versions or ECS task sets are specified in the deployment's AppSpec file.

            :param canary_interval: The number of minutes between the first and second traffic shifts of a ``TimeBasedCanary`` deployment.
            :param canary_percentage: The percentage of traffic to shift in the first increment of a ``TimeBasedCanary`` deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-timebasedcanary.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                time_based_canary_property = codedeploy_mixins.CfnDeploymentConfigPropsMixin.TimeBasedCanaryProperty(
                    canary_interval=123,
                    canary_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__debf2e63d591511519f4f720804140b3385d2ef86de0a5aa3817e54e41e38bcf)
                check_type(argname="argument canary_interval", value=canary_interval, expected_type=type_hints["canary_interval"])
                check_type(argname="argument canary_percentage", value=canary_percentage, expected_type=type_hints["canary_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if canary_interval is not None:
                self._values["canary_interval"] = canary_interval
            if canary_percentage is not None:
                self._values["canary_percentage"] = canary_percentage

        @builtins.property
        def canary_interval(self) -> typing.Optional[jsii.Number]:
            '''The number of minutes between the first and second traffic shifts of a ``TimeBasedCanary`` deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-timebasedcanary.html#cfn-codedeploy-deploymentconfig-timebasedcanary-canaryinterval
            '''
            result = self._values.get("canary_interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def canary_percentage(self) -> typing.Optional[jsii.Number]:
            '''The percentage of traffic to shift in the first increment of a ``TimeBasedCanary`` deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-timebasedcanary.html#cfn-codedeploy-deploymentconfig-timebasedcanary-canarypercentage
            '''
            result = self._values.get("canary_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeBasedCanaryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentConfigPropsMixin.TimeBasedLinearProperty",
        jsii_struct_bases=[],
        name_mapping={
            "linear_interval": "linearInterval",
            "linear_percentage": "linearPercentage",
        },
    )
    class TimeBasedLinearProperty:
        def __init__(
            self,
            *,
            linear_interval: typing.Optional[jsii.Number] = None,
            linear_percentage: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A configuration that shifts traffic from one version of a Lambda function or ECS task set to another in equal increments, with an equal number of minutes between each increment.

            The original and target Lambda function versions or ECS task sets are specified in the deployment's AppSpec file.

            :param linear_interval: The number of minutes between each incremental traffic shift of a ``TimeBasedLinear`` deployment.
            :param linear_percentage: The percentage of traffic that is shifted at the start of each increment of a ``TimeBasedLinear`` deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-timebasedlinear.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                time_based_linear_property = codedeploy_mixins.CfnDeploymentConfigPropsMixin.TimeBasedLinearProperty(
                    linear_interval=123,
                    linear_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ded0fef4a5acccbf0db88069f379f33d572517df04442b9e1238e64072f19c66)
                check_type(argname="argument linear_interval", value=linear_interval, expected_type=type_hints["linear_interval"])
                check_type(argname="argument linear_percentage", value=linear_percentage, expected_type=type_hints["linear_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if linear_interval is not None:
                self._values["linear_interval"] = linear_interval
            if linear_percentage is not None:
                self._values["linear_percentage"] = linear_percentage

        @builtins.property
        def linear_interval(self) -> typing.Optional[jsii.Number]:
            '''The number of minutes between each incremental traffic shift of a ``TimeBasedLinear`` deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-timebasedlinear.html#cfn-codedeploy-deploymentconfig-timebasedlinear-linearinterval
            '''
            result = self._values.get("linear_interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def linear_percentage(self) -> typing.Optional[jsii.Number]:
            '''The percentage of traffic that is shifted at the start of each increment of a ``TimeBasedLinear`` deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-timebasedlinear.html#cfn-codedeploy-deploymentconfig-timebasedlinear-linearpercentage
            '''
            result = self._values.get("linear_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeBasedLinearProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentConfigPropsMixin.TrafficRoutingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "time_based_canary": "timeBasedCanary",
            "time_based_linear": "timeBasedLinear",
            "type": "type",
        },
    )
    class TrafficRoutingConfigProperty:
        def __init__(
            self,
            *,
            time_based_canary: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentConfigPropsMixin.TimeBasedCanaryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            time_based_linear: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentConfigPropsMixin.TimeBasedLinearProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration that specifies how traffic is shifted from one version of a Lambda function to another version during an AWS Lambda deployment, or from one Amazon ECS task set to another during an Amazon ECS deployment.

            :param time_based_canary: A configuration that shifts traffic from one version of a Lambda function or ECS task set to another in two increments. The original and target Lambda function versions or ECS task sets are specified in the deployment's AppSpec file.
            :param time_based_linear: A configuration that shifts traffic from one version of a Lambda function or Amazon ECS task set to another in equal increments, with an equal number of minutes between each increment. The original and target Lambda function versions or Amazon ECS task sets are specified in the deployment's AppSpec file.
            :param type: The type of traffic shifting ( ``TimeBasedCanary`` or ``TimeBasedLinear`` ) used by a deployment configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-trafficroutingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                traffic_routing_config_property = codedeploy_mixins.CfnDeploymentConfigPropsMixin.TrafficRoutingConfigProperty(
                    time_based_canary=codedeploy_mixins.CfnDeploymentConfigPropsMixin.TimeBasedCanaryProperty(
                        canary_interval=123,
                        canary_percentage=123
                    ),
                    time_based_linear=codedeploy_mixins.CfnDeploymentConfigPropsMixin.TimeBasedLinearProperty(
                        linear_interval=123,
                        linear_percentage=123
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4fa8882e1528a36275c594ee1a27b13d1cb37396df3a0cc0051458fb88ff9b76)
                check_type(argname="argument time_based_canary", value=time_based_canary, expected_type=type_hints["time_based_canary"])
                check_type(argname="argument time_based_linear", value=time_based_linear, expected_type=type_hints["time_based_linear"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if time_based_canary is not None:
                self._values["time_based_canary"] = time_based_canary
            if time_based_linear is not None:
                self._values["time_based_linear"] = time_based_linear
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def time_based_canary(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentConfigPropsMixin.TimeBasedCanaryProperty"]]:
            '''A configuration that shifts traffic from one version of a Lambda function or ECS task set to another in two increments.

            The original and target Lambda function versions or ECS task sets are specified in the deployment's AppSpec file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-trafficroutingconfig.html#cfn-codedeploy-deploymentconfig-trafficroutingconfig-timebasedcanary
            '''
            result = self._values.get("time_based_canary")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentConfigPropsMixin.TimeBasedCanaryProperty"]], result)

        @builtins.property
        def time_based_linear(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentConfigPropsMixin.TimeBasedLinearProperty"]]:
            '''A configuration that shifts traffic from one version of a Lambda function or Amazon ECS task set to another in equal increments, with an equal number of minutes between each increment.

            The original and target Lambda function versions or Amazon ECS task sets are specified in the deployment's AppSpec file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-trafficroutingconfig.html#cfn-codedeploy-deploymentconfig-trafficroutingconfig-timebasedlinear
            '''
            result = self._values.get("time_based_linear")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentConfigPropsMixin.TimeBasedLinearProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of traffic shifting ( ``TimeBasedCanary`` or ``TimeBasedLinear`` ) used by a deployment configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-trafficroutingconfig.html#cfn-codedeploy-deploymentconfig-trafficroutingconfig-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TrafficRoutingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentConfigPropsMixin.ZonalConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "first_zone_monitor_duration_in_seconds": "firstZoneMonitorDurationInSeconds",
            "minimum_healthy_hosts_per_zone": "minimumHealthyHostsPerZone",
            "monitor_duration_in_seconds": "monitorDurationInSeconds",
        },
    )
    class ZonalConfigProperty:
        def __init__(
            self,
            *,
            first_zone_monitor_duration_in_seconds: typing.Optional[jsii.Number] = None,
            minimum_healthy_hosts_per_zone: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentConfigPropsMixin.MinimumHealthyHostsPerZoneProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            monitor_duration_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Configure the ``ZonalConfig`` object if you want AWS CodeDeploy to deploy your application to one `Availability Zone <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-availability-zones>`_ at a time, within an AWS Region. By deploying to one Availability Zone at a time, you can expose your deployment to a progressively larger audience as confidence in the deployment's performance and viability grows. If you don't configure the ``ZonalConfig`` object, CodeDeploy deploys your application to a random selection of hosts across a Region.

            For more information about the zonal configuration feature, see `zonal configuration <https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations-create.html#zonal-config>`_ in the *CodeDeploy User Guide* .

            :param first_zone_monitor_duration_in_seconds: The period of time, in seconds, that CodeDeploy must wait after completing a deployment to the *first* Availability Zone. CodeDeploy will wait this amount of time before starting a deployment to the second Availability Zone. You might set this option if you want to allow extra bake time for the first Availability Zone. If you don't specify a value for ``firstZoneMonitorDurationInSeconds`` , then CodeDeploy uses the ``monitorDurationInSeconds`` value for the first Availability Zone. For more information about the zonal configuration feature, see `zonal configuration <https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations-create.html#zonal-config>`_ in the *CodeDeploy User Guide* .
            :param minimum_healthy_hosts_per_zone: The number or percentage of instances that must remain available per Availability Zone during a deployment. This option works in conjunction with the ``MinimumHealthyHosts`` option. For more information, see `About the minimum number of healthy hosts per Availability Zone <https://docs.aws.amazon.com//codedeploy/latest/userguide/instances-health.html#minimum-healthy-hosts-az>`_ in the *CodeDeploy User Guide* . If you don't specify the ``minimumHealthyHostsPerZone`` option, then CodeDeploy uses a default value of ``0`` percent. For more information about the zonal configuration feature, see `zonal configuration <https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations-create.html#zonal-config>`_ in the *CodeDeploy User Guide* .
            :param monitor_duration_in_seconds: The period of time, in seconds, that CodeDeploy must wait after completing a deployment to an Availability Zone. CodeDeploy will wait this amount of time before starting a deployment to the next Availability Zone. Consider adding a monitor duration to give the deployment some time to prove itself (or 'bake') in one Availability Zone before it is released in the next zone. If you don't specify a ``monitorDurationInSeconds`` , CodeDeploy starts deploying to the next Availability Zone immediately. For more information about the zonal configuration feature, see `zonal configuration <https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations-create.html#zonal-config>`_ in the *CodeDeploy User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-zonalconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                zonal_config_property = codedeploy_mixins.CfnDeploymentConfigPropsMixin.ZonalConfigProperty(
                    first_zone_monitor_duration_in_seconds=123,
                    minimum_healthy_hosts_per_zone=codedeploy_mixins.CfnDeploymentConfigPropsMixin.MinimumHealthyHostsPerZoneProperty(
                        type="type",
                        value=123
                    ),
                    monitor_duration_in_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__95ccba8bcf1b9115c6538fc8978f6db17b54dcc4a34fe9f285be6dc373562814)
                check_type(argname="argument first_zone_monitor_duration_in_seconds", value=first_zone_monitor_duration_in_seconds, expected_type=type_hints["first_zone_monitor_duration_in_seconds"])
                check_type(argname="argument minimum_healthy_hosts_per_zone", value=minimum_healthy_hosts_per_zone, expected_type=type_hints["minimum_healthy_hosts_per_zone"])
                check_type(argname="argument monitor_duration_in_seconds", value=monitor_duration_in_seconds, expected_type=type_hints["monitor_duration_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if first_zone_monitor_duration_in_seconds is not None:
                self._values["first_zone_monitor_duration_in_seconds"] = first_zone_monitor_duration_in_seconds
            if minimum_healthy_hosts_per_zone is not None:
                self._values["minimum_healthy_hosts_per_zone"] = minimum_healthy_hosts_per_zone
            if monitor_duration_in_seconds is not None:
                self._values["monitor_duration_in_seconds"] = monitor_duration_in_seconds

        @builtins.property
        def first_zone_monitor_duration_in_seconds(
            self,
        ) -> typing.Optional[jsii.Number]:
            '''The period of time, in seconds, that CodeDeploy must wait after completing a deployment to the *first* Availability Zone.

            CodeDeploy will wait this amount of time before starting a deployment to the second Availability Zone. You might set this option if you want to allow extra bake time for the first Availability Zone. If you don't specify a value for ``firstZoneMonitorDurationInSeconds`` , then CodeDeploy uses the ``monitorDurationInSeconds`` value for the first Availability Zone.

            For more information about the zonal configuration feature, see `zonal configuration <https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations-create.html#zonal-config>`_ in the *CodeDeploy User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-zonalconfig.html#cfn-codedeploy-deploymentconfig-zonalconfig-firstzonemonitordurationinseconds
            '''
            result = self._values.get("first_zone_monitor_duration_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def minimum_healthy_hosts_per_zone(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentConfigPropsMixin.MinimumHealthyHostsPerZoneProperty"]]:
            '''The number or percentage of instances that must remain available per Availability Zone during a deployment.

            This option works in conjunction with the ``MinimumHealthyHosts`` option. For more information, see `About the minimum number of healthy hosts per Availability Zone <https://docs.aws.amazon.com//codedeploy/latest/userguide/instances-health.html#minimum-healthy-hosts-az>`_ in the *CodeDeploy User Guide* .

            If you don't specify the ``minimumHealthyHostsPerZone`` option, then CodeDeploy uses a default value of ``0`` percent.

            For more information about the zonal configuration feature, see `zonal configuration <https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations-create.html#zonal-config>`_ in the *CodeDeploy User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-zonalconfig.html#cfn-codedeploy-deploymentconfig-zonalconfig-minimumhealthyhostsperzone
            '''
            result = self._values.get("minimum_healthy_hosts_per_zone")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentConfigPropsMixin.MinimumHealthyHostsPerZoneProperty"]], result)

        @builtins.property
        def monitor_duration_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The period of time, in seconds, that CodeDeploy must wait after completing a deployment to an Availability Zone.

            CodeDeploy will wait this amount of time before starting a deployment to the next Availability Zone. Consider adding a monitor duration to give the deployment some time to prove itself (or 'bake') in one Availability Zone before it is released in the next zone. If you don't specify a ``monitorDurationInSeconds`` , CodeDeploy starts deploying to the next Availability Zone immediately.

            For more information about the zonal configuration feature, see `zonal configuration <https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations-create.html#zonal-config>`_ in the *CodeDeploy User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-zonalconfig.html#cfn-codedeploy-deploymentconfig-zonalconfig-monitordurationinseconds
            '''
            result = self._values.get("monitor_duration_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ZonalConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "alarm_configuration": "alarmConfiguration",
        "application_name": "applicationName",
        "auto_rollback_configuration": "autoRollbackConfiguration",
        "auto_scaling_groups": "autoScalingGroups",
        "blue_green_deployment_configuration": "blueGreenDeploymentConfiguration",
        "deployment": "deployment",
        "deployment_config_name": "deploymentConfigName",
        "deployment_group_name": "deploymentGroupName",
        "deployment_style": "deploymentStyle",
        "ec2_tag_filters": "ec2TagFilters",
        "ec2_tag_set": "ec2TagSet",
        "ecs_services": "ecsServices",
        "load_balancer_info": "loadBalancerInfo",
        "on_premises_instance_tag_filters": "onPremisesInstanceTagFilters",
        "on_premises_tag_set": "onPremisesTagSet",
        "outdated_instances_strategy": "outdatedInstancesStrategy",
        "service_role_arn": "serviceRoleArn",
        "tags": "tags",
        "termination_hook_enabled": "terminationHookEnabled",
        "trigger_configurations": "triggerConfigurations",
    },
)
class CfnDeploymentGroupMixinProps:
    def __init__(
        self,
        *,
        alarm_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.AlarmConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        application_name: typing.Optional[builtins.str] = None,
        auto_rollback_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.AutoRollbackConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        auto_scaling_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        blue_green_deployment_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.BlueGreenDeploymentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        deployment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.DeploymentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        deployment_config_name: typing.Optional[builtins.str] = None,
        deployment_group_name: typing.Optional[builtins.str] = None,
        deployment_style: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.DeploymentStyleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ec2_tag_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.EC2TagFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ec2_tag_set: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.EC2TagSetProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ecs_services: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.ECSServiceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        load_balancer_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.LoadBalancerInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        on_premises_instance_tag_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.TagFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        on_premises_tag_set: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.OnPremisesTagSetProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        outdated_instances_strategy: typing.Optional[builtins.str] = None,
        service_role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        termination_hook_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        trigger_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.TriggerConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnDeploymentGroupPropsMixin.

        :param alarm_configuration: Information about the Amazon CloudWatch alarms that are associated with the deployment group.
        :param application_name: The name of an existing CodeDeploy application to associate this deployment group with.
        :param auto_rollback_configuration: Information about the automatic rollback configuration that is associated with the deployment group. If you specify this property, don't specify the ``Deployment`` property.
        :param auto_scaling_groups: A list of associated Amazon EC2 Auto Scaling groups that CodeDeploy automatically deploys revisions to when new instances are created. Duplicates are not allowed.
        :param blue_green_deployment_configuration: Information about blue/green deployment options for a deployment group.
        :param deployment: The application revision to deploy to this deployment group. If you specify this property, your target application revision is deployed as soon as the provisioning process is complete. If you specify this property, don't specify the ``AutoRollbackConfiguration`` property.
        :param deployment_config_name: A deployment configuration name or a predefined configuration name. With predefined configurations, you can deploy application revisions to one instance at a time ( ``CodeDeployDefault.OneAtATime`` ), half of the instances at a time ( ``CodeDeployDefault.HalfAtATime`` ), or all the instances at once ( ``CodeDeployDefault.AllAtOnce`` ). For more information and valid values, see `Working with Deployment Configurations <https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations.html>`_ in the *AWS CodeDeploy User Guide* .
        :param deployment_group_name: A name for the deployment group. If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the deployment group name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param deployment_style: Attributes that determine the type of deployment to run and whether to route deployment traffic behind a load balancer. If you specify this property with a blue/green deployment type, don't specify the ``AutoScalingGroups`` , ``LoadBalancerInfo`` , or ``Deployment`` properties. .. epigraph:: For blue/green deployments, CloudFormation supports deployments on Lambda compute platforms only. You can perform Amazon ECS blue/green deployments using ``AWS::CodeDeploy::BlueGreen`` hook. See `Perform Amazon ECS blue/green deployments through CodeDeploy using CloudFormation <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/blue-green.html>`_ for more information.
        :param ec2_tag_filters: The Amazon EC2 tags that are already applied to Amazon EC2 instances that you want to include in the deployment group. CodeDeploy includes all Amazon EC2 instances identified by any of the tags you specify in this deployment group. Duplicates are not allowed. You can specify ``EC2TagFilters`` or ``Ec2TagSet`` , but not both.
        :param ec2_tag_set: Information about groups of tags applied to Amazon EC2 instances. The deployment group includes only Amazon EC2 instances identified by all the tag groups. Cannot be used in the same call as ``ec2TagFilter`` .
        :param ecs_services: The target Amazon ECS services in the deployment group. This applies only to deployment groups that use the Amazon ECS compute platform. A target Amazon ECS service is specified as an Amazon ECS cluster and service name pair using the format ``<clustername>:<servicename>`` .
        :param load_balancer_info: Information about the load balancer to use in a deployment. For more information, see `Integrating CodeDeploy with ELB <https://docs.aws.amazon.com/codedeploy/latest/userguide/integrations-aws-elastic-load-balancing.html>`_ in the *AWS CodeDeploy User Guide* .
        :param on_premises_instance_tag_filters: The on-premises instance tags already applied to on-premises instances that you want to include in the deployment group. CodeDeploy includes all on-premises instances identified by any of the tags you specify in this deployment group. To register on-premises instances with CodeDeploy , see `Working with On-Premises Instances for CodeDeploy <https://docs.aws.amazon.com/codedeploy/latest/userguide/instances-on-premises.html>`_ in the *AWS CodeDeploy User Guide* . Duplicates are not allowed. You can specify ``OnPremisesInstanceTagFilters`` or ``OnPremisesInstanceTagSet`` , but not both.
        :param on_premises_tag_set: Information about groups of tags applied to on-premises instances. The deployment group includes only on-premises instances identified by all the tag groups. You can specify ``OnPremisesInstanceTagFilters`` or ``OnPremisesInstanceTagSet`` , but not both.
        :param outdated_instances_strategy: Indicates what happens when new Amazon EC2 instances are launched mid-deployment and do not receive the deployed application revision. If this option is set to ``UPDATE`` or is unspecified, CodeDeploy initiates one or more 'auto-update outdated instances' deployments to apply the deployed application revision to the new Amazon EC2 instances. If this option is set to ``IGNORE`` , CodeDeploy does not initiate a deployment to update the new Amazon EC2 instances. This may result in instances having different revisions.
        :param service_role_arn: A service role Amazon Resource Name (ARN) that grants CodeDeploy permission to make calls to AWS services on your behalf. For more information, see `Create a Service Role for AWS CodeDeploy <https://docs.aws.amazon.com/codedeploy/latest/userguide/getting-started-create-service-role.html>`_ in the *AWS CodeDeploy User Guide* . .. epigraph:: In some cases, you might need to add a dependency on the service role's policy. For more information, see IAM role policy in `DependsOn Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ .
        :param tags: The metadata that you apply to CodeDeploy deployment groups to help you organize and categorize them. Each tag consists of a key and an optional value, both of which you define.
        :param termination_hook_enabled: Indicates whether the deployment group was configured to have CodeDeploy install a termination hook into an Amazon EC2 Auto Scaling group. For more information about the termination hook, see `How Amazon EC2 Auto Scaling works with CodeDeploy <https://docs.aws.amazon.com//codedeploy/latest/userguide/integrations-aws-auto-scaling.html#integrations-aws-auto-scaling-behaviors>`_ in the *AWS CodeDeploy User Guide* .
        :param trigger_configurations: Information about triggers associated with the deployment group. Duplicates are not allowed

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
            
            cfn_deployment_group_mixin_props = codedeploy_mixins.CfnDeploymentGroupMixinProps(
                alarm_configuration=codedeploy_mixins.CfnDeploymentGroupPropsMixin.AlarmConfigurationProperty(
                    alarms=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.AlarmProperty(
                        name="name"
                    )],
                    enabled=False,
                    ignore_poll_alarm_failure=False
                ),
                application_name="applicationName",
                auto_rollback_configuration=codedeploy_mixins.CfnDeploymentGroupPropsMixin.AutoRollbackConfigurationProperty(
                    enabled=False,
                    events=["events"]
                ),
                auto_scaling_groups=["autoScalingGroups"],
                blue_green_deployment_configuration=codedeploy_mixins.CfnDeploymentGroupPropsMixin.BlueGreenDeploymentConfigurationProperty(
                    deployment_ready_option=codedeploy_mixins.CfnDeploymentGroupPropsMixin.DeploymentReadyOptionProperty(
                        action_on_timeout="actionOnTimeout",
                        wait_time_in_minutes=123
                    ),
                    green_fleet_provisioning_option=codedeploy_mixins.CfnDeploymentGroupPropsMixin.GreenFleetProvisioningOptionProperty(
                        action="action"
                    ),
                    terminate_blue_instances_on_deployment_success=codedeploy_mixins.CfnDeploymentGroupPropsMixin.BlueInstanceTerminationOptionProperty(
                        action="action",
                        termination_wait_time_in_minutes=123
                    )
                ),
                deployment=codedeploy_mixins.CfnDeploymentGroupPropsMixin.DeploymentProperty(
                    description="description",
                    ignore_application_stop_failures=False,
                    revision=codedeploy_mixins.CfnDeploymentGroupPropsMixin.RevisionLocationProperty(
                        git_hub_location=codedeploy_mixins.CfnDeploymentGroupPropsMixin.GitHubLocationProperty(
                            commit_id="commitId",
                            repository="repository"
                        ),
                        revision_type="revisionType",
                        s3_location=codedeploy_mixins.CfnDeploymentGroupPropsMixin.S3LocationProperty(
                            bucket="bucket",
                            bundle_type="bundleType",
                            e_tag="eTag",
                            key="key",
                            version="version"
                        )
                    )
                ),
                deployment_config_name="deploymentConfigName",
                deployment_group_name="deploymentGroupName",
                deployment_style=codedeploy_mixins.CfnDeploymentGroupPropsMixin.DeploymentStyleProperty(
                    deployment_option="deploymentOption",
                    deployment_type="deploymentType"
                ),
                ec2_tag_filters=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.EC2TagFilterProperty(
                    key="key",
                    type="type",
                    value="value"
                )],
                ec2_tag_set=codedeploy_mixins.CfnDeploymentGroupPropsMixin.EC2TagSetProperty(
                    ec2_tag_set_list=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.EC2TagSetListObjectProperty(
                        ec2_tag_group=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.EC2TagFilterProperty(
                            key="key",
                            type="type",
                            value="value"
                        )]
                    )]
                ),
                ecs_services=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.ECSServiceProperty(
                    cluster_name="clusterName",
                    service_name="serviceName"
                )],
                load_balancer_info=codedeploy_mixins.CfnDeploymentGroupPropsMixin.LoadBalancerInfoProperty(
                    elb_info_list=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.ELBInfoProperty(
                        name="name"
                    )],
                    target_group_info_list=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.TargetGroupInfoProperty(
                        name="name"
                    )],
                    target_group_pair_info_list=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.TargetGroupPairInfoProperty(
                        prod_traffic_route=codedeploy_mixins.CfnDeploymentGroupPropsMixin.TrafficRouteProperty(
                            listener_arns=["listenerArns"]
                        ),
                        target_groups=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.TargetGroupInfoProperty(
                            name="name"
                        )],
                        test_traffic_route=codedeploy_mixins.CfnDeploymentGroupPropsMixin.TrafficRouteProperty(
                            listener_arns=["listenerArns"]
                        )
                    )]
                ),
                on_premises_instance_tag_filters=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.TagFilterProperty(
                    key="key",
                    type="type",
                    value="value"
                )],
                on_premises_tag_set=codedeploy_mixins.CfnDeploymentGroupPropsMixin.OnPremisesTagSetProperty(
                    on_premises_tag_set_list=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.OnPremisesTagSetListObjectProperty(
                        on_premises_tag_group=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.TagFilterProperty(
                            key="key",
                            type="type",
                            value="value"
                        )]
                    )]
                ),
                outdated_instances_strategy="outdatedInstancesStrategy",
                service_role_arn="serviceRoleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                termination_hook_enabled=False,
                trigger_configurations=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.TriggerConfigProperty(
                    trigger_events=["triggerEvents"],
                    trigger_name="triggerName",
                    trigger_target_arn="triggerTargetArn"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__628b02985efb38d1cbcd86f1dc7cc55f335721b16a452ef1b4e0e2040dfedd56)
            check_type(argname="argument alarm_configuration", value=alarm_configuration, expected_type=type_hints["alarm_configuration"])
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
            check_type(argname="argument auto_rollback_configuration", value=auto_rollback_configuration, expected_type=type_hints["auto_rollback_configuration"])
            check_type(argname="argument auto_scaling_groups", value=auto_scaling_groups, expected_type=type_hints["auto_scaling_groups"])
            check_type(argname="argument blue_green_deployment_configuration", value=blue_green_deployment_configuration, expected_type=type_hints["blue_green_deployment_configuration"])
            check_type(argname="argument deployment", value=deployment, expected_type=type_hints["deployment"])
            check_type(argname="argument deployment_config_name", value=deployment_config_name, expected_type=type_hints["deployment_config_name"])
            check_type(argname="argument deployment_group_name", value=deployment_group_name, expected_type=type_hints["deployment_group_name"])
            check_type(argname="argument deployment_style", value=deployment_style, expected_type=type_hints["deployment_style"])
            check_type(argname="argument ec2_tag_filters", value=ec2_tag_filters, expected_type=type_hints["ec2_tag_filters"])
            check_type(argname="argument ec2_tag_set", value=ec2_tag_set, expected_type=type_hints["ec2_tag_set"])
            check_type(argname="argument ecs_services", value=ecs_services, expected_type=type_hints["ecs_services"])
            check_type(argname="argument load_balancer_info", value=load_balancer_info, expected_type=type_hints["load_balancer_info"])
            check_type(argname="argument on_premises_instance_tag_filters", value=on_premises_instance_tag_filters, expected_type=type_hints["on_premises_instance_tag_filters"])
            check_type(argname="argument on_premises_tag_set", value=on_premises_tag_set, expected_type=type_hints["on_premises_tag_set"])
            check_type(argname="argument outdated_instances_strategy", value=outdated_instances_strategy, expected_type=type_hints["outdated_instances_strategy"])
            check_type(argname="argument service_role_arn", value=service_role_arn, expected_type=type_hints["service_role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument termination_hook_enabled", value=termination_hook_enabled, expected_type=type_hints["termination_hook_enabled"])
            check_type(argname="argument trigger_configurations", value=trigger_configurations, expected_type=type_hints["trigger_configurations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarm_configuration is not None:
            self._values["alarm_configuration"] = alarm_configuration
        if application_name is not None:
            self._values["application_name"] = application_name
        if auto_rollback_configuration is not None:
            self._values["auto_rollback_configuration"] = auto_rollback_configuration
        if auto_scaling_groups is not None:
            self._values["auto_scaling_groups"] = auto_scaling_groups
        if blue_green_deployment_configuration is not None:
            self._values["blue_green_deployment_configuration"] = blue_green_deployment_configuration
        if deployment is not None:
            self._values["deployment"] = deployment
        if deployment_config_name is not None:
            self._values["deployment_config_name"] = deployment_config_name
        if deployment_group_name is not None:
            self._values["deployment_group_name"] = deployment_group_name
        if deployment_style is not None:
            self._values["deployment_style"] = deployment_style
        if ec2_tag_filters is not None:
            self._values["ec2_tag_filters"] = ec2_tag_filters
        if ec2_tag_set is not None:
            self._values["ec2_tag_set"] = ec2_tag_set
        if ecs_services is not None:
            self._values["ecs_services"] = ecs_services
        if load_balancer_info is not None:
            self._values["load_balancer_info"] = load_balancer_info
        if on_premises_instance_tag_filters is not None:
            self._values["on_premises_instance_tag_filters"] = on_premises_instance_tag_filters
        if on_premises_tag_set is not None:
            self._values["on_premises_tag_set"] = on_premises_tag_set
        if outdated_instances_strategy is not None:
            self._values["outdated_instances_strategy"] = outdated_instances_strategy
        if service_role_arn is not None:
            self._values["service_role_arn"] = service_role_arn
        if tags is not None:
            self._values["tags"] = tags
        if termination_hook_enabled is not None:
            self._values["termination_hook_enabled"] = termination_hook_enabled
        if trigger_configurations is not None:
            self._values["trigger_configurations"] = trigger_configurations

    @builtins.property
    def alarm_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.AlarmConfigurationProperty"]]:
        '''Information about the Amazon CloudWatch alarms that are associated with the deployment group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-alarmconfiguration
        '''
        result = self._values.get("alarm_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.AlarmConfigurationProperty"]], result)

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''The name of an existing CodeDeploy application to associate this deployment group with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-applicationname
        '''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_rollback_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.AutoRollbackConfigurationProperty"]]:
        '''Information about the automatic rollback configuration that is associated with the deployment group.

        If you specify this property, don't specify the ``Deployment`` property.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-autorollbackconfiguration
        '''
        result = self._values.get("auto_rollback_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.AutoRollbackConfigurationProperty"]], result)

    @builtins.property
    def auto_scaling_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of associated Amazon EC2 Auto Scaling groups that CodeDeploy automatically deploys revisions to when new instances are created.

        Duplicates are not allowed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-autoscalinggroups
        '''
        result = self._values.get("auto_scaling_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def blue_green_deployment_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.BlueGreenDeploymentConfigurationProperty"]]:
        '''Information about blue/green deployment options for a deployment group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-bluegreendeploymentconfiguration
        '''
        result = self._values.get("blue_green_deployment_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.BlueGreenDeploymentConfigurationProperty"]], result)

    @builtins.property
    def deployment(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.DeploymentProperty"]]:
        '''The application revision to deploy to this deployment group.

        If you specify this property, your target application revision is deployed as soon as the provisioning process is complete. If you specify this property, don't specify the ``AutoRollbackConfiguration`` property.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deployment
        '''
        result = self._values.get("deployment")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.DeploymentProperty"]], result)

    @builtins.property
    def deployment_config_name(self) -> typing.Optional[builtins.str]:
        '''A deployment configuration name or a predefined configuration name.

        With predefined configurations, you can deploy application revisions to one instance at a time ( ``CodeDeployDefault.OneAtATime`` ), half of the instances at a time ( ``CodeDeployDefault.HalfAtATime`` ), or all the instances at once ( ``CodeDeployDefault.AllAtOnce`` ). For more information and valid values, see `Working with Deployment Configurations <https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations.html>`_ in the *AWS CodeDeploy User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentconfigname
        '''
        result = self._values.get("deployment_config_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_group_name(self) -> typing.Optional[builtins.str]:
        '''A name for the deployment group.

        If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the deployment group name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentgroupname
        '''
        result = self._values.get("deployment_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_style(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.DeploymentStyleProperty"]]:
        '''Attributes that determine the type of deployment to run and whether to route deployment traffic behind a load balancer.

        If you specify this property with a blue/green deployment type, don't specify the ``AutoScalingGroups`` , ``LoadBalancerInfo`` , or ``Deployment`` properties.
        .. epigraph::

           For blue/green deployments, CloudFormation supports deployments on Lambda compute platforms only. You can perform Amazon ECS blue/green deployments using ``AWS::CodeDeploy::BlueGreen`` hook. See `Perform Amazon ECS blue/green deployments through CodeDeploy using CloudFormation <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/blue-green.html>`_ for more information.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentstyle
        '''
        result = self._values.get("deployment_style")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.DeploymentStyleProperty"]], result)

    @builtins.property
    def ec2_tag_filters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.EC2TagFilterProperty"]]]]:
        '''The Amazon EC2 tags that are already applied to Amazon EC2 instances that you want to include in the deployment group.

        CodeDeploy includes all Amazon EC2 instances identified by any of the tags you specify in this deployment group. Duplicates are not allowed.

        You can specify ``EC2TagFilters`` or ``Ec2TagSet`` , but not both.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-ec2tagfilters
        '''
        result = self._values.get("ec2_tag_filters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.EC2TagFilterProperty"]]]], result)

    @builtins.property
    def ec2_tag_set(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.EC2TagSetProperty"]]:
        '''Information about groups of tags applied to Amazon EC2 instances.

        The deployment group includes only Amazon EC2 instances identified by all the tag groups. Cannot be used in the same call as ``ec2TagFilter`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-ec2tagset
        '''
        result = self._values.get("ec2_tag_set")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.EC2TagSetProperty"]], result)

    @builtins.property
    def ecs_services(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.ECSServiceProperty"]]]]:
        '''The target Amazon ECS services in the deployment group.

        This applies only to deployment groups that use the Amazon ECS compute platform. A target Amazon ECS service is specified as an Amazon ECS cluster and service name pair using the format ``<clustername>:<servicename>`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-ecsservices
        '''
        result = self._values.get("ecs_services")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.ECSServiceProperty"]]]], result)

    @builtins.property
    def load_balancer_info(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.LoadBalancerInfoProperty"]]:
        '''Information about the load balancer to use in a deployment.

        For more information, see `Integrating CodeDeploy with ELB <https://docs.aws.amazon.com/codedeploy/latest/userguide/integrations-aws-elastic-load-balancing.html>`_ in the *AWS CodeDeploy User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-loadbalancerinfo
        '''
        result = self._values.get("load_balancer_info")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.LoadBalancerInfoProperty"]], result)

    @builtins.property
    def on_premises_instance_tag_filters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.TagFilterProperty"]]]]:
        '''The on-premises instance tags already applied to on-premises instances that you want to include in the deployment group.

        CodeDeploy includes all on-premises instances identified by any of the tags you specify in this deployment group. To register on-premises instances with CodeDeploy , see `Working with On-Premises Instances for CodeDeploy <https://docs.aws.amazon.com/codedeploy/latest/userguide/instances-on-premises.html>`_ in the *AWS CodeDeploy User Guide* . Duplicates are not allowed.

        You can specify ``OnPremisesInstanceTagFilters`` or ``OnPremisesInstanceTagSet`` , but not both.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-onpremisesinstancetagfilters
        '''
        result = self._values.get("on_premises_instance_tag_filters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.TagFilterProperty"]]]], result)

    @builtins.property
    def on_premises_tag_set(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.OnPremisesTagSetProperty"]]:
        '''Information about groups of tags applied to on-premises instances.

        The deployment group includes only on-premises instances identified by all the tag groups.

        You can specify ``OnPremisesInstanceTagFilters`` or ``OnPremisesInstanceTagSet`` , but not both.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-onpremisestagset
        '''
        result = self._values.get("on_premises_tag_set")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.OnPremisesTagSetProperty"]], result)

    @builtins.property
    def outdated_instances_strategy(self) -> typing.Optional[builtins.str]:
        '''Indicates what happens when new Amazon EC2 instances are launched mid-deployment and do not receive the deployed application revision.

        If this option is set to ``UPDATE`` or is unspecified, CodeDeploy initiates one or more 'auto-update outdated instances' deployments to apply the deployed application revision to the new Amazon EC2 instances.

        If this option is set to ``IGNORE`` , CodeDeploy does not initiate a deployment to update the new Amazon EC2 instances. This may result in instances having different revisions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-outdatedinstancesstrategy
        '''
        result = self._values.get("outdated_instances_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_role_arn(self) -> typing.Optional[builtins.str]:
        '''A service role Amazon Resource Name (ARN) that grants CodeDeploy permission to make calls to AWS services on your behalf.

        For more information, see `Create a Service Role for AWS CodeDeploy <https://docs.aws.amazon.com/codedeploy/latest/userguide/getting-started-create-service-role.html>`_ in the *AWS CodeDeploy User Guide* .
        .. epigraph::

           In some cases, you might need to add a dependency on the service role's policy. For more information, see IAM role policy in `DependsOn Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-servicerolearn
        '''
        result = self._values.get("service_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The metadata that you apply to CodeDeploy deployment groups to help you organize and categorize them.

        Each tag consists of a key and an optional value, both of which you define.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def termination_hook_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether the deployment group was configured to have CodeDeploy install a termination hook into an Amazon EC2 Auto Scaling group.

        For more information about the termination hook, see `How Amazon EC2 Auto Scaling works with CodeDeploy <https://docs.aws.amazon.com//codedeploy/latest/userguide/integrations-aws-auto-scaling.html#integrations-aws-auto-scaling-behaviors>`_ in the *AWS CodeDeploy User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-terminationhookenabled
        '''
        result = self._values.get("termination_hook_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def trigger_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.TriggerConfigProperty"]]]]:
        '''Information about triggers associated with the deployment group.

        Duplicates are not allowed

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-triggerconfigurations
        '''
        result = self._values.get("trigger_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.TriggerConfigProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDeploymentGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin",
):
    '''The ``AWS::CodeDeploy::DeploymentGroup`` resource creates an AWS CodeDeploy deployment group that specifies which instances your application revisions are deployed to, along with other deployment options.

    For more information, see `CreateDeploymentGroup <https://docs.aws.amazon.com/codedeploy/latest/APIReference/API_CreateDeploymentGroup.html>`_ in the *CodeDeploy API Reference* .
    .. epigraph::

       Amazon ECS blue/green deployments through CodeDeploy do not use the ``AWS::CodeDeploy::DeploymentGroup`` resource. To perform Amazon ECS blue/green deployments, use the ``AWS::CodeDeploy::BlueGreen`` hook. See `Perform Amazon ECS blue/green deployments through CodeDeploy using CloudFormation <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/blue-green.html>`_ for more information.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html
    :cloudformationResource: AWS::CodeDeploy::DeploymentGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
        
        cfn_deployment_group_props_mixin = codedeploy_mixins.CfnDeploymentGroupPropsMixin(codedeploy_mixins.CfnDeploymentGroupMixinProps(
            alarm_configuration=codedeploy_mixins.CfnDeploymentGroupPropsMixin.AlarmConfigurationProperty(
                alarms=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.AlarmProperty(
                    name="name"
                )],
                enabled=False,
                ignore_poll_alarm_failure=False
            ),
            application_name="applicationName",
            auto_rollback_configuration=codedeploy_mixins.CfnDeploymentGroupPropsMixin.AutoRollbackConfigurationProperty(
                enabled=False,
                events=["events"]
            ),
            auto_scaling_groups=["autoScalingGroups"],
            blue_green_deployment_configuration=codedeploy_mixins.CfnDeploymentGroupPropsMixin.BlueGreenDeploymentConfigurationProperty(
                deployment_ready_option=codedeploy_mixins.CfnDeploymentGroupPropsMixin.DeploymentReadyOptionProperty(
                    action_on_timeout="actionOnTimeout",
                    wait_time_in_minutes=123
                ),
                green_fleet_provisioning_option=codedeploy_mixins.CfnDeploymentGroupPropsMixin.GreenFleetProvisioningOptionProperty(
                    action="action"
                ),
                terminate_blue_instances_on_deployment_success=codedeploy_mixins.CfnDeploymentGroupPropsMixin.BlueInstanceTerminationOptionProperty(
                    action="action",
                    termination_wait_time_in_minutes=123
                )
            ),
            deployment=codedeploy_mixins.CfnDeploymentGroupPropsMixin.DeploymentProperty(
                description="description",
                ignore_application_stop_failures=False,
                revision=codedeploy_mixins.CfnDeploymentGroupPropsMixin.RevisionLocationProperty(
                    git_hub_location=codedeploy_mixins.CfnDeploymentGroupPropsMixin.GitHubLocationProperty(
                        commit_id="commitId",
                        repository="repository"
                    ),
                    revision_type="revisionType",
                    s3_location=codedeploy_mixins.CfnDeploymentGroupPropsMixin.S3LocationProperty(
                        bucket="bucket",
                        bundle_type="bundleType",
                        e_tag="eTag",
                        key="key",
                        version="version"
                    )
                )
            ),
            deployment_config_name="deploymentConfigName",
            deployment_group_name="deploymentGroupName",
            deployment_style=codedeploy_mixins.CfnDeploymentGroupPropsMixin.DeploymentStyleProperty(
                deployment_option="deploymentOption",
                deployment_type="deploymentType"
            ),
            ec2_tag_filters=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.EC2TagFilterProperty(
                key="key",
                type="type",
                value="value"
            )],
            ec2_tag_set=codedeploy_mixins.CfnDeploymentGroupPropsMixin.EC2TagSetProperty(
                ec2_tag_set_list=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.EC2TagSetListObjectProperty(
                    ec2_tag_group=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.EC2TagFilterProperty(
                        key="key",
                        type="type",
                        value="value"
                    )]
                )]
            ),
            ecs_services=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.ECSServiceProperty(
                cluster_name="clusterName",
                service_name="serviceName"
            )],
            load_balancer_info=codedeploy_mixins.CfnDeploymentGroupPropsMixin.LoadBalancerInfoProperty(
                elb_info_list=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.ELBInfoProperty(
                    name="name"
                )],
                target_group_info_list=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.TargetGroupInfoProperty(
                    name="name"
                )],
                target_group_pair_info_list=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.TargetGroupPairInfoProperty(
                    prod_traffic_route=codedeploy_mixins.CfnDeploymentGroupPropsMixin.TrafficRouteProperty(
                        listener_arns=["listenerArns"]
                    ),
                    target_groups=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.TargetGroupInfoProperty(
                        name="name"
                    )],
                    test_traffic_route=codedeploy_mixins.CfnDeploymentGroupPropsMixin.TrafficRouteProperty(
                        listener_arns=["listenerArns"]
                    )
                )]
            ),
            on_premises_instance_tag_filters=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.TagFilterProperty(
                key="key",
                type="type",
                value="value"
            )],
            on_premises_tag_set=codedeploy_mixins.CfnDeploymentGroupPropsMixin.OnPremisesTagSetProperty(
                on_premises_tag_set_list=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.OnPremisesTagSetListObjectProperty(
                    on_premises_tag_group=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.TagFilterProperty(
                        key="key",
                        type="type",
                        value="value"
                    )]
                )]
            ),
            outdated_instances_strategy="outdatedInstancesStrategy",
            service_role_arn="serviceRoleArn",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            termination_hook_enabled=False,
            trigger_configurations=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.TriggerConfigProperty(
                trigger_events=["triggerEvents"],
                trigger_name="triggerName",
                trigger_target_arn="triggerTargetArn"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDeploymentGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CodeDeploy::DeploymentGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b694585ede99d65d64f83954ec877206cd3f6dbfeff2f14bc9eb57ceae22e44)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b971f3c45b75fab985aa35b531019de4ad9a81d0c5c1629ebe453b97b2d2b272)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abb8ed9e1e0bf41f8469246c2ede160f2d1f0afcca3622c14d1d31f9c1b4eb36)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDeploymentGroupMixinProps:
        return typing.cast(CfnDeploymentGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.AlarmConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alarms": "alarms",
            "enabled": "enabled",
            "ignore_poll_alarm_failure": "ignorePollAlarmFailure",
        },
    )
    class AlarmConfigurationProperty:
        def __init__(
            self,
            *,
            alarms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.AlarmProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            ignore_poll_alarm_failure: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The ``AlarmConfiguration`` property type configures CloudWatch alarms for an AWS CodeDeploy deployment group.

            ``AlarmConfiguration`` is a property of the `DeploymentGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html>`_ resource.

            :param alarms: A list of alarms configured for the deployment or deployment group. A maximum of 10 alarms can be added.
            :param enabled: Indicates whether the alarm configuration is enabled.
            :param ignore_poll_alarm_failure: Indicates whether a deployment should continue if information about the current state of alarms cannot be retrieved from Amazon CloudWatch . The default value is ``false`` . - ``true`` : The deployment proceeds even if alarm status information can't be retrieved from CloudWatch . - ``false`` : The deployment stops if alarm status information can't be retrieved from CloudWatch .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarmconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                alarm_configuration_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.AlarmConfigurationProperty(
                    alarms=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.AlarmProperty(
                        name="name"
                    )],
                    enabled=False,
                    ignore_poll_alarm_failure=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__08f70cdb5b4112d0a3f6cddda42b855acba372690e9a502e7af7f6fd921eaa24)
                check_type(argname="argument alarms", value=alarms, expected_type=type_hints["alarms"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument ignore_poll_alarm_failure", value=ignore_poll_alarm_failure, expected_type=type_hints["ignore_poll_alarm_failure"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alarms is not None:
                self._values["alarms"] = alarms
            if enabled is not None:
                self._values["enabled"] = enabled
            if ignore_poll_alarm_failure is not None:
                self._values["ignore_poll_alarm_failure"] = ignore_poll_alarm_failure

        @builtins.property
        def alarms(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.AlarmProperty"]]]]:
            '''A list of alarms configured for the deployment or deployment group.

            A maximum of 10 alarms can be added.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarmconfiguration.html#cfn-codedeploy-deploymentgroup-alarmconfiguration-alarms
            '''
            result = self._values.get("alarms")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.AlarmProperty"]]]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the alarm configuration is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarmconfiguration.html#cfn-codedeploy-deploymentgroup-alarmconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def ignore_poll_alarm_failure(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether a deployment should continue if information about the current state of alarms cannot be retrieved from Amazon CloudWatch .

            The default value is ``false`` .

            - ``true`` : The deployment proceeds even if alarm status information can't be retrieved from CloudWatch .
            - ``false`` : The deployment stops if alarm status information can't be retrieved from CloudWatch .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarmconfiguration.html#cfn-codedeploy-deploymentgroup-alarmconfiguration-ignorepollalarmfailure
            '''
            result = self._values.get("ignore_poll_alarm_failure")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.AlarmProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class AlarmProperty:
        def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
            '''The ``Alarm`` property type specifies a CloudWatch alarm to use for an AWS CodeDeploy deployment group.

            The ``Alarm`` property of the `CodeDeploy DeploymentGroup AlarmConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarmconfiguration.html>`_ property contains a list of ``Alarm`` property types.

            :param name: The name of the alarm. Maximum length is 255 characters. Each alarm name can be used only once in a list of alarms.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarm.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                alarm_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.AlarmProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b3fbd96e5fafbf406ff10ae6637f914bb1418c7b2533f7935a4830babb1b964e)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the alarm.

            Maximum length is 255 characters. Each alarm name can be used only once in a list of alarms.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarm.html#cfn-codedeploy-deploymentgroup-alarm-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.AutoRollbackConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "events": "events"},
    )
    class AutoRollbackConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            events: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The ``AutoRollbackConfiguration`` property type configures automatic rollback for an AWS CodeDeploy deployment group when a deployment is not completed successfully.

            For more information, see `Automatic Rollbacks <https://docs.aws.amazon.com/codedeploy/latest/userguide/deployments-rollback-and-redeploy.html#deployments-rollback-and-redeploy-automatic-rollbacks>`_ in the *AWS CodeDeploy User Guide* .

            ``AutoRollbackConfiguration`` is a property of the `DeploymentGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html>`_ resource.

            :param enabled: Indicates whether a defined automatic rollback configuration is currently enabled.
            :param events: The event type or types that trigger a rollback. Valid values are ``DEPLOYMENT_FAILURE`` , ``DEPLOYMENT_STOP_ON_ALARM`` , or ``DEPLOYMENT_STOP_ON_REQUEST`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-autorollbackconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                auto_rollback_configuration_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.AutoRollbackConfigurationProperty(
                    enabled=False,
                    events=["events"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1fc4fa9139bcb0e3c67a29adc78904f2c5dc2374b42c83ca8a62841c260ecbfc)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if events is not None:
                self._values["events"] = events

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether a defined automatic rollback configuration is currently enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-autorollbackconfiguration.html#cfn-codedeploy-deploymentgroup-autorollbackconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def events(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The event type or types that trigger a rollback.

            Valid values are ``DEPLOYMENT_FAILURE`` , ``DEPLOYMENT_STOP_ON_ALARM`` , or ``DEPLOYMENT_STOP_ON_REQUEST`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-autorollbackconfiguration.html#cfn-codedeploy-deploymentgroup-autorollbackconfiguration-events
            '''
            result = self._values.get("events")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoRollbackConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.BlueGreenDeploymentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "deployment_ready_option": "deploymentReadyOption",
            "green_fleet_provisioning_option": "greenFleetProvisioningOption",
            "terminate_blue_instances_on_deployment_success": "terminateBlueInstancesOnDeploymentSuccess",
        },
    )
    class BlueGreenDeploymentConfigurationProperty:
        def __init__(
            self,
            *,
            deployment_ready_option: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.DeploymentReadyOptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            green_fleet_provisioning_option: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.GreenFleetProvisioningOptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            terminate_blue_instances_on_deployment_success: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.BlueInstanceTerminationOptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about blue/green deployment options for a deployment group.

            :param deployment_ready_option: Information about the action to take when newly provisioned instances are ready to receive traffic in a blue/green deployment.
            :param green_fleet_provisioning_option: Information about how instances are provisioned for a replacement environment in a blue/green deployment.
            :param terminate_blue_instances_on_deployment_success: Information about whether to terminate instances in the original fleet during a blue/green deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-bluegreendeploymentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                blue_green_deployment_configuration_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.BlueGreenDeploymentConfigurationProperty(
                    deployment_ready_option=codedeploy_mixins.CfnDeploymentGroupPropsMixin.DeploymentReadyOptionProperty(
                        action_on_timeout="actionOnTimeout",
                        wait_time_in_minutes=123
                    ),
                    green_fleet_provisioning_option=codedeploy_mixins.CfnDeploymentGroupPropsMixin.GreenFleetProvisioningOptionProperty(
                        action="action"
                    ),
                    terminate_blue_instances_on_deployment_success=codedeploy_mixins.CfnDeploymentGroupPropsMixin.BlueInstanceTerminationOptionProperty(
                        action="action",
                        termination_wait_time_in_minutes=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4557a2c9c2df51e1e95d0c70ea65055b7e8a4f5690ae6cd1bf866395478b7215)
                check_type(argname="argument deployment_ready_option", value=deployment_ready_option, expected_type=type_hints["deployment_ready_option"])
                check_type(argname="argument green_fleet_provisioning_option", value=green_fleet_provisioning_option, expected_type=type_hints["green_fleet_provisioning_option"])
                check_type(argname="argument terminate_blue_instances_on_deployment_success", value=terminate_blue_instances_on_deployment_success, expected_type=type_hints["terminate_blue_instances_on_deployment_success"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if deployment_ready_option is not None:
                self._values["deployment_ready_option"] = deployment_ready_option
            if green_fleet_provisioning_option is not None:
                self._values["green_fleet_provisioning_option"] = green_fleet_provisioning_option
            if terminate_blue_instances_on_deployment_success is not None:
                self._values["terminate_blue_instances_on_deployment_success"] = terminate_blue_instances_on_deployment_success

        @builtins.property
        def deployment_ready_option(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.DeploymentReadyOptionProperty"]]:
            '''Information about the action to take when newly provisioned instances are ready to receive traffic in a blue/green deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-bluegreendeploymentconfiguration.html#cfn-codedeploy-deploymentgroup-bluegreendeploymentconfiguration-deploymentreadyoption
            '''
            result = self._values.get("deployment_ready_option")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.DeploymentReadyOptionProperty"]], result)

        @builtins.property
        def green_fleet_provisioning_option(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.GreenFleetProvisioningOptionProperty"]]:
            '''Information about how instances are provisioned for a replacement environment in a blue/green deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-bluegreendeploymentconfiguration.html#cfn-codedeploy-deploymentgroup-bluegreendeploymentconfiguration-greenfleetprovisioningoption
            '''
            result = self._values.get("green_fleet_provisioning_option")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.GreenFleetProvisioningOptionProperty"]], result)

        @builtins.property
        def terminate_blue_instances_on_deployment_success(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.BlueInstanceTerminationOptionProperty"]]:
            '''Information about whether to terminate instances in the original fleet during a blue/green deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-bluegreendeploymentconfiguration.html#cfn-codedeploy-deploymentgroup-bluegreendeploymentconfiguration-terminateblueinstancesondeploymentsuccess
            '''
            result = self._values.get("terminate_blue_instances_on_deployment_success")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.BlueInstanceTerminationOptionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BlueGreenDeploymentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.BlueInstanceTerminationOptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "termination_wait_time_in_minutes": "terminationWaitTimeInMinutes",
        },
    )
    class BlueInstanceTerminationOptionProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            termination_wait_time_in_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information about whether instances in the original environment are terminated when a blue/green deployment is successful.

            ``BlueInstanceTerminationOption`` does not apply to Lambda deployments.

            :param action: The action to take on instances in the original environment after a successful blue/green deployment. - ``TERMINATE`` : Instances are terminated after a specified wait time. - ``KEEP_ALIVE`` : Instances are left running after they are deregistered from the load balancer and removed from the deployment group.
            :param termination_wait_time_in_minutes: For an Amazon EC2 deployment, the number of minutes to wait after a successful blue/green deployment before terminating instances from the original environment. For an Amazon ECS deployment, the number of minutes before deleting the original (blue) task set. During an Amazon ECS deployment, CodeDeploy shifts traffic from the original (blue) task set to a replacement (green) task set. The maximum setting is 2880 minutes (2 days).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-blueinstanceterminationoption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                blue_instance_termination_option_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.BlueInstanceTerminationOptionProperty(
                    action="action",
                    termination_wait_time_in_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a2f8d93ebeb046531f2392843742b9d9b1cae74c44df29b3bbc8139b10a497ac)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument termination_wait_time_in_minutes", value=termination_wait_time_in_minutes, expected_type=type_hints["termination_wait_time_in_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if termination_wait_time_in_minutes is not None:
                self._values["termination_wait_time_in_minutes"] = termination_wait_time_in_minutes

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action to take on instances in the original environment after a successful blue/green deployment.

            - ``TERMINATE`` : Instances are terminated after a specified wait time.
            - ``KEEP_ALIVE`` : Instances are left running after they are deregistered from the load balancer and removed from the deployment group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-blueinstanceterminationoption.html#cfn-codedeploy-deploymentgroup-blueinstanceterminationoption-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def termination_wait_time_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''For an Amazon EC2 deployment, the number of minutes to wait after a successful blue/green deployment before terminating instances from the original environment.

            For an Amazon ECS deployment, the number of minutes before deleting the original (blue) task set. During an Amazon ECS deployment, CodeDeploy shifts traffic from the original (blue) task set to a replacement (green) task set.

            The maximum setting is 2880 minutes (2 days).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-blueinstanceterminationoption.html#cfn-codedeploy-deploymentgroup-blueinstanceterminationoption-terminationwaittimeinminutes
            '''
            result = self._values.get("termination_wait_time_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BlueInstanceTerminationOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.DeploymentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "ignore_application_stop_failures": "ignoreApplicationStopFailures",
            "revision": "revision",
        },
    )
    class DeploymentProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            ignore_application_stop_failures: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            revision: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.RevisionLocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''``Deployment`` is a property of the `DeploymentGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html>`_ resource that specifies an AWS CodeDeploy application revision to be deployed to instances in the deployment group. If you specify an application revision, your target revision is deployed as soon as the provisioning process is complete.

            :param description: A comment about the deployment.
            :param ignore_application_stop_failures: If true, then if an ``ApplicationStop`` , ``BeforeBlockTraffic`` , or ``AfterBlockTraffic`` deployment lifecycle event to an instance fails, then the deployment continues to the next deployment lifecycle event. For example, if ``ApplicationStop`` fails, the deployment continues with DownloadBundle. If ``BeforeBlockTraffic`` fails, the deployment continues with ``BlockTraffic`` . If ``AfterBlockTraffic`` fails, the deployment continues with ``ApplicationStop`` . If false or not specified, then if a lifecycle event fails during a deployment to an instance, that deployment fails. If deployment to that instance is part of an overall deployment and the number of healthy hosts is not less than the minimum number of healthy hosts, then a deployment to the next instance is attempted. During a deployment, the AWS CodeDeploy agent runs the scripts specified for ``ApplicationStop`` , ``BeforeBlockTraffic`` , and ``AfterBlockTraffic`` in the AppSpec file from the previous successful deployment. (All other scripts are run from the AppSpec file in the current deployment.) If one of these scripts contains an error and does not run successfully, the deployment can fail. If the cause of the failure is a script from the last successful deployment that will never run successfully, create a new deployment and use ``ignoreApplicationStopFailures`` to specify that the ``ApplicationStop`` , ``BeforeBlockTraffic`` , and ``AfterBlockTraffic`` failures should be ignored.
            :param revision: Information about the location of stored application artifacts and the service from which to retrieve them.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                deployment_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.DeploymentProperty(
                    description="description",
                    ignore_application_stop_failures=False,
                    revision=codedeploy_mixins.CfnDeploymentGroupPropsMixin.RevisionLocationProperty(
                        git_hub_location=codedeploy_mixins.CfnDeploymentGroupPropsMixin.GitHubLocationProperty(
                            commit_id="commitId",
                            repository="repository"
                        ),
                        revision_type="revisionType",
                        s3_location=codedeploy_mixins.CfnDeploymentGroupPropsMixin.S3LocationProperty(
                            bucket="bucket",
                            bundle_type="bundleType",
                            e_tag="eTag",
                            key="key",
                            version="version"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e9c133fd9786afb84aaaa034d1a1f247aae2198877e6754833f018495ae72683)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument ignore_application_stop_failures", value=ignore_application_stop_failures, expected_type=type_hints["ignore_application_stop_failures"])
                check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if ignore_application_stop_failures is not None:
                self._values["ignore_application_stop_failures"] = ignore_application_stop_failures
            if revision is not None:
                self._values["revision"] = revision

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A comment about the deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment.html#cfn-codedeploy-deploymentgroup-deployment-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ignore_application_stop_failures(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If true, then if an ``ApplicationStop`` , ``BeforeBlockTraffic`` , or ``AfterBlockTraffic`` deployment lifecycle event to an instance fails, then the deployment continues to the next deployment lifecycle event.

            For example, if ``ApplicationStop`` fails, the deployment continues with DownloadBundle. If ``BeforeBlockTraffic`` fails, the deployment continues with ``BlockTraffic`` . If ``AfterBlockTraffic`` fails, the deployment continues with ``ApplicationStop`` .

            If false or not specified, then if a lifecycle event fails during a deployment to an instance, that deployment fails. If deployment to that instance is part of an overall deployment and the number of healthy hosts is not less than the minimum number of healthy hosts, then a deployment to the next instance is attempted.

            During a deployment, the AWS CodeDeploy agent runs the scripts specified for ``ApplicationStop`` , ``BeforeBlockTraffic`` , and ``AfterBlockTraffic`` in the AppSpec file from the previous successful deployment. (All other scripts are run from the AppSpec file in the current deployment.) If one of these scripts contains an error and does not run successfully, the deployment can fail.

            If the cause of the failure is a script from the last successful deployment that will never run successfully, create a new deployment and use ``ignoreApplicationStopFailures`` to specify that the ``ApplicationStop`` , ``BeforeBlockTraffic`` , and ``AfterBlockTraffic`` failures should be ignored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment.html#cfn-codedeploy-deploymentgroup-deployment-ignoreapplicationstopfailures
            '''
            result = self._values.get("ignore_application_stop_failures")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def revision(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.RevisionLocationProperty"]]:
            '''Information about the location of stored application artifacts and the service from which to retrieve them.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment.html#cfn-codedeploy-deploymentgroup-deployment-revision
            '''
            result = self._values.get("revision")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.RevisionLocationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.DeploymentReadyOptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_on_timeout": "actionOnTimeout",
            "wait_time_in_minutes": "waitTimeInMinutes",
        },
    )
    class DeploymentReadyOptionProperty:
        def __init__(
            self,
            *,
            action_on_timeout: typing.Optional[builtins.str] = None,
            wait_time_in_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information about how traffic is rerouted to instances in a replacement environment in a blue/green deployment.

            :param action_on_timeout: Information about when to reroute traffic from an original environment to a replacement environment in a blue/green deployment. - CONTINUE_DEPLOYMENT: Register new instances with the load balancer immediately after the new application revision is installed on the instances in the replacement environment. - STOP_DEPLOYMENT: Do not register new instances with a load balancer unless traffic rerouting is started using `ContinueDeployment <https://docs.aws.amazon.com/codedeploy/latest/APIReference/API_ContinueDeployment.html>`_ . If traffic rerouting is not started before the end of the specified wait period, the deployment status is changed to Stopped.
            :param wait_time_in_minutes: The number of minutes to wait before the status of a blue/green deployment is changed to Stopped if rerouting is not started manually. Applies only to the ``STOP_DEPLOYMENT`` option for ``actionOnTimeout`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deploymentreadyoption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                deployment_ready_option_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.DeploymentReadyOptionProperty(
                    action_on_timeout="actionOnTimeout",
                    wait_time_in_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d7a4ebad7ded694ce81aeb2921e0d2790c6f78b901ea07ede84965239e80751e)
                check_type(argname="argument action_on_timeout", value=action_on_timeout, expected_type=type_hints["action_on_timeout"])
                check_type(argname="argument wait_time_in_minutes", value=wait_time_in_minutes, expected_type=type_hints["wait_time_in_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action_on_timeout is not None:
                self._values["action_on_timeout"] = action_on_timeout
            if wait_time_in_minutes is not None:
                self._values["wait_time_in_minutes"] = wait_time_in_minutes

        @builtins.property
        def action_on_timeout(self) -> typing.Optional[builtins.str]:
            '''Information about when to reroute traffic from an original environment to a replacement environment in a blue/green deployment.

            - CONTINUE_DEPLOYMENT: Register new instances with the load balancer immediately after the new application revision is installed on the instances in the replacement environment.
            - STOP_DEPLOYMENT: Do not register new instances with a load balancer unless traffic rerouting is started using `ContinueDeployment <https://docs.aws.amazon.com/codedeploy/latest/APIReference/API_ContinueDeployment.html>`_ . If traffic rerouting is not started before the end of the specified wait period, the deployment status is changed to Stopped.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deploymentreadyoption.html#cfn-codedeploy-deploymentgroup-deploymentreadyoption-actionontimeout
            '''
            result = self._values.get("action_on_timeout")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def wait_time_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''The number of minutes to wait before the status of a blue/green deployment is changed to Stopped if rerouting is not started manually.

            Applies only to the ``STOP_DEPLOYMENT`` option for ``actionOnTimeout`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deploymentreadyoption.html#cfn-codedeploy-deploymentgroup-deploymentreadyoption-waittimeinminutes
            '''
            result = self._values.get("wait_time_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentReadyOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.DeploymentStyleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "deployment_option": "deploymentOption",
            "deployment_type": "deploymentType",
        },
    )
    class DeploymentStyleProperty:
        def __init__(
            self,
            *,
            deployment_option: typing.Optional[builtins.str] = None,
            deployment_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the type of deployment, either in-place or blue/green, you want to run and whether to route deployment traffic behind a load balancer.

            :param deployment_option: Indicates whether to route deployment traffic behind a load balancer. .. epigraph:: An Amazon EC2 Application Load Balancer or Network Load Balancer is required for an Amazon ECS deployment.
            :param deployment_type: Indicates whether to run an in-place or blue/green deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deploymentstyle.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                deployment_style_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.DeploymentStyleProperty(
                    deployment_option="deploymentOption",
                    deployment_type="deploymentType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c804eaaee25fb58df3f55bad37e0a7012279300a60de9381a5b39dad79b19c6f)
                check_type(argname="argument deployment_option", value=deployment_option, expected_type=type_hints["deployment_option"])
                check_type(argname="argument deployment_type", value=deployment_type, expected_type=type_hints["deployment_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if deployment_option is not None:
                self._values["deployment_option"] = deployment_option
            if deployment_type is not None:
                self._values["deployment_type"] = deployment_type

        @builtins.property
        def deployment_option(self) -> typing.Optional[builtins.str]:
            '''Indicates whether to route deployment traffic behind a load balancer.

            .. epigraph::

               An Amazon EC2 Application Load Balancer or Network Load Balancer is required for an Amazon ECS deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deploymentstyle.html#cfn-codedeploy-deploymentgroup-deploymentstyle-deploymentoption
            '''
            result = self._values.get("deployment_option")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def deployment_type(self) -> typing.Optional[builtins.str]:
            '''Indicates whether to run an in-place or blue/green deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deploymentstyle.html#cfn-codedeploy-deploymentgroup-deploymentstyle-deploymenttype
            '''
            result = self._values.get("deployment_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentStyleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.EC2TagFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "type": "type", "value": "value"},
    )
    class EC2TagFilterProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about an Amazon EC2 tag filter.

            For more information about using tags and tag groups to help manage your Amazon EC2 instances and on-premises instances, see `Tagging Instances for Deployment Groups in AWS CodeDeploy <https://docs.aws.amazon.com/codedeploy/latest/userguide/instances-tagging.html>`_ in the *AWS CodeDeploy User Guide* .

            :param key: The tag filter key.
            :param type: The tag filter type:. - ``KEY_ONLY`` : Key only. - ``VALUE_ONLY`` : Value only. - ``KEY_AND_VALUE`` : Key and value.
            :param value: The tag filter value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                e_c2_tag_filter_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.EC2TagFilterProperty(
                    key="key",
                    type="type",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1eaa2ccfe42d379776334904525bdc83e35d0dd3b393ad3e187db987ea70554d)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The tag filter key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagfilter.html#cfn-codedeploy-deploymentgroup-ec2tagfilter-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The tag filter type:.

            - ``KEY_ONLY`` : Key only.
            - ``VALUE_ONLY`` : Value only.
            - ``KEY_AND_VALUE`` : Key and value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagfilter.html#cfn-codedeploy-deploymentgroup-ec2tagfilter-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The tag filter value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagfilter.html#cfn-codedeploy-deploymentgroup-ec2tagfilter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EC2TagFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.EC2TagSetListObjectProperty",
        jsii_struct_bases=[],
        name_mapping={"ec2_tag_group": "ec2TagGroup"},
    )
    class EC2TagSetListObjectProperty:
        def __init__(
            self,
            *,
            ec2_tag_group: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.EC2TagFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``EC2TagSet`` property type specifies information about groups of tags applied to Amazon EC2 instances.

            The deployment group includes only Amazon EC2 instances identified by all the tag groups. Cannot be used in the same template as EC2TagFilters.

            For more information about using tags and tag groups to help manage your Amazon EC2 instances and on-premises instances, see `Tagging Instances for Deployment Groups in AWS CodeDeploy <https://docs.aws.amazon.com/codedeploy/latest/userguide/instances-tagging.html>`_ in the *AWS CodeDeploy User Guide* .

            ``EC2TagSet`` is a property of the `DeploymentGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html>`_ resource type.

            :param ec2_tag_group: A list that contains other lists of Amazon EC2 instance tag groups. For an instance to be included in the deployment group, it must be identified by all of the tag groups in the list.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagsetlistobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                e_c2_tag_set_list_object_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.EC2TagSetListObjectProperty(
                    ec2_tag_group=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.EC2TagFilterProperty(
                        key="key",
                        type="type",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5cadcf7f602128e073914eced1f7ef81faf38a9505b236379b2a4a3d489a4a20)
                check_type(argname="argument ec2_tag_group", value=ec2_tag_group, expected_type=type_hints["ec2_tag_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ec2_tag_group is not None:
                self._values["ec2_tag_group"] = ec2_tag_group

        @builtins.property
        def ec2_tag_group(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.EC2TagFilterProperty"]]]]:
            '''A list that contains other lists of Amazon EC2 instance tag groups.

            For an instance to be included in the deployment group, it must be identified by all of the tag groups in the list.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagsetlistobject.html#cfn-codedeploy-deploymentgroup-ec2tagsetlistobject-ec2taggroup
            '''
            result = self._values.get("ec2_tag_group")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.EC2TagFilterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EC2TagSetListObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.EC2TagSetProperty",
        jsii_struct_bases=[],
        name_mapping={"ec2_tag_set_list": "ec2TagSetList"},
    )
    class EC2TagSetProperty:
        def __init__(
            self,
            *,
            ec2_tag_set_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.EC2TagSetListObjectProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``EC2TagSet`` property type specifies information about groups of tags applied to Amazon EC2 instances.

            The deployment group includes only Amazon EC2 instances identified by all the tag groups. ``EC2TagSet`` cannot be used in the same template as ``EC2TagFilter`` .

            For information about using tags and tag groups to help manage your Amazon EC2 instances and on-premises instances, see `Tagging Instances for Deployment Groups in AWS CodeDeploy <https://docs.aws.amazon.com/codedeploy/latest/userguide/instances-tagging.html>`_ .

            :param ec2_tag_set_list: The Amazon EC2 tags that are already applied to Amazon EC2 instances that you want to include in the deployment group. CodeDeploy includes all Amazon EC2 instances identified by any of the tags you specify in this deployment group. Duplicates are not allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagset.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                e_c2_tag_set_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.EC2TagSetProperty(
                    ec2_tag_set_list=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.EC2TagSetListObjectProperty(
                        ec2_tag_group=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.EC2TagFilterProperty(
                            key="key",
                            type="type",
                            value="value"
                        )]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a51968364f92bd998f09493663d02db433482c5be2f1c7707376e03449d6011f)
                check_type(argname="argument ec2_tag_set_list", value=ec2_tag_set_list, expected_type=type_hints["ec2_tag_set_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ec2_tag_set_list is not None:
                self._values["ec2_tag_set_list"] = ec2_tag_set_list

        @builtins.property
        def ec2_tag_set_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.EC2TagSetListObjectProperty"]]]]:
            '''The Amazon EC2 tags that are already applied to Amazon EC2 instances that you want to include in the deployment group.

            CodeDeploy includes all Amazon EC2 instances identified by any of the tags you specify in this deployment group.

            Duplicates are not allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagset.html#cfn-codedeploy-deploymentgroup-ec2tagset-ec2tagsetlist
            '''
            result = self._values.get("ec2_tag_set_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.EC2TagSetListObjectProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EC2TagSetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.ECSServiceProperty",
        jsii_struct_bases=[],
        name_mapping={"cluster_name": "clusterName", "service_name": "serviceName"},
    )
    class ECSServiceProperty:
        def __init__(
            self,
            *,
            cluster_name: typing.Optional[builtins.str] = None,
            service_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains the service and cluster names used to identify an Amazon ECS deployment's target.

            :param cluster_name: The name of the cluster that the Amazon ECS service is associated with.
            :param service_name: The name of the target Amazon ECS service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ecsservice.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                e_cSService_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.ECSServiceProperty(
                    cluster_name="clusterName",
                    service_name="serviceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0de548bfcd9840c76bb9547cabaa17cb0454f531129885f26953e88c5a899136)
                check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
                check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cluster_name is not None:
                self._values["cluster_name"] = cluster_name
            if service_name is not None:
                self._values["service_name"] = service_name

        @builtins.property
        def cluster_name(self) -> typing.Optional[builtins.str]:
            '''The name of the cluster that the Amazon ECS service is associated with.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ecsservice.html#cfn-codedeploy-deploymentgroup-ecsservice-clustername
            '''
            result = self._values.get("cluster_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_name(self) -> typing.Optional[builtins.str]:
            '''The name of the target Amazon ECS service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ecsservice.html#cfn-codedeploy-deploymentgroup-ecsservice-servicename
            '''
            result = self._values.get("service_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ECSServiceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.ELBInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class ELBInfoProperty:
        def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
            '''The ``ELBInfo`` property type specifies information about the ELB load balancer used for an CodeDeploy deployment group.

            If you specify the ``ELBInfo`` property, the ``DeploymentStyle.DeploymentOption`` property must be set to ``WITH_TRAFFIC_CONTROL`` for AWS CodeDeploy to route your traffic using the specified load balancers.

            ``ELBInfo`` is a property of the `AWS CodeDeploy DeploymentGroup LoadBalancerInfo <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-loadbalancerinfo.html>`_ property type.

            :param name: For blue/green deployments, the name of the load balancer that is used to route traffic from original instances to replacement instances in a blue/green deployment. For in-place deployments, the name of the load balancer that instances are deregistered from so they are not serving traffic during a deployment, and then re-registered with after the deployment is complete. .. epigraph:: CloudFormation supports blue/green deployments on AWS Lambda compute platforms only.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-elbinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                e_lBInfo_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.ELBInfoProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__444360e44b01538725adcfe7ff5bbb2b998c4015f777a9038aa10679271ba1e5)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''For blue/green deployments, the name of the load balancer that is used to route traffic from original instances to replacement instances in a blue/green deployment.

            For in-place deployments, the name of the load balancer that instances are deregistered from so they are not serving traffic during a deployment, and then re-registered with after the deployment is complete.
            .. epigraph::

               CloudFormation supports blue/green deployments on AWS Lambda compute platforms only.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-elbinfo.html#cfn-codedeploy-deploymentgroup-elbinfo-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ELBInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.GitHubLocationProperty",
        jsii_struct_bases=[],
        name_mapping={"commit_id": "commitId", "repository": "repository"},
    )
    class GitHubLocationProperty:
        def __init__(
            self,
            *,
            commit_id: typing.Optional[builtins.str] = None,
            repository: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``GitHubLocation`` is a property of the `CodeDeploy DeploymentGroup Revision <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision.html>`_ property that specifies the location of an application revision that is stored in GitHub.

            :param commit_id: The SHA1 commit ID of the GitHub commit that represents the bundled artifacts for the application revision.
            :param repository: The GitHub account and repository pair that stores a reference to the commit that represents the bundled artifacts for the application revision. Specify the value as ``account/repository`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-githublocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                git_hub_location_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.GitHubLocationProperty(
                    commit_id="commitId",
                    repository="repository"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c8a097f934e5908ee8a9590e993b2865813e6c1ef684d2ef111c1154f3dfa8df)
                check_type(argname="argument commit_id", value=commit_id, expected_type=type_hints["commit_id"])
                check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if commit_id is not None:
                self._values["commit_id"] = commit_id
            if repository is not None:
                self._values["repository"] = repository

        @builtins.property
        def commit_id(self) -> typing.Optional[builtins.str]:
            '''The SHA1 commit ID of the GitHub commit that represents the bundled artifacts for the application revision.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-githublocation.html#cfn-codedeploy-deploymentgroup-githublocation-commitid
            '''
            result = self._values.get("commit_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def repository(self) -> typing.Optional[builtins.str]:
            '''The GitHub account and repository pair that stores a reference to the commit that represents the bundled artifacts for the application revision.

            Specify the value as ``account/repository`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-githublocation.html#cfn-codedeploy-deploymentgroup-githublocation-repository
            '''
            result = self._values.get("repository")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GitHubLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.GreenFleetProvisioningOptionProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action"},
    )
    class GreenFleetProvisioningOptionProperty:
        def __init__(self, *, action: typing.Optional[builtins.str] = None) -> None:
            '''Information about the instances that belong to the replacement environment in a blue/green deployment.

            :param action: The method used to add instances to a replacement environment. - ``DISCOVER_EXISTING`` : Use instances that already exist or will be created manually. - ``COPY_AUTO_SCALING_GROUP`` : Use settings from a specified Amazon EC2 Auto Scaling group to define and create instances in a new Amazon EC2 Auto Scaling group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-greenfleetprovisioningoption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                green_fleet_provisioning_option_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.GreenFleetProvisioningOptionProperty(
                    action="action"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__45b1abdc2bd8f455fb55792770cd3785e9069fef438d3bfe8579f656ae742480)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The method used to add instances to a replacement environment.

            - ``DISCOVER_EXISTING`` : Use instances that already exist or will be created manually.
            - ``COPY_AUTO_SCALING_GROUP`` : Use settings from a specified Amazon EC2 Auto Scaling group to define and create instances in a new Amazon EC2 Auto Scaling group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-greenfleetprovisioningoption.html#cfn-codedeploy-deploymentgroup-greenfleetprovisioningoption-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GreenFleetProvisioningOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.LoadBalancerInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "elb_info_list": "elbInfoList",
            "target_group_info_list": "targetGroupInfoList",
            "target_group_pair_info_list": "targetGroupPairInfoList",
        },
    )
    class LoadBalancerInfoProperty:
        def __init__(
            self,
            *,
            elb_info_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.ELBInfoProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            target_group_info_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.TargetGroupInfoProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            target_group_pair_info_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.TargetGroupPairInfoProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``LoadBalancerInfo`` property type specifies information about the load balancer or target group used for an AWS CodeDeploy deployment group.

            For more information, see `Integrating CodeDeploy with ELB <https://docs.aws.amazon.com/codedeploy/latest/userguide/integrations-aws-elastic-load-balancing.html>`_ in the *AWS CodeDeploy User Guide* .

            For CloudFormation to use the properties specified in ``LoadBalancerInfo`` , the ``DeploymentStyle.DeploymentOption`` property must be set to ``WITH_TRAFFIC_CONTROL`` . If ``DeploymentStyle.DeploymentOption`` is not set to ``WITH_TRAFFIC_CONTROL`` , CloudFormation ignores any settings specified in ``LoadBalancerInfo`` .
            .. epigraph::

               CloudFormation supports blue/green deployments on the AWS Lambda compute platform only.

            ``LoadBalancerInfo`` is a property of the `DeploymentGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html>`_ resource.

            :param elb_info_list: An array that contains information about the load balancers to use for load balancing in a deployment. If you're using Classic Load Balancers, specify those load balancers in this array. .. epigraph:: You can add up to 10 load balancers to the array. > If you're using Application Load Balancers or Network Load Balancers, use the ``targetGroupInfoList`` array instead of this one.
            :param target_group_info_list: An array that contains information about the target groups to use for load balancing in a deployment. If you're using Application Load Balancers and Network Load Balancers, specify their associated target groups in this array. .. epigraph:: You can add up to 10 target groups to the array. > If you're using Classic Load Balancers, use the ``elbInfoList`` array instead of this one.
            :param target_group_pair_info_list: The target group pair information. This is an array of ``TargeGroupPairInfo`` objects with a maximum size of one.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-loadbalancerinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                load_balancer_info_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.LoadBalancerInfoProperty(
                    elb_info_list=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.ELBInfoProperty(
                        name="name"
                    )],
                    target_group_info_list=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.TargetGroupInfoProperty(
                        name="name"
                    )],
                    target_group_pair_info_list=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.TargetGroupPairInfoProperty(
                        prod_traffic_route=codedeploy_mixins.CfnDeploymentGroupPropsMixin.TrafficRouteProperty(
                            listener_arns=["listenerArns"]
                        ),
                        target_groups=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.TargetGroupInfoProperty(
                            name="name"
                        )],
                        test_traffic_route=codedeploy_mixins.CfnDeploymentGroupPropsMixin.TrafficRouteProperty(
                            listener_arns=["listenerArns"]
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__38aa28b11e717fff11bcf187c0502de7f457166d05f14bd2dde2fe8f5e831c83)
                check_type(argname="argument elb_info_list", value=elb_info_list, expected_type=type_hints["elb_info_list"])
                check_type(argname="argument target_group_info_list", value=target_group_info_list, expected_type=type_hints["target_group_info_list"])
                check_type(argname="argument target_group_pair_info_list", value=target_group_pair_info_list, expected_type=type_hints["target_group_pair_info_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if elb_info_list is not None:
                self._values["elb_info_list"] = elb_info_list
            if target_group_info_list is not None:
                self._values["target_group_info_list"] = target_group_info_list
            if target_group_pair_info_list is not None:
                self._values["target_group_pair_info_list"] = target_group_pair_info_list

        @builtins.property
        def elb_info_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.ELBInfoProperty"]]]]:
            '''An array that contains information about the load balancers to use for load balancing in a deployment.

            If you're using Classic Load Balancers, specify those load balancers in this array.
            .. epigraph::

               You can add up to 10 load balancers to the array. > If you're using Application Load Balancers or Network Load Balancers, use the ``targetGroupInfoList`` array instead of this one.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-loadbalancerinfo.html#cfn-codedeploy-deploymentgroup-loadbalancerinfo-elbinfolist
            '''
            result = self._values.get("elb_info_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.ELBInfoProperty"]]]], result)

        @builtins.property
        def target_group_info_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.TargetGroupInfoProperty"]]]]:
            '''An array that contains information about the target groups to use for load balancing in a deployment.

            If you're using Application Load Balancers and Network Load Balancers, specify their associated target groups in this array.
            .. epigraph::

               You can add up to 10 target groups to the array. > If you're using Classic Load Balancers, use the ``elbInfoList`` array instead of this one.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-loadbalancerinfo.html#cfn-codedeploy-deploymentgroup-loadbalancerinfo-targetgroupinfolist
            '''
            result = self._values.get("target_group_info_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.TargetGroupInfoProperty"]]]], result)

        @builtins.property
        def target_group_pair_info_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.TargetGroupPairInfoProperty"]]]]:
            '''The target group pair information.

            This is an array of ``TargeGroupPairInfo`` objects with a maximum size of one.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-loadbalancerinfo.html#cfn-codedeploy-deploymentgroup-loadbalancerinfo-targetgrouppairinfolist
            '''
            result = self._values.get("target_group_pair_info_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.TargetGroupPairInfoProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoadBalancerInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.OnPremisesTagSetListObjectProperty",
        jsii_struct_bases=[],
        name_mapping={"on_premises_tag_group": "onPremisesTagGroup"},
    )
    class OnPremisesTagSetListObjectProperty:
        def __init__(
            self,
            *,
            on_premises_tag_group: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.TagFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``OnPremisesTagSetListObject`` property type specifies lists of on-premises instance tag groups.

            In order for an instance to be included in the deployment group, it must be identified by all the tag groups in the list.

            ``OnPremisesTagSetListObject`` is a property of the `CodeDeploy DeploymentGroup OnPremisesTagSet <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-onpremisestagset.html>`_ property type.

            :param on_premises_tag_group: Information about groups of on-premises instance tags.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-onpremisestagsetlistobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                on_premises_tag_set_list_object_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.OnPremisesTagSetListObjectProperty(
                    on_premises_tag_group=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.TagFilterProperty(
                        key="key",
                        type="type",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__38e61dc1820401a3cad44fa7b3ef49eec19b2a66ba8950d272a3329078bc71e8)
                check_type(argname="argument on_premises_tag_group", value=on_premises_tag_group, expected_type=type_hints["on_premises_tag_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if on_premises_tag_group is not None:
                self._values["on_premises_tag_group"] = on_premises_tag_group

        @builtins.property
        def on_premises_tag_group(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.TagFilterProperty"]]]]:
            '''Information about groups of on-premises instance tags.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-onpremisestagsetlistobject.html#cfn-codedeploy-deploymentgroup-onpremisestagsetlistobject-onpremisestaggroup
            '''
            result = self._values.get("on_premises_tag_group")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.TagFilterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnPremisesTagSetListObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.OnPremisesTagSetProperty",
        jsii_struct_bases=[],
        name_mapping={"on_premises_tag_set_list": "onPremisesTagSetList"},
    )
    class OnPremisesTagSetProperty:
        def __init__(
            self,
            *,
            on_premises_tag_set_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.OnPremisesTagSetListObjectProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``OnPremisesTagSet`` property type specifies a list containing other lists of on-premises instance tag groups.

            In order for an instance to be included in the deployment group, it must be identified by all the tag groups in the list.

            For more information about using tags and tag groups to help manage your Amazon EC2 instances and on-premises instances, see `Tagging Instances for Deployment Groups in AWS CodeDeploy <https://docs.aws.amazon.com/codedeploy/latest/userguide/instances-tagging.html>`_ in the *AWS CodeDeploy User Guide* .

            ``OnPremisesTagSet`` is a property of the `DeploymentGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html>`_ resource.

            :param on_premises_tag_set_list: A list that contains other lists of on-premises instance tag groups. For an instance to be included in the deployment group, it must be identified by all of the tag groups in the list. Duplicates are not allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-onpremisestagset.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                on_premises_tag_set_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.OnPremisesTagSetProperty(
                    on_premises_tag_set_list=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.OnPremisesTagSetListObjectProperty(
                        on_premises_tag_group=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.TagFilterProperty(
                            key="key",
                            type="type",
                            value="value"
                        )]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cc930d8f085b841b2c789263c21d0908d109468786dd0b6556ef9d10c1a0fc87)
                check_type(argname="argument on_premises_tag_set_list", value=on_premises_tag_set_list, expected_type=type_hints["on_premises_tag_set_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if on_premises_tag_set_list is not None:
                self._values["on_premises_tag_set_list"] = on_premises_tag_set_list

        @builtins.property
        def on_premises_tag_set_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.OnPremisesTagSetListObjectProperty"]]]]:
            '''A list that contains other lists of on-premises instance tag groups.

            For an instance to be included in the deployment group, it must be identified by all of the tag groups in the list.

            Duplicates are not allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-onpremisestagset.html#cfn-codedeploy-deploymentgroup-onpremisestagset-onpremisestagsetlist
            '''
            result = self._values.get("on_premises_tag_set_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.OnPremisesTagSetListObjectProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnPremisesTagSetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.RevisionLocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "git_hub_location": "gitHubLocation",
            "revision_type": "revisionType",
            "s3_location": "s3Location",
        },
    )
    class RevisionLocationProperty:
        def __init__(
            self,
            *,
            git_hub_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.GitHubLocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            revision_type: typing.Optional[builtins.str] = None,
            s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''``RevisionLocation`` is a property that defines the location of the CodeDeploy application revision to deploy.

            :param git_hub_location: Information about the location of application artifacts stored in GitHub.
            :param revision_type: The type of application revision:. - S3: An application revision stored in Amazon S3. - GitHub: An application revision stored in GitHub (EC2/On-premises deployments only). - String: A YAML-formatted or JSON-formatted string ( AWS Lambda deployments only). - AppSpecContent: An ``AppSpecContent`` object that contains the contents of an AppSpec file for an AWS Lambda or Amazon ECS deployment. The content is formatted as JSON or YAML stored as a RawString.
            :param s3_location: Information about the location of a revision stored in Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-revisionlocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                revision_location_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.RevisionLocationProperty(
                    git_hub_location=codedeploy_mixins.CfnDeploymentGroupPropsMixin.GitHubLocationProperty(
                        commit_id="commitId",
                        repository="repository"
                    ),
                    revision_type="revisionType",
                    s3_location=codedeploy_mixins.CfnDeploymentGroupPropsMixin.S3LocationProperty(
                        bucket="bucket",
                        bundle_type="bundleType",
                        e_tag="eTag",
                        key="key",
                        version="version"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a2cc2581b9f1a9e9e7dfd610534b23b16cebc6b5083e9a07e76a7cd537571d05)
                check_type(argname="argument git_hub_location", value=git_hub_location, expected_type=type_hints["git_hub_location"])
                check_type(argname="argument revision_type", value=revision_type, expected_type=type_hints["revision_type"])
                check_type(argname="argument s3_location", value=s3_location, expected_type=type_hints["s3_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if git_hub_location is not None:
                self._values["git_hub_location"] = git_hub_location
            if revision_type is not None:
                self._values["revision_type"] = revision_type
            if s3_location is not None:
                self._values["s3_location"] = s3_location

        @builtins.property
        def git_hub_location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.GitHubLocationProperty"]]:
            '''Information about the location of application artifacts stored in GitHub.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-revisionlocation.html#cfn-codedeploy-deploymentgroup-revisionlocation-githublocation
            '''
            result = self._values.get("git_hub_location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.GitHubLocationProperty"]], result)

        @builtins.property
        def revision_type(self) -> typing.Optional[builtins.str]:
            '''The type of application revision:.

            - S3: An application revision stored in Amazon S3.
            - GitHub: An application revision stored in GitHub (EC2/On-premises deployments only).
            - String: A YAML-formatted or JSON-formatted string ( AWS Lambda deployments only).
            - AppSpecContent: An ``AppSpecContent`` object that contains the contents of an AppSpec file for an AWS Lambda or Amazon ECS deployment. The content is formatted as JSON or YAML stored as a RawString.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-revisionlocation.html#cfn-codedeploy-deploymentgroup-revisionlocation-revisiontype
            '''
            result = self._values.get("revision_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.S3LocationProperty"]]:
            '''Information about the location of a revision stored in Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-revisionlocation.html#cfn-codedeploy-deploymentgroup-revisionlocation-s3location
            '''
            result = self._values.get("s3_location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.S3LocationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RevisionLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "bundle_type": "bundleType",
            "e_tag": "eTag",
            "key": "key",
            "version": "version",
        },
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            bundle_type: typing.Optional[builtins.str] = None,
            e_tag: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``S3Location`` is a property of the `CodeDeploy DeploymentGroup Revision <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision.html>`_ property that specifies the location of an application revision that is stored in Amazon Simple Storage Service ( Amazon S3 ).

            :param bucket: The name of the Amazon S3 bucket where the application revision is stored.
            :param bundle_type: The file type of the application revision. Must be one of the following:. - JSON - tar: A tar archive file. - tgz: A compressed tar archive file. - YAML - zip: A zip archive file.
            :param e_tag: The ETag of the Amazon S3 object that represents the bundled artifacts for the application revision. If the ETag is not specified as an input parameter, ETag validation of the object is skipped.
            :param key: The name of the Amazon S3 object that represents the bundled artifacts for the application revision.
            :param version: A specific version of the Amazon S3 object that represents the bundled artifacts for the application revision. If the version is not specified, the system uses the most recent version by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                s3_location_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.S3LocationProperty(
                    bucket="bucket",
                    bundle_type="bundleType",
                    e_tag="eTag",
                    key="key",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ef5667934f7dfb19eba837b855edd057406a5fe7b5ae8fc69b7ae892b88706cd)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument bundle_type", value=bundle_type, expected_type=type_hints["bundle_type"])
                check_type(argname="argument e_tag", value=e_tag, expected_type=type_hints["e_tag"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if bundle_type is not None:
                self._values["bundle_type"] = bundle_type
            if e_tag is not None:
                self._values["e_tag"] = e_tag
            if key is not None:
                self._values["key"] = key
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon S3 bucket where the application revision is stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-s3location.html#cfn-codedeploy-deploymentgroup-s3location-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bundle_type(self) -> typing.Optional[builtins.str]:
            '''The file type of the application revision. Must be one of the following:.

            - JSON
            - tar: A tar archive file.
            - tgz: A compressed tar archive file.
            - YAML
            - zip: A zip archive file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-s3location.html#cfn-codedeploy-deploymentgroup-s3location-bundletype
            '''
            result = self._values.get("bundle_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def e_tag(self) -> typing.Optional[builtins.str]:
            '''The ETag of the Amazon S3 object that represents the bundled artifacts for the application revision.

            If the ETag is not specified as an input parameter, ETag validation of the object is skipped.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-s3location.html#cfn-codedeploy-deploymentgroup-s3location-etag
            '''
            result = self._values.get("e_tag")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon S3 object that represents the bundled artifacts for the application revision.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-s3location.html#cfn-codedeploy-deploymentgroup-s3location-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''A specific version of the Amazon S3 object that represents the bundled artifacts for the application revision.

            If the version is not specified, the system uses the most recent version by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-s3location.html#cfn-codedeploy-deploymentgroup-s3location-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.TagFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "type": "type", "value": "value"},
    )
    class TagFilterProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``TagFilter`` is a property type of the `AWS::CodeDeploy::DeploymentGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html>`_ resource that specifies which on-premises instances to associate with the deployment group. To register on-premise instances with AWS CodeDeploy , see `Configure Existing On-Premises Instances by Using AWS CodeDeploy <https://docs.aws.amazon.com/codedeploy/latest/userguide/instances-on-premises.html>`_ in the *AWS CodeDeploy User Guide* .

            For more information about using tags and tag groups to help manage your Amazon EC2 instances and on-premises instances, see `Tagging Instances for Deployment Groups in AWS CodeDeploy <https://docs.aws.amazon.com/codedeploy/latest/userguide/instances-tagging.html>`_ in the *AWS CodeDeploy User Guide* .

            :param key: The on-premises instance tag filter key.
            :param type: The on-premises instance tag filter type:. - KEY_ONLY: Key only. - VALUE_ONLY: Value only. - KEY_AND_VALUE: Key and value.
            :param value: The on-premises instance tag filter value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-tagfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                tag_filter_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.TagFilterProperty(
                    key="key",
                    type="type",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6e56b9ee265d0f0e0aac68760a46984d9dc1f3898ef1b645a020518f6ff335ca)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The on-premises instance tag filter key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-tagfilter.html#cfn-codedeploy-deploymentgroup-tagfilter-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The on-premises instance tag filter type:.

            - KEY_ONLY: Key only.
            - VALUE_ONLY: Value only.
            - KEY_AND_VALUE: Key and value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-tagfilter.html#cfn-codedeploy-deploymentgroup-tagfilter-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The on-premises instance tag filter value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-tagfilter.html#cfn-codedeploy-deploymentgroup-tagfilter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.TargetGroupInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class TargetGroupInfoProperty:
        def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
            '''The ``TargetGroupInfo`` property type specifies information about a target group in ELB to use in a deployment.

            Instances are registered as targets in a target group, and traffic is routed to the target group. For more information, see `TargetGroupInfo <https://docs.aws.amazon.com/codedeploy/latest/APIReference/API_TargetGroupInfo.html>`_ in the *AWS CodeDeploy API Reference*

            If you specify the ``TargetGroupInfo`` property, the ``DeploymentStyle.DeploymentOption`` property must be set to ``WITH_TRAFFIC_CONTROL`` for CodeDeploy to route your traffic using the specified target groups.

            ``TargetGroupInfo`` is a property of the `LoadBalancerInfo <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-loadbalancerinfo.html>`_ property type.

            :param name: For blue/green deployments, the name of the target group that instances in the original environment are deregistered from, and instances in the replacement environment registered with. For in-place deployments, the name of the target group that instances are deregistered from, so they are not serving traffic during a deployment, and then re-registered with after the deployment completes. No duplicates allowed. .. epigraph:: CloudFormation supports blue/green deployments on AWS Lambda compute platforms only. This value cannot exceed 32 characters, so you should use the ``Name`` property of the target group, or the ``TargetGroupName`` attribute with the ``Fn::GetAtt`` intrinsic function, as shown in the following example. Don't use the group's Amazon Resource Name (ARN) or ``TargetGroupFullName`` attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-targetgroupinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                target_group_info_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.TargetGroupInfoProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0aeab93bfc751240ebe5c0c1ecb5d8d9502897179d27c0747a01c9065784d783)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''For blue/green deployments, the name of the target group that instances in the original environment are deregistered from, and instances in the replacement environment registered with.

            For in-place deployments, the name of the target group that instances are deregistered from, so they are not serving traffic during a deployment, and then re-registered with after the deployment completes. No duplicates allowed.
            .. epigraph::

               CloudFormation supports blue/green deployments on AWS Lambda compute platforms only.

            This value cannot exceed 32 characters, so you should use the ``Name`` property of the target group, or the ``TargetGroupName`` attribute with the ``Fn::GetAtt`` intrinsic function, as shown in the following example. Don't use the group's Amazon Resource Name (ARN) or ``TargetGroupFullName`` attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-targetgroupinfo.html#cfn-codedeploy-deploymentgroup-targetgroupinfo-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetGroupInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.TargetGroupPairInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "prod_traffic_route": "prodTrafficRoute",
            "target_groups": "targetGroups",
            "test_traffic_route": "testTrafficRoute",
        },
    )
    class TargetGroupPairInfoProperty:
        def __init__(
            self,
            *,
            prod_traffic_route: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.TrafficRouteProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            target_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.TargetGroupInfoProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            test_traffic_route: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentGroupPropsMixin.TrafficRouteProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about two target groups and how traffic is routed during an Amazon ECS deployment.

            An optional test traffic route can be specified.

            :param prod_traffic_route: The path used by a load balancer to route production traffic when an Amazon ECS deployment is complete.
            :param target_groups: One pair of target groups. One is associated with the original task set. The second is associated with the task set that serves traffic after the deployment is complete.
            :param test_traffic_route: An optional path used by a load balancer to route test traffic after an Amazon ECS deployment. Validation can occur while test traffic is served during a deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-targetgrouppairinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                target_group_pair_info_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.TargetGroupPairInfoProperty(
                    prod_traffic_route=codedeploy_mixins.CfnDeploymentGroupPropsMixin.TrafficRouteProperty(
                        listener_arns=["listenerArns"]
                    ),
                    target_groups=[codedeploy_mixins.CfnDeploymentGroupPropsMixin.TargetGroupInfoProperty(
                        name="name"
                    )],
                    test_traffic_route=codedeploy_mixins.CfnDeploymentGroupPropsMixin.TrafficRouteProperty(
                        listener_arns=["listenerArns"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__db94dcc16e7c05c0815817dd93cf464e0c95d6bb6fc672ae027a82500437764d)
                check_type(argname="argument prod_traffic_route", value=prod_traffic_route, expected_type=type_hints["prod_traffic_route"])
                check_type(argname="argument target_groups", value=target_groups, expected_type=type_hints["target_groups"])
                check_type(argname="argument test_traffic_route", value=test_traffic_route, expected_type=type_hints["test_traffic_route"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if prod_traffic_route is not None:
                self._values["prod_traffic_route"] = prod_traffic_route
            if target_groups is not None:
                self._values["target_groups"] = target_groups
            if test_traffic_route is not None:
                self._values["test_traffic_route"] = test_traffic_route

        @builtins.property
        def prod_traffic_route(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.TrafficRouteProperty"]]:
            '''The path used by a load balancer to route production traffic when an Amazon ECS deployment is complete.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-targetgrouppairinfo.html#cfn-codedeploy-deploymentgroup-targetgrouppairinfo-prodtrafficroute
            '''
            result = self._values.get("prod_traffic_route")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.TrafficRouteProperty"]], result)

        @builtins.property
        def target_groups(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.TargetGroupInfoProperty"]]]]:
            '''One pair of target groups.

            One is associated with the original task set. The second is associated with the task set that serves traffic after the deployment is complete.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-targetgrouppairinfo.html#cfn-codedeploy-deploymentgroup-targetgrouppairinfo-targetgroups
            '''
            result = self._values.get("target_groups")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.TargetGroupInfoProperty"]]]], result)

        @builtins.property
        def test_traffic_route(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.TrafficRouteProperty"]]:
            '''An optional path used by a load balancer to route test traffic after an Amazon ECS deployment.

            Validation can occur while test traffic is served during a deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-targetgrouppairinfo.html#cfn-codedeploy-deploymentgroup-targetgrouppairinfo-testtrafficroute
            '''
            result = self._values.get("test_traffic_route")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentGroupPropsMixin.TrafficRouteProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetGroupPairInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.TrafficRouteProperty",
        jsii_struct_bases=[],
        name_mapping={"listener_arns": "listenerArns"},
    )
    class TrafficRouteProperty:
        def __init__(
            self,
            *,
            listener_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Information about a listener.

            The listener contains the path used to route traffic that is received from the load balancer to a target group.

            :param listener_arns: The Amazon Resource Name (ARN) of one listener. The listener identifies the route between a target group and a load balancer. This is an array of strings with a maximum size of one.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-trafficroute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                traffic_route_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.TrafficRouteProperty(
                    listener_arns=["listenerArns"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8902e51ce236fc2bc693e1f5e58c0152e40f708c269763fcd1ca67db55da851b)
                check_type(argname="argument listener_arns", value=listener_arns, expected_type=type_hints["listener_arns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if listener_arns is not None:
                self._values["listener_arns"] = listener_arns

        @builtins.property
        def listener_arns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The Amazon Resource Name (ARN) of one listener.

            The listener identifies the route between a target group and a load balancer. This is an array of strings with a maximum size of one.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-trafficroute.html#cfn-codedeploy-deploymentgroup-trafficroute-listenerarns
            '''
            result = self._values.get("listener_arns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TrafficRouteProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codedeploy.mixins.CfnDeploymentGroupPropsMixin.TriggerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "trigger_events": "triggerEvents",
            "trigger_name": "triggerName",
            "trigger_target_arn": "triggerTargetArn",
        },
    )
    class TriggerConfigProperty:
        def __init__(
            self,
            *,
            trigger_events: typing.Optional[typing.Sequence[builtins.str]] = None,
            trigger_name: typing.Optional[builtins.str] = None,
            trigger_target_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about notification triggers for the deployment group.

            :param trigger_events: The event type or types that trigger notifications.
            :param trigger_name: The name of the notification trigger.
            :param trigger_target_arn: The Amazon Resource Name (ARN) of the Amazon Simple Notification Service topic through which notifications about deployment or instance events are sent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-triggerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codedeploy import mixins as codedeploy_mixins
                
                trigger_config_property = codedeploy_mixins.CfnDeploymentGroupPropsMixin.TriggerConfigProperty(
                    trigger_events=["triggerEvents"],
                    trigger_name="triggerName",
                    trigger_target_arn="triggerTargetArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5ee8eb38cce3d00c16d7278b16e47147e76d029d0a4bb4584da964e0ad2413e4)
                check_type(argname="argument trigger_events", value=trigger_events, expected_type=type_hints["trigger_events"])
                check_type(argname="argument trigger_name", value=trigger_name, expected_type=type_hints["trigger_name"])
                check_type(argname="argument trigger_target_arn", value=trigger_target_arn, expected_type=type_hints["trigger_target_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if trigger_events is not None:
                self._values["trigger_events"] = trigger_events
            if trigger_name is not None:
                self._values["trigger_name"] = trigger_name
            if trigger_target_arn is not None:
                self._values["trigger_target_arn"] = trigger_target_arn

        @builtins.property
        def trigger_events(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The event type or types that trigger notifications.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-triggerconfig.html#cfn-codedeploy-deploymentgroup-triggerconfig-triggerevents
            '''
            result = self._values.get("trigger_events")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def trigger_name(self) -> typing.Optional[builtins.str]:
            '''The name of the notification trigger.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-triggerconfig.html#cfn-codedeploy-deploymentgroup-triggerconfig-triggername
            '''
            result = self._values.get("trigger_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def trigger_target_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon Simple Notification Service topic through which notifications about deployment or instance events are sent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-triggerconfig.html#cfn-codedeploy-deploymentgroup-triggerconfig-triggertargetarn
            '''
            result = self._values.get("trigger_target_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TriggerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnApplicationMixinProps",
    "CfnApplicationPropsMixin",
    "CfnDeploymentConfigMixinProps",
    "CfnDeploymentConfigPropsMixin",
    "CfnDeploymentGroupMixinProps",
    "CfnDeploymentGroupPropsMixin",
]

publication.publish()

def _typecheckingstub__c9922994ee16b14d481ca65862354242a86ceb7596b105d24c5d3f3c72d888ad(
    *,
    application_name: typing.Optional[builtins.str] = None,
    compute_platform: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40927613ae7f44db9986a939a06abf06f85734fe34ea2cdd80b696907b392305(
    props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaa42e09551a360f1655ff1bf5ba3112f516b28b5eac228964cf3e67715fb7e6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__897abd8cda7a779d2b19ac6c8ec327b503858f02e06a9602234435e3125a31e0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8058eeae33fe8c9638aac58461c0d0f60dff85246919dfc1556172660aacc2b4(
    *,
    compute_platform: typing.Optional[builtins.str] = None,
    deployment_config_name: typing.Optional[builtins.str] = None,
    minimum_healthy_hosts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentConfigPropsMixin.MinimumHealthyHostsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    traffic_routing_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentConfigPropsMixin.TrafficRoutingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    zonal_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentConfigPropsMixin.ZonalConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2599c5863f2d0fdf46cc07e1cf6c374fea09df43a4ed825ffab7797936466400(
    props: typing.Union[CfnDeploymentConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ba75513d03506052a9f7ad261f311bf709327ce1b3e8a53410f267b4e02545(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9268e9c0ccde6c53c0e3a604fe618d600777f5a8b504651b35e4111c03190868(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c6a41708b4039e371d33a39453b6ccc9299625df70d7c2bdacd441c2a6be7f6(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eabdf224ebb36fa5643804d9788ab45d27108f6d5117d1d52b4f59bd15f43610(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__debf2e63d591511519f4f720804140b3385d2ef86de0a5aa3817e54e41e38bcf(
    *,
    canary_interval: typing.Optional[jsii.Number] = None,
    canary_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ded0fef4a5acccbf0db88069f379f33d572517df04442b9e1238e64072f19c66(
    *,
    linear_interval: typing.Optional[jsii.Number] = None,
    linear_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa8882e1528a36275c594ee1a27b13d1cb37396df3a0cc0051458fb88ff9b76(
    *,
    time_based_canary: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentConfigPropsMixin.TimeBasedCanaryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    time_based_linear: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentConfigPropsMixin.TimeBasedLinearProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95ccba8bcf1b9115c6538fc8978f6db17b54dcc4a34fe9f285be6dc373562814(
    *,
    first_zone_monitor_duration_in_seconds: typing.Optional[jsii.Number] = None,
    minimum_healthy_hosts_per_zone: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentConfigPropsMixin.MinimumHealthyHostsPerZoneProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    monitor_duration_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__628b02985efb38d1cbcd86f1dc7cc55f335721b16a452ef1b4e0e2040dfedd56(
    *,
    alarm_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.AlarmConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    application_name: typing.Optional[builtins.str] = None,
    auto_rollback_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.AutoRollbackConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    auto_scaling_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    blue_green_deployment_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.BlueGreenDeploymentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    deployment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.DeploymentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    deployment_config_name: typing.Optional[builtins.str] = None,
    deployment_group_name: typing.Optional[builtins.str] = None,
    deployment_style: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.DeploymentStyleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ec2_tag_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.EC2TagFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ec2_tag_set: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.EC2TagSetProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ecs_services: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.ECSServiceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    load_balancer_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.LoadBalancerInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    on_premises_instance_tag_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.TagFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    on_premises_tag_set: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.OnPremisesTagSetProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    outdated_instances_strategy: typing.Optional[builtins.str] = None,
    service_role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    termination_hook_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    trigger_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.TriggerConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b694585ede99d65d64f83954ec877206cd3f6dbfeff2f14bc9eb57ceae22e44(
    props: typing.Union[CfnDeploymentGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b971f3c45b75fab985aa35b531019de4ad9a81d0c5c1629ebe453b97b2d2b272(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abb8ed9e1e0bf41f8469246c2ede160f2d1f0afcca3622c14d1d31f9c1b4eb36(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08f70cdb5b4112d0a3f6cddda42b855acba372690e9a502e7af7f6fd921eaa24(
    *,
    alarms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.AlarmProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ignore_poll_alarm_failure: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3fbd96e5fafbf406ff10ae6637f914bb1418c7b2533f7935a4830babb1b964e(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc4fa9139bcb0e3c67a29adc78904f2c5dc2374b42c83ca8a62841c260ecbfc(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    events: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4557a2c9c2df51e1e95d0c70ea65055b7e8a4f5690ae6cd1bf866395478b7215(
    *,
    deployment_ready_option: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.DeploymentReadyOptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    green_fleet_provisioning_option: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.GreenFleetProvisioningOptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    terminate_blue_instances_on_deployment_success: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.BlueInstanceTerminationOptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2f8d93ebeb046531f2392843742b9d9b1cae74c44df29b3bbc8139b10a497ac(
    *,
    action: typing.Optional[builtins.str] = None,
    termination_wait_time_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9c133fd9786afb84aaaa034d1a1f247aae2198877e6754833f018495ae72683(
    *,
    description: typing.Optional[builtins.str] = None,
    ignore_application_stop_failures: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    revision: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.RevisionLocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7a4ebad7ded694ce81aeb2921e0d2790c6f78b901ea07ede84965239e80751e(
    *,
    action_on_timeout: typing.Optional[builtins.str] = None,
    wait_time_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c804eaaee25fb58df3f55bad37e0a7012279300a60de9381a5b39dad79b19c6f(
    *,
    deployment_option: typing.Optional[builtins.str] = None,
    deployment_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eaa2ccfe42d379776334904525bdc83e35d0dd3b393ad3e187db987ea70554d(
    *,
    key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cadcf7f602128e073914eced1f7ef81faf38a9505b236379b2a4a3d489a4a20(
    *,
    ec2_tag_group: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.EC2TagFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a51968364f92bd998f09493663d02db433482c5be2f1c7707376e03449d6011f(
    *,
    ec2_tag_set_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.EC2TagSetListObjectProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0de548bfcd9840c76bb9547cabaa17cb0454f531129885f26953e88c5a899136(
    *,
    cluster_name: typing.Optional[builtins.str] = None,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__444360e44b01538725adcfe7ff5bbb2b998c4015f777a9038aa10679271ba1e5(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a097f934e5908ee8a9590e993b2865813e6c1ef684d2ef111c1154f3dfa8df(
    *,
    commit_id: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45b1abdc2bd8f455fb55792770cd3785e9069fef438d3bfe8579f656ae742480(
    *,
    action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38aa28b11e717fff11bcf187c0502de7f457166d05f14bd2dde2fe8f5e831c83(
    *,
    elb_info_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.ELBInfoProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    target_group_info_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.TargetGroupInfoProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    target_group_pair_info_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.TargetGroupPairInfoProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38e61dc1820401a3cad44fa7b3ef49eec19b2a66ba8950d272a3329078bc71e8(
    *,
    on_premises_tag_group: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.TagFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc930d8f085b841b2c789263c21d0908d109468786dd0b6556ef9d10c1a0fc87(
    *,
    on_premises_tag_set_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.OnPremisesTagSetListObjectProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2cc2581b9f1a9e9e7dfd610534b23b16cebc6b5083e9a07e76a7cd537571d05(
    *,
    git_hub_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.GitHubLocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    revision_type: typing.Optional[builtins.str] = None,
    s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef5667934f7dfb19eba837b855edd057406a5fe7b5ae8fc69b7ae892b88706cd(
    *,
    bucket: typing.Optional[builtins.str] = None,
    bundle_type: typing.Optional[builtins.str] = None,
    e_tag: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e56b9ee265d0f0e0aac68760a46984d9dc1f3898ef1b645a020518f6ff335ca(
    *,
    key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aeab93bfc751240ebe5c0c1ecb5d8d9502897179d27c0747a01c9065784d783(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db94dcc16e7c05c0815817dd93cf464e0c95d6bb6fc672ae027a82500437764d(
    *,
    prod_traffic_route: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.TrafficRouteProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.TargetGroupInfoProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    test_traffic_route: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentGroupPropsMixin.TrafficRouteProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8902e51ce236fc2bc693e1f5e58c0152e40f708c269763fcd1ca67db55da851b(
    *,
    listener_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ee8eb38cce3d00c16d7278b16e47147e76d029d0a4bb4584da964e0ad2413e4(
    *,
    trigger_events: typing.Optional[typing.Sequence[builtins.str]] = None,
    trigger_name: typing.Optional[builtins.str] = None,
    trigger_target_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
