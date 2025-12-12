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
    jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.mixins.CfnCellMixinProps",
    jsii_struct_bases=[],
    name_mapping={"cell_name": "cellName", "cells": "cells", "tags": "tags"},
)
class CfnCellMixinProps:
    def __init__(
        self,
        *,
        cell_name: typing.Optional[builtins.str] = None,
        cells: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnCellPropsMixin.

        :param cell_name: The name of the cell to create.
        :param cells: A list of cell Amazon Resource Names (ARNs) contained within this cell, for use in nested cells. For example, Availability Zones within specific AWS Regions .
        :param tags: A collection of tags associated with a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-cell.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53recoveryreadiness import mixins as route53recoveryreadiness_mixins
            
            cfn_cell_mixin_props = route53recoveryreadiness_mixins.CfnCellMixinProps(
                cell_name="cellName",
                cells=["cells"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3300656b2bc95226bc7a647752bb1fbdeef9fb147f1d8d71a2af72a98a1802d7)
            check_type(argname="argument cell_name", value=cell_name, expected_type=type_hints["cell_name"])
            check_type(argname="argument cells", value=cells, expected_type=type_hints["cells"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cell_name is not None:
            self._values["cell_name"] = cell_name
        if cells is not None:
            self._values["cells"] = cells
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def cell_name(self) -> typing.Optional[builtins.str]:
        '''The name of the cell to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-cell.html#cfn-route53recoveryreadiness-cell-cellname
        '''
        result = self._values.get("cell_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cells(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of cell Amazon Resource Names (ARNs) contained within this cell, for use in nested cells.

        For example, Availability Zones within specific AWS Regions .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-cell.html#cfn-route53recoveryreadiness-cell-cells
        '''
        result = self._values.get("cells")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A collection of tags associated with a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-cell.html#cfn-route53recoveryreadiness-cell-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCellMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCellPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.mixins.CfnCellPropsMixin",
):
    '''Creates a cell in recovery group in Amazon Route 53 Application Recovery Controller.

    A cell in Route 53 ARC represents replicas or independent units of failover in your application. It groups within it all the AWS resources that are necessary for your application to run independently. Typically, you would have define one set of resources in a primary cell and another set in a standby cell in your recovery group.

    After you set up the cells for your application, you can create readiness checks in Route 53 ARC to continually audit readiness for AWS resource quotas, capacity, network routing policies, and other predefined rules.

    You can set up notifications about changes that would affect your ability to fail over to a replica and recover. However, you should make decisions about whether to fail away from or to a replica based on your monitoring and health check systems. You should consider readiness checks as a complementary service to those systems.

    Route 53 ARC Readiness supports us-east-1 and us-west-2 AWS Regions only.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-cell.html
    :cloudformationResource: AWS::Route53RecoveryReadiness::Cell
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_route53recoveryreadiness import mixins as route53recoveryreadiness_mixins
        
        cfn_cell_props_mixin = route53recoveryreadiness_mixins.CfnCellPropsMixin(route53recoveryreadiness_mixins.CfnCellMixinProps(
            cell_name="cellName",
            cells=["cells"],
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
        props: typing.Union[CfnCellMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Route53RecoveryReadiness::Cell``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a92313d59fe660ddc6661d7f5d0bc6ec41931c54ef38635fe30fe455af038cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07c08bc1b0159029c20185365685e714fd4d1dc62ee35424159dc7e2bdf26a1e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__316ff3fe67837d2b98b80005780244775c2b92f44bc25c5262ee7d66a660f022)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCellMixinProps:
        return typing.cast(CfnCellMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.mixins.CfnReadinessCheckMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "readiness_check_name": "readinessCheckName",
        "resource_set_name": "resourceSetName",
        "tags": "tags",
    },
)
class CfnReadinessCheckMixinProps:
    def __init__(
        self,
        *,
        readiness_check_name: typing.Optional[builtins.str] = None,
        resource_set_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnReadinessCheckPropsMixin.

        :param readiness_check_name: The name of the readiness check to create.
        :param resource_set_name: The name of the resource set to check.
        :param tags: A collection of tags associated with a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-readinesscheck.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53recoveryreadiness import mixins as route53recoveryreadiness_mixins
            
            cfn_readiness_check_mixin_props = route53recoveryreadiness_mixins.CfnReadinessCheckMixinProps(
                readiness_check_name="readinessCheckName",
                resource_set_name="resourceSetName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e2f5998441d5d4e2a6d689ff32c329e564f2d17279d08ff06b812afbbe0cd9b)
            check_type(argname="argument readiness_check_name", value=readiness_check_name, expected_type=type_hints["readiness_check_name"])
            check_type(argname="argument resource_set_name", value=resource_set_name, expected_type=type_hints["resource_set_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if readiness_check_name is not None:
            self._values["readiness_check_name"] = readiness_check_name
        if resource_set_name is not None:
            self._values["resource_set_name"] = resource_set_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def readiness_check_name(self) -> typing.Optional[builtins.str]:
        '''The name of the readiness check to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-readinesscheck.html#cfn-route53recoveryreadiness-readinesscheck-readinesscheckname
        '''
        result = self._values.get("readiness_check_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_set_name(self) -> typing.Optional[builtins.str]:
        '''The name of the resource set to check.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-readinesscheck.html#cfn-route53recoveryreadiness-readinesscheck-resourcesetname
        '''
        result = self._values.get("resource_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A collection of tags associated with a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-readinesscheck.html#cfn-route53recoveryreadiness-readinesscheck-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReadinessCheckMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnReadinessCheckPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.mixins.CfnReadinessCheckPropsMixin",
):
    '''Creates a readiness check in Amazon Route 53 Application Recovery Controller.

    A readiness check continually monitors a resource set in your application, such as a set of Amazon Aurora instances, that Route 53 ARC is auditing recovery readiness for. The audits run once every minute on every resource that's associated with a readiness check.

    Every resource type has a set of rules associated with it that Route 53 ARC uses to audit resources for readiness. For more information, see `Readiness rules descriptions <https://docs.aws.amazon.com/r53recovery/latest/dg/recovery-readiness.rules-resources.html>`_ in the Amazon Route 53 Application Recovery Controller Developer Guide.

    Route 53 ARC Readiness supports us-east-1 and us-west-2 AWS Regions only.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-readinesscheck.html
    :cloudformationResource: AWS::Route53RecoveryReadiness::ReadinessCheck
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_route53recoveryreadiness import mixins as route53recoveryreadiness_mixins
        
        cfn_readiness_check_props_mixin = route53recoveryreadiness_mixins.CfnReadinessCheckPropsMixin(route53recoveryreadiness_mixins.CfnReadinessCheckMixinProps(
            readiness_check_name="readinessCheckName",
            resource_set_name="resourceSetName",
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
        props: typing.Union[CfnReadinessCheckMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Route53RecoveryReadiness::ReadinessCheck``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcd09a492fa13152e35f0876cd56e20807a41b3f6af7d8917b7f8d3ff4e6f1a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2da74c0f268610f9ee5536ff7b61c4def8816595bc5881d2e448cbaacbca4cf1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fda9c02bbe76baa635cf1064e3c295656a140ec081513b6c08ae1215d52c12f4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnReadinessCheckMixinProps:
        return typing.cast(CfnReadinessCheckMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.mixins.CfnRecoveryGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "cells": "cells",
        "recovery_group_name": "recoveryGroupName",
        "tags": "tags",
    },
)
class CfnRecoveryGroupMixinProps:
    def __init__(
        self,
        *,
        cells: typing.Optional[typing.Sequence[builtins.str]] = None,
        recovery_group_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnRecoveryGroupPropsMixin.

        :param cells: A list of the cell Amazon Resource Names (ARNs) in the recovery group.
        :param recovery_group_name: The name of the recovery group to create.
        :param tags: A collection of tags associated with a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-recoverygroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53recoveryreadiness import mixins as route53recoveryreadiness_mixins
            
            cfn_recovery_group_mixin_props = route53recoveryreadiness_mixins.CfnRecoveryGroupMixinProps(
                cells=["cells"],
                recovery_group_name="recoveryGroupName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__624814fb0d3e91b11cf47feb0b509789c95b63adcf6710cddd99c6092c9d3278)
            check_type(argname="argument cells", value=cells, expected_type=type_hints["cells"])
            check_type(argname="argument recovery_group_name", value=recovery_group_name, expected_type=type_hints["recovery_group_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cells is not None:
            self._values["cells"] = cells
        if recovery_group_name is not None:
            self._values["recovery_group_name"] = recovery_group_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def cells(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of the cell Amazon Resource Names (ARNs) in the recovery group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-recoverygroup.html#cfn-route53recoveryreadiness-recoverygroup-cells
        '''
        result = self._values.get("cells")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def recovery_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the recovery group to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-recoverygroup.html#cfn-route53recoveryreadiness-recoverygroup-recoverygroupname
        '''
        result = self._values.get("recovery_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A collection of tags associated with a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-recoverygroup.html#cfn-route53recoveryreadiness-recoverygroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRecoveryGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRecoveryGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.mixins.CfnRecoveryGroupPropsMixin",
):
    '''Creates a recovery group in Amazon Route 53 Application Recovery Controller.

    A recovery group represents your application. It typically consists of two or more cells that are replicas of each other in terms of resources and functionality, so that you can fail over from one to the other, for example, from one Region to another. You create recovery groups so you can use readiness checks to audit resources in your application.

    For more information, see `Readiness checks, resource sets, and readiness scopes <https://docs.aws.amazon.com/r53recovery/latest/dg/recovery-readiness.recovery-groups.readiness-scope.html>`_ in the Amazon Route 53 Application Recovery Controller Developer Guide.

    Route 53 ARC Readiness supports us-east-1 and us-west-2 AWS Regions only.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-recoverygroup.html
    :cloudformationResource: AWS::Route53RecoveryReadiness::RecoveryGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_route53recoveryreadiness import mixins as route53recoveryreadiness_mixins
        
        cfn_recovery_group_props_mixin = route53recoveryreadiness_mixins.CfnRecoveryGroupPropsMixin(route53recoveryreadiness_mixins.CfnRecoveryGroupMixinProps(
            cells=["cells"],
            recovery_group_name="recoveryGroupName",
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
        props: typing.Union[CfnRecoveryGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Route53RecoveryReadiness::RecoveryGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbeb65bc2f69a7976ca5c0a26d239013db796a599ac543076e60fe50c1ebcad0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d1317ed7f536aa5b97348da40adff4966100b6194c313fb334c205bcd778889)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6325f7693d9cee89ad894b69b203012bb83f9efaaabe480bac1562963b111200)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRecoveryGroupMixinProps:
        return typing.cast(CfnRecoveryGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.mixins.CfnResourceSetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "resources": "resources",
        "resource_set_name": "resourceSetName",
        "resource_set_type": "resourceSetType",
        "tags": "tags",
    },
)
class CfnResourceSetMixinProps:
    def __init__(
        self,
        *,
        resources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceSetPropsMixin.ResourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        resource_set_name: typing.Optional[builtins.str] = None,
        resource_set_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnResourceSetPropsMixin.

        :param resources: A list of resource objects in the resource set.
        :param resource_set_name: The name of the resource set to create.
        :param resource_set_type: The resource type of the resources in the resource set. Enter one of the following values for resource type:. AWS::ApiGateway::Stage, AWS::ApiGatewayV2::Stage, AWS::AutoScaling::AutoScalingGroup, AWS::CloudWatch::Alarm, AWS::EC2::CustomerGateway, AWS::DynamoDB::Table, AWS::EC2::Volume, AWS::ElasticLoadBalancing::LoadBalancer, AWS::ElasticLoadBalancingV2::LoadBalancer, AWS::Lambda::Function, AWS::MSK::Cluster, AWS::RDS::DBCluster, AWS::Route53::HealthCheck, AWS::SQS::Queue, AWS::SNS::Topic, AWS::SNS::Subscription, AWS::EC2::VPC, AWS::EC2::VPNConnection, AWS::EC2::VPNGateway, AWS::Route53RecoveryReadiness::DNSTargetResource. Note that AWS::Route53RecoveryReadiness::DNSTargetResource is only used for this setting. It isn't an actual AWS CloudFormation resource type.
        :param tags: A tag to associate with the parameters for a resource set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-resourceset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53recoveryreadiness import mixins as route53recoveryreadiness_mixins
            
            cfn_resource_set_mixin_props = route53recoveryreadiness_mixins.CfnResourceSetMixinProps(
                resources=[route53recoveryreadiness_mixins.CfnResourceSetPropsMixin.ResourceProperty(
                    component_id="componentId",
                    dns_target_resource=route53recoveryreadiness_mixins.CfnResourceSetPropsMixin.DNSTargetResourceProperty(
                        domain_name="domainName",
                        hosted_zone_arn="hostedZoneArn",
                        record_set_id="recordSetId",
                        record_type="recordType",
                        target_resource=route53recoveryreadiness_mixins.CfnResourceSetPropsMixin.TargetResourceProperty(
                            nlb_resource=route53recoveryreadiness_mixins.CfnResourceSetPropsMixin.NLBResourceProperty(
                                arn="arn"
                            ),
                            r53_resource=route53recoveryreadiness_mixins.CfnResourceSetPropsMixin.R53ResourceRecordProperty(
                                domain_name="domainName",
                                record_set_id="recordSetId"
                            )
                        )
                    ),
                    readiness_scopes=["readinessScopes"],
                    resource_arn="resourceArn"
                )],
                resource_set_name="resourceSetName",
                resource_set_type="resourceSetType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29fe5d260e101431cecc1a50985b81d41982472a69ee06b7e97bf1c20b4d0d07)
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument resource_set_name", value=resource_set_name, expected_type=type_hints["resource_set_name"])
            check_type(argname="argument resource_set_type", value=resource_set_type, expected_type=type_hints["resource_set_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resources is not None:
            self._values["resources"] = resources
        if resource_set_name is not None:
            self._values["resource_set_name"] = resource_set_name
        if resource_set_type is not None:
            self._values["resource_set_type"] = resource_set_type
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def resources(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceSetPropsMixin.ResourceProperty"]]]]:
        '''A list of resource objects in the resource set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-resourceset.html#cfn-route53recoveryreadiness-resourceset-resources
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceSetPropsMixin.ResourceProperty"]]]], result)

    @builtins.property
    def resource_set_name(self) -> typing.Optional[builtins.str]:
        '''The name of the resource set to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-resourceset.html#cfn-route53recoveryreadiness-resourceset-resourcesetname
        '''
        result = self._values.get("resource_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_set_type(self) -> typing.Optional[builtins.str]:
        '''The resource type of the resources in the resource set. Enter one of the following values for resource type:.

        AWS::ApiGateway::Stage, AWS::ApiGatewayV2::Stage, AWS::AutoScaling::AutoScalingGroup, AWS::CloudWatch::Alarm, AWS::EC2::CustomerGateway, AWS::DynamoDB::Table, AWS::EC2::Volume, AWS::ElasticLoadBalancing::LoadBalancer, AWS::ElasticLoadBalancingV2::LoadBalancer, AWS::Lambda::Function, AWS::MSK::Cluster, AWS::RDS::DBCluster, AWS::Route53::HealthCheck, AWS::SQS::Queue, AWS::SNS::Topic, AWS::SNS::Subscription, AWS::EC2::VPC, AWS::EC2::VPNConnection, AWS::EC2::VPNGateway, AWS::Route53RecoveryReadiness::DNSTargetResource.

        Note that AWS::Route53RecoveryReadiness::DNSTargetResource is only used for this setting. It isn't an actual AWS CloudFormation resource type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-resourceset.html#cfn-route53recoveryreadiness-resourceset-resourcesettype
        '''
        result = self._values.get("resource_set_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A tag to associate with the parameters for a resource set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-resourceset.html#cfn-route53recoveryreadiness-resourceset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceSetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResourceSetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.mixins.CfnResourceSetPropsMixin",
):
    '''Creates a resource set in Amazon Route 53 Application Recovery Controller.

    A resource set is a set of resources of one type, such as Network Load Balancers, that span multiple cells. You can associate a resource set with a readiness check to have Route 53 ARC continually monitor the resources in the set for failover readiness.

    You typically create a resource set and a readiness check for each supported type of AWS resource in your application.

    For more information, see `Readiness checks, resource sets, and readiness scopes <https://docs.aws.amazon.com/r53recovery/latest/dg/recovery-readiness.recovery-groups.readiness-scope.html>`_ in the Amazon Route 53 Application Recovery Controller Developer Guide.

    Route 53 ARC Readiness supports us-east-1 and us-west-2 AWS Regions only.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-resourceset.html
    :cloudformationResource: AWS::Route53RecoveryReadiness::ResourceSet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_route53recoveryreadiness import mixins as route53recoveryreadiness_mixins
        
        cfn_resource_set_props_mixin = route53recoveryreadiness_mixins.CfnResourceSetPropsMixin(route53recoveryreadiness_mixins.CfnResourceSetMixinProps(
            resources=[route53recoveryreadiness_mixins.CfnResourceSetPropsMixin.ResourceProperty(
                component_id="componentId",
                dns_target_resource=route53recoveryreadiness_mixins.CfnResourceSetPropsMixin.DNSTargetResourceProperty(
                    domain_name="domainName",
                    hosted_zone_arn="hostedZoneArn",
                    record_set_id="recordSetId",
                    record_type="recordType",
                    target_resource=route53recoveryreadiness_mixins.CfnResourceSetPropsMixin.TargetResourceProperty(
                        nlb_resource=route53recoveryreadiness_mixins.CfnResourceSetPropsMixin.NLBResourceProperty(
                            arn="arn"
                        ),
                        r53_resource=route53recoveryreadiness_mixins.CfnResourceSetPropsMixin.R53ResourceRecordProperty(
                            domain_name="domainName",
                            record_set_id="recordSetId"
                        )
                    )
                ),
                readiness_scopes=["readinessScopes"],
                resource_arn="resourceArn"
            )],
            resource_set_name="resourceSetName",
            resource_set_type="resourceSetType",
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
        props: typing.Union[CfnResourceSetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Route53RecoveryReadiness::ResourceSet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfb6e9cc10b0b70a7a56d63ce361265da3f700079f582ca141b40e215833b84d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__774b848eea34051ff64f2e3cd0761675950eaef872a05f6b53efdd22100f2a45)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e1fdb46c9ef72631334007a7431d2db3a6d5f4cc8f55f300e45b18f09b8c816)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResourceSetMixinProps:
        return typing.cast(CfnResourceSetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.mixins.CfnResourceSetPropsMixin.DNSTargetResourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "domain_name": "domainName",
            "hosted_zone_arn": "hostedZoneArn",
            "record_set_id": "recordSetId",
            "record_type": "recordType",
            "target_resource": "targetResource",
        },
    )
    class DNSTargetResourceProperty:
        def __init__(
            self,
            *,
            domain_name: typing.Optional[builtins.str] = None,
            hosted_zone_arn: typing.Optional[builtins.str] = None,
            record_set_id: typing.Optional[builtins.str] = None,
            record_type: typing.Optional[builtins.str] = None,
            target_resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceSetPropsMixin.TargetResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A component for DNS/routing control readiness checks and architecture checks.

            :param domain_name: The domain name that acts as an ingress point to a portion of the customer application.
            :param hosted_zone_arn: The hosted zone Amazon Resource Name (ARN) that contains the DNS record with the provided name of the target resource.
            :param record_set_id: The Amazon Route 53 record set ID that uniquely identifies a DNS record, given a name and a type.
            :param record_type: The type of DNS record of the target resource.
            :param target_resource: The target resource that the Route 53 record points to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-dnstargetresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53recoveryreadiness import mixins as route53recoveryreadiness_mixins
                
                d_nSTarget_resource_property = route53recoveryreadiness_mixins.CfnResourceSetPropsMixin.DNSTargetResourceProperty(
                    domain_name="domainName",
                    hosted_zone_arn="hostedZoneArn",
                    record_set_id="recordSetId",
                    record_type="recordType",
                    target_resource=route53recoveryreadiness_mixins.CfnResourceSetPropsMixin.TargetResourceProperty(
                        nlb_resource=route53recoveryreadiness_mixins.CfnResourceSetPropsMixin.NLBResourceProperty(
                            arn="arn"
                        ),
                        r53_resource=route53recoveryreadiness_mixins.CfnResourceSetPropsMixin.R53ResourceRecordProperty(
                            domain_name="domainName",
                            record_set_id="recordSetId"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__48bc92f8ea75156c9b4854ab2124fa5b2af81794838b566fde953daadf17edc8)
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
                check_type(argname="argument hosted_zone_arn", value=hosted_zone_arn, expected_type=type_hints["hosted_zone_arn"])
                check_type(argname="argument record_set_id", value=record_set_id, expected_type=type_hints["record_set_id"])
                check_type(argname="argument record_type", value=record_type, expected_type=type_hints["record_type"])
                check_type(argname="argument target_resource", value=target_resource, expected_type=type_hints["target_resource"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain_name is not None:
                self._values["domain_name"] = domain_name
            if hosted_zone_arn is not None:
                self._values["hosted_zone_arn"] = hosted_zone_arn
            if record_set_id is not None:
                self._values["record_set_id"] = record_set_id
            if record_type is not None:
                self._values["record_type"] = record_type
            if target_resource is not None:
                self._values["target_resource"] = target_resource

        @builtins.property
        def domain_name(self) -> typing.Optional[builtins.str]:
            '''The domain name that acts as an ingress point to a portion of the customer application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-dnstargetresource.html#cfn-route53recoveryreadiness-resourceset-dnstargetresource-domainname
            '''
            result = self._values.get("domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hosted_zone_arn(self) -> typing.Optional[builtins.str]:
            '''The hosted zone Amazon Resource Name (ARN) that contains the DNS record with the provided name of the target resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-dnstargetresource.html#cfn-route53recoveryreadiness-resourceset-dnstargetresource-hostedzonearn
            '''
            result = self._values.get("hosted_zone_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def record_set_id(self) -> typing.Optional[builtins.str]:
            '''The Amazon Route 53 record set ID that uniquely identifies a DNS record, given a name and a type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-dnstargetresource.html#cfn-route53recoveryreadiness-resourceset-dnstargetresource-recordsetid
            '''
            result = self._values.get("record_set_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def record_type(self) -> typing.Optional[builtins.str]:
            '''The type of DNS record of the target resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-dnstargetresource.html#cfn-route53recoveryreadiness-resourceset-dnstargetresource-recordtype
            '''
            result = self._values.get("record_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_resource(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceSetPropsMixin.TargetResourceProperty"]]:
            '''The target resource that the Route 53 record points to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-dnstargetresource.html#cfn-route53recoveryreadiness-resourceset-dnstargetresource-targetresource
            '''
            result = self._values.get("target_resource")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceSetPropsMixin.TargetResourceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DNSTargetResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.mixins.CfnResourceSetPropsMixin.NLBResourceProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class NLBResourceProperty:
        def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
            '''The Network Load Balancer resource that a DNS target resource points to.

            :param arn: The Network Load Balancer resource Amazon Resource Name (ARN).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-nlbresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53recoveryreadiness import mixins as route53recoveryreadiness_mixins
                
                n_lBResource_property = route53recoveryreadiness_mixins.CfnResourceSetPropsMixin.NLBResourceProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5c180a7262098cc4711c93b9fb569d84ca4b8bae5b92689ab11fc3d442c3a0d9)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The Network Load Balancer resource Amazon Resource Name (ARN).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-nlbresource.html#cfn-route53recoveryreadiness-resourceset-nlbresource-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NLBResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.mixins.CfnResourceSetPropsMixin.R53ResourceRecordProperty",
        jsii_struct_bases=[],
        name_mapping={"domain_name": "domainName", "record_set_id": "recordSetId"},
    )
    class R53ResourceRecordProperty:
        def __init__(
            self,
            *,
            domain_name: typing.Optional[builtins.str] = None,
            record_set_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Amazon Route 53 resource that a DNS target resource record points to.

            :param domain_name: The DNS target domain name.
            :param record_set_id: The Amazon Route 53 Resource Record Set ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-r53resourcerecord.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53recoveryreadiness import mixins as route53recoveryreadiness_mixins
                
                r53_resource_record_property = route53recoveryreadiness_mixins.CfnResourceSetPropsMixin.R53ResourceRecordProperty(
                    domain_name="domainName",
                    record_set_id="recordSetId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8cad036c22f2f3f9e446a046895798519ef71e605a08ebda631af8acb8198cf0)
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
                check_type(argname="argument record_set_id", value=record_set_id, expected_type=type_hints["record_set_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain_name is not None:
                self._values["domain_name"] = domain_name
            if record_set_id is not None:
                self._values["record_set_id"] = record_set_id

        @builtins.property
        def domain_name(self) -> typing.Optional[builtins.str]:
            '''The DNS target domain name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-r53resourcerecord.html#cfn-route53recoveryreadiness-resourceset-r53resourcerecord-domainname
            '''
            result = self._values.get("domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def record_set_id(self) -> typing.Optional[builtins.str]:
            '''The Amazon Route 53 Resource Record Set ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-r53resourcerecord.html#cfn-route53recoveryreadiness-resourceset-r53resourcerecord-recordsetid
            '''
            result = self._values.get("record_set_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "R53ResourceRecordProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.mixins.CfnResourceSetPropsMixin.ResourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component_id": "componentId",
            "dns_target_resource": "dnsTargetResource",
            "readiness_scopes": "readinessScopes",
            "resource_arn": "resourceArn",
        },
    )
    class ResourceProperty:
        def __init__(
            self,
            *,
            component_id: typing.Optional[builtins.str] = None,
            dns_target_resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceSetPropsMixin.DNSTargetResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            readiness_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
            resource_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The resource element of a resource set.

            :param component_id: The component identifier of the resource, generated when DNS target resource is used.
            :param dns_target_resource: A component for DNS/routing control readiness checks. This is a required setting when ``ResourceSet`` ``ResourceSetType`` is set to ``AWS::Route53RecoveryReadiness::DNSTargetResource`` . Do not set it for any other ``ResourceSetType`` setting.
            :param readiness_scopes: The recovery group Amazon Resource Name (ARN) or the cell ARN that the readiness checks for this resource set are scoped to.
            :param resource_arn: The Amazon Resource Name (ARN) of the AWS resource. This is a required setting for all ``ResourceSet`` ``ResourceSetType`` settings except ``AWS::Route53RecoveryReadiness::DNSTargetResource`` . Do not set this when ``ResourceSetType`` is set to ``AWS::Route53RecoveryReadiness::DNSTargetResource`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-resource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53recoveryreadiness import mixins as route53recoveryreadiness_mixins
                
                resource_property = route53recoveryreadiness_mixins.CfnResourceSetPropsMixin.ResourceProperty(
                    component_id="componentId",
                    dns_target_resource=route53recoveryreadiness_mixins.CfnResourceSetPropsMixin.DNSTargetResourceProperty(
                        domain_name="domainName",
                        hosted_zone_arn="hostedZoneArn",
                        record_set_id="recordSetId",
                        record_type="recordType",
                        target_resource=route53recoveryreadiness_mixins.CfnResourceSetPropsMixin.TargetResourceProperty(
                            nlb_resource=route53recoveryreadiness_mixins.CfnResourceSetPropsMixin.NLBResourceProperty(
                                arn="arn"
                            ),
                            r53_resource=route53recoveryreadiness_mixins.CfnResourceSetPropsMixin.R53ResourceRecordProperty(
                                domain_name="domainName",
                                record_set_id="recordSetId"
                            )
                        )
                    ),
                    readiness_scopes=["readinessScopes"],
                    resource_arn="resourceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f1fdbc475ba46bb323b4c3f08b3a98c9cc7913e0ce426486f6a15fe976521da9)
                check_type(argname="argument component_id", value=component_id, expected_type=type_hints["component_id"])
                check_type(argname="argument dns_target_resource", value=dns_target_resource, expected_type=type_hints["dns_target_resource"])
                check_type(argname="argument readiness_scopes", value=readiness_scopes, expected_type=type_hints["readiness_scopes"])
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if component_id is not None:
                self._values["component_id"] = component_id
            if dns_target_resource is not None:
                self._values["dns_target_resource"] = dns_target_resource
            if readiness_scopes is not None:
                self._values["readiness_scopes"] = readiness_scopes
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn

        @builtins.property
        def component_id(self) -> typing.Optional[builtins.str]:
            '''The component identifier of the resource, generated when DNS target resource is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-resource.html#cfn-route53recoveryreadiness-resourceset-resource-componentid
            '''
            result = self._values.get("component_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dns_target_resource(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceSetPropsMixin.DNSTargetResourceProperty"]]:
            '''A component for DNS/routing control readiness checks.

            This is a required setting when ``ResourceSet`` ``ResourceSetType`` is set to ``AWS::Route53RecoveryReadiness::DNSTargetResource`` . Do not set it for any other ``ResourceSetType`` setting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-resource.html#cfn-route53recoveryreadiness-resourceset-resource-dnstargetresource
            '''
            result = self._values.get("dns_target_resource")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceSetPropsMixin.DNSTargetResourceProperty"]], result)

        @builtins.property
        def readiness_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The recovery group Amazon Resource Name (ARN) or the cell ARN that the readiness checks for this resource set are scoped to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-resource.html#cfn-route53recoveryreadiness-resourceset-resource-readinessscopes
            '''
            result = self._values.get("readiness_scopes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the AWS resource.

            This is a required setting for all ``ResourceSet`` ``ResourceSetType`` settings except ``AWS::Route53RecoveryReadiness::DNSTargetResource`` . Do not set this when ``ResourceSetType`` is set to ``AWS::Route53RecoveryReadiness::DNSTargetResource`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-resource.html#cfn-route53recoveryreadiness-resourceset-resource-resourcearn
            '''
            result = self._values.get("resource_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.mixins.CfnResourceSetPropsMixin.TargetResourceProperty",
        jsii_struct_bases=[],
        name_mapping={"nlb_resource": "nlbResource", "r53_resource": "r53Resource"},
    )
    class TargetResourceProperty:
        def __init__(
            self,
            *,
            nlb_resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceSetPropsMixin.NLBResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            r53_resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceSetPropsMixin.R53ResourceRecordProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The target resource that the Route 53 record points to.

            :param nlb_resource: The Network Load Balancer resource that a DNS target resource points to.
            :param r53_resource: The Route 53 resource that a DNS target resource record points to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-targetresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_route53recoveryreadiness import mixins as route53recoveryreadiness_mixins
                
                target_resource_property = route53recoveryreadiness_mixins.CfnResourceSetPropsMixin.TargetResourceProperty(
                    nlb_resource=route53recoveryreadiness_mixins.CfnResourceSetPropsMixin.NLBResourceProperty(
                        arn="arn"
                    ),
                    r53_resource=route53recoveryreadiness_mixins.CfnResourceSetPropsMixin.R53ResourceRecordProperty(
                        domain_name="domainName",
                        record_set_id="recordSetId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d7a2f54a1c23dd410cac4722f59536e102ed055f1df599450b8dc59369f40af2)
                check_type(argname="argument nlb_resource", value=nlb_resource, expected_type=type_hints["nlb_resource"])
                check_type(argname="argument r53_resource", value=r53_resource, expected_type=type_hints["r53_resource"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if nlb_resource is not None:
                self._values["nlb_resource"] = nlb_resource
            if r53_resource is not None:
                self._values["r53_resource"] = r53_resource

        @builtins.property
        def nlb_resource(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceSetPropsMixin.NLBResourceProperty"]]:
            '''The Network Load Balancer resource that a DNS target resource points to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-targetresource.html#cfn-route53recoveryreadiness-resourceset-targetresource-nlbresource
            '''
            result = self._values.get("nlb_resource")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceSetPropsMixin.NLBResourceProperty"]], result)

        @builtins.property
        def r53_resource(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceSetPropsMixin.R53ResourceRecordProperty"]]:
            '''The Route 53 resource that a DNS target resource record points to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-targetresource.html#cfn-route53recoveryreadiness-resourceset-targetresource-r53resource
            '''
            result = self._values.get("r53_resource")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceSetPropsMixin.R53ResourceRecordProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnCellMixinProps",
    "CfnCellPropsMixin",
    "CfnReadinessCheckMixinProps",
    "CfnReadinessCheckPropsMixin",
    "CfnRecoveryGroupMixinProps",
    "CfnRecoveryGroupPropsMixin",
    "CfnResourceSetMixinProps",
    "CfnResourceSetPropsMixin",
]

publication.publish()

def _typecheckingstub__3300656b2bc95226bc7a647752bb1fbdeef9fb147f1d8d71a2af72a98a1802d7(
    *,
    cell_name: typing.Optional[builtins.str] = None,
    cells: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a92313d59fe660ddc6661d7f5d0bc6ec41931c54ef38635fe30fe455af038cd(
    props: typing.Union[CfnCellMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c08bc1b0159029c20185365685e714fd4d1dc62ee35424159dc7e2bdf26a1e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316ff3fe67837d2b98b80005780244775c2b92f44bc25c5262ee7d66a660f022(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e2f5998441d5d4e2a6d689ff32c329e564f2d17279d08ff06b812afbbe0cd9b(
    *,
    readiness_check_name: typing.Optional[builtins.str] = None,
    resource_set_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcd09a492fa13152e35f0876cd56e20807a41b3f6af7d8917b7f8d3ff4e6f1a2(
    props: typing.Union[CfnReadinessCheckMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2da74c0f268610f9ee5536ff7b61c4def8816595bc5881d2e448cbaacbca4cf1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fda9c02bbe76baa635cf1064e3c295656a140ec081513b6c08ae1215d52c12f4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__624814fb0d3e91b11cf47feb0b509789c95b63adcf6710cddd99c6092c9d3278(
    *,
    cells: typing.Optional[typing.Sequence[builtins.str]] = None,
    recovery_group_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbeb65bc2f69a7976ca5c0a26d239013db796a599ac543076e60fe50c1ebcad0(
    props: typing.Union[CfnRecoveryGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d1317ed7f536aa5b97348da40adff4966100b6194c313fb334c205bcd778889(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6325f7693d9cee89ad894b69b203012bb83f9efaaabe480bac1562963b111200(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29fe5d260e101431cecc1a50985b81d41982472a69ee06b7e97bf1c20b4d0d07(
    *,
    resources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceSetPropsMixin.ResourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_set_name: typing.Optional[builtins.str] = None,
    resource_set_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfb6e9cc10b0b70a7a56d63ce361265da3f700079f582ca141b40e215833b84d(
    props: typing.Union[CfnResourceSetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__774b848eea34051ff64f2e3cd0761675950eaef872a05f6b53efdd22100f2a45(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1fdb46c9ef72631334007a7431d2db3a6d5f4cc8f55f300e45b18f09b8c816(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48bc92f8ea75156c9b4854ab2124fa5b2af81794838b566fde953daadf17edc8(
    *,
    domain_name: typing.Optional[builtins.str] = None,
    hosted_zone_arn: typing.Optional[builtins.str] = None,
    record_set_id: typing.Optional[builtins.str] = None,
    record_type: typing.Optional[builtins.str] = None,
    target_resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceSetPropsMixin.TargetResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c180a7262098cc4711c93b9fb569d84ca4b8bae5b92689ab11fc3d442c3a0d9(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cad036c22f2f3f9e446a046895798519ef71e605a08ebda631af8acb8198cf0(
    *,
    domain_name: typing.Optional[builtins.str] = None,
    record_set_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1fdbc475ba46bb323b4c3f08b3a98c9cc7913e0ce426486f6a15fe976521da9(
    *,
    component_id: typing.Optional[builtins.str] = None,
    dns_target_resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceSetPropsMixin.DNSTargetResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    readiness_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7a2f54a1c23dd410cac4722f59536e102ed055f1df599450b8dc59369f40af2(
    *,
    nlb_resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceSetPropsMixin.NLBResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    r53_resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceSetPropsMixin.R53ResourceRecordProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
