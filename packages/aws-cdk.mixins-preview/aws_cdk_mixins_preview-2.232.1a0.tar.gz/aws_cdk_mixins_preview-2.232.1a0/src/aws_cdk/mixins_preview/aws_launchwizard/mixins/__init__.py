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
    jsii_type="@aws-cdk/mixins-preview.aws_launchwizard.mixins.CfnDeploymentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "deployment_pattern_name": "deploymentPatternName",
        "name": "name",
        "specifications": "specifications",
        "tags": "tags",
        "workload_name": "workloadName",
    },
)
class CfnDeploymentMixinProps:
    def __init__(
        self,
        *,
        deployment_pattern_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        specifications: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        workload_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDeploymentPropsMixin.

        :param deployment_pattern_name: The name of the deployment pattern.
        :param name: The name of the deployment.
        :param specifications: The settings specified for the deployment. These settings define how to deploy and configure your resources created by the deployment. For more information about the specifications required for creating a deployment for a SAP workload, see `SAP deployment specifications <https://docs.aws.amazon.com/launchwizard/latest/APIReference/launch-wizard-specifications-sap.html>`_ . To retrieve the specifications required to create a deployment for other workloads, use the ```GetWorkloadDeploymentPattern`` <https://docs.aws.amazon.com/launchwizard/latest/APIReference/API_GetWorkloadDeploymentPattern.html>`_ operation.
        :param tags: Information about the tags attached to a deployment.
        :param workload_name: The name of the workload.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-launchwizard-deployment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_launchwizard import mixins as launchwizard_mixins
            
            cfn_deployment_mixin_props = launchwizard_mixins.CfnDeploymentMixinProps(
                deployment_pattern_name="deploymentPatternName",
                name="name",
                specifications={
                    "specifications_key": "specifications"
                },
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                workload_name="workloadName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__327e79304698557a8a90714eeaf633e4bc2607bd66b290ae68125ed1ca2020ed)
            check_type(argname="argument deployment_pattern_name", value=deployment_pattern_name, expected_type=type_hints["deployment_pattern_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument specifications", value=specifications, expected_type=type_hints["specifications"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument workload_name", value=workload_name, expected_type=type_hints["workload_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deployment_pattern_name is not None:
            self._values["deployment_pattern_name"] = deployment_pattern_name
        if name is not None:
            self._values["name"] = name
        if specifications is not None:
            self._values["specifications"] = specifications
        if tags is not None:
            self._values["tags"] = tags
        if workload_name is not None:
            self._values["workload_name"] = workload_name

    @builtins.property
    def deployment_pattern_name(self) -> typing.Optional[builtins.str]:
        '''The name of the deployment pattern.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-launchwizard-deployment.html#cfn-launchwizard-deployment-deploymentpatternname
        '''
        result = self._values.get("deployment_pattern_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the deployment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-launchwizard-deployment.html#cfn-launchwizard-deployment-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def specifications(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''The settings specified for the deployment.

        These settings define how to deploy and configure your resources created by the deployment. For more information about the specifications required for creating a deployment for a SAP workload, see `SAP deployment specifications <https://docs.aws.amazon.com/launchwizard/latest/APIReference/launch-wizard-specifications-sap.html>`_ . To retrieve the specifications required to create a deployment for other workloads, use the ```GetWorkloadDeploymentPattern`` <https://docs.aws.amazon.com/launchwizard/latest/APIReference/API_GetWorkloadDeploymentPattern.html>`_ operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-launchwizard-deployment.html#cfn-launchwizard-deployment-specifications
        '''
        result = self._values.get("specifications")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Information about the tags attached to a deployment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-launchwizard-deployment.html#cfn-launchwizard-deployment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def workload_name(self) -> typing.Optional[builtins.str]:
        '''The name of the workload.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-launchwizard-deployment.html#cfn-launchwizard-deployment-workloadname
        '''
        result = self._values.get("workload_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDeploymentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_launchwizard.mixins.CfnDeploymentPropsMixin",
):
    '''Creates a deployment for the given workload.

    Deployments created by this operation are not available in the Launch Wizard console to use the ``Clone deployment`` action on.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-launchwizard-deployment.html
    :cloudformationResource: AWS::LaunchWizard::Deployment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_launchwizard import mixins as launchwizard_mixins
        
        cfn_deployment_props_mixin = launchwizard_mixins.CfnDeploymentPropsMixin(launchwizard_mixins.CfnDeploymentMixinProps(
            deployment_pattern_name="deploymentPatternName",
            name="name",
            specifications={
                "specifications_key": "specifications"
            },
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            workload_name="workloadName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDeploymentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::LaunchWizard::Deployment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0d54da4635edc1cb47198a08a330ddb9add0449f3d62fd59f5d52f888dd35e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee557ca1aa1edc598ac431f492507f53c2e3c2ab3b0ad685dcbaf61b9937c9f4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8f49c549e1e604668a7053d2bf53a655e72a5e2d6eec5e8dd13243540a2599f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDeploymentMixinProps:
        return typing.cast(CfnDeploymentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnDeploymentMixinProps",
    "CfnDeploymentPropsMixin",
]

publication.publish()

def _typecheckingstub__327e79304698557a8a90714eeaf633e4bc2607bd66b290ae68125ed1ca2020ed(
    *,
    deployment_pattern_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    specifications: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    workload_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0d54da4635edc1cb47198a08a330ddb9add0449f3d62fd59f5d52f888dd35e2(
    props: typing.Union[CfnDeploymentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee557ca1aa1edc598ac431f492507f53c2e3c2ab3b0ad685dcbaf61b9937c9f4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8f49c549e1e604668a7053d2bf53a655e72a5e2d6eec5e8dd13243540a2599f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
