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
    jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnConfigMixinProps",
    jsii_struct_bases=[],
    name_mapping={"config_data": "configData", "name": "name", "tags": "tags"},
)
class CfnConfigMixinProps:
    def __init__(
        self,
        *,
        config_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigPropsMixin.ConfigDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnConfigPropsMixin.

        :param config_data: Object containing the parameters of a config. Only one subtype may be specified per config. See the subtype definitions for a description of each config subtype.
        :param name: The name of the config object.
        :param tags: Tags assigned to a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-config.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
            
            cfn_config_mixin_props = groundstation_mixins.CfnConfigMixinProps(
                config_data=groundstation_mixins.CfnConfigPropsMixin.ConfigDataProperty(
                    antenna_downlink_config=groundstation_mixins.CfnConfigPropsMixin.AntennaDownlinkConfigProperty(
                        spectrum_config=groundstation_mixins.CfnConfigPropsMixin.SpectrumConfigProperty(
                            bandwidth=groundstation_mixins.CfnConfigPropsMixin.FrequencyBandwidthProperty(
                                units="units",
                                value=123
                            ),
                            center_frequency=groundstation_mixins.CfnConfigPropsMixin.FrequencyProperty(
                                units="units",
                                value=123
                            ),
                            polarization="polarization"
                        )
                    ),
                    antenna_downlink_demod_decode_config=groundstation_mixins.CfnConfigPropsMixin.AntennaDownlinkDemodDecodeConfigProperty(
                        decode_config=groundstation_mixins.CfnConfigPropsMixin.DecodeConfigProperty(
                            unvalidated_json="unvalidatedJson"
                        ),
                        demodulation_config=groundstation_mixins.CfnConfigPropsMixin.DemodulationConfigProperty(
                            unvalidated_json="unvalidatedJson"
                        ),
                        spectrum_config=groundstation_mixins.CfnConfigPropsMixin.SpectrumConfigProperty(
                            bandwidth=groundstation_mixins.CfnConfigPropsMixin.FrequencyBandwidthProperty(
                                units="units",
                                value=123
                            ),
                            center_frequency=groundstation_mixins.CfnConfigPropsMixin.FrequencyProperty(
                                units="units",
                                value=123
                            ),
                            polarization="polarization"
                        )
                    ),
                    antenna_uplink_config=groundstation_mixins.CfnConfigPropsMixin.AntennaUplinkConfigProperty(
                        spectrum_config=groundstation_mixins.CfnConfigPropsMixin.UplinkSpectrumConfigProperty(
                            center_frequency=groundstation_mixins.CfnConfigPropsMixin.FrequencyProperty(
                                units="units",
                                value=123
                            ),
                            polarization="polarization"
                        ),
                        target_eirp=groundstation_mixins.CfnConfigPropsMixin.EirpProperty(
                            units="units",
                            value=123
                        ),
                        transmit_disabled=False
                    ),
                    dataflow_endpoint_config=groundstation_mixins.CfnConfigPropsMixin.DataflowEndpointConfigProperty(
                        dataflow_endpoint_name="dataflowEndpointName",
                        dataflow_endpoint_region="dataflowEndpointRegion"
                    ),
                    s3_recording_config=groundstation_mixins.CfnConfigPropsMixin.S3RecordingConfigProperty(
                        bucket_arn="bucketArn",
                        prefix="prefix",
                        role_arn="roleArn"
                    ),
                    tracking_config=groundstation_mixins.CfnConfigPropsMixin.TrackingConfigProperty(
                        autotrack="autotrack"
                    ),
                    uplink_echo_config=groundstation_mixins.CfnConfigPropsMixin.UplinkEchoConfigProperty(
                        antenna_uplink_config_arn="antennaUplinkConfigArn",
                        enabled=False
                    )
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__958095e85b501a929d8f9f7463d01c55c3e0a6b8ae67ce5fa47da28e34b30f7f)
            check_type(argname="argument config_data", value=config_data, expected_type=type_hints["config_data"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config_data is not None:
            self._values["config_data"] = config_data
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def config_data(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.ConfigDataProperty"]]:
        '''Object containing the parameters of a config.

        Only one subtype may be specified per config. See the subtype definitions for a description of each config subtype.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-config.html#cfn-groundstation-config-configdata
        '''
        result = self._values.get("config_data")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.ConfigDataProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the config object.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-config.html#cfn-groundstation-config-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags assigned to a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-config.html#cfn-groundstation-config-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConfigPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnConfigPropsMixin",
):
    '''Creates a ``Config`` with the specified parameters.

    Config objects provide Ground Station with the details necessary in order to schedule and execute satellite contacts.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-config.html
    :cloudformationResource: AWS::GroundStation::Config
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
        
        cfn_config_props_mixin = groundstation_mixins.CfnConfigPropsMixin(groundstation_mixins.CfnConfigMixinProps(
            config_data=groundstation_mixins.CfnConfigPropsMixin.ConfigDataProperty(
                antenna_downlink_config=groundstation_mixins.CfnConfigPropsMixin.AntennaDownlinkConfigProperty(
                    spectrum_config=groundstation_mixins.CfnConfigPropsMixin.SpectrumConfigProperty(
                        bandwidth=groundstation_mixins.CfnConfigPropsMixin.FrequencyBandwidthProperty(
                            units="units",
                            value=123
                        ),
                        center_frequency=groundstation_mixins.CfnConfigPropsMixin.FrequencyProperty(
                            units="units",
                            value=123
                        ),
                        polarization="polarization"
                    )
                ),
                antenna_downlink_demod_decode_config=groundstation_mixins.CfnConfigPropsMixin.AntennaDownlinkDemodDecodeConfigProperty(
                    decode_config=groundstation_mixins.CfnConfigPropsMixin.DecodeConfigProperty(
                        unvalidated_json="unvalidatedJson"
                    ),
                    demodulation_config=groundstation_mixins.CfnConfigPropsMixin.DemodulationConfigProperty(
                        unvalidated_json="unvalidatedJson"
                    ),
                    spectrum_config=groundstation_mixins.CfnConfigPropsMixin.SpectrumConfigProperty(
                        bandwidth=groundstation_mixins.CfnConfigPropsMixin.FrequencyBandwidthProperty(
                            units="units",
                            value=123
                        ),
                        center_frequency=groundstation_mixins.CfnConfigPropsMixin.FrequencyProperty(
                            units="units",
                            value=123
                        ),
                        polarization="polarization"
                    )
                ),
                antenna_uplink_config=groundstation_mixins.CfnConfigPropsMixin.AntennaUplinkConfigProperty(
                    spectrum_config=groundstation_mixins.CfnConfigPropsMixin.UplinkSpectrumConfigProperty(
                        center_frequency=groundstation_mixins.CfnConfigPropsMixin.FrequencyProperty(
                            units="units",
                            value=123
                        ),
                        polarization="polarization"
                    ),
                    target_eirp=groundstation_mixins.CfnConfigPropsMixin.EirpProperty(
                        units="units",
                        value=123
                    ),
                    transmit_disabled=False
                ),
                dataflow_endpoint_config=groundstation_mixins.CfnConfigPropsMixin.DataflowEndpointConfigProperty(
                    dataflow_endpoint_name="dataflowEndpointName",
                    dataflow_endpoint_region="dataflowEndpointRegion"
                ),
                s3_recording_config=groundstation_mixins.CfnConfigPropsMixin.S3RecordingConfigProperty(
                    bucket_arn="bucketArn",
                    prefix="prefix",
                    role_arn="roleArn"
                ),
                tracking_config=groundstation_mixins.CfnConfigPropsMixin.TrackingConfigProperty(
                    autotrack="autotrack"
                ),
                uplink_echo_config=groundstation_mixins.CfnConfigPropsMixin.UplinkEchoConfigProperty(
                    antenna_uplink_config_arn="antennaUplinkConfigArn",
                    enabled=False
                )
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
        props: typing.Union[CfnConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GroundStation::Config``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa073db2c0f09d28062420244118cbbe67e5b0fd47b852dce0c2356c0597cb06)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cd4f68f8f36713d422343e12aa4b29362017f70ff8a9566c4ec40e6fef75218)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9379f1df3478235c060bf355876c237138178f9f33970626dd77c8272eb0f1d8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConfigMixinProps:
        return typing.cast(CfnConfigMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnConfigPropsMixin.AntennaDownlinkConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"spectrum_config": "spectrumConfig"},
    )
    class AntennaDownlinkConfigProperty:
        def __init__(
            self,
            *,
            spectrum_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigPropsMixin.SpectrumConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides information about how AWS Ground Station should configure an antenna for downlink during a contact.

            Use an antenna downlink config in a mission profile to receive the downlink data in raw DigIF format.

            :param spectrum_config: Defines the spectrum configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-antennadownlinkconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                antenna_downlink_config_property = groundstation_mixins.CfnConfigPropsMixin.AntennaDownlinkConfigProperty(
                    spectrum_config=groundstation_mixins.CfnConfigPropsMixin.SpectrumConfigProperty(
                        bandwidth=groundstation_mixins.CfnConfigPropsMixin.FrequencyBandwidthProperty(
                            units="units",
                            value=123
                        ),
                        center_frequency=groundstation_mixins.CfnConfigPropsMixin.FrequencyProperty(
                            units="units",
                            value=123
                        ),
                        polarization="polarization"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__94b1b82935a35d8f0a63b8c2c814df3a8ec47756089f01a1b261a40336c3a528)
                check_type(argname="argument spectrum_config", value=spectrum_config, expected_type=type_hints["spectrum_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if spectrum_config is not None:
                self._values["spectrum_config"] = spectrum_config

        @builtins.property
        def spectrum_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.SpectrumConfigProperty"]]:
            '''Defines the spectrum configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-antennadownlinkconfig.html#cfn-groundstation-config-antennadownlinkconfig-spectrumconfig
            '''
            result = self._values.get("spectrum_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.SpectrumConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AntennaDownlinkConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnConfigPropsMixin.AntennaDownlinkDemodDecodeConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "decode_config": "decodeConfig",
            "demodulation_config": "demodulationConfig",
            "spectrum_config": "spectrumConfig",
        },
    )
    class AntennaDownlinkDemodDecodeConfigProperty:
        def __init__(
            self,
            *,
            decode_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigPropsMixin.DecodeConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            demodulation_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigPropsMixin.DemodulationConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            spectrum_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigPropsMixin.SpectrumConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides information about how AWS Ground Station should configure an antenna for downlink during a contact.

            Use an antenna downlink demod decode config in a mission profile to receive the downlink data that has been demodulated and decoded.

            :param decode_config: Defines how the RF signal will be decoded.
            :param demodulation_config: Defines how the RF signal will be demodulated.
            :param spectrum_config: Defines the spectrum configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-antennadownlinkdemoddecodeconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                antenna_downlink_demod_decode_config_property = groundstation_mixins.CfnConfigPropsMixin.AntennaDownlinkDemodDecodeConfigProperty(
                    decode_config=groundstation_mixins.CfnConfigPropsMixin.DecodeConfigProperty(
                        unvalidated_json="unvalidatedJson"
                    ),
                    demodulation_config=groundstation_mixins.CfnConfigPropsMixin.DemodulationConfigProperty(
                        unvalidated_json="unvalidatedJson"
                    ),
                    spectrum_config=groundstation_mixins.CfnConfigPropsMixin.SpectrumConfigProperty(
                        bandwidth=groundstation_mixins.CfnConfigPropsMixin.FrequencyBandwidthProperty(
                            units="units",
                            value=123
                        ),
                        center_frequency=groundstation_mixins.CfnConfigPropsMixin.FrequencyProperty(
                            units="units",
                            value=123
                        ),
                        polarization="polarization"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ede83788e32643d28c05693a18a965383579cf6cb19f6d2bd4bb569a0b7824c5)
                check_type(argname="argument decode_config", value=decode_config, expected_type=type_hints["decode_config"])
                check_type(argname="argument demodulation_config", value=demodulation_config, expected_type=type_hints["demodulation_config"])
                check_type(argname="argument spectrum_config", value=spectrum_config, expected_type=type_hints["spectrum_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if decode_config is not None:
                self._values["decode_config"] = decode_config
            if demodulation_config is not None:
                self._values["demodulation_config"] = demodulation_config
            if spectrum_config is not None:
                self._values["spectrum_config"] = spectrum_config

        @builtins.property
        def decode_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.DecodeConfigProperty"]]:
            '''Defines how the RF signal will be decoded.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-antennadownlinkdemoddecodeconfig.html#cfn-groundstation-config-antennadownlinkdemoddecodeconfig-decodeconfig
            '''
            result = self._values.get("decode_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.DecodeConfigProperty"]], result)

        @builtins.property
        def demodulation_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.DemodulationConfigProperty"]]:
            '''Defines how the RF signal will be demodulated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-antennadownlinkdemoddecodeconfig.html#cfn-groundstation-config-antennadownlinkdemoddecodeconfig-demodulationconfig
            '''
            result = self._values.get("demodulation_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.DemodulationConfigProperty"]], result)

        @builtins.property
        def spectrum_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.SpectrumConfigProperty"]]:
            '''Defines the spectrum configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-antennadownlinkdemoddecodeconfig.html#cfn-groundstation-config-antennadownlinkdemoddecodeconfig-spectrumconfig
            '''
            result = self._values.get("spectrum_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.SpectrumConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AntennaDownlinkDemodDecodeConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnConfigPropsMixin.AntennaUplinkConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "spectrum_config": "spectrumConfig",
            "target_eirp": "targetEirp",
            "transmit_disabled": "transmitDisabled",
        },
    )
    class AntennaUplinkConfigProperty:
        def __init__(
            self,
            *,
            spectrum_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigPropsMixin.UplinkSpectrumConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            target_eirp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigPropsMixin.EirpProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            transmit_disabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Provides information about how AWS Ground Station should configure an antenna for uplink during a contact.

            :param spectrum_config: Defines the spectrum configuration.
            :param target_eirp: The equivalent isotropically radiated power (EIRP) to use for uplink transmissions. Valid values are between 20.0 to 50.0 dBW.
            :param transmit_disabled: Whether or not uplink transmit is disabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-antennauplinkconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                antenna_uplink_config_property = groundstation_mixins.CfnConfigPropsMixin.AntennaUplinkConfigProperty(
                    spectrum_config=groundstation_mixins.CfnConfigPropsMixin.UplinkSpectrumConfigProperty(
                        center_frequency=groundstation_mixins.CfnConfigPropsMixin.FrequencyProperty(
                            units="units",
                            value=123
                        ),
                        polarization="polarization"
                    ),
                    target_eirp=groundstation_mixins.CfnConfigPropsMixin.EirpProperty(
                        units="units",
                        value=123
                    ),
                    transmit_disabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9ce32518684c906d888c70f297daeb18887baaee045f86e58112f242357395fc)
                check_type(argname="argument spectrum_config", value=spectrum_config, expected_type=type_hints["spectrum_config"])
                check_type(argname="argument target_eirp", value=target_eirp, expected_type=type_hints["target_eirp"])
                check_type(argname="argument transmit_disabled", value=transmit_disabled, expected_type=type_hints["transmit_disabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if spectrum_config is not None:
                self._values["spectrum_config"] = spectrum_config
            if target_eirp is not None:
                self._values["target_eirp"] = target_eirp
            if transmit_disabled is not None:
                self._values["transmit_disabled"] = transmit_disabled

        @builtins.property
        def spectrum_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.UplinkSpectrumConfigProperty"]]:
            '''Defines the spectrum configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-antennauplinkconfig.html#cfn-groundstation-config-antennauplinkconfig-spectrumconfig
            '''
            result = self._values.get("spectrum_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.UplinkSpectrumConfigProperty"]], result)

        @builtins.property
        def target_eirp(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.EirpProperty"]]:
            '''The equivalent isotropically radiated power (EIRP) to use for uplink transmissions.

            Valid values are between 20.0 to 50.0 dBW.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-antennauplinkconfig.html#cfn-groundstation-config-antennauplinkconfig-targeteirp
            '''
            result = self._values.get("target_eirp")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.EirpProperty"]], result)

        @builtins.property
        def transmit_disabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether or not uplink transmit is disabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-antennauplinkconfig.html#cfn-groundstation-config-antennauplinkconfig-transmitdisabled
            '''
            result = self._values.get("transmit_disabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AntennaUplinkConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnConfigPropsMixin.ConfigDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "antenna_downlink_config": "antennaDownlinkConfig",
            "antenna_downlink_demod_decode_config": "antennaDownlinkDemodDecodeConfig",
            "antenna_uplink_config": "antennaUplinkConfig",
            "dataflow_endpoint_config": "dataflowEndpointConfig",
            "s3_recording_config": "s3RecordingConfig",
            "tracking_config": "trackingConfig",
            "uplink_echo_config": "uplinkEchoConfig",
        },
    )
    class ConfigDataProperty:
        def __init__(
            self,
            *,
            antenna_downlink_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigPropsMixin.AntennaDownlinkConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            antenna_downlink_demod_decode_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigPropsMixin.AntennaDownlinkDemodDecodeConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            antenna_uplink_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigPropsMixin.AntennaUplinkConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dataflow_endpoint_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigPropsMixin.DataflowEndpointConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_recording_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigPropsMixin.S3RecordingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            tracking_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigPropsMixin.TrackingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            uplink_echo_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigPropsMixin.UplinkEchoConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Config objects provide information to Ground Station about how to configure the antenna and how data flows during a contact.

            :param antenna_downlink_config: Provides information for an antenna downlink config object. Antenna downlink config objects are used to provide parameters for downlinks where no demodulation or decoding is performed by Ground Station (RF over IP downlinks).
            :param antenna_downlink_demod_decode_config: Provides information for a downlink demod decode config object. Downlink demod decode config objects are used to provide parameters for downlinks where the Ground Station service will demodulate and decode the downlinked data.
            :param antenna_uplink_config: Provides information for an uplink config object. Uplink config objects are used to provide parameters for uplink contacts.
            :param dataflow_endpoint_config: Provides information for a dataflow endpoint config object. Dataflow endpoint config objects are used to provide parameters about which IP endpoint(s) to use during a contact. Dataflow endpoints are where Ground Station sends data during a downlink contact and where Ground Station receives data to send to the satellite during an uplink contact.
            :param s3_recording_config: Provides information for an S3 recording config object. S3 recording config objects are used to provide parameters for S3 recording during downlink contacts.
            :param tracking_config: Provides information for a tracking config object. Tracking config objects are used to provide parameters about how to track the satellite through the sky during a contact.
            :param uplink_echo_config: Provides information for an uplink echo config object. Uplink echo config objects are used to provide parameters for uplink echo during uplink contacts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-configdata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                config_data_property = groundstation_mixins.CfnConfigPropsMixin.ConfigDataProperty(
                    antenna_downlink_config=groundstation_mixins.CfnConfigPropsMixin.AntennaDownlinkConfigProperty(
                        spectrum_config=groundstation_mixins.CfnConfigPropsMixin.SpectrumConfigProperty(
                            bandwidth=groundstation_mixins.CfnConfigPropsMixin.FrequencyBandwidthProperty(
                                units="units",
                                value=123
                            ),
                            center_frequency=groundstation_mixins.CfnConfigPropsMixin.FrequencyProperty(
                                units="units",
                                value=123
                            ),
                            polarization="polarization"
                        )
                    ),
                    antenna_downlink_demod_decode_config=groundstation_mixins.CfnConfigPropsMixin.AntennaDownlinkDemodDecodeConfigProperty(
                        decode_config=groundstation_mixins.CfnConfigPropsMixin.DecodeConfigProperty(
                            unvalidated_json="unvalidatedJson"
                        ),
                        demodulation_config=groundstation_mixins.CfnConfigPropsMixin.DemodulationConfigProperty(
                            unvalidated_json="unvalidatedJson"
                        ),
                        spectrum_config=groundstation_mixins.CfnConfigPropsMixin.SpectrumConfigProperty(
                            bandwidth=groundstation_mixins.CfnConfigPropsMixin.FrequencyBandwidthProperty(
                                units="units",
                                value=123
                            ),
                            center_frequency=groundstation_mixins.CfnConfigPropsMixin.FrequencyProperty(
                                units="units",
                                value=123
                            ),
                            polarization="polarization"
                        )
                    ),
                    antenna_uplink_config=groundstation_mixins.CfnConfigPropsMixin.AntennaUplinkConfigProperty(
                        spectrum_config=groundstation_mixins.CfnConfigPropsMixin.UplinkSpectrumConfigProperty(
                            center_frequency=groundstation_mixins.CfnConfigPropsMixin.FrequencyProperty(
                                units="units",
                                value=123
                            ),
                            polarization="polarization"
                        ),
                        target_eirp=groundstation_mixins.CfnConfigPropsMixin.EirpProperty(
                            units="units",
                            value=123
                        ),
                        transmit_disabled=False
                    ),
                    dataflow_endpoint_config=groundstation_mixins.CfnConfigPropsMixin.DataflowEndpointConfigProperty(
                        dataflow_endpoint_name="dataflowEndpointName",
                        dataflow_endpoint_region="dataflowEndpointRegion"
                    ),
                    s3_recording_config=groundstation_mixins.CfnConfigPropsMixin.S3RecordingConfigProperty(
                        bucket_arn="bucketArn",
                        prefix="prefix",
                        role_arn="roleArn"
                    ),
                    tracking_config=groundstation_mixins.CfnConfigPropsMixin.TrackingConfigProperty(
                        autotrack="autotrack"
                    ),
                    uplink_echo_config=groundstation_mixins.CfnConfigPropsMixin.UplinkEchoConfigProperty(
                        antenna_uplink_config_arn="antennaUplinkConfigArn",
                        enabled=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__68e47f37ef91eff42eac677894acf6d61a3c014d5f11d939f9ef530221931fea)
                check_type(argname="argument antenna_downlink_config", value=antenna_downlink_config, expected_type=type_hints["antenna_downlink_config"])
                check_type(argname="argument antenna_downlink_demod_decode_config", value=antenna_downlink_demod_decode_config, expected_type=type_hints["antenna_downlink_demod_decode_config"])
                check_type(argname="argument antenna_uplink_config", value=antenna_uplink_config, expected_type=type_hints["antenna_uplink_config"])
                check_type(argname="argument dataflow_endpoint_config", value=dataflow_endpoint_config, expected_type=type_hints["dataflow_endpoint_config"])
                check_type(argname="argument s3_recording_config", value=s3_recording_config, expected_type=type_hints["s3_recording_config"])
                check_type(argname="argument tracking_config", value=tracking_config, expected_type=type_hints["tracking_config"])
                check_type(argname="argument uplink_echo_config", value=uplink_echo_config, expected_type=type_hints["uplink_echo_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if antenna_downlink_config is not None:
                self._values["antenna_downlink_config"] = antenna_downlink_config
            if antenna_downlink_demod_decode_config is not None:
                self._values["antenna_downlink_demod_decode_config"] = antenna_downlink_demod_decode_config
            if antenna_uplink_config is not None:
                self._values["antenna_uplink_config"] = antenna_uplink_config
            if dataflow_endpoint_config is not None:
                self._values["dataflow_endpoint_config"] = dataflow_endpoint_config
            if s3_recording_config is not None:
                self._values["s3_recording_config"] = s3_recording_config
            if tracking_config is not None:
                self._values["tracking_config"] = tracking_config
            if uplink_echo_config is not None:
                self._values["uplink_echo_config"] = uplink_echo_config

        @builtins.property
        def antenna_downlink_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.AntennaDownlinkConfigProperty"]]:
            '''Provides information for an antenna downlink config object.

            Antenna downlink config objects are used to provide parameters for downlinks where no demodulation or decoding is performed by Ground Station (RF over IP downlinks).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-configdata.html#cfn-groundstation-config-configdata-antennadownlinkconfig
            '''
            result = self._values.get("antenna_downlink_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.AntennaDownlinkConfigProperty"]], result)

        @builtins.property
        def antenna_downlink_demod_decode_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.AntennaDownlinkDemodDecodeConfigProperty"]]:
            '''Provides information for a downlink demod decode config object.

            Downlink demod decode config objects are used to provide parameters for downlinks where the Ground Station service will demodulate and decode the downlinked data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-configdata.html#cfn-groundstation-config-configdata-antennadownlinkdemoddecodeconfig
            '''
            result = self._values.get("antenna_downlink_demod_decode_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.AntennaDownlinkDemodDecodeConfigProperty"]], result)

        @builtins.property
        def antenna_uplink_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.AntennaUplinkConfigProperty"]]:
            '''Provides information for an uplink config object.

            Uplink config objects are used to provide parameters for uplink contacts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-configdata.html#cfn-groundstation-config-configdata-antennauplinkconfig
            '''
            result = self._values.get("antenna_uplink_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.AntennaUplinkConfigProperty"]], result)

        @builtins.property
        def dataflow_endpoint_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.DataflowEndpointConfigProperty"]]:
            '''Provides information for a dataflow endpoint config object.

            Dataflow endpoint config objects are used to provide parameters about which IP endpoint(s) to use during a contact. Dataflow endpoints are where Ground Station sends data during a downlink contact and where Ground Station receives data to send to the satellite during an uplink contact.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-configdata.html#cfn-groundstation-config-configdata-dataflowendpointconfig
            '''
            result = self._values.get("dataflow_endpoint_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.DataflowEndpointConfigProperty"]], result)

        @builtins.property
        def s3_recording_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.S3RecordingConfigProperty"]]:
            '''Provides information for an S3 recording config object.

            S3 recording config objects are used to provide parameters for S3 recording during downlink contacts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-configdata.html#cfn-groundstation-config-configdata-s3recordingconfig
            '''
            result = self._values.get("s3_recording_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.S3RecordingConfigProperty"]], result)

        @builtins.property
        def tracking_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.TrackingConfigProperty"]]:
            '''Provides information for a tracking config object.

            Tracking config objects are used to provide parameters about how to track the satellite through the sky during a contact.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-configdata.html#cfn-groundstation-config-configdata-trackingconfig
            '''
            result = self._values.get("tracking_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.TrackingConfigProperty"]], result)

        @builtins.property
        def uplink_echo_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.UplinkEchoConfigProperty"]]:
            '''Provides information for an uplink echo config object.

            Uplink echo config objects are used to provide parameters for uplink echo during uplink contacts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-configdata.html#cfn-groundstation-config-configdata-uplinkechoconfig
            '''
            result = self._values.get("uplink_echo_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.UplinkEchoConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnConfigPropsMixin.DataflowEndpointConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dataflow_endpoint_name": "dataflowEndpointName",
            "dataflow_endpoint_region": "dataflowEndpointRegion",
        },
    )
    class DataflowEndpointConfigProperty:
        def __init__(
            self,
            *,
            dataflow_endpoint_name: typing.Optional[builtins.str] = None,
            dataflow_endpoint_region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information to AWS Ground Station about which IP endpoints to use during a contact.

            :param dataflow_endpoint_name: The name of the dataflow endpoint to use during contacts.
            :param dataflow_endpoint_region: The region of the dataflow endpoint to use during contacts. When omitted, Ground Station will use the region of the contact.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-dataflowendpointconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                dataflow_endpoint_config_property = groundstation_mixins.CfnConfigPropsMixin.DataflowEndpointConfigProperty(
                    dataflow_endpoint_name="dataflowEndpointName",
                    dataflow_endpoint_region="dataflowEndpointRegion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__764028d11eb082731531e574fd61a4311641440727a9faa894b83e6c722340fc)
                check_type(argname="argument dataflow_endpoint_name", value=dataflow_endpoint_name, expected_type=type_hints["dataflow_endpoint_name"])
                check_type(argname="argument dataflow_endpoint_region", value=dataflow_endpoint_region, expected_type=type_hints["dataflow_endpoint_region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dataflow_endpoint_name is not None:
                self._values["dataflow_endpoint_name"] = dataflow_endpoint_name
            if dataflow_endpoint_region is not None:
                self._values["dataflow_endpoint_region"] = dataflow_endpoint_region

        @builtins.property
        def dataflow_endpoint_name(self) -> typing.Optional[builtins.str]:
            '''The name of the dataflow endpoint to use during contacts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-dataflowendpointconfig.html#cfn-groundstation-config-dataflowendpointconfig-dataflowendpointname
            '''
            result = self._values.get("dataflow_endpoint_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dataflow_endpoint_region(self) -> typing.Optional[builtins.str]:
            '''The region of the dataflow endpoint to use during contacts.

            When omitted, Ground Station will use the region of the contact.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-dataflowendpointconfig.html#cfn-groundstation-config-dataflowendpointconfig-dataflowendpointregion
            '''
            result = self._values.get("dataflow_endpoint_region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataflowEndpointConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnConfigPropsMixin.DecodeConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"unvalidated_json": "unvalidatedJson"},
    )
    class DecodeConfigProperty:
        def __init__(
            self,
            *,
            unvalidated_json: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines decoding settings.

            :param unvalidated_json: The decoding settings are in JSON format and define a set of steps to perform to decode the data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-decodeconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                decode_config_property = groundstation_mixins.CfnConfigPropsMixin.DecodeConfigProperty(
                    unvalidated_json="unvalidatedJson"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f7b9b73405654832011b38fa56e84f9b02e74683270d115c7a325a41d9d9cb78)
                check_type(argname="argument unvalidated_json", value=unvalidated_json, expected_type=type_hints["unvalidated_json"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if unvalidated_json is not None:
                self._values["unvalidated_json"] = unvalidated_json

        @builtins.property
        def unvalidated_json(self) -> typing.Optional[builtins.str]:
            '''The decoding settings are in JSON format and define a set of steps to perform to decode the data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-decodeconfig.html#cfn-groundstation-config-decodeconfig-unvalidatedjson
            '''
            result = self._values.get("unvalidated_json")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DecodeConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnConfigPropsMixin.DemodulationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"unvalidated_json": "unvalidatedJson"},
    )
    class DemodulationConfigProperty:
        def __init__(
            self,
            *,
            unvalidated_json: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines demodulation settings.

            :param unvalidated_json: The demodulation settings are in JSON format and define parameters for demodulation, for example which modulation scheme (e.g. PSK, QPSK, etc.) and matched filter to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-demodulationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                demodulation_config_property = groundstation_mixins.CfnConfigPropsMixin.DemodulationConfigProperty(
                    unvalidated_json="unvalidatedJson"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7cf07ac45cf974bb1910f94d6aa2e9004b32df61d39904040e49e2cc19e49a84)
                check_type(argname="argument unvalidated_json", value=unvalidated_json, expected_type=type_hints["unvalidated_json"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if unvalidated_json is not None:
                self._values["unvalidated_json"] = unvalidated_json

        @builtins.property
        def unvalidated_json(self) -> typing.Optional[builtins.str]:
            '''The demodulation settings are in JSON format and define parameters for demodulation, for example which modulation scheme (e.g. PSK, QPSK, etc.) and matched filter to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-demodulationconfig.html#cfn-groundstation-config-demodulationconfig-unvalidatedjson
            '''
            result = self._values.get("unvalidated_json")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DemodulationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnConfigPropsMixin.EirpProperty",
        jsii_struct_bases=[],
        name_mapping={"units": "units", "value": "value"},
    )
    class EirpProperty:
        def __init__(
            self,
            *,
            units: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Defines an equivalent isotropically radiated power (EIRP).

            :param units: The units of the EIRP.
            :param value: The value of the EIRP. Valid values are between 20.0 to 50.0 dBW.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-eirp.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                eirp_property = groundstation_mixins.CfnConfigPropsMixin.EirpProperty(
                    units="units",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d8f811a579ec38f034616146157535a01673a8944bdd67a006e47053c297de99)
                check_type(argname="argument units", value=units, expected_type=type_hints["units"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if units is not None:
                self._values["units"] = units
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def units(self) -> typing.Optional[builtins.str]:
            '''The units of the EIRP.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-eirp.html#cfn-groundstation-config-eirp-units
            '''
            result = self._values.get("units")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''The value of the EIRP.

            Valid values are between 20.0 to 50.0 dBW.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-eirp.html#cfn-groundstation-config-eirp-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EirpProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnConfigPropsMixin.FrequencyBandwidthProperty",
        jsii_struct_bases=[],
        name_mapping={"units": "units", "value": "value"},
    )
    class FrequencyBandwidthProperty:
        def __init__(
            self,
            *,
            units: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Defines a bandwidth.

            :param units: The units of the bandwidth.
            :param value: The value of the bandwidth. AWS Ground Station currently has the following bandwidth limitations:. - For ``AntennaDownlinkDemodDecodeconfig`` , valid values are between 125 kHz to 650 MHz. - For ``AntennaDownlinkconfig`` , valid values are between 10 kHz to 54 MHz. - For ``AntennaUplinkConfig`` , valid values are between 10 kHz to 54 MHz.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-frequencybandwidth.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                frequency_bandwidth_property = groundstation_mixins.CfnConfigPropsMixin.FrequencyBandwidthProperty(
                    units="units",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__de0f30942253e1ac58c2efebe6ad5f74fe40df4f6bfa3da07a921e13157a956e)
                check_type(argname="argument units", value=units, expected_type=type_hints["units"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if units is not None:
                self._values["units"] = units
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def units(self) -> typing.Optional[builtins.str]:
            '''The units of the bandwidth.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-frequencybandwidth.html#cfn-groundstation-config-frequencybandwidth-units
            '''
            result = self._values.get("units")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''The value of the bandwidth. AWS Ground Station currently has the following bandwidth limitations:.

            - For ``AntennaDownlinkDemodDecodeconfig`` , valid values are between 125 kHz to 650 MHz.
            - For ``AntennaDownlinkconfig`` , valid values are between 10 kHz to 54 MHz.
            - For ``AntennaUplinkConfig`` , valid values are between 10 kHz to 54 MHz.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-frequencybandwidth.html#cfn-groundstation-config-frequencybandwidth-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FrequencyBandwidthProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnConfigPropsMixin.FrequencyProperty",
        jsii_struct_bases=[],
        name_mapping={"units": "units", "value": "value"},
    )
    class FrequencyProperty:
        def __init__(
            self,
            *,
            units: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Defines a frequency.

            :param units: The units of the frequency.
            :param value: The value of the frequency. Valid values are between 2200 to 2300 MHz and 7750 to 8400 MHz for downlink and 2025 to 2120 MHz for uplink.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-frequency.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                frequency_property = groundstation_mixins.CfnConfigPropsMixin.FrequencyProperty(
                    units="units",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c6344f217297cca12876d99b4ac4750162fcedb48919bae0b9cc971cada4babb)
                check_type(argname="argument units", value=units, expected_type=type_hints["units"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if units is not None:
                self._values["units"] = units
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def units(self) -> typing.Optional[builtins.str]:
            '''The units of the frequency.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-frequency.html#cfn-groundstation-config-frequency-units
            '''
            result = self._values.get("units")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''The value of the frequency.

            Valid values are between 2200 to 2300 MHz and 7750 to 8400 MHz for downlink and 2025 to 2120 MHz for uplink.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-frequency.html#cfn-groundstation-config-frequency-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FrequencyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnConfigPropsMixin.S3RecordingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_arn": "bucketArn",
            "prefix": "prefix",
            "role_arn": "roleArn",
        },
    )
    class S3RecordingConfigProperty:
        def __init__(
            self,
            *,
            bucket_arn: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information about how AWS Ground Station should save downlink data to S3.

            :param bucket_arn: S3 Bucket where the data is written. The name of the S3 Bucket provided must begin with ``aws-groundstation`` .
            :param prefix: The prefix of the S3 data object. If you choose to use any optional keys for substitution, these values will be replaced with the corresponding information from your contact details. For example, a prefix of ``{satellite_id}/{year}/{month}/{day}/`` will replaced with ``fake_satellite_id/2021/01/10/`` *Optional keys for substitution* : ``{satellite_id}`` | ``{config-name}`` | ``{config-id}`` | ``{year}`` | ``{month}`` | ``{day}``
            :param role_arn: Defines the ARN of the role assumed for putting archives to S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-s3recordingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                s3_recording_config_property = groundstation_mixins.CfnConfigPropsMixin.S3RecordingConfigProperty(
                    bucket_arn="bucketArn",
                    prefix="prefix",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ecb2e8a7e8590c47b9013bd4dd3e2525fef7f510594b0ef1a9aba1fab06d02b1)
                check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_arn is not None:
                self._values["bucket_arn"] = bucket_arn
            if prefix is not None:
                self._values["prefix"] = prefix
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def bucket_arn(self) -> typing.Optional[builtins.str]:
            '''S3 Bucket where the data is written.

            The name of the S3 Bucket provided must begin with ``aws-groundstation`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-s3recordingconfig.html#cfn-groundstation-config-s3recordingconfig-bucketarn
            '''
            result = self._values.get("bucket_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''The prefix of the S3 data object.

            If you choose to use any optional keys for substitution, these values will be replaced with the corresponding information from your contact details. For example, a prefix of ``{satellite_id}/{year}/{month}/{day}/`` will replaced with ``fake_satellite_id/2021/01/10/``

            *Optional keys for substitution* : ``{satellite_id}`` | ``{config-name}`` | ``{config-id}`` | ``{year}`` | ``{month}`` | ``{day}``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-s3recordingconfig.html#cfn-groundstation-config-s3recordingconfig-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''Defines the ARN of the role assumed for putting archives to S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-s3recordingconfig.html#cfn-groundstation-config-s3recordingconfig-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3RecordingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnConfigPropsMixin.SpectrumConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bandwidth": "bandwidth",
            "center_frequency": "centerFrequency",
            "polarization": "polarization",
        },
    )
    class SpectrumConfigProperty:
        def __init__(
            self,
            *,
            bandwidth: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigPropsMixin.FrequencyBandwidthProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            center_frequency: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigPropsMixin.FrequencyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            polarization: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines a spectrum.

            :param bandwidth: The bandwidth of the spectrum. AWS Ground Station currently has the following bandwidth limitations:. - For ``AntennaDownlinkDemodDecodeconfig`` , valid values are between 125 kHz to 650 MHz. - For ``AntennaDownlinkconfig`` , valid values are between 10 kHz to 54 MHz. - For ``AntennaUplinkConfig`` , valid values are between 10 kHz to 54 MHz.
            :param center_frequency: The center frequency of the spectrum. Valid values are between 2200 to 2300 MHz and 7750 to 8400 MHz for downlink and 2025 to 2120 MHz for uplink.
            :param polarization: The polarization of the spectrum. Valid values are ``"RIGHT_HAND"`` and ``"LEFT_HAND"`` . Capturing both ``"RIGHT_HAND"`` and ``"LEFT_HAND"`` polarization requires two separate configs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-spectrumconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                spectrum_config_property = groundstation_mixins.CfnConfigPropsMixin.SpectrumConfigProperty(
                    bandwidth=groundstation_mixins.CfnConfigPropsMixin.FrequencyBandwidthProperty(
                        units="units",
                        value=123
                    ),
                    center_frequency=groundstation_mixins.CfnConfigPropsMixin.FrequencyProperty(
                        units="units",
                        value=123
                    ),
                    polarization="polarization"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e44e98abc58c653f4e1df8f66e85c3a32763bd11297721dcc63236192c6a4572)
                check_type(argname="argument bandwidth", value=bandwidth, expected_type=type_hints["bandwidth"])
                check_type(argname="argument center_frequency", value=center_frequency, expected_type=type_hints["center_frequency"])
                check_type(argname="argument polarization", value=polarization, expected_type=type_hints["polarization"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bandwidth is not None:
                self._values["bandwidth"] = bandwidth
            if center_frequency is not None:
                self._values["center_frequency"] = center_frequency
            if polarization is not None:
                self._values["polarization"] = polarization

        @builtins.property
        def bandwidth(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.FrequencyBandwidthProperty"]]:
            '''The bandwidth of the spectrum. AWS Ground Station currently has the following bandwidth limitations:.

            - For ``AntennaDownlinkDemodDecodeconfig`` , valid values are between 125 kHz to 650 MHz.
            - For ``AntennaDownlinkconfig`` , valid values are between 10 kHz to 54 MHz.
            - For ``AntennaUplinkConfig`` , valid values are between 10 kHz to 54 MHz.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-spectrumconfig.html#cfn-groundstation-config-spectrumconfig-bandwidth
            '''
            result = self._values.get("bandwidth")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.FrequencyBandwidthProperty"]], result)

        @builtins.property
        def center_frequency(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.FrequencyProperty"]]:
            '''The center frequency of the spectrum.

            Valid values are between 2200 to 2300 MHz and 7750 to 8400 MHz for downlink and 2025 to 2120 MHz for uplink.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-spectrumconfig.html#cfn-groundstation-config-spectrumconfig-centerfrequency
            '''
            result = self._values.get("center_frequency")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.FrequencyProperty"]], result)

        @builtins.property
        def polarization(self) -> typing.Optional[builtins.str]:
            '''The polarization of the spectrum.

            Valid values are ``"RIGHT_HAND"`` and ``"LEFT_HAND"`` . Capturing both ``"RIGHT_HAND"`` and ``"LEFT_HAND"`` polarization requires two separate configs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-spectrumconfig.html#cfn-groundstation-config-spectrumconfig-polarization
            '''
            result = self._values.get("polarization")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SpectrumConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnConfigPropsMixin.TrackingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"autotrack": "autotrack"},
    )
    class TrackingConfigProperty:
        def __init__(self, *, autotrack: typing.Optional[builtins.str] = None) -> None:
            '''Provides information about how AWS Ground Station should track the satellite through the sky during a contact.

            :param autotrack: Specifies whether or not to use autotrack. ``REMOVED`` specifies that program track should only be used during the contact. ``PREFERRED`` specifies that autotracking is preferred during the contact but fallback to program track if the signal is lost. ``REQUIRED`` specifies that autotracking is required during the contact and not to use program track if the signal is lost.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-trackingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                tracking_config_property = groundstation_mixins.CfnConfigPropsMixin.TrackingConfigProperty(
                    autotrack="autotrack"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5fffc4dd481f5fbef033a772dfc17c22c3792031fb22fb0d5ebfbc2db77ea2ae)
                check_type(argname="argument autotrack", value=autotrack, expected_type=type_hints["autotrack"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if autotrack is not None:
                self._values["autotrack"] = autotrack

        @builtins.property
        def autotrack(self) -> typing.Optional[builtins.str]:
            '''Specifies whether or not to use autotrack.

            ``REMOVED`` specifies that program track should only be used during the contact. ``PREFERRED`` specifies that autotracking is preferred during the contact but fallback to program track if the signal is lost. ``REQUIRED`` specifies that autotracking is required during the contact and not to use program track if the signal is lost.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-trackingconfig.html#cfn-groundstation-config-trackingconfig-autotrack
            '''
            result = self._values.get("autotrack")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TrackingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnConfigPropsMixin.UplinkEchoConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "antenna_uplink_config_arn": "antennaUplinkConfigArn",
            "enabled": "enabled",
        },
    )
    class UplinkEchoConfigProperty:
        def __init__(
            self,
            *,
            antenna_uplink_config_arn: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Provides information about how AWS Ground Station should echo back uplink transmissions to a dataflow endpoint.

            :param antenna_uplink_config_arn: Defines the ARN of the uplink config to echo back to a dataflow endpoint.
            :param enabled: Whether or not uplink echo is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-uplinkechoconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                uplink_echo_config_property = groundstation_mixins.CfnConfigPropsMixin.UplinkEchoConfigProperty(
                    antenna_uplink_config_arn="antennaUplinkConfigArn",
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d6557bc2a118661ae94297c89ccf18b3fbeee9bd93e9ee9994aa1f513cf93b9)
                check_type(argname="argument antenna_uplink_config_arn", value=antenna_uplink_config_arn, expected_type=type_hints["antenna_uplink_config_arn"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if antenna_uplink_config_arn is not None:
                self._values["antenna_uplink_config_arn"] = antenna_uplink_config_arn
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def antenna_uplink_config_arn(self) -> typing.Optional[builtins.str]:
            '''Defines the ARN of the uplink config to echo back to a dataflow endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-uplinkechoconfig.html#cfn-groundstation-config-uplinkechoconfig-antennauplinkconfigarn
            '''
            result = self._values.get("antenna_uplink_config_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether or not uplink echo is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-uplinkechoconfig.html#cfn-groundstation-config-uplinkechoconfig-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UplinkEchoConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnConfigPropsMixin.UplinkSpectrumConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "center_frequency": "centerFrequency",
            "polarization": "polarization",
        },
    )
    class UplinkSpectrumConfigProperty:
        def __init__(
            self,
            *,
            center_frequency: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigPropsMixin.FrequencyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            polarization: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines a uplink spectrum.

            :param center_frequency: The center frequency of the spectrum. Valid values are between 2200 to 2300 MHz and 7750 to 8400 MHz for downlink and 2025 to 2120 MHz for uplink.
            :param polarization: The polarization of the spectrum. Valid values are ``"RIGHT_HAND"`` and ``"LEFT_HAND"`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-uplinkspectrumconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                uplink_spectrum_config_property = groundstation_mixins.CfnConfigPropsMixin.UplinkSpectrumConfigProperty(
                    center_frequency=groundstation_mixins.CfnConfigPropsMixin.FrequencyProperty(
                        units="units",
                        value=123
                    ),
                    polarization="polarization"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__129fff0b1fa065e4dfbe23d610466fb0c4303fd6265d5dc7025fce00882450cd)
                check_type(argname="argument center_frequency", value=center_frequency, expected_type=type_hints["center_frequency"])
                check_type(argname="argument polarization", value=polarization, expected_type=type_hints["polarization"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if center_frequency is not None:
                self._values["center_frequency"] = center_frequency
            if polarization is not None:
                self._values["polarization"] = polarization

        @builtins.property
        def center_frequency(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.FrequencyProperty"]]:
            '''The center frequency of the spectrum.

            Valid values are between 2200 to 2300 MHz and 7750 to 8400 MHz for downlink and 2025 to 2120 MHz for uplink.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-uplinkspectrumconfig.html#cfn-groundstation-config-uplinkspectrumconfig-centerfrequency
            '''
            result = self._values.get("center_frequency")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigPropsMixin.FrequencyProperty"]], result)

        @builtins.property
        def polarization(self) -> typing.Optional[builtins.str]:
            '''The polarization of the spectrum.

            Valid values are ``"RIGHT_HAND"`` and ``"LEFT_HAND"`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-uplinkspectrumconfig.html#cfn-groundstation-config-uplinkspectrumconfig-polarization
            '''
            result = self._values.get("polarization")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UplinkSpectrumConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnDataflowEndpointGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "contact_post_pass_duration_seconds": "contactPostPassDurationSeconds",
        "contact_pre_pass_duration_seconds": "contactPrePassDurationSeconds",
        "endpoint_details": "endpointDetails",
        "tags": "tags",
    },
)
class CfnDataflowEndpointGroupMixinProps:
    def __init__(
        self,
        *,
        contact_post_pass_duration_seconds: typing.Optional[jsii.Number] = None,
        contact_pre_pass_duration_seconds: typing.Optional[jsii.Number] = None,
        endpoint_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataflowEndpointGroupPropsMixin.EndpointDetailsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDataflowEndpointGroupPropsMixin.

        :param contact_post_pass_duration_seconds: Amount of time, in seconds, after a contact ends that the Ground Station Dataflow Endpoint Group will be in a ``POSTPASS`` state. A Ground Station Dataflow Endpoint Group State Change event will be emitted when the Dataflow Endpoint Group enters and exits the ``POSTPASS`` state.
        :param contact_pre_pass_duration_seconds: Amount of time, in seconds, before a contact starts that the Ground Station Dataflow Endpoint Group will be in a ``PREPASS`` state. A Ground Station Dataflow Endpoint Group State Change event will be emitted when the Dataflow Endpoint Group enters and exits the ``PREPASS`` state.
        :param endpoint_details: List of Endpoint Details, containing address and port for each endpoint. All dataflow endpoints within a single dataflow endpoint group must be of the same type. You cannot mix AWS Ground Station Agent endpoints with Dataflow endpoints in the same group. If your use case requires both types of endpoints, you must create separate dataflow endpoint groups for each type.
        :param tags: Tags assigned to a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-dataflowendpointgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
            
            cfn_dataflow_endpoint_group_mixin_props = groundstation_mixins.CfnDataflowEndpointGroupMixinProps(
                contact_post_pass_duration_seconds=123,
                contact_pre_pass_duration_seconds=123,
                endpoint_details=[groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.EndpointDetailsProperty(
                    aws_ground_station_agent_endpoint=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.AwsGroundStationAgentEndpointProperty(
                        agent_status="agentStatus",
                        audit_results="auditResults",
                        egress_address=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.ConnectionDetailsProperty(
                            mtu=123,
                            socket_address=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.SocketAddressProperty(
                                name="name",
                                port=123
                            )
                        ),
                        ingress_address=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.RangedConnectionDetailsProperty(
                            mtu=123,
                            socket_address=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.RangedSocketAddressProperty(
                                name="name",
                                port_range=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.IntegerRangeProperty(
                                    maximum=123,
                                    minimum=123
                                )
                            )
                        ),
                        name="name"
                    ),
                    endpoint=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.DataflowEndpointProperty(
                        address=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.SocketAddressProperty(
                            name="name",
                            port=123
                        ),
                        mtu=123,
                        name="name"
                    ),
                    security_details=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.SecurityDetailsProperty(
                        role_arn="roleArn",
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ed4f97cfb19ee25b8d444feea789a5cab46c2805a7162066ee7293e3348ac4f)
            check_type(argname="argument contact_post_pass_duration_seconds", value=contact_post_pass_duration_seconds, expected_type=type_hints["contact_post_pass_duration_seconds"])
            check_type(argname="argument contact_pre_pass_duration_seconds", value=contact_pre_pass_duration_seconds, expected_type=type_hints["contact_pre_pass_duration_seconds"])
            check_type(argname="argument endpoint_details", value=endpoint_details, expected_type=type_hints["endpoint_details"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contact_post_pass_duration_seconds is not None:
            self._values["contact_post_pass_duration_seconds"] = contact_post_pass_duration_seconds
        if contact_pre_pass_duration_seconds is not None:
            self._values["contact_pre_pass_duration_seconds"] = contact_pre_pass_duration_seconds
        if endpoint_details is not None:
            self._values["endpoint_details"] = endpoint_details
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def contact_post_pass_duration_seconds(self) -> typing.Optional[jsii.Number]:
        '''Amount of time, in seconds, after a contact ends that the Ground Station Dataflow Endpoint Group will be in a ``POSTPASS`` state.

        A Ground Station Dataflow Endpoint Group State Change event will be emitted when the Dataflow Endpoint Group enters and exits the ``POSTPASS`` state.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-dataflowendpointgroup.html#cfn-groundstation-dataflowendpointgroup-contactpostpassdurationseconds
        '''
        result = self._values.get("contact_post_pass_duration_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def contact_pre_pass_duration_seconds(self) -> typing.Optional[jsii.Number]:
        '''Amount of time, in seconds, before a contact starts that the Ground Station Dataflow Endpoint Group will be in a ``PREPASS`` state.

        A Ground Station Dataflow Endpoint Group State Change event will be emitted when the Dataflow Endpoint Group enters and exits the ``PREPASS`` state.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-dataflowendpointgroup.html#cfn-groundstation-dataflowendpointgroup-contactprepassdurationseconds
        '''
        result = self._values.get("contact_pre_pass_duration_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def endpoint_details(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataflowEndpointGroupPropsMixin.EndpointDetailsProperty"]]]]:
        '''List of Endpoint Details, containing address and port for each endpoint.

        All dataflow endpoints within a single dataflow endpoint group must be of the same type. You cannot mix AWS Ground Station Agent endpoints with Dataflow endpoints in the same group. If your use case requires both types of endpoints, you must create separate dataflow endpoint groups for each type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-dataflowendpointgroup.html#cfn-groundstation-dataflowendpointgroup-endpointdetails
        '''
        result = self._values.get("endpoint_details")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataflowEndpointGroupPropsMixin.EndpointDetailsProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags assigned to a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-dataflowendpointgroup.html#cfn-groundstation-dataflowendpointgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataflowEndpointGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDataflowEndpointGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnDataflowEndpointGroupPropsMixin",
):
    '''Creates a Dataflow Endpoint Group request.

    Dataflow endpoint groups contain a list of endpoints. When the name of a dataflow endpoint group is specified in a mission profile, the Ground Station service will connect to the endpoints and flow data during a contact.

    For more information about dataflow endpoint groups, see `Dataflow Endpoint Groups <https://docs.aws.amazon.com/ground-station/latest/ug/dataflowendpointgroups.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-dataflowendpointgroup.html
    :cloudformationResource: AWS::GroundStation::DataflowEndpointGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
        
        cfn_dataflow_endpoint_group_props_mixin = groundstation_mixins.CfnDataflowEndpointGroupPropsMixin(groundstation_mixins.CfnDataflowEndpointGroupMixinProps(
            contact_post_pass_duration_seconds=123,
            contact_pre_pass_duration_seconds=123,
            endpoint_details=[groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.EndpointDetailsProperty(
                aws_ground_station_agent_endpoint=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.AwsGroundStationAgentEndpointProperty(
                    agent_status="agentStatus",
                    audit_results="auditResults",
                    egress_address=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.ConnectionDetailsProperty(
                        mtu=123,
                        socket_address=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.SocketAddressProperty(
                            name="name",
                            port=123
                        )
                    ),
                    ingress_address=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.RangedConnectionDetailsProperty(
                        mtu=123,
                        socket_address=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.RangedSocketAddressProperty(
                            name="name",
                            port_range=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.IntegerRangeProperty(
                                maximum=123,
                                minimum=123
                            )
                        )
                    ),
                    name="name"
                ),
                endpoint=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.DataflowEndpointProperty(
                    address=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.SocketAddressProperty(
                        name="name",
                        port=123
                    ),
                    mtu=123,
                    name="name"
                ),
                security_details=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.SecurityDetailsProperty(
                    role_arn="roleArn",
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
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
        props: typing.Union[CfnDataflowEndpointGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GroundStation::DataflowEndpointGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67773db5fcde5d9ad91e07c23947c90b35b569dc769964ada321ddf1f9b6162f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee85c0a90eda51b288ca0c1249313171901417d372f9405bf856928135da2b7b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__309b2ca9912f6af2c5a6ae0c92f1b249a54e143b3a8cb38e66b50a93e8c83a6b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDataflowEndpointGroupMixinProps:
        return typing.cast(CfnDataflowEndpointGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnDataflowEndpointGroupPropsMixin.AwsGroundStationAgentEndpointProperty",
        jsii_struct_bases=[],
        name_mapping={
            "agent_status": "agentStatus",
            "audit_results": "auditResults",
            "egress_address": "egressAddress",
            "ingress_address": "ingressAddress",
            "name": "name",
        },
    )
    class AwsGroundStationAgentEndpointProperty:
        def __init__(
            self,
            *,
            agent_status: typing.Optional[builtins.str] = None,
            audit_results: typing.Optional[builtins.str] = None,
            egress_address: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataflowEndpointGroupPropsMixin.ConnectionDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ingress_address: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataflowEndpointGroupPropsMixin.RangedConnectionDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about AwsGroundStationAgentEndpoint.

            :param agent_status: The status of AgentEndpoint.
            :param audit_results: The results of the audit.
            :param egress_address: The egress address of AgentEndpoint.
            :param ingress_address: The ingress address of AgentEndpoint.
            :param name: Name string associated with AgentEndpoint. Used as a human-readable identifier for AgentEndpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-awsgroundstationagentendpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                aws_ground_station_agent_endpoint_property = groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.AwsGroundStationAgentEndpointProperty(
                    agent_status="agentStatus",
                    audit_results="auditResults",
                    egress_address=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.ConnectionDetailsProperty(
                        mtu=123,
                        socket_address=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.SocketAddressProperty(
                            name="name",
                            port=123
                        )
                    ),
                    ingress_address=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.RangedConnectionDetailsProperty(
                        mtu=123,
                        socket_address=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.RangedSocketAddressProperty(
                            name="name",
                            port_range=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.IntegerRangeProperty(
                                maximum=123,
                                minimum=123
                            )
                        )
                    ),
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bc114c8c45de5822c870ef8985b645cc62f69d398cb589dbf7648e9042b1be16)
                check_type(argname="argument agent_status", value=agent_status, expected_type=type_hints["agent_status"])
                check_type(argname="argument audit_results", value=audit_results, expected_type=type_hints["audit_results"])
                check_type(argname="argument egress_address", value=egress_address, expected_type=type_hints["egress_address"])
                check_type(argname="argument ingress_address", value=ingress_address, expected_type=type_hints["ingress_address"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if agent_status is not None:
                self._values["agent_status"] = agent_status
            if audit_results is not None:
                self._values["audit_results"] = audit_results
            if egress_address is not None:
                self._values["egress_address"] = egress_address
            if ingress_address is not None:
                self._values["ingress_address"] = ingress_address
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def agent_status(self) -> typing.Optional[builtins.str]:
            '''The status of AgentEndpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-awsgroundstationagentendpoint.html#cfn-groundstation-dataflowendpointgroup-awsgroundstationagentendpoint-agentstatus
            '''
            result = self._values.get("agent_status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def audit_results(self) -> typing.Optional[builtins.str]:
            '''The results of the audit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-awsgroundstationagentendpoint.html#cfn-groundstation-dataflowendpointgroup-awsgroundstationagentendpoint-auditresults
            '''
            result = self._values.get("audit_results")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def egress_address(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataflowEndpointGroupPropsMixin.ConnectionDetailsProperty"]]:
            '''The egress address of AgentEndpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-awsgroundstationagentendpoint.html#cfn-groundstation-dataflowendpointgroup-awsgroundstationagentendpoint-egressaddress
            '''
            result = self._values.get("egress_address")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataflowEndpointGroupPropsMixin.ConnectionDetailsProperty"]], result)

        @builtins.property
        def ingress_address(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataflowEndpointGroupPropsMixin.RangedConnectionDetailsProperty"]]:
            '''The ingress address of AgentEndpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-awsgroundstationagentendpoint.html#cfn-groundstation-dataflowendpointgroup-awsgroundstationagentendpoint-ingressaddress
            '''
            result = self._values.get("ingress_address")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataflowEndpointGroupPropsMixin.RangedConnectionDetailsProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''Name string associated with AgentEndpoint.

            Used as a human-readable identifier for AgentEndpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-awsgroundstationagentendpoint.html#cfn-groundstation-dataflowendpointgroup-awsgroundstationagentendpoint-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AwsGroundStationAgentEndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnDataflowEndpointGroupPropsMixin.ConnectionDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"mtu": "mtu", "socket_address": "socketAddress"},
    )
    class ConnectionDetailsProperty:
        def __init__(
            self,
            *,
            mtu: typing.Optional[jsii.Number] = None,
            socket_address: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataflowEndpointGroupPropsMixin.SocketAddressProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Egress address of AgentEndpoint with an optional mtu.

            :param mtu: Maximum transmission unit (MTU) size in bytes of a dataflow endpoint.
            :param socket_address: A socket address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-connectiondetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                connection_details_property = groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.ConnectionDetailsProperty(
                    mtu=123,
                    socket_address=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.SocketAddressProperty(
                        name="name",
                        port=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__293e32423949346f09b921fe3c2ea972da5ccd18766a335aa0e606aeeee9b02e)
                check_type(argname="argument mtu", value=mtu, expected_type=type_hints["mtu"])
                check_type(argname="argument socket_address", value=socket_address, expected_type=type_hints["socket_address"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mtu is not None:
                self._values["mtu"] = mtu
            if socket_address is not None:
                self._values["socket_address"] = socket_address

        @builtins.property
        def mtu(self) -> typing.Optional[jsii.Number]:
            '''Maximum transmission unit (MTU) size in bytes of a dataflow endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-connectiondetails.html#cfn-groundstation-dataflowendpointgroup-connectiondetails-mtu
            '''
            result = self._values.get("mtu")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def socket_address(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataflowEndpointGroupPropsMixin.SocketAddressProperty"]]:
            '''A socket address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-connectiondetails.html#cfn-groundstation-dataflowendpointgroup-connectiondetails-socketaddress
            '''
            result = self._values.get("socket_address")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataflowEndpointGroupPropsMixin.SocketAddressProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectionDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnDataflowEndpointGroupPropsMixin.DataflowEndpointProperty",
        jsii_struct_bases=[],
        name_mapping={"address": "address", "mtu": "mtu", "name": "name"},
    )
    class DataflowEndpointProperty:
        def __init__(
            self,
            *,
            address: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataflowEndpointGroupPropsMixin.SocketAddressProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            mtu: typing.Optional[jsii.Number] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information such as socket address and name that defines an endpoint.

            :param address: The address and port of an endpoint.
            :param mtu: Maximum transmission unit (MTU) size in bytes of a dataflow endpoint. Valid values are between 1400 and 1500. A default value of 1500 is used if not set.
            :param name: The endpoint name. When listing available contacts for a satellite, Ground Station searches for a dataflow endpoint whose name matches the value specified by the dataflow endpoint config of the selected mission profile. If no matching dataflow endpoints are found then Ground Station will not display any available contacts for the satellite.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-dataflowendpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                dataflow_endpoint_property = groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.DataflowEndpointProperty(
                    address=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.SocketAddressProperty(
                        name="name",
                        port=123
                    ),
                    mtu=123,
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__545c1759bc6cfd2f52198da574ac0e09c268511b814b6fc3d50611a21a8347fe)
                check_type(argname="argument address", value=address, expected_type=type_hints["address"])
                check_type(argname="argument mtu", value=mtu, expected_type=type_hints["mtu"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address is not None:
                self._values["address"] = address
            if mtu is not None:
                self._values["mtu"] = mtu
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def address(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataflowEndpointGroupPropsMixin.SocketAddressProperty"]]:
            '''The address and port of an endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-dataflowendpoint.html#cfn-groundstation-dataflowendpointgroup-dataflowendpoint-address
            '''
            result = self._values.get("address")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataflowEndpointGroupPropsMixin.SocketAddressProperty"]], result)

        @builtins.property
        def mtu(self) -> typing.Optional[jsii.Number]:
            '''Maximum transmission unit (MTU) size in bytes of a dataflow endpoint.

            Valid values are between 1400 and 1500. A default value of 1500 is used if not set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-dataflowendpoint.html#cfn-groundstation-dataflowendpointgroup-dataflowendpoint-mtu
            '''
            result = self._values.get("mtu")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The endpoint name.

            When listing available contacts for a satellite, Ground Station searches for a dataflow endpoint whose name matches the value specified by the dataflow endpoint config of the selected mission profile. If no matching dataflow endpoints are found then Ground Station will not display any available contacts for the satellite.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-dataflowendpoint.html#cfn-groundstation-dataflowendpointgroup-dataflowendpoint-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataflowEndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnDataflowEndpointGroupPropsMixin.EndpointDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aws_ground_station_agent_endpoint": "awsGroundStationAgentEndpoint",
            "endpoint": "endpoint",
            "security_details": "securityDetails",
        },
    )
    class EndpointDetailsProperty:
        def __init__(
            self,
            *,
            aws_ground_station_agent_endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataflowEndpointGroupPropsMixin.AwsGroundStationAgentEndpointProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataflowEndpointGroupPropsMixin.DataflowEndpointProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            security_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataflowEndpointGroupPropsMixin.SecurityDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The security details and endpoint information.

            :param aws_ground_station_agent_endpoint: An agent endpoint.
            :param endpoint: Information about the endpoint such as name and the endpoint address.
            :param security_details: The role ARN, and IDs for security groups and subnets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-endpointdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                endpoint_details_property = groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.EndpointDetailsProperty(
                    aws_ground_station_agent_endpoint=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.AwsGroundStationAgentEndpointProperty(
                        agent_status="agentStatus",
                        audit_results="auditResults",
                        egress_address=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.ConnectionDetailsProperty(
                            mtu=123,
                            socket_address=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.SocketAddressProperty(
                                name="name",
                                port=123
                            )
                        ),
                        ingress_address=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.RangedConnectionDetailsProperty(
                            mtu=123,
                            socket_address=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.RangedSocketAddressProperty(
                                name="name",
                                port_range=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.IntegerRangeProperty(
                                    maximum=123,
                                    minimum=123
                                )
                            )
                        ),
                        name="name"
                    ),
                    endpoint=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.DataflowEndpointProperty(
                        address=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.SocketAddressProperty(
                            name="name",
                            port=123
                        ),
                        mtu=123,
                        name="name"
                    ),
                    security_details=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.SecurityDetailsProperty(
                        role_arn="roleArn",
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c9387d0d69eb5498e0a162e2d728c89e9e11694818fec1498c1ac04e0d1c733c)
                check_type(argname="argument aws_ground_station_agent_endpoint", value=aws_ground_station_agent_endpoint, expected_type=type_hints["aws_ground_station_agent_endpoint"])
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
                check_type(argname="argument security_details", value=security_details, expected_type=type_hints["security_details"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_ground_station_agent_endpoint is not None:
                self._values["aws_ground_station_agent_endpoint"] = aws_ground_station_agent_endpoint
            if endpoint is not None:
                self._values["endpoint"] = endpoint
            if security_details is not None:
                self._values["security_details"] = security_details

        @builtins.property
        def aws_ground_station_agent_endpoint(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataflowEndpointGroupPropsMixin.AwsGroundStationAgentEndpointProperty"]]:
            '''An agent endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-endpointdetails.html#cfn-groundstation-dataflowendpointgroup-endpointdetails-awsgroundstationagentendpoint
            '''
            result = self._values.get("aws_ground_station_agent_endpoint")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataflowEndpointGroupPropsMixin.AwsGroundStationAgentEndpointProperty"]], result)

        @builtins.property
        def endpoint(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataflowEndpointGroupPropsMixin.DataflowEndpointProperty"]]:
            '''Information about the endpoint such as name and the endpoint address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-endpointdetails.html#cfn-groundstation-dataflowendpointgroup-endpointdetails-endpoint
            '''
            result = self._values.get("endpoint")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataflowEndpointGroupPropsMixin.DataflowEndpointProperty"]], result)

        @builtins.property
        def security_details(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataflowEndpointGroupPropsMixin.SecurityDetailsProperty"]]:
            '''The role ARN, and IDs for security groups and subnets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-endpointdetails.html#cfn-groundstation-dataflowendpointgroup-endpointdetails-securitydetails
            '''
            result = self._values.get("security_details")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataflowEndpointGroupPropsMixin.SecurityDetailsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EndpointDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnDataflowEndpointGroupPropsMixin.IntegerRangeProperty",
        jsii_struct_bases=[],
        name_mapping={"maximum": "maximum", "minimum": "minimum"},
    )
    class IntegerRangeProperty:
        def __init__(
            self,
            *,
            maximum: typing.Optional[jsii.Number] = None,
            minimum: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An integer range that has a minimum and maximum value.

            :param maximum: A maximum value.
            :param minimum: A minimum value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-integerrange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                integer_range_property = groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.IntegerRangeProperty(
                    maximum=123,
                    minimum=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__79e1b0e5f6b797827a2aa84299410e0db57999a80af7f99eb9053a8e5d7e3ec9)
                check_type(argname="argument maximum", value=maximum, expected_type=type_hints["maximum"])
                check_type(argname="argument minimum", value=minimum, expected_type=type_hints["minimum"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if maximum is not None:
                self._values["maximum"] = maximum
            if minimum is not None:
                self._values["minimum"] = minimum

        @builtins.property
        def maximum(self) -> typing.Optional[jsii.Number]:
            '''A maximum value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-integerrange.html#cfn-groundstation-dataflowendpointgroup-integerrange-maximum
            '''
            result = self._values.get("maximum")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def minimum(self) -> typing.Optional[jsii.Number]:
            '''A minimum value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-integerrange.html#cfn-groundstation-dataflowendpointgroup-integerrange-minimum
            '''
            result = self._values.get("minimum")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntegerRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnDataflowEndpointGroupPropsMixin.RangedConnectionDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"mtu": "mtu", "socket_address": "socketAddress"},
    )
    class RangedConnectionDetailsProperty:
        def __init__(
            self,
            *,
            mtu: typing.Optional[jsii.Number] = None,
            socket_address: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataflowEndpointGroupPropsMixin.RangedSocketAddressProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Ingress address of AgentEndpoint with a port range and an optional mtu.

            :param mtu: Maximum transmission unit (MTU) size in bytes of a dataflow endpoint.
            :param socket_address: A ranged socket address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-rangedconnectiondetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                ranged_connection_details_property = groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.RangedConnectionDetailsProperty(
                    mtu=123,
                    socket_address=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.RangedSocketAddressProperty(
                        name="name",
                        port_range=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.IntegerRangeProperty(
                            maximum=123,
                            minimum=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__60147b8203a433358ee84afe4509d1760c0e0d3ef2114b76e49cc1b85f3576af)
                check_type(argname="argument mtu", value=mtu, expected_type=type_hints["mtu"])
                check_type(argname="argument socket_address", value=socket_address, expected_type=type_hints["socket_address"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mtu is not None:
                self._values["mtu"] = mtu
            if socket_address is not None:
                self._values["socket_address"] = socket_address

        @builtins.property
        def mtu(self) -> typing.Optional[jsii.Number]:
            '''Maximum transmission unit (MTU) size in bytes of a dataflow endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-rangedconnectiondetails.html#cfn-groundstation-dataflowendpointgroup-rangedconnectiondetails-mtu
            '''
            result = self._values.get("mtu")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def socket_address(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataflowEndpointGroupPropsMixin.RangedSocketAddressProperty"]]:
            '''A ranged socket address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-rangedconnectiondetails.html#cfn-groundstation-dataflowendpointgroup-rangedconnectiondetails-socketaddress
            '''
            result = self._values.get("socket_address")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataflowEndpointGroupPropsMixin.RangedSocketAddressProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RangedConnectionDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnDataflowEndpointGroupPropsMixin.RangedSocketAddressProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "port_range": "portRange"},
    )
    class RangedSocketAddressProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            port_range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataflowEndpointGroupPropsMixin.IntegerRangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A socket address with a port range.

            :param name: IPv4 socket address.
            :param port_range: Port range of a socket address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-rangedsocketaddress.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                ranged_socket_address_property = groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.RangedSocketAddressProperty(
                    name="name",
                    port_range=groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.IntegerRangeProperty(
                        maximum=123,
                        minimum=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2a1ca769c108aba98617cd5558ce6ec61a616d329ea157c1d35d7b6968ab0c88)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument port_range", value=port_range, expected_type=type_hints["port_range"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if port_range is not None:
                self._values["port_range"] = port_range

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''IPv4 socket address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-rangedsocketaddress.html#cfn-groundstation-dataflowendpointgroup-rangedsocketaddress-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port_range(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataflowEndpointGroupPropsMixin.IntegerRangeProperty"]]:
            '''Port range of a socket address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-rangedsocketaddress.html#cfn-groundstation-dataflowendpointgroup-rangedsocketaddress-portrange
            '''
            result = self._values.get("port_range")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataflowEndpointGroupPropsMixin.IntegerRangeProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RangedSocketAddressProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnDataflowEndpointGroupPropsMixin.SecurityDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "role_arn": "roleArn",
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class SecurityDetailsProperty:
        def __init__(
            self,
            *,
            role_arn: typing.Optional[builtins.str] = None,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Information about IAM roles, subnets, and security groups needed for this DataflowEndpointGroup.

            :param role_arn: The ARN of a role which Ground Station has permission to assume, such as ``arn:aws:iam::1234567890:role/DataDeliveryServiceRole`` . Ground Station will assume this role and create an ENI in your VPC on the specified subnet upon creation of a dataflow endpoint group. This ENI is used as the ingress/egress point for data streamed during a satellite contact.
            :param security_group_ids: The security group Ids of the security role, such as ``sg-1234567890abcdef0`` .
            :param subnet_ids: The subnet Ids of the security details, such as ``subnet-12345678`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-securitydetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                security_details_property = groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.SecurityDetailsProperty(
                    role_arn="roleArn",
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d9bbdafcf423374c7112f7c1d0639deaf931721643e4d5c6b72ddb2826599767)
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of a role which Ground Station has permission to assume, such as ``arn:aws:iam::1234567890:role/DataDeliveryServiceRole`` .

            Ground Station will assume this role and create an ENI in your VPC on the specified subnet upon creation of a dataflow endpoint group. This ENI is used as the ingress/egress point for data streamed during a satellite contact.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-securitydetails.html#cfn-groundstation-dataflowendpointgroup-securitydetails-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The security group Ids of the security role, such as ``sg-1234567890abcdef0`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-securitydetails.html#cfn-groundstation-dataflowendpointgroup-securitydetails-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The subnet Ids of the security details, such as ``subnet-12345678`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-securitydetails.html#cfn-groundstation-dataflowendpointgroup-securitydetails-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecurityDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnDataflowEndpointGroupPropsMixin.SocketAddressProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "port": "port"},
    )
    class SocketAddressProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The address of the endpoint, such as ``192.168.1.1`` .

            :param name: The name of the endpoint, such as ``Endpoint 1`` .
            :param port: The port of the endpoint, such as ``55888`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-socketaddress.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                socket_address_property = groundstation_mixins.CfnDataflowEndpointGroupPropsMixin.SocketAddressProperty(
                    name="name",
                    port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4c6da644bcffbbb024cdaf77b55978cd80593ca17689e529f6ce2d74ff2f8fa0)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if port is not None:
                self._values["port"] = port

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the endpoint, such as ``Endpoint 1`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-socketaddress.html#cfn-groundstation-dataflowendpointgroup-socketaddress-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port of the endpoint, such as ``55888`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-socketaddress.html#cfn-groundstation-dataflowendpointgroup-socketaddress-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SocketAddressProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnMissionProfileMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "contact_post_pass_duration_seconds": "contactPostPassDurationSeconds",
        "contact_pre_pass_duration_seconds": "contactPrePassDurationSeconds",
        "dataflow_edges": "dataflowEdges",
        "minimum_viable_contact_duration_seconds": "minimumViableContactDurationSeconds",
        "name": "name",
        "streams_kms_key": "streamsKmsKey",
        "streams_kms_role": "streamsKmsRole",
        "tags": "tags",
        "tracking_config_arn": "trackingConfigArn",
    },
)
class CfnMissionProfileMixinProps:
    def __init__(
        self,
        *,
        contact_post_pass_duration_seconds: typing.Optional[jsii.Number] = None,
        contact_pre_pass_duration_seconds: typing.Optional[jsii.Number] = None,
        dataflow_edges: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMissionProfilePropsMixin.DataflowEdgeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        minimum_viable_contact_duration_seconds: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        streams_kms_key: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMissionProfilePropsMixin.StreamsKmsKeyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        streams_kms_role: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        tracking_config_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnMissionProfilePropsMixin.

        :param contact_post_pass_duration_seconds: Amount of time in seconds after a contact ends that you’d like to receive a Ground Station Contact State Change indicating the pass has finished.
        :param contact_pre_pass_duration_seconds: Amount of time in seconds prior to contact start that you'd like to receive a Ground Station Contact State Change Event indicating an upcoming pass.
        :param dataflow_edges: A list containing lists of config ARNs. Each list of config ARNs is an edge, with a "from" config and a "to" config.
        :param minimum_viable_contact_duration_seconds: Minimum length of a contact in seconds that Ground Station will return when listing contacts. Ground Station will not return contacts shorter than this duration.
        :param name: The name of the mission profile.
        :param streams_kms_key: KMS key to use for encrypting streams.
        :param streams_kms_role: Role to use for encrypting streams with KMS key.
        :param tags: Tags assigned to the mission profile.
        :param tracking_config_arn: The ARN of a tracking config objects that defines how to track the satellite through the sky during a contact.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
            
            cfn_mission_profile_mixin_props = groundstation_mixins.CfnMissionProfileMixinProps(
                contact_post_pass_duration_seconds=123,
                contact_pre_pass_duration_seconds=123,
                dataflow_edges=[groundstation_mixins.CfnMissionProfilePropsMixin.DataflowEdgeProperty(
                    destination="destination",
                    source="source"
                )],
                minimum_viable_contact_duration_seconds=123,
                name="name",
                streams_kms_key=groundstation_mixins.CfnMissionProfilePropsMixin.StreamsKmsKeyProperty(
                    kms_alias_arn="kmsAliasArn",
                    kms_alias_name="kmsAliasName",
                    kms_key_arn="kmsKeyArn"
                ),
                streams_kms_role="streamsKmsRole",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                tracking_config_arn="trackingConfigArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f49943bc9143c021840e419025f299afec7c9537466a130d24db13576907065)
            check_type(argname="argument contact_post_pass_duration_seconds", value=contact_post_pass_duration_seconds, expected_type=type_hints["contact_post_pass_duration_seconds"])
            check_type(argname="argument contact_pre_pass_duration_seconds", value=contact_pre_pass_duration_seconds, expected_type=type_hints["contact_pre_pass_duration_seconds"])
            check_type(argname="argument dataflow_edges", value=dataflow_edges, expected_type=type_hints["dataflow_edges"])
            check_type(argname="argument minimum_viable_contact_duration_seconds", value=minimum_viable_contact_duration_seconds, expected_type=type_hints["minimum_viable_contact_duration_seconds"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument streams_kms_key", value=streams_kms_key, expected_type=type_hints["streams_kms_key"])
            check_type(argname="argument streams_kms_role", value=streams_kms_role, expected_type=type_hints["streams_kms_role"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tracking_config_arn", value=tracking_config_arn, expected_type=type_hints["tracking_config_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contact_post_pass_duration_seconds is not None:
            self._values["contact_post_pass_duration_seconds"] = contact_post_pass_duration_seconds
        if contact_pre_pass_duration_seconds is not None:
            self._values["contact_pre_pass_duration_seconds"] = contact_pre_pass_duration_seconds
        if dataflow_edges is not None:
            self._values["dataflow_edges"] = dataflow_edges
        if minimum_viable_contact_duration_seconds is not None:
            self._values["minimum_viable_contact_duration_seconds"] = minimum_viable_contact_duration_seconds
        if name is not None:
            self._values["name"] = name
        if streams_kms_key is not None:
            self._values["streams_kms_key"] = streams_kms_key
        if streams_kms_role is not None:
            self._values["streams_kms_role"] = streams_kms_role
        if tags is not None:
            self._values["tags"] = tags
        if tracking_config_arn is not None:
            self._values["tracking_config_arn"] = tracking_config_arn

    @builtins.property
    def contact_post_pass_duration_seconds(self) -> typing.Optional[jsii.Number]:
        '''Amount of time in seconds after a contact ends that you’d like to receive a Ground Station Contact State Change indicating the pass has finished.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html#cfn-groundstation-missionprofile-contactpostpassdurationseconds
        '''
        result = self._values.get("contact_post_pass_duration_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def contact_pre_pass_duration_seconds(self) -> typing.Optional[jsii.Number]:
        '''Amount of time in seconds prior to contact start that you'd like to receive a Ground Station Contact State Change Event indicating an upcoming pass.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html#cfn-groundstation-missionprofile-contactprepassdurationseconds
        '''
        result = self._values.get("contact_pre_pass_duration_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dataflow_edges(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMissionProfilePropsMixin.DataflowEdgeProperty"]]]]:
        '''A list containing lists of config ARNs.

        Each list of config ARNs is an edge, with a "from" config and a "to" config.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html#cfn-groundstation-missionprofile-dataflowedges
        '''
        result = self._values.get("dataflow_edges")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMissionProfilePropsMixin.DataflowEdgeProperty"]]]], result)

    @builtins.property
    def minimum_viable_contact_duration_seconds(self) -> typing.Optional[jsii.Number]:
        '''Minimum length of a contact in seconds that Ground Station will return when listing contacts.

        Ground Station will not return contacts shorter than this duration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html#cfn-groundstation-missionprofile-minimumviablecontactdurationseconds
        '''
        result = self._values.get("minimum_viable_contact_duration_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the mission profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html#cfn-groundstation-missionprofile-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def streams_kms_key(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMissionProfilePropsMixin.StreamsKmsKeyProperty"]]:
        '''KMS key to use for encrypting streams.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html#cfn-groundstation-missionprofile-streamskmskey
        '''
        result = self._values.get("streams_kms_key")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMissionProfilePropsMixin.StreamsKmsKeyProperty"]], result)

    @builtins.property
    def streams_kms_role(self) -> typing.Optional[builtins.str]:
        '''Role to use for encrypting streams with KMS key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html#cfn-groundstation-missionprofile-streamskmsrole
        '''
        result = self._values.get("streams_kms_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags assigned to the mission profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html#cfn-groundstation-missionprofile-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def tracking_config_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of a tracking config objects that defines how to track the satellite through the sky during a contact.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html#cfn-groundstation-missionprofile-trackingconfigarn
        '''
        result = self._values.get("tracking_config_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMissionProfileMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMissionProfilePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnMissionProfilePropsMixin",
):
    '''Mission profiles specify parameters and provide references to config objects to define how Ground Station lists and executes contacts.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html
    :cloudformationResource: AWS::GroundStation::MissionProfile
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
        
        cfn_mission_profile_props_mixin = groundstation_mixins.CfnMissionProfilePropsMixin(groundstation_mixins.CfnMissionProfileMixinProps(
            contact_post_pass_duration_seconds=123,
            contact_pre_pass_duration_seconds=123,
            dataflow_edges=[groundstation_mixins.CfnMissionProfilePropsMixin.DataflowEdgeProperty(
                destination="destination",
                source="source"
            )],
            minimum_viable_contact_duration_seconds=123,
            name="name",
            streams_kms_key=groundstation_mixins.CfnMissionProfilePropsMixin.StreamsKmsKeyProperty(
                kms_alias_arn="kmsAliasArn",
                kms_alias_name="kmsAliasName",
                kms_key_arn="kmsKeyArn"
            ),
            streams_kms_role="streamsKmsRole",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            tracking_config_arn="trackingConfigArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMissionProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GroundStation::MissionProfile``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f17c5599d6c2ae35f3d12ff68fbc233028e435f1a22888292162dbec6444de02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__141f22db8c7241856d1ab87d99f4ee9da9cc0532da0033af30c1ef5de682a9c1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__029927d6c371c941f97f7c88ffa115ca1e7d997cf3eb74112ce8f90a66c348ba)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMissionProfileMixinProps:
        return typing.cast(CfnMissionProfileMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnMissionProfilePropsMixin.DataflowEdgeProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination", "source": "source"},
    )
    class DataflowEdgeProperty:
        def __init__(
            self,
            *,
            destination: typing.Optional[builtins.str] = None,
            source: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A dataflow edge defines from where and to where data will flow during a contact.

            :param destination: The ARN of the destination for this dataflow edge. For example, specify the ARN of a dataflow endpoint config for a downlink edge or an antenna uplink config for an uplink edge.
            :param source: The ARN of the source for this dataflow edge. For example, specify the ARN of an antenna downlink config for a downlink edge or a dataflow endpoint config for an uplink edge.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-missionprofile-dataflowedge.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                dataflow_edge_property = groundstation_mixins.CfnMissionProfilePropsMixin.DataflowEdgeProperty(
                    destination="destination",
                    source="source"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7bc4a576b3e2849ceede3cd33aebaf262564e3e3dc91adc28edfb576689d2bd3)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination is not None:
                self._values["destination"] = destination
            if source is not None:
                self._values["source"] = source

        @builtins.property
        def destination(self) -> typing.Optional[builtins.str]:
            '''The ARN of the destination for this dataflow edge.

            For example, specify the ARN of a dataflow endpoint config for a downlink edge or an antenna uplink config for an uplink edge.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-missionprofile-dataflowedge.html#cfn-groundstation-missionprofile-dataflowedge-destination
            '''
            result = self._values.get("destination")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''The ARN of the source for this dataflow edge.

            For example, specify the ARN of an antenna downlink config for a downlink edge or a dataflow endpoint config for an uplink edge.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-missionprofile-dataflowedge.html#cfn-groundstation-missionprofile-dataflowedge-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataflowEdgeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_groundstation.mixins.CfnMissionProfilePropsMixin.StreamsKmsKeyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kms_alias_arn": "kmsAliasArn",
            "kms_alias_name": "kmsAliasName",
            "kms_key_arn": "kmsKeyArn",
        },
    )
    class StreamsKmsKeyProperty:
        def __init__(
            self,
            *,
            kms_alias_arn: typing.Optional[builtins.str] = None,
            kms_alias_name: typing.Optional[builtins.str] = None,
            kms_key_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''KMS key info.

            :param kms_alias_arn: KMS Alias Arn.
            :param kms_alias_name: KMS Alias Name.
            :param kms_key_arn: KMS Key Arn.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-missionprofile-streamskmskey.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_groundstation import mixins as groundstation_mixins
                
                streams_kms_key_property = groundstation_mixins.CfnMissionProfilePropsMixin.StreamsKmsKeyProperty(
                    kms_alias_arn="kmsAliasArn",
                    kms_alias_name="kmsAliasName",
                    kms_key_arn="kmsKeyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3a02b5622ceb099837fd7cdd3e628f9d45b4b751838614b3f8fdde7ed5b5ae70)
                check_type(argname="argument kms_alias_arn", value=kms_alias_arn, expected_type=type_hints["kms_alias_arn"])
                check_type(argname="argument kms_alias_name", value=kms_alias_name, expected_type=type_hints["kms_alias_name"])
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_alias_arn is not None:
                self._values["kms_alias_arn"] = kms_alias_arn
            if kms_alias_name is not None:
                self._values["kms_alias_name"] = kms_alias_name
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn

        @builtins.property
        def kms_alias_arn(self) -> typing.Optional[builtins.str]:
            '''KMS Alias Arn.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-missionprofile-streamskmskey.html#cfn-groundstation-missionprofile-streamskmskey-kmsaliasarn
            '''
            result = self._values.get("kms_alias_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_alias_name(self) -> typing.Optional[builtins.str]:
            '''KMS Alias Name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-missionprofile-streamskmskey.html#cfn-groundstation-missionprofile-streamskmskey-kmsaliasname
            '''
            result = self._values.get("kms_alias_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''KMS Key Arn.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-missionprofile-streamskmskey.html#cfn-groundstation-missionprofile-streamskmskey-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamsKmsKeyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnConfigMixinProps",
    "CfnConfigPropsMixin",
    "CfnDataflowEndpointGroupMixinProps",
    "CfnDataflowEndpointGroupPropsMixin",
    "CfnMissionProfileMixinProps",
    "CfnMissionProfilePropsMixin",
]

publication.publish()

def _typecheckingstub__958095e85b501a929d8f9f7463d01c55c3e0a6b8ae67ce5fa47da28e34b30f7f(
    *,
    config_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigPropsMixin.ConfigDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa073db2c0f09d28062420244118cbbe67e5b0fd47b852dce0c2356c0597cb06(
    props: typing.Union[CfnConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cd4f68f8f36713d422343e12aa4b29362017f70ff8a9566c4ec40e6fef75218(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9379f1df3478235c060bf355876c237138178f9f33970626dd77c8272eb0f1d8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94b1b82935a35d8f0a63b8c2c814df3a8ec47756089f01a1b261a40336c3a528(
    *,
    spectrum_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigPropsMixin.SpectrumConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ede83788e32643d28c05693a18a965383579cf6cb19f6d2bd4bb569a0b7824c5(
    *,
    decode_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigPropsMixin.DecodeConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    demodulation_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigPropsMixin.DemodulationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    spectrum_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigPropsMixin.SpectrumConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce32518684c906d888c70f297daeb18887baaee045f86e58112f242357395fc(
    *,
    spectrum_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigPropsMixin.UplinkSpectrumConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_eirp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigPropsMixin.EirpProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    transmit_disabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e47f37ef91eff42eac677894acf6d61a3c014d5f11d939f9ef530221931fea(
    *,
    antenna_downlink_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigPropsMixin.AntennaDownlinkConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    antenna_downlink_demod_decode_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigPropsMixin.AntennaDownlinkDemodDecodeConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    antenna_uplink_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigPropsMixin.AntennaUplinkConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dataflow_endpoint_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigPropsMixin.DataflowEndpointConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_recording_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigPropsMixin.S3RecordingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tracking_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigPropsMixin.TrackingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    uplink_echo_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigPropsMixin.UplinkEchoConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__764028d11eb082731531e574fd61a4311641440727a9faa894b83e6c722340fc(
    *,
    dataflow_endpoint_name: typing.Optional[builtins.str] = None,
    dataflow_endpoint_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7b9b73405654832011b38fa56e84f9b02e74683270d115c7a325a41d9d9cb78(
    *,
    unvalidated_json: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cf07ac45cf974bb1910f94d6aa2e9004b32df61d39904040e49e2cc19e49a84(
    *,
    unvalidated_json: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f811a579ec38f034616146157535a01673a8944bdd67a006e47053c297de99(
    *,
    units: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de0f30942253e1ac58c2efebe6ad5f74fe40df4f6bfa3da07a921e13157a956e(
    *,
    units: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6344f217297cca12876d99b4ac4750162fcedb48919bae0b9cc971cada4babb(
    *,
    units: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb2e8a7e8590c47b9013bd4dd3e2525fef7f510594b0ef1a9aba1fab06d02b1(
    *,
    bucket_arn: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e44e98abc58c653f4e1df8f66e85c3a32763bd11297721dcc63236192c6a4572(
    *,
    bandwidth: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigPropsMixin.FrequencyBandwidthProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    center_frequency: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigPropsMixin.FrequencyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    polarization: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fffc4dd481f5fbef033a772dfc17c22c3792031fb22fb0d5ebfbc2db77ea2ae(
    *,
    autotrack: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d6557bc2a118661ae94297c89ccf18b3fbeee9bd93e9ee9994aa1f513cf93b9(
    *,
    antenna_uplink_config_arn: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__129fff0b1fa065e4dfbe23d610466fb0c4303fd6265d5dc7025fce00882450cd(
    *,
    center_frequency: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigPropsMixin.FrequencyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    polarization: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ed4f97cfb19ee25b8d444feea789a5cab46c2805a7162066ee7293e3348ac4f(
    *,
    contact_post_pass_duration_seconds: typing.Optional[jsii.Number] = None,
    contact_pre_pass_duration_seconds: typing.Optional[jsii.Number] = None,
    endpoint_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataflowEndpointGroupPropsMixin.EndpointDetailsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67773db5fcde5d9ad91e07c23947c90b35b569dc769964ada321ddf1f9b6162f(
    props: typing.Union[CfnDataflowEndpointGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee85c0a90eda51b288ca0c1249313171901417d372f9405bf856928135da2b7b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__309b2ca9912f6af2c5a6ae0c92f1b249a54e143b3a8cb38e66b50a93e8c83a6b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc114c8c45de5822c870ef8985b645cc62f69d398cb589dbf7648e9042b1be16(
    *,
    agent_status: typing.Optional[builtins.str] = None,
    audit_results: typing.Optional[builtins.str] = None,
    egress_address: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataflowEndpointGroupPropsMixin.ConnectionDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ingress_address: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataflowEndpointGroupPropsMixin.RangedConnectionDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__293e32423949346f09b921fe3c2ea972da5ccd18766a335aa0e606aeeee9b02e(
    *,
    mtu: typing.Optional[jsii.Number] = None,
    socket_address: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataflowEndpointGroupPropsMixin.SocketAddressProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__545c1759bc6cfd2f52198da574ac0e09c268511b814b6fc3d50611a21a8347fe(
    *,
    address: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataflowEndpointGroupPropsMixin.SocketAddressProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mtu: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9387d0d69eb5498e0a162e2d728c89e9e11694818fec1498c1ac04e0d1c733c(
    *,
    aws_ground_station_agent_endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataflowEndpointGroupPropsMixin.AwsGroundStationAgentEndpointProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataflowEndpointGroupPropsMixin.DataflowEndpointProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    security_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataflowEndpointGroupPropsMixin.SecurityDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e1b0e5f6b797827a2aa84299410e0db57999a80af7f99eb9053a8e5d7e3ec9(
    *,
    maximum: typing.Optional[jsii.Number] = None,
    minimum: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60147b8203a433358ee84afe4509d1760c0e0d3ef2114b76e49cc1b85f3576af(
    *,
    mtu: typing.Optional[jsii.Number] = None,
    socket_address: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataflowEndpointGroupPropsMixin.RangedSocketAddressProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a1ca769c108aba98617cd5558ce6ec61a616d329ea157c1d35d7b6968ab0c88(
    *,
    name: typing.Optional[builtins.str] = None,
    port_range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataflowEndpointGroupPropsMixin.IntegerRangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9bbdafcf423374c7112f7c1d0639deaf931721643e4d5c6b72ddb2826599767(
    *,
    role_arn: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c6da644bcffbbb024cdaf77b55978cd80593ca17689e529f6ce2d74ff2f8fa0(
    *,
    name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f49943bc9143c021840e419025f299afec7c9537466a130d24db13576907065(
    *,
    contact_post_pass_duration_seconds: typing.Optional[jsii.Number] = None,
    contact_pre_pass_duration_seconds: typing.Optional[jsii.Number] = None,
    dataflow_edges: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMissionProfilePropsMixin.DataflowEdgeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    minimum_viable_contact_duration_seconds: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    streams_kms_key: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMissionProfilePropsMixin.StreamsKmsKeyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    streams_kms_role: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    tracking_config_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f17c5599d6c2ae35f3d12ff68fbc233028e435f1a22888292162dbec6444de02(
    props: typing.Union[CfnMissionProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__141f22db8c7241856d1ab87d99f4ee9da9cc0532da0033af30c1ef5de682a9c1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029927d6c371c941f97f7c88ffa115ca1e7d997cf3eb74112ce8f90a66c348ba(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc4a576b3e2849ceede3cd33aebaf262564e3e3dc91adc28edfb576689d2bd3(
    *,
    destination: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a02b5622ceb099837fd7cdd3e628f9d45b4b751838614b3f8fdde7ed5b5ae70(
    *,
    kms_alias_arn: typing.Optional[builtins.str] = None,
    kms_alias_name: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
