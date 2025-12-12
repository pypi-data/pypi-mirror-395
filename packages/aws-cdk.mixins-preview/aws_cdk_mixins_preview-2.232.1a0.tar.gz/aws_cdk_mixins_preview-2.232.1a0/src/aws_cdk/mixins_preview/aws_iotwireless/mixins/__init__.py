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
    jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnDestinationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "expression": "expression",
        "expression_type": "expressionType",
        "name": "name",
        "role_arn": "roleArn",
        "tags": "tags",
    },
)
class CfnDestinationMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        expression: typing.Optional[builtins.str] = None,
        expression_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDestinationPropsMixin.

        :param description: The description of the new resource. Maximum length is 2048 characters.
        :param expression: The rule name to send messages to.
        :param expression_type: The type of value in ``Expression`` .
        :param name: The name of the new resource.
        :param role_arn: The ARN of the IAM Role that authorizes the destination.
        :param tags: The tags are an array of key-value pairs to attach to the specified resource. Tags can have a minimum of 0 and a maximum of 50 items.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-destination.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
            
            cfn_destination_mixin_props = iotwireless_mixins.CfnDestinationMixinProps(
                description="description",
                expression="expression",
                expression_type="expressionType",
                name="name",
                role_arn="roleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0f754e82917c71c4f5225f56f503cf2fcd09195153dd068ef875820102004bb)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument expression_type", value=expression_type, expected_type=type_hints["expression_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if expression is not None:
            self._values["expression"] = expression
        if expression_type is not None:
            self._values["expression_type"] = expression_type
        if name is not None:
            self._values["name"] = name
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the new resource.

        Maximum length is 2048 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-destination.html#cfn-iotwireless-destination-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expression(self) -> typing.Optional[builtins.str]:
        '''The rule name to send messages to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-destination.html#cfn-iotwireless-destination-expression
        '''
        result = self._values.get("expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expression_type(self) -> typing.Optional[builtins.str]:
        '''The type of value in ``Expression`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-destination.html#cfn-iotwireless-destination-expressiontype
        '''
        result = self._values.get("expression_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the new resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-destination.html#cfn-iotwireless-destination-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM Role that authorizes the destination.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-destination.html#cfn-iotwireless-destination-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags are an array of key-value pairs to attach to the specified resource.

        Tags can have a minimum of 0 and a maximum of 50 items.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-destination.html#cfn-iotwireless-destination-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDestinationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDestinationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnDestinationPropsMixin",
):
    '''Creates a new destination that maps a device message to an AWS IoT rule.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-destination.html
    :cloudformationResource: AWS::IoTWireless::Destination
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
        
        cfn_destination_props_mixin = iotwireless_mixins.CfnDestinationPropsMixin(iotwireless_mixins.CfnDestinationMixinProps(
            description="description",
            expression="expression",
            expression_type="expressionType",
            name="name",
            role_arn="roleArn",
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
        props: typing.Union[CfnDestinationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTWireless::Destination``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8de865eb4b44bbef7791a41f8460d1ff85fbc17af6735cf7ba261780da7f12c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54b2a1195fa9740b386f6afd91755bd2d9479c6f5510ffc848f1e2dff91bc009)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57e89abc664ca98a5ca63ab20121bdee972b436033df3fd86bdb99b3cb41615d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDestinationMixinProps:
        return typing.cast(CfnDestinationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnDeviceProfileMixinProps",
    jsii_struct_bases=[],
    name_mapping={"lo_ra_wan": "loRaWan", "name": "name", "tags": "tags"},
)
class CfnDeviceProfileMixinProps:
    def __init__(
        self,
        *,
        lo_ra_wan: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeviceProfilePropsMixin.LoRaWANDeviceProfileProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDeviceProfilePropsMixin.

        :param lo_ra_wan: LoRaWAN device profile object.
        :param name: The name of the new resource.
        :param tags: The tags are an array of key-value pairs to attach to the specified resource. Tags can have a minimum of 0 and a maximum of 50 items.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-deviceprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
            
            cfn_device_profile_mixin_props = iotwireless_mixins.CfnDeviceProfileMixinProps(
                lo_ra_wan=iotwireless_mixins.CfnDeviceProfilePropsMixin.LoRaWANDeviceProfileProperty(
                    class_bTimeout=123,
                    class_cTimeout=123,
                    factory_preset_freqs_list=[123],
                    mac_version="macVersion",
                    max_duty_cycle=123,
                    max_eirp=123,
                    ping_slot_dr=123,
                    ping_slot_freq=123,
                    ping_slot_period=123,
                    reg_params_revision="regParamsRevision",
                    rf_region="rfRegion",
                    rx_data_rate2=123,
                    rx_delay1=123,
                    rx_dr_offset1=123,
                    rx_freq2=123,
                    supports32_bit_fCnt=False,
                    supports_class_b=False,
                    supports_class_c=False,
                    supports_join=False
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f967a193a75e817a1998c4c11f0e287e2e58dcfbebe8ed63b84bad9afd79649)
            check_type(argname="argument lo_ra_wan", value=lo_ra_wan, expected_type=type_hints["lo_ra_wan"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if lo_ra_wan is not None:
            self._values["lo_ra_wan"] = lo_ra_wan
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def lo_ra_wan(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeviceProfilePropsMixin.LoRaWANDeviceProfileProperty"]]:
        '''LoRaWAN device profile object.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-deviceprofile.html#cfn-iotwireless-deviceprofile-lorawan
        '''
        result = self._values.get("lo_ra_wan")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeviceProfilePropsMixin.LoRaWANDeviceProfileProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the new resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-deviceprofile.html#cfn-iotwireless-deviceprofile-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags are an array of key-value pairs to attach to the specified resource.

        Tags can have a minimum of 0 and a maximum of 50 items.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-deviceprofile.html#cfn-iotwireless-deviceprofile-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeviceProfileMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDeviceProfilePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnDeviceProfilePropsMixin",
):
    '''Creates a new device profile.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-deviceprofile.html
    :cloudformationResource: AWS::IoTWireless::DeviceProfile
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
        
        cfn_device_profile_props_mixin = iotwireless_mixins.CfnDeviceProfilePropsMixin(iotwireless_mixins.CfnDeviceProfileMixinProps(
            lo_ra_wan=iotwireless_mixins.CfnDeviceProfilePropsMixin.LoRaWANDeviceProfileProperty(
                class_bTimeout=123,
                class_cTimeout=123,
                factory_preset_freqs_list=[123],
                mac_version="macVersion",
                max_duty_cycle=123,
                max_eirp=123,
                ping_slot_dr=123,
                ping_slot_freq=123,
                ping_slot_period=123,
                reg_params_revision="regParamsRevision",
                rf_region="rfRegion",
                rx_data_rate2=123,
                rx_delay1=123,
                rx_dr_offset1=123,
                rx_freq2=123,
                supports32_bit_fCnt=False,
                supports_class_b=False,
                supports_class_c=False,
                supports_join=False
            ),
            name="name",
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
        props: typing.Union[CfnDeviceProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTWireless::DeviceProfile``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__592ef0137f085e7cfdc1fd75884bdf82f79d524f6ccb378829c8a4db2557d02b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30213c7bceb78e8a490676fd36b4cbd1718b959969b200c828773acb9321180f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e49e3d855ffc303a8f003386e2dab3f0b92401f9e242f5bef6ffdd442db04a5f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDeviceProfileMixinProps:
        return typing.cast(CfnDeviceProfileMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnDeviceProfilePropsMixin.LoRaWANDeviceProfileProperty",
        jsii_struct_bases=[],
        name_mapping={
            "class_b_timeout": "classBTimeout",
            "class_c_timeout": "classCTimeout",
            "factory_preset_freqs_list": "factoryPresetFreqsList",
            "mac_version": "macVersion",
            "max_duty_cycle": "maxDutyCycle",
            "max_eirp": "maxEirp",
            "ping_slot_dr": "pingSlotDr",
            "ping_slot_freq": "pingSlotFreq",
            "ping_slot_period": "pingSlotPeriod",
            "reg_params_revision": "regParamsRevision",
            "rf_region": "rfRegion",
            "rx_data_rate2": "rxDataRate2",
            "rx_delay1": "rxDelay1",
            "rx_dr_offset1": "rxDrOffset1",
            "rx_freq2": "rxFreq2",
            "supports32_bit_f_cnt": "supports32BitFCnt",
            "supports_class_b": "supportsClassB",
            "supports_class_c": "supportsClassC",
            "supports_join": "supportsJoin",
        },
    )
    class LoRaWANDeviceProfileProperty:
        def __init__(
            self,
            *,
            class_b_timeout: typing.Optional[jsii.Number] = None,
            class_c_timeout: typing.Optional[jsii.Number] = None,
            factory_preset_freqs_list: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
            mac_version: typing.Optional[builtins.str] = None,
            max_duty_cycle: typing.Optional[jsii.Number] = None,
            max_eirp: typing.Optional[jsii.Number] = None,
            ping_slot_dr: typing.Optional[jsii.Number] = None,
            ping_slot_freq: typing.Optional[jsii.Number] = None,
            ping_slot_period: typing.Optional[jsii.Number] = None,
            reg_params_revision: typing.Optional[builtins.str] = None,
            rf_region: typing.Optional[builtins.str] = None,
            rx_data_rate2: typing.Optional[jsii.Number] = None,
            rx_delay1: typing.Optional[jsii.Number] = None,
            rx_dr_offset1: typing.Optional[jsii.Number] = None,
            rx_freq2: typing.Optional[jsii.Number] = None,
            supports32_bit_f_cnt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            supports_class_b: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            supports_class_c: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            supports_join: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''LoRaWAN device profile object.

            :param class_b_timeout: The ClassBTimeout value.
            :param class_c_timeout: The ClassCTimeout value.
            :param factory_preset_freqs_list: The list of values that make up the FactoryPresetFreqs value. Valid range of values include a minimum value of 1000000 and a maximum value of 16700000.
            :param mac_version: The MAC version (such as OTAA 1.1 or OTAA 1.0.3) to use with this device profile.
            :param max_duty_cycle: The MaxDutyCycle value.
            :param max_eirp: The MaxEIRP value.
            :param ping_slot_dr: The PingSlotDR value.
            :param ping_slot_freq: The PingSlotFreq value.
            :param ping_slot_period: The PingSlotPeriod value.
            :param reg_params_revision: The version of regional parameters.
            :param rf_region: The frequency band (RFRegion) value.
            :param rx_data_rate2: The RXDataRate2 value.
            :param rx_delay1: The RXDelay1 value.
            :param rx_dr_offset1: The RXDROffset1 value.
            :param rx_freq2: The RXFreq2 value.
            :param supports32_bit_f_cnt: The Supports32BitFCnt value.
            :param supports_class_b: The SupportsClassB value.
            :param supports_class_c: The SupportsClassC value.
            :param supports_join: The SupportsJoin value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-deviceprofile-lorawandeviceprofile.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
                
                lo_ra_wANDevice_profile_property = iotwireless_mixins.CfnDeviceProfilePropsMixin.LoRaWANDeviceProfileProperty(
                    class_bTimeout=123,
                    class_cTimeout=123,
                    factory_preset_freqs_list=[123],
                    mac_version="macVersion",
                    max_duty_cycle=123,
                    max_eirp=123,
                    ping_slot_dr=123,
                    ping_slot_freq=123,
                    ping_slot_period=123,
                    reg_params_revision="regParamsRevision",
                    rf_region="rfRegion",
                    rx_data_rate2=123,
                    rx_delay1=123,
                    rx_dr_offset1=123,
                    rx_freq2=123,
                    supports32_bit_fCnt=False,
                    supports_class_b=False,
                    supports_class_c=False,
                    supports_join=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__abf4d04290f902097b53a9e557f83f90b25eff2816112c62e928d7ec88d53c22)
                check_type(argname="argument class_b_timeout", value=class_b_timeout, expected_type=type_hints["class_b_timeout"])
                check_type(argname="argument class_c_timeout", value=class_c_timeout, expected_type=type_hints["class_c_timeout"])
                check_type(argname="argument factory_preset_freqs_list", value=factory_preset_freqs_list, expected_type=type_hints["factory_preset_freqs_list"])
                check_type(argname="argument mac_version", value=mac_version, expected_type=type_hints["mac_version"])
                check_type(argname="argument max_duty_cycle", value=max_duty_cycle, expected_type=type_hints["max_duty_cycle"])
                check_type(argname="argument max_eirp", value=max_eirp, expected_type=type_hints["max_eirp"])
                check_type(argname="argument ping_slot_dr", value=ping_slot_dr, expected_type=type_hints["ping_slot_dr"])
                check_type(argname="argument ping_slot_freq", value=ping_slot_freq, expected_type=type_hints["ping_slot_freq"])
                check_type(argname="argument ping_slot_period", value=ping_slot_period, expected_type=type_hints["ping_slot_period"])
                check_type(argname="argument reg_params_revision", value=reg_params_revision, expected_type=type_hints["reg_params_revision"])
                check_type(argname="argument rf_region", value=rf_region, expected_type=type_hints["rf_region"])
                check_type(argname="argument rx_data_rate2", value=rx_data_rate2, expected_type=type_hints["rx_data_rate2"])
                check_type(argname="argument rx_delay1", value=rx_delay1, expected_type=type_hints["rx_delay1"])
                check_type(argname="argument rx_dr_offset1", value=rx_dr_offset1, expected_type=type_hints["rx_dr_offset1"])
                check_type(argname="argument rx_freq2", value=rx_freq2, expected_type=type_hints["rx_freq2"])
                check_type(argname="argument supports32_bit_f_cnt", value=supports32_bit_f_cnt, expected_type=type_hints["supports32_bit_f_cnt"])
                check_type(argname="argument supports_class_b", value=supports_class_b, expected_type=type_hints["supports_class_b"])
                check_type(argname="argument supports_class_c", value=supports_class_c, expected_type=type_hints["supports_class_c"])
                check_type(argname="argument supports_join", value=supports_join, expected_type=type_hints["supports_join"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if class_b_timeout is not None:
                self._values["class_b_timeout"] = class_b_timeout
            if class_c_timeout is not None:
                self._values["class_c_timeout"] = class_c_timeout
            if factory_preset_freqs_list is not None:
                self._values["factory_preset_freqs_list"] = factory_preset_freqs_list
            if mac_version is not None:
                self._values["mac_version"] = mac_version
            if max_duty_cycle is not None:
                self._values["max_duty_cycle"] = max_duty_cycle
            if max_eirp is not None:
                self._values["max_eirp"] = max_eirp
            if ping_slot_dr is not None:
                self._values["ping_slot_dr"] = ping_slot_dr
            if ping_slot_freq is not None:
                self._values["ping_slot_freq"] = ping_slot_freq
            if ping_slot_period is not None:
                self._values["ping_slot_period"] = ping_slot_period
            if reg_params_revision is not None:
                self._values["reg_params_revision"] = reg_params_revision
            if rf_region is not None:
                self._values["rf_region"] = rf_region
            if rx_data_rate2 is not None:
                self._values["rx_data_rate2"] = rx_data_rate2
            if rx_delay1 is not None:
                self._values["rx_delay1"] = rx_delay1
            if rx_dr_offset1 is not None:
                self._values["rx_dr_offset1"] = rx_dr_offset1
            if rx_freq2 is not None:
                self._values["rx_freq2"] = rx_freq2
            if supports32_bit_f_cnt is not None:
                self._values["supports32_bit_f_cnt"] = supports32_bit_f_cnt
            if supports_class_b is not None:
                self._values["supports_class_b"] = supports_class_b
            if supports_class_c is not None:
                self._values["supports_class_c"] = supports_class_c
            if supports_join is not None:
                self._values["supports_join"] = supports_join

        @builtins.property
        def class_b_timeout(self) -> typing.Optional[jsii.Number]:
            '''The ClassBTimeout value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-deviceprofile-lorawandeviceprofile.html#cfn-iotwireless-deviceprofile-lorawandeviceprofile-classbtimeout
            '''
            result = self._values.get("class_b_timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def class_c_timeout(self) -> typing.Optional[jsii.Number]:
            '''The ClassCTimeout value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-deviceprofile-lorawandeviceprofile.html#cfn-iotwireless-deviceprofile-lorawandeviceprofile-classctimeout
            '''
            result = self._values.get("class_c_timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def factory_preset_freqs_list(
            self,
        ) -> typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]]:
            '''The list of values that make up the FactoryPresetFreqs value.

            Valid range of values include a minimum value of 1000000 and a maximum value of 16700000.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-deviceprofile-lorawandeviceprofile.html#cfn-iotwireless-deviceprofile-lorawandeviceprofile-factorypresetfreqslist
            '''
            result = self._values.get("factory_preset_freqs_list")
            return typing.cast(typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def mac_version(self) -> typing.Optional[builtins.str]:
            '''The MAC version (such as OTAA 1.1 or OTAA 1.0.3) to use with this device profile.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-deviceprofile-lorawandeviceprofile.html#cfn-iotwireless-deviceprofile-lorawandeviceprofile-macversion
            '''
            result = self._values.get("mac_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_duty_cycle(self) -> typing.Optional[jsii.Number]:
            '''The MaxDutyCycle value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-deviceprofile-lorawandeviceprofile.html#cfn-iotwireless-deviceprofile-lorawandeviceprofile-maxdutycycle
            '''
            result = self._values.get("max_duty_cycle")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_eirp(self) -> typing.Optional[jsii.Number]:
            '''The MaxEIRP value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-deviceprofile-lorawandeviceprofile.html#cfn-iotwireless-deviceprofile-lorawandeviceprofile-maxeirp
            '''
            result = self._values.get("max_eirp")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def ping_slot_dr(self) -> typing.Optional[jsii.Number]:
            '''The PingSlotDR value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-deviceprofile-lorawandeviceprofile.html#cfn-iotwireless-deviceprofile-lorawandeviceprofile-pingslotdr
            '''
            result = self._values.get("ping_slot_dr")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def ping_slot_freq(self) -> typing.Optional[jsii.Number]:
            '''The PingSlotFreq value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-deviceprofile-lorawandeviceprofile.html#cfn-iotwireless-deviceprofile-lorawandeviceprofile-pingslotfreq
            '''
            result = self._values.get("ping_slot_freq")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def ping_slot_period(self) -> typing.Optional[jsii.Number]:
            '''The PingSlotPeriod value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-deviceprofile-lorawandeviceprofile.html#cfn-iotwireless-deviceprofile-lorawandeviceprofile-pingslotperiod
            '''
            result = self._values.get("ping_slot_period")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def reg_params_revision(self) -> typing.Optional[builtins.str]:
            '''The version of regional parameters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-deviceprofile-lorawandeviceprofile.html#cfn-iotwireless-deviceprofile-lorawandeviceprofile-regparamsrevision
            '''
            result = self._values.get("reg_params_revision")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rf_region(self) -> typing.Optional[builtins.str]:
            '''The frequency band (RFRegion) value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-deviceprofile-lorawandeviceprofile.html#cfn-iotwireless-deviceprofile-lorawandeviceprofile-rfregion
            '''
            result = self._values.get("rf_region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rx_data_rate2(self) -> typing.Optional[jsii.Number]:
            '''The RXDataRate2 value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-deviceprofile-lorawandeviceprofile.html#cfn-iotwireless-deviceprofile-lorawandeviceprofile-rxdatarate2
            '''
            result = self._values.get("rx_data_rate2")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def rx_delay1(self) -> typing.Optional[jsii.Number]:
            '''The RXDelay1 value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-deviceprofile-lorawandeviceprofile.html#cfn-iotwireless-deviceprofile-lorawandeviceprofile-rxdelay1
            '''
            result = self._values.get("rx_delay1")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def rx_dr_offset1(self) -> typing.Optional[jsii.Number]:
            '''The RXDROffset1 value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-deviceprofile-lorawandeviceprofile.html#cfn-iotwireless-deviceprofile-lorawandeviceprofile-rxdroffset1
            '''
            result = self._values.get("rx_dr_offset1")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def rx_freq2(self) -> typing.Optional[jsii.Number]:
            '''The RXFreq2 value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-deviceprofile-lorawandeviceprofile.html#cfn-iotwireless-deviceprofile-lorawandeviceprofile-rxfreq2
            '''
            result = self._values.get("rx_freq2")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def supports32_bit_f_cnt(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The Supports32BitFCnt value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-deviceprofile-lorawandeviceprofile.html#cfn-iotwireless-deviceprofile-lorawandeviceprofile-supports32bitfcnt
            '''
            result = self._values.get("supports32_bit_f_cnt")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def supports_class_b(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The SupportsClassB value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-deviceprofile-lorawandeviceprofile.html#cfn-iotwireless-deviceprofile-lorawandeviceprofile-supportsclassb
            '''
            result = self._values.get("supports_class_b")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def supports_class_c(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The SupportsClassC value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-deviceprofile-lorawandeviceprofile.html#cfn-iotwireless-deviceprofile-lorawandeviceprofile-supportsclassc
            '''
            result = self._values.get("supports_class_c")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def supports_join(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The SupportsJoin value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-deviceprofile-lorawandeviceprofile.html#cfn-iotwireless-deviceprofile-lorawandeviceprofile-supportsjoin
            '''
            result = self._values.get("supports_join")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoRaWANDeviceProfileProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnFuotaTaskMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "associate_multicast_group": "associateMulticastGroup",
        "associate_wireless_device": "associateWirelessDevice",
        "description": "description",
        "disassociate_multicast_group": "disassociateMulticastGroup",
        "disassociate_wireless_device": "disassociateWirelessDevice",
        "firmware_update_image": "firmwareUpdateImage",
        "firmware_update_role": "firmwareUpdateRole",
        "lo_ra_wan": "loRaWan",
        "name": "name",
        "tags": "tags",
    },
)
class CfnFuotaTaskMixinProps:
    def __init__(
        self,
        *,
        associate_multicast_group: typing.Optional[builtins.str] = None,
        associate_wireless_device: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        disassociate_multicast_group: typing.Optional[builtins.str] = None,
        disassociate_wireless_device: typing.Optional[builtins.str] = None,
        firmware_update_image: typing.Optional[builtins.str] = None,
        firmware_update_role: typing.Optional[builtins.str] = None,
        lo_ra_wan: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFuotaTaskPropsMixin.LoRaWANProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnFuotaTaskPropsMixin.

        :param associate_multicast_group: The ID of the multicast group to associate with a FUOTA task.
        :param associate_wireless_device: The ID of the wireless device to associate with a multicast group.
        :param description: The description of the new resource.
        :param disassociate_multicast_group: The ID of the multicast group to disassociate from a FUOTA task.
        :param disassociate_wireless_device: The ID of the wireless device to disassociate from a FUOTA task.
        :param firmware_update_image: The S3 URI points to a firmware update image that is to be used with a FUOTA task.
        :param firmware_update_role: The firmware update role that is to be used with a FUOTA task.
        :param lo_ra_wan: The LoRaWAN information used with a FUOTA task.
        :param name: The name of a FUOTA task.
        :param tags: The tags are an array of key-value pairs to attach to the specified resource. Tags can have a minimum of 0 and a maximum of 50 items.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-fuotatask.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
            
            cfn_fuota_task_mixin_props = iotwireless_mixins.CfnFuotaTaskMixinProps(
                associate_multicast_group="associateMulticastGroup",
                associate_wireless_device="associateWirelessDevice",
                description="description",
                disassociate_multicast_group="disassociateMulticastGroup",
                disassociate_wireless_device="disassociateWirelessDevice",
                firmware_update_image="firmwareUpdateImage",
                firmware_update_role="firmwareUpdateRole",
                lo_ra_wan=iotwireless_mixins.CfnFuotaTaskPropsMixin.LoRaWANProperty(
                    rf_region="rfRegion",
                    start_time="startTime"
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26f98065d0fe5e30a55c3efd3c2d301591f80488aaa732f7db8ac7cff30dd45d)
            check_type(argname="argument associate_multicast_group", value=associate_multicast_group, expected_type=type_hints["associate_multicast_group"])
            check_type(argname="argument associate_wireless_device", value=associate_wireless_device, expected_type=type_hints["associate_wireless_device"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disassociate_multicast_group", value=disassociate_multicast_group, expected_type=type_hints["disassociate_multicast_group"])
            check_type(argname="argument disassociate_wireless_device", value=disassociate_wireless_device, expected_type=type_hints["disassociate_wireless_device"])
            check_type(argname="argument firmware_update_image", value=firmware_update_image, expected_type=type_hints["firmware_update_image"])
            check_type(argname="argument firmware_update_role", value=firmware_update_role, expected_type=type_hints["firmware_update_role"])
            check_type(argname="argument lo_ra_wan", value=lo_ra_wan, expected_type=type_hints["lo_ra_wan"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if associate_multicast_group is not None:
            self._values["associate_multicast_group"] = associate_multicast_group
        if associate_wireless_device is not None:
            self._values["associate_wireless_device"] = associate_wireless_device
        if description is not None:
            self._values["description"] = description
        if disassociate_multicast_group is not None:
            self._values["disassociate_multicast_group"] = disassociate_multicast_group
        if disassociate_wireless_device is not None:
            self._values["disassociate_wireless_device"] = disassociate_wireless_device
        if firmware_update_image is not None:
            self._values["firmware_update_image"] = firmware_update_image
        if firmware_update_role is not None:
            self._values["firmware_update_role"] = firmware_update_role
        if lo_ra_wan is not None:
            self._values["lo_ra_wan"] = lo_ra_wan
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def associate_multicast_group(self) -> typing.Optional[builtins.str]:
        '''The ID of the multicast group to associate with a FUOTA task.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-fuotatask.html#cfn-iotwireless-fuotatask-associatemulticastgroup
        '''
        result = self._values.get("associate_multicast_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def associate_wireless_device(self) -> typing.Optional[builtins.str]:
        '''The ID of the wireless device to associate with a multicast group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-fuotatask.html#cfn-iotwireless-fuotatask-associatewirelessdevice
        '''
        result = self._values.get("associate_wireless_device")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the new resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-fuotatask.html#cfn-iotwireless-fuotatask-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disassociate_multicast_group(self) -> typing.Optional[builtins.str]:
        '''The ID of the multicast group to disassociate from a FUOTA task.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-fuotatask.html#cfn-iotwireless-fuotatask-disassociatemulticastgroup
        '''
        result = self._values.get("disassociate_multicast_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disassociate_wireless_device(self) -> typing.Optional[builtins.str]:
        '''The ID of the wireless device to disassociate from a FUOTA task.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-fuotatask.html#cfn-iotwireless-fuotatask-disassociatewirelessdevice
        '''
        result = self._values.get("disassociate_wireless_device")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firmware_update_image(self) -> typing.Optional[builtins.str]:
        '''The S3 URI points to a firmware update image that is to be used with a FUOTA task.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-fuotatask.html#cfn-iotwireless-fuotatask-firmwareupdateimage
        '''
        result = self._values.get("firmware_update_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firmware_update_role(self) -> typing.Optional[builtins.str]:
        '''The firmware update role that is to be used with a FUOTA task.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-fuotatask.html#cfn-iotwireless-fuotatask-firmwareupdaterole
        '''
        result = self._values.get("firmware_update_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lo_ra_wan(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFuotaTaskPropsMixin.LoRaWANProperty"]]:
        '''The LoRaWAN information used with a FUOTA task.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-fuotatask.html#cfn-iotwireless-fuotatask-lorawan
        '''
        result = self._values.get("lo_ra_wan")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFuotaTaskPropsMixin.LoRaWANProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of a FUOTA task.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-fuotatask.html#cfn-iotwireless-fuotatask-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags are an array of key-value pairs to attach to the specified resource.

        Tags can have a minimum of 0 and a maximum of 50 items.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-fuotatask.html#cfn-iotwireless-fuotatask-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFuotaTaskMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFuotaTaskPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnFuotaTaskPropsMixin",
):
    '''A FUOTA task.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-fuotatask.html
    :cloudformationResource: AWS::IoTWireless::FuotaTask
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
        
        cfn_fuota_task_props_mixin = iotwireless_mixins.CfnFuotaTaskPropsMixin(iotwireless_mixins.CfnFuotaTaskMixinProps(
            associate_multicast_group="associateMulticastGroup",
            associate_wireless_device="associateWirelessDevice",
            description="description",
            disassociate_multicast_group="disassociateMulticastGroup",
            disassociate_wireless_device="disassociateWirelessDevice",
            firmware_update_image="firmwareUpdateImage",
            firmware_update_role="firmwareUpdateRole",
            lo_ra_wan=iotwireless_mixins.CfnFuotaTaskPropsMixin.LoRaWANProperty(
                rf_region="rfRegion",
                start_time="startTime"
            ),
            name="name",
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
        props: typing.Union[CfnFuotaTaskMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTWireless::FuotaTask``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44a50bfaa658e34a7252bd93fa0583c42810da6c7d3bd6121a540c399c0fc980)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85d28a2aa503e1e14f6066bf43bd7e5462cd95eec99221a5f57bf44bf3a5c263)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f20979babf7a1f772cff434271835cdd3b2d47bdce418d5b3ba305372c14e50)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFuotaTaskMixinProps:
        return typing.cast(CfnFuotaTaskMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnFuotaTaskPropsMixin.LoRaWANProperty",
        jsii_struct_bases=[],
        name_mapping={"rf_region": "rfRegion", "start_time": "startTime"},
    )
    class LoRaWANProperty:
        def __init__(
            self,
            *,
            rf_region: typing.Optional[builtins.str] = None,
            start_time: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The LoRaWAN information used with a FUOTA task.

            :param rf_region: The frequency band (RFRegion) value.
            :param start_time: Start time of a FUOTA task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-fuotatask-lorawan.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
                
                lo_ra_wANProperty = iotwireless_mixins.CfnFuotaTaskPropsMixin.LoRaWANProperty(
                    rf_region="rfRegion",
                    start_time="startTime"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__97554e720a0b1c625fe918b6b7886d870a1c966e5eb18cfbaff98683e3266f04)
                check_type(argname="argument rf_region", value=rf_region, expected_type=type_hints["rf_region"])
                check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rf_region is not None:
                self._values["rf_region"] = rf_region
            if start_time is not None:
                self._values["start_time"] = start_time

        @builtins.property
        def rf_region(self) -> typing.Optional[builtins.str]:
            '''The frequency band (RFRegion) value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-fuotatask-lorawan.html#cfn-iotwireless-fuotatask-lorawan-rfregion
            '''
            result = self._values.get("rf_region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def start_time(self) -> typing.Optional[builtins.str]:
            '''Start time of a FUOTA task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-fuotatask-lorawan.html#cfn-iotwireless-fuotatask-lorawan-starttime
            '''
            result = self._values.get("start_time")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoRaWANProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnMulticastGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "associate_wireless_device": "associateWirelessDevice",
        "description": "description",
        "disassociate_wireless_device": "disassociateWirelessDevice",
        "lo_ra_wan": "loRaWan",
        "name": "name",
        "tags": "tags",
    },
)
class CfnMulticastGroupMixinProps:
    def __init__(
        self,
        *,
        associate_wireless_device: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        disassociate_wireless_device: typing.Optional[builtins.str] = None,
        lo_ra_wan: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMulticastGroupPropsMixin.LoRaWANProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnMulticastGroupPropsMixin.

        :param associate_wireless_device: The ID of the wireless device to associate with a multicast group.
        :param description: The description of the multicast group.
        :param disassociate_wireless_device: The ID of the wireless device to disassociate from a multicast group.
        :param lo_ra_wan: The LoRaWAN information that is to be used with the multicast group.
        :param name: The name of the multicast group.
        :param tags: The tags are an array of key-value pairs to attach to the specified resource. Tags can have a minimum of 0 and a maximum of 50 items.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-multicastgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
            
            cfn_multicast_group_mixin_props = iotwireless_mixins.CfnMulticastGroupMixinProps(
                associate_wireless_device="associateWirelessDevice",
                description="description",
                disassociate_wireless_device="disassociateWirelessDevice",
                lo_ra_wan=iotwireless_mixins.CfnMulticastGroupPropsMixin.LoRaWANProperty(
                    dl_class="dlClass",
                    number_of_devices_in_group=123,
                    number_of_devices_requested=123,
                    rf_region="rfRegion"
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__831ecfadd9132a3ec164404b0eb2973d454674474dcd8742e4b715008ba7b95d)
            check_type(argname="argument associate_wireless_device", value=associate_wireless_device, expected_type=type_hints["associate_wireless_device"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disassociate_wireless_device", value=disassociate_wireless_device, expected_type=type_hints["disassociate_wireless_device"])
            check_type(argname="argument lo_ra_wan", value=lo_ra_wan, expected_type=type_hints["lo_ra_wan"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if associate_wireless_device is not None:
            self._values["associate_wireless_device"] = associate_wireless_device
        if description is not None:
            self._values["description"] = description
        if disassociate_wireless_device is not None:
            self._values["disassociate_wireless_device"] = disassociate_wireless_device
        if lo_ra_wan is not None:
            self._values["lo_ra_wan"] = lo_ra_wan
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def associate_wireless_device(self) -> typing.Optional[builtins.str]:
        '''The ID of the wireless device to associate with a multicast group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-multicastgroup.html#cfn-iotwireless-multicastgroup-associatewirelessdevice
        '''
        result = self._values.get("associate_wireless_device")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the multicast group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-multicastgroup.html#cfn-iotwireless-multicastgroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disassociate_wireless_device(self) -> typing.Optional[builtins.str]:
        '''The ID of the wireless device to disassociate from a multicast group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-multicastgroup.html#cfn-iotwireless-multicastgroup-disassociatewirelessdevice
        '''
        result = self._values.get("disassociate_wireless_device")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lo_ra_wan(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMulticastGroupPropsMixin.LoRaWANProperty"]]:
        '''The LoRaWAN information that is to be used with the multicast group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-multicastgroup.html#cfn-iotwireless-multicastgroup-lorawan
        '''
        result = self._values.get("lo_ra_wan")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMulticastGroupPropsMixin.LoRaWANProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the multicast group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-multicastgroup.html#cfn-iotwireless-multicastgroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags are an array of key-value pairs to attach to the specified resource.

        Tags can have a minimum of 0 and a maximum of 50 items.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-multicastgroup.html#cfn-iotwireless-multicastgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMulticastGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMulticastGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnMulticastGroupPropsMixin",
):
    '''A multicast group.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-multicastgroup.html
    :cloudformationResource: AWS::IoTWireless::MulticastGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
        
        cfn_multicast_group_props_mixin = iotwireless_mixins.CfnMulticastGroupPropsMixin(iotwireless_mixins.CfnMulticastGroupMixinProps(
            associate_wireless_device="associateWirelessDevice",
            description="description",
            disassociate_wireless_device="disassociateWirelessDevice",
            lo_ra_wan=iotwireless_mixins.CfnMulticastGroupPropsMixin.LoRaWANProperty(
                dl_class="dlClass",
                number_of_devices_in_group=123,
                number_of_devices_requested=123,
                rf_region="rfRegion"
            ),
            name="name",
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
        props: typing.Union[CfnMulticastGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTWireless::MulticastGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__696838f172b0af0022434675a542dd823b071e97335751e6baec7e2785c915e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ca6c7f6986f32325806f9c05a701c350e787d11a2fc3b81063f58374136f56d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__193687e5581c68de4b59e4940db24a7a45702424cb34670f5a7051f6da6888c8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMulticastGroupMixinProps:
        return typing.cast(CfnMulticastGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnMulticastGroupPropsMixin.LoRaWANProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dl_class": "dlClass",
            "number_of_devices_in_group": "numberOfDevicesInGroup",
            "number_of_devices_requested": "numberOfDevicesRequested",
            "rf_region": "rfRegion",
        },
    )
    class LoRaWANProperty:
        def __init__(
            self,
            *,
            dl_class: typing.Optional[builtins.str] = None,
            number_of_devices_in_group: typing.Optional[jsii.Number] = None,
            number_of_devices_requested: typing.Optional[jsii.Number] = None,
            rf_region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The LoRaWAN information that is to be used with the multicast group.

            :param dl_class: DlClass for LoRaWAN. Valid values are ClassB and ClassC.
            :param number_of_devices_in_group: Number of devices that are associated to the multicast group.
            :param number_of_devices_requested: Number of devices that are requested to be associated with the multicast group.
            :param rf_region: The frequency band (RFRegion) value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-multicastgroup-lorawan.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
                
                lo_ra_wANProperty = iotwireless_mixins.CfnMulticastGroupPropsMixin.LoRaWANProperty(
                    dl_class="dlClass",
                    number_of_devices_in_group=123,
                    number_of_devices_requested=123,
                    rf_region="rfRegion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4f44d8fd8d816ec48f720435f25141268e5bbf18af5fe768c8b90747cfbd2adc)
                check_type(argname="argument dl_class", value=dl_class, expected_type=type_hints["dl_class"])
                check_type(argname="argument number_of_devices_in_group", value=number_of_devices_in_group, expected_type=type_hints["number_of_devices_in_group"])
                check_type(argname="argument number_of_devices_requested", value=number_of_devices_requested, expected_type=type_hints["number_of_devices_requested"])
                check_type(argname="argument rf_region", value=rf_region, expected_type=type_hints["rf_region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dl_class is not None:
                self._values["dl_class"] = dl_class
            if number_of_devices_in_group is not None:
                self._values["number_of_devices_in_group"] = number_of_devices_in_group
            if number_of_devices_requested is not None:
                self._values["number_of_devices_requested"] = number_of_devices_requested
            if rf_region is not None:
                self._values["rf_region"] = rf_region

        @builtins.property
        def dl_class(self) -> typing.Optional[builtins.str]:
            '''DlClass for LoRaWAN.

            Valid values are ClassB and ClassC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-multicastgroup-lorawan.html#cfn-iotwireless-multicastgroup-lorawan-dlclass
            '''
            result = self._values.get("dl_class")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def number_of_devices_in_group(self) -> typing.Optional[jsii.Number]:
            '''Number of devices that are associated to the multicast group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-multicastgroup-lorawan.html#cfn-iotwireless-multicastgroup-lorawan-numberofdevicesingroup
            '''
            result = self._values.get("number_of_devices_in_group")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def number_of_devices_requested(self) -> typing.Optional[jsii.Number]:
            '''Number of devices that are requested to be associated with the multicast group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-multicastgroup-lorawan.html#cfn-iotwireless-multicastgroup-lorawan-numberofdevicesrequested
            '''
            result = self._values.get("number_of_devices_requested")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def rf_region(self) -> typing.Optional[builtins.str]:
            '''The frequency band (RFRegion) value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-multicastgroup-lorawan.html#cfn-iotwireless-multicastgroup-lorawan-rfregion
            '''
            result = self._values.get("rf_region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoRaWANProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnNetworkAnalyzerConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "tags": "tags",
        "trace_content": "traceContent",
        "wireless_devices": "wirelessDevices",
        "wireless_gateways": "wirelessGateways",
    },
)
class CfnNetworkAnalyzerConfigurationMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        trace_content: typing.Any = None,
        wireless_devices: typing.Optional[typing.Sequence[builtins.str]] = None,
        wireless_gateways: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnNetworkAnalyzerConfigurationPropsMixin.

        :param description: The description of the resource.
        :param name: Name of the network analyzer configuration.
        :param tags: The tags to attach to the specified resource. Tags are metadata that you can use to manage a resource.
        :param trace_content: Trace content for your wireless gateway and wireless device resources.
        :param wireless_devices: Wireless device resources to add to the network analyzer configuration. Provide the ``WirelessDeviceId`` of the resource to add in the input array.
        :param wireless_gateways: Wireless gateway resources to add to the network analyzer configuration. Provide the ``WirelessGatewayId`` of the resource to add in the input array.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-networkanalyzerconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
            
            # trace_content: Any
            
            cfn_network_analyzer_configuration_mixin_props = iotwireless_mixins.CfnNetworkAnalyzerConfigurationMixinProps(
                description="description",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                trace_content=trace_content,
                wireless_devices=["wirelessDevices"],
                wireless_gateways=["wirelessGateways"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__420538a85014f0c71073dc5d726d573ee8f47401da75d2abfab391e1ab1f17df)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument trace_content", value=trace_content, expected_type=type_hints["trace_content"])
            check_type(argname="argument wireless_devices", value=wireless_devices, expected_type=type_hints["wireless_devices"])
            check_type(argname="argument wireless_gateways", value=wireless_gateways, expected_type=type_hints["wireless_gateways"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if trace_content is not None:
            self._values["trace_content"] = trace_content
        if wireless_devices is not None:
            self._values["wireless_devices"] = wireless_devices
        if wireless_gateways is not None:
            self._values["wireless_gateways"] = wireless_gateways

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-networkanalyzerconfiguration.html#cfn-iotwireless-networkanalyzerconfiguration-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the network analyzer configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-networkanalyzerconfiguration.html#cfn-iotwireless-networkanalyzerconfiguration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to attach to the specified resource.

        Tags are metadata that you can use to manage a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-networkanalyzerconfiguration.html#cfn-iotwireless-networkanalyzerconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def trace_content(self) -> typing.Any:
        '''Trace content for your wireless gateway and wireless device resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-networkanalyzerconfiguration.html#cfn-iotwireless-networkanalyzerconfiguration-tracecontent
        '''
        result = self._values.get("trace_content")
        return typing.cast(typing.Any, result)

    @builtins.property
    def wireless_devices(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Wireless device resources to add to the network analyzer configuration.

        Provide the ``WirelessDeviceId`` of the resource to add in the input array.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-networkanalyzerconfiguration.html#cfn-iotwireless-networkanalyzerconfiguration-wirelessdevices
        '''
        result = self._values.get("wireless_devices")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def wireless_gateways(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Wireless gateway resources to add to the network analyzer configuration.

        Provide the ``WirelessGatewayId`` of the resource to add in the input array.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-networkanalyzerconfiguration.html#cfn-iotwireless-networkanalyzerconfiguration-wirelessgateways
        '''
        result = self._values.get("wireless_gateways")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNetworkAnalyzerConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnNetworkAnalyzerConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnNetworkAnalyzerConfigurationPropsMixin",
):
    '''Network analyzer configuration.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-networkanalyzerconfiguration.html
    :cloudformationResource: AWS::IoTWireless::NetworkAnalyzerConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
        
        # trace_content: Any
        
        cfn_network_analyzer_configuration_props_mixin = iotwireless_mixins.CfnNetworkAnalyzerConfigurationPropsMixin(iotwireless_mixins.CfnNetworkAnalyzerConfigurationMixinProps(
            description="description",
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            trace_content=trace_content,
            wireless_devices=["wirelessDevices"],
            wireless_gateways=["wirelessGateways"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnNetworkAnalyzerConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTWireless::NetworkAnalyzerConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__244b9085b4b92c6c182968f1190bc532e2ca2bd422b05f10b99f2ba4ef5d5f66)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba40b85d7c1b2ba291fc7f02e1c1a4b0cabcf879393963453090a4db08254dba)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__615b9ccce9dee61e7ae3b954ddbaecf344c70f6dc60476a085f7c08de2c75568)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnNetworkAnalyzerConfigurationMixinProps:
        return typing.cast(CfnNetworkAnalyzerConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnNetworkAnalyzerConfigurationPropsMixin.TraceContentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "log_level": "logLevel",
            "wireless_device_frame_info": "wirelessDeviceFrameInfo",
        },
    )
    class TraceContentProperty:
        def __init__(
            self,
            *,
            log_level: typing.Optional[builtins.str] = None,
            wireless_device_frame_info: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Trace content for your wireless gateway and wireless device resources.

            :param log_level: The log level for a log message. The log levels can be disabled, or set to ``ERROR`` to display less verbose logs containing only error information, or to ``INFO`` for more detailed logs
            :param wireless_device_frame_info: ``FrameInfo`` of your wireless device resources for the trace content. Use FrameInfo to debug the communication between your LoRaWAN end devices and the network server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-networkanalyzerconfiguration-tracecontent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
                
                trace_content_property = iotwireless_mixins.CfnNetworkAnalyzerConfigurationPropsMixin.TraceContentProperty(
                    log_level="logLevel",
                    wireless_device_frame_info="wirelessDeviceFrameInfo"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__31a7a06e93debabd56b5de01ed1ec0dd3a4e06e2da625e8924b6a7652716ae65)
                check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
                check_type(argname="argument wireless_device_frame_info", value=wireless_device_frame_info, expected_type=type_hints["wireless_device_frame_info"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_level is not None:
                self._values["log_level"] = log_level
            if wireless_device_frame_info is not None:
                self._values["wireless_device_frame_info"] = wireless_device_frame_info

        @builtins.property
        def log_level(self) -> typing.Optional[builtins.str]:
            '''The log level for a log message.

            The log levels can be disabled, or set to ``ERROR`` to display less verbose logs containing only error information, or to ``INFO`` for more detailed logs

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-networkanalyzerconfiguration-tracecontent.html#cfn-iotwireless-networkanalyzerconfiguration-tracecontent-loglevel
            '''
            result = self._values.get("log_level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def wireless_device_frame_info(self) -> typing.Optional[builtins.str]:
            '''``FrameInfo`` of your wireless device resources for the trace content.

            Use FrameInfo to debug the communication between your LoRaWAN end devices and the network server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-networkanalyzerconfiguration-tracecontent.html#cfn-iotwireless-networkanalyzerconfiguration-tracecontent-wirelessdeviceframeinfo
            '''
            result = self._values.get("wireless_device_frame_info")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TraceContentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnPartnerAccountMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "account_linked": "accountLinked",
        "partner_account_id": "partnerAccountId",
        "partner_type": "partnerType",
        "sidewalk": "sidewalk",
        "sidewalk_response": "sidewalkResponse",
        "sidewalk_update": "sidewalkUpdate",
        "tags": "tags",
    },
)
class CfnPartnerAccountMixinProps:
    def __init__(
        self,
        *,
        account_linked: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        partner_account_id: typing.Optional[builtins.str] = None,
        partner_type: typing.Optional[builtins.str] = None,
        sidewalk: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPartnerAccountPropsMixin.SidewalkAccountInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sidewalk_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPartnerAccountPropsMixin.SidewalkAccountInfoWithFingerprintProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sidewalk_update: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPartnerAccountPropsMixin.SidewalkUpdateAccountProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPartnerAccountPropsMixin.

        :param account_linked: Whether the partner account is linked to the AWS account.
        :param partner_account_id: The ID of the partner account to update.
        :param partner_type: The partner type.
        :param sidewalk: The Sidewalk account credentials.
        :param sidewalk_response: Information about a Sidewalk account.
        :param sidewalk_update: Sidewalk update.
        :param tags: The tags are an array of key-value pairs to attach to the specified resource. Tags can have a minimum of 0 and a maximum of 50 items.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-partneraccount.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
            
            cfn_partner_account_mixin_props = iotwireless_mixins.CfnPartnerAccountMixinProps(
                account_linked=False,
                partner_account_id="partnerAccountId",
                partner_type="partnerType",
                sidewalk=iotwireless_mixins.CfnPartnerAccountPropsMixin.SidewalkAccountInfoProperty(
                    app_server_private_key="appServerPrivateKey"
                ),
                sidewalk_response=iotwireless_mixins.CfnPartnerAccountPropsMixin.SidewalkAccountInfoWithFingerprintProperty(
                    amazon_id="amazonId",
                    arn="arn",
                    fingerprint="fingerprint"
                ),
                sidewalk_update=iotwireless_mixins.CfnPartnerAccountPropsMixin.SidewalkUpdateAccountProperty(
                    app_server_private_key="appServerPrivateKey"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1feb9dfbe264a9bdb86d1d9ca016f55eb7d15bfb579ec0ec5683edd9bcd8bb2c)
            check_type(argname="argument account_linked", value=account_linked, expected_type=type_hints["account_linked"])
            check_type(argname="argument partner_account_id", value=partner_account_id, expected_type=type_hints["partner_account_id"])
            check_type(argname="argument partner_type", value=partner_type, expected_type=type_hints["partner_type"])
            check_type(argname="argument sidewalk", value=sidewalk, expected_type=type_hints["sidewalk"])
            check_type(argname="argument sidewalk_response", value=sidewalk_response, expected_type=type_hints["sidewalk_response"])
            check_type(argname="argument sidewalk_update", value=sidewalk_update, expected_type=type_hints["sidewalk_update"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_linked is not None:
            self._values["account_linked"] = account_linked
        if partner_account_id is not None:
            self._values["partner_account_id"] = partner_account_id
        if partner_type is not None:
            self._values["partner_type"] = partner_type
        if sidewalk is not None:
            self._values["sidewalk"] = sidewalk
        if sidewalk_response is not None:
            self._values["sidewalk_response"] = sidewalk_response
        if sidewalk_update is not None:
            self._values["sidewalk_update"] = sidewalk_update
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def account_linked(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether the partner account is linked to the AWS account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-partneraccount.html#cfn-iotwireless-partneraccount-accountlinked
        '''
        result = self._values.get("account_linked")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def partner_account_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the partner account to update.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-partneraccount.html#cfn-iotwireless-partneraccount-partneraccountid
        '''
        result = self._values.get("partner_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partner_type(self) -> typing.Optional[builtins.str]:
        '''The partner type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-partneraccount.html#cfn-iotwireless-partneraccount-partnertype
        '''
        result = self._values.get("partner_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sidewalk(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnerAccountPropsMixin.SidewalkAccountInfoProperty"]]:
        '''The Sidewalk account credentials.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-partneraccount.html#cfn-iotwireless-partneraccount-sidewalk
        '''
        result = self._values.get("sidewalk")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnerAccountPropsMixin.SidewalkAccountInfoProperty"]], result)

    @builtins.property
    def sidewalk_response(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnerAccountPropsMixin.SidewalkAccountInfoWithFingerprintProperty"]]:
        '''Information about a Sidewalk account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-partneraccount.html#cfn-iotwireless-partneraccount-sidewalkresponse
        '''
        result = self._values.get("sidewalk_response")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnerAccountPropsMixin.SidewalkAccountInfoWithFingerprintProperty"]], result)

    @builtins.property
    def sidewalk_update(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnerAccountPropsMixin.SidewalkUpdateAccountProperty"]]:
        '''Sidewalk update.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-partneraccount.html#cfn-iotwireless-partneraccount-sidewalkupdate
        '''
        result = self._values.get("sidewalk_update")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartnerAccountPropsMixin.SidewalkUpdateAccountProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags are an array of key-value pairs to attach to the specified resource.

        Tags can have a minimum of 0 and a maximum of 50 items.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-partneraccount.html#cfn-iotwireless-partneraccount-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPartnerAccountMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPartnerAccountPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnPartnerAccountPropsMixin",
):
    '''A partner account.

    If ``PartnerAccountId`` and ``PartnerType`` are ``null`` , returns all partner accounts.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-partneraccount.html
    :cloudformationResource: AWS::IoTWireless::PartnerAccount
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
        
        cfn_partner_account_props_mixin = iotwireless_mixins.CfnPartnerAccountPropsMixin(iotwireless_mixins.CfnPartnerAccountMixinProps(
            account_linked=False,
            partner_account_id="partnerAccountId",
            partner_type="partnerType",
            sidewalk=iotwireless_mixins.CfnPartnerAccountPropsMixin.SidewalkAccountInfoProperty(
                app_server_private_key="appServerPrivateKey"
            ),
            sidewalk_response=iotwireless_mixins.CfnPartnerAccountPropsMixin.SidewalkAccountInfoWithFingerprintProperty(
                amazon_id="amazonId",
                arn="arn",
                fingerprint="fingerprint"
            ),
            sidewalk_update=iotwireless_mixins.CfnPartnerAccountPropsMixin.SidewalkUpdateAccountProperty(
                app_server_private_key="appServerPrivateKey"
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
        props: typing.Union[CfnPartnerAccountMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTWireless::PartnerAccount``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__133720bf4cb46a0b14c7eeb49b0e7cd4a94c21d52dce7084e96cb570b6e3c6a9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c0e8a19dd344704e4840d05852c15d8fd7c191599ebc42d722741955baa205f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1439c7c94dd1a31bad1494a2b57fdf37fed85471335485ab90554cd3e2aa2be3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPartnerAccountMixinProps:
        return typing.cast(CfnPartnerAccountMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnPartnerAccountPropsMixin.SidewalkAccountInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"app_server_private_key": "appServerPrivateKey"},
    )
    class SidewalkAccountInfoProperty:
        def __init__(
            self,
            *,
            app_server_private_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a Sidewalk account.

            :param app_server_private_key: The Sidewalk application server private key. The application server private key is a secret key, which you should handle in a similar way as you would an application password. You can protect the application server private key by storing the value in the AWS Secrets Manager and use the `secretsmanager <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html#dynamic-references-secretsmanager>`_ to reference this value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-partneraccount-sidewalkaccountinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
                
                sidewalk_account_info_property = iotwireless_mixins.CfnPartnerAccountPropsMixin.SidewalkAccountInfoProperty(
                    app_server_private_key="appServerPrivateKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1079a03794d63e2ea872be0245b068ba625186de97fe65d6444f8eeadcc8b11f)
                check_type(argname="argument app_server_private_key", value=app_server_private_key, expected_type=type_hints["app_server_private_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if app_server_private_key is not None:
                self._values["app_server_private_key"] = app_server_private_key

        @builtins.property
        def app_server_private_key(self) -> typing.Optional[builtins.str]:
            '''The Sidewalk application server private key.

            The application server private key is a secret key, which you should handle in a similar way as you would an application password. You can protect the application server private key by storing the value in the AWS Secrets Manager and use the `secretsmanager <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html#dynamic-references-secretsmanager>`_ to reference this value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-partneraccount-sidewalkaccountinfo.html#cfn-iotwireless-partneraccount-sidewalkaccountinfo-appserverprivatekey
            '''
            result = self._values.get("app_server_private_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SidewalkAccountInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnPartnerAccountPropsMixin.SidewalkAccountInfoWithFingerprintProperty",
        jsii_struct_bases=[],
        name_mapping={
            "amazon_id": "amazonId",
            "arn": "arn",
            "fingerprint": "fingerprint",
        },
    )
    class SidewalkAccountInfoWithFingerprintProperty:
        def __init__(
            self,
            *,
            amazon_id: typing.Optional[builtins.str] = None,
            arn: typing.Optional[builtins.str] = None,
            fingerprint: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a Sidewalk account.

            :param amazon_id: The Sidewalk Amazon ID.
            :param arn: The Amazon Resource Name (ARN) of the resource.
            :param fingerprint: The fingerprint of the Sidewalk application server private key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-partneraccount-sidewalkaccountinfowithfingerprint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
                
                sidewalk_account_info_with_fingerprint_property = iotwireless_mixins.CfnPartnerAccountPropsMixin.SidewalkAccountInfoWithFingerprintProperty(
                    amazon_id="amazonId",
                    arn="arn",
                    fingerprint="fingerprint"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5cce43c2c1d2261a4f5644bc66381134131c8d0972aeaa361b6f61174c6614a9)
                check_type(argname="argument amazon_id", value=amazon_id, expected_type=type_hints["amazon_id"])
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument fingerprint", value=fingerprint, expected_type=type_hints["fingerprint"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if amazon_id is not None:
                self._values["amazon_id"] = amazon_id
            if arn is not None:
                self._values["arn"] = arn
            if fingerprint is not None:
                self._values["fingerprint"] = fingerprint

        @builtins.property
        def amazon_id(self) -> typing.Optional[builtins.str]:
            '''The Sidewalk Amazon ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-partneraccount-sidewalkaccountinfowithfingerprint.html#cfn-iotwireless-partneraccount-sidewalkaccountinfowithfingerprint-amazonid
            '''
            result = self._values.get("amazon_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-partneraccount-sidewalkaccountinfowithfingerprint.html#cfn-iotwireless-partneraccount-sidewalkaccountinfowithfingerprint-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def fingerprint(self) -> typing.Optional[builtins.str]:
            '''The fingerprint of the Sidewalk application server private key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-partneraccount-sidewalkaccountinfowithfingerprint.html#cfn-iotwireless-partneraccount-sidewalkaccountinfowithfingerprint-fingerprint
            '''
            result = self._values.get("fingerprint")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SidewalkAccountInfoWithFingerprintProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnPartnerAccountPropsMixin.SidewalkUpdateAccountProperty",
        jsii_struct_bases=[],
        name_mapping={"app_server_private_key": "appServerPrivateKey"},
    )
    class SidewalkUpdateAccountProperty:
        def __init__(
            self,
            *,
            app_server_private_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Sidewalk update.

            :param app_server_private_key: The new Sidewalk application server private key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-partneraccount-sidewalkupdateaccount.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
                
                sidewalk_update_account_property = iotwireless_mixins.CfnPartnerAccountPropsMixin.SidewalkUpdateAccountProperty(
                    app_server_private_key="appServerPrivateKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0de01f740a81b01c044c3384d88a8407abec071c014078daac2a4a9e58d7ec3f)
                check_type(argname="argument app_server_private_key", value=app_server_private_key, expected_type=type_hints["app_server_private_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if app_server_private_key is not None:
                self._values["app_server_private_key"] = app_server_private_key

        @builtins.property
        def app_server_private_key(self) -> typing.Optional[builtins.str]:
            '''The new Sidewalk application server private key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-partneraccount-sidewalkupdateaccount.html#cfn-iotwireless-partneraccount-sidewalkupdateaccount-appserverprivatekey
            '''
            result = self._values.get("app_server_private_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SidewalkUpdateAccountProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnServiceProfileMixinProps",
    jsii_struct_bases=[],
    name_mapping={"lo_ra_wan": "loRaWan", "name": "name", "tags": "tags"},
)
class CfnServiceProfileMixinProps:
    def __init__(
        self,
        *,
        lo_ra_wan: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceProfilePropsMixin.LoRaWANServiceProfileProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnServiceProfilePropsMixin.

        :param lo_ra_wan: LoRaWAN service profile object.
        :param name: The name of the new resource.
        :param tags: The tags are an array of key-value pairs to attach to the specified resource. Tags can have a minimum of 0 and a maximum of 50 items.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-serviceprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
            
            cfn_service_profile_mixin_props = iotwireless_mixins.CfnServiceProfileMixinProps(
                lo_ra_wan=iotwireless_mixins.CfnServiceProfilePropsMixin.LoRaWANServiceProfileProperty(
                    add_gw_metadata=False,
                    channel_mask="channelMask",
                    dev_status_req_freq=123,
                    dl_bucket_size=123,
                    dl_rate=123,
                    dl_rate_policy="dlRatePolicy",
                    dr_max=123,
                    dr_min=123,
                    hr_allowed=False,
                    min_gw_diversity=123,
                    nwk_geo_loc=False,
                    pr_allowed=False,
                    ra_allowed=False,
                    report_dev_status_battery=False,
                    report_dev_status_margin=False,
                    target_per=123,
                    ul_bucket_size=123,
                    ul_rate=123,
                    ul_rate_policy="ulRatePolicy"
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b7a27dfc20de1a40003bea11f979959d61d4d898d90f5644befff8c573df71d)
            check_type(argname="argument lo_ra_wan", value=lo_ra_wan, expected_type=type_hints["lo_ra_wan"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if lo_ra_wan is not None:
            self._values["lo_ra_wan"] = lo_ra_wan
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def lo_ra_wan(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceProfilePropsMixin.LoRaWANServiceProfileProperty"]]:
        '''LoRaWAN service profile object.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-serviceprofile.html#cfn-iotwireless-serviceprofile-lorawan
        '''
        result = self._values.get("lo_ra_wan")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceProfilePropsMixin.LoRaWANServiceProfileProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the new resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-serviceprofile.html#cfn-iotwireless-serviceprofile-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags are an array of key-value pairs to attach to the specified resource.

        Tags can have a minimum of 0 and a maximum of 50 items.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-serviceprofile.html#cfn-iotwireless-serviceprofile-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceProfileMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnServiceProfilePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnServiceProfilePropsMixin",
):
    '''Creates a new service profile.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-serviceprofile.html
    :cloudformationResource: AWS::IoTWireless::ServiceProfile
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
        
        cfn_service_profile_props_mixin = iotwireless_mixins.CfnServiceProfilePropsMixin(iotwireless_mixins.CfnServiceProfileMixinProps(
            lo_ra_wan=iotwireless_mixins.CfnServiceProfilePropsMixin.LoRaWANServiceProfileProperty(
                add_gw_metadata=False,
                channel_mask="channelMask",
                dev_status_req_freq=123,
                dl_bucket_size=123,
                dl_rate=123,
                dl_rate_policy="dlRatePolicy",
                dr_max=123,
                dr_min=123,
                hr_allowed=False,
                min_gw_diversity=123,
                nwk_geo_loc=False,
                pr_allowed=False,
                ra_allowed=False,
                report_dev_status_battery=False,
                report_dev_status_margin=False,
                target_per=123,
                ul_bucket_size=123,
                ul_rate=123,
                ul_rate_policy="ulRatePolicy"
            ),
            name="name",
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
        props: typing.Union[CfnServiceProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTWireless::ServiceProfile``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be45cb0cc715db4ff657b3d596929f63ef5d96aad34eb856d5fe12817e70f1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bd7c4b69fcb48185e91b8e98325205dc5fdf4285ce8e231708842c1f644880b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcf90559b41a00aa1b22797c656e014bc73e21922917538a4d4ba192cf970b86)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnServiceProfileMixinProps:
        return typing.cast(CfnServiceProfileMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnServiceProfilePropsMixin.LoRaWANServiceProfileProperty",
        jsii_struct_bases=[],
        name_mapping={
            "add_gw_metadata": "addGwMetadata",
            "channel_mask": "channelMask",
            "dev_status_req_freq": "devStatusReqFreq",
            "dl_bucket_size": "dlBucketSize",
            "dl_rate": "dlRate",
            "dl_rate_policy": "dlRatePolicy",
            "dr_max": "drMax",
            "dr_min": "drMin",
            "hr_allowed": "hrAllowed",
            "min_gw_diversity": "minGwDiversity",
            "nwk_geo_loc": "nwkGeoLoc",
            "pr_allowed": "prAllowed",
            "ra_allowed": "raAllowed",
            "report_dev_status_battery": "reportDevStatusBattery",
            "report_dev_status_margin": "reportDevStatusMargin",
            "target_per": "targetPer",
            "ul_bucket_size": "ulBucketSize",
            "ul_rate": "ulRate",
            "ul_rate_policy": "ulRatePolicy",
        },
    )
    class LoRaWANServiceProfileProperty:
        def __init__(
            self,
            *,
            add_gw_metadata: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            channel_mask: typing.Optional[builtins.str] = None,
            dev_status_req_freq: typing.Optional[jsii.Number] = None,
            dl_bucket_size: typing.Optional[jsii.Number] = None,
            dl_rate: typing.Optional[jsii.Number] = None,
            dl_rate_policy: typing.Optional[builtins.str] = None,
            dr_max: typing.Optional[jsii.Number] = None,
            dr_min: typing.Optional[jsii.Number] = None,
            hr_allowed: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            min_gw_diversity: typing.Optional[jsii.Number] = None,
            nwk_geo_loc: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            pr_allowed: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            ra_allowed: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            report_dev_status_battery: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            report_dev_status_margin: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            target_per: typing.Optional[jsii.Number] = None,
            ul_bucket_size: typing.Optional[jsii.Number] = None,
            ul_rate: typing.Optional[jsii.Number] = None,
            ul_rate_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''LoRaWANServiceProfile object.

            :param add_gw_metadata: The AddGWMetaData value.
            :param channel_mask: The ChannelMask value. This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``
            :param dev_status_req_freq: The DevStatusReqFreq value. This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``
            :param dl_bucket_size: The DLBucketSize value. This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``
            :param dl_rate: The DLRate value. This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``
            :param dl_rate_policy: The DLRatePolicy value. This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``
            :param dr_max: The DRMax value. This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``
            :param dr_min: The DRMin value. This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``
            :param hr_allowed: The HRAllowed value that describes whether handover roaming is allowed. This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``
            :param min_gw_diversity: The MinGwDiversity value. This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``
            :param nwk_geo_loc: The NwkGeoLoc value. This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``
            :param pr_allowed: The PRAllowed value that describes whether passive roaming is allowed. This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``
            :param ra_allowed: The RAAllowed value that describes whether roaming activation is allowed.
            :param report_dev_status_battery: The ReportDevStatusBattery value. This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``
            :param report_dev_status_margin: The ReportDevStatusMargin value. This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``
            :param target_per: The TargetPer value. This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``
            :param ul_bucket_size: The UlBucketSize value. This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``
            :param ul_rate: The ULRate value. This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``
            :param ul_rate_policy: The ULRatePolicy value. This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-serviceprofile-lorawanserviceprofile.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
                
                lo_ra_wANService_profile_property = iotwireless_mixins.CfnServiceProfilePropsMixin.LoRaWANServiceProfileProperty(
                    add_gw_metadata=False,
                    channel_mask="channelMask",
                    dev_status_req_freq=123,
                    dl_bucket_size=123,
                    dl_rate=123,
                    dl_rate_policy="dlRatePolicy",
                    dr_max=123,
                    dr_min=123,
                    hr_allowed=False,
                    min_gw_diversity=123,
                    nwk_geo_loc=False,
                    pr_allowed=False,
                    ra_allowed=False,
                    report_dev_status_battery=False,
                    report_dev_status_margin=False,
                    target_per=123,
                    ul_bucket_size=123,
                    ul_rate=123,
                    ul_rate_policy="ulRatePolicy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__42d698a42b05fd254a30bbcf7614d2d486ed8979b30b8b2fa35371f17acdb22e)
                check_type(argname="argument add_gw_metadata", value=add_gw_metadata, expected_type=type_hints["add_gw_metadata"])
                check_type(argname="argument channel_mask", value=channel_mask, expected_type=type_hints["channel_mask"])
                check_type(argname="argument dev_status_req_freq", value=dev_status_req_freq, expected_type=type_hints["dev_status_req_freq"])
                check_type(argname="argument dl_bucket_size", value=dl_bucket_size, expected_type=type_hints["dl_bucket_size"])
                check_type(argname="argument dl_rate", value=dl_rate, expected_type=type_hints["dl_rate"])
                check_type(argname="argument dl_rate_policy", value=dl_rate_policy, expected_type=type_hints["dl_rate_policy"])
                check_type(argname="argument dr_max", value=dr_max, expected_type=type_hints["dr_max"])
                check_type(argname="argument dr_min", value=dr_min, expected_type=type_hints["dr_min"])
                check_type(argname="argument hr_allowed", value=hr_allowed, expected_type=type_hints["hr_allowed"])
                check_type(argname="argument min_gw_diversity", value=min_gw_diversity, expected_type=type_hints["min_gw_diversity"])
                check_type(argname="argument nwk_geo_loc", value=nwk_geo_loc, expected_type=type_hints["nwk_geo_loc"])
                check_type(argname="argument pr_allowed", value=pr_allowed, expected_type=type_hints["pr_allowed"])
                check_type(argname="argument ra_allowed", value=ra_allowed, expected_type=type_hints["ra_allowed"])
                check_type(argname="argument report_dev_status_battery", value=report_dev_status_battery, expected_type=type_hints["report_dev_status_battery"])
                check_type(argname="argument report_dev_status_margin", value=report_dev_status_margin, expected_type=type_hints["report_dev_status_margin"])
                check_type(argname="argument target_per", value=target_per, expected_type=type_hints["target_per"])
                check_type(argname="argument ul_bucket_size", value=ul_bucket_size, expected_type=type_hints["ul_bucket_size"])
                check_type(argname="argument ul_rate", value=ul_rate, expected_type=type_hints["ul_rate"])
                check_type(argname="argument ul_rate_policy", value=ul_rate_policy, expected_type=type_hints["ul_rate_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if add_gw_metadata is not None:
                self._values["add_gw_metadata"] = add_gw_metadata
            if channel_mask is not None:
                self._values["channel_mask"] = channel_mask
            if dev_status_req_freq is not None:
                self._values["dev_status_req_freq"] = dev_status_req_freq
            if dl_bucket_size is not None:
                self._values["dl_bucket_size"] = dl_bucket_size
            if dl_rate is not None:
                self._values["dl_rate"] = dl_rate
            if dl_rate_policy is not None:
                self._values["dl_rate_policy"] = dl_rate_policy
            if dr_max is not None:
                self._values["dr_max"] = dr_max
            if dr_min is not None:
                self._values["dr_min"] = dr_min
            if hr_allowed is not None:
                self._values["hr_allowed"] = hr_allowed
            if min_gw_diversity is not None:
                self._values["min_gw_diversity"] = min_gw_diversity
            if nwk_geo_loc is not None:
                self._values["nwk_geo_loc"] = nwk_geo_loc
            if pr_allowed is not None:
                self._values["pr_allowed"] = pr_allowed
            if ra_allowed is not None:
                self._values["ra_allowed"] = ra_allowed
            if report_dev_status_battery is not None:
                self._values["report_dev_status_battery"] = report_dev_status_battery
            if report_dev_status_margin is not None:
                self._values["report_dev_status_margin"] = report_dev_status_margin
            if target_per is not None:
                self._values["target_per"] = target_per
            if ul_bucket_size is not None:
                self._values["ul_bucket_size"] = ul_bucket_size
            if ul_rate is not None:
                self._values["ul_rate"] = ul_rate
            if ul_rate_policy is not None:
                self._values["ul_rate_policy"] = ul_rate_policy

        @builtins.property
        def add_gw_metadata(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The AddGWMetaData value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-serviceprofile-lorawanserviceprofile.html#cfn-iotwireless-serviceprofile-lorawanserviceprofile-addgwmetadata
            '''
            result = self._values.get("add_gw_metadata")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def channel_mask(self) -> typing.Optional[builtins.str]:
            '''The ChannelMask value.

            This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-serviceprofile-lorawanserviceprofile.html#cfn-iotwireless-serviceprofile-lorawanserviceprofile-channelmask
            '''
            result = self._values.get("channel_mask")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dev_status_req_freq(self) -> typing.Optional[jsii.Number]:
            '''The DevStatusReqFreq value.

            This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-serviceprofile-lorawanserviceprofile.html#cfn-iotwireless-serviceprofile-lorawanserviceprofile-devstatusreqfreq
            '''
            result = self._values.get("dev_status_req_freq")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def dl_bucket_size(self) -> typing.Optional[jsii.Number]:
            '''The DLBucketSize value.

            This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-serviceprofile-lorawanserviceprofile.html#cfn-iotwireless-serviceprofile-lorawanserviceprofile-dlbucketsize
            '''
            result = self._values.get("dl_bucket_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def dl_rate(self) -> typing.Optional[jsii.Number]:
            '''The DLRate value.

            This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-serviceprofile-lorawanserviceprofile.html#cfn-iotwireless-serviceprofile-lorawanserviceprofile-dlrate
            '''
            result = self._values.get("dl_rate")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def dl_rate_policy(self) -> typing.Optional[builtins.str]:
            '''The DLRatePolicy value.

            This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-serviceprofile-lorawanserviceprofile.html#cfn-iotwireless-serviceprofile-lorawanserviceprofile-dlratepolicy
            '''
            result = self._values.get("dl_rate_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dr_max(self) -> typing.Optional[jsii.Number]:
            '''The DRMax value.

            This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-serviceprofile-lorawanserviceprofile.html#cfn-iotwireless-serviceprofile-lorawanserviceprofile-drmax
            '''
            result = self._values.get("dr_max")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def dr_min(self) -> typing.Optional[jsii.Number]:
            '''The DRMin value.

            This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-serviceprofile-lorawanserviceprofile.html#cfn-iotwireless-serviceprofile-lorawanserviceprofile-drmin
            '''
            result = self._values.get("dr_min")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def hr_allowed(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The HRAllowed value that describes whether handover roaming is allowed.

            This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-serviceprofile-lorawanserviceprofile.html#cfn-iotwireless-serviceprofile-lorawanserviceprofile-hrallowed
            '''
            result = self._values.get("hr_allowed")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def min_gw_diversity(self) -> typing.Optional[jsii.Number]:
            '''The MinGwDiversity value.

            This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-serviceprofile-lorawanserviceprofile.html#cfn-iotwireless-serviceprofile-lorawanserviceprofile-mingwdiversity
            '''
            result = self._values.get("min_gw_diversity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def nwk_geo_loc(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The NwkGeoLoc value.

            This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-serviceprofile-lorawanserviceprofile.html#cfn-iotwireless-serviceprofile-lorawanserviceprofile-nwkgeoloc
            '''
            result = self._values.get("nwk_geo_loc")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def pr_allowed(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The PRAllowed value that describes whether passive roaming is allowed.

            This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-serviceprofile-lorawanserviceprofile.html#cfn-iotwireless-serviceprofile-lorawanserviceprofile-prallowed
            '''
            result = self._values.get("pr_allowed")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def ra_allowed(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The RAAllowed value that describes whether roaming activation is allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-serviceprofile-lorawanserviceprofile.html#cfn-iotwireless-serviceprofile-lorawanserviceprofile-raallowed
            '''
            result = self._values.get("ra_allowed")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def report_dev_status_battery(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The ReportDevStatusBattery value.

            This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-serviceprofile-lorawanserviceprofile.html#cfn-iotwireless-serviceprofile-lorawanserviceprofile-reportdevstatusbattery
            '''
            result = self._values.get("report_dev_status_battery")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def report_dev_status_margin(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The ReportDevStatusMargin value.

            This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-serviceprofile-lorawanserviceprofile.html#cfn-iotwireless-serviceprofile-lorawanserviceprofile-reportdevstatusmargin
            '''
            result = self._values.get("report_dev_status_margin")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def target_per(self) -> typing.Optional[jsii.Number]:
            '''The TargetPer value.

            This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-serviceprofile-lorawanserviceprofile.html#cfn-iotwireless-serviceprofile-lorawanserviceprofile-targetper
            '''
            result = self._values.get("target_per")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def ul_bucket_size(self) -> typing.Optional[jsii.Number]:
            '''The UlBucketSize value.

            This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-serviceprofile-lorawanserviceprofile.html#cfn-iotwireless-serviceprofile-lorawanserviceprofile-ulbucketsize
            '''
            result = self._values.get("ul_bucket_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def ul_rate(self) -> typing.Optional[jsii.Number]:
            '''The ULRate value.

            This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-serviceprofile-lorawanserviceprofile.html#cfn-iotwireless-serviceprofile-lorawanserviceprofile-ulrate
            '''
            result = self._values.get("ul_rate")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def ul_rate_policy(self) -> typing.Optional[builtins.str]:
            '''The ULRatePolicy value.

            This property is ``ReadOnly`` and can't be inputted for create. It's returned with ``Fn::GetAtt``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-serviceprofile-lorawanserviceprofile.html#cfn-iotwireless-serviceprofile-lorawanserviceprofile-ulratepolicy
            '''
            result = self._values.get("ul_rate_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoRaWANServiceProfileProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnTaskDefinitionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_create_tasks": "autoCreateTasks",
        "lo_ra_wan_update_gateway_task_entry": "loRaWanUpdateGatewayTaskEntry",
        "name": "name",
        "tags": "tags",
        "task_definition_type": "taskDefinitionType",
        "update": "update",
    },
)
class CfnTaskDefinitionMixinProps:
    def __init__(
        self,
        *,
        auto_create_tasks: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        lo_ra_wan_update_gateway_task_entry: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskDefinitionPropsMixin.LoRaWANUpdateGatewayTaskEntryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        task_definition_type: typing.Optional[builtins.str] = None,
        update: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskDefinitionPropsMixin.UpdateWirelessGatewayTaskCreateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnTaskDefinitionPropsMixin.

        :param auto_create_tasks: Whether to automatically create tasks using this task definition for all gateways with the specified current version. If ``false`` , the task must be created by calling ``CreateWirelessGatewayTask`` .
        :param lo_ra_wan_update_gateway_task_entry: LoRaWANUpdateGatewayTaskEntry object.
        :param name: The name of the new resource.
        :param tags: The tags are an array of key-value pairs to attach to the specified resource. Tags can have a minimum of 0 and a maximum of 50 items.
        :param task_definition_type: A filter to list only the wireless gateway task definitions that use this task definition type.
        :param update: Information about the gateways to update.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-taskdefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
            
            cfn_task_definition_mixin_props = iotwireless_mixins.CfnTaskDefinitionMixinProps(
                auto_create_tasks=False,
                lo_ra_wan_update_gateway_task_entry=iotwireless_mixins.CfnTaskDefinitionPropsMixin.LoRaWANUpdateGatewayTaskEntryProperty(
                    current_version=iotwireless_mixins.CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty(
                        model="model",
                        package_version="packageVersion",
                        station="station"
                    ),
                    update_version=iotwireless_mixins.CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty(
                        model="model",
                        package_version="packageVersion",
                        station="station"
                    )
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                task_definition_type="taskDefinitionType",
                update=iotwireless_mixins.CfnTaskDefinitionPropsMixin.UpdateWirelessGatewayTaskCreateProperty(
                    lo_ra_wan=iotwireless_mixins.CfnTaskDefinitionPropsMixin.LoRaWANUpdateGatewayTaskCreateProperty(
                        current_version=iotwireless_mixins.CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty(
                            model="model",
                            package_version="packageVersion",
                            station="station"
                        ),
                        sig_key_crc=123,
                        update_signature="updateSignature",
                        update_version=iotwireless_mixins.CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty(
                            model="model",
                            package_version="packageVersion",
                            station="station"
                        )
                    ),
                    update_data_role="updateDataRole",
                    update_data_source="updateDataSource"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b7210cf74c4dcb3006320fbc5f554fefdef6f36dd18e741fa6072a2c0e7d572)
            check_type(argname="argument auto_create_tasks", value=auto_create_tasks, expected_type=type_hints["auto_create_tasks"])
            check_type(argname="argument lo_ra_wan_update_gateway_task_entry", value=lo_ra_wan_update_gateway_task_entry, expected_type=type_hints["lo_ra_wan_update_gateway_task_entry"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument task_definition_type", value=task_definition_type, expected_type=type_hints["task_definition_type"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_create_tasks is not None:
            self._values["auto_create_tasks"] = auto_create_tasks
        if lo_ra_wan_update_gateway_task_entry is not None:
            self._values["lo_ra_wan_update_gateway_task_entry"] = lo_ra_wan_update_gateway_task_entry
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if task_definition_type is not None:
            self._values["task_definition_type"] = task_definition_type
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def auto_create_tasks(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether to automatically create tasks using this task definition for all gateways with the specified current version.

        If ``false`` , the task must be created by calling ``CreateWirelessGatewayTask`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-taskdefinition.html#cfn-iotwireless-taskdefinition-autocreatetasks
        '''
        result = self._values.get("auto_create_tasks")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def lo_ra_wan_update_gateway_task_entry(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskDefinitionPropsMixin.LoRaWANUpdateGatewayTaskEntryProperty"]]:
        '''LoRaWANUpdateGatewayTaskEntry object.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-taskdefinition.html#cfn-iotwireless-taskdefinition-lorawanupdategatewaytaskentry
        '''
        result = self._values.get("lo_ra_wan_update_gateway_task_entry")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskDefinitionPropsMixin.LoRaWANUpdateGatewayTaskEntryProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the new resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-taskdefinition.html#cfn-iotwireless-taskdefinition-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags are an array of key-value pairs to attach to the specified resource.

        Tags can have a minimum of 0 and a maximum of 50 items.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-taskdefinition.html#cfn-iotwireless-taskdefinition-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def task_definition_type(self) -> typing.Optional[builtins.str]:
        '''A filter to list only the wireless gateway task definitions that use this task definition type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-taskdefinition.html#cfn-iotwireless-taskdefinition-taskdefinitiontype
        '''
        result = self._values.get("task_definition_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskDefinitionPropsMixin.UpdateWirelessGatewayTaskCreateProperty"]]:
        '''Information about the gateways to update.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-taskdefinition.html#cfn-iotwireless-taskdefinition-update
        '''
        result = self._values.get("update")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskDefinitionPropsMixin.UpdateWirelessGatewayTaskCreateProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTaskDefinitionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTaskDefinitionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnTaskDefinitionPropsMixin",
):
    '''Creates a gateway task definition.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-taskdefinition.html
    :cloudformationResource: AWS::IoTWireless::TaskDefinition
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
        
        cfn_task_definition_props_mixin = iotwireless_mixins.CfnTaskDefinitionPropsMixin(iotwireless_mixins.CfnTaskDefinitionMixinProps(
            auto_create_tasks=False,
            lo_ra_wan_update_gateway_task_entry=iotwireless_mixins.CfnTaskDefinitionPropsMixin.LoRaWANUpdateGatewayTaskEntryProperty(
                current_version=iotwireless_mixins.CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty(
                    model="model",
                    package_version="packageVersion",
                    station="station"
                ),
                update_version=iotwireless_mixins.CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty(
                    model="model",
                    package_version="packageVersion",
                    station="station"
                )
            ),
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            task_definition_type="taskDefinitionType",
            update=iotwireless_mixins.CfnTaskDefinitionPropsMixin.UpdateWirelessGatewayTaskCreateProperty(
                lo_ra_wan=iotwireless_mixins.CfnTaskDefinitionPropsMixin.LoRaWANUpdateGatewayTaskCreateProperty(
                    current_version=iotwireless_mixins.CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty(
                        model="model",
                        package_version="packageVersion",
                        station="station"
                    ),
                    sig_key_crc=123,
                    update_signature="updateSignature",
                    update_version=iotwireless_mixins.CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty(
                        model="model",
                        package_version="packageVersion",
                        station="station"
                    )
                ),
                update_data_role="updateDataRole",
                update_data_source="updateDataSource"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTaskDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTWireless::TaskDefinition``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eb3ca73801a401f0a64d7e983404b744b3bfabc99e4e174a6d85a198d2c5a41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df2b5d03cbc26c72fb65618a8caad500ee7cb2ac959a83255943e9bdc4db0087)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba679495279749913337573b3a258be43751129aaeb7f53224a26bfda477b5fb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTaskDefinitionMixinProps:
        return typing.cast(CfnTaskDefinitionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "model": "model",
            "package_version": "packageVersion",
            "station": "station",
        },
    )
    class LoRaWANGatewayVersionProperty:
        def __init__(
            self,
            *,
            model: typing.Optional[builtins.str] = None,
            package_version: typing.Optional[builtins.str] = None,
            station: typing.Optional[builtins.str] = None,
        ) -> None:
            '''LoRaWANGatewayVersion object.

            :param model: The model number of the wireless gateway.
            :param package_version: The version of the wireless gateway firmware.
            :param station: The basic station version of the wireless gateway.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-taskdefinition-lorawangatewayversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
                
                lo_ra_wANGateway_version_property = iotwireless_mixins.CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty(
                    model="model",
                    package_version="packageVersion",
                    station="station"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__316e580b818f511331a851e6adff9fa480c6a15f445a08ff71f572754293b513)
                check_type(argname="argument model", value=model, expected_type=type_hints["model"])
                check_type(argname="argument package_version", value=package_version, expected_type=type_hints["package_version"])
                check_type(argname="argument station", value=station, expected_type=type_hints["station"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if model is not None:
                self._values["model"] = model
            if package_version is not None:
                self._values["package_version"] = package_version
            if station is not None:
                self._values["station"] = station

        @builtins.property
        def model(self) -> typing.Optional[builtins.str]:
            '''The model number of the wireless gateway.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-taskdefinition-lorawangatewayversion.html#cfn-iotwireless-taskdefinition-lorawangatewayversion-model
            '''
            result = self._values.get("model")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def package_version(self) -> typing.Optional[builtins.str]:
            '''The version of the wireless gateway firmware.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-taskdefinition-lorawangatewayversion.html#cfn-iotwireless-taskdefinition-lorawangatewayversion-packageversion
            '''
            result = self._values.get("package_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def station(self) -> typing.Optional[builtins.str]:
            '''The basic station version of the wireless gateway.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-taskdefinition-lorawangatewayversion.html#cfn-iotwireless-taskdefinition-lorawangatewayversion-station
            '''
            result = self._values.get("station")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoRaWANGatewayVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnTaskDefinitionPropsMixin.LoRaWANUpdateGatewayTaskCreateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "current_version": "currentVersion",
            "sig_key_crc": "sigKeyCrc",
            "update_signature": "updateSignature",
            "update_version": "updateVersion",
        },
    )
    class LoRaWANUpdateGatewayTaskCreateProperty:
        def __init__(
            self,
            *,
            current_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sig_key_crc: typing.Optional[jsii.Number] = None,
            update_signature: typing.Optional[builtins.str] = None,
            update_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The signature used to verify the update firmware.

            :param current_version: The version of the gateways that should receive the update.
            :param sig_key_crc: The CRC of the signature private key to check.
            :param update_signature: The signature used to verify the update firmware.
            :param update_version: The firmware version to update the gateway to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-taskdefinition-lorawanupdategatewaytaskcreate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
                
                lo_ra_wANUpdate_gateway_task_create_property = iotwireless_mixins.CfnTaskDefinitionPropsMixin.LoRaWANUpdateGatewayTaskCreateProperty(
                    current_version=iotwireless_mixins.CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty(
                        model="model",
                        package_version="packageVersion",
                        station="station"
                    ),
                    sig_key_crc=123,
                    update_signature="updateSignature",
                    update_version=iotwireless_mixins.CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty(
                        model="model",
                        package_version="packageVersion",
                        station="station"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1b97f06c27547540bdd28656e1af4db6485cc3634712393d48efe3fd63ae5c9c)
                check_type(argname="argument current_version", value=current_version, expected_type=type_hints["current_version"])
                check_type(argname="argument sig_key_crc", value=sig_key_crc, expected_type=type_hints["sig_key_crc"])
                check_type(argname="argument update_signature", value=update_signature, expected_type=type_hints["update_signature"])
                check_type(argname="argument update_version", value=update_version, expected_type=type_hints["update_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if current_version is not None:
                self._values["current_version"] = current_version
            if sig_key_crc is not None:
                self._values["sig_key_crc"] = sig_key_crc
            if update_signature is not None:
                self._values["update_signature"] = update_signature
            if update_version is not None:
                self._values["update_version"] = update_version

        @builtins.property
        def current_version(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty"]]:
            '''The version of the gateways that should receive the update.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-taskdefinition-lorawanupdategatewaytaskcreate.html#cfn-iotwireless-taskdefinition-lorawanupdategatewaytaskcreate-currentversion
            '''
            result = self._values.get("current_version")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty"]], result)

        @builtins.property
        def sig_key_crc(self) -> typing.Optional[jsii.Number]:
            '''The CRC of the signature private key to check.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-taskdefinition-lorawanupdategatewaytaskcreate.html#cfn-iotwireless-taskdefinition-lorawanupdategatewaytaskcreate-sigkeycrc
            '''
            result = self._values.get("sig_key_crc")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def update_signature(self) -> typing.Optional[builtins.str]:
            '''The signature used to verify the update firmware.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-taskdefinition-lorawanupdategatewaytaskcreate.html#cfn-iotwireless-taskdefinition-lorawanupdategatewaytaskcreate-updatesignature
            '''
            result = self._values.get("update_signature")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def update_version(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty"]]:
            '''The firmware version to update the gateway to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-taskdefinition-lorawanupdategatewaytaskcreate.html#cfn-iotwireless-taskdefinition-lorawanupdategatewaytaskcreate-updateversion
            '''
            result = self._values.get("update_version")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoRaWANUpdateGatewayTaskCreateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnTaskDefinitionPropsMixin.LoRaWANUpdateGatewayTaskEntryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "current_version": "currentVersion",
            "update_version": "updateVersion",
        },
    )
    class LoRaWANUpdateGatewayTaskEntryProperty:
        def __init__(
            self,
            *,
            current_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            update_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''LoRaWANUpdateGatewayTaskEntry object.

            :param current_version: The version of the gateways that should receive the update.
            :param update_version: The firmware version to update the gateway to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-taskdefinition-lorawanupdategatewaytaskentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
                
                lo_ra_wANUpdate_gateway_task_entry_property = iotwireless_mixins.CfnTaskDefinitionPropsMixin.LoRaWANUpdateGatewayTaskEntryProperty(
                    current_version=iotwireless_mixins.CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty(
                        model="model",
                        package_version="packageVersion",
                        station="station"
                    ),
                    update_version=iotwireless_mixins.CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty(
                        model="model",
                        package_version="packageVersion",
                        station="station"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3c6c9b8b705b0f8704f7b0cc742eeb4f05416a178f7ec15549b681f022973ac5)
                check_type(argname="argument current_version", value=current_version, expected_type=type_hints["current_version"])
                check_type(argname="argument update_version", value=update_version, expected_type=type_hints["update_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if current_version is not None:
                self._values["current_version"] = current_version
            if update_version is not None:
                self._values["update_version"] = update_version

        @builtins.property
        def current_version(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty"]]:
            '''The version of the gateways that should receive the update.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-taskdefinition-lorawanupdategatewaytaskentry.html#cfn-iotwireless-taskdefinition-lorawanupdategatewaytaskentry-currentversion
            '''
            result = self._values.get("current_version")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty"]], result)

        @builtins.property
        def update_version(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty"]]:
            '''The firmware version to update the gateway to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-taskdefinition-lorawanupdategatewaytaskentry.html#cfn-iotwireless-taskdefinition-lorawanupdategatewaytaskentry-updateversion
            '''
            result = self._values.get("update_version")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoRaWANUpdateGatewayTaskEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnTaskDefinitionPropsMixin.UpdateWirelessGatewayTaskCreateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lo_ra_wan": "loRaWan",
            "update_data_role": "updateDataRole",
            "update_data_source": "updateDataSource",
        },
    )
    class UpdateWirelessGatewayTaskCreateProperty:
        def __init__(
            self,
            *,
            lo_ra_wan: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskDefinitionPropsMixin.LoRaWANUpdateGatewayTaskCreateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            update_data_role: typing.Optional[builtins.str] = None,
            update_data_source: typing.Optional[builtins.str] = None,
        ) -> None:
            '''UpdateWirelessGatewayTaskCreate object.

            :param lo_ra_wan: The properties that relate to the LoRaWAN wireless gateway.
            :param update_data_role: The IAM role used to read data from the S3 bucket.
            :param update_data_source: The link to the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-taskdefinition-updatewirelessgatewaytaskcreate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
                
                update_wireless_gateway_task_create_property = iotwireless_mixins.CfnTaskDefinitionPropsMixin.UpdateWirelessGatewayTaskCreateProperty(
                    lo_ra_wan=iotwireless_mixins.CfnTaskDefinitionPropsMixin.LoRaWANUpdateGatewayTaskCreateProperty(
                        current_version=iotwireless_mixins.CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty(
                            model="model",
                            package_version="packageVersion",
                            station="station"
                        ),
                        sig_key_crc=123,
                        update_signature="updateSignature",
                        update_version=iotwireless_mixins.CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty(
                            model="model",
                            package_version="packageVersion",
                            station="station"
                        )
                    ),
                    update_data_role="updateDataRole",
                    update_data_source="updateDataSource"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b31d70c750269101b29e37637bc4bb006aaec63f4cc8f5effdb6fcf47b74b9c7)
                check_type(argname="argument lo_ra_wan", value=lo_ra_wan, expected_type=type_hints["lo_ra_wan"])
                check_type(argname="argument update_data_role", value=update_data_role, expected_type=type_hints["update_data_role"])
                check_type(argname="argument update_data_source", value=update_data_source, expected_type=type_hints["update_data_source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lo_ra_wan is not None:
                self._values["lo_ra_wan"] = lo_ra_wan
            if update_data_role is not None:
                self._values["update_data_role"] = update_data_role
            if update_data_source is not None:
                self._values["update_data_source"] = update_data_source

        @builtins.property
        def lo_ra_wan(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskDefinitionPropsMixin.LoRaWANUpdateGatewayTaskCreateProperty"]]:
            '''The properties that relate to the LoRaWAN wireless gateway.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-taskdefinition-updatewirelessgatewaytaskcreate.html#cfn-iotwireless-taskdefinition-updatewirelessgatewaytaskcreate-lorawan
            '''
            result = self._values.get("lo_ra_wan")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskDefinitionPropsMixin.LoRaWANUpdateGatewayTaskCreateProperty"]], result)

        @builtins.property
        def update_data_role(self) -> typing.Optional[builtins.str]:
            '''The IAM role used to read data from the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-taskdefinition-updatewirelessgatewaytaskcreate.html#cfn-iotwireless-taskdefinition-updatewirelessgatewaytaskcreate-updatedatarole
            '''
            result = self._values.get("update_data_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def update_data_source(self) -> typing.Optional[builtins.str]:
            '''The link to the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-taskdefinition-updatewirelessgatewaytaskcreate.html#cfn-iotwireless-taskdefinition-updatewirelessgatewaytaskcreate-updatedatasource
            '''
            result = self._values.get("update_data_source")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UpdateWirelessGatewayTaskCreateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnWirelessDeviceImportTaskMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination_name": "destinationName",
        "sidewalk": "sidewalk",
        "tags": "tags",
    },
)
class CfnWirelessDeviceImportTaskMixinProps:
    def __init__(
        self,
        *,
        destination_name: typing.Optional[builtins.str] = None,
        sidewalk: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWirelessDeviceImportTaskPropsMixin.SidewalkProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnWirelessDeviceImportTaskPropsMixin.

        :param destination_name: The name of the destination that describes the IoT rule to route messages from the Sidewalk devices in the import task to other applications.
        :param sidewalk: The Sidewalk-related information of the wireless device import task.
        :param tags: Adds to or modifies the tags of the given resource. Tags are metadata that you can use to manage a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessdeviceimporttask.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
            
            cfn_wireless_device_import_task_mixin_props = iotwireless_mixins.CfnWirelessDeviceImportTaskMixinProps(
                destination_name="destinationName",
                sidewalk=iotwireless_mixins.CfnWirelessDeviceImportTaskPropsMixin.SidewalkProperty(
                    device_creation_file="deviceCreationFile",
                    device_creation_file_list=["deviceCreationFileList"],
                    role="role",
                    sidewalk_manufacturing_sn="sidewalkManufacturingSn"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1750c9cea1260b6e08956340b513f22cc2f2170a1de0072ab314527f3412942)
            check_type(argname="argument destination_name", value=destination_name, expected_type=type_hints["destination_name"])
            check_type(argname="argument sidewalk", value=sidewalk, expected_type=type_hints["sidewalk"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination_name is not None:
            self._values["destination_name"] = destination_name
        if sidewalk is not None:
            self._values["sidewalk"] = sidewalk
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def destination_name(self) -> typing.Optional[builtins.str]:
        '''The name of the destination that describes the IoT rule to route messages from the Sidewalk devices in the import task to other applications.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessdeviceimporttask.html#cfn-iotwireless-wirelessdeviceimporttask-destinationname
        '''
        result = self._values.get("destination_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sidewalk(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWirelessDeviceImportTaskPropsMixin.SidewalkProperty"]]:
        '''The Sidewalk-related information of the wireless device import task.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessdeviceimporttask.html#cfn-iotwireless-wirelessdeviceimporttask-sidewalk
        '''
        result = self._values.get("sidewalk")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWirelessDeviceImportTaskPropsMixin.SidewalkProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Adds to or modifies the tags of the given resource.

        Tags are metadata that you can use to manage a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessdeviceimporttask.html#cfn-iotwireless-wirelessdeviceimporttask-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWirelessDeviceImportTaskMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWirelessDeviceImportTaskPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnWirelessDeviceImportTaskPropsMixin",
):
    '''Information about an import task for wireless devices.

    When creating the resource, either create a single wireless device import task using the Sidewalk manufacturing serial number (SMSN) of the wireless device, or create an import task for multiple devices by specifying both the ``DeviceCreationFile`` and the ``Role`` .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessdeviceimporttask.html
    :cloudformationResource: AWS::IoTWireless::WirelessDeviceImportTask
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
        
        cfn_wireless_device_import_task_props_mixin = iotwireless_mixins.CfnWirelessDeviceImportTaskPropsMixin(iotwireless_mixins.CfnWirelessDeviceImportTaskMixinProps(
            destination_name="destinationName",
            sidewalk=iotwireless_mixins.CfnWirelessDeviceImportTaskPropsMixin.SidewalkProperty(
                device_creation_file="deviceCreationFile",
                device_creation_file_list=["deviceCreationFileList"],
                role="role",
                sidewalk_manufacturing_sn="sidewalkManufacturingSn"
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
        props: typing.Union[CfnWirelessDeviceImportTaskMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTWireless::WirelessDeviceImportTask``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15694f9b42e5a2179b3fbc7c77d810945b3844fd13be4e7fbc7227366609a0aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a0b6e5e25090a94990c58dfbd7984785ca6db9787b7d4bcc7470597ca45dfde)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b68571f68caaa7f577314855f4d1ea3a13e38be4c3a2051432ff4f1e5610d6d3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWirelessDeviceImportTaskMixinProps:
        return typing.cast(CfnWirelessDeviceImportTaskMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnWirelessDeviceImportTaskPropsMixin.SidewalkProperty",
        jsii_struct_bases=[],
        name_mapping={
            "device_creation_file": "deviceCreationFile",
            "device_creation_file_list": "deviceCreationFileList",
            "role": "role",
            "sidewalk_manufacturing_sn": "sidewalkManufacturingSn",
        },
    )
    class SidewalkProperty:
        def __init__(
            self,
            *,
            device_creation_file: typing.Optional[builtins.str] = None,
            device_creation_file_list: typing.Optional[typing.Sequence[builtins.str]] = None,
            role: typing.Optional[builtins.str] = None,
            sidewalk_manufacturing_sn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Sidewalk-related information about a wireless device import task.

            :param device_creation_file: The CSV file contained in an S3 bucket that's used for adding devices to an import task.
            :param device_creation_file_list: List of Sidewalk devices that are added to the import task.
            :param role: The IAM role that allows to access the CSV file in the S3 bucket.
            :param sidewalk_manufacturing_sn: The Sidewalk manufacturing serial number (SMSN) of the Sidewalk device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdeviceimporttask-sidewalk.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
                
                sidewalk_property = iotwireless_mixins.CfnWirelessDeviceImportTaskPropsMixin.SidewalkProperty(
                    device_creation_file="deviceCreationFile",
                    device_creation_file_list=["deviceCreationFileList"],
                    role="role",
                    sidewalk_manufacturing_sn="sidewalkManufacturingSn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9694f1d8297545c8535e87d0ea209271652e21c14db0e83738f9fb14410fbb9a)
                check_type(argname="argument device_creation_file", value=device_creation_file, expected_type=type_hints["device_creation_file"])
                check_type(argname="argument device_creation_file_list", value=device_creation_file_list, expected_type=type_hints["device_creation_file_list"])
                check_type(argname="argument role", value=role, expected_type=type_hints["role"])
                check_type(argname="argument sidewalk_manufacturing_sn", value=sidewalk_manufacturing_sn, expected_type=type_hints["sidewalk_manufacturing_sn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if device_creation_file is not None:
                self._values["device_creation_file"] = device_creation_file
            if device_creation_file_list is not None:
                self._values["device_creation_file_list"] = device_creation_file_list
            if role is not None:
                self._values["role"] = role
            if sidewalk_manufacturing_sn is not None:
                self._values["sidewalk_manufacturing_sn"] = sidewalk_manufacturing_sn

        @builtins.property
        def device_creation_file(self) -> typing.Optional[builtins.str]:
            '''The CSV file contained in an S3 bucket that's used for adding devices to an import task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdeviceimporttask-sidewalk.html#cfn-iotwireless-wirelessdeviceimporttask-sidewalk-devicecreationfile
            '''
            result = self._values.get("device_creation_file")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def device_creation_file_list(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''List of Sidewalk devices that are added to the import task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdeviceimporttask-sidewalk.html#cfn-iotwireless-wirelessdeviceimporttask-sidewalk-devicecreationfilelist
            '''
            result = self._values.get("device_creation_file_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def role(self) -> typing.Optional[builtins.str]:
            '''The IAM role that allows  to access the CSV file in the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdeviceimporttask-sidewalk.html#cfn-iotwireless-wirelessdeviceimporttask-sidewalk-role
            '''
            result = self._values.get("role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sidewalk_manufacturing_sn(self) -> typing.Optional[builtins.str]:
            '''The Sidewalk manufacturing serial number (SMSN) of the Sidewalk device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdeviceimporttask-sidewalk.html#cfn-iotwireless-wirelessdeviceimporttask-sidewalk-sidewalkmanufacturingsn
            '''
            result = self._values.get("sidewalk_manufacturing_sn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SidewalkProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnWirelessDeviceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "destination_name": "destinationName",
        "last_uplink_received_at": "lastUplinkReceivedAt",
        "lo_ra_wan": "loRaWan",
        "name": "name",
        "positioning": "positioning",
        "tags": "tags",
        "thing_arn": "thingArn",
        "type": "type",
    },
)
class CfnWirelessDeviceMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        destination_name: typing.Optional[builtins.str] = None,
        last_uplink_received_at: typing.Optional[builtins.str] = None,
        lo_ra_wan: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWirelessDevicePropsMixin.LoRaWANDeviceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        positioning: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        thing_arn: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnWirelessDevicePropsMixin.

        :param description: The description of the new resource. Maximum length is 2048.
        :param destination_name: The name of the destination to assign to the new wireless device. Can have only have alphanumeric, - (hyphen) and _ (underscore) characters and it can't have any spaces.
        :param last_uplink_received_at: The date and time when the most recent uplink was received.
        :param lo_ra_wan: The device configuration information to use to create the wireless device. Must be at least one of OtaaV10x, OtaaV11, AbpV11, or AbpV10x.
        :param name: The name of the new resource.
        :param positioning: FPort values for the GNSS, Stream, and ClockSync functions of the positioning information.
        :param tags: The tags are an array of key-value pairs to attach to the specified resource. Tags can have a minimum of 0 and a maximum of 50 items.
        :param thing_arn: The ARN of the thing to associate with the wireless device.
        :param type: The wireless device type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessdevice.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
            
            cfn_wireless_device_mixin_props = iotwireless_mixins.CfnWirelessDeviceMixinProps(
                description="description",
                destination_name="destinationName",
                last_uplink_received_at="lastUplinkReceivedAt",
                lo_ra_wan=iotwireless_mixins.CfnWirelessDevicePropsMixin.LoRaWANDeviceProperty(
                    abp_v10_x=iotwireless_mixins.CfnWirelessDevicePropsMixin.AbpV10xProperty(
                        dev_addr="devAddr",
                        session_keys=iotwireless_mixins.CfnWirelessDevicePropsMixin.SessionKeysAbpV10xProperty(
                            app_sKey="appSKey",
                            nwk_sKey="nwkSKey"
                        )
                    ),
                    abp_v11=iotwireless_mixins.CfnWirelessDevicePropsMixin.AbpV11Property(
                        dev_addr="devAddr",
                        session_keys=iotwireless_mixins.CfnWirelessDevicePropsMixin.SessionKeysAbpV11Property(
                            app_sKey="appSKey",
                            f_nwk_sInt_key="fNwkSIntKey",
                            nwk_sEnc_key="nwkSEncKey",
                            s_nwk_sInt_key="sNwkSIntKey"
                        )
                    ),
                    dev_eui="devEui",
                    device_profile_id="deviceProfileId",
                    f_ports=iotwireless_mixins.CfnWirelessDevicePropsMixin.FPortsProperty(
                        applications=[iotwireless_mixins.CfnWirelessDevicePropsMixin.ApplicationProperty(
                            destination_name="destinationName",
                            f_port=123,
                            type="type"
                        )]
                    ),
                    otaa_v10_x=iotwireless_mixins.CfnWirelessDevicePropsMixin.OtaaV10xProperty(
                        app_eui="appEui",
                        app_key="appKey"
                    ),
                    otaa_v11=iotwireless_mixins.CfnWirelessDevicePropsMixin.OtaaV11Property(
                        app_key="appKey",
                        join_eui="joinEui",
                        nwk_key="nwkKey"
                    ),
                    service_profile_id="serviceProfileId"
                ),
                name="name",
                positioning="positioning",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                thing_arn="thingArn",
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__097fa1d41ad7d479104476be749b92523f543a182900d1843600a5b16e965ef0)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument destination_name", value=destination_name, expected_type=type_hints["destination_name"])
            check_type(argname="argument last_uplink_received_at", value=last_uplink_received_at, expected_type=type_hints["last_uplink_received_at"])
            check_type(argname="argument lo_ra_wan", value=lo_ra_wan, expected_type=type_hints["lo_ra_wan"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument positioning", value=positioning, expected_type=type_hints["positioning"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument thing_arn", value=thing_arn, expected_type=type_hints["thing_arn"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if destination_name is not None:
            self._values["destination_name"] = destination_name
        if last_uplink_received_at is not None:
            self._values["last_uplink_received_at"] = last_uplink_received_at
        if lo_ra_wan is not None:
            self._values["lo_ra_wan"] = lo_ra_wan
        if name is not None:
            self._values["name"] = name
        if positioning is not None:
            self._values["positioning"] = positioning
        if tags is not None:
            self._values["tags"] = tags
        if thing_arn is not None:
            self._values["thing_arn"] = thing_arn
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the new resource.

        Maximum length is 2048.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessdevice.html#cfn-iotwireless-wirelessdevice-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_name(self) -> typing.Optional[builtins.str]:
        '''The name of the destination to assign to the new wireless device.

        Can have only have alphanumeric, - (hyphen) and _ (underscore) characters and it can't have any spaces.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessdevice.html#cfn-iotwireless-wirelessdevice-destinationname
        '''
        result = self._values.get("destination_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def last_uplink_received_at(self) -> typing.Optional[builtins.str]:
        '''The date and time when the most recent uplink was received.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessdevice.html#cfn-iotwireless-wirelessdevice-lastuplinkreceivedat
        '''
        result = self._values.get("last_uplink_received_at")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lo_ra_wan(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWirelessDevicePropsMixin.LoRaWANDeviceProperty"]]:
        '''The device configuration information to use to create the wireless device.

        Must be at least one of OtaaV10x, OtaaV11, AbpV11, or AbpV10x.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessdevice.html#cfn-iotwireless-wirelessdevice-lorawan
        '''
        result = self._values.get("lo_ra_wan")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWirelessDevicePropsMixin.LoRaWANDeviceProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the new resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessdevice.html#cfn-iotwireless-wirelessdevice-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def positioning(self) -> typing.Optional[builtins.str]:
        '''FPort values for the GNSS, Stream, and ClockSync functions of the positioning information.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessdevice.html#cfn-iotwireless-wirelessdevice-positioning
        '''
        result = self._values.get("positioning")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags are an array of key-value pairs to attach to the specified resource.

        Tags can have a minimum of 0 and a maximum of 50 items.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessdevice.html#cfn-iotwireless-wirelessdevice-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def thing_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the thing to associate with the wireless device.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessdevice.html#cfn-iotwireless-wirelessdevice-thingarn
        '''
        result = self._values.get("thing_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The wireless device type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessdevice.html#cfn-iotwireless-wirelessdevice-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWirelessDeviceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWirelessDevicePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnWirelessDevicePropsMixin",
):
    '''Provisions a wireless device.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessdevice.html
    :cloudformationResource: AWS::IoTWireless::WirelessDevice
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
        
        cfn_wireless_device_props_mixin = iotwireless_mixins.CfnWirelessDevicePropsMixin(iotwireless_mixins.CfnWirelessDeviceMixinProps(
            description="description",
            destination_name="destinationName",
            last_uplink_received_at="lastUplinkReceivedAt",
            lo_ra_wan=iotwireless_mixins.CfnWirelessDevicePropsMixin.LoRaWANDeviceProperty(
                abp_v10_x=iotwireless_mixins.CfnWirelessDevicePropsMixin.AbpV10xProperty(
                    dev_addr="devAddr",
                    session_keys=iotwireless_mixins.CfnWirelessDevicePropsMixin.SessionKeysAbpV10xProperty(
                        app_sKey="appSKey",
                        nwk_sKey="nwkSKey"
                    )
                ),
                abp_v11=iotwireless_mixins.CfnWirelessDevicePropsMixin.AbpV11Property(
                    dev_addr="devAddr",
                    session_keys=iotwireless_mixins.CfnWirelessDevicePropsMixin.SessionKeysAbpV11Property(
                        app_sKey="appSKey",
                        f_nwk_sInt_key="fNwkSIntKey",
                        nwk_sEnc_key="nwkSEncKey",
                        s_nwk_sInt_key="sNwkSIntKey"
                    )
                ),
                dev_eui="devEui",
                device_profile_id="deviceProfileId",
                f_ports=iotwireless_mixins.CfnWirelessDevicePropsMixin.FPortsProperty(
                    applications=[iotwireless_mixins.CfnWirelessDevicePropsMixin.ApplicationProperty(
                        destination_name="destinationName",
                        f_port=123,
                        type="type"
                    )]
                ),
                otaa_v10_x=iotwireless_mixins.CfnWirelessDevicePropsMixin.OtaaV10xProperty(
                    app_eui="appEui",
                    app_key="appKey"
                ),
                otaa_v11=iotwireless_mixins.CfnWirelessDevicePropsMixin.OtaaV11Property(
                    app_key="appKey",
                    join_eui="joinEui",
                    nwk_key="nwkKey"
                ),
                service_profile_id="serviceProfileId"
            ),
            name="name",
            positioning="positioning",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            thing_arn="thingArn",
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnWirelessDeviceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTWireless::WirelessDevice``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e86363c3883ca01e564c81a3db970d4de8b5dcebe8b399c04781b56eccc8579a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a059b7d02f7b77367ae122b48cf8e3e0ed62e5ff1f6038687f48b89be469951)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7f11ca29d77999f8b912280e5075ae093853aad6c6a3d99576b7749583cc76a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWirelessDeviceMixinProps:
        return typing.cast(CfnWirelessDeviceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnWirelessDevicePropsMixin.AbpV10xProperty",
        jsii_struct_bases=[],
        name_mapping={"dev_addr": "devAddr", "session_keys": "sessionKeys"},
    )
    class AbpV10xProperty:
        def __init__(
            self,
            *,
            dev_addr: typing.Optional[builtins.str] = None,
            session_keys: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWirelessDevicePropsMixin.SessionKeysAbpV10xProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''ABP device object for LoRaWAN specification v1.0.x.

            :param dev_addr: The DevAddr value.
            :param session_keys: Session keys for ABP v1.0.x.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-abpv10x.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
                
                abp_v10x_property = iotwireless_mixins.CfnWirelessDevicePropsMixin.AbpV10xProperty(
                    dev_addr="devAddr",
                    session_keys=iotwireless_mixins.CfnWirelessDevicePropsMixin.SessionKeysAbpV10xProperty(
                        app_sKey="appSKey",
                        nwk_sKey="nwkSKey"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f89afbf75d770708f5900afea3af386ebf0fb18f6527f8ae495ddfeb4dcfacb6)
                check_type(argname="argument dev_addr", value=dev_addr, expected_type=type_hints["dev_addr"])
                check_type(argname="argument session_keys", value=session_keys, expected_type=type_hints["session_keys"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dev_addr is not None:
                self._values["dev_addr"] = dev_addr
            if session_keys is not None:
                self._values["session_keys"] = session_keys

        @builtins.property
        def dev_addr(self) -> typing.Optional[builtins.str]:
            '''The DevAddr value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-abpv10x.html#cfn-iotwireless-wirelessdevice-abpv10x-devaddr
            '''
            result = self._values.get("dev_addr")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def session_keys(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWirelessDevicePropsMixin.SessionKeysAbpV10xProperty"]]:
            '''Session keys for ABP v1.0.x.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-abpv10x.html#cfn-iotwireless-wirelessdevice-abpv10x-sessionkeys
            '''
            result = self._values.get("session_keys")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWirelessDevicePropsMixin.SessionKeysAbpV10xProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AbpV10xProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnWirelessDevicePropsMixin.AbpV11Property",
        jsii_struct_bases=[],
        name_mapping={"dev_addr": "devAddr", "session_keys": "sessionKeys"},
    )
    class AbpV11Property:
        def __init__(
            self,
            *,
            dev_addr: typing.Optional[builtins.str] = None,
            session_keys: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWirelessDevicePropsMixin.SessionKeysAbpV11Property", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''ABP device object for create APIs for v1.1.

            :param dev_addr: The DevAddr value.
            :param session_keys: Session keys for ABP v1.1.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-abpv11.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
                
                abp_v11_property = iotwireless_mixins.CfnWirelessDevicePropsMixin.AbpV11Property(
                    dev_addr="devAddr",
                    session_keys=iotwireless_mixins.CfnWirelessDevicePropsMixin.SessionKeysAbpV11Property(
                        app_sKey="appSKey",
                        f_nwk_sInt_key="fNwkSIntKey",
                        nwk_sEnc_key="nwkSEncKey",
                        s_nwk_sInt_key="sNwkSIntKey"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__82a81dfc73e88e30f2097fcfaad35799c0d8b3ee1535b65cefc3613ab2e1f1f7)
                check_type(argname="argument dev_addr", value=dev_addr, expected_type=type_hints["dev_addr"])
                check_type(argname="argument session_keys", value=session_keys, expected_type=type_hints["session_keys"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dev_addr is not None:
                self._values["dev_addr"] = dev_addr
            if session_keys is not None:
                self._values["session_keys"] = session_keys

        @builtins.property
        def dev_addr(self) -> typing.Optional[builtins.str]:
            '''The DevAddr value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-abpv11.html#cfn-iotwireless-wirelessdevice-abpv11-devaddr
            '''
            result = self._values.get("dev_addr")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def session_keys(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWirelessDevicePropsMixin.SessionKeysAbpV11Property"]]:
            '''Session keys for ABP v1.1.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-abpv11.html#cfn-iotwireless-wirelessdevice-abpv11-sessionkeys
            '''
            result = self._values.get("session_keys")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWirelessDevicePropsMixin.SessionKeysAbpV11Property"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AbpV11Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnWirelessDevicePropsMixin.ApplicationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_name": "destinationName",
            "f_port": "fPort",
            "type": "type",
        },
    )
    class ApplicationProperty:
        def __init__(
            self,
            *,
            destination_name: typing.Optional[builtins.str] = None,
            f_port: typing.Optional[jsii.Number] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A list of optional LoRaWAN application information, which can be used for geolocation.

            :param destination_name: The name of the position data destination that describes the IoT rule that processes the device's position data.
            :param f_port: The name of the new destination for the device.
            :param type: Application type, which can be specified to obtain real-time position information of your LoRaWAN device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-application.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
                
                application_property = iotwireless_mixins.CfnWirelessDevicePropsMixin.ApplicationProperty(
                    destination_name="destinationName",
                    f_port=123,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__234ef254febd39ebe8873b2ce5f00d28211e798155a91aff514d3c224033c408)
                check_type(argname="argument destination_name", value=destination_name, expected_type=type_hints["destination_name"])
                check_type(argname="argument f_port", value=f_port, expected_type=type_hints["f_port"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_name is not None:
                self._values["destination_name"] = destination_name
            if f_port is not None:
                self._values["f_port"] = f_port
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def destination_name(self) -> typing.Optional[builtins.str]:
            '''The name of the position data destination that describes the IoT rule that processes the device's position data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-application.html#cfn-iotwireless-wirelessdevice-application-destinationname
            '''
            result = self._values.get("destination_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def f_port(self) -> typing.Optional[jsii.Number]:
            '''The name of the new destination for the device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-application.html#cfn-iotwireless-wirelessdevice-application-fport
            '''
            result = self._values.get("f_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Application type, which can be specified to obtain real-time position information of your LoRaWAN device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-application.html#cfn-iotwireless-wirelessdevice-application-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnWirelessDevicePropsMixin.FPortsProperty",
        jsii_struct_bases=[],
        name_mapping={"applications": "applications"},
    )
    class FPortsProperty:
        def __init__(
            self,
            *,
            applications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWirelessDevicePropsMixin.ApplicationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''List of FPorts assigned for different LoRaWAN application packages to use.

            :param applications: LoRaWAN application configuration, which can be used to perform geolocation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-fports.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
                
                f_ports_property = iotwireless_mixins.CfnWirelessDevicePropsMixin.FPortsProperty(
                    applications=[iotwireless_mixins.CfnWirelessDevicePropsMixin.ApplicationProperty(
                        destination_name="destinationName",
                        f_port=123,
                        type="type"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__61f96813e1fec3489285d993c5bfcc2ced91689c0b55c02160fb33b88a058369)
                check_type(argname="argument applications", value=applications, expected_type=type_hints["applications"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if applications is not None:
                self._values["applications"] = applications

        @builtins.property
        def applications(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWirelessDevicePropsMixin.ApplicationProperty"]]]]:
            '''LoRaWAN application configuration, which can be used to perform geolocation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-fports.html#cfn-iotwireless-wirelessdevice-fports-applications
            '''
            result = self._values.get("applications")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWirelessDevicePropsMixin.ApplicationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FPortsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnWirelessDevicePropsMixin.LoRaWANDeviceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "abp_v10_x": "abpV10X",
            "abp_v11": "abpV11",
            "dev_eui": "devEui",
            "device_profile_id": "deviceProfileId",
            "f_ports": "fPorts",
            "otaa_v10_x": "otaaV10X",
            "otaa_v11": "otaaV11",
            "service_profile_id": "serviceProfileId",
        },
    )
    class LoRaWANDeviceProperty:
        def __init__(
            self,
            *,
            abp_v10_x: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWirelessDevicePropsMixin.AbpV10xProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            abp_v11: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWirelessDevicePropsMixin.AbpV11Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            dev_eui: typing.Optional[builtins.str] = None,
            device_profile_id: typing.Optional[builtins.str] = None,
            f_ports: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWirelessDevicePropsMixin.FPortsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            otaa_v10_x: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWirelessDevicePropsMixin.OtaaV10xProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            otaa_v11: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWirelessDevicePropsMixin.OtaaV11Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            service_profile_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''LoRaWAN object for create functions.

            :param abp_v10_x: ABP device object for LoRaWAN specification v1.0.x.
            :param abp_v11: ABP device object for create APIs for v1.1.
            :param dev_eui: The DevEUI value.
            :param device_profile_id: The ID of the device profile for the new wireless device.
            :param f_ports: List of FPort assigned for different LoRaWAN application packages to use.
            :param otaa_v10_x: OTAA device object for create APIs for v1.0.x.
            :param otaa_v11: OTAA device object for v1.1 for create APIs.
            :param service_profile_id: The ID of the service profile.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-lorawandevice.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
                
                lo_ra_wANDevice_property = iotwireless_mixins.CfnWirelessDevicePropsMixin.LoRaWANDeviceProperty(
                    abp_v10_x=iotwireless_mixins.CfnWirelessDevicePropsMixin.AbpV10xProperty(
                        dev_addr="devAddr",
                        session_keys=iotwireless_mixins.CfnWirelessDevicePropsMixin.SessionKeysAbpV10xProperty(
                            app_sKey="appSKey",
                            nwk_sKey="nwkSKey"
                        )
                    ),
                    abp_v11=iotwireless_mixins.CfnWirelessDevicePropsMixin.AbpV11Property(
                        dev_addr="devAddr",
                        session_keys=iotwireless_mixins.CfnWirelessDevicePropsMixin.SessionKeysAbpV11Property(
                            app_sKey="appSKey",
                            f_nwk_sInt_key="fNwkSIntKey",
                            nwk_sEnc_key="nwkSEncKey",
                            s_nwk_sInt_key="sNwkSIntKey"
                        )
                    ),
                    dev_eui="devEui",
                    device_profile_id="deviceProfileId",
                    f_ports=iotwireless_mixins.CfnWirelessDevicePropsMixin.FPortsProperty(
                        applications=[iotwireless_mixins.CfnWirelessDevicePropsMixin.ApplicationProperty(
                            destination_name="destinationName",
                            f_port=123,
                            type="type"
                        )]
                    ),
                    otaa_v10_x=iotwireless_mixins.CfnWirelessDevicePropsMixin.OtaaV10xProperty(
                        app_eui="appEui",
                        app_key="appKey"
                    ),
                    otaa_v11=iotwireless_mixins.CfnWirelessDevicePropsMixin.OtaaV11Property(
                        app_key="appKey",
                        join_eui="joinEui",
                        nwk_key="nwkKey"
                    ),
                    service_profile_id="serviceProfileId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__91111f227e51c77c519d4db2d046eb4aac2cc7f4e68915aa639beb890bff98cf)
                check_type(argname="argument abp_v10_x", value=abp_v10_x, expected_type=type_hints["abp_v10_x"])
                check_type(argname="argument abp_v11", value=abp_v11, expected_type=type_hints["abp_v11"])
                check_type(argname="argument dev_eui", value=dev_eui, expected_type=type_hints["dev_eui"])
                check_type(argname="argument device_profile_id", value=device_profile_id, expected_type=type_hints["device_profile_id"])
                check_type(argname="argument f_ports", value=f_ports, expected_type=type_hints["f_ports"])
                check_type(argname="argument otaa_v10_x", value=otaa_v10_x, expected_type=type_hints["otaa_v10_x"])
                check_type(argname="argument otaa_v11", value=otaa_v11, expected_type=type_hints["otaa_v11"])
                check_type(argname="argument service_profile_id", value=service_profile_id, expected_type=type_hints["service_profile_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if abp_v10_x is not None:
                self._values["abp_v10_x"] = abp_v10_x
            if abp_v11 is not None:
                self._values["abp_v11"] = abp_v11
            if dev_eui is not None:
                self._values["dev_eui"] = dev_eui
            if device_profile_id is not None:
                self._values["device_profile_id"] = device_profile_id
            if f_ports is not None:
                self._values["f_ports"] = f_ports
            if otaa_v10_x is not None:
                self._values["otaa_v10_x"] = otaa_v10_x
            if otaa_v11 is not None:
                self._values["otaa_v11"] = otaa_v11
            if service_profile_id is not None:
                self._values["service_profile_id"] = service_profile_id

        @builtins.property
        def abp_v10_x(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWirelessDevicePropsMixin.AbpV10xProperty"]]:
            '''ABP device object for LoRaWAN specification v1.0.x.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-lorawandevice.html#cfn-iotwireless-wirelessdevice-lorawandevice-abpv10x
            '''
            result = self._values.get("abp_v10_x")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWirelessDevicePropsMixin.AbpV10xProperty"]], result)

        @builtins.property
        def abp_v11(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWirelessDevicePropsMixin.AbpV11Property"]]:
            '''ABP device object for create APIs for v1.1.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-lorawandevice.html#cfn-iotwireless-wirelessdevice-lorawandevice-abpv11
            '''
            result = self._values.get("abp_v11")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWirelessDevicePropsMixin.AbpV11Property"]], result)

        @builtins.property
        def dev_eui(self) -> typing.Optional[builtins.str]:
            '''The DevEUI value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-lorawandevice.html#cfn-iotwireless-wirelessdevice-lorawandevice-deveui
            '''
            result = self._values.get("dev_eui")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def device_profile_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the device profile for the new wireless device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-lorawandevice.html#cfn-iotwireless-wirelessdevice-lorawandevice-deviceprofileid
            '''
            result = self._values.get("device_profile_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def f_ports(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWirelessDevicePropsMixin.FPortsProperty"]]:
            '''List of FPort assigned for different LoRaWAN application packages to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-lorawandevice.html#cfn-iotwireless-wirelessdevice-lorawandevice-fports
            '''
            result = self._values.get("f_ports")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWirelessDevicePropsMixin.FPortsProperty"]], result)

        @builtins.property
        def otaa_v10_x(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWirelessDevicePropsMixin.OtaaV10xProperty"]]:
            '''OTAA device object for create APIs for v1.0.x.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-lorawandevice.html#cfn-iotwireless-wirelessdevice-lorawandevice-otaav10x
            '''
            result = self._values.get("otaa_v10_x")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWirelessDevicePropsMixin.OtaaV10xProperty"]], result)

        @builtins.property
        def otaa_v11(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWirelessDevicePropsMixin.OtaaV11Property"]]:
            '''OTAA device object for v1.1 for create APIs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-lorawandevice.html#cfn-iotwireless-wirelessdevice-lorawandevice-otaav11
            '''
            result = self._values.get("otaa_v11")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWirelessDevicePropsMixin.OtaaV11Property"]], result)

        @builtins.property
        def service_profile_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the service profile.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-lorawandevice.html#cfn-iotwireless-wirelessdevice-lorawandevice-serviceprofileid
            '''
            result = self._values.get("service_profile_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoRaWANDeviceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnWirelessDevicePropsMixin.OtaaV10xProperty",
        jsii_struct_bases=[],
        name_mapping={"app_eui": "appEui", "app_key": "appKey"},
    )
    class OtaaV10xProperty:
        def __init__(
            self,
            *,
            app_eui: typing.Optional[builtins.str] = None,
            app_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''OTAA device object for v1.0.x.

            :param app_eui: The AppEUI value. You specify this value when using LoRaWAN versions v1.0.2 or v1.0.3.
            :param app_key: The AppKey value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-otaav10x.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
                
                otaa_v10x_property = iotwireless_mixins.CfnWirelessDevicePropsMixin.OtaaV10xProperty(
                    app_eui="appEui",
                    app_key="appKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d6e22baca329e9dbc86d429310ab94a2db9eaa7cc3dc8b1f7256ee00d5bdcef)
                check_type(argname="argument app_eui", value=app_eui, expected_type=type_hints["app_eui"])
                check_type(argname="argument app_key", value=app_key, expected_type=type_hints["app_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if app_eui is not None:
                self._values["app_eui"] = app_eui
            if app_key is not None:
                self._values["app_key"] = app_key

        @builtins.property
        def app_eui(self) -> typing.Optional[builtins.str]:
            '''The AppEUI value.

            You specify this value when using LoRaWAN versions v1.0.2 or v1.0.3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-otaav10x.html#cfn-iotwireless-wirelessdevice-otaav10x-appeui
            '''
            result = self._values.get("app_eui")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def app_key(self) -> typing.Optional[builtins.str]:
            '''The AppKey value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-otaav10x.html#cfn-iotwireless-wirelessdevice-otaav10x-appkey
            '''
            result = self._values.get("app_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OtaaV10xProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnWirelessDevicePropsMixin.OtaaV11Property",
        jsii_struct_bases=[],
        name_mapping={"app_key": "appKey", "join_eui": "joinEui", "nwk_key": "nwkKey"},
    )
    class OtaaV11Property:
        def __init__(
            self,
            *,
            app_key: typing.Optional[builtins.str] = None,
            join_eui: typing.Optional[builtins.str] = None,
            nwk_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''OTAA device object for v1.1 for create APIs.

            :param app_key: The AppKey is a secret key, which you should handle in a similar way as you would an application password. You can protect the AppKey value by storing it in the AWS Secrets Manager and use the `secretsmanager <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html#dynamic-references-secretsmanager>`_ to reference this value.
            :param join_eui: The JoinEUI value.
            :param nwk_key: The NwkKey is a secret key, which you should handle in a similar way as you would an application password. You can protect the NwkKey value by storing it in the AWS Secrets Manager and use the `secretsmanager <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html#dynamic-references-secretsmanager>`_ to reference this value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-otaav11.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
                
                otaa_v11_property = iotwireless_mixins.CfnWirelessDevicePropsMixin.OtaaV11Property(
                    app_key="appKey",
                    join_eui="joinEui",
                    nwk_key="nwkKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b2e5950d8b0615769b2d379faee874a13194a465daf70c331e456170b2ca6d14)
                check_type(argname="argument app_key", value=app_key, expected_type=type_hints["app_key"])
                check_type(argname="argument join_eui", value=join_eui, expected_type=type_hints["join_eui"])
                check_type(argname="argument nwk_key", value=nwk_key, expected_type=type_hints["nwk_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if app_key is not None:
                self._values["app_key"] = app_key
            if join_eui is not None:
                self._values["join_eui"] = join_eui
            if nwk_key is not None:
                self._values["nwk_key"] = nwk_key

        @builtins.property
        def app_key(self) -> typing.Optional[builtins.str]:
            '''The AppKey is a secret key, which you should handle in a similar way as you would an application password.

            You can protect the AppKey value by storing it in the AWS Secrets Manager and use the `secretsmanager <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html#dynamic-references-secretsmanager>`_ to reference this value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-otaav11.html#cfn-iotwireless-wirelessdevice-otaav11-appkey
            '''
            result = self._values.get("app_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def join_eui(self) -> typing.Optional[builtins.str]:
            '''The JoinEUI value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-otaav11.html#cfn-iotwireless-wirelessdevice-otaav11-joineui
            '''
            result = self._values.get("join_eui")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def nwk_key(self) -> typing.Optional[builtins.str]:
            '''The NwkKey is a secret key, which you should handle in a similar way as you would an application password.

            You can protect the NwkKey value by storing it in the AWS Secrets Manager and use the `secretsmanager <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html#dynamic-references-secretsmanager>`_ to reference this value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-otaav11.html#cfn-iotwireless-wirelessdevice-otaav11-nwkkey
            '''
            result = self._values.get("nwk_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OtaaV11Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnWirelessDevicePropsMixin.SessionKeysAbpV10xProperty",
        jsii_struct_bases=[],
        name_mapping={"app_s_key": "appSKey", "nwk_s_key": "nwkSKey"},
    )
    class SessionKeysAbpV10xProperty:
        def __init__(
            self,
            *,
            app_s_key: typing.Optional[builtins.str] = None,
            nwk_s_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Session keys for ABP v1.0.x.

            :param app_s_key: The AppSKey value.
            :param nwk_s_key: The NwkKey value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-sessionkeysabpv10x.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
                
                session_keys_abp_v10x_property = iotwireless_mixins.CfnWirelessDevicePropsMixin.SessionKeysAbpV10xProperty(
                    app_sKey="appSKey",
                    nwk_sKey="nwkSKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cf856b92fb5c981981b278d1408a16bc04321b82145a11c51368d92bc600925d)
                check_type(argname="argument app_s_key", value=app_s_key, expected_type=type_hints["app_s_key"])
                check_type(argname="argument nwk_s_key", value=nwk_s_key, expected_type=type_hints["nwk_s_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if app_s_key is not None:
                self._values["app_s_key"] = app_s_key
            if nwk_s_key is not None:
                self._values["nwk_s_key"] = nwk_s_key

        @builtins.property
        def app_s_key(self) -> typing.Optional[builtins.str]:
            '''The AppSKey value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-sessionkeysabpv10x.html#cfn-iotwireless-wirelessdevice-sessionkeysabpv10x-appskey
            '''
            result = self._values.get("app_s_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def nwk_s_key(self) -> typing.Optional[builtins.str]:
            '''The NwkKey value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-sessionkeysabpv10x.html#cfn-iotwireless-wirelessdevice-sessionkeysabpv10x-nwkskey
            '''
            result = self._values.get("nwk_s_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SessionKeysAbpV10xProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnWirelessDevicePropsMixin.SessionKeysAbpV11Property",
        jsii_struct_bases=[],
        name_mapping={
            "app_s_key": "appSKey",
            "f_nwk_s_int_key": "fNwkSIntKey",
            "nwk_s_enc_key": "nwkSEncKey",
            "s_nwk_s_int_key": "sNwkSIntKey",
        },
    )
    class SessionKeysAbpV11Property:
        def __init__(
            self,
            *,
            app_s_key: typing.Optional[builtins.str] = None,
            f_nwk_s_int_key: typing.Optional[builtins.str] = None,
            nwk_s_enc_key: typing.Optional[builtins.str] = None,
            s_nwk_s_int_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Session keys for ABP v1.1.

            :param app_s_key: The AppSKey is a secret key, which you should handle in a similar way as you would an application password. You can protect the AppSKey value by storing it in the AWS Secrets Manager and use the `secretsmanager <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html#dynamic-references-secretsmanager>`_ to reference this value.
            :param f_nwk_s_int_key: The FNwkSIntKey is a secret key, which you should handle in a similar way as you would an application password. You can protect the FNwkSIntKey value by storing it in the AWS Secrets Manager and use the `secretsmanager <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html#dynamic-references-secretsmanager>`_ to reference this value.
            :param nwk_s_enc_key: The NwkSEncKey is a secret key, which you should handle in a similar way as you would an application password. You can protect the NwkSEncKey value by storing it in the AWS Secrets Manager and use the `secretsmanager <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html#dynamic-references-secretsmanager>`_ to reference this value.
            :param s_nwk_s_int_key: The SNwkSIntKey is a secret key, which you should handle in a similar way as you would an application password. You can protect the SNwkSIntKey value by storing it in the AWS Secrets Manager and use the `secretsmanager <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html#dynamic-references-secretsmanager>`_ to reference this value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-sessionkeysabpv11.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
                
                session_keys_abp_v11_property = iotwireless_mixins.CfnWirelessDevicePropsMixin.SessionKeysAbpV11Property(
                    app_sKey="appSKey",
                    f_nwk_sInt_key="fNwkSIntKey",
                    nwk_sEnc_key="nwkSEncKey",
                    s_nwk_sInt_key="sNwkSIntKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__53ac144c4e920c4c8d7a600ab5053a48dab007ee4789c1574b1fe63f56b4474a)
                check_type(argname="argument app_s_key", value=app_s_key, expected_type=type_hints["app_s_key"])
                check_type(argname="argument f_nwk_s_int_key", value=f_nwk_s_int_key, expected_type=type_hints["f_nwk_s_int_key"])
                check_type(argname="argument nwk_s_enc_key", value=nwk_s_enc_key, expected_type=type_hints["nwk_s_enc_key"])
                check_type(argname="argument s_nwk_s_int_key", value=s_nwk_s_int_key, expected_type=type_hints["s_nwk_s_int_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if app_s_key is not None:
                self._values["app_s_key"] = app_s_key
            if f_nwk_s_int_key is not None:
                self._values["f_nwk_s_int_key"] = f_nwk_s_int_key
            if nwk_s_enc_key is not None:
                self._values["nwk_s_enc_key"] = nwk_s_enc_key
            if s_nwk_s_int_key is not None:
                self._values["s_nwk_s_int_key"] = s_nwk_s_int_key

        @builtins.property
        def app_s_key(self) -> typing.Optional[builtins.str]:
            '''The AppSKey is a secret key, which you should handle in a similar way as you would an application password.

            You can protect the AppSKey value by storing it in the AWS Secrets Manager and use the `secretsmanager <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html#dynamic-references-secretsmanager>`_ to reference this value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-sessionkeysabpv11.html#cfn-iotwireless-wirelessdevice-sessionkeysabpv11-appskey
            '''
            result = self._values.get("app_s_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def f_nwk_s_int_key(self) -> typing.Optional[builtins.str]:
            '''The FNwkSIntKey is a secret key, which you should handle in a similar way as you would an application password.

            You can protect the FNwkSIntKey value by storing it in the AWS Secrets Manager and use the `secretsmanager <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html#dynamic-references-secretsmanager>`_ to reference this value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-sessionkeysabpv11.html#cfn-iotwireless-wirelessdevice-sessionkeysabpv11-fnwksintkey
            '''
            result = self._values.get("f_nwk_s_int_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def nwk_s_enc_key(self) -> typing.Optional[builtins.str]:
            '''The NwkSEncKey is a secret key, which you should handle in a similar way as you would an application password.

            You can protect the NwkSEncKey value by storing it in the AWS Secrets Manager and use the `secretsmanager <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html#dynamic-references-secretsmanager>`_ to reference this value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-sessionkeysabpv11.html#cfn-iotwireless-wirelessdevice-sessionkeysabpv11-nwksenckey
            '''
            result = self._values.get("nwk_s_enc_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s_nwk_s_int_key(self) -> typing.Optional[builtins.str]:
            '''The SNwkSIntKey is a secret key, which you should handle in a similar way as you would an application password.

            You can protect the SNwkSIntKey value by storing it in the AWS Secrets Manager and use the `secretsmanager <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html#dynamic-references-secretsmanager>`_ to reference this value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessdevice-sessionkeysabpv11.html#cfn-iotwireless-wirelessdevice-sessionkeysabpv11-snwksintkey
            '''
            result = self._values.get("s_nwk_s_int_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SessionKeysAbpV11Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnWirelessGatewayMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "last_uplink_received_at": "lastUplinkReceivedAt",
        "lo_ra_wan": "loRaWan",
        "name": "name",
        "tags": "tags",
        "thing_arn": "thingArn",
        "thing_name": "thingName",
    },
)
class CfnWirelessGatewayMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        last_uplink_received_at: typing.Optional[builtins.str] = None,
        lo_ra_wan: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWirelessGatewayPropsMixin.LoRaWANGatewayProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        thing_arn: typing.Optional[builtins.str] = None,
        thing_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnWirelessGatewayPropsMixin.

        :param description: The description of the new resource. The maximum length is 2048 characters.
        :param last_uplink_received_at: The date and time when the most recent uplink was received.
        :param lo_ra_wan: The gateway configuration information to use to create the wireless gateway.
        :param name: The name of the new resource.
        :param tags: The tags are an array of key-value pairs to attach to the specified resource. Tags can have a minimum of 0 and a maximum of 50 items.
        :param thing_arn: The ARN of the thing to associate with the wireless gateway.
        :param thing_name: The name of the thing associated with the wireless gateway. The value is empty if a thing isn't associated with the gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessgateway.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
            
            cfn_wireless_gateway_mixin_props = iotwireless_mixins.CfnWirelessGatewayMixinProps(
                description="description",
                last_uplink_received_at="lastUplinkReceivedAt",
                lo_ra_wan=iotwireless_mixins.CfnWirelessGatewayPropsMixin.LoRaWANGatewayProperty(
                    gateway_eui="gatewayEui",
                    rf_region="rfRegion"
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                thing_arn="thingArn",
                thing_name="thingName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e4b38684031b5a341b6cb2ed328f62f1d987ef24dba8d11a2e7d75196225003)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument last_uplink_received_at", value=last_uplink_received_at, expected_type=type_hints["last_uplink_received_at"])
            check_type(argname="argument lo_ra_wan", value=lo_ra_wan, expected_type=type_hints["lo_ra_wan"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument thing_arn", value=thing_arn, expected_type=type_hints["thing_arn"])
            check_type(argname="argument thing_name", value=thing_name, expected_type=type_hints["thing_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if last_uplink_received_at is not None:
            self._values["last_uplink_received_at"] = last_uplink_received_at
        if lo_ra_wan is not None:
            self._values["lo_ra_wan"] = lo_ra_wan
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if thing_arn is not None:
            self._values["thing_arn"] = thing_arn
        if thing_name is not None:
            self._values["thing_name"] = thing_name

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the new resource.

        The maximum length is 2048 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessgateway.html#cfn-iotwireless-wirelessgateway-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def last_uplink_received_at(self) -> typing.Optional[builtins.str]:
        '''The date and time when the most recent uplink was received.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessgateway.html#cfn-iotwireless-wirelessgateway-lastuplinkreceivedat
        '''
        result = self._values.get("last_uplink_received_at")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lo_ra_wan(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWirelessGatewayPropsMixin.LoRaWANGatewayProperty"]]:
        '''The gateway configuration information to use to create the wireless gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessgateway.html#cfn-iotwireless-wirelessgateway-lorawan
        '''
        result = self._values.get("lo_ra_wan")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWirelessGatewayPropsMixin.LoRaWANGatewayProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the new resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessgateway.html#cfn-iotwireless-wirelessgateway-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags are an array of key-value pairs to attach to the specified resource.

        Tags can have a minimum of 0 and a maximum of 50 items.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessgateway.html#cfn-iotwireless-wirelessgateway-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def thing_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the thing to associate with the wireless gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessgateway.html#cfn-iotwireless-wirelessgateway-thingarn
        '''
        result = self._values.get("thing_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def thing_name(self) -> typing.Optional[builtins.str]:
        '''The name of the thing associated with the wireless gateway.

        The value is empty if a thing isn't associated with the gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessgateway.html#cfn-iotwireless-wirelessgateway-thingname
        '''
        result = self._values.get("thing_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWirelessGatewayMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWirelessGatewayPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnWirelessGatewayPropsMixin",
):
    '''Provisions a wireless gateway.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotwireless-wirelessgateway.html
    :cloudformationResource: AWS::IoTWireless::WirelessGateway
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
        
        cfn_wireless_gateway_props_mixin = iotwireless_mixins.CfnWirelessGatewayPropsMixin(iotwireless_mixins.CfnWirelessGatewayMixinProps(
            description="description",
            last_uplink_received_at="lastUplinkReceivedAt",
            lo_ra_wan=iotwireless_mixins.CfnWirelessGatewayPropsMixin.LoRaWANGatewayProperty(
                gateway_eui="gatewayEui",
                rf_region="rfRegion"
            ),
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            thing_arn="thingArn",
            thing_name="thingName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnWirelessGatewayMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTWireless::WirelessGateway``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__511ae0fb30e68692693b5166e4e7f5d21395b9e6df5144fc00b37b458c22c596)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d4946a115b6b36b76cd36ec04df0f077c910dacf609f1ee4a381e12a1e2684a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37b6504d1c381a304abb46de435fb23fe768607f6a7e3b292647c897e98c5cb6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWirelessGatewayMixinProps:
        return typing.cast(CfnWirelessGatewayMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotwireless.mixins.CfnWirelessGatewayPropsMixin.LoRaWANGatewayProperty",
        jsii_struct_bases=[],
        name_mapping={"gateway_eui": "gatewayEui", "rf_region": "rfRegion"},
    )
    class LoRaWANGatewayProperty:
        def __init__(
            self,
            *,
            gateway_eui: typing.Optional[builtins.str] = None,
            rf_region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''LoRaWAN wireless gateway object.

            :param gateway_eui: The gateway's EUI value.
            :param rf_region: The frequency band (RFRegion) value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessgateway-lorawangateway.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotwireless import mixins as iotwireless_mixins
                
                lo_ra_wANGateway_property = iotwireless_mixins.CfnWirelessGatewayPropsMixin.LoRaWANGatewayProperty(
                    gateway_eui="gatewayEui",
                    rf_region="rfRegion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a900e2348884dd99ef17633ce058f0ce3db02712e72a02db22d12b2e59258b50)
                check_type(argname="argument gateway_eui", value=gateway_eui, expected_type=type_hints["gateway_eui"])
                check_type(argname="argument rf_region", value=rf_region, expected_type=type_hints["rf_region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if gateway_eui is not None:
                self._values["gateway_eui"] = gateway_eui
            if rf_region is not None:
                self._values["rf_region"] = rf_region

        @builtins.property
        def gateway_eui(self) -> typing.Optional[builtins.str]:
            '''The gateway's EUI value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessgateway-lorawangateway.html#cfn-iotwireless-wirelessgateway-lorawangateway-gatewayeui
            '''
            result = self._values.get("gateway_eui")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rf_region(self) -> typing.Optional[builtins.str]:
            '''The frequency band (RFRegion) value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotwireless-wirelessgateway-lorawangateway.html#cfn-iotwireless-wirelessgateway-lorawangateway-rfregion
            '''
            result = self._values.get("rf_region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoRaWANGatewayProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnDestinationMixinProps",
    "CfnDestinationPropsMixin",
    "CfnDeviceProfileMixinProps",
    "CfnDeviceProfilePropsMixin",
    "CfnFuotaTaskMixinProps",
    "CfnFuotaTaskPropsMixin",
    "CfnMulticastGroupMixinProps",
    "CfnMulticastGroupPropsMixin",
    "CfnNetworkAnalyzerConfigurationMixinProps",
    "CfnNetworkAnalyzerConfigurationPropsMixin",
    "CfnPartnerAccountMixinProps",
    "CfnPartnerAccountPropsMixin",
    "CfnServiceProfileMixinProps",
    "CfnServiceProfilePropsMixin",
    "CfnTaskDefinitionMixinProps",
    "CfnTaskDefinitionPropsMixin",
    "CfnWirelessDeviceImportTaskMixinProps",
    "CfnWirelessDeviceImportTaskPropsMixin",
    "CfnWirelessDeviceMixinProps",
    "CfnWirelessDevicePropsMixin",
    "CfnWirelessGatewayMixinProps",
    "CfnWirelessGatewayPropsMixin",
]

publication.publish()

def _typecheckingstub__c0f754e82917c71c4f5225f56f503cf2fcd09195153dd068ef875820102004bb(
    *,
    description: typing.Optional[builtins.str] = None,
    expression: typing.Optional[builtins.str] = None,
    expression_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8de865eb4b44bbef7791a41f8460d1ff85fbc17af6735cf7ba261780da7f12c1(
    props: typing.Union[CfnDestinationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b2a1195fa9740b386f6afd91755bd2d9479c6f5510ffc848f1e2dff91bc009(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57e89abc664ca98a5ca63ab20121bdee972b436033df3fd86bdb99b3cb41615d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f967a193a75e817a1998c4c11f0e287e2e58dcfbebe8ed63b84bad9afd79649(
    *,
    lo_ra_wan: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeviceProfilePropsMixin.LoRaWANDeviceProfileProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__592ef0137f085e7cfdc1fd75884bdf82f79d524f6ccb378829c8a4db2557d02b(
    props: typing.Union[CfnDeviceProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30213c7bceb78e8a490676fd36b4cbd1718b959969b200c828773acb9321180f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e49e3d855ffc303a8f003386e2dab3f0b92401f9e242f5bef6ffdd442db04a5f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf4d04290f902097b53a9e557f83f90b25eff2816112c62e928d7ec88d53c22(
    *,
    class_b_timeout: typing.Optional[jsii.Number] = None,
    class_c_timeout: typing.Optional[jsii.Number] = None,
    factory_preset_freqs_list: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
    mac_version: typing.Optional[builtins.str] = None,
    max_duty_cycle: typing.Optional[jsii.Number] = None,
    max_eirp: typing.Optional[jsii.Number] = None,
    ping_slot_dr: typing.Optional[jsii.Number] = None,
    ping_slot_freq: typing.Optional[jsii.Number] = None,
    ping_slot_period: typing.Optional[jsii.Number] = None,
    reg_params_revision: typing.Optional[builtins.str] = None,
    rf_region: typing.Optional[builtins.str] = None,
    rx_data_rate2: typing.Optional[jsii.Number] = None,
    rx_delay1: typing.Optional[jsii.Number] = None,
    rx_dr_offset1: typing.Optional[jsii.Number] = None,
    rx_freq2: typing.Optional[jsii.Number] = None,
    supports32_bit_f_cnt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    supports_class_b: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    supports_class_c: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    supports_join: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26f98065d0fe5e30a55c3efd3c2d301591f80488aaa732f7db8ac7cff30dd45d(
    *,
    associate_multicast_group: typing.Optional[builtins.str] = None,
    associate_wireless_device: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    disassociate_multicast_group: typing.Optional[builtins.str] = None,
    disassociate_wireless_device: typing.Optional[builtins.str] = None,
    firmware_update_image: typing.Optional[builtins.str] = None,
    firmware_update_role: typing.Optional[builtins.str] = None,
    lo_ra_wan: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFuotaTaskPropsMixin.LoRaWANProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a50bfaa658e34a7252bd93fa0583c42810da6c7d3bd6121a540c399c0fc980(
    props: typing.Union[CfnFuotaTaskMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d28a2aa503e1e14f6066bf43bd7e5462cd95eec99221a5f57bf44bf3a5c263(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f20979babf7a1f772cff434271835cdd3b2d47bdce418d5b3ba305372c14e50(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97554e720a0b1c625fe918b6b7886d870a1c966e5eb18cfbaff98683e3266f04(
    *,
    rf_region: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__831ecfadd9132a3ec164404b0eb2973d454674474dcd8742e4b715008ba7b95d(
    *,
    associate_wireless_device: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    disassociate_wireless_device: typing.Optional[builtins.str] = None,
    lo_ra_wan: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMulticastGroupPropsMixin.LoRaWANProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__696838f172b0af0022434675a542dd823b071e97335751e6baec7e2785c915e7(
    props: typing.Union[CfnMulticastGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ca6c7f6986f32325806f9c05a701c350e787d11a2fc3b81063f58374136f56d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__193687e5581c68de4b59e4940db24a7a45702424cb34670f5a7051f6da6888c8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f44d8fd8d816ec48f720435f25141268e5bbf18af5fe768c8b90747cfbd2adc(
    *,
    dl_class: typing.Optional[builtins.str] = None,
    number_of_devices_in_group: typing.Optional[jsii.Number] = None,
    number_of_devices_requested: typing.Optional[jsii.Number] = None,
    rf_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__420538a85014f0c71073dc5d726d573ee8f47401da75d2abfab391e1ab1f17df(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    trace_content: typing.Any = None,
    wireless_devices: typing.Optional[typing.Sequence[builtins.str]] = None,
    wireless_gateways: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244b9085b4b92c6c182968f1190bc532e2ca2bd422b05f10b99f2ba4ef5d5f66(
    props: typing.Union[CfnNetworkAnalyzerConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba40b85d7c1b2ba291fc7f02e1c1a4b0cabcf879393963453090a4db08254dba(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__615b9ccce9dee61e7ae3b954ddbaecf344c70f6dc60476a085f7c08de2c75568(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31a7a06e93debabd56b5de01ed1ec0dd3a4e06e2da625e8924b6a7652716ae65(
    *,
    log_level: typing.Optional[builtins.str] = None,
    wireless_device_frame_info: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1feb9dfbe264a9bdb86d1d9ca016f55eb7d15bfb579ec0ec5683edd9bcd8bb2c(
    *,
    account_linked: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    partner_account_id: typing.Optional[builtins.str] = None,
    partner_type: typing.Optional[builtins.str] = None,
    sidewalk: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPartnerAccountPropsMixin.SidewalkAccountInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sidewalk_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPartnerAccountPropsMixin.SidewalkAccountInfoWithFingerprintProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sidewalk_update: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPartnerAccountPropsMixin.SidewalkUpdateAccountProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__133720bf4cb46a0b14c7eeb49b0e7cd4a94c21d52dce7084e96cb570b6e3c6a9(
    props: typing.Union[CfnPartnerAccountMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c0e8a19dd344704e4840d05852c15d8fd7c191599ebc42d722741955baa205f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1439c7c94dd1a31bad1494a2b57fdf37fed85471335485ab90554cd3e2aa2be3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1079a03794d63e2ea872be0245b068ba625186de97fe65d6444f8eeadcc8b11f(
    *,
    app_server_private_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cce43c2c1d2261a4f5644bc66381134131c8d0972aeaa361b6f61174c6614a9(
    *,
    amazon_id: typing.Optional[builtins.str] = None,
    arn: typing.Optional[builtins.str] = None,
    fingerprint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0de01f740a81b01c044c3384d88a8407abec071c014078daac2a4a9e58d7ec3f(
    *,
    app_server_private_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b7a27dfc20de1a40003bea11f979959d61d4d898d90f5644befff8c573df71d(
    *,
    lo_ra_wan: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceProfilePropsMixin.LoRaWANServiceProfileProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be45cb0cc715db4ff657b3d596929f63ef5d96aad34eb856d5fe12817e70f1b(
    props: typing.Union[CfnServiceProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd7c4b69fcb48185e91b8e98325205dc5fdf4285ce8e231708842c1f644880b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcf90559b41a00aa1b22797c656e014bc73e21922917538a4d4ba192cf970b86(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42d698a42b05fd254a30bbcf7614d2d486ed8979b30b8b2fa35371f17acdb22e(
    *,
    add_gw_metadata: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    channel_mask: typing.Optional[builtins.str] = None,
    dev_status_req_freq: typing.Optional[jsii.Number] = None,
    dl_bucket_size: typing.Optional[jsii.Number] = None,
    dl_rate: typing.Optional[jsii.Number] = None,
    dl_rate_policy: typing.Optional[builtins.str] = None,
    dr_max: typing.Optional[jsii.Number] = None,
    dr_min: typing.Optional[jsii.Number] = None,
    hr_allowed: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    min_gw_diversity: typing.Optional[jsii.Number] = None,
    nwk_geo_loc: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    pr_allowed: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ra_allowed: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    report_dev_status_battery: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    report_dev_status_margin: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    target_per: typing.Optional[jsii.Number] = None,
    ul_bucket_size: typing.Optional[jsii.Number] = None,
    ul_rate: typing.Optional[jsii.Number] = None,
    ul_rate_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b7210cf74c4dcb3006320fbc5f554fefdef6f36dd18e741fa6072a2c0e7d572(
    *,
    auto_create_tasks: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    lo_ra_wan_update_gateway_task_entry: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskDefinitionPropsMixin.LoRaWANUpdateGatewayTaskEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_definition_type: typing.Optional[builtins.str] = None,
    update: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskDefinitionPropsMixin.UpdateWirelessGatewayTaskCreateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eb3ca73801a401f0a64d7e983404b744b3bfabc99e4e174a6d85a198d2c5a41(
    props: typing.Union[CfnTaskDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df2b5d03cbc26c72fb65618a8caad500ee7cb2ac959a83255943e9bdc4db0087(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba679495279749913337573b3a258be43751129aaeb7f53224a26bfda477b5fb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316e580b818f511331a851e6adff9fa480c6a15f445a08ff71f572754293b513(
    *,
    model: typing.Optional[builtins.str] = None,
    package_version: typing.Optional[builtins.str] = None,
    station: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b97f06c27547540bdd28656e1af4db6485cc3634712393d48efe3fd63ae5c9c(
    *,
    current_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sig_key_crc: typing.Optional[jsii.Number] = None,
    update_signature: typing.Optional[builtins.str] = None,
    update_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6c9b8b705b0f8704f7b0cc742eeb4f05416a178f7ec15549b681f022973ac5(
    *,
    current_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    update_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskDefinitionPropsMixin.LoRaWANGatewayVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31d70c750269101b29e37637bc4bb006aaec63f4cc8f5effdb6fcf47b74b9c7(
    *,
    lo_ra_wan: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskDefinitionPropsMixin.LoRaWANUpdateGatewayTaskCreateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    update_data_role: typing.Optional[builtins.str] = None,
    update_data_source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1750c9cea1260b6e08956340b513f22cc2f2170a1de0072ab314527f3412942(
    *,
    destination_name: typing.Optional[builtins.str] = None,
    sidewalk: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWirelessDeviceImportTaskPropsMixin.SidewalkProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15694f9b42e5a2179b3fbc7c77d810945b3844fd13be4e7fbc7227366609a0aa(
    props: typing.Union[CfnWirelessDeviceImportTaskMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a0b6e5e25090a94990c58dfbd7984785ca6db9787b7d4bcc7470597ca45dfde(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b68571f68caaa7f577314855f4d1ea3a13e38be4c3a2051432ff4f1e5610d6d3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9694f1d8297545c8535e87d0ea209271652e21c14db0e83738f9fb14410fbb9a(
    *,
    device_creation_file: typing.Optional[builtins.str] = None,
    device_creation_file_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    role: typing.Optional[builtins.str] = None,
    sidewalk_manufacturing_sn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__097fa1d41ad7d479104476be749b92523f543a182900d1843600a5b16e965ef0(
    *,
    description: typing.Optional[builtins.str] = None,
    destination_name: typing.Optional[builtins.str] = None,
    last_uplink_received_at: typing.Optional[builtins.str] = None,
    lo_ra_wan: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWirelessDevicePropsMixin.LoRaWANDeviceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    positioning: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    thing_arn: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e86363c3883ca01e564c81a3db970d4de8b5dcebe8b399c04781b56eccc8579a(
    props: typing.Union[CfnWirelessDeviceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a059b7d02f7b77367ae122b48cf8e3e0ed62e5ff1f6038687f48b89be469951(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7f11ca29d77999f8b912280e5075ae093853aad6c6a3d99576b7749583cc76a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f89afbf75d770708f5900afea3af386ebf0fb18f6527f8ae495ddfeb4dcfacb6(
    *,
    dev_addr: typing.Optional[builtins.str] = None,
    session_keys: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWirelessDevicePropsMixin.SessionKeysAbpV10xProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a81dfc73e88e30f2097fcfaad35799c0d8b3ee1535b65cefc3613ab2e1f1f7(
    *,
    dev_addr: typing.Optional[builtins.str] = None,
    session_keys: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWirelessDevicePropsMixin.SessionKeysAbpV11Property, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__234ef254febd39ebe8873b2ce5f00d28211e798155a91aff514d3c224033c408(
    *,
    destination_name: typing.Optional[builtins.str] = None,
    f_port: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f96813e1fec3489285d993c5bfcc2ced91689c0b55c02160fb33b88a058369(
    *,
    applications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWirelessDevicePropsMixin.ApplicationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91111f227e51c77c519d4db2d046eb4aac2cc7f4e68915aa639beb890bff98cf(
    *,
    abp_v10_x: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWirelessDevicePropsMixin.AbpV10xProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    abp_v11: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWirelessDevicePropsMixin.AbpV11Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    dev_eui: typing.Optional[builtins.str] = None,
    device_profile_id: typing.Optional[builtins.str] = None,
    f_ports: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWirelessDevicePropsMixin.FPortsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    otaa_v10_x: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWirelessDevicePropsMixin.OtaaV10xProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    otaa_v11: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWirelessDevicePropsMixin.OtaaV11Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_profile_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d6e22baca329e9dbc86d429310ab94a2db9eaa7cc3dc8b1f7256ee00d5bdcef(
    *,
    app_eui: typing.Optional[builtins.str] = None,
    app_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2e5950d8b0615769b2d379faee874a13194a465daf70c331e456170b2ca6d14(
    *,
    app_key: typing.Optional[builtins.str] = None,
    join_eui: typing.Optional[builtins.str] = None,
    nwk_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf856b92fb5c981981b278d1408a16bc04321b82145a11c51368d92bc600925d(
    *,
    app_s_key: typing.Optional[builtins.str] = None,
    nwk_s_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ac144c4e920c4c8d7a600ab5053a48dab007ee4789c1574b1fe63f56b4474a(
    *,
    app_s_key: typing.Optional[builtins.str] = None,
    f_nwk_s_int_key: typing.Optional[builtins.str] = None,
    nwk_s_enc_key: typing.Optional[builtins.str] = None,
    s_nwk_s_int_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e4b38684031b5a341b6cb2ed328f62f1d987ef24dba8d11a2e7d75196225003(
    *,
    description: typing.Optional[builtins.str] = None,
    last_uplink_received_at: typing.Optional[builtins.str] = None,
    lo_ra_wan: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWirelessGatewayPropsMixin.LoRaWANGatewayProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    thing_arn: typing.Optional[builtins.str] = None,
    thing_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__511ae0fb30e68692693b5166e4e7f5d21395b9e6df5144fc00b37b458c22c596(
    props: typing.Union[CfnWirelessGatewayMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d4946a115b6b36b76cd36ec04df0f077c910dacf609f1ee4a381e12a1e2684a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37b6504d1c381a304abb46de435fb23fe768607f6a7e3b292647c897e98c5cb6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a900e2348884dd99ef17633ce058f0ce3db02712e72a02db22d12b2e59258b50(
    *,
    gateway_eui: typing.Optional[builtins.str] = None,
    rf_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
