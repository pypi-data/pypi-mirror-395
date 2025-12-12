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
    jsii_type="@aws-cdk/mixins-preview.aws_controltower.mixins.CfnEnabledBaselineMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "baseline_identifier": "baselineIdentifier",
        "baseline_version": "baselineVersion",
        "parameters": "parameters",
        "tags": "tags",
        "target_identifier": "targetIdentifier",
    },
)
class CfnEnabledBaselineMixinProps:
    def __init__(
        self,
        *,
        baseline_identifier: typing.Optional[builtins.str] = None,
        baseline_version: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnabledBaselinePropsMixin.ParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnEnabledBaselinePropsMixin.

        :param baseline_identifier: The specific ``Baseline`` enabled as part of the ``EnabledBaseline`` resource.
        :param baseline_version: The enabled version of the ``Baseline`` .
        :param parameters: Shows the parameters that are applied when enabling this ``Baseline`` .
        :param tags: 
        :param target_identifier: The target on which to enable the ``Baseline`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-enabledbaseline.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_controltower import mixins as controltower_mixins
            
            # value: Any
            
            cfn_enabled_baseline_mixin_props = controltower_mixins.CfnEnabledBaselineMixinProps(
                baseline_identifier="baselineIdentifier",
                baseline_version="baselineVersion",
                parameters=[controltower_mixins.CfnEnabledBaselinePropsMixin.ParameterProperty(
                    key="key",
                    value=value
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_identifier="targetIdentifier"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16f86d60536e6783c6500b0b1fbe449705949497759ac7e3a3abbe0aa3ee0cc7)
            check_type(argname="argument baseline_identifier", value=baseline_identifier, expected_type=type_hints["baseline_identifier"])
            check_type(argname="argument baseline_version", value=baseline_version, expected_type=type_hints["baseline_version"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_identifier", value=target_identifier, expected_type=type_hints["target_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if baseline_identifier is not None:
            self._values["baseline_identifier"] = baseline_identifier
        if baseline_version is not None:
            self._values["baseline_version"] = baseline_version
        if parameters is not None:
            self._values["parameters"] = parameters
        if tags is not None:
            self._values["tags"] = tags
        if target_identifier is not None:
            self._values["target_identifier"] = target_identifier

    @builtins.property
    def baseline_identifier(self) -> typing.Optional[builtins.str]:
        '''The specific ``Baseline`` enabled as part of the ``EnabledBaseline`` resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-enabledbaseline.html#cfn-controltower-enabledbaseline-baselineidentifier
        '''
        result = self._values.get("baseline_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def baseline_version(self) -> typing.Optional[builtins.str]:
        '''The enabled version of the ``Baseline`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-enabledbaseline.html#cfn-controltower-enabledbaseline-baselineversion
        '''
        result = self._values.get("baseline_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnabledBaselinePropsMixin.ParameterProperty"]]]]:
        '''Shows the parameters that are applied when enabling this ``Baseline`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-enabledbaseline.html#cfn-controltower-enabledbaseline-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnabledBaselinePropsMixin.ParameterProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-enabledbaseline.html#cfn-controltower-enabledbaseline-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def target_identifier(self) -> typing.Optional[builtins.str]:
        '''The target on which to enable the ``Baseline`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-enabledbaseline.html#cfn-controltower-enabledbaseline-targetidentifier
        '''
        result = self._values.get("target_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnabledBaselineMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEnabledBaselinePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_controltower.mixins.CfnEnabledBaselinePropsMixin",
):
    '''Definition of AWS::ControlTower::EnabledBaseline Resource Type.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-enabledbaseline.html
    :cloudformationResource: AWS::ControlTower::EnabledBaseline
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_controltower import mixins as controltower_mixins
        
        # value: Any
        
        cfn_enabled_baseline_props_mixin = controltower_mixins.CfnEnabledBaselinePropsMixin(controltower_mixins.CfnEnabledBaselineMixinProps(
            baseline_identifier="baselineIdentifier",
            baseline_version="baselineVersion",
            parameters=[controltower_mixins.CfnEnabledBaselinePropsMixin.ParameterProperty(
                key="key",
                value=value
            )],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_identifier="targetIdentifier"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEnabledBaselineMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ControlTower::EnabledBaseline``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__477a1188b12af4ad3656bf4319c71b1415b2d89861e930b9cf0eeddfe69150f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1782c1ba3f1ba74eacc44b9881235b9bcb7c3c9e5ddf05000eb5194b438fad25)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7084effe0d129cc093eb9b123fa7cdd70be026a9f14e3f63576a33d0c83ddcfd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEnabledBaselineMixinProps:
        return typing.cast(CfnEnabledBaselineMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_controltower.mixins.CfnEnabledBaselinePropsMixin.ParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class ParameterProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Any = None,
        ) -> None:
            '''
            :param key: 
            :param value: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-controltower-enabledbaseline-parameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_controltower import mixins as controltower_mixins
                
                # value: Any
                
                parameter_property = controltower_mixins.CfnEnabledBaselinePropsMixin.ParameterProperty(
                    key="key",
                    value=value
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2de76a0b4ac0797db7cefaa57fe350e9d12d676f312b90e84dbbaabb25680e44)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-controltower-enabledbaseline-parameter.html#cfn-controltower-enabledbaseline-parameter-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Any:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-controltower-enabledbaseline-parameter.html#cfn-controltower-enabledbaseline-parameter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_controltower.mixins.CfnEnabledControlMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "control_identifier": "controlIdentifier",
        "parameters": "parameters",
        "tags": "tags",
        "target_identifier": "targetIdentifier",
    },
)
class CfnEnabledControlMixinProps:
    def __init__(
        self,
        *,
        control_identifier: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnabledControlPropsMixin.EnabledControlParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnEnabledControlPropsMixin.

        :param control_identifier: The ARN of the control. Only *Strongly recommended* and *Elective* controls are permitted, with the exception of the *Region deny* control. For information on how to find the ``controlIdentifier`` , see `the overview page <https://docs.aws.amazon.com//controltower/latest/APIReference/Welcome.html>`_ .
        :param parameters: Array of ``EnabledControlParameter`` objects.
        :param tags: A set of tags to assign to the enabled control.
        :param target_identifier: The ARN of the organizational unit. For information on how to find the ``targetIdentifier`` , see `the overview page <https://docs.aws.amazon.com//controltower/latest/APIReference/Welcome.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-enabledcontrol.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_controltower import mixins as controltower_mixins
            
            # value: Any
            
            cfn_enabled_control_mixin_props = controltower_mixins.CfnEnabledControlMixinProps(
                control_identifier="controlIdentifier",
                parameters=[controltower_mixins.CfnEnabledControlPropsMixin.EnabledControlParameterProperty(
                    key="key",
                    value=value
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_identifier="targetIdentifier"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5608ac72bba6be49e43e9b9fb724550cc8e0eab132993fa668f640d532621e69)
            check_type(argname="argument control_identifier", value=control_identifier, expected_type=type_hints["control_identifier"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_identifier", value=target_identifier, expected_type=type_hints["target_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if control_identifier is not None:
            self._values["control_identifier"] = control_identifier
        if parameters is not None:
            self._values["parameters"] = parameters
        if tags is not None:
            self._values["tags"] = tags
        if target_identifier is not None:
            self._values["target_identifier"] = target_identifier

    @builtins.property
    def control_identifier(self) -> typing.Optional[builtins.str]:
        '''The ARN of the control.

        Only *Strongly recommended* and *Elective* controls are permitted, with the exception of the *Region deny* control. For information on how to find the ``controlIdentifier`` , see `the overview page <https://docs.aws.amazon.com//controltower/latest/APIReference/Welcome.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-enabledcontrol.html#cfn-controltower-enabledcontrol-controlidentifier
        '''
        result = self._values.get("control_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnabledControlPropsMixin.EnabledControlParameterProperty"]]]]:
        '''Array of ``EnabledControlParameter`` objects.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-enabledcontrol.html#cfn-controltower-enabledcontrol-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnabledControlPropsMixin.EnabledControlParameterProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A set of tags to assign to the enabled control.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-enabledcontrol.html#cfn-controltower-enabledcontrol-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def target_identifier(self) -> typing.Optional[builtins.str]:
        '''The ARN of the organizational unit.

        For information on how to find the ``targetIdentifier`` , see `the overview page <https://docs.aws.amazon.com//controltower/latest/APIReference/Welcome.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-enabledcontrol.html#cfn-controltower-enabledcontrol-targetidentifier
        '''
        result = self._values.get("target_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnabledControlMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEnabledControlPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_controltower.mixins.CfnEnabledControlPropsMixin",
):
    '''The resource represents an enabled control.

    It specifies an asynchronous operation that creates AWS resources on the specified organizational unit and the accounts it contains. The resources created will vary according to the control that you specify.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-enabledcontrol.html
    :cloudformationResource: AWS::ControlTower::EnabledControl
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_controltower import mixins as controltower_mixins
        
        # value: Any
        
        cfn_enabled_control_props_mixin = controltower_mixins.CfnEnabledControlPropsMixin(controltower_mixins.CfnEnabledControlMixinProps(
            control_identifier="controlIdentifier",
            parameters=[controltower_mixins.CfnEnabledControlPropsMixin.EnabledControlParameterProperty(
                key="key",
                value=value
            )],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_identifier="targetIdentifier"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEnabledControlMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ControlTower::EnabledControl``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a60e4d1f5dbd0302f33f0355d71383d614563e7895339199042f4f4e7dce874a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37da36d66bf1a27c7b2735e3a03cf1573d3fdf2d09d3c70889fa3049a605f2f8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__152511931dac7bcf93d3f718a3648cde4ceb3492b689f29772c1417dd4937ee4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEnabledControlMixinProps:
        return typing.cast(CfnEnabledControlMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_controltower.mixins.CfnEnabledControlPropsMixin.EnabledControlParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class EnabledControlParameterProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Any = None,
        ) -> None:
            '''A set of parameters that configure the behavior of the enabled control.

            Expressed as a key/value pair, where ``Key`` is of type ``String`` and ``Value`` is of type ``Document`` .

            :param key: The key of a key/value pair. It is of type ``string`` .
            :param value: The value of a key/value pair. It can be of type ``array`` , ``string`` , ``number`` , ``object`` , or ``boolean`` . [Note: The *Type* field that follows may show a single type such as Number, which is only one possible type.]

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-controltower-enabledcontrol-enabledcontrolparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_controltower import mixins as controltower_mixins
                
                # value: Any
                
                enabled_control_parameter_property = controltower_mixins.CfnEnabledControlPropsMixin.EnabledControlParameterProperty(
                    key="key",
                    value=value
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__480901902c96f2044e36e64efc8c4e79dfcb8bbbf1aa1e2adf45b7101fe81a55)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key of a key/value pair.

            It is of type ``string`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-controltower-enabledcontrol-enabledcontrolparameter.html#cfn-controltower-enabledcontrol-enabledcontrolparameter-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Any:
            '''The value of a key/value pair.

            It can be of type ``array`` , ``string`` , ``number`` , ``object`` , or ``boolean`` . [Note: The *Type* field that follows may show a single type such as Number, which is only one possible type.]

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-controltower-enabledcontrol-enabledcontrolparameter.html#cfn-controltower-enabledcontrol-enabledcontrolparameter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnabledControlParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_controltower.mixins.CfnLandingZoneMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "manifest": "manifest",
        "remediation_types": "remediationTypes",
        "tags": "tags",
        "version": "version",
    },
)
class CfnLandingZoneMixinProps:
    def __init__(
        self,
        *,
        manifest: typing.Any = None,
        remediation_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnLandingZonePropsMixin.

        :param manifest: The landing zone manifest JSON text file that specifies the landing zone configurations.
        :param remediation_types: The types of remediation actions configured for the landing zone, such as automatic drift correction or compliance enforcement.
        :param tags: Tags to be applied to the landing zone.
        :param version: The landing zone's current deployed version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-landingzone.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_controltower import mixins as controltower_mixins
            
            # manifest: Any
            
            cfn_landing_zone_mixin_props = controltower_mixins.CfnLandingZoneMixinProps(
                manifest=manifest,
                remediation_types=["remediationTypes"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                version="version"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47f40bcdcf2a86d0e80cef651516bf1155abfae5841e9a64ab31f94381d7c8ab)
            check_type(argname="argument manifest", value=manifest, expected_type=type_hints["manifest"])
            check_type(argname="argument remediation_types", value=remediation_types, expected_type=type_hints["remediation_types"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if manifest is not None:
            self._values["manifest"] = manifest
        if remediation_types is not None:
            self._values["remediation_types"] = remediation_types
        if tags is not None:
            self._values["tags"] = tags
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def manifest(self) -> typing.Any:
        '''The landing zone manifest JSON text file that specifies the landing zone configurations.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-landingzone.html#cfn-controltower-landingzone-manifest
        '''
        result = self._values.get("manifest")
        return typing.cast(typing.Any, result)

    @builtins.property
    def remediation_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The types of remediation actions configured for the landing zone, such as automatic drift correction or compliance enforcement.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-landingzone.html#cfn-controltower-landingzone-remediationtypes
        '''
        result = self._values.get("remediation_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags to be applied to the landing zone.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-landingzone.html#cfn-controltower-landingzone-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The landing zone's current deployed version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-landingzone.html#cfn-controltower-landingzone-version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLandingZoneMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLandingZonePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_controltower.mixins.CfnLandingZonePropsMixin",
):
    '''Creates a new landing zone.

    This API call starts an asynchronous operation that creates and configures a landing zone, based on the parameters specified in the manifest JSON file.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-landingzone.html
    :cloudformationResource: AWS::ControlTower::LandingZone
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_controltower import mixins as controltower_mixins
        
        # manifest: Any
        
        cfn_landing_zone_props_mixin = controltower_mixins.CfnLandingZonePropsMixin(controltower_mixins.CfnLandingZoneMixinProps(
            manifest=manifest,
            remediation_types=["remediationTypes"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            version="version"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLandingZoneMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ControlTower::LandingZone``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3be21fa607b570b26a6a3970787d164cb53954b596869ccb4002f33ac1bf945a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1d04774f1122e40abe92085965b38004ce01e1e547cd60388cd1173afd26926)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb81e48053f737ff3a144a2e0efa2ec257383d03dc77cbcb238c4b12cf20021)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLandingZoneMixinProps:
        return typing.cast(CfnLandingZoneMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnEnabledBaselineMixinProps",
    "CfnEnabledBaselinePropsMixin",
    "CfnEnabledControlMixinProps",
    "CfnEnabledControlPropsMixin",
    "CfnLandingZoneMixinProps",
    "CfnLandingZonePropsMixin",
]

publication.publish()

def _typecheckingstub__16f86d60536e6783c6500b0b1fbe449705949497759ac7e3a3abbe0aa3ee0cc7(
    *,
    baseline_identifier: typing.Optional[builtins.str] = None,
    baseline_version: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnabledBaselinePropsMixin.ParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__477a1188b12af4ad3656bf4319c71b1415b2d89861e930b9cf0eeddfe69150f6(
    props: typing.Union[CfnEnabledBaselineMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1782c1ba3f1ba74eacc44b9881235b9bcb7c3c9e5ddf05000eb5194b438fad25(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7084effe0d129cc093eb9b123fa7cdd70be026a9f14e3f63576a33d0c83ddcfd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2de76a0b4ac0797db7cefaa57fe350e9d12d676f312b90e84dbbaabb25680e44(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5608ac72bba6be49e43e9b9fb724550cc8e0eab132993fa668f640d532621e69(
    *,
    control_identifier: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnabledControlPropsMixin.EnabledControlParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a60e4d1f5dbd0302f33f0355d71383d614563e7895339199042f4f4e7dce874a(
    props: typing.Union[CfnEnabledControlMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37da36d66bf1a27c7b2735e3a03cf1573d3fdf2d09d3c70889fa3049a605f2f8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__152511931dac7bcf93d3f718a3648cde4ceb3492b689f29772c1417dd4937ee4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480901902c96f2044e36e64efc8c4e79dfcb8bbbf1aa1e2adf45b7101fe81a55(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47f40bcdcf2a86d0e80cef651516bf1155abfae5841e9a64ab31f94381d7c8ab(
    *,
    manifest: typing.Any = None,
    remediation_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3be21fa607b570b26a6a3970787d164cb53954b596869ccb4002f33ac1bf945a(
    props: typing.Union[CfnLandingZoneMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d04774f1122e40abe92085965b38004ce01e1e547cd60388cd1173afd26926(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb81e48053f737ff3a144a2e0efa2ec257383d03dc77cbcb238c4b12cf20021(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
